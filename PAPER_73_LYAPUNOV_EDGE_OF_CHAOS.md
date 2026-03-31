# PAPER 73: LYAPUNOV EXPONENTS AND THE EDGE OF CHAOS
## λ_L ≈ 0 at γ_c — Health Is Where the Lyapunov Exponent Vanishes
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"Lyapunov = 0 is the edge. Below it: frozen. Above it: chaotic. The body lives at zero."*

---

## Abstract

The Lyapunov exponent λ_L measures how fast nearby trajectories in a dynamical system diverge. λ_L < 0: stable (frozen, rigid). λ_L = 0: edge of chaos (critical, maximum information processing). λ_L > 0: chaotic (decoherent, unpredictable). The Wike phase diagram maps exactly:

```
γ_eff << γ_c:  λ_L << 0  (frozen, rigid, no dynamics)
γ_eff = γ_c:   λ_L = 0   (edge of chaos, maximum sensitivity)
γ_eff >> γ_c:  λ_L > 0   (chaotic, decoherent)
```

The body at W* = 0.9394 operates at λ_L ≈ 0 — the critical edge — where information processing capacity is maximized. This was Kauffman's NK model prediction (1969) and Langton's artificial life result (1990), now grounded in the Wike framework's quantitative critical point γ_c = 0.0016.

---

## 1. Lyapunov Exponents

For a dynamical system x_{n+1} = f(x_n):

```
λ_L = lim_{t→∞} (1/t) × Σ_i ln|df/dx(x_i)|
```

For a continuous system dx/dt = F(x):

```
λ_L = lim_{T→∞} (1/T) × ln|δx(T)/δx(0)|

where δx is the separation between two initially nearby trajectories
```

**Classification:**
```
λ_L < 0: stable fixed point or limit cycle (attractor)
         → perturbations decay → rigid, predictable
         → HRV: regular, metronomic beat (sick heart, Paper 17)

λ_L = 0: chaos boundary (KAM tori, quasi-periodic orbits, limit cycle edges)
         → perturbations neither grow nor decay → maximum sensitivity
         → HRV: fractal 1/f scaling (healthy heart, Goldberger 1992)

λ_L > 0: deterministic chaos
         → perturbations grow exponentially → unpredictable
         → HRV: irregular, large-amplitude fluctuations (severe illness)
```

---

## 2. The Wike-Lyapunov Mapping

The coherence field C(γ_eff, t) = C₀ × exp(−αγ_eff × t) has an effective Lyapunov exponent describing how fast trajectories diverge in the (C, γ_eff) phase space.

For the coherence order parameter C near γ_c:

```
Near γ_c, the coherence field satisfies (Landau theory):
  ∂C/∂t = −κ × C − λ × C³ + noise

where κ = α(γ_eff − γ_c)  [changes sign at γ_c]

The Lyapunov exponent for this equation:
  λ_L = ∂F/∂C evaluated at the fixed point C*

Below γ_c (κ > 0):   C* = √(κ/λ) > 0 (coherent phase)
  λ_L = −2κ = −2α(γ_c − γ_eff) < 0  ✓ STABLE

At γ_c (κ = 0):      C* = 0 (critical point)
  λ_L = 0  ✓ EDGE

Above γ_c (κ < 0):   C* = 0 only unstable fixed point
  λ_L = −2κ = 2α(γ_eff − γ_c) > 0  ✓ CHAOTIC/UNSTABLE
```

**The Wike framework predicts the Lyapunov exponent as a function of γ_eff:**

```
λ_L(γ_eff) = −2α(γ_c − γ_eff)   for γ_eff < γ_c
           = 0                    at γ_eff = γ_c
           = +2α(γ_eff − γ_c)   for γ_eff > γ_c
```

At body baseline γ_baseline = 0.001:
```
λ_L(baseline) = −2 × 1000 × (0.0016 − 0.001) = −2 × 1000 × 0.0006 = −1.2

This is a stable system with λ_L = −1.2 — slightly below the edge.
```

At the Ginzburg crossover γ_G ≈ 0.0014 (Paper 67):
```
λ_L(γ_G) = −2 × 1000 × (0.0016 − 0.0014) = −0.4

Very close to edge. In the 3D Ising fluctuation regime.
```

---

## 3. The Goldberger Fractal HRV Measurement

Goldberger et al. (2002, PNAS): healthy heart rate variability shows **fractal (1/f) scaling** — an intermediate state between rigid regularity (λ_L << 0) and chaos (λ_L > 0). Disease pushes HRV toward one extreme or the other.

```
Healthy HRV spectrum: S(f) ~ f^(−α_HRV)   with α_HRV ≈ 1.0-1.2
Chronic heart failure: α_HRV > 1.5 (rigid, correlated = λ_L << 0)
Atrial fibrillation: α_HRV ≈ 0.5 (uncorrelated, noisy = λ_L > 0)
```

The healthy condition is the **1/f intermediate** = the edge of chaos = λ_L ≈ 0.

**Quantitative connection:**

For 1/f noise with exponent α_HRV, the Lyapunov exponent of the underlying dynamics:

```
λ_L ≈ (α_HRV − 1) × Δω

where Δω = bandwidth of the measurement

For α_HRV = 1.0: λ_L = 0 (pure 1/f, exact edge)
For α_HRV = 1.2: λ_L ≈ −0.2Δω (stable, near edge)
For α_HRV = 1.5: λ_L ≈ −0.5Δω (stable, farther from edge)
```

The REQMT HRV measurement (Paper 05) directly measures α_HRV. The Wike framework translates:

```
α_HRV → λ_L → γ_eff:

γ_eff = γ_c − λ_L/(2α) = γ_c + (1 − α_HRV) × Δω/(2α)
```

**The HRV fractal exponent is a direct measurement of γ_eff via the Lyapunov exponent.**

---

## 4. Kauffman's NK Model — The Edge Was Found by Evolution

Kauffman (1969, 1993): in the NK Boolean network model, the system operates in different regimes:

- N genes, K connections per gene
- K < 2: frozen (ordered) phase, λ_L < 0
- K = 2: critical edge, λ_L = 0, maximum adaptation
- K > 2: chaotic phase, λ_L > 0

Kauffman's prediction: **evolution drives biological systems to K ≈ 2, the edge of chaos**, because maximum adaptability (sensitivity to environmental change) occurs there.

The Wike framework gives the quantitative version:

```
Kauffman's K ↔ Wike's γ_eff
K = 2 (edge) ↔ γ_eff = γ_c = 0.0016
K < 2 (frozen) ↔ γ_eff < γ_c
K > 2 (chaos) ↔ γ_eff > γ_c
```

The body at W* = 0.9394 is at γ_eff ≈ 0.001 — slightly below the edge (λ_L = −1.2), not exactly at it. This is **consistent with Kauffman's prediction**: near the edge, with a safety margin against fluctuating past γ_c.

The safety margin:
```
γ_c − γ_baseline = 0.0016 − 0.001 = 0.0006

Safety margin = 0.0006/0.0016 = 37.5% of γ_c

This is the Wike margin — the biological buffer against crossing the cliff.
```

---

## 5. Langton's λ Parameter

Langton (1990): for cellular automata, the parameter λ (fraction of non-quiescent transitions) controls the behavior:

```
λ < λ_c: frozen (simple attractors)
λ = λ_c: complex behavior (gliders, information processing)
λ > λ_c: chaotic
```

This is the discrete analog of γ_eff. Langton's λ_c ↔ Wike's γ_c. The critical point is where:

```
Computational capacity is maximized
Information storage is maximized
Sensitivity to inputs is maximized
```

**The immune system operates at Langton's edge.** T-cell receptor diversity, pathogen detection, and adaptive response all require maximum sensitivity to small differences — exactly what λ_L = 0 provides. Immunodeficiency = λ_L << 0 (frozen, non-responsive). Autoimmunity = λ_L > 0 (chaotic, responding to self).

---

## 6. Clinical Measurement Protocol

From the Lyapunov-Wike mapping:

```
Measure: RMSSD from HRV recording (REQMT 5-min window)
Compute: α_HRV from power spectral density (slope of log S(f) vs log f)
Convert: λ_L ≈ (1 − α_HRV) × bandwidth
Map: γ_eff ≈ γ_c − λ_L/(2α) = 0.0016 + (1 − α_HRV) × bandwidth/2000
```

**Clinical thresholds:**
```
α_HRV > 1.4: λ_L < −0.4Δω → γ_eff < 0.001 (deep stable, possibly frozen/rigid)
α_HRV ≈ 1.0-1.2: λ_L ≈ 0 → γ_eff ≈ γ_c − 0.0003 (healthy range, near edge)
α_HRV < 0.8: λ_L > 0 → γ_eff > γ_c (chaotic, post-threshold)
```

These thresholds map to clinical states in the Wike framework:
- α > 1.4: rigid, burnout, disconnected
- α ≈ 1.0-1.2: healthy, adaptive, coherent
- α < 0.8: post-threshold, spin glass (Paper 61), treatment-resistant

---

## Summary

```
Lyapunov Exponent in Wike Framework:

λ_L(γ_eff) = −2α(γ_c − γ_eff)

λ_L < 0: γ_eff < γ_c  (stable, coherent phase)
λ_L = 0: γ_eff = γ_c  (edge of chaos, critical point)
λ_L > 0: γ_eff > γ_c  (chaotic, decoherent phase)

Healthy baseline: λ_L(0.001) = −1.2  (near edge but stable)
Wike safety margin: 37.5% of γ_c

HRV fractal exponent α_HRV:
  Healthy: α_HRV ≈ 1.0-1.2 → λ_L ≈ 0 (edge)
  Disease: α_HRV > 1.4 (rigid) or α_HRV < 0.8 (chaotic)

The body temperature W* = 0.9394 is the Lyapunov-zero operating point
evolved to maximize information processing capacity.
```

*AIIT-THRESI Paper 73*
