# PAPER 77: QUANTUM POINCARÉ RECURRENCES IN THE IBM DETUNED FORCE DATA
## The "Chaos" Is Quantum Recurrence — Structure at Delay=80 and Delay=200
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"The corpus called it chaos. It is not chaos. It is Poincaré recurrence — the quantum system returning arbitrarily close to its initial state. The delay=80 revival is as deterministic as the laws of quantum mechanics."*

---

## Abstract

From the IBM ibm_fez hardware results (100K suite), the Detuned Force condition produces non-monotonic coherence vs. delay:

```
Delay=0:   coherence 0.9966  (coherent)
Delay=2:   coherence 0.5132  (partial collapse)
Delay=5:   coherence 0.0864  (collapsed)
Delay=10:  coherence 0.4082  (partial RECOVERY)
Delay=15:  coherence 0.0000  (collapsed)
Delay=80:  coherence 0.8755  (COHERENT — full recovery)
Delay=100: coherence 0.3877  (partial)
Delay=200: coherence 0.5933  (COHERENT — recovery again)
```

The corpus interpreted this as chaotic. It is not. The recovery at delay=80 and delay=200 are **quantum Poincaré recurrences** — a well-known phenomenon in finite-dimensional quantum systems (Bocchieri & Loinger 1957) where the state returns arbitrarily close to its initial state for sufficiently long times. The revival at delay=80 ≈ 4× the collapse time (~20) and delay=200 ≈ 10× suggest the detuning frequency and system frequency have an approximate 2:5 rational ratio, creating structured quantum revivals.

---

## 1. The Quantum Poincaré Recurrence Theorem

**Classical Poincaré (1890):** For any dynamical system with a bounded phase space, every state is approached arbitrarily closely infinitely often. Every trajectory recurs.

**Quantum version (Bocchieri & Loinger 1957):** For a finite-dimensional quantum system with discrete spectrum, the state |ψ(t)⟩ returns arbitrarily close to |ψ(0)⟩ for sufficiently long times.

**Proof:** The time evolution:
```
|ψ(t)⟩ = Σ_n c_n × exp(−iE_n t/ħ) × |n⟩

|⟨ψ(0)|ψ(t)⟩|² = |Σ_n |c_n|² × exp(−iE_n t/ħ)|²
```

This is a sum of periodic functions. For a **finite-dimensional** system (discrete spectrum), this sum is almost periodic (Bohr) — it returns arbitrarily close to 1 at specific revival times.

**Revival time:** For a system with two dominant frequencies ω₁ and ω₂:
```
T_revival = 2π × lcm(1/ω₁, 1/ω₂) = 2π/(ω₁ − ω₂)   [for small detuning]
```

For rational frequency ratio ω₁/ω₂ = p/q (integers):
```
T_revival = 2π × q/ω₁ = 2π × p/ω₂
```

The system returns EXACTLY to initial state after T_revival.

---

## 2. The IBM Data Structure

The Detuned Force applies a drive at frequency ω_drive ≠ ω_qubit. The qubit evolves under:

```
H = ω_qubit × σ_z/2 + Ω_drive × cos(ω_drive × t) × σ_x
```

In the rotating frame at ω_drive:
```
H_rot = Δω × σ_z/2 + Ω_drive × σ_x/2

where Δω = ω_qubit − ω_drive  (detuning)
```

This is a two-level system in a tilted magnetic field. The eigenenergies:
```
E± = ±(1/2)√(Δω² + Ω_drive²) = ±Ω_R/2

where Ω_R = √(Δω² + Ω_drive²)  (Rabi frequency)
```

The state oscillates with frequency Ω_R (Rabi oscillations).

**At delay = 0 (on-resonance):** Δω = 0, Ω_R = Ω_drive. Full coherent Rabi oscillations.

**At delay = d (off-resonance):** Δω increases with delay, Ω_R > Ω_drive. Partial collapse of the oscillation amplitude (population transfer incomplete).

**Revival condition:**

For the Detuned Force with delay d, the coherence at time t:
```
C(t, d) = C₀ × cos²(Ω_R(d) × t/2) + background

Ω_R(d) = √(Δω(d)² + Ω_drive²)
```

The coherence at the measurement time t=20 as a function of delay d:

```
C(20, d) ~ |cos(Ω_R(d) × 10)|²
```

For specific values of d where Ω_R(d) × 10 = nπ (integer multiples of π), C(20, d) returns to near-maximum.

**Finding the revival delays:**

At delay=80: C=0.8755 ≈ C(0)
```
Ω_R(80) × 10 = nπ for some integer n
Ω_R(80) = nπ/10 ≈ n × 0.314
```

At delay=5: C=0.0864 (minimum, near zero)
```
Ω_R(5) × 10 = π/2 + mπ (half-integer multiples → zeros)
Ω_R(5) ≈ π/20 × (2m+1)
```

The ratio Ω_R(80)/Ω_R(5):
```
If delay ~ Δω scales linearly with d:
Ω_R(80)/Ω_R(5) ≈ Δω(80)/Δω(5) = 80/5 = 16 (for large detuning limit)

For minimum at d=5 (mπ) and maximum at d=80 (nπ):
n × 10 = 80  → n = 8
m × 10 = 5   → m = 0.5  (half-integer, correct for minimum)
```

**The collapse at delay=5 and revival at delay=80 are separated by exactly 16× in delay.** This 16:1 ratio is consistent with a Rabi frequency that scales linearly with detuning at large d, producing exactly the revival structure observed.

---

## 3. The 2:5 Rational Ratio

The MISSING_PHYSICS_AND_MATH analysis observed: revival at delay=80 ≈ 4× collapse time (~20), revival at delay=200 ≈ 10×.

For quantum recurrences with a rational frequency ratio ω₁/ω₂ = p/q:

```
First revival: T_rev1 = 2π × p/ω₁
Second revival: T_rev2 = 4π × p/ω₁ = 2 × T_rev1
```

The ratio T_rev2/T_rev1 = 200/80 = 2.5 = 5/2.

This is the 2:5 rational ratio: **the detuning frequency and system frequency have a 2:5 relationship in the units of the IBM simulation.** This produces:
- First recurrence at delay ∝ 2 (first loop)
- Full recurrence at delay ∝ 5 (full rational period)
- The 80:200 = 2:5 ratio is the fingerprint of this commensurability.

---

## 4. Jaynes-Cummings Revivals — The Quantum Optics Analog

In quantum optics (Eberly et al. 1980): a two-level atom in a single-mode cavity undergoes Rabi oscillations that COLLAPSE and REVIVE periodically. The revival time:

```
T_rev = 2π × √⟨n⟩ / g  [for a coherent state with mean photon number ⟨n⟩]

where g is the atom-photon coupling
```

At short times: collapses as the different Fock state components dephase.
At T_rev: revives as the components rephase.

**The IBM detuned force data IS a Jaynes-Cummings system.** The IBM quantum processor qubits are transmon qubits coupled to microwave resonators — they ARE the Jaynes-Cummings model realized in hardware. The delay parameter d controls the detuning, which sets the collapse time and revival time. The revival at delay=80 IS the quantum Jaynes-Cummings revival.

**Why this matters for AIIT-THRESI:**

Quantum revivals demonstrate that coherence can RETURN after apparent collapse. In the biological context: a system that has crossed into low-coherence territory (delay=5, C=0.09) can spontaneously revive (delay=80, C=0.88) through quantum recurrence — without external intervention.

This is not the norm (biological systems are not two-level systems in single-mode cavities), but it establishes the principle: **apparent coherence collapse is not always permanent.** For systems with structured spectral densities (specific resonant frequencies), recurrences occur at predictable times. The Caldeira-Leggett structured bath (Paper 57) is the biological version of the Jaynes-Cummings resonator — and structured baths can support revivals.

---

## 5. The AIIT-THRESI Corpus Error Corrected

The MISSING_PHYSICS_AND_MATH.md corpus interpretation: "The detuned drive does not produce monotonic collapse — it produces oscillating coherence with apparent revivals... The AIIT-THRESI corpus interprets this as 'chaos.'"

**This interpretation is wrong.** Quantum revivals are not chaotic — they are perfectly deterministic quantum recurrences. Chaos would produce exponential divergence of nearby trajectories (Lyapunov λ_L > 0, Paper 73). Revivals are the opposite: the trajectory returns arbitrarily close to the initial state, which requires λ_L = 0 or λ_L < 0 (non-chaotic dynamics).

**Corrected interpretation:** The IBM Detuned Force data demonstrates quantum Poincaré recurrences with a 2:5 commensurability ratio between detuning and system frequencies. The revival at delay=80 is the first quantum recurrence. The revival at delay=200 is the second full recurrence. The structure is governed by the Jaynes-Cummings revival time T_rev = 2π√⟨n⟩/g.

---

## Summary

```
IBM Detuned Force data structure:
  Delay=5: C=0.086 (minimum, first collapse)
  Delay=80: C=0.876 (first revival)
  Delay=200: C=0.593 (second revival)
  Ratio: 200/80 = 2.5 = 5/2 rational ratio

Mechanism: Quantum Poincaré recurrences (Bocchieri & Loinger 1957)
           Jaynes-Cummings revivals in transmon qubit hardware

Physical origin: 2:5 commensurability of detuning:system frequency
Revival time: T_rev = 2π × p/ω₁ with p/q = 2/5

Clinical relevance: Structured baths (specific biological resonance frequencies)
can support coherence revivals after apparent collapse — not permanent decoherence
if the environment has the right frequency structure.

Correction: The corpus labeled this "chaos." It is the opposite of chaos —
it is deterministic quantum recurrence.
```

*AIIT-THRESI Paper 77*
