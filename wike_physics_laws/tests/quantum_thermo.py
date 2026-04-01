"""
WIKE Physics Laws Simulation Suite - Category F: Quantum Thermodynamics
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

F1  Landauer Principle          (35 configs)
F2  Quantum Heat Engine (Otto)  (35 configs)
F3  Work from Coherence         (30 configs)
                          Total: 100 configs
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ── Helpers ─────────────────────────────────────────────────────────────

def von_neumann_entropy(rho):
    """S(rho) = -Tr(rho ln rho) in natural log (nats)."""
    evals = np.real(rho.eigenenergies())
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


def thermal_state(H, T, kB=1.0):
    """Gibbs thermal state rho = exp(-H/kT) / Z."""
    beta = 1.0 / (kB * T) if T > 0 else 1e12
    evals, evecs = H.eigenstates()
    Z = sum(np.exp(-beta * E) for E in evals)
    rho = sum((np.exp(-beta * E) / Z) * qt.ket2dm(v)
              for E, v in zip(evals, evecs))
    return rho


# ═══════════════════════════════════════════════════════════════════════
class QuantumThermoTests(PhysicsTestCategory):
    """Category F: Quantum Thermodynamics (100 configs)."""

    @property
    def category_id(self):
        return "F"

    @property
    def category_name(self):
        return "Quantum Thermodynamics"

    @property
    def description(self):
        return ("Landauer erasure principle, quantum Otto cycle efficiency, "
                "and extractable work from quantum coherence.")

    # ── configuration generation ────────────────────────────────────────

    def get_configs(self):
        configs = []

        # F1 Landauer Principle: 7 temps x 5 speeds = 35
        temps = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
        speeds = [0.01, 0.05, 0.1, 0.5, 1.0]
        for T in temps:
            for speed in speeds:
                configs.append({
                    "test_id": "F1", "law": "Landauer Principle",
                    "temperature": T, "speed": speed,
                })

        # F2 Heat Engine (Otto): 7 operating points x 5 gamma = 35
        operating_points = [
            {"omega_h": 4.0, "omega_c": 1.0},
            {"omega_h": 3.0, "omega_c": 1.0},
            {"omega_h": 5.0, "omega_c": 1.0},
            {"omega_h": 4.0, "omega_c": 2.0},
            {"omega_h": 6.0, "omega_c": 1.0},
            {"omega_h": 3.0, "omega_c": 0.5},
            {"omega_h": 8.0, "omega_c": 2.0},
        ]
        gammas_otto = [0.01, 0.05, 0.1, 0.2, 0.5]
        for op in operating_points:
            for g in gammas_otto:
                configs.append({
                    "test_id": "F2", "law": "Heat Engine Efficiency",
                    "omega_h": op["omega_h"], "omega_c": op["omega_c"],
                    "T_hot": 10.0, "T_cold": 1.0, "gamma": g,
                })

        # F3 Work from Coherence: 6 coherence levels x 5 temps = 30
        coherence_levels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.49]
        temps_coh = [0.5, 1.0, 2.0, 5.0, 10.0]
        for c in coherence_levels:
            for T in temps_coh:
                configs.append({
                    "test_id": "F3", "law": "Work from Coherence",
                    "coherence": c, "temperature": T,
                })

        return configs

    # ── simulation ──────────────────────────────────────────────────────

    def run_single(self, config, run_index):
        tid = config["test_id"]

        if tid == "F1":
            return self._run_landauer(config)
        elif tid == "F2":
            return self._run_otto(config)
        elif tid == "F3":
            return self._run_coherence_work(config)
        return {}

    def _run_landauer(self, config):
        """Erase a qubit by ramping energy gap; track heat to bath."""
        T = config["temperature"]
        speed = config["speed"]
        kB = 1.0

        # Initial state: maximally mixed (unknown bit)
        rho = qt.qeye(2) / 2.0

        # Erasure protocol: ramp splitting from epsilon_0 to 10*epsilon_0
        epsilon_0 = 1.0
        n_steps = max(50, int(1.0 / speed))
        dt = 1.0 / n_steps
        total_heat = 0.0

        for step in range(n_steps):
            frac = step / n_steps
            epsilon = epsilon_0 * (1.0 + 9.0 * frac)  # ramp to 10x

            H = epsilon * qt.sigmaz() / 2.0
            rho_thermal = thermal_state(H, T, kB)

            # Energy before relaxation
            E_before = np.real((H * rho).tr())

            # Partial thermalization
            rate = 1.0 - np.exp(-speed * dt * 10.0)
            rho_new = (1.0 - rate) * rho + rate * rho_thermal

            # Energy after relaxation
            E_after = np.real((H * rho_new).tr())

            # Heat = energy lost by system to bath
            total_heat += float(E_before - E_after)
            rho = rho_new

        landauer_bound = kB * T * np.log(2)
        return {
            "Q_dissipated": total_heat,
            "landauer_bound": landauer_bound,
        }

    def _run_otto(self, config):
        """Quantum Otto cycle: 2-level system between hot/cold baths."""
        omega_h = config["omega_h"]
        omega_c = config["omega_c"]
        T_hot = config["T_hot"]
        T_cold = config["T_cold"]
        gamma = config["gamma"]
        kB = 1.0

        H_h = omega_h * qt.sigmaz() / 2.0
        H_c = omega_c * qt.sigmaz() / 2.0

        # Step 1: Isochoric heating at omega_h
        rho_hot = thermal_state(H_h, T_hot, kB)
        rho_init = thermal_state(H_c, T_cold, kB)
        rho_after_heat = (1.0 - gamma) * rho_hot + gamma * rho_init

        # Step 2: Isentropic expansion omega_h -> omega_c
        p_excited_hot = float(np.real(rho_after_heat[1, 1]))
        p_ground_hot = 1.0 - p_excited_hot

        E_after_expansion = (p_ground_hot * (-omega_c / 2.0)
                             + p_excited_hot * (omega_c / 2.0))
        E_before_expansion = float(np.real((H_h * rho_after_heat).tr()))
        W_expansion = E_before_expansion - E_after_expansion

        # Step 3: Isochoric cooling at omega_c
        rho_cold = thermal_state(H_c, T_cold, kB)
        rho_after_cool = (1.0 - gamma) * rho_cold + gamma * rho_after_heat

        # Step 4: Isentropic compression omega_c -> omega_h
        p_excited_cold = float(np.real(rho_after_cool[1, 1]))
        p_ground_cold = 1.0 - p_excited_cold

        E_after_compression = (p_ground_cold * (-omega_h / 2.0)
                               + p_excited_cold * (omega_h / 2.0))
        E_before_compression = float(np.real((H_c * rho_after_cool).tr()))
        W_compression = E_before_compression - E_after_compression

        W_net = W_expansion + W_compression
        Q_hot = (float(np.real((H_h * rho_after_heat).tr()))
                 - E_after_compression)

        eta = W_net / Q_hot if Q_hot > 1e-15 else 0.0
        eta = max(0.0, eta)

        eta_carnot = 1.0 - T_cold / T_hot

        return {
            "eta": eta,
            "eta_carnot": eta_carnot,
            "W_net": W_net,
            "Q_hot": Q_hot,
        }

    def _run_coherence_work(self, config):
        """Extractable work from quantum coherence in energy basis."""
        c = config["coherence"]
        T = config["temperature"]
        kB = 1.0

        # Qubit Hamiltonian
        omega = 1.0
        H = omega * qt.sigmaz() / 2.0

        # State with coherence c in energy basis
        rho = qt.Qobj([[0.5, c], [c, 0.5]])

        # Diagonal (dephased) state
        rho_diag = qt.Qobj([[0.5, 0], [0, 0.5]])

        S_rho = von_neumann_entropy(rho)
        S_diag = von_neumann_entropy(rho_diag)

        # Work from coherence: W_coh = kB*T*(S_diag - S_rho)
        W_coh = kB * T * (S_diag - S_rho)

        return {
            "W_coh": W_coh,
            "S_rho": S_rho,
            "S_diag": S_diag,
        }

    # ── validation ──────────────────────────────────────────────────────

    def validate(self, config, results):
        """Validate aggregated results. Returns dict of law_name -> Verdict."""
        verdicts = {}
        tid = config["test_id"]
        result = results[0]

        if tid == "F1":
            verdicts["Landauer Principle"] = PhysicsValidator.check_inequality(
                "Landauer: Q >= kT*ln(2)",
                result["Q_dissipated"], result["landauer_bound"],
                direction=">=", threshold=1e-6)

        elif tid == "F2":
            verdicts["Otto Efficiency"] = PhysicsValidator.check_inequality(
                "Otto Efficiency: eta <= eta_Carnot",
                result["eta"], result["eta_carnot"],
                direction="<=", threshold=1e-6)

        elif tid == "F3":
            verdicts["Work from Coherence"] = PhysicsValidator.check_inequality(
                "Coherence Work: W_coh >= 0",
                result["W_coh"], 0.0,
                direction=">=", threshold=1e-10)

        return verdicts
