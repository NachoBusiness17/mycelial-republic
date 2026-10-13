"""tests/test_carrier_patch_t1w1.py - carrier-patch probes (2026-10-01).

Pins the three spend-bleed cures in tools/hermes_burn.py ordered by the
coordinator against the day-1 bleed receipts (watch/inbox/hermes_burn/
DAY1_CROSS_RACTOR.md E1/E3/N3, DAY1_RIB_WARMTH.md X1/X2/X5; $18.89 of
$29.91 was re-fire theater):

  patch 1  LANDED BEATS FORCE: an ask whose output file exists is skipped
           even with force=true; only a revision riding turn2_only re-opens
  patch 2  REFUSED IS TERMINAL: the second banked refusal mints
           <ask_dir>/REFUSED; the carrier then skips on sight (marker or
           ledger backfill)
  patch 3  EVIDENCE PREFLIGHT: missing path, unrendered material, empty
           evidence and empty material file each fail closed BEFORE any
           API call

Every test runs against a tmp ROOT (ask dirs, evidence, outputs, ledger);
no live queue, ledger or output is touched and _call is always a stub.
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


def _refusal_resp() -> dict:
    return {"usage": {"prompt_tokens": 10, "completion_tokens": 0},
            "choices": [{"message": {"refusal": "violative cyber content blocked"}}]}


def _spy_call(monkeypatch, resp: dict) -> list[list[dict]]:
    fired: list[list[dict]] = []

    # extra_body param added 2026-10-04 with the wire merge (parked-decisions
    # SYNTHESIS.md:243-250, usage.jsonl:1151): hermes_burn._call now takes the
    # plan's extra_body and merges it at the wire; the spy must accept the
    # kwarg the real signature carries (3 spy tests TypeError'd without it).
    def fake_call(model, messages, max_tokens, key, retries=1,
                  extra_body=None):
        fired.append([dict(m) for m in messages])
        return resp

    monkeypatch.setattr(hb, "_call", fake_call)
    return fired


# ── patch 1: landed beats force ─────────────────────────────────────────────

def test_landed_output_skips_even_with_force(carrier, monkeypatch) -> None:
    """The A1 bleed shape: force=true ask whose deliverable already landed."""
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP1_force", force=True)
    out = hb.OUT_DIR / "CP1_force.md"
    hb.OUT_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text("# CP1_force (landed 16:10Z)\n\ndeliverable already here\n",
                   encoding="utf-8")

    row = hb.run_ask(d, "k")
    assert row["ok"] is True and row["skipped"].startswith("output exists")
    assert fired == [], "a landed deliverable must never re-fire, force or not"


def test_revision_on_landed_ask_still_fires_turn2_only(carrier, monkeypatch) -> None:
    """The one legal re-open: revision + turn2_only on a landed deliverable."""
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP1_rev", revision=True, turn2_only=True)
    (d / "revision.md").write_text("now ship it", encoding="utf-8")
    hb.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (hb.OUT_DIR / "CP1_rev.md").write_text("landed turn 1\n", encoding="utf-8")

    row = hb.run_ask(d, "k")
    assert row["ok"] is True
    assert len(fired) == 1, "exactly the revision turn fires"
    assert "REVISION (turn 2)" in (hb.OUT_DIR / "CP1_rev.md").read_text(encoding="utf-8")


def test_revision_flag_without_turn2_only_still_skips(carrier, monkeypatch) -> None:
    """Legacy shape parity: the old entry gate skipped this ask too."""
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP1_revnostage", revision=True)
    (d / "revision.md").write_text("now ship it", encoding="utf-8")
    hb.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (hb.OUT_DIR / "CP1_revnostage.md").write_text("landed\n", encoding="utf-8")

    row = hb.run_ask(d, "k")
    assert row["ok"] is True and "skipped" in row
    assert fired == []


# ── patch 2: REFUSED is terminal ────────────────────────────────────────────

def test_second_refusal_mints_marker_then_skip_on_sight(carrier, monkeypatch) -> None:
    fired = _spy_call(monkeypatch, _refusal_resp())
    d = _ask_dir(carrier, "CP2_refused")

    with pytest.raises(RuntimeError, match="REFUSED by provider"):
        hb.run_ask(d, "k")                      # refusal 1: banked, no marker
    assert not (d / "REFUSED").is_file()
    assert len(fired) == 1

    with pytest.raises(RuntimeError, match="REFUSED by provider"):
        hb.run_ask(d, "k")                      # refusal 2: banked + marker
    marker = d / "REFUSED"
    assert marker.is_file()
    assert "violative cyber content" in marker.read_text(encoding="utf-8")
    assert len(fired) == 2

    row = hb.run_ask(d, "k")                    # cycle 3+: skip on sight
    assert row["ok"] is True and row["skipped"].startswith("REFUSED")
    assert len(fired) == 2, "a terminal refusal must never fire again"


def test_ledger_backfill_mints_marker_without_another_fire(carrier, monkeypatch) -> None:
    """Standing disease heal: 46 ledger refusals, no marker yet."""
    fired = _spy_call(monkeypatch, _refusal_resp())
    d = _ask_dir(carrier, "CP2_backfill")
    hb.USAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(hb.USAGE, "a", encoding="utf-8") as fh:
        for _ in range(42):
            fh.write(json.dumps({"ts": "2026-10-01T18:00:00Z", "id": "CP2_backfill",
                                 "model": MODEL, "turn": 1,
                                 "refused": "violative cyber content",
                                 "cost_usd": 0.0, "ok": False}) + "\n")

    row = hb.run_ask(d, "k")
    assert row["ok"] is True and "REFUSED" in row["skipped"]
    assert (d / "REFUSED").is_file()
    assert fired == [], "backfill must heal without one more fire"


# ── patch 3: evidence preflight fails closed before any API call ────────────

def test_missing_evidence_path_fails_closed(carrier, monkeypatch) -> None:
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP3_missing", evidence=["materials/gone.md"])

    with pytest.raises(RuntimeError, match="EVIDENCE-PREFLIGHT.*gone.md"):
        hb.run_ask(d, "k")
    assert fired == []


def test_unrendered_material_fails_closed(carrier, monkeypatch) -> None:
    """The DUEL2 shape: the path exists but the render dropped the bytes."""
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP3_unrendered")
    monkeypatch.setattr(hb, "_read_evidence", lambda paths: "")  # render loss

    with pytest.raises(RuntimeError, match="absent from the message body"):
        hb.run_ask(d, "k")
    assert fired == []


def test_empty_evidence_list_fails_closed(carrier, monkeypatch) -> None:
    """The T1W2 shape: evidence: [] went out and burned premium for generics."""
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP3_empty", evidence=[])

    with pytest.raises(RuntimeError, match="no evidence paths"):
        hb.run_ask(d, "k")
    assert fired == []


def test_empty_material_file_fails_closed(carrier, monkeypatch) -> None:
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP3_blankev")
    (carrier / "materials" / "ev.md").write_text("   \n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="evidence file is empty"):
        hb.run_ask(d, "k")
    assert fired == []


def test_healthy_evidence_fires_and_lands(carrier, monkeypatch) -> None:
    fired = _spy_call(monkeypatch, _ok_resp())
    d = _ask_dir(carrier, "CP3_ok")

    row = hb.run_ask(d, "k")
    assert row["ok"] is True and len(fired) == 1
    assert "material head bytes that must reach the model" in fired[0][0]["content"]
    out = hb.OUT_DIR / "CP3_ok.md"
    assert out.is_file() and "the deliverable" in out.read_text(encoding="utf-8")
