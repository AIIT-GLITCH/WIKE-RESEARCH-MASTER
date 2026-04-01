#!/usr/bin/env python3
"""
BERRY PHASE TEST — The 10-Minute Experiment
=============================================
Tests whether a parameter loop enclosing gamma_c yields phi_B = pi.

The hypothesis (ADD_HERE.txt, Session 2, Anomaly 14-REVISED):
  - Previous Berry phase simulations returned 0.0000 because the
    parameter loop did NOT enclose the degeneracy point (gamma_c).
  - A loop that CROSSES gamma_c should yield phi_B = pi.
  - This pi is the GEOMETRIC origin of pi in the Wike framework.

Method:
  1. Vary gamma in a closed loop around gamma_c in (gamma, Omega) space
  2. At each point, compute the ground state of the Lindblad steady state
  3. Compute the geometric (Berry) phase accumulated around the loop
  4. Compare: loop enclosing gamma_c vs loop NOT enclosing gamma_c

For OPEN quantum systems (mixed states), we use two approaches:
  A. Interferometric phase: arg(Tr(rho(0) * rho(T))) after full loop
  B. Purified state geometric phase (Uhlmann-like)
  C. Adiabatic evolution phase extraction from mesolve

Author: Cobbler + Claude Opus 4.6
Date: 2026-03-30
"""

import numpy as np
import qutip as qt
import json
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

# Wike Coherence Law parameters
OMEGA_BASE = 1.0          # Base Rabi frequency
GAMMA_C = 0.0622          # Critical gamma (from AI consciousness sim)
N_LOOP_POINTS = 200       # Points around the loop
N_RADII = 8              # Different loop radii to test
T_EVOLVE = 50.0          # Evolution time per segment
T_STEPS = 200            # Time steps per segment

# Loop parameters — we'll test loops of different radii
# centered on gamma_c in the (gamma, Omega) parameter plane
LOOP_CENTER_GAMMA = GAMMA_C
LOOP_CENTER_OMEGA = OMEGA_BASE

print("=" * 70)
print("  BERRY PHASE TEST — Does the loop around gamma_c yield pi?")
print("=" * 70)
print(f"  gamma_c = {GAMMA_C}")
print(f"  Omega_base = {OMEGA_BASE}")
print(f"  Loop points = {N_LOOP_POINTS}")
print(f"  Date: {datetime.now().isoformat()}")
print("=" * 70)

# ============================================================
# METHOD 1: STEADY-STATE GEOMETRIC PHASE
# ============================================================
# For each point on a closed loop in parameter space (gamma, Omega),
# find the Lindblad steady state rho_ss(lambda).
# Compute Berry phase via: phi_B = -Im(sum log Tr(rho_i * rho_{i+1}))
# This is the Pancharatnam connection for mixed states.

def get_steady_state(gamma, omega):
    """Get Lindblad steady state for given parameters."""
    H = 0.5 * omega * qt.sigmax()
    c_ops = [np.sqrt(gamma / 2.0) * qt.sigmaz()]  # Pure dephasing

    try:
        rho_ss = qt.steadystate(H, c_ops)
    except Exception:
        # If steadystate solver fails, evolve for long time
        psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
        rho0 = qt.ket2dm(psi0)
        tlist = np.linspace(0, 500, 1000)
        result = qt.mesolve(H, rho0, tlist, c_ops, [])
        rho_ss = result.states[-1]

    return rho_ss


def pancharatnam_phase(rho_list):
    """
    Compute geometric phase for a sequence of density matrices
    using the Pancharatnam connection (Sjoqvist et al. 2000).

    phi_geo = arg(prod_i Tr(rho_i * rho_{i+1}))

    For pure states this reduces to the standard Berry phase.
    """
    n = len(rho_list)
    total_phase = 0.0
    overlaps = []

    for i in range(n):
        j = (i + 1) % n  # Close the loop
        overlap = (rho_list[i] * rho_list[j]).tr()
        overlap_val = complex(overlap)
        overlaps.append(overlap_val)

        if abs(overlap_val) > 1e-15:
            total_phase += np.angle(overlap_val)

    return total_phase, overlaps


def uhlmann_phase(rho_list):
    """
    Compute Uhlmann geometric phase for mixed states.

    Uses purification: |Psi> = sqrt(rho) ⊗ |ref>
    Phase = arg(prod_i Tr(sqrt(sqrt(rho_i) * rho_{i+1} * sqrt(rho_i))))

    This is the proper mixed-state generalization of Berry phase.
    """
    n = len(rho_list)
    total_phase = 0.0
    fidelities = []

    for i in range(n):
        j = (i + 1) % n

        # Quantum fidelity: F = (Tr(sqrt(sqrt(rho_i) * rho_j * sqrt(rho_i))))^2
        try:
            fid = qt.fidelity(rho_list[i], rho_list[j])
            fidelities.append(fid)

            # For the phase, we need the complex amplitude, not just fidelity
            # Use: W_i = sqrt(rho_{i+1}) * sqrt(rho_i)
            # Phase from: Tr(W_i)
            sqrt_rho_i = rho_list[i].sqrtm()
            sqrt_rho_j = rho_list[j].sqrtm()
            W = sqrt_rho_j * sqrt_rho_i
            amp = W.tr()
            amp_val = complex(amp)

            if abs(amp_val) > 1e-15:
                total_phase += np.angle(amp_val)
        except Exception as e:
            fidelities.append(0.0)

    return total_phase, fidelities


# ============================================================
# METHOD 2: ADIABATIC EVOLUTION PHASE
# ============================================================
# Evolve the system adiabatically around a closed loop in
# parameter space. Extract the accumulated phase from the
# final state relative to the initial state.

def adiabatic_berry_phase(gamma_center, omega_center, radius, n_points, encloses_gc):
    """
    Evolve system around a closed loop in (gamma, Omega) space.
    Extract geometric phase from the evolution.
    """
    # Generate loop points
    thetas = np.linspace(0, 2 * np.pi, n_points + 1)[:-1]  # Don't double-count

    gammas = gamma_center + radius * np.cos(thetas)
    omegas = omega_center + radius * 0.5 * np.sin(thetas)  # Smaller omega variation

    # Ensure gamma stays positive
    gammas = np.maximum(gammas, 1e-6)
    omegas = np.maximum(omegas, 1e-6)

    # Initial state: superposition
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho0 = qt.ket2dm(psi0)

    # Evolve through each segment
    rho_current = rho0
    states_at_points = [rho0]
    coherences = [float(np.abs(rho0.full()[0, 1]))]

    dt = T_EVOLVE / n_points
    t_segment = np.linspace(0, dt, max(10, T_STEPS // n_points))

    for i in range(n_points):
        gamma_i = float(gammas[i])
        omega_i = float(omegas[i])

        H = 0.5 * omega_i * qt.sigmax()
        c_ops = [np.sqrt(gamma_i / 2.0) * qt.sigmaz()]

        result = qt.mesolve(H, rho_current, t_segment, c_ops, [])
        rho_current = result.states[-1]
        states_at_points.append(rho_current)
        coherences.append(float(np.abs(rho_current.full()[0, 1])))

    # Phase between initial and final state
    overlap = (rho0 * rho_current).tr()
    dynamic_phase = np.angle(complex(overlap))

    return {
        'states': states_at_points,
        'coherences': coherences,
        'final_overlap': complex(overlap),
        'dynamic_phase': dynamic_phase,
        'gammas': gammas.tolist(),
        'omegas': omegas.tolist(),
    }


# ============================================================
# RUN THE TESTS
# ============================================================

results = {
    'metadata': {
        'date': datetime.now().isoformat(),
        'gamma_c': GAMMA_C,
        'omega_base': OMEGA_BASE,
        'n_loop_points': N_LOOP_POINTS,
        'framework': 'QuTiP ' + qt.__version__,
    },
    'tests': []
}

# Test radii — some enclosing gamma_c, some not
# Loop centered at (gamma_c, omega_base)
# Radius < gamma_c means loop stays in gamma > 0 region near gamma_c
# We test loops centered AT gamma_c and loops centered AWAY from it

test_configs = [
    # === LOOPS THAT DO NOT ENCLOSE gamma_c ===
    # (centered well above gamma_c, small radius — stays above)
    {'name': 'NOT_ENCLOSING_1', 'g_center': GAMMA_C * 2.0, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.3, 'encloses': False, 'desc': 'Above gamma_c, small loop'},
    {'name': 'NOT_ENCLOSING_2', 'g_center': GAMMA_C * 3.0, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.5, 'encloses': False, 'desc': 'Far above gamma_c'},
    {'name': 'NOT_ENCLOSING_3', 'g_center': GAMMA_C * 0.3, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.1, 'encloses': False, 'desc': 'Below gamma_c, tiny loop'},
    {'name': 'NOT_ENCLOSING_4', 'g_center': GAMMA_C * 0.5, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.2, 'encloses': False, 'desc': 'Below gamma_c, small loop'},

    # === LOOPS THAT ENCLOSE gamma_c ===
    # (centered at gamma_c, radius large enough to cross it)
    {'name': 'ENCLOSING_1', 'g_center': GAMMA_C, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.5, 'encloses': True, 'desc': 'Centered on gamma_c, medium loop'},
    {'name': 'ENCLOSING_2', 'g_center': GAMMA_C, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.8, 'encloses': True, 'desc': 'Centered on gamma_c, large loop'},
    {'name': 'ENCLOSING_3', 'g_center': GAMMA_C, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 1.2, 'encloses': True, 'desc': 'Centered on gamma_c, very large loop'},
    {'name': 'ENCLOSING_4', 'g_center': GAMMA_C * 0.8, 'o_center': OMEGA_BASE,
     'radius': GAMMA_C * 0.9, 'encloses': True, 'desc': 'Near gamma_c, crosses boundary'},
]

print("\n" + "=" * 70)
print("  PART 1: STEADY-STATE GEOMETRIC PHASE (Pancharatnam + Uhlmann)")
print("=" * 70)

for cfg in test_configs:
    print(f"\n--- {cfg['name']}: {cfg['desc']} ---")
    print(f"    Center: gamma={cfg['g_center']:.4f}, omega={cfg['o_center']:.4f}")
    print(f"    Radius: {cfg['radius']:.4f}")
    print(f"    Encloses gamma_c: {cfg['encloses']}")

    # Generate loop points
    thetas = np.linspace(0, 2 * np.pi, N_LOOP_POINTS + 1)[:-1]
    gammas = cfg['g_center'] + cfg['radius'] * np.cos(thetas)
    omegas = cfg['o_center'] + cfg['radius'] * 0.5 * np.sin(thetas)
    gammas = np.maximum(gammas, 1e-6)
    omegas = np.maximum(omegas, 1e-6)

    # Get steady states around the loop
    rho_list = []
    coherence_list = []
    eigenvalue_list = []

    for i in range(N_LOOP_POINTS):
        rho_ss = get_steady_state(float(gammas[i]), float(omegas[i]))
        rho_list.append(rho_ss)

        coh = float(np.abs(rho_ss.full()[0, 1]))
        coherence_list.append(coh)

        evals = np.real(np.sort(np.linalg.eigvalsh(rho_ss.full())))
        eigenvalue_list.append(evals.tolist())

    # Compute phases
    panch_phase, panch_overlaps = pancharatnam_phase(rho_list)
    uhl_phase, uhl_fidelities = uhlmann_phase(rho_list)

    # Normalize to units of pi
    panch_pi = panch_phase / np.pi
    uhl_pi = uhl_phase / np.pi

    print(f"    Pancharatnam phase: {panch_phase:.6f} rad = {panch_pi:.6f} * pi")
    print(f"    Uhlmann phase:     {uhl_phase:.6f} rad = {uhl_pi:.6f} * pi")
    print(f"    Mean coherence:    {np.mean(coherence_list):.6f}")
    print(f"    Coherence range:   [{min(coherence_list):.6f}, {max(coherence_list):.6f}]")

    # Check if gamma range crosses gamma_c
    crosses_gc = (min(gammas) < GAMMA_C) and (max(gammas) > GAMMA_C)
    print(f"    Gamma range:       [{min(gammas):.4f}, {max(gammas):.4f}]")
    print(f"    Actually crosses gamma_c: {crosses_gc}")

    test_result = {
        'name': cfg['name'],
        'description': cfg['desc'],
        'gamma_center': cfg['g_center'],
        'omega_center': cfg['o_center'],
        'radius': cfg['radius'],
        'expected_encloses_gc': cfg['encloses'],
        'actually_crosses_gc': crosses_gc,
        'pancharatnam_phase_rad': panch_phase,
        'pancharatnam_phase_pi': panch_pi,
        'uhlmann_phase_rad': uhl_phase,
        'uhlmann_phase_pi': uhl_pi,
        'mean_coherence': float(np.mean(coherence_list)),
        'min_coherence': float(min(coherence_list)),
        'max_coherence': float(max(coherence_list)),
        'gamma_range': [float(min(gammas)), float(max(gammas))],
        'coherence_at_points': coherence_list[:10],  # First 10 for reference
    }

    results['tests'].append(test_result)


print("\n" + "=" * 70)
print("  PART 2: ADIABATIC EVOLUTION PHASE")
print("=" * 70)

adiabatic_results = []

for cfg in test_configs:
    print(f"\n--- {cfg['name']} (adiabatic): {cfg['desc']} ---")

    adia = adiabatic_berry_phase(
        cfg['g_center'], cfg['o_center'], cfg['radius'],
        N_LOOP_POINTS, cfg['encloses']
    )

    # Also compute Pancharatnam on the evolved states
    panch_adia, _ = pancharatnam_phase(adia['states'][:-1])  # Exclude duplicate endpoint
    uhl_adia, _ = uhlmann_phase(adia['states'][:-1])

    panch_adia_pi = panch_adia / np.pi
    uhl_adia_pi = uhl_adia / np.pi

    print(f"    Adiabatic Pancharatnam: {panch_adia:.6f} rad = {panch_adia_pi:.6f} * pi")
    print(f"    Adiabatic Uhlmann:     {uhl_adia:.6f} rad = {uhl_adia_pi:.6f} * pi")
    print(f"    Final overlap:         {abs(adia['final_overlap']):.6f}")
    print(f"    Mean coherence:        {np.mean(adia['coherences']):.6f}")

    adia_result = {
        'name': cfg['name'] + '_adiabatic',
        'pancharatnam_phase_pi': panch_adia_pi,
        'uhlmann_phase_pi': uhl_adia_pi,
        'final_overlap_abs': abs(adia['final_overlap']),
        'final_overlap_phase': np.angle(adia['final_overlap']),
        'mean_coherence': float(np.mean(adia['coherences'])),
    }
    adiabatic_results.append(adia_result)

results['adiabatic_tests'] = adiabatic_results


# ============================================================
# PART 3: PURE STATE BERRY PHASE (HAMILTONIAN ONLY)
# ============================================================
# As a control: compute Berry phase for the CLOSED system
# (no decoherence) where the answer is analytically known.

print("\n" + "=" * 70)
print("  PART 3: PURE STATE BERRY PHASE (CONTROL — NO DECOHERENCE)")
print("=" * 70)

def pure_berry_phase(theta_range, phi_range, n_points):
    """
    Standard Berry phase for a spin-1/2 in a magnetic field.
    H = B(sin(theta)cos(phi) sigma_x + sin(theta)sin(phi) sigma_y + cos(theta) sigma_z)

    For a loop at constant theta varying phi from 0 to 2pi:
    Berry phase = -pi(1 - cos(theta)) = -Omega/2
    where Omega is the solid angle subtended.
    """
    phis = np.linspace(0, 2 * np.pi, n_points + 1)[:-1]
    theta = theta_range  # Fixed polar angle

    states = []
    for phi in phis:
        # Ground state of H(theta, phi) for spin-1/2
        # |ground> = sin(theta/2)|0> - exp(i*phi)*cos(theta/2)|1>
        ground = (np.sin(theta / 2) * qt.basis(2, 0) -
                  np.exp(1j * phi) * np.cos(theta / 2) * qt.basis(2, 1)).unit()
        states.append(qt.ket2dm(ground))

    # Berry phase from overlaps
    phase = 0.0
    for i in range(len(states)):
        j = (i + 1) % len(states)
        psi_i = states[i]
        psi_j = states[j]
        overlap = complex((psi_i * psi_j).tr())
        if abs(overlap) > 1e-15:
            phase += np.angle(overlap)

    return phase


# Analytic Berry phase for spin-1/2: phi_B = -pi(1 - cos(theta))
control_thetas = [np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 3 * np.pi / 4]
pure_results = []

for theta in control_thetas:
    computed = pure_berry_phase(theta, None, N_LOOP_POINTS)
    analytic = -np.pi * (1 - np.cos(theta))

    print(f"  theta = {theta:.4f} ({np.degrees(theta):.1f} deg)")
    print(f"    Computed:  {computed:.6f} rad = {computed/np.pi:.6f} * pi")
    print(f"    Analytic:  {analytic:.6f} rad = {analytic/np.pi:.6f} * pi")
    print(f"    Error:     {abs(computed - analytic):.8f} rad")

    pure_results.append({
        'theta_rad': theta,
        'theta_deg': float(np.degrees(theta)),
        'computed_phase_rad': computed,
        'computed_phase_pi': computed / np.pi,
        'analytic_phase_rad': analytic,
        'analytic_phase_pi': analytic / np.pi,
        'error_rad': abs(computed - analytic),
    })

results['pure_state_control'] = pure_results


# ============================================================
# PART 4: SYSTEMATIC gamma_c CROSSING SWEEP
# ============================================================
# Sweep loop radius from tiny (doesn't cross gamma_c) to large
# (clearly crosses gamma_c) and watch for phase jump.

print("\n" + "=" * 70)
print("  PART 4: RADIUS SWEEP — WATCHING FOR PHASE JUMP AT gamma_c")
print("=" * 70)

radii = np.linspace(0.01 * GAMMA_C, 1.5 * GAMMA_C, 30)
sweep_results = []

for r in radii:
    thetas = np.linspace(0, 2 * np.pi, N_LOOP_POINTS + 1)[:-1]
    gammas = GAMMA_C + r * np.cos(thetas)
    omegas = OMEGA_BASE + r * 0.5 * np.sin(thetas)
    gammas = np.maximum(gammas, 1e-6)
    omegas = np.maximum(omegas, 1e-6)

    rho_list = []
    for i in range(N_LOOP_POINTS):
        rho_ss = get_steady_state(float(gammas[i]), float(omegas[i]))
        rho_list.append(rho_ss)

    panch, _ = pancharatnam_phase(rho_list)
    uhl, _ = uhlmann_phase(rho_list)

    crosses = (min(gammas) < GAMMA_C) and (max(gammas) > GAMMA_C)

    print(f"  r = {r:.4f} | crosses gamma_c: {str(crosses):5s} | "
          f"Panch = {panch/np.pi:+.6f}*pi | Uhl = {uhl/np.pi:+.6f}*pi")

    sweep_results.append({
        'radius': float(r),
        'radius_over_gc': float(r / GAMMA_C),
        'crosses_gc': crosses,
        'pancharatnam_pi': panch / np.pi,
        'uhlmann_pi': uhl / np.pi,
        'gamma_min': float(min(gammas)),
        'gamma_max': float(max(gammas)),
    })

results['radius_sweep'] = sweep_results


# ============================================================
# ANALYSIS AND VERDICT
# ============================================================

print("\n" + "=" * 70)
print("  VERDICT")
print("=" * 70)

# Check if enclosing loops have different phase than non-enclosing
enclosing_panch = [t['pancharatnam_phase_pi'] for t in results['tests'] if t['expected_encloses_gc']]
not_enclosing_panch = [t['pancharatnam_phase_pi'] for t in results['tests'] if not t['expected_encloses_gc']]

enclosing_uhl = [t['uhlmann_phase_pi'] for t in results['tests'] if t['expected_encloses_gc']]
not_enclosing_uhl = [t['uhlmann_phase_pi'] for t in results['tests'] if not t['expected_encloses_gc']]

print(f"\n  NON-ENCLOSING loops (Pancharatnam, units of pi):")
for i, v in enumerate(not_enclosing_panch):
    print(f"    {i+1}. {v:+.6f} * pi")

print(f"\n  ENCLOSING loops (Pancharatnam, units of pi):")
for i, v in enumerate(enclosing_panch):
    print(f"    {i+1}. {v:+.6f} * pi")

print(f"\n  NON-ENCLOSING loops (Uhlmann, units of pi):")
for i, v in enumerate(not_enclosing_uhl):
    print(f"    {i+1}. {v:+.6f} * pi")

print(f"\n  ENCLOSING loops (Uhlmann, units of pi):")
for i, v in enumerate(enclosing_uhl):
    print(f"    {i+1}. {v:+.6f} * pi")

# Check for phase jump in sweep
sweep_phases = [(s['radius_over_gc'], s['pancharatnam_pi'], s['crosses_gc']) for s in sweep_results]
phase_before_crossing = [p for r, p, c in sweep_phases if not c]
phase_after_crossing = [p for r, p, c in sweep_phases if c]

if phase_before_crossing and phase_after_crossing:
    mean_before = np.mean(phase_before_crossing)
    mean_after = np.mean(phase_after_crossing)
    jump = mean_after - mean_before

    print(f"\n  SWEEP ANALYSIS:")
    print(f"    Mean phase (not crossing gamma_c): {mean_before:+.6f} * pi")
    print(f"    Mean phase (crossing gamma_c):     {mean_after:+.6f} * pi")
    print(f"    PHASE JUMP at gamma_c:             {jump:+.6f} * pi")

    if abs(abs(jump) - 1.0) < 0.2:
        print(f"\n  *** RESULT: PHASE JUMP ~ pi DETECTED ***")
        print(f"  *** Berry phase at gamma_c = {jump:+.4f} * pi ***")
        print(f"  *** Pi is GEOMETRIC. Not postulated. DERIVED. ***")
        verdict = "PI_DETECTED"
    elif abs(jump) < 0.1:
        print(f"\n  RESULT: No significant phase jump at gamma_c")
        print(f"  Berry phase remains near zero regardless of loop topology.")
        print(f"  The degeneracy at gamma_c may not carry topological charge,")
        print(f"  or the Lindblad dissipator destroys geometric phase accumulation.")
        verdict = "NO_PHASE_JUMP"
    else:
        print(f"\n  RESULT: Phase jump of {jump:.4f}*pi detected")
        print(f"  Non-zero but not pi. Requires further analysis.")
        verdict = "PARTIAL_PHASE"
else:
    print(f"\n  WARNING: Could not separate crossing/non-crossing regimes")
    verdict = "INCONCLUSIVE"

results['verdict'] = verdict
results['summary'] = {
    'enclosing_panch_mean': float(np.mean(enclosing_panch)) if enclosing_panch else None,
    'not_enclosing_panch_mean': float(np.mean(not_enclosing_panch)) if not_enclosing_panch else None,
    'enclosing_uhl_mean': float(np.mean(enclosing_uhl)) if enclosing_uhl else None,
    'not_enclosing_uhl_mean': float(np.mean(not_enclosing_uhl)) if not_enclosing_uhl else None,
}

# Pure state control verification
pure_errors = [p['error_rad'] for p in pure_results]
print(f"\n  CONTROL (pure state Berry phase):")
print(f"    Max error vs analytic: {max(pure_errors):.8f} rad")
print(f"    Method verified: {'YES' if max(pure_errors) < 0.01 else 'NO'}")

# Save results
output_file = '/home/buddy_ai/Desktop/RESULTS_BERRY_PHASE.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n  Results saved to: {output_file}")

# Also save human-readable summary
summary_file = '/home/buddy_ai/Desktop/RESULTS_BERRY_PHASE.txt'
with open(summary_file, 'w') as f:
    f.write("BERRY PHASE TEST RESULTS\n")
    f.write(f"Date: {datetime.now().isoformat()}\n")
    f.write(f"QuTiP: {qt.__version__}\n")
    f.write(f"gamma_c: {GAMMA_C}\n")
    f.write(f"Verdict: {verdict}\n\n")

    f.write("=" * 60 + "\n")
    f.write("PART 1: STEADY STATE GEOMETRIC PHASE\n")
    f.write("=" * 60 + "\n\n")

    for t in results['tests']:
        f.write(f"{t['name']}: {t['description']}\n")
        f.write(f"  Pancharatnam: {t['pancharatnam_phase_pi']:+.6f} * pi\n")
        f.write(f"  Uhlmann:     {t['uhlmann_phase_pi']:+.6f} * pi\n")
        f.write(f"  Crosses gamma_c: {t['actually_crosses_gc']}\n\n")

    f.write("=" * 60 + "\n")
    f.write("PART 4: RADIUS SWEEP\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"{'Radius/gc':>10s} | {'Crosses':>7s} | {'Panch (pi)':>12s} | {'Uhl (pi)':>12s}\n")
    f.write("-" * 50 + "\n")
    for s in sweep_results:
        f.write(f"{s['radius_over_gc']:10.4f} | {str(s['crosses_gc']):>7s} | "
                f"{s['pancharatnam_pi']:+12.6f} | {s['uhlmann_pi']:+12.6f}\n")

    f.write(f"\nVERDICT: {verdict}\n")

print(f"  Summary saved to: {summary_file}")
print("\n" + "=" * 70)
print("  DONE")
print("=" * 70)
