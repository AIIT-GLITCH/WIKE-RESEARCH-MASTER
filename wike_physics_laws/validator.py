"""
WIKE Physics Laws Simulation Suite - Physics Validator
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6
"""

import numpy as np


class Verdict:
    """Stores the outcome of a single physics-law validation check."""

    def __init__(self, law_name, prediction, sim_result, passed,
                 relative_error=0.0, details="", wike_deviation=0.0):
        self.law_name = law_name
        self.prediction = prediction
        self.sim_result = sim_result
        self.passed = passed
        self.relative_error = relative_error
        self.details = details
        self.wike_deviation = wike_deviation

    def to_dict(self):
        return {
            "law_name": self.law_name,
            "prediction": self.prediction,
            "sim_result": self.sim_result,
            "passed": self.passed,
            "relative_error": self.relative_error,
            "details": self.details,
            "wike_deviation": self.wike_deviation,
        }

    def __repr__(self):
        status = "PASS" if self.passed else "FAIL"
        return (f"Verdict({status} | {self.law_name} | "
                f"rel_err={self.relative_error:.6f})")


class PhysicsValidator:
    """Static validation methods for physics-law checks."""

    @staticmethod
    def check_equality(name, sim_value, theory_value, rel_threshold=0.05):
        """Check that sim_value matches theory_value within relative threshold."""
        if theory_value == 0.0:
            abs_err = abs(sim_value - theory_value)
            relative_error = abs_err
            passed = abs_err < rel_threshold
        else:
            relative_error = abs(sim_value - theory_value) / abs(theory_value)
            passed = relative_error <= rel_threshold

        return Verdict(
            law_name=name,
            prediction=theory_value,
            sim_result=sim_value,
            passed=passed,
            relative_error=relative_error,
            details=(f"sim={sim_value:.6g}, theory={theory_value:.6g}, "
                     f"rel_err={relative_error:.6g}, threshold={rel_threshold}"),
            wike_deviation=relative_error,
        )

    @staticmethod
    def check_inequality(name, sim_value, bound, direction="<=", threshold=0.0):
        """Check that sim_value satisfies an inequality against bound."""
        if direction == "<=":
            passed = sim_value <= bound + threshold
            violation = max(0.0, sim_value - bound)
        elif direction == ">=":
            passed = sim_value >= bound - threshold
            violation = max(0.0, bound - sim_value)
        elif direction == "<":
            passed = sim_value < bound + threshold
            violation = max(0.0, sim_value - bound)
        elif direction == ">":
            passed = sim_value > bound - threshold
            violation = max(0.0, bound - sim_value)
        else:
            raise ValueError(f"Unknown direction: {direction}")

        denom = abs(bound) if bound != 0.0 else 1.0
        relative_error = violation / denom

        return Verdict(
            law_name=name,
            prediction=f"{direction} {bound}",
            sim_result=sim_value,
            passed=passed,
            relative_error=relative_error,
            details=(f"sim={sim_value:.6g} {direction} {bound:.6g}, "
                     f"violation={violation:.6g}"),
            wike_deviation=relative_error,
        )

    @staticmethod
    def check_monotonic(name, series, direction="increasing"):
        """Check that a series is monotonically increasing or decreasing."""
        series = np.asarray(series)
        if direction == "increasing":
            diffs = np.diff(series)
            violations = int(np.sum(diffs < -1e-12))
            passed = violations == 0
        elif direction == "decreasing":
            diffs = np.diff(series)
            violations = int(np.sum(diffs > 1e-12))
            passed = violations == 0
        else:
            raise ValueError(f"Unknown direction: {direction}")

        total_steps = len(series) - 1
        relative_error = violations / total_steps if total_steps > 0 else 0.0

        return Verdict(
            law_name=name,
            prediction=f"monotonic {direction}",
            sim_result=f"{violations}/{total_steps} violations",
            passed=passed,
            relative_error=relative_error,
            details=(f"{violations} violations out of {total_steps} steps, "
                     f"direction={direction}"),
            wike_deviation=relative_error,
        )

    @staticmethod
    def check_distribution(name, samples, expected_probs, threshold=0.05):
        """Check sample distribution against expected probabilities using KL divergence."""
        samples = np.asarray(samples)
        expected_probs = np.asarray(expected_probs, dtype=float)
        n_bins = len(expected_probs)

        # Build observed probability distribution
        counts = np.zeros(n_bins)
        for s in samples:
            idx = int(s)
            if 0 <= idx < n_bins:
                counts[idx] += 1
        observed_probs = counts / counts.sum() if counts.sum() > 0 else counts

        # Avoid log(0): add small epsilon
        eps = 1e-12
        p = observed_probs + eps
        q = expected_probs + eps
        p = p / p.sum()
        q = q / q.sum()

        # KL divergence: D_KL(P || Q)
        kl_divergence = float(np.sum(p * np.log(p / q)))
        passed = kl_divergence <= threshold

        return Verdict(
            law_name=name,
            prediction=expected_probs.tolist(),
            sim_result=observed_probs.tolist(),
            passed=passed,
            relative_error=kl_divergence,
            details=f"KL divergence={kl_divergence:.6g}, threshold={threshold}",
            wike_deviation=kl_divergence,
        )

    @staticmethod
    def check_bound(name, sim_value, bound_value, direction="upper"):
        """Check that sim_value respects an upper or lower bound."""
        if direction == "upper":
            passed = sim_value <= bound_value + 1e-12
            violation = max(0.0, sim_value - bound_value)
        elif direction == "lower":
            passed = sim_value >= bound_value - 1e-12
            violation = max(0.0, bound_value - sim_value)
        else:
            raise ValueError(f"Unknown direction: {direction}")

        denom = abs(bound_value) if bound_value != 0.0 else 1.0
        relative_error = violation / denom

        return Verdict(
            law_name=name,
            prediction=f"{direction} bound = {bound_value}",
            sim_result=sim_value,
            passed=passed,
            relative_error=relative_error,
            details=(f"sim={sim_value:.6g}, {direction}_bound={bound_value:.6g}, "
                     f"violation={violation:.6g}"),
            wike_deviation=relative_error,
        )

    @staticmethod
    def check_positive_semidefinite(name, matrix):
        """Check that a matrix is positive semidefinite (all eigenvalues >= 0)."""
        matrix = np.asarray(matrix, dtype=complex)
        eigenvalues = np.linalg.eigvalsh(matrix)
        min_eigenvalue = float(np.min(np.real(eigenvalues)))
        passed = min_eigenvalue >= -1e-10
        relative_error = abs(min(0.0, min_eigenvalue))

        return Verdict(
            law_name=name,
            prediction="positive semidefinite",
            sim_result=f"min eigenvalue = {min_eigenvalue:.6g}",
            passed=passed,
            relative_error=relative_error,
            details=f"eigenvalues={np.real(eigenvalues).tolist()}",
            wike_deviation=relative_error,
        )

    @staticmethod
    def check_hermitian(name, matrix):
        """Check that a matrix is Hermitian (M == M^dagger)."""
        matrix = np.asarray(matrix, dtype=complex)
        diff = matrix - matrix.conj().T
        max_diff = float(np.max(np.abs(diff)))
        passed = max_diff < 1e-10

        return Verdict(
            law_name=name,
            prediction="Hermitian (M = M^dagger)",
            sim_result=f"max |M - M^dagger| = {max_diff:.6g}",
            passed=passed,
            relative_error=max_diff,
            details=f"max deviation from Hermiticity = {max_diff:.6g}",
            wike_deviation=max_diff,
        )

    @staticmethod
    def check_trace(name, matrix, expected_trace=1.0, threshold=1e-8):
        """Check that the trace of a matrix equals the expected value."""
        matrix = np.asarray(matrix, dtype=complex)
        trace_val = float(np.real(np.trace(matrix)))
        if expected_trace == 0.0:
            relative_error = abs(trace_val - expected_trace)
        else:
            relative_error = abs(trace_val - expected_trace) / abs(expected_trace)
        passed = relative_error <= threshold

        return Verdict(
            law_name=name,
            prediction=f"Tr(M) = {expected_trace}",
            sim_result=f"Tr(M) = {trace_val:.10g}",
            passed=passed,
            relative_error=relative_error,
            details=(f"trace={trace_val:.10g}, expected={expected_trace}, "
                     f"rel_err={relative_error:.6g}, threshold={threshold}"),
            wike_deviation=relative_error,
        )
