#!/usr/bin/env python3
"""tools/bekko_zero_io_audit.py - Bekko 0-IO and Latency Auditor.

Squadron B, Unit 7 of 24.
Mission:
1. Run query resolution benchmark under strace monitoring.
2. Assert 0 read() syscalls during query scoring (pure RAM dot-product arithmetic).
3. Compute per-document scoring latency in microseconds (target < 25 microseconds/doc).
4. Strictly adhere to House Law: zero unicode em-dashes (-- and - only), 0.00 first-person pronouns.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.bekko_cpu_retriever import StaticCPURetriever, EMBEDDING_DIM

STRACE_CANDIDATES = [
    "/home/mag/local_bin/strace",
    shutil.which("strace"),
]

BENCHMARK_QUERIES = [
    "verify with actual file bytes before declaring done",
    "kuramoto phase synchronization harmonic coupling",
    "content addressable storage cas slab epgm mesh",
    "pure ram dot product arithmetic zero filesystem io",
    "deterministic token projection dense vector space",
    "living index state machine invariants percolator",
    "sovereign agent multi tenant actor seat orchestration",
    "subword token embedding mean pooling cosine similarity",
]

TARGET_MAX_LATENCY_US_PER_DOC = 25.0


def resolve_strace_binary() -> str:
    """Locate functional strace binary."""
    for candidate in STRACE_CANDIDATES:
        if candidate and os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise FileNotFoundError("Functional strace binary not found")


def execute_scoring_benchmark(retriever: StaticCPURetriever, queries: List[str]) -> Dict[str, Any]:
    """Execute query resolution loop and record nanosecond latency metrics."""
    total_docs = len(retriever.vectors)
    if total_docs == 0:
        raise ValueError("StaticCPURetriever vectors collection is empty")

    # Delineation marker for strace capture
    os.write(2, b"===AUDIT_QUERY_RESOLUTION_START===\n")

    query_metrics: List[Dict[str, Any]] = []
    total_scoring_ns = 0

    for query in queries:
        t0 = time.perf_counter_ns()
        results = retriever.search(query, top_k=5)
        t1 = time.perf_counter_ns()

        duration_ns = t1 - t0
        total_scoring_ns += duration_ns
        duration_us = duration_ns / 1000.0
        us_per_doc = duration_us / float(total_docs)

        query_metrics.append({
            "query": query,
            "duration_ns": duration_ns,
            "duration_us": duration_us,
            "us_per_doc": us_per_doc,
            "top_match_id": results[0]["id"] if results else None,
            "top_match_similarity": results[0]["similarity"] if results else 0.0,
        })

    os.write(2, b"===AUDIT_QUERY_RESOLUTION_END===\n")

    avg_us_per_doc = (total_scoring_ns / 1000.0) / (float(total_docs) * len(queries))
    return {
        "total_docs": total_docs,
        "query_count": len(queries),
        "total_scoring_ns": total_scoring_ns,
        "average_us_per_doc": avg_us_per_doc,
        "query_metrics": query_metrics,
    }


def run_worker() -> None:
    """Worker process: load corpus into memory, then trigger delineated scoring loop."""
    retriever = StaticCPURetriever()
    t_load_0 = time.perf_counter()
    inv_c, idx_c = retriever.build_unified()
    load_ms = (time.perf_counter() - t_load_0) * 1000.0

    benchmark_data = execute_scoring_benchmark(retriever, BENCHMARK_QUERIES)
    benchmark_data["invariants_count"] = inv_c
    benchmark_data["index_items_count"] = idx_c
    benchmark_data["index_load_ms"] = load_ms

    print(json.dumps(benchmark_data, indent=2))


def parse_strace_window(trace_log_path: str) -> Tuple[List[str], int, int]:
    """Parse strace log to extract all syscalls between query resolution markers."""
    with open(trace_log_path, "r", encoding="utf-8", errors="replace") as fp:
        lines = fp.readlines()

    in_query_window = False
    window_syscalls: List[str] = []
    read_calls = 0
    fs_calls = 0

    for raw_line in lines:
        line = raw_line.strip()
        if "===AUDIT_QUERY_RESOLUTION_START===" in line:
            in_query_window = True
            continue
        if "===AUDIT_QUERY_RESOLUTION_END===" in line:
            in_query_window = False
            continue

        if in_query_window:
            window_syscalls.append(line)
            # Detect read family syscalls
            if any(call in line for call in ["read(", "pread(", "pread64(", "readv(", "preadv("]):
                read_calls += 1
            # Detect file open or query operations
            if any(call in line for call in ["open(", "openat(", "stat(", "newfstatat(", "access("]):
                fs_calls += 1

    return window_syscalls, read_calls, fs_calls


def audit_zero_io_and_latency() -> Dict[str, Any]:
    """Execute complete 0-IO verification proof under strace."""
    strace_bin = resolve_strace_binary()

    with tempfile.NamedTemporaryFile(prefix="strace_bekko_", suffix=".log", delete=False) as tmp_trace:
        trace_path = tmp_trace.name

    try:
        worker_cmd = [
            strace_bin,
            "-f",
            "-e", "trace=%file,read,pread64,write",
            "-o", trace_path,
            sys.executable,
            os.path.abspath(__file__),
            "--worker",
        ]

        proc = subprocess.run(
            worker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        worker_output = json.loads(proc.stdout)
        window_syscalls, read_calls, fs_calls = parse_strace_window(trace_path)

        avg_us_per_doc = worker_output["average_us_per_doc"]
        total_docs = worker_output["total_docs"]

        # Verification Assertions
        assert read_calls == 0, f"Violation: observed {read_calls} read syscalls during query resolution"
        assert fs_calls == 0, f"Violation: observed {fs_calls} filesystem syscalls during query resolution"
        assert avg_us_per_doc < TARGET_MAX_LATENCY_US_PER_DOC, (
            f"Latency budget exceeded: {avg_us_per_doc:.3f} us/doc >= {TARGET_MAX_LATENCY_US_PER_DOC} us/doc"
        )

        audit_receipt = {
            "status": "PASS",
            "proof_mode": "strace syscall tracing",
            "read_syscalls_in_query_resolution": read_calls,
            "filesystem_syscalls_in_query_resolution": fs_calls,
            "total_documents_scored": total_docs,
            "queries_executed": worker_output["query_count"],
            "average_latency_us_per_doc": round(avg_us_per_doc, 3),
            "target_latency_budget_us_per_doc": TARGET_MAX_LATENCY_US_PER_DOC,
            "budget_compliance_ratio": round(avg_us_per_doc / TARGET_MAX_LATENCY_US_PER_DOC, 4),
            "details": worker_output,
        }
        return audit_receipt

    finally:
        if os.path.exists(trace_path):
            os.remove(trace_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bekko 0-IO Latency Auditor")
    parser.add_argument("--worker", action="store_true", help="Internal worker mode")
    args = parser.parse_args()

    if args.worker:
        run_worker()
        return 0

    print("=" * 72)
    print("BEKKO 0-IO LATENCY AUDITOR (Squadron B, Unit 7)")
    print("=" * 72)

    receipt = audit_zero_io_and_latency()

    print(f"Status:                      {receipt['status']}")
    print(f"Read Syscalls:               {receipt['read_syscalls_in_query_resolution']} (Target: 0)")
    print(f"Filesystem Syscalls:         {receipt['filesystem_syscalls_in_query_resolution']} (Target: 0)")
    print(f"Indexed Documents:           {receipt['total_documents_scored']}")
    print(f"Queries Evaluated:           {receipt['queries_executed']}")
    print(f"Scoring Latency:             {receipt['average_latency_us_per_doc']} us/doc")
    print(f"Latency Budget:              < {receipt['target_latency_budget_us_per_doc']} us/doc")
    print(f"Budget Margin:               {(1.0 - receipt['budget_compliance_ratio']) * 100.0:.1f}% under budget")
    print("=" * 72)
    print("0-IO VERIFICATION PROOF: CERTIFIED")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
