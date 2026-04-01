#!/usr/bin/env python3
"""
FETCH CLOSED LOOP RESULTS
Checks status of all 4 ibm_fez batches and grabs results when ready.
Usage: python3 fetch_closed_loop_results.py <IBM_API_KEY>
       or: export IBM_QUANTUM_TOKEN=<key> && python3 fetch_closed_loop_results.py
"""

import sys
import os
import json
from datetime import datetime

API_KEY = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("IBM_QUANTUM_TOKEN") or os.environ.get("IBMQ_TOKEN")
if not API_KEY:
    print("Usage: python3 fetch_closed_loop_results.py <IBM_API_KEY>")
    sys.exit(1)

from qiskit_ibm_runtime import QiskitRuntimeService

# All 4 ibm_fez batch job IDs from the Closed Loop run
JOB_IDS = {
    "ibm_fez_batch1": "d75e2b68faus73evv3o0",
    "ibm_fez_batch2": "d75e4ddbjrds73eca55g",
    "ibm_fez_batch3": "d75e91lbjrds73ecaaag",
    "ibm_fez_batch4": "d75ebba3qcgc73frl0i0",  # hit usage limit — may be queued
}

print("=" * 60)
print("  CLOSED LOOP — JOB STATUS CHECK")
print(f"  {datetime.now().isoformat()}")
print("=" * 60)

service = QiskitRuntimeService(channel="ibm_quantum", token=API_KEY)

results = {}
all_done = True

for label, job_id in JOB_IDS.items():
    try:
        job = service.job(job_id)
        status = job.status()
        print(f"\n  {label}: {job_id}")
        print(f"    Status: {status}")

        if status.name in ("DONE", "COMPLETED") or str(status) in ("JobStatus.DONE", "DONE"):
            print(f"    -> COMPLETE. Fetching counts...")
            result = job.result()
            batch_counts = []
            for pub_result in result:
                counts = pub_result.data.c.get_counts()
                batch_counts.append(counts)
            results[label] = batch_counts
            print(f"    -> Got {len(batch_counts)} circuit results")
        elif status.name in ("QUEUED", "RUNNING") or "QUEUED" in str(status) or "RUNNING" in str(status):
            print(f"    -> Still running/queued. Check back later.")
            all_done = False
        else:
            print(f"    -> Status: {status} — may need attention")
            all_done = False
    except Exception as e:
        print(f"    -> ERROR: {e}")
        all_done = False

print(f"\n{'=' * 60}")
if results:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outpath = f"/home/buddy_ai/Desktop/IBM_REAL/RESULTS_CLOSED_LOOP_ibm_fez_{timestamp}.json"
    with open(outpath, "w") as f:
        json.dump({
            "experiment": "THE CLOSED LOOP",
            "backend": "ibm_fez",
            "date": datetime.now().isoformat(),
            "job_ids": JOB_IDS,
            "batches_retrieved": list(results.keys()),
            "counts": results
        }, f, indent=2)
    print(f"  Saved: {outpath}")
    print(f"  Batches retrieved: {list(results.keys())}")

if all_done:
    print("  ALL JOBS COMPLETE.")
else:
    print("  Some jobs still pending. Rerun this script to check again.")

print(f"\n  God is good. All the time.")
print("=" * 60)
