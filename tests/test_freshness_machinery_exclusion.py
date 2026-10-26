"""R5 canon adjudication: machinery pages are excluded from the mtime crown.

Register row: the R5 logic-lens amendment's CANON SELECTOR RESIDUAL
(state/NIGHT_LOOP_20261005.md). AGENTS.md load-order row 0a already rules in
prose that machinery-regenerated pages (state/LIVE_REPORT.md,
state/REDBOARD.md, state/START_BRIEF.md) never take the boot crown because
their mtime moves on automation cadence, not window authorship; the freshness
meter (tools/freshness_check.py) must read the world the same way. Before the
clause the live meter read "state/START_BRIEF.md: 2.2d old [untracked-mtime]
STALE" (exit 1) on 2026-10-06 because START_BRIEF.md had simply not been
regenerated since 10-04: mtime is the channel sibling seats churn, so the
meter stopped reading it for machinery pages.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools.freshness_check import CRITICAL_DOCS, MACHINERY_REGEN

TOOL = Path(__file__).resolve().parents[1] / "tools" / "freshness_check.py"

# HEADLESS law (spawn_sites_no_window, ratcheted by tests/test_headless_law.py):
# every subprocess spawn carries CREATE_NO_WINDOW on win32 so no console window
# pops on the operator's desktop. 0 on platforms without the flag.
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def test_machinery_regen_names_the_row_0a_triad():
    assert set(MACHINERY_REGEN) == {
        "state/LIVE_REPORT.md",
        "state/REDBOARD.md",
        "state/START_BRIEF.md",
    }


def test_window_docs_stay_judged():
    # The exclusion is scoped to machinery pages only: the authored window doc
    # state/CURRENT.md must remain inside the crown, or the meter gates nothing.
    assert "state/CURRENT.md" not in MACHINERY_REGEN
    assert "state/CURRENT.md" in CRITICAL_DOCS


def test_start_brief_stays_listed_so_the_exclusion_prints():
    # START_BRIEF.md remains in CRITICAL_DOCS: the meter prints its
    # adjudication line instead of silently dropping a listed doc.
    assert "state/START_BRIEF.md" in CRITICAL_DOCS


def test_live_meter_excludes_machinery_pages_from_the_crown():
    # The real CLI on the live repo: the exclusion line must appear for the
    # listed machinery page, and no FAIL line may name one (before the clause
    # the same run read "state/START_BRIEF.md ... STALE" and exited 1).
    proc = subprocess.run(
        [sys.executable, str(TOOL)],
        capture_output=True,
        text=True,
        timeout=120,
        creationflags=HEADLESS,
    )
    out = proc.stdout + proc.stderr
    assert "FRESHNESS:" in out, out  # the meter actually ran; a git refusal exits 2 without per-doc lines
    for doc in MACHINERY_REGEN:
        if doc in CRITICAL_DOCS:
            assert f"{doc}: [machinery-regen] excluded from the mtime crown" in out, out
    for line in out.splitlines():
        if line.startswith("FRESHNESS: FAIL"):
            for doc in MACHINERY_REGEN:
                assert doc not in line, line
    assert proc.returncode in (0, 1), out  # 2 would mean git refused to guess
