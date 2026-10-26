"""stash_sweep_watch tests (d02-stash-seam lane, dogfood-100m-20261006).

Proves the two contract shapes of the R5-named sibling-sweep detector:
detection fires when a NEW stash push captures paths in the recent-write
window, and a quiet window (stale writes or an already-seen ref) appends
nothing. Incident evidence: watch/inbox/ouroboros_20261005/r3_land_teeth.md
(the 2026-10-05 19:00:39 EDT mid-flight sweep on HEAD ebcd2583d).
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import stash_sweep_watch as ssw  # noqa: E402


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True)
    return proc.stdout


def _make_repo(tmp_path: Path) -> Path:
    """A minimal shared-tree stand-in: two tracked files, one commit."""
    repo = tmp_path / "shared_tree"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "lane@example.test")
    _git(repo, "config", "user.name", "lane-test")
    (repo / "lane_work.txt").write_text("base\n", encoding="utf-8")
    (repo / "other_lane.txt").write_text("base2\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "base")
    return repo


def test_detection_fires_on_new_sweep_of_recent_writes(tmp_path):
    repo = _make_repo(tmp_path)
    # another surface's in-flight edit, then a sibling-seat stash push
    (repo / "lane_work.txt").write_text("in-flight lane edit\n",
                                        encoding="utf-8")
    _git(repo, "stash", "push", "-m", "sibling sweep")
    attention = repo / "memory" / "attention.md"
    state = repo / "state" / "stash_sweep_watch_state.json"
    verdict = ssw.check(root=repo, window_seconds=900,
                        attention_path=attention, state_path=state)
    assert verdict["fired"] is True
    assert len(verdict["new_stashes"]) == 1
    assert "lane_work.txt" in verdict["intersected"]
    assert attention.is_file()
    text = attention.read_text(encoding="utf-8")
    assert "STASH-SWEEP-WATCH alert" in text
    assert "lane_work.txt" in text
    assert verdict["new_stashes"][0]["ref"] in text
    assert text.count("STASH-SWEEP-WATCH alert") == 1


def test_quiet_window_stays_quiet(tmp_path):
    repo = _make_repo(tmp_path)
    (repo / "lane_work.txt").write_text("aged edit\n", encoding="utf-8")
    _git(repo, "stash", "push", "-m", "aged sweep")
    # the tree writes aged out of the window before anyone detected
    old = time.time() - 2 * 900
    for name in ("lane_work.txt", "other_lane.txt"):
        os.utime(repo / name, (old, old))
    attention = repo / "memory" / "attention.md"
    state = repo / "state" / "stash_sweep_watch_state.json"
    verdict = ssw.check(root=repo, window_seconds=900,
                        attention_path=attention, state_path=state)
    assert verdict["fired"] is False
    assert not attention.exists()
    # second run: the ref is seen now, so even fresh live writes elsewhere
    # stay quiet (state dedup, instance_guard law)
    (repo / "other_lane.txt").write_text("touched again\n", encoding="utf-8")
    verdict2 = ssw.check(root=repo, window_seconds=900,
                         attention_path=attention, state_path=state)
    assert verdict2["fired"] is False
    assert verdict2["quiet_reason"] is not None
    assert not attention.exists()
