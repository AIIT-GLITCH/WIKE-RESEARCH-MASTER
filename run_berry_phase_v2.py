#!/usr/bin/env python3
"""
BERRY PHASE TEST v2 — FIXED
============================
v1 bug: Tr(rho_i * rho_j) = |<psi_i|psi_j>|^2 is always real.
         Can't get phase from density matrix overlaps.

Fix: Use STATE VECTORS for pure-state Berry phase (control),
     then test whether Lindblad dephasing at gamma_c modifies it.

The proper question is NOT "does gamma_c have a Berry phase"
but rather: "does dephasing near gamma_c MODIFY the geometric
phase that the Hamiltonian's parameter loop already carries?"

Setup: Spin-1/2 in rotating magnetic field
  H(phi) = B[sin(theta)cos(phi) sigma_x + sin(theta)sin(phi) sigma_y + cos(theta) sigma_z]
  Loop: phi goes 0 -> 2pi at fixed theta
  Pure Berry phase = -pi(1 - cos(theta))   [Exact, analytic]
  At theta = pi/2: Berry phase = -pi       [The prediction]

Then add Lindblad dephasing and ask: what happens to the phase?

Author: Cobbler + Claude Opus 4.6
Date: 2026-03-30
"""

import numpy as np
import qutip as qt
import json
from datetime import datetime

print("=" * 70)
print("  BERRY PHASE v2 — FIXED COMPUTATION")
print("=" * 70)
print(f"  Date: {datetime.now().isoformat()}")
print(f"  QuTiP: {qt.__version__}")
print("=" * 70)

# ============================================================
# PART 1: PURE STATE BERRY PHASE (State vector method)
# ============================================================

def ground_state_spin_half(theta, phi):
    """
    Ground state of H = B * n_hat . sigma
    where n_hat = (sin(theta)cos(phi), sin(theta)sin(phi), cos(theta))

    Ground state (eigenvalue -B):
    |-> = sin(theta/2)|0> - exp(i*phi)*cos(theta/2)|1>
    """
    psi = (np.sin(theta / 2) * qt.basis(2, 0) -
           np.exp(1j * phi) * np.cos(theta / 2) * qt.basis(2, 1))
    return psi.unit()


def berry_phase_pure(theta, n_points=500):
    """
    Compute Berry phase for spin-1/2 ground state as phi: 0 -> 2pi.
    Uses discrete Pancharatnam connection on STATE VECTORS.

    phi_B = -Im(sum_i log <psi_i|psi_{i+1}>)
    """
    phis = np.linspace(0, 2 * np.pi, n_points + 1)  # Include endpoint for closure

    # Get state vectors
    states = [ground_state_spin_half(theta, phi) for phi in phis]

    # Accumulate phase via overlaps of STATE VECTORS (not density matrices!)
    total_phase = 0.0
    for i in range(n_points):
        overlap = states[i].dag() * states[i + 1]
        # In QuTiP 5, this returns a scalar directly
        if hasattr(overlap, 'full'):
            overlap_val = complex(overlap.full()[0, 0])
        elif hasattr(overlap, '__getitem__'):
            try:
                overlap_val = complex(overlap[0, 0])
            except TypeError:
                overlap_val = complex(overlap)
        else:
            overlap_val = complex(overlap)

        # Gauge fix: make overlap real and positive by parallel transport
        if abs(overlap_val) > 1e-15:
            total_phase += np.angle(overlap_val)

    return total_phase


print("\n--- PART 1: PURE STATE CONTROL ---")
print("    Testing Berry phase computation on known analytic results\n")

thetas = [np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, np.pi]
control_results = []

for theta in thetas:
    computed = berry_phase_pure(theta, n_points=2000)
    analytic = -np.pi * (1 - np.cos(theta))
    error = abs(computed - analytic)

    print(f"  theta = {np.degrees(theta):6.1f} deg | "
          f"Computed: {computed/np.pi:+8.5f}*pi | "
          f"Analytic: {analytic/np.pi:+8.5f}*pi | "
          f"Error: {error:.6f} rad")

    control_results.append({
        'theta_deg': float(np.degrees(theta)),
        'computed_pi': computed / np.pi,
        'analytic_pi': analytic / np.pi,
        'error_rad': error,
    })

max_error = max(r['error_rad'] for r in control_results)
print(f"\n  Max error: {max_error:.6f} rad")
print(f"  Method works: {'YES' if max_error < 0.05 else 'NO'}")


# ============================================================
# PART 2: BERRY PHASE UNDER DEPHASING
# ============================================================
# Now the real test: add Lindblad dephasing and see how it
# modifies the geometric phase.
#
# Method: Adiabatic evolution around the loop with mesolve.
# Extract phase from off-diagonal element of final density matrix
# relative to initial.

print("\n" + "=" * 70)
print("  PART 2: BERRY PHASE UNDER DEPHASING")
print("=" * 70)

def berry_phase_with_dephasing(theta, gamma, n_points=200, B=1.0, n_cycles=1):
    """
    Evolve spin-1/2 adiabatically around a loop in field direction
    with Lindblad dephasing. Extract geometric phase.

    H(t) = B * [sin(theta)cos(phi(t)) sigma_x +
                sin(theta)sin(phi(t)) sigma_y +
                cos(theta) sigma_z]

    phi(t) goes from 0 to 2*pi over time T.
    T must be >> 1/B for adiabaticity.

    Collapse operator: sqrt(gamma) * sigma_z (pure dephasing along z)
    """
    # Adiabatic condition: T >> 2*pi/B
    T_total = 200.0 / B  # Well into adiabatic regime
    tlist = np.linspace(0, T_total * n_cycles, n_points * n_cycles + 1)

    # Time-dependent Hamiltonian using string-based coefficient
    # phi(t) = 2*pi*t/T
    sx = qt.sigmax()
    sy = qt.sigmay()
    sz = qt.sigmaz()

    omega_drive = 2 * np.pi / T_total  # Angular frequency of field rotation

    # H(t) = B*sin(theta)*cos(omega*t)*sx + B*sin(theta)*sin(omega*t)*sy + B*cos(theta)*sz
    H_coeff_x = f'{B * np.sin(theta)} * np.cos({omega_drive} * t)'
    H_coeff_y = f'{B * np.sin(theta)} * np.sin({omega_drive} * t)'
    H_static = B * np.cos(theta) * sz

    H = [H_static, [sx, H_coeff_x], [sy, H_coeff_y]]

    # Collapse operators
    if gamma > 1e-12:
        c_ops = [np.sqrt(gamma) * sz]
    else:
        c_ops = []

    # Initial state: ground state at phi=0
    psi0 = ground_state_spin_half(theta, 0.0)
    rho0 = qt.ket2dm(psi0)

    # Evolve
    result = qt.mesolve(H, rho0, tlist, c_ops, [])

    rho_final = result.states[-1]

    # Extract phase information
    # The off-diagonal element carries the geometric + dynamic phase
    rho_01_initial = complex(rho0.full()[0, 1])
    rho_01_final = complex(rho_final.full()[0, 1])

    # Coherence magnitude
    coh_initial = abs(rho_01_initial)
    coh_final = abs(rho_01_final)

    # Phase of off-diagonal element
    phase_initial = np.angle(rho_01_initial) if coh_initial > 1e-15 else 0.0
    phase_final = np.angle(rho_01_final) if coh_final > 1e-15 else 0.0

    # Total accumulated phase (includes dynamic + geometric)
    total_phase = phase_final - phase_initial

    # For comparison: dynamic phase for ground state over one cycle
    # E_ground = -B, so dynamic phase = B*T = B * (2*pi/(omega_drive))
    dynamic_phase = -B * T_total * n_cycles  # Accumulated dynamic phase
    dynamic_phase_mod = dynamic_phase % (2 * np.pi)

    # Geometric phase = total - dynamic (mod 2*pi)
    # But this is hard to extract cleanly from mixed states
    # Better approach: compare phase WITH and WITHOUT the loop

    # Overlap between initial and final
    overlap = complex((rho0 * rho_final).tr())
    fidelity = qt.fidelity(rho0, rho_final) ** 2

    # For pure states evolved adiabatically:
    # <psi(0)|psi(T)> = exp(i * dynamic_phase) * exp(i * berry_phase)
    # We can extract berry phase by comparing two evolutions:
    # one with the loop, one without (static H)

    return {
        'coherence_initial': coh_initial,
        'coherence_final': coh_final,
        'coherence_ratio': coh_final / coh_initial if coh_initial > 1e-15 else 0.0,
        'phase_initial': phase_initial,
        'phase_final': phase_final,
        'total_phase_diff': total_phase,
        'fidelity': fidelity,
        'rho_final': rho_final.full().tolist(),
    }


def berry_phase_by_comparison(theta, gamma, n_points=200, B=1.0):
    """
    Extract geometric phase by comparing:
    1. Evolution WITH rotating field (accumulates dynamic + geometric phase)
    2. Evolution with STATIC field (accumulates only dynamic phase)

    Geometric phase = difference
    """
    T_total = 200.0 / B
    tlist = np.linspace(0, T_total, n_points + 1)

    sx = qt.sigmax()
    sy = qt.sigmay()
    sz = qt.sigmaz()

    omega_drive = 2 * np.pi / T_total

    # Initial state: ground state at phi=0
    psi0 = ground_state_spin_half(theta, 0.0)
    rho0 = qt.ket2dm(psi0)

    c_ops = [np.sqrt(gamma) * sz] if gamma > 1e-12 else []

    # Evolution 1: ROTATING field (loop in parameter space)
    H_rot = [B * np.cos(theta) * sz,
             [sx, f'{B * np.sin(theta)} * np.cos({omega_drive} * t)'],
             [sy, f'{B * np.sin(theta)} * np.sin({omega_drive} * t)']]

    result_rot = qt.mesolve(H_rot, rho0, tlist, c_ops, [])
    rho_rot = result_rot.states[-1]

    # Evolution 2: STATIC field (no loop, same H as t=0)
    H_static = B * np.sin(theta) * sx + B * np.cos(theta) * sz

    result_static = qt.mesolve(H_static, rho0, tlist, c_ops, [])
    rho_static = result_static.states[-1]

    # Compare off-diagonal phases
    rho01_rot = complex(rho_rot.full()[0, 1])
    rho01_static = complex(rho_static.full()[0, 1])

    coh_rot = abs(rho01_rot)
    coh_static = abs(rho01_static)

    # The DIFFERENCE in phase between rotating and static = geometric phase
    if coh_rot > 1e-10 and coh_static > 1e-10:
        phase_rot = np.angle(rho01_rot)
        phase_static = np.angle(rho01_static)
        geometric_phase = phase_rot - phase_static

        # Normalize to [-pi, pi]
        geometric_phase = (geometric_phase + np.pi) % (2 * np.pi) - np.pi

        measurable = True
    else:
        geometric_phase = 0.0
        measurable = False

    return {
        'geometric_phase_rad': geometric_phase,
        'geometric_phase_pi': geometric_phase / np.pi if measurable else float('nan'),
        'coherence_rotating': coh_rot,
        'coherence_static': coh_static,
        'measurable': measurable,
        'analytic_berry_pi': -(1 - np.cos(theta)),
    }


# Test at theta = pi/2 (where Berry phase = -pi) with varying gamma
print("\n--- Fixed theta = pi/2, varying dephasing gamma ---")
print("    Analytic Berry phase at theta=pi/2: -1.0 * pi\n")

GAMMA_C = 0.0622  # From framework
gammas_test = [0, 0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05,
               GAMMA_C * 0.5, GAMMA_C * 0.8, GAMMA_C * 0.9, GAMMA_C,
               GAMMA_C * 1.1, GAMMA_C * 1.5, GAMMA_C * 2.0,
               0.1, 0.2, 0.5, 1.0]

dephasing_results = []

print(f"  {'gamma':>8s} | {'gamma/gc':>8s} | {'Geo Phase (pi)':>14s} | "
      f"{'Coh_rot':>8s} | {'Coh_static':>10s} | {'Measurable':>10s}")
print("-" * 75)

for gamma in gammas_test:
    res = berry_phase_by_comparison(np.pi / 2, gamma, n_points=300, B=1.0)

    phase_str = f"{res['geometric_phase_pi']:+.6f}" if res['measurable'] else "     ---"

    print(f"  {gamma:8.4f} | {gamma/GAMMA_C:8.4f} | {phase_str:>14s} | "
          f"{res['coherence_rotating']:8.6f} | {res['coherence_static']:10.6f} | "
          f"{str(res['measurable']):>10s}")

    dephasing_results.append({
        'gamma': gamma,
        'gamma_over_gc': gamma / GAMMA_C,
        'geometric_phase_pi': res['geometric_phase_pi'],
        'coherence_rotating': res['coherence_rotating'],
        'coherence_static': res['coherence_static'],
        'measurable': res['measurable'],
    })


# ============================================================
# PART 3: THETA SWEEP at key gamma values
# ============================================================

print("\n" + "=" * 70)
print("  PART 3: THETA SWEEP — Berry phase vs cone angle at different gamma")
print("=" * 70)

theta_sweep = np.linspace(0.1, np.pi - 0.1, 20)
gamma_values = [0, 0.01, GAMMA_C * 0.5, GAMMA_C, GAMMA_C * 2, 0.5]

theta_results = {}

for gamma in gamma_values:
    label = f"gamma={gamma:.4f}"
    print(f"\n  {label} (gamma/gc = {gamma/GAMMA_C:.2f}):")
    theta_results[label] = []

    for theta in theta_sweep:
        res = berry_phase_by_comparison(theta, gamma, n_points=200, B=1.0)
        analytic = -(1 - np.cos(theta))

        theta_results[label].append({
            'theta_deg': float(np.degrees(theta)),
            'geometric_phase_pi': res['geometric_phase_pi'],
            'analytic_pi': analytic,
            'measurable': res['measurable'],
        })

        phase_str = f"{res['geometric_phase_pi']:+.5f}" if res['measurable'] else "  ---"
        print(f"    theta={np.degrees(theta):6.1f} deg | "
              f"Measured: {phase_str:>8s}*pi | "
              f"Analytic: {analytic:+.5f}*pi | "
              f"Coh: {res['coherence_rotating']:.4f}")


# ============================================================
# PART 4: THE CRITICAL TEST — Phase at theta=pi/2 vs gamma
# ============================================================
# Fine sweep of gamma around gamma_c
# Does the Berry phase change at the phase transition?

print("\n" + "=" * 70)
print("  PART 4: FINE gamma SWEEP at theta=pi/2 (Berry = -pi)")
print("  Looking for phase modification at gamma_c")
print("=" * 70)

fine_gammas = np.concatenate([
    np.linspace(0, GAMMA_C * 0.9, 20),
    np.linspace(GAMMA_C * 0.9, GAMMA_C * 1.1, 20),  # Dense near gamma_c
    np.linspace(GAMMA_C * 1.1, GAMMA_C * 5, 20),
])

fine_results = []

print(f"\n  {'gamma':>8s} | {'gamma/gc':>8s} | {'Berry (pi)':>11s} | "
      f"{'Coh_rot':>8s} | {'Status':>12s}")
print("-" * 60)

for gamma in fine_gammas:
    res = berry_phase_by_comparison(np.pi / 2, gamma, n_points=300, B=1.0)

    if res['measurable']:
        phase_str = f"{res['geometric_phase_pi']:+.5f}"
        if abs(res['geometric_phase_pi'] + 1.0) < 0.1:
            status = "BERRY = -pi"
        elif abs(res['geometric_phase_pi']) < 0.1:
            status = "BERRY = 0"
        else:
            status = f"BERRY = {res['geometric_phase_pi']:+.2f}pi"
    else:
        phase_str = "   ---"
        status = "DECOHERENT"

    print(f"  {gamma:8.5f} | {gamma/GAMMA_C:8.4f} | {phase_str:>11s} | "
          f"{res['coherence_rotating']:8.6f} | {status:>12s}")

    fine_results.append({
        'gamma': float(gamma),
        'gamma_over_gc': float(gamma / GAMMA_C),
        'berry_pi': res['geometric_phase_pi'],
        'coherence': res['coherence_rotating'],
        'measurable': res['measurable'],
    })


# ============================================================
# VERDICT
# ============================================================

print("\n" + "=" * 70)
print("  VERDICT")
print("=" * 70)

# Check if Berry phase survives at gamma < gamma_c
surviving = [r for r in fine_results if r['measurable'] and r['gamma'] < GAMMA_C]
dead = [r for r in fine_results if not r['measurable'] or r['gamma'] > GAMMA_C * 3]

if surviving:
    mean_surviving = np.nanmean([r['berry_pi'] for r in surviving if not np.isnan(r['berry_pi'])])
    print(f"\n  Below gamma_c: Berry phase = {mean_surviving:+.4f} * pi")
    print(f"  (Analytic prediction: -1.0000 * pi)")

    if abs(mean_surviving + 1.0) < 0.15:
        print(f"\n  *** BERRY PHASE SURVIVES BELOW gamma_c ***")
        print(f"  *** Geometric phase -pi persists in the coherent regime ***")
    else:
        print(f"\n  Berry phase modified by dephasing: {mean_surviving:+.4f}*pi vs -1.0*pi")

# Check transition
transition_region = [r for r in fine_results
                     if r['measurable'] and
                     GAMMA_C * 0.8 < r['gamma'] < GAMMA_C * 1.2]
if transition_region:
    phases_at_gc = [r['berry_pi'] for r in transition_region if not np.isnan(r['berry_pi'])]
    if phases_at_gc:
        print(f"\n  At gamma_c: Berry phase = {np.mean(phases_at_gc):+.4f} * pi")

# Check if phase is destroyed above gamma_c
above_gc = [r for r in fine_results if r['gamma'] > GAMMA_C * 2]
measurable_above = [r for r in above_gc if r['measurable']]
if above_gc:
    if not measurable_above:
        print(f"\n  Above 2*gamma_c: Coherence destroyed, Berry phase unmeasurable")
        print(f"  *** GEOMETRIC PHASE DESTROYED BY DECOHERENCE ***")
    else:
        phases_above = [r['berry_pi'] for r in measurable_above if not np.isnan(r['berry_pi'])]
        if phases_above:
            print(f"\n  Above 2*gamma_c: Berry phase = {np.mean(phases_above):+.4f} * pi")

# Final determination
print(f"\n  THE QUESTION: Does gamma_c mark a topological phase transition?")

# Save everything
all_results = {
    'metadata': {
        'date': datetime.now().isoformat(),
        'qutip_version': qt.__version__,
        'gamma_c': GAMMA_C,
        'version': 'v2_fixed',
    },
    'control_pure_state': control_results,
    'dephasing_sweep': dephasing_results,
    'fine_gamma_sweep': fine_results,
}

with open('/home/buddy_ai/Desktop/RESULTS_BERRY_PHASE_v2.json', 'w') as f:
    json.dump(all_results, f, indent=2, default=str)

print(f"\n  Results saved to RESULTS_BERRY_PHASE_v2.json")
print("=" * 70)
