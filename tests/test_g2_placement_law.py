"""G2 placement law tests (port wave 2026-10-07, lane P6 port 3).

The law (swarm-orchestration steal card steal 1, ArcticSwarm): interagent
findings feed happens at review; blind sweeps within a pass are legal;
cross-pass pooling only after review. Enforcement is the WARN-level soft row
on the G2 check: a cross-pass pool named before the first review step (or with
no review step at all) soft-warns and never changes the 0/1/2 exit contract.
Reference implementation: .zcode/workflows/olm-mine.dwf.ts:272-289 /
:342-349 / :396-403.
"""
from __future__ import annotations

from tools.workflow_gate import (
    g2_placement_pool_before_review,
    run_checks,
    split_rows,
)

MINE_SHAPE = """
const gophers = items.map((it, i) => agent("sweep-" + i, {}));
const settled = await Promise.allSettled(gophers.map((g, i) =>
  g.ask<SweepResult>("AREA " + areas[i] + ". Fetch recipe: " + RECIPES[areas[i]])));
const steer = agent("steer", {});
const review = await steer.ask<Review>(
  "Read " + OUT + "/steal.md and the returned card JSON. Previous critique: " + critique);
"""

POOL_BEFORE_REVIEW = """
const pool = allFindings.flat();
const ask2 = "Search continuation with peer context: " + JSON.stringify(pool);
const steer = agent("steer", {});
const review = await steer.ask<Review>("Reviewer reported these issues: " + rev.notes);
"""

POOL_NO_REVIEW = """
const pool = pooled.flat();
const ask2 = "Search again with: " + JSON.stringify(pool);
"""


def test_reference_mine_shape_stays_clean():
    # Blind sweep asks, then pooling at the steal round beside the reviewer:
    # the law's own reference shape must not warn.
    assert g2_placement_pool_before_review(MINE_SHAPE) is False


def test_pool_before_review_warns_soft_not_hard():
    rows = run_checks(POOL_BEFORE_REVIEW)
    failed, warned = split_rows(rows)
    assert "G2-passoff" not in failed
    assert "G2-passoff" in warned
    row = next(r for r in rows if r["id"] == "G2-passoff")
    assert row["soft"] is True
    assert "placement law" in row["reason"]
    assert "olm-mine.dwf.ts:272-289" in row["reason"]


def test_pool_with_no_review_step_warns():
    assert g2_placement_pool_before_review(POOL_NO_REVIEW) is True
    rows = run_checks(POOL_NO_REVIEW)
    failed, warned = split_rows(rows)
    assert "G2-passoff" in warned
    assert "G2-passoff" not in failed


def test_review_then_pool_is_legal_and_clean():
    late_pool = (
        MINE_SHAPE
        + '\nconst dump = "pooled findings: " + JSON.stringify(allFindings);\n'
    )
    assert g2_placement_pool_before_review(late_pool) is False
    _, warned = split_rows(run_checks(late_pool))
    assert "G2-passoff" not in warned


def test_warn_never_changes_exit_contract():
    # The soft row rides G2 without entering the failed set, so a script whose
    # only finding is the placement warn still exits 0-shaped (no hard fail).
    rows = run_checks(POOL_BEFORE_REVIEW)
    failed, _ = split_rows(rows)
    assert "G2-passoff" not in failed


def test_comment_only_pool_token_does_not_warn():
    # The G8 comment-fooling lesson, warn side: a pool token living only in a
    # full-line // comment certifies nothing and warns about nothing.
    commented = (
        "// cross-pass pool feeds the next pass here\n"
        + MINE_SHAPE
    )
    assert g2_placement_pool_before_review(commented) is False
