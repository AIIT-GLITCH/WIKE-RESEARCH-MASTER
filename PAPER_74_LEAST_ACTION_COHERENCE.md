# PAPER 74: FERMAT'S PRINCIPLE AND THE LEAST-ACTION BASIS OF COHERENCE
## γ_c Is the Noise Threshold Beyond Which the Least-Action Path Cannot Be Found
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"A coherent system is one that found the path. γ_c is the noise level at which the path is lost. The Principle of Least Action has a decoherence analog."*

---

## Abstract

Fermat's Principle (1662): light takes the path of least time. Hamilton's Principle of Least Action (1834): every physical system evolves along the path that makes the action S = ∫L dt stationary. Feynman's path integral (1948): a quantum system takes ALL paths simultaneously, with phases that interfere — paths near the classical (least-action) path interfere constructively (coherence), all others interfere destructively (decoherence).

The mapping to the Wike framework is exact:

```
Coherence = constructive interference = system found the least-action path
γ_eff < γ_c = noise is small enough that path coherence is maintained
γ_c = the noise level at which the least-action path is no longer identifiable
γ_eff > γ_c = all paths equally represented → incoherent sum → collapse
```

The Berry phase −π at γ_c (Papers 01, 15) is the geometric phase accumulated along the path integral at exactly the noise level where the saddle point of the action ceases to exist. The singularity is where the path is lost.

---

## 1. Fermat's Principle → Hamilton's Principle → Feynman Path Integral

**Fermat (1662):** Among all paths between two points, light follows the path of least time.

**Hamilton (1834):** For any mechanical system, the actual trajectory between times t₁ and t₂ is the one that makes S stationary:

```
δS = 0    where   S = ∫_{t₁}^{t₂} L(q, q̇, t) dt

L = T − V   (kinetic minus potential energy)
```

**Feynman (1948):** For a quantum particle, the amplitude to go from x₁ to x₂ is:

```
K(x₂, t₂; x₁, t₁) = ∫ D[x(t)] × exp(iS[x]/ħ)

Integral over ALL paths, each weighted by exp(iS/ħ)
```

**Constructive interference:** Paths near the classical path (δS ≈ 0) have phases that differ by δφ = δS/ħ ≈ 0, so they interfere constructively. The system's probability amplitude peaks at the classical trajectory.

**Destructive interference:** Paths far from the classical path have wildly varying phases that average to zero. They cancel.

**Coherence = the constructive interference exists.** The classical path = least-action path = the path of coherence.

---

## 2. Decoherence as Path Loss

Environmental noise introduces a random phase kick to each path:

```
K_noisy(x₂; x₁) = ∫ D[x(t)] × exp(iS[x]/ħ) × exp(iΦ_noise[x])

where Φ_noise[x] = ∫ dξ(x(t)) × dW(t)  (random environmental coupling)
```

For a noise process with spectral density J(ω) (Caldeira-Leggett model, Paper 57):

```
⟨exp(iΦ_noise[x] − iΦ_noise[x'])⟩ = exp(−Γ[x, x'])

where Γ[x, x'] = ∫₀^T dt dt' K(t-t') (x(t) − x'(t))(x(t) − x'(t'))
and K(τ) = ∫ dω J(ω) cos(ωτ)/π (noise kernel)
```

The coherence is the off-diagonal density matrix element:

```
ρ(x, x') = ∫ Dx Dx' × exp(i(S[x] − S[x'])/ħ) × exp(−Γ[x, x'])
```

At γ_eff < γ_c: Γ is small, the path integral is dominated by paths near x = x', and the coherence persists.

At γ_eff = γ_c: Γ grows large enough that the saddle point of the path integral (the least-action path) is swamped by the noise. The constructive interference peak vanishes.

At γ_eff > γ_c: Γ >> 1 for all non-diagonal paths, ρ(x, x') → 0 for x ≠ x' → classical incoherent mixture.

**γ_c is where Γ = 1: the noise-induced phase shift equals the action-induced phase coherence.**

---

## 3. Derivation of γ_c from the Action Principle

The condition for coherence maintenance:

```
The path integral is coherent when:
  Γ[x_cl, x'] < 1  for x' near x_cl

where x_cl is the classical (least-action) path
```

For a Lindblad dephasing model, the decoherence functional:

```
Γ(t) = 2γ × ∫₀^t dt' ∫₀^{t'} dt'' K(t' − t'') ≈ 2γt   [for Markovian noise]
```

Coherence maintained when Γ < 1:

```
2γt < 1 → γ < 1/(2t)

This is the Wike Measurement Window (Paper 68): γ_opt = 1/(2t)
```

Over the biological coherence time t_bio ≈ 1/(2γ_c):

```
t_bio = 1/(2 × 0.0016) = 312.5 simulation time units
```

The biological coherence time is the time over which the path integral remains coherent at γ = γ_c. This is the maximum integration time for the Feynman path integral before noise overwhelms the action.

---

## 4. The Berry Phase −π as a Topological Action

The Berry phase (Papers 01, 15) of −π at γ = γ_c is a geometric phase accumulated when the system traverses a closed path in parameter space. In path integral language:

```
φ_Berry = Im[ln ⟨ψ(T)|ψ(0)⟩] = Im[ln ∫ D[path] exp(iS/ħ)]

For a closed path in (γ_eff, C) parameter space at γ = γ_c:
φ_Berry = −π
```

This is the topological contribution to the action — the Wess-Zumino-Witten term in the effective field theory. It cannot be removed by smooth deformations of the path and is therefore robust.

**The Berry phase −π is the action of traversing the saddle point at γ_c.** It is the cost, in units of ħ, of the system losing its least-action path. The transition at γ_c costs exactly π radians of geometric phase — one half-turn in the parameter space of the coherence field.

This connects to Paper 56 (Golden Ratio): the vertex angle deficit in a Penrose tiling vertex is π/5, and the sum of all vertex deficits for a closed path in quasicrystalline geometry equals π. The geometry of the path integral at γ_c is Penrose-like — aperiodic, with π as the topological invariant.

---

## 5. The Principle of Least Action = The Wike Coherence Law

Restated:

**Classical Least Action:** δS = 0 → the system follows the unique classical path.

**Quantum Coherence:** Most paths contribute constructively near δS = 0. Decoherence destroys the interference.

**Wike Coherence Law (2026):** The coherent biological system follows the least-metabolic-cost path through its phase space (the path that minimizes the action S_bio = ∫(γ_eff − γ_c × Θ(C)) dt). This path is maintained when γ_eff < γ_c. When γ_eff > γ_c, the system can no longer find the minimum-action path and evolves incoherently.

```
Fermat's Principle (geometric optics):
  Light finds the path of least time.

Hamilton's Principle (mechanics):
  A particle finds the path of stationary action.

Wike's Principle (biology):
  A coherent biological system finds the path of minimum decoherence.
  It can do this when γ_eff < γ_c.
  It cannot do this when γ_eff > γ_c.
  γ_c is the noise threshold where the least-decoherence path is lost.
```

---

## 6. Application: The Path of Least Suffering

In clinical terms, the "path of least action" for a person navigating chronic pain or illness is the path through state space that minimizes cumulative γ_eff exposure.

This is not:
- The path of least total pain (that might require high γ_eff surgery/intervention)
- The path of least effort (avoidance → behavioral fragmentation, Paper 52 Anti-Zeno effect)

It is: the path that keeps the system's coherence field closest to the attractor at γ_baseline, spending minimum time near γ_c.

**Therapeutic implication:** The optimal treatment trajectory is the **geodesic in coherence phase space** — the path of minimum action from the current state (high γ_eff, approaching γ_c) to the target state (γ_eff → γ_baseline). The geodesic equation in the (C, γ_eff) space gives:

```
Optimal treatment rate: dγ_eff/dt = −(γ_eff − γ_baseline) × κ(γ_eff)

where κ(γ_eff) ~ (γ_c − γ_eff)^1.2372  (Le Chatelier restoring constant, Paper 69)
```

Too fast a return (high dγ_eff/dt) = Kibble-Zurek defects (Paper 53). Too slow = system remains near γ_c, vulnerable to crossing. The geodesic is the optimal rate.

---

## Summary

```
Fermat's Principle          →  least time
Hamilton's Principle        →  stationary action (δS = 0)
Feynman Path Integral       →  constructive interference near classical path
Wike Coherence Law          →  coherence = system found the least-action path

γ_c: noise level where saddle point of path integral vanishes
     Γ(t) = 1 at γ_c = noise-action balance point
     Berry phase −π = topological cost of losing the path

Clinical geodesic: dγ_eff/dt = −(γ_eff − γ_baseline) × (γ_c − γ_eff)^1.2372
                   (too fast = Kibble-Zurek defects, too slow = near-cliff vulnerability)
```

**Coherence is what happens when a system successfully minimizes its action against environmental noise. γ_c is the noise level beyond which the action cannot be minimized.**

*AIIT-THRESI Paper 74*
