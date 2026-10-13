"""research_x_tabs — read the captured X-surface tabs and ground each through memlance.

Deterministic + $0, module functions only (no terminal spawns, no LLM). For each tab file in
memory/ghost/x_surface/nachoquixotic_prompts/ it:
  1. reads the file's real bytes,
  2. derives a search goal from the filename + first heading,
  3. runs mag.ghost_memlance.select(goal, k=k) to find the relevant VERIFIED memory states,
  4. prints a grounded readout per tab ([V] = verified, [U] = unverified).

Schema: x_tabs_memlance.v1
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(ROOT))

X_DIR = ROOT / "memory" / "ghost" / "x_surface" / "nachoquixotic_prompts"
EXT = {".md", ".txt", ".mkd"}
_TITLE_RE = re.compile(r"^#\s+(.+)$", re.M)

# filename -> research goal (defining theme of the tab). Fallback: derive from name/heading.
_THEME_MAP = {
    "team": "multi-agent team leader collaboration consensus frontier agents",
    "code-fast": "safety policy jailbreak resistance leak detection canary",
    "grok4.20": "multi-agent team leader collaboration consensus frontier agents",
    "grok4.1": "identity defense grounding honesty provenance truth-seeking",
    "grok4": "agent as os tool surface x search web search code execution machine",
    "grok3": "memory persistence cross session stateless distilled invariant",
}


def _heading(path: Path, text: str) -> str:
    m = _TITLE_RE.search(text)
    return m.group(1).strip()[:120] if m else path.stem


def _goal_for(path: Path, text: str) -> str:
    low = path.stem.lower()
    for key, goal in _THEME_MAP.items():
        if key in low:
            return goal
    return f"{_heading(path, text)} research grounding sovereign swarm"


def research_tabs(*, k: int = 5, refresh: bool = False, domain: str = "x-tabs") -> list[dict[str, Any]]:
    """Percolate every X tab (signal/noise split), then ground the SIGNAL through memlance.

    Refined (2026-08-11): only USEFUL data is brought in. Each tab is passed through
    mag.percolator.percolate — noise/theater is written to the noise file, repeated signal is
    compiled into invariants, novel signal is queued for exploration. Only the clean signal
    sentences are then grounded via ghost_memlance. Inaccessible tabs -> intake register.
    Deterministic + $0 (module functions only, no LLM).
    """
    from mag import ghost_memlance as gl, percolator as pc

    if refresh:
        gl.index(refresh=True)
    tabs: list[dict[str, Any]] = []
    for f in sorted(X_DIR.glob("*")):
        if f.is_dir() or f.suffix.lower() not in EXT:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            # cannot read -> intake register to look into later
            pc.intake_register(str(f), reason_blocked=f"read_error: {str(e)[:80]}",
                               why_useful=_goal_for(f, f.name), source="x-tabs", domain=domain)
            continue
        perc = pc.percolate(text, source=f.name, domain=domain)  # files noise; compiles invariants
        goal = _goal_for(f, text)
        r = gl.select(goal, k=k)
        tabs.append({
            "file": f.relative_to(ROOT).as_posix(),
            "heading": _heading(f, text),
            "n_chars": len(text),
            "verdict": perc.get("verdict"),
            "n_signal": perc.get("n_signal"),
            "n_stripped": perc.get("n_stripped"),
            "explore": perc.get("explore"),
            "n_indexed": r["n_indexed"],
            "selected": [{"path": s["path"], "kind": s["kind"], "title": s["title"],
                          "ts": s["ts"], "verified": s["verified"],
                          "reason": s["reason"], "excerpt": s["excerpt"]}
                         for s in r["selected"]],
        })
    return tabs


def render_markdown(tabs: list[dict[str, Any]]) -> str:
    """Render the grounded readout as markdown for the synthesis step."""
    lines = ["# X-Tabs → Memlance Grounded Readout", ""]
    for t in tabs:
        lines.append(f"## {t['heading']}")
        lines.append(f"`{t['file']}` · {t['n_chars']} chars · indexed {t['n_indexed']}")
        lines.append("")
        for s in t["selected"]:
            flag = "V" if s["verified"] else "U"
            lines.append(f"- [{flag}] `{s['path']}` — {s['title']} ({s['reason']})")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json
    ap = argparse.ArgumentParser(prog="x-tabs-memlance")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--markdown", action="store_true", help="render as markdown instead of JSON")
    ap.add_argument("--refresh", action="store_true", help="force memlance index refresh")
    a = ap.parse_args(argv)
    tabs = research_tabs(k=a.k, refresh=a.refresh)
    if a.markdown:
        print(render_markdown(tabs))
    else:
        print(json.dumps(tabs, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
