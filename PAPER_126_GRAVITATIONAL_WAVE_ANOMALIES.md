# PAPER 126: GRAVITATIONAL ANOMALIES AND THE DECOHERENCE FIELD
## Nine Closures from a Single Equation
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### April 1, 2026

---

> *"General relativity is the low-coherence limit of a deeper theory. Every gravitational anomaly that resists explanation within GR alone resolves the moment you restore the coherence term GR set to zero."*

---

## Abstract

Nine gravitational anomalies spanning gravitational wave memory, the nanohertz stochastic background, the GW170817 speed constraint, the Abell 520 dark matter distribution, dwarf galaxy diversity, the equivalence principle, frame-dragging, LIGO mass gap events, and anomalous perihelion precessions are closed using one equation: the Wike Coherence Law C = C_0 * exp(-alpha * gamma_eff). Each anomaly maps to a specific regime of this equation. Gravitational wave memory is a permanent decoherence scar. The NANOGrav excess traces cosmological phase transitions at the critical decoherence rate gamma_c. The speed constraint v = c follows necessarily because gravitational waves are perturbations of the vacuum coherence field, which IS spacetime. The Abell 520 and Bullet Cluster dark matter distributions both follow from C_vacuum tracking local gamma_eff. Dwarf galaxy diversity reflects environmental decoherence history. The equivalence principle holds because in the decohered regime C approaches 0 and all matter couples identically to gravity. Frame-dragging is coherence rotation. Mass gap objects form in the finite-width phase transition near gamma_c. Perihelion anomalies emerge at the acceleration scale a_0 = c * gamma_c where vacuum coherence becomes non-negligible. Zero free parameters are introduced beyond those already fixed by the framework.

---

## 1. The Core Equation

The Wike Coherence Law, derived from the Lindblad master equation in Papers 1-5:

```
C = C_0 * exp(-alpha * gamma_eff)
```

where:
- C is the coherence amplitude of any quantum subsystem
- C_0 is the initial (maximum) coherence
- alpha is the coupling constant to the decoherence bath
- gamma_eff is the effective decoherence rate from all environmental channels

The framework has one critical point: gamma_c, the decoherence rate at which the system undergoes a phase transition (3D Ising universality class, Papers 50-55, 102, 106). Below gamma_c, coherence is macroscopically significant. Above gamma_c, the system is classical.

For the vacuum itself, C_vacuum is the coherence of the quantum vacuum state:

```
C_vacuum = C_0^vac * exp(-alpha_vac * gamma_eff^local)
```

This vacuum coherence generates what general relativity interprets as spacetime curvature in the classical limit, and what observations attribute to dark matter and dark energy in regimes where C_vacuum is non-negligible (Papers 62, 75, 77).

The connection to observed gravity: in the fully decohered limit (gamma_eff >> gamma_c), C_vacuum approaches 0 and GR is exact. At gamma_eff near gamma_c, vacuum coherence contributes an additional effective mass-energy, producing deviations from pure GR.

---

## 2. GW Memory

**The anomaly:** General relativity predicts that after a gravitational wave passes, spacetime retains a permanent displacement -- gravitational wave memory (Christodoulou 1991, Thorne 1992). This memory effect has not been directly detected despite dedicated searches by LIGO/Virgo and pulsar timing arrays.

**The closure:**

Gravitational wave memory IS a permanent decoherence scar. When a gravitational wave passes through a region, it temporarily drives the local gamma_eff above gamma_c:

```
gamma_eff(t) = gamma_eff^background + delta_gamma_GW(t)

During GW passage:
  gamma_eff(t) > gamma_c    (temporarily)

After passage:
  gamma_eff returns to background
  BUT: coherence state has shifted permanently
```

The mechanism: a system driven past gamma_c undergoes a phase transition. Phase transitions are irreversible -- the coherence state does not return to its pre-transition value when gamma_eff drops back below gamma_c. This is hysteresis, a universal property of first-order phase transitions.

The permanent displacement predicted by GR is the permanent shift in local C_vacuum:

```
Delta_C_vacuum = C_0^vac * [exp(-alpha_vac * gamma_c) - exp(-alpha_vac * gamma_eff^peak)]
```

The magnitude depends on how far gamma_eff^peak exceeds gamma_c during the wave passage. For astrophysical GW sources at cosmological distances, the strain at Earth is h ~ 10^-21, producing delta_gamma_GW << gamma_c. The memory effect exists but is below current detection thresholds -- consistent with non-detection.

**Prediction:** GW memory will be detected first in events where gamma_eff^peak / gamma_c is largest: nearby, high-mass mergers. The memory magnitude scales with the degree of gamma_c crossing.

---

## 3. Nanohertz Gravitational Wave Background (NANOGrav)

**The anomaly:** NANOGrav (2023) and other pulsar timing arrays detected a stochastic gravitational wave background at nanohertz frequencies. The measured amplitude may exceed predictions from supermassive black hole (SMBH) binary populations alone (Agazie et al. 2023). The spectral slope is consistent with SMBH binaries but the amplitude has excess power that standard astrophysical models struggle to account for.

**The closure:**

The excess amplitude comes from cosmological coherence phase transitions in the early universe:

```
GW background = GW_SMBH + GW_phase_transition

GW_phase_transition from:
  gamma_eff^cosmic(T) crosses gamma_c at temperature T_transition
  Coherence energy released: Delta_E = C_0^vac * (1 - exp(-alpha_vac * gamma_c))
  Energy converts to gravitational radiation
```

Phase transitions at gamma_c release coherence energy because the vacuum coherence field couples to gravity. When C_vacuum changes discontinuously at a phase transition, the energy difference radiates as gravitational waves.

In the early universe, the cosmic decoherence rate gamma_eff^cosmic decreased as the universe expanded and cooled:

```
gamma_eff^cosmic(T) proportional to T^n    (n depends on dominant decoherence channel)

At T = T_transition:
  gamma_eff^cosmic(T_transition) = gamma_c
  Phase transition occurs
  Coherence energy released as GWs
```

These GWs redshift to nanohertz frequencies today, contributing a stochastic background on top of the SMBH binary signal. The spectral shape from the phase transition is similar to SMBH binaries at low frequencies, making the two sources difficult to disentangle -- consistent with the ambiguity in current data.

**Prediction:** As PTA sensitivity improves, the spectral slope at f > 30 nHz will deviate from the f^(-2/3) power law expected from SMBH binaries alone. The deviation encodes the temperature and width of the cosmological gamma_c transition.

---

## 4. GW170817 Speed Constraint

**The anomaly:** The binary neutron star merger GW170817 (LIGO/Virgo 2017) was observed simultaneously in gravitational waves and electromagnetic radiation (gamma-ray burst GRB 170817A, Fermi). The arrival time difference constrains the speed of gravity:

```
|v_gravity - c| / c < 10^-15
```

This eliminates many modified gravity theories that predict v_gravity != c.

**The closure:**

This result is not an anomaly within the framework -- it is a direct prediction. Gravitational waves are perturbations in the vacuum coherence field. The vacuum coherence field IS spacetime. Perturbations of spacetime propagate at c by definition:

```
v_GW = c    (exact, not approximate)

Reason: GWs are decoherence waves -- propagating disturbances in C_vacuum
C_vacuum defines the local metric
Metric perturbations propagate at c (from the structure of the Lindblad equation)
```

Any theory predicting v_gravity != c is predicting that spacetime perturbations propagate at a speed different from the speed set by spacetime itself -- a logical contradiction.

The 10^-15 precision of GW170817 does not constrain the framework. It confirms it.

---

## 5. Abell 520 "Train Wreck" Cluster

**The anomaly:** In the Bullet Cluster (1E 0657-56), dark matter follows the galaxies and is offset from the hot gas -- cited as evidence for collisionless particle dark matter. In Abell 520, the opposite occurs: a significant dark matter concentration coincides with the gas at the collision center, offset from the galaxies (Mahdavi et al. 2007, Jee et al. 2012). If dark matter is collisionless particles, it should not accumulate with the collisional gas.

**The closure:**

Both clusters are consistent with C_vacuum responding to local gamma_eff:

```
Dark matter distribution follows:
  C_vacuum(x) = C_0^vac * exp(-alpha_vac * gamma_eff(x))

gamma_eff(x) is determined by local matter density and temperature:
  gamma_eff proportional to rho * T^(1/2)    (collisional decoherence rate)
```

**Bullet Cluster geometry:** Two clusters pass through each other. Gas shocks and piles up at center (high rho, high T). Galaxies pass through (low interaction cross-section). After passage, the highest gamma_eff is at the gas center. But the galaxies carry their own gamma_eff halos. In the Bullet Cluster geometry (high relative velocity, clean separation), the galaxy halos dominate over the residual gas contribution. C_vacuum tracks the galaxy halos. Apparent DM follows galaxies.

**Abell 520 geometry:** More complex merger (possibly three-body). Gas remains concentrated at collision center with high density. In this geometry, the gas contribution to gamma_eff at the center exceeds the galaxy halo contributions (which are more dispersed due to the multi-body dynamics). C_vacuum tracks the dominant gamma_eff source -- the gas. Apparent DM follows gas.

```
Bullet Cluster: gamma_eff^galaxies > gamma_eff^gas at galaxy positions --> DM follows galaxies
Abell 520:      gamma_eff^gas > gamma_eff^galaxies at center --> DM follows gas
```

Different collision geometries produce different gamma_eff profiles produce different apparent dark matter distributions. Both are consistent with a single mechanism.

---

## 6. Dwarf Galaxy Dark Matter Diversity

**The anomaly:** Dwarf galaxies of similar stellar mass, size, and morphology exhibit wildly different mass-to-light (M/L) ratios -- from M/L ~ 5 (modest dark matter) to M/L > 1000 (dark matter dominated). This "diversity problem" (Oman et al. 2015) is difficult to explain with standard CDM, which predicts that halos of similar mass should produce similar M/L ratios.

**The closure:**

M/L ratios reflect the environmental decoherence history of each dwarf galaxy:

```
M/L proportional to (1 + C_vacuum / C_baryonic)

C_vacuum depends on the full history of gamma_eff:
  C_vacuum(t_now) = C_0^vac * exp(-alpha_vac * integral[gamma_eff(t') dt', 0, t_now])
```

The integral over the full decoherence history means that two dwarfs with identical present-day properties can have different C_vacuum (and therefore different apparent DM content) if their histories differ:

- A dwarf that spent 5 Gyr near a massive galaxy (high gamma_eff environment) has lower C_vacuum than one that evolved in isolation.
- A dwarf that formed stars rapidly (high internal gamma_eff from supernovae feedback) has lower C_vacuum than one with quiescent star formation.
- A dwarf that experienced a close tidal encounter has a permanently altered C_vacuum (decoherence scar, same mechanism as GW memory in Section 2).

The diversity is not random -- it correlates with environmental history. This is a testable prediction: M/L should correlate with tidal history, proximity to massive hosts, and star formation history, independently of present-day stellar mass.

---

## 7. Equivalence Principle

**The anomaly:** The MICROSCOPE satellite (Touboul et al. 2022) confirmed the weak equivalence principle to:

```
eta(Ti, Pt) = (2 * |a_Ti - a_Pt|) / (a_Ti + a_Pt) < 10^-15
```

All matter falls the same way in a gravitational field, regardless of composition, to extraordinary precision.

**The closure:**

In the fully decohered (classical) regime, C approaches 0 for all matter:

```
Classical regime: gamma_eff >> gamma_c

For any material A:   C_A = C_0^A * exp(-alpha_A * gamma_eff) --> 0
For any material B:   C_B = C_0^B * exp(-alpha_B * gamma_eff) --> 0

Gravitational coupling proportional to mass + f(C)
When C --> 0 for all matter: coupling proportional to mass only
--> Universality of free fall (equivalence principle)
```

The equivalence principle holds in the classical regime because coherence is exponentially suppressed. The suppression factor exp(-alpha * gamma_eff) drives all coherence-dependent corrections below any measurable threshold for macroscopic matter at room temperature.

Violations of the equivalence principle occur only when C > 0 -- at quantum gravity scales, in ultracold systems, or in the immediate vicinity of gamma_c. MICROSCOPE operates firmly in the classical regime.

**Prediction:** Equivalence principle violations at the 10^-17 level or below may appear in experiments using ultracold atoms (BEC free-fall tests), where gamma_eff is low enough that C remains non-negligible.

---

## 8. Frame-Dragging

**The anomaly:** Gravity Probe B (Everitt et al. 2011) confirmed frame-dragging (the Lense-Thirring effect) at the 19% level. LARES and LAGEOS laser ranging confirm it at the 5% level (Ciufolini et al. 2019). Both are consistent with GR.

**The closure:**

Frame-dragging IS coherence rotation. A rotating mass drags the local vacuum coherence field:

```
Rotating mass M with angular momentum J:

Vacuum coherence field:
  C_vacuum(r, theta) = C_0^vac * exp(-alpha_vac * gamma_eff(r, theta))

Rotation of mass --> rotation of gamma_eff profile --> rotation of C_vacuum
This rotation of C_vacuum IS the frame-dragging measured by GP-B
```

GR gives the correct frame-dragging prediction because GR IS the low-coherence limit of the framework. In the regime gamma_eff >> gamma_c (all GP-B and LARES measurements), the coherence contribution is exponentially small and the GR prediction is exact.

Frame-dragging does not constrain the framework -- it confirms that GR emerges as the correct low-coherence limit. Deviations from the GR prediction for frame-dragging would appear only near compact objects where gamma_eff approaches gamma_c (neutron star surfaces, black hole horizons).

---

## 9. LIGO Mass Gap Events

**The anomaly:** LIGO/Virgo detected objects in the "mass gaps" where stellar physics predicts no compact objects should form:

- **GW190814** (Abbott et al. 2020): Contains a 2.6 M_sun object -- in the "lower mass gap" between the heaviest neutron stars (~2.2 M_sun) and lightest black holes (~5 M_sun).
- **GW190521** (Abbott et al. 2020): Two black holes of ~85 M_sun and ~66 M_sun -- in the "upper mass gap" (65-120 M_sun) where pair-instability supernovae should prevent black hole formation.

**The closure:**

The mass gaps correspond to unstable regions near gamma_c for nuclear and stellar matter:

```
Nuclear matter phase transition at gamma_c:

For neutron star matter:
  gamma_eff(rho, T) crosses gamma_c at specific (rho, T) combinations
  The phase transition has finite width Delta_gamma around gamma_c
  In the transition region: matter is metastable, not forbidden

Mass gap = region where:
  |gamma_eff - gamma_c| < Delta_gamma
  Objects CAN form but are metastable
  Formation is rare but not impossible
```

**Lower mass gap (2.2-5 M_sun):** At these masses, the central density places gamma_eff within Delta_gamma of gamma_c for nuclear matter. The neutron star equation of state is in the transition region. Most formation channels avoid this region (they produce objects above or below it), but rare channels -- such as accretion onto a neutron star or secondary collapse during merger -- can place objects in the gap.

**Upper mass gap (65-120 M_sun):** Pair-instability physics depends on the nuclear reaction rates, which are sensitive to the coherence state of the stellar core plasma. Near gamma_c, the effective nuclear rates shift, widening the window for black hole formation through the pair-instability region. The suppression is weakened, not eliminated -- gap objects are rare, consistent with observation.

**Prediction:** Mass gap objects should show a clustering near the boundaries of the gaps (where Delta_gamma is largest) rather than uniform distribution within the gaps.

---

## 10. Anomalous Perihelion Precessions

**The anomaly:** After accounting for all known Newtonian and GR effects, some solar system bodies show residual unmodeled accelerations at the scale:

```
a_residual ~ 10^-10 m/s^2
```

This is the same order as the MOND acceleration scale a_0 = 1.2 * 10^-10 m/s^2 (Milgrom 1983). The Pioneer anomaly (since resolved by thermal recoil) and ongoing residuals in outer solar system orbit fits both point to this scale.

**The closure:**

The acceleration scale a_0 marks where vacuum coherence becomes non-negligible:

```
a_0 = c * gamma_c

At accelerations a >> a_0:
  gamma_eff >> gamma_c
  C_vacuum --> 0
  Pure GR (Newtonian + relativistic corrections)

At accelerations a ~ a_0:
  gamma_eff ~ gamma_c
  C_vacuum is non-negligible
  Additional effective mass-energy from vacuum coherence
  Small deviations from pure GR
```

The connection a_0 = c * gamma_c was established in Papers 62 and 75. It means that a_0 is not a free parameter -- it is determined by the same gamma_c that governs all other coherence phase transitions in the framework.

At the acceleration scale a_0, the vacuum coherence correction to the gravitational potential is:

```
Phi_total = Phi_GR + Phi_coherence

Phi_coherence = -(1/2) * a_0 * r * (C_vacuum / C_0^vac)

For a ~ a_0: Phi_coherence / Phi_GR ~ O(1)
For a >> a_0: Phi_coherence / Phi_GR --> 0 exponentially
```

This produces small residual precessions at the 10^-10 m/s^2 level in the outer solar system, where accelerations drop toward a_0. The framework predicts MOND-like behavior at low accelerations as a consequence of vacuum coherence, not as an ad hoc modification of Newton's law.

---

## 11. Unified Picture

All nine anomalies resolve from a single mechanism: the vacuum coherence field C_vacuum responds to the local decoherence rate gamma_eff through the Wike Coherence Law:

```
C_vacuum = C_0^vac * exp(-alpha_vac * gamma_eff)
```

| Anomaly | Regime | Mechanism |
|---------|--------|-----------|
| GW Memory | gamma_eff temporarily > gamma_c | Permanent decoherence scar (hysteresis) |
| NANOGrav excess | gamma_eff^cosmic crossed gamma_c in early universe | Phase transition GW radiation |
| v_gravity = c | All regimes | GWs are C_vacuum perturbations; spacetime IS C_vacuum |
| Abell 520 | gamma_eff dominated by gas at center | C_vacuum tracks dominant gamma_eff source |
| Dwarf diversity | Different gamma_eff histories | C_vacuum retains decoherence history |
| Equivalence principle | gamma_eff >> gamma_c (classical) | C --> 0 for all matter; universal coupling |
| Frame-dragging | gamma_eff >> gamma_c (classical) | Coherence rotation = GR in low-C limit |
| Mass gap events | gamma_eff near gamma_c | Finite-width phase transition; metastable objects |
| Perihelion anomalies | a ~ a_0 = c * gamma_c | Vacuum coherence correction non-negligible |

The framework does not modify GR. It contains GR as the exact low-coherence limit. Every anomaly that is "consistent with GR" (speed constraint, equivalence principle, frame-dragging) is consistent because GR is the gamma_eff >> gamma_c sector of the framework. Every anomaly that "deviates from GR" (NANOGrav excess, dwarf diversity, perihelion residuals) deviates because gamma_eff approaches gamma_c and the coherence term C_vacuum becomes non-negligible.

---

## 12. Predictions

The closures in this paper generate the following testable predictions:

1. **GW memory detection** will occur first in nearby high-mass mergers. Memory magnitude correlates with peak strain, not merely with total radiated energy.

2. **NANOGrav spectral slope** will deviate from f^(-2/3) above ~30 nHz as PTA baselines extend, revealing the phase transition contribution.

3. **Equivalence principle violation** at 10^-17 or below will appear in BEC free-fall experiments where gamma_eff is sufficiently low to maintain C > 0.

4. **Mass gap object distribution** within the gaps will cluster near gap boundaries, not uniformly fill the gaps.

5. **Dwarf galaxy M/L ratios** correlate with tidal history and environmental proximity independently of present-day stellar mass.

6. **Frame-dragging deviations** from GR predictions will appear in observations of neutron star and black hole spin dynamics at the percent level, where gamma_eff approaches gamma_c.

7. **Outer solar system orbit residuals** scale as a_0 = c * gamma_c, with gamma_c fixed independently from biological and condensed-matter measurements (Papers 102, 109).

---

## 13. Conclusion

Nine gravitational anomalies. One equation. Zero new free parameters.

The Wike Coherence Law C = C_0 * exp(-alpha * gamma_eff) does not add epicycles to general relativity. It identifies the deeper structure from which GR emerges in the decohered limit. GR is exact when C_vacuum = 0. Every gravitational anomaly maps to a regime where C_vacuum is non-zero -- either transiently (GW memory), historically (dwarf galaxy diversity, NANOGrav), or at the boundary of the classical regime (mass gap events, perihelion precessions).

The framework makes the same prediction it has made across 126 papers: the physics of coherence and decoherence, governed by a single exponential decay law derived from first principles, unifies phenomena from nuclear structure (Paper 105) through biology (Papers 100-109) to cosmology (this paper). The critical point gamma_c is the same in all domains. The universality class is 3D Ising.

---

**Paper 126 of the AIIT-THRESI series.**

**Author:** Rhet Dillard Wike, Council Hill, Oklahoma.

**Correspondence:** AIIT-THRESI Research Initiative.

**Date:** April 1, 2026.
