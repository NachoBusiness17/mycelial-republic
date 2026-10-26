"""tests/test_spend_balance_v1.py - spend_balance.v1 probes (2026-10-07).

Pins the twice-owed Oct 2 economics move (ops-triage move 2, morning-block
20261007 lane m4-hermes-rails; watch/inbox/ractor_engine/ractor-topic/
economics.md:128, re-owed by break-economics.md:377):

  move 1  FIFTH SURFACE: memory/runs/hermes_burn/usage.jsonl joins the
          rollup (the estate's biggest single-surface spend ledger was
          priced at zero by the four-surface scan)
  move 2  SPEND BALANCE WRITER: every cost_rollup run writes
          memory/runs/spend_balance.json {schema, as_of, spent per ledger
          path, grand totals, recorded funding figures, balance}
  move 3  BALANCE HONESTY: provider balance is null with a stamped probe
          note, never a fabricated figure

All tests run against a tmp root; no live ledger is touched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools import cost_rollup as cr  # noqa: E402


def _make_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "logs" / "duel").mkdir(parents=True)
    (root / "memory" / "runs" / "hermes_burn").mkdir(parents=True)
    (root / "training").mkdir(parents=True)
    (root / "logs" / "duel" / "duels.jsonl").write_text(
        json.dumps({"ts": "2026-10-06T10:00:00Z", "a_model": "m1",
                    "a_cost": 0.5}) + "\n", encoding="utf-8")
    (root / "memory" / "runs" / "hermes_burn" / "usage.jsonl").write_text(
        "\n".join(json.dumps(r) for r in [
            {"ts": "2026-10-06T23:55:08Z", "id": "A2", "model": "anthropic/claude-haiku-4.5",
             "turn": 1, "cost_usd": 0.0233, "ok": True},
            {"ts": "2026-10-06T23:55:27Z", "id": "A3", "model": "anthropic/claude-haiku-4.5",
             "turn": 1, "cost_usd": 0.0104, "ok": True},
            {"ts": "2026-10-07T09:02:21Z", "id": "A1", "model": "anthropic/claude-sonnet-5.5",
             "turn": None, "transport_error": "transport failed after 2 tries: 402",
             "cost_usd": 0.0, "ok": False},
        ]) + "\n", encoding="utf-8")
    (root / "training" / "cost_ledger.jsonl").write_text(
        json.dumps({"ts": "2026-10-05T09:00:00Z",
                    "actual": {"usd_est": 1.25, "usd_fixed": 0.0, "calls": 3},
                    "platform": {"model": "m2"}}) + "\n", encoding="utf-8")
    return root


def test_hermes_burn_surface_rolls_up(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    report = cr.build_report(root)
    by_surface = {s["surface"]: s for s in report["surfaces"]}
    assert cr.SURFACE_HERMES_BURN in by_surface
    assert by_surface[cr.SURFACE_HERMES_BURN]["cost_rows"] == 3
    hermes_usd = sum(c["total_usd"] for c in report["rollup"]
                     if cr.SURFACE_HERMES_BURN in c["surfaces"])
    assert abs(hermes_usd - 0.0337) < 1e-6, "A2 0.0233 + A3 0.0104, the 402 row carries 0.0"
    assert report["grand_total_usd"] > 1.7, "hermes spend joins duel + ledger totals"


def test_missing_hermes_surface_is_named_not_dropped(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    (root / "memory" / "runs" / "hermes_burn" / "usage.jsonl").unlink()
    report = cr.build_report(root)
    named = [u for u in report["unparseable"]
             if u["surface"] == cr.SURFACE_HERMES_BURN]
    assert named and "missing" in named[0]["error"]


def test_spend_balance_written_on_run(tmp_path: Path, capsys) -> None:
    root = _make_root(tmp_path)
    rc = cr.main(["--root", str(root)])
    assert rc == 0
    sb_path = root / "memory" / "runs" / "spend_balance.json"
    assert sb_path.is_file(), "every run mints the spend_balance move"
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    assert sb["schema"] == "spend_balance.v1"
    assert sb["writer"] == "tools/cost_rollup.py"
    paths = sb["spent_per_ledger_path"]
    assert cr.SURFACE_HERMES_BURN in paths
    assert abs(paths[cr.SURFACE_HERMES_BURN]["usd"] - 0.0337) < 1e-6
    assert sb["grand_total_usd"] == cr.build_report(root)["grand_total_usd"]
    assert sb["recorded_funding_usd"]["hermes_order_2026_10_01_usd"] == 70.0
    out = capsys.readouterr().out
    assert "spend_balance written" in out


def test_balance_is_null_with_probe_note(tmp_path: Path) -> None:
    root = _make_root(tmp_path)
    report = cr.build_report(root)
    sb = cr.build_spend_balance(root, report)
    assert sb["balance"]["provider_api_usd"] is None, \
        "no balance endpoint exists; null is the honest value"
    assert "402 is reserve-cost vs remaining balance" in sb["balance"]["note"]
    assert "PROBE_LADDER" in sb["balance"]["note"], \
        "the note points at the byte evidence in usage.jsonl"
