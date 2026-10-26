"""tests/test_hermes_burn_terminal_rails.py - TERMINAL rail probes (2026-10-07).

Pins the ops-triage move 2 cures in tools/hermes_burn.py (morning-block
20261007 lane m4-hermes-rails; the disease: the 10-06 23:54Z .. 10-07
08:00Z provider 402 wall fired MagHermesBurn247 hourly ~8 times, 402ing
H247_A1 twice per fire with nothing banked and no terminal state, every
fire exit 1 - logs/hermes_burn_247.log):

  rail 1  TRANSPORT IS DATA: a transport failure banks an ok:false row with
          transport_error and turn None (guard_terminal precedent)
  rail 2  TWO CONSECUTIVE = TERMINAL: the ask's TRAILING ledger run of 2
          transport failures mints <ask_dir>/TERMINAL; a non-transport
          outcome for the ask resets the run
  rail 3  PREFLIGHT = TERMINAL: one EVIDENCE-PREFLIGHT failure mints the
          marker immediately (deterministic, never self-heals)
  rail 4  SKIP ON SIGHT: a TERMINAL ask never fires again
  rail 5  SPLIT SUMMARY: the main() line reads
          "paid N skipped M failed K of T asks" (the old "2/3 asks" shape
          read skips as successes)

Every test runs against a tmp ROOT/OUT_DIR/USAGE; _call is always a stub.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools import hermes_burn as hb  # noqa: E402

MODEL = "anthropic/claude-opus-5.5"


@pytest.fixture()
def carrier(tmp_path: Path, monkeypatch):
    """A tmp carrier estate: ROOT, OUT_DIR and USAGE all under tmp_path."""
    monkeypatch.setattr(hb, "ROOT", tmp_path)
    monkeypatch.setattr(hb, "OUT_DIR", tmp_path / "watch" / "inbox" / "hermes_burn")
    monkeypatch.setattr(hb, "USAGE", tmp_path / "usage.jsonl")
    (tmp_path / "materials").mkdir()
    return tmp_path


def _ask_dir(root: Path, ask_id: str, **over) -> Path:
    d = root / "queues" / ask_id
    d.mkdir(parents=True, exist_ok=True)
    meta = {"id": ask_id, "model": MODEL, "max_tokens": 100, "force": False,
            "contract": "do the thing", "evidence": ["materials/ev.md"],
            "revision": False, "turn2_only": False}
    meta.update(over)
    (d / "ask.json").write_text(json.dumps(meta), encoding="utf-8")
    (root / "materials" / "ev.md").write_text(
        "material head bytes that must reach the model\nsecond line\n", encoding="utf-8")
    return d


def _ok_resp() -> dict:
    return {"usage": {"prompt_tokens": 10, "completion_tokens": 20},
            "choices": [{"message": {"content": "the deliverable"}}]}


def _raise_transport(monkeypatch, status: int = 402) -> list[int]:
    calls = []

    def fake_call(model, messages, max_tokens, key, retries=1,
                  extra_body=None):
        calls.append(1)
        raise RuntimeError(
            f"transport failed after {retries + 1} tries: "
            f"<HTTPError {status}: 'Payment Required'>")

    monkeypatch.setattr(hb, "_call", fake_call)
    return calls


def _raise_ok(monkeypatch) -> list[int]:
    calls = []

    def fake_call(model, messages, max_tokens, key, retries=1,
                  extra_body=None):
        calls.append(1)
        return _ok_resp()

    monkeypatch.setattr(hb, "_call", fake_call)
    return calls


def _ledger_rows(root: Path) -> list[dict]:
    ledger = root / "usage.jsonl"
    if not ledger.is_file():
        return []
    return [json.loads(line) for line in
            ledger.read_text(encoding="utf-8").splitlines() if line.strip()]


# ── rail 1 + 2: transport failures bank, then go terminal ───────────────────

def test_second_consecutive_transport_failure_mints_terminal(carrier, monkeypatch) -> None:
    fired = _raise_transport(monkeypatch)
    d = _ask_dir(carrier, "TR_twice")

    with pytest.raises(RuntimeError, match="transport failed"):
        hb.run_ask(d, "k")                      # wall fire 1: banked, no marker
    assert not (d / "TERMINAL").is_file()
    rows = [r for r in _ledger_rows(carrier) if r["id"] == "TR_twice"]
    assert len(rows) == 1 and rows[0]["ok"] is False
    assert "transport_error" in rows[0] and rows[0]["turn"] is None
    assert rows[0]["cost_usd"] == 0.0
    assert len(fired) == 1

    with pytest.raises(RuntimeError, match="transport failed"):
        hb.run_ask(d, "k")                      # wall fire 2: banked + marker
    marker = d / "TERMINAL"
    assert marker.is_file()
    assert "Payment Required" in marker.read_text(encoding="utf-8")
    assert len(fired) == 2

    row = hb.run_ask(d, "k")                    # cycle 3+: skip on sight
    assert row["ok"] is True and row["skipped"].startswith("TERMINAL")
    assert len(fired) == 2, "a TERMINAL ask must never fire again"


def test_terminal_state_counts_only_trailing_transport_run(carrier) -> None:
    """The reset semantics at the reader (an end-to-end reset would need the
    revision re-open: a landed success skips at _landed_skip forever, by
    law, so the trailing run is exercised at _terminal_state directly)."""
    hb.USAGE.parent.mkdir(parents=True, exist_ok=True)

    def bank(rows):
        with open(hb.USAGE, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")

    terr = "transport failed after 2 tries: 402"
    trow = {"ts": "t", "id": "TR_reader", "model": MODEL, "turn": None,
            "transport_error": terr, "cost_usd": 0.0, "ok": False}
    orow = {"ts": "t", "id": "TR_reader", "model": MODEL, "turn": 1,
            "cost_usd": 0.01, "ok": True}
    rrow = {"ts": "t", "id": "TR_reader", "model": MODEL, "turn": 1,
            "refused": "no", "cost_usd": 0.0, "ok": False}

    bank([trow, trow])
    assert hb._terminal_state("TR_reader") == (2, terr)

    bank([orow])
    assert hb._terminal_state("TR_reader") == (0, ""), "a paid row resets the run"

    bank([trow])
    assert hb._terminal_state("TR_reader") == (1, terr), "run restarts at 1"

    bank([rrow])
    assert hb._terminal_state("TR_reader") == (0, ""), "a refusal row also resets"

    bank([trow, trow, trow])
    count, err = hb._terminal_state("TR_reader")
    assert count == 3 and err == terr
    assert hb._terminal_state("other_id") == (0, ""), "per-ask isolation"


def test_ledger_backfill_mints_terminal_without_another_fire(carrier, monkeypatch) -> None:
    """Standing-disease heal, the refusal-backfill shape: 2 ledger transport
    rows, no marker yet (the 10-07 08:00Z A1 state had this shape)."""
    fired = _raise_transport(monkeypatch)
    d = _ask_dir(carrier, "TR_backfill")
    hb.USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(hb.USAGE, "a", encoding="utf-8") as fh:
        for _ in range(2):
            fh.write(json.dumps(
                {"ts": "2026-10-07T03:00:10Z", "id": "TR_backfill",
                 "model": MODEL, "turn": None,
                 "transport_error": "transport failed after 2 tries: 402",
                 "cost_usd": 0.0, "ok": False}) + "\n")

    row = hb.run_ask(d, "k")
    assert row["ok"] is True and "TERMINAL" in row["skipped"]
    assert (d / "TERMINAL").is_file()
    assert fired == [], "backfill must heal without one more fire"


# ── rail 3: preflight failure mints terminal immediately ────────────────────

def test_preflight_failure_mints_terminal_immediately(carrier, monkeypatch) -> None:
    fired = _raise_ok(monkeypatch)
    d = _ask_dir(carrier, "TR_preflight", evidence=["materials/gone.md"])

    with pytest.raises(RuntimeError, match="EVIDENCE-PREFLIGHT"):
        hb.run_ask(d, "k")
    assert (d / "TERMINAL").is_file(), "a deterministic preflight defect mints on first occurrence"
    assert fired == [], "preflight fires before any API call"

    row = hb.run_ask(d, "k")
    assert row["ok"] is True and row["skipped"].startswith("TERMINAL")


# ── rail 5: the summary splits paid / skipped / failed ──────────────────────

def test_summary_splits_paid_skipped_failed(carrier, monkeypatch, capsys) -> None:
    monkeypatch.setattr(hb, "_hermes_key", lambda: "k")
    fired = _raise_ok(monkeypatch)
    skip_dir = _ask_dir(carrier, "TR_sum_skip")
    hb.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (hb.OUT_DIR / "TR_sum_skip.md").write_text("landed\n", encoding="utf-8")
    _ask_dir(carrier, "TR_sum_fail", model="anthropic/not-a-model")

    rc = hb.main([str(carrier / "queues")])
    out = capsys.readouterr().out
    assert "paid 0 skipped 1 failed 1 of 2 asks" in out
    assert rc == 1
    assert len(fired) == 0, "a landed skip and an unknown-model fail never fire"


def test_summary_all_skipped_is_pass_exit0(carrier, monkeypatch, capsys) -> None:
    monkeypatch.setattr(hb, "_hermes_key", lambda: "k")
    _raise_ok(monkeypatch)
    skip_dir = _ask_dir(carrier, "TR_sum_skip2")
    hb.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (hb.OUT_DIR / "TR_sum_skip2.md").write_text("landed\n", encoding="utf-8")

    rc = hb.main([str(carrier / "queues")])
    out = capsys.readouterr().out
    assert "paid 0 skipped 1 failed 0 of 1 asks" in out
    assert "HERMES-BURN: PASS" in out
    assert rc == 0
