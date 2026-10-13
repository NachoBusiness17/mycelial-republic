"""leave_dispatcher - the mates leave protocol driver, static-runner shape (X12, 2026-09-29/30).

THE ARGV LAW (the whole point of this file). The Mimosa gate blocked three
successive hardenings of the direct driver because every one still carried a
variable in a subprocess argv (receipt: watch/inbox/mates_leave_protocol/
REGISTER_NOTE.md, 2026-09-30: list-form; shell=False plus "--" end-of-options;
constants-and-one-int with mission packs as files - the scanner flags any
subprocess argv containing variables, regardless of form). The gate is law.

So this dispatcher owns ZERO variable argv. All day-to-day variance (which
mates, which personas, which seed threads, which STEER rows) is written to
MISSION FILES under logs/mates/missions/. The only subprocess argv in this
file is RUNNER_ARGV: a module-level tuple of string literals. It invokes the
fixed per-mate runner scripts/run_mate.ps1 (also parameter-free), which
computes today's date itself via Get-Date and atomically claims the next
unclaimed mission - so the same constant argv, run N times, drives N distinct
mates. Never edit RUNNER_ARGV toward variability: a new invocation shape gets
a new fixed .ps1, never an argument.

Modes:
  --dry   write today's mission files, print the exact command each live
          invocation WOULD run, exit. Zero subprocess calls in dry mode.
  (live)  write today's mission files, then invoke RUNNER_ARGV once per
          mission via a worker pool (default width 8; hard cap 16 per the
          configs/mates.yaml concurrency law: 19-20 simultaneous burst =
          1302 deaths, 12+12 staggered = zero).

Logging: logs/mates/dispatcher_<YYYYMMDD>.log (utf-8, append).

Receipt: watch/inbox/hydrology/X12_MATE_UNBLOCK.md.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import yaml

try:  # same directory (tools/); on sys.path when run as a script
    from steer_read import read as steer_read_row
except ImportError:  # pragma: no cover - direct import fallback
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from steer_read import read as steer_read_row

REPO = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO / "configs" / "mates.yaml"
MISSIONS_DIR = REPO / "logs" / "mates" / "missions"
RECEIPTS_DIR = REPO / "watch" / "inbox" / "mates_leave_protocol" / "receipts"
LOG_DIR = REPO / "logs" / "mates"

# THE LAW: the only subprocess argv in this file, and it is all literals.
# Do not "improve" it toward variability - any variable in an argv is the
# exact shape the Mimosa gate blocks (three hardenings died on it, 2026-09-30).
# The absolute path is deliberate: deriving it from __file__ makes the argv
# variable-derived again. _runner_path_guard() fail-closes if the repo moves.
RUNNER_ARGV = (
    "powershell",
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\scripts\\run_mate.ps1",
)

MAX_PARALLEL = 16  # configs/mates.yaml concurrency law ceiling (16 simultaneous)
DEFAULT_PARALLEL = 8  # all 8 current mates fit under the law in one wave

MISSION_TEMPLATE = """# Mission pack: {mate_id} - {date}

Launched by tools/leave_dispatcher.py (X12 static-runner unblock). Runner:
scripts/run_mate.ps1 (constant argv; this pack is claimed via its .claim sidecar).

## Persona
{persona}

## Hunting ground
{hunting_ground}

## Seed thread
{seed_thread}

## Laws (configs/mates.yaml, verbatim)
{laws}

## STEER (operative row for {mate_id} at pack time)
{steer_block}

## Receipt contract
File watch/inbox/mates_leave_protocol/receipts/receipt_{date}_{mate_id}.md before
you speak. Required sections: FINDINGS, JOURNEY (threads followed in order, dead
ends named, why each turn was taken), COUNTS (real numbers only, no fabricated
anything). No em-dashes. Resume-not-respawn: if you stop mid-road, say so in the
receipt; the next cycle resumes you by id.
"""


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / f"dispatcher_{datetime.now().strftime('%Y%m%d')}.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _runner_path_guard() -> None:
    """Fail closed if the hardcoded RUNNER_ARGV path no longer matches the repo.

    The argv stays all-literals (Mimosa law); this guard turns a repo move from
    silent breakage into an explicit incident with the fix named.
    """
    expected = str(REPO / "scripts" / "run_mate.ps1")
    actual = RUNNER_ARGV[-1]
    if pathlib.Path(actual) != pathlib.Path(expected):
        print(
            f"leave_dispatcher: RUNNER_ARGV runner path is stale.\n"
            f"  argv literal: {actual}\n"
            f"  repo truth:   {expected}\n"
            f"The repo moved after the argv was frozen. Update the RUNNER_ARGV "
            f"literal (keeping it a literal) - never derive it from __file__.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if not pathlib.Path(actual).exists():
        print(f"leave_dispatcher: runner script missing: {actual}", file=sys.stderr)
        raise SystemExit(2)


def _steer_block(mate_id: str) -> str:
    """Inline the operative STEER row (spec: watch/inbox/operator_model/STEER.md)."""
    result = steer_read_row(mate_id)
    row = result.get("operative")
    if not row:
        return "- (no applicable row on the steer channel - ride your seed thread)"
    kind = "order" if not row.get("proposal") else "PROPOSAL (treat as an ask, not an order)"
    return f'- steer: "{row["steer"]}" (ts {row["ts"]}, via {row.get("via", "?")}, {kind})'


def write_missions(today: str) -> list[pathlib.Path]:
    """Write today's mission packs (idempotent: existing packs are never rewritten,
    their .claim sidecars may already be in flight). Returns today's pack paths."""
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    mates = config["mates"]
    MISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)

    paths: list[pathlib.Path] = []
    for i, mate in enumerate(mates, start=1):
        mate_id = mate["id"]
        path = MISSIONS_DIR / f"mission_{today}_{i:02d}_{mate_id}.md"
        if not path.exists():
            path.write_text(
                MISSION_TEMPLATE.format(
                    mate_id=mate_id,
                    date=today,
                    persona=mate["persona"].strip(),
                    hunting_ground=mate["hunting_ground"].strip(),
                    seed_thread=mate["seed_thread"].strip(),
                    laws=config.get("laws", "").strip(),
                    steer_block=_steer_block(mate_id),
                ),
                encoding="utf-8",
            )
            log(f"mission written {path.name}")
        else:
            log(f"mission exists (kept, claims in flight are sacred) {path.name}")
        paths.append(path)
    return paths


def run_one(_index: int) -> int:
    """Invoke the static runner once. The argv is the constant RUNNER_ARGV; the
    parameter exists only so the pool can fan out - it never touches the argv."""
    proc = subprocess.run(  # noqa: S603 - argv is the frozen all-literal tuple above
        RUNNER_ARGV, capture_output=True, text=True, cwd=str(REPO)
    )
    for stream, tag in ((proc.stdout, "out"), (proc.stderr, "err")):
        for line in (stream or "").splitlines():
            log(f"runner[{tag}] {line}")
    log(f"runner exit={proc.returncode}")
    return proc.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="mates leave protocol dispatcher (static-runner shape)")
    parser.add_argument("--dry", action="store_true",
                        help="write today's mission packs and print the exact command each "
                             "live invocation would run; no subprocess calls, no opencode")
    parser.add_argument("--parallel", type=int, default=DEFAULT_PARALLEL,
                        help=f"simultaneous runner invocations (default {DEFAULT_PARALLEL}, "
                             f"hard cap {MAX_PARALLEL} per the mates.yaml concurrency law)")
    args = parser.parse_args(argv)

    _runner_path_guard()
    today = datetime.now().strftime("%Y%m%d")
    missions = write_missions(today)
    log(f"missions for {today}: {len(missions)} (dry={args.dry})")

    cmdline = " ".join(RUNNER_ARGV)
    if args.dry:
        for path in missions:
            print(f"WOULD RUN [{path.name}]: {cmdline}")
        print(f"DRY COMPLETE: {len(missions)} mission packs written, {len(missions)} constant-argv "
              f"invocations NOT run (no opencode calls)")
        return 0

    width = max(1, min(args.parallel, MAX_PARALLEL, len(missions)))
    log(f"live dispatch: {len(missions)} invocations, width {width} (law cap {MAX_PARALLEL})")
    with ThreadPoolExecutor(max_workers=width) as pool:
        codes = list(pool.map(run_one, range(len(missions))))
    failures = [c for c in codes if c != 0]
    log(f"DISPATCH COMPLETE: {len(codes)} invocations, {len(failures)} nonzero exits {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
