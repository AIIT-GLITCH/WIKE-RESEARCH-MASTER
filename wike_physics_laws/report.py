"""
WIKE Physics Laws Simulation Suite - Report Generation
Author: Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma
Builder: Claude Opus 4.6
"""

import json
import os
from datetime import datetime


HEADER = "WIKE COHERENCE vs KNOWN PHYSICS LAWS"
AUTHOR = "Rhet Dillard Wike | AIIT-THRESI | Bristow, Oklahoma"
BUILDER = "Claude Opus 4.6"
FOOTER = "God is good. All the time."


def _group_by_category(all_verdicts):
    """Group verdict dicts by their 'category' key."""
    grouped = {}
    for v in all_verdicts:
        cat = v.get("category", "unknown")
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(v)
    return grouped


def _compute_summary(verdicts):
    """Compute pass/fail counts from a list of verdict dicts."""
    total = len(verdicts)
    passed = sum(1 for v in verdicts if v.get("passed", False))
    failed = total - passed
    return total, passed, failed


def generate_txt_report(all_verdicts, categories_run, total_runtime, output_dir):
    """Write a human-readable text report to RESULTS_PHYSICS_LAWS.txt.

    Args:
        all_verdicts: list of verdict dicts
        categories_run: list of category names/ids that were executed
        total_runtime: total wall-clock time in seconds
        output_dir: directory in which to write the report
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "RESULTS_PHYSICS_LAWS.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    grouped = _group_by_category(all_verdicts)
    overall_total, overall_pass, overall_fail = _compute_summary(all_verdicts)

    lines = []
    lines.append("=" * 72)
    lines.append(f"  {HEADER}")
    lines.append("=" * 72)
    lines.append(f"  Author:    {AUTHOR}")
    lines.append(f"  Builder:   {BUILDER}")
    lines.append(f"  Generated: {timestamp}")
    lines.append(f"  Runtime:   {total_runtime:.2f}s")
    lines.append(f"  Categories tested: {', '.join(categories_run)}")
    lines.append("=" * 72)
    lines.append("")

    # Overall summary
    lines.append(f"  OVERALL: {overall_pass}/{overall_total} checks passed"
                 f"  |  {overall_fail} discrepancies")
    if overall_total > 0:
        pct = 100.0 * overall_pass / overall_total
        lines.append(f"  Pass rate: {pct:.1f}%")
    lines.append("")

    # Per-category breakdown
    for cat in categories_run:
        cat_verdicts = grouped.get(cat, [])
        cat_total, cat_pass, cat_fail = _compute_summary(cat_verdicts)

        lines.append("-" * 72)
        lines.append(f"  CATEGORY: {cat}")
        lines.append(f"  Checks: {cat_total} | PASS: {cat_pass} | FAIL: {cat_fail}")
        lines.append("-" * 72)

        for v in cat_verdicts:
            status = "[PASS]" if v.get("passed", False) else "[FAIL]"
            law = v.get("law_name", "unknown")
            rel_err = v.get("relative_error", 0.0)
            lines.append(f"    {status} {law}  (rel_err={rel_err:.6f})")

        # List discrepancies
        failures = [v for v in cat_verdicts if not v.get("passed", False)]
        if failures:
            lines.append("")
            lines.append(f"  Discrepancies in {cat}:")
            for v in failures:
                law = v.get("law_name", "unknown")
                details = v.get("details", "")
                wike_dev = v.get("wike_deviation", 0.0)
                lines.append(f"    - {law}: {details}")
                lines.append(f"      WIKE deviation: {wike_dev:.6g}")

        lines.append("")

    # Footer
    lines.append("=" * 72)
    lines.append(f"  {FOOTER}")
    lines.append("=" * 72)
    lines.append("")

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

    return filepath


def generate_json_report(all_verdicts, categories_run, total_runtime, output_dir):
    """Write a machine-readable JSON report to RESULTS_PHYSICS_LAWS.json.

    Args:
        all_verdicts: list of verdict dicts
        categories_run: list of category names/ids that were executed
        total_runtime: total wall-clock time in seconds
        output_dir: directory in which to write the report
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "RESULTS_PHYSICS_LAWS.json")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    grouped = _group_by_category(all_verdicts)
    overall_total, overall_pass, overall_fail = _compute_summary(all_verdicts)

    # Build category summaries
    category_details = {}
    for cat in categories_run:
        cat_verdicts = grouped.get(cat, [])
        cat_total, cat_pass, cat_fail = _compute_summary(cat_verdicts)
        discrepancies = [
            {
                "law_name": v.get("law_name"),
                "details": v.get("details"),
                "relative_error": v.get("relative_error"),
                "wike_deviation": v.get("wike_deviation"),
            }
            for v in cat_verdicts if not v.get("passed", False)
        ]
        category_details[cat] = {
            "total_checks": cat_total,
            "passed": cat_pass,
            "failed": cat_fail,
            "pass_rate": (100.0 * cat_pass / cat_total) if cat_total > 0 else 0.0,
            "discrepancies": discrepancies,
            "verdicts": _serialize_verdicts(cat_verdicts),
        }

    report = {
        "header": HEADER,
        "author": AUTHOR,
        "builder": BUILDER,
        "timestamp": timestamp,
        "runtime_seconds": round(total_runtime, 3),
        "categories_run": categories_run,
        "overall": {
            "total_checks": overall_total,
            "passed": overall_pass,
            "failed": overall_fail,
            "pass_rate": (100.0 * overall_pass / overall_total)
                         if overall_total > 0 else 0.0,
        },
        "categories": category_details,
        "footer": FOOTER,
    }

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, default=str)

    return filepath


def _serialize_verdicts(verdicts):
    """Make verdict dicts JSON-safe by converting non-serializable values."""
    safe = []
    for v in verdicts:
        entry = {}
        for k, val in v.items():
            try:
                json.dumps(val)
                entry[k] = val
            except (TypeError, ValueError):
                entry[k] = str(val)
        safe.append(entry)
    return safe
