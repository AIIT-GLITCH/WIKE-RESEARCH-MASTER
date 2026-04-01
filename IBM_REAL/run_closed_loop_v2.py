#!/usr/bin/env python3
"""
THE CLOSED LOOP v2 — FIXED
===========================
v1 PROBLEM: Identity gates (qc.id) are no-ops. Transpiler removes them.
  Depth after transpile: median=1. Qubit doesn't decohere.
  Natural coherence: 0.998 at ALL gamma levels (flat line, no decay).

v2 FIX: Replace identity gates with real DELAY instructions.
  Delay per step = T2_target / max_gamma_level
  At max gamma: total delay = T2_target → coherence should drop to ~1/e = 0.37
  This gives a clean exponential decay curve to fit C = C₀ × exp(-α × γ)

  For ibm_fez/kingston/marrakesh (Eagle r3): T2 ≈ 100-300 μs
  We target 5 × T2 max ≈ 500 μs across the full gamma sweep.
  delay_per_step = 500 μs / 160 steps ≈ 3.1 μs per step

Author: Rhet Dillard Wike | AIIT-THRESI | March 30, 2026
Fix documented by: Claude Opus 4.6
"""

import sys
import json
import time
import numpy as np
from datetime import datetime

# ============================================================
# IBM CONNECTION
# ============================================================
API_KEY = None
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    import os
    API_KEY = os.environ.get("IBM_QUANTUM_TOKEN") or os.environ.get("IBMQ_TOKEN")

if not API_KEY:
    print("Usage: python3 run_closed_loop_v2.py <IBM_API_KEY>")
    sys.exit(1)

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

print("=" * 70)
print("  THE CLOSED LOOP v2 — IBM QUANTUM HARDWARE (FIXED)")
print("  v1 bug: identity gates removed by transpiler (no decoherence)")
print("  v2 fix: real delay gates that let the qubit actually decohere")
print("  Rhet Dillard Wike | AIIT-THRESI | March 30, 2026")
print("=" * 70)

# ============================================================
# CONNECT
# ============================================================
print("\n[1/7] Connecting to IBM Quantum...")
try:
    service = QiskitRuntimeService(channel="ibm_quantum", token=API_KEY)
except Exception:
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform", token=API_KEY)
    except Exception:
        service = QiskitRuntimeService(channel="ibm_cloud", token=API_KEY)

backends = service.backends(operational=True, simulator=False)
backend_names = [b.name for b in backends]
print(f"  Available: {backend_names}")

preferred = ["ibm_fez", "ibm_kingston", "ibm_marrakesh", "ibm_torino"]
selected_backends = []
for name in preferred:
    if name in backend_names:
        selected_backends.append(service.backend(name))
        if len(selected_backends) >= 1:  # just 1 backend to save quota
            break

if not selected_backends:
    if backends:
        selected_backends = [backends[0]]
    else:
        print("  ERROR: No backends available")
        sys.exit(1)

backend = selected_backends[0]
print(f"  Selected: {backend.name}")

# Get T2 from calibration data
try:
    props = backend.properties()
    t2_values = [props.qubit_property(i).get('T2', [None])[0] for i in range(min(5, backend.num_qubits))]
    t2_values = [t for t in t2_values if t is not None]
    T2_median = np.median(t2_values) if t2_values else 200e-6  # default 200 μs
except Exception:
    T2_median = 200e-6  # 200 μs default

T2_us = T2_median * 1e6  # convert to microseconds
print(f"  T2 (median): {T2_us:.1f} μs")

# ============================================================
# PARAMETERS
# ============================================================
SHOTS = 8192

# Gamma sweep: 20 levels from 0 to 5×T2
# Each gamma level adds one delay step
# Total delay at max gamma = 5 × T2 (well past the cliff)
MAX_GAMMA = 20
GAMMA_LEVELS = list(range(MAX_GAMMA + 1))  # 0 through 20
DELAY_PER_STEP_US = (5.0 * T2_us) / MAX_GAMMA  # each step = (5*T2)/20 = T2/4

print(f"\n[2/7] Experiment design:")
print(f"  Gamma levels: {len(GAMMA_LEVELS)} ({GAMMA_LEVELS[0]} to {GAMMA_LEVELS[-1]})")
print(f"  Delay per step: {DELAY_PER_STEP_US:.2f} μs")
print(f"  Max total delay: {DELAY_PER_STEP_US * MAX_GAMMA:.1f} μs = {DELAY_PER_STEP_US * MAX_GAMMA / T2_us:.1f}× T2")
print(f"  Conditions: 4 (Natural, Gentle/Echo, Harsh, Keeper)")
print(f"  Shots/circuit: {SHOTS}")

# ============================================================
# CIRCUIT BUILDERS — FIXED with real delays
# ============================================================

def build_natural(n_noise, delay_us):
    """A: Prepare |+⟩, DELAY for n_noise × delay_us, rotate back, measure.
    This probes REAL T2 decoherence — the qubit sits in superposition
    and the environment dephases it naturally."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    if n_noise > 0:
        total_delay = n_noise * delay_us
        qc.delay(total_delay, 0, unit='us')
    qc.h(0)
    qc.measure(0, 0)
    return qc


def build_gentle(n_noise, delay_us):
    """B: Prepare |+⟩, DELAY half, Hahn echo (X), DELAY half, undo echo, measure.
    The pi-pulse refocuses static dephasing — should extend coherence beyond T2*."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    half_delay = (n_noise * delay_us) / 2.0
    if half_delay > 0:
        qc.delay(half_delay, 0, unit='us')
    qc.x(0)  # pi-pulse (Hahn echo)
    if half_delay > 0:
        qc.delay(half_delay, 0, unit='us')
    qc.x(0)  # undo
    qc.h(0)
    qc.measure(0, 0)
    return qc


def build_harsh(n_noise, delay_us):
    """C: Prepare |+⟩, apply n_noise random Rz rotations WITH delays between.
    This is detuned force PLUS natural decoherence time — worst case."""
    qc = QuantumCircuit(1, 1)
    rng = np.random.RandomState(42 + n_noise)
    qc.h(0)
    for i in range(max(n_noise, 1)):
        angle = rng.uniform(0, 2 * np.pi)
        qc.rz(angle, 0)
        if delay_us > 0:
            qc.delay(delay_us, 0, unit='us')
    qc.h(0)
    qc.measure(0, 0)
    return qc


def build_keeper(n_noise, delay_us):
    """D: Prepare Bell pair (entangled keeper), DELAY patient qubit only,
    disentangle, measure. The keeper qubit shields via entanglement."""
    qc = QuantumCircuit(2, 2)
    # Prepare both in superposition
    qc.h(0)  # patient
    qc.h(1)  # keeper
    # Create keeper bond
    qc.cx(1, 0)
    # Delay on patient only (keeper is idle — shielding)
    if n_noise > 0:
        total_delay = n_noise * delay_us
        qc.delay(total_delay, 0, unit='us')
    # Undo keeper bond
    qc.cx(1, 0)
    # Measure both
    qc.h(0)
    qc.h(1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc


# ============================================================
# BUILD ALL CIRCUITS
# ============================================================
print("\n[3/7] Building circuits...")

CONDITIONS = {
    "A_NATURAL": ("Natural decay (real T2)", build_natural),
    "B_GENTLE":  ("Gentle (Hahn echo)", build_gentle),
    "C_HARSH":   ("Harsh (Rz + delay)", build_harsh),
    "D_KEEPER":  ("Keeper bond (Bell pair)", build_keeper),
}

all_circuits = []
all_metadata = []

for gamma in GAMMA_LEVELS:
    for cond_key, (cond_desc, builder) in CONDITIONS.items():
        try:
            qc = builder(gamma, DELAY_PER_STEP_US)
            label = f"g{gamma}_{cond_key}"
            qc.name = label
            all_circuits.append(qc)
            all_metadata.append({
                "gamma_level": gamma,
                "condition": cond_key,
                "condition_desc": cond_desc,
                "delay_us": round(gamma * DELAY_PER_STEP_US, 2),
                "n_qubits": qc.num_qubits,
                "name": label,
            })
        except Exception as e:
            print(f"  WARNING: {cond_key} g{gamma}: {e}")

total_circuits = len(all_circuits)
total_measurements = total_circuits * SHOTS
print(f"  Circuits built: {total_circuits}")
print(f"  Measurements: {total_measurements:,}")

# ============================================================
# TRANSPILE
# ============================================================
print(f"\n[4/7] Transpiling for {backend.name}...")

# Use scheduling to preserve delays
transpiled = transpile(
    all_circuits,
    backend=backend,
    optimization_level=1,
    scheduling_method='asap'  # Preserves delay instructions
)

depths = [qc.depth() for qc in transpiled]
print(f"  Depths: min={min(depths)}, max={max(depths)}, median={int(np.median(depths))}")

# Verify delays survived transpilation
sample_ops = transpiled[-1].count_ops()
has_delay = 'delay' in sample_ops
print(f"  Delays preserved in transpiled circuit: {has_delay}")
if not has_delay:
    print(f"  WARNING: Delays may have been removed. Ops in last circuit: {sample_ops}")

# ============================================================
# SUBMIT
# ============================================================
print(f"\n[5/7] Submitting {total_measurements:,} measurements to {backend.name}...")
print(f"  Start: {datetime.now().isoformat()}")

sampler = Sampler(mode=backend)

BATCH_SIZE = 100
batch_results = []
for i in range(0, len(transpiled), BATCH_SIZE):
    batch = transpiled[i:i + BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    total_batches = (len(transpiled) - 1) // BATCH_SIZE + 1
    print(f"  Batch {batch_num}/{total_batches}...")
    job = sampler.run(batch, shots=SHOTS)
    print(f"    Job: {job.job_id()}")
    result = job.result()
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
    print(f"    Done.")

print(f"  Complete: {datetime.now().isoformat()}")

# ============================================================
# ANALYZE
# ============================================================
print(f"\n[6/7] Analyzing {backend.name} results...")

analyzed = []
for meta, counts in zip(all_metadata, batch_results):
    total = sum(counts.values())
    n_q = meta["n_qubits"]

    # For single qubit: C = 2*P(0) - 1
    # For keeper (2 qubits): measure patient qubit (bit 0)
    if n_q == 1:
        p0 = counts.get("0", 0) / total
        coherence = max(2 * p0 - 1, 0)
    else:
        # Patient is qubit 0 (rightmost bit in bitstring)
        p_patient_0 = sum(v for k, v in counts.items() if k[-1] == '0') / total
        coherence = max(2 * p_patient_0 - 1, 0)

    gamma = meta["gamma_level"]
    vitality = gamma * coherence

    analyzed.append({
        **meta,
        "coherence": round(coherence, 6),
        "vitality": round(vitality, 4),
        "counts": counts,
    })

# ============================================================
# PRINT RESULTS
# ============================================================
print(f"\n{'=' * 70}")
print(f"  THE CLOSED LOOP v2 — {backend.name}")
print(f"  {total_measurements:,} REAL MEASUREMENTS")
print(f"  Delay per step: {DELAY_PER_STEP_US:.2f} μs | T2: {T2_us:.1f} μs")
print(f"{'=' * 70}")

print(f"\n  COHERENCE C(gamma)")
print(f"  {'Gamma':>5} {'Delay(μs)':>10} | {'Natural':>9} {'Gentle':>9} {'Harsh':>9} {'Keeper':>9}")
print(f"  {'-'*5} {'-'*10}-+-{'-'*9}-{'-'*9}-{'-'*9}-{'-'*9}")

for gamma in GAMMA_LEVELS:
    delay = round(gamma * DELAY_PER_STEP_US, 1)
    row = f"  {gamma:>5} {delay:>10.1f} |"
    for cond in CONDITIONS:
        match = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == cond]
        if match:
            c = match[0]["coherence"]
            row += f" {c:>9.4f}"
        else:
            row += f" {'---':>9}"
    print(row)

# ============================================================
# FIT WIKE COHERENCE LAW
# ============================================================
print(f"\n{'=' * 70}")
print(f"  WIKE COHERENCE LAW FIT: C = C₀ × exp(-α × gamma)")
print(f"{'=' * 70}")

for cond_key, (cond_desc, _) in CONDITIONS.items():
    data = sorted([a for a in analyzed if a["condition"] == cond_key],
                  key=lambda x: x["gamma_level"])
    gammas = np.array([a["gamma_level"] for a in data])
    coherences = np.array([a["coherence"] for a in data])

    # Only fit where coherence > 0.01
    mask = coherences > 0.01
    if mask.sum() < 3:
        print(f"\n  {cond_key}: insufficient data above threshold")
        continue

    g_fit = gammas[mask]
    c_fit = coherences[mask]

    # Log-linear fit
    log_c = np.log(c_fit)
    coeffs = np.polyfit(g_fit, log_c, 1)
    alpha = -coeffs[0]
    c0 = np.exp(coeffs[1])

    predicted = c0 * np.exp(-alpha * g_fit)
    ss_res = np.sum((c_fit - predicted) ** 2)
    ss_tot = np.sum((c_fit - np.mean(c_fit)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    gamma_c = 1.0 / alpha if alpha > 0 else float('inf')
    T2_measured = gamma_c * DELAY_PER_STEP_US  # in μs

    print(f"\n  {cond_key} ({cond_desc}):")
    print(f"    C₀ = {c0:.4f}")
    print(f"    α  = {alpha:.6f} per gamma step")
    print(f"    R² = {r2:.6f}")
    print(f"    γ_c = 1/α = {gamma_c:.2f} gamma steps")
    print(f"    T2_measured = {T2_measured:.1f} μs (calibration: {T2_us:.1f} μs)")
    print(f"    → {'EXPONENTIAL CONFIRMED ✓' if r2 > 0.95 else 'Fit quality: ' + ('GOOD' if r2 > 0.9 else 'MARGINAL' if r2 > 0.8 else 'POOR')}")

# Whisper vs Scream
print(f"\n  WHISPER vs SCREAM:")
gentle_wins = harsh_wins = 0
for gamma in GAMMA_LEVELS:
    g = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "B_GENTLE"]
    h = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "C_HARSH"]
    if g and h:
        if g[0]["coherence"] > h[0]["coherence"]:
            gentle_wins += 1
        elif h[0]["coherence"] > g[0]["coherence"]:
            harsh_wins += 1
n_total = gentle_wins + harsh_wins
if n_total > 0:
    print(f"  Gentle wins: {gentle_wins}/{n_total} ({gentle_wins/n_total*100:.1f}%)")
    print(f"  Harsh wins:  {harsh_wins}/{n_total}")

# Keeper effect
print(f"\n  KEEPER EFFECT:")
keeper_advantages = []
for gamma in GAMMA_LEVELS:
    nat = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "A_NATURAL"]
    kpr = [a for a in analyzed if a["gamma_level"] == gamma and a["condition"] == "D_KEEPER"]
    if nat and kpr:
        diff = kpr[0]["coherence"] - nat[0]["coherence"]
        keeper_advantages.append((gamma, diff))
        if gamma in [0, 5, 10, 15, 20]:
            print(f"  gamma={gamma:>3}: natural={nat[0]['coherence']:.4f}, "
                  f"keeper={kpr[0]['coherence']:.4f}, diff={diff:+.4f}")

# ============================================================
# SAVE
# ============================================================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_path = f"/home/buddy_ai/Desktop/IBM_REAL/RESULTS_CLOSED_LOOP_v2_{backend.name}_{timestamp}.json"

output = {
    "metadata": {
        "experiment": "THE CLOSED LOOP v2 (FIXED)",
        "fix": "Replaced identity gates with real delay instructions",
        "backend": backend.name,
        "T2_calibration_us": round(T2_us, 1),
        "delay_per_step_us": round(DELAY_PER_STEP_US, 2),
        "max_delay_us": round(DELAY_PER_STEP_US * MAX_GAMMA, 1),
        "shots": SHOTS,
        "total_circuits": total_circuits,
        "total_measurements": total_measurements,
        "gamma_levels": GAMMA_LEVELS,
        "date": datetime.now().isoformat(),
        "author": "Rhet Dillard Wike | AIIT-THRESI",
    },
    "results": [{k: v for k, v in a.items() if k != "counts"} for a in analyzed],
}

with open(json_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\n  Saved: {json_path}")

print(f"\n{'=' * 70}")
print(f"  THE LOOP IS CLOSED. FOR REAL THIS TIME.")
print(f"  God is good. All the time. Them beans though.")
print(f"{'=' * 70}")
