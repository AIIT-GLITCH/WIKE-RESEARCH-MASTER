"""
WIKE Physics Laws Simulation Suite - Category E: Quantum Information
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

E1  Holevo Bound              (35 configs)
E2  Channel Capacity           (35 configs)
E3  CKW Monogamy of Entanglement (35 configs)
E4  CHSH / Tsirelson Bound     (35 configs)
                         Total: 140 configs
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ── Helpers ─────────────────────────────────────────────────────────────

def von_neumann_entropy(rho):
    """Compute S(rho) = -Tr(rho log2 rho) via eigenvalues."""
    evals = np.real(rho.eigenenergies())
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log2(evals)))


def dephasing_channel(rho, gamma):
    """Apply single-qubit dephasing: off-diag elements multiplied by (1 - gamma)."""
    r = rho.full().copy()
    r[0, 1] *= (1.0 - gamma)
    r[1, 0] *= (1.0 - gamma)
    return qt.Qobj(r, dims=rho.dims)


def depolarizing_channel(rho, p):
    """Apply depolarizing channel: rho -> (1-p)*rho + p*I/d."""
    d = rho.shape[0]
    return (1.0 - p) * rho + p * qt.qeye(d) / d


def amplitude_damping_channel(rho, gamma):
    """Single-qubit amplitude damping via Kraus operators."""
    K0 = qt.Qobj([[1, 0], [0, np.sqrt(1 - gamma)]])
    K1 = qt.Qobj([[0, np.sqrt(gamma)], [0, 0]])
    return K0 * rho * K0.dag() + K1 * rho * K1.dag()


def concurrence_2qubit(rho):
    """Wootters concurrence for a 2-qubit density matrix."""
    sy = qt.sigmay()
    sy_sy = qt.tensor(sy, sy)
    rho_tilde = sy_sy * rho.conj() * sy_sy
    R2 = rho * rho_tilde
    evals = np.sort(np.real(np.sqrt(np.maximum(R2.eigenenergies(), 0))))[::-1]
    return float(max(0.0, evals[0] - evals[1] - evals[2] - evals[3]))


# ── Ensemble Generators ─────────────────────────────────────────────────

def _make_ensemble(kind, rng):
    """Return list of (p_i, rho_i) tuples for a qubit ensemble."""
    b0, b1 = qt.basis(2, 0), qt.basis(2, 1)
    plus = (b0 + b1).unit()
    minus = (b0 - b1).unit()
    plus_y = (b0 + 1j * b1).unit()

    if kind == "uniform_z":
        return [(0.5, qt.ket2dm(b0)), (0.5, qt.ket2dm(b1))]
    elif kind == "uniform_x":
        return [(0.5, qt.ket2dm(plus)), (0.5, qt.ket2dm(minus))]
    elif kind == "biased_z":
        return [(0.8, qt.ket2dm(b0)), (0.2, qt.ket2dm(b1))]
    elif kind == "three_state":
        return [(1 / 3, qt.ket2dm(b0)), (1 / 3, qt.ket2dm(plus)),
                (1 / 3, qt.ket2dm(plus_y))]
    elif kind == "pure_mix":
        rho_mix = 0.5 * qt.qeye(2) / 2.0 + 0.5 * qt.ket2dm(b0)
        return [(0.5, qt.ket2dm(b0)), (0.5, rho_mix)]
    elif kind == "random_2":
        psi1 = qt.rand_ket(2, seed=rng)
        psi2 = qt.rand_ket(2, seed=rng)
        return [(0.5, qt.ket2dm(psi1)), (0.5, qt.ket2dm(psi2))]
    elif kind == "random_4":
        states = [qt.rand_ket(2, seed=rng) for _ in range(4)]
        return [(0.25, qt.ket2dm(s)) for s in states]
    else:
        return [(0.5, qt.ket2dm(b0)), (0.5, qt.ket2dm(b1))]


# ── 3-qubit state generators ────────────────────────────────────────────

def _make_3qubit_state(kind, rng):
    """Return a 3-qubit density matrix."""
    b0, b1 = qt.basis(2, 0), qt.basis(2, 1)
    if kind == "ghz":
        psi = (qt.tensor(b0, b0, b0) + qt.tensor(b1, b1, b1)).unit()
    elif kind == "w":
        psi = (qt.tensor(b1, b0, b0) + qt.tensor(b0, b1, b0) +
               qt.tensor(b0, b0, b1)).unit()
    elif kind == "random":
        psi = qt.rand_ket(8, seed=rng)
        psi.dims = [[2, 2, 2], [1, 1, 1]]
    elif kind == "bisep_12":
        psi12 = qt.rand_ket(4, seed=rng)
        psi12.dims = [[2, 2], [1, 1]]
        psi3 = qt.basis(2, 0)
        psi = qt.tensor(psi12, psi3)
    elif kind == "bisep_13":
        psi1 = qt.rand_ket(2, seed=rng)
        psi2 = qt.basis(2, 0)
        psi3 = qt.rand_ket(2, seed=rng)
        psi = qt.tensor(psi1, psi2, psi3)
    elif kind == "product":
        psi = qt.tensor(qt.rand_ket(2, seed=rng),
                         qt.rand_ket(2, seed=rng),
                         qt.rand_ket(2, seed=rng))
    elif kind == "cluster":
        plus = (b0 + b1).unit()
        psi = qt.tensor(plus, plus, plus)
        cz01 = qt.Qobj(np.diag([1, 1, 1, -1]), dims=[[2, 2], [2, 2]])
        cz01_full = qt.tensor(cz01, qt.qeye(2))
        cz12 = qt.tensor(qt.qeye(2), cz01)
        psi = cz12 * cz01_full * psi
    else:
        psi = qt.tensor(b0, b0, b0)
    return qt.ket2dm(psi)


# ═══════════════════════════════════════════════════════════════════════
class QuantumInfoTests(PhysicsTestCategory):
    """Category E: Quantum Information (140 configs)."""

    @property
    def category_id(self):
        return "E"

    @property
    def category_name(self):
        return "Quantum Information"

    @property
    def description(self):
        return ("Holevo bound, channel capacity, CKW monogamy of "
                "entanglement, and CHSH/Tsirelson inequality.")

    # ── configuration generation ────────────────────────────────────────

    def get_configs(self):
        configs = []

        # E1 Holevo Bound: 7 ensembles x 5 gamma = 35
        ensembles = ["uniform_z", "uniform_x", "biased_z", "three_state",
                     "pure_mix", "random_2", "random_4"]
        gammas = [0.01, 0.05, 0.1, 0.2, 0.5]
        for ens in ensembles:
            for g in gammas:
                configs.append({
                    "test_id": "E1", "law": "Holevo Bound",
                    "ensemble": ens, "gamma": g,
                })

        # E2 Channel Capacity: 3 channels x 7 noise + 14 extras = 35
        channels = ["depolarizing", "amplitude_damping", "dephasing"]
        noise_params = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
        for ch in channels:
            for p in noise_params:
                configs.append({
                    "test_id": "E2", "law": "Channel Capacity",
                    "channel": ch, "noise_param": p,
                })
        # 14 extras for finer coverage
        extra_noise = [0.02, 0.03, 0.07, 0.15, 0.25, 0.35, 0.4,
                       0.45, 0.55, 0.6, 0.65, 0.7, 0.75, 0.9]
        for i, p in enumerate(extra_noise):
            ch = channels[i % len(channels)]
            configs.append({
                "test_id": "E2", "law": "Channel Capacity",
                "channel": ch, "noise_param": p,
            })

        # E3 CKW Monogamy: 7 state types x 5 gamma = 35
        state_types = ["ghz", "w", "random", "bisep_12", "bisep_13",
                       "product", "cluster"]
        gammas_ckw = [0.0, 0.01, 0.05, 0.1, 0.2]
        for st in state_types:
            for g in gammas_ckw:
                configs.append({
                    "test_id": "E3", "law": "CKW Monogamy",
                    "state_type": st, "gamma": g,
                })

        # E4 CHSH: 7 angle configs x 5 gamma = 35
        angle_configs = [
            {"a1": 0.0, "a2": np.pi / 2, "b1": np.pi / 4, "b2": -np.pi / 4},
            {"a1": 0.0, "a2": np.pi / 4, "b1": np.pi / 8, "b2": -np.pi / 8},
            {"a1": np.pi / 6, "a2": np.pi / 3, "b1": np.pi / 4, "b2": 0.0},
            {"a1": 0.0, "a2": np.pi / 2, "b1": 0.0, "b2": np.pi / 2},
            {"a1": np.pi / 4, "a2": 3 * np.pi / 4,
             "b1": np.pi / 2, "b2": 0.0},
            {"a1": 0.0, "a2": np.pi / 3, "b1": np.pi / 6, "b2": -np.pi / 6},
            {"a1": np.pi / 8, "a2": 3 * np.pi / 8,
             "b1": np.pi / 4, "b2": 0.0},
        ]
        gammas_chsh = [0.0, 0.01, 0.05, 0.1, 0.3]
        for ac in angle_configs:
            for g in gammas_chsh:
                configs.append({
                    "test_id": "E4", "law": "CHSH Tsirelson Bound",
                    "angles": ac, "gamma": g,
                })

        return configs

    # ── simulation ──────────────────────────────────────────────────────

    def run_single(self, config, run_index):
        rng = np.random.default_rng(42 + run_index)
        tid = config["test_id"]

        if tid == "E1":
            return self._run_holevo(config, rng)
        elif tid == "E2":
            return self._run_channel_capacity(config, rng)
        elif tid == "E3":
            return self._run_ckw(config, rng)
        elif tid == "E4":
            return self._run_chsh(config, rng)
        return {}

    def _run_holevo(self, config, rng):
        ensemble = _make_ensemble(config["ensemble"], rng)
        gamma = config["gamma"]

        # Apply dephasing channel to each state
        channel_ensemble = [(p, dephasing_channel(rho, gamma))
                            for p, rho in ensemble]

        # Average state
        rho_avg = sum(p * rho for p, rho in channel_ensemble)

        # Holevo chi quantity
        S_avg = von_neumann_entropy(rho_avg)
        S_weighted = sum(p * von_neumann_entropy(rho)
                         for p, rho in channel_ensemble)
        chi = S_avg - S_weighted

        return {"chi": chi, "holevo_bound": 1.0}

    def _run_channel_capacity(self, config, rng):
        p = config["noise_param"]
        ch = config["channel"]

        # Use maximally mixed input (worst-case entropy output)
        rho_in = qt.qeye(2) / 2.0

        if ch == "depolarizing":
            rho_out = depolarizing_channel(rho_in, p)
        elif ch == "amplitude_damping":
            rho_out = amplitude_damping_channel(rho_in, p)
        elif ch == "dephasing":
            rho_out = dephasing_channel(rho_in, p)
        else:
            rho_out = rho_in

        S_output = von_neumann_entropy(rho_out)
        return {"S_output": S_output, "bound": 1.0}

    def _run_ckw(self, config, rng):
        rho_abc = _make_3qubit_state(config["state_type"], rng)
        gamma = config["gamma"]

        # Apply dephasing on qubit A if gamma > 0
        if gamma > 0:
            dims_orig = rho_abc.dims
            r = rho_abc.full().copy()
            n = r.shape[0]  # 8
            for i in range(n):
                for j in range(n):
                    q0_i = (i >> 2) & 1
                    q0_j = (j >> 2) & 1
                    if q0_i != q0_j:
                        r[i, j] *= (1.0 - gamma)
            rho_abc = qt.Qobj(r, dims=dims_orig)

        # Reduced states
        rho_ab = rho_abc.ptrace([0, 1])
        rho_ac = rho_abc.ptrace([0, 2])

        # Concurrences
        C_AB = concurrence_2qubit(rho_ab)
        C_AC = concurrence_2qubit(rho_ac)

        # C(A|BC): tangle of A vs BC bipartition
        # For a pure state, C(A|BC) = 2*sqrt(det(rho_A))
        rho_a = rho_abc.ptrace([0])
        det_a = np.real(np.linalg.det(rho_a.full()))
        C_ABC = 2.0 * np.sqrt(max(0.0, det_a))

        return {
            "C_AB": C_AB, "C_AC": C_AC, "C_ABC": C_ABC,
            "C2_ABC": C_ABC ** 2,
            "C2_AB_plus_AC": C_AB ** 2 + C_AC ** 2,
        }

    def _run_chsh(self, config, rng):
        gamma = config["gamma"]
        angles = config["angles"]

        # Bell state |Phi+> = (|00> + |11>)/sqrt(2), then dephase
        b0, b1 = qt.basis(2, 0), qt.basis(2, 1)
        bell = (qt.tensor(b0, b0) + qt.tensor(b1, b1)).unit()
        rho = qt.ket2dm(bell)

        # Dephasing on both qubits
        if gamma > 0:
            r = rho.full().copy()
            for i in range(4):
                for j in range(4):
                    q0_i, q0_j = (i >> 1) & 1, (j >> 1) & 1
                    q1_i, q1_j = i & 1, j & 1
                    damp = 1.0
                    if q0_i != q0_j:
                        damp *= (1.0 - gamma)
                    if q1_i != q1_j:
                        damp *= (1.0 - gamma)
                    r[i, j] *= damp
            rho = qt.Qobj(r, dims=[[2, 2], [2, 2]])

        # sigma_n(theta) = cos(theta)*sigma_z + sin(theta)*sigma_x
        def sigma_n(theta):
            return np.cos(theta) * qt.sigmaz() + np.sin(theta) * qt.sigmax()

        def E(a, b):
            op = qt.tensor(sigma_n(a), sigma_n(b))
            return float(np.real((rho * op).tr()))

        a1, a2 = angles["a1"], angles["a2"]
        b1, b2 = angles["b1"], angles["b2"]
        S = E(a1, b1) - E(a1, b2) + E(a2, b1) + E(a2, b2)

        return {
            "S": float(S), "abs_S": float(abs(S)),
            "tsirelson_bound": 2.0 * np.sqrt(2.0),
        }

    # ── validation ──────────────────────────────────────────────────────

    def validate(self, config, results):
        """Validate aggregated results. Returns dict of law_name -> Verdict."""
        verdicts = {}
        tid = config["test_id"]

        # Use first result (deterministic sims)
        result = results[0]

        if tid == "E1":
            verdicts["Holevo Bound"] = PhysicsValidator.check_bound(
                "Holevo Bound: chi <= log2(d)",
                result["chi"], result["holevo_bound"], direction="upper")

        elif tid == "E2":
            verdicts["Channel Capacity"] = PhysicsValidator.check_bound(
                "Channel Output Entropy: S <= log2(d)",
                result["S_output"], result["bound"], direction="upper")

        elif tid == "E3":
            verdicts["CKW Monogamy"] = PhysicsValidator.check_inequality(
                "CKW Monogamy: C^2(A|BC) >= C^2(AB) + C^2(AC)",
                result["C2_ABC"], result["C2_AB_plus_AC"],
                direction=">=", threshold=1e-6)

        elif tid == "E4":
            verdicts["CHSH Tsirelson"] = PhysicsValidator.check_bound(
                "CHSH Tsirelson: |S| <= 2*sqrt(2)",
                result["abs_S"], result["tsirelson_bound"],
                direction="upper")

        return verdicts
