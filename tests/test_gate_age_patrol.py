"""gate_age_patrol tests - the Q40 operator-gate age alarm.

Q40 (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md): operator gates
stall indefinitely because the row absent from attention.md/todo IS the
answer. These pin the alarm's four laws: an old open gate WARNs and files an
attention row; a young open gate stays silent; a decided gate never alarms
(append-only: the decided row is the record); and a register row citing a
receipt that does not exist on disk is a validation error (no-fabrication
teeth), never a silent skip.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import gate_age_patrol as gap  # noqa: E402

TODAY = date(2026, 10, 1)


def _mk_register(tmp_path: Path, gates: list[dict]) -> Path:
    reg = tmp_path / "gate_register.json"
    reg.write_text(json.dumps({"schema": "gate_register.v1", "gates": gates}),
                   encoding="utf-8")
    return reg


def _mk_receipt(root: Path, rel: str = "watch/inbox/FAKE_GATE_RECEIPT.md") -> str:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# receipt naming the gate being opened\n", encoding="utf-8")
    return rel


def _mk_row(**over) -> dict:
    row = {
        "slug": "test-gate",
        "name": "test operator gate",
        "opened": "2026-09-30",
        "status": "open",
        "source_receipt": "watch/inbox/FAKE_GATE_RECEIPT.md",
    }
    row.update(over)
    return row


def test_old_open_gate_warns_and_files_attention_row(tmp_path, capsys):
    receipt = _mk_receipt(tmp_path)
    reg = _mk_register(tmp_path, [_mk_row(opened="2026-09-01", source_receipt=receipt)])
    attention = tmp_path / "attention.md"
    attention.write_text("existing surface\n", encoding="utf-8")
    rc = gap.run(root=tmp_path, register_path=reg, attention_path=attention,
                 threshold_days=14, today=TODAY, write_attention=True)
    out = capsys.readouterr().out
    assert rc == 1
    assert "GATE-AGE: stalled" in out
    assert "test-gate 30d (bar 14d, opened 2026-09-01)" in out
    text = attention.read_text(encoding="utf-8")
    assert "### Gate-age patrol fired" in text
    assert "GATE-AGE: STALLED - 1 open gate(s) over the bar" in text
    assert "test-gate 30d" in text
    assert "- key: gate-age test-gate 2026-10-01" in text
    assert "existing surface" in text  # append-only, prior bytes preserved


def test_young_open_gate_stays_silent(tmp_path, capsys):
    receipt = _mk_receipt(tmp_path)
    reg = _mk_register(tmp_path, [_mk_row(opened="2026-09-30", source_receipt=receipt)])
    attention = tmp_path / "attention.md"
    rc = gap.run(root=tmp_path, register_path=reg, attention_path=attention,
                 threshold_days=14, today=TODAY, write_attention=True)
    out = capsys.readouterr().out
    assert rc == 0
    assert "GATE-AGE: ok" in out
    assert "1 open gate(s), all inside the 14d bar" in out
    assert not attention.exists() or "Gate-age" not in attention.read_text(encoding="utf-8")


def test_decided_gate_never_alarms(tmp_path, capsys):
    receipt = _mk_receipt(tmp_path)
    reg = _mk_register(tmp_path, [_mk_row(
        opened="2026-08-01", status="decided", decided="2026-08-02",
        source_receipt=receipt)])
    attention = tmp_path / "attention.md"
    rc = gap.run(root=tmp_path, register_path=reg, attention_path=attention,
                 threshold_days=14, today=TODAY, write_attention=True)
    out = capsys.readouterr().out
    assert rc == 0
    assert "GATE-AGE: ok" in out
    assert "1 decided row(s) on record" in out
    assert not attention.exists() or "Gate-age" not in attention.read_text(encoding="utf-8")


def test_row_without_real_receipt_is_validation_error(tmp_path, capsys):
    reg = _mk_register(tmp_path, [_mk_row(source_receipt="watch/inbox/NEVER_LANDED.md")])
    rc = gap.run(root=tmp_path, register_path=reg,
                 attention_path=tmp_path / "attention.md",
                 threshold_days=14, today=TODAY, write_attention=True)
    out = capsys.readouterr().out
    assert rc == 2
    assert "cannot verify" in out
    assert "source_receipt not on disk: watch/inbox/NEVER_LANDED.md" in out
    assert "no-fabrication law" in out


def test_same_day_rerun_dedups_the_attention_row(tmp_path, capsys):
    receipt = _mk_receipt(tmp_path)
    reg = _mk_register(tmp_path, [_mk_row(opened="2026-09-01", source_receipt=receipt)])
    attention = tmp_path / "attention.md"
    first = gap.run(root=tmp_path, register_path=reg, attention_path=attention,
                    threshold_days=14, today=TODAY, write_attention=True)
    assert first == 1
    blocks = attention.read_text(encoding="utf-8").count("### Gate-age patrol fired")
    second = gap.run(root=tmp_path, register_path=reg, attention_path=attention,
                     threshold_days=14, today=TODAY, write_attention=True)
    out2 = capsys.readouterr().out
    assert second == 1
    assert blocks == 1
    assert attention.read_text(encoding="utf-8").count("### Gate-age patrol fired") == 1
    assert "already present for today" in out2


def test_future_dated_opened_fail_closes(tmp_path, capsys):
    receipt = _mk_receipt(tmp_path)
    reg = _mk_register(tmp_path, [_mk_row(opened="2026-10-05", source_receipt=receipt)])
    rc = gap.run(root=tmp_path, register_path=reg,
                 attention_path=tmp_path / "attention.md",
                 threshold_days=14, today=TODAY, write_attention=True)
    out = capsys.readouterr().out
    assert rc == 2
    assert "future (fabrication smell)" in out


def test_decided_row_missing_decided_date_is_invalid(tmp_path):
    receipt = _mk_receipt(tmp_path)
    reg = _mk_register(tmp_path, [_mk_row(
        opened="2026-08-01", status="decided", source_receipt=receipt)])
    rc = gap.run(root=tmp_path, register_path=reg,
                 attention_path=tmp_path / "attention.md",
                 threshold_days=14, today=TODAY, write_attention=True)
    assert rc == 2


def test_live_register_on_disk_validates(tmp_path):
    """The seeded production register passes validation against the real root."""
    rows = [gap.validate_row(row, ROOT, i)
            for i, row in enumerate(gap.load_register(ROOT / "configs" / "gate_register.json")["gates"])]
    assert len(rows) >= 7
    assert {r["slug"] for r in rows} >= {
        "cerebras-card-gate", "adam-invite", "nous-portal-topup", "phase2-lensing-go"}
    assert all((ROOT / r["source_receipt"]).is_file() for r in rows)
