# PAPER 72: THE NERNST EQUATION AND MEMBRANE DECOHERENCE
## Every Neuron Maintains Coherence via Electrochemical Gradient — The Gate That Won't Close Is a Nernst Instability
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"The Nernst Equation is the Wike Coherence Law at the membrane. Every neuron is solving dρ/dt = −γ[σ_z,[σ_z,ρ]] with ions."*

---

## Abstract

The Nernst Equation (Nernst 1888) gives the equilibrium potential across a membrane for any ion:

```
E_ion = (RT/zF) × ln([ion]_out / [ion]_in)
```

This equation IS the classical analog of the Wike Coherence Law at the cellular membrane scale. The resting membrane potential (−70 mV) is maintained by Na+/K+ ATPase — the exact pump restored by NIR photobiomodulation (Paper 02, Bootstrap Loop). Wind-up sensitization (Paper 16) is a Nernst instability: the Na+ equilibrium potential is driven away from its stable fixed point, and the "gate that won't close" is the Nernst potential at a runaway equilibrium. Every term in the Nernst equation maps to a term in the Wike framework.

---

## 1. The Nernst Equation

For an ion with charge z crossing a membrane:

```
E_Nernst = (RT/zF) × ln([ion]_outside / [ion]_inside)

R = 8.314 J/mol/K   (gas constant = k_B × N_A)
T = 310 K           (body temperature)
z = charge of ion   (Na+: z=+1, K+: z=+1, Ca²+: z=+2, Cl⁻: z=−1)
F = 96485 C/mol     (Faraday constant)
```

**Standard equilibrium potentials:**
```
E_Na+ = (+58 mV) × log([145]/[12]) = +58 × 1.081 = +63 mV
E_K+  = (+58 mV) × log([4]/[150])  = +58 × (−1.574) = −91 mV
E_Ca²+= (+29 mV) × log([1.2]/[0.0001]) = +29 × 4.079 = +118 mV
E_Cl⁻ = (−58 mV) × log([120]/[4])  = −58 × 1.477 = −86 mV
```

The resting membrane potential (−70 mV) is set by the weighted average of these equilibria via the Goldman equation, dominated by K+ permeability at rest.

---

## 2. The f = kT/h Chain Inside the Nernst Equation

From Paper 04: the thermal frequency f = k_BT/h = 6.25 THz at 310K.

The Nernst equation contains R = k_B × N_A:

```
E_Nernst = (k_BT/zF/N_A) × ln(C_ratio)
         = (k_BT/(ze)) × ln(C_ratio)

where e = F/N_A = elementary charge
```

The thermal energy k_BT appears explicitly. The Nernst potential is **proportional to k_BT** — it is a thermally driven potential. At T=0: E_Nernst = 0 (no membrane potential, no gating, no life). At T=T_c: E_Nernst_max (membrane potential destabilizes due to thermal noise).

**The temperature scaling:**

```
E_Nernst(T) = (k_BT/ze) × ln(C_ratio)

dE_Nernst/dT = (k_B/ze) × ln(C_ratio)

At T = 310K → 330K (+20K = approaching T_c):
ΔE_Nernst/E_Nernst = ΔT/T = 20/310 = 6.4%
```

A 20K increase in local temperature (equivalent to moving from body temperature to T_c) increases membrane potentials by 6.4%. This enhanced membrane potential at elevated temperature creates conditions for spontaneous depolarization — the electrical analog of approaching γ_c from the coherence field perspective.

---

## 3. The Na+/K+ ATPase as Bootstrap Engine

The resting membrane potential (−70 mV) is maintained by continuous operation of Na+/K+ ATPase:

```
3 Na+ out, 2 K+ in, per ATP hydrolized
Net: +1 positive charge out per ATP → hyperpolarizing current
Maintains: Na+ gradient ([Na+]_in = 12 mM, [Na+]_out = 145 mM, ratio = 12.1:1)
```

From Paper 02 (Bootstrap Loop): NIR photobiomodulation → mitochondrial ATP production → Na+/K+ ATPase restoration.

**The Nernst equation makes this mechanistic:**

```
NIR → ATP → Na+/K+ ATPase → maintains Na+ gradient → E_Na+ = +63 mV maintained
         ↓
Membrane potential = −70 mV maintained (stable)
         ↓
NMDA receptor threshold maintained at correct depolarization level
         ↓
γ_eff(neural) < γ_c  (gate closes normally)
```

Without NIR/ATP:
```
Na+/K+ ATPase fails → Na+ gradient collapses → E_Na+ → 0 mV
Membrane depolarizes from −70 mV toward 0 mV
NMDA receptor opens at lower threshold
γ_eff(neural) → γ_c  (gate stays open = wind-up sensitization)
```

**Wind-up = Nernst potential failure = membrane γ_c crossing.**

---

## 4. The Nernst Fixed Point and Its Stability

The membrane potential V_m is at a stable equilibrium when:

```
dV_m/dt = −(V_m − V_rest) / τ_m  (linear recovery)

Stable fixed point: V_m* = V_rest = −70 mV
```

This is stable as long as τ_m > 0 (the restoring time constant is positive). This is the Le Chatelier condition (Paper 69) applied to the membrane.

**NMDA wind-up as Nernst instability:**

Under repeated C-fiber stimulation (Paper 16):
1. Na+ influx per pulse accumulates intracellularly
2. Na+/K+ ATPase cannot fully restore gradient between pulses
3. [Na+]_in → increases → E_Na+ → decreases
4. Membrane potential rises toward 0 mV (partial depolarization maintained)
5. NMDA Mg²+ block removed (requires ~−40 mV threshold)
6. Ca²+ influx → intracellular Ca²+ overload → runaway sensitization

**The mathematical statement:**

```
At normal state:
  [Na+]_in = 12, [Na+]_out = 145 → E_Na+ = +63 mV
  Membrane stable at −70 mV (Le Chatelier: κ > 0)

During wind-up:
  [Na+]_in → 30, [Na+]_out = 145 → E_Na+ = +58 × log(145/30) = +58 × 0.684 = +40 mV
  Membrane partial depolarization: V_m → −50 mV
  NMDA threshold breached: persistent Ca²+ influx

This is the Nernst analog of γ_eff → γ_c: the fixed point destabilizes.
```

At the critical point:
```
[Na+]_in = [Na+]_out → E_Na+ = 0 mV → no gradient → total depolarization
Nernst: E = (RT/zF) × ln(1) = 0   ←—  this is the Nernst γ_c
```

When [Na+]_in = [Na+]_out, the Nernst potential vanishes, membrane potential goes to 0 mV, and the neuron is fully depolarized — equivalent to crossing γ_c in the quantum coherence framework.

---

## 5. The Debye Screening Connection

Paper 02 (Bootstrap): EZ water provides Debye screening of thermal noise.

The Debye screening length (Debye-Hückel):
```
λ_D = √(ε₀ε_r k_BT / (e² × Σ_i n_i z_i²))

At 310K, physiological ionic strength (I = 0.15 M):
λ_D = √(8.854×10⁻¹² × 80 × 1.38×10⁻²³ × 310 / (1.6×10⁻¹⁹)² × 2 × 0.15 × 6.022×10²³)
    ≈ 0.8 nm
```

The Debye screening length in physiological saline is 0.8 nm — less than the size of a protein. Without EZ water enhancement (which extends effective λ_D by organizing water structure around charges), thermal fluctuations at the 1-10 nm scale are unscreened and contribute directly to γ_eff.

**EZ water (Paper 02) extends the effective Debye length:**
```
λ_D(EZ) ≈ 2-5 × λ_D(bulk) ≈ 1.6-4 nm
```

This extended screening protects ion channels and receptor binding sites from thermal noise — directly reducing γ_eff at the membrane.

**The Nernst-Bootstrap connection:**
```
NIR → EZ water → extended λ_D → protected Nernst potential → stable membrane potential → γ_eff < γ_c
```

Every term in the Nernst equation (k_BT, ion concentrations, membrane geometry) feeds into the γ_eff calculation. The Nernst equation and the Wike Coherence Law are descriptions of the same membrane physics at different abstraction levels.

---

## 6. The Goldman Equation and Effective γ_eff

The Goldman-Hodgkin-Katz equation gives the true membrane potential when multiple ions contribute:

```
V_m = (RT/F) × ln([P_K × K_out + P_Na × Na_out + P_Cl × Cl_in] /
                   [P_K × K_in  + P_Na × Na_in  + P_Cl × Cl_out])
```

where P_K, P_Na, P_Cl are membrane permeabilities.

The effective γ_eff of the neural membrane is:

```
γ_eff(membrane) = α × k_BT × Σ_i P_i × (V_i − V_m)²
                   ──────────────────────────────────────
                      (ħ × τ_coherence)

where V_i = Nernst potential for ion i
      P_i = permeability of ion i
```

When the membrane is at resting potential (−70 mV) and each ion is near its Nernst potential:
- Driving force for Na+: (−70) − (+63) = −133 mV → large Na+ current when Na+ channels open
- Driving force for K+: (−70) − (−91) = +21 mV → small K+ current at rest
- Small driving forces → small γ_eff contribution per channel

When depolarized toward 0 mV (wind-up):
- Driving forces change: all ions further from their Nernst potentials
- γ_eff(membrane) → γ_c
- The neural gate opens and won't close

---

## Summary

```
Nernst Equation:   E = (RT/zF) × ln(C_ratio)
Wike Analog:       C = C₀ × exp(−α × γ_eff)

Shared parameter:  k_BT appears in both

Stable membrane (−70 mV) = γ_eff < γ_c   (Le Chatelier restoring, Paper 69)
Wind-up (V → 0 mV)       = γ_eff → γ_c   (Nernst fixed point destabilized)
Na+ gradient collapse     = C₀ → 0        (percolation model fails, Paper 63)
NIR → ATP → Na+/K+-ATPase = Bootstrap Loop maintaining Nernst equilibrium

NMDA wind-up is a Nernst instability.
The Bootstrap Loop is a Nernst potential restoration engine.
The Debye screening length is the bridge between the two.
```

*AIIT-THRESI Paper 72*
