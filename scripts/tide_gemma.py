"""Tide gemma leg — the deterministic morning-brief call behind tide-card step 5.

FW-16 fix (memory/plans/fifty_wide_20260917.md): the tide template told the tide seat to
"send the card to gemma:2b" ad hoc, so every night re-invented the invocation. Observed on
the 2026-09-17 first fire (memory/corpus/tide_cards/card_2026-09-17.md): "GEMMA: EMPTY"
first pass, then a loose second-pass summary. Reproduced 2026-09-28 against the live
ollama (receipt watch/inbox/burn_reset_20260927/queue/Q-022.md):
  - gemma4:latest, naive /api/chat shape (no think flag): content='' done_reason=length —
    thinking tokens consume the whole num_predict budget -> the EMPTY class;
  - gemma:2b with the literal template shape (instruction + card concatenated): reproduces
    the card's flabby summary nearly verbatim, and fact-bounds poorly even when prompted.

This script is the one sanctioned caller: chat shape, think:false forced, card delimited,
facts bounded to the card, non-empty validation with one retry at a higher budget, and a
GEMMA: UNAVAILABLE marker distinct from a true EMPTY. Idempotent: re-running replaces the
card's existing GEMMA section instead of stacking sections.

Usage:
    .venv\\Scripts\\python.exe scripts\\tide_gemma.py                 # latest card, gemma4
    .venv\\Scripts\\python.exe scripts\\tide_gemma.py --card PATH    # explicit card
    .venv\\Scripts\\python.exe scripts\\tide_gemma.py --model gemma:2b --no-apply

Exit codes: 0 brief written (or ollama down -> UNAVAILABLE marker, per template's
"skip silently" law); 1 both passes empty (loud, never silent); 2 no card found.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "memory" / "corpus" / "tide_cards"
GEMMA_SECTION = re.compile(r"^GEMMA:.*?(?=\n## |\n# |\Z)", re.S | re.M)

SYSTEM_PROMPT = (
    "You compress the fleet night into the operator's 3-sentence morning brief. "
    "Use ONLY facts stated in the CARD. No preamble, no disclaimers, no new claims. "
    "Output exactly three numbered sentences covering: what shipped, what broke/fixed, "
    "what is owed."
)


def latest_card() -> Path | None:
    cards = sorted(CARD_DIR.glob("card_*.md"))
    return cards[-1] if cards else None


def ollama_up(base_url: str, timeout: int = 8) -> bool:
    try:
        with urllib.request.urlopen(base_url + "/api/tags", timeout=timeout):
            return True
    except (urllib.error.URLError, OSError):
        return False


def chat(base_url: str, model: str, card_text: str, num_predict: int, timeout: int = 300):
    """One /api/chat call. Returns the message dict (content + thinking kept separate)."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "=== CARD ===\n" + card_text + "\n=== END CARD ===\nMorning brief:",
            },
        ],
        "stream": False,
        # think:false is the load-bearing flag: a thinking worker (gemma4) burns the whole
        # num_predict budget on reasoning tokens and returns content='' otherwise.
        "think": False,
        "options": {"num_predict": num_predict, "temperature": 0.3},
    }
    req = urllib.request.Request(
        base_url + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def tidy(text: str) -> str:
    text = text.strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def render_gemma_section(reply: str) -> str:
    return "GEMMA:\n" + reply + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--card", type=Path, default=None, help="card path (default: latest)")
    ap.add_argument("--model", default="gemma4:latest", help="ollama model (default gemma4:latest, the harness short worker)")
    ap.add_argument("--base-url", default="http://localhost:11434")
    ap.add_argument("--num-predict", type=int, default=400)
    ap.add_argument("--retry-num-predict", type=int, default=800)
    ap.add_argument("--no-apply", action="store_true", help="print the brief, do not rewrite the card")
    args = ap.parse_args()

    card_path = args.card or latest_card()
    if card_path is None or not card_path.exists():
        print(json.dumps({"status": "no_card", "card": str(card_path)}))
        return 2

    card_text = card_path.read_text(encoding="utf-8")

    if not ollama_up(args.base_url):
        # Template law: "If ollama is down, skip silently." Keep the card honest about why:
        # an explicit UNAVAILABLE marker, not a bare EMPTY.
        marker = f"GEMMA: UNAVAILABLE (ollama down at {datetime.now(timezone.utc).isoformat(timespec='seconds')})"
        if not args.no_apply:
            new_text = GEMMA_SECTION.sub("", card_text).rstrip("\n") + "\n\n" + marker + "\n"
            card_path.write_text(new_text, encoding="utf-8")
        print(json.dumps({"status": "unavailable", "card": str(card_path), "model": args.model}))
        return 0

    t0 = time.time()
    reply, retries = "", 0
    try:
        first = chat(args.base_url, args.model, card_text, args.num_predict)
        reply = tidy((first.get("message") or {}).get("content", ""))
        if not reply:
            retries = 1
            second = chat(args.base_url, args.model, card_text, args.retry_num_predict)
            reply = tidy((second.get("message") or {}).get("content", ""))
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "card": str(card_path), "model": args.model,
                          "error": f"{type(exc).__name__}: {exc}"}))
        return 1

    if not reply:
        print(json.dumps({"status": "empty", "card": str(card_path), "model": args.model,
                          "seconds": round(time.time() - t0, 1), "retries": retries,
                          "note": "both passes empty - the brief leg is broken, not skipped"}))
        return 1

    if not args.no_apply:
        new_text = GEMMA_SECTION.sub("", card_text).rstrip("\n") + "\n\n" + render_gemma_section(reply)
        card_path.write_text(new_text, encoding="utf-8")

    print(json.dumps({"status": "ok", "card": str(card_path), "model": args.model,
                      "chars": len(reply), "seconds": round(time.time() - t0, 1),
                      "retries": retries, "applied": not args.no_apply}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
