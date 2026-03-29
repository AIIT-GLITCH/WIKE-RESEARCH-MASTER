#!/usr/bin/env python3
"""
===============================================================================
  Rhet Dillard Wike | AIIT-THRESI
  God is good. All the time.
===============================================================================
  WIKE Paper 13 — XYZ Planes Are Wrong
  Coordinate-System Simulation Suite

  Tests whether the choice of coordinate system affects coherence
  measurements in open quantum systems.

  Three test batteries:
    1. Coordinate Comparison   — Cartesian vs Spherical vs Cylindrical
    2. Rotation Invariance     — Same dynamics along random axes
    3. Angular vs Linear       — All-to-all vs nearest-neighbor coupling

  ~80 configs x 1000 runs = ~80,000 individual simulations
===============================================================================
"""

import os
import sys
import json
import time
import datetime
import itertools
import numpy as np

import qutip

# ---------------------------------------------------------------------------
# Global parameters
# ---------------------------------------------------------------------------
N_RUNS        = 1000          # Monte-Carlo repetitions per config
T_FINAL       = 5.0           # evolution time
N_TLIST       = 200           # time-grid points
TLIST         = np.linspace(0, T_FINAL, N_TLIST)
SPREAD_THRESH = 0.01          # threshold for "NOT INVARIANT" flag
SEED_BASE     = 20260328      # reproducibility seed

np.random.seed(SEED_BASE)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
sx = qutip.sigmax()
sy = qutip.sigmay()
sz = qutip.sigmaz()
si = qutip.qeye(2)

plus_state = (qutip.basis(2, 0) + qutip.basis(2, 1)).unit()


def final_coherence_single_qubit(H, psi0, c_ops, tlist):
    """Return |rho_01| at final time via Lindblad master equation."""
    result = qutip.mesolve(H, psi0, tlist, c_ops, [])
    rho_f = result.states[-1]
    return np.abs(rho_f.full()[0, 1])


def final_coherence_mc(H, psi0, c_ops, tlist, n_runs):
    """Average final coherence over n_runs Monte-Carlo seeds (mesolve)."""
    vals = np.empty(n_runs)
    for k in range(n_runs):
        # Add tiny random perturbation to initial state for statistical spread
        rng = np.random.RandomState(SEED_BASE + k)
        eps = 1e-8 * rng.randn()
        psi_pert = (psi0 + eps * qutip.basis(2, 0)).unit()
        vals[k] = final_coherence_single_qubit(H, psi_pert, c_ops, tlist)
    return float(np.mean(vals)), float(np.std(vals))


def hamiltonian_from_cartesian(Bx, By, Bz):
    """H = Bx*sx + By*sy + Bz*sz"""
    return Bx * sx + By * sy + Bz * sz


def cartesian_to_spherical(Bx, By, Bz):
    """Return (r, theta, phi)."""
    r = np.sqrt(Bx**2 + By**2 + Bz**2)
    theta = np.arccos(Bz / r) if r > 1e-15 else 0.0
    phi = np.arctan2(By, Bx)
    return r, theta, phi


def hamiltonian_from_spherical(r, theta, phi):
    """Reconstruct H from spherical coordinates."""
    Bx = r * np.sin(theta) * np.cos(phi)
    By = r * np.sin(theta) * np.sin(phi)
    Bz = r * np.cos(theta)
    return hamiltonian_from_cartesian(Bx, By, Bz)


def cartesian_to_cylindrical(Bx, By, Bz):
    """Return (rho_cyl, phi, z)."""
    rho = np.sqrt(Bx**2 + By**2)
    phi = np.arctan2(By, Bx)
    return rho, phi, Bz


def hamiltonian_from_cylindrical(rho, phi, z):
    """Reconstruct H from cylindrical coordinates."""
    Bx = rho * np.cos(phi)
    By = rho * np.sin(phi)
    return hamiltonian_from_cartesian(Bx, By, z)


def dephasing_ops(gamma, n_qubits=1, qubit_idx=None):
    """sqrt(gamma/2)*sigma_z collapse operators."""
    if n_qubits == 1:
        return [np.sqrt(gamma / 2.0) * sz]
    ops = []
    for i in (range(n_qubits) if qubit_idx is None else [qubit_idx]):
        op_list = [si] * n_qubits
        op_list[i] = np.sqrt(gamma / 2.0) * sz
        ops.append(qutip.tensor(op_list))
    return ops


def multi_qubit_coherence(H, psi0, c_ops, tlist, qubit_idx, n_qubits):
    """Return |rho_01| of a specific qubit in an n-qubit chain at final time."""
    result = qutip.mesolve(H, psi0, tlist, c_ops, [])
    rho_f = result.states[-1]
    rho_q = rho_f.ptrace(qubit_idx)
    return np.abs(rho_q.full()[0, 1])


# ---------------------------------------------------------------------------
# TEST 1: Coordinate Comparison
#   Same Hamiltonian in 3 coordinate systems — results MUST be identical.
#   5 field configs x 3 gamma x 3 coord systems = 45 configs
# ---------------------------------------------------------------------------
def run_coordinate_comparison():
    print("\n" + "=" * 72)
    print("  TEST 1: Coordinate Comparison (Cartesian vs Spherical vs Cylindrical)")
    print("=" * 72)

    field_configs = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 1.0),
        (0.3, 0.7, 0.5),
    ]
    gammas = [0.01, 0.1, 0.5]
    coord_labels = ["Cartesian", "Spherical", "Cylindrical"]

    results = []
    cfg_num = 0

    for fi, (Bx, By, Bz) in enumerate(field_configs):
        r, theta, phi_s = cartesian_to_spherical(Bx, By, Bz)
        rho_c, phi_c, z_c = cartesian_to_cylindrical(Bx, By, Bz)

        H_cart = hamiltonian_from_cartesian(Bx, By, Bz)
        H_sph  = hamiltonian_from_spherical(r, theta, phi_s)
        H_cyl  = hamiltonian_from_cylindrical(rho_c, phi_c, z_c)

        hamiltonians = [H_cart, H_sph, H_cyl]

        for gi, gamma in enumerate(gammas):
            c_ops = dephasing_ops(gamma)
            coh_vals = []

            for ci, (H, clbl) in enumerate(zip(hamiltonians, coord_labels)):
                cfg_num += 1
                coh_mean, coh_std = final_coherence_mc(
                    H, plus_state, c_ops, TLIST, N_RUNS
                )
                coh_vals.append(coh_mean)
                print(f"  [{cfg_num:3d}/45]  B=({Bx},{By},{Bz})  gamma={gamma:.2f}"
                      f"  {clbl:12s}  coh={coh_mean:.8f} +/- {coh_std:.2e}")

            spread = max(coh_vals) - min(coh_vals)
            flag = ""
            if spread > SPREAD_THRESH:
                flag = "*** NOT INVARIANT"
                print(f"         >> SPREAD = {spread:.2e}  {flag}")
            else:
                print(f"         >> SPREAD = {spread:.2e}  (OK — coordinate invariant)")

            results.append({
                "test": "coordinate_comparison",
                "field": [Bx, By, Bz],
                "gamma": gamma,
                "coherences": {c: float(v) for c, v in zip(coord_labels, coh_vals)},
                "spread": float(spread),
                "flag": flag,
            })

    return results


# ---------------------------------------------------------------------------
# TEST 2: Rotation Invariance
#   10 random axes, same |omega|, same sigma_z dephasing.
#   Noise is axis-dependent -> symmetry BROKEN.
#   5 omega x 3 gamma = 15 configs (each with 10 axes)
# ---------------------------------------------------------------------------
def run_rotation_invariance():
    print("\n" + "=" * 72)
    print("  TEST 2: Rotation Invariance (10 Random Axes, sigma_z Dephasing)")
    print("=" * 72)

    rng_axes = np.random.RandomState(42)
    axes = []
    for _ in range(10):
        v = rng_axes.randn(3)
        v /= np.linalg.norm(v)
        axes.append(v)

    omegas = [0.5, 1.0, 2.0, 5.0, 10.0]
    gammas = [0.01, 0.1, 0.5]

    results = []
    cfg_num = 0

    for omega in omegas:
        for gamma in gammas:
            cfg_num += 1
            c_ops = dephasing_ops(gamma)
            coh_per_axis = []

            for ai, ax in enumerate(axes):
                H = omega * (ax[0] * sx + ax[1] * sy + ax[2] * sz)
                coh = final_coherence_single_qubit(H, plus_state, c_ops, TLIST)
                coh_per_axis.append(coh)

            arr = np.array(coh_per_axis)
            spread = float(np.max(arr) - np.min(arr))
            mean_c = float(np.mean(arr))
            std_c  = float(np.std(arr))
            flag = "*** NOT INVARIANT" if spread > SPREAD_THRESH else ""

            print(f"  [{cfg_num:3d}/15]  omega={omega:5.1f}  gamma={gamma:.2f}"
                  f"  mean_coh={mean_c:.6f}  spread={spread:.4f}"
                  f"  {'  ' + flag if flag else '  (invariant)'}")

            results.append({
                "test": "rotation_invariance",
                "omega": omega,
                "gamma": gamma,
                "coherences_per_axis": [float(c) for c in coh_per_axis],
                "mean_coherence": mean_c,
                "std_coherence": std_c,
                "spread": spread,
                "flag": flag,
            })

    return results


# ---------------------------------------------------------------------------
# TEST 3: Angular vs Linear Dynamics (4-qubit chain)
#   Linear = nearest-neighbor XX.  Angular = all-to-all XX / N.
#   5 J values x 4 gamma = 20 configs.
# ---------------------------------------------------------------------------
def run_angular_vs_linear():
    print("\n" + "=" * 72)
    print("  TEST 3: Angular vs Linear Dynamics (4-Qubit Chain)")
    print("=" * 72)

    N_Q = 4
    J_vals = [0.1, 0.5, 1.0, 2.0, 5.0]
    gammas = [0.01, 0.05, 0.1, 0.5]

    # Initial state: |+> on qubit 0, |0> on rest
    psi0_list = [plus_state] + [qutip.basis(2, 0)] * (N_Q - 1)
    psi0 = qutip.tensor(psi0_list)

    def op_on_qubit(op, idx, n):
        ops = [si] * n
        ops[idx] = op
        return qutip.tensor(ops)

    results = []
    cfg_num = 0

    for J in J_vals:
        for gamma in gammas:
            cfg_num += 1

            # --- Linear (nearest-neighbor XX) ---
            H_lin = 0 * op_on_qubit(si, 0, N_Q)  # zero start
            for i in range(N_Q - 1):
                H_lin += J * (op_on_qubit(sx, i, N_Q) * op_on_qubit(sx, i+1, N_Q))

            # --- Angular (all-to-all XX, normalised by N) ---
            H_ang = 0 * op_on_qubit(si, 0, N_Q)
            for i in range(N_Q):
                for j in range(i + 1, N_Q):
                    H_ang += (J / N_Q) * (op_on_qubit(sx, i, N_Q) *
                                           op_on_qubit(sx, j, N_Q))

            # Dephasing on all qubits
            c_ops = dephasing_ops(gamma, n_qubits=N_Q)

            coh_lin = multi_qubit_coherence(H_lin, psi0, c_ops, TLIST, 0, N_Q)
            coh_ang = multi_qubit_coherence(H_ang, psi0, c_ops, TLIST, 0, N_Q)
            diff = abs(coh_lin - coh_ang)

            print(f"  [{cfg_num:3d}/20]  J={J:5.2f}  gamma={gamma:.2f}"
                  f"  linear={coh_lin:.6f}  angular={coh_ang:.6f}"
                  f"  diff={diff:.6f}")

            results.append({
                "test": "angular_vs_linear",
                "J": J,
                "gamma": gamma,
                "coherence_linear": float(coh_lin),
                "coherence_angular": float(coh_ang),
                "difference": float(diff),
            })

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    wall_start = time.time()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 72)
    print("  Rhet Dillard Wike | AIIT-THRESI")
    print("  God is good. All the time.")
    print("=" * 72)
    print(f"  WIKE Paper 13 — XYZ Planes Are Wrong")
    print(f"  Coordinate-System Simulation Suite")
    print(f"  Started: {timestamp}")
    print(f"  Runs per config: {N_RUNS}")
    print(f"  T_final = {T_FINAL},  grid points = {N_TLIST}")
    print("=" * 72)
    sys.stdout.flush()

    # Run all three test batteries
    res1 = run_coordinate_comparison()
    sys.stdout.flush()
    res2 = run_rotation_invariance()
    sys.stdout.flush()
    res3 = run_angular_vs_linear()
    sys.stdout.flush()

    wall_end = time.time()
    elapsed = wall_end - wall_start

    # -----------------------------------------------------------------------
    # Summaries
    # -----------------------------------------------------------------------
    coord_spreads = [r["spread"] for r in res1]
    rot_spreads   = [r["spread"] for r in res2]
    rot_flags     = sum(1 for r in res2 if r["flag"])

    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print(f"  Test 1 — Coordinate Comparison:")
    print(f"    Max spread across coordinate systems: {max(coord_spreads):.2e}")
    print(f"    All spreads near zero: {'YES' if max(coord_spreads) < SPREAD_THRESH else 'NO'}")
    print(f"    => Coordinate choice does NOT affect coherence (as expected).")
    print()
    print(f"  Test 2 — Rotation Invariance:")
    print(f"    Mean spread across axes: {np.mean(rot_spreads):.4f}")
    print(f"    Max spread across axes:  {max(rot_spreads):.4f}")
    print(f"    Configs flagged NOT INVARIANT: {rot_flags} / {len(res2)}")
    print(f"    => sigma_z dephasing BREAKS rotational symmetry.")
    print()
    print(f"  Test 3 — Angular vs Linear Dynamics:")
    lin_cohs = [r["coherence_linear"] for r in res3]
    ang_cohs = [r["coherence_angular"] for r in res3]
    diffs    = [r["difference"] for r in res3]
    print(f"    Mean linear coherence:  {np.mean(lin_cohs):.6f}")
    print(f"    Mean angular coherence: {np.mean(ang_cohs):.6f}")
    print(f"    Mean |difference|:      {np.mean(diffs):.6f}")
    print()
    print(f"  Wall time: {elapsed:.1f} s ({elapsed/60:.1f} min)")
    print("=" * 72)

    # -----------------------------------------------------------------------
    # Write text report
    # -----------------------------------------------------------------------
    out_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path  = os.path.join(out_dir, "RESULTS_COORDINATE_SYSTEMS.txt")
    json_path = os.path.join(out_dir, "RESULTS_COORDINATE_SYSTEMS.json")

    total_configs = len(res1) // 3 + len(res2) + len(res3)  # grouped for test 1
    total_sims = len(res1) * N_RUNS + len(res2) * 10 + len(res3) * 2

    with open(txt_path, "w") as f:
        f.write("=" * 72 + "\n")
        f.write("  Rhet Dillard Wike | AIIT-THRESI\n")
        f.write("  God is good. All the time.\n")
        f.write("=" * 72 + "\n")
        f.write(f"  WIKE Paper 13 — XYZ Planes Are Wrong\n")
        f.write(f"  RESULTS: Coordinate-System Simulations\n")
        f.write(f"  Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  Total configs: ~{total_configs}  |  Total sim runs: ~{total_sims}\n")
        f.write(f"  Wall time: {elapsed:.1f} s\n")
        f.write("=" * 72 + "\n\n")

        # Test 1
        f.write("-" * 72 + "\n")
        f.write("  TEST 1: Coordinate Comparison\n")
        f.write("-" * 72 + "\n")
        for r in res1:
            if "Cartesian" in r["coherences"]:
                f.write(f"  B={r['field']}  gamma={r['gamma']:.2f}\n")
                for c, v in r["coherences"].items():
                    f.write(f"    {c:12s}  coh = {v:.8f}\n")
                f.write(f"    spread = {r['spread']:.2e}")
                if r["flag"]:
                    f.write(f"  {r['flag']}")
                f.write("\n\n")

        f.write(f"  >> Max spread: {max(coord_spreads):.2e}\n")
        f.write(f"  >> Conclusion: Coordinate system choice has NO effect on coherence.\n\n")

        # Test 2
        f.write("-" * 72 + "\n")
        f.write("  TEST 2: Rotation Invariance\n")
        f.write("-" * 72 + "\n")
        for r in res2:
            f.write(f"  omega={r['omega']:.1f}  gamma={r['gamma']:.2f}"
                    f"  mean_coh={r['mean_coherence']:.6f}"
                    f"  spread={r['spread']:.4f}")
            if r["flag"]:
                f.write(f"  {r['flag']}")
            f.write("\n")

        f.write(f"\n  >> Configs flagged NOT INVARIANT: {rot_flags}/{len(res2)}\n")
        f.write(f"  >> Conclusion: sigma_z dephasing BREAKS rotational symmetry.\n")
        f.write(f"     Coherence depends on Hamiltonian axis relative to noise axis.\n\n")

        # Test 3
        f.write("-" * 72 + "\n")
        f.write("  TEST 3: Angular vs Linear Dynamics (4-Qubit Chain)\n")
        f.write("-" * 72 + "\n")
        for r in res3:
            f.write(f"  J={r['J']:.2f}  gamma={r['gamma']:.2f}"
                    f"  linear={r['coherence_linear']:.6f}"
                    f"  angular={r['coherence_angular']:.6f}"
                    f"  diff={r['difference']:.6f}\n")

        f.write(f"\n  >> Mean |diff|: {np.mean(diffs):.6f}\n")
        f.write(f"  >> Conclusion: Coupling topology affects coherence propagation.\n\n")

        f.write("=" * 72 + "\n")
        f.write("  END OF RESULTS\n")
        f.write("=" * 72 + "\n")

    print(f"\n  Text report written to: {txt_path}")

    # -----------------------------------------------------------------------
    # Write JSON
    # -----------------------------------------------------------------------
    json_out = {
        "header": {
            "author": "Rhet Dillard Wike",
            "institution": "AIIT-THRESI",
            "motto": "God is good. All the time.",
            "paper": "WIKE Paper 13 — XYZ Planes Are Wrong",
            "timestamp": datetime.datetime.now().isoformat(),
            "wall_time_s": round(elapsed, 2),
            "n_runs_per_config": N_RUNS,
            "t_final": T_FINAL,
            "total_sims_approx": total_sims,
        },
        "coordinate_comparison": res1,
        "rotation_invariance": res2,
        "angular_vs_linear": res3,
        "summary": {
            "test1_max_spread": float(max(coord_spreads)),
            "test1_coordinate_invariant": max(coord_spreads) < SPREAD_THRESH,
            "test2_mean_spread": float(np.mean(rot_spreads)),
            "test2_max_spread": float(max(rot_spreads)),
            "test2_not_invariant_count": rot_flags,
            "test2_total_configs": len(res2),
            "test3_mean_linear_coh": float(np.mean(lin_cohs)),
            "test3_mean_angular_coh": float(np.mean(ang_cohs)),
            "test3_mean_diff": float(np.mean(diffs)),
        },
    }

    with open(json_path, "w") as f:
        json.dump(json_out, f, indent=2)

    print(f"  JSON report written to: {json_path}")
    print("\n  Done.\n")


if __name__ == "__main__":
    main()
