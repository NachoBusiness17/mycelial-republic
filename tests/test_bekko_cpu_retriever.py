"""tests/test_bekko_cpu_retriever.py - Verification for Bekko CPU Retriever."""
from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.bekko_cpu_retriever import (
    StaticCPURetriever,
    cosine_similarity,
    text_to_embedding,
    token_to_vector,
)


def test_token_vector_determinism():
    v1 = token_to_vector("ledger")
    v2 = token_to_vector("ledger")
    assert v1 == v2
    norm = math.sqrt(sum(x * x for x in v1))
    assert abs(norm - 1.0) < 1e-5


def test_text_embedding_properties():
    emb = text_to_embedding("Miriam walked into the stone archive")
    assert len(emb) == 128
    norm = math.sqrt(sum(x * x for x in emb))
    assert abs(norm - 1.0) < 1e-5


def test_semantic_ranking():
    retriever = StaticCPURetriever()
    retriever.add_document("doc_ledger", "The ledger records every timber and stone purchase in the house.")
    retriever.add_document("doc_wave", "Traveling waves in the circular gallery pulse at frozen motionless nodes.")
    retriever.add_document("doc_map", "The illuminated vellum map lies, but the floor checks the hash.")

    # Search for timber records
    res_timber = retriever.search("timber purchase in the ledger", top_k=2)
    assert res_timber[0]["id"] == "doc_ledger"
    assert res_timber[0]["similarity"] > res_timber[1]["similarity"]

    # Search for wave nodes
    res_wave = retriever.search("standing wave and motionless nodes", top_k=2)
    assert res_wave[0]["id"] == "doc_wave"
    assert res_wave[0]["similarity"] > res_wave[1]["similarity"]

    # Search for lying map
    res_map = retriever.search("the floor verifies the hash when the map lies", top_k=2)
    assert res_map[0]["id"] == "doc_map"
    assert res_map[0]["similarity"] > res_map[1]["similarity"]


def test_cas_mesh_retrieval():
    cas_slabs_dir = os.path.join(ROOT, "memory", "cas", "slabs")
    if not os.path.exists(cas_slabs_dir):
        return
    retriever = StaticCPURetriever()
    count = retriever.build_from_cas(ROOT)
    assert count > 0, "Expected non-zero CAS slab entries"
    # Query CAS vectors
    results = retriever.search("Kuramoto harmonic phase slot synchronization", top_k=3)
    assert len(results) > 0
    assert results[0]["similarity"] > 0.0


def test_em_dash_cleanliness():
    forbidden = ["\u2014", "\u2013"]
    tool_file = os.path.join(ROOT, "tools", "bekko_cpu_retriever.py")
    content = open(tool_file, "r", encoding="utf-8").read()
    for char in forbidden:
        assert char not in content, f"Forbidden unicode dash {repr(char)} found in bekko_cpu_retriever.py"
    audit_file = os.path.join(ROOT, "tools", "bekko_zero_io_audit.py")
    if os.path.exists(audit_file):
        acontent = open(audit_file, "r", encoding="utf-8").read()
        for char in forbidden:
            assert char not in acontent, f"Forbidden unicode dash {repr(char)} found in bekko_zero_io_audit.py"
    test_file = os.path.join(ROOT, "tests", "test_bekko_cpu_retriever.py")
    tcontent = open(test_file, "r", encoding="utf-8").read()
    for char in forbidden:
        assert char not in tcontent, f"Forbidden unicode dash {repr(char)} found in test_bekko_cpu_retriever.py"


def test_zero_io_query_resolution():
    from tools.bekko_zero_io_audit import audit_zero_io_and_latency
    receipt = audit_zero_io_and_latency()
    assert receipt["status"] == "PASS"
    assert receipt["read_syscalls_in_query_resolution"] == 0
    assert receipt["filesystem_syscalls_in_query_resolution"] == 0
    assert receipt["average_latency_us_per_doc"] < 25.0


if __name__ == "__main__":
    test_token_vector_determinism()
    test_text_embedding_properties()
    test_semantic_ranking()
    test_cas_mesh_retrieval()
    test_em_dash_cleanliness()
    test_zero_io_query_resolution()
    print("ALL TESTS PASSED in test_bekko_cpu_retriever.py")
