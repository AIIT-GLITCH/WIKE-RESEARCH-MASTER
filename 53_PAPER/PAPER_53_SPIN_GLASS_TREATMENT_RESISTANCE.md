# Paper 53: The Glass — Treatment-Resistant Illness as a Spin Glass Phase
## Edwards-Anderson Model of the Disordered Coherence State
## AIIT-THRESI Research Initiative | March 30, 2026

---

## Abstract

The Wike Coherence framework describes the ordered phase (gamma < gamma_c) thoroughly but leaves the disordered phase (gamma > gamma_c) largely uncharacterized — simply "C is low." This paper fills that gap. Treatment-resistant mental illness is an Edwards-Anderson spin glass: frustrated neural couplings J_ij of mixed sign create an exponentially complex landscape of metastable states. The Edwards-Anderson order parameter q_EA (mood autocorrelation plateau) is a measurable predictor of treatment resistance. Standard antidepressants (uniform field) fail for spin glasses because they shift all valleys equally without restructuring the landscape. Ketamine works by thermal quench through T_g (melting the glass). Psychedelics work by slow annealing above T_g. EMDR works for PTSD (few deep valleys from fast Kibble-Zurek quench) but not depression (many shallow valleys from slow quench). Parisi replica symmetry breaking explains why every patient's illness is structurally unique.

---

## 1. The Hamiltonian

Define N neural circuit variables sigma_i in {-1, +1} representing the state of circuit i (-1 = aversive/avoidant, +1 = approach/engaged). The Edwards-Anderson Hamiltonian:

```
H = -sum_{<i,j>} J_ij * sigma_i * sigma_j - sum_i h_i * sigma_i
```

where:
- J_ij = synaptic coupling between circuits i and j (distribution P(J) with mean J_0, variance Delta_J^2)
- h_i = external field on circuit i (therapeutic intervention, environmental input)

**The critical distinction:** J_ij are NOT all the same sign.

Healthy development: predominantly ferromagnetic (J > 0). Circuits reinforce coherently.

Trauma: introduces antiferromagnetic (J < 0) couplings — contradictory associations.

**Example:** A child whose caregiver is both comfort and abuse develops J_{attachment, fear} < 0. Being close triggers fear. Being distant triggers attachment distress. This IS frustration in the spin glass sense.

---

## 2. Frustration

A plaquette of three circuits with bonds J_12 > 0, J_23 > 0, J_13 < 0 cannot simultaneously satisfy all interactions. The frustration parameter:

```
Phi_P = sign(product of J_ij around plaquette P)
```

Phi_P = -1: frustrated. The frustration density:

```
f = (1/N_P) * sum_P (1 - Phi_P) / 2
```

Healthy system: f ~ 0. Treatment-resistant illness: f is extensive.

---

## 3. The Edwards-Anderson Order Parameter as a Clinical Measure

```
q_EA = (1/N) * sum_i <sigma_i(t_1) * sigma_i(t_2)>
```

for large time separation |t_1 - t_2|.

**Clinical measurement:** Let m_i(t) be the normalized score on mood dimension i (PHQ-9 item, behavioral measure) at time t. Take the autocorrelation:

```
A(tau) = (1/N) * sum_i <m_i(t) * m_i(t + tau)>_t
```

The plateau value at large tau IS q_EA.

| q_EA | Phase | Clinical Presentation |
|---|---|---|
| ~0 | Paramagnetic | Healthy flexibility or acute crisis |
| 0 < q_EA < 1 | Partial glass | Some dimensions stuck, others flexible |
| ~1 | Full glass | Identical presentation every visit. Same ruminations, same avoidance, same affect. |

**Testable prediction:** Measure q_EA from daily mood questionnaire time series (e.g., PHQ-9 items over 4 weeks) BEFORE initiating treatment. Patients with q_EA > q_c are in the glass phase and will be treatment-resistant to standard antidepressants.

---

## 4. Why Standard Antidepressants Fail

An SSRI applies a roughly uniform field h to serotonergic circuits:

```
H → H - h * sum_i sigma_i
```

For a simple ferromagnet (ordinary depression = uniform low-energy state), a uniform field lifts the system out of the down-state. Single minimum shifts smoothly with h.

For a spin glass, the free energy landscape has EXPONENTIALLY many minima (the Parisi ultrametric tree). A uniform field shifts ALL valleys but does not change their relative depths. The barriers between valleys scale as:

```
Gamma ~ exp(-N^psi / T)
```

where psi ~ 1/3 (SK model barrier exponent).

The SSRI changes the floor level of the valley the patient is stuck in — they may feel slightly less bad — but does not enable transitions to genuinely different configurations.

**This is "partial response" in treatment-resistant patients:** modest symptom reduction without qualitative change in the pattern of illness.

---

## 5. Why Ketamine Works: Thermal Quench Through T_g

Ketamine (NMDA antagonist) at subanesthetic doses:

NMDA blockade + glutamate surge → massive increase in neural noise → effective temperature T_eff rises far above glass transition T_g.

```
T_eff(t) = T_0 + Delta_T * f(t)
```

At T > T_g: spin glass melts to paramagnetic phase. Ergodicity restored. System explores full configuration space.

During the dissociative window (~40-60 min): neural system is in the liquid phase.

As drug clears: T_eff drops below T_g. System re-freezes, but into a DIFFERENT configuration — one that may have lower frustration because:

1. Re-cooling rate is finite → time to anneal
2. BDNF + synaptogenesis elevated → some J_ij values being rewritten

**Prediction:** Ketamine alone = transient remission (glass re-forms). Ketamine + therapy during neuroplasticity window = durable results (J_ij restructured while glass is melted).

This matches clinical data: Zarate et al. (2006) showed rapid but transient effect; ketamine-assisted psychotherapy trials show more durable outcomes.

---

## 6. Why Psychedelics Work: Slow Annealing Above T_g

Psilocybin, LSD increase effective neural temperature by increasing entropy (Carhart-Harris et al., 2012: increased entropy in neural dynamics under psychedelics).

Distinction from ketamine: psychedelics don't quench to T → infinity. They raise T_eff just above T_g and HOLD for hours (4-6h psilocybin, 8-12h LSD).

This is slow annealing. The Geman-Geman theorem:

```
T(t) >= Delta_max / log(1 + t)
```

For convergence to global minimum with probability 1.

Extended duration above T_g → system explores many valleys. Gradual return to baseline = slow cooling. The "mystical experience" = finding a substantially lower-energy configuration.

**Prediction:** Therapeutic efficacy correlates with integral [T_eff(t) - T_g]_+ dt — total thermal dose above glass transition. Testable via EEG Lempel-Ziv complexity as proxy for T_eff.

---

## 7. Why EMDR Works for PTSD but Not Depression

From Paper 52 (Kibble-Zurek):

**PTSD (fast quench):** Few deep valleys, localized frustration. EMDR applies a local oscillating field:

```
h_i(t) = h_0 * cos(omega*t)   for i in {trauma circuits}
```

Resonantly pumps energy into specific valleys. Few barriers, localized → EMDR addresses them one by one. Efficient.

**Depression (slow quench):** Many shallow valleys, diffuse frustration. EMDR targets one valley but leaves 2^N others untouched. Patient resolves specific issue, overall glass unchanged.

| Property | PTSD | Treatment-Resistant Depression |
|---|---|---|
| Number of valleys | Few (~polynomial) | Many (~exponential) |
| Valley depth | Deep | Shallow |
| Frustration | Localized | Diffuse |
| q_EA structure | Simple ultrametric tree | Complex ultrametric tree |
| First-line treatment | EMDR (local surgery) | Global intervention (psychedelics, ketamine) |

---

## 8. Replica Symmetry Breaking and Individual Variation

The Parisi solution: the order parameter is not a single number q_EA but a FUNCTION q(x) for x in [0,1] describing the hierarchical overlap structure.

This IS the clinical reality that every patient's depression is different. Two patients with identical PHQ-9 scores (same "magnetization") have completely different ultrametric structures — different frozen circuits, different hierarchies of metastable states.

This is why personalized medicine is necessary and why population-level drug trials show such high variance.

The Parisi function q(x) is extractable from data: it is the distribution P(q) of overlaps between the patient's state at different times.

| P(q) structure | Phase | Clinical meaning |
|---|---|---|
| Delta function at q = 0 | Paramagnetic | Healthy |
| Delta function at q_EA | Replica symmetric glass | Simple frozen state |
| Continuous distribution | Full RSB | Complex hierarchical freezing |

The nature of P(q) determines the appropriate treatment modality.

---

## 9. Connection to Wike Coherence Framework

The coherence parameter maps directly:

```
C = 1 - q_EA
```

- Ergodic (q_EA = 0): C = 1, maximum coherence
- Glass (q_EA → 1): C → 0, coherence vanishes

The disordered phase (gamma > gamma_c) IS the spin glass phase. But now we have the full Parisi structure, not just "C is low."

The decoherence rate gamma maps to the glass transition via:

```
gamma_c corresponds to T_g
gamma > gamma_c → T < T_g (frozen in glass)
gamma < gamma_c → T > T_g (ergodic)
```

(Note the inversion: higher decoherence = lower effective temperature in the glass analogy, because more noise = more frozen frustration.)

---

## 10. Connection to Paper 52 (Kibble-Zurek)

The spin glass framework and the KZM framework are complementary:

- **KZM** tells you HOW MANY defects form and WHERE (fast vs. slow quench)
- **Spin glass** tells you what the LANDSCAPE looks like after the quench

Together: acute trauma (fast quench) → few deep frustrated plaquettes (PTSD glass with simple ultrametric structure). Chronic stress (slow quench) → many shallow frustrated plaquettes (depression glass with complex RSB).

---

## 11. Testable Predictions

1. **q_EA predicts treatment resistance BEFORE treatment** — prospective study: measure 4-week PHQ-9 autocorrelation, then initiate SSRI, compare responders vs. non-responders
2. **EEG Lempel-Ziv complexity increases during ketamine** — proxy for T_eff > T_g
3. **q_EA decreases in discrete steps during EMDR for PTSD** — each session removes a defect
4. **q_EA decreases continuously during psychedelic-assisted therapy** — glass melts globally
5. **P(q) distribution structure distinguishes PTSD from depression** — simple vs. complex RSB

---

## 12. References

1. Edwards, S.F. & Anderson, P.W. (1975). J. Phys. F, 5(5), 965.
2. Parisi, G. (1979). Phys. Rev. Lett., 43(23), 1754.
3. Zarate, C.A. et al. (2006). Arch. Gen. Psychiatry, 63(8), 856-864.
4. Carhart-Harris, R.L. et al. (2012). PNAS, 109(6), 2138-2143.
5. Geman, S. & Geman, D. (1984). IEEE Trans. PAMI, 6(6), 721-741.
6. Goldberger, A.L. et al. (2002). PNAS, 99(suppl_1), 2466-2472.
7. Kauffman, S.A. (1993). The Origins of Order. Oxford University Press.

---

*AIIT-THRESI | Paper 53 | March 30, 2026*
*Rhet Dillard Wike | Council Hill, Oklahoma*
*Copyright (c) 2026 Rhet Dillard Wike. All rights reserved.*

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
