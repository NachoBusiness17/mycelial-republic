"""gaming_corpus_pass — brief every orphaned game/tool page and every mag game engine
file, categorize, and file the pass report. Operator GO 2026-09-23 night ("do a new
pass on our gaming corpus and knock out all remaining orphans"). SSRF law n/a (local
reads + lane calls only).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from models.env_load import load_dotenv
load_dotenv()
from mag import lite_guard  # noqa: E402

OUT_MD = ROOT / "watch" / "inbox" / "GAMING_CORPUS_PASS_20260923.md"
OUT_JSONL = ROOT / "state" / "fuel" / "gaming_corpus_briefs.jsonl"
STATIC = ROOT / "dashboard" / "static"
MAG = ROOT / "mag"

LANE_DEFS = [
    ("deepseek-chat", "https://api.deepseek.com/chat/completions", "deepseek-chat", "DEEPSEEK_API_KEY"),
    ("openrouter-a1", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto", "OPENROUTER_API_KEY"),
    ("nvidia-glm53", "https://integrate.api.nvidia.com/v1/chat/completions", "z-ai/glm-5.3-flash", "NVIDIABuild"),
    ("openrouter-a2", "https://openrouter.ai/api/v1/chat/completions", "openrouter/auto", "OPENROUTER_API_KEY_2"),
]
LANES = []
for n, u, m, k in LANE_DEFS:
    key = (os.environ.get(k, "") or "").strip()
    if key:
        LANES.append({"name": n, "url": u, "model": m, "key": key})
lane_idx = [0]


def next_lane() -> dict:
    ln = LANES[lane_idx[0] % len(LANES)]
    lane_idx[0] += 1
    return ln


def brief(path: Path, kind: str) -> dict:
    lane = next_lane()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:3500]
    except Exception as e:
        return {"path": str(path), "kind": kind, "brief": "[unreadable: " + type(e).__name__ + "]"}
    prompt = ("This is a page or module from an AI-game estate. Output ONE line: "
              "what it is, max 20 words, plain English. If it is a playable game page say GAME: first. "
              "If it is an operator tool say TOOL: first. Otherwise one line.\n\n" + text)
    body = json.dumps({"model": lane["model"],
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 120, "temperature": 0}).encode()
    req = urllib.request.Request(lane["url"], data=body, headers={
        "Authorization": "Bearer " + lane["key"], "Content-Type": "application/json"})
    try:
        with lite_guard._OPENER.open(req, timeout=90) as r:
            d = json.loads(r.read().decode())
        msg = (d.get("choices") or [{}])[0].get("message", {}) or {}
        content = (msg.get("content") or "").strip()
        if not content:
            payload = json.loads(json.dumps({"model": lane["model"],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300, "temperature": 0, "thinking": {"type": "disabled"}}))
            req2 = urllib.request.Request(lane["url"], data=json.dumps(payload).encode(), headers={
                "Authorization": "Bearer " + lane["key"], "Content-Type": "application/json"})
            with lite_guard._OPENER.open(req2, timeout=120) as r2:
                d2 = json.loads(r2.read().decode())
            m2 = (d2.get("choices") or [{}])[0].get("message", {}) or {}
            content = (m2.get("content") or "").strip() or "[empty]"
    except Exception as e:
        content = "[fail:" + type(e).__name__ + ": " + str(e)[:60] + "]"
    return {"path": str(path).replace(str(ROOT) + "\\", ""), "kind": kind, "brief": content}


def main() -> dict:
    targets = []
    done_paths = set()
    out_prev = ROOT / "state" / "fuel" / "gaming_corpus_briefs.jsonl"
    if out_prev.is_file():
        for line in out_prev.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                done_paths.add(json.loads(line).get("path", ""))
            except Exception:
                pass
    # orphan HTML pages (not linked from index/work)
    static = ROOT / "dashboard" / "static"
    index_text = ""
    for idx in ("index.html", "work.html"):
        p = static / idx
        if p.is_file():
            index_text += p.read_text(encoding="utf-8", errors="replace")
    linked = set(re.findall(r'href="([^"]+\.html)"', index_text))
    linked |= set(re.findall(r'"([^"]+\.html)"', index_text))
    for p in sorted(static.rglob("*.html")):
        rel = str(p.relative_to(static))
        if rel in ("index.html", "work.html") or "frontdoor" in rel:
            continue
        if str(p) in done_paths:
            continue
        if rel not in linked:
            targets.append((p, "orphan-page"))
    # mag game engine modules
    for p in sorted(MAG.glob("game_*.py")) + sorted(MAG.glob("campaign*.py")) + [MAG / "riddler_campaign.py"]:
        if p.is_file():
            targets.append((p, "engine-module"))
    # game_estate records
    for p in sorted((ROOT / "corpus" / "game_estate").glob("*.md")):
        targets.append((p, "estate-record"))

    print(f"gaming corpus pass: {len(targets)} targets", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(lambda t: brief(t[0], t[1]), targets):
            results.append(r)
            print(json.dumps({"path": r["path"], "brief": r["brief"][:90]}), flush=True)

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("a", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    games = [r for r in results if r["brief"].startswith("GAME:")]
    tools = [r for r in results if r["brief"].startswith("TOOL:")]
    other = [r for r in results if not r["brief"].startswith(("GAME:", "TOOL:"))]
    md = [
        "# GAMING CORPUS PASS — 2026-09-23 night",
        "",
        f"targets: {len(results)} ({len(games)} games, {len(tools)} tools, {len(other)} other/notes)",
        "",
        "## Games",
        "",
    ]
    for g in games:
        md.append("- " + g["path"] + " — " + g["brief"])
    md += ["", "## Tools", ""]
    for t in tools:
        md.append("- " + t["path"] + " — " + t["brief"])
    md += ["", "## Other", ""]
    for o in other:
        md.append("- " + o["path"] + " — " + o["brief"])
    md += ["", "*Append-only. The linking pass (orphans → index) is the operator's next GO.*"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    return {"targets": len(results), "games": len(games), "tools": len(tools),
            "other": len(other), "file": str(OUT_MD)}


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
