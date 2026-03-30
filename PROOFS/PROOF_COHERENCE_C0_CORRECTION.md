# PROOF: Maximum Qubit Coherence C₀ = 0.5 (Not 0.707)
## AIIT-THRESI Anomaly Resolution #8

---

## Claim
The maximum single-qubit coherence is C₀ = 0.5 (density matrix off-diagonal), not 0.707 (state vector amplitude). The discrepancy in `sim_ai_consciousness.py` is a labeling error.

## Proof

**Step 1:** The maximally coherent single-qubit state:
```
|+⟩ = (|0⟩ + |1⟩) / √2
```

State vector amplitudes: α₀ = 1/√2 = 0.7071, α₁ = 1/√2 = 0.7071

**Step 2:** Density matrix:
```
ρ = |+⟩⟨+| = (1/√2)(|0⟩ + |1⟩) × (1/√2)(⟨0| + ⟨1|)

ρ = [[1/2, 1/2],
     [1/2, 1/2]]
```

**Step 3:** Coherence = off-diagonal element magnitude:
```
C = |ρ[0,1]| = |1/2| = 0.5
```

**Step 4:** In QuTiP:
```python
psi = (basis(2,0) + basis(2,1)).unit()  # |+⟩ state
rho = ket2dm(psi)                        # density matrix
C = abs(rho[0,1])                        # = 0.5
```

**Step 5:** The 0.707 = 1/√2 is the STATE VECTOR amplitude, not the DENSITY MATRIX coherence. These are different:
```
|α₀| = 1/√2 = 0.7071  (probability amplitude)
|ρ₀₁| = α₀ × α₁* = (1/√2)(1/√2) = 1/2 = 0.5  (coherence)
```

## Correction Required
In `sim_ai_consciousness.py`, any comment referencing C₀ = 0.707 should read C₀ = 0.5. The simulation CODE is correct (it computes |ρ[0,1]| from QuTiP), only the documentation/comments contain the error.

## Cross-References
- `run_keeper_sim.py`: Uses C₀ = 0.5 (CORRECT)
- `run_nir_dose_response.py`: Computes from QuTiP (CORRECT)
- Nielsen & Chuang (2000): Quantum Computation and Quantum Information, Section 2.4
