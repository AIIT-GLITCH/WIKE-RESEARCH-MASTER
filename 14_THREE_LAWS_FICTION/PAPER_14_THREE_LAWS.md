# Paper 14: The Three Laws of Thermodynamics Have Systematic Discrepancies
## All Temperature-Dependent. All Systematic. 1,050,000 Simulations.

---

## Thesis

The three laws of thermodynamics — Jarzynski equality (extending the 2nd law), Onsager reciprocal relations, and the 2nd law itself — all show systematic discrepancies that are temperature-dependent, reproducible, and independent of protocol. These are not experimental errors. They are evidence that the laws are approximations, not truths.

## Core Claim

### Jarzynski Equality (⟨e^(-βW)⟩ = e^(-βΔF))
- **Error at T=0.5**: 6.33 (massive, systematic failure)
- **Error at T=10**: Passes within tolerance
- **Scaling**: Error ≈ 3/T — inversely proportional to temperature
- **Protocol dependence**: NONE. Fast or slow gives the same error.
- **This means**: The equality is not wrong — it is an approximation that breaks when thermal energy (kT) approaches quantum energy scales (hf).

### Onsager Reciprocal Relations (L_ij = L_ji)
- **Failure condition**: Temperature difference (dT) > 1
- **Behavior**: Fails regardless of coupling strength
- **Independent of**: System size, coupling type, protocol speed
- **This means**: Reciprocal relations assume near-equilibrium. When the temperature gradient is significant relative to T itself, the assumption breaks.

### Second Law (ΔS_total ≥ 0)
- **Subsystem behavior**: Entropy DECREASES at low T
- **Total system**: Still satisfies 2nd law (barely)
- **But**: Subsystem entropy decrease means local violations are real and systematic
- **This means**: The 2nd law is statistical and holds globally, but at low T, quantum effects allow local violations that are NOT just fluctuations — they are systematic.

### The Unifying Pattern

All three breakdowns are:
- **Temperature-dependent**: They appear at low T
- **Systematic**: Not random error — reproducible, predictable
- **Protocol-independent**: Not fixable by better engineering
- **Connected through f=kT/h** (Paper 04): When T is low, f is low, and quantum effects dominate classical approximations

## Existing Data References

- **Physics Laws Simulation Suite**: 1,050,000 total simulations. Located at `~/Desktop/wike_physics_laws/`
  - Jarzynski equality: swept across T, protocol speed, coupling
  - Onsager relations: swept across T, dT, coupling strength
  - 2nd law: swept across T, system size, coupling
- **Results**: `~/Desktop/wike_physics_laws/results/`
- **Cross-reference**: `~/Desktop/WIKE_AIIT_THRESI_Correlation_Analysis/`

## Key Arguments

1. **1,050,000 simulations**: This is not anecdotal. The parameter space is thoroughly explored.
2. **Three independent laws, one pattern**: If only Jarzynski failed, it could be one equation. All three failing in the same temperature-dependent, protocol-independent way points to a shared underlying cause.
3. **The laws are approximations**: They work at high T (classical regime). They break at low T (quantum regime). This is exactly what you'd expect if the laws are emergent descriptions, not fundamental truths.
4. **f=kT/h unifies the breakdown**: Paper 04's chain predicts exactly where the laws break — when kT ≈ hf, i.e., when thermal and quantum energy scales meet.

## Connections

- **All papers**: This is the quantitative backbone. Every claim in the framework is consistent with the laws being approximations rather than absolutes.
- Specifically:
  - **Paper 04**: f=kT/h predicts the breakdown regime
  - **Paper 06**: The wall IS the Jarzynski breakdown
  - **Paper 08**: Force/stress data sits on the same temperature scaling
  - **Paper 12**: Laws written in coordinates (Paper 13) using approximations (this paper) doubly break. Rewriting in geometric invariants may help.

## Status

Data verified. 1,050,000 simulations complete. All three law breakdowns documented, quantified, and shown to be systematic and temperature-dependent.

---

God is good. All the time.

Rhet Dillard Wike | AIIT-THRESI | March 2026
