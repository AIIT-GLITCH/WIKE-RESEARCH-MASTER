"""
WIKE Physics Laws Simulation Suite - Category B: QM Fundamentals
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

160 test configurations covering:
  B1 - Born Rule (40)
  B2 - Heisenberg Uncertainty xp (30)
  B3 - Energy-Time Uncertainty (20)
  B4 - No-Cloning Theorem (20)
  B5 - Quantum Zeno Effect (25)
  B6 - Landau-Zener Transition (25)
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ===========================================================================
# Category B
# ===========================================================================

class QMFundamentalsTests(PhysicsTestCategory):

    @property
    def category_id(self):
        return "B"

    @property
    def category_name(self):
        return "QM Fundamentals"

    @property
    def description(self):
        return ("Born Rule, Heisenberg Uncertainty, Energy-Time Uncertainty, "
                "No-Cloning, Quantum Zeno, and Landau-Zener across 160 configurations.")

    # -----------------------------------------------------------------------
    # Configurations
    # -----------------------------------------------------------------------

    def get_configs(self):
        configs = []
        configs.extend(self._b1_configs())
        configs.extend(self._b2_configs())
        configs.extend(self._b3_configs())
        configs.extend(self._b4_configs())
        configs.extend(self._b5_configs())
        configs.extend(self._b6_configs())
        return configs

    # -- B1 Born Rule (40) --------------------------------------------------

    @staticmethod
    def _b1_configs():
        thetas = np.linspace(0.1, np.pi - 0.1, 10)
        gammas = [0.0, 0.01, 0.05, 0.1]
        cfgs = []
        for theta in thetas:
            for g in gammas:
                cfgs.append({
                    "test_id": f"B1_th{theta:.3f}_g{g}",
                    "sub": "B1",
                    "theta": float(theta),
                    "gamma": g,
                    "t_max": 10.0,
                    "t_steps": 200,
                })
        return cfgs

    # -- B2 Heisenberg xp (30) ---------------------------------------------

    @staticmethod
    def _b2_configs():
        alphas = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]
        gammas = [0.0, 0.001, 0.005, 0.01, 0.05]
        cfgs = []
        for alpha in alphas:
            for g in gammas:
                cfgs.append({
                    "test_id": f"B2_a{alpha}_g{g}",
                    "sub": "B2",
                    "alpha": alpha,
                    "gamma": g,
                    "N_fock": 25,
                    "t_max": 5.0,
                    "t_steps": 100,
                })
        return cfgs

    # -- B3 Energy-Time Uncertainty (20) ------------------------------------

    @staticmethod
    def _b3_configs():
        omegas = [0.5, 1.0, 2.0, 5.0, 10.0]
        mix_params = [0.1, 0.3, 0.5, 0.7]
        cfgs = []
        for w in omegas:
            for m in mix_params:
                cfgs.append({
                    "test_id": f"B3_w{w}_m{m}",
                    "sub": "B3",
                    "omega": w,
                    "mix": m,
                    "t_max": 10.0,
                    "t_steps": 500,
                })
        return cfgs

    # -- B4 No-Cloning (20) ------------------------------------------------

    @staticmethod
    def _b4_configs():
        thetas = np.linspace(0.1, np.pi - 0.1, 10)
        strategies = ["cnot", "swap"]
        cfgs = []
        for theta in thetas:
            for strat in strategies:
                cfgs.append({
                    "test_id": f"B4_th{theta:.3f}_{strat}",
                    "sub": "B4",
                    "theta": float(theta),
                    "strategy": strat,
                })
        return cfgs

    # -- B5 Quantum Zeno (25) ----------------------------------------------

    @staticmethod
    def _b5_configs():
        n_meas_list = [2, 5, 10, 20, 50]
        omegas = [0.5, 1.0, 2.0, 5.0, 10.0]
        cfgs = []
        for n in n_meas_list:
            for w in omegas:
                cfgs.append({
                    "test_id": f"B5_n{n}_w{w}",
                    "sub": "B5",
                    "n_measurements": n,
                    "omega": w,
                    "total_time": 1.0,
                })
        return cfgs

    # -- B6 Landau-Zener (25) ----------------------------------------------

    @staticmethod
    def _b6_configs():
        sweep_rates = [0.1, 0.5, 1.0, 5.0, 20.0]
        gaps = [0.1, 0.3, 0.5, 1.0, 2.0]
        cfgs = []
        for v in sweep_rates:
            for delta in gaps:
                cfgs.append({
                    "test_id": f"B6_v{v}_d{delta}",
                    "sub": "B6",
                    "sweep_rate": v,
                    "gap": delta,
                    "t_span": 20.0,
                    "t_steps": 2000,
                })
        return cfgs

    # -----------------------------------------------------------------------
    # Run dispatcher
    # -----------------------------------------------------------------------

    def run_single(self, config, run_index=0):
        sub = config["sub"]
        return {
            "B1": self._run_b1,
            "B2": self._run_b2,
            "B3": self._run_b3,
            "B4": self._run_b4,
            "B5": self._run_b5,
            "B6": self._run_b6,
        }[sub](config)

    # -- B1 Run: Born Rule --------------------------------------------------

    @staticmethod
    def _run_b1(cfg):
        """Prepare state, evolve with optional dephasing, measure P(|0>)."""
        theta = cfg["theta"]
        gamma = cfg["gamma"]

        psi0 = np.cos(theta / 2) * qt.basis(2, 0) + np.sin(theta / 2) * qt.basis(2, 1)
        rho0 = qt.ket2dm(psi0)

        H = qt.qeye(2) * 0  # trivial Hamiltonian
        c_ops = []
        if gamma > 0:
            c_ops.append(np.sqrt(gamma) * qt.sigmaz())

        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, c_ops, [])

        rho_final = result.states[-1]
        p0_sim = float(np.real(rho_final[0, 0]))
        p0_theory = np.cos(theta / 2) ** 2
        trace = float(np.real(rho_final.tr()))

        return {
            "p0_sim": p0_sim,
            "p0_theory": p0_theory,
            "trace": trace,
        }

    # -- B2 Run: Heisenberg xp ----------------------------------------------

    @staticmethod
    def _run_b2(cfg):
        """Coherent state in harmonic oscillator, check dx*dp >= 0.5."""
        N = cfg["N_fock"]
        alpha = cfg["alpha"]
        gamma = cfg["gamma"]

        H = qt.num(N)  # harmonic oscillator (hbar*omega = 1)
        psi0 = qt.coherent(N, alpha)
        rho0 = qt.ket2dm(psi0)

        c_ops = []
        if gamma > 0:
            c_ops.append(np.sqrt(gamma) * qt.destroy(N))

        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, c_ops, [])

        rho = result.states[-1]

        # Position and momentum quadratures
        a = qt.destroy(N)
        x_op = (a + a.dag()) / np.sqrt(2)
        p_op = 1j * (a.dag() - a) / np.sqrt(2)

        x_mean = float(np.real(qt.expect(x_op, rho)))
        p_mean = float(np.real(qt.expect(p_op, rho)))
        x2_mean = float(np.real(qt.expect(x_op * x_op, rho)))
        p2_mean = float(np.real(qt.expect(p_op * p_op, rho)))

        dx = np.sqrt(max(x2_mean - x_mean ** 2, 0))
        dp = np.sqrt(max(p2_mean - p_mean ** 2, 0))

        return {"dx": dx, "dp": dp, "product": dx * dp}

    # -- B3 Run: Energy-Time Uncertainty ------------------------------------

    @staticmethod
    def _run_b3(cfg):
        """Superposition of two energy eigenstates, check dE*tau >= 0.5."""
        omega = cfg["omega"]
        m = cfg["mix"]

        H = omega * qt.sigmaz() / 2.0
        psi0 = (np.sqrt(1 - m) * qt.basis(2, 0) + np.sqrt(m) * qt.basis(2, 1)).unit()

        # Energy uncertainty
        rho0 = qt.ket2dm(psi0)
        E_mean = float(np.real(qt.expect(H, rho0)))
        E2_mean = float(np.real(qt.expect(H * H, rho0)))
        dE = np.sqrt(max(E2_mean - E_mean ** 2, 0))

        # Characteristic time: time for state to become orthogonal or
        # for expectation value of observable to change by its std dev.
        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, [], [qt.sigmaz()])
        sz_vals = np.array(result.expect[0])

        # Find time for significant change: |<sz>(t) - <sz>(0)| >= std
        sz_std = np.std(sz_vals)
        dt_idx = np.where(np.abs(sz_vals - sz_vals[0]) >= sz_std)[0]
        if len(dt_idx) > 0:
            tau = tlist[dt_idx[0]]
        else:
            tau = tlist[-1]

        # Avoid trivial tau = 0
        tau = max(tau, 1e-12)

        return {"dE": dE, "tau": tau, "product": dE * tau}

    # -- B4 Run: No-Cloning -------------------------------------------------

    @staticmethod
    def _run_b4(cfg):
        """Attempt to clone via CNOT or SWAP; check fidelity < 1 for non-basis."""
        theta = cfg["theta"]
        strategy = cfg["strategy"]

        psi_in = np.cos(theta / 2) * qt.basis(2, 0) + np.sin(theta / 2) * qt.basis(2, 1)
        target = qt.basis(2, 0)  # blank ancilla
        psi_total = qt.tensor(psi_in, target)

        if strategy == "cnot":
            gate = qt.Qobj([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dims=[[2,2],[2,2]])
        else:  # swap
            gate = qt.Qobj([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dims=[[2,2],[2,2]])

        psi_out = gate * psi_total
        rho_out = qt.ket2dm(psi_out)

        # Reduced states of each qubit
        rho_a = rho_out.ptrace(0)
        rho_b = rho_out.ptrace(1)

        # Ideal clone: both should be |psi_in>
        ideal = qt.ket2dm(psi_in)
        fid_a = float(np.real(qt.fidelity(rho_a, ideal) ** 2))
        fid_b = float(np.real(qt.fidelity(rho_b, ideal) ** 2))

        # Is it a basis state (theta ~ 0 or pi)?
        is_basis = (abs(theta) < 0.01) or (abs(theta - np.pi) < 0.01)

        return {
            "fidelity_a": fid_a,
            "fidelity_b": fid_b,
            "is_basis": is_basis,
        }

    # -- B5 Run: Quantum Zeno -----------------------------------------------

    @staticmethod
    def _run_b5(cfg):
        """Repeated projective measurements suppress transitions."""
        n = cfg["n_measurements"]
        omega = cfg["omega"]
        T = cfg["total_time"]
        dt = T / n

        H = omega * qt.sigmax() / 2.0
        proj_0 = qt.ket2dm(qt.basis(2, 0))
        rho = qt.ket2dm(qt.basis(2, 0))

        # Evolve and project n times
        survival = 1.0
        for _ in range(n):
            tlist = np.linspace(0, dt, 50)
            result = qt.mesolve(H, rho, tlist, [], [])
            rho_evolved = result.states[-1]
            p0 = float(np.real((proj_0 * rho_evolved).tr()))
            survival *= p0
            # Post-measurement state (project onto |0>)
            if p0 > 1e-15:
                rho = proj_0 * rho_evolved * proj_0 / p0
            else:
                rho = proj_0
                break

        # Theoretical Zeno prediction
        zeno_theory = np.cos(omega * dt / 2) ** (2 * n)

        return {
            "survival_sim": survival,
            "survival_theory": zeno_theory,
        }

    # -- B6 Run: Landau-Zener -----------------------------------------------

    @staticmethod
    def _run_b6(cfg):
        """Piecewise evolution of time-dependent H for Landau-Zener transition."""
        v = cfg["sweep_rate"]
        delta = cfg["gap"]
        t_span = cfg["t_span"]
        n_steps = cfg["t_steps"]

        tlist = np.linspace(-t_span / 2, t_span / 2, n_steps)
        dt = tlist[1] - tlist[0]

        # Start in ground state of initial H (large negative t -> |1> in sigma_z basis)
        psi = qt.basis(2, 1)

        # Piecewise constant evolution
        for i in range(len(tlist) - 1):
            t_mid = (tlist[i] + tlist[i + 1]) / 2.0
            H_t = v * t_mid * qt.sigmaz() / 2.0 + delta * qt.sigmax() / 2.0
            U = (-1j * H_t * dt).expm()
            psi = U * psi

        # Probability of staying in |1> (diabatic state)
        p_diabatic = float(abs(psi.overlap(qt.basis(2, 1))) ** 2)

        # Landau-Zener formula: probability of diabatic transition
        p_lz_theory = np.exp(-np.pi * delta ** 2 / (2 * v))

        return {
            "p_diabatic_sim": p_diabatic,
            "p_diabatic_theory": p_lz_theory,
        }

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def validate(self, config, results):
        """Validate aggregated results. Uses last result for deterministic sims."""
        result = results[-1] if isinstance(results, list) else results
        sub = config["sub"]
        verdicts = {
            "B1": self._validate_b1,
            "B2": self._validate_b2,
            "B3": self._validate_b3,
            "B4": self._validate_b4,
            "B5": self._validate_b5,
            "B6": self._validate_b6,
        }[sub](config, result)
        return {v.law_name: v for v in verdicts}

    @staticmethod
    def _validate_b1(cfg, res):
        verdicts = []
        # P(|0>) = cos^2(theta/2)
        verdicts.append(PhysicsValidator.check_equality(
            f"B1 Born Rule P0 ({cfg['test_id']})",
            res["p0_sim"], res["p0_theory"], rel_threshold=0.05,
        ))
        # Trace preservation
        verdicts.append(PhysicsValidator.check_equality(
            f"B1 Trace ({cfg['test_id']})",
            res["trace"], 1.0, rel_threshold=1e-6,
        ))
        return verdicts

    @staticmethod
    def _validate_b2(cfg, res):
        return [PhysicsValidator.check_inequality(
            f"B2 Heisenberg xp ({cfg['test_id']})",
            res["product"], 0.5, direction=">=", threshold=1e-6,
        )]

    @staticmethod
    def _validate_b3(cfg, res):
        return [PhysicsValidator.check_inequality(
            f"B3 Energy-Time ({cfg['test_id']})",
            res["product"], 0.5, direction=">=", threshold=1e-6,
        )]

    @staticmethod
    def _validate_b4(cfg, res):
        verdicts = []
        if not res["is_basis"]:
            # For non-basis states, at least one copy must have fid < 1
            min_fid = min(res["fidelity_a"], res["fidelity_b"])
            verdicts.append(PhysicsValidator.check_inequality(
                f"B4 No-Cloning ({cfg['test_id']})",
                min_fid, 1.0, direction="<", threshold=1e-6,
            ))
        else:
            # Basis states can be "cloned" via CNOT -- fidelity may be 1
            verdicts.append(PhysicsValidator.check_inequality(
                f"B4 Basis clone ({cfg['test_id']})",
                res["fidelity_a"], 0.0, direction=">=",
            ))
        return verdicts

    @staticmethod
    def _validate_b5(cfg, res):
        return [PhysicsValidator.check_equality(
            f"B5 Zeno ({cfg['test_id']})",
            res["survival_sim"], res["survival_theory"],
            rel_threshold=0.05,
        )]

    @staticmethod
    def _validate_b6(cfg, res):
        return [PhysicsValidator.check_equality(
            f"B6 Landau-Zener ({cfg['test_id']})",
            res["p_diabatic_sim"], res["p_diabatic_theory"],
            rel_threshold=0.10,
        )]
