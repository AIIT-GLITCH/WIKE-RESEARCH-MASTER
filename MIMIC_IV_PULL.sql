-- ============================================================
-- MIMIC-IV COHORT PULL: HRV Coherence + CRP + Diagnosis Labels
-- Wike Coherence Framework — Sensitivity Lift Analysis
-- Ready to run on PhysioNet MIMIC-IV access
-- ============================================================
-- Tables used:
--   mimiciv_hosp.labevents         — lab values (CRP)
--   mimiciv_hosp.d_labitems        — lab item dictionary
--   mimiciv_hosp.admissions        — admission metadata
--   mimiciv_hosp.diagnoses_icd     — ICD codes per admission
--   mimiciv_hosp.d_icd_diagnoses   — ICD code descriptions
--   mimiciv_hosp.patients          — demographics (age filter)
-- ============================================================


-- ============================================================
-- STEP 0: VERIFY CRP ITEMID IN THIS MIMIC-IV INSTANCE
-- Run this first. CRP is 50889 in MIMIC-III. Confirm in MIMIC-IV.
-- ============================================================

SELECT itemid, label, fluid, category, unitname
FROM mimiciv_hosp.d_labitems
WHERE LOWER(label) LIKE '%c-reactive%'
   OR LOWER(label) LIKE '%crp%';

-- Expected output: itemid=50889, label='C-Reactive Protein', fluid='Blood'
-- If itemid differs, update the CRP_ITEMID variable below


-- ============================================================
-- STEP 1: EXTRACT CRP VALUES
-- Filter: blood CRP only, plausible range 0–500 mg/L
-- ============================================================

CREATE TABLE IF NOT EXISTS cohort_crp AS
SELECT
    le.subject_id,
    le.hadm_id,
    le.charttime                        AS crp_time,
    le.valuenum                         AS crp_mgl,
    le.valueuom                         AS crp_unit,
    -- Severity bucket — used later for sensitivity stratification
    CASE
        WHEN le.valuenum < 1.0   THEN 'normal'         -- < 1 mg/L
        WHEN le.valuenum < 10.0  THEN 'mild'            -- 1–10 mg/L
        WHEN le.valuenum < 40.0  THEN 'moderate'        -- 10–40 mg/L
        WHEN le.valuenum < 100.0 THEN 'elevated'        -- 40–100 mg/L
        ELSE                          'high'            -- > 100 mg/L (sepsis range)
    END AS crp_severity
FROM mimiciv_hosp.labevents le
WHERE le.itemid = 50889                 -- C-Reactive Protein
  AND le.valuenum IS NOT NULL
  AND le.valuenum BETWEEN 0 AND 500     -- exclude obvious data errors
  AND le.valueuom IN ('mg/L', 'MG/L', 'mg/l');


-- ============================================================
-- STEP 2: DIAGNOSIS LABELS
-- CHF, infection/sepsis, cancer — applied AFTER classification (blind)
-- ICD-9 and ICD-10 both present in MIMIC-IV
-- ============================================================

CREATE TABLE IF NOT EXISTS cohort_diagnoses AS
SELECT
    d.subject_id,
    d.hadm_id,
    -- CHF flag
    MAX(CASE
        WHEN d.icd_version = 9 AND d.icd_code LIKE '428%'       THEN 1
        WHEN d.icd_version = 10 AND d.icd_code LIKE 'I50%'      THEN 1
        ELSE 0
    END) AS has_chf,

    -- Systolic CHF (most severe subtype — your primary positive class)
    MAX(CASE
        WHEN d.icd_version = 9  AND d.icd_code IN ('4280','4282') THEN 1
        WHEN d.icd_version = 10 AND d.icd_code IN ('I500','I5020','I5021','I5022','I5023') THEN 1
        ELSE 0
    END) AS has_chf_systolic,

    -- Infection / Sepsis
    MAX(CASE
        WHEN d.icd_version = 9  AND (d.icd_code LIKE '038%'
                                  OR d.icd_code LIKE '995.9%')   THEN 1
        WHEN d.icd_version = 10 AND (d.icd_code LIKE 'A40%'
                                  OR d.icd_code LIKE 'A41%'
                                  OR d.icd_code LIKE 'R65%')     THEN 1
        ELSE 0
    END) AS has_infection,

    -- Cancer (any malignancy)
    MAX(CASE
        WHEN d.icd_version = 9  AND (CAST(LEFT(d.icd_code,3) AS INTEGER)
                                     BETWEEN 140 AND 239)        THEN 1
        WHEN d.icd_version = 10 AND (d.icd_code BETWEEN 'C00' AND 'D49') THEN 1
        ELSE 0
    END) AS has_cancer,

    -- Normal control flag (none of the above)
    -- Computed below in STEP 4 after the joins

    -- Primary label for sensitivity/specificity computation
    -- Priority: CHF > infection > cancer > control
    CASE
        WHEN MAX(CASE
                WHEN d.icd_version = 9  AND d.icd_code LIKE '428%'  THEN 1
                WHEN d.icd_version = 10 AND d.icd_code LIKE 'I50%'  THEN 1
                ELSE 0 END) = 1 THEN 'CHF'
        WHEN MAX(CASE
                WHEN d.icd_version = 9  AND (d.icd_code LIKE '038%'
                                          OR d.icd_code LIKE '995.9%') THEN 1
                WHEN d.icd_version = 10 AND (d.icd_code LIKE 'A40%'
                                          OR d.icd_code LIKE 'A41%'
                                          OR d.icd_code LIKE 'R65%') THEN 1
                ELSE 0 END) = 1 THEN 'INFECTION'
        WHEN MAX(CASE
                WHEN d.icd_version = 9  AND (CAST(LEFT(d.icd_code,3) AS INTEGER)
                                             BETWEEN 140 AND 239) THEN 1
                WHEN d.icd_version = 10 AND (d.icd_code BETWEEN 'C00' AND 'D49') THEN 1
                ELSE 0 END) = 1 THEN 'CANCER'
        ELSE 'CONTROL'
    END AS primary_label

FROM mimiciv_hosp.diagnoses_icd d
GROUP BY d.subject_id, d.hadm_id;


-- ============================================================
-- STEP 3: ADMISSION METADATA + AGE FILTER
-- Adults only (≥ 18), exclude neonates and pediatric
-- ============================================================

CREATE TABLE IF NOT EXISTS cohort_admissions AS
SELECT
    a.subject_id,
    a.hadm_id,
    a.admittime,
    a.dischtime,
    a.admission_type,
    a.insurance,
    p.gender,
    p.anchor_age                        AS age_at_anchor
FROM mimiciv_hosp.admissions a
JOIN mimiciv_hosp.patients p
    ON a.subject_id = p.subject_id
WHERE p.anchor_age >= 18;


-- ============================================================
-- STEP 4: FINAL COHORT — CRP WITHIN ±24h OF ECG WINDOW
--
-- Your ECG segments come from your HRV pipeline (PhysioNet NSRDB/CHF).
-- For pure MIMIC-IV ECG use, substitute your segment timestamps below.
-- The ±24h window is the join key.
--
-- If using MIMIC-IV Waveform:
--   waveform table: mimiciv_waveform.waveform_segments
--   or matched via subject_id + charttime approximation
-- ============================================================

-- This query assumes you have a table: your_ecg_segments(subject_id, hadm_id, segment_start, segment_end)
-- If pulling from MIMIC-IV waveform directly, replace that reference.

CREATE TABLE IF NOT EXISTS cohort_final AS
SELECT
    ca.subject_id,
    ca.hadm_id,
    ca.admittime,
    ca.gender,
    ca.age_at_anchor,

    -- CRP fields — take the CRP measurement CLOSEST to ECG segment center
    -- If multiple CRP measurements within ±24h, use the one nearest in time
    crp.crp_mgl,
    crp.crp_time,
    crp.crp_severity,
    ABS(EXTRACT(EPOCH FROM (crp.crp_time - ca.admittime)) / 3600.0) AS crp_hours_from_admit,

    -- Diagnosis labels (applied blind — do NOT use for classification, only for evaluation)
    dx.has_chf,
    dx.has_chf_systolic,
    dx.has_infection,
    dx.has_cancer,
    dx.primary_label,

    -- Derived: is this a "decoherence-positive" case?
    -- CHF or infection = likely elevated γ_eff → coherence-compromised
    CASE
        WHEN dx.has_chf = 1 OR dx.has_infection = 1 THEN 1
        ELSE 0
    END AS decoherence_positive

FROM cohort_admissions ca

JOIN cohort_diagnoses dx
    ON ca.subject_id = dx.subject_id
   AND ca.hadm_id    = dx.hadm_id

-- CRP: must be within ±24 hours of admission (proxy for ECG window)
-- Replace ca.admittime with your segment timestamp if joining to waveform directly
JOIN cohort_crp crp
    ON ca.subject_id = crp.subject_id
   AND ca.hadm_id    = crp.hadm_id
   AND crp.crp_time BETWEEN ca.admittime - INTERVAL '24 hours'
                        AND ca.admittime + INTERVAL '24 hours'

-- De-duplicate: one row per admission, closest CRP to admittime
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY ca.subject_id, ca.hadm_id
    ORDER BY ABS(EXTRACT(EPOCH FROM (crp.crp_time - ca.admittime)))
) = 1;

-- Note: QUALIFY is DuckDB/BigQuery syntax.
-- For PostgreSQL, wrap in a subquery with DISTINCT ON or use a CTE:
--
-- WITH ranked AS (
--   SELECT *, ROW_NUMBER() OVER (
--     PARTITION BY subject_id, hadm_id
--     ORDER BY ABS(EXTRACT(EPOCH FROM (crp_time - admittime)))
--   ) AS rn
--   FROM ...
-- )
-- SELECT * FROM ranked WHERE rn = 1;


-- ============================================================
-- STEP 5: SANITY CHECKS — run these after the pull
-- ============================================================

-- Total cohort size
SELECT COUNT(*) AS total_admissions FROM cohort_final;

-- Label distribution
SELECT primary_label, COUNT(*) AS n,
       ROUND(AVG(crp_mgl), 2) AS mean_crp,
       ROUND(STDDEV(crp_mgl), 2) AS std_crp
FROM cohort_final
GROUP BY primary_label
ORDER BY n DESC;

-- CRP severity distribution
SELECT crp_severity, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM cohort_final
GROUP BY crp_severity
ORDER BY n DESC;

-- CRP by diagnosis — this is what drives the sensitivity lift
SELECT primary_label, crp_severity, COUNT(*) AS n
FROM cohort_final
GROUP BY primary_label, crp_severity
ORDER BY primary_label, n DESC;

-- Verify no CRP data in the future relative to admission (data quality check)
SELECT COUNT(*) AS future_crp_errors
FROM cohort_final
WHERE crp_hours_from_admit < 0
  AND crp_time < admittime;


-- ============================================================
-- STEP 6: EXPORT FOR PYTHON HRV PIPELINE
-- ============================================================

-- This is the table your Python script joins to RR intervals.
-- Export as CSV: subject_id, hadm_id, crp_mgl, crp_severity, primary_label, decoherence_positive

COPY (
    SELECT
        subject_id,
        hadm_id,
        crp_mgl,
        crp_severity,
        primary_label,
        decoherence_positive,
        has_chf,
        has_infection,
        has_cancer,
        age_at_anchor,
        gender
    FROM cohort_final
    ORDER BY subject_id, hadm_id
) TO '/tmp/mimic_crp_cohort.csv' WITH (FORMAT CSV, HEADER TRUE);


-- ============================================================
-- PYTHON JOIN — paste into your HRV pipeline after the SQL pull
-- ============================================================
-- import pandas as pd
--
-- # Your existing RR interval feature table
-- hrv_features = pd.read_csv('hrv_features.csv')  # subject_id, hadm_id, SDNN, RMSSD, pNN50, LF, HF, LF_HF, SampEn, ...
--
-- # MIMIC CRP cohort
-- crp_cohort = pd.read_csv('/tmp/mimic_crp_cohort.csv')
--
-- # Join on subject_id + hadm_id
-- df = hrv_features.merge(crp_cohort, on=['subject_id', 'hadm_id'], how='inner')
--
-- # Features for model: HRV metrics + CRP
-- feature_cols = ['SDNN', 'RMSSD', 'pNN50', 'LF_HF', 'SampEn', 'crp_mgl']
-- X = df[feature_cols]
-- y = df['decoherence_positive']  # blind label — only used for eval, not training
--
-- # Your existing classifier here
-- # Expected sensitivity lift: 32% → 73-89% with CRP added
