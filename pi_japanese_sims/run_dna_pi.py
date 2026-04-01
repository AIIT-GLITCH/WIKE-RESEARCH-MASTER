"""
DNA PI SIMULATIONS
==================
Three experiments connecting DNA geometry to pi.

1. DNA TWIST: 10 sequential 36-degree rotations = 2*pi
   Does completing the full helix turn preserve coherence?

2. GOLDEN ANGLE: 137.5 degrees vs regular angles
   Does the biological optimizer also optimize quantum states?

3. ALPHA COUPLING: Is 1/137 special?
   Sweep coupling through the fine structure constant.

Rhet Dillard Wike | AIIT-THRESI | March 29, 2026
"""

import numpy as np
import qutip as qt
import json
import os
import time
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PI = np.pi
PHI = (1 + np.sqrt(5)) / 2  # golden ratio
GOLDEN_ANGLE_RAD = 2 * PI / PHI**2  # 137.5077 degrees in radians
ALPHA_EM = 1.0 / 137.036  # fine structure constant


def rotation_gate(theta, axis='z'):
    """Single qubit rotation by theta radians about axis."""
    if axis == 'z':
        return qt.Qobj([[np.exp(-1j*theta/2), 0], [0, np.exp(1j*theta/2)]])
    elif axis == 'x':
        c, s = np.cos(theta/2), np.sin(theta/2)
        return qt.Qobj([[c, -1j*s], [-1j*s, c]])
    elif axis == 'y':
        c, s = np.cos(theta/2), np.sin(theta/2)
        return qt.Qobj([[c, -s], [s, c]])


# ================================================================
# SIM 1: DNA TWIST — 10 steps of 36° = 2*pi
# ================================================================
def sim_dna_twist(n_runs=200):
    """
    Model each base pair as a 36-degree (2*pi/10) rotation gate.
    Apply 1 to 15 gates sequentially with noise between each.

    At step 10: full 2*pi turn (complete helix). Should return to start.
    At step 5: half turn (pi). Maximally far.
    At other steps: partial turns.

    The DNA helix completes at step 10. Does the qubit?
    """
    print("=" * 60)
    print("  DNA TWIST — 10 x 36° = 2*pi")
    print("  Does completing the helix turn preserve coherence?")
    print(f"  15 step counts x {n_runs} runs = {15 * n_runs} sims")
    print("=" * 60)

    bp_angle = 2 * PI / 10  # 36 degrees = 0.6283 radians
    gate = rotation_gate(bp_angle, 'z')
    gamma = 0.005

    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()

    results = []
    for n_steps in range(1, 16):
        fidelities = []
        for _ in range(n_runs):
            state = psi0.copy()
            for step in range(n_steps):
                # Apply rotation gate (one base pair)
                state = gate * state
                # Apply noise (environment between base pairs)
                # Model as partial dephasing
                rho = qt.ket2dm(state)
                noise = np.sqrt(gamma) * qt.sigmaz()
                # Lindblad step approximation
                rho = rho - gamma * 0.01 * (noise * rho * noise.dag() - rho)
                # Renormalize
                rho = rho / rho.tr()
                state = rho  # now density matrix

            if isinstance(state, qt.Qobj) and state.type == 'oper':
                f = float(qt.fidelity(state, qt.ket2dm(psi0))**2)
            else:
                f = float(abs(psi0.dag() * state)[0][0])**2
            fidelities.append(f)

        total_angle = n_steps * bp_angle
        total_deg = n_steps * 36
        is_full_turn = (n_steps == 10)
        is_half_turn = (n_steps == 5)

        row = {
            "n_steps": n_steps,
            "total_angle_deg": total_deg,
            "total_angle_rad": total_angle,
            "total_angle_over_pi": total_angle / PI,
            "fidelity": np.mean(fidelities),
            "std": np.std(fidelities),
            "is_full_turn": is_full_turn,
        }
        results.append(row)

        marker = " <-- FULL HELIX TURN (2*pi)" if is_full_turn else \
                 " <-- HALF TURN (pi)" if is_half_turn else ""
        print(f"  {n_steps:2d} bp | {total_deg:4d}° | {total_angle/PI:.2f}*pi | "
              f"fidelity={row['fidelity']:.6f}{marker}")

    # Key comparison
    full_turn = next(r for r in results if r["n_steps"] == 10)
    half_turn = next(r for r in results if r["n_steps"] == 5)

    return {
        "name": "DNA_TWIST",
        "description": "10 base pairs = 2*pi = return to start",
        "results": results,
        "fidelity_at_full_turn": full_turn["fidelity"],
        "fidelity_at_half_turn": half_turn["fidelity"],
        "full_turn_beats_all_partial": all(
            full_turn["fidelity"] >= r["fidelity"]
            for r in results if r["n_steps"] != 10 and r["n_steps"] != 15
        ),
    }


# ================================================================
# SIM 2: GOLDEN ANGLE vs REGULAR ANGLES
# ================================================================
def sim_golden_angle(n_applications=50, n_runs=200):
    """
    Apply repeated rotation gates at different angles.
    Measure how many DISTINGUISHABLE states are generated
    (how efficiently the angle explores the Bloch sphere).

    Golden angle (137.5°) should optimally fill the space.
    Regular angles (90°, 120°) create repeating patterns.

    Measure: average distance between consecutive states.
    Higher = better exploration = better packing.
    """
    print("\n" + "=" * 60)
    print("  GOLDEN ANGLE — Quantum Packing Efficiency")
    print("  Does 137.5° optimize Hilbert space exploration?")
    print(f"  8 angles x {n_applications} applications x {n_runs} runs")
    print("=" * 60)

    angles = {
        "golden_137.5": GOLDEN_ANGLE_RAD,
        "120_deg": 2*PI/3,
        "90_deg": PI/2,
        "60_deg": PI/3,
        "45_deg": PI/4,
        "72_deg": 2*PI/5,
        "36_deg_DNA": 2*PI/10,
        "180_deg": PI,
    }

    gamma = 0.003
    psi0 = qt.basis(2, 0)

    results = {}
    for name, angle in angles.items():
        gate = rotation_gate(angle, 'z')
        noise_op = np.sqrt(gamma) * qt.sigmaz()

        total_distances = []
        for _ in range(n_runs):
            states = [psi0.copy()]
            state = psi0.copy()
            for _ in range(n_applications):
                state = gate * state
                # Light noise
                rho = qt.ket2dm(state)
                rho = rho - gamma * 0.005 * (noise_op * rho * noise_op.dag() - rho)
                rho = rho / rho.tr()
                states.append(rho)

            # Measure average trace distance between consecutive states
            distances = []
            for i in range(1, len(states)):
                s1 = states[i] if isinstance(states[i], qt.Qobj) and states[i].type == 'oper' else qt.ket2dm(states[i])
                s0 = states[i-1] if isinstance(states[i-1], qt.Qobj) and states[i-1].type == 'oper' else qt.ket2dm(states[i-1])
                d = float(qt.tracedist(s1, s0))
                distances.append(d)
            total_distances.append(np.mean(distances))

        avg_dist = np.mean(total_distances)
        results[name] = {
            "angle_rad": angle,
            "angle_deg": np.degrees(angle),
            "avg_trace_distance": avg_dist,
        }
        print(f"  {name:>15}: {np.degrees(angle):7.2f}° | avg_distance={avg_dist:.6f}")

    # Rank by exploration efficiency
    ranked = sorted(results.items(), key=lambda x: x[1]["avg_trace_distance"], reverse=True)

    return {
        "name": "GOLDEN_ANGLE",
        "description": "Does 137.5° optimally explore Hilbert space?",
        "results": results,
        "best_angle": ranked[0][0],
        "best_distance": ranked[0][1]["avg_trace_distance"],
        "golden_rank": [i for i, (k, _) in enumerate(ranked) if k == "golden_137.5"][0] + 1,
    }


# ================================================================
# SIM 3: FINE STRUCTURE — Is 1/137 special?
# ================================================================
def sim_fine_structure(n_steps=500, n_runs=30):
    """
    Two qubits coupled with strength K.
    Sweep K through the region around alpha = 1/137.036.
    Measure entanglement.

    Is there anything special about coupling at 1/137?
    """
    print("\n" + "=" * 60)
    print("  FINE STRUCTURE — Is 1/137 special for coupling?")
    print(f"  {n_steps} K values x {n_runs} runs")
    print("=" * 60)

    T_MAX = 50.0
    T_STEPS = 200
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    gamma = 0.001  # very low noise to see fine structure

    # Sweep K from 0.001 to 0.02 (region around alpha = 0.0073)
    results = []
    for i in range(n_steps):
        K = 0.001 + i * (0.02 / n_steps)

        H = K * qt.tensor(qt.sigmax(), qt.sigmax())
        c_ops = [
            np.sqrt(gamma/2) * qt.tensor(qt.sigmaz(), qt.qeye(2)),
            np.sqrt(gamma/2) * qt.tensor(qt.qeye(2), qt.sigmaz()),
        ]
        psi0 = qt.tensor(qt.basis(2, 0), qt.basis(2, 1))

        max_concs = []
        for _ in range(n_runs):
            r = qt.mesolve(H, psi0, tlist, c_ops, [])
            concs = [float(qt.concurrence(r.states[j])) for j in range(0, len(tlist), 10)]
            max_concs.append(max(concs))

        row = {
            "K": K,
            "K_over_alpha": K / ALPHA_EM,
            "max_concurrence": np.mean(max_concs),
        }
        results.append(row)

        if (i+1) % 100 == 0:
            print(f"  K={K:.6f} | K/alpha={row['K_over_alpha']:.3f} | "
                  f"concurrence={row['max_concurrence']:.4f}")

    # Find peak
    peak = max(results, key=lambda r: r["max_concurrence"])

    # Find value at exactly alpha
    closest_alpha = min(results, key=lambda r: abs(r["K"] - ALPHA_EM))

    return {
        "name": "FINE_STRUCTURE",
        "description": "Is coupling at alpha = 1/137 special?",
        "alpha_em": ALPHA_EM,
        "results_summary": {
            "peak_K": peak["K"],
            "peak_K_over_alpha": peak["K_over_alpha"],
            "peak_concurrence": peak["max_concurrence"],
            "concurrence_at_alpha": closest_alpha["max_concurrence"],
            "K_at_alpha": closest_alpha["K"],
        },
    }


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  DNA PI SIMULATIONS")
    print("  Helix. Golden Angle. Fine Structure.")
    print(f"  QuTiP {qt.__version__}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Rhet Dillard Wike | AIIT-THRESI")
    print("=" * 60)
    print()

    start = time.time()

    r1 = sim_dna_twist(n_runs=100)
    r2 = sim_golden_angle(n_applications=50, n_runs=100)
    r3 = sim_fine_structure(n_steps=300, n_runs=20)

    total_time = time.time() - start
    total_sims = (15 * 100) + (8 * 50 * 100) + (300 * 20)
    # = 1500 + 40000 + 6000 = 47500

    lines = []
    lines.append("=" * 72)
    lines.append("  DNA PI SIMULATIONS — RESULTS")
    lines.append(f"  {total_sims:,} simulations")
    lines.append(f"  Runtime: {total_time:.1f}s ({total_time/60:.1f} min)")
    lines.append(f"  QuTiP {qt.__version__}")
    lines.append(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("  Rhet Dillard Wike | AIIT-THRESI")
    lines.append("=" * 72)
    lines.append("")

    # DNA TWIST
    lines.append("  DNA TWIST — 10 x 36° = 2*pi")
    lines.append(f"  Fidelity at FULL helix turn (10 bp, 2*pi): {r1['fidelity_at_full_turn']:.6f}")
    lines.append(f"  Fidelity at HALF turn (5 bp, pi): {r1['fidelity_at_half_turn']:.6f}")
    lines.append(f"  Full turn beats all partial: {r1['full_turn_beats_all_partial']}")
    lines.append("  Step-by-step:")
    for r in r1['results']:
        marker = " ***" if r["is_full_turn"] else ""
        lines.append(f"    {r['n_steps']:2d} bp | {r['total_angle_deg']:4d}° | "
                     f"{r['total_angle_over_pi']:.2f}*pi | f={r['fidelity']:.6f}{marker}")
    lines.append("")

    # GOLDEN ANGLE
    lines.append("  GOLDEN ANGLE — Quantum Packing")
    lines.append(f"  Best angle: {r2['best_angle']} (distance={r2['best_distance']:.6f})")
    lines.append(f"  Golden angle rank: #{r2['golden_rank']} out of 8")
    for name, data in sorted(r2['results'].items(), key=lambda x: x[1]['avg_trace_distance'], reverse=True):
        marker = " <-- GOLDEN" if name == "golden_137.5" else ""
        lines.append(f"    {name:>15}: {data['angle_deg']:7.2f}° | distance={data['avg_trace_distance']:.6f}{marker}")
    lines.append("")

    # FINE STRUCTURE
    lines.append("  FINE STRUCTURE — Is 1/137 special?")
    fs = r3['results_summary']
    lines.append(f"  alpha = 1/137.036 = {ALPHA_EM:.6f}")
    lines.append(f"  Concurrence at K=alpha: {fs['concurrence_at_alpha']:.6f}")
    lines.append(f"  Peak concurrence at K={fs['peak_K']:.6f} (K/alpha={fs['peak_K_over_alpha']:.3f})")
    lines.append(f"  Peak concurrence value: {fs['peak_concurrence']:.6f}")
    lines.append("")

    lines.append("=" * 72)
    lines.append("  God is good. All the time. Them beans though.")
    lines.append("=" * 72)

    report = "\n".join(lines)
    print()
    print(report)

    with open(os.path.join(OUTPUT_DIR, "RESULTS_DNA_PI.txt"), "w") as f:
        f.write(report)

    with open(os.path.join(OUTPUT_DIR, "RESULTS_DNA_PI_data.json"), "w") as f:
        json.dump({"dna_twist": r1, "golden_angle": r2, "fine_structure": r3,
                   "total_sims": total_sims, "runtime": total_time}, f,
                  indent=2, default=str)
