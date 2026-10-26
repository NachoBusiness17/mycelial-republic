"""Q48 — first real production route through the effect broker.

Finding (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md Q48):
production memory/runs/effect_broker/effects.jsonl DID NOT EXIST — the
broker's meter only grew on model_call/lane_spawn, exactly the two effect
classes standing organs are policy-forbidden to dispatch headless
(operator-label tier gate in switchboard_v2._implicit_authority + policy
require_confirmation), so broker-metered production coverage was 0 of
25,427 cost-rollup calls.

Wiring under test (landed 2026-10-01):
  mag/state_snapshot.py capture_summary — the pile-habit organ — files each
  production capture's durable evidence through the full authority mesh
  (switchboard propose -> grant -> mark_executing ->
  effect_broker.execute("board_write") -> complete/fail -> commit_receipt,
  the swarm_cycle._blackboard_note pattern) and stamps corr_id on every
  row (env MAG_CORR_ID per the AH14 law; a uuid4 hex8 mint when unset,
  the duel_harness series-mint shape); mag/effect_broker.py
  _broker_board_write banks one meter row per successful board_write,
  taking its corr_id from the note's `event` field so it joins the ORGAN's
  corr_id, not just the grant event_id.

These tests pin:
  1. the happy path end-to-end: pile row + effects.jsonl row share corr_id,
     board note + broker receipt + trail chain all land;
  2. the unset-env mint (hex8) still joins;
  3. the isolation law: a redirected PILE (this organ's test convention,
     tests/test_state_pile.py _iso) files NO broker row — the production
     meter meters production work only;
  4. the broker regression: a direct brokered board_write banks a row;
  5. the fail-visible law: an unbankable meter append is a FAILED receipt
     and an ok=False capture naming the incident — never a silent pass.

All handles are monkeypatched to tmp_path (pile, broker receipts+ledger,
switchboard blackboard+trail).  The default-path production wiring in the
source is untouched real code; these overrides exist so the suite banks no
rows on the production ledger (AH18 law: test dispatches meter nothing).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _production_handles(monkeypatch, tmp_path):
    """Redirect every durable handle the wired path touches, together."""
    from mag import effect_broker as eb
    from mag import switchboard_v2 as sb
    import mag.state_snapshot as ss

    pile = tmp_path / "pile" / "state_summaries.jsonl"
    monkeypatch.setattr(ss, "PILE", pile)
    # The filing gate compares PILE to _PROD_PILE: point both at tmp so the
    # redirected pile still exercises the production filing CODE path.
    monkeypatch.setattr(ss, "_PROD_PILE", pile)
    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path / "receipts")
    monkeypatch.setattr(sb, "BB", tmp_path / "bb")
    monkeypatch.setattr(sb, "TRAIL", tmp_path / "trail.jsonl")
    sb._GRANTED_EVENT_IDS.clear()  # replay guard is process-global
    return ss, eb, sb, pile


def _meter_rows(eb) -> list[dict]:
    log = eb.RECEIPTS_DIR / eb.EFFECTS_LOG_NAME
    if not log.exists():
        return []
    return [json.loads(line) for line in
            log.read_text(encoding="utf-8").splitlines() if line.strip()]


def _pile_rows(pile: Path) -> list[dict]:
    if not pile.exists():
        return []
    return [json.loads(line) for line in
            pile.read_text(encoding="utf-8").splitlines() if line.strip()]


# ── 1. happy path end-to-end ────────────────────────────────────────────────

def test_production_capture_banks_joined_rows_end_to_end(monkeypatch, tmp_path):
    ss, eb, sb, pile = _production_handles(monkeypatch, tmp_path)
    monkeypatch.setenv("MAG_CORR_ID", "deadbeef")

    r = ss.capture_summary(goal="wire the broker", outcome="ok", tier="local",
                           kind="operator", source="q48-test")

    assert r["ok"] is True, r
    broker = r["broker"]
    assert broker["ok"] is True
    assert broker["meter_row"] is True
    assert broker["corr_id"] == "deadbeef"
    assert broker["authority_status"] == "RECEIPT_COMMITTED"

    # pile row carries the corr_id
    prows = _pile_rows(pile)
    assert len(prows) == 1
    assert prows[0]["corr_id"] == "deadbeef"
    assert prows[0]["id"] == r["row"]["id"]

    # effects.jsonl banks exactly one board_write meter row, joined on corr_id
    rows = _meter_rows(eb)
    assert len(rows) == 1, rows
    row = rows[0]
    assert row["effect"] == "board_write"
    assert row["corr_id"] == "deadbeef"          # THE join: organ corr lands
    assert row["seq"] == broker["seq"] == 1      # first note in redirected BB
    assert row["owner"] == "state_snapshot"
    assert row["path"].endswith("bb-00001.json")

    # board note persisted with event = corr_id
    note = json.loads((tmp_path / "bb" / "bb-00001.json").read_text(encoding="utf-8"))
    assert note["event"] == "deadbeef"
    assert note["owner"] == "state_snapshot"
    assert note["kind"] == "state_summary"

    # broker receipt committed with real postcondition evidence
    receipts = sorted((tmp_path / "receipts").glob("*_board_write_*.json"))
    assert len(receipts) == 1
    rec = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"]["ok"] is True
    assert rec["result"]["effect_row_logged"] is True
    assert rec["postcondition_evidence"]["effect_row_logged"] is True

    # switchboard trail walks the full state machine (propose() builds the
    # record but only grant() and later states trail_append)
    statuses = [json.loads(l)["receipt_status"] for l in
                (tmp_path / "trail.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert statuses == ["AUTHORIZED", "EXECUTING", "COMPLETED",
                        "RECEIPT_COMMITTED"]


def test_capture_mints_hex8_corr_id_when_env_unset(monkeypatch, tmp_path):
    ss, eb, _sb, pile = _production_handles(monkeypatch, tmp_path)
    monkeypatch.delenv("MAG_CORR_ID", raising=False)

    r = ss.capture_summary(goal="no env corr", outcome="ok", tier="local",
                           source="q48-test")
    assert r["ok"] is True
    corr = r["row"]["corr_id"]
    assert re.fullmatch(r"[0-9a-f]{8}", corr), corr  # AH14 uuid4-hex8 shape

    # the mint still joins pile row to meter row
    assert _pile_rows(pile)[0]["corr_id"] == corr
    assert _meter_rows(eb)[0]["corr_id"] == corr


def test_corr_carrying_lane_may_capture_twice(monkeypatch, tmp_path):
    """Replay guard: same MAG_CORR_ID across two captures must not collide.

    The filing mints a unique grant event_id per capture (corr + row id)
    precisely so a corr-carrying lane can capture more than once; the meter
    row keeps the bare corr_id for the join.
    """
    ss, eb, _sb, pile = _production_handles(monkeypatch, tmp_path)
    monkeypatch.setenv("MAG_CORR_ID", "cafe1234")

    r1 = ss.capture_summary(goal="first", outcome="ok", tier="local",
                            source="q48-test")
    r2 = ss.capture_summary(goal="second", outcome="ok", tier="local",
                            source="q48-test")
    assert r1["ok"] and r2["ok"], (r1, r2)

    rows = _meter_rows(eb)
    assert len(rows) == 2
    assert [row["corr_id"] for row in rows] == ["cafe1234", "cafe1234"]
    assert rows[0]["seq"] != rows[1]["seq"]
    assert len(_pile_rows(pile)) == 2


# ── 2. isolation law ────────────────────────────────────────────────────────

def test_redirected_pile_skips_broker_filing_loudly(monkeypatch, tmp_path):
    """tests/test_state_pile.py redirects ONLY ss.PILE — that convention must
    keep broker rows off the production ledgers (structurally, per the
    B2-336 principle) while staying visible in the return."""
    import mag.state_snapshot as ss
    from mag import effect_broker as eb

    monkeypatch.setattr(ss, "PILE", tmp_path / "state_summaries.jsonl")
    # NOTE: ss._PROD_PILE and eb.RECEIPTS_DIR deliberately NOT redirected —
    # if the filing ran anyway it would write the real receipt dir.  The
    # production ledger (which real runs populate) must stay byte-still.
    prod_ledger = eb.RECEIPTS_DIR / eb.EFFECTS_LOG_NAME
    before = prod_ledger.read_bytes() if prod_ledger.exists() else None
    monkeypatch.delenv("MAG_CORR_ID", raising=False)

    r = ss.capture_summary(goal="scratch pile capture", outcome="ok",
                           tier="local", source="q48-test")

    assert r["ok"] is True
    assert "skipped" in r["broker"] and r["broker"]["ok"] is True
    # the redirected pile got its row; the production ledger did not move
    assert _pile_rows(tmp_path / "state_summaries.jsonl")
    after = prod_ledger.read_bytes() if prod_ledger.exists() else None
    assert before == after, "redirected-pile capture banked a production row"


# ── 3. broker regression ────────────────────────────────────────────────────

def _auth(effect: str, event_id: str) -> dict:
    """A clean authority record that passes the reference-monitor gate
    (same shape as tests/test_effect_broker_ah18.py)."""
    return {
        "status": "AUTHORIZED",
        "granted_capabilities": [effect],
        "event_id": event_id,
        "budget": {"max_calls": 5},
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ttl_seconds": 900,
    }


def test_broker_board_write_direct_banks_meter_row(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    from mag import switchboard_v2 as sb

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    monkeypatch.setattr(sb, "BB", tmp_path / "bb")

    rec = eb.execute("board_write",
                     {"note": {"owner": "q48-test", "kind": "finding",
                               "text": "direct broker board_write",
                               "event": "beef0001"}},
                     _auth("board_write", "q48-direct-1"))

    assert rec["status"] == "RECEIPT_COMMITTED"
    res = rec["result"]
    assert res["ok"] is True, rec.get("error")
    assert res["effect_row_logged"] is True

    rows = _meter_rows(eb)
    assert len(rows) == 1
    # the note's event field wins as corr_id (organ join), not the event_id
    assert rows[0]["corr_id"] == "beef0001"
    assert rows[0]["owner"] == "q48-test"
    assert rows[0]["seq"] == res["seq"]
    assert rec["postcondition_evidence"]["effect_row_logged"] is True


def test_broker_board_write_denied_banks_no_meter_row(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    from mag import switchboard_v2 as sb

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    monkeypatch.setattr(sb, "BB", tmp_path / "bb")

    rec = eb.execute("board_write", {"note": {"text": "no caps"}},
                     _auth("fs_write", "q48-denied-1"))  # wrong capability
    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"].get("ok") is not True
    assert _meter_rows(eb) == [], "denied board_write must not meter a row"


def test_evidence_class_board_write_meters_nothing(monkeypatch, tmp_path):
    """tests/test_switchboard.py::test_executing_authority_reaches_effect_broker
    dispatches a REAL brokered board_write unredirected (production receipt
    dir, production blackboard) with a test-prefixed event and kind=test —
    that dispatch must bank NO meter row, else every pytest run fabricates
    broker coverage on the production ledger (harness.py _record_receipt
    evidence-class law)."""
    from mag import effect_broker as eb
    from mag import switchboard_v2 as sb

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    monkeypatch.setattr(sb, "BB", tmp_path / "bb")

    for event_id, note in (
        ("test-executing-broker-contract", {"text": "contract test", "kind": "test"}),
        ("q48-plain-event", {"text": "kind test", "kind": "test"}),
    ):
        rec = eb.execute("board_write", {"note": note}, _auth("board_write", event_id))
        assert rec["status"] == "RECEIPT_COMMITTED"
        assert rec["result"]["ok"] is True
        assert rec["result"]["effect_row_logged"] is False
        assert "evidence-class" in rec["result"]["meter_row_skipped"]
    assert _meter_rows(eb) == []


# ── 4. fail-visible law ─────────────────────────────────────────────────────

def test_unbankable_meter_append_is_a_fail_visible_incident(monkeypatch, tmp_path):
    """The meter append is part of the effect: if the row cannot be banked
    (Q48 task law: an effect that cannot be banked is an incident, not a
    silent pass) the receipt goes FAILED naming the cause, and the organ
    reports ok=False — while the pile row that DID land is still returned."""
    ss, eb, _sb, pile = _production_handles(monkeypatch, tmp_path)
    monkeypatch.setenv("MAG_CORR_ID", "f00d0001")

    def _exploding_append(effect, row):
        raise RuntimeError("ledger disk full")

    monkeypatch.setattr(eb, "_append_effect_row", _exploding_append)

    r = ss.capture_summary(goal="banking fails", outcome="ok", tier="local",
                           source="q48-test")

    # incident named, pile row still returned (it landed)
    assert r["ok"] is False
    assert "broker evidence filing failed" in r["error"]
    assert r["row"]["corr_id"] == "f00d0001"
    assert len(_pile_rows(pile)) == 1
    # nothing banked
    assert _meter_rows(eb) == []
    # the broker receipt recorded the failure honestly (the bb note may have
    # landed; post_state in the receipt shows the truth).  Exception-path
    # receipts carry the failure in rec["error"] with an empty result — the
    # broker's established grammar (see test_effect_broker_ah18 note).
    receipts = sorted((tmp_path / "receipts").glob("*_board_write_*.json"))
    assert len(receipts) == 1
    rec = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"].get("ok") is not True
    assert "ledger disk full" in (rec.get("error") or "")


def test_capture_cli_exits_nonzero_on_incident(monkeypatch, tmp_path, capsys):
    """The CLI turns an ok=False capture into exit 1 — fail-visible at the
    shell, the surface a scheduled habit runs from."""
    ss, eb, _sb, _pile = _production_handles(monkeypatch, tmp_path)
    monkeypatch.setenv("MAG_CORR_ID", "f00d0002")
    monkeypatch.setattr(
        ss, "_file_broker_evidence",
        lambda row, corr: {"ok": False, "error": "simulated broker outage"})

    rc = ss.main(["capture", "--goal", "cli incident", "--outcome", "ok",
                  "--tier", "local", "--source", "q48-test"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "simulated broker outage" in out
