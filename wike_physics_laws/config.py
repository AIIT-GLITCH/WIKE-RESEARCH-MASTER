"""
WIKE Physics Laws Simulation Suite - Global Configuration
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6
"""

# ── Simulation Defaults ──────────────────────────────────────────────
T_MAX = 20.0
T_STEPS = 200
RUNS_PER_CONFIG = 1000
DISCREPANCY_THRESHOLD = 0.05
STRICT_THRESHOLD = 0.01

# ── Physical Constants ───────────────────────────────────────────────
K_B = 1.380649e-23          # Boltzmann constant (J/K)
HBAR = 1.0545718e-34        # Reduced Planck constant (J*s)
K_B_NATURAL = 1.0           # Boltzmann constant in natural units

# ── WIKE Parameter Ranges ────────────────────────────────────────────
WIKE_GAMMA_RANGE = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
WIKE_TEMP_RANGE = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]

# ── Per-Category Overrides ───────────────────────────────────────────
CATEGORY_CONFIGS = {
    "thermodynamics": {
        "runs": 1000,
        "t_max": 20.0,
        "t_steps": 200,
    },
    "quantum_mechanics": {
        "runs": 1000,
        "t_max": 10.0,
        "t_steps": 500,
    },
    "statistical_mechanics": {
        "runs": 2000,
        "t_max": 20.0,
        "t_steps": 200,
    },
    "electrodynamics": {
        "runs": 1000,
        "t_max": 15.0,
        "t_steps": 300,
    },
    "classical_mechanics": {
        "runs": 1000,
        "t_max": 20.0,
        "t_steps": 200,
    },
    "relativity": {
        "runs": 1000,
        "t_max": 10.0,
        "t_steps": 400,
    },
    "information_theory": {
        "runs": 1500,
        "t_max": 20.0,
        "t_steps": 200,
    },
}
