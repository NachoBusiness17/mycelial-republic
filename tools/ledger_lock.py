#!/usr/bin/env python3
"""Single-writer lock + fsync append for shared JSONL ledgers. Stdlib only, Windows-safe.

Forced by the concurrent-claim falsifier (watch/inbox/BURN_b2-wave-fold_20260926_c.md):
4 self-feed renumber corrections in the next-50 window exceeded the >2 threshold,
so LEDGER.jsonl appends get the B2-360-shaped single-writer sidecar. The two collision
species this shapes against: restore-clobber duplication (concurrent whole-file restores
erase landed rows) and stale lock-holder starvation (hung PIDs hold a lock forever).

Usage (CLI):
  python tools/ledger_lock.py append --target memory/burns/LEDGER.jsonl \
      --lock memory/burns/LEDGER.lock --line '{"id": "B2-500", "...": "..."}'

Usage (programmatic):
  from tools.ledger_lock import LedgerLock, append_line
  with LedgerLock("memory/burns/LEDGER.lock"):
      append_line("memory/burns/LEDGER.jsonl", json.dumps(row))

Contract: the line is validated as JSON BEFORE the lock is acquired (invalid lines
refuse with exit 2 and never touch the lock). The appended bytes are a canonical
single-line json.dumps of the payload (the ledger's own receipt_contract: "via python
json.dumps, never heredoc"). The lockfile carries a writer identity stamp
(pid + host + acquired-at). A lock older than --stale-seconds (default 600 = 10 min)
is broken and the break is recorded in "<lock>.log". Writers adopt this cross-window;
nothing here is wired into a live writer at landing.

Adoption (2026-09-27): appends whose target is the burn ledger additionally face
tools/ledger_append_gate.validate_line BEFORE the lock (the PROBE-C fix gaining its
schedule). A gate Refusal exits 2 without touching the lock; if the gate module
cannot be imported the append also refuses (fail-closed: an ungated burn-ledger
append is the detector-miss species this wiring exists to end). Other targets keep
the JSON-only contract.

Exit codes: 0 appended, 2 invalid JSON (refused pre-lock), 3 lock held and fresh.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
from pathlib import Path

DEFAULT_STALE_SECONDS = 600  # 10 minutes; B2-450 stale-holder species

REPO = Path(__file__).resolve().parents[1]
GATED_LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"


class LockHeldError(RuntimeError):
    """The lockfile exists and is younger than the stale threshold."""


def _now_z() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _identity() -> dict:
    return {"pid": os.getpid(), "host": socket.gethostname(), "acquired": _now_z()}


class LedgerLock:
    """Single-writer lockfile: O_CREAT|O_EXCL acquire, mtime stale-break, stamped release."""

    def __init__(self, lock_path: str, stale_seconds: int = DEFAULT_STALE_SECONDS,
                 log_path: str | None = None):
        self.lock_path = lock_path
        self.stale_seconds = stale_seconds
        self.log_path = log_path or lock_path + ".log"
        self._token = None

    def _log(self, event: str, **extra) -> None:
        # pid+host stamp every row; "acquired" only on acquire rows (it names the
        # lock token's acquisition time, not this log write, so release/stale-break
        # rows must not carry it or the audit trail misstamps).
        row = {"event": event, "ts": _now_z(), "pid": os.getpid(),
               "host": socket.gethostname()}
        row.update(extra)
        with open(self.log_path, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")

    def _age_seconds(self) -> float:
        try:
            return max(0.0, time.time() - os.path.getmtime(self.lock_path))
        except FileNotFoundError:
            return 0.0

    def acquire(self) -> dict:
        """Atomically create the lockfile (O_CREAT|O_EXCL is atomic on Windows and POSIX)."""
        identity = _identity()
        while True:
            try:
                fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                age = self._age_seconds()
                if age > self.stale_seconds:
                    self._break_stale(age)
                    continue
                raise LockHeldError(
                    f"{self.lock_path} held and fresh (age {age:.0f}s, "
                    f"stale threshold {self.stale_seconds}s)"
                )
            except FileNotFoundError:
                continue  # stale-break race: loser re-loops
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(json.dumps(identity, sort_keys=True))
            self._token = identity
            self._log("acquire", acquired=identity["acquired"], target_lock=self.lock_path)
            return identity

    def _break_stale(self, age: float) -> None:
        try:
            os.remove(self.lock_path)
        except FileNotFoundError:
            return  # another waiter already broke it
        self._log("stale-break", age_seconds=round(age, 1),
                  threshold_seconds=self.stale_seconds, lock_path=self.lock_path)

    def release(self) -> None:
        """Remove the lockfile only if we are still the stamped holder."""
        if self._token is None:
            return
        token, self._token = self._token, None
        try:
            with open(self.lock_path, "r", encoding="utf-8") as f:
                holder = json.load(f)
        except (OSError, ValueError):
            holder = None
        if holder is not None and holder != token:
            self._log("release-skipped-not-holder", lock_path=self.lock_path)
            return  # our lock was broken and re-acquired elsewhere; never clobber
        try:
            os.remove(self.lock_path)
        except FileNotFoundError:
            # lock already gone (reaped or released elsewhere): the outcome
            # release wants, but named instead of silent (ratchet except-pass
            # fix 2026-09-27)
            self._log("release-already-gone", lock_path=self.lock_path)
        self._log("release", lock_path=self.lock_path)

    def __enter__(self) -> "LedgerLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.release()
        return False


def append_line(target: str, line: str) -> None:
    """Append one line to target with flush + fsync (receipt-before-disk species)."""
    with open(target, "a", encoding="utf-8", newline="\n") as f:
        f.write(line.rstrip("\n") + "\n")
        f.flush()
        os.fsync(f.fileno())


def cmd_append(args: argparse.Namespace) -> int:
    try:
        payload = json.loads(args.line)
    except ValueError as e:
        print(f"REFUSE invalid JSON line (checked before lock): {e}", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        print("REFUSE line must be a JSON object (ledger rows are objects)", file=sys.stderr)
        return 2
    parent = os.path.dirname(os.path.abspath(args.target))
    if parent:
        os.makedirs(parent, exist_ok=True)
    canonical = json.dumps(payload, ensure_ascii=False)
    # Pre-lock append gate for the burn ledger (adoption 2026-09-27). Proven at wiring
    # time: VALID on a well-formed row; REFUSE on string fresh_failure_mode, phantom
    # landing, byte-identical duplicate one_line; ledger row count unchanged through
    # all four probes. Fail-closed on ImportError: an ungated burn-ledger append is
    # the PROBE-C detector-miss species (BURN_adversarial-self-probes_20260926_d.md).
    if os.path.normpath(os.path.abspath(args.target)) == os.path.normpath(str(GATED_LEDGER)):
        try:
            from tools.ledger_append_gate import Refusal, validate_line
        except ImportError:
            sys.path.insert(0, str(REPO))
            try:
                from tools.ledger_append_gate import Refusal, validate_line
            except ImportError as e:
                print(f"REFUSE append gate unavailable ({e}); burn-ledger appends stay gated",
                      file=sys.stderr)
                return 2
        try:
            validate_line(canonical, args.target)
        except Refusal as e:
            print(f"REFUSE append gate: {e}", file=sys.stderr)
            return 2
    lock = LedgerLock(args.lock, stale_seconds=args.stale_seconds)
    try:
        lock.acquire()
    except LockHeldError as e:
        print(f"REFUSE lock held: {e}", file=sys.stderr)
        return 3
    try:
        append_line(args.target, canonical)
    finally:
        lock.release()
    print(f"OK appended 1 row to {args.target} under lock {args.lock}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("append", help="lock, fsync-append one JSONL row, unlock")
    a.add_argument("--target", required=True, help="JSONL file to append to")
    a.add_argument("--lock", required=True, help="lockfile path")
    a.add_argument("--line", required=True, help="JSON object literal for the row")
    a.add_argument("--stale-seconds", type=int, default=DEFAULT_STALE_SECONDS,
                   help=f"lock mtime age over which it is broken (default {DEFAULT_STALE_SECONDS})")
    a.set_defaults(func=cmd_append)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
