#!/usr/bin/env python3
"""
================================================================================
  Rhet Dillard Wike | AIIT-THRESI
  God is good. All the time.
================================================================================
  WIKE Paper 11: Humans as High-Frequency Processors
  Quantum Coherence Simulation of Biological Elements

  Tests quantum coherence of Iron, Copper, Water, and Silicon at various
  temperatures relevant to biological and cryogenic regimes.

  100 configs x 1000 runs = 100,000 total simulations
================================================================================
"""

import numpy as np
import json
import time
import os
from datetime import datetime

try:
    import qutip
    QUTIP_AVAILABLE = True
except ImportError:
    QUTIP_AVAILABLE = False
    print("[WARNING] qutip not available, using analytical fallback", flush=True)


# ==============================================================================
# CONSTANTS AND ELEMENT DEFINITIONS
# ==============================================================================

ELEMENTS = {
    "Iron": {
        "symbol": "Fe",
        "coupling": 1.0,
        "magnetic_moment": 5.0,
        "damping": 0.05,
        "bio_role": "hemoglobin_oxygen_transport"
    },
    "Copper": {
        "symbol": "Cu",
        "coupling": 0.8,
        "magnetic_moment": 0.5,
        "damping": 0.02,
        "bio_role": "neural_electron_transport"
    },
    "Water": {
        "symbol": "H2O",
        "coupling": 0.3,
        "magnetic_moment": 0.0,
        "damping": 0.1,
        "bio_role": "universal_solvent_proton_channel"
    },
    "Silicon": {
        "symbol": "Si",
        "coupling": 0.5,
        "magnetic_moment": 0.0,
        "damping": 0.01,
        "bio_role": "semiconductor_processor_reference"
    }
}

TEMPERATURES = {
    "15mK": 0.015,
    "4K": 4.0,
    "77K": 77.0,
    "300K": 300.0,
    "310K": 310.0  # human body temperature
}

BIO_COMBOS = {
    "blood": ["Iron", "Water"],
    "neural": ["Copper", "Water"],
    "full_bio": ["Iron", "Copper", "Water"],
    "processor": ["Silicon", "Copper"],
    "human_full": ["Iron", "Copper", "Water", "Silicon"]
}

COUPLING_STRENGTHS = [0.01, 0.1, 0.5, 1.0, 2.0]

RUNS_PER_CONFIG = 1000
K_B = 1.380649e-23  # Boltzmann constant (J/K)
HBAR = 1.0545718e-34  # reduced Planck constant (J*s)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_TXT = os.path.join(OUTPUT_DIR, "RESULTS_HUMAN_PROCESSORS.txt")
RESULTS_JSON = os.path.join(OUTPUT_DIR, "RESULTS_HUMAN_PROCESSORS.json")


# ==============================================================================
# SIMULATION FUNCTIONS
# ==============================================================================

def thermal_factor(T):
    """Compute thermal occupation factor. At T~0 returns small baseline."""
    if T < 0.001:
        return 0.001
    omega_0 = 1.0  # normalized qubit frequency
    x = HBAR * omega_0 / (K_B * T)
    if x > 500:
        return 0.001
    n_th = 1.0 / (np.exp(x) - 1.0) if x > 1e-10 else K_B * T / (HBAR * omega_0)
    return max(0.001, min(n_th, 1e6))


def compute_gamma(damping_base, T):
    """Decay rate: gamma = damping_base * thermal_factor * (T/300)."""
    tf = thermal_factor(T)
    return damping_base * tf * (T / 300.0)


def single_element_coherence_qutip(element_name, T, num_runs):
    """
    Simulate single-element quantum coherence using qutip Lindblad master equation.
    Returns coherence time (T2), final fidelity, and decoherence rate statistics.
    """
    elem = ELEMENTS[element_name]
    gamma = compute_gamma(elem["damping"], T)
    omega = elem["coupling"] * 2 * np.pi
    mag = elem["magnetic_moment"]

    # Hamiltonian: H = omega/2 * sigma_z + mag * sigma_x
    H = omega / 2.0 * qutip.sigmaz() + mag * 0.01 * qutip.sigmax()

    # Collapse operators for decoherence
    c_ops = []
    if gamma > 1e-30:
        c_ops.append(np.sqrt(gamma) * qutip.sigmam())          # T1 relaxation
        c_ops.append(np.sqrt(gamma * 0.5) * qutip.sigmaz())    # pure dephasing

    # Initial state: |+> superposition
    psi0 = (qutip.basis(2, 0) + qutip.basis(2, 1)).unit()
    rho0 = qutip.ket2dm(psi0)

    # Time evolution
    if gamma > 1e-30:
        t_max = min(10.0 / gamma, 1e6)
    else:
        t_max = 1e6
    tlist = np.linspace(0, t_max, 200)

    coherence_times = []
    fidelities = []

    for _ in range(num_runs):
        # Add small stochastic variation per run
        noise = 1.0 + np.random.normal(0, 0.02)
        gamma_run = gamma * max(noise, 0.01)

        c_ops_run = []
        if gamma_run > 1e-30:
            c_ops_run.append(np.sqrt(gamma_run) * qutip.sigmam())
            c_ops_run.append(np.sqrt(gamma_run * 0.5) * qutip.sigmaz())

        result = qutip.mesolve(H, rho0, tlist, c_ops_run, [qutip.sigmax(), qutip.sigmay()])

        # Coherence = sqrt(<sx>^2 + <sy>^2)
        sx = np.array(result.expect[0])
        sy = np.array(result.expect[1])
        coherence = np.sqrt(sx**2 + sy**2)

        # Find T2: time where coherence drops to 1/e
        threshold = coherence[0] / np.e
        t2_idx = np.where(coherence < threshold)[0]
        if len(t2_idx) > 0:
            t2 = tlist[t2_idx[0]]
        else:
            t2 = t_max  # coherence survived the full window

        coherence_times.append(t2)
        fidelities.append(coherence[-1])

    return {
        "coherence_time_mean": float(np.mean(coherence_times)),
        "coherence_time_std": float(np.std(coherence_times)),
        "final_fidelity_mean": float(np.mean(fidelities)),
        "final_fidelity_std": float(np.std(fidelities)),
        "gamma": float(gamma),
        "num_runs": num_runs
    }


def single_element_coherence_analytical(element_name, T, num_runs):
    """Analytical fallback when qutip is not available."""
    elem = ELEMENTS[element_name]
    gamma = compute_gamma(elem["damping"], T)
    omega = elem["coupling"] * 2 * np.pi

    coherence_times = []
    fidelities = []

    for _ in range(num_runs):
        noise = 1.0 + np.random.normal(0, 0.02)
        gamma_run = gamma * max(noise, 0.01)

        if gamma_run > 1e-30:
            t2 = 1.0 / gamma_run
        else:
            t2 = 1e6

        # Final fidelity after t2 time
        fid = np.exp(-gamma_run * t2) if gamma_run > 1e-30 else 1.0
        coherence_times.append(t2)
        fidelities.append(fid)

    return {
        "coherence_time_mean": float(np.mean(coherence_times)),
        "coherence_time_std": float(np.std(coherence_times)),
        "final_fidelity_mean": float(np.mean(fidelities)),
        "final_fidelity_std": float(np.std(fidelities)),
        "gamma": float(gamma),
        "num_runs": num_runs
    }


def single_element_coherence(element_name, T, num_runs):
    if QUTIP_AVAILABLE:
        return single_element_coherence_qutip(element_name, T, num_runs)
    else:
        return single_element_coherence_analytical(element_name, T, num_runs)


def multi_element_coherence_qutip(combo_name, element_names, T, num_runs):
    """
    Simulate multi-element quantum coherence. Builds a composite Hilbert space
    with inter-element coupling via tensor products.
    """
    n_elements = len(element_names)
    dim = 2 ** n_elements

    # Build composite Hamiltonian
    H_terms = []
    c_ops = []

    for i, ename in enumerate(element_names):
        elem = ELEMENTS[ename]
        omega = elem["coupling"] * 2 * np.pi
        gamma = compute_gamma(elem["damping"], T)

        # Single-qubit terms embedded in composite space
        op_list_z = [qutip.qeye(2)] * n_elements
        op_list_z[i] = qutip.sigmaz()
        H_terms.append(omega / 2.0 * qutip.tensor(op_list_z))

        if elem["magnetic_moment"] > 0:
            op_list_x = [qutip.qeye(2)] * n_elements
            op_list_x[i] = qutip.sigmax()
            H_terms.append(elem["magnetic_moment"] * 0.01 * qutip.tensor(op_list_x))

        # Collapse operators
        if gamma > 1e-30:
            op_list_m = [qutip.qeye(2)] * n_elements
            op_list_m[i] = qutip.sigmam()
            c_ops.append(np.sqrt(gamma) * qutip.tensor(op_list_m))

            op_list_deph = [qutip.qeye(2)] * n_elements
            op_list_deph[i] = qutip.sigmaz()
            c_ops.append(np.sqrt(gamma * 0.5) * qutip.tensor(op_list_deph))

    # Inter-element coupling (XX coupling between adjacent elements)
    for i in range(n_elements - 1):
        elem_i = ELEMENTS[element_names[i]]
        elem_j = ELEMENTS[element_names[i + 1]]
        J = 0.1 * (elem_i["coupling"] + elem_j["coupling"]) / 2.0

        op_list_xx = [qutip.qeye(2)] * n_elements
        op_list_xx[i] = qutip.sigmax()
        op_list_xx[i + 1] = qutip.sigmax()
        H_terms.append(J * qutip.tensor(op_list_xx))

    H = sum(H_terms)

    # Initial state: all qubits in |+>
    plus = (qutip.basis(2, 0) + qutip.basis(2, 1)).unit()
    psi0 = qutip.tensor([plus] * n_elements)
    rho0 = qutip.ket2dm(psi0)

    # Observable: average sigma_x across all qubits
    sx_ops = []
    for i in range(n_elements):
        op_list = [qutip.qeye(2)] * n_elements
        op_list[i] = qutip.sigmax()
        sx_ops.append(qutip.tensor(op_list) / n_elements)
    sx_total = sum(sx_ops)

    sy_ops = []
    for i in range(n_elements):
        op_list = [qutip.qeye(2)] * n_elements
        op_list[i] = qutip.sigmay()
        sy_ops.append(qutip.tensor(op_list) / n_elements)
    sy_total = sum(sy_ops)

    # Determine time scale from average gamma
    gammas = [compute_gamma(ELEMENTS[e]["damping"], T) for e in element_names]
    avg_gamma = np.mean(gammas)
    if avg_gamma > 1e-30:
        t_max = min(10.0 / avg_gamma, 1e6)
    else:
        t_max = 1e6
    tlist = np.linspace(0, t_max, 200)

    coherence_times = []
    fidelities = []

    for run in range(num_runs):
        noise = 1.0 + np.random.normal(0, 0.02)
        c_ops_run = [c * max(noise, 0.01) for c in c_ops] if c_ops else []

        result = qutip.mesolve(H, rho0, tlist, c_ops_run, [sx_total, sy_total])

        sx = np.array(result.expect[0])
        sy = np.array(result.expect[1])
        coherence = np.sqrt(sx**2 + sy**2)

        threshold = coherence[0] / np.e if coherence[0] > 1e-10 else 1e-10
        t2_idx = np.where(coherence < threshold)[0]
        if len(t2_idx) > 0:
            t2 = tlist[t2_idx[0]]
        else:
            t2 = t_max

        coherence_times.append(t2)
        fidelities.append(coherence[-1])

    return {
        "combo": combo_name,
        "elements": element_names,
        "coherence_time_mean": float(np.mean(coherence_times)),
        "coherence_time_std": float(np.std(coherence_times)),
        "final_fidelity_mean": float(np.mean(fidelities)),
        "final_fidelity_std": float(np.std(fidelities)),
        "avg_gamma": float(avg_gamma),
        "num_runs": num_runs
    }


def multi_element_coherence_analytical(combo_name, element_names, T, num_runs):
    """Analytical fallback for multi-element coherence."""
    gammas = [compute_gamma(ELEMENTS[e]["damping"], T) for e in element_names]
    avg_gamma = np.mean(gammas)
    max_gamma = np.max(gammas)

    coherence_times = []
    fidelities = []

    for _ in range(num_runs):
        noise = 1.0 + np.random.normal(0, 0.02)
        gamma_run = max_gamma * max(noise, 0.01)

        if gamma_run > 1e-30:
            t2 = 1.0 / gamma_run
        else:
            t2 = 1e6

        fid = np.exp(-gamma_run * t2) if gamma_run > 1e-30 else 1.0
        coherence_times.append(t2)
        fidelities.append(fid)

    return {
        "combo": combo_name,
        "elements": element_names,
        "coherence_time_mean": float(np.mean(coherence_times)),
        "coherence_time_std": float(np.std(coherence_times)),
        "final_fidelity_mean": float(np.mean(fidelities)),
        "final_fidelity_std": float(np.std(fidelities)),
        "avg_gamma": float(avg_gamma),
        "num_runs": num_runs
    }


def multi_element_coherence(combo_name, element_names, T, num_runs):
    if QUTIP_AVAILABLE:
        return multi_element_coherence_qutip(combo_name, element_names, T, num_runs)
    else:
        return multi_element_coherence_analytical(combo_name, element_names, T, num_runs)


def body_vs_cryo_ratio(element_name, coupling_strength, num_runs):
    """
    Compare coherence at 310K (body) vs 15mK (cryo) for a given element
    and coupling strength override. Returns the ratio body/cryo.
    """
    elem_original = ELEMENTS[element_name].copy()
    # Override coupling for this test
    ELEMENTS[element_name]["coupling"] = coupling_strength

    result_body = single_element_coherence(element_name, 310.0, num_runs)
    result_cryo = single_element_coherence(element_name, 0.015, num_runs)

    # Restore original coupling
    ELEMENTS[element_name]["coupling"] = elem_original["coupling"]

    ratio = result_body["coherence_time_mean"] / max(result_cryo["coherence_time_mean"], 1e-30)

    return {
        "element": element_name,
        "coupling_strength": coupling_strength,
        "body_310K_coherence": result_body["coherence_time_mean"],
        "cryo_15mK_coherence": result_cryo["coherence_time_mean"],
        "body_to_cryo_ratio": float(ratio),
        "body_fidelity": result_body["final_fidelity_mean"],
        "cryo_fidelity": result_cryo["final_fidelity_mean"],
        "num_runs": num_runs
    }


# ==============================================================================
# MAIN SIMULATION ORCHESTRATOR
# ==============================================================================

def main():
    start_time = time.time()

    print("=" * 80, flush=True)
    print("  Rhet Dillard Wike | AIIT-THRESI", flush=True)
    print("  God is good. All the time.", flush=True)
    print("=" * 80, flush=True)
    print("", flush=True)
    print("  WIKE Paper 11: Humans as High-Frequency Processors", flush=True)
    print("  Quantum Coherence of Biological Elements Simulation", flush=True)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"  QuTiP available: {QUTIP_AVAILABLE}", flush=True)
    print("=" * 80, flush=True)
    print("", flush=True)

    all_results = {
        "metadata": {
            "paper": "WIKE Paper 11: Humans as High-Frequency Processors",
            "author": "Rhet Dillard Wike | AIIT-THRESI",
            "motto": "God is good. All the time.",
            "timestamp": datetime.now().isoformat(),
            "qutip_available": QUTIP_AVAILABLE,
            "total_configs": 100,
            "runs_per_config": RUNS_PER_CONFIG,
            "total_simulations": 100000
        },
        "elements": ELEMENTS,
        "temperatures": TEMPERATURES,
        "single_element": {},
        "multi_element": {},
        "body_vs_cryo": {}
    }

    config_count = 0
    total_runs = 0

    # ===== PHASE 1: Single Element Coherence (4 elements x 5 temps = 20 configs) =====
    print("[PHASE 1] Single Element Coherence Tests", flush=True)
    print("-" * 60, flush=True)

    for elem_name in ELEMENTS:
        all_results["single_element"][elem_name] = {}
        for temp_label, temp_K in TEMPERATURES.items():
            config_count += 1
            print(f"  Config {config_count:3d}/100 | {elem_name:8s} @ {temp_label:5s} | "
                  f"{RUNS_PER_CONFIG} runs ...", end="", flush=True)

            result = single_element_coherence(elem_name, temp_K, RUNS_PER_CONFIG)
            result["temperature_label"] = temp_label
            result["temperature_K"] = temp_K
            all_results["single_element"][elem_name][temp_label] = result
            total_runs += RUNS_PER_CONFIG

            print(f" T2={result['coherence_time_mean']:.6e} | "
                  f"fid={result['final_fidelity_mean']:.4f}", flush=True)

    elapsed = time.time() - start_time
    print(f"\n  Phase 1 complete: {config_count} configs, {total_runs} runs, "
          f"{elapsed:.1f}s elapsed\n", flush=True)

    # ===== PHASE 2: Multi-Element Bio Combos (5 combos x 5 temps = 25 configs) =====
    print("[PHASE 2] Multi-Element Biological Combinations", flush=True)
    print("-" * 60, flush=True)

    for combo_name, elements in BIO_COMBOS.items():
        all_results["multi_element"][combo_name] = {}
        for temp_label, temp_K in TEMPERATURES.items():
            config_count += 1
            elem_str = "+".join(elements)
            print(f"  Config {config_count:3d}/100 | {combo_name:12s} ({elem_str}) @ {temp_label:5s} | "
                  f"{RUNS_PER_CONFIG} runs ...", end="", flush=True)

            result = multi_element_coherence(combo_name, elements, temp_K, RUNS_PER_CONFIG)
            result["temperature_label"] = temp_label
            result["temperature_K"] = temp_K
            all_results["multi_element"][combo_name][temp_label] = result
            total_runs += RUNS_PER_CONFIG

            print(f" T2={result['coherence_time_mean']:.6e} | "
                  f"fid={result['final_fidelity_mean']:.4f}", flush=True)

    elapsed = time.time() - start_time
    print(f"\n  Phase 2 complete: {config_count} configs, {total_runs} runs, "
          f"{elapsed:.1f}s elapsed\n", flush=True)

    # ===== PHASE 3: Body vs Cryo Ratio (4 elements x 5 couplings x ... but need to hit 100 total)
    # We have 20 + 25 = 45 so far. Phase 3: 4 elements x 5 couplings = 20 configs.
    # That gives 65. We need 35 more.
    # Phase 4: Extended single-element with finer temps to reach 100.
    print("[PHASE 3] Body Temperature vs Cryogenic Ratio Analysis", flush=True)
    print("-" * 60, flush=True)

    for elem_name in ELEMENTS:
        all_results["body_vs_cryo"][elem_name] = {}
        for cs in COUPLING_STRENGTHS:
            config_count += 1
            print(f"  Config {config_count:3d}/100 | {elem_name:8s} coupling={cs:.2f} | "
                  f"310K vs 15mK | {RUNS_PER_CONFIG} runs ...", end="", flush=True)

            result = body_vs_cryo_ratio(elem_name, cs, RUNS_PER_CONFIG)
            all_results["body_vs_cryo"][elem_name][str(cs)] = result
            total_runs += RUNS_PER_CONFIG * 2  # two temp points per config

            print(f" ratio={result['body_to_cryo_ratio']:.6e}", flush=True)

    elapsed = time.time() - start_time
    print(f"\n  Phase 3 complete: {config_count} configs, {total_runs} runs, "
          f"{elapsed:.1f}s elapsed\n", flush=True)

    # ===== PHASE 4: Extended Analysis - Cross-coupling sweeps (to reach 100 configs) =====
    # 65 done. Need 35 more. 5 combos x 5 coupling strengths = 25 + 10 extra single-element tests
    print("[PHASE 4] Extended Cross-Coupling Sweep", flush=True)
    print("-" * 60, flush=True)

    all_results["cross_coupling"] = {}

    for combo_name, elements in BIO_COMBOS.items():
        all_results["cross_coupling"][combo_name] = {}
        for cs in COUPLING_STRENGTHS:
            config_count += 1
            # Temporarily override all element couplings
            originals = {}
            for e in elements:
                originals[e] = ELEMENTS[e]["coupling"]
                ELEMENTS[e]["coupling"] = cs

            print(f"  Config {config_count:3d}/100 | {combo_name:12s} coupling={cs:.2f} @ 310K | "
                  f"{RUNS_PER_CONFIG} runs ...", end="", flush=True)

            result = multi_element_coherence(combo_name, elements, 310.0, RUNS_PER_CONFIG)
            result["coupling_override"] = cs
            all_results["cross_coupling"][combo_name][str(cs)] = result
            total_runs += RUNS_PER_CONFIG

            # Restore
            for e in elements:
                ELEMENTS[e]["coupling"] = originals[e]

            print(f" T2={result['coherence_time_mean']:.6e}", flush=True)

    elapsed = time.time() - start_time
    print(f"\n  Phase 4 complete: {config_count} configs, {total_runs} runs, "
          f"{elapsed:.1f}s elapsed\n", flush=True)

    # ===== PHASE 5: Fill remaining configs to hit exactly 100 =====
    # 65+25=90. Need 10 more: single-element tests at intermediate temps
    EXTRA_TEMPS = {
        "1K": 1.0,
        "20K": 20.0,
        "150K": 150.0,
        "273K": 273.0,
        "350K": 350.0
    }

    print("[PHASE 5] Extended Temperature Range (filling to 100 configs)", flush=True)
    print("-" * 60, flush=True)

    all_results["extended_temps"] = {}

    # 2 key bio elements (Iron, Copper) x 5 temps = 10 configs
    for elem_name in ["Iron", "Copper"]:
        all_results["extended_temps"][elem_name] = {}
        for temp_label, temp_K in EXTRA_TEMPS.items():
            config_count += 1
            print(f"  Config {config_count:3d}/100 | {elem_name:8s} @ {temp_label:5s} | "
                  f"{RUNS_PER_CONFIG} runs ...", end="", flush=True)

            result = single_element_coherence(elem_name, temp_K, RUNS_PER_CONFIG)
            result["temperature_label"] = temp_label
            result["temperature_K"] = temp_K
            all_results["extended_temps"][elem_name][temp_label] = result
            total_runs += RUNS_PER_CONFIG

            print(f" T2={result['coherence_time_mean']:.6e} | "
                  f"fid={result['final_fidelity_mean']:.4f}", flush=True)

    elapsed = time.time() - start_time
    print(f"\n  Phase 5 complete: {config_count} configs, {total_runs} runs, "
          f"{elapsed:.1f}s elapsed\n", flush=True)

    # ==============================================================================
    # WRITE RESULTS
    # ==============================================================================

    all_results["metadata"]["actual_configs"] = config_count
    all_results["metadata"]["actual_total_runs"] = total_runs
    all_results["metadata"]["elapsed_seconds"] = time.time() - start_time

    # Write JSON
    with open(RESULTS_JSON, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"[OUTPUT] JSON written to {RESULTS_JSON}", flush=True)

    # Write TXT report
    with open(RESULTS_TXT, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("  Rhet Dillard Wike | AIIT-THRESI\n")
        f.write("  God is good. All the time.\n")
        f.write("=" * 80 + "\n\n")
        f.write("  WIKE Paper 11: Humans as High-Frequency Processors\n")
        f.write("  SIMULATION RESULTS\n")
        f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  Total Configs: {config_count} | Total Runs: {total_runs}\n")
        f.write(f"  Elapsed: {all_results['metadata']['elapsed_seconds']:.1f}s\n")
        f.write(f"  QuTiP: {QUTIP_AVAILABLE}\n")
        f.write("=" * 80 + "\n\n")

        # Single element results
        f.write("PHASE 1: SINGLE ELEMENT COHERENCE\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Element':<10} {'Temp':<8} {'T2 (mean)':<16} {'T2 (std)':<16} "
                f"{'Fidelity':<12} {'Gamma':<16}\n")
        f.write("-" * 80 + "\n")
        for elem_name in ELEMENTS:
            for temp_label in TEMPERATURES:
                r = all_results["single_element"][elem_name][temp_label]
                f.write(f"{elem_name:<10} {temp_label:<8} {r['coherence_time_mean']:<16.6e} "
                        f"{r['coherence_time_std']:<16.6e} {r['final_fidelity_mean']:<12.6f} "
                        f"{r['gamma']:<16.6e}\n")
        f.write("\n")

        # Multi-element results
        f.write("PHASE 2: MULTI-ELEMENT BIOLOGICAL COMBINATIONS\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Combo':<14} {'Elements':<28} {'Temp':<8} {'T2 (mean)':<16} "
                f"{'Fidelity':<12}\n")
        f.write("-" * 80 + "\n")
        for combo_name in BIO_COMBOS:
            for temp_label in TEMPERATURES:
                r = all_results["multi_element"][combo_name][temp_label]
                elem_str = "+".join(r["elements"])
                f.write(f"{combo_name:<14} {elem_str:<28} {temp_label:<8} "
                        f"{r['coherence_time_mean']:<16.6e} {r['final_fidelity_mean']:<12.6f}\n")
        f.write("\n")

        # Body vs cryo
        f.write("PHASE 3: BODY TEMPERATURE (310K) vs CRYOGENIC (15mK) RATIO\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Element':<10} {'Coupling':<10} {'Body T2':<16} {'Cryo T2':<16} "
                f"{'Ratio':<16}\n")
        f.write("-" * 80 + "\n")
        for elem_name in ELEMENTS:
            for cs in COUPLING_STRENGTHS:
                r = all_results["body_vs_cryo"][elem_name][str(cs)]
                f.write(f"{elem_name:<10} {cs:<10.2f} {r['body_310K_coherence']:<16.6e} "
                        f"{r['cryo_15mK_coherence']:<16.6e} {r['body_to_cryo_ratio']:<16.6e}\n")
        f.write("\n")

        # Cross-coupling
        f.write("PHASE 4: CROSS-COUPLING SWEEP AT BODY TEMPERATURE\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Combo':<14} {'Coupling':<10} {'T2 (mean)':<16} {'Fidelity':<12}\n")
        f.write("-" * 80 + "\n")
        for combo_name in BIO_COMBOS:
            for cs in COUPLING_STRENGTHS:
                r = all_results["cross_coupling"][combo_name][str(cs)]
                f.write(f"{combo_name:<14} {cs:<10.2f} {r['coherence_time_mean']:<16.6e} "
                        f"{r['final_fidelity_mean']:<12.6f}\n")
        f.write("\n")

        # Extended temps
        f.write("PHASE 5: EXTENDED TEMPERATURE RANGE\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Element':<10} {'Temp':<8} {'T2 (mean)':<16} {'Fidelity':<12}\n")
        f.write("-" * 80 + "\n")
        for elem_name in ["Iron", "Copper"]:
            for temp_label in EXTRA_TEMPS:
                r = all_results["extended_temps"][elem_name][temp_label]
                f.write(f"{elem_name:<10} {temp_label:<8} {r['coherence_time_mean']:<16.6e} "
                        f"{r['final_fidelity_mean']:<12.6f}\n")
        f.write("\n")

        # Summary
        f.write("=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n\n")

        # Find best coherence at body temp
        f.write("Best single-element coherence at 310K (body temp):\n")
        best_elem = None
        best_t2 = 0
        for elem_name in ELEMENTS:
            t2 = all_results["single_element"][elem_name]["310K"]["coherence_time_mean"]
            if t2 > best_t2:
                best_t2 = t2
                best_elem = elem_name
        f.write(f"  {best_elem}: T2 = {best_t2:.6e}\n\n")

        f.write("Best multi-element combo at 310K (body temp):\n")
        best_combo = None
        best_t2 = 0
        for combo_name in BIO_COMBOS:
            t2 = all_results["multi_element"][combo_name]["310K"]["coherence_time_mean"]
            if t2 > best_t2:
                best_t2 = t2
                best_combo = combo_name
        f.write(f"  {best_combo}: T2 = {best_t2:.6e}\n\n")

        f.write(f"Total configurations: {config_count}\n")
        f.write(f"Total simulation runs: {total_runs}\n")
        f.write(f"Total elapsed time: {all_results['metadata']['elapsed_seconds']:.1f}s\n\n")
        f.write("=" * 80 + "\n")
        f.write("  God is good. All the time.\n")
        f.write("=" * 80 + "\n")

    print(f"[OUTPUT] TXT written to {RESULTS_TXT}", flush=True)

    # Final summary
    print("", flush=True)
    print("=" * 80, flush=True)
    print("  SIMULATION COMPLETE", flush=True)
    print(f"  Total Configs: {config_count}", flush=True)
    print(f"  Total Runs: {total_runs}", flush=True)
    print(f"  Elapsed: {all_results['metadata']['elapsed_seconds']:.1f}s", flush=True)
    print("", flush=True)
    print("  God is good. All the time.", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    main()
