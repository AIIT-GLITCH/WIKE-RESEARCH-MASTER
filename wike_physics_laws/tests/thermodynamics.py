"""
WIKE Physics Laws Simulation Suite - Category A: Thermodynamics
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

150 test configurations covering:
  A1 - Second Law of Thermodynamics (50)
  A2 - Detailed Balance (30)
  A3 - Boltzmann Distribution (40)
  A4 - Carnot Efficiency Bound (30)
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _von_neumann_entropy(rho):
    """Compute S = -Tr(rho * log(rho)) via eigenvalues."""
    evals = np.real(rho.eigenenergies())
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


def _thermal_state(H, temp, k_B=1.0):
    """Construct the canonical thermal state rho = exp(-H/kT) / Z."""
    beta = 1.0 / (k_B * temp) if temp > 0 else np.inf
    evals, evecs = H.eigenstates()
    Z = np.sum(np.exp(-beta * evals))
    rho = sum(np.exp(-beta * e) / Z * v * v.dag() for e, v in zip(evals, evecs))
    return rho


def _initial_qubit_state(label):
    """Return a 2x2 density matrix for common initial states."""
    mapping = {
        "ground":  qt.ket2dm(qt.basis(2, 0)),
        "excited": qt.ket2dm(qt.basis(2, 1)),
        "plus":    qt.ket2dm((qt.basis(2, 0) + qt.basis(2, 1)).unit()),
        "minus":   qt.ket2dm((qt.basis(2, 0) - qt.basis(2, 1)).unit()),
        "mixed":   qt.Qobj(np.array([[0.5, 0.0], [0.0, 0.5]])),
    }
    return mapping[label]


# ===========================================================================
# Category A
# ===========================================================================

class ThermodynamicsTests(PhysicsTestCategory):

    @property
    def category_id(self):
        return "A"

    @property
    def category_name(self):
        return "Thermodynamics"

    @property
    def description(self):
        return ("Second Law, Detailed Balance, Boltzmann Distribution, "
                "and Carnot Efficiency across 150 configurations.")

    # -----------------------------------------------------------------------
    # Configuration generators
    # -----------------------------------------------------------------------

    def get_configs(self):
        configs = []
        configs.extend(self._a1_configs())
        configs.extend(self._a2_configs())
        configs.extend(self._a3_configs())
        configs.extend(self._a4_configs())
        return configs

    # -- A1 Second Law (50) -------------------------------------------------

    @staticmethod
    def _a1_configs():
        states = ["ground", "excited", "plus", "minus", "mixed"]
        temps = [0.1, 1.0, 5.0, 10.0, 50.0]
        gammas = [0.01, 0.1]
        cfgs = []
        for s in states:
            for T in temps:
                for g in gammas:
                    cfgs.append({
                        "test_id": f"A1_{s}_T{T}_g{g}",
                        "sub": "A1",
                        "initial_state": s,
                        "temp": T,
                        "gamma": g,
                        "t_max": 20.0,
                        "t_steps": 200,
                    })
        return cfgs

    # -- A2 Detailed Balance (30) -------------------------------------------

    @staticmethod
    def _a2_configs():
        temps = [0.1, 0.5, 1.0, 5.0, 10.0, 50.0]
        gaps = [0.5, 1.0, 2.0, 5.0, 10.0]
        cfgs = []
        for T in temps:
            for E in gaps:
                cfgs.append({
                    "test_id": f"A2_T{T}_E{E}",
                    "sub": "A2",
                    "temp": T,
                    "energy_gap": E,
                    "gamma_base": 0.1,
                    "t_max": 50.0,
                    "t_steps": 500,
                })
        return cfgs

    # -- A3 Boltzmann Distribution (40) -------------------------------------

    @staticmethod
    def _a3_configs():
        sizes = [3, 4, 5]
        temps = [0.5, 1.0, 5.0, 20.0]
        spacings = [0.5, 1.0, 2.0]
        cfgs = []
        for N in sizes:
            for T in temps:
                for dE in spacings:
                    cfgs.append({
                        "test_id": f"A3_N{N}_T{T}_dE{dE}",
                        "sub": "A3",
                        "n_levels": N,
                        "temp": T,
                        "energy_spacing": dE,
                        "gamma": 0.1,
                        "t_max": 80.0,
                        "t_steps": 400,
                    })
        # 4 extras: edge cases
        extras = [
            {"n_levels": 3, "temp": 0.1, "energy_spacing": 1.0},
            {"n_levels": 5, "temp": 100.0, "energy_spacing": 0.5},
            {"n_levels": 4, "temp": 0.01, "energy_spacing": 2.0},
            {"n_levels": 5, "temp": 50.0, "energy_spacing": 3.0},
        ]
        for i, ex in enumerate(extras):
            cfgs.append({
                "test_id": f"A3_extra_{i}",
                "sub": "A3",
                "gamma": 0.1,
                "t_max": 80.0,
                "t_steps": 400,
                **ex,
            })
        return cfgs

    # -- A4 Carnot Efficiency (30) ------------------------------------------

    @staticmethod
    def _a4_configs():
        temp_pairs = [
            (1.0, 5.0), (1.0, 10.0), (1.0, 50.0),
            (2.0, 10.0), (5.0, 50.0), (0.5, 20.0),
        ]
        compressions = [1.5, 2.0, 3.0, 5.0, 10.0]
        cfgs = []
        for (Tc, Th) in temp_pairs:
            for r in compressions:
                cfgs.append({
                    "test_id": f"A4_Tc{Tc}_Th{Th}_r{r}",
                    "sub": "A4",
                    "T_cold": Tc,
                    "T_hot": Th,
                    "compression_ratio": r,
                    "t_max": 40.0,
                    "t_steps": 400,
                })
        return cfgs

    # -----------------------------------------------------------------------
    # Simulation dispatcher
    # -----------------------------------------------------------------------

    def run_single(self, config, run_index=0):
        sub = config["sub"]
        if sub == "A1":
            return self._run_a1(config)
        elif sub == "A2":
            return self._run_a2(config)
        elif sub == "A3":
            return self._run_a3(config)
        elif sub == "A4":
            return self._run_a4(config)
        raise ValueError(f"Unknown sub-test: {sub}")

    # -- A1 Run -------------------------------------------------------------

    @staticmethod
    def _run_a1(cfg):
        """Evolve qubit with amplitude damping toward thermal state, track entropy."""
        T = cfg["temp"]
        gamma = cfg["gamma"]
        H = qt.sigmaz() * 0.5  # energy gap = 1

        # Thermal occupation: n_bar = 1/(exp(E/kT)-1)
        beta = 1.0 / T
        n_bar = 1.0 / (np.exp(beta) - 1.0) if beta < 50 else 0.0

        # Collapse operators for thermal amplitude damping
        c_ops = []
        rate_down = gamma * (1.0 + n_bar)
        rate_up = gamma * n_bar
        if rate_down > 0:
            c_ops.append(np.sqrt(rate_down) * qt.destroy(2))
        if rate_up > 0:
            c_ops.append(np.sqrt(rate_up) * qt.create(2))

        rho0 = _initial_qubit_state(cfg["initial_state"])
        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, c_ops, [])

        entropies = [_von_neumann_entropy(r) for r in result.states]
        return {"entropies": entropies, "tlist": tlist.tolist()}

    # -- A2 Run -------------------------------------------------------------

    @staticmethod
    def _run_a2(cfg):
        """Thermal collapse ops with detailed balance; evolve to steady state."""
        T = cfg["temp"]
        E = cfg["energy_gap"]
        gamma_base = cfg["gamma_base"]

        H = E * qt.num(2)  # |1> has energy E
        beta = 1.0 / T

        gamma_down = gamma_base
        gamma_up = gamma_base * np.exp(-beta * E)

        c_ops = [
            np.sqrt(gamma_down) * qt.destroy(2),
            np.sqrt(gamma_up) * qt.create(2),
        ]

        rho0 = qt.ket2dm((qt.basis(2, 0) + qt.basis(2, 1)).unit())
        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, c_ops, [])

        rho_final = result.states[-1]
        p0 = float(np.real(rho_final[0, 0]))
        p1 = float(np.real(rho_final[1, 1]))

        ratio_sim = p1 / p0 if p0 > 1e-15 else np.inf
        ratio_theory = np.exp(-beta * E)
        return {
            "p0": p0,
            "p1": p1,
            "ratio_sim": ratio_sim,
            "ratio_theory": ratio_theory,
        }

    # -- A3 Run -------------------------------------------------------------

    @staticmethod
    def _run_a3(cfg):
        """Multi-level system thermalizing to Boltzmann distribution."""
        N = cfg["n_levels"]
        T = cfg["temp"]
        dE = cfg["energy_spacing"]
        gamma = cfg["gamma"]

        energies = np.array([n * dE for n in range(N)])
        H = qt.Qobj(np.diag(energies))

        beta = 1.0 / T
        boltz = np.exp(-beta * energies)
        expected_pops = boltz / boltz.sum()

        # Collapse ops: transitions between adjacent levels
        c_ops = []
        for n in range(N - 1):
            lower = qt.basis(N, n)
            upper = qt.basis(N, n + 1)
            jump_down = lower * upper.dag()
            jump_up = upper * lower.dag()
            dE_n = energies[n + 1] - energies[n]
            n_bar = 1.0 / (np.exp(beta * dE_n) - 1.0) if beta * dE_n < 50 else 0.0
            c_ops.append(np.sqrt(gamma * (1.0 + n_bar)) * jump_down)
            if n_bar > 1e-15:
                c_ops.append(np.sqrt(gamma * n_bar) * jump_up)

        # Start in equal superposition
        psi0 = sum(qt.basis(N, n) for n in range(N))
        psi0 = psi0.unit()
        rho0 = qt.ket2dm(psi0)

        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, c_ops, [])

        rho_final = result.states[-1]
        sim_pops = np.array([float(np.real(rho_final[n, n])) for n in range(N)])

        return {
            "sim_pops": sim_pops.tolist(),
            "expected_pops": expected_pops.tolist(),
        }

    # -- A4 Run -------------------------------------------------------------

    @staticmethod
    def _run_a4(cfg):
        """Quantum Otto cycle: two isochoric + two adiabatic strokes."""
        Tc = cfg["T_cold"]
        Th = cfg["T_hot"]
        r = cfg["compression_ratio"]

        # Qubit gaps for hot and cold strokes
        E_cold = 1.0
        E_hot = E_cold * r

        H_cold = E_cold * qt.num(2)
        H_hot = E_hot * qt.num(2)

        # Isochoric heating: thermalise at T_hot with H_hot
        rho_hot = _thermal_state(H_hot, Th)
        # Isochoric cooling: thermalise at T_cold with H_cold
        rho_cold = _thermal_state(H_cold, Tc)

        # Populations
        p1_hot = float(np.real(rho_hot[1, 1]))
        p1_cold = float(np.real(rho_cold[1, 1]))

        # Heat absorbed from hot reservoir during isochoric heating
        Q_hot = E_hot * (p1_hot - p1_cold)
        # Heat released to cold reservoir during isochoric cooling
        Q_cold = E_cold * (p1_hot - p1_cold)
        # Work output
        W = Q_hot - Q_cold

        eta_sim = W / Q_hot if Q_hot > 1e-15 else 0.0
        eta_carnot = 1.0 - Tc / Th

        return {
            "eta_sim": eta_sim,
            "eta_carnot": eta_carnot,
            "Q_hot": Q_hot,
            "Q_cold": Q_cold,
            "W": W,
        }

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def validate(self, config, results):
        """Validate aggregated results. Uses last result for deterministic sims."""
        result = results[-1] if isinstance(results, list) else results
        sub = config["sub"]
        if sub == "A1":
            verdicts = self._validate_a1(config, result)
        elif sub == "A2":
            verdicts = self._validate_a2(config, result)
        elif sub == "A3":
            verdicts = self._validate_a3(config, result)
        elif sub == "A4":
            verdicts = self._validate_a4(config, result)
        else:
            raise ValueError(f"Unknown sub-test: {sub}")
        return {v.law_name: v for v in verdicts}

    @staticmethod
    def _validate_a1(cfg, res):
        """Entropy should be non-decreasing (Second Law)."""
        v = PhysicsValidator.check_monotonic(
            f"A1 Second Law ({cfg['test_id']})",
            res["entropies"],
            direction="increasing",
        )
        return [v]

    @staticmethod
    def _validate_a2(cfg, res):
        """Steady-state ratio p1/p0 should equal exp(-E/kT)."""
        v = PhysicsValidator.check_equality(
            f"A2 Detailed Balance ({cfg['test_id']})",
            res["ratio_sim"],
            res["ratio_theory"],
            rel_threshold=0.05,
        )
        return [v]

    @staticmethod
    def _validate_a3(cfg, res):
        """Final populations should match Boltzmann distribution."""
        sim = np.array(res["sim_pops"])
        exp = np.array(res["expected_pops"])
        verdicts = []
        for i in range(len(sim)):
            verdicts.append(PhysicsValidator.check_equality(
                f"A3 Boltzmann pop[{i}] ({cfg['test_id']})",
                sim[i], exp[i], rel_threshold=0.05,
            ))
        return verdicts

    @staticmethod
    def _validate_a4(cfg, res):
        """Otto cycle efficiency must not exceed Carnot bound."""
        v = PhysicsValidator.check_inequality(
            f"A4 Carnot Bound ({cfg['test_id']})",
            res["eta_sim"],
            res["eta_carnot"],
            direction="<=",
            threshold=1e-10,
        )
        return [v]
