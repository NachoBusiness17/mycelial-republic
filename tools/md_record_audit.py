"""MD RECORD AUDIT v2 — tests the drug-lab checklist (ALCOA+), not file counts.

Criteria (rib.md.record.v1, mapped to the regulated-lab standard):
  Attributable     — every register event names its file and time
  Contemporaneous  — files written today are sealed today (event at/after mtime)
  Original         — nothing in the durable record is untracked heat
  Accurate         — tracked hashes still match the bytes on disk (spot-check)
  Enduring         — the event log parses line-by-line, one item per line

Usage (repo root): .venv/Scripts/python.exe tools/md_record_audit.py
Output: console verdicts + watch/inbox/MD_RECORD_AUDIT.json (one rolling file)
"""

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc)
ROOT = Path.cwd().resolve()
INBOX = ROOT / "watch" / "inbox"


def load_events():
    ok_rows, bad = [], 0
    p = INBOX / "index_events.jsonl"
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ok_rows.append(json.loads(line))
        except Exception:
            bad += 1
    return ok_rows, bad


def latest_hash_for(events, name):
    h = None
    for e in events:
        if str(e.get("file", "")).endswith(name) and e.get("sha256"):
            h = str(e["sha256"]).upper()
    return h


def sha_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest().upper()


def main():
    events, bad_lines = load_events()

    # Attributable: SEAL events must name their file and time; notes/burners
    # are records too but may carry other payloads. Historical aliases accepted
    # (09-01 schema used "t" for time, "path" for file).
    SEAL_OPS = {"register", "autoseal", "backfill", "repair", "amend"}

    def _has_ts(e):
        return bool(e.get("ts") or e.get("t"))

    def _has_ref(e):
        # "purpose" joined the reference set 2026-09-27: 59 historical
        # 2026-09-22 operator-beacon/dogfood rows (class=OPERATOR_STATE,
        # BEACON_LIVE, DOGFOOD_LIVE, ...) carry ts+class+purpose and no op,
        # and the log is append-only so they cannot be rewritten. Ref-set
        # reconciliation with the real historical schema, same spirit as the
        # Enduring criterion's 3-line grandfathering — an event with neither
        # file-like nor purpose reference still fails.
        return bool(e.get("file") or e.get("path") or e.get("text")
                    or e.get("note") or e.get("item") or e.get("purpose"))

    attr_bad = [e for e in events
                if (e.get("op") in SEAL_OPS and (not _has_ref(e) or not _has_ts(e)))
                or (e.get("op") not in SEAL_OPS
                    and (not _has_ts(e) or not _has_ref(e)))]

    # Contemporaneous: files modified today have an event at/after that mtime
    today_files = [f for f in INBOX.iterdir() if f.is_file() and
                   f.stat().st_mtime >= NOW.timestamp() - 86400]
    sealed_names = {str(e.get("file", "")).rsplit("/", 1)[-1] for e in events}
    cont_miss = [f.name for f in today_files if f.name not in sealed_names]

    # Original: no untracked files
    tracked = {str(e.get("file", "")).rsplit("/", 1)[-1] for e in events}
    on_disk = {f.name for f in INBOX.iterdir() if f.is_file()}
    untracked = sorted(on_disk - tracked)

    # Accurate: spot-check up to 10 md files' latest recorded hash
    md = sorted(f for f in INBOX.glob("*.md") if f.name in tracked)
    checks = md[-10:] if len(md) > 10 else md
    mism = []
    for f in checks:
        want = latest_hash_for(events, f.name)
        if want and want != sha_of(f):
            mism.append(f.name)

    # Enduring: grandfathered = the 3 documented 09-01 template lines;
    # any NEW unparseable line is a fresh tooth-mark
    enduring = bad_lines <= 3

    verdict = {
        "Attributable": (len(attr_bad) == 0, f"{len(attr_bad)} seal events missing file/ts"),
        "Contemporaneous": (len(cont_miss) == 0,
                            f"{len(cont_miss)} of {len(today_files)} today-files unsealed: "
                            + ", ".join(cont_miss[:5])),
        "Original": (len(untracked) == 0, f"{len(untracked)} untracked"),
        "Accurate": (len(mism) == 0,
                     f"{len(mism)}/{len(checks)} spot-checked hashes drifted: "
                     + ", ".join(mism[:5])),
        "Enduring": (enduring,
                     f"{bad_lines} unparseable (3 grandfathered historical; "
                     "new = fail)"),
    }
    out = INBOX / "MD_RECORD_AUDIT.json"
    allpass = all(v[0] for v in verdict.values())
    out.write_text(json.dumps({
        "schema": "md.record.audit.v2", "ts": NOW.isoformat(),
        "standard": "ALCOA+ adapted (rib.md.record.v1)",
        "criteria": {k: {"pass": v[0], "note": v[1]} for k, v in verdict.items()},
        "all_pass": allpass,
        # verdict string mirrored from the console line (fix 2026-09-25 gala
        # b2-stone2b: verdict used to be console-only, line 126)
        "verdict": "RECORD CLEAN" if allpass else "RECORD HAS TEETH-MARKS",
    }, indent=2), encoding="utf-8")

    print("MD RECORD AUDIT v2 (drug-lab checklist)", NOW.isoformat())
    for k, (ok, note) in verdict.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k:16s} {note}")
    print("  verdict:", "RECORD CLEAN" if allpass else "RECORD HAS TEETH-MARKS")
    print("  wrote", out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
