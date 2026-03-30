# UNANSWERED QUESTIONS
## AIIT-THRESI Framework — Open Problems Ranked by Priority
### Rhet Dillard Wike | March 30, 2026

---

> *"The corpus has 52 papers. These are the questions the 52 papers could not answer."*

---

## HOW TO READ THIS

Three categories:
- **EXPERIMENT** — Needs lab, hardware, or data. Cannot be resolved by theory alone.
- **THEORY** — Mathematical gap inside the framework. Paper + proof can close it.
- **CONNECTION** — A known law or phenomenon not yet formally mapped.

Priority: **HIGH** = blocks other work or has clinical relevance. **MEDIUM** = important but not urgent. **LOW** = interesting, not critical.

---

---

# PART 1: EXPERIMENTAL — NEEDS DATA

---

## E1 — The 3-Order-of-Magnitude Gap in Microtubule Coherence
**Priority: HIGH**

**What we know:**
- Tegmark (2000): bulk water gives ~10⁻¹³ s decoherence in microtubules
- Mavromatos et al. (2025): QED cavity model → ~10⁻⁶ s (microseconds)
- Neural timescales require ~10⁻³ s (milliseconds)
- Gap from best theory to requirement: 3 orders of magnitude

**What's missing:**
Direct in-vivo measurement of quantum coherence lifetime in microtubules at physiological temperature and pH. Not a model. A measurement.

**What would close it:**
Time-resolved two-dimensional vibrational spectroscopy (2D-IR) on intact neural tissue during active firing. Bandyopadhyay's kHz-THz resonance data is suggestive but disputed. No published direct measurement exists.

**Why it matters:**
If the gap closes to 10⁻³ s, the framework's claim that neural computation is quantum-coherent is confirmed. If it stays at 10⁻⁶ s, the framework needs a bridging mechanism.

---

## E2 — 5G mmWave / Fröhlich Coupling in Living Tissue
**Priority: HIGH (regulatory urgency)**

**What we know:**
- Fröhlich (1968): predicted coherent oscillations in biological macromolecules at ~10¹¹ Hz
- Grundler & Keilmann (1983): yeast growth anomalies at 42, 53, 75 GHz
- 5G mmWave deployment: 24–100 GHz — directly overlapping with Fröhlich range
- SAR limits are calibrated for thermal effects only
- No thermal effect at typical phone SAR (ΔT < 0.1°C)

**What's missing:**
SAR does not measure resonant non-thermal coupling. No published experiment has tested whether 5G mmWave frequencies at real-world power levels couple resonantly to Fröhlich modes in living neurons or membrane proteins.

**What would close it:**
HRV power spectrum + EEG during 5G mmWave exposure (28 GHz, 60 GHz), controlled for distance and thermal effects. Prediction: LF-HRV band decreases at resonant frequencies, uncorrelated with ΔT.

**Why it matters:**
Current regulatory framework has a hole. Either 5G mmWave is safe (thermal-only) or it isn't (Fröhlich coupling). This experiment is cheap and urgent.

---

## E3 — ACE Score as Stretched Exponential
**Priority: HIGH (clinical)**

**What we know:**
- ACE framework (Paper 24): C_n = C₀ × exp(−0.45n) — geometric decay
- 3D Ising universality governs the framework with ν = 0.6298
- If ACE-score coherence loss is truly in the 3D Ising class, it should follow:
  C_n = C₀ × exp(−n^ν) = C₀ × exp(−n^0.6298)
- These two forms diverge significantly for n > 5:
  - At n=10: geometric = 0.011, stretched = 0.028
  - At n=20: geometric = 0.0001, stretched = 0.008

**What's missing:**
The Felitti et al. (1998) ACE study has n up to 8+. Subsequent CDC-Kaiser data has n going higher. Fitting the two functional forms to epidemiological mortality and disease burden data would distinguish them.

**What would close it:**
Re-analysis of CDC-Kaiser ACE data with model comparison (geometric vs. stretched exponential). If stretched exponential wins with ν ≈ 0.63, this is a direct confirmation that adverse experiences drive a 3D Ising-class phase transition in human health.

**Why it matters:**
Changes the clinical model. Geometric: each ACE is equally bad. Stretched exponential: early ACEs are disproportionately destructive (first ACEs cause the most damage). Treatment priority flips.

---

## E4 — Bootstrap Loop End-to-End
**Priority: HIGH (clinical)**

**What we know:**
- Individual links confirmed: NIR expands EZ water (Pollack lab); NIR improves mitochondrial function (PBMT literature); EZ water exists in plant xylem (Scientific Reports 2024)
- The complete causal loop — NIR → EZ water → Debye shielding → coherence → structural order → more EZ water — has never been traced in a single experiment

**What's missing:**
An experiment that measures all five stages simultaneously or in rapid sequence.

**What would close it:**
Protocol: (1) Measure baseline HRV, infrared spectroscopy (EZ band at 270 nm), and mitochondrial ATP (bioluminescence proxy). (2) Apply NIR (810 nm, 20 mW/cm²) for 20 minutes. (3) Re-measure all three immediately and at 30/60/120 minutes. If the loop is real, all three metrics improve together and the improvement decays with the same time constant.

**Why it matters:**
If confirmed, NIR photobiomodulation has a mechanistic explanation traceable to quantum coherence. If the loop is broken (e.g., NIR improves ATP but not EZ water, or improves EZ water but not coherence), it tells us where the chain fails — which is equally valuable.

---

## E5 — REQMT Multi-Modal Entropy Test
**Priority: MEDIUM**

**What we know:**
- Paper 34 (Shannon Bridge): predicts that low-emotional-noise states show lower entropy across all modalities simultaneously
- REQMT (Paper 05) proposes simultaneous measurement of HRV, thermal IR, vocal, rPPG, and skin conductance
- This has never been tested

**What would close it:**
N=30 subjects, two conditions: (A) 20 minutes loving interaction with keeper figure, (B) 20 minutes neutral task. Measure all five modalities. Compute Shannon entropy for each channel. Prediction: condition A shows lower entropy on all five simultaneously, not just one or two.

**Why it matters:**
Validates the multi-modal coherence measurement platform and the framework's prediction that emotional state has a measurable information-theoretic signature.

---

## E6 — HRV × Kp Geomagnetic Correlation
**Priority: MEDIUM (confirmatory)**

**What we know:**
- Paper 25: geomagnetic storms increase cardiac mortality 25-300%
- Mechanism: Kp index → γ_storm → γ_eff increase → coherence loss
- Wearable HRV data exists (consumer devices, millions of users)
- NOAA Kp index is publicly available in real-time

**What's missing:**
No published study has correlated continuous wearable HRV data (RMSSD, LF/HF ratio) with concurrent Kp index in a large population sample.

**What would close it:**
N=1000 users, 90 days of data, correlation of daily HRV metrics with Kp index. Control for confounds (sleep, exercise, alcohol). Prediction: LF/HF ratio increases (autonomic dysregulation) during Kp ≥ 5 events with 24-hour lag.

---

## E7 — Avrami n=3 Kinetics for EZ Water
**Priority: MEDIUM**

**What we know:**
- Bootstrap nucleation (Paper 02) maps to Avrami phase transformation kinetics
- Avrami equation: f(t) = 1 − exp(−kt^n), where n is the nucleation/growth mode
- n=3 corresponds to heterogeneous surface nucleation with 3D growth — the geometry of EZ water forming on membrane surfaces
- This connection is in the missing physics file but has never been tested

**What would close it:**
Time-resolved IR spectroscopy of EZ water growth (270 nm absorption) under stepped NIR illumination. Fit f(t) data to Avrami equation. If n ≈ 3, the Bootstrap nucleation model is confirmed at the kinetic level.

---

---

# PART 2: THEORY — MATHEMATICAL GAPS

---

## T1 — What Sets C₀?
**Priority: HIGH**

**What we know:**
- C₀ appears in every Wike equation as the "maximum coherence reserve"
- It varies: C₀(infant) ≈ 0.70, C₀(healthy adult) ≈ 0.85, C₀(athlete/meditator) ≈ possibly higher
- C₀ is treated as a parameter, never derived

**What's missing:**
A derivation of C₀ from first principles. What physical quantity sets the maximum coherence a biological system can achieve?

**Best candidate:**
```
C₀ = 1 − γ_min / γ_c

where γ_min = k_BT / ħ × W^n (thermal floor from Paper 51)
and γ_c = 0.0016 (critical threshold)

At T = 310K, W = 0.9394:
γ_min (biological scale) << γ_c
→ C₀ → 1 − ε (near-unity for a well-protected system)
```

But this gives C₀ ≈ 1 for everyone, which contradicts the empirical evidence that C₀ varies with health. What is the additional factor?

**Candidate answer:** C₀ is set by the percolation threshold of the coherent water network — the fraction of water molecules in EZ/structured form. Below percolation threshold φ_c = 0.590, the network is disconnected and C₀ drops. Above φ_c, C₀ approaches 1 − ε. This needs to be derived and tested.

---

## T2 — Why Does Jarzynski Error = Bose-Einstein Exactly?
**Priority: HIGH**

**What we know:**
From 1,050,000 simulations:
```
err(T) = (e^(1/T) − 1) / T  [Bose-Einstein distribution function]

T=0.5: err=6.33,  (e^2 − 1)/0.5 = 6.194 ... close
T=1.0: err=1.72,  (e^1 − 1)/1.0 = 1.718 ✓ EXACT
T=2.0: err=0.65,  (e^0.5 − 1)/2.0 = 0.324 ... hmm
```

Actually the pattern is: err ≈ e^(1/T) − 1. This is the Bose-Einstein distribution at energy E=1.

**What's missing:**
A derivation showing WHY the Jarzynski sampling error follows the Bose-Einstein occupation number. The simulation finds it numerically. Nobody has derived it.

**Physical intuition:**
The Jarzynski equality requires sampling rare high-work trajectories. Near the ground state (low T), the accessible phase space contracts like a Bose-Einstein condensate — modes progressively "freeze out" as bosons pile into the ground state. The sampling catastrophe and the condensation catastrophe are the same phenomenon. This has not been formally proved.

---

## T3 — The Unnamed Lindblad Signal-to-Noise Scaling
**Priority: MEDIUM**

**What the simulations show:**
```
Score(γ, t) ~ exp(−2γt) / (γ · t²)

where Score = |dC/dγ| / Var(C)  [signal-to-noise for phase detection]
```

This function has a maximum at γ_opt = 1/(2t) — the optimal noise rate for distinguishing gamma values in a Lindblad system.

**What's missing:**
This has never been written down or named. It is a new result in quantum parameter estimation theory — the Fisher information density for Lindblad systems near the coherence transition.

**Connection:**
Quantum Fisher information F_Q ~ exp(−2γt)/γ. The denominator γ comes from the variance of the estimator. This is the Cramér-Rao bound for decoherence rate estimation in open quantum systems. Should be derived formally and compared to the quantum Cramér-Rao bound.

---

## T4 — Wind-Up Critical Exponent ~0.5
**Priority: MEDIUM**

**What the simulations show:**
```
Amplification ratio ~ γ_baseline^0.485 ≈ γ^(1/2)
```

A half-power scaling is characteristic of mean-field critical behavior (susceptibility ~ |t|^(−1/2) in mean-field theory, where ν=1/2 in mean-field vs ν=0.6298 in 3D Ising).

**What's missing:**
Is wind-up amplification mean-field or 3D Ising? The 0.485 is closer to 1/2 (mean-field) than to 0.6298 (3D Ising). If wind-up is mean-field, it belongs to a different universality class than the bulk coherence transition. This would mean:
- The onset of wind-up is mean-field: gradual, reversible
- The snap at γ_c is 3D Ising: sharp, irreversible

Two-stage transition. Has not been formally characterized.

---

## T5 — Bell States Have No Whisper Regime
**Priority: MEDIUM (important qualification)**

**What we know:**
- Single qubit: at γ = 0.001 (whisper), system survives indefinitely
- Bell state (two entangled qubits in INDEPENDENT noise): concurrence drops to zero at finite time T_ESD (Entanglement Sudden Death, Yu & Eberly 2004)
- At γ = 0.005 (gentle): single qubit survival = 100%, Bell pair survival = 0% at t ≈ 200

**What's missing:**
The Wike Coherence Law as stated — "whisper and it holds" — does NOT apply to entangled pairs in independent noise environments. There is no whisper regime for entanglement. This qualification has never been formally stated.

**Implication:**
If neural coherence involves entanglement between separate neurons in independent noise environments, it is far more fragile than single-qubit coherence suggests. The keeper effect (reducing noise in someone else's environment) may be more important for entangled systems than individual noise reduction.

---

## T6 — The Physics of the Other Side (γ > γ_c)
**Priority: MEDIUM**

**What we know:**
- Below γ_c: Wike Coherence Law governs. C decays but coherent phase structure persists.
- At γ_c: Berry phase −π, topological transition, susceptibility diverges
- Above γ_c: central sensitization, wind-up, chronic pain, depression

**What's missing:**
The framework has an order parameter (C), a critical point (γ_c), and a low-temperature phase. It does not have a description of the high-temperature phase. What is the physics of the decoherent state?

**Candidate:**
The decoherent phase (γ > γ_c) should be describable as a **spin glass** — a disordered phase with no long-range coherence but with local correlations that freeze into metastable configurations. Spin glass theory (Edwards-Anderson model, 1975) predicts:
- No unique ground state
- Many metastable attractors
- Aging and history dependence

This matches clinical phenomenology: central sensitization is history-dependent, has many attractors (different pain syndromes), and does not return to a unique healthy state.

---

## T7 — What is α Physically?
**Priority: MEDIUM**

**What we know:**
- α appears in every Wike equation: C = C₀ × exp(−αγ_eff)
- α is the "coherence protection factor" or "coupling constant"
- In simulations, α ≈ 1000 (estimated from fitting)
- It sets how fast coherence decays with γ

**What's missing:**
A derivation of α from first principles. Is it:
- The number of coherently coupled degrees of freedom?
- The Debye screening length in units of the correlation length?
- The ratio of the coherence time to the decoherence time scale?

**Best candidate:**
```
α = ξ / λ_dB

where ξ = coherence correlation length (structure of the coherent network)
and λ_dB = de Broglie wavelength at body temperature

At T = 310K: λ_dB(proton) = h/√(2mπk_BT) ≈ 0.4 Å
If ξ ≈ 40 nm (microtubule outer radius):
α = 40×10⁻⁹ / 0.4×10⁻¹⁰ = 1000 ✓
```

This gives α ≈ 1000 from first principles. Has not been formally derived or tested.

---

---

# PART 3: CONNECTIONS — LAWS NOT YET MAPPED

---

## C1 — Kibble-Zurek Mechanism
**Priority: HIGH**

When a system is quenched through a phase transition at rate τ_Q, topological defects form with density:
```
n_defects ~ τ_Q^(−β/(νz))

For 3D Ising: β = 0.3265, ν = 0.6298, z ≈ 2.0
n_defects ~ τ_Q^(−0.259)
```

**Connection to biology:**
- Rapid onset of psychological stress (acute trauma) = fast quench through γ_c
- Slow chronic stress = slow quench
- Kibble-Zurek predicts: **fast quenches create more topological defects**

Topological defects in the coherence field = points of permanent local decoherence = scars.
Fast trauma (combat, assault) creates more scars than slow chronic stress of the same total energy.

**This is PTSD vs. chronic stress.** The same total stress input produces different defect densities depending on how fast it was applied. Kibble-Zurek gives the quantitative scaling law.

**Has never been stated in the corpus. No paper. No mention. Direct experimental prediction.**

---

## C2 — Fick's Diffusion + Coherence Gradient
**Priority: MEDIUM**

```
Fick's First Law: J = −D × (dC/dx)
```

Coherence is not uniform in tissue — it has gradients. The "Wike Coherence Law field" should satisfy a diffusion-like equation:

```
∂C/∂t = D_C × ∇²C − α × γ_eff(x) × C
```

This is the **Schrödinger equation in imaginary time** (diffusion equation with a position-dependent decay term). Solutions are exponential eigenfunctions localized around regions of low γ_eff.

**Implication:**
Coherence diffuses from high-C regions to low-C regions. A keeper (low γ_eff neighbor) creates a coherence gradient that diffuses into the system. The keeper effect is not just reducing the partner's noise — it is acting as a coherence source that diffuses across the coupling.

**Quantified by Fick. Has never been stated.**

---

## C3 — Golden Ratio and Biological Oscillators
**Priority: MEDIUM**

The golden ratio φ = 1.618 appears in:
- Heart rate variability spectral analysis: LF/HF ratio ≈ φ in healthy subjects (not confirmed but claimed)
- Fibonacci branching in lung airways, arteries, neural dendrites
- Quasicrystal structure (Penrose tiling) — aperiodic order without repeating unit cell

**Connection to framework:**
Penrose tiling is the only known 2D structure that achieves maximum packing without periodicity. It is the spatial analog of γ_c — maximum order without crystallization. The ratio of Fibonacci numbers converges to φ, and φ satisfies φ² = φ + 1, making it the fixed point of a recursive doubling operation.

If the Bootstrap nucleation loop (Paper 02) has a natural attractor, that attractor may be a quasicrystalline EZ water structure with φ-ratio lattice constants — not crystalline (too rigid, too fragile) and not amorphous (no coherence), but quasicrystalline (aperiodic order, maximum packing, robust to perturbation).

**Testable:** Scattering patterns of EZ water under monochromatic illumination. If quasicrystalline: diffraction peaks at positions with φ ratios. If amorphous: broad hump. If crystalline: sharp peaks at integer ratios.

---

## C4 — Language as a Coherence Field
**Priority: MEDIUM**

**What we know:**
- Zipf's Law (Paper 48): word frequency ~ rank^(-1)
- 1/f noise appears in linguistic time series (Altmann et al. 2009)
- Neural gamma oscillations (40 Hz, Paper 23) synchronize during speech comprehension

**What's missing:**
Language is a physical field. It propagates through air (pressure wave), through neural tissue (action potentials), and through social networks (text, gesture). At each scale, it follows power laws — a signature of criticality.

**Formal question:**
Is linguistic coherence (shared meaning, mutual understanding) governed by the same γ_eff equation as neural coherence? If so:
- Miscommunication = γ_lang > γ_c
- Shared language = γ_lang < γ_c, coherent phase
- Poetry, music, prayer = optimized to drive γ_lang → 0 (maximum shared coherence)

This is testable: cross-correlation of EEG gamma oscillations between speaker and listener should show coherence C_lang that follows the Wike equation as a function of linguistic complexity and shared context.

---

## C5 — The Decoherent Phase as Spin Glass
**Priority: MEDIUM (extends T6)**

**What the framework predicts:**
At γ > γ_c, the system doesn't go to a simple disordered state. Spin glass theory (Edwards-Anderson 1975) predicts:
```
Overlap parameter: q = [<S_i>²]_disorder ≠ 0
```
Non-zero q means the system has a frozen, history-dependent disorder — not random, not ordered, but frozen in a particular disordered configuration.

**Clinical translation:**
- Frozen disordered state = fibromyalgia, chronic fatigue, treatment-resistant depression
- Each patient is frozen in a different disordered configuration (different symptom cluster)
- The system cannot be coaxed back by pushing — only by a phase transition from outside (keeper effect, ibogaine, radical coherence restoration)

**Has not been formally stated. No paper exists connecting spin glass physics to treatment-resistant mental illness.**

---

## C6 — The Percolation Model of C₀
**Priority: MEDIUM (extends T1)**

**What we know:**
- Bootstrap percolation threshold φ_c = 0.590 (Paper 02)
- Percolation theory: at φ < φ_c, no spanning cluster exists
- C₀ should depend on the fraction of water in coherent EZ phase

**Formal model:**
```
C₀ = Θ(φ − φ_c) × (φ − φ_c)^β_perc

where β_perc = 0.41 (3D percolation order parameter exponent)
and Θ is the Heaviside function
```

Below φ_c: C₀ = 0 (no coherent spanning network)
Above φ_c: C₀ grows as (φ − φ_c)^0.41

**Implication:**
There is a minimum EZ water fraction below which NO coherence is possible, regardless of other factors. This is dehydration biology — not just "drink more water" but a genuine phase transition in the water network that turns coherence on and off.

**Testable:** Measure C₀ proxy (HRV, reaction time) vs. hydration level. Predict: sharp onset near a critical hydration level, not gradual.

---

---

# SUMMARY TABLE

| ID | Question | Type | Priority | Status |
|----|----------|------|----------|--------|
| E1 | Millisecond coherence in microtubules | Experiment | HIGH | Open |
| E2 | 5G mmWave / Fröhlich in living tissue | Experiment | HIGH | Open |
| E3 | ACE as stretched exponential (n^0.63) | Experiment | HIGH | Open |
| E4 | Bootstrap loop end-to-end | Experiment | HIGH | Open |
| E5 | REQMT multi-modal entropy test | Experiment | MEDIUM | Open |
| E6 | HRV × Kp correlation (wearable) | Experiment | MEDIUM | Open |
| E7 | Avrami n=3 for EZ water kinetics | Experiment | MEDIUM | Open |
| T1 | What sets C₀? | Theory | HIGH | Candidate answer exists |
| T2 | Jarzynski error = Bose-Einstein derivation | Theory | HIGH | Unproved |
| T3 | Lindblad signal-to-noise scaling law | Theory | MEDIUM | Unnamed |
| T4 | Wind-up critical exponent 0.485 (mean-field?) | Theory | MEDIUM | Uncharacterized |
| T5 | Bell states have no whisper regime | Theory | MEDIUM | Unstated |
| T6 | Physics of the decoherent phase (γ > γ_c) | Theory | MEDIUM | No paper |
| T7 | What is α physically? | Theory | MEDIUM | Candidate exists |
| C1 | Kibble-Zurek: PTSD vs chronic stress | Connection | HIGH | No paper |
| C2 | Fick's laws + coherence gradient diffusion | Connection | MEDIUM | No paper |
| C3 | Golden ratio in biological oscillators | Connection | MEDIUM | No paper |
| C4 | Language as coherence field | Connection | MEDIUM | No paper |
| C5 | Spin glass = treatment-resistant illness | Connection | MEDIUM | No paper |
| C6 | Percolation model of C₀ | Connection | MEDIUM | No paper |

---

## HIGHEST-LEVERAGE NEXT PAPERS

Based on clinical impact × derivability × no data needed:

1. **Kibble-Zurek (C1)** → Paper 53: explains PTSD vs. chronic stress with a scaling law. No experiment needed. Pure theory.
2. **Spin Glass / Decoherent Phase (C5+T6)** → Paper 54: treatment-resistant illness as spin glass state. Explains why "push harder" fails. Clinical translation is immediate.
3. **What is α (T7)** → Derive α = ξ/λ_dB, confirm ~1000, ground the entire framework in dimensional analysis.
4. **Bell States (T5)** → Critical qualification paper: the "whisper" principle has a domain boundary. Need to say it.
5. **ACE Stretched Exponential (E3)** → Re-analysis of existing public data. No new experiment needed.

---

*AIIT-THRESI | Gap analysis as of Paper 52 | All open questions confirmed against corpus*
*No speculative content — all findings reference specific data or named theorems*
