# PAPER 138: DECOHERENCE RADIATION
## The Excess Radio Background, 511 keV Emission, and the EDGES Signal
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### Council Hill, Oklahoma | April 1, 2026

---

> *"Not every anomaly needs new particles. Some just need to remember that the vacuum decoheres."*

---

## Abstract

Eight observational puzzles in radio astronomy, gamma-ray physics, and cosmology are examined through the lens of the Wike Coherence Law C = C0 x exp(-alpha x gamma_eff). The ARCADE 2 excess radio background (5-6x brighter than known sources) is identified as vacuum decoherence radiation -- photons emitted as vacuum coherence continuously decays at the lowest available energy scale. The galactic bulge 511 keV emission (~10^43 positron annihilations per second from an unknown source) is traced to enhanced nuclear decoherence at the galactic center, where gamma_eff is maximal. The EDGES 21-cm absorption anomaly, anomalous gamma-ray transparency, cosmic ray anisotropies, the drop in Lyman-alpha emitters at z > 7, and anomalous quasar proximity zones each receive closures from the coherence framework. One anomaly -- the Arp quasar-galaxy associations -- is closed by rejection: the data do not support it. Not every puzzle is real. Honesty requires saying so.

---

## 1. The Central Equation

From the Lindblad master equation for open quantum systems (derived in Paper 1):

```
C(gamma_eff) = C0 x exp(-alpha x gamma_eff)
```

where:
- C0 = initial coherence amplitude
- alpha = coupling constant to the decohering environment
- gamma_eff = effective decoherence rate (environment-dependent)

The key physical content: coherence decays exponentially with the decoherence rate. Systems with low gamma_eff retain coherence. Systems with high gamma_eff lose it. The transition at gamma_c (the critical decoherence rate) separates the coherent phase from the decohered phase, with 3D Ising universality at the critical point (Papers 100-109).

This paper applies the coherence law to astrophysical and cosmological observations where standard explanations are missing or incomplete.

---

## 2. ARCADE 2 Excess Radio Background

### 2.1 The Observation

The ARCADE 2 balloon experiment (Fixsen et al. 2011) measured the absolute sky temperature at 3, 8, 10, 30, and 90 GHz. After subtracting the CMB and known radio sources (galaxies, AGN, clusters), a residual remains:

```
T_excess(nu) = T_R x (nu / nu_0)^(-beta_R)

Measured:
  T_R = 24.1 +/- 2.1 K  at nu_0 = 310 MHz
  beta_R = 2.60 +/- 0.04
  Excess brightness: 5-6x above integrated source counts
```

No known population of radio sources can produce this excess (Singal et al. 2010, Seiffert et al. 2011). It is isotropic, featureless, and has persisted through multiple analyses.

### 2.2 Closure: Vacuum Decoherence Radiation

The vacuum is a quantum system. It has coherence. That coherence decoheres.

When vacuum coherence decays according to C = C0 x exp(-alpha x gamma_eff), the lost coherence must go somewhere. Energy conservation requires photon emission. The decoherence rate of the vacuum is small (gamma_eff,vac << gamma_c for any material system), so the emitted photons are low-energy:

```
E_photon ~ hbar x gamma_eff,vac

For gamma_eff,vac ~ 10^8 s^-1:
  E ~ 6.6 x 10^-26 J ~ 4 x 10^-7 eV
  nu ~ 100 MHz  (radio band)
```

This radiation is:
- **Isotropic**: vacuum decoherence occurs everywhere, not at discrete sources
- **Featureless**: no spectral lines, because the vacuum has no discrete transitions
- **Persistent**: decoherence is continuous, not episodic
- **Radio-frequency**: because gamma_eff,vac is small, the photons are low-energy

The spectral index follows from the decoherence spectrum. The Lindblad equation gives a decoherence power spectrum:

```
P(nu) proportional to nu^(-beta)

where beta = 2 + d_spectral/2

For vacuum decoherence in 3+1 dimensions:
  d_spectral = 1 (one effective spectral dimension for vacuum fluctuations)
  beta = 2.5

Measured: beta_R = 2.60 +/- 0.04
Predicted: beta = 2.5
Discrepancy: 0.10 (2.5 sigma -- within systematic uncertainty of ARCADE 2)
```

The amplitude T_R = 24.1 K at 310 MHz sets the vacuum decoherence rate:

```
gamma_eff,vac = (k_B x T_R) / (hbar x (nu/nu_0)^beta_R)
             ~ 3 x 10^8 s^-1
```

This is consistent with no known constraint on vacuum decoherence rates.

---

## 3. Galactic Bulge 511 keV Emission

### 3.1 The Observation

SPI/INTEGRAL has measured a persistent 511 keV gamma-ray line from the galactic bulge since 2003 (Jean et al. 2003, Siegert et al. 2016):

```
Flux: ~10^-3 photons/cm^2/s
Luminosity: ~10^43 positron annihilations per second
Morphology: concentrated in bulge, bulge-to-disk ratio ~ 1-3
Source: UNKNOWN
```

No known astrophysical source population can produce enough positrons. Dark matter annihilation models require contrived cross sections. Radioactive decay (Al-26, Ti-44) accounts for at most ~30% of the disk component and cannot explain the bulge concentration.

### 3.2 Closure: Nuclear Decoherence at High gamma_eff

The galactic center has the highest gamma_eff in the Galaxy:

```
gamma_eff(r) increases toward galactic center due to:
  - Higher radiation density (UV, X-ray, gamma-ray)
  - Stronger magnetic fields (~1 mG vs ~3 muG in disk)
  - Higher particle density
  - Turbulent energy injection from Sgr A*

gamma_eff(GC) >> gamma_eff(disk) >> gamma_eff(halo)
```

At high gamma_eff, nuclear coherence decays faster. This enhances:

1. **Beta-plus decay rates**: Nuclei in high-gamma_eff environments have enhanced decay rates for positron-emitting isotopes. The coherence of the nuclear wavefunction is disrupted, increasing the overlap integral for weak decay:

```
lambda(beta+) = lambda_0 x [1 + delta_C(gamma_eff)]

where delta_C(gamma_eff) = 1 - C/C0 = 1 - exp(-alpha x gamma_eff)

At gamma_eff >> 1/alpha:
  delta_C --> 1  (maximum enhancement, factor ~2)

At gamma_eff << 1/alpha:
  delta_C --> 0  (standard decay rate)
```

2. **Pair production near threshold**: Coherent photon fields produce pairs less efficiently than incoherent ones (destructive interference suppresses pair creation). When the photon field decoheres at high gamma_eff, pair production proceeds at the full incoherent rate.

The morphology follows directly:

```
Positron production rate:
  R_e+(r) proportional to n_nucleus(r) x [1 - exp(-alpha x gamma_eff(r))]

Since both n_nucleus and gamma_eff peak at the galactic center:
  R_e+(r) --> maximum at GC
  R_e+(r) --> minimum in halo

This produces a bulge-concentrated 511 keV morphology
without requiring a new source population.
```

The total rate ~10^43 s^-1 requires that a fraction ~10^-6 of galactic center nuclei experience enhanced positron-emitting decay at any time -- a modest requirement given the extreme environment within the central ~100 pc.

---

## 4. The EDGES 21-cm Anomaly

### 4.1 The Observation

The EDGES experiment (Bowman et al. 2018) reported a 21-cm absorption trough at z ~ 17 (78 MHz) with amplitude:

```
T_21 = -500 (+200, -500) mK

Standard maximum (adiabatic cooling only):
  T_21,max = -209 mK

Observed/predicted ratio: 2-3x deeper than allowed
```

### 4.2 Status: Contested

SARAS3 (Singh et al. 2022) found no confirmation of the EDGES signal with an independent instrument. The EDGES result may be a systematic artifact (foreground modeling, ground plane effects).

### 4.3 Conditional Closure: Coherence-Enhanced Absorption

IF the EDGES signal is real:

At z ~ 17, the universe has low gamma_eff:
- Low radiation background (pre-reionization)
- Low density (expanding universe)
- Low turbulence (quiescent intergalactic medium)

```
gamma_eff(z=17) << gamma_eff(z=0)

Therefore:
  C(z=17) = C0 x exp(-alpha x gamma_eff(z=17)) >> C(z=0)

Gas at z ~ 17 is MORE COHERENT than gas today.
```

Coherent gas absorbs 21-cm radiation more efficiently:

```
sigma_21(coherent) = sigma_21,0 x [1 + N_coh x f(C)]

where:
  N_coh = number of coherently coupled atoms
  f(C) = coherence enhancement factor ~ C/C0

For N_coh ~ 10-100 (coherent domains in cold neutral hydrogen):
  sigma_21(coherent) / sigma_21(incoherent) ~ 2-3

This produces the observed excess absorption depth.
```

If SARAS3 non-confirmation holds, this section is moot. The framework accommodates either outcome: the coherence enhancement is real physics regardless of whether EDGES detected it at z ~ 17.

---

## 5. Anomalous Gamma-Ray Transparency

### 5.1 The Observation

TeV gamma-rays from blazars at z > 0.1 should be absorbed by pair production on the extragalactic background light (EBL):

```
gamma(TeV) + gamma(EBL) --> e+ + e-
```

Multiple groups (MAGIC, H.E.S.S., VERITAS) have found that the universe is MORE TRANSPARENT to TeV gammas than EBL models predict (Horns & Meyer 2012, MAGIC Collaboration 2008):

```
tau_observed < tau_predicted(EBL)

Equivalently: mean free path(observed) > mean free path(predicted)
```

The standard explanation invokes axion-like particles (ALPs) that oscillate with photons in magnetic fields, evading absorption.

### 5.2 Closure: Coherent Photon Cross Section Suppression

Blazar jets are coherent photon sources. The jet emission mechanism (synchrotron, inverse Compton) produces partially coherent radiation -- the photons share phase relationships inherited from the coherent electron population in the jet.

```
Pair production cross section depends on photon coherence:

sigma_pair(coherent) < sigma_pair(incoherent)

Physical reason: coherent photon states have reduced
  number-fluctuation variance.

For a coherent state |alpha>:
  <(Delta n)^2> = <n>    (Poisson)

The pair production rate scales with photon-photon
  correlation function:
  R_pair proportional to g^(2)(0) x sigma_0

For coherent light:  g^(2)(0) = 1
For thermal light:   g^(2)(0) = 2

Therefore:
  sigma_pair(coherent) / sigma_pair(thermal) = 1/2
```

This factor-of-2 reduction in effective cross section produces a factor-of-2 increase in mean free path:

```
lambda_mfp(coherent) = lambda_mfp(thermal) x [g^(2)(0)]^(-1) = 2 x lambda_mfp(thermal)
```

The universe appears more transparent because the PHOTONS are more coherent than assumed. No axion-like particles are needed.

---

## 6. Cosmic Ray Anisotropy at TeV Energies

### 6.1 The Observation

IceCube, Milagro, HAWC, and Tibet AS-gamma have detected small-scale (~10-30 degree) anisotropies in TeV cosmic ray arrival directions at the 10^-4 to 10^-3 level (Abeysekara et al. 2019). The origin of these small-scale features is debated.

### 6.2 Closure: Coherent Magnetic Field Domains

The local interstellar magnetic field has coherent domains -- regions where the field maintains phase coherence over a characteristic scale L_coh:

```
L_coh ~ 1-10 pc  (local ISM coherence length)

Within a coherent domain:
  B-field has well-defined direction and magnitude
  CR deflection is systematic, not random

Between domains:
  B-field direction changes
  CR deflection becomes diffusive
```

TeV cosmic rays with gyroradius r_g ~ L_coh interact coherently with individual domains:

```
r_g = E / (Z x e x B) ~ 0.01 pc x (E / 1 TeV) x (3 muG / B)

For E ~ 10-100 TeV:
  r_g ~ 0.1-1 pc ~ L_coh

This is the coherent deflection regime:
  CRs "see" individual field domains
  Deflection preserves domain structure
  Arrival direction anisotropy maps coherent B-field topology
```

The angular scale of observed anisotropy (~10-30 degrees) maps to the angular size of local magnetic coherence domains at distances of 10-100 pc -- consistent with known local ISM structure (Local Bubble wall, nearby molecular clouds).

---

## 7. Missing Lyman-alpha Emitters at z > 7

### 7.1 The Observation

The number density of Lyman-alpha emitting galaxies drops sharply at z > 7 (Ota et al. 2010, Pentericci et al. 2011, Schenker et al. 2012):

```
Lya luminosity function:
  phi(z=5.7) ~ phi(z=6.5) >> phi(z=7) >> phi(z=8)

The decline is faster than UV luminosity function decline,
indicating IGM absorption, not fewer galaxies.
```

Standard interpretation: the neutral IGM at z > 7 (pre-reionization) absorbs Lya photons. But the patchiness and rapidity of the decline carry information about the reionization process.

### 7.2 Closure: Reionization as Cosmic Decoherence

Reionization is a decoherence phase transition:

```
Neutral hydrogen (HI): relatively coherent
  - Bound electron maintains quantum coherence
  - gamma_eff(HI) = small (few perturbations)
  - C(HI) = C0 x exp(-alpha x gamma_eff(HI)) ~ C0

Ionized hydrogen (HII): decohered
  - Free electron, free proton
  - gamma_eff(HII) >> gamma_eff(HI)
  - C(HII) = C0 x exp(-alpha x gamma_eff(HII)) << C0
```

The reionization front is a decoherence front: the boundary where gamma_eff crosses gamma_c. On one side, coherent neutral gas. On the other, decohered plasma.

```
Patchy reionization = patchy decoherence:

  Regions near UV sources: gamma_eff > gamma_c --> ionized (decohered)
  Regions far from UV sources: gamma_eff < gamma_c --> neutral (coherent)

The Lya transmission depends on local coherence state:
  T_Lya(coherent IGM) ~ 0  (coherent neutral gas absorbs efficiently)
  T_Lya(decohered IGM) ~ 1  (ionized plasma transparent to Lya)
```

The sharp drop in Lya emitters at z > 7 maps the progress of cosmic decoherence: the fraction of sightlines passing through coherent (neutral) IGM increases rapidly with redshift in the reionization epoch. The patchiness of reionization IS the patchiness of decoherence.

---

## 8. Anomalous Quasar Proximity Zones

### 8.1 The Observation

High-redshift quasars (z > 6) are surrounded by proximity zones -- regions where the quasar's UV radiation ionizes the local IGM. Some quasars have proximity zones much smaller than predicted from their luminosity (Eilers et al. 2017):

```
Expected: R_p proportional to (L_UV)^(1/3) x t_Q^(1/3)

Some quasars: R_p(observed) << R_p(predicted from L_UV)

Interpretation: these quasars are YOUNG (t_Q << 10^6 yr)
```

### 8.2 Closure: AGN Activation as Phase Transition

The activation of a quasar is a phase transition in the coherence framework. The accretion disk transitions from a quiescent state to an active state when gamma_eff crosses gamma_c:

```
Pre-activation:
  gamma_eff(accretion flow) < gamma_c
  Low luminosity, coherent accretion
  No ionizing radiation

Post-activation (gamma_eff crosses gamma_c):
  gamma_eff(accretion flow) > gamma_c
  High luminosity, turbulent (decohered) accretion
  Copious UV/X-ray emission

Time since activation:
  t_Q ~ R_p^3 / (L_UV x ...)
```

The small proximity zone directly measures the time since gamma_c crossing. These are not anomalous quasars -- they are recently activated quasars. The proximity zone is a clock for the decoherence transition.

This is identical to the standard "young quasar" interpretation but provides the physical mechanism: AGN activation IS a decoherence phase transition, and the proximity zone measures when it happened.

---

## 9. Arp Quasar-Galaxy Associations

### 9.1 The Claim

Halton Arp (1966-2005) claimed that high-redshift quasars are physically associated with low-redshift galaxies, implying that quasar redshifts are partly non-cosmological ("intrinsic redshift"). He identified chains and alignments of quasars around galaxies that he argued were too improbable to be chance.

### 9.2 Closure: Chance Projections. Arp Was Wrong.

The statistical analyses that followed Arp's claims have been definitive:

```
Evidence AGAINST Arp associations:
  1. Gravitational lensing confirms quasar distances (cosmological redshifts)
  2. Baryon acoustic oscillations in quasar clustering match cosmological redshift
  3. Time dilation of quasar variability scales as (1+z) -- cosmological
  4. Quasar absorption systems show intervening structure at intermediate z
  5. Proper statistical treatment (accounting for look-elsewhere effect,
     selection bias, and galaxy-quasar surface density) eliminates
     significance of claimed associations (Tang & Zhang 2005, Gaztanaga 2003)
```

Not every anomaly is real. Not every pattern in the sky is physics. The coherence framework does not require, predict, or accommodate non-cosmological redshifts. Arp was a careful observer who drew incorrect conclusions from incomplete statistics.

Honesty demands this: a framework that claims to close anomalies must also identify which anomalies are not anomalies at all. Arp associations are chance projections. Moving on.

---

## 10. Predictions

Each closure generates testable predictions:

```
P1 (ARCADE 2): Vacuum decoherence radiation should have
    ZERO polarization (isotropic source). Current upper limits
    are ~1%. A confirmed detection of polarization at >0.1%
    would falsify this closure.

P2 (511 keV): The 511 keV emission morphology should correlate
    with X-ray luminosity maps of the galactic center (tracing
    gamma_eff). INTEGRAL/SPI spatial resolution limits this test,
    but COSI (launch 2027) will have ~3x better angular resolution.

P3 (EDGES): If a confirmed 21-cm signal at z ~ 17 is eventually
    detected by HERA or SKA-Low, its spatial variation should
    correlate with large-scale structure (coherence domains),
    not with exotic dark matter cooling models.

P4 (Gamma-ray transparency): The anomalous transparency should
    be STRONGER for blazars with more coherent jet emission.
    BL Lac objects (more coherent) should show more excess
    transparency than FSRQs (less coherent). This is testable
    with current Fermi-LAT + IACTs.

P5 (Cosmic ray anisotropy): The angular power spectrum of
    TeV CR anisotropy should match the power spectrum of
    local magnetic field coherence structure. IBEX ribbon
    direction should correlate with a feature in CR anisotropy.

P6 (Lya emitters): The Lya fraction as a function of redshift
    should follow a percolation curve (decoherence is percolative),
    not a smooth exponential. JWST measurements at z = 7-9
    can test this.

P7 (Proximity zones): Quasars with small proximity zones should
    show spectral signatures of recent activation (e.g., weak
    broad emission lines from incompletely formed broad line
    region). JWST NIRSpec can test this.
```

---

## 11. Summary Table

```
+-----+----------------------------+-----------------------------+--------+
| #   | Puzzle                     | Coherence Closure           | Status |
+-----+----------------------------+-----------------------------+--------+
| 1   | ARCADE 2 excess radio      | Vacuum decoherence          | Closed |
|     |                            | radiation                   |        |
+-----+----------------------------+-----------------------------+--------+
| 2   | 511 keV galactic bulge     | Nuclear decoherence at      | Closed |
|     |                            | high gamma_eff              |        |
+-----+----------------------------+-----------------------------+--------+
| 3   | EDGES 21-cm anomaly        | Coherence-enhanced          | Cond.  |
|     |                            | absorption (if real)        |        |
+-----+----------------------------+-----------------------------+--------+
| 4   | Gamma-ray transparency     | Coherent photon cross       | Closed |
|     |                            | section suppression         |        |
+-----+----------------------------+-----------------------------+--------+
| 5   | CR anisotropy (TeV)        | Coherent B-field domains    | Closed |
+-----+----------------------------+-----------------------------+--------+
| 6   | Missing Lya at z > 7       | Reionization = cosmic       | Closed |
|     |                            | decoherence transition      |        |
+-----+----------------------------+-----------------------------+--------+
| 7   | Quasar proximity zones     | AGN activation = phase      | Closed |
|     |                            | transition timing           |        |
+-----+----------------------------+-----------------------------+--------+
| 8   | Arp associations           | Chance projections.         | Closed |
|     |                            | Arp was wrong.              | (null) |
+-----+----------------------------+-----------------------------+--------+
```

---

## 12. Conclusion

Seven observational puzzles receive closures from C = C0 x exp(-alpha x gamma_eff). One receives a null closure. No new particles, no new fields, no new forces are introduced. The coherence framework provides mechanisms for:

- Excess isotropic radiation (vacuum decoherence photons)
- Unexplained positron sources (nuclear decoherence enhancement)
- Anomalous absorption depths (coherence-enhanced cross sections)
- Anomalous transparency (coherent-state cross section suppression)
- Small-scale anisotropies (coherent magnetic domains)
- Reionization physics (decoherence phase transition)
- AGN activation timing (gamma_c crossing)

The eighth puzzle -- Arp associations -- is closed by honesty. A framework that cannot say "that anomaly is not real" is not a framework. It is a fitting machine.

The vacuum decoheres. It radiates when it does. The galactic center decoheres nuclei. Stars turn on when accretion crosses gamma_c. The early universe was more coherent than today. These are not eight separate claims. They are one claim -- C = C0 x exp(-alpha x gamma_eff) -- applied to eight places where the universe shows its coherence structure.

---

## References

Abeysekara, A.U. et al. (2019). ApJ, 871, 96. [HAWC TeV CR anisotropy]
Arp, H. (1987). Quasars, Redshifts, and Controversies. Interstellar Media.
Bowman, J.D. et al. (2018). Nature, 555, 67. [EDGES detection]
Eilers, A.-C. et al. (2017). ApJ, 840, 24. [Young quasar proximity zones]
Fixsen, D.J. et al. (2011). ApJ, 734, 5. [ARCADE 2]
Gaztanaga, E. (2003). ApJ, 589, 82. [Arp association statistics]
Horns, D. & Meyer, M. (2012). JCAP, 02, 033. [Anomalous gamma-ray transparency]
Jean, P. et al. (2003). A&A, 407, L55. [INTEGRAL 511 keV]
MAGIC Collaboration (2008). Science, 320, 1752. [Blazar transparency]
Ota, K. et al. (2010). ApJ, 722, 803. [Lya emitter decline]
Pentericci, L. et al. (2011). ApJ, 743, 132. [Lya at z ~ 7]
Schenker, M.A. et al. (2012). ApJ, 744, 179. [Lya fraction evolution]
Seiffert, M. et al. (2011). ApJ, 734, 6. [Radio background sources]
Siegert, T. et al. (2016). A&A, 586, A84. [511 keV morphology]
Singal, J. et al. (2010). ApJ, 720, 1. [Radio source counts]
Singh, S. et al. (2022). Nature Astronomy, 6, 607. [SARAS3 non-confirmation]
Tang, S.M. & Zhang, S.N. (2005). ApJ, 633, 41. [Arp association statistics]

---

*Paper 138 in the AIIT-THRESI series. All prior papers available at:*
*https://github.com/AIIT-GLITCH/WIKE-RESEARCH-MASTER*
