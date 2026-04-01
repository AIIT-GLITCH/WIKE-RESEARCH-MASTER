"""
WIKE Physics Laws Simulation Suite - Category G: Open Quantum Systems
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

G1  Lindblad Validity          (35 configs)
G2  Complete Positivity         (35 configs)
G3  Quantum Regression Theorem  (30 configs)
G4  Spin-Boson Model            (30 configs)
                          Total: 130 configs
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ── Helpers ─────────────────────────────────────────────────────────────

def _make_hamiltonian(kind):
    """Return a single-qubit Hamiltonian by name."""
    if kind == "sigma_z":
        return qt.sigmaz()
    elif kind == "sigma_x":
        return qt.sigmax()
    elif kind == "sigma_y":
        return qt.sigmay()
    elif kind == "detuned_z":
        return 2.0 * qt.sigmaz() + 0.5 * qt.sigmax()
    elif kind == "driven":
        return qt.sigmaz() + 0.3 * qt.sigmax()
    else:
        return qt.sigmaz()


def _make_collapse_ops(kind, gamma=0.1):
    """Return list of collapse operators for a single qubit."""
    sm = qt.destroy(2)
    sp = sm.dag()

    if kind == "decay":
        return [np.sqrt(gamma) * sm]
    elif kind == "excitation":
        return [np.sqrt(gamma) * sp]
    elif kind == "dephasing":
        return [np.sqrt(gamma) * qt.sigmaz()]
    elif kind == "decay_dephasing":
        return [np.sqrt(gamma) * sm,
                np.sqrt(gamma * 0.5) * qt.sigmaz()]
    elif kind == "thermal":
        n_th = 0.5
        return [np.sqrt(gamma * (n_th + 1)) * sm,
                np.sqrt(gamma * n_th) * sp]
    elif kind == "strong_decay":
        return [np.sqrt(gamma * 5.0) * sm]
    elif kind == "multi_channel":
        return [np.sqrt(gamma * 0.5) * sm,
                np.sqrt(gamma * 0.3) * qt.sigmaz(),
                np.sqrt(gamma * 0.2) * qt.sigmax()]
    else:
        return [np.sqrt(gamma) * sm]


# ═══════════════════════════════════════════════════════════════════════
class OpenSystemsTests(PhysicsTestCategory):
    """Category G: Open Quantum Systems (130 configs)."""

    @property
    def category_id(self):
        return "G"

    @property
    def category_name(self):
        return "Open Quantum Systems"

    @property
    def description(self):
        return ("Lindblad validity, complete positivity via Choi matrix, "
                "quantum regression theorem, and spin-boson dynamics.")

    # ── configuration generation ────────────────────────────────────────

    def get_configs(self):
        configs = []

        # G1 Lindblad Validity: 7 collapse configs x 5 Hamiltonians = 35
        collapse_kinds = ["decay", "excitation", "dephasing",
                          "decay_dephasing", "thermal", "strong_decay",
                          "multi_channel"]
        ham_kinds = ["sigma_z", "sigma_x", "sigma_y",
                     "detuned_z", "driven"]
        for ck in collapse_kinds:
            for hk in ham_kinds:
                configs.append({
                    "test_id": "G1", "law": "Lindblad Validity",
                    "collapse_kind": ck, "hamiltonian_kind": hk,
                    "gamma": 0.1, "t_max": 10.0, "n_steps": 100,
                })

        # G2 Complete Positivity: 7 noise models x 5 time points = 35
        noise_models = ["decay", "excitation", "dephasing",
                        "decay_dephasing", "thermal", "strong_decay",
                        "multi_channel"]
        time_points = [0.5, 1.0, 2.0, 5.0, 10.0]
        for nm in noise_models:
            for tp in time_points:
                configs.append({
                    "test_id": "G2", "law": "Complete Positivity",
                    "noise_model": nm, "t_eval": tp,
                    "gamma": 0.1,
                })

        # G3 Quantum Regression Theorem: 6 observable pairs x 5 gamma = 30
        obs_pairs = [
            ("sigma_x", "sigma_x"),
            ("sigma_y", "sigma_y"),
            ("sigma_z", "sigma_z"),
            ("sigma_x", "sigma_z"),
            ("sigma_plus", "sigma_minus"),
            ("sigma_minus", "sigma_plus"),
        ]
        gammas_qrt = [0.01, 0.05, 0.1, 0.2, 0.5]
        for A_name, B_name in obs_pairs:
            for g in gammas_qrt:
                configs.append({
                    "test_id": "G3",
                    "law": "Quantum Regression Theorem",
                    "obs_A": A_name, "obs_B": B_name, "gamma": g,
                    "t_steady": 20.0, "tau_max": 5.0, "n_tau": 50,
                })

        # G4 Spin-Boson: 6 coupling x 5 bath types = 30
        alphas = [0.01, 0.05, 0.1, 0.3, 0.5, 1.0]
        bath_types = ["ohmic", "super_ohmic", "sub_ohmic",
                      "lorentzian", "white_noise"]
        for alpha in alphas:
            for bt in bath_types:
                configs.append({
                    "test_id": "G4", "law": "Spin-Boson Dynamics",
                    "alpha": alpha, "bath_type": bt,
                    "T_bath": 1.0, "Delta": 1.0, "t_max": 20.0,
                })

        return configs

    # ── simulation ──────────────────────────────────────────────────────

    def run_single(self, config, run_index):
        tid = config["test_id"]

        if tid == "G1":
            return self._run_lindblad_validity(config)
        elif tid == "G2":
            return self._run_complete_positivity(config)
        elif tid == "G3":
            return self._run_regression(config)
        elif tid == "G4":
            return self._run_spin_boson(config)
        return {}

    def _run_lindblad_validity(self, config):
        """Evolve under Lindblad ME; check rho validity at every step."""
        H = _make_hamiltonian(config["hamiltonian_kind"])
        c_ops = _make_collapse_ops(config["collapse_kind"], config["gamma"])
        t_max = config["t_max"]
        n_steps = config["n_steps"]
        tlist = np.linspace(0, t_max, n_steps + 1)

        # Initial state: |+> for nontrivial coherences
        psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()

        result = qt.mesolve(H, psi0, tlist, c_ops, [])

        traces = []
        hermitian_diffs = []
        min_eigenvalues = []

        for rho in result.states:
            rho_full = rho.full()
            traces.append(float(np.real(np.trace(rho_full))))
            herm_diff = float(
                np.max(np.abs(rho_full - rho_full.conj().T)))
            hermitian_diffs.append(herm_diff)
            evals = np.real(np.linalg.eigvalsh(rho_full))
            min_eigenvalues.append(float(np.min(evals)))

        return {
            "traces": traces,
            "hermitian_diffs": hermitian_diffs,
            "min_eigenvalues": min_eigenvalues,
            "n_steps": n_steps,
        }

    def _run_complete_positivity(self, config):
        """Reconstruct Choi matrix from process tomography; check PSD."""
        c_ops = _make_collapse_ops(config["noise_model"], config["gamma"])
        H = qt.sigmaz()
        t_eval = config["t_eval"]

        # Basis operators: |0><0|, |0><1|, |1><0|, |1><1|
        basis_ops = [
            qt.basis(2, 0) * qt.basis(2, 0).dag(),
            qt.basis(2, 0) * qt.basis(2, 1).dag(),
            qt.basis(2, 1) * qt.basis(2, 0).dag(),
            qt.basis(2, 1) * qt.basis(2, 1).dag(),
        ]

        # Evolve each basis operator
        evolved = []
        for rho_in in basis_ops:
            res = qt.mesolve(H, rho_in, [0, t_eval], c_ops, [])
            evolved.append(res.states[-1].full())

        # Construct Choi matrix (4x4)
        choi = np.zeros((4, 4), dtype=complex)
        for i in range(2):
            for j in range(2):
                idx = i * 2 + j
                E_ij = evolved[idx]
                for m in range(2):
                    for n in range(2):
                        choi[i * 2 + m, j * 2 + n] = E_ij[m, n]

        eigenvalues = np.real(np.linalg.eigvalsh(choi))
        min_eig = float(np.min(eigenvalues))

        return {
            "choi_matrix": choi,
            "choi_eigenvalues": eigenvalues.tolist(),
            "min_eigenvalue": min_eig,
        }

    def _run_regression(self, config):
        """Compare two-time correlator via regression theorem vs direct."""
        gamma = config["gamma"]

        H = qt.sigmaz()
        c_ops = [np.sqrt(gamma) * qt.destroy(2)]

        def _get_op(name):
            if name == "sigma_x":
                return qt.sigmax()
            elif name == "sigma_y":
                return qt.sigmay()
            elif name == "sigma_z":
                return qt.sigmaz()
            elif name == "sigma_plus":
                return qt.destroy(2).dag()
            elif name == "sigma_minus":
                return qt.destroy(2)
            return qt.sigmax()

        A = _get_op(config["obs_A"])
        B = _get_op(config["obs_B"])

        # Reach approximate steady state
        psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
        t_steady = config["t_steady"]
        res_ss = qt.mesolve(H, psi0, [0, t_steady], c_ops, [])
        rho_ss = res_ss.states[-1]

        # Regression theorem: <A(t+tau)B(t)>_ss = Tr(A * G(tau)[B*rho_ss])
        tau_max = config["tau_max"]
        n_tau = config["n_tau"]
        taulist = np.linspace(0, tau_max, n_tau)

        # Via regression theorem
        rho_B = B * rho_ss
        res_reg = qt.mesolve(H, rho_B, taulist, c_ops, [A])
        corr_regression = np.array(res_reg.expect[0])

        # Direct calculation
        corr_direct = np.array(
            qt.correlation_2op_1t(H, rho_ss, taulist, c_ops, A, B))

        max_diff = float(np.max(np.abs(corr_regression - corr_direct)))
        mean_diff = float(np.mean(np.abs(corr_regression - corr_direct)))

        return {
            "corr_regression": np.real(corr_regression).tolist(),
            "corr_direct": np.real(corr_direct).tolist(),
            "max_diff": max_diff,
            "mean_diff": mean_diff,
        }

    def _run_spin_boson(self, config):
        """Spin-boson via effective Lindblad: tunnelling qubit + bath."""
        alpha = config["alpha"]
        bt = config["bath_type"]
        T_bath = config["T_bath"]
        Delta = config["Delta"]
        t_max = config["t_max"]

        # Effective dissipation rate from bath spectral density
        omega_0 = Delta
        if bt == "ohmic":
            gamma_eff = alpha * omega_0
        elif bt == "super_ohmic":
            gamma_eff = alpha * omega_0 ** 2
        elif bt == "sub_ohmic":
            gamma_eff = alpha * np.sqrt(omega_0)
        elif bt == "lorentzian":
            omega_c = 5.0 * omega_0
            gamma_eff = (alpha * omega_0 * omega_c ** 2
                         / (omega_0 ** 2 + omega_c ** 2))
        elif bt == "white_noise":
            gamma_eff = alpha
        else:
            gamma_eff = alpha * omega_0

        # Thermal occupation
        kB = 1.0
        if T_bath > 0:
            n_th = 1.0 / (np.exp(omega_0 / (kB * T_bath)) - 1.0)
        else:
            n_th = 0.0

        # H = Delta/2 * sigma_x (tunnelling qubit)
        H = (Delta / 2.0) * qt.sigmax()

        sm = qt.destroy(2)
        c_ops = [
            np.sqrt(gamma_eff * (n_th + 1)) * sm,
            np.sqrt(gamma_eff * n_th) * sm.dag(),
        ]

        # Initial state: spin up (localized)
        psi0 = qt.basis(2, 0)
        n_steps = 200
        tlist = np.linspace(0, t_max, n_steps + 1)

        res = qt.mesolve(H, psi0, tlist, c_ops,
                          [qt.sigmaz(), qt.sigmax()])

        sz = np.array(res.expect[0])
        sx = np.array(res.expect[1])

        # Classify dynamics
        is_weak = alpha < 0.3
        if is_weak:
            crossings = int(np.sum(np.diff(np.sign(sz)) != 0))
            oscillatory = crossings >= 2
        else:
            oscillatory = False

        late_sz = np.mean(np.abs(sz[-20:]))
        localized = late_sz > 0.3 and not oscillatory

        return {
            "sz": sz.tolist(),
            "sx": sx.tolist(),
            "tlist": tlist.tolist(),
            "alpha": alpha,
            "gamma_eff": gamma_eff,
            "oscillatory": oscillatory,
            "localized": localized,
            "is_weak_coupling": is_weak,
        }

    # ── validation ──────────────────────────────────────────────────────

    def validate(self, config, results):
        """Validate aggregated results. Returns dict of law_name -> Verdict."""
        verdicts = {}
        tid = config["test_id"]
        result = results[0]

        if tid == "G1":
            # Check trace, Hermiticity, PSD at every timestep
            for i, tr in enumerate(result["traces"]):
                verdicts[f"Tr(rho)=1 [step {i}]"] = (
                    PhysicsValidator.check_equality(
                        f"Lindblad Tr(rho)=1 [step {i}]", tr, 1.0,
                        rel_threshold=1e-8))
            for i, hd in enumerate(result["hermitian_diffs"]):
                verdicts[f"Hermitian [step {i}]"] = (
                    PhysicsValidator.check_inequality(
                        f"Lindblad Hermitian [step {i}]",
                        hd, 1e-10, direction="<="))
            for i, me in enumerate(result["min_eigenvalues"]):
                verdicts[f"PSD [step {i}]"] = (
                    PhysicsValidator.check_inequality(
                        f"Lindblad PSD [step {i}]",
                        me, -1e-10, direction=">="))

        elif tid == "G2":
            verdicts["Choi PSD"] = (
                PhysicsValidator.check_positive_semidefinite(
                    "Choi Matrix PSD (Complete Positivity)",
                    result["choi_matrix"]))

        elif tid == "G3":
            verdicts["Regression Theorem"] = (
                PhysicsValidator.check_inequality(
                    "Quantum Regression Theorem: max |diff| small",
                    result["max_diff"], 1e-4,
                    direction="<=", threshold=1e-4))

        elif tid == "G4":
            if result["is_weak_coupling"]:
                detail = ("oscillatory" if result["oscillatory"]
                          else "non-oscillatory")
                passed = result["oscillatory"]
                verdicts["Spin-Boson Dynamics"] = (
                    PhysicsValidator.check_inequality(
                        f"Spin-Boson Weak Coupling: oscillatory decay "
                        f"({detail})",
                        0.0 if passed else 1.0, 0.5, direction="<="))
            else:
                detail = ("localized" if result["localized"]
                          else "delocalized")
                passed = result["localized"]
                verdicts["Spin-Boson Dynamics"] = (
                    PhysicsValidator.check_inequality(
                        f"Spin-Boson Strong Coupling: localization "
                        f"({detail})",
                        0.0 if passed else 1.0, 0.5, direction="<="))

        return verdicts
