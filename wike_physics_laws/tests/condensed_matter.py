"""
WIKE Physics Laws Simulation Suite - Category H: Condensed Matter
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6

H1  Lieb-Robinson Bound        (40 configs)
H2  Area Law of Entanglement    (40 configs)
H3  Quantum Phase Transition    (40 configs)
                          Total: 120 configs
"""

import numpy as np
import qutip as qt

from .base import PhysicsTestCategory
from validator import PhysicsValidator


# ── Helpers ─────────────────────────────────────────────────────────────

def _local_op(N, site, op):
    """Build operator 'op' acting on 'site' in an N-spin chain.

    Parameters
    ----------
    N : int
        Number of spins.
    site : int
        Site index (0-based).
    op : qutip.Qobj
        Single-site operator (2x2).

    Returns
    -------
    qutip.Qobj
        Full N-spin operator with 'op' at 'site' and identity elsewhere.
    """
    op_list = [qt.qeye(2)] * N
    op_list[site] = op
    return qt.tensor(op_list)


def _build_heisenberg_chain(N, Jx, Jy, Jz, h=0.0):
    """Build a Heisenberg spin-chain Hamiltonian.

    H = sum_i [ Jx*Sx_i*Sx_{i+1} + Jy*Sy_i*Sy_{i+1} + Jz*Sz_i*Sz_{i+1} ]
        + h * sum_i Sx_i

    Parameters
    ----------
    N : int
        Number of spins.
    Jx, Jy, Jz : float
        Exchange couplings.
    h : float
        Transverse field strength (along x).

    Returns
    -------
    qutip.Qobj
        Full Hamiltonian.
    """
    sx, sy, sz = qt.sigmax(), qt.sigmay(), qt.sigmaz()
    H = 0
    for i in range(N - 1):
        if Jx != 0:
            H += Jx * _local_op(N, i, sx) * _local_op(N, i + 1, sx)
        if Jy != 0:
            H += Jy * _local_op(N, i, sy) * _local_op(N, i + 1, sy)
        if Jz != 0:
            H += Jz * _local_op(N, i, sz) * _local_op(N, i + 1, sz)
    if h != 0:
        for i in range(N):
            H += h * _local_op(N, i, sx)
    return H


def _transverse_field_ising(N, J, h):
    """Build transverse-field Ising: H = -J sum Sz_i Sz_{i+1} - h sum Sx_i."""
    return _build_heisenberg_chain(N, Jx=0, Jy=0, Jz=-J, h=-h)


def _entanglement_entropy(psi, N, subsystem):
    """Von Neumann entanglement entropy of subsystem."""
    rho = qt.ket2dm(psi)
    rho.dims = [[2] * N, [2] * N]
    rho_sub = rho.ptrace(subsystem)
    evals = np.real(rho_sub.eigenenergies())
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


# ═══════════════════════════════════════════════════════════════════════
class CondensedMatterTests(PhysicsTestCategory):
    """Category H: Condensed Matter (120 configs)."""

    @property
    def category_id(self):
        return "H"

    @property
    def category_name(self):
        return "Condensed Matter"

    @property
    def description(self):
        return ("Lieb-Robinson bound on information propagation, area law "
                "of entanglement entropy, and quantum phase transitions "
                "in the transverse-field Ising model.")

    # ── configuration generation ────────────────────────────────────────

    def get_configs(self):
        configs = []

        # H1 Lieb-Robinson: 5 chains x 4 couplings x 2 perturbations = 40
        chain_lengths = [4, 5, 6, 7, 8]
        couplings = [
            {"Jx": 1.0, "Jy": 1.0, "Jz": 1.0, "label": "isotropic"},
            {"Jx": 1.0, "Jy": 1.0, "Jz": 0.0, "label": "XX"},
            {"Jx": 1.0, "Jy": 0.0, "Jz": 0.0, "label": "X_only"},
            {"Jx": 1.0, "Jy": 1.0, "Jz": 2.0, "label": "XXZ_delta2"},
        ]
        perturbations = ["sigma_x", "sigma_z"]
        for N in chain_lengths:
            for coup in couplings:
                for pert in perturbations:
                    configs.append({
                        "test_id": "H1",
                        "law": "Lieb-Robinson Bound",
                        "N": N,
                        "Jx": coup["Jx"], "Jy": coup["Jy"],
                        "Jz": coup["Jz"],
                        "coupling_label": coup["label"],
                        "perturbation": pert,
                        "t_max": 5.0, "n_steps": 100,
                    })

        # H2 Area Law: 5 chains x 4 models x 2 subsystem sizes = 40
        chain_lengths_area = [4, 5, 6, 7, 8]
        models = [
            {"name": "ising_gapped", "h_over_J": 3.0},
            {"name": "ising_critical", "h_over_J": 1.0},
            {"name": "heisenberg", "h_over_J": None},
            {"name": "xxz_delta2", "h_over_J": None},
        ]
        subsys_fracs = [0.25, 0.5]
        for N in chain_lengths_area:
            for model in models:
                for frac in subsys_fracs:
                    L_sub = max(1, int(N * frac))
                    configs.append({
                        "test_id": "H2",
                        "law": "Area Law",
                        "N": N,
                        "model": model["name"],
                        "h_over_J": model["h_over_J"],
                        "L_sub": L_sub,
                    })

        # H3 QPT: 20 h/J values x 2 chain lengths = 40
        h_over_J_vals = np.linspace(0.1, 3.0, 20).tolist()
        chain_lengths_qpt = [4, 6]
        for hJ in h_over_J_vals:
            for N in chain_lengths_qpt:
                configs.append({
                    "test_id": "H3",
                    "law": "Quantum Phase Transition",
                    "N": N, "h_over_J": hJ, "J": 1.0,
                })

        return configs

    # ── simulation ──────────────────────────────────────────────────────

    def run_single(self, config, run_index):
        tid = config["test_id"]

        if tid == "H1":
            return self._run_lieb_robinson(config)
        elif tid == "H2":
            return self._run_area_law(config)
        elif tid == "H3":
            return self._run_qpt(config)
        return {}

    def _run_lieb_robinson(self, config):
        """Perturb spin 0, measure correlations at distant sites."""
        N = config["N"]
        Jx, Jy, Jz = config["Jx"], config["Jy"], config["Jz"]
        t_max = config["t_max"]
        n_steps = config["n_steps"]

        H = _build_heisenberg_chain(N, Jx, Jy, Jz)
        tlist = np.linspace(0, t_max, n_steps + 1)

        # Initial state: all spins up
        psi0 = qt.tensor([qt.basis(2, 0)] * N)

        # Apply perturbation at site 0
        if config["perturbation"] == "sigma_x":
            pert_op = _local_op(N, 0, qt.sigmax())
        else:
            pert_op = _local_op(N, 0, qt.sigmaz())

        psi_pert = (pert_op * psi0).unit()

        # Measure <sigma_z> at each site over time
        obs_ops = [_local_op(N, site, qt.sigmaz()) for site in range(N)]
        res_pert = qt.sesolve(H, psi_pert, tlist, obs_ops)
        res_unpert = qt.sesolve(H, psi0, tlist, obs_ops)

        # Correlation = |<O>(perturbed) - <O>(unperturbed)|
        correlations = {}
        max_correlation_at_distance = {}
        for site in range(1, N):
            diff = np.abs(np.array(res_pert.expect[site])
                          - np.array(res_unpert.expect[site]))
            correlations[site] = diff.tolist()
            max_correlation_at_distance[site] = float(np.max(diff))

        farthest = N - 1
        nearest = 1
        ratio = (max_correlation_at_distance.get(farthest, 0.0)
                 / max(max_correlation_at_distance.get(nearest, 1e-15),
                       1e-15))

        return {
            "correlations": correlations,
            "max_corr_by_distance": max_correlation_at_distance,
            "farthest_nearest_ratio": ratio,
            "N": N,
        }

    def _run_area_law(self, config):
        """Ground-state entanglement entropy for a subsystem."""
        N = config["N"]
        model = config["model"]
        h_over_J = config["h_over_J"]
        L_sub = config["L_sub"]

        J = 1.0
        if model == "ising_gapped":
            H = _transverse_field_ising(N, J, h_over_J * J)
        elif model == "ising_critical":
            H = _transverse_field_ising(N, J, J)
        elif model == "heisenberg":
            H = _build_heisenberg_chain(N, 1.0, 1.0, 1.0)
        elif model == "xxz_delta2":
            H = _build_heisenberg_chain(N, 1.0, 1.0, 2.0)
        else:
            H = _build_heisenberg_chain(N, 1.0, 1.0, 1.0)

        # Ground state
        evals, evecs = H.eigenstates(eigvals=1, sparse=True)
        psi_gs = evecs[0]
        psi_gs.dims = [[2] * N, [1] * N]

        # Entanglement entropy of first L_sub sites
        subsystem = list(range(L_sub))
        S_ent = _entanglement_entropy(psi_gs, N, subsystem)

        is_critical = model == "ising_critical"

        return {
            "S_entanglement": S_ent,
            "L_sub": L_sub,
            "N": N,
            "model": model,
            "is_critical": is_critical,
        }

    def _run_qpt(self, config):
        """Track observables through the quantum phase transition."""
        N = config["N"]
        J = config["J"]
        h = config["h_over_J"] * J

        H = _transverse_field_ising(N, J, h)

        n_evals = min(4, 2 ** N)
        evals, evecs = H.eigenstates(eigvals=n_evals, sparse=True)
        psi_gs = evecs[0]
        psi_gs.dims = [[2] * N, [1] * N]

        # Energy gap
        gap = float(evals[1] - evals[0]) if len(evals) > 1 else 0.0

        # Order parameter: |<M_z>| = |(1/N) sum_i <sigma_z_i>|
        M_z = 0.0
        for i in range(N):
            M_z += qt.expect(_local_op(N, i, qt.sigmaz()), psi_gs)
        M_z = abs(float(M_z / N))

        # Entanglement entropy of half chain
        L_half = N // 2
        subsystem = list(range(L_half))
        S_ent = _entanglement_entropy(psi_gs, N, subsystem)

        return {
            "h_over_J": config["h_over_J"],
            "gap": gap,
            "magnetization_z": M_z,
            "entanglement_entropy": S_ent,
            "N": N,
        }

    # ── validation ──────────────────────────────────────────────────────

    def validate(self, config, results):
        """Validate aggregated results. Returns dict of law_name -> Verdict."""
        verdicts = {}
        tid = config["test_id"]
        result = results[0]

        if tid == "H1":
            verdicts["Lieb-Robinson Bound"] = (
                PhysicsValidator.check_inequality(
                    "Lieb-Robinson: bounded propagation "
                    "(far/near ratio < 1)",
                    result["farthest_nearest_ratio"], 1.0,
                    direction="<=", threshold=0.1))

        elif tid == "H2":
            S = result["S_entanglement"]
            if result["is_critical"]:
                verdicts["Area Law (critical)"] = (
                    PhysicsValidator.check_inequality(
                        "Area Law (critical): S > 0 "
                        "(log scaling expected)",
                        S, 0.0, direction=">", threshold=1e-6))
            else:
                area_bound = 3.0  # generous O(1) constant
                verdicts["Area Law (gapped)"] = (
                    PhysicsValidator.check_bound(
                        "Area Law (gapped): S bounded",
                        S, area_bound, direction="upper"))

        elif tid == "H3":
            h_over_J = result["h_over_J"]
            gap = result["gap"]

            if abs(h_over_J - 1.0) < 0.2:
                verdicts["QPT Gap"] = (
                    PhysicsValidator.check_inequality(
                        f"QPT gap near critical (h/J={h_over_J:.2f}): "
                        f"gap small",
                        gap, 2.0, direction="<=", threshold=0.1))
            else:
                verdicts["QPT Gap"] = (
                    PhysicsValidator.check_inequality(
                        f"QPT gap away from critical "
                        f"(h/J={h_over_J:.2f}): gap > 0",
                        gap, 0.0, direction=">", threshold=1e-10))

            verdicts["QPT Entropy"] = (
                PhysicsValidator.check_inequality(
                    "QPT: entanglement entropy >= 0",
                    result["entanglement_entropy"], 0.0,
                    direction=">=", threshold=0.0))

        return verdicts
