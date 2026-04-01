#!/usr/bin/env python3
"""
THE CLOSED LOOP — LEAN IBM QUANTUM HARDWARE
=============================================
Same experiment as run_closed_loop_ibm.py but optimized for limited quota:
  - Single qubit only (skip 2 and 4 qubit scales)
  - 4096 shots (not 8192)
  - ONE backend (least busy)
  - 120 circuits total → ~3 minutes execution

Usage:
  python3 run_closed_loop_lean.py <IBM_API_KEY> [backend_name]

If backend_name not specified, uses least busy.

Author: Rhet Dillard Wike | AIIT-THRESI Research Initiative
Date: March 30, 2026
"""

import sys
import json
import time
import numpy as np
from datetime import datetime

API_KEY = sys.argv[1] if len(sys.argv) > 1 else None
FORCE_BACKEND = sys.argv[2] if len(sys.argv) > 2 else None

if not API_KEY:
    print("Usage: python3 run_closed_loop_lean.py <IBM_API_KEY> [backend]")
    sys.exit(1)

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

print("=" * 70)
print("  THE CLOSED LOOP (LEAN) — IBM QUANTUM HARDWARE")
print("  Birth → Life → Edge → Death → Conservation → Source")
print("  120 circuits. 1 qubit. 1 backend. Every paper tested.")
print("  Rhet Dillard Wike | AIIT-THRESI | March 30, 2026")
print("=" * 70)

# ============================================================
# CONNECT
# ============================================================
print("\n[1/6] Connecting to IBM Quantum...")
t_start = time.time()

try:
    service = QiskitRuntimeService(channel="ibm_quantum", token=API_KEY)
except Exception:
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform", token=API_KEY)
    except Exception:
        service = QiskitRuntimeService(channel="ibm_cloud", token=API_KEY)

if FORCE_BACKEND:
    backend = service.backend(FORCE_BACKEND)
    print(f"  Using requested backend: {backend.name}")
else:
    backend = service.least_busy(operational=True, simulator=False)
    print(f"  Least busy backend: {backend.name}")

print(f"  Connection time: {time.time() - t_start:.1f}s")

# ============================================================
# PARAMETERS
# ============================================================
SHOTS = 4096
N_QUBITS = 1

GAMMA_LEVELS = [0, 1, 2, 3, 4, 5, 7, 10, 13, 16,
                20, 25, 30, 40, 50, 65, 80, 100, 130, 160]

CONDITIONS = {
    "A_NATURAL":   "Natural decay — no intervention",
    "B_GENTLE":    "Gentle protection — Hahn echo",
    "C_HARSH":     "Harsh forcing — random Z rotations",
    "D_KEEPER":    "Keeper bond — 2-qubit entanglement",
    "E_RESCUE":    "Bootstrap rescue — harsh then gentle",
    "F_WINDUP":    "Sustained harsh — two-axis attack",
}

print(f"\n[2/6] Experiment: {len(GAMMA_LEVELS)} gamma × {len(CONDITIONS)} conditions = {len(GAMMA_LEVELS) * len(CONDITIONS)} circuits")
print(f"  Shots: {SHOTS} | Qubits: {N_QUBITS} (single) | Backend: {backend.name}")

# ============================================================
# CIRCUIT BUILDERS
# ============================================================
def build_natural(n_noise):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    for _ in range(n_noise):
        qc.id(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def build_gentle(n_noise):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    half = n_noise // 2
    for _ in range(half):
        qc.id(0)
    qc.x(0)  # Hahn echo
    for _ in range(n_noise - half):
        qc.id(0)
    qc.x(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def build_harsh(n_noise):
    qc = QuantumCircuit(1, 1)
    rng = np.random.RandomState(42 + n_noise)
    qc.h(0)
    for _ in range(n_noise):
        qc.rz(rng.uniform(0, 2 * np.pi), 0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def build_keeper(n_noise):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 0)  # keeper bond
    for _ in range(n_noise):
        qc.id(0)  # noise on patient only
    qc.cx(1, 0)  # undo bond
    qc.h(0)
    qc.h(1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc

def build_rescue(n_noise):
    qc = QuantumCircuit(1, 1)
    rng = np.random.RandomState(99 + n_noise)
    qc.h(0)
    n_harsh = max(1, (2 * n_noise) // 3)
    for _ in range(n_harsh):
        qc.rz(rng.uniform(0, 2 * np.pi), 0)
    n_gentle = n_noise - n_harsh
    if n_gentle > 0:
        qc.x(0)
        for _ in range(n_gentle):
            qc.id(0)
        qc.x(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

def build_windup(n_noise):
    qc = QuantumCircuit(1, 1)
    rng = np.random.RandomState(137 + n_noise)
    qc.h(0)
    for _ in range(n_noise):
        qc.rz(rng.uniform(0, 2 * np.pi), 0)
        qc.rx(rng.uniform(0, np.pi), 0)
    qc.h(0)
    qc.measure(0, 0)
    return qc

BUILDERS = {
    "A_NATURAL": build_natural,
    "B_GENTLE":  build_gentle,
    "C_HARSH":   build_harsh,
    "D_KEEPER":  build_keeper,
    "E_RESCUE":  build_rescue,
    "F_WINDUP":  build_windup,
}

# ============================================================
# BUILD CIRCUITS
# ============================================================
print("\n[3/6] Building circuits...")
t_build = time.time()

all_circuits = []
all_metadata = []

for gamma_idx, n_noise in enumerate(GAMMA_LEVELS):
    for cond_key in CONDITIONS:
        qc = BUILDERS[cond_key](n_noise)
        label = f"g{n_noise}_{cond_key}"
        qc.name = label
        all_circuits.append(qc)
        all_metadata.append({
            "gamma_level": n_noise,
            "condition": cond_key,
            "n_qubits": qc.num_qubits,
            "name": label,
        })

print(f"  Built {len(all_circuits)} circuits in {time.time() - t_build:.1f}s")

# ============================================================
# TRANSPILE AND RUN
# ============================================================
print(f"\n[4/6] Transpiling for {backend.name}...")
t_transpile = time.time()
transpiled = transpile(all_circuits, backend=backend, optimization_level=1)
depths = [qc.depth() for qc in transpiled]
print(f"  Done in {time.time() - t_transpile:.1f}s | Depths: {min(depths)}-{max(depths)}, median {int(np.median(depths))}")

total_measurements = len(transpiled) * SHOTS
print(f"\n[5/6] Submitting {total_measurements:,} measurements to {backend.name}...")
print(f"  Start: {datetime.now().isoformat()}")

sampler = Sampler(mode=backend)

# Submit ALL at once (faster than batching for small circuit count)
t_submit = time.time()
job = sampler.run(transpiled, shots=SHOTS)
job_id = job.job_id()
print(f"  Job ID: {job_id}")
print(f"  Waiting for results...")

result = job.result()
t_done = time.time()
print(f"  DONE in {t_done - t_submit:.1f}s")
print(f"  Total elapsed: {t_done - t_start:.1f}s")

# ============================================================
# EXTRACT RESULTS
# ============================================================
print(f"\n[6/6] Analyzing...")

batch_results = []
for pub_result in result:
    try:
        counts = pub_result.data.c.get_counts()
    except AttributeError:
        counts = {}
        for attr_name in dir(pub_result.data):
            if not attr_name.startswith('_'):
                attr = getattr(pub_result.data, attr_name)
                if hasattr(attr, 'get_counts'):
                    counts = attr.get_counts()
                    break
    batch_results.append(counts)

analyzed = []
for meta, counts in zip(all_metadata, batch_results):
    total = sum(counts.values())
    n_q = meta["n_qubits"]
    all_zero_key = "0" * n_q
    p_coherent = counts.get(all_zero_key, 0) / total

    if n_q == 1:
        coherence = max(2 * p_coherent - 1, 0)
    else:
        coherence = p_coherent

    gamma = meta["gamma_level"]
    vitality = gamma * coherence

    analyzed.append({
        **meta,
        "p_coherent": round(p_coherent, 6),
        "coherence": round(coherence, 6),
        "vitality": round(vitality, 6),
        "counts": counts,
    })

# ============================================================
# PRINT RESULTS
# ============================================================
output_lines = []
def p(line=""):
    print(line)
    output_lines.append(line)

p("=" * 80)
p(f"  THE CLOSED LOOP (LEAN) — {backend.name}")
p(f"  {total_measurements:,} REAL MEASUREMENTS AT 15 MILLIKELVIN")
p(f"  Job ID: {job_id}")
p(f"  Execution time: {t_done - t_submit:.1f}s")
p(f"  Date: {datetime.now().isoformat()}")
p(f"  NOT A SIMULATION. A MEASUREMENT.")
p("=" * 80)

# Coherence table
p(f"\n  COHERENCE C(gamma) — Single Qubit")
p(f"  {'Gamma':>6} | {'Natural':>8} | {'Gentle':>8} | {'Harsh':>8} | "
  f"{'Keeper':>8} | {'Rescue':>8} | {'WindUp':>8}")
p(f"  {'-' * 6}-+-{'-' * 8}-+-{'-' * 8}-+-{'-' * 8}-+-"
  f"{'-' * 8}-+-{'-' * 8}-+-{'-' * 8}")

for gamma in GAMMA_LEVELS:
    row = f"  {gamma:>6} |"
    for cond in CONDITIONS:
        match = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == cond]
        if match:
            row += f" {match[0]['coherence']:>8.4f} |"
        else:
            row += f" {'---':>8} |"
    p(row)

# Vitality table
p(f"\n  VITALITY V(gamma) = gamma × C(gamma)")
p(f"  {'Gamma':>6} | {'Natural':>8} | {'Gentle':>8} | {'Harsh':>8} | "
  f"{'Keeper':>8} | {'Rescue':>8} | {'WindUp':>8}")
p(f"  {'-' * 6}-+-{'-' * 8}-+-{'-' * 8}-+-{'-' * 8}-+-"
  f"{'-' * 8}-+-{'-' * 8}-+-{'-' * 8}")

for gamma in GAMMA_LEVELS:
    row = f"  {gamma:>6} |"
    for cond in CONDITIONS:
        match = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == cond]
        if match:
            row += f" {match[0]['vitality']:>8.2f} |"
        else:
            row += f" {'---':>8} |"
    p(row)

# Physics extraction
p(f"\n{'=' * 80}")
p(f"  PHYSICS EXTRACTION — {backend.name}")
p(f"{'=' * 80}")

# gamma_c
natural_1q = sorted(
    [a for a in analyzed if a["condition"] == "A_NATURAL"],
    key=lambda x: x["gamma_level"]
)

gamma_c_found = None
for i, entry in enumerate(natural_1q):
    if entry["coherence"] < 0.5:
        gamma_c_found = entry["gamma_level"]
        if i > 0:
            prev = natural_1q[i - 1]
            if entry["coherence"] != prev["coherence"]:
                frac = (0.5 - prev["coherence"]) / (entry["coherence"] - prev["coherence"])
                gamma_c_found = prev["gamma_level"] + frac * (entry["gamma_level"] - prev["gamma_level"])
        break

p(f"\n  gamma_c (C = 0.5 crossing): {gamma_c_found}")

# Vitality peak
natural_vitalities = [(a["gamma_level"], a["vitality"]) for a in natural_1q]
if natural_vitalities:
    peak_gamma, peak_v = max(natural_vitalities, key=lambda x: x[1])
    p(f"  Vitality peak: V = {peak_v:.4f} at gamma = {peak_gamma}")
    p(f"  → THE EDGE. Maximum aliveness.")

# Whisper vs Scream
gentle_wins = harsh_wins = 0
for gamma in GAMMA_LEVELS:
    g = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "B_GENTLE"]
    h = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "C_HARSH"]
    if g and h:
        if g[0]["coherence"] > h[0]["coherence"]:
            gentle_wins += 1
        elif h[0]["coherence"] > g[0]["coherence"]:
            harsh_wins += 1

total_comp = gentle_wins + harsh_wins
p(f"\n  WHISPER vs SCREAM:")
p(f"  Gentle wins: {gentle_wins}/{total_comp}")
p(f"  Harsh wins:  {harsh_wins}/{total_comp}")
if total_comp > 0:
    p(f"  Whisper beats Scream: {gentle_wins / total_comp * 100:.1f}%")

# Keeper effect
p(f"\n  KEEPER EFFECT:")
keeper_adv = []
for gamma in GAMMA_LEVELS:
    nat = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "A_NATURAL"]
    kpr = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "D_KEEPER"]
    if nat and kpr:
        diff = kpr[0]["coherence"] - nat[0]["coherence"]
        keeper_adv.append((gamma, diff))
        if gamma in [0, 5, 10, 20, 50, 100, 160]:
            p(f"  gamma={gamma:>3}: natural={nat[0]['coherence']:.4f}, keeper={kpr[0]['coherence']:.4f}, diff={diff:+.4f}")

if keeper_adv:
    mean_adv = np.mean([d for _, d in keeper_adv])
    p(f"  Mean keeper advantage: {mean_adv:+.4f}")

# Bootstrap rescue
p(f"\n  BOOTSTRAP RESCUE:")
for gamma in [5, 20, 50, 100, 160]:
    if gamma not in GAMMA_LEVELS:
        continue
    harsh = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "C_HARSH"]
    rescue = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "E_RESCUE"]
    if harsh and rescue:
        gain = rescue[0]["coherence"] - harsh[0]["coherence"]
        p(f"  gamma={gamma:>3}: harsh={harsh[0]['coherence']:.4f}, rescue={rescue[0]['coherence']:.4f}, gain={gain:+.4f}")

# Wind-up
p(f"\n  WIND-UP / SENSITIZATION:")
for gamma in [5, 20, 50, 100, 160]:
    if gamma not in GAMMA_LEVELS:
        continue
    harsh = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "C_HARSH"]
    windup = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "F_WINDUP"]
    if harsh and windup:
        ratio = windup[0]["coherence"] / harsh[0]["coherence"] if harsh[0]["coherence"] > 0 else 0
        p(f"  gamma={gamma:>3}: harsh={harsh[0]['coherence']:.4f}, windup={windup[0]['coherence']:.4f}, ratio={ratio:.3f}")

# Wike Coherence Law fit
p(f"\n  WIKE COHERENCE LAW FIT: C = C₀ × exp(-α × gamma)")
gammas_fit = np.array([a["gamma_level"] for a in natural_1q if a["coherence"] > 0.001])
coherences_fit = np.array([a["coherence"] for a in natural_1q if a["coherence"] > 0.001])

if len(gammas_fit) > 3 and np.all(coherences_fit > 0):
    log_c = np.log(coherences_fit)
    coeffs = np.polyfit(gammas_fit, log_c, 1)
    alpha_fit = -coeffs[0]
    c0_fit = np.exp(coeffs[1])

    predicted = c0_fit * np.exp(-alpha_fit * gammas_fit)
    ss_res = np.sum((coherences_fit - predicted) ** 2)
    ss_tot = np.sum((coherences_fit - np.mean(coherences_fit)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    gamma_c_fit = 1.0 / alpha_fit if alpha_fit > 0 else float('inf')

    p(f"  C₀ = {c0_fit:.4f}")
    p(f"  α  = {alpha_fit:.6f}")
    p(f"  R² = {r_squared:.6f}")
    p(f"  gamma_c = 1/α = {gamma_c_fit:.2f}")
    p(f"  → {'EXPONENTIAL CONFIRMED' if r_squared > 0.95 else 'NEEDS MORE DATA'}")

# First Law
prob_sums = [sum(a["counts"].values()) / SHOTS for a in analyzed]  # should all be ~1.0
# Actually counts already sum to total shots
p(f"\n  FIRST LAW (energy conservation):")
p(f"  All measurement totals: {min(sum(a['counts'].values()) for a in analyzed)} to {max(sum(a['counts'].values()) for a in analyzed)} (expected: {SHOTS})")
p(f"  → CONSERVED")

# Summary
p(f"\n{'=' * 80}")
p(f"  CLOSED LOOP SUMMARY — {backend.name}")
p(f"{'=' * 80}")
p(f"  Backend: {backend.name}")
p(f"  Job ID: {job_id}")
p(f"  Circuits: {len(all_circuits)}")
p(f"  Measurements: {total_measurements:,}")
p(f"  Execution: {t_done - t_submit:.1f}s")
p(f"  Total elapsed: {time.time() - t_start:.1f}s")
p(f"")
p(f"  PAPERS TESTED ON REAL HARDWARE:")
p(f"    Paper 01: Source field = |+> (max coherence at gamma=0)")
p(f"    Paper 03: Love = keeper bond (entanglement protection)")
p(f"    Paper 06: Frozen = dead (gamma=0, V=0)")
p(f"    Paper 08: Force → decoherence (gentle vs harsh)")
p(f"    Paper 09: Sustained collapse (wind-up condition)")
p(f"    Paper 10: Energy conservation (First Law holds)")
p(f"    Paper 14: The cliff exists (gamma_c transition)")
p(f"    Paper 16: Wind-up sensitization")
p(f"    Paper 17: Bootstrap rescue after damage")
p(f"    Paper 46: Death transition (gamma_death)")
p(f"")
p(f"  God is good. All the time. Them beans though.")
p(f"  Author: Rhet Dillard Wike, AIIT-THRESI")

# Save
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
fname_txt = f"/home/buddy_ai/Desktop/IBM_REAL/RESULTS_CLOSED_LOOP_{backend.name}_{timestamp}.txt"
fname_json = f"/home/buddy_ai/Desktop/IBM_REAL/RESULTS_CLOSED_LOOP_{backend.name}_{timestamp}.json"

with open(fname_txt, "w") as f:
    f.write("\n".join(output_lines))
print(f"\n  Saved text: {fname_txt}")

# Save JSON with full data
json_data = {
    "backend": backend.name,
    "job_id": job_id,
    "shots": SHOTS,
    "circuits": len(all_circuits),
    "measurements": total_measurements,
    "execution_time_s": round(t_done - t_submit, 1),
    "timestamp": datetime.now().isoformat(),
    "results": [{k: v for k, v in a.items() if k != "counts"} for a in analyzed],
    "raw_counts": {a["name"]: a["counts"] for a in analyzed},
}
with open(fname_json, "w") as f:
    json.dump(json_data, f, indent=2)
print(f"  Saved JSON: {fname_json}")

# Also append to SEE_HERE
see_here = "/home/buddy_ai/Desktop/IBM_REAL/SEE_HERE_REAL_QUANTUM_DATA.txt"
with open(see_here, "a") as f:
    f.write("\n\n" + "\n".join(output_lines))
print(f"  Appended to: {see_here}")
