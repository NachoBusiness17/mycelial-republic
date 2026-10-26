"""Orphan census for the shared inbox (Mickey17 wave 3, 2026-09-29).

Drift-style join of what is on disk under watch/inbox against what the
append-only event log ever saw, plus the new consumption dimension. This is
the derived READ/DEAD-LETTER INDEX the return-5 edge-miner asked for
(watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md): one consume op
(tools/inbox_consume.py) plus one disk-walk join, so the never-read class is
visible before it is re-written.

Headline classes (the three the lane was asked to report):
- never_registered: content file on disk, ZERO registration events naming it
  under any accepted spelling. Invisible to the log; a refold can never see
  it because a fold cannot invent events.
- registered_missing: the log registered the file (an accepted inbox
  spelling) but it is not on disk. The dangling-sha class; INDEX.json still
  lists it as active until an invalidate heals it.
- registered_never_consumed: registered and on disk, but ZERO consume
  events. The write-only class. Shrinks only when tools/inbox_consume.py
  records real reads.

Join spelling law (why the join is not just the fold's normalization):
mag.surface_rebuild._norm is reused as the base (board/inbox, app/inbox,
inbox/ and host-absolute stripping, B2-149/B2-157), then the census adds two
join aliases the fold deliberately does NOT apply, each counted in meta so
nothing is silently reinterpreted:
- "watch/inbox/..." prefixed registrations (328 at the 2026-09-29 census, the
  B2-02 writer spelling) are JOINED to their inbox file: the log did see the
  file, so counting it never_registered would understate the log's coverage;
  the fold itself drops these events (OUTSIDE_RE), so meta counts them as
  fold_blind_watch_prefix for the blindness ledger.
- registrations naming files OUTSIDE the surface (drive-letter absolutes,
  bare board/ container-root paths, repo files like tools/ or memory/) are
  bucketed as registered_outside_surface, NOT as registered_missing: the fold
  drops them as outside and they make no claim about inbox bytes. Detection
  is existential (the file exists at repo root) or syntactic (drive letter,
  leading slash, bare board/), never a hand-maintained root list.
Double slashes are collapsed (the fullsend_s2// family, 6 paths at census).

Read-only analysis: touches no ledger, appends nothing. The only write is
its own output artifact ORPHAN_CENSUS.json (skipped by later censuses the
way the fold's control files are).

Census-denominator law (B2-216) applies: every count below is one snapshot
of one tree at one moment; the log grows while you read this.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "watch" / "inbox"
EVENTS = INBOX / "index_events.jsonl"
DEFAULT_OUT = INBOX / "ORPHAN_CENSUS.json"

REGISTRATION_OPS = frozenset({"register", "autoseal", "filed"})
CONSUMPTION_OPS = frozenset({"consume"})

# Fold control plane + this tool's own output: not inbox content, never
# counted as orphans (mirrors mag.surface_rebuild CENSUS_SKIP_FILES).
CENSUS_SKIP_FILES = frozenset(
    {"index.json", "index.md", "shared_surface_contract.json",
     "index_events.jsonl", "orphan_census.json"}
)

_DRIVE_RE = re.compile(r"^[a-z]:/")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mag.surface_rebuild import _norm  # noqa: E402  (canonical fold normalizer)


def join_norm(raw: str, inbox: Path) -> str:
    """Fold normalization plus the census join aliases (see module docstring)."""
    p = _norm(raw, inbox)
    while "//" in p:
        p = p.replace("//", "/")
    low = p.lower()
    if low.startswith("watch/inbox/"):  # B2-02 spelling: joined, fold-blind
        p = p[len("watch/inbox/"):]
    return p


def disk_walk(inbox: Path) -> tuple[set[str], set[str]]:
    """Return (content, all) lowercase inbox-relative posix path sets.

    `all` includes the fold control files (existence checks for consume
    telemetry); `content` excludes them and is the denominator for the three
    headline classes.
    """
    everything: set[str] = set()
    for p in inbox.rglob("*"):
        if p.is_file():
            everything.add(p.relative_to(inbox).as_posix().lower())
    content = {p for p in everything if p not in CENSUS_SKIP_FILES}
    return content, everything


def scan_events(events_log: Path, inbox: Path) -> dict:
    """One tolerant pass over the log. Returns sets + meta, all lowercase."""
    registered: set[str] = set()
    consumed: set[str] = set()
    outside: set[str] = set()
    fold_blind_watch_prefix: set[str] = set()
    malformed = 0
    parsed = 0
    ops: Counter = Counter()
    if events_log.is_file():
        with events_log.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except Exception:
                    malformed += 1  # tolerant reader, same as the fold; no erase
                    continue
                if not isinstance(ev, dict):
                    malformed += 1
                    continue
                parsed += 1
                ops[ev.get("op")] += 1
                target = ev.get("file") or ev.get("path")
                if not target:
                    continue
                rel = join_norm(str(target), inbox).lower()
                if not rel:
                    continue
                if ev.get("op") in CONSUMPTION_OPS:
                    consumed.add(rel)
                if ev.get("op") not in REGISTRATION_OPS:
                    continue
                outside_claim = (
                    _DRIVE_RE.match(rel) is not None
                    or rel.startswith("/")
                    or rel.split("/", 1)[0] == "board"
                )
                if outside_claim:
                    outside.add(rel)
                else:
                    registered.add(rel)
                    if str(target).replace("\\", "/").lower().lstrip("/").startswith("watch/inbox/"):
                        fold_blind_watch_prefix.add(rel)
    return {
        "registered": registered,
        "consumed": consumed,
        "outside": outside,
        "fold_blind_watch_prefix": fold_blind_watch_prefix,
        "meta": {
            "events_parsed": parsed,
            "malformed_lines": malformed,
            "ops": dict(ops),
        },
    }


def classify(inbox: Path, events_log: Path) -> dict:
    """Build the full census dict. Pure read; writes nothing."""
    content, everything = disk_walk(inbox)
    scan = scan_events(events_log, inbox)
    registered, consumed, outside = (
        scan["registered"], scan["consumed"], scan["outside"]
    )
    # outside-surface registrations whose file exists at repo root (tools/,
    # memory/, docs/ ...): the log's claim is true but not about this surface.
    # Syntactic outside (drive letter, /abs, bare board/) plus inbox-shaped
    # registrations whose bytes actually live at repo root: both counted in
    # registered_outside_surface so every registered path lands somewhere
    # (present / missing / outside), nothing silently dropped.
    outside_all = outside | {p for p in registered - everything
                             if (ROOT / p).is_file()}
    outside_confirmed = {p for p in outside_all if (ROOT / p).is_file()}
    # registered claims with no inbox bytes anywhere: the true dangling class
    registered_missing = sorted(registered - everything - outside_all)
    registered_present = registered & everything
    # inbox-scope registrations: what the three headline classes divide up
    registered_scope = registered - outside_all
    consumed_present = sorted(p for p in consumed if p in everything)
    never_registered = sorted(content - registered)
    registered_never_consumed = sorted(registered_present - consumed)
    return {
        "schema": "orphan_census.v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),
        "inbox": inbox.resolve().relative_to(ROOT).as_posix()
        if inbox.resolve().is_relative_to(ROOT) else str(inbox),
        "registration_ops": sorted(REGISTRATION_OPS),
        "consumption_ops": sorted(CONSUMPTION_OPS),
        "disk_files": len(content),
        "registered_unique": len(registered_scope),
        "counts": {
            "never_registered": len(never_registered),
            "registered_missing": len(registered_missing),
            "registered_never_consumed": len(registered_never_consumed),
            "consumed": len(consumed_present),
        },
        "never_registered": never_registered,
        "registered_missing": registered_missing,
        "registered_never_consumed": registered_never_consumed,
        "consumed": consumed_present,
        "worst_offenders": {
            "never_registered_by_dir": _by_dir(never_registered),
            "registered_missing_by_dir": _by_dir(registered_missing),
            "registered_never_consumed_by_dir": _by_dir(registered_never_consumed),
        },
        "meta": {
            **scan["meta"],
            "registered_outside_surface": len(outside_all),
            "outside_confirmed_on_repo": len(outside_confirmed),
            "fold_blind_watch_prefix": len(scan["fold_blind_watch_prefix"]),
            "outside_examples": sorted(outside)[:10],
            "note": "counts are one snapshot at generated_at (B2-216); "
                    "consumed includes control files, the three headline "
                    "classes cover content files only",
        },
    }


def _by_dir(paths: list[str], top: int = 15) -> list[list]:
    """Rank paths by their top-level directory (root files rank as TOP)."""
    counts: Counter = Counter()
    for p in paths:
        seg = p.split("/", 1)[0] if "/" in p else "TOP"
        counts[seg] += 1
    return [[seg, n] for seg, n in counts.most_common(top)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Census watch/inbox vs the event log.")
    ap.add_argument("--inbox", default=str(INBOX))
    ap.add_argument("--events", default=str(EVENTS))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--stdout", action="store_true", help="print JSON, write nothing")
    args = ap.parse_args(argv)
    census = classify(Path(args.inbox), Path(args.events))
    if args.stdout:
        print(json.dumps(census, ensure_ascii=False, indent=2))
    else:
        out = Path(args.out)
        out.write_text(json.dumps(census, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
        try:
            from tools.md_record_seal import autoseal_file
            autoseal_file(out)
        except Exception:
            pass
        c = census["counts"]
        m = census["meta"]
        print(
            f"ORPHAN_CENSUS written to {out}\n"
            f"  disk content files:        {census['disk_files']}\n"
            f"  registered unique:         {census['registered_unique']}\n"
            f"  never_registered:          {c['never_registered']}\n"
            f"  registered_missing:        {c['registered_missing']}\n"
            f"  registered_never_consumed: {c['registered_never_consumed']}\n"
            f"  consumed:                  {c['consumed']}\n"
            f"  meta: outside_surface={m['registered_outside_surface']} "
            f"fold_blind_watch_prefix={m['fold_blind_watch_prefix']} "
            f"malformed_lines={m['malformed_lines']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
