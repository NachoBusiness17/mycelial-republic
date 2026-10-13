"""Estate-index dedup tool tests (W3 lane, 2026-09-29).

Covers the two mission-gated behaviors of tools/estate_index_dedup.py:
  1. an identical dup-dir fixture -> --apply writes the one-line pointer AND
     banks full sha256s of both copies before the swap;
  2. a divergent fixture -> NOTHING is touched (mirror bytes byte-still, no
     pointer, no bank), check flags divergence with exit 1.
Loaded via importlib from the file path (test_ack_reaper pattern) so the
heavy tools/__init__ import chain stays out of these tests.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path

import pytest

_TOOL = Path(__file__).resolve().parents[1] / "tools" / "estate_index_dedup.py"
_spec = importlib.util.spec_from_file_location("estate_index_dedup", _TOOL)
eid = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eid)

SAMPLE = 16 * 1024
SIZE = 128 * 1024
DATE = "2026-09-30"


def _make_pair(tmp_path: Path, diverge: str | None = None,
               mirror_size: int | None = None) -> tuple[Path, Path, bytes]:
    """Deterministic primary + mirror fixtures; optional divergence mode."""
    data = random.Random(20260929).randbytes(SIZE)
    primary = tmp_path / "PRIMARY.jsonl"
    primary.write_bytes(data)
    mdata = bytearray(data)
    if diverge == "tail-flip":
        mdata[-1] ^= 0xFF  # inside the tail sample; head/mid samples still match
    elif diverge == "truncated":
        mdata = mdata[: SIZE - 7]
    if mirror_size is not None:
        mdata = bytearray(mdata[:mirror_size])
    mirror = tmp_path / "mirror" / "PRIMARY.jsonl"
    mirror.parent.mkdir()
    mirror.write_bytes(bytes(mdata))
    return primary, mirror, data


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_check_identical_pair_reports_dup(tmp_path, capsys):
    primary, mirror, _ = _make_pair(tmp_path)
    res = eid.check_pair(primary, mirror, SAMPLE)
    assert res["state"] == "dup"
    assert res["sizes_equal"] is True
    assert all(v["match"] for v in res["regions"].values())
    rc = eid.main(["--check", "--primary", str(primary), "--mirror", str(mirror),
                   "--sample-mb", str(SAMPLE / 1048576)])
    assert rc == 0
    assert "DUPLICATE CONFIRMED" in capsys.readouterr().out


def test_check_divergent_tail_reports_mismatch(tmp_path, capsys):
    primary, mirror, _ = _make_pair(tmp_path, diverge="tail-flip")
    res = eid.check_pair(primary, mirror, SAMPLE)
    assert res["state"] == "divergent"
    assert res["regions"]["head"]["match"] is True      # head alone is not proof
    assert res["regions"]["tail"]["match"] is False     # tail sample catches it
    rc = eid.main(["--check", "--primary", str(primary), "--mirror", str(mirror),
                   "--sample-mb", str(SAMPLE / 1048576)])
    assert rc == 1
    assert "DIVERGENT" in capsys.readouterr().out


def test_apply_identical_writes_pointer_and_banks_shas(tmp_path):
    primary, mirror, data = _make_pair(tmp_path)
    res = eid.apply_pointer(primary, mirror, DATE, SAMPLE)
    assert res["state"] == "deduped" and res["touched"] is True
    # pointer: exactly one line, names the primary and the dedup date
    text = mirror.read_text(encoding="utf-8")
    assert text.count("\n") == 1 and text.startswith("superseded by ")
    assert f"deduped {DATE}" in text and "sha head/tail recorded" in text
    # bank: written BEFORE the swap, carries the full equal sha256s of both copies
    bank = Path(str(res["bank"]))
    assert bank.exists() and bank == mirror.with_name(mirror.name + ".dedup_shas.json")
    b = json.loads(bank.read_text(encoding="utf-8"))
    assert b["primary_sha256"] == b["mirror_sha256"] == _sha(data)
    assert b["size_bytes"] == SIZE
    assert b["verdict"].startswith("byte-identical")
    # primary untouched by the whole operation
    assert primary.read_bytes() == data


def test_apply_divergent_touches_nothing(tmp_path):
    primary, mirror, _ = _make_pair(tmp_path, diverge="tail-flip")
    before = mirror.read_bytes()
    res = eid.apply_pointer(primary, mirror, DATE, SAMPLE)
    assert res["state"] == "divergent" and res["touched"] is False
    assert mirror.read_bytes() == before  # byte-still, still the data file
    assert not mirror.with_name(mirror.name + ".dedup_shas.json").exists()
    rc = eid.main(["--apply", "--primary", str(primary), "--mirror", str(mirror),
                   "--sample-mb", str(SAMPLE / 1048576)])
    assert rc == 1  # CLI path aborts too, and never swaps


def test_apply_size_mismatch_aborts_untouched(tmp_path):
    primary, mirror, _ = _make_pair(tmp_path, mirror_size=SIZE - 1)
    before = mirror.read_bytes()
    assert len(before) == SIZE - 1  # fixture: same prefix, one byte shorter
    res = eid.apply_pointer(primary, mirror, DATE, SAMPLE)
    assert res["state"] == "divergent" and res["touched"] is False
    assert mirror.read_bytes() == before


def test_check_after_apply_reports_deduped_and_apply_is_noop(tmp_path, capsys):
    primary, mirror, _ = _make_pair(tmp_path)
    assert eid.apply_pointer(primary, mirror, DATE, SAMPLE)["state"] == "deduped"
    chk = eid.check_pair(primary, mirror, SAMPLE)
    assert chk["state"] == "deduped"
    assert chk["pointer_line"].startswith("superseded by ")
    assert eid.main(["--check", "--primary", str(primary), "--mirror", str(mirror),
                     "--sample-mb", str(SAMPLE / 1048576)]) == 0
    again = eid.apply_pointer(primary, mirror, DATE, SAMPLE)
    assert again["state"] == "already-deduped" and again["touched"] is False
    assert "already deduped" in capsys.readouterr().out


def test_missing_files_are_errors_not_divergence(tmp_path):
    primary, mirror, _ = _make_pair(tmp_path)
    assert eid.check_pair(primary, tmp_path / "nope.jsonl", SAMPLE)["state"] == "missing-mirror"
    res = eid.apply_pointer(tmp_path / "nope.jsonl", mirror, DATE, SAMPLE)
    assert res["state"] == "missing-primary" and res["touched"] is False
    assert mirror.exists()
