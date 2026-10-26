"""Pin maintenance law in check7 FAIL output (B2-275, 2026-09-26).

Mutation test per the brief: append a resurgent row (the B2-68 pinned-absent
"7/10 plane crashes" tuple) to a TEMP ledger copy, run the verifier's main()
against it, and require the check7 FAIL output to name the pin maintenance
law's required steps. Also pins the PASS line byte-identity: the PASS branch
format string in the source must be untouched by the law text.
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERIFY = REPO / "scripts" / "the50_t21_q_caption_ledger_verify.py"

LAW_MARKERS = (
    "PIN MAINTENANCE LAW (B2-259)",
    "re-audit every differing row against qdrops.jsonl",
    "re-derive the pin constants from that audit",
    "name the audit in the landing receipt",
    "never delete or weaken pins to get green",
)

# the B2-68 pinned-absent tuple, exactly as the generator used to re-emit it
RESURGENT = {"id": "34917", "date": "2017-07-10",
             "claim": "7/10 plane crashes are targeted kills.", "confidence": 0.65}


def _load_module():
    spec = importlib.util.spec_from_file_location("t21_verify_mut", VERIFY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["t21_verify_mut"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_drilled_check7_fail_names_law_steps(tmp_path):
    mod = _load_module()
    assert mod.OUT.is_file(), "live caption ledger missing"
    drilled = tmp_path / "q_caption_ledger.jsonl"
    drilled.write_text(
        mod.OUT.read_text(encoding="utf-8").rstrip("\n")
        + "\n" + json.dumps(RESURGENT) + "\n",
        encoding="utf-8")
    mod.OUT = drilled  # the only mutation: the ledger copy, never the repo file
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main()
    out = buf.getvalue()
    assert rc == 1, out[-400:]
    assert "check7 guard pin" in out and " FAIL " in out
    for marker in LAW_MARKERS:
        assert marker in out, f"drilled check7 FAIL lacks law guidance: {marker!r}"


def test_pass_line_stays_byte_identical():
    source = VERIFY.read_text(encoding="utf-8")
    # the historical PASS branch format bytes, unchanged by B2-275
    assert ('f"check7 guard pin (B2-68/B2-220/B2-219/B2-242/B2-243): "\n'
            '              f"{pin_msg} PASS")') in source
    # the law text belongs to the FAIL branch only: the PASS line is plain
    assert 'PASS")\n    else:' in source.replace("\r\n", "\n")


def test_green_run_result_line_unchanged_and_real_pass():
    """A real green run against the live ledger: RESULT PASS line keeps its
    historical shape and NO law text rides a green run."""
    mod = _load_module()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main()
    out = buf.getvalue()
    assert rc == 0, out[-400:]
    assert "PIN MAINTENANCE LAW" not in out  # the law never fires on green
    assert " PASS" in out


# W3A canary regression (2026-09-29): the gate_canary caption_ledger_verify
# family proved this gate DEAD -- deleting a ledger row left RESULT: PASS
# because every check built its denominator FROM the ledger rows it read.
# Fix under test: check9 seals row count + sha256 in the verifier's own
# source (independent baseline). These tests replay the exact canary plant
# (drop the last row of a fixture ledger copy) and its control.
# Receipt: watch/inbox/mates_leave_protocol/W3A_CAPTION_GATE_FIX.md.


def test_canary_row_deletion_fails_seal(tmp_path):
    """The canary's deletion scenario: fixture ledger minus its last row
    must FAIL (check9 seal + RESULT: FAIL + exit 1)."""
    mod = _load_module()
    assert mod.OUT.is_file(), "live caption ledger missing"
    lines = [ln for ln in mod.OUT.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    drilled = tmp_path / "q_caption_ledger.jsonl"
    drilled.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    mod.OUT = drilled  # the only mutation: the ledger copy, never the repo file
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main()
    out = buf.getvalue()
    assert rc == 1, out[-400:]
    assert "RESULT: FAIL" in out  # the exact token the canary and hook grep
    assert "check9 sealed baseline (W3A): FAIL" in out
    assert f"row count {len(lines) - 1} != sealed {len(lines)}" in out
    assert "SEAL MAINTENANCE LAW (W3A)" in out  # the FAIL names its law


def test_intact_copy_passes_seal(tmp_path):
    """Control: a byte-identical fixture copy passes check9, so the seal
    targets byte drift, not the --ledger/copy path itself."""
    mod = _load_module()
    assert mod.OUT.is_file(), "live caption ledger missing"
    copy = tmp_path / "q_caption_ledger.jsonl"
    copy.write_bytes(mod.OUT.read_bytes())
    mod.OUT = copy
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main()
    out = buf.getvalue()
    assert rc == 0, out[-400:]
    assert "check9 sealed baseline (W3A): rows " in out
    assert "match seal PASS" in out
    assert "RESULT: PASS" in out
