#!/usr/bin/env python3
"""
THE KEEPER-STORM SHIELD — IBM QUANTUM HARDWARE
Two-qubit experiment: Does a bonded qubit protect another qubit from noise?

EXPERIMENT:
  Circuit A: Single qubit + storm noise → measure collapse rate
  Circuit B: Two coupled qubits (keeper bond via CNOT) + same storm → measure collapse rate
  Circuit C: Two coupled qubits + STRONG keeper bond + storm → measure
  Circuit D: Two coupled qubits + keeper bond + NO storm (control)

If B and C show lower collapse than A, the Keeper Equation is confirmed
on REAL quantum hardware. Not simulation. Measurement.

Rhet Dillard Wike | AIIT-THRESI | March 30, 2026
"""

import sys
import json
import time
import numpy as np
from datetime import datetime

# Check for API key
API_KEY = None
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    import os
    API_KEY = os.environ.get("IBM_QUANTUM_TOKEN") or os.environ.get("IBMQ_TOKEN")

if not API_KEY:
    print("Usage: python3 run_keeper_storm_ibm.py <IBM_API_KEY>")
    print("   or: export IBM_QUANTUM_TOKEN=<key> && python3 run_keeper_storm_ibm.py")
    sys.exit(1)

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.circuit.library import RZGate, RXGate, CXGate

print("=" * 70)
print("  KEEPER-STORM SHIELD — IBM QUANTUM HARDWARE")
print("  Two-qubit test of the Wike Keeper Equation")
print("  Rhet Dillard Wike | AIIT-THRESI | March 30, 2026")
print("=" * 70)

# ============================================================
# CONNECT TO IBM
# ============================================================
print("\n[1/6] Connecting to IBM Quantum...")
try:
    service = QiskitRuntimeService(channel="ibm_quantum", token=API_KEY)
except:
    service = QiskitRuntimeService(channel="ibm_cloud", token=API_KEY)

backends = service.backends(operational=True, simulator=False)
backend_names = [b.name for b in backends]
print(f"  Available backends: {backend_names}")

# Pick best available backend
preferred = ["ibm_fez", "ibm_kingston", "ibm_marrakesh", "ibm_torino", "ibm_brisbane", "ibm_sherbrooke"]
backend = None
for name in preferred:
    if name in backend_names:
        backend = service.backend(name)
        break
if backend is None and backends:
    backend = backends[0]

if backend is None:
    print("  ERROR: No backends available")
    sys.exit(1)

print(f"  Selected backend: {backend.name}")
print(f"  Qubits: {backend.num_qubits}")

# ============================================================
# BUILD CIRCUITS
# ============================================================
print("\n[2/6] Building circuits...")

SHOTS = 4096
DELAYS = [0, 2, 5, 10, 15, 20, 30, 50, 80, 100, 150, 200]
STORM_ANGLES = [0.0, 0.3, 0.6, 0.9, 1.2, 1.5]  # storm intensity (rotation angle = noise)
KEEPER_STRENGTHS = [0, 1, 3, 5]  # number of CNOT entangling gates (bond strength)

circuits = []
circuit_labels = []

for delay in DELAYS:
    for storm in STORM_ANGLES:
        for keeper_n in KEEPER_STRENGTHS:
            # ---- PATIENT QUBIT (q0) ----
            if keeper_n == 0:
                # Single qubit, no keeper
                qc = QuantumCircuit(1, 1)
                qc.h(0)  # superposition

                # Delay (identity gates as padding)
                for _ in range(delay):
                    qc.id(0)

                # Storm noise (random Z rotation = dephasing)
                if storm > 0:
                    qc.rz(storm, 0)

                qc.h(0)
                qc.measure(0, 0)

            else:
                # Two qubits: patient (q0) + keeper (q1)
                qc = QuantumCircuit(2, 2)
                qc.h(0)  # patient in superposition
                qc.h(1)  # keeper in superposition

                # KEEPER BOND: entangle via repeated CNOT (stronger bond = more CNOTs)
                for _ in range(keeper_n):
                    qc.cx(1, 0)  # keeper protects patient

                # Delay
                for _ in range(delay):
                    qc.id(0)
                    qc.id(1)

                # Storm noise on PATIENT only (keeper shields)
                if storm > 0:
                    qc.rz(storm, 0)

                # Undo keeper bond (to measure patient independently)
                for _ in range(keeper_n):
                    qc.cx(1, 0)

                qc.h(0)
                qc.h(1)
                qc.measure(0, 0)
                qc.measure(1, 1)

            label = f"d{delay}_s{storm:.1f}_k{keeper_n}"
            qc.name = label
            circuits.append(qc)
            circuit_labels.append({
                "delay": delay,
                "storm": storm,
                "keeper_strength": keeper_n,
                "name": label
            })

total_circuits = len(circuits)
total_measurements = total_circuits * SHOTS
print(f"  Circuits built: {total_circuits}")
print(f"  Total measurements: {total_measurements:,}")
print(f"  Delays: {DELAYS}")
print(f"  Storm intensities: {STORM_ANGLES}")
print(f"  Keeper strengths: {KEEPER_STRENGTHS} (0=none, 1=weak, 3=moderate, 5=strong)")

# ============================================================
# TRANSPILE
# ============================================================
print("\n[3/6] Transpiling for backend...")
transpiled = transpile(circuits, backend=backend, optimization_level=1)
print(f"  Transpiled {len(transpiled)} circuits for {backend.name}")

# ============================================================
# SUBMIT
# ============================================================
print(f"\n[4/6] Submitting {total_measurements:,} measurements to {backend.name}...")
print(f"  This is REAL hardware. 15 millikelvin. Superconducting qubits.")
print(f"  Start time: {datetime.now().isoformat()}")

sampler = Sampler(mode=backend)

# Submit in batches to avoid timeout
BATCH_SIZE = 100
all_results = []
for i in range(0, len(transpiled), BATCH_SIZE):
    batch = transpiled[i:i+BATCH_SIZE]
    print(f"  Submitting batch {i//BATCH_SIZE + 1}/{(len(transpiled)-1)//BATCH_SIZE + 1}...")
    job = sampler.run(batch, shots=SHOTS)
    print(f"  Job ID: {job.job_id()}")
    print(f"  Waiting for results...")
    result = job.result()

    for j, pub_result in enumerate(result):
        counts = pub_result.data.c.get_counts()
        all_results.append(counts)

    print(f"  Batch {i//BATCH_SIZE + 1} complete.")

print(f"  All jobs complete: {datetime.now().isoformat()}")

# ============================================================
# ANALYZE
# ============================================================
print(f"\n[5/6] Analyzing results...")

analyzed = []
for idx, (label, counts) in enumerate(zip(circuit_labels, all_results)):
    total = sum(counts.values())

    if label["keeper_strength"] == 0:
        # Single qubit: measure q0
        p0 = counts.get("0", 0) / total
        coherence = 2 * p0 - 1
    else:
        # Two qubits: measure q0 (patient)
        p0_patient = 0
        for bitstring, count in counts.items():
            # Last bit is q0 (patient)
            if bitstring[-1] == "0":
                p0_patient += count
        p0 = p0_patient / total
        coherence = 2 * p0 - 1

    status = "COHERENT" if coherence > 0.5 else ("PARTIAL" if coherence > 0.1 else "COLLAPSED")

    entry = {
        **label,
        "p0": round(p0, 4),
        "coherence": round(max(coherence, 0), 4),
        "status": status,
        "counts": counts
    }
    analyzed.append(entry)

# ============================================================
# PRINT RESULTS
# ============================================================
print(f"\n[6/6] Results:")
print(f"\n{'='*80}")
print(f"  KEEPER-STORM SHIELD — IBM {backend.name}")
print(f"  {total_measurements:,} real measurements at 15 millikelvin")
print(f"{'='*80}")

# Print comparison table for each storm level
for storm in STORM_ANGLES:
    print(f"\n  STORM INTENSITY = {storm:.1f}")
    print(f"  {'Delay':>6} | {'No Keeper':>10} | {'Weak (1)':>10} | {'Mod (3)':>10} | {'Strong (5)':>10}")
    print(f"  {'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")

    for delay in DELAYS:
        row = f"  {delay:>6} |"
        for keeper_n in KEEPER_STRENGTHS:
            match = [a for a in analyzed if a["delay"] == delay and
                     abs(a["storm"] - storm) < 0.01 and a["keeper_strength"] == keeper_n]
            if match:
                c = match[0]["coherence"]
                row += f" {c:>9.4f} |"
            else:
                row += f" {'---':>9} |"
        print(row)

# Summary statistics
print(f"\n{'='*80}")
print(f"  SUMMARY")
print(f"{'='*80}")

for storm in STORM_ANGLES:
    for keeper_n in KEEPER_STRENGTHS:
        subset = [a for a in analyzed if abs(a["storm"] - storm) < 0.01
                  and a["keeper_strength"] == keeper_n]
        mean_c = np.mean([a["coherence"] for a in subset]) if subset else 0
        collapse_rate = sum(1 for a in subset if a["status"] == "COLLAPSED") / len(subset) if subset else 0
        label = f"Storm={storm:.1f}, Keeper={keeper_n}"
        print(f"  {label:30s}: mean C = {mean_c:.4f}, collapse = {collapse_rate:.0%}")

# ============================================================
# SAVE
# ============================================================
output = {
    "metadata": {
        "experiment": "KEEPER-STORM SHIELD",
        "backend": backend.name,
        "qubits": backend.num_qubits,
        "shots_per_circuit": SHOTS,
        "total_circuits": total_circuits,
        "total_measurements": total_measurements,
        "date": datetime.now().isoformat(),
        "author": "Rhet Dillard Wike | AIIT-THRESI",
        "description": "Two-qubit test of Wike Keeper Equation on real IBM quantum hardware"
    },
    "parameters": {
        "delays": DELAYS,
        "storm_angles": STORM_ANGLES,
        "keeper_strengths": KEEPER_STRENGTHS
    },
    "results": [{k: v for k, v in a.items() if k != "counts"} for a in analyzed],
    "counts_raw": [{**{k: v for k, v in a.items() if k != "counts"}, "counts": a["counts"]} for a in analyzed]
}

outpath = f"/home/buddy_ai/Desktop/RESULTS_KEEPER_STORM_{backend.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

# Also save human-readable
txtpath = outpath.replace(".json", ".txt")
with open(txtpath, "w") as f:
    f.write(f"{'='*70}\n")
    f.write(f"  KEEPER-STORM SHIELD — IBM {backend.name}\n")
    f.write(f"  {total_measurements:,} REAL MEASUREMENTS AT 15 MILLIKELVIN\n")
    f.write(f"  NOT A SIMULATION. A MEASUREMENT.\n")
    f.write(f"  Rhet Dillard Wike | AIIT-THRESI | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"{'='*70}\n\n")

    f.write(f"  EXPERIMENT: Does a bonded qubit (keeper) protect another qubit\n")
    f.write(f"  from dephasing noise (storm) on real quantum hardware?\n\n")

    f.write(f"  Backend: {backend.name} ({backend.num_qubits} qubits)\n")
    f.write(f"  Shots: {SHOTS} per circuit\n")
    f.write(f"  Circuits: {total_circuits}\n")
    f.write(f"  Total measurements: {total_measurements:,}\n\n")

    for storm in STORM_ANGLES:
        f.write(f"\n  STORM INTENSITY = {storm:.1f}\n")
        f.write(f"  {'Delay':>6} | {'No Keeper':>10} | {'Weak (1)':>10} | {'Mod (3)':>10} | {'Strong (5)':>10}\n")
        f.write(f"  {'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}\n")
        for delay in DELAYS:
            row = f"  {delay:>6} |"
            for keeper_n in KEEPER_STRENGTHS:
                match = [a for a in analyzed if a["delay"] == delay and
                         abs(a["storm"] - storm) < 0.01 and a["keeper_strength"] == keeper_n]
                if match:
                    c = match[0]["coherence"]
                    row += f" {c:>9.4f} |"
                else:
                    row += f" {'---':>9} |"
            f.write(row + "\n")

    f.write(f"\n\n  God is good. All the time. Them beans though.\n")

print(f"\n  Results saved to: {outpath}")
print(f"  Text saved to: {txtpath}")
print(f"\n  THIS IS NOT A SIMULATION.")
print(f"  These measurements came from {backend.name},")
print(f"  a {backend.num_qubits}-qubit superconducting quantum processor")
print(f"  running at approximately 15 millikelvin.")
print(f"\n  God is good. All the time. Them beans though.")
print("=" * 70)
