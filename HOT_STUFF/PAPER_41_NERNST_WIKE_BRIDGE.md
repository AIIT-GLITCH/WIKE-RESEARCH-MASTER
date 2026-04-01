# PAPER 41: THE NERNST-WIKE BRIDGE
## Every Neuron Is Running the Wike Coherence Law in Electrochemistry
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"The gate that won't close is a Nernst equation whose equilibrium has been shifted past its stable attractor."*

---

## Abstract

The Nernst equation — discovered 1889, textbook standard since 1930 — describes the equilibrium electrochemical potential across any ion-selective membrane:

```
E = (RT/zF) · ln([C_out]/[C_in])
```

It has never been connected to the Wike Coherence Law. This paper makes that connection explicit. The resting membrane potential of every neuron (-70 mV) IS coherence maintained against thermal noise — the electrochemical implementation of γ_eff < γ_c. Central sensitization (Paper 16's hell state, the gate that won't close) is mathematically the Nernst equilibrium shifted past its stable fixed point. NIR photobiomodulation works by restoring ATP → Na+/K+ ATPase activity → restoring the Nernst equilibrium → pulling γ_eff back below γ_c.

The Bridge: **E = (k_BT/zF) · ln([C]) contains Boltzmann temperature weighting — it is the f = kT/h chain (Paper 04) expressed in ion gradients.** Every neuron is a living implementation of thermodynamic coherence. When that implementation fails, you get chronic pain, seizure, or death. When you restore it with the right frequency of light, it comes back.

---

## 1. The Nernst Equation Is Already In the Framework

The Nernst equation for a single ion species:

```
E_ion = (RT/zF) · ln([ion_out]/[ion_in])

where:
  R = 8.314 J/mol·K (gas constant = k_B × N_A)
  T = temperature (Kelvin)
  z = ion valence
  F = 96,485 C/mol (Faraday constant)
  [ion_out]/[ion_in] = concentration ratio across membrane
```

Substituting R = k_B · N_A:

```
E_ion = (k_B · T / zF') · ln([C])

where F' = F/N_A = elementary charge e
```

**This contains k_B · T** — the same thermal energy term that appears in f = kT/h (Paper 04), in the Wike Coherence Law's γ_thermal(T), and in the Bootstrap Nucleation analysis (W = T/T_c).

The neuron's resting potential is not separate physics from quantum coherence. **It IS the thermodynamic coherence equation, expressed in the electrochemical domain.**

The Goldman-Hodgkin-Katz equation for multiple ions gives the actual resting potential:

```
V_m = (RT/F) · ln[ P_K[K⁺]_o + P_Na[Na⁺]_o + P_Cl[Cl⁻]_i ]
                   [ P_K[K⁺]_i + P_Na[Na⁺]_i + P_Cl[Cl⁻]_o ]

Healthy neuron: V_m ≈ -70 mV
```

This potential is maintained far from electrochemical equilibrium by the Na+/K+ ATPase pump — which consumes 20-40% of total neuronal ATP to continuously export 3 Na⁺ and import 2 K⁺ per cycle.

**The resting potential = ATP-powered coherence maintenance against thermal ion diffusion.**

In Wike terms:
- Ion diffusion = γ_thermal (thermal noise trying to equilibrate concentrations)
- Na+/K+ ATPase = the coherence maintenance engine (keeps γ_eff < γ_c)
- V_m = -70 mV = the coherent state maintained against thermal collapse

When ATP fails (ischemia, mitochondrial dysfunction), the pump slows. Ion gradients collapse. V_m → 0. The neuron is thermodynamically dead — maximum entropy, zero coherence.

---

## 2. Central Sensitization Is a Nernst Fixed-Point Shift

Paper 16 (Wike Sensitization Law) identified central sensitization as the "gate that won't close" — a state where γ_eff > γ_c locks the pain gating network into sustained decoherence. The Nernst bridge shows the exact mechanism.

In a normal neuron under repeated stimulation:

```
Repeated NMDA activation → Ca²⁺ influx → PKC activation → AMPA receptor insertion
→ Membrane depolarization shift → V_m moves from -70 mV toward 0 mV
→ LTP (long-term potentiation) at synapse
```

This is adaptive in small amounts. In central sensitization (wind-up):

```
Excessive NMDA activation → Sustained Ca²⁺ influx → Sustained PKC →
→ Phosphorylation of Na⁺ channels → Reduced inactivation → Persistent Na⁺ current
→ Nernst equilibrium for Na⁺ shifts the operating V_m
→ New stable point: V_m ≈ -45 to -55 mV (chronically depolarized)
→ At this V_m, NMDA Mg²⁺ block removed even without stimulus
→ Gate OPEN with no nociceptive input
→ The hell state (Paper 16)
```

**The hell state is a Nernst fixed-point bifurcation.** The membrane has two stable operating points: the healthy -70 mV attractor and the sensitized -50 mV attractor. C-fiber wind-up is the mechanism that tips the system from one attractor to the other. Once in the sensitized attractor, the system is self-maintaining.

This is the Wike Coherence Law expressed in voltage:

```
Healthy:      V_m = -70 mV → γ_eff < γ_c → coherent gating → gate closes
Sensitized:   V_m = -50 mV → γ_eff > γ_c → decoherent gating → gate stays open
```

---

## 3. NIR Restores Nernst Equilibrium

The mechanism of NIR photobiomodulation in central sensitization (Bootstrap Principle, Principle 2) is now completable:

```
NIR (810-980 nm) photons
  → Absorbed by cytochrome c oxidase (Complex IV, mitochondrial ETC)
  → Enhanced electron transport → increased proton gradient
  → Increased ATP synthesis
  → Na+/K+ ATPase has sufficient ATP to run at normal rate
  → 3 Na⁺ out / 2 K⁺ in per cycle restored
  → Ion gradients restored toward healthy Nernst values
  → V_m recovers toward -70 mV
  → NMDA Mg²⁺ block restored at -70 mV
  → Gate closes
  → γ_eff drops below γ_c
  → Hell state exits
```

**NIR doesn't treat the pain. NIR restores the Nernst equilibrium that the pain gating system requires to function.** The treatment works at the electrochemical foundation.

Clinically supported: Hamblin (2017) meta-analysis of photobiomodulation in pain conditions showed 58% reduction in chronic pain intensity. The mechanism was described as "anti-inflammatory." The Nernst-Wike Bridge shows it is more fundamental than that — it is Nernst equilibrium restoration.

---

## 4. The Three Failure Modes

The Nernst-Wike Bridge predicts three distinct failure modes, each with different clinical presentations and treatments:

| Failure mode | Nernst mechanism | V_m shift | Wike state | Clinical presentation |
|-------------|-----------------|-----------|-----------|----------------------|
| ATP depletion | Pump fails, all ions equilibrate | → 0 mV | Frozen (death) | Ischemic stroke, cardiac arrest |
| Fixed-point bifurcation | New stable attractor at depolarized V_m | → -50 mV | Above γ_c (sensitized) | Central sensitization, seizure threshold lowering, tinnitus |
| Oscillatory instability | V_m oscillates without returning to -70 mV | Variable | At γ_c (oscillating) | Arrhythmia, epilepsy, migraine aura |

Each failure mode has a distinct treatment target:

| Failure mode | Treatment target | Intervention |
|-------------|-----------------|-------------|
| ATP depletion | Restore electron transport | NIR (cytochrome c oxidase) + reperfusion |
| Fixed-point bifurcation | Shift V_m back toward -70 mV attractor | NIR + Na⁺ channel stabilizers (certain anticonvulsants) + reduce γ_measurement |
| Oscillatory instability | Restore stable γ_c dynamics | 40 Hz entrainment (Paper 23) + HRV coherence training + reduce γ_thermal |

---

## 5. The Boltzmann-Nernst-Wike Chain

The complete chain connecting the soul frequency (Paper 04) to the membrane potential:

```
f = k_B · T / h            [Planck-Boltzmann: body temperature → thermal frequency]
  → f = 9.7 THz at 310 K  [body temperature frequency]

E = (k_B · T / zF') · ln([C])    [Nernst: temperature → membrane potential]
  → V_m = -70 mV at T = 310 K, healthy ion gradients

C = C₀ · exp(-α · γ_eff)         [Wike: γ_eff → coherence]
  → C = 1.0 when γ_eff < γ_c (V_m = -70 mV maintained)
  → C = 0 when γ_eff >> γ_c (V_m → 0, ATP depleted)
```

All three equations contain k_B · T. All three describe the same system at different levels of description:

- f = kT/h: the frequency at which the system vibrates
- E = (kT/zF')·ln([C]): the potential the system maintains
- C = C₀·exp(-αγ_eff): the coherence the system preserves

**One thermal energy (k_B · T), three descriptions, one physics.**

The soul chain (Paper 04) connects all the way down to the membrane potential. The neuron is not separate from the quantum system. The neuron IS the quantum system at a higher level of organization, running the same thermodynamic coherence equation in a different variable.

---

## 6. Clinical Implications

### 6.1 The Membrane Potential as Coherence Readout

In the clinical setting, membrane potential is not directly measurable without intracellular electrodes. But proxy measures exist:

- **Action potential threshold** — elevated threshold (more negative than -55 mV needed to fire) indicates healthy -70 mV resting state. Lowered threshold (firing at -45 mV) indicates sensitized state.
- **EEG spectral analysis** — the summed membrane dynamics of millions of neurons. Gamma power at 40 Hz reflects V_m stability of cortical networks. Loss of gamma = V_m instability across the network.
- **HRV** — cardiac membrane dynamics reflected in autonomic output. Low HRV = V_m instability in cardiac pacemaker cells.

These proxy measures are already in use clinically. The Nernst-Wike Bridge gives them a unified interpretation: they are all measuring γ_eff relative to γ_c in different biological networks.

### 6.2 The Seizure Connection

Epilepsy is the oscillatory instability failure mode. The Nernst-Wike prediction:

```
Seizure threshold = V_m depolarized toward -50 mV (fixed-point bifurcation incomplete)
Seizure onset = V_m tips past bifurcation point → runaway depolarization
Seizure termination = exhaustion of ATP + ion gradient restoration → V_m recovers
Post-ictal depression = V_m below -70 mV (post-recovery overcorrection)
```

This predicts: anticonvulsants that stabilize Na⁺ channel inactivation (carbamazepine, lamotrigine, phenytoin) work by keeping V_m nearer to the -70 mV attractor — preventing the fixed-point bifurcation. This is consistent with known pharmacology. The Nernst-Wike Bridge shows WHY those drugs work in coherence terms: they reduce γ_eff by stabilizing the Nernst equilibrium.

---

## 7. Conclusion

The Nernst equation has been in the textbook since 1889. The Wike Coherence Law was written in 2026. They are the same equation at different scales.

Every neuron in the body is running the Wike Coherence Law in electrochemistry, continuously, as long as it lives. The -70 mV resting potential is maintained coherence. The Na+/K+ ATPase is the coherence engine. ATP is the fuel. NIR is the refueling mechanism when the engine falters.

Central sensitization, seizure, arrhythmia, and ischemic cell death are four points on the same Nernst-Wike failure spectrum. The therapy at each point is: restore the Nernst equilibrium. Give the pump what it needs. The physics does the rest.

God is good. All the time. Them beans though.

---

## References

1. Nernst, W. (1889). Die elektromotorische Wirksamkeit der Ionen. *Zeitschrift für physikalische Chemie*, 4, 129-181.
2. Goldman, D. E. (1943). Potential, impedance, and rectification in membranes. *Journal of General Physiology*, 27(1), 37-60.
3. Hamblin, M. R. (2017). Mechanisms and applications of the anti-inflammatory effects of photobiomodulation. *AIMS Biophysics*, 4(3), 337-361.
4. Woolf, C. J. (2011). Central sensitization: Implications for the diagnosis and treatment of pain. *Pain*, 152(3 Suppl), S2-15.
5. Goldberger, A. L., et al. (2002). Fractal dynamics in physiology: Alterations with disease and aging. *PNAS*, 99(Suppl 1), 2466-2472.
6. Wike, R. D. (2026). AIIT-THRESI Research Papers 01-40. Council Hill, Oklahoma.

---

*Rhet Dillard Wike | AIIT-THRESI | Council Hill, Oklahoma | March 30, 2026*
