"""code_swarm tests (SWARM-1 lane, 2026-10-01).

Covers the manifest builder (sha-stamped inline bytes, byte-identical
contract across families, truncation, grid filter) and the convergence
rollup (REAL vs CO-LOCATION vs UNIQUE, out-of-range cite grading). No real
API fires anywhere in this file: everything tested is offline.
"""
from __future__ import annotations

import json

import pytest

from tools import code_swarm as cs
from tools import model_garden as mg


@pytest.fixture
def estate(tmp_path, monkeypatch):
    """Synthetic mini-estate: cs/mg ROOT + OUT_DIR + grid pointed at tmp."""
    monkeypatch.setattr(cs, "ROOT", tmp_path)
    monkeypatch.setattr(mg, "ROOT", tmp_path)
    monkeypatch.setattr(cs, "GARDEN", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(cs, "SWEEP_GRID",
                        tmp_path / "watch" / "inbox" / "model_garden"
                        / "dollar_burn" / "sweep_grid.json")
    monkeypatch.setattr(mg, "OUT_DIR", tmp_path / "watch" / "inbox" / "model_garden")
    monkeypatch.setattr(mg, "USAGE",
                        tmp_path / "memory" / "runs" / "model_garden" / "usage.jsonl")
    (tmp_path / "mag").mkdir()
    (tmp_path / "mag" / "lane_x.py").write_text(
        "import os\n" * 40, encoding="utf-8")
    return tmp_path


# --- manifest builder ------------------------------------------------------

def test_manifest_stages_sha_stamped_identical_contracts(estate):
    rows = cs.build_manifest("t1", ["mag/lane_x.py"], ["kimi", "glm-flash"])
    assert len(rows) == 2
    contracts = {}
    for r in rows:
        meta = json.loads((estate / r["ask_dir"] / "ask.json").read_text(
            encoding="utf-8"))
        assert meta["id"] == r["ask_id"]
        assert meta["evidence"] == [] and meta["self_contained"] is True
        assert f"<SOURCE path=mag/lane_x.py sha256={r['sha256']} lines=40>" \
            in meta["contract"]
        contracts[r["family"]] = meta["contract"]
        assert r["lines"] == 40 and r["truncated"] is False
    # G2 law: the same ask bytes across families, diffs attribute to family
    assert contracts["kimi"] == contracts["glm-flash"]
    # inference_budget recipes ride: each family row records its recipe
    by_fam = {r["family"]: r for r in rows}
    assert by_fam["kimi"]["recipe"] == "kimi"
    assert by_fam["glm-flash"]["recipe"] == "glm-5.3-flash"
    assert by_fam["glm-flash"]["max_tokens"] is None  # uncap law


def test_manifest_truncates_oversized_files(estate):
    big = estate / "mag" / "big.py"
    big.write_text("x = 1\n" * 50_000, encoding="utf-8")  # 300k chars, 50k lines
    rows = cs.build_manifest("t2", ["mag/big.py"], ["deepseek"])
    meta = json.loads((estate / rows[0]["ask_dir"] / "ask.json").read_text(
        encoding="utf-8"))
    assert rows[0]["truncated"] is True
    assert "truncated at" in meta["contract"]
    assert rows[0]["lines"] == 50_000  # true line count survives truncation


def test_triple_violator_grid_filter(estate):
    grid_dir = cs.SWEEP_GRID.parent
    grid_dir.mkdir(parents=True, exist_ok=True)
    no = {"v": "NO-violation"}
    cs.SWEEP_GRID.write_text(json.dumps({
        "mag/a.py": {"verdicts": {"a": no, "b": no, "c": no}},
        "mag/b.py": {"verdicts": {"a": no, "b": no, "c": {"v": "YES"}}},
        "mag/c.py": {"verdicts": {"a": no, "b": {"v": "NA"}, "c": no}},
    }), encoding="utf-8")
    assert cs.load_targets("triple-violators", []) == ["mag/a.py"]


# --- reply grading ---------------------------------------------------------

REPLY = (
    "DEFECT 1: retry loop swallows the exception and banks a fake row | "
    "EVIDENCE: mag/lane_x.py:12 | FIX: re-raise after banking\n"
    "DEFECT 2: missing timeout on the socket | EVIDENCE: mag/lane_x.py:8 | "
    "FIX: add timeout=30\n"
    "DEAD-CODE: legacy flag never read | EVIDENCE: mag/lane_x.py:3\n"
    "ONE-SITTING FIX: wrap the ledger append in tmp+replace | "
    "EVIDENCE: mag/lane_x.py:5\n")


def test_parse_reply_grades_clean_shape():
    g = cs.parse_reply(REPLY, "mag/lane_x.py", 40)
    assert all(g["checks"].values())
    assert len(g["defects"]) == 2
    assert g["defects"][0]["start"] == 12
    assert "fake row" in g["defects"][0]["claim"]


def test_parse_reply_flags_out_of_range_wrong_path_emdash_extra_line():
    bad = REPLY.replace("lane_x.py:8", "lane_x.py:888") \
               .replace("lane_x.py:3", "other.py:3") + \
        "PRAISE: this file is great\nNOTE: extra line one\nNOTE: extra line two\n"
    bad = bad.replace("FIX: add", "FIX: add an \u2014 em dash")
    g = cs.parse_reply(bad, "mag/lane_x.py", 40)
    assert g["checks"]["shape"] is False        # PRAISE/NOTE lines break shape
    assert g["checks"]["lines_in_range"] is False  # 888 > 40 lines
    assert g["checks"]["cites_resolve"] is False   # other.py is not the target
    assert g["checks"]["no_em_dash"] is False
    assert g["checks"]["max_lines"] is False       # 4 shape lines + 3 junk = 7


# --- convergence rollup ----------------------------------------------------

def _graded(file, family, defects):
    return {"file": file, "family": family, "ok": True,
            "defects": [{"claim": c, "start": s, "nums": [s], "path_ok": True,
                         "lines_ok": True, "raw": ""} for c, s in defects]}


def test_converge_real_needs_two_families_same_claim_region():
    clusters = cs.converge([
        _graded("f.py", "kimi",
                [("retry loop swallows exceptions silently", 12)]),
        _graded("f.py", "deepseek",
                [("the retry swallows the exception and hides it", 14)]),
        _graded("f.py", "glm-flash", [("unrelated other thing entirely", 200)]),
    ])
    by_status = {c["status"] for c in clusters}
    real = [c for c in clusters if c["status"] == "REAL"]
    assert by_status == {"REAL", "UNIQUE"}
    assert real[0]["n_families"] == 2 and real[0]["lines"] == [12, 14]


def test_converge_colocation_when_claims_disagree_lexically():
    clusters = cs.converge([
        _graded("f.py", "kimi", [("race on the shared counter", 30)]),
        _graded("f.py", "glm-flash", [("hardcoded credential in the url", 33)]),
    ])
    assert clusters[0]["status"] == "CO-LOCATION"  # window overlaps, not claims


def test_converge_single_family_is_unique_even_repeated():
    clusters = cs.converge([
        _graded("f.py", "deepseek", [("defect alpha", 5), ("defect beta", 6)]),
    ])
    assert all(c["status"] == "UNIQUE" and c["n_families"] == 1
               for c in clusters)


def test_converge_window_far_apart_never_clusters():
    clusters = cs.converge([
        _graded("f.py", "kimi", [("timeout missing on socket", 20)]),
        _graded("f.py", "deepseek", [("timeout missing on socket", 90)]),
    ])
    assert all(c["status"] == "UNIQUE" for c in clusters)
