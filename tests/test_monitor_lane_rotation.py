"""Tests for the monitor_lane TERM ROTATION organ (2026-10-04 cure; receipt
watch/inbox/night_shift_20261004/research_rotation_cured.md).

Rotation law: a term with 0 new items for ROTATE_AFTER_BLANK consecutive runs
rotates out; the pool term least-recently-used (never-used first) rotates in;
the window stays ACTIVE_TERMS wide; the epoch counts swap events; hand-added
terms outside the pool never rotate out. Pure-logic tests plus one run_once
integration test with a fake keyless source (no network).
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "monitor_lane_under_test", _REPO / "watch" / "monitor_lane.py")
monitor_lane = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = monitor_lane
_SPEC.loader.exec_module(monitor_lane)

POOL = [f"term{i}" for i in range(21)]  # production shape: 21-pool, 7-window
ACTIVE = POOL[:7]


def _no_sleep(monkeypatch, tmp_path):
    """Point every module path at tmp and kill the politeness sleeps."""
    monkeypatch.setattr(monitor_lane, "TERMS_FILE", tmp_path / "terms.json")
    monkeypatch.setattr(monitor_lane, "POOL_FILE", tmp_path / "pool.json")
    monkeypatch.setattr(monitor_lane, "STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr(monitor_lane, "SPOOL_DIR", tmp_path / "scout")
    monkeypatch.setattr(monitor_lane, "ROOM", tmp_path / "room.jsonl")
    monkeypatch.setattr(monitor_lane, "ROOT", tmp_path)
    monkeypatch.setattr(monitor_lane, "SOURCE_SLEEP_S", {})
    monkeypatch.setattr(monitor_lane, "POLL_SLEEP_S", 0.0)


def test_blank_streak_advances_on_zero_and_resets_on_yield():
    terms = ACTIVE[:]
    blank, ledger, epoch = {}, {}, 0
    # three blank runs for every term
    for _ in range(3):
        terms, rot, blank, ledger, epoch = monitor_lane.rotate_terms(
            terms, POOL, blank, ledger, epoch,
            yields={t: 0 for t in terms})
    assert rot  # rotation fired
    assert len(terms) == monitor_lane.ACTIVE_TERMS
    assert epoch == len(ACTIVE)  # one swap event per rotated term
    # the whole first window was pool members past threshold -> all swapped
    assert not set(ACTIVE) & set(terms)
    # ledger stamped every out-term with its swap epoch
    for t in ACTIVE:
        assert ledger[t] >= 1
    # a yield resets the streak: fresh window, one term yields forever
    blank = {t: monitor_lane.ROTATE_AFTER_BLANK - 1 for t in terms}
    terms2, rot2, blank2, _, _ = monitor_lane.rotate_terms(
        terms, POOL, blank, {}, 100, yields={terms[0]: 5, **{t: 0 for t in terms[1:]}})
    assert terms2[0] == terms[0]  # yielded -> stays
    assert all(o != terms[0] for o, _ in rot2)


def test_never_used_then_oldest_ledger_order():
    # window has one term past threshold; pool free agents: one never used,
    # one used at epoch 3, one used at epoch 7 -> never-used wins
    terms = ["term0", "term1", "term2", "term3", "term4", "term5", "term6"]
    blank = {**{t: 0 for t in terms[:6]}, terms[6]: monitor_lane.ROTATE_AFTER_BLANK}
    ledger = {"term7": 3, "term8": 7}
    new_terms, rot, _, ledger2, epoch = monitor_lane.rotate_terms(
        terms, POOL, blank, ledger, 10, yields={t: 0 for t in terms})
    assert rot == [(terms[6], "term9")]  # term9 never used -> first pick
    assert ledger2[terms[6]] == 11
    # ledger order surfaces once the never-used are gone: a tight pool where
    # the only free agents carry stamps -> the OLDEST stamp rotates in first
    tight = [f"s{i}" for i in range(9)]
    win = tight[:7]
    led = {"s7": 3, "s8": 7}          # the two free agents, both used before
    blank = {**{t: 0 for t in win[:5]}, win[5]: monitor_lane.ROTATE_AFTER_BLANK,
             win[6]: monitor_lane.ROTATE_AFTER_BLANK}
    new2, rot2, _, _, _ = monitor_lane.rotate_terms(
        win, tight, blank, led, 20, yields={t: 0 for t in win})
    assert [i for _, i in rot2] == ["s7", "s8"]  # stamp 3 before stamp 7


def test_hand_added_term_never_rotates_out():
    hand = "operator-said-so"
    terms = ACTIVE[:6] + [hand]
    blank = {t: 99 for t in terms}
    new_terms, rot, blank2, _, _ = monitor_lane.rotate_terms(
        terms, POOL, blank, {}, 0, yields={t: 0 for t in terms})
    assert hand in new_terms
    assert all(o != hand for o, _ in rot)
    assert len(new_terms) == monitor_lane.ACTIVE_TERMS


def test_pool_exhausted_keeps_window_full():
    # every pool member is already active: no free agent exists, so no term
    # rotates (the window never shrinks below what it had)
    pool = ["a", "b", "e", "f", "g"]
    terms = ["a", "b", "c-not-in-pool", "d-not-in-pool", "e", "f", "g"]
    blank = {t: monitor_lane.ROTATE_AFTER_BLANK for t in terms}
    new_terms, rot, _, _, _ = monitor_lane.rotate_terms(
        terms, pool, blank, {}, 0, yields={t: 0 for t in terms})
    assert rot == []
    assert new_terms == terms


def test_state_roundtrip_preserves_rotation_block(tmp_path):
    _no_sleep(pytest.MonkeyPatch(), tmp_path)  # ensure paths isolated
    monitor_lane.save_state(
        {"t": ["id1", "id2"]}, {"openalex": 123.0},
        {"epoch": 4, "ledger": {"t": 2}, "blank": {"t": 3}})
    state, cooldown, rotation = monitor_lane.load_state()
    assert state == {"t": ["id1", "id2"]}
    assert cooldown == {"openalex": 123.0}
    assert rotation == {"epoch": 4, "ledger": {"t": 2}, "blank": {"t": 3}}


def test_run_once_rotates_after_three_blank_runs(monkeypatch, tmp_path):
    """Integration: a fake keyless source that always returns the same item.
    Streaks seeded one below threshold: run 1 polls the stale window (all
    dedup -> blank hits threshold), rotates the whole pool-member window to
    never-used terms; run 2 polls the fresh window (item fresh -> new items,
    streaks reset); runs 3-4 go blank but stay under threshold. The epoch
    lands in the room rows, the terms file swaps, and the seen-id state for
    rotated-out terms survives."""
    _no_sleep(monkeypatch, tmp_path)
    monitor_lane.save_terms(ACTIVE)
    monitor_lane.save_pool(POOL)

    item = {"id": "hn:fixed", "source": "hn", "title": "t",
            "url": "https://example.com", "abstract": "a"}
    calls = {"n": 0}

    def fake_poll(term):
        calls["n"] += 1
        return [dict(item)]

    monkeypatch.setattr(monitor_lane, "SOURCES", [("hn", fake_poll)])

    monitor_lane.save_state(
        {t: ["hn:fixed"] for t in ACTIVE}, {},
        {"epoch": 0, "ledger": {},
         "blank": {t: monitor_lane.ROTATE_AFTER_BLANK - 1 for t in ACTIVE}})

    rc1 = monitor_lane.run_once()
    assert rc1 == 0
    # run 1 rotated the saturated window; rotation happens AFTER the poll,
    # so the fresh terms are polled starting run 2
    terms_mid = json.loads((tmp_path / "terms.json").read_text(encoding="utf-8"))
    assert len(terms_mid) == monitor_lane.ACTIVE_TERMS
    assert not set(ACTIVE) & set(terms_mid)

    for _ in range(3):
        assert monitor_lane.run_once() == 0

    state, _, rotation = monitor_lane.load_state()
    assert rotation["epoch"] == len(ACTIVE)   # one swap event per rotated term
    assert all(t in state for t in ACTIVE)    # seen-ids survive rotation (dedup continuity)
    assert all(state[t] == ["hn:fixed"] for t in terms_mid)  # fresh window banked the item on run 2
    room = (tmp_path / "room.jsonl").read_text(encoding="utf-8").splitlines()
    assert f"epoch={len(ACTIVE)} rotated=" in room[0]
    assert f"epoch={len(ACTIVE)}" in room[-1]
    assert calls["n"] == 4 * monitor_lane.ACTIVE_TERMS
