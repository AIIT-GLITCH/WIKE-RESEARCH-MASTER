"""
WIKE Physics Laws Simulation Suite - Category D: Statistical Mechanics
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

120 test configurations covering:
  D1 - Fluctuation-Dissipation Theorem (40)
  D2 - Kubo Formula / Linear Response (30)
  D3 - Onsager Reciprocal Relations (20)
  D4 - Jarzynski Equality (30)
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _thermal_state(H, temp):
    """Canonical thermal state rho = exp(-beta*H) / Z in natural units (k_B=1)."""
    beta = 1.0 / temp
    evals, evecs = H.eigenstates()
    boltz = np.exp(-beta * evals)
    Z = np.sum(boltz)
    rho = sum((b / Z) * qt.ket2dm(v) for b, v in zip(boltz, evecs))
    return rho, Z


def _free_energy(H, temp):
    """F = -kT * ln(Z)."""
    beta = 1.0 / temp
    evals = H.eigenenergies()
    Z = np.sum(np.exp(-beta * evals))
    return -temp * np.log(Z)


# ===========================================================================
# Category D
# ===========================================================================

class StatMechTests(PhysicsTestCategory):

    @property
    def category_id(self):
        return "D"

    @property
    def category_name(self):
        return "Statistical Mechanics"

    @property
    def description(self):
        return ("Fluctuation-Dissipation Theorem, Kubo Formula, Onsager Reciprocal "
                "Relations, and Jarzynski Equality across 120 configurations.")

    # -----------------------------------------------------------------------
    # Configurations
    # -----------------------------------------------------------------------

    def get_configs(self):
        configs = []
        configs.extend(self._d1_configs())
        configs.extend(self._d2_configs())
        configs.extend(self._d3_configs())
        configs.extend(self._d4_configs())
        return configs

    # -- D1 FDT (40) --------------------------------------------------------

    @staticmethod
    def _d1_configs():
        temps = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
        gaps = [0.5, 1.0, 2.0, 5.0, 10.0]
        cfgs = []
        for T in temps:
            for E in gaps:
                cfgs.append({
                    "test_id": f"D1_T{T}_E{E}",
                    "sub": "D1",
                    "temp": T,
                    "energy_gap": E,
                })
        return cfgs

    # -- D2 Kubo Formula (30) -----------------------------------------------

    @staticmethod
    def _d2_configs():
        obs_pairs = [
            ("sx", "sx"), ("sy", "sy"), ("sz", "sz"),
            ("sx", "sy"), ("sx", "sz"), ("sy", "sz"),
        ]
        temps = [0.5, 1.0, 2.0, 5.0, 10.0]
        cfgs = []
        for (a, b) in obs_pairs:
            for T in temps:
                cfgs.append({
                    "test_id": f"D2_{a}{b}_T{T}",
                    "sub": "D2",
                    "obs_A": a,
                    "obs_B": b,
                    "temp": T,
                    "epsilon": 0.01,
                    "energy_gap": 1.0,
                    "t_max": 5.0,
                    "t_steps": 200,
                })
        return cfgs

    # -- D3 Onsager Reciprocal (20) -----------------------------------------

    @staticmethod
    def _d3_configs():
        couplings = [0.05, 0.1, 0.5, 1.0, 2.0]
        dTs = [0.1, 0.5, 1.0, 2.0]
        cfgs = []
        for g in couplings:
            for dT in dTs:
                cfgs.append({
                    "test_id": f"D3_g{g}_dT{dT}",
                    "sub": "D3",
                    "coupling": g,
                    "dT": dT,
                    "T_base": 5.0,
                    "gamma_bath": 0.1,
                    "t_max": 30.0,
                    "t_steps": 300,
                })
        return cfgs

    # -- D4 Jarzynski Equality (30) -----------------------------------------

    @staticmethod
    def _d4_configs():
        speeds = [0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
        temps = [0.5, 1.0, 2.0, 5.0, 10.0]
        cfgs = []
        for v in speeds:
            for T in temps:
                cfgs.append({
                    "test_id": f"D4_v{v}_T{T}",
                    "sub": "D4",
                    "speed": v,
                    "temp": T,
                    "E_initial": 1.0,
                    "E_final": 3.0,
                    "n_realizations": 500,
                    "t_steps": 200,
                })
        return cfgs

    # -----------------------------------------------------------------------
    # Run dispatcher
    # -----------------------------------------------------------------------

    def run_single(self, config, run_index=0):
        sub = config["sub"]
        return {
            "D1": self._run_d1,
            "D2": self._run_d2,
            "D3": self._run_d3,
            "D4": self._run_d4,
        }[sub](config)

    # -- D1 Run: FDT --------------------------------------------------------

    @staticmethod
    def _run_d1(cfg):
        """Compute fluctuation <sz^2>-<sz>^2, compare to FDT susceptibility."""
        T = cfg["temp"]
        E = cfg["energy_gap"]

        H = E * qt.sigmaz() / 2.0
        rho_th, Z = _thermal_state(H, T)

        sz = qt.sigmaz()
        sz_mean = float(np.real(qt.expect(sz, rho_th)))
        sz2_mean = float(np.real(qt.expect(sz * sz, rho_th)))
        fluctuation = sz2_mean - sz_mean ** 2

        # Static susceptibility from FDT: chi = beta * <(A - <A>)^2>
        # So fluctuation = T * chi  =>  chi_fdt = fluctuation / T
        # Direct susceptibility: chi = d<sz>/dh at h=0
        # For H = E*sz/2 - h*sz: <sz> = -tanh(beta*E/2) at h=0
        # chi = d<sz>/dh = beta * (1 - tanh^2(beta*E/2))
        beta = 1.0 / T
        chi_theory = beta * (1.0 - np.tanh(beta * E / 2.0) ** 2)
        fdt_prediction = T * chi_theory  # should equal fluctuation

        return {
            "fluctuation": fluctuation,
            "fdt_prediction": fdt_prediction,
            "chi_theory": chi_theory,
        }

    # -- D2 Run: Kubo Formula -----------------------------------------------

    @staticmethod
    def _run_d2(cfg):
        """Linear response via direct perturbation vs equilibrium correlation."""
        T = cfg["temp"]
        E = cfg["energy_gap"]
        eps = cfg["epsilon"]
        t_max = cfg["t_max"]
        t_steps = cfg["t_steps"]

        op_map = {"sx": qt.sigmax(), "sy": qt.sigmay(), "sz": qt.sigmaz()}
        A = op_map[cfg["obs_A"]]
        B = op_map[cfg["obs_B"]]

        H0 = E * qt.sigmaz() / 2.0
        rho_eq, _ = _thermal_state(H0, T)

        # Method 1: Direct perturbation -- add eps*B to H, measure change in <A>
        H_pert = H0 + eps * B
        tlist = np.linspace(0, t_max, t_steps)
        result = qt.mesolve(H_pert, rho_eq, tlist, [], [A])

        # Linear response: delta<A>(t) = <A>(t) - <A>_eq
        A_eq = float(np.real(qt.expect(A, rho_eq)))
        delta_A_direct = np.array(result.expect[0]) - A_eq

        # Method 2: Kubo formula -- response via equilibrium correlation
        # chi(t) = -i * Tr(rho_eq * [A(t), B]) (integrated Kubo)
        # For static perturbation turned on at t=0:
        # delta<A>(t) = eps * integral_0^t chi(t') dt'
        # Use Heisenberg picture for A(t) = exp(iHt) A exp(-iHt)
        kubo_response = np.zeros(t_steps)
        beta = 1.0 / T
        for k, t in enumerate(tlist):
            if t == 0:
                continue
            U = (-1j * H0 * t).expm()
            U_dag = (1j * H0 * t).expm()
            A_t = U_dag * A * U
            commutator = A_t * B - B * A_t
            chi_t = -1j * (rho_eq * commutator).tr()
            kubo_response[k] = float(np.real(chi_t))

        # Integrate: delta<A>_kubo(t) = eps * cumulative integral of chi(t')
        dt = tlist[1] - tlist[0] if len(tlist) > 1 else 1.0
        delta_A_kubo = eps * np.cumsum(kubo_response) * dt

        # Compare at final time
        response_direct = float(delta_A_direct[-1])
        response_kubo = float(delta_A_kubo[-1])

        return {
            "response_direct": response_direct,
            "response_kubo": response_kubo,
        }

    # -- D3 Run: Onsager Reciprocal -----------------------------------------

    @staticmethod
    def _run_d3(cfg):
        """Two coupled qubits with separate thermal baths. Measure L12 vs L21."""
        g = cfg["coupling"]
        dT = cfg["dT"]
        T_base = cfg["T_base"]
        gamma = cfg["gamma_bath"]

        T1 = T_base + dT / 2.0
        T2 = T_base - dT / 2.0
        T2 = max(T2, 0.1)  # avoid negative temperature

        E1 = 1.0
        E2 = 1.5

        H1 = E1 * qt.sigmaz() / 2.0
        H2 = E2 * qt.sigmaz() / 2.0
        H_int = g * qt.tensor(qt.sigmax(), qt.sigmax())
        H = qt.tensor(H1, qt.qeye(2)) + qt.tensor(qt.qeye(2), H2) + H_int

        # Thermal bath collapse operators for each qubit
        beta1 = 1.0 / T1
        beta2 = 1.0 / T2

        n1 = 1.0 / (np.exp(beta1 * E1) - 1.0) if beta1 * E1 < 50 else 0.0
        n2 = 1.0 / (np.exp(beta2 * E2) - 1.0) if beta2 * E2 < 50 else 0.0

        # Qubit 1 bath
        a1 = qt.tensor(qt.destroy(2), qt.qeye(2))
        c_ops = [
            np.sqrt(gamma * (1.0 + n1)) * a1,
            np.sqrt(gamma * n1) * a1.dag(),
        ]
        # Qubit 2 bath
        a2 = qt.tensor(qt.qeye(2), qt.destroy(2))
        c_ops += [
            np.sqrt(gamma * (1.0 + n2)) * a2,
            np.sqrt(gamma * n2) * a2.dag(),
        ]

        # Start from product thermal state
        rho1_th, _ = _thermal_state(H1, T_base)
        rho2_th, _ = _thermal_state(H2, T_base)
        rho0 = qt.tensor(rho1_th, rho2_th)

        tlist = np.linspace(0, cfg["t_max"], cfg["t_steps"])
        result = qt.mesolve(H, rho0, tlist, c_ops, [])

        # Energy currents: J_k = d<H_k>/dt
        H1_full = qt.tensor(H1, qt.qeye(2))
        H2_full = qt.tensor(qt.qeye(2), H2)

        e1_vals = [float(np.real(qt.expect(H1_full, s))) for s in result.states]
        e2_vals = [float(np.real(qt.expect(H2_full, s))) for s in result.states]

        dt = tlist[1] - tlist[0]
        J1 = np.gradient(e1_vals, dt)
        J2 = np.gradient(e2_vals, dt)

        # Onsager coefficients: L12 ~ J1 / (dT applied to qubit 2)
        # L21 ~ J2 / (dT applied to qubit 1)
        # At steady state (use late-time average)
        late = len(tlist) // 2
        J1_ss = float(np.mean(J1[late:]))
        J2_ss = float(np.mean(J2[late:]))

        # Thermodynamic forces: X_k = -dT_k / T_base^2
        # L12 = J1 / X2, L21 = J2 / X1
        X1 = dT / (2.0 * T_base ** 2)   # force on qubit 1
        X2 = -dT / (2.0 * T_base ** 2)  # force on qubit 2

        L12 = J1_ss / X2 if abs(X2) > 1e-15 else 0.0
        L21 = J2_ss / X1 if abs(X1) > 1e-15 else 0.0

        return {
            "L12": L12,
            "L21": L21,
        }

    # -- D4 Run: Jarzynski Equality -----------------------------------------

    @staticmethod
    def _run_d4(cfg):
        """Two-point measurement protocol. Check <exp(-beta*W)> = exp(-beta*dF)."""
        T = cfg["temp"]
        E_i = cfg["E_initial"]
        E_f = cfg["E_final"]
        speed = cfg["speed"]
        n_real = cfg["n_realizations"]
        n_steps = cfg["t_steps"]

        beta = 1.0 / T
        ramp_time = abs(E_f - E_i) / speed

        # Initial and final Hamiltonians
        H_i = E_i * qt.sigmaz() / 2.0
        H_f = E_f * qt.sigmaz() / 2.0

        # Free energy difference
        F_i = _free_energy(H_i, T)
        F_f = _free_energy(H_f, T)
        dF = F_f - F_i

        # Initial thermal state
        rho_th, _ = _thermal_state(H_i, T)
        evals_i, evecs_i = H_i.eigenstates()
        def _expect_val(v, rho):
            val = v.dag() * rho * v
            if isinstance(val, qt.Qobj):
                return float(np.real(val.full()[0, 0]))
            else:
                return float(np.real(val))
        probs_i = np.array([_expect_val(v, rho_th) for v in evecs_i])

        # Collect work values
        np.random.seed(0)
        work_values = []

        for _ in range(n_real):
            # First measurement: sample initial energy eigenstate
            idx_i = np.random.choice(len(evals_i), p=probs_i / probs_i.sum())
            E_n = evals_i[idx_i]
            psi0 = evecs_i[idx_i]

            # Evolve with time-dependent H via piecewise constant
            tlist = np.linspace(0, ramp_time, n_steps)
            dt = tlist[1] - tlist[0] if len(tlist) > 1 else ramp_time
            psi = psi0

            for k in range(len(tlist) - 1):
                t_mid = (tlist[k] + tlist[k + 1]) / 2.0
                lam = t_mid / ramp_time  # interpolation parameter [0, 1]
                E_t = E_i + (E_f - E_i) * lam
                H_t = E_t * qt.sigmaz() / 2.0
                U = (-1j * H_t * dt).expm()
                psi = U * psi

            # Second measurement: project onto final energy eigenstates
            evals_f, evecs_f = H_f.eigenstates()
            probs_f = np.array([float(abs(v.dag().overlap(psi)) ** 2)
                                for v in evecs_f])
            probs_f = probs_f / probs_f.sum()
            idx_f = np.random.choice(len(evals_f), p=probs_f)
            E_m = evals_f[idx_f]

            W = E_m - E_n
            work_values.append(W)

        work_values = np.array(work_values)
        jarzynski_avg = float(np.mean(np.exp(-beta * work_values)))
        jarzynski_theory = np.exp(-beta * dF)

        return {
            "jarzynski_avg": jarzynski_avg,
            "jarzynski_theory": jarzynski_theory,
            "dF": dF,
            "mean_work": float(np.mean(work_values)),
        }

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def validate(self, config, results):
        """Validate aggregated results. Uses last result for deterministic sims."""
        result = results[-1] if isinstance(results, list) else results
        sub = config["sub"]
        verdicts = {
            "D1": self._validate_d1,
            "D2": self._validate_d2,
            "D3": self._validate_d3,
            "D4": self._validate_d4,
        }[sub](config, result)
        return {v.law_name: v for v in verdicts}

    @staticmethod
    def _validate_d1(cfg, res):
        """Fluctuation should match FDT prediction."""
        return [PhysicsValidator.check_equality(
            f"D1 FDT ({cfg['test_id']})",
            res["fluctuation"], res["fdt_prediction"],
            rel_threshold=0.05,
        )]

    @staticmethod
    def _validate_d2(cfg, res):
        """Direct perturbation response should match Kubo formula."""
        # Use generous threshold since both involve numerical integration
        return [PhysicsValidator.check_equality(
            f"D2 Kubo ({cfg['test_id']})",
            res["response_direct"], res["response_kubo"],
            rel_threshold=0.15,
        )]

    @staticmethod
    def _validate_d3(cfg, res):
        """L12 should equal L21 (Onsager reciprocity)."""
        return [PhysicsValidator.check_equality(
            f"D3 Onsager L12=L21 ({cfg['test_id']})",
            res["L12"], res["L21"],
            rel_threshold=0.20,
        )]

    @staticmethod
    def _validate_d4(cfg, res):
        """<exp(-beta*W)> should equal exp(-beta*dF)."""
        return [PhysicsValidator.check_equality(
            f"D4 Jarzynski ({cfg['test_id']})",
            res["jarzynski_avg"], res["jarzynski_theory"],
            rel_threshold=0.10,
        )]
