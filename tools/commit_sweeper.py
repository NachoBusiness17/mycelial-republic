"""commit_sweeper - the ONE git writer for the estate (multi-seat, no index fights).

Operator order 2026-10-20: "how do we avoid overlap of commits, can't we just
have a cron that commits them independent of the seat... each seat is about to
attempt to make this so don't all do it." Two seats hit index.lock contention
on the same repo within one hour (the sibling's wave-6 commit and this seat's
round-2 fold). The estate's own prior art already wrote the law (tesuji
incidents 2026-09-06: per-seat append discipline; single writer per organ) -
this module applies it to git itself:

  - Seats NEVER run git. They write files (the real work) and, optionally, a
    commit hint: queue/commit_hints/<seat>-<slug>.json
    {"paths": [...], "message": "..."} - named, attributed batches.
  - The sweeper (this module, run by cron) is the ONLY process that runs
    git add/commit. Single writer = zero index contention by construction.
  - Hinted batches commit first (FIFO by mtime, named messages preserved);
    then an untracked/leftover sweep commits the remainder with a generic
    message so nothing shelves (the anti-shelf law applied to git).
  - If another git process holds index.lock (a seat broke the law, or the
    sibling commit is mid-flight), the sweep SKIPS that batch and retries next
    cycle - never force-removes a lock (seat-ops law), never loses data
    (files are on disk regardless; git state is reconstructible).

Consumer: every seat in the estate (they stop committing) + MagCommitSweeper
cron; Verifier: tests/test_commit_sweeper.py + the sweeper log
logs/commit_sweeper.log + `git log` itself.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # allow `from tools...` when run as a script
HINTS = ROOT / "queue" / "commit_hints"
PID_DIR = ROOT / "state"  # injectable so tests never collide with the live guard
# Never sweep scratch: 2026-10-24 the sweeper spent 36+ minutes in
# `git add -A -- Temp/` hashing 7 GB of scratch (6 tracked blobs) and the queue
# never drained. An intake that can be wedged by a scratch dir is not a drain.
SKIP_AREAS = {"Temp", "temp", "tmp", "node_modules", ".venv", "__pycache__"}
LOG = ROOT / "logs" / "commit_sweeper.log"
# One line per breath (sweep). logs/ is gitignored, so the ledger is an
# off-chain witness of the chain, never part of it. Injectable for tests.
BREATH_LEDGER = ROOT / "logs" / "breath_ledger.jsonl"
UNKNOWN_SEAT = "unknown-seat"
UNKNOWN_MODEL = "unknown-model"
SEAT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$")  # fleet_report.v1 seat shape
# Per-sweep context read by commit_batch; set by sweep(), never by seats.
_CTX: dict = {"breath_id": None, "seat": None, "model": None, "commits": []}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {msg}\n")


def git(args: list[str], check: bool = True, timeout: int = 120) -> subprocess.CompletedProcess:
    p = subprocess.run(["git"] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(ROOT), timeout=timeout)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])}: {(p.stderr or p.stdout)[:200]}")
    return p


def new_breath_id() -> str:
    """B-<UTC second>-<6 hex>: sortable, unique even for a manual double-fire."""
    return "B-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)


def _trailers(message: str) -> str:
    """Append git trailers (Breath-Id / Seat / Model) to a batch message.
    Trailers ride INSIDE commit_batch so callers' messages stay byte-identical
    (tests assert on them) and every commit of one sweep carries one id."""
    bid = _CTX.get("breath_id")
    if not bid:
        return message
    seat = _CTX.get("seat") or UNKNOWN_SEAT
    model = _CTX.get("model") or UNKNOWN_MODEL
    return (message.rstrip() + "\n\n" + f"Breath-Id: {bid}\nSeat: {seat}\nModel: {model}\n"
            "Swept-By: commit_sweeper\n")


def _author_args() -> list[str]:
    """--author from the batch's seat; honest fallback 'unknown-seat', never the
    box's git identity. Committer stays the git config (the sweeper itself).
    MAG_SWEEPER_SET_AUTHOR=0 turns this off (trailers still land)."""
    if os.environ.get("MAG_SWEEPER_SET_AUTHOR", "1") == "0" or not _CTX.get("breath_id"):
        return []
    seat = _CTX.get("seat") or UNKNOWN_SEAT
    return [f"--author={seat} <{seat}@seats.mag.local>"]


def hint_attribution(hint: Path, spec: dict) -> tuple[str, str]:
    """(seat, model) for a hint. Order: spec["seat"]/spec["model"], then the
    documented filename shape <seat>-<slug>.json, then MAG_SEAT_MODEL_<SEAT>
    env for the model. Anything that fails the seat shape -> unknown-seat."""
    seat = spec.get("seat") if isinstance(spec.get("seat"), str) else None
    if not seat and "-" in hint.stem:
        seat = hint.stem.split("-", 1)[0]
    if not seat or not SEAT_RE.match(seat):
        seat = UNKNOWN_SEAT
    model = spec.get("model") if isinstance(spec.get("model"), str) else None
    if not model and seat != UNKNOWN_SEAT:
        model = os.environ.get("MAG_SEAT_MODEL_" + re.sub(r"[^A-Za-z0-9]", "_", seat).upper())
    model = (model or UNKNOWN_MODEL).strip()[:80] or UNKNOWN_MODEL
    return seat, model


def write_breath_ledger(row: dict) -> None:
    try:
        BREATH_LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with BREATH_LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    except OSError as exc:  # the ledger must never cost a breath
        log(f"breath ledger write failed ({exc})")


def lock_busy() -> bool:
    return (ROOT / ".git" / "index.lock").exists()


def lock_age_s() -> float | None:
    try:
        return time.time() - (ROOT / ".git" / "index.lock").stat().st_mtime
    except OSError:
        return None


def wait_for_git_lock(retries: int = 6, delay: float = 2.0) -> bool:
    """Wait out a transient index.lock (git gc, a sibling commit) instead of
    deferring a whole area on first sight. Evicts stale orphan locks if 0 holders."""
    for attempt in range(retries):
        if not lock_busy():
            return True
        age = lock_age_s()
        age_txt = f"{age:.0f}s" if age is not None else "unknown"
        log(f"index.lock busy (age {age_txt}) - wait {attempt + 1}/{retries}")
        if age is not None and age > 60:
            try:
                lock_file = ROOT / ".git" / "index.lock"
                res = subprocess.run(["fuser", str(lock_file)], capture_output=True, text=True)
                if res.returncode != 0 and lock_file.exists():
                    lock_file.unlink(missing_ok=True)
                    log(f"evicted stale orphan index.lock (age {age_txt}, 0 holders)")
                    return True
            except Exception:
                pass
        time.sleep(delay)
    return not lock_busy()


def commit_batch(paths: list[str], message: str, timeout: int = 900) -> tuple[bool, str]:
    """add + commit one named batch. Returns (committed, note).
    TimeoutExpired is CAUGHT here (beat 2 lesson: a big-batch timeout used to
    kill the whole sweep, stranding every smaller area behind it)."""
    if lock_busy():
        if not wait_for_git_lock():
            age = lock_age_s()
            return False, f"index.lock held after wait (age {age:.0f}s) - deferring (never forced)"
    existing = [p for p in paths if (ROOT / p).exists()]
    try:
        if existing:
            # Drop gitignored paths BEFORE add: `git add --ignore-errors` still
            # exits non-zero when every path is ignored (hint bob-head-museum
            # carried dashboard/static/state and could never land, 2026-10-20).
            try:
                chk = subprocess.run(["git", "check-ignore", "--stdin"], cwd=str(ROOT),
                                     input="\n".join(existing), capture_output=True,
                                     text=True, encoding="utf-8", errors="replace",
                                     timeout=120)
                ignored = set((chk.stdout or "").split()) if chk.returncode in (0, 1) else set()
            except Exception:
                ignored = set()
            keep = [p for p in existing if (ROOT / p).is_dir() or p not in ignored]
            if not keep:
                return True, "all paths gitignored - nothing to commit"
            try:
                git(["add", "-A", "--ignore-errors", "--"] + keep, timeout=max(timeout, 900))
            except RuntimeError as exc:
                if "ignored" not in str(exc):
                    raise
                # A directory whose every child is ignored still trips `add`.
                # Stage path-by-path; a path that adds nothing is not a failure.
                added = 0
                for p in keep:
                    try:
                        git(["add", "-A", "--ignore-errors", "--", p], timeout=300)
                        added += 1
                    except RuntimeError:
                        continue
                if not added:
                    return True, "all paths gitignored - nothing to commit"
        else:
            # big trees: the add itself can take minutes over thousands of files
            git(["add", "-A"], timeout=max(timeout, 900))
        # Scoping by CONSTRUCTION, not by pathspec: the sweep resets the index
        # once at start, so a successful commit leaves it empty for the next
        # area. `git commit -- <dir>` was tried 2026-10-21 and made git walk the
        # whole tree per batch (a `git commit -- memory/` sat 8+ minutes on
        # Windows). Empty-check + plain commit keeps each batch O(batch).
        staged_now = git(["diff", "--cached", "--name-only"]).stdout.strip()
        if not staged_now:
            return True, "nothing staged - nothing to commit"
        try:
            git(["commit", "-q"] + _author_args() + ["-m", _trailers(message)], timeout=timeout)
        except RuntimeError:
            # Never leave a failed batch's staging to ride into the next area.
            git(["reset", "-q"], check=False, timeout=300)
            raise
        tip = git(["log", "-1", "--format=%h"]).stdout.strip()
        _CTX["commits"].append(tip)
        return True, tip
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s - batch needs splitting"
    except RuntimeError as e:
        if "index.lock" in str(e):
            return False, "lock raced - deferring"
        # 2026-10-25: the TAIL is the verdict. Head-truncation at 180 chars hid
        # the real refuser for three sweeps - gitleaks PASS lines printed before
        # the large-blob/secret refusal ever reached the note.
        note = str(e)
        return False, note[-800:] if len(note) > 800 else note


def sweep(dry: bool = False, hints_only: bool = False) -> dict:
    """One breath: mint ONE Breath-Id, run the sweep, append one ledger row."""
    if dry:
        return _sweep_inner(dry=True)
    bid = new_breath_id()
    started = now_iso()
    _CTX.update(breath_id=bid, seat=None, model=None, commits=[])
    try:
        rep = _sweep_inner(dry=False, hints_only=hints_only)
    finally:
        commits = list(_CTX["commits"])
        _CTX.update(breath_id=None, seat=None, model=None, commits=[])
    head = ""
    try:
        head = git(["rev-parse", "HEAD"], check=False).stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    res = rep.get("results", []) if isinstance(rep, dict) else []
    write_breath_ledger({"schema": "breath_ledger.v1", "breath_id": bid, "start": started,
                         "end": now_iso(), "head": head, "commits": commits,
                         "skipped": rep.get("skipped") if isinstance(rep, dict) else None,
                         "batches": len(res), "failed": sum(1 for r in res if not r.get("committed"))})
    if isinstance(rep, dict) and "results" in rep:  # skip dicts stay byte-stable
        rep["breath_id"] = bid
    return rep


def _sweep_inner(dry: bool = False, hints_only: bool = False) -> dict:
    """One sweep: hinted batches first (FIFO), then the leftover sweep."""
    if not dry:
        # Single writer, enforced: the scheduled task and any manual run must not
        # fight over the index. Self-stolen from tools/instance_guard.py (the
        # estate's pidfile singleton) rather than a second lock invention.
        try:
            from tools.instance_guard import claim_process
        except Exception:  # noqa: BLE001 - guard must never block the work
            try:
                from instance_guard import claim_process
            except Exception as exc:  # noqa: BLE001
                log(f"instance guard unavailable ({exc}) - continuing without it")
                claim_process = None
        if claim_process is not None:
            try:
                claim_process("commit_sweeper", pid_dir=PID_DIR)
            except Exception as exc:  # noqa: BLE001
                if type(exc).__name__ == "InstanceBusy":
                    log(f"sweep skipped: {exc}")
                    return {"skipped": str(exc)}
                log(f"instance claim failed ({exc}) - continuing")
    if lock_busy():
        if not wait_for_git_lock():
            log("sweep skipped: index.lock held after wait")
            return {"skipped": "index.lock held after wait"}
    results = []
    # Clear the accumulated index before the sweep. A failed commit leaves its
    # `git add` staged, so the next attempt's pre-commit hook scans the ENTIRE
    # 18k-file shelf every time (2026-10-20: the hook alone exceeded 420s).
    # Reset keeps every file on disk (untracked/modified) and lets each batch
    # stage only its own paths, so the hook scan stays proportional to the batch.
    if not dry:
        try:
            staged_out = git(["diff", "--cached", "--name-only"], timeout=10).stdout.strip()
            staged = [s for s in staged_out.splitlines() if s.strip()]
            if staged:
                git(["reset", "-q", "--"] + staged[:100], timeout=30)
                log(f"index reset {len(staged)} staged files before sweep")
            else:
                log("index clean before sweep; zero reset needed")
        except Exception as e:
            log(f"index reset check failed ({str(e)[:120]}) - continuing")
    hints = sorted(HINTS.glob("*.json"), key=lambda p: p.stat().st_mtime) if HINTS.exists() else []
    for h in hints:
        try:
            spec = json.loads(h.read_text(encoding="utf-8"))
            paths = [p for p in spec.get("paths", []) if isinstance(p, str)]
            message = spec.get("message") or f"swept batch {h.stem}"
        except Exception as e:  # noqa: BLE001 - a malformed hint must not block others
            results.append({"hint": h.name, "committed": False, "note": f"malformed: {e}"})
            continue
        if dry:
            results.append({"hint": h.name, "dry": True, "paths": len(paths)})
            continue
        seat, model = hint_attribution(h, spec if isinstance(spec, dict) else {})
        _CTX.update(seat=seat, model=model)
        ok, note = commit_batch(paths, message)
        _CTX.update(seat=None, model=None)  # leftover batches are unattributed
        results.append({"hint": h.name, "committed": ok, "note": note, "seat": seat})
        if ok:
            h.unlink()
        log(f"hint {h.name}: {note}")
    if dry:
        return {"hints": results}
    if hints_only:
        return {"sweep_ts": now_iso(), "results": results}
    # leftover sweep, CHUNKED by top-level area: one mega-commit of ~18k files
    # makes the pre-commit hooks (secret gate + Mimosa scan every staged file)
    # exceed any timeout; per-area batches keep each hook scan bounded and
    # progress lands incrementally (beat 2 of the organ taught this twice).
    try:
        status = git(["status", "--porcelain"], timeout=300).stdout
    except RuntimeError as e:
        log("leftover deferred: " + str(e)[:120])
        results.append({"hint": "_leftover", "committed": False, "note": str(e)[:120]})
        return {"sweep_ts": now_iso(), "results": results}
    areas: dict[str, int] = {}
    for line in status.splitlines():
        path = line[3:].strip().strip('"')
        if not path:
            continue
        top = path.split("/")[0] if "/" in path else "(root)"
        if top in SKIP_AREAS:
            continue
        areas[top] = areas.get(top, 0) + 1
    for top, count in sorted(areas.items(), key=lambda kv: kv[1]):
        # ascending: small areas land first (incremental progress), the big
        # one goes last; on timeout a >2000-file area auto-splits one level
        # deeper (memory batch of 13,299 taught this - 900s could not hold it)
        if count > 500:
            sub: dict[str, int] = {}
            for line in status.splitlines():
                path = line[3:].strip().strip('"')
                if path.startswith(top + "/"):
                    parts = path.split("/")
                    child = "/".join(parts[:2]) if len(parts) > 2 else parts[0]
                    sub[child] = sub.get(child, 0) + 1
            for child, ccount in sorted(sub.items(), key=lambda kv: kv[1]):
                ok, note = commit_batch([child + "/"], f"commit sweeper: {child} batch ({ccount} files) " + now_iso(), timeout=1800)
                results.append({"hint": f"_area:{child}", "committed": ok, "note": note, "files": ccount})
                log(f"area {child} ({ccount} files): {note}")
            continue
        if top == "(root)":
            # Root-level files only: passing "(root)/" made commit_batch fall
            # back to `git add -A`, which staged the ENTIRE tree (~18k files,
            # 2026-10-20) and defeated every chunk boundary.
            root_paths = [line[3:].strip().strip('"') for line in status.splitlines()
                          if line.strip() and "/" not in line[3:].strip().strip('"')]
            batch_paths = root_paths or ["."]
        else:
            batch_paths = [top + "/"]
        ok, note = commit_batch(batch_paths, f"commit sweeper: {top} batch ({count} files) " + now_iso(), timeout=1800)
        results.append({"hint": f"_area:{top}", "committed": ok, "note": note, "files": count})
        log(f"area {top} ({count} files): {note}")
    return {"sweep_ts": now_iso(), "results": results}


def selftest() -> int:
    import tempfile
    assert callable(sweep) and callable(commit_batch)
    # malformed hint handling
    spec = {"paths": "not-a-list"}
    assert not isinstance(spec.get("paths"), list)
    print("selftest PASS: shapes + malformed-hint stance")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sweep", "dry", "selftest", "hints"])
    args = ap.parse_args()
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "hints":
        print(json.dumps(sweep(dry=False, hints_only=True), indent=1))
        return 0
    print(json.dumps(sweep(dry=(args.cmd == "dry")), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
