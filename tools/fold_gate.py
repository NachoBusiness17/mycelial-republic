#!/usr/bin/env python3
"""fold_gate.py - cross-run fold mutex for workflow fold phases (2026-10-05).

The disease (operator ask, 2026-10-05 evening): concurrent workflows
(day-N frontier mines, the mickey17-burn R-series consolidations) all end in
a FOLD phase, and when two runs fold at the same time they run into each
other - same-day output folders, shared watch/inbox appends, and simultaneous
giant-prompt fold dispatches on the one account - and error into retry loops
(the day-5 mine's fold published without its receipt while R4 landed in
parallel). Folds must serialize politely: a second fold WAITS, never errors,
and a dead holder (reboot species) is cleared by stale-break, not by hand.

Lock core is the tools/ledger_lock.py pattern (O_CREAT|O_EXCL acquire is
atomic on Windows and POSIX; mtime stale-break; JSONL audit trail), with one
deliberate divergence: identity is the caller-supplied --holder STRING, not a
pid - acquire and release run in different short-lived processes (separate
agent tool-calls, separate world.run bash calls), so pid-match release could
never succeed. Release removes the lock only when the holder string matches
(or --force, logged).

Never-block law: acquire waits up to --wait (default 900s) for a fresh lock;
a lock older than --stale-seconds (default 2700s = 45 min, above a fold with
two repair loops; the day-5 fold took ~11 min including its receipt retry)
is broken and taken. On wait timeout acquire exits 4 and LOGS it - callers
treat 4 as "proceed unlocked, append to shared files only via
tools/ledger_lock.py append, and note the timeout in the receipt". A fold
must never error out just because another fold is live.

Usage:
  python tools/fold_gate.py acquire  --holder "olm-mine 2026-10-05" [--name workflow-fold] [--wait 900] [--stale-seconds 2700] [--poll 3] [--dir <locks-dir>]
  python tools/fold_gate.py release  --holder "olm-mine 2026-10-05" [--name workflow-fold] [--force] [--dir <locks-dir>]
  python tools/fold_gate.py status   [--name workflow-fold] [--dir <locks-dir>]

Locks live in memory/runs/fold_locks/ (<name>.lock + <name>.lock.log audit
rows: acquire, stale-break, wait-timeout, release, release-refused,
force-release).

Exit codes: 0 success/held-or-freed-or-status, 4 acquire wait timeout,
5 release refused (not holder, or not held).

SCOPE (2026-10-07, morning-block m5): the charter below is the named list of
surfaces a fold phase must hold this gate for, so shared-write protection is
code-as-law here instead of convention memory. Amend the list in the same
commit that teaches a fold to touch a new shared surface.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_DIR = REPO / "memory" / "runs" / "fold_locks"
DEFAULT_NAME = "workflow-fold"
DEFAULT_WAIT = 900          # 15 min: a healthy fold holds the lock well inside this
DEFAULT_STALE = 2700        # 45 min: above fold + two repair loops; reboot-dead holders clear at this age
DEFAULT_POLL = 3

# The surfaces this gate serializes (the docstring SCOPE section is the law
# text; this tuple is the path list). Repo-root-relative glob patterns plus
# one non-path entry for the shared account. Sourced from the founding
# incident (2026-10-05): mickey17-v2 and gap-analysis both wrote the FIXED
# master path corpus/steal/MASTER_MICKEY17_V2.md in parallel - the
# silent-clobber species this gate is the only serializer for - and fold
# phases also append receipts to watch/inbox and dispatch giant-prompt folds
# on the one funded inference account.
SCOPE = (
    "corpus/steal/MASTER_*.md",          # fixed master paths several folds write
    "memory/runs/**/FOLD_SECTIONS.md",   # scripted fold outputs + their run dirs
    "watch/inbox/**",                    # post-fold receipt and INDEX.json appends
    "@account:funded-inference-dispatch",  # NOT a path: the one funded account; simultaneous giant-prompt fold dispatches 429-storm it
)


class FoldGate:
    def __init__(self, name: str, lock_dir: str):
        self.dir = Path(lock_dir)
        self.lock_path = self.dir / (name + ".lock")
        self.log_path = self.dir / (name + ".lock.log")

    def _log(self, event: str, **extra) -> None:
        row = {"event": event, "ts": _now_z(), "pid": os.getpid(),
               "host": socket.gethostname()}
        row.update(extra)
        with open(self.log_path, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")

    def read_stamp(self) -> dict | None:
        try:
            with open(self.lock_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def _age(self) -> float:
        try:
            return max(0.0, time.time() - os.path.getmtime(self.lock_path))
        except FileNotFoundError:
            return 0.0

    def _try_create(self, holder: str) -> bool:
        self.dir.mkdir(parents=True, exist_ok=True)
        stamp = {"holder": holder, "host": socket.gethostname(),
                 "pid": os.getpid(), "acquired": _now_z()}
        try:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return False
        except FileNotFoundError:
            return False  # stale-break race: loser re-loops
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(stamp, sort_keys=True))
        self._log("acquire", holder=holder, stamp=stamp)
        return True

    def acquire(self, holder: str, wait: int, stale: int, poll: int) -> int:
        deadline = time.monotonic() + max(0, wait)
        while True:
            if self._try_create(holder):
                print(f"HELD {self.lock_path} holder={holder}")
                return 0
            age = self._age()
            if age > stale:
                try:
                    os.remove(self.lock_path)
                except FileNotFoundError:
                    pass  # another waiter broke it first
                else:
                    stamp = self.read_stamp()  # None post-remove; log what we can
                    self._log("stale-break", age_seconds=round(age, 1),
                              threshold_seconds=stale, prior_holder=(stamp or {}).get("holder", "unknown"))
                continue
            if time.monotonic() >= deadline:
                cur = self.read_stamp()
                self._log("wait-timeout", holder=holder, wait_seconds=wait,
                          held_by=(cur or {}).get("holder", "unknown"),
                          held_age_seconds=round(age, 1))
                print(f"TIMEOUT lock {self.lock_path} still held by "
                      f"{(cur or {}).get('holder', 'unknown')} (age {age:.0f}s); "
                      f"proceed unlocked, shared appends via tools/ledger_lock.py append",
                      file=sys.stderr)
                return 4
            time.sleep(max(1, poll))

    def release(self, holder: str, force: bool) -> int:
        stamp = self.read_stamp()
        if stamp is None:
            print(f"FREE {self.lock_path} (nothing held)")
            return 0
        if not force and stamp.get("holder") != holder:
            self._log("release-refused", caller=holder,
                      held_by=stamp.get("holder"))
            print(f"REFUSE {self.lock_path} held by {stamp.get('holder')!r}, "
                  f"not {holder!r}; use --force to override", file=sys.stderr)
            return 5
        try:
            os.remove(self.lock_path)
        except FileNotFoundError:
            self._log("release-already-gone", caller=holder)
            print(f"FREE {self.lock_path} (already released)")
            return 0
        self._log("force-release" if force else "release", caller=holder,
                  prior_holder=stamp.get("holder"))
        print(f"RELEASED {self.lock_path} by {holder}" + (" (forced)" if force else ""))
        return 0

    def status(self) -> int:
        stamp = self.read_stamp()
        if stamp is None:
            print(f"FREE {self.lock_path}")
        else:
            age = self._age()
            print(f"HELD {self.lock_path} holder={stamp.get('holder')} "
                  f"host={stamp.get('host')} age={age:.0f}s")
        return 0


def _now_z() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="cross-run fold mutex")
    sub = p.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--name", default=DEFAULT_NAME)
    common.add_argument("--dir", default=str(DEFAULT_DIR))
    a = sub.add_parser("acquire", parents=[common])
    a.add_argument("--holder", required=True)
    a.add_argument("--wait", type=int, default=DEFAULT_WAIT)
    a.add_argument("--stale-seconds", type=int, default=DEFAULT_STALE)
    a.add_argument("--poll", type=int, default=DEFAULT_POLL)
    r = sub.add_parser("release", parents=[common])
    r.add_argument("--holder", required=True)
    r.add_argument("--force", action="store_true")
    s = sub.add_parser("status", parents=[common])
    args = p.parse_args(argv)
    gate = FoldGate(args.name, args.dir)
    if args.cmd == "acquire":
        return gate.acquire(args.holder, args.wait, args.stale_seconds, args.poll)
    if args.cmd == "release":
        return gate.release(args.holder, args.force)
    return gate.status()


if __name__ == "__main__":
    sys.exit(main())
