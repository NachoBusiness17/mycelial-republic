"""Tests for mag.verkle_compaction (card verkle99), design move 4.

Landed BEFORE any --compact --execute CLI wiring exists (the landing gate in
mag/verkle_compaction's docstring): the migration is a tested module, not a
session script. Cases per the card: preflight refusal on a broken chain; fold
of synthetic noise rows among live-shaped rows; counter obligations (count,
folded_root, pre_fold_root, archive sha); prove(counter) verifies; prove() at
an ARCHIVED folded index verifies against the archived pre-fold chain;
idempotence; LF byte law; guard delta obligations; plan() writes nothing.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag import chain_guard, verkle_compaction as vc
from mag import verkle_knot as vk


def _mk_row(sid: str, *, theme: str | None, filename: str | None, ts: str,
            knot_exists: bool = False, evidence_lost: bool = False,
            start: str = "2026-09-11T17:12:00Z", end: str = "2026-09-11T17:42:00Z",
            knots: Path | None = None) -> dict:
    row = {
        "ts": ts,
        "session_id": sid,
        "filename": filename,
        "start_minute": start,
        "end_minute": end,
        "dominant_theme": theme,
        "theme_vector_normalized": [0.0, 0.0, 0.0] if theme is None else [0.5, 0.0, 0.0],
        "tension_index": 0.42,
        "dossier_commit": None,
        "amended": False,
    }
    if evidence_lost:
        row["evidence_lost"] = True
    row["leaf_hash"] = vk._leaf_hash(dict(row))
    if filename and knot_exists and knots is not None:
        (knots / filename).write_text(json.dumps({"session_id": sid}), encoding="utf-8")
    return row


@pytest.fixture()
def folded_env(tmp_path, monkeypatch):
    """A tmp chain shaped like the live one: 3 fold candidates (knot gone),
    1 noise-class row with a LIVE knot (the keep case), themed + tail rows,
    an evolution file, and chain_guard pointed at the same tmp root."""
    chain = tmp_path / "verkle_chain.jsonl"
    tip = tmp_path / "verkle_tip.json"
    knots = tmp_path / "knots"
    knots.mkdir()
    evo = tmp_path / "topic_evolution.json"
    monkeypatch.setattr(vk, "CHAIN", chain)
    monkeypatch.setattr(vk, "TIP", tip)
    monkeypatch.setattr(vk, "KNOTS", knots)
    monkeypatch.setattr(vk, "EVOLUTION", evo)
    monkeypatch.setattr(vk, "LATEST", tmp_path / "latest.knot.json")
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    monkeypatch.setattr(chain_guard, "CHAIN", chain)
    monkeypatch.setattr(chain_guard, "TIP", tip)
    monkeypatch.setattr(chain_guard, "KNOTS", knots)
    monkeypatch.setattr(chain_guard, "MARKER", tmp_path / "verkle_repair_state.json")

    rows = [
        _mk_row("sess-real-1", theme="biography", filename="a.knot.json", ts="2026-09-11T10:00:00Z",
                knot_exists=True, knots=knots,
                start="2026-09-11T10:00:00Z", end="2026-09-11T10:42:00Z"),
        # 3 fold candidates: noise class, knot file absent (evidence gone).
        # Minutes are ZERO-WIDTH and scattered, live-chain-shaped (the live
        # noise rows carry inherited start==end minutes weeks apart).
        _mk_row("mag-agent-orc-t1", theme=None, filename="n1.knot.json", ts="2026-09-11T17:12:00Z",
                evidence_lost=True, start="2026-09-11T17:12:00Z", end="2026-09-11T17:12:00Z"),
        _mk_row("mag-agent-orc-t2", theme=None, filename="n2.knot.json", ts="2026-09-11T18:00:00Z",
                start="2026-09-11T18:00:00Z", end="2026-09-11T18:00:00Z"),
        _mk_row("mag-agent-orc-t3", theme=None, filename="n3.knot.json", ts="2026-09-11T19:00:00Z",
                start="2026-09-11T19:00:00Z", end="2026-09-11T19:00:00Z"),
        # keep case: noise class but the knot is LIVE, never folded
        _mk_row("mag-agent-orc-t4", theme=None, filename="live.knot.json", ts="2026-09-11T20:00:00Z",
                knot_exists=True, knots=knots,
                start="2026-09-11T20:00:00Z", end="2026-09-11T20:00:00Z"),
        # themed orchestrator row: signal, stays
        _mk_row("mag-agent-orc-t5", theme="biography", filename="th.knot.json", ts="2026-09-11T21:00:00Z",
                knot_exists=True, knots=knots,
                start="2026-09-11T21:00:00Z", end="2026-09-11T21:40:00Z"),
        _mk_row("sess-tail", theme="mag_hands", filename="tail.knot.json", ts="2026-09-11T23:00:00Z",
                knot_exists=True, knots=knots,
                start="2026-09-11T22:00:00Z", end="2026-09-11T23:00:00Z"),
    ]
    hashes = [r["leaf_hash"] for r in rows]
    root = vk._merkle_root(hashes)
    # per-row chain fields the way appends write them (verkle_root on the last
    # row is what _verify_chain_consistent's preflight checks)
    for i, r in enumerate(rows):
        r["index"] = i
        r["n_leaves"] = i + 1
        r["parent_verkle_root"] = vk._merkle_root(hashes[:i]) if i else vk._h(b"empty")
        r["verkle_root"] = vk._merkle_root(hashes[:i + 1])
    chain.write_bytes(("\n".join(json.dumps(r) for r in rows) + "\n").encode("utf-8"))
    tip.write_text(json.dumps({"schema": "verkle_tip.v1", "root": root,
                               "n_leaves": len(hashes)}), encoding="utf-8")
    evo.write_text(json.dumps({
        "series": [
            {"index": i, "session_id": r["session_id"],
             "start_minute": r["start_minute"], "dominant_theme": r["dominant_theme"]}
            for i, r in enumerate(rows)
        ],
        "n_leaves": len(rows), "verkle_root": root,
    }), encoding="utf-8")
    return {"chain": chain, "tip": tip, "knots": knots, "evo": evo,
            "rows": rows, "root": root, "tmp_path": tmp_path}


def test_plan_is_read_only_and_reports_both_dispositions(folded_env):
    before = folded_env["chain"].read_bytes()
    p = vc.plan()
    assert p["fold"]["count"] == 3
    assert p["keep"]["count_live_knot"] == 1
    assert p["noise_class_total"] == 4
    assert p["pre_fold_root"] == folded_env["root"]
    assert p["would_be_n_leaves"] == 5  # 7 rows - 3 folded + 1 counter
    assert p["execute"] is False
    assert folded_env["chain"].read_bytes() == before  # plan wrote nothing
    assert not (folded_env["tmp_path"] / "compaction_archive").exists()


def test_apply_execute_false_writes_nothing(folded_env):
    before = folded_env["chain"].read_bytes()
    res = vc.apply(execute=False)
    assert res["ok"] is True and res["changed"] is False and res["execute"] is False
    assert folded_env["chain"].read_bytes() == before
    assert not (folded_env["tmp_path"] / "compaction_archive").exists()
    assert not (folded_env["tmp_path"] / "verkle_repair_state.json").exists()


def test_apply_folds_candidates_and_anchors_archive(folded_env):
    res = vc.apply(execute=True)
    assert res["ok"] is True, res
    assert res["changed"] is True and res["folded"] == 3 and res["kept_rows"] == 5

    new_rows = vk._load_chain_rows()
    counter = next(r for r in new_rows if r.get("session_id") == vc.COUNTER_SESSION_ID)
    assert counter["count"] == 3
    assert counter["pre_fold_root"] == folded_env["root"]
    assert counter["pre_fold_n_leaves"] == 7
    assert counter["first_index"] == 1 and counter["last_index"] == 3
    assert counter["filename"] is None
    # kept rows survived: the live-knot noise row and the themed orc row
    sids = {r["session_id"] for r in new_rows}
    assert {"mag-agent-orc-t4", "mag-agent-orc-t5", "sess-real-1", "sess-tail"} <= sids
    assert not {"mag-agent-orc-t1", "mag-agent-orc-t2", "mag-agent-orc-t3"} & sids
    # tip matches recomputed root
    tip = json.loads(folded_env["tip"].read_text(encoding="utf-8"))
    assert tip["root"] == vk._merkle_root([r["leaf_hash"] for r in new_rows])
    # LF byte law (B2-393)
    assert b"\r" not in folded_env["chain"].read_bytes()
    # archive anchor: root + sha + folded-root witness all match
    anchor = vc.verify_archive_anchor(Path(res["archive_dir"]))
    assert anchor["ok"] is True, anchor
    assert anchor["root_match"] and anchor["sha_match"] and anchor["folded_root_match"]
    assert anchor["folded_count_recomputed"] == 3
    # no duplicate session ids introduced
    sids_list = [r["session_id"] for r in new_rows]
    assert len(sids_list) == len(set(sids_list))


def test_prove_counter_and_prove_archived_folded_leaf(folded_env):
    """Bullet-1 obligation, landed: prove() at an ARCHIVED folded index
    against the archived pre-fold chain, via the estate's own prover."""
    res = vc.apply(execute=True)
    assert res["prove_counter"]["verified"] is True

    arch_dir = Path(res["archive_dir"])
    # folded original indexes were 1..3; prove index 2 (a middle folded leaf)
    for folded_index in (1, 2, 3):
        p = vc.prove_archived_leaf(arch_dir, folded_index)
        assert p["ok"] is True, p
        assert p["verified"] is True
        assert p["root_matches_archive"] is True
        assert p["leaf_hash_is_archived_row"] is True
        assert p["proof_root"] == res["pre_fold_root"]
        # the proven leaf is committed by the live counter's folded witness
        counter = next(r for r in vk._load_chain_rows()
                       if r.get("session_id") == vc.COUNTER_SESSION_ID)
        folded_hashes = [folded_env["rows"][i]["leaf_hash"] for i in (1, 2, 3)]
        import hashlib
        sha = hashlib.sha256("\n".join(folded_hashes).encode("utf-8")).hexdigest()
        assert p["leaf_hash"] in folded_hashes
        assert counter["folded_leaf_hashes_sha256"] == sha
        assert vk._merkle_root(folded_hashes) == counter["folded_root"]


def test_apply_refuses_broken_chain(folded_env):
    rows = vk._load_chain_rows()
    rows[0]["leaf_hash"] = "0" * 64  # tamper: root mismatch at preflight
    folded_env["chain"].write_bytes(
        ("\n".join(json.dumps(r) for r in rows) + "\n").encode("utf-8"))
    before = folded_env["chain"].read_bytes()
    res = vc.apply(execute=True)
    assert res["ok"] is False and res["refused"] is True
    assert folded_env["chain"].read_bytes() == before  # refused = zero writes
    assert not (folded_env["tmp_path"] / "compaction_archive").exists()


def test_plan_and_apply_refuse_v2(folded_env, monkeypatch):
    """AH19 v2 guard (VERKLE_V2_DECISION.md §2.1 + §4 precondition 1, 2026-09-30).

    Compaction REWRITES the chain dropping fold candidates; under chain_mode=v2
    those rows are canonical append-only history, so BOTH entry points refuse
    with the estate's hard-block exit 2 (mirror of verkle_knot.consolidate's
    guard) and write nothing. The fixture chain has 3 real fold candidates —
    the refusal is the only thing stopping the fold, so this is not vacuous.
    """
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V2)
    before = folded_env["chain"].read_bytes()

    p = vc.plan()
    assert p["ok"] is False and p["refused"] is True and p["exit"] == 2
    assert "canonical" in p["reason"] and "v2" in p["reason"]
    assert folded_env["chain"].read_bytes() == before

    res = vc.apply(execute=True)
    assert res["ok"] is False and res["refused"] is True and res["exit"] == 2
    assert res["changed"] is False
    assert folded_env["chain"].read_bytes() == before  # refused = zero writes
    assert not (folded_env["tmp_path"] / "compaction_archive").exists()
    assert len(vk._load_chain_rows()) == 7  # nothing folded, no counter leaf


def test_apply_is_idempotent(folded_env):
    r1 = vc.apply(execute=True)
    assert r1["changed"] is True
    bytes_after_first = folded_env["chain"].read_bytes()
    n_archives_first = len(list((folded_env["tmp_path"] / "compaction_archive").iterdir()))
    r2 = vc.apply(execute=True)
    assert r2["ok"] is True and r2["changed"] is False
    assert folded_env["chain"].read_bytes() == bytes_after_first
    assert len(list((folded_env["tmp_path"] / "compaction_archive").iterdir())) == n_archives_first


def test_guard_delta_obligations(folded_env):
    def counts(rows):
        dang = [r for r in rows if r.get("filename")
                and not (folded_env["knots"] / str(r["filename"])).is_file()]
        flagged = [r for r in rows if r.get("evidence_lost")]
        return (len(dang), len(flagged), len([r for r in dang if not r.get("evidence_lost")]))

    pre = counts(folded_env["rows"])
    res = vc.apply(execute=True)
    post = counts(vk._load_chain_rows())
    # 3 dangling folded (1 flagged + 2 unflagged): exact strict delta, none added
    assert post[0] == pre[0] - 3
    assert post[1] == pre[1] - 1
    assert post[2] == pre[2] - 2
    # canary re-marked at post-fold truth
    marker = json.loads((folded_env["tmp_path"] / "verkle_repair_state.json").read_text(encoding="utf-8"))
    assert marker["evidence_lost_expected"] == post[1]
    assert marker["repair_root"] == res["new_root"][:16]
    # evolution: folded sids dropped, counter sid not added, reindexed
    evo = json.loads(folded_env["evo"].read_text(encoding="utf-8"))
    evo_sids = [s["session_id"] for s in evo["series"]]
    assert not {"mag-agent-orc-t1", "mag-agent-orc-t2", "mag-agent-orc-t3"} & set(evo_sids)
    assert vc.COUNTER_SESSION_ID not in evo_sids
    assert [s["index"] for s in evo["series"]] == list(range(len(evo_sids)))


def test_counter_row_is_never_a_fold_candidate():
    counter = {
        "session_id": vc.COUNTER_SESSION_ID, "dominant_theme": None,
        "theme_vector_normalized": None, "filename": None,
    }
    assert vc.is_fold_candidate(counter) is False
    # a hypothetical future counter WITH a filename whose knot is gone would
    # match the predicate; the null filename is the structural guard
    assert vc.is_fold_candidate({**counter, "filename": "x.knot.json"}) is True


def test_cache_map_theme_attribution_is_fold_invariant(folded_env):
    """The counter must not pose as a session window.

    Regression cause (2026-09-27 live probe, revise_verkle99_consumers_out.txt):
    stitching cand[0].start_minute -> cand[-1].end_minute gave the counter a
    32-DAY window over the live chain's scattered zero-width noise minutes, and
    the cache_map time-window join re-attributed 29,360 remote calls from real
    themes to "unmapped". The fix is a zero-width tombstone minute; this test
    pins the join's by_theme attribution as identical pre-fold vs post-fold.
    """
    from mag import cache_map

    usage = [
        {"ts": "2026-09-11T10:20:00Z", "provider": "deepseek", "ok": True,
         "prompt_tokens": 100, "completion_tokens": 10},
        {"ts": "2026-09-11T17:12:30Z", "provider": "deepseek", "ok": True,
         "prompt_tokens": 50, "completion_tokens": 5},
        {"ts": "2026-09-11T18:30:00Z", "provider": "deepseek", "ok": True,
         "prompt_tokens": 20, "completion_tokens": 2},
        {"ts": "2026-09-11T22:10:00Z", "provider": "deepseek", "ok": True,
         "prompt_tokens": 30, "completion_tokens": 3},
    ]
    pre = cache_map.build_map(usage_rows=usage, chain_rows=folded_env["rows"])
    res = vc.apply(execute=True)
    assert res["changed"] is True
    post_rows = vk._load_chain_rows()
    counter = next(r for r in post_rows if r.get("session_id") == vc.COUNTER_SESSION_ID)
    assert counter["start_minute"] == counter["end_minute"]  # zero-width tombstone
    assert counter["first_start_minute"] == "2026-09-11T17:12:00Z"
    assert counter["last_end_minute"] == "2026-09-11T19:00:00Z"
    post = cache_map.build_map(usage_rows=usage, chain_rows=post_rows)
    assert pre.get("by_theme") == post.get("by_theme")
