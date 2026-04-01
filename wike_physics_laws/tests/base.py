"""
WIKE Physics Laws Simulation Suite - Abstract Base Test Category
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6
"""

import time
from abc import ABC, abstractmethod


class PhysicsTestCategory(ABC):
    """Abstract base class for a category of physics-law tests."""

    @property
    @abstractmethod
    def category_name(self):
        """Human-readable name for this category (e.g., 'Thermodynamics')."""
        ...

    @property
    @abstractmethod
    def category_id(self):
        """Machine-friendly identifier (e.g., 'thermodynamics')."""
        ...

    @property
    @abstractmethod
    def description(self):
        """Short description of what this category tests."""
        ...

    @abstractmethod
    def get_configs(self):
        """Return a list of configuration dicts for the test sweeps.

        Each dict should contain the parameters needed by run_single().
        """
        ...

    @abstractmethod
    def run_single(self, config, run_index):
        """Execute a single simulation run.

        Args:
            config: dict from get_configs()
            run_index: integer index of this run (0-based)

        Returns:
            dict of raw simulation results
        """
        ...

    @abstractmethod
    def validate(self, config, results):
        """Validate aggregated results against physics laws.

        Args:
            config: the configuration dict for this sweep
            results: list of dicts returned by run_single()

        Returns:
            dict mapping law names to Verdict objects (or verdict dicts)
        """
        ...

    def run_all(self, n_runs=1000, verbose=True):
        """Run all configurations and return a flat list of verdict dicts.

        Args:
            n_runs: number of simulation runs per configuration
            verbose: if True, print progress and timing info

        Returns:
            list of verdict dicts (each from Verdict.to_dict())
        """
        configs = self.get_configs()
        all_verdicts = []
        category_pass = 0
        category_fail = 0
        category_start = time.time()

        if verbose:
            print(f"\n{'='*70}")
            print(f"  CATEGORY: {self.category_name}")
            print(f"  {self.description}")
            print(f"  Configs: {len(configs)} | Runs per config: {n_runs}")
            print(f"{'='*70}")

        for cfg_idx, config in enumerate(configs):
            cfg_start = time.time()

            # Execute simulation runs
            results = []
            for run_idx in range(n_runs):
                result = self.run_single(config, run_idx)
                results.append(result)

            # Validate against physics laws
            verdicts = self.validate(config, results)

            cfg_elapsed = time.time() - cfg_start

            # Process verdicts
            for law_name, verdict in verdicts.items():
                if hasattr(verdict, "to_dict"):
                    vdict = verdict.to_dict()
                else:
                    vdict = verdict

                vdict["category"] = self.category_id
                vdict["config_index"] = cfg_idx
                vdict["config"] = config

                if vdict.get("passed", False):
                    category_pass += 1
                    status = "PASS"
                else:
                    category_fail += 1
                    status = "FAIL"

                if verbose:
                    marker = "[PASS]" if status == "PASS" else "[FAIL]"
                    print(f"  {marker} {vdict.get('law_name', law_name)}"
                          f"  (rel_err={vdict.get('relative_error', 0.0):.6f})")
                    if status == "FAIL":
                        print(f"         Details: {vdict.get('details', '')}")

                all_verdicts.append(vdict)

            if verbose:
                print(f"  --- Config {cfg_idx+1}/{len(configs)} done "
                      f"in {cfg_elapsed:.2f}s ---")

        category_elapsed = time.time() - category_start
        total = category_pass + category_fail

        if verbose:
            print(f"\n  {'-'*50}")
            print(f"  CATEGORY SUMMARY: {self.category_name}")
            print(f"  Total checks: {total} | "
                  f"PASS: {category_pass} | FAIL: {category_fail}")
            if total > 0:
                pct = 100.0 * category_pass / total
                print(f"  Pass rate: {pct:.1f}%")
            print(f"  Time: {category_elapsed:.2f}s")
            print(f"  {'-'*50}\n")

        return all_verdicts
