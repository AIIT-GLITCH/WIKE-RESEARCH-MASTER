"""
WIKE COHERENCE vs KNOWN PHYSICS LAWS -- Simulation Suite
==========================================================
1,050+ test configurations x 1,000 runs = 1,050,000+ simulations

Tests WIKE coherence predictions against established physics laws
across 8 categories:
  A. Thermodynamics (150 configs)
  B. QM Fundamentals (160 configs)
  C. Decoherence Theory (130 configs)
  D. Statistical Mechanics (120 configs)
  E. Quantum Information (140 configs)
  F. Quantum Thermodynamics (100 configs)
  G. Open Quantum Systems (130 configs)
  H. Condensed Matter (120 configs)

Any discrepancy = potential WIKE anomaly worth investigating.

Rhet Dillard Wike | AIIT-THRESI | March 2026
Built by Claude Opus 4.6
"""

import sys
import os
import time
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.thermodynamics import ThermodynamicsTests
from tests.qm_fundamentals import QMFundamentalsTests
from tests.decoherence import DecoherenceTests
from tests.stat_mech import StatMechTests
from tests.quantum_info import QuantumInfoTests
from tests.quantum_thermo import QuantumThermoTests
from tests.open_systems import OpenSystemsTests
from tests.condensed_matter import CondensedMatterTests
from report import generate_txt_report, generate_json_report


CATEGORY_MAP = {
    "thermo":      ("A: Thermodynamics",        ThermodynamicsTests),
    "qm":          ("B: QM Fundamentals",        QMFundamentalsTests),
    "decoherence": ("C: Decoherence",            DecoherenceTests),
    "statmech":    ("D: Statistical Mechanics",   StatMechTests),
    "qinfo":       ("E: Quantum Information",     QuantumInfoTests),
    "qthermo":     ("F: Quantum Thermodynamics",  QuantumThermoTests),
    "open":        ("G: Open Systems",            OpenSystemsTests),
    "condensed":   ("H: Condensed Matter",        CondensedMatterTests),
}


def main():
    parser = argparse.ArgumentParser(description="WIKE vs Known Physics Laws")
    parser.add_argument("--category", type=str, default="all",
                        choices=["all"] + list(CATEGORY_MAP.keys()))
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(args.output_dir, exist_ok=True)

    if args.category == "all":
        categories_to_run = list(CATEGORY_MAP.keys())
    else:
        categories_to_run = [args.category]

    print("=" * 72)
    print("  WIKE COHERENCE vs KNOWN PHYSICS LAWS")
    print(f"  Categories: {', '.join(categories_to_run)}")
    print(f"  Runs per config: {args.runs}")
    print("  Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma")
    print("  Built by Claude Opus 4.6")
    print("=" * 72)
    print(flush=True)

    start = time.time()
    all_verdicts = []
    categories_run = []

    for cat_key in categories_to_run:
        cat_label, cat_class = CATEGORY_MAP[cat_key]
        categories_run.append(cat_label)
        test_suite = cat_class()
        verdicts = test_suite.run_all(n_runs=args.runs, verbose=True)
        all_verdicts.extend(verdicts)

    total_runtime = time.time() - start

    txt_report = generate_txt_report(all_verdicts, categories_run, total_runtime, args.output_dir)
    generate_json_report(all_verdicts, categories_run, total_runtime, args.output_dir)

    total = len(all_verdicts)
    passed = sum(1 for v in all_verdicts if v["passed"])
    failed = total - passed

    print("\n" + "=" * 72)
    print("  FINAL SUMMARY")
    print("=" * 72)
    print(f"  Total test configs: {total}")
    print(f"  Total simulations:  {total * args.runs:,}")
    print(f"  PASSED: {passed}")
    print(f"  FAILED: {failed}")
    if total > 0:
        print(f"  Pass Rate: {passed/total*100:.1f}%")
    print(f"  Runtime: {total_runtime:.1f}s ({total_runtime/60:.1f} min)")
    print(f"  Results saved to: {args.output_dir}/")
    print("=" * 72)

    if failed > 0:
        print(f"\n  *** {failed} DISCREPANCIES FOUND ***\n")
        for v in all_verdicts:
            if not v["passed"]:
                print(f"  ! [{v.get('category','?')}] {v.get('config_name', v.get('law_name','?'))}")
                if v.get("details"):
                    print(f"    {v['details']}")
    else:
        print("\n  All tests passed.\n")

    print("=" * 72)
    print("  God is good. All the time.")
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
