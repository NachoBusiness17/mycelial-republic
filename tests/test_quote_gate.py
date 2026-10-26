"""tests for tools/quote_gate.py - verbatim-quote gate (Mickey17 V2 item 3).

Offline only, $0, stdlib only: raw byte hit, whitespace-normalized fallback,
miss exits 2, and every error path (missing source, unreadable source, empty
quote) raises into the fail-closed verdict instead of a traceback. No network.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "quote_gate.py"

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

SOURCE = (
    "The estate files receipts, not claims.\n"
    "Verbatim quotes must match the cited source byte for byte,\n"
    "and the gate keeps the hit-rate as a standing number.\n"
)


def run_gate(quote: str, source: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), quote, str(source)],
        capture_output=True,
        text=True,
        creationflags=HEADLESS,
    )


def test_raw_verbatim_hit_exits_0(tmp_path):
    src = tmp_path / "source.md"
    src.write_text(SOURCE, encoding="utf-8")
    r = run_gate("Verbatim quotes must match the cited source byte for byte,", src)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "QUOTE-GATE PASS" in r.stdout
    assert "raw" in r.stdout
    assert r.stdout.count("\n") == 1  # the contract: exactly one verdict line


def test_whitespace_normalized_fallback_hit_exits_0(tmp_path):
    src = tmp_path / "source.md"
    src.write_text(SOURCE, encoding="utf-8")
    # same words, reflowed across lines with doubled spaces: not a raw hit
    r = run_gate("Verbatim quotes\n  must match the cited   source\nbyte for byte,", src)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "QUOTE-GATE PASS" in r.stdout
    assert "whitespace-normalized" in r.stdout


def test_crlf_line_wrapped_quote_hits_normalized(tmp_path):
    src = tmp_path / "source.md"
    src.write_text(SOURCE.replace("\n", "\r\n"), encoding="utf-8")
    r = run_gate("The estate files receipts,\nnot claims.", src)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "whitespace-normalized" in r.stdout


def test_paraphrase_miss_exits_2(tmp_path):
    src = tmp_path / "source.md"
    src.write_text(SOURCE, encoding="utf-8")
    r = run_gate("Quotes may paraphrase the cited source when convenient,", src)
    assert r.returncode == 2
    assert "QUOTE-GATE FAIL" in r.stdout
    assert "not found" in r.stdout


def test_missing_source_raises_into_failure(tmp_path):
    # gate contract: an error surfaces as the fail-closed exit 2 verdict,
    # never as an unhandled traceback
    r = run_gate("any quote at all", tmp_path / "no_such_file.md")
    assert r.returncode == 2
    assert "QUOTE-GATE FAIL" in r.stdout
    assert "not found" in r.stdout
    assert "Traceback" not in r.stderr


def test_empty_quote_fails_closed(tmp_path):
    src = tmp_path / "source.md"
    src.write_text(SOURCE, encoding="utf-8")
    r = run_gate("   ", src)
    assert r.returncode == 2
    assert "QUOTE-GATE FAIL" in r.stdout
    assert "Traceback" not in r.stderr
