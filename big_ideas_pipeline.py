"""
BIG IDEAs Glycemic Wearable — HRV Coherence Pipeline
Wike Coherence Framework — Pre-Diabetes Tier Analysis

Signals:
  IBI   → RR intervals → full HRV feature set
  EDA   → electrodermal activity → sympathetic tone (γ_eff proxy)
  CGM   → continuous glucose → glycemic variability (metabolic γ_eff)
  HR    → heart rate → mean + variability
  TEMP  → skin temperature → inflammatory proxy

Output:
  Per-subject feature table ready to join with MIMIC-IV cohort
  Coherence score C = C0 * exp(-alpha * gamma_eff)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import signal, stats
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = Path("/tmp/physionet.org/files/big-ideas-glycemic-wearable/1.1.3")
DEMO = BASE / "Demographics.csv"
OUT  = Path("/tmp/WIKE-RESEARCH-MASTER/big_ideas_features.csv")

# ── Wike Coherence Parameters ──────────────────────────────────────────────
C0    = 1.0   # normalized maximum coherence
ALPHA = 1.0   # coupling constant (tuned to CHF/NSR separation from prior work)


# ══════════════════════════════════════════════════════════════════════════
# 1. LOADERS
# ══════════════════════════════════════════════════════════════════════════

def load_ibi(subj: str) -> pd.Series:
    """Load IBI (inter-beat intervals) in seconds → RR interval series."""
    p = BASE / subj / f"IBI_{subj}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=['datetime'])
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['ibi'])
    # Physiological filter: 0.3–2.0s (30–200 BPM)
    df = df[(df['ibi'] > 0.3) & (df['ibi'] < 2.0)]
    df = df.set_index('datetime').sort_index()
    return df['ibi']


def load_eda(subj: str) -> pd.Series:
    """Load EDA (μS) — tonic sympathetic drive."""
    p = BASE / subj / f"EDA_{subj}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=['datetime'])
    df.columns = df.columns.str.strip()
    df = df.set_index('datetime').sort_index()
    return df['eda']


def load_glucose(subj: str) -> pd.Series:
    """Load Dexcom CGM glucose (mg/dL) — EGV rows only."""
    # Try 3-digit path first, fall back to 3-digit only (that's what we have)
    p = BASE / subj / f"Dexcom_{subj}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p)
    df.columns = df.columns.str.strip()
    # Keep only EGV (estimated glucose value) rows
    egv = df[df['Event Type'] == 'EGV'].copy()
    if egv.empty:
        return None
    egv['ts'] = pd.to_datetime(egv['Timestamp (YYYY-MM-DDThh:mm:ss)'], errors='coerce')
    egv = egv.dropna(subset=['ts', 'Glucose Value (mg/dL)'])
    egv = egv.set_index('ts').sort_index()
    return egv['Glucose Value (mg/dL)'].astype(float)


def load_temp(subj: str) -> pd.Series:
    """Load wrist skin temperature (°C)."""
    p = BASE / subj / f"TEMP_{subj}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=['datetime'])
    df.columns = df.columns.str.strip()
    df = df.set_index('datetime').sort_index()
    return df['temp']


# ══════════════════════════════════════════════════════════════════════════
# 2. HRV FEATURE EXTRACTION (from IBI/RR series)
# ══════════════════════════════════════════════════════════════════════════

def hrv_features(rr: pd.Series, window_minutes: int = 300) -> dict:
    """
    Full HRV feature set from RR interval series (seconds).
    Uses first N minutes to avoid OOM on multi-day recordings.
    Time domain + FFT frequency domain + nonlinear (SampEn).
    """
    # Clip to window to keep memory sane
    if len(rr) > 0:
        t0 = rr.index[0]
        rr = rr[rr.index <= t0 + pd.Timedelta(minutes=window_minutes)]

    rr_vals = rr.values
    n = len(rr_vals)
    if n < 30:
        return {}

    # ── Time Domain ───────────────────────────────────────────────────────
    mean_rr = np.mean(rr_vals)
    sdnn    = np.std(rr_vals, ddof=1)
    diff_rr = np.diff(rr_vals)
    rmssd   = np.sqrt(np.mean(diff_rr**2))
    pnn50   = 100.0 * np.sum(np.abs(diff_rr) > 0.05) / len(diff_rr)
    mean_hr = 60.0 / mean_rr

    # ── Frequency Domain via resampled FFT ────────────────────────────────
    # Resample IBI to 4 Hz evenly-spaced grid, then FFT
    t_s = (rr.index - rr.index[0]).total_seconds().values
    fs  = 4.0  # Hz
    t_even = np.arange(0, t_s[-1], 1.0 / fs)
    rr_interp = np.interp(t_even, t_s, rr_vals)

    # Detrend and window
    rr_interp = signal.detrend(rr_interp)
    win = np.hanning(len(rr_interp))
    rr_interp *= win

    # FFT PSD
    fft_vals = np.fft.rfft(rr_interp)
    psd      = (np.abs(fft_vals) ** 2) / (fs * len(rr_interp))
    freqs    = np.fft.rfftfreq(len(rr_interp), d=1.0/fs)

    def band_power(f_lo, f_hi):
        mask = (freqs >= f_lo) & (freqs < f_hi)
        return float(np.trapezoid(psd[mask], freqs[mask])) if mask.sum() > 1 else 0.0

    vlf = band_power(0.003, 0.04)
    lf  = band_power(0.04,  0.15)
    hf  = band_power(0.15,  0.40)
    tp  = vlf + lf + hf

    lf_norm = lf / (lf + hf + 1e-9)
    hf_norm = hf / (lf + hf + 1e-9)
    lf_hf   = lf / (hf + 1e-9)
    coherence_band = band_power(0.08, 0.12)  # 0.1 Hz HeartMath coherence

    # ── Nonlinear: Sample Entropy (200 beats, fast) ───────────────────────
    def sample_entropy(x, m=2, r_frac=0.2):
        r = r_frac * np.std(x)
        N = len(x)
        B, A = 0, 0
        for i in range(N - m - 1):
            for j in range(i + 1, N - m):
                if np.max(np.abs(x[i:i+m] - x[j:j+m])) < r:
                    B += 1
                    if abs(x[i+m] - x[j+m]) < r:
                        A += 1
        return -np.log((A + 1e-9) / (B + 1e-9))

    samp_en = sample_entropy(rr_vals[:200])

    # ── Poincaré SD1/SD2 ─────────────────────────────────────────────────
    sd1 = np.sqrt(0.5) * rmssd
    sd2 = np.sqrt(max(2 * sdnn**2 - 0.5 * rmssd**2, 0))
    sd1_sd2 = sd1 / (sd2 + 1e-9)

    return {
        'n_beats'        : n,
        'mean_rr_s'      : round(mean_rr, 4),
        'mean_hr_bpm'    : round(mean_hr, 2),
        'sdnn_s'         : round(sdnn, 4),
        'rmssd_s'        : round(rmssd, 4),
        'pnn50_pct'      : round(pnn50, 2),
        'lf_ms2'         : round(lf * 1e6, 4),
        'hf_ms2'         : round(hf * 1e6, 4),
        'vlf_ms2'        : round(vlf * 1e6, 4),
        'lf_norm'        : round(lf_norm, 4),
        'hf_norm'        : round(hf_norm, 4),
        'lf_hf_ratio'    : round(lf_hf, 4),
        'total_power'    : round(tp * 1e6, 4),
        'coherence_01hz' : round(coherence_band * 1e6, 4),
        'samp_en'        : round(samp_en, 4),
        'sd1'            : round(sd1, 4),
        'sd2'            : round(sd2, 4),
        'sd1_sd2_ratio'  : round(sd1_sd2, 4),
    }


# ══════════════════════════════════════════════════════════════════════════
# 3. EDA FEATURES (sympathetic γ_eff proxy)
# ══════════════════════════════════════════════════════════════════════════

def eda_features(eda: pd.Series) -> dict:
    """Tonic EDA level + phasic burst count."""
    if eda is None or len(eda) < 10:
        return {}
    vals = eda.values
    tonic_mean  = np.mean(vals)
    tonic_std   = np.std(vals)

    # Phasic bursts: peaks > mean + 2*std
    peaks, _ = signal.find_peaks(vals, height=tonic_mean + 2*tonic_std, distance=16)
    # Duration in minutes
    dur_min = (eda.index[-1] - eda.index[0]).total_seconds() / 60.0

    return {
        'eda_mean_us'    : round(tonic_mean, 4),
        'eda_std_us'     : round(tonic_std, 4),
        'eda_bursts_pm'  : round(len(peaks) / (dur_min + 1e-9), 4),
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. GLYCEMIC VARIABILITY FEATURES
# ══════════════════════════════════════════════════════════════════════════

def glucose_features(glc: pd.Series) -> dict:
    """
    Glycemic variability → metabolic γ_eff.
    High CV, high MAGE, high time-above-range = high metabolic decoherence.
    """
    if glc is None or len(glc) < 5:
        return {}
    vals = glc.values
    mean_g = np.mean(vals)
    std_g  = np.std(vals)
    cv_g   = 100.0 * std_g / (mean_g + 1e-9)

    # Time in range (70–180 mg/dL) — pre-diabetes standard
    tir = 100.0 * np.mean((vals >= 70) & (vals <= 180))
    tar = 100.0 * np.mean(vals > 180)
    tbr = 100.0 * np.mean(vals < 70)

    # MAGE (mean amplitude of glycemic excursions)
    # Simple: mean of |diff| > 1 SD
    diffs = np.abs(np.diff(vals))
    mage = np.mean(diffs[diffs > std_g]) if np.any(diffs > std_g) else 0.0

    # Glucose rate of change (mg/dL/min average absolute)
    t_min = (glc.index - glc.index[0]).total_seconds().values / 60.0
    if len(t_min) > 1:
        roc = np.abs(np.diff(vals)) / (np.diff(t_min) + 1e-9)
        mean_roc = np.mean(roc)
    else:
        mean_roc = 0.0

    return {
        'glucose_mean_mgdl' : round(mean_g, 2),
        'glucose_std_mgdl'  : round(std_g, 2),
        'glucose_cv_pct'    : round(cv_g, 2),
        'time_in_range_pct' : round(tir, 2),
        'time_above_pct'    : round(tar, 2),
        'time_below_pct'    : round(tbr, 2),
        'mage_mgdl'         : round(mage, 2),
        'glucose_roc_mgdl_min': round(mean_roc, 4),
    }


# ══════════════════════════════════════════════════════════════════════════
# 5. WIKE GAMMA_EFF COMPOSITE + COHERENCE SCORE
# ══════════════════════════════════════════════════════════════════════════

def compute_gamma_eff(feats: dict) -> float:
    """
    γ_eff composite from HRV + EDA + glucose features.
    Normalized so γ_eff = 1.0 at the CHF population mean from prior work.

    Components:
      - LF/HF ratio       (↑ = sympathetic dominance = ↑ γ_eff)
      - RMSSD             (↓ = reduced vagal tone = ↑ γ_eff)
      - SampEn            (↓ = reduced complexity = ↑ γ_eff)
      - EDA mean          (↑ = sympathetic activation = ↑ γ_eff)
      - Glucose CV        (↑ = metabolic noise = ↑ γ_eff)
    """
    # Each term normalized to [0,1] range from population data
    # Reference ranges from literature:
    #   Healthy: RMSSD ~42ms, LF/HF ~1.5, SampEn ~1.2
    #   CHF:     RMSSD ~18ms, LF/HF ~3.2, SampEn ~0.6

    components = []

    if 'lf_hf_ratio' in feats:
        lf_hf_norm = np.clip(feats['lf_hf_ratio'] / 4.0, 0, 1)
        components.append(lf_hf_norm)

    if 'rmssd_s' in feats:
        # Invert: low RMSSD = high γ_eff
        rmssd_ms = feats['rmssd_s'] * 1000
        rmssd_norm = np.clip(1.0 - (rmssd_ms / 60.0), 0, 1)
        components.append(rmssd_norm)

    if 'samp_en' in feats:
        # Invert: low SampEn = high γ_eff
        sampen_norm = np.clip(1.0 - (feats['samp_en'] / 2.0), 0, 1)
        components.append(sampen_norm)

    if 'eda_mean_us' in feats:
        eda_norm = np.clip(feats['eda_mean_us'] / 5.0, 0, 1)
        components.append(eda_norm)

    if 'glucose_cv_pct' in feats:
        cv_norm = np.clip(feats['glucose_cv_pct'] / 36.0, 0, 1)
        components.append(cv_norm)

    if not components:
        return float('nan')

    return float(np.mean(components))


def coherence_score(gamma_eff: float, c0: float = C0, alpha: float = ALPHA) -> float:
    """C = C₀ · exp(−α · γ_eff)  — Wike Coherence Law"""
    if np.isnan(gamma_eff):
        return float('nan')
    return c0 * np.exp(-alpha * gamma_eff)


# ══════════════════════════════════════════════════════════════════════════
# 6. MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════

def process_subject(subj: str) -> dict:
    print(f"Processing {subj}...")

    # Load all signals
    ibi  = load_ibi(subj)
    eda  = load_eda(subj)
    glc  = load_glucose(subj)
    temp = load_temp(subj)

    feats = {'subject_id': subj}

    # HRV
    if ibi is not None and len(ibi) > 30:
        feats.update(hrv_features(ibi))
        feats['ibi_duration_hrs'] = round(
            (ibi.index[-1] - ibi.index[0]).total_seconds() / 3600, 2)
    else:
        print(f"  ⚠ No IBI data for {subj}")

    # EDA
    if eda is not None:
        feats.update(eda_features(eda))

    # Glucose
    if glc is not None:
        feats.update(glucose_features(glc))

    # Temperature
    if temp is not None:
        feats['temp_mean_c'] = round(float(temp.mean()), 3)
        feats['temp_std_c']  = round(float(temp.std()), 4)

    # γ_eff + coherence score
    gamma = compute_gamma_eff(feats)
    feats['gamma_eff']       = round(gamma, 4) if not np.isnan(gamma) else None
    feats['coherence_score'] = round(coherence_score(gamma), 4) if not np.isnan(gamma) else None

    return feats


def main():
    # Load demographics
    demo = pd.read_csv(DEMO)
    demo.columns = demo.columns.str.strip()
    # Subject folders: 001–016
    subjects = sorted([d.name for d in BASE.iterdir()
                       if d.is_dir() and d.name.isdigit()])

    all_feats = []
    for subj in subjects:
        try:
            f = process_subject(subj)
            # Merge HbA1c from demographics
            subj_id = int(subj)
            row = demo[demo['ID'] == subj_id]
            if not row.empty:
                f['hba1c']  = float(row['HbA1c'].values[0])
                f['gender'] = row['Gender'].values[0]
                # HbA1c tiers: < 5.7 = normal, 5.7–6.4 = pre-diabetes, ≥ 6.5 = diabetes
                h = f['hba1c']
                f['glycemic_tier'] = (
                    'pre-diabetes' if 5.7 <= h < 6.5 else
                    'diabetes'     if h >= 6.5        else
                    'normal'
                )
            all_feats.append(f)
        except Exception as e:
            print(f"  ERROR {subj}: {e}")

    df = pd.DataFrame(all_feats)
    df = df.sort_values('subject_id').reset_index(drop=True)

    # Save
    df.to_csv(OUT, index=False)
    print(f"\n✅ Saved: {OUT}")
    print(f"   {len(df)} subjects × {len(df.columns)} features")

    # Quick summary
    print("\n── Coherence Scores by HbA1c Tier ──────────────────────")
    if 'coherence_score' in df.columns and 'glycemic_tier' in df.columns:
        summary = df.groupby('glycemic_tier')[['coherence_score','gamma_eff',
                                               'rmssd_s','lf_hf_ratio',
                                               'glucose_cv_pct']].mean().round(3)
        print(summary.to_string())

    print("\n── Full Feature Table Preview ───────────────────────────")
    print(df[['subject_id','hba1c','glycemic_tier','gamma_eff',
              'coherence_score','rmssd_s','lf_hf_ratio',
              'samp_en','eda_mean_us','glucose_cv_pct']].to_string(index=False))

    return df


if __name__ == "__main__":
    df = main()
