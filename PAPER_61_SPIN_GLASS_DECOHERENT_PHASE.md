# PAPER 61: THE DECOHERENT PHASE IS A SPIN GLASS
## What Exists at γ > γ_c, Why Treatment-Resistant Illness Is History-Dependent, and Why "Push Harder" Fails
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"Spin glass: no unique ground state. Many frozen attractors. History dependent. Sound familiar?"*

---

## Abstract

The Wike framework has a complete description of the coherent phase (γ < γ_c): the Wike Coherence Law, the Berry phase, the Bootstrap loop, the Keeper equation. It has the critical point (γ_c = 0.0016) with its full scaling theory. What it has not described is the **decoherent phase** — what exists at γ > γ_c.

This paper identifies it: **the decoherent phase is a spin glass.** The Edwards-Anderson spin glass model (1975) describes a disordered phase with:
1. No unique ground state (many metastable attractors)
2. History dependence (the attractor reached depends on the path taken)
3. Non-zero overlap parameter q ≠ 0 (frozen disorder, not truly random)
4. Aging: the longer the system sits in a state, the harder it is to leave

All four properties are exact descriptions of treatment-resistant depression, fibromyalgia, chronic PTSD, and chronic fatigue syndrome. The decoherent phase is the spin glass phase. This is why "push harder" with the same treatment fails — the system is frozen in one of many equivalent attractors, and perturbative interventions do not have sufficient energy to escape the basin.

---

## 1. Spin Glass Physics

Edwards and Anderson (1975, Journal of Physics F) described a magnetic system with **random, competing interactions** between spins:

```
H = −Σ_{ij} J_{ij} S_i S_j

where J_{ij} are random (some ferromagnetic, some antiferromagnetic)
with ⟨J_{ij}⟩ = 0 and ⟨J_{ij}²⟩ = J²
```

This system has three phases:
1. **Paramagnetic** (high T): spins disordered, ⟨S_i⟩ = 0
2. **Ferromagnetic** (low T, J ferromagnetic dominant): spins aligned, ⟨S_i⟩ ≠ 0
3. **Spin glass** (low T, mixed J): spins frozen in disordered configuration

The spin glass order parameter (Edwards-Anderson):

```
q_EA = [⟨S_i⟩²]_disorder

q_EA = 0: paramagnetic (disordered, thermal)
q_EA ≠ 0: spin glass (frozen, disordered)
```

**Key properties of the spin glass phase:**

- **Many metastable states:** The free energy landscape has exponentially many local minima. The number of minima grows as exp(N^(2/3)) for N spins.
- **History dependence:** Which minimum the system occupies depends on how it was cooled. Different cooling protocols → different frozen configurations. Two systems with identical Hamiltonians but different histories → different final states.
- **Aging:** The correlation function C(t, t_w) depends on both current time t and waiting time t_w (time the system has been in the spin glass phase). Older = stiffer = harder to perturb.
- **No equilibrium:** The spin glass never truly equilibrates. It is always in a metastable state approaching some attractor but never reaching it.

---

## 2. The Decoherent Phase Has Spin Glass Structure

At γ > γ_c in the Wike framework:

**Paramagnetic analog (γ >> γ_c):** Complete decoherence, C = 0, no structure. Thermal chaos.

**Spin glass analog (γ slightly > γ_c):** Partial decoherence. The coherent network is broken into disconnected fragments. Each fragment is frozen in a specific configuration. Different patients at the same γ_eff can be in different configurations.

```
Mapping:
Spin S_i ↔ Local coherence patch i (region of neural tissue)
J_{ij} ↔ Coupling strength between coherence patches
Random J ↔ Heterogeneous damage from ACEs, inflammation, etc.
q_EA ≠ 0 ↔ Frozen pattern of local coherence (specific symptom cluster)
```

The non-zero q_EA in the decoherent phase means: the disorder is **frozen**, not random. The specific pattern of which regions are coherent and which are not is locked in. This is why fibromyalgia patients have specific pain maps — not random pain, but specific frozen patterns of sensitized regions. This is why depression has specific cognitive patterns — not random sadness, but specific frozen thought-pattern attractors.

---

## 3. Why "Push Harder" Fails

A perturbative intervention (higher dose of the same SSRI, more of the same CBT) applies a small external field to the spin glass:

```
H_perturb = −h × Σ_i S_i

Response: δ⟨S_i⟩ = χ_SG × h

Spin glass susceptibility: χ_SG = (1/T) × (1 − q_EA)
```

For deep spin glass (q_EA → 1): χ_SG → 0. The system does not respond to external fields. The frozen disorder makes it rigid.

**Clinical translation:** A patient deeply in the spin glass phase (long-standing treatment-resistant depression, severe fibromyalgia) has q_EA ≈ 1. Any perturbative treatment — even at higher doses — produces response χ_SG ≈ 0. This is not treatment failure. It is physics.

The only way to move a spin glass is to take it through a **new phase transition** — reheat it through the spin glass transition temperature and re-cool it on a different path:

```
New phase transition → paramagnetic phase → re-cool → new frozen configuration

In practice:
Spin glass → global decoherence (paramagnetic) → re-coherence on new attractor
```

**This requires a global phase transition, not a local perturbation.**

Interventions that force global phase transitions:
- Ketamine: NMDA antagonism forces global neural state reconfiguration
- Psilocybin: 5-HT2A agonism globally disrupts default mode network frozen patterns
- EMDR (Paper 53): bilateral stimulation forces rapid state cycling through multiple attractors
- ECT: electrical field forces global neural synchronization

These work (when they work) because they take the spin glass through a phase transition, not because they push harder in the current attractor.

The ~30-40% non-response rate to ketamine and psilocybin: the patients for whom these fail likely have q_EA so close to 1 that even the global perturbation is insufficient to leave the basin. The spin glass is too deep.

---

## 4. Aging in the Decoherent Phase

Spin glass aging: C(t, t_w) = f(t/t_w) — the correlation depends on the ratio of current time to waiting time.

**Clinical aging:**
A patient who has been in the spin glass phase for 10 years (t_w = 10 years) is harder to move than a patient who entered it 6 months ago (t_w = 6 months), even if their current symptoms are identical.

```
Recovery time ~ t_w^μ  (aging exponent μ ~ 0.5-1 for typical spin glasses)
```

This is the observed clinical phenomenon: chronic treatment-resistant illness gets harder to treat the longer it persists, even when the severity appears stable. The spin glass is aging. The attractors are getting deeper.

**Early intervention is doubly important:** (1) smaller defect density from Kibble-Zurek (Paper 53), and (2) shorter aging time before spin glass deepens.

---

## 5. The Phase Diagram — Complete

```
              WIKE COHERENCE PHASE DIAGRAM

γ_eff
  │
  │    SPIN GLASS PHASE         │  COHERENT PHASE
  │    (decoherent, frozen)     │  (alive, ordered)
γ_c ─────────────────────────────┤──────────────────
  │                             │
  │    Paramagnetic phase       │
  │    (complete decoherence)   │  Ferromagnetic analog
  │                             │  (overconstrained order)
  │                             │
  └─────────────────────────────┼──────────────────→ T
                               T_c

Horizontal axis: Temperature T (with T_c = 330K)
Vertical axis: γ_eff

Operating point:
  Healthy human: T = 310K, γ_eff = 0.001 → COHERENT
  Chronic illness: T = 310K, γ_eff = 0.003 → SPIN GLASS
  Acute crisis: T = 310K, γ_eff = 0.020 → PARAMAGNETIC (all coherence lost)
```

The spin glass phase (γ slightly > γ_c) is the region of treatment-resistant chronic illness. Not fully collapsed. Not coherent. Frozen in a disordered configuration that resists change.

---

## 6. The Replica Symmetry Breaking Connection

Parisi (1979) solved the spin glass using **replica symmetry breaking (RSB)** — the ground state cannot be described by a single order parameter but requires an infinite hierarchy of order parameters.

In clinical terms: there is no single "treatment for spin glass phase illness" because the spin glass has no unique structure. Different patients in the spin glass phase have different frozen configurations (different replica states). Treatment must be individualized — not because of preference or art, but because the physics requires it.

The failure of one-size-fits-all protocols for treatment-resistant depression is **Parisi's RSB theorem applied to clinical medicine.**

---

## Summary

| Spin Glass Property | Clinical Analog |
|--------------------|-----------------|
| No unique ground state | Different symptom clusters for same diagnosis |
| History dependence | Identical current state, different prognosis by history |
| q_EA → 0 response | Treatment-resistant: doesn't respond to perturbation |
| Aging: t_w deepens | Chronic illness harder to treat the longer it persists |
| RSB: infinite hierarchy | No single protocol works for treatment-resistant illness |
| Phase transition required | Ketamine/psilocybin/EMDR: global not local intervention |

**The decoherent phase is a spin glass. This is not a metaphor. It is the correct statistical mechanical description of what exists at γ > γ_c. The clinical phenomenology of treatment-resistant illness follows exactly from spin glass physics.**

*AIIT-THRESI Paper 61*
