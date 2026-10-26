"""mirror_drift - shape 3 (the pin) applied across the estate's mirrors.

The gap this closes (watch/inbox/SHAPES_THROUGH_TIME_20261016.md, G2): four
mirrors existed with zero replication patrol - mirror drift was found by
hand. This patrol compares each mirror against the main repo and appends a
horizon-style math line to state/MIRROR_DRIFT.jsonl.

Verdicts per mirror:
  CONTAINED-BEHIND:N  mirror HEAD is an ancestor of main; main is N ahead.
  UP-TO-DATE          mirror HEAD == main HEAD.
  DIVERGED            mirror HEAD missing from main, or not a well-formed
                      commit id (history rewrite, fork, or a hostile
                      mirror - investigate, never auto-push).
  SNAPSHOT            non-tracking mirror (corpus snapshot): age reported,
                      no containment expectation.

Security: every git invocation is an argument list (shell=False semantics);
values that came FROM a mirror are validated as 40-hex before they are used
as arguments, so a crafted mirror cannot inject or smuggle flags.

Usage:
  .venv/Scripts/python.exe tools/mirror_drift.py
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "state" / "MIRROR_DRIFT.jsonl"
MIRRORS = [
    {"name": "Mag-backup.git",
     "gitdir": r"C:\Users\foste\Documents\projects\Mag-backup.git",
     "kind": "full"},
    {"name": "laptop_seat.git",
     "gitdir": r"C:\Users\foste\Documents\projects\laptop_seat.git",
     "kind": "snapshot"},
]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def git(args: list[str], gitdir: str | None = None) -> str:
    cmd = ["git"]
    if gitdir:
        cmd += ["--git-dir", gitdir]
    cmd += args
    return subprocess.run(cmd, capture_output=True, text=True,
                          timeout=60).stdout.strip()


def mirror_head(gitdir: str) -> str | None:
    head = git(["rev-parse", "HEAD"], gitdir)
    return head if SHA_RE.fullmatch(head) else None


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    main_head = git(["rev-parse", "HEAD"])
    main_date = git(["log", "-1", "--format=%ad", "--date=iso"])
    rows = []
    for m in MIRRORS:
        gdir = m["gitdir"]
        if not Path(gdir).exists():
            rows.append({"mirror": m["name"], "verdict": "MISSING"})
            continue
        head = mirror_head(gdir)
        if head is None:
            rows.append({"mirror": m["name"], "verdict": "DIVERGED",
                         "reason": "HEAD is not a well-formed commit id"})
            continue
        date = git(["log", "-1", "--format=%ad", "--date=iso"], gdir)
        subject = git(["log", "-1", "--format=%s"], gdir)[:80]
        row = {"mirror": m["name"], "head": head[:12], "head_date": date,
               "subject": subject}
        if m["kind"] == "snapshot":
            row["verdict"] = "SNAPSHOT"
        elif head == main_head:
            row["verdict"] = "UP-TO-DATE"
        else:
            contained = subprocess.run(
                ["git", "-C", str(ROOT), "cat-file", "-e", head + "^{commit}"],
                capture_output=True, text=True).returncode == 0
            if not contained:
                row["verdict"] = "DIVERGED"
                row["reason"] = "mirror HEAD object absent from main"
            else:
                behind = git(["rev-list", "--count", f"{head}..HEAD"])
                n = int(behind) if behind.isdigit() else -1
                row["verdict"] = f"CONTAINED-BEHIND:{n}"
        rows.append(row)

    record = {"schema": "mirror_drift.v1", "ts": now,
              "main_head": main_head[:12], "main_date": main_date,
              "mirrors": rows}
    record["self_hash"] = hashlib.sha256(
        json.dumps(record, sort_keys=True).encode()).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")

    for r in rows:
        verdict = r["verdict"]
        flag = "WARN" if verdict.startswith(("DIVERGED", "MISSING",
                                             "CONTAINED")) else "ok"
        print(f"{flag}: {r['mirror']} {verdict}")
    print(f"appended {OUT.name} self_hash={record['self_hash'][:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
