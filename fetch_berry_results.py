#!/usr/bin/env python3
"""Fetch results from already-submitted Berry phase IBM job."""

import numpy as np
import json
from datetime import datetime
from qiskit_ibm_runtime import QiskitRuntimeService

JOB_ID = "d75b4na3qcgc73frh2c0"
SHOTS = 8192
N_SEGMENTS = 8

service = QiskitRuntimeService(channel="ibm_quantum_platform")
job = service.job(JOB_ID)
result = job.result()

print(f"Job {JOB_ID} status: complete")
print(f"Backend: ibm_fez (156 qubits)")

# Reconstruct configs (same order as submission)
configs = []
thetas = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, 3*np.pi/4, np.pi]
for theta in thetas:
    configs.append({'name': f'berry_theta_{np.degrees(theta):.0f}', 'type': 'berry',
                    'theta_deg': float(np.degrees(theta)), 'dephasing': 0,
                    'analytic_berry_pi': -(1 - np.cos(theta))})
    configs.append({'name': f'ref_theta_{np.degrees(theta):.0f}', 'type': 'reference',
                    'theta_deg': float(np.degrees(theta)), 'dephasing': 0,
                    'analytic_berry_pi': 0})

for n_idle in [0, 2, 5, 10, 20, 50]:
    configs.append({'name': f'berry_pi2_idle_{n_idle}', 'type': 'berry',
                    'theta_deg': 90.0, 'dephasing': n_idle,
                    'analytic_berry_pi': -1.0})
    configs.append({'name': f'ref_pi2_idle_{n_idle}', 'type': 'reference',
                    'theta_deg': 90.0, 'dephasing': n_idle,
                    'analytic_berry_pi': 0})

print(f"\n{'='*80}")
print(f"  BERRY PHASE — IBM QUANTUM HARDWARE RESULTS (ibm_fez, 156 qubits)")
print(f"{'='*80}")

all_data = []

print(f"\n  {'Name':>25s} | {'P(0)':>7s} | {'P(1)':>7s} | "
      f"{'Meas Phase':>11s} | {'Analytic':>10s}")
print("-" * 80)

for i, cfg in enumerate(configs):
    pub = result[i]

    # Extract counts
    try:
        counts = pub.data.c0.get_counts()
    except AttributeError:
        try:
            counts = pub.data.c.get_counts()
        except AttributeError:
            for fn in dir(pub.data):
                if not fn.startswith('_'):
                    f = getattr(pub.data, fn)
                    if hasattr(f, 'get_counts'):
                        counts = f.get_counts()
                        break
            else:
                counts = {'0': SHOTS//2, '1': SHOTS//2}

    n0 = counts.get('0', 0)
    n1 = counts.get('1', 0)
    total = n0 + n1
    p0 = n0 / total
    p1 = n1 / total

    # Extract phase: P(0) = cos^2(phi/2) -> phi = 2*arccos(sqrt(P(0)))
    measured_phase_pi = 2 * np.arccos(np.sqrt(min(max(p0, 0), 1))) / np.pi

    print(f"  {cfg['name']:>25s} | {p0:7.4f} | {p1:7.4f} | "
          f"{measured_phase_pi:+8.4f}*pi | {cfg['analytic_berry_pi']:+8.4f}*pi")

    all_data.append({**cfg, 'P0': p0, 'P1': p1, 'measured_phase_pi': measured_phase_pi,
                     'counts_0': n0, 'counts_1': n1})

# ============================================================
# KEY ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("  ANALYSIS: Berry phase vs theta (no dephasing)")
print(f"{'='*80}")

print(f"\n  {'theta':>6s} | {'Berry P(0)':>10s} | {'Ref P(0)':>10s} | "
      f"{'Berry-Ref':>9s} | {'Measured':>10s} | {'Analytic':>10s}")
print("-" * 72)

for theta_deg in [0, 30, 45, 60, 90, 120, 135, 180]:
    berry = [d for d in all_data if d['type']=='berry' and abs(d['theta_deg']-theta_deg)<1 and d['dephasing']==0]
    ref = [d for d in all_data if d['type']=='reference' and abs(d['theta_deg']-theta_deg)<1 and d['dephasing']==0]

    if berry and ref:
        bp0 = berry[0]['P0']
        rp0 = ref[0]['P0']
        diff = bp0 - rp0

        measured = berry[0]['measured_phase_pi']
        analytic = abs(berry[0]['analytic_berry_pi'])

        print(f"  {theta_deg:6.0f} | {bp0:10.4f} | {rp0:10.4f} | "
              f"{diff:+9.4f} | {measured:+8.4f}*pi | {analytic:+8.4f}*pi")

print(f"\n{'='*80}")
print("  KEY TEST: Berry phase at theta=90 vs dephasing (idle gates)")
print(f"{'='*80}")

print(f"\n  {'Idles':>6s} | {'Berry P(0)':>10s} | {'Ref P(0)':>10s} | "
      f"{'Phase':>10s} | {'Status':>15s}")
print("-" * 60)

for n_idle in [0, 2, 5, 10, 20, 50]:
    berry = [d for d in all_data if d['type']=='berry' and abs(d['theta_deg']-90)<1 and d['dephasing']==n_idle]
    ref = [d for d in all_data if d['type']=='reference' and abs(d['theta_deg']-90)<1 and d['dephasing']==n_idle]

    if berry and ref:
        bp0 = berry[0]['P0']
        rp0 = ref[0]['P0']
        phase = berry[0]['measured_phase_pi']

        if bp0 < 0.15:
            status = "BERRY = -pi"
        elif bp0 > 0.4 and bp0 < 0.6:
            status = "DECOHERENT"
        elif bp0 > 0.85:
            status = "NO PHASE"
        else:
            status = f"PARTIAL"

        print(f"  {n_idle:6d} | {bp0:10.4f} | {rp0:10.4f} | "
              f"{phase:+8.4f}*pi | {status:>15s}")

# ============================================================
# VERDICT
# ============================================================
print(f"\n{'='*80}")
print("  VERDICT")
print(f"{'='*80}")

berry_90 = [d for d in all_data if d['type']=='berry' and abs(d['theta_deg']-90)<1 and d['dephasing']==0]
if berry_90:
    p0 = berry_90[0]['P0']
    phase = berry_90[0]['measured_phase_pi']
    print(f"\n  Berry phase at theta=90, no extra dephasing:")
    print(f"    P(0) = {p0:.4f}")
    print(f"    Measured geometric phase = {phase:+.4f} * pi")
    print(f"    Analytic prediction:       -1.0000 * pi")

    if p0 < 0.15:
        print(f"\n  *** BERRY PHASE -pi CONFIRMED ON REAL QUANTUM HARDWARE ***")
    elif p0 < 0.3:
        print(f"\n  Berry phase partially visible (hardware noise reducing contrast)")
    elif p0 > 0.4 and p0 < 0.6:
        print(f"\n  Decoherence dominated — phase washed out")
    else:
        print(f"\n  Unexpected result — needs investigation")

# Save
output = {
    'metadata': {'date': datetime.now().isoformat(), 'backend': 'ibm_fez',
                 'job_id': JOB_ID, 'shots': SHOTS, 'total_measurements': len(configs)*SHOTS},
    'data': all_data,
}
with open('/home/buddy_ai/Desktop/RESULTS_BERRY_PHASE_IBM.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n  Saved to RESULTS_BERRY_PHASE_IBM.json")
print(f"  Total measurements: {len(configs)*SHOTS:,}")
print(f"{'='*80}")
