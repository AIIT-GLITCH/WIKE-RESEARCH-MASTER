# PAPER 46: THE LEAST ACTION PRINCIPLE IS THE WIKE COHERENCE LAW
## All of Physics Derives from One Principle. So Does Coherence.
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"Coherence is what happens when the system finds the path. γ_c is the noise threshold beyond which the path cannot be found."*

---

## Abstract

Hamilton's Principle of Least Action (δS = 0) is the deepest principle in physics. All of classical mechanics, electrodynamics, quantum mechanics, general relativity, and quantum field theory follow from it. A particle takes the path that extremizes the action S = ∫L dt. In Feynman's path integral formulation of quantum mechanics, a particle takes all paths simultaneously — but paths near the least-action path interfere constructively (coherence), while paths far from it interfere destructively (decoherence). This paper makes explicit what has never been stated: **coherence IS successful least-action path-finding in the presence of noise. Decoherence IS failure to find the least-action path. γ_c is the noise threshold at which the path integral's saddle point ceases to exist.** The Wike Coherence Law is the Principle of Least Action expressed in the language of open quantum systems.

---

## 1. The Principle of Least Action

Hamilton (1833) stated the variational principle underlying all classical mechanics:

```
The actual path taken by a physical system between two states
is the one for which the action S = ∫L dt is stationary (δS = 0)

where L = T - V (kinetic minus potential energy, the Lagrangian)
```

Lagrangian mechanics, Hamiltonian mechanics, Noether's theorem (symmetries → conservation laws), Maxwell's equations, Einstein's field equations, the Standard Model — all derivable from this one principle.

**Why does it work?** Feynman's answer: because quantum mechanics is deeper than classical mechanics, and quantum mechanics literally sums over all paths. The classical path is the saddle point of the sum.

---

## 2. Feynman Path Integrals: All Paths, Weighted by Phase

Feynman (1948) formulated quantum mechanics as:

```
⟨x_f|x_i⟩ = ∫ D[x(t)] exp(iS[x]/ℏ)

The amplitude is a sum over ALL paths x(t) from x_i to x_f.
Each path contributes a phase factor exp(iS/ℏ).
```

**The key:** paths near the stationary action point (classical path) have slowly varying phase → they interfere **constructively** → they contribute the most to the amplitude.

Paths far from the classical path have rapidly oscillating phase → they interfere **destructively** → they cancel.

**Coherence in the path integral IS the constructive interference of near-classical paths.**
**Decoherence IS the destruction of that constructive interference by environmental noise.**

When the environment introduces random phase shifts to each path — through thermal fluctuations, measurements, or interactions — the delicate constructive interference is disrupted. The paths no longer add coherently. The classical least-action path loses its privileged status.

**This is exactly what γ_eff measures:** the rate at which the environment randomizes the phases of quantum paths, destroying their constructive interference.

---

## 3. γ_c Is Where the Saddle Point Disappears

The action S[x] has a saddle point at the classical path. The path integral is dominated by the neighborhood of this saddle point — the stationary phase region.

When environmental noise (γ_eff) is small: the saddle point dominates. The system follows near-classical paths. Coherence is maintained.

When γ_eff = γ_c: the noise is comparable to the action differences between paths. The saddle point region begins to wash out. The path integral transitions from saddle-point dominated to diffuse.

When γ_eff > γ_c: no path is privileged. The interference pattern is destroyed. The system cannot find the least-action path. Decoherence is complete.

```
γ_eff < γ_c:  Saddle point intact → constructive interference → coherence
              C = C₀ · exp(-αγ_eff) > C_critical

γ_eff = γ_c:  Saddle point marginal → transition → C = C₀/e

γ_eff > γ_c:  No saddle point → all paths equally weighted → decoherence
              C → 0
```

**The Wike Coherence Law is the path integral's saddle-point condition, expressed in terms of measurable decoherence rates.**

---

## 4. Why Pi Appears Everywhere (The Path Integral Answer)

The SINGULARITY_IS_PI_DATA and CIRCLES_ALL_THE_WAY_DOWN documents establish that pi governs coherence thresholds at every scale. The path integral explains why.

The saddle-point approximation of the path integral produces a Gaussian integral:

```
∫ D[x] exp(iS/ℏ) ≈ exp(iS_cl/ℏ) × ∫ D[η] exp(i/ℏ ∫ η·(d²S/dx²)·η dt)

The Gaussian integral produces: (det(-d²S/dx²))^(-1/2)

This determinant involves eigenvalues of the second variation of S.
For oscillatory systems: eigenvalues are ω²_n — the squared frequencies.
The product ∏ ω_n generates factors of π through Γ(1/2) = √π.
```

**Pi enters the path integral through the Gaussian saddle-point correction.** Every coherent oscillation contributes a factor involving π. The Wike Universality Theorem (γ_c = ω/2πα) is the direct path integral result: **the factor of 2π comes from the Gaussian integral over one complete oscillation cycle.** The circle completes. The saddle point exists. Coherence is maintained.

When γ_eff > γ_c, the oscillation cannot complete — the Gaussian integral's saddle point is in the complex plane rather than on the real axis. The constructive interference requires a full 2π phase accumulation. If the system cannot complete 2π before decoherence destroys the phase, the saddle point is lost.

**π is the geometry of coherence. The Wike Universality Theorem is the path integral's condition for coherence survival.**

---

## 5. The Principle of Least Action Restated for Biology

The Principle of Least Action as it applies to biological coherence:

**Classical version:** A physical system evolves along the path that minimizes action.

**Biological coherence version (Wike 2026):** A biological system maintains coherence as long as its quantum states can find the least-action path through environmental noise. The coherence threshold γ_c is the noise level above which the least-action path-finding fails. Below γ_c: the system evolves efficiently toward its natural attractor. Above γ_c: the path integral loses its saddle point and the system evolves diffusively (classically, incoherently) toward maximum entropy.

**Medical restatement:** Disease is the failure to find the least-action path. Inflammation, chronic pain, Alzheimer's, cardiovascular disease — all represent biological systems operating above γ_c where the constructive interference of biological processes has been disrupted by noise. The therapy in every case: reduce γ_eff below γ_c so the system can find its natural path again.

---

## 6. Noether's Theorem and the Conservation Laws of Coherence

Noether's theorem (1915): every continuous symmetry of a physical system corresponds to a conservation law.

- Time symmetry → conservation of energy
- Spatial symmetry → conservation of momentum
- Rotational symmetry → conservation of angular momentum

In the path integral framework: these symmetries are preserved when the saddle point exists — when coherence is maintained. When γ_eff > γ_c and the saddle point is destroyed, **symmetries are broken locally**:

- Time-translational symmetry breaks → energy is no longer conserved locally (dissipation)
- The system enters a fundamentally irreversible state

**The Wike Coherence Law is the condition for preserving Noether's symmetries in open quantum systems.** Coherence = symmetry preservation. Decoherence = symmetry breaking at the scale of the system.

This is why fever, malnutrition, trauma, and any other γ_eff elevation all feel qualitatively like "things falling apart" — they are, literally. The Noether symmetries that normally guarantee ordered biological dynamics are being broken by the destruction of the path integral's saddle point.

---

## 7. One Principle, All Scales

```
Principle of Least Action (δS = 0):
  → Classical mechanics (particles, planets, fluids)
  → Electrodynamics (light, fields)
  → General relativity (spacetime curvature)
  → Quantum mechanics (path integrals, uncertainty)
  → The Standard Model (gauge symmetries)
  → The Wike Coherence Law (γ_c, coherence threshold, biological order)

All of physics from one principle.
All of biology from one threshold.
One equation. Every scale.
```

The Wike Coherence Law is not a separate law from physics. It IS physics — specifically, it is the least action principle applied to open quantum systems in the presence of environmental decoherence. It was always there. Nobody had written it in the language of γ_eff before.

God is good. All the time. Them beans though.

---

## References

1. Hamilton, W. R. (1833). On a general method of expressing the paths of light. *Dublin University Review*, 795-826.
2. Feynman, R. P. (1948). Space-time approach to non-relativistic quantum mechanics. *Reviews of Modern Physics*, 20(2), 367-387.
3. Noether, E. (1918). Invariante Variationsprobleme. *Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen*, 235-257.
4. Zinn-Justin, J. (2002). *Quantum Field Theory and Critical Phenomena* (4th ed.). Oxford University Press.
5. Wike, R. D. (2026). AIIT-THRESI Research Papers 01-45. Council Hill, Oklahoma.

---
*Rhet Dillard Wike | AIIT-THRESI | Council Hill, Oklahoma | March 30, 2026*
