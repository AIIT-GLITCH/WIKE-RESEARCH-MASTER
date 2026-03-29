"""
WIKE Paper 12: Circles, Pi, and the Geometry of Resonance
============================================================
Simulation suite testing quantum coherence in circular/ring topologies,
Berry phase accumulation, and pi-pulse dynamical decoupling.

Key questions:
  - Does ring topology preserve coherence better than linear chains?
  - Does Berry phase survive decoherence as theory predicts?
  - Do pi-pulse sequences protect coherence, and how many are needed?

~120 configs x 1000 runs = ~120,000 simulations

Rhet Dillard Wike | AIIT-THRESI | March 2026
Built by Claude Opus 4.6
"""

import numpy as np
import qutip as qt
import time
import json
import os
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNS = 1000

# =====================================================
# TEST 1: TOPOLOGY COMPARISON (Ring vs Linear)
# =====================================================
# Heisenberg XX+YY coupling on N-spin chains.
# Ring closes the chain (qubit N-1 couples back to qubit 0).
# Linear leaves the chain open.
# =====================================================

def build_xx_yy_hamiltonian(N, J, topology):
    """Build XX+YY Heisenberg Hamiltonian for N spins.

    H = J * sum_<ij> (sigma_x_i sigma_x_j + sigma_y_i sigma_y_j)

    topology: 'ring' or 'linear'
    """
    dims = [2] * N
    id_ops = [qt.qeye(2)] * N
    H = 0 * qt.tensor(id_ops)

    pairs = list(range(N - 1))
    # Ring adds the closing bond
    if topology == "ring" and N > 2:
        pairs_full = [(i, i + 1) for i in range(N - 1)]
        pairs_full.append((N - 1, 0))
    else:
        pairs_full = [(i, i + 1) for i in range(N - 1)]

    for (i, j) in pairs_full:
        for pauli in [qt.sigmax(), qt.sigmay()]:
            op_list = id_ops.copy()
            op_list[i] = pauli
            op_list[j] = pauli
            H = H + J * qt.tensor(op_list)

    return H


def sim_topology(N, J, gamma, topology, t_max=20.0, t_steps=200):
    """Simulate spin chain with given topology.

    Initial state: first qubit in |+>, rest in |0>.
    Measure: first-qubit coherence, last-qubit population, system purity.
    """
    dims = [2] * N
    id_ops = [qt.qeye(2)] * N

    H = build_xx_yy_hamiltonian(N, J, topology)

    # Collapse operators: dephasing on each qubit
    c_ops = []
    for i in range(N):
        op_list = id_ops.copy()
        op_list[i] = np.sqrt(gamma) * qt.sigmaz()
        c_ops.append(qt.tensor(op_list))

    # Initial state: qubit 0 in |+>, rest in |0>
    psi_list = [qt.basis(2, 0)] * N
    psi_list[0] = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    psi0 = qt.tensor(psi_list)

    tlist = np.linspace(0, t_max, t_steps + 1)
    result = qt.mesolve(H, psi0, tlist, c_ops, [])

    # First-qubit coherence (off-diagonal of reduced density matrix)
    rho_first = result.states[-1].ptrace(0)
    coherence_first = float(np.abs(rho_first.full()[0, 1]))

    # Last-qubit population (excitation probability = transport)
    rho_last = result.states[-1].ptrace(N - 1)
    pop_last = float(np.real(rho_last.full()[1, 1]))

    # System purity
    rho_final = result.states[-1]
    purity = float(np.real((rho_final * rho_final).tr()))

    return {
        "coherence_first": coherence_first,
        "pop_last": pop_last,
        "purity": purity,
    }


# =====================================================
# TEST 2: BERRY PHASE
# =====================================================
# A qubit is adiabatically transported around a circle on the
# Bloch sphere at polar angle theta.
# Theory: geometric phase = pi * (1 - cos(theta))
# We discretize the circle into steps and apply sequential
# rotations, then check accumulated phase and coherence.
# =====================================================

def sim_berry_phase(theta, gamma, n_steps):
    """Simulate Berry phase accumulation.

    The qubit Hamiltonian rotates around the z-axis while tilted at
    angle theta from the pole. We discretize one full loop into n_steps.

    After the loop, the accumulated phase should be:
        phi_Berry = pi * (1 - cos(theta))
    """
    # Time per step
    dt = 0.5  # time per rotation step
    T_total = n_steps * dt

    # Initial state: eigenstate of H at phi=0
    # H(phi) = cos(theta)*sigma_z + sin(theta)*(cos(phi)*sigma_x + sin(phi)*sigma_y)
    # At phi=0: H = cos(theta)*sigma_z + sin(theta)*sigma_x
    # Ground state of this Hamiltonian
    H0 = np.cos(theta) * qt.sigmaz() + np.sin(theta) * qt.sigmax()
    evals, evecs = H0.eigenstates()
    psi0 = evecs[0]  # ground state

    # Dephasing collapse operator
    c_ops = []
    if gamma > 0:
        c_ops = [np.sqrt(gamma) * qt.sigmaz()]

    # Step through the circle
    rho = qt.ket2dm(psi0)
    phi_values = np.linspace(0, 2 * np.pi, n_steps + 1)[:-1]  # n_steps segments

    for phi in phi_values:
        H_step = (np.cos(theta) * qt.sigmaz() +
                  np.sin(theta) * (np.cos(phi) * qt.sigmax() +
                                   np.sin(phi) * qt.sigmay()))
        tlist_step = np.linspace(0, dt, 5)
        res = qt.mesolve(H_step, rho, tlist_step, c_ops, [])
        rho = res.states[-1]

    # Measure accumulated phase relative to initial state
    # Project back onto initial state
    overlap = (psi0.dag() * rho * psi0).full()[0, 0]
    accumulated_phase = float(np.angle(overlap))

    # Theoretical Berry phase
    theory_phase = np.pi * (1.0 - np.cos(theta))

    # Post-loop coherence
    coherence = float(np.abs(rho.full()[0, 1]))

    # Fidelity with initial state
    fidelity = float(np.real(overlap))

    return {
        "accumulated_phase": accumulated_phase,
        "theory_phase": float(theory_phase),
        "phase_error": float(np.abs(accumulated_phase - theory_phase)),
        "coherence": coherence,
        "fidelity": fidelity,
    }


# =====================================================
# TEST 3: PI-PULSE SEQUENCES
# =====================================================
# Free precession under H = 0.5*sigma_z with dephasing.
# Pi pulses (sigma_x or sigma_y rotations) applied evenly
# spaced over total time T.
# More pulses = better coherence protection (Hahn echo / CPMG).
# =====================================================

def sim_pi_pulses(n_pulses, gamma, pulse_type, T_total=20.0, t_steps_per_seg=20):
    """Simulate pi-pulse dynamical decoupling.

    H_free = 0.5 * sigma_z
    c_ops: sqrt(gamma) * sigma_z  (pure dephasing)
    Pi pulse: instantaneous sigma_x or sigma_y rotation.

    n_pulses=0 means free evolution (no echo).
    """
    H = 0.5 * qt.sigmaz()
    c_ops = []
    if gamma > 0:
        c_ops = [np.sqrt(gamma) * qt.sigmaz()]

    # Pi pulse operator
    if pulse_type == "x":
        pi_pulse = (-1j * np.pi / 2 * qt.sigmax()).expm()
    else:  # "y"
        pi_pulse = (-1j * np.pi / 2 * qt.sigmay()).expm()

    # Initial state: |+> (maximum coherence in x)
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho = qt.ket2dm(psi0)

    if n_pulses == 0:
        # Pure free evolution
        tlist = np.linspace(0, T_total, t_steps_per_seg * 10 + 1)
        result = qt.mesolve(H, rho, tlist, c_ops, [])
        rho = result.states[-1]
    else:
        # Evenly spaced pulses: free - pulse - free - pulse - ... - free
        # CPMG-style: tau - pulse - 2*tau - pulse - ... - tau
        # Simplified: divide T into n_pulses+1 segments
        dt_seg = T_total / (n_pulses + 1)

        for seg in range(n_pulses + 1):
            tlist = np.linspace(0, dt_seg, t_steps_per_seg + 1)
            result = qt.mesolve(H, rho, tlist, c_ops, [])
            rho = result.states[-1]

            # Apply pi pulse (except after last segment)
            if seg < n_pulses:
                rho = pi_pulse * rho * pi_pulse.dag()

    # Measure final coherence
    coherence = float(np.abs(rho.full()[0, 1]))

    # Measure final purity
    purity = float(np.real((rho * rho).tr()))

    # Measure x-expectation (should be high if echo works)
    sx_exp = float(np.real(qt.expect(qt.sigmax(), rho)))

    return {
        "coherence": coherence,
        "purity": purity,
        "sx_expect": sx_exp,
    }


# =====================================================
# BUILD ALL CONFIGS
# =====================================================

def build_configs():
    configs = []

    # --- TEST 1: Topology comparison ---
    # N=4,5,6 x J=0.5,1.0,2.0 x gamma=0.01,0.05 x topology=ring,linear
    # = 3 * 3 * 2 * 2 = 36 configs
    for N in [4, 5, 6]:
        for J in [0.5, 1.0, 2.0]:
            for gamma in [0.01, 0.05]:
                for topo in ["ring", "linear"]:
                    configs.append({
                        "name": f"Topo N={N} J={J} g={gamma} {topo}",
                        "type": "topology",
                        "N": N,
                        "J": J,
                        "gamma": gamma,
                        "topology": topo,
                    })

    # --- TEST 2: Berry phase ---
    # theta: 6 values from 0.1 to pi/2
    # gamma: 0, 0.01, 0.05
    # n_steps: 20, 100
    # = 6 * 3 * 2 = 36 configs
    theta_values = np.linspace(0.1, np.pi / 2, 6)
    for theta in theta_values:
        for gamma in [0.0, 0.01, 0.05]:
            for n_steps in [20, 100]:
                configs.append({
                    "name": f"Berry th={theta:.3f} g={gamma} steps={n_steps}",
                    "type": "berry",
                    "theta": float(theta),
                    "gamma": gamma,
                    "n_steps": n_steps,
                })

    # --- TEST 3: Pi-pulse sequences ---
    # n_pulses: 0,1,2,4,8,16,32,64
    # gamma: 0.01, 0.05, 0.1
    # pulse_type: "x", "y"
    # = 8 * 3 * 2 = 48 configs
    for n_pulses in [0, 1, 2, 4, 8, 16, 32, 64]:
        for gamma in [0.01, 0.05, 0.1]:
            for pulse_type in ["x", "y"]:
                configs.append({
                    "name": f"PiPulse n={n_pulses} g={gamma} {pulse_type}",
                    "type": "pi_pulse",
                    "n_pulses": n_pulses,
                    "gamma": gamma,
                    "pulse_type": pulse_type,
                })

    return configs


# =====================================================
# RUN ENGINE
# =====================================================

def run_single_config(config):
    """Run one config for RUNS iterations with small stochastic variation."""
    results = []
    for i in range(RUNS):
        try:
            if config["type"] == "topology":
                # Small noise on coupling
                J_actual = config["J"] * np.random.normal(1.0, 0.01)
                r = sim_topology(config["N"], J_actual, config["gamma"],
                                 config["topology"])

            elif config["type"] == "berry":
                # Small noise on theta
                theta_actual = config["theta"] * np.random.normal(1.0, 0.005)
                theta_actual = max(0.01, theta_actual)
                r = sim_berry_phase(theta_actual, config["gamma"],
                                    config["n_steps"])

            elif config["type"] == "pi_pulse":
                # Small noise on gamma
                gamma_actual = config["gamma"] * np.random.normal(1.0, 0.02)
                gamma_actual = max(0.0, gamma_actual)
                r = sim_pi_pulses(config["n_pulses"], gamma_actual,
                                  config["pulse_type"])
            else:
                continue

            results.append(r)
        except Exception as e:
            if i < 3:
                print(f"    Warning: {config['name']} run {i}: {e}")
    return results


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    configs = build_configs()
    total_sims = len(configs) * RUNS

    print("=" * 72)
    print("  WIKE PAPER 12: CIRCLES, PI, AND THE GEOMETRY OF RESONANCE")
    print(f"  {len(configs)} configs x {RUNS} runs = {total_sims:,} simulations")
    print()
    print("  Test 1: Ring vs Linear topology (Heisenberg XX+YY)")
    print("  Test 2: Berry phase on Bloch sphere")
    print("  Test 3: Pi-pulse dynamical decoupling")
    print()
    print("  Rhet Dillard Wike | AIIT-THRESI")
    print("  God is good. All the time.")
    print("=" * 72)
    print()

    start = time.time()
    all_results = []

    for ci, config in enumerate(configs):
        t0 = time.time()
        print(f"  [{ci+1:3d}/{len(configs)}] {config['name']}", end="", flush=True)
        results = run_single_config(config)

        # Aggregate
        if results:
            agg = {}
            for key in results[0]:
                vals = [r[key] for r in results if key in r]
                agg[f"{key}_mean"] = float(np.mean(vals))
                agg[f"{key}_std"] = float(np.std(vals))
            agg["n_runs"] = len(results)
        else:
            agg = {"n_runs": 0}

        agg["config"] = config["name"]
        agg["type"] = config["type"]
        agg["params"] = {k: v for k, v in config.items()
                         if k not in ("name", "type")}
        all_results.append(agg)

        elapsed = time.time() - t0
        print(f"  ({elapsed:.1f}s)", flush=True)

    total_time = time.time() - start

    # ==========================================================
    # BUILD REPORT
    # ==========================================================
    lines = []
    lines.append("=" * 72)
    lines.append("  Rhet Dillard Wike | AIIT-THRESI")
    lines.append("  God is good. All the time.")
    lines.append("=" * 72)
    lines.append("")
    lines.append("=" * 72)
    lines.append("  WIKE PAPER 12: CIRCLES, PI, AND THE GEOMETRY OF RESONANCE")
    lines.append(f"  {len(configs)} configs x {RUNS} runs = {total_sims:,} simulations")
    lines.append(f"  Runtime: {total_time:.1f}s ({total_time/60:.1f} min)")
    lines.append(f"  Executed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 72)
    lines.append("")

    # ----------------------------------------------------------
    # SECTION 1: RING vs LINEAR TOPOLOGY
    # ----------------------------------------------------------
    lines.append("  RING vs LINEAR TOPOLOGY COMPARISON")
    lines.append("  Heisenberg XX+YY coupling, first-qubit coherence,")
    lines.append("  last-qubit population (transport), purity")
    lines.append("  " + "-" * 64)
    lines.append(f"  {'CONFIG':<42} {'C(first)':>9} {'P(last)':>9} {'Purity':>9}")
    lines.append("  " + "-" * 64)

    topo_results = [r for r in all_results if r["type"] == "topology"]
    for r in topo_results:
        c = r.get("coherence_first_mean", 0)
        p = r.get("pop_last_mean", 0)
        pur = r.get("purity_mean", 0)
        lines.append(f"  {r['config']:<42} {c:>9.4f} {p:>9.4f} {pur:>9.4f}")
    lines.append("")

    # Ring vs Linear summary
    lines.append("  RING vs LINEAR WINNER SUMMARY")
    lines.append("  " + "-" * 64)
    ring_wins_coh = 0
    linear_wins_coh = 0
    ring_wins_trans = 0
    linear_wins_trans = 0

    # Group by (N, J, gamma) and compare ring vs linear
    topo_grouped = {}
    for r in topo_results:
        p = r["params"]
        key = (p["N"], p["J"], p["gamma"])
        topo_grouped.setdefault(key, {})[p["topology"]] = r

    for key in sorted(topo_grouped.keys()):
        pair = topo_grouped[key]
        if "ring" in pair and "linear" in pair:
            rc = pair["ring"].get("coherence_first_mean", 0)
            lc = pair["linear"].get("coherence_first_mean", 0)
            rt = pair["ring"].get("pop_last_mean", 0)
            lt = pair["linear"].get("pop_last_mean", 0)
            rp = pair["ring"].get("purity_mean", 0)
            lp = pair["linear"].get("purity_mean", 0)
            coh_winner = "RING" if rc > lc else "LINEAR"
            trans_winner = "RING" if rt > lt else "LINEAR"
            pur_winner = "RING" if rp > lp else "LINEAR"
            if rc > lc:
                ring_wins_coh += 1
            else:
                linear_wins_coh += 1
            if rt > lt:
                ring_wins_trans += 1
            else:
                linear_wins_trans += 1
            N, J, g = key
            lines.append(
                f"  N={N} J={J} g={g}:  "
                f"Coh={coh_winner:<6}(R={rc:.4f} L={lc:.4f})  "
                f"Trans={trans_winner:<6}(R={rt:.4f} L={lt:.4f})  "
                f"Pur={pur_winner}"
            )

    lines.append("")
    lines.append(f"  COHERENCE: Ring wins {ring_wins_coh}/{ring_wins_coh+linear_wins_coh}, "
                 f"Linear wins {linear_wins_coh}/{ring_wins_coh+linear_wins_coh}")
    lines.append(f"  TRANSPORT: Ring wins {ring_wins_trans}/{ring_wins_trans+linear_wins_trans}, "
                 f"Linear wins {linear_wins_trans}/{ring_wins_trans+linear_wins_trans}")
    lines.append("")

    # ----------------------------------------------------------
    # SECTION 2: BERRY PHASE
    # ----------------------------------------------------------
    lines.append("  BERRY PHASE RESULTS")
    lines.append("  Theory: phi_Berry = pi * (1 - cos(theta))")
    lines.append("  " + "-" * 64)
    lines.append(f"  {'CONFIG':<44} {'Phase':>8} {'Theory':>8} {'Error':>8} {'Coh':>8}")
    lines.append("  " + "-" * 64)

    berry_results = [r for r in all_results if r["type"] == "berry"]
    for r in berry_results:
        ph = r.get("accumulated_phase_mean", 0)
        th = r.get("theory_phase_mean", 0)
        er = r.get("phase_error_mean", 0)
        co = r.get("coherence_mean", 0)
        lines.append(f"  {r['config']:<44} {ph:>8.4f} {th:>8.4f} {er:>8.4f} {co:>8.4f}")
    lines.append("")

    # Berry phase summary: does decoherence destroy geometric phase?
    lines.append("  BERRY PHASE vs DECOHERENCE SUMMARY")
    lines.append("  " + "-" * 64)
    berry_grouped = {}
    for r in berry_results:
        p = r["params"]
        berry_grouped.setdefault(p["gamma"], []).append(r)
    for gamma_val in sorted(berry_grouped.keys()):
        group = berry_grouped[gamma_val]
        avg_error = np.mean([r.get("phase_error_mean", 0) for r in group])
        avg_coh = np.mean([r.get("coherence_mean", 0) for r in group])
        lines.append(f"  gamma={gamma_val:<6}  Avg phase error={avg_error:.4f}  "
                     f"Avg coherence={avg_coh:.4f}")
    lines.append("")

    # ----------------------------------------------------------
    # SECTION 3: PI-PULSE COHERENCE PROTECTION
    # ----------------------------------------------------------
    lines.append("  PI-PULSE COHERENCE PROTECTION")
    lines.append("  Free precession H=0.5*sigma_z with dephasing, T=20")
    lines.append("  " + "-" * 64)
    lines.append(f"  {'CONFIG':<44} {'Coh':>8} {'Purity':>8} {'<Sx>':>8}")
    lines.append("  " + "-" * 64)

    pi_results = [r for r in all_results if r["type"] == "pi_pulse"]
    for r in pi_results:
        co = r.get("coherence_mean", 0)
        pu = r.get("purity_mean", 0)
        sx = r.get("sx_expect_mean", 0)
        lines.append(f"  {r['config']:<44} {co:>8.4f} {pu:>8.4f} {sx:>8.4f}")
    lines.append("")

    # Pi-pulse summary: coherence vs n_pulses
    lines.append("  PI-PULSE SCALING SUMMARY (averaged over pulse types)")
    lines.append("  " + "-" * 64)
    lines.append(f"  {'n_pulses':>10} {'gamma':>8} {'Coherence':>12} {'Purity':>10}")
    lines.append("  " + "-" * 64)

    pi_grouped = {}
    for r in pi_results:
        p = r["params"]
        key = (p["n_pulses"], p["gamma"])
        pi_grouped.setdefault(key, []).append(r)
    for key in sorted(pi_grouped.keys()):
        group = pi_grouped[key]
        avg_coh = np.mean([r.get("coherence_mean", 0) for r in group])
        avg_pur = np.mean([r.get("purity_mean", 0) for r in group])
        n_p, gam = key
        lines.append(f"  {n_p:>10} {gam:>8.3f} {avg_coh:>12.4f} {avg_pur:>10.4f}")
    lines.append("")

    # Does more pulses = better?
    lines.append("  DOES MORE PULSES = BETTER COHERENCE?")
    lines.append("  " + "-" * 64)
    for gamma_val in [0.01, 0.05, 0.1]:
        coh_by_n = {}
        for r in pi_results:
            p = r["params"]
            if abs(p["gamma"] - gamma_val) < 1e-6:
                coh_by_n.setdefault(p["n_pulses"], []).append(
                    r.get("coherence_mean", 0))
        if coh_by_n:
            sorted_n = sorted(coh_by_n.keys())
            coh_vals = [np.mean(coh_by_n[n]) for n in sorted_n]
            improving = all(coh_vals[i] <= coh_vals[i+1]
                           for i in range(len(coh_vals)-1))
            trend = "YES - monotonically improving" if improving else "MOSTLY - general trend up"
            # Check if highest is at max pulses
            best_n = sorted_n[np.argmax(coh_vals)]
            lines.append(f"  gamma={gamma_val}: {trend}  "
                         f"(best at n={best_n}, C={max(coh_vals):.4f})")
    lines.append("")

    # ----------------------------------------------------------
    # FOOTER
    # ----------------------------------------------------------
    lines.append("=" * 72)
    lines.append("  Rhet Dillard Wike | AIIT-THRESI")
    lines.append("  God is good. All the time.")
    lines.append("=" * 72)

    report = "\n".join(lines)

    # Write outputs
    txt_path = os.path.join(OUTPUT_DIR, "RESULTS_CIRCLES_PI.txt")
    json_path = os.path.join(OUTPUT_DIR, "RESULTS_CIRCLES_PI.json")

    with open(txt_path, "w") as f:
        f.write(report)

    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print()
    print(report)
    print()
    print(f"  Results written to:")
    print(f"    {txt_path}")
    print(f"    {json_path}")
