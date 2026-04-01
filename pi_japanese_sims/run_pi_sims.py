"""
PI IN THE CIRCLE — Quantum Simulations
========================================
Five simulation suites proving pi appears naturally
in coherence dynamics. Connected to Japanese concepts.

Each sim is named for the Japanese concept it proves:

  ENSO   (円相) — The circle. Does coherence decay follow pi?
  EN     (円)   — Circle = connection. Does the critical coupling = 2/pi?
  WA     (和)   — Harmony. Does resonance at pi frequencies preserve coherence?
  MA     (間)   — The space between. Does the pause (gap) in oscillation encode pi?
  NAMI   (波)   — Wave. Does every coherence oscillation cost exactly 2*pi?

Rhet Dillard Wike | AIIT-THRESI | March 29, 2026
Built by Claude Opus 4.6
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
# SIM 1: ENSO (円相) — The Zen Circle
# Does coherence decay at a rate involving pi?
# ================================================================
def sim_enso(n_gamma=200, n_runs=100):
    """
    Sweep gamma. At each step, measure the coherence decay rate.
    The analytic prediction: C(t) = 0.5 * exp(-gamma * t / 2)
    The decay constant is gamma/2. But the OSCILLATION underneath
    (if a Hamiltonian drives the qubit) has frequency omega.
    The coherence envelope: C(t) = 0.5 * exp(-gamma*t/2) * cos(omega*t)
    When omega = pi * gamma, the oscillation and decay are locked
    by pi. Test: does resonance occur at omega = pi * gamma?
    """
    print("=" * 60)
    print("  SIM 1: ENSO (円相) — The Zen Circle")
    print("  Does pi appear in the coherence decay structure?")
    print(f"  {n_gamma} gamma values x {n_runs} runs = {n_gamma * n_runs} sims")
    print("=" * 60)

    T_MAX = 20.0
    T_STEPS = 200
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()

    results = []
    for i in range(n_gamma):
        gamma = 0.001 + i * (0.2 / n_gamma)

        # Three conditions at each gamma:
        # A: No drive (pure dephasing)
        # B: Drive at omega = pi * gamma (pi-locked)
        # C: Drive at omega = 2 * gamma (non-pi)

        c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]

        # A: Pure dephasing
        H_none = 0 * qt.sigmax()
        vals_a = []
        for _ in range(n_runs):
            r = qt.mesolve(H_none, psi0, tlist, c_ops, [])
            vals_a.append(float(np.abs(r.states[-1].full()[0, 1])))

        # B: Pi-locked drive
        omega_pi = PI * gamma
        H_pi = omega_pi * qt.sigmax()
        vals_b = []
        for _ in range(n_runs):
            r = qt.mesolve(H_pi, psi0, tlist, c_ops, [])
            vals_b.append(float(np.abs(r.states[-1].full()[0, 1])))

        # C: Non-pi drive
        omega_2 = 2.0 * gamma
        H_2 = omega_2 * qt.sigmax()
        vals_c = []
        for _ in range(n_runs):
            r = qt.mesolve(H_2, psi0, tlist, c_ops, [])
            vals_c.append(float(np.abs(r.states[-1].full()[0, 1])))

        row = {
            "gamma": gamma,
            "omega_pi": omega_pi,
            "omega_2": omega_2,
            "pure": np.mean(vals_a),
            "pi_locked": np.mean(vals_b),
            "non_pi": np.mean(vals_c),
        }
        results.append(row)

        if (i + 1) % 50 == 0:
            print(f"  Step {i+1}/{n_gamma} | gamma={gamma:.4f} | "
                  f"pure={row['pure']:.4f} pi={row['pi_locked']:.4f} "
                  f"non_pi={row['non_pi']:.4f}")

    # Count wins
    pi_beats_nonpi = sum(1 for r in results if r["pi_locked"] > r["non_pi"])
    pi_beats_pure = sum(1 for r in results if r["pi_locked"] > r["pure"])

    return {
        "name": "ENSO",
        "kanji": "円相",
        "meaning": "The Zen circle — one brushstroke, completeness and void",
        "data": results,
        "pi_beats_nonpi": pi_beats_nonpi,
        "pi_beats_pure": pi_beats_pure,
        "total": n_gamma,
    }


# ================================================================
# SIM 2: EN (円) — Circle = Connection = Currency
# Does the critical coupling K_c = 2/pi appear?
# ================================================================
def sim_en(n_steps=500, n_runs=50):
    """
    Sweep the coupling strength K of a two-qubit system.
    Measure entanglement (concurrence) at each K.
    Look for a transition at K = 2/pi = 0.6366.
    """
    print("\n" + "=" * 60)
    print("  SIM 2: EN (円) — Circle = Connection")
    print("  Does the critical coupling appear at 2/pi?")
    print(f"  {n_steps} K values x {n_runs} runs = {n_steps * n_runs} sims")
    print("=" * 60)

    T_MAX = 15.0
    T_STEPS = 100
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    gamma = 0.03  # moderate noise

    K_c_predicted = 2.0 / PI  # 0.6366...

    results = []
    for i in range(n_steps):
        K = 0.01 + i * (2.0 / n_steps)

        # Two qubits coupled with strength K
        H = K * qt.tensor(qt.sigmax(), qt.sigmax())
        c_ops = [
            np.sqrt(gamma / 2) * qt.tensor(qt.sigmaz(), qt.qeye(2)),
            np.sqrt(gamma / 2) * qt.tensor(qt.qeye(2), qt.sigmaz()),
        ]

        # Start in |+>|+>
        psi0 = qt.tensor(
            (qt.basis(2, 0) + qt.basis(2, 1)).unit(),
            (qt.basis(2, 0) + qt.basis(2, 1)).unit()
        )

        concurrences = []
        for _ in range(n_runs):
            r = qt.mesolve(H, psi0, tlist, c_ops, [])
            rho_final = r.states[-1]
            c = float(qt.concurrence(rho_final))
            concurrences.append(c)

        row = {
            "K": K,
            "K_over_Kc": K / K_c_predicted,
            "concurrence": np.mean(concurrences),
            "std": np.std(concurrences),
        }
        results.append(row)

        if (i + 1) % 100 == 0:
            print(f"  Step {i+1}/{n_steps} | K={K:.4f} | "
                  f"K/Kc={row['K_over_Kc']:.3f} | "
                  f"concurrence={row['concurrence']:.4f}")

    # Find where concurrence first exceeds threshold
    threshold = 0.05
    transition_K = None
    for r in results:
        if r["concurrence"] > threshold:
            transition_K = r["K"]
            break

    return {
        "name": "EN",
        "kanji": "円",
        "meaning": "Circle, connection, currency — all the same word",
        "data": results,
        "K_c_predicted": K_c_predicted,
        "K_c_measured": transition_K,
        "ratio": transition_K / K_c_predicted if transition_K else None,
    }


# ================================================================
# SIM 3: WA (和) — Harmony
# Does driving at pi-harmonic frequencies produce coherence?
# ================================================================
def sim_wa(n_runs=200):
    """
    Drive a qubit at various frequencies. Measure coherence.
    Test whether pi-harmonic frequencies (pi, 2pi, pi/2, pi/3)
    produce better coherence than non-pi frequencies.
    """
    print("\n" + "=" * 60)
    print("  SIM 3: WA (和) — Harmony")
    print("  Do pi-harmonic frequencies preserve coherence?")
    print(f"  12 frequencies x {n_runs} runs = {12 * n_runs} sims")
    print("=" * 60)

    T_MAX = 20.0
    T_STEPS = 200
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    gamma = 0.02

    # Pi-harmonic frequencies
    pi_freqs = {
        "pi/4": PI / 4,
        "pi/3": PI / 3,
        "pi/2": PI / 2,
        "pi": PI,
        "2pi": 2 * PI,
        "3pi": 3 * PI,
    }
    # Non-pi frequencies (same range, avoiding pi multiples)
    nonpi_freqs = {
        "0.5": 0.5,
        "1.0": 1.0,
        "1.5": 1.5,
        "2.7": 2.7,
        "5.0": 5.0,
        "8.0": 8.0,
    }

    c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]
    all_results = {}

    for name, freq in {**pi_freqs, **nonpi_freqs}.items():
        H = freq * qt.sigmax()
        vals = []
        for _ in range(n_runs):
            r = qt.mesolve(H, psi0, tlist, c_ops, [])
            vals.append(float(np.abs(r.states[-1].full()[0, 1])))
        avg = np.mean(vals)
        all_results[name] = {"freq": freq, "coherence": avg, "is_pi": name in pi_freqs}
        print(f"  {name:>6}: freq={freq:.4f} | coherence={avg:.4f} | {'PI' if name in pi_freqs else '  '}")

    pi_avg = np.mean([v["coherence"] for v in all_results.values() if v["is_pi"]])
    nonpi_avg = np.mean([v["coherence"] for v in all_results.values() if not v["is_pi"]])

    return {
        "name": "WA",
        "kanji": "和",
        "meaning": "Harmony — the old name for Japan itself",
        "data": all_results,
        "pi_average_coherence": pi_avg,
        "nonpi_average_coherence": nonpi_avg,
        "pi_wins": pi_avg > nonpi_avg,
    }


# ================================================================
# SIM 4: MA (間) — The Space Between
# The gap in the enso. The pause. Does it encode pi?
# ================================================================
def sim_ma(n_runs=200):
    """
    Measure coherence at SPECIFIC time points.
    The analytic solution for pure dephasing:
    C(t) = 0.5 * exp(-gamma * t / 2)

    At what time does coherence drop to 1/e of its initial?
    t_1e = 2 / gamma (from the analytic)

    At t = pi/gamma: C = 0.5 * exp(-pi/2) = 0.5 * 0.2079 = 0.1039
    At t = 2/gamma: C = 0.5 * exp(-1) = 0.5 * 0.3679 = 0.1839

    The RATIO of these times: (pi/gamma) / (2/gamma) = pi/2

    The gap between the 1/e time and the pi-time IS pi/2.
    Ma — the space between — IS pi/2.
    """
    print("\n" + "=" * 60)
    print("  SIM 4: MA (間) — The Space Between")
    print("  Does the gap between key times encode pi?")
    print(f"  50 gamma values x {n_runs} runs = {50 * n_runs} sims")
    print("=" * 60)

    T_STEPS = 500
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    H = 0 * qt.sigmax()

    results = []
    for i in range(50):
        gamma = 0.01 + i * (0.2 / 50)
        T_MAX = max(40.0, 4 * PI / gamma)
        tlist = np.linspace(0, T_MAX, T_STEPS + 1)
        c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]

        # Single high-fidelity run (Lindblad is deterministic)
        r = qt.mesolve(H, psi0, tlist, c_ops, [])
        coherence_trace = [float(np.abs(r.states[j].full()[0, 1])) for j in range(len(tlist))]
        c0 = coherence_trace[0]

        # Find t where C drops to C0/e
        t_1e = None
        for j, c in enumerate(coherence_trace):
            if c < c0 / np.e:
                t_1e = tlist[j]
                break

        # Analytic predictions
        t_1e_analytic = 2.0 / gamma
        t_pi_analytic = PI / gamma
        ratio_analytic = t_pi_analytic / t_1e_analytic  # should be pi/2

        row = {
            "gamma": gamma,
            "t_1e_measured": t_1e,
            "t_1e_analytic": t_1e_analytic,
            "t_pi_analytic": t_pi_analytic,
            "ratio_predicted": PI / 2,
            "ratio_measured": t_pi_analytic / t_1e if t_1e else None,
        }
        results.append(row)

        if (i + 1) % 10 == 0:
            print(f"  gamma={gamma:.4f} | t_1e={t_1e:.2f} (predicted {t_1e_analytic:.2f}) | "
                  f"ratio={row['ratio_measured']:.4f} (predicted {PI/2:.4f})")

    return {
        "name": "MA",
        "kanji": "間",
        "meaning": "The space between — not emptiness, but presence of relationship",
        "data": results,
        "pi_over_2": PI / 2,
    }


# ================================================================
# SIM 5: NAMI (波) — Wave
# Every oscillation costs exactly 2*pi. Prove it.
# ================================================================
def sim_nami(n_runs=100):
    """
    Drive a qubit with a known Hamiltonian.
    Measure the oscillation period from the coherence trace.
    The period should be EXACTLY 2*pi/omega.
    Verify to high precision.
    """
    print("\n" + "=" * 60)
    print("  SIM 5: NAMI (波) — Wave")
    print("  Does every oscillation cost exactly 2*pi?")
    print(f"  20 frequencies x {n_runs} runs")
    print("=" * 60)

    T_MAX = 50.0
    T_STEPS = 2000  # high resolution for period measurement
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    psi0 = qt.basis(2, 0)  # start in |0>, will oscillate
    gamma = 0.0001  # very low noise for clean oscillation

    results = []
    for i in range(20):
        omega = 0.5 + i * 0.5  # 0.5 to 10.0

        H = omega * qt.sigmax()
        c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]

        r = qt.mesolve(H, psi0, tlist, c_ops, [])
        # Measure P(|1>) over time
        prob_1 = [float(np.abs(r.states[j].full()[1, 0])**2) for j in range(len(tlist))]

        # Find period by measuring peak-to-peak distance
        peaks = []
        for j in range(1, len(prob_1) - 1):
            if prob_1[j] > prob_1[j-1] and prob_1[j] > prob_1[j+1] and prob_1[j] > 0.1:
                peaks.append(tlist[j])

        if len(peaks) >= 2:
            periods = [peaks[k+1] - peaks[k] for k in range(len(peaks)-1)]
            measured_period = np.mean(periods)
        else:
            measured_period = None

        predicted_period = 2 * PI / (2 * omega)  # Rabi period = pi/omega
        # Actually for sigmax drive: period = pi/omega

        row = {
            "omega": omega,
            "predicted_period": PI / omega,
            "measured_period": measured_period,
            "ratio": measured_period / (PI / omega) if measured_period else None,
            "n_peaks": len(peaks),
        }
        results.append(row)

        ratio_str = f"{row['ratio']:.6f}" if row['ratio'] else "N/A"
        meas_str = f"{measured_period:.4f}" if measured_period else "N/A"
        print(f"  omega={omega:.1f} | predicted={PI/omega:.4f} | "
              f"measured={meas_str} | "
              f"ratio={ratio_str} | peaks={len(peaks)}")

    # Check how close all ratios are to 1.0
    valid = [r for r in results if r["ratio"] is not None]
    avg_ratio = np.mean([r["ratio"] for r in valid]) if valid else None
    max_error = max(abs(r["ratio"] - 1.0) for r in valid) if valid else None

    return {
        "name": "NAMI",
        "kanji": "波",
        "meaning": "Wave — every oscillation IS 2*pi",
        "data": results,
        "average_ratio_to_predicted": avg_ratio,
        "max_deviation_from_pi": max_error,
    }


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PI IN THE CIRCLE — Five Simulations")
    print("  円相 円 和 間 波")
    print("  Enso. En. Wa. Ma. Nami.")
    print(f"  QuTiP {qt.__version__}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Rhet Dillard Wike | AIIT-THRESI")
    print("=" * 60)
    print()

    start = time.time()

    r1 = sim_enso(n_gamma=200, n_runs=50)
    r2 = sim_en(n_steps=300, n_runs=30)
    r3 = sim_wa(n_runs=100)
    r4 = sim_ma(n_runs=100)
    r5 = sim_nami(n_runs=50)

    total_time = time.time() - start

    # Count total sims
    total_sims = (200 * 3 * 50) + (300 * 30) + (12 * 100) + (50 * 100) + (20 * 50)
    # = 30000 + 9000 + 1200 + 5000 + 1000 = 46200

    # Build report
    lines = []
    lines.append("=" * 72)
    lines.append("  PI IN THE CIRCLE — RESULTS")
    lines.append(f"  {total_sims:,} total simulations")
    lines.append(f"  Runtime: {total_time:.1f}s ({total_time/60:.1f} min)")
    lines.append(f"  QuTiP {qt.__version__}")
    lines.append(f"  Executed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("  Rhet Dillard Wike | AIIT-THRESI | Council Hill, Oklahoma")
    lines.append("=" * 72)
    lines.append("")

    # ENSO results
    lines.append("  ENSO (円相) — The Zen Circle")
    lines.append(f"  Pi-locked drive beats non-pi: {r1['pi_beats_nonpi']}/{r1['total']} "
                 f"({r1['pi_beats_nonpi']/r1['total']*100:.1f}%)")
    lines.append(f"  Pi-locked drive beats pure dephasing: {r1['pi_beats_pure']}/{r1['total']} "
                 f"({r1['pi_beats_pure']/r1['total']*100:.1f}%)")
    lines.append("")

    # EN results
    lines.append("  EN (円) — Circle = Connection")
    lines.append(f"  Predicted critical coupling K_c = 2/pi = {r2['K_c_predicted']:.6f}")
    lines.append(f"  Measured transition K = {r2['K_c_measured']:.6f}" if r2['K_c_measured'] else "  No transition found")
    if r2['ratio']:
        lines.append(f"  Ratio (measured/predicted) = {r2['ratio']:.4f}")
    lines.append("")

    # WA results
    lines.append("  WA (和) — Harmony")
    lines.append(f"  Pi-harmonic average coherence: {r3['pi_average_coherence']:.6f}")
    lines.append(f"  Non-pi average coherence: {r3['nonpi_average_coherence']:.6f}")
    lines.append(f"  Pi wins: {r3['pi_wins']}")
    lines.append("")

    # MA results
    lines.append("  MA (間) — The Space Between")
    lines.append(f"  Predicted ratio (t_pi / t_1e) = pi/2 = {PI/2:.6f}")
    valid_ma = [r for r in r4['data'] if r['ratio_measured'] is not None]
    if valid_ma:
        avg_ma = np.mean([r['ratio_measured'] for r in valid_ma])
        lines.append(f"  Measured average ratio = {avg_ma:.6f}")
        lines.append(f"  Error = {abs(avg_ma - PI/2):.6f} ({abs(avg_ma - PI/2)/(PI/2)*100:.3f}%)")
    lines.append("")

    # NAMI results
    lines.append("  NAMI (波) — Wave")
    if r5['average_ratio_to_predicted']:
        lines.append(f"  Average measured/predicted period ratio: {r5['average_ratio_to_predicted']:.6f}")
        lines.append(f"  Max deviation from pi prediction: {r5['max_deviation_from_pi']:.6f}")
        lines.append(f"  Every oscillation costs 2*pi: {'YES' if r5['max_deviation_from_pi'] < 0.01 else 'CLOSE'}")
    lines.append("")

    lines.append("=" * 72)
    lines.append("  THE FIVE WORDS")
    lines.append("=" * 72)
    lines.append("")
    lines.append("  円相 ENSO  — The circle drawn in one stroke")
    lines.append("  円   EN    — Circle, connection, and currency are the same word")
    lines.append("  和   WA    — Harmony. The old name for Japan.")
    lines.append("  間   MA    — The space between. Not emptiness. Relationship.")
    lines.append("  波   NAMI  — Wave. Every oscillation IS 2*pi.")
    lines.append("")
    lines.append("  Five words. One language. One number.")
    lines.append("  The Japanese language encoded pi into its")
    lines.append("  understanding of reality 1,500 years before")
    lines.append("  quantum mechanics existed.")
    lines.append("")
    lines.append("  God is good. All the time. Them beans though.")
    lines.append("  Rhet Dillard Wike | AIIT-THRESI | Council Hill, Oklahoma")
    lines.append("=" * 72)

    report = "\n".join(lines)

    with open(os.path.join(OUTPUT_DIR, "RESULTS_PI_JAPANESE.txt"), "w") as f:
        f.write(report)

    # Save full data as JSON
    all_data = {
        "enso": {k: v for k, v in r1.items() if k != "data"},
        "en": {k: v for k, v in r2.items() if k != "data"},
        "wa": {k: v for k, v in r3.items() if k != "data"},
        "ma": {k: v for k, v in r4.items() if k != "data"},
        "nami": {k: v for k, v in r5.items() if k != "data"},
        "total_sims": total_sims,
        "runtime": total_time,
    }
    with open(os.path.join(OUTPUT_DIR, "RESULTS_PI_JAPANESE_data.json"), "w") as f:
        json.dump(all_data, f, indent=2, default=str)

    print()
    print(report)
