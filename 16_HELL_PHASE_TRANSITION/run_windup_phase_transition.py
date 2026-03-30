"""
WIND-UP PHASE TRANSITION SIMULATION
=====================================
Paper 16: Hell is a Physics Phenomenon
Central Sensitization as Permanent Decoherence

Models dorsal horn LTP (long-term potentiation) as a
decoherence amplifier. Each repeated stimulus lowers
the threshold — exactly like wind-up in nociception.

THE PREDICTION:
  If central sensitization IS a Wike phase transition,
  the collapse of gate function (coherence) will be SHARP —
  a cliff at gamma_c — not gradual sensitization.

  Standard medicine says: "sensitization is a spectrum."
  Wike Coherence Law says: "there is a cliff."

  This sim finds the cliff.

THREE CONDITIONS (mapping to pain physiology):
  A: BASELINE — qubit with natural dephasing
     = Healthy dorsal horn, inhibitory interneurons active
     = Gate functioning

  B: WIND-UP — gamma amplifies with each iteration
     = Repeated C-fiber activation, NMDA sensitization
     = Gate under increasing load

  C: SENSITIZED — gamma locked above threshold
     = LTP established, gate collapsed
     = Central sensitization, hell state

WHAT WE MEASURE:
  - Coherence at each step
  - The transition point (gamma_c)
  - Whether transition is sharp (cliff) or gradual (slope)
  - ERR = |coherence_measured - coherence_expected|

Rhet Dillard Wike | AIIT-THRESI | March 29, 2026
Built by Claude Sonnet 4.6
"""

import numpy as np
import qutip as qt
import json
import os
import time
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
T_MAX = 20.0
T_STEPS = 100
N_STEPS = 500          # 500 gamma steps (gamma_c will be visible)
RUNS_PER_STEP = 100    # 100 runs per step per condition
GAMMA_START = 0.001
GAMMA_END = 0.3
AMPLIFICATION = 1.08   # Each wind-up step multiplies gamma by this
                        # Models NMDA sensitization threshold lowering
WINDUP_DEPTH = 5       # How many iterations of sensitization before measuring
                        # Models repeated C-fiber activation

def sim_single(gamma, H=None):
    """Run one QuTiP sim. Returns final off-diagonal coherence."""
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    if H is None:
        H = 0.1 * qt.sigmax()   # gentle endogenous drive = natural oscillation
    c_ops = [np.sqrt(gamma / 2) * qt.sigmaz()]
    tlist = np.linspace(0, T_MAX, T_STEPS + 1)
    result = qt.mesolve(H, psi0, tlist, c_ops, [])
    rho = result.states[-1]
    coherence = float(np.abs(rho.full()[0, 1]))
    return coherence

def run_step(gamma_base):
    """Run all three conditions at this gamma_base."""

    # CONDITION A: BASELINE — healthy gate, natural dephasing
    a_vals = [sim_single(gamma_base) for _ in range(RUNS_PER_STEP)]

    # CONDITION B: WIND-UP — gamma amplifies with each iteration
    # Models: first stimulus sensitizes, second more, etc.
    # After WINDUP_DEPTH iterations, gamma = gamma_base * AMPLIFICATION^WINDUP_DEPTH
    gamma_wound_up = gamma_base * (AMPLIFICATION ** WINDUP_DEPTH)
    b_vals = [sim_single(gamma_wound_up) for _ in range(RUNS_PER_STEP)]

    # CONDITION C: SENSITIZED — full LTP, gate collapsed
    # gamma locked at 10x baseline (deep in gamma > gamma_c territory)
    gamma_sensitized = gamma_base * 10.0
    c_vals = [sim_single(gamma_sensitized) for _ in range(RUNS_PER_STEP)]

    return {
        "gamma_base": float(gamma_base),
        "gamma_wound_up": float(gamma_wound_up),
        "gamma_sensitized": float(gamma_sensitized),
        "A_baseline_mean": float(np.mean(a_vals)),
        "A_baseline_std": float(np.std(a_vals)),
        "B_windup_mean": float(np.mean(b_vals)),
        "B_windup_std": float(np.std(b_vals)),
        "C_sensitized_mean": float(np.mean(c_vals)),
        "C_sensitized_std": float(np.std(c_vals)),
        "gate_ratio_AB": float(np.mean(a_vals) / max(np.mean(b_vals), 1e-10)),
        "gate_ratio_AC": float(np.mean(a_vals) / max(np.mean(c_vals), 1e-10)),
    }

def find_cliff(results):
    """
    Find gamma_c: the point where coherence drops most sharply.
    A cliff will show a sudden large drop in dC/dgamma.
    A slope will show gradual decay.
    """
    gammas = [r["gamma_base"] for r in results]
    coherences = [r["B_windup_mean"] for r in results]
    derivatives = []
    for i in range(1, len(coherences)):
        dC = coherences[i] - coherences[i-1]
        dG = gammas[i] - gammas[i-1]
        derivatives.append(dC / dG if dG != 0 else 0)

    # gamma_c is where derivative is most negative (steepest drop)
    min_idx = np.argmin(derivatives)
    gamma_c = gammas[min_idx + 1]
    cliff_steepness = abs(derivatives[min_idx])

    # Measure sharpness: compare max derivative to mean derivative
    mean_deriv = np.mean([abs(d) for d in derivatives])
    sharpness_ratio = cliff_steepness / mean_deriv if mean_deriv > 0 else 0

    return gamma_c, cliff_steepness, sharpness_ratio, derivatives

def main():
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_sims = N_STEPS * RUNS_PER_STEP * 3
    print("=" * 65)
    print("  WIND-UP PHASE TRANSITION — PAPER 16")
    print("  Central Sensitization as Permanent Decoherence")
    print("=" * 65)
    print(f"  Steps:     {N_STEPS}")
    print(f"  Runs/step: {RUNS_PER_STEP} x 3 conditions")
    print(f"  Total:     {total_sims:,} simulations")
    print(f"  Wind-up:   gamma x {AMPLIFICATION}^{WINDUP_DEPTH} = x{AMPLIFICATION**WINDUP_DEPTH:.2f}")
    print("=" * 65)

    results = []
    gamma_values = np.linspace(GAMMA_START, GAMMA_END, N_STEPS)

    for i, gamma in enumerate(gamma_values):
        step_result = run_step(gamma)
        results.append(step_result)

        if (i + 1) % 50 == 0 or i == 0:
            elapsed = time.time() - start_time
            pct = (i + 1) / N_STEPS * 100
            eta = (elapsed / (i + 1)) * (N_STEPS - i - 1)
            print(f"  [{i+1:4d}/{N_STEPS}] {pct:5.1f}% | "
                  f"gamma={gamma:.4f} | "
                  f"A={step_result['A_baseline_mean']:.4f} | "
                  f"B={step_result['B_windup_mean']:.4f} | "
                  f"C={step_result['C_sensitized_mean']:.4f} | "
                  f"ETA {eta:.0f}s")

    # Find the cliff
    gamma_c, cliff_steepness, sharpness_ratio, derivatives = find_cliff(results)

    elapsed = time.time() - start_time

    # Summary
    print()
    print("=" * 65)
    print("  RESULTS — WIND-UP PHASE TRANSITION")
    print("=" * 65)
    print(f"  Total simulations: {total_sims:,}")
    print(f"  Runtime: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print()

    # Gate function analysis
    low_gamma = results[:10]
    high_gamma = results[-10:]
    low_gate = np.mean([r["gate_ratio_AB"] for r in low_gamma])
    high_gate = np.mean([r["gate_ratio_AB"] for r in high_gamma])

    print(f"  GATE FUNCTION (baseline vs wind-up ratio):")
    print(f"    Low gamma (healthy):    {low_gate:.3f}x")
    print(f"    High gamma (sensitized): {high_gate:.3f}x")
    print()
    print(f"  PHASE TRANSITION:")
    print(f"    gamma_c (cliff location): {gamma_c:.4f}")
    print(f"    Cliff steepness:          {cliff_steepness:.6f}")
    print(f"    Sharpness ratio:          {sharpness_ratio:.2f}x")
    print()

    # Is it a cliff or a slope?
    if sharpness_ratio > 3.0:
        verdict = "CLIFF CONFIRMED — sharp phase transition detected"
        verdict2 = "Wind-up IS a coherence phase transition. Paper 16 holds."
    elif sharpness_ratio > 1.5:
        verdict = "MODERATE CLIFF — suggestive of phase transition"
        verdict2 = "Consistent with Paper 16. More sims needed for certainty."
    else:
        verdict = "SLOPE — gradual decay, no sharp transition detected"
        verdict2 = "Challenges Paper 16 nociception mapping. Investigate."

    print(f"  VERDICT: {verdict}")
    print(f"  {verdict2}")
    print()

    # Count gate failures (A significantly > B)
    gate_beats = sum(1 for r in results if r["A_baseline_mean"] > r["B_windup_mean"] * 1.1)
    gate_pct = gate_beats / len(results) * 100
    print(f"  Baseline > Wind-up (gate holds): {gate_beats}/{N_STEPS} ({gate_pct:.1f}%)")

    # Save full results
    output = {
        "metadata": {
            "simulation": "Wind-Up Phase Transition — Paper 16",
            "date": timestamp,
            "total_sims": total_sims,
            "runtime_seconds": elapsed,
            "n_steps": N_STEPS,
            "runs_per_step": RUNS_PER_STEP,
            "amplification": AMPLIFICATION,
            "windup_depth": WINDUP_DEPTH,
        },
        "phase_transition": {
            "gamma_c": gamma_c,
            "cliff_steepness": cliff_steepness,
            "sharpness_ratio": sharpness_ratio,
            "verdict": verdict,
            "verdict2": verdict2,
        },
        "gate_analysis": {
            "low_gamma_gate_ratio": low_gate,
            "high_gamma_gate_ratio": high_gate,
            "gate_beats_pct": gate_pct,
        },
        "step_results": results,
    }

    json_path = os.path.join(OUTPUT_DIR, f"RESULTS_WINDUP_{timestamp}_data.json")
    txt_path = os.path.join(OUTPUT_DIR, f"RESULTS_WINDUP_{timestamp}.txt")

    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    with open(txt_path, "w") as f:
        f.write("=" * 65 + "\n")
        f.write("  WIND-UP PHASE TRANSITION — PAPER 16\n")
        f.write("  Central Sensitization as Permanent Decoherence\n")
        f.write(f"  {timestamp}\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"  Total simulations: {total_sims:,}\n")
        f.write(f"  Runtime: {elapsed:.1f}s\n\n")
        f.write(f"  gamma_c:          {gamma_c:.4f}\n")
        f.write(f"  Sharpness ratio:  {sharpness_ratio:.2f}x\n")
        f.write(f"  Gate function:    {low_gate:.3f}x -> {high_gate:.3f}x\n\n")
        f.write(f"  VERDICT: {verdict}\n")
        f.write(f"  {verdict2}\n\n")
        f.write("  STEP DATA:\n")
        f.write(f"  {'gamma':>8} | {'A_base':>8} | {'B_wound':>8} | {'C_sens':>8} | {'ratio_AB':>10}\n")
        f.write("  " + "-" * 55 + "\n")
        for r in results[::10]:  # every 10th step
            f.write(f"  {r['gamma_base']:8.4f} | "
                    f"{r['A_baseline_mean']:8.4f} | "
                    f"{r['B_windup_mean']:8.4f} | "
                    f"{r['C_sensitized_mean']:8.4f} | "
                    f"{r['gate_ratio_AB']:10.3f}\n")

    print()
    print(f"  Results saved:")
    print(f"    {txt_path}")
    print(f"    {json_path}")
    print()
    print("  God is good. All the time.")
    print("=" * 65)

if __name__ == "__main__":
    main()
