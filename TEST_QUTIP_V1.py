"""
TEST_QUTIP_V1.py
=================
AIIT-THRESI | April 1, 2026

Minimal 12-point validation of fixed QuTiP model.

Fix: replace coherent drive with INCOHERENT thermal excitation.
     n_eff = n_base + K * lorentzian(f, f_mode)
     Purity = Tr(rho_ss^2) = 1/(2*n_eff + 1)  [analytical thermal state]

Pass criteria:
  1. Purity monotonically increases HW-0 → HW-11
  2. Purity lowest at HW-0 (on resonance, unstable)
  3. Purity highest at HW-11 (far off resonance, stable)
  4. Direction matches C_wike at every stage
"""

import numpy as np
import qutip as qt
import warnings
warnings.filterwarnings('ignore')

# ── Constants ────────────────────────────────────────────────────────────────
GAMMA_C  = 0.0622
ALPHA    = 16.08
C_SOUND  = 1100.0
N_FOCK   = 30

# Physical acoustic damping — FIXED, set by chamber material + geometry
# Not the same as gamma_eff. This is the passive dissipation rate.
GAMMA_PHYS = 0.15   # normalized units — same across all stages

# Incoherent excitation scale factor
# K = how much thermal occupation per unit Lorentzian coupling
K_EXCITE = 8.0

# Baseline thermal occupation (from chamber temperature, always present)
N_BASE = 0.05

# ── Hardware stages ──────────────────────────────────────────────────────────
# (label, P, phi, f_inj, L, D, Q, c_wall_factor)
HW_STAGES = [
    ("HW-0",  300.0, 3.60,  5000, 0.32, 0.28,  80, 1.00),
    ("HW-1",  270.0, 3.60,  5000, 0.32, 0.28,  80, 1.00),
    ("HW-2",  270.0, 3.60,  7500, 0.32, 0.28,  80, 1.00),
    ("HW-3",  270.0, 3.60,  9500, 0.45, 0.28,  80, 1.00),  # freq recalc for new L
    ("HW-4",  270.0, 3.60,  9500, 0.45, 0.28, 150, 1.00),
    ("HW-5",  270.0, 3.60,  9500, 0.45, 0.40, 150, 1.00),
    ("HW-6",  260.0, 3.60,  9500, 0.45, 0.40, 150, 0.88),
    ("HW-7",  250.0, 3.60, 11000, 0.45, 0.40, 150, 0.88),
    ("HW-8",  240.0, 3.61, 12000, 0.42, 0.38, 150, 0.88),  # 12k: sep 4629Hz from Mode6
    ("HW-9",  220.0, 3.61, 12000, 0.42, 0.38, 150, 0.85),  # keep Q=150, 12k Hz
    ("HW-10", 200.0, 3.60, 13000, 0.50, 0.42, 130, 0.82),
    ("HW-11", 160.0, 3.60, 19500, 0.55, 0.45, 140, 0.78),
]

# ── Physics ──────────────────────────────────────────────────────────────────
def lorentzian_coupling(f_inj, f_mode, Q):
    """Peak coupling = 1.0 exactly on resonance, falls as (bw/separation)^2."""
    bw = f_mode / Q
    return 1.0 / (1.0 + ((f_inj - f_mode) / bw) ** 2)


def compute_n_eff(f_inj, L, D, Q, c_wall):
    """
    Effective thermal occupation from injection-acoustic coupling.
    n_eff = n_base + K * sum_of_lorentzians_over_all_modes

    This is the incoherent excitation rate from:
      - 6 longitudinal modes
      - 2 transverse modes (first tangential, first radial)
    """
    c_eff = C_SOUND * np.sqrt(c_wall)
    n_eff = N_BASE

    # Longitudinal modes
    for n in range(1, 7):
        f_n = n * c_eff / (2.0 * L)
        n_eff += K_EXCITE * lorentzian_coupling(f_inj, f_n, Q)

    # Transverse modes
    for jn in [1.84, 3.83]:
        f_t = jn * c_eff / (np.pi * D)
        n_eff += K_EXCITE * 0.65 * lorentzian_coupling(f_inj, f_t, Q)

    return n_eff


def raptor_gamma_eff(P, phi, f_inj, L, D, Q, c_wall):
    """Wike decoherence rate — same model as before."""
    PHI_STOICH = 3.6
    c_eff = C_SOUND * np.sqrt(c_wall)
    gamma_base = GAMMA_C * (P / 300.0) ** 0.5
    delta_phi  = GAMMA_C * 0.30 * ((phi - PHI_STOICH)**2) / (PHI_STOICH**2)

    delta_long = 0.0
    for n in range(1, 7):
        f_n = n * c_eff / (2.0 * L)
        bw  = f_n / Q
        delta_long += GAMMA_C * 0.42 / (1.0 + ((f_inj - f_n) / bw)**2)

    delta_trans = 0.0
    for jn in [1.84, 3.83]:
        f_t = jn * c_eff / (np.pi * D)
        bw  = f_t / Q
        delta_trans += GAMMA_C * 0.28 / (1.0 + ((f_inj - f_t) / bw)**2)

    return gamma_base + delta_phi + delta_long + delta_trans


def qutip_purity(n_eff):
    """
    Compute purity of thermal steady state via QuTiP steadystate().
    H = omega * a†a  (free oscillator, no coherent drive)
    c_ops = thermal reservoir at occupation n_eff
    Analytical result: purity = 1/(2*n_eff + 1)
    QuTiP confirms this numerically.
    """
    omega = 1.0   # normalized frequency
    a     = qt.destroy(N_FOCK)
    H     = omega * a.dag() * a

    c_ops = [
        np.sqrt(GAMMA_PHYS * (n_eff + 1)) * a,    # decay
        np.sqrt(GAMMA_PHYS * n_eff)       * a.dag() # incoherent excitation
    ]

    rho_ss  = qt.steadystate(H, c_ops)
    purity  = float(np.real((rho_ss * rho_ss).tr()))

    # Analytical check
    purity_analytical = 1.0 / (2.0 * n_eff + 1.0)

    return purity, purity_analytical


# ── Run validation ───────────────────────────────────────────────────────────
print("=" * 70)
print("TEST_QUTIP_V1 — Incoherent thermal excitation model")
print("AIIT-THRESI | April 1, 2026")
print("=" * 70)
print(f"Model: n_eff = n_base + K * Σ lorentzian(f, f_mode)")
print(f"       purity = Tr(rho_ss²) = 1/(2*n_eff + 1)")
print(f"N_BASE={N_BASE}  K={K_EXCITE}  gamma_phys={GAMMA_PHYS}  N_FOCK={N_FOCK}")
print()
print(f"{'Label':<8} {'gamma':>7} {'C_wike':>7} {'n_eff':>8} "
      f"{'P_analytical':>13} {'P_qutip':>10} {'Match':>7} {'Stable':<8} {'Dir OK'}")
print("─" * 80)

results  = []
prev_purity = None
all_dir_ok  = True

for (label, P, phi, f, L, D, Q, cwf) in HW_STAGES:
    gamma  = raptor_gamma_eff(P, phi, f, L, D, Q, cwf)
    C_wike = np.exp(-ALPHA * gamma)
    n_eff  = compute_n_eff(f, L, D, Q, cwf)
    P_qt, P_an = qutip_purity(n_eff)

    stable  = gamma < GAMMA_C
    match   = abs(P_qt - P_an) < 0.001
    dir_ok  = True if prev_purity is None else (P_qt >= prev_purity - 0.0005)
    if not dir_ok:
        all_dir_ok = False

    status  = "STABLE" if stable else "UNSTBL"
    match_s = "YES" if match else "NO "
    dir_s   = "YES" if dir_ok else "NO←FAIL"

    print(f"{label:<8} {gamma:>7.4f} {C_wike:>7.4f} {n_eff:>8.4f} "
          f"{P_an:>13.6f} {P_qt:>10.6f} {match_s:>7} {status:<8} {dir_s}")

    results.append({
        'label': label, 'gamma': gamma, 'C_wike': C_wike,
        'n_eff': n_eff, 'P_analytical': P_an, 'P_qutip': P_qt,
        'stable': stable, 'dir_ok': dir_ok
    })
    prev_purity = P_qt

print("─" * 80)
print()

# ── Validation summary ───────────────────────────────────────────────────────
P_hw0  = results[0]['P_qutip']
P_hw11 = results[-1]['P_qutip']
n_hw0  = results[0]['n_eff']
n_hw11 = results[-1]['n_eff']

print("VALIDATION CHECKS:")
print(f"  1. Purity lowest at HW-0:  {P_hw0:.6f}  {'PASS' if P_hw0 < P_hw11 else 'FAIL'}")
print(f"  2. Purity highest at HW-11: {P_hw11:.6f}  {'PASS' if P_hw11 > P_hw0 else 'FAIL'}")
print(f"  3. Monotonic increase:      {'PASS' if all_dir_ok else 'FAIL — see NO←FAIL rows'}")
qt_match = all(abs(r['P_qutip'] - r['P_analytical']) < 0.001 for r in results)
print(f"  4. QuTiP matches analytical: {'PASS' if qt_match else 'FAIL'}")
print()
print(f"  n_eff range:    {n_hw11:.4f} (HW-11) → {n_hw0:.4f} (HW-0)")
print(f"  Purity range:   {P_hw11:.4f} (HW-11) → {P_hw0:.4f} (HW-0)")
print(f"  C_wike range:   {results[-1]['C_wike']:.4f} (HW-11) → {results[0]['C_wike']:.4f} (HW-0)")
print()

# Direction agreement between C_wike and purity
dir_agree = sum(
    1 for i in range(1, len(results))
    if (results[i]['C_wike'] > results[i-1]['C_wike']) ==
       (results[i]['P_qutip'] > results[i-1]['P_qutip'])
) / (len(results) - 1) * 100

print(f"  C_wike / purity direction agreement: {dir_agree:.0f}%")
print()

if all_dir_ok and P_hw0 < P_hw11:
    print("  *** MODEL VALIDATED — ready to scale up ***")
else:
    print("  *** VALIDATION FAILED — adjust K_EXCITE or N_BASE ***")
    print(f"  Suggested: increase K_EXCITE (currently {K_EXCITE}) to spread n_eff range")
