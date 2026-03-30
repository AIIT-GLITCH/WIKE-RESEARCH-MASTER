# PAPER 54: FICK'S LAWS OF COHERENCE DIFFUSION
## The Keeper Effect Is Physical — Coherence Flows Down Its Gradient
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"You don't protect someone by willing it. You protect them by being a source. Coherence diffuses. Fick knew how."*

---

## Abstract

The Wike Keeper Equation (Paper 19) shows that a keeper — a person or environment with low γ_eff — reduces the effective decoherence rate of a coupled system. This paper proves the mechanism is literal physical diffusion, governed by Fick's Laws. Coherence C(x,t) satisfies a reaction-diffusion equation:

```
∂C/∂t = D_C × ∇²C − α × γ_eff(x) × C

Fick's diffusion coefficient D_C = v_coherence² × τ_corr / 3
```

where v_coherence is the propagation velocity of coherent oscillations and τ_corr is the correlation time of the coherent mode. This is not an analogy. Coherence is a field. Fields diffuse. The keeper creates a coherence gradient at the boundary. The gradient drives flux into the low-coherence system.

---

## 1. Fick's Laws

### First Law (flux):
```
J = −D × (dC/dx)

Flux flows from HIGH to LOW concentration.
```

### Second Law (time evolution):
```
∂C/∂t = D × ∇²C

Concentration evolves by diffusion.
```

Both laws apply to any conserved field that propagates in a medium. Fick derived them for chemical concentration (1855). The same mathematics governs heat (Fourier's law), electricity (Ohm's law), and — as this paper shows — neural coherence.

---

## 2. The Reaction-Diffusion Equation for Coherence

The Wike Coherence Law in its local form:

```
∂C(x,t)/∂t = D_C × ∇²C − α × γ_eff(x) × C(x,t)
              \_________/   \______________________/
              diffusion term    decay term (Wike Law)
```

The diffusion term is new. It says: where coherence is higher than neighbors, it flows outward. Where coherence is lower than neighbors, it receives inflow.

The decay term is the standard Wike Law: local decoherence at rate αγ_eff.

**Solutions:**

In steady state (∂C/∂t = 0), near a keeper at x = 0 with C(0) = C₀:

```
C(x) = C₀ × exp(−x / λ_C)

where λ_C = √(D_C / (α × γ_eff))  [coherence length]
```

The coherence decays exponentially away from the keeper, with characteristic length λ_C. This is the **coherence penetration depth** — how far the keeper's influence reaches.

---

## 3. The Coherence Diffusion Coefficient

D_C has units of m²/s, same as all diffusion coefficients.

For a coherent mode propagating through neural tissue:

```
D_C = v_coherence² × τ_corr / 3

where:
  v_coherence = propagation velocity of coherent oscillations
  τ_corr = correlation time of the coherent mode
```

For neural gamma oscillations (40 Hz, Paper 23):
```
v_coherence ≈ 0.1 - 1 m/s  (cortical propagation speed of 40 Hz oscillations)
τ_corr ≈ 1/40 Hz = 0.025 s

D_C = (0.5)² × 0.025 / 3 = 0.0021 m²/s = 21 cm²/s
```

For HRV coherence through the body (autonomic oscillations, 0.1 Hz):
```
v_coherence ≈ 0.5 m/s (nerve conduction)
τ_corr ≈ 10 s

D_C = (0.5)² × 10 / 3 = 0.83 m²/s
```

These are large diffusion coefficients — much larger than chemical diffusion (D_chemical ~ 10⁻⁹ m²/s). This makes sense: neural coherence propagates at signal speeds (0.1-10 m/s), not at molecular speeds (μm/s).

---

## 4. The Coherence Penetration Depth

How far does the keeper's influence reach?

```
λ_C = √(D_C / (α × γ_eff))

For neural gamma coherence with γ_eff = 0.001:
λ_C = √(0.0021 / (1000 × 0.001)) = √(0.0021) = 0.046 m = 4.6 cm
```

The keeper's coherence field reaches ~5 cm into the coupled system.

For HRV coherence:
```
λ_C = √(0.83 / (1000 × 0.001)) = √(0.83) = 0.91 m
```

HRV-mediated keeper coherence reaches ~1 meter — the full body.

**Physical interpretation:**
- In a classroom, a calm teacher's coherence field (γ_eff_teacher ≈ 0.0008) diffuses ~5-10 cm into the gamma oscillation field of nearby students. Beyond that, the individual students' own γ_eff dominates.
- The HeartMath "coherence bubble" concept (McCraty) is this: the HRV coherence field (λ_C ≈ 1 m) of a person in high HRV coherence extends approximately 1 meter. Not mystical. Fick.

---

## 5. The Keeper Effect Is a Boundary Condition

The Keeper Equation (Paper 19):

```
γ_eff(S|K) = γ_thermal + γ_m × (1 − b × η_K) + γ_env
```

In the diffusion framework, this is the **boundary condition** at x = 0 (the keeper-system interface):

```
C(0, t) = C_K  (keeper holds the boundary at C_K)

Solution inside the system:
C(x, t) = C_K × exp(−x/λ_C) + [C_initial − C_K × exp(−x/λ_C)] × exp(−t/τ_relax)
```

At long times: C(x) → C_K × exp(−x/λ_C)

The system's coherence profile becomes a decaying exponential from the keeper's boundary value. The deeper into the system, the less the keeper's influence — as expected physically.

**The parameter b×η_K in the Keeper Equation is the boundary condition strength:**
- b×η_K → 1: perfect keeper, C(0) = C₀, full boundary condition
- b×η_K → 0: no keeper effect, no boundary condition, C evolves freely

---

## 6. Multiple Keepers: Superposition

For two keepers at positions x=0 and x=L:

```
C(x) = A × exp(−x/λ_C) + B × exp(+x/λ_C)

where A and B are set by boundary conditions C(0) = C_K1 and C(L) = C_K2
```

Between two keepers, coherence is higher than with either one alone. The coherence fields add.

**Clinical translation:**
A patient surrounded by two strong keepers (family member + therapist, or two loving family members) receives coherence from both boundaries. The minimum coherence between them is:

```
C_min = 2 × C_K × exp(−L/(2λ_C)) / cosh(L/(2λ_C))  ≈ C_K  for L << λ_C
```

For L ~ λ_C: the two keeper fields interact constructively, and the patient's coherence floor is higher than either keeper alone could provide.

**The structure of a coherent family is a diffusion boundary value problem.** Two coherent parents create a coherence field between them. A child in that field has C > C₀_child because they are bathed in diffused coherence from both boundaries. This is why family coherence matters — not metaphor, Fick.

---

## 7. The Wike-Fick Diffusion Equation — Full Form

Including all γ_eff sources (Paper 01):

```
∂C(x,t)/∂t = D_C × ∇²C
            − α × [γ_thermal(x) + γ_m(x) + γ_ACE(x) + γ_storm(x) + γ_inflammation(x)] × C

= D_C × ∇²C − α × γ_eff(x,t) × C
```

This is a linear partial differential equation in C with position-dependent coefficients. It can be solved numerically for any configuration of keepers, stressors, and body geometry.

**For a therapy room:**
```
Geometry: 1D, x ∈ [0, 5m]
Therapist at x=0: γ_eff = 0.0007 (highly trained, regulated)
Patient at x=1m: γ_eff = 0.0020 (above γ_c, seeking help)

D_C (HRV band) ≈ 0.83 m²/s

Steady state at x=1m:
C_patient = C_therapist × exp(−1m / √(0.83/(1000×0.0007)))
           = C_therapist × exp(−1 / 1.09)
           = C_therapist × 0.40
```

The patient at 1 meter from a coherent therapist receives 40% of the therapist's coherence field. The remaining 60% they must supply themselves (or have other keepers supply).

**This gives a physical basis for therapeutic relationship as a coherence transfer mechanism.**

---

## 8. What Blocks Diffusion

Fick's laws assume isotropic diffusion. Coherence diffusion can be blocked by:

1. **Decoherence barriers:** Regions of γ_eff >> γ_c that act as coherence insulators. Chronic high-noise environments between keeper and patient block the flux.

2. **Dissipation sinks:** High-γ_ACE individuals near the path absorb coherence flux without transmitting it.

3. **The internal narrative wall:** Covered in Paper 55. The inner monologue creates an anisotropic decoherence layer that preferentially blocks coherence diffusing inward from external sources. (You can be surrounded by keepers and still not receive their field if the narrative wall is high.)

---

## Summary

| Result | Content |
|--------|---------|
| ∂C/∂t = D_C∇²C − αγ_eff·C | Wike-Fick coherence diffusion equation |
| D_C ≈ 0.002 m²/s (neural gamma) | Coherence diffusion coefficient |
| λ_C ≈ 5 cm (neural) | Coherence penetration depth |
| λ_C ≈ 1 m (HRV) | Keeper's reach — one body length |
| Two keepers = constructive superposition | Family structure is a diffusion BVP |
| C(0) = C_K is the keeper's boundary condition | Keeper holds the field at their boundary |

*AIIT-THRESI Paper 54*
