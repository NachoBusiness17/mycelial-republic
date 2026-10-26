"""B2-373 falsifier probe: census vs the REAL _log_seat_crash writer bytes.

Runs the actual mag.agent_cli._log_seat_crash (not a fixture copy) against the
MAG_SEAT_CRASH_LOG temp sink (B2-86 seam, no production write), then applies
mag.improve.crash_log_census to the writer's own bytes:

  stanza A: stage=do_turn   RuntimeError("INJECTED-PROBE-TEST")  -> test crash
  stanza B: stage=one_shot  RuntimeError("real operator socket died") -> real crash

Writer contract the census reader assumes (B2-357 docstring): one
"[<iso-utc>] stage=<stage>" line per crash, so a 2-crash log must census as
entries=2 test=1 real=1. If the writer's stanza prefix drifts from the reader
regex (imported here from mag.improve so probe and reader cannot drift), the
census silently collapses the log into one preamble body and real drops to 0:
that is the B2-373 disease this lane pins shut in tests/test_seat_crash_guard.py.

Run with the repo venv from the repo root:
  .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_373_falsifier_probe.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import mag.agent_cli as ac
from mag.improve import _CRASH_STANZA_RE, crash_log_census

EXPECTED = {"blocks": 2, "entries": 2, "test": 1, "real": 1, "chains": 0}


def _raised(msg: str) -> RuntimeError:
    """Return an exception that was actually RAISED, so it carries a
    __traceback__ and format_exception prints the Traceback header the
    census counts. (First probe cut constructed RuntimeError(msg) directly;
    a constructed exception has no traceback, the writer then logs a
    header-less stanza and the census rightly counts 0 entries. Probe
    defect, not drift; corrected here.)"""
    try:
        raise RuntimeError(msg)
    except RuntimeError as exc:
        return exc


def main() -> int:
    old = os.environ.get("MAG_SEAT_CRASH_LOG")
    tmp_dir = tempfile.mkdtemp(prefix="b2_373_probe_")
    sink = Path(tmp_dir) / "seat_crashes.log"
    os.environ["MAG_SEAT_CRASH_LOG"] = str(sink)
    try:
        ac._log_seat_crash("do_turn", _raised("INJECTED-PROBE-TEST"))
        ac._log_seat_crash("one_shot", _raised("real operator socket died"))
    finally:
        if old is None:
            os.environ.pop("MAG_SEAT_CRASH_LOG", None)
        else:
            os.environ["MAG_SEAT_CRASH_LOG"] = old
    text = sink.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    first_line = lines[0] if lines else ""
    census = crash_log_census(text)
    reader_sees_first_line = bool(_CRASH_STANZA_RE.match(first_line))
    out = {
        "writer": "mag.agent_cli._log_seat_crash (real call, temp MAG_SEAT_CRASH_LOG sink)",
        "writer_first_line": first_line,
        "reader_regex": _CRASH_STANZA_RE.pattern,
        "reader_sees_first_line": reader_sees_first_line,
        "census_on_writer_bytes": census,
        "expected_census": EXPECTED,
        "census_matches_writer_contract": census == EXPECTED,
        "verdict": (
            "OK: the census reads the writer's bytes as 2 entries, 1 test, 1 real"
            if census == EXPECTED
            else "DRIFT: the census does NOT read the writer's bytes as written "
            "(the B2-373 silent break; a writer-side stanza pin must go red here)"
        ),
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
