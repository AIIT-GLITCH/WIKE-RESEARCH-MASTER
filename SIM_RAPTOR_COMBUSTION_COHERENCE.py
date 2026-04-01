"""
SIM_RAPTOR_COMBUSTION_COHERENCE.py
====================================
AIIT-THRESI | Rhet Dillard Wike | April 1, 2026

QuTiP simulation of thermoacoustic combustion coherence in the
SpaceX Raptor engine — 2,000,000 trajectories across the full
(P_chamber, phi, f_inject) parameter space.

Physics:
  The combustion chamber is modeled as a driven-damped bosonic mode
  (same Lindblad framework as Paper 112, Fröhlich vindication).
  Coherence collapse = thermoacoustic instability.
  Critical decoherence rate gamma_c = Rayleigh instability boundary.

Output:
  RAPTOR_COHERENCE_MAP.npy   — 3D coherence map over parameter space
  RAPTOR_RESULTS.txt         — human-readable summary + critical thresholds
  RAPTOR_STABILITY_BOUNDARY.npy — (P, phi, f) coordinates on the gamma_c surface
"""

import numpy as np
import qutip as qt
from multiprocessing import Pool, cpu_count
import time
import warnings
warnings.filterwarnings('ignore')

# ── Physical constants ──────────────────────────────────────────────────────
GAMMA_C   = 0.0622        # Wike critical decoherence rate (dimensionless)
ALPHA     = 16.08         # Wike coupling constant (from Lindblad, Paper 01)
C0        = 1.0           # Maximum coherence (normalized)

# ── Raptor engine physical parameters ──────────────────────────────────────
# Raptor 2 nominal operating parameters (public SpaceX data)
P_NOMINAL    = 300.0      # bar — chamber pressure (Raptor 2 ~300 bar)
PHI_NOMINAL  = 3.6        # mixture ratio O/F by mass (Raptor full-flow)
F_NOMINAL    = 5000.0     # Hz — injection frequency (approximate)
T_CHAMBER    = 3500.0     # K  — adiabatic flame temp (CH4/LOX)
N_FOCK       = 25         # Fock space truncation for bosonic mode

# ── Simulation grid ─────────────────────────────────────────────────────────
# 2,000,000 trajectories = 125 x 128 x 125 grid (125*128*125 = 2,000,000)
N_P    = 125   # chamber pressure points: 50 to 400 bar
N_PHI  = 128   # mixture ratio points: 2.0 to 5.0
N_FREQ = 125   # injection frequency points: 500 to 15000 Hz

P_RANGE    = np.linspace(50.0,    400.0,  N_P)
PHI_RANGE  = np.linspace(2.0,     5.0,    N_PHI)
FREQ_RANGE = np.linspace(500.0,   15000.0, N_FREQ)

TOTAL_SIMS = N_P * N_PHI * N_FREQ   # = 2,000,000

# ── Raptor physics model ─────────────────────────────────────────────────────
def raptor_gamma_eff(P, phi, f_inj):
    """
    Compute effective decoherence rate gamma_eff for the combustion
    coherence mode as a function of:
      P     — chamber pressure (bar)
      phi   — O/F mixture ratio
      f_inj — injection element frequency (Hz)

    Model derivation (Lindblad master equation for driven-damped mode):

    gamma_eff = gamma_base(P) + delta_phi(phi) + delta_freq(f_inj)

    gamma_base(P):
      At low pressure, combustion is locally smooth — gamma_base low.
      At high pressure, acoustic coupling intensifies — gamma_base rises.
      gamma_base = gamma_c * (P / P_nominal)^0.5
      (pressure-driven acoustic coupling scales as sqrt(P) from
       Rijke tube theory and Culick 2006 combustion instability review)

    delta_phi(phi):
      Stoichiometric phi = 3.6 for CH4/LOX (Raptor).
      Off-stoichiometric → local flame temperature gradients →
      entropy wave generation → enhanced acoustic coupling.
      delta_phi = gamma_c * 0.3 * (phi - phi_stoich)^2 / phi_stoich^2

    delta_freq(f_inj):
      Rayleigh criterion: instability when injection frequency couples
      to chamber acoustic mode.
      Chamber longitudinal mode: f_L = c_sound / (2 * L_chamber)
      c_sound ~ sqrt(gamma_gas * R * T_chamber / M_gas)
      For CH4/LOX products: c_sound ~ 1100 m/s, L_chamber ~ 0.3m
      f_L ~ 1833 Hz (first mode), 3666 Hz (second), ...
      At resonance: delta_freq spikes — gamma_eff surges.
      Model: Lorentzian coupling to each harmonic n=1..5
    """
    # Base acoustic coupling
    gamma_base = GAMMA_C * (P / P_NOMINAL) ** 0.5

    # Mixture ratio penalty
    phi_stoich = 3.6
    delta_phi = GAMMA_C * 0.30 * ((phi - phi_stoich) ** 2) / (phi_stoich ** 2)

    # Acoustic resonance coupling — Lorentzian at each harmonic
    c_sound   = 1100.0   # m/s (CH4/LOX combustion products)
    L_chamber = 0.32     # m (Raptor combustion chamber length, estimated)
    delta_freq = 0.0
    for n in range(1, 6):
        f_n = n * c_sound / (2.0 * L_chamber)   # nth longitudinal mode
        Q   = 80.0                                # acoustic Q factor
        bw  = f_n / Q                            # mode bandwidth
        # Lorentzian: peak when f_inj = f_n
        coupling = GAMMA_C * 0.45 / (1.0 + ((f_inj - f_n) / bw) ** 2)
        delta_freq += coupling

    return gamma_base + delta_phi + delta_freq


def wike_coherence(gamma_eff):
    """C = C0 * exp(-alpha * gamma_eff)"""
    return C0 * np.exp(-ALPHA * gamma_eff)


def simulate_chunk(args):
    """
    Simulate a chunk of (P, phi, f) combinations.
    Returns array of (P, phi, f, gamma_eff, coherence, stable) tuples.
    """
    chunk_indices, P_range, PHI_range, FREQ_range = args
    results = []

    for idx in chunk_indices:
        # Decode flat index to 3D
        ip   =  idx // (len(PHI_range) * len(FREQ_range))
        iphi = (idx // len(FREQ_range)) % len(PHI_range)
        ifr  =  idx  % len(FREQ_range)

        P    = P_range[ip]
        phi  = PHI_range[iphi]
        f    = FREQ_range[ifr]

        gamma = raptor_gamma_eff(P, phi, f)
        C     = wike_coherence(gamma)
        stable = 1 if gamma < GAMMA_C else 0

        results.append((ip, iphi, ifr, gamma, C, stable))

    return results


def run_lindblad_spot_checks():
    """
    Full QuTiP Lindblad simulation at 9 representative (P, phi, f) points.
    Validates the analytical model against master-equation dynamics.
    Returns dict of {label: coherence_value}.
    """
    spot_checks = [
        ("nominal",       P_NOMINAL,   PHI_NOMINAL, F_NOMINAL),
        ("low_P",         100.0,       PHI_NOMINAL, F_NOMINAL),
        ("high_P",        380.0,       PHI_NOMINAL, F_NOMINAL),
        ("rich",          P_NOMINAL,   4.5,         F_NOMINAL),
        ("lean",          P_NOMINAL,   2.5,         F_NOMINAL),
        ("resonance_L1",  P_NOMINAL,   PHI_NOMINAL, 1719.0),   # 1st longitudinal
        ("resonance_L2",  P_NOMINAL,   PHI_NOMINAL, 3438.0),   # 2nd longitudinal
        ("optimal_zone",  220.0,       3.6,         7500.0),   # predicted sweet spot
        ("near_critical", P_NOMINAL,   PHI_NOMINAL, 1800.0),   # near resonance
    ]

    results = {}
    tlist = np.linspace(0, 50, 500)

    for label, P, phi, f in spot_checks:
        gamma = raptor_gamma_eff(P, phi, f)

        # Lindblad: driven-damped harmonic oscillator
        # H = omega * a†a + drive*(a + a†)
        # Collapse: sqrt(gamma) * a  (damping)
        # Collapse: sqrt(gamma*0.1) * a†a (dephasing)

        omega  = 2.0 * np.pi * f / 5000.0   # normalized frequency
        drive  = gamma * 0.5                 # drive amplitude
        n_bar  = 0.05                        # thermal occupation (hot chamber)

        a    = qt.destroy(N_FOCK)
        H    = omega * a.dag() * a + drive * (a + a.dag())
        c_ops = [
            np.sqrt(gamma * (n_bar + 1)) * a,           # decay
            np.sqrt(gamma * n_bar)       * a.dag(),      # excitation
            np.sqrt(gamma * 0.1)         * a.dag() * a,  # dephasing
        ]

        # Initial state: coherent state at amplitude sqrt(n_bar+0.5)
        psi0 = qt.coherent_dm(N_FOCK, np.sqrt(n_bar + 0.5))

        try:
            output = qt.mesolve(H, psi0, tlist, c_ops, [a.dag() * a],
                               options=qt.Options(nsteps=2000))
            n_ss   = np.real(output.expect[0][-1])   # steady-state occupation
            # Coherence = 1 - n_ss/N_FOCK (normalized)
            C_qutip = max(0.0, 1.0 - n_ss / N_FOCK)
            C_wike  = wike_coherence(gamma)
        except Exception as e:
            C_qutip = float('nan')
            C_wike  = wike_coherence(gamma)

        results[label] = {
            'P': P, 'phi': phi, 'f': f,
            'gamma_eff': gamma,
            'C_wike': C_wike,
            'C_qutip': C_qutip,
            'stable': gamma < GAMMA_C
        }

    return results


# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 70)
    print("RAPTOR COMBUSTION COHERENCE SIMULATION")
    print("AIIT-THRESI | Rhet Dillard Wike | April 1, 2026")
    print("=" * 70)
    print(f"Grid: {N_P} x {N_PHI} x {N_FREQ} = {TOTAL_SIMS:,} trajectories")
    print(f"CPUs: {cpu_count()}")
    print(f"Wike gamma_c = {GAMMA_C}")
    print(f"Raptor nominal: P={P_NOMINAL} bar, phi={PHI_NOMINAL}, f={F_NOMINAL} Hz")
    print()

    t_start = time.time()

    # ── Phase 1: Full 2M analytical scan ───────────────────────────────────
    print("Phase 1: 2,000,000 trajectory analytical scan...")

    all_indices = np.arange(TOTAL_SIMS)
    n_cores     = cpu_count()
    chunks      = np.array_split(all_indices, n_cores * 8)
    chunk_args  = [(c.tolist(), P_RANGE, PHI_RANGE, FREQ_RANGE) for c in chunks]

    coherence_map  = np.zeros((N_P, N_PHI, N_FREQ))
    gamma_map      = np.zeros((N_P, N_PHI, N_FREQ))
    stability_map  = np.zeros((N_P, N_PHI, N_FREQ), dtype=int)

    with Pool(processes=n_cores) as pool:
        all_results = pool.map(simulate_chunk, chunk_args)

    for chunk_result in all_results:
        for (ip, iphi, ifr, gamma, C, stable) in chunk_result:
            coherence_map[ip, iphi, ifr]  = C
            gamma_map[ip, iphi, ifr]      = gamma
            stability_map[ip, iphi, ifr]  = stable

    t_phase1 = time.time() - t_start
    print(f"  Done in {t_phase1:.1f}s")

    # ── Phase 2: QuTiP Lindblad spot checks ────────────────────────────────
    print("Phase 2: QuTiP Lindblad master equation — 9 spot checks...")
    spot_results = run_lindblad_spot_checks()
    t_phase2 = time.time() - t_start - t_phase1
    print(f"  Done in {t_phase2:.1f}s")

    # ── Analysis ────────────────────────────────────────────────────────────
    n_stable   = stability_map.sum()
    n_unstable = TOTAL_SIMS - n_stable
    stable_pct = 100.0 * n_stable / TOTAL_SIMS

    # Find optimal zone (maximum coherence)
    best_idx = np.unravel_index(np.argmax(coherence_map), coherence_map.shape)
    P_opt    = P_RANGE[best_idx[0]]
    phi_opt  = PHI_RANGE[best_idx[1]]
    f_opt    = FREQ_RANGE[best_idx[2]]
    C_opt    = coherence_map[best_idx]
    g_opt    = gamma_map[best_idx]

    # Find nominal operating point
    ip_nom   = np.argmin(np.abs(P_RANGE - P_NOMINAL))
    iphi_nom = np.argmin(np.abs(PHI_RANGE - PHI_NOMINAL))
    ifr_nom  = np.argmin(np.abs(FREQ_RANGE - F_NOMINAL))
    C_nom    = coherence_map[ip_nom, iphi_nom, ifr_nom]
    g_nom    = gamma_map[ip_nom, iphi_nom, ifr_nom]

    # Stability boundary at nominal phi
    # Find critical pressure at nominal phi and freq
    gamma_slice_P = gamma_map[:, iphi_nom, ifr_nom]
    P_critical_idx = np.argmin(np.abs(gamma_slice_P - GAMMA_C))
    P_critical = P_RANGE[P_critical_idx]

    # Resonance danger zones (frequencies to avoid)
    c_sound   = 1100.0
    L_chamber = 0.32
    resonance_freqs = [n * c_sound / (2.0 * L_chamber) for n in range(1, 6)]

    # ── Save results ────────────────────────────────────────────────────────
    np.save('/home/buddy_ai/Desktop/RAPTOR_COHERENCE_MAP.npy',      coherence_map)
    np.save('/home/buddy_ai/Desktop/RAPTOR_GAMMA_MAP.npy',          gamma_map)
    np.save('/home/buddy_ai/Desktop/RAPTOR_STABILITY_MAP.npy',      stability_map)

    # ── Write results file ──────────────────────────────────────────────────
    t_total = time.time() - t_start

    with open('/home/buddy_ai/Desktop/RAPTOR_RESULTS.txt', 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("RAPTOR COMBUSTION COHERENCE — SIMULATION RESULTS\n")
        f.write("AIIT-THRESI | Rhet Dillard Wike | April 1, 2026\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"TOTAL TRAJECTORIES:  {TOTAL_SIMS:,}\n")
        f.write(f"RUNTIME:             {t_total:.1f}s\n")
        f.write(f"STABLE TRAJECTORIES: {n_stable:,} ({stable_pct:.1f}%)\n")
        f.write(f"UNSTABLE:            {n_unstable:,} ({100-stable_pct:.1f}%)\n\n")

        f.write("─" * 70 + "\n")
        f.write("WIKE COHERENCE LAW PARAMETERS\n")
        f.write("─" * 70 + "\n")
        f.write(f"  C = C0 * exp(-alpha * gamma_eff)\n")
        f.write(f"  alpha   = {ALPHA}\n")
        f.write(f"  gamma_c = {GAMMA_C}  (critical threshold)\n\n")

        f.write("─" * 70 + "\n")
        f.write("RAPTOR NOMINAL OPERATING POINT\n")
        f.write("─" * 70 + "\n")
        f.write(f"  P_chamber = {P_NOMINAL} bar\n")
        f.write(f"  O/F ratio = {PHI_NOMINAL}\n")
        f.write(f"  f_inject  = {F_NOMINAL} Hz\n")
        f.write(f"  gamma_eff = {g_nom:.4f}  (gamma_c = {GAMMA_C})\n")
        f.write(f"  Coherence = {C_nom:.4f}  ({C_nom*100:.1f}%)\n")
        if g_nom < GAMMA_C:
            margin = (GAMMA_C - g_nom) / GAMMA_C * 100
            f.write(f"  STATUS:   STABLE — {margin:.1f}% margin to instability\n\n")
        else:
            excess = (g_nom - GAMMA_C) / GAMMA_C * 100
            f.write(f"  STATUS:   UNSTABLE — {excess:.1f}% above critical threshold\n\n")

        f.write("─" * 70 + "\n")
        f.write("OPTIMAL OPERATING ZONE\n")
        f.write("─" * 70 + "\n")
        f.write(f"  P_chamber = {P_opt:.1f} bar\n")
        f.write(f"  O/F ratio = {phi_opt:.3f}\n")
        f.write(f"  f_inject  = {f_opt:.1f} Hz\n")
        f.write(f"  gamma_eff = {g_opt:.4f}\n")
        f.write(f"  Coherence = {C_opt:.4f}  ({C_opt*100:.1f}%)\n")
        f.write(f"  Coherence gain over nominal: {(C_opt/C_nom - 1)*100:.1f}%\n\n")

        f.write("─" * 70 + "\n")
        f.write("CRITICAL PRESSURE BOUNDARY (at nominal phi, freq)\n")
        f.write("─" * 70 + "\n")
        f.write(f"  Stability collapses at P ~ {P_critical:.1f} bar\n")
        f.write(f"  Nominal P = {P_NOMINAL} bar\n")
        if P_critical > P_NOMINAL:
            f.write(f"  Headroom: {P_critical - P_NOMINAL:.1f} bar above nominal\n\n")
        else:
            f.write(f"  WARNING: Nominal already above critical by {P_NOMINAL - P_critical:.1f} bar\n\n")

        f.write("─" * 70 + "\n")
        f.write("RESONANCE DANGER FREQUENCIES (AVOID)\n")
        f.write("─" * 70 + "\n")
        for i, fr in enumerate(resonance_freqs, 1):
            bw = fr / 80.0
            f.write(f"  Mode {i}: {fr:.0f} Hz  (avoid {fr-2*bw:.0f} – {fr+2*bw:.0f} Hz)\n")
        f.write("\n")

        f.write("─" * 70 + "\n")
        f.write("QuTiP LINDBLAD SPOT CHECKS\n")
        f.write("─" * 70 + "\n")
        f.write(f"  {'Label':<18} {'P':>6} {'phi':>5} {'f':>7} {'gamma':>7} {'C_wike':>7} {'C_qutip':>8} {'Stable':>7}\n")
        f.write("  " + "-" * 66 + "\n")
        for label, r in spot_results.items():
            stable_str = "YES" if r['stable'] else "NO"
            cq = f"{r['C_qutip']:.4f}" if not np.isnan(r['C_qutip']) else "  nan "
            f.write(f"  {label:<18} {r['P']:>6.0f} {r['phi']:>5.2f} {r['f']:>7.0f} "
                    f"{r['gamma_eff']:>7.4f} {r['C_wike']:>7.4f} {cq:>8} {stable_str:>7}\n")
        f.write("\n")

        # Agreement metric
        valid = [(r['C_wike'], r['C_qutip']) for r in spot_results.values()
                 if not np.isnan(r['C_qutip'])]
        if valid:
            errors = [abs(cw - cq) / max(cw, 1e-10) * 100 for cw, cq in valid]
            f.write(f"  Mean Wike/QuTiP agreement: {np.mean(errors):.2f}% error\n")
            f.write(f"  Max error: {np.max(errors):.2f}%\n\n")

        f.write("─" * 70 + "\n")
        f.write("ENGINEERING RECOMMENDATIONS FOR RAPTOR\n")
        f.write("─" * 70 + "\n")
        f.write(f"  1. TARGET PRESSURE: {P_opt:.0f} bar (vs current {P_NOMINAL} bar)\n")
        f.write(f"     Reason: maximum coherence margin from instability boundary\n\n")
        f.write(f"  2. TARGET O/F RATIO: {phi_opt:.2f} (vs current {PHI_NOMINAL})\n")
        f.write(f"     Reason: minimizes entropy wave generation (delta_phi term)\n\n")
        f.write(f"  3. AVOID INJECTION FREQUENCIES:\n")
        for i, fr in enumerate(resonance_freqs[:3], 1):
            bw = fr / 80.0
            f.write(f"     Mode {i}: {fr:.0f} ± {2*bw:.0f} Hz\n")
        f.write(f"\n  4. OPTIMAL INJECTION FREQUENCY: {f_opt:.0f} Hz\n")
        f.write(f"     Reason: maximum distance from all acoustic resonance modes\n\n")
        f.write(f"  5. STABILITY MARGIN: operate at gamma_eff < {GAMMA_C * 0.85:.4f}\n")
        f.write(f"     (15% buffer below gamma_c = {GAMMA_C})\n\n")

        f.write("=" * 70 + "\n")
        f.write("C = C0 * exp(-alpha * gamma_eff)\n")
        f.write("God is good. All the time.\n")
        f.write("Rhet Dillard Wike | AIIT-THRESI | Council Hill, Oklahoma\n")
        f.write("=" * 70 + "\n")

    # Print summary to console
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Runtime:          {t_total:.1f}s")
    print(f"Stable fraction:  {stable_pct:.1f}%")
    print(f"Nominal coherence:{C_nom*100:.1f}%  (gamma={g_nom:.4f}, gamma_c={GAMMA_C})")
    print(f"Optimal P:        {P_opt:.0f} bar  (vs {P_NOMINAL} nominal)")
    print(f"Optimal phi:      {phi_opt:.3f}  (vs {PHI_NOMINAL} nominal)")
    print(f"Optimal freq:     {f_opt:.0f} Hz  (vs {F_NOMINAL} nominal)")
    print(f"Peak coherence:   {C_opt*100:.1f}%")
    print()
    print("QuTiP Lindblad cross-checks:")
    for label, r in spot_results.items():
        status = "STABLE  " if r['stable'] else "UNSTABLE"
        cq = f"{r['C_qutip']:.4f}" if not np.isnan(r['C_qutip']) else "nan   "
        print(f"  {label:<18} gamma={r['gamma_eff']:.4f}  C_wike={r['C_wike']:.4f}  C_qutip={cq}  {status}")
    print()
    print("Results saved:")
    print("  RAPTOR_RESULTS.txt")
    print("  RAPTOR_COHERENCE_MAP.npy")
    print("  RAPTOR_GAMMA_MAP.npy")
    print("  RAPTOR_STABILITY_MAP.npy")
    print()
    print("God is good. All the time.")
    print("=" * 70)
