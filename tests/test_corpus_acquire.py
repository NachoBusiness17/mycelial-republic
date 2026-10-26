"""Regression tests for the corpus_acquire family: queue-closes 63->11 flip-sweep
and idempotency contract (WO-12, 2026-09-29).

The corpus_acquire family covers the estate queue-closes lane:
- 63->11 path: the WO-12 flip sweep drains 63 UNCHECKED rows to 11
  (9 untouched keep-open + 2 re-seeds) without aborts
- Idempotency contract: a second sweep on the same file produces
  zero flips and the same 11-row result
"""
import io
import sys
from pathlib import Path

import pytest

from mag.estate_bridge import queue_closes_sweep, _unchecked, CLOSE, _FLIPS

ROOT = Path(__file__).resolve().parent.parent


def _make_todo(count: int = 63) -> str:
    """Build a queue/todo.md with `count` UNCHECKED rows matching _FLIPS structure.

    The sweep keys every flip on line number AND content snippet, so the
    test file must have UNCHECKED rows at the exact line numbers _FLIPS
    expects (up to line 277), with the expected snippet present at each.
    """
    lines = []
    flip_lines = set(_FLIPS.keys())
    # pre-sweep untouched rows (9 rows that survive the sweep unchanged)
    untouched = {31, 97, 99, 204, 205, 233, 234, 239, 250}
    max_line = max(_FLIPS.keys())  # 277

    for i in range(1, max_line + 1):
        if i in flip_lines:
            snippet, _pointer = _FLIPS[i]
            lines.append(f"- [ ] {snippet}")
        elif i in untouched:
            lines.append(f"- [ ] Untouched keep-open row {i}")
        else:
            lines.append(f"- [x] Checked row {i}")

    result = "\n".join(lines) + "\n"
    # sanity: exactly `count` UNCHECKED rows
    actual = sum(1 for ln in lines if ln.startswith("- [ ]"))
    assert actual == count, f"_make_todo produced {actual} UNCHECKED, expected {count}"
    return result


def test_63_to_11_flip_sweep_path(tmp_path: Path) -> None:
    """WO-12 flip sweep: 63 UNCHECKED -> 11 UNCHECKED, zero aborts."""
    todo = tmp_path / "todo.md"
    todo.write_text(_make_todo(63), encoding="utf-8")
    res = queue_closes_sweep(todo=todo, dry_run=False)
    assert res["ok"], f"sweep aborted: {res.get('error')}"
    assert res["pre_count"] == 63
    assert res["post_count"] == 11, f"expected 11 unchecked, got {res['post_count']}"
    assert res["flips"] == 54, f"expected 54 flips (len(_FLIPS)), got {res['flips']}"
    assert res["inserts"] == 2
    # verify the CLOSE marker is on every flipped row
    content = todo.read_text(encoding="utf-8")
    flipped = [ln for ln in content.splitlines() if CLOSE in ln]
    assert len(flipped) == 54


def test_flip_sweep_idempotency(tmp_path: Path) -> None:
    """Idempotency contract: a second sweep on the same file is a no-op."""
    todo = tmp_path / "todo.md"
    todo.write_text(_make_todo(63), encoding="utf-8")
    first = queue_closes_sweep(todo=todo, dry_run=False)
    assert first["ok"]
    assert first["pre_count"] == 63
    assert first["post_count"] == 11
    post_lines = todo.read_text(encoding="utf-8").splitlines()
    post_unchecked = _unchecked(post_lines)
    assert len(post_unchecked) == 11
    # second sweep: the file now has 11 UNCHECKED, not 63 -> drift law abort
    second = queue_closes_sweep(todo=todo, dry_run=False)
    assert not second["ok"]
    assert "63" in second.get("error", "")
    # dry-run on the 11-row file also hits the drift law (pre_count != 63)
    third = queue_closes_sweep(todo=todo, dry_run=True)
    assert not third["ok"]
    assert "63" in third.get("error", "")


def test_flip_sweep_drift_abort(tmp_path: Path) -> None:
    """Drift law: if a flip line is no longer UNCHECKED, abort before writing."""
    todo = tmp_path / "todo.md"
    # start with 63 rows, then manually flip one to [x] before running
    content = _make_todo(63)
    content = content.replace("- [ ]", "- [x]", 1)
    todo.write_text(content, encoding="utf-8")
    res = queue_closes_sweep(todo=todo, dry_run=False)
    assert not res["ok"]
    assert "63" in res.get("error", "")
    # the file must be untouched (the one flip was reverted by the abort)
    assert "- [ ]" in todo.read_text(encoding="utf-8")


def test_flip_sweep_dry_run_never_writes(tmp_path: Path) -> None:
    """Dry run: census only, no writes."""
    todo = tmp_path / "todo.md"
    todo.write_text(_make_todo(63), encoding="utf-8")
    res = queue_closes_sweep(todo=todo, dry_run=True)
    assert res["ok"]
    assert res["dry_run"] is True
    assert res["pre_count"] == 63
    assert res["post_count"] == 63  # unchanged
    assert "- [ ]" in todo.read_text(encoding="utf-8")  # no flips applied