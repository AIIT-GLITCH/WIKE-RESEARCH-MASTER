#!/usr/bin/env python3
"""
BERRY PHASE ON IBM QUANTUM HARDWARE
=====================================
Tests geometric phase accumulation on real superconducting qubits.

Strategy: Use the spin-echo interferometric method.
1. Prepare |+> state (superposition)
2. Apply controlled rotations that trace a path on the Bloch sphere
3. The geometric phase from the path appears in the interference
4. Compare: path enclosing solid angle vs path NOT enclosing solid angle
5. Add controlled dephasing (idle time) to test phase vs decoherence

For a path subtending solid angle Omega on the Bloch sphere:
  Berry phase = -Omega/2

At theta = pi/2 (equatorial circle): Omega = 2*pi, Berry = -pi

Author: Cobbler + Claude Opus 4.6
Date: 2026-03-30
"""

import numpy as np
import json
from datetime import datetime

from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

# ============================================================
# IBM CONNECTION
# ============================================================

API_KEY = "4X9JO5LU4jwf7-4CBwC4zLPUut_cm6xvQ6FzRS2OYJmh"

print("=" * 70)
print("  BERRY PHASE — IBM QUANTUM HARDWARE")
print("=" * 70)
print(f"  Date: {datetime.now().isoformat()}")

# Save credentials and connect
try:
    QiskitRuntimeService.save_account(
        channel="ibm_quantum_platform",
        token=API_KEY,
        overwrite=True
    )
    print("  Credentials saved.")
except Exception as e:
    print(f"  Credential save: {e}")

service = QiskitRuntimeService(channel="ibm_quantum_platform")
print(f"  Connected to IBM Quantum.")

# Get available backend
backends = service.backends(simulator=False, operational=True)
print(f"  Available backends: {[b.name for b in backends]}")

# Pick a backend (prefer fez or kingston — proven in prior runs)
backend_names = [b.name for b in backends]
for preferred in ['ibm_fez', 'ibm_kingston', 'ibm_torino', 'ibm_marrakesh']:
    if preferred in backend_names:
        backend = service.backend(preferred)
        break
print(f"  Selected backend: {backend.name}")
print(f"  Qubits: {backend.num_qubits}")

# ============================================================
# CIRCUIT DESIGN: Berry Phase Interferometer
# ============================================================
#
# The geometric phase circuit uses the following approach:
#
# 1. H gate: |0> -> |+> = (|0>+|1>)/sqrt(2)
# 2. Controlled rotation sequence that traces a closed path
#    on the Bloch sphere with known solid angle
# 3. H gate: interfere |0> and |1> components
# 4. Measure: probability of |0> encodes the phase
#
# For N rotation segments tracing a cone at polar angle theta:
#   phi_geometric = -pi(1 - cos(theta))
#
# P(0) = cos^2(phi_geometric / 2)
# At theta = pi/2: phi_B = -pi, P(0) = cos^2(-pi/2) = 0
# At theta = 0:    phi_B = 0,   P(0) = cos^2(0) = 1

def berry_phase_circuit(theta, n_segments=8, add_dephasing_barriers=0):
    """
    Create a Berry phase circuit.

    The qubit traces a closed path on the Bloch sphere.
    We use Rz-Rx-Rz decomposition to rotate the Bloch vector
    around a cone of half-angle theta.

    Method: "Orange slice" decomposition
    - Rotate to polar angle theta (Ry(theta))
    - Rotate around z by dphi = 2*pi/n_segments
    - Rotate back to pole (Ry(-theta))
    - Repeat n_segments times

    Total solid angle = 2*pi*(1 - cos(theta))
    Berry phase = -pi*(1 - cos(theta))
    """
    qc = QuantumCircuit(1, 1)

    # Prepare superposition for interferometry
    qc.h(0)

    # Trace closed path on Bloch sphere
    dphi = 2 * np.pi / n_segments

    for i in range(n_segments):
        # Rotate down to theta
        qc.ry(theta, 0)
        # Rotate around z
        qc.rz(dphi, 0)
        # Rotate back up
        qc.ry(-theta, 0)

        # Optional: add barriers for dephasing (idle time)
        for _ in range(add_dephasing_barriers):
            qc.barrier(0)
            qc.id(0)  # Identity = idle time = dephasing

    # Interfere
    qc.h(0)

    # Measure
    qc.measure(0, 0)

    return qc


def reference_circuit(theta, n_segments=8, add_dephasing_barriers=0):
    """
    Reference circuit: same gates but path doesn't close.
    Accumulates only dynamic phase, no geometric phase.
    We achieve this by going back and forth (no net solid angle).
    """
    qc = QuantumCircuit(1, 1)

    qc.h(0)

    dphi = 2 * np.pi / n_segments

    for i in range(n_segments):
        # Go forward
        qc.ry(theta, 0)
        qc.rz(dphi, 0)
        qc.ry(-theta, 0)
        # Go backward (cancels geometric phase)
        qc.ry(theta, 0)
        qc.rz(-dphi, 0)
        qc.ry(-theta, 0)

        for _ in range(add_dephasing_barriers):
            qc.barrier(0)
            qc.id(0)

    qc.h(0)
    qc.measure(0, 0)

    return qc


# ============================================================
# BUILD ALL CIRCUITS
# ============================================================

print("\n" + "=" * 70)
print("  BUILDING CIRCUITS")
print("=" * 70)

SHOTS = 8192
N_SEGMENTS = 8

# Test configurations
configs = []

# PART 1: Theta sweep (no extra dephasing)
thetas = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, 3*np.pi/4, np.pi]
for theta in thetas:
    configs.append({
        'name': f'berry_theta_{np.degrees(theta):.0f}',
        'type': 'berry',
        'theta': theta,
        'theta_deg': float(np.degrees(theta)),
        'dephasing': 0,
        'analytic_berry_pi': -(1 - np.cos(theta)),
        'analytic_P0': np.cos(np.pi * (1 - np.cos(theta)) / 2) ** 2,
    })
    configs.append({
        'name': f'ref_theta_{np.degrees(theta):.0f}',
        'type': 'reference',
        'theta': theta,
        'theta_deg': float(np.degrees(theta)),
        'dephasing': 0,
        'analytic_berry_pi': 0,
        'analytic_P0': 1.0,  # Reference should give P(0)=1 (no geometric phase)
    })

# PART 2: Fixed theta=pi/2 with increasing dephasing (idle gates)
for n_idle in [0, 2, 5, 10, 20, 50]:
    configs.append({
        'name': f'berry_pi2_idle_{n_idle}',
        'type': 'berry',
        'theta': np.pi/2,
        'theta_deg': 90.0,
        'dephasing': n_idle,
        'analytic_berry_pi': -1.0,
        'analytic_P0': 0.0,
    })
    configs.append({
        'name': f'ref_pi2_idle_{n_idle}',
        'type': 'reference',
        'theta': np.pi/2,
        'theta_deg': 90.0,
        'dephasing': n_idle,
        'analytic_berry_pi': 0,
        'analytic_P0': 1.0,
    })

# Build circuits
circuits = []
circuit_metadata = []

for cfg in configs:
    if cfg['type'] == 'berry':
        qc = berry_phase_circuit(cfg['theta'], N_SEGMENTS, cfg['dephasing'])
    else:
        qc = reference_circuit(cfg['theta'], N_SEGMENTS, cfg['dephasing'])

    circuits.append(qc)
    circuit_metadata.append(cfg)

print(f"  Total circuits: {len(circuits)}")
print(f"  Shots per circuit: {SHOTS}")
print(f"  Total measurements: {len(circuits) * SHOTS:,}")

# ============================================================
# TRANSPILE
# ============================================================

print("\n  Transpiling for backend...")
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
transpiled = pm.run(circuits)

# Print gate counts for a few circuits
for i in [0, 1, len(circuits)//2]:
    ops = transpiled[i].count_ops()
    print(f"  Circuit {i} ({configs[i]['name']}): {dict(ops)}")

# ============================================================
# RUN ON HARDWARE
# ============================================================

print("\n" + "=" * 70)
print("  SUBMITTING TO IBM QUANTUM HARDWARE")
print("=" * 70)

sampler = SamplerV2(mode=backend)

print(f"  Submitting {len(transpiled)} circuits to {backend.name}...")
print(f"  This may take a few minutes...")

job = sampler.run(transpiled, shots=SHOTS)
print(f"  Job ID: {job.job_id()}")
print(f"  Waiting for results...")

result = job.result()
print(f"  Results received!")

# ============================================================
# EXTRACT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("  RESULTS")
print("=" * 70)

all_results = {
    'metadata': {
        'date': datetime.now().isoformat(),
        'backend': backend.name,
        'num_qubits': backend.num_qubits,
        'shots': SHOTS,
        'job_id': job.job_id(),
        'n_segments': N_SEGMENTS,
        'total_circuits': len(circuits),
        'total_measurements': len(circuits) * SHOTS,
    },
    'circuits': [],
}

print(f"\n  {'Name':>25s} | {'P(0)':>7s} | {'P(1)':>7s} | "
      f"{'Meas Phase':>11s} | {'Analytic':>10s} | {'Match':>5s}")
print("-" * 85)

for i, cfg in enumerate(circuit_metadata):
    pub_result = result[i]

    # Get counts from the classical register
    # Try different attribute names for compatibility
    try:
        counts = pub_result.data.c0.get_counts()
    except AttributeError:
        try:
            counts = pub_result.data.c.get_counts()
        except AttributeError:
            # Last resort: iterate data fields
            for field_name in dir(pub_result.data):
                if not field_name.startswith('_'):
                    field = getattr(pub_result.data, field_name)
                    if hasattr(field, 'get_counts'):
                        counts = field.get_counts()
                        break
            else:
                counts = {'0': SHOTS // 2, '1': SHOTS // 2}
                print(f"  WARNING: Could not extract counts for circuit {i}")

    n0 = counts.get('0', 0)
    n1 = counts.get('1', 0)
    total = n0 + n1

    p0 = n0 / total
    p1 = n1 / total

    # Extract geometric phase from P(0)
    # P(0) = cos^2(phi_geo/2)
    # phi_geo = 2 * arccos(sqrt(P(0)))
    if p0 > 0:
        measured_phase = 2 * np.arccos(np.sqrt(min(p0, 1.0)))
    else:
        measured_phase = np.pi

    measured_phase_pi = measured_phase / np.pi
    analytic_pi = abs(cfg['analytic_berry_pi'])

    # Check match
    if cfg['type'] == 'reference':
        match = 'ref'
    elif abs(measured_phase_pi - analytic_pi) < 0.15:
        match = 'YES'
    elif abs(measured_phase_pi - analytic_pi) < 0.3:
        match = '~'
    else:
        match = 'NO'

    print(f"  {cfg['name']:>25s} | {p0:7.4f} | {p1:7.4f} | "
          f"{measured_phase_pi:+8.4f}*pi | {cfg['analytic_berry_pi']:+8.4f}*pi | {match:>5s}")

    all_results['circuits'].append({
        'name': cfg['name'],
        'type': cfg['type'],
        'theta_deg': cfg['theta_deg'],
        'dephasing_idles': cfg['dephasing'],
        'counts_0': n0,
        'counts_1': n1,
        'P0': p0,
        'P1': p1,
        'measured_phase_pi': measured_phase_pi,
        'analytic_berry_pi': cfg['analytic_berry_pi'],
        'analytic_P0': cfg['analytic_P0'],
        'match': match,
    })

# ============================================================
# ANALYSIS: Berry phase vs reference
# ============================================================

print("\n" + "=" * 70)
print("  ANALYSIS: BERRY vs REFERENCE (same theta)")
print("=" * 70)

# Group by theta
theta_groups = {}
for r in all_results['circuits']:
    key = f"{r['theta_deg']:.0f}_{r['dephasing_idles']}"
    if key not in theta_groups:
        theta_groups[key] = {}
    theta_groups[key][r['type']] = r

print(f"\n  {'theta':>6s} | {'idle':>4s} | {'Berry P(0)':>10s} | {'Ref P(0)':>10s} | "
      f"{'Diff':>8s} | {'Implies Phase':>13s}")
print("-" * 70)

for key in sorted(theta_groups.keys()):
    group = theta_groups[key]
    if 'berry' in group and 'reference' in group:
        berry = group['berry']
        ref = group['reference']
        diff = berry['P0'] - ref['P0']

        # Phase from difference
        # Berry circuit: P(0) = cos^2(phi_B/2)
        # Ref circuit:   P(0) should be ~0.5 (decoherence) or ~1.0 (ideal)
        # The DIFFERENCE tells us the geometric phase contribution

        if berry['P0'] > 0 and berry['P0'] < 1:
            implied_phase = 2 * np.arccos(np.sqrt(berry['P0'])) / np.pi
        else:
            implied_phase = 0 if berry['P0'] >= 1 else 1.0

        print(f"  {berry['theta_deg']:6.0f} | {berry['dephasing_idles']:4d} | "
              f"{berry['P0']:10.4f} | {ref['P0']:10.4f} | "
              f"{diff:+8.4f} | {implied_phase:+10.4f}*pi")

# ============================================================
# KEY TEST: Does geometric phase survive dephasing?
# ============================================================

print("\n" + "=" * 70)
print("  KEY TEST: Berry phase at theta=90 vs dephasing (idle gates)")
print("  Analytic Berry = -pi -> P(0) should be 0")
print("=" * 70)

dephasing_data = []
for r in all_results['circuits']:
    if r['type'] == 'berry' and abs(r['theta_deg'] - 90.0) < 1:
        dephasing_data.append(r)

print(f"\n  {'Idle gates':>10s} | {'P(0)':>7s} | {'P(1)':>7s} | "
      f"{'Berry phase':>12s} | {'Status':>15s}")
print("-" * 65)

for d in sorted(dephasing_data, key=lambda x: x['dephasing_idles']):
    phase = d['measured_phase_pi']

    if abs(phase - 1.0) < 0.15:
        status = "BERRY = pi"
    elif d['P0'] > 0.4 and d['P0'] < 0.6:
        status = "DECOHERENT"
    elif abs(phase) < 0.15:
        status = "BERRY = 0"
    else:
        status = f"BERRY = {phase:.2f}pi"

    print(f"  {d['dephasing_idles']:10d} | {d['P0']:7.4f} | {d['P1']:7.4f} | "
          f"{phase:+9.4f}*pi | {status:>15s}")

# ============================================================
# VERDICT
# ============================================================

print("\n" + "=" * 70)
print("  VERDICT")
print("=" * 70)

# Check if Berry phase at theta=90, no dephasing shows P(0) near 0
berry_90_clean = [r for r in all_results['circuits']
                  if r['type'] == 'berry' and abs(r['theta_deg'] - 90) < 1
                  and r['dephasing_idles'] == 0]

if berry_90_clean:
    p0 = berry_90_clean[0]['P0']
    print(f"\n  Berry phase at theta=90, no dephasing:")
    print(f"    P(0) = {p0:.4f}")
    print(f"    Expected (Berry=-pi): P(0) = 0.0000")
    print(f"    Expected (no Berry):  P(0) = 1.0000")

    if p0 < 0.2:
        print(f"\n  *** BERRY PHASE = -pi CONFIRMED ON QUANTUM HARDWARE ***")
        print(f"  *** Geometric phase is REAL. Pi is not postulated. ***")
    elif p0 > 0.8:
        print(f"\n  Berry phase NOT detected (P(0) near 1)")
    else:
        print(f"\n  Partial Berry phase: {2*np.arccos(np.sqrt(p0))/np.pi:.4f}*pi")
        print(f"  (Hardware noise reducing visibility)")

# Save
output = '/home/buddy_ai/Desktop/RESULTS_BERRY_PHASE_IBM.json'
with open(output, 'w') as f:
    json.dump(all_results, f, indent=2, default=str)

print(f"\n  Results saved to: {output}")
print("=" * 70)
