# BROKEN THINGS
## What Actually Failed Across ~1.3 Million Simulations
### Rhet Dillard Wike | AIIT-THRESI | March 2026

---

## The Split

| BROKEN (systematic failures) | NOT BROKEN (100% hold) |
|------------------------------|------------------------|
| Axis-dependent decoherence rates | Holevo bound |
| Jarzynski equality at low T | Tsirelson bound |
| Onsager reciprocity at large gradients | CKW monogamy |
| Subsystem entropy at cold | Lindblad CPTP |
| Non-Markovian predictions | Complete positivity |
| Pointer state theory | Channel capacity |
| "Coherence requires cold" | Quantum regression theorem |

**Left column:** About temperature, thermal models, assumptions, axes.
**Right column:** About information, geometry, bounds, structure.

---

## Broken #1: Rotational Symmetry of Decoherence
**Source:** Paper 13, ~15,000 runs

The standard noise model (sigma_z dephasing) is in virtually every quantum
computing paper. It assumes dephasing happens along one axis.

**Finding:** Coherence varies up to 30.4% just by rotating which axis you
call z. Every T1, T2, T_phi measurement in the literature is relative to
an arbitrary axis. The decoherence RATE is partly a coordinate artifact.

Nature has no z-axis. The model picks one anyway.

## Broken #2: Jarzynski Equality at Low Temperature
**Source:** 1,050,000 runs across 30 Jarzynski configs

| T | Error | Err*T | Status |
|---|-------|-------|--------|
| 0.5 | 6.33 | 3.17 | FAIL |
| 1.0 | 1.72 | 1.72 | FAIL |
| 2.0 | 0.65 | 1.30 | FAIL |
| 5.0 | 0.22 | 1.10 | FAIL |
| 10.0 | 0.11 | 1.05 | PASS |

Err*T converges to 1.0 as T increases. The error follows the Bose-Einstein
distribution function: err ≈ (e^(1/T) - 1). Independent of protocol speed.

The equality assumes the system can explore all microstates (ergodicity).
At low T, the system is frozen into the ground state. Phase space is blocked.

## Broken #3: Onsager Reciprocity at Large Gradients
**Source:** 1,050,000 runs across 20 Onsager configs

| dT | Error | Status |
|----|-------|--------|
| 0.5 | 0.10 | PASS |
| 1.0 | 0.22 | FAIL |
| 2.0 | 0.50 | FAIL |
| 5.0 | 1.97 | FAIL |

Independent of coupling strength J. Only depends on temperature gradient.
Onsager assumes LINEAR response (small perturbation). At large dT,
linearity breaks. The environment stops being a passive mirror.

## Broken #4: Subsystem Entropy at Low Temperature
**Source:** 1,050,000 runs

Maximally mixed state entropy DECREASES when thermalizing at cold temperatures:
- T=0.1: entropy 0.693 → 0.021 (97% decrease)
- T=1.0: entropy 0.693 → 0.582 (16% decrease)
- T=5.0+: entropy increases as expected

Cold forces order. The second law applies to the total system, but the
subsystem — the part we live in — gets MORE ordered by cold, not less.

## Broken #5: Decoherence Theory Itself
**Source:** 130,000 runs, 46% pass rate (worst category)

The theory that explains WHY things decohere is the LEAST reliable theory
we tested. Failures in:
- Non-Markovian decay shapes (1/f and Lorentzian noise)
- Pointer state selection at weak coupling
- Einselection at small environment sizes

Standard decoherence theory assumes Markovian environment. Real
environments are not Markovian. The theory works for textbook noise
and fails for realistic noise.

## Broken #6: "Coherence Requires Cold"
**Source:** Paper 11, 120,000 runs

Silicon retains coherence at body temperature. Copper retains coherence
at body temperature. The neural combo (Cu+H2O) shows temperature-independent
fidelity. Biological elements support coherence at 310K.

---

## The Pattern

The thermal/dynamical predictions break.
The information/geometric constraints hold.

**Temperature is where physics is fragile.**
**Information is where physics is unbreakable.**

The universe doesn't care about our thermal predictions.
The universe ENFORCES informational and geometric limits.

Temperature is negotiable. Geometry is not. Pi is not.

---

God is good. All the time.
