#!/usr/bin/env python3
"""instance_guard - shared singleton + per-ask claim guards.

Born from the dogfood-48h ractor moves 1+4 (2026-10-02,
watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md): $25.53 of the
window's $37.76 paid hermes ledger was re-fire excess, the celebrated twin
kill covered ~4.5 pct of that class, and exactly 1 of 11 long-running scripts
carried any guard. One module swept everywhere, so the next drainer cannot
re-open the class (the unwired-organ law: a fix that does not sweep its
siblings is unfinished).

Shapes:
- claim_process / guard_or_exit: pidfile singleton with exit-3 semantics and
  stale-pid reclaim (the scripts/descent_driver.sh guard lifted to python).
- claim_ask / release_ask: O_EXCL per-ask CLAIM at the fire path. Two racers
  that both pass the landed-skip check cannot both pay for the same ask.
- ledger_key_exists / doubled_key_check: the ingest-side tripwire that
  alarms when the same (id, turn) is banked twice.

Liveness law (T1W1 RACTOR V1 + 12h-run orchestrator fix): on Windows
os.kill(pid, 0) is NOT a probe (sig 0 is CTRL_C_EVENT through
GenerateConsoleCtrlEvent; it can send a real Ctrl+C or misreport dead pids),
so psutil.pid_exists is preferred with a tasklist fallback.
"""
from __future__ import annotations

import atexit
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InstanceBusy(RuntimeError):
    """Another live instance holds the claim. Callers exit 3 (the descent
    driver contract: loud refusal, never a silent double-drain)."""


def _pid_alive(pid: int | None) -> bool:
    if not pid or pid <= 0:
        return False
    try:
        import psutil
    except Exception:  # psutil optional on minimal venvs; fallbacks below
        psutil = None
    if psutil is not None:
        return psutil.pid_exists(pid)
    if sys.platform == "win32":
        # psutil-free fallback, authoritative on Windows: tasklist filter.
        try:
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True, text=True, timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            ).stdout
            return str(pid) in out
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _read_pid(path: Path) -> int | None:
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def claim_process(name: str, pid_dir: Path | None = None) -> Path:
    """Claim the named singleton; raises InstanceBusy if a live holder has
    it. A stale pidfile (holder pid dead / unparseable) is reclaimed. The
    claim self-releases on normal interpreter exit via atexit; a killed
    holder leaves the pidfile for the next start's stale-reclaim path.

    Reclaim race note: two simultaneous starters of a dead holder can both
    replace the pidfile (last-wins, a microseconds window against 45s driver
    cycles - same accepted window the bash guard carries). The money-tight
    race is the per-ask O_EXCL claim, not this one."""
    pid_dir = pid_dir or (ROOT / "state")
    pid_dir.mkdir(parents=True, exist_ok=True)
    path = pid_dir / f"{name}.pid"
    if path.exists():
        old = _read_pid(path)
        if old is not None and _pid_alive(old):
            raise InstanceBusy(
                f"{name}: instance pid {old} already running; refusing to start")
        print(f"INSTANCE-GUARD: {name}: stale pidfile (pid {old} dead); "
              f"reclaiming", file=sys.stderr)
    tmp = path.with_suffix(".pid.tmp")
    tmp.write_text(str(os.getpid()), encoding="utf-8")
    os.replace(tmp, path)

    def _release() -> None:
        if _read_pid(path) == os.getpid():
            try:
                path.unlink()
            except OSError as exc:
                print(f"INSTANCE-GUARD: pidfile release failed for {path}: "
                      f"{exc}", file=sys.stderr)

    atexit.register(_release)
    return path


def guard_or_exit(name: str, pid_dir: Path | None = None) -> Path:
    """claim_process with the exit-3 contract wired: the one-liner loops
    call at entry. Returns the pidfile path on success; never returns on a
    busy claim (exits 3, loud, the descent-driver semantics)."""
    try:
        return claim_process(name, pid_dir)
    except InstanceBusy as exc:
        print(f"INSTANCE-GUARD: {exc}", file=sys.stderr)
        sys.exit(3)


def claim_ask(ask_dir: Path, ask_id: str,
              stale_seconds: float = 1800.0) -> Path | None:
    """Atomically claim one ask fire. Returns the marker Path when claimed,
    None when a fresh live holder holds it (caller skips the paid call).
    A claim is stale when its holder pid is dead or it aged past
    stale_seconds (a fire can legitimately take minutes; 1800s covers the
    longest observed paid turn with margin); stale claims are stolen."""
    marker = ask_dir / "CLAIM"
    payload = json.dumps({"pid": os.getpid(), "ts": round(time.time(), 3),
                          "id": ask_id})
    try:
        fd = os.open(str(marker), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            holder = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            holder = {}
        hpid, hts = holder.get("pid"), float(holder.get("ts") or 0)
        fresh = time.time() - hts < stale_seconds
        if isinstance(hpid, int) and _pid_alive(hpid) and fresh:
            return None
        print(f"INSTANCE-GUARD: ask {ask_id}: stale CLAIM (pid {hpid}, "
              f"age {int(time.time() - hts)}s); stealing", file=sys.stderr)
        marker.write_text(payload, encoding="utf-8")
        return marker
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(payload)
    return marker


def release_ask(marker: Path | None) -> None:
    """Release a claim we still own (a stolen-over marker is left alone)."""
    if marker is None:
        return
    try:
        holder = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return  # unreadable marker: nothing we can prove we own
    if holder.get("pid") == os.getpid():
        try:
            marker.unlink()
        except OSError as exc:
            print(f"INSTANCE-GUARD: release failed for {marker}: {exc}",
                  file=sys.stderr)


def ledger_key_exists(ledger: Path, ask_id: str, turn: int | None,
                      tail: int = 1000) -> bool:
    """True when (id, turn) already rows the ledger - the re-fire signature
    (13 doubled keys burned $2.25 in the twins window; A1 alone re-fired 49x
    for $21.09). Tail-bounded so ingest stays cheap as the ledger grows."""
    if not ledger.exists() or ask_id is None:
        return False
    try:
        lines = ledger.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False
    for line in lines[-tail:]:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("id") == ask_id and row.get("turn") == turn:
            return True
    return False


def doubled_key_check(ledger: Path, row: dict) -> dict:
    """Ingest-side tripwire: stamp + alarm when a banked row repeats an
    (id, turn) already in the ledger. Returns the row to bank (flagged or
    as-is). The alarm lands in memory/attention.md, the estate alarm
    surface (the FTS-law channel).
    DEDUP (2026-10-03): the alarm appends ONCE per (id, turn); repeat fires
    still stamp the row but do not re-append. The 2026-10-03 DND0/TAVERN
    cross-session id collisions flooded attention.md with 800+ duplicate
    alarm lines (one every ~5s for hours), burying every other alarm on the
    surface. Receipt: watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md."""
    ask_id, turn = row.get("id"), row.get("turn")
    if ask_id is None or turn is None or not ledger_key_exists(
            ledger, str(ask_id), turn):
        return row
    flagged = dict(row)
    flagged["doubled_key"] = True
    attention = ROOT / "memory" / "attention.md"
    sig = f"already rows (id={ask_id}, turn={turn})"
    line = (f"- [x] INSTANCE-GUARD doubled-key alarm {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: "
            f"ledger {ledger.name} already rows (id={ask_id}, turn={turn}); "
            f"this fire is a re-fire (dogfood-48h move 1 ingest tripwire)\n")
    try:
        attention.parent.mkdir(parents=True, exist_ok=True)
        text = (attention.read_text(encoding="utf-8", errors="replace")
                if attention.is_file() else "")
        if sig not in text:  # one alarm line per key keeps the surface readable
            with open(attention, "a", encoding="utf-8") as fh:
                fh.write(line)
    except OSError as exc:  # a silent alarm failure hides a live money bug
        print(f"INSTANCE-GUARD: attention alarm write failed: {exc}",
              file=sys.stderr)
    return flagged


if __name__ == "__main__":
    print(__doc__)
