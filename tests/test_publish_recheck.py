"""Tests for tools.publish_recheck (d16, 2026-10-06).

The founding law: the handoff :69 rot class must FAIL the recheck. The
founding subject (the dawn report's cite to the XAI 403 console check that
the economics append moved off its cited line) is replayed on fixtures
with pinned mtimes, so the battery never depends on live repo mtimes: a
citing receipt carries a true line cite, an append lands ABOVE the anchor
(the economics-append class), and the cited span no longer carries the
claim tokens. Negatives: the same receipt with the append landing BELOW
the cited span (the cited bytes held), the source untouched since the
receipt, and a quotation-marked evidence mention of a rot; none may
block.

Receipt: tools/publish_recheck.py module docstring + the lane file.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from tools import citation_lint_io as cio
from tools import publish_recheck as pr

T0 = 1_700_000_000.0
SRC_LINES = (
    [f"header {i}" for i in range(1, 10)]
    + ["XAI 403 console check anchor"]
    + [f"tail {i}" for i in range(11, 16)]
)
CLAIM = "The XAI 403 console check lives at next-window-handoff.md:10-12 (my read).\n"


def _pin(path: Path, ts: float) -> None:
    os.utime(path, (ts, ts))


def _world(tmp_path: Path) -> Path:
    """Throwaway estate slice: a handoff-shaped source with the check at line 10."""
    cio._RESOLVE_CACHE.clear()
    cio._LSFILES_CACHE.clear()
    src = tmp_path / "next-window-handoff.md"
    src.write_text("\n".join(SRC_LINES) + "\n", encoding="utf-8")
    return src


def test_append_above_rots_the_cite(tmp_path):
    """POSITIVE: the founding handoff :69 class must flag ROTTED and exit 1."""
    src = _world(tmp_path)
    rec = tmp_path / "report.md"
    rec.write_text(CLAIM, encoding="utf-8")
    # the economics-append class: lines land ABOVE the anchor and move it down
    src.write_text(
        "\n".join(f"amend {i}" for i in range(4)) + "\n" + src.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    _pin(rec, T0)
    _pin(src, T0 + 60.0)
    anchors, findings = pr.recheck_record(rec, cio.read_lines(rec))
    assert anchors == 1
    rot = [f for f in findings if f.rule == "ROTTED"]
    assert len(rot) == 1, findings
    assert rot[0].anchor == "next-window-handoff.md"
    assert "10-12" in rot[0].detail
    assert "source moved after the receipt's mtime" in rot[0].detail
    rc = pr.main(["publish_recheck", "check", "--files", str(rec),
             "--baseline", str(tmp_path / "none.json")])
    assert rc == 1


def test_append_below_leaves_the_cite_live(tmp_path):
    """NEGATIVE: an append BELOW the cited span does not rot the cite."""
    src = _world(tmp_path)
    rec = tmp_path / "report.md"
    rec.write_text(CLAIM, encoding="utf-8")
    # postscript lands after line 16: the cited bytes at 10-12 hold
    src.write_text(
        src.read_text(encoding="utf-8") + "postscript a\npostscript b\n",
        encoding="utf-8",
    )
    _pin(rec, T0)
    _pin(src, T0 + 60.0)
    _, findings = pr.recheck_record(rec, cio.read_lines(rec))
    assert [f for f in findings if f.rule == "ROTTED"] == []
    # honesty tier: the source DID move, so the re-check warn fires, never blocks
    assert [f for f in findings if f.rule == "ROT-RECHECK"], findings
    rc = pr.main(["publish_recheck", "check", "--files", str(rec),
             "--baseline", str(tmp_path / "none.json")])
    assert rc == 0


def test_source_untouched_since_receipt_is_clean(tmp_path):
    """NEGATIVE: a source not moved since the receipt cannot rot; zero findings."""
    src = _world(tmp_path)
    rec = tmp_path / "report.md"
    rec.write_text(CLAIM, encoding="utf-8")
    _pin(src, T0 - 60.0)
    _pin(rec, T0)
    anchors, findings = pr.recheck_record(rec, cio.read_lines(rec))
    assert anchors == 1
    assert findings == []
    # boundary: equal mtimes are not "moved after"
    _pin(src, T0)
    _, findings2 = pr.recheck_record(rec, cio.read_lines(rec))
    assert findings2 == []
    rc = pr.main(["publish_recheck", "check", "--files", str(rec),
             "--baseline", str(tmp_path / "none.json")])
    assert rc == 0


def test_quoted_evidence_of_a_rot_does_not_block(tmp_path):
    """The dawn report's own account form: a quoted dead cite is evidence, not a claim."""
    src = _world(tmp_path)
    rec = tmp_path / "report.md"
    rec.write_text(
        'The citation "next-window-handoff.md:10" above rotted when the economics '
        "append landed above it: the XAI 403 console check now sits at line 14 "
        "(my grep).\n",
        encoding="utf-8",
    )
    src.write_text(
        "\n".join(f"amend {i}" for i in range(4)) + "\n" + src.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    _pin(rec, T0)
    _pin(src, T0 + 60.0)
    _, findings = pr.recheck_record(rec, cio.read_lines(rec))
    rules = {f.rule for f in findings}
    assert "ROTTED" not in rules
    assert "ROT-QUOTED" in rules, findings
    rc = pr.main(["publish_recheck", "check", "--files", str(rec),
             "--baseline", str(tmp_path / "none.json")])
    assert rc == 0
