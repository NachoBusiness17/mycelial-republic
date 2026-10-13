#!/usr/bin/env python3
"""stash_sweep_watch - detector for the sibling-seat stash-sweep defect class.

Born from the R5-named incident (2026-10-05, watch/inbox/ouroboros_20261005/
r3_land_teeth.md:92-105): a `git stash` fired mid-landing by a seat that was
not the landing lane captured ALL working-tree modifications on HEAD
ebcd2583d, including another lane's eleven executor files; the lane had to
re-apply its edits surgically onto the post-sweep tree. The estate keeps
three such sweep stashes live (census 2026-10-06: stash@{0} 8b45fe97,
stash@{1} 2902e0d3, stash@{2} 8baa166e, all HOLD-RECONCILE, never dropped).

Contract (d02-stash-seam lane, dogfood-100m-20261006):
- check: flag a NEW stash push (ref unseen in the state file) whose captured
  paths intersect the recent-write window (tree files with mtime within
  window_seconds of now, or absent from the tree when the sweep captured a
  deletion); each hit appends ONE alert line to memory/attention.md, the
  estate alarm surface. Exit 0 quiet, 1 alert appended, 2 error.
- census: print disposition rows for every live stash (content class, lane
  hints, HOLD-RECONCILE verdict). The tool has NO drop or pop verb by design:
  a sweep stash may carry an unlanded lane's only copy of its work.

Dedup law (mirrors tools/instance_guard.py doubled_key_check): one alert
line per stash ref, ever; repeat sightings stamp state only.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_SEEN_REFS = 500


class SweepWatchError(RuntimeError):
    """git failed or the root is not a repository. Callers exit 2."""


def _git(root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=60,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SweepWatchError(f"git {' '.join(args)} failed: {exc}") from exc
    if proc.returncode != 0:
        raise SweepWatchError(
            f"git {' '.join(args)} exit {proc.returncode}: "
            f"{proc.stderr.strip()[:300]}")
    return proc.stdout


def _iso(ts: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def list_stashes(root: Path) -> list[dict]:
    """Every live stash as {label, ref, created}. Order matches git stash
    list (newest first). Created is the stash commit's committer timestamp,
    the sweep moment."""
    out = _git(root, "stash", "list", "--format=%gd|%H|%ct")
    stashes: list[dict] = []
    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) != 3:
            continue
        label, ref, ts = parts[0], parts[1], parts[2]
        try:
            created = float(ts)
        except ValueError:
            continue
        stashes.append({"label": label, "ref": ref, "created": created})
    return stashes


def stash_paths(root: Path, label: str) -> list[str]:
    """Paths a stash captures (tracked changes only, the sweep surface)."""
    out = _git(root, "stash", "show", "--name-only", label)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def fresh_mtimes(root: Path, paths: list[str], window_seconds: float,
                 now: float | None = None) -> dict[str, float]:
    """Recent-write window membership for exactly the given paths: those
    whose tree mtime is within window_seconds of now. Targeted stat, not a
    tree walk: this estate holds ~680k files outside .git (memory/ alone
    550k, census 2026-10-06), so a full walk cannot finish inside a patrol
    cadence, and the intersection only ever needs the stash's own paths."""
    now = time.time() if now is None else now
    cutoff = now - window_seconds
    fresh: dict[str, float] = {}
    for rel in paths:
        try:
            mtime = (root / rel).stat().st_mtime
        except OSError:
            continue
        if mtime >= cutoff:
            fresh[rel] = mtime
    return fresh


def _load_state(state_path: Path) -> dict:
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"seen": {}}


def _save_state(state_path: Path, state: dict) -> None:
    seen = state.get("seen", {})
    if len(seen) > MAX_SEEN_REFS:
        keep = sorted(seen.items(), key=lambda kv: -kv[1].get("ts", 0.0))
        state["seen"] = dict(keep[:MAX_SEEN_REFS])
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, sort_keys=True), encoding="utf-8")
    os.replace(tmp, state_path)


def _append_alert(attention_path: Path, line: str, sig: str) -> bool:
    """Append the alert line once per sig (instance_guard dedup law).
    Returns True when a line was appended."""
    try:
        attention_path.parent.mkdir(parents=True, exist_ok=True)
        text = (attention_path.read_text(encoding="utf-8", errors="replace")
                if attention_path.is_file() else "")
        if sig in text:
            return False
        with open(attention_path, "a", encoding="utf-8") as fh:
            fh.write(line)
        return True
    except OSError as exc:
        print(f"STASH-SWEEP-WATCH: attention append failed: {exc}",
              file=sys.stderr)
        return False


def check(root: Path | None = None, window_seconds: float = 900.0,
          now: float | None = None, attention_path: Path | None = None,
          state_path: Path | None = None) -> dict:
    """One detection pass. New stash + path intersection in the recent-write
    window = alert line appended to attention, exit-1 verdict. Everything
    else is quiet (exit-0 verdict) and the state file absorbs the refs."""
    root = Path(root) if root else ROOT
    now = time.time() if now is None else now
    attention_path = attention_path or (root / "memory" / "attention.md")
    state_path = state_path or (root / "state"
                                / "stash_sweep_watch_state.json")
    verdict: dict = {
        "mode": "check", "root": str(root),
        "window_seconds": window_seconds, "moment": _iso(now),
        "new_stashes": [], "intersected": [], "fired": False,
        "alert_path": None, "quiet_reason": None,
    }
    state = _load_state(state_path)
    seen: dict = state.setdefault("seen", {})
    try:
        stashes = list_stashes(root)
    except SweepWatchError as exc:
        verdict["error"] = str(exc)
        return verdict
    fresh: dict[str, float] = {}
    for stash in stashes:
        ref = stash["ref"]
        if ref in seen:
            continue
        paths = stash_paths(root, stash["label"])
        stash["paths"] = paths
        fresh = fresh_mtimes(root, paths, window_seconds, now)
        entry = {
            "label": stash["label"], "ref": ref,
            "created": _iso(stash["created"]), "paths": paths,
        }
        verdict["new_stashes"].append(entry)
        hits = []
        for p in paths:
            if p in fresh:
                hits.append(p)
            elif not (root / p).exists():
                hits.append(f"{p} (absent-from-tree, deletion captured)")
        if hits:
            verdict["intersected"].extend(hits)
            verdict["fired"] = True
            line = (f"- [x] STASH-SWEEP-WATCH alert {_iso(now)}: "
                    f"new git stash {ref} ({stash['label']}, created "
                    f"{entry['created']}) captures {len(hits)} "
                    f"path(s) in the recent-write window "
                    f"({int(window_seconds)}s): "
                    f"{'; '.join(hits[:12])}; reconcile against the owning "
                    f"lane before any pop (incident: "
                    f"watch/inbox/ouroboros_20261005/"
                    f"r3_land_teeth.md:92)\n")
            if _append_alert(attention_path, line, f"new git stash {ref} "):
                verdict["alert_path"] = str(attention_path)
            seen[ref] = {"ts": now, "when": _iso(now), "fired": True}
        else:
            seen[ref] = {"ts": now, "when": _iso(now), "fired": False}
    if not verdict["new_stashes"]:
        verdict["quiet_reason"] = (
            f"no unseen stashes (state carries {len(seen)} ref(s))")
    elif not verdict["fired"]:
        verdict["quiet_reason"] = (
            f"{len(verdict['new_stashes'])} new stash(es) but no path "
            f"intersects the recent-write window ({int(window_seconds)}s)")
    _save_state(state_path, state)
    return verdict


def census(root: Path | None = None) -> list[dict]:
    """Disposition rows for every live stash. Classifies content by lane
    hint (queue/lanes/*) and estate surface; every row is HOLD-RECONCILE.
    No verb in this tool can drop or pop a stash."""
    root = Path(root) if root else ROOT
    rows = []
    for stash in list_stashes(root):
        paths = stash_paths(root, stash["label"])
        lanes = sorted({p.split("/")[2] for p in paths
                        if p.startswith("queue/lanes/")
                        and len(p.split("/")) > 2})
        classes: dict[str, int] = {}
        for p in paths:
            top = p.split("/")[0]
            classes[top] = classes.get(top, 0) + 1
        rows.append({
            "label": stash["label"], "ref": stash["ref"],
            "created": _iso(stash["created"]), "file_count": len(paths),
            "content_classes": classes, "lane_hints": lanes,
            "sample_paths": paths[:8],
            "disposition": ("HOLD-RECONCILE: may carry an unlanded lane's "
                            "only copy of its work; reconcile against the "
                            "tree before any pop; never drop"),
        })
    return rows


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = "check"
    if argv and argv[0] in ("check", "census"):
        cmd = argv.pop(0)
    root = ROOT
    window = 900.0
    as_json = False
    i = 0
    while i < len(argv):
        if argv[i] == "--root":
            root = Path(argv[i + 1]); i += 2
        elif argv[i] == "--window":
            window = float(argv[i + 1]); i += 2
        elif argv[i] == "--json":
            as_json = True; i += 1
        else:
            print(f"unknown arg {argv[i]}", file=sys.stderr); return 2
    try:
        if cmd == "census":
            rows = census(root)
            print(json.dumps(rows, indent=2 if as_json else None))
            return 0
        verdict = check(root, window_seconds=window)
    except SweepWatchError as exc:
        print(f"STASH-SWEEP-WATCH: {exc}", file=sys.stderr)
        return 2
    if verdict.get("error"):
        print(f"STASH-SWEEP-WATCH: {verdict['error']}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(verdict, indent=2))
    if verdict["fired"]:
        hits = ", ".join(verdict["intersected"][:6])
        print(f"STASH-SWEEP-WATCH: ALERT new stash sweep intersects the "
              f"recent-write window: {hits}")
        return 1
    print(f"STASH-SWEEP-WATCH: quiet ({verdict['quiet_reason']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
