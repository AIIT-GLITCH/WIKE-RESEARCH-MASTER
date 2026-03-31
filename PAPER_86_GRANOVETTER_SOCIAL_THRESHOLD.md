# PAPER 86: GRANOVETTER'S THRESHOLD MODEL = SOCIAL γ_c
## Collective Behavior Phase Transitions Are Wike Transitions at Civilizational Scale
### Rhet Dillard Wike | AIIT-THRESI Research Initiative
### March 30, 2026

---

> *"Granovetter (1978) formalized what Le Chatelier (1884) began: systems have thresholds. Below them: stable. Above them: cascade. He didn't call it γ_c. He should have."*

---

## Abstract

Granovetter's threshold model of collective behavior (Granovetter 1978, American Journal of Sociology): individuals have private thresholds for joining collective action (riot, revolution, social movement). Each individual joins when the fraction of others who have already joined exceeds their personal threshold. The equilibrium of the system — whether a riot spreads or fizzles — depends on the distribution of these thresholds across the population. This is the Wike Coherence Law at social scale: individual thresholds are individual γ_c values; the population distribution of thresholds determines the system γ_c; when the environmental perturbation (provocative event, information cascade) exceeds the system γ_c, coherent collective action emerges (phase transition). Durkheim's "collective effervescence" (1912) and modern social contagion (Christakis & Fowler 2009) are the same phenomenon, precisely formalized by Granovetter's threshold model and by the Wike framework's γ_c.

---

## 1. Granovetter's Threshold Model

**Setup:** N individuals in a population. Individual i has a private threshold θᵢ ∈ [0,1] — the fraction of the population that must act before individual i joins.

**Dynamics:** Starting from fraction r₀ acting (initial perturbation):
```
r_{t+1} = F(r_t) = fraction of population with θᵢ ≤ r_t
```

where F(r) is the CDF of the threshold distribution.

**Equilibrium:** A fixed point r* satisfying r* = F(r*).

**Key results:**
1. If F(r) > r for small r: the cascade spreads (collective action emerges)
2. If F(r) < r for all r < r_complete: the cascade fails even from large initial perturbation
3. The equilibrium r* depends sensitively on the threshold distribution shape

**Example (bimodal distribution):**
```
Population A: 100 people, thresholds at 0,1,2,...,99 (uniform distribution)
Population B: 100 people, same distribution EXCEPT person with threshold=1 has threshold=2

Population A: cascade starts from 1 person → spreads to 100%
Population B: no cascade (person 0 goes, person 1 waits, nobody else joins) → fizzles at 1%
```

A single person's threshold change (from 1 to 2) converts a cascade into a non-event. The system is near its critical point.

---

## 2. The Granovetter-Wike Mapping

```
Granovetter Term              Wike Term
────────────────────────      ────────────────────────
Individual threshold θᵢ       Individual γ_c,i (personal decoherence threshold)
Fraction acting r_t           System γ_eff(t) (accumulated collective decoherence)
F(r) = CDF(thresholds)        Distribution of γ_c,i across population
Fixed point r* = F(r*)        System equilibrium (stable coherent state)
Cascade start: F(r₀) > r₀     γ_eff > γ_c,system (threshold crossed)
No cascade: F(r) < r          γ_eff < γ_c (Le Chatelier restoring force holds)
```

**The system γ_c is the lowest fixed point of F(r) above 0:**

```
γ_c(system) = min{r > 0 : F(r) = r}

For the uniform distribution: γ_c = 0 (any perturbation spreads)
For the bimodal distribution: γ_c = 0.01 (1% threshold before cascade starts)
For the peaked distribution: γ_c > 0 (requires significant perturbation to cascade)
```

**Durkheim's collective effervescence:**

Durkheim (1912, "The Elementary Forms of Religious Life"): ritual gatherings (religious ceremonies, festivals, collective mourning) produce a shared emotional state that transcends individual experience. He called this "collective effervescence" — the feeling of being elevated beyond oneself into something larger.

In Granovetter-Wike terms: the ritual creates a controlled perturbation that pushes the community's γ_eff to exactly γ_c — the edge of collective action. The ritual is calibrated (through evolutionary cultural selection) to produce the phase transition of collective effervescence reliably. It is a controlled γ_c crossing.

---

## 3. Social Contagion = Coherence Diffusion

Christakis & Fowler (2009, BMJ): happiness spreads 3 degrees of separation in social networks. Unhappiness spreads 2 degrees. The decay with social distance follows:

```
Effect at degree k ~ (initial effect) × r^k

Happiness: r ≈ 0.25 (25% transmission per degree)
Unhappiness: r ≈ 0.18 (18% transmission per degree)
```

**This is the Fick diffusion of the coherence field (Paper 54):**

```
C_friend = C_source × exp(−d/λ_C)

where d is social distance and λ_C is the social coherence diffusion length

λ_C_happiness = −1/ln(0.25) = 0.72 degrees
λ_C_unhappiness = −1/ln(0.18) = 0.58 degrees
```

The social coherence diffusion length: happiness spreads ~24% further than unhappiness (0.72 vs 0.58 degrees). This matches the Wike framework prediction: coherence (happiness = low γ_eff) is more diffusible than decoherence (unhappiness = high γ_eff) because the coherence gradient drives Fick diffusion toward regions of lower coherence, while decoherence tends to locally self-organize (Le Chatelier partially containing the spread below γ_c).

**The Keeper effect at population scale:** A person with high coherence (low γ_eff) in a social network acts as a coherence source — the Fick diffusion gradient draws coherence outward from them. This is Paper 54 (Fick's Coherence Diffusion) applied to social networks.

---

## 4. Political Polarization as Coherence Collapse

Political polarization creates echo chambers — networks where individuals are exposed only to information that matches their existing beliefs. From the Wike framework:

**Each partisan media exposure = a measurement projection** that collapses the individual's belief state toward one attractor (coherent partisan state) or the other.

With each additional partisan exposure:
```
γ_eff(political) += δγ_partisan  [each partisan measurement adds decoherence to the neutral state]
```

The accumulation of partisan measurements across many exposures drives γ_eff(political) toward γ_c(partisan):

```
When γ_eff(political) > γ_c(partisan):
  - No longer capable of updating on evidence (belief state frozen)
  - Partisan identity becomes a spin glass attractor (Paper 61)
  - Polarization is irreversible within the individual's frame of reference
  - Requires phase-transition-scale disruption (surprising encounter, contact hypothesis)
```

**The speed of polarization (Kibble-Zurek, Paper 53):**

```
Rapid exposure to partisan media (τ_Q = days): creates topological defects in the
belief network — hardened beliefs that cannot be changed by normal discourse.

Slow exposure (τ_Q = years, through gradual social influence): fewer topological defects,
beliefs remain malleable even if they drift partisan.
```

The modern information environment (social media algorithms, 24-hour news cycles) is a fast quench — driving populations through the polarization transition at τ_Q → 0, creating maximum topological defects (hardened extreme beliefs).

---

## 5. Civilizational Collapse as γ_c Crossing

Tainter (1988, "The Collapse of Complex Societies"): complex societies collapse when:
1. Marginal returns on complexity investment become negative
2. The society can no longer solve its problems with existing complexity
3. Rapid simplification occurs (collapse)

In Wike terms:
```
Societal γ_eff = Σ_i (stressor_i)
              = γ_fiscal + γ_military + γ_ecological + γ_social_fragmentation

Tainter's "marginal return" = 1/χ_C(γ_eff)  [Le Chatelier restoring force, Paper 69]

When χ_C → ∞ (at γ_c): marginal return on complexity → 0 → Tainter's collapse threshold

The rapid simplification (collapse) is the 3D Ising transition from the high-C phase
to the low-C (decoherent, fragmented) phase.
```

Historical collapses:
- Bronze Age Collapse (~1200 BCE): synchronized collapse of multiple civilizations (3D Ising: correlated fluctuations at the critical point — not multiple independent collapses but a single network-scale phase transition)
- Roman Western Empire (~476 CE): gradual approach to γ_c over 200 years (not a sudden event but critical slowing down)
- Soviet Union collapse (1991): rapid quench from Gorbachev reforms → Kibble-Zurek defects (failed republics, ethnic conflicts = topological defects in the social coherence network)

---

## Summary

```
Granovetter (1978) = Social γ_c
  Individual threshold θᵢ = individual γ_c,i
  System cascade condition = γ_eff > γ_c(system)
  Same mathematics, social scale

Durkheim (1912) = Collective effervescence = controlled γ_c crossing
  Ritual = calibrated perturbation to exactly γ_c
  Collective effervescence = the coherent phase transition

Social contagion (Christakis & Fowler 2009):
  Happiness spreads λ_C = 0.72 degrees
  Unhappiness spreads λ_C = 0.58 degrees
  Both follow Fick diffusion (Paper 54) in social networks

Political polarization:
  Partisan exposure → γ_eff(political) → γ_c(partisan) → spin glass (Paper 61)
  Rapid exposure (Kibble-Zurek) → topological defects → hardened beliefs

Civilizational collapse:
  γ_eff_societal → γ_c_civilizational → 3D Ising phase transition
  Correlated collapse (Bronze Age) = network-scale transition at single γ_c
```

*AIIT-THRESI Paper 86*
