"""tests for mag/surface_rebuild.py (WO-10, 2026-09-29).

The rebuild verb must heal the shared surface strictly through the fold's own
writer verbs (add / invalidate / rebuild against scripts/index_fold_host.mjs),
never by hand-editing INDEX.json, and it must be idempotent: a second run on a
healed surface appends nothing. Census classes pinned here:

- invisible: top-level non-control file with ZERO register events -> registered
  (a refold alone can never see it; MASTER_MICKEY17_V2.md D2 ruling).
- stale: active non-living item whose whole-file sha256 no longer matches ->
  re-registered with current bytes (stale-register heal); a living-open item
  is never stale by design (LIVING_HASH_LAW section: no byte seal).
- missing: active item whose file is gone -> invalidated (log history kept).

Runs the real fold with node against throwaway inboxes; the durable
watch/inbox is never touched by these tests.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from mag.surface_rebuild import rebuild_surface

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "index_fold_host.mjs"
NODE = shutil.which("node")

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

pytestmark = pytest.mark.skipif(NODE is None, reason="node not available")


def _env(inbox: Path) -> dict:
    return dict(
        os.environ,
        INDEX_INBOX_DIR=inbox.resolve().as_posix(),
        INDEX_WRITER="surface-rebuild-test",
    )


def _register(inbox: Path, name: str, klass: str = "receipt") -> None:
    proc = subprocess.run(
        [NODE, str(SCRIPT), "add", (inbox / name).resolve().as_posix(), klass],
        capture_output=True, text=True, timeout=60, env=_env(inbox),
        creationflags=HEADLESS,
    )
    assert proc.returncode != 1, f"fold add failed: {proc.stderr}"


def _seed(inbox: Path) -> None:
    inbox.mkdir(parents=True, exist_ok=True)
    # the fold's writers require a pre-existing events log (appendOp dies on a
    # missing file), so every throwaway inbox starts with an empty one
    (inbox / "index_events.jsonl").write_text("", encoding="utf-8")
    (inbox / "a_current.md").write_text("registered and current\n", encoding="utf-8")
    (inbox / "b_stale.md").write_text("registered then amended\n", encoding="utf-8")
    (inbox / "c_invisible.md").write_text("never registered\n", encoding="utf-8")
    (inbox / "d_missing.md").write_text("registered then deleted\n", encoding="utf-8")
    (inbox / "e_open.md").write_text("living open board\n", encoding="utf-8")
    for name in ("a_current.md", "b_stale.md", "d_missing.md"):
        _register(inbox, name)
    proc = subprocess.run(
        [NODE, str(SCRIPT), "add", (inbox / "e_open.md").resolve().as_posix(),
         "board", "--living-open"],
        capture_output=True, text=True, timeout=60, env=_env(inbox),
        creationflags=HEADLESS,
    )
    assert proc.returncode != 1, f"fold add --living-open failed: {proc.stderr}"
    # drift the surface after registration
    (inbox / "b_stale.md").write_text(
        "registered then amended\nplus an append after the seal\n", encoding="utf-8")
    (inbox / "d_missing.md").unlink()
    (inbox / "e_open.md").write_text(
        "living open board\nappended freely, never stale\n", encoding="utf-8")


def _log_lines(inbox: Path) -> int:
    log = inbox / "index_events.jsonl"
    return len([ln for ln in log.read_text(encoding="utf-8").splitlines() if ln.strip()])


def _active_paths(inbox: Path) -> set[str]:
    idx = json.loads((inbox / "INDEX.json").read_text(encoding="utf-8"))
    return {it["path"] for it in idx.get("items", [])}


def test_rebuild_heals_all_three_classes(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    _seed(inbox)
    res = rebuild_surface(inbox=inbox)
    assert res["ok"], json.dumps(res.get("errors", []), indent=2)
    assert res["before"]["invisible"] == ["c_invisible.md"]
    assert [s["path"] for s in res["before"]["stale"]] == ["b_stale.md"]
    assert res["before"]["missing"] == ["d_missing.md"]
    ops = {h["op"]: [x["path"] for x in res["heals"] if x["op"] == h["op"]]
           for h in res["heals"]}
    assert ops.get("register") == ["c_invisible.md"]
    assert ops.get("reregister") == ["b_stale.md"]
    assert ops.get("invalidate") == ["d_missing.md"]
    assert res["after"]["invisible"] == []
    assert res["after"]["stale"] == []
    assert res["after"]["missing"] == []
    active = _active_paths(inbox)
    assert "c_invisible.md" in active
    assert "d_missing.md" not in active
    # e_open.md was appended after its registration: living-open is never stale
    assert "e_open.md" in active
    assert all(h["path"] != "e_open.md" for h in res["heals"])


def test_rebuild_is_idempotent(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    _seed(inbox)
    first = rebuild_surface(inbox=inbox)
    assert first["ok"]
    lines = _log_lines(inbox)
    active_after_first = _active_paths(inbox)
    second = rebuild_surface(inbox=inbox)
    assert second["ok"]
    assert second["plan"] == {"register": 0, "reregister": 0, "invalidate": 0}
    assert second["heals"] == []
    assert _log_lines(inbox) == lines, "no-op rebuild must not append events"
    assert _active_paths(inbox) == active_after_first, "refold must be stable"
    assert second["after"]["active_items"] == first["after"]["active_items"]


def test_rebuild_dry_run_never_writes(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox"
    _seed(inbox)
    lines = _log_lines(inbox)
    active = _active_paths(inbox)
    res = rebuild_surface(inbox=inbox, dry_run=True)
    assert res["ok"] is True
    assert res["dry_run"] is True
    assert res["plan"] == {"register": 1, "reregister": 1, "invalidate": 1}
    assert res["heals"] == []
    assert _log_lines(inbox) == lines, "dry run must not append events"
    assert _active_paths(inbox) == active, "dry run must not refold"
