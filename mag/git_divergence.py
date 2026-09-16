"""git_divergence -- the Steins;Git steal: a worldline divergence meter for this repo.

The operator's directive (2026-09-16): "Steins;Git needs a full blown steal and
mapping." The stolen mechanism (Amelie Royer's weekend git visualizer): every
branch carries a DIVERGENCE NUMBER -- how far it has drifted from main -- read
like a worldline meter. Here it is for the fleet estate, computed from git bytes,
not vibes.

Divergence score per branch:
    divergence = ahead + 2*behind + age_days
(ahead: commits only we hold; behind: commits only main holds -- behind counts
double because a drifting branch also silently misses what main learned;
age_days: days since the branch's last commit -- an unmaintained worldline).

Schema: git_divergence.v1 . deterministic . $0 . read-only (git calls only)

RUN:
  python -m mag.git_divergence            # worldline table, main first
  python -m mag.git_divergence --json     # deck-ready JSON (the meter feed)
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys

BASE = "master"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          check=True, encoding="utf-8", errors="replace").stdout


def _counts(branch: str) -> tuple[int, int]:
    out = _git("rev-list", "--left-right", "--count", f"{BASE}...{branch}")
    behind, ahead = (int(x) for x in out.split())
    return ahead, behind


def _age_days(branch: str) -> float:
    ts = _git("log", "-1", "--format=%ct", branch).strip()
    if not ts:
        return 999.0
    delta = dt.datetime.now().timestamp() - int(ts)
    return round(delta / 86400, 1)


def measure() -> dict:
    cur = _git("branch", "--show-current").strip() or "(detached)"
    branches = [b.strip().lstrip("*+ ").replace("remotes/origin/", "")
                for b in _git("branch").splitlines() if b.strip()]
    base_line = _git("rev-list", "--count", BASE).strip()
    rows = []
    for b in sorted(set(branches)):
        if b == BASE:
            continue
        try:
            ahead, behind = _counts(b)
            rows.append({"branch": b, "ahead": ahead, "behind": behind,
                         "age_days": _age_days(b),
                         "divergence": ahead + 2 * behind + _age_days(b)})
        except subprocess.CalledProcessError:
            rows.append({"branch": b, "ahead": -1, "behind": -1,
                         "age_days": -1, "divergence": -1})
    rows.sort(key=lambda r: r["divergence"], reverse=True)
    return {"ok": True, "schema": "git_divergence.v1", "base": BASE,
            "base_commits": int(base_line), "current": cur,
            "branches": len(rows), "worldlines": rows}


def render(m: dict) -> str:
    lines = [f"WORLDLINE METER — base {m['base']} ({m['base_commits']} commits) · "
             f"current {m['current']} · {m['branches']} worldlines", ""]
    for r in m["worldlines"]:
        if r["divergence"] < 0:
            lines.append(f"  {r['branch'][:44]:44s}  ? (unresolvable)")
            continue
        bar = "#" * min(60, int(r["divergence"]))
        lines.append(f"  {r['branch'][:44]:44s}  div {r['divergence']:6.1f}  "
                     f"+{r['ahead']}/-{r['behind']}  age {r['age_days']}d  {bar}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    m = measure()
    if "--json" in argv:
        print(json.dumps(m, ensure_ascii=False, indent=2))
    else:
        print(render(m))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
