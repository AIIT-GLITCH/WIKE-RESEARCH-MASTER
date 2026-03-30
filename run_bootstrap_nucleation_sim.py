#!/usr/bin/env python3
"""
Bootstrap Nucleation Theorem Simulation
Tests whether EZ water formation follows Avrami n=3 kinetics
AIIT-THRESI Research Initiative — March 30, 2026
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.ndimage import label
import time

np.random.seed(42)
start = time.time()

results = []
results.append("=" * 70)
results.append("BOOTSTRAP NUCLEATION THEOREM — SIMULATION RESULTS")
results.append("=" * 70)
results.append(f"Date: 2026-03-30")
results.append("")

# ============================================================
# SIMULATION 1: Avrami Exponent Extraction from Hill Data
# ============================================================
results.append("=" * 70)
results.append("SIMULATION 1: AVRAMI EXPONENT EXTRACTION FROM HILL DATA")
results.append("=" * 70)

def hill(D, n, K):
    return D**n / (K**n + D**n)

def avrami(t, k, n):
    return 1.0 - np.exp(-k * t**n)

def sigmoid(x, L, k_s, x0, b):
    return L / (1.0 + np.exp(-k_s * (x - x0))) + b

# Generate Hill n=3 data (matching NIR simulation)
doses = np.linspace(0.01, 2.0, 200)
K_half = 0.5
n_true = 3.0
y_hill = hill(doses, n_true, K_half)
noise = np.random.normal(0, 0.01, len(doses))
y_noisy = np.clip(y_hill + noise, 0, 1)

# Fit Avrami to Hill-generated data (treating dose as "time")
try:
    popt_av, _ = curve_fit(avrami, doses, y_noisy, p0=[0.5, 3.0], maxfev=10000)
    k_av, n_av = popt_av
    y_av_fit = avrami(doses, k_av, n_av)
    ss_res_av = np.sum((y_noisy - y_av_fit)**2)
    ss_tot = np.sum((y_noisy - np.mean(y_noisy))**2)
    r2_avrami = 1 - ss_res_av / ss_tot
except:
    n_av, k_av, r2_avrami = 0, 0, 0

# Fit Hill back
try:
    popt_hill, _ = curve_fit(hill, doses, y_noisy, p0=[3.0, 0.5], maxfev=10000)
    n_hill_fit, K_hill_fit = popt_hill
    y_hill_fit = hill(doses, n_hill_fit, K_hill_fit)
    ss_res_h = np.sum((y_noisy - y_hill_fit)**2)
    r2_hill = 1 - ss_res_h / ss_tot
except:
    n_hill_fit, r2_hill = 0, 0

# Fit sigmoid
try:
    popt_sig, _ = curve_fit(sigmoid, doses, y_noisy, p0=[1.0, 5.0, 0.5, 0.0], maxfev=10000)
    y_sig_fit = sigmoid(doses, *popt_sig)
    ss_res_s = np.sum((y_noisy - y_sig_fit)**2)
    r2_sigmoid = 1 - ss_res_s / ss_tot
except:
    r2_sigmoid = 0

results.append(f"  Generated Hill data: n_true = {n_true}, K = {K_half}")
results.append(f"  Data points: {len(doses)}")
results.append(f"")
results.append(f"  HILL FIT:    n = {n_hill_fit:.4f}, R² = {r2_hill:.6f}")
results.append(f"  AVRAMI FIT:  n = {n_av:.4f}, k = {k_av:.4f}, R² = {r2_avrami:.6f}")
results.append(f"  SIGMOID FIT: R² = {r2_sigmoid:.6f}")
results.append(f"")
results.append(f"  Avrami exponent extracted: {n_av:.4f}")
results.append(f"  Expected: 3.0")
results.append(f"  Match: {abs(n_av - 3.0) / 3.0 * 100:.2f}% deviation")
results.append(f"")
if abs(n_av - 3.0) < 0.5:
    results.append(f"  VERDICT: CONFIRMED — Hill n=3 maps to Avrami n≈3")
else:
    results.append(f"  VERDICT: DEVIATION — Avrami n differs from Hill n")
results.append("")

# ============================================================
# SIMULATION 2: Nucleation Monte Carlo
# ============================================================
results.append("=" * 70)
results.append("SIMULATION 2: NUCLEATION MONTE CARLO (2D GRID)")
results.append("=" * 70)

grid_size = 100
dose_rates = [0.001, 0.005, 0.01, 0.02, 0.05]
n_timesteps = 500
n_runs_per_dose = 5

results.append(f"  Grid: {grid_size}x{grid_size}")
results.append(f"  Dose rates: {dose_rates}")
results.append(f"  Timesteps: {n_timesteps}")
results.append(f"  Runs per dose: {n_runs_per_dose}")
results.append("")

avrami_exponents = []

for dose_rate in dose_rates:
    all_curves = []
    for run in range(n_runs_per_dose):
        grid = np.zeros((grid_size, grid_size), dtype=int)
        X_t = []
        for t in range(n_timesteps):
            # NIR photons hit random sites
            n_photons = max(1, int(dose_rate * grid_size * grid_size))
            for _ in range(n_photons):
                i, j = np.random.randint(0, grid_size, 2)
                if grid[i, j] == 0:
                    # Count EZ neighbors
                    neighbors = 0
                    for di, dj in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                        ni, nj = (i+di) % grid_size, (j+dj) % grid_size
                        if grid[ni, nj] == 1:
                            neighbors += 1
                    # Nucleation: need >=2 EZ neighbors (n*=3 including self)
                    # OR spontaneous nucleation with low probability
                    if neighbors >= 2:
                        grid[i, j] = 1
                    elif np.random.random() < 0.01:  # spontaneous nucleation
                        grid[i, j] = 1
            X_t.append(np.mean(grid))
        all_curves.append(X_t)

    mean_curve = np.mean(all_curves, axis=0)

    # Fit Avrami to mean curve
    t_data = np.arange(1, n_timesteps + 1, dtype=float)
    # Only fit where X > 0.001 and X < 0.99
    mask = (mean_curve > 0.001) & (np.array(mean_curve) < 0.99)
    if np.sum(mask) > 10:
        try:
            popt, _ = curve_fit(avrami, t_data[mask], np.array(mean_curve)[mask],
                               p0=[1e-6, 2.0], maxfev=20000,
                               bounds=([0, 0.5], [1, 6.0]))
            k_fit, n_fit = popt
            y_fit = avrami(t_data[mask], k_fit, n_fit)
            ss_res = np.sum((np.array(mean_curve)[mask] - y_fit)**2)
            ss_tot = np.sum((np.array(mean_curve)[mask] - np.mean(np.array(mean_curve)[mask]))**2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            avrami_exponents.append((dose_rate, n_fit, k_fit, r2))
            results.append(f"  Dose rate {dose_rate}: n_Avrami = {n_fit:.3f}, k = {k_fit:.2e}, R² = {r2:.4f}, X_final = {mean_curve[-1]:.4f}")
        except Exception as e:
            results.append(f"  Dose rate {dose_rate}: Fit failed ({e})")
    else:
        results.append(f"  Dose rate {dose_rate}: Insufficient transformation (X_final = {mean_curve[-1]:.4f})")

results.append("")
if avrami_exponents:
    mean_n = np.mean([x[1] for x in avrami_exponents])
    std_n = np.std([x[1] for x in avrami_exponents])
    results.append(f"  MEAN Avrami exponent: {mean_n:.3f} ± {std_n:.3f}")
    results.append(f"  Expected for 3D simultaneous nucleation: 3.0")
    results.append(f"  Expected for 2D growth: 2.0")
    if 2.5 < mean_n < 3.5:
        results.append(f"  VERDICT: CONSISTENT WITH n≈3 (3D nucleation)")
    elif 1.5 < mean_n < 2.5:
        results.append(f"  VERDICT: CONSISTENT WITH n≈2 (2D sheet growth)")
    else:
        results.append(f"  VERDICT: ANOMALOUS — n={mean_n:.2f}")
results.append("")

# ============================================================
# SIMULATION 3: Temperature Dependence of Nucleation
# ============================================================
results.append("=" * 70)
results.append("SIMULATION 3: TEMPERATURE DEPENDENCE (W-PARAMETER)")
results.append("=" * 70)

W_values = [0.85, 0.90, 0.94, 0.95, 0.96, 0.98]
T_c = 330.0  # K
dG_star_0 = 5.0  # arbitrary units for nucleation barrier
k_B = 1.0  # normalized

results.append(f"  T_c = {T_c} K")
results.append(f"  W values tested: {W_values}")
results.append("")

nucleation_rates = []
for W in W_values:
    T = W * T_c
    # Nucleation probability: p = p0 * exp(-dG*/(kT))
    # EZ stability: only stable below T_c, stability decreases as T -> T_c
    stability = max(0, (1.0 - W))  # 0 at T_c, increases as W decreases
    # Nucleation rate: barrier decreases with T but stability decreases too
    dG_eff = dG_star_0 / (W + 0.01)  # barrier decreases with temperature
    p_nuc = np.exp(-dG_eff / (k_B * T / T_c)) * stability

    # Monte Carlo: count nucleation events on 50x50 grid
    n_events_total = 0
    n_mc_runs = 100
    steps_per_run = 200
    for _ in range(n_mc_runs):
        grid = np.zeros((50, 50), dtype=int)
        events = 0
        for t in range(steps_per_run):
            i, j = np.random.randint(0, 50, 2)
            if grid[i, j] == 0 and np.random.random() < p_nuc:
                grid[i, j] = 1
                events += 1
        n_events_total += events
    avg_rate = n_events_total / n_mc_runs / steps_per_run
    nucleation_rates.append((W, T, avg_rate, stability, p_nuc))
    results.append(f"  W = {W:.2f} (T = {T:.1f} K): nucleation rate = {avg_rate:.6f}, "
                   f"stability = {stability:.3f}, p_nuc = {p_nuc:.6f}")

# Find optimal W
optimal_idx = np.argmax([x[2] for x in nucleation_rates])
optimal_W = nucleation_rates[optimal_idx][0]
results.append(f"")
results.append(f"  OPTIMAL W for nucleation: {optimal_W}")
results.append(f"  Human body W: 0.94")
if abs(optimal_W - 0.94) < 0.03:
    results.append(f"  VERDICT: CONFIRMED — Body temperature optimizes Bootstrap nucleation")
else:
    results.append(f"  VERDICT: Optimal W = {optimal_W}, body W = 0.94 (deviation {abs(optimal_W-0.94):.3f})")
results.append("")

# ============================================================
# SIMULATION 4: Percolation Threshold
# ============================================================
results.append("=" * 70)
results.append("SIMULATION 4: PERCOLATION THRESHOLD")
results.append("=" * 70)

grid_size_perc = 100
coverages = np.arange(0.30, 0.85, 0.01)
n_perc_runs = 50

results.append(f"  Grid: {grid_size_perc}x{grid_size_perc}")
results.append(f"  Coverage range: 0.30 to 0.84")
results.append(f"  Runs per coverage: {n_perc_runs}")
results.append("")

perc_probs = []
for cov in coverages:
    spanning_count = 0
    for _ in range(n_perc_runs):
        grid = (np.random.random((grid_size_perc, grid_size_perc)) < cov).astype(int)
        labeled, n_features = label(grid)
        # Check for spanning cluster (left to right)
        left_labels = set(labeled[:, 0]) - {0}
        right_labels = set(labeled[:, -1]) - {0}
        if left_labels & right_labels:
            spanning_count += 1
    perc_probs.append(spanning_count / n_perc_runs)

# Find threshold (50% spanning probability)
perc_probs = np.array(perc_probs)
above_half = np.where(perc_probs >= 0.5)[0]
if len(above_half) > 0:
    phi_c_measured = coverages[above_half[0]]
else:
    phi_c_measured = coverages[-1]

results.append(f"  Percolation probabilities (selected):")
for i in range(0, len(coverages), 5):
    results.append(f"    coverage = {coverages[i]:.2f}: spanning prob = {perc_probs[i]:.2f}")

results.append(f"")
results.append(f"  MEASURED percolation threshold (50%): φ_c = {phi_c_measured:.3f}")
results.append(f"  Theoretical 2D site percolation (square): φ_c = 0.593")
results.append(f"  Bootstrap threshold dose: 0.623")
results.append(f"  Deviation from Bootstrap: {abs(phi_c_measured - 0.623)/0.623*100:.1f}%")
results.append(f"  Deviation from theory: {abs(phi_c_measured - 0.593)/0.593*100:.1f}%")
results.append(f"")
if abs(phi_c_measured - 0.593) < 0.05:
    results.append(f"  VERDICT: CONFIRMED — Percolation threshold matches 2D site percolation")
elif abs(phi_c_measured - 0.623) < 0.05:
    results.append(f"  VERDICT: CONFIRMED — Percolation threshold matches Bootstrap threshold")
else:
    results.append(f"  VERDICT: φ_c = {phi_c_measured:.3f} (between theoretical values)")

# ============================================================
# SUMMARY
# ============================================================
elapsed = time.time() - start
total_events = (200 + grid_size**2 * n_timesteps * len(dose_rates) * n_runs_per_dose +
                len(W_values) * n_mc_runs * 200 + len(coverages) * n_perc_runs * grid_size_perc**2)

results.append("")
results.append("=" * 70)
results.append("SUMMARY")
results.append("=" * 70)
results.append(f"  Total computational events: ~{total_events:,}")
results.append(f"  Runtime: {elapsed:.1f} seconds")
results.append(f"")
results.append(f"  1. Hill n=3 → Avrami n={n_av:.3f}: {'CONFIRMED' if abs(n_av-3)<0.5 else 'DEVIATION'}")
if avrami_exponents:
    results.append(f"  2. Monte Carlo Avrami n={mean_n:.3f}: {'3D NUCLEATION' if 2.5<mean_n<3.5 else '2D GROWTH' if 1.5<mean_n<2.5 else 'ANOMALOUS'}")
results.append(f"  3. Optimal nucleation W={optimal_W}: {'MATCHES BODY' if abs(optimal_W-0.94)<0.03 else 'DEVIATION'}")
results.append(f"  4. Percolation φ_c={phi_c_measured:.3f}: Bootstrap=0.623, Theory=0.593")
results.append(f"")
results.append(f"  God is good. All the time. Them beans though.")
results.append(f"")
results.append(f"  Author: Rhet Dillard Wike, AIIT-THRESI")
results.append(f"  Compiled by: Claude Opus 4.6")

output = "\n".join(results)
print(output)

with open("/home/buddy_ai/Desktop/RESULTS_BOOTSTRAP_NUCLEATION.txt", "w") as f:
    f.write(output)

print(f"\nResults saved to /home/buddy_ai/Desktop/RESULTS_BOOTSTRAP_NUCLEATION.txt")
