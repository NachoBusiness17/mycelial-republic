"""Tide dashboard surface — expose the latest tide card + tide file like x_radar (FW-17).

Until 2026-09-28 the tide's nightly output was buried in state/fuel/tide/ and
memory/corpus/tide_cards/ with no dashboard surface, while the X radar got
dashboard/static/x_radar.json. This builder gives the tide the same treatment:

  dashboard/static/tide/tide.json         metadata block (dates, strike-clock verdict,
                                          gemma leg status) — the x_radar.json analogue
  dashboard/static/tide/latest.md         copy of the newest state/fuel/tide/tide_*.md
  dashboard/static/tide/latest_card.md    copy of the newest tide card
  dashboard/static/tide.html              self-contained viewer (card embedded, works
                                          from file:// like deck.html)

Usage:
    .venv\\Scripts\\python.exe scripts\\tide_dashboard.py
"""

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from tide_strike_clock import count_strikes  # noqa: E402

TIDE_DIR = ROOT / "state" / "fuel" / "tide"
CARD_DIR = ROOT / "memory" / "corpus" / "tide_cards"
OUT_DIR = ROOT / "dashboard" / "static" / "tide"
OUT_HTML = ROOT / "dashboard" / "static" / "tide.html"


def gemma_status(card_text: str) -> str:
    if re.search(r"^GEMMA: UNAVAILABLE\b", card_text, re.M):
        return "unavailable"
    m = re.search(r"^GEMMA:?\s*$\n?(.+?)(?=\n## |\n# |\Z)", card_text, re.S | re.M)
    if not m:
        m2 = re.search(r"^GEMMA:\s*(.+)$", card_text, re.M)
        if m2 and "EMPTY" not in m2.group(1):
            return m2.group(1).strip()[:80]
        return "empty/absent"
    body = m.group(1).strip()
    return f"ok ({len(body)} chars)" if body else "empty"


def html_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_html(meta: dict, tide_md: str, card_md: str) -> str:
    card_html = html_escape(card_md)
    tide_html = html_escape(tide_md)
    verdict_color = "#ff6b6b" if meta["strike_clock"]["void_condition_met"] else (
        "#ffb347" if meta["strike_clock"]["warn"] else "#8dff7a")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>TIDE — nightly compaction</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ background:#0b0e14; color:#d8dee9; font:14px/1.55 ui-monospace,Consolas,monospace; margin:0; padding:24px; }}
  h1 {{ color:#6fd6ff; font-size:18px; margin:0 0 4px; }}
  h2 {{ color:#6fd6ff; font-size:14px; border-bottom:1px solid #232a36; padding-bottom:4px; margin-top:28px; }}
  .sub {{ color:#7a8699; font-size:12px; }}
  .chips {{ margin:12px 0; }}
  .chip {{ display:inline-block; border:1px solid #2c3547; border-radius:12px; padding:2px 10px; margin:2px 6px 2px 0; font-size:12px; }}
  .strike {{ color:{verdict_color}; border-color:{verdict_color}; }}
  pre {{ background:#10141d; border:1px solid #232a36; border-radius:8px; padding:14px; white-space:pre-wrap; word-wrap:break-word; }}
  a {{ color:#6fd6ff; }}
</style></head><body>
<h1>TIDE <span class="sub">// nightly scattershot compaction — automation-b0ebbbb9, daily 06:15</span></h1>
<div class="chips">
  <span class="chip">tide: {html_escape(meta["tide_date"])}</span>
  <span class="chip">card: {html_escape(meta["card_date"])}</span>
  <span class="chip strike">amendment strikes: {meta["strike_clock"]["strikes"]} — {html_escape("VOID" if meta["strike_clock"]["void_condition_met"] else ("WARN" if meta["strike_clock"]["warn"] else "ok"))}</span>
  <span class="chip">gemma leg: {html_escape(meta["gemma_status"])}</span>
</div>
<p class="sub">built {html_escape(meta["built"])} · sources: state/fuel/tide/, memory/corpus/tide_cards/ · clock: scripts/tide_strike_clock.py · gemma leg: scripts/tide_gemma.py · raw: <a href="tide/tide.json">tide.json</a></p>
<h2>LATEST TIDE CARD</h2>
<pre>{card_html}</pre>
<h2>FULL TIDE FILE</h2>
<pre>{tide_html}</pre>
</body></html>
"""


def main() -> int:
    tides = sorted(TIDE_DIR.glob("tide_*.md"))
    cards = sorted(CARD_DIR.glob("card_*.md"))
    if not tides or not cards:
        print(json.dumps({"status": "no_tide_files", "tides": len(tides), "cards": len(cards)}))
        return 2

    tide_path, card_path = tides[-1], cards[-1]
    tide_md = tide_path.read_text(encoding="utf-8")
    card_md = card_path.read_text(encoding="utf-8")
    clock = count_strikes(TIDE_DIR, ROOT / "state" / "fuel" / "amendments.jsonl")

    meta = {
        "tide_date": tide_path.stem.replace("tide_", ""),
        "card_date": card_path.stem.replace("card_", ""),
        "gemma_status": gemma_status(card_md),
        "strike_clock": clock,
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "tide.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    shutil.copyfile(tide_path, OUT_DIR / "latest.md")
    shutil.copyfile(card_path, OUT_DIR / "latest_card.md")
    OUT_HTML.write_text(build_html(meta, tide_md, card_md), encoding="utf-8")

    print(json.dumps({"status": "ok", "tide": str(tide_path), "card": str(card_path),
                      "html": str(OUT_HTML), "gemma_status": meta["gemma_status"],
                      "strikes": clock["strikes"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
