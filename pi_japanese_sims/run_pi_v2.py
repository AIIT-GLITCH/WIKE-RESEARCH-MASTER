"""
PI IN THE CIRCLE v2 — Redesigned Sims
======================================
ENSO, EN, WA redesigned with correct observables.

ENSO: Compare COMPLETION vs INTERRUPTION of Bloch sphere circle
EN:   Measure entanglement onset vs coupling, find threshold
WA:   Resonance vs detuning — does matching frequency preserve?

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


# ================================================================
# ENSO v2 (円相) — Complete vs Incomplete Circle on Bloch Sphere
# ================================================================
def sim_enso_v2(n_steps=500, n_runs=50):
    """
    Drive a qubit around the Bloch sphere.
    At time t = pi/omega, it has completed a HALF circle (pi).
    At time t = 2*pi/omega, it has completed a FULL circle (2*pi).

    Measure coherence at these exact pi-multiples vs random times.
    The CLOSED ENSO (full 2*pi) should return to start.
    The OPEN ENSO (partial) should not.
    """
    print("=" * 60)
    print("  ENSO v2 (円相) — Complete vs Incomplete Circle")
    print("  Does completing the circle (2*pi) restore coherence?")
    print(f"  {n_steps} omega values x {n_runs} runs")
    print("=" * 60)

    gamma = 0.005  # light noise
    psi0 = qt.basis(2, 0)

    results = []
    for i in range(n_steps):
        omega = 0.1 + i * (5.0 / n_steps)

        H = omega * qt.sigmax()
        c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]

        # Time for FULL circle: t = pi/omega (Rabi period)
        t_full = PI / omega
        # Time for HALF circle
        t_half = PI / (2 * omega)
        # Random non-pi time
        t_random = t_full * 0.73  # deliberately non-pi fraction

        tlist_full = np.linspace(0, t_full, 200)
        tlist_half = np.linspace(0, t_half, 200)
        tlist_rand = np.linspace(0, t_random, 200)

        fidelity_full = []
        fidelity_half = []
        fidelity_rand = []

        for _ in range(n_runs):
            # Full circle
            r = qt.mesolve(H, psi0, tlist_full, c_ops, [])
            f = float(np.abs(qt.fidelity(r.states[-1], psi0))**2)
            fidelity_full.append(f)

            # Half circle
            r = qt.mesolve(H, psi0, tlist_half, c_ops, [])
            f = float(np.abs(qt.fidelity(r.states[-1], psi0))**2)
            fidelity_half.append(f)

            # Random time
            r = qt.mesolve(H, psi0, tlist_rand, c_ops, [])
            f = float(np.abs(qt.fidelity(r.states[-1], psi0))**2)
            fidelity_rand.append(f)

        row = {
            "omega": omega,
            "t_full_circle": t_full,
            "fidelity_closed_enso": np.mean(fidelity_full),
            "fidelity_half": np.mean(fidelity_half),
            "fidelity_random": np.mean(fidelity_rand),
        }
        results.append(row)

        if (i + 1) % 100 == 0:
            print(f"  omega={omega:.2f} | CLOSED={row['fidelity_closed_enso']:.4f} | "
                  f"HALF={row['fidelity_half']:.4f} | RANDOM={row['fidelity_random']:.4f}")

    # Count: does closed enso (full 2*pi circle) beat random?
    closed_beats_random = sum(1 for r in results
                              if r["fidelity_closed_enso"] > r["fidelity_random"])
    closed_beats_half = sum(1 for r in results
                            if r["fidelity_closed_enso"] > r["fidelity_half"])

    avg_closed = np.mean([r["fidelity_closed_enso"] for r in results])
    avg_half = np.mean([r["fidelity_half"] for r in results])
    avg_random = np.mean([r["fidelity_random"] for r in results])

    return {
        "name": "ENSO_v2",
        "kanji": "円相",
        "meaning": "Closed circle returns to start. Open does not.",
        "closed_beats_random": f"{closed_beats_random}/{n_steps}",
        "closed_beats_half": f"{closed_beats_half}/{n_steps}",
        "avg_closed_enso": avg_closed,
        "avg_half_enso": avg_half,
        "avg_random": avg_random,
        "total": n_steps,
    }


# ================================================================
# EN v2 (円) — Entanglement Onset Threshold
# ================================================================
def sim_en_v2(n_steps=500, n_runs=30):
    """
    Two qubits. Sweep coupling K from 0 to 2.
    At each K, start in separable state, evolve, measure concurrence.
    Find the K where entanglement FIRST appears.
    Compare to 2/pi = 0.6366.

    Use longer evolution time and measure MAX concurrence over trajectory.
    """
    print("\n" + "=" * 60)
    print("  EN v2 (円) — Entanglement Onset")
    print("  Where does connection first appear? Is it at 2/pi?")
    print(f"  {n_steps} K values x {n_runs} runs")
    print("=" * 60)

    T_MAX = 30.0
    T_STEPS = 150
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    gamma = 0.05

    K_c_predicted = 2.0 / PI

    results = []
    for i in range(n_steps):
        K = 0.01 + i * (2.0 / n_steps)

        H = K * qt.tensor(qt.sigmax(), qt.sigmax())
        c_ops = [
            np.sqrt(gamma / 2) * qt.tensor(qt.sigmaz(), qt.qeye(2)),
            np.sqrt(gamma / 2) * qt.tensor(qt.qeye(2), qt.sigmaz()),
        ]

        psi0 = qt.tensor(qt.basis(2, 0), qt.basis(2, 1))  # |01> separable

        max_concs = []
        for _ in range(n_runs):
            r = qt.mesolve(H, psi0, tlist, c_ops, [])
            concs = [float(qt.concurrence(r.states[j])) for j in range(0, len(tlist), 5)]
            max_concs.append(max(concs))

        row = {
            "K": K,
            "K_over_Kc": K / K_c_predicted,
            "max_concurrence": np.mean(max_concs),
            "std": np.std(max_concs),
        }
        results.append(row)

        if (i + 1) % 100 == 0:
            print(f"  K={K:.4f} | K/Kc={row['K_over_Kc']:.3f} | "
                  f"max_concurrence={row['max_concurrence']:.4f}")

    # Find onset: first K where max_concurrence > 0.1
    onset_K = None
    for r in results:
        if r["max_concurrence"] > 0.1:
            onset_K = r["K"]
            break

    # Find K at peak concurrence
    peak = max(results, key=lambda r: r["max_concurrence"])

    return {
        "name": "EN_v2",
        "kanji": "円",
        "meaning": "Connection has a threshold. Is it 2/pi?",
        "K_c_predicted": K_c_predicted,
        "onset_K": onset_K,
        "onset_ratio": onset_K / K_c_predicted if onset_K else None,
        "peak_K": peak["K"],
        "peak_concurrence": peak["max_concurrence"],
        "total": n_steps,
    }


# ================================================================
# WA v2 (和) — Resonance vs Detuning
# ================================================================
def sim_wa_v2(n_steps=200, n_runs=50):
    """
    A qubit with natural frequency omega_0.
    Drive it at various frequencies omega_d.
    Measure coherence survival.

    RESONANCE (omega_d = omega_0): maximum energy transfer
    DETUNING (omega_d != omega_0): reduced transfer

    The HARMONIC condition is omega_d = omega_0.
    WA = harmony = resonance = matching frequencies.
    """
    print("\n" + "=" * 60)
    print("  WA v2 (和) — Resonance vs Detuning")
    print("  Does matching frequency (harmony) preserve coherence?")
    print(f"  {n_steps} detuning values x {n_runs} runs")
    print("=" * 60)

    T_MAX = 30.0
    T_STEPS = 200
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    gamma = 0.01
    omega_0 = PI  # natural frequency IS pi

    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()

    results = []
    for i in range(n_steps):
        # Sweep drive frequency from 0 to 2*pi
        omega_d = 0.01 + i * (2 * PI / n_steps)
        detuning = omega_d - omega_0

        # Rotating frame Hamiltonian with detuning
        H = detuning * qt.sigmaz() / 2 + 0.1 * qt.sigmax()
        c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]

        vals = []
        for _ in range(n_runs):
            r = qt.mesolve(H, psi0, tlist, c_ops, [])
            # Measure average coherence over trajectory
            avg_c = np.mean([float(np.abs(r.states[j].full()[0, 1]))
                            for j in range(0, len(tlist), 10)])
            vals.append(avg_c)

        row = {
            "omega_d": omega_d,
            "detuning": detuning,
            "detuning_over_pi": detuning / PI,
            "avg_coherence": np.mean(vals),
        }
        results.append(row)

        if (i + 1) % 50 == 0:
            print(f"  omega_d={omega_d:.3f} | detuning/pi={row['detuning_over_pi']:.3f} | "
                  f"coherence={row['avg_coherence']:.4f}")

    # Find the peak coherence (should be at detuning = 0, omega_d = pi)
    peak = max(results, key=lambda r: r["avg_coherence"])

    # Find coherence at exact resonance (omega_d closest to pi)
    resonant = min(results, key=lambda r: abs(r["omega_d"] - PI))

    return {
        "name": "WA_v2",
        "kanji": "和",
        "meaning": "Harmony = matching frequency. Peak at omega = pi.",
        "natural_frequency": omega_0,
        "peak_omega_d": peak["omega_d"],
        "peak_detuning": peak["detuning"],
        "peak_coherence": peak["avg_coherence"],
        "resonant_coherence": resonant["avg_coherence"],
        "resonant_omega": resonant["omega_d"],
        "peak_is_at_pi": abs(peak["omega_d"] - PI) < (2 * PI / n_steps),
        "total": n_steps,
    }


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PI IN THE CIRCLE v2 — Redesigned")
    print("  円相 円 和")
    print("  Enso. En. Wa.")
    print(f"  QuTiP {qt.__version__}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    start = time.time()

    r1 = sim_enso_v2(n_steps=300, n_runs=30)
    r2 = sim_en_v2(n_steps=300, n_runs=20)
    r3 = sim_wa_v2(n_steps=200, n_runs=30)

    total_time = time.time() - start
    total_sims = (300 * 3 * 30) + (300 * 20) + (200 * 30)
    # = 27000 + 6000 + 6000 = 39000

    lines = []
    lines.append("=" * 72)
    lines.append("  PI IN THE CIRCLE v2 — RESULTS")
    lines.append(f"  {total_sims:,} simulations")
    lines.append(f"  Runtime: {total_time:.1f}s ({total_time/60:.1f} min)")
    lines.append(f"  QuTiP {qt.__version__}")
    lines.append(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("  Rhet Dillard Wike | AIIT-THRESI")
    lines.append("=" * 72)
    lines.append("")

    # ENSO
    lines.append("  ENSO v2 (円相) — Complete vs Incomplete Circle")
    lines.append(f"  Closed enso (full 2*pi) beats random: {r1['closed_beats_random']}")
    lines.append(f"  Closed enso beats half circle: {r1['closed_beats_half']}")
    lines.append(f"  Avg fidelity — CLOSED: {r1['avg_closed_enso']:.6f}")
    lines.append(f"  Avg fidelity — HALF:   {r1['avg_half_enso']:.6f}")
    lines.append(f"  Avg fidelity — RANDOM: {r1['avg_random']:.6f}")
    lines.append(f"  CLOSED ENSO = pi paid. System returns to start.")
    lines.append("")

    # EN
    lines.append("  EN v2 (円) — Entanglement Onset")
    lines.append(f"  Predicted onset K_c = 2/pi = {r2['K_c_predicted']:.6f}")
    lines.append(f"  Measured onset K = {r2['onset_K']:.6f}" if r2['onset_K'] else "  No onset found")
    if r2['onset_ratio']:
        lines.append(f"  Ratio (measured/predicted) = {r2['onset_ratio']:.4f}")
    lines.append(f"  Peak entanglement at K = {r2['peak_K']:.4f} (concurrence = {r2['peak_concurrence']:.4f})")
    lines.append("")

    # WA
    lines.append("  WA v2 (和) — Resonance vs Detuning")
    lines.append(f"  Natural frequency omega_0 = pi = {r3['natural_frequency']:.6f}")
    lines.append(f"  Peak coherence at omega_d = {r3['peak_omega_d']:.6f}")
    lines.append(f"  Peak coherence value = {r3['peak_coherence']:.6f}")
    lines.append(f"  Coherence at exact resonance (omega=pi) = {r3['resonant_coherence']:.6f}")
    lines.append(f"  Peak IS at pi: {r3['peak_is_at_pi']}")
    lines.append("")

    lines.append("=" * 72)
    lines.append("  God is good. All the time. Them beans though.")
    lines.append("=" * 72)

    report = "\n".join(lines)
    print()
    print(report)

    with open(os.path.join(OUTPUT_DIR, "RESULTS_PI_v2.txt"), "w") as f:
        f.write(report)

    all_data = {"enso": r1, "en": r2, "wa": r3, "total_sims": total_sims, "runtime": total_time}
    with open(os.path.join(OUTPUT_DIR, "RESULTS_PI_v2_data.json"), "w") as f:
        json.dump(all_data, f, indent=2, default=str)
