#!/usr/bin/env python3
"""burn_gated -- does a self-audit gate beat a prohibition?

The 2026-10-24 grid: 6 of 10 lanes used Freud's vocabulary inside a Jung brief
that explicitly forbade it. The lesson was "a prohibition in a prompt is not a
gate". This runs the counter-test: same brief, then a second pass that must audit
its own draft for the forbidden lexicon and rewrite if it finds any.

Measured: clean rate vs the 4/10 baseline, and whether the gate introduces a new
failure (a rewrite that loses the mechanism, or an empty second pass).

    python tools/burn_gated.py --lanes deepseek-flash,zcode-1,... --workers 5
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from burn_lanes import LANES, RECEIPTS, http_lane  # noqa: E402

BRIEF = (
    "Write ONE parable of 90-130 words as a ractor would, in English only.\n"
    "Lens: JUNG. Required mechanism: a shadow figure or double that is given a seat, "
    "a persona/mask, or an archetype recurring across two unrelated cultures.\n"
    "End with a one-line 'mechanism:' sentence naming what makes it Jung."
)

BRIEF_FORBID = (
    "Write ONE parable of 90-130 words as a ractor would, in English only.\n"
    "Lens: JUNG. Required mechanism: a shadow figure or double that is given a seat, "
    "a persona/mask, or an archetype recurring across two unrelated cultures.\n"
    "FORBIDDEN: anything returning from a cellar, symptoms, repetition-compulsion, "
    "or a 'cured/repressed' ending - that is FREUD's mechanism, not Jung's.\n"
    "End with a one-line 'mechanism:' sentence naming what makes it Jung."
)

AUDIT = (
    "You are auditing your own draft against its brief. The draft is below.\n"
    "Check for these words or their stems: cellar, symptom, repress, "
    "repetition-compulsion, unconscious wish, neurosis.\n"
    "If any are present, REWRITE the parable so none appear, keeping the Jung "
    "mechanism (shadow/double given a seat, persona, or recurring archetype).\n"
    "If none are present, return the draft unchanged.\n"
    "Output ONLY the final parable followed by its 'mechanism:' line.\n\n--- DRAFT ---\n"
)

FORBIDDEN = ("cellar", "symptom", "repress", "repetition-compulsion",
             "unconscious wish", "neurosis")


def leaks(text: str) -> list[str]:
    low = (text or "").lower()
    return [w for w in FORBIDDEN if w in low]


def run_one(lane: dict, prohibition: bool = False, audit: bool = True) -> dict:
    draft = http_lane(lane, BRIEF_FORBID if prohibition else BRIEF, 3500)
    rec = {"lane": lane["id"], "task": "jung-gated", "provider": lane["provider"],
           "draft_ok": bool(draft.get("ok")), "draft_leaks": leaks(draft.get("text", "")),
           "draft_chars": draft.get("chars", 0)}
    if not draft.get("ok"):
        rec.update({"ok": False, "error": draft.get("error"), "text": ""})
        return rec
    if not audit:
        rec.update({"ok": True, "text": draft["text"], "chars": draft.get("chars", 0),
                    "final_leaks": rec["draft_leaks"], "cost_usd": draft.get("cost_usd") or 0,
                    "latency_s": draft.get("latency_s") or 0})
        return rec
    revised = http_lane(lane, AUDIT + draft["text"], 3500)
    final = revised.get("text") or ""
    rec.update({
        "ok": bool(final.strip()),
        "text": final,
        "chars": len(final),
        "final_leaks": leaks(final),
        "gate_fixed": bool(rec["draft_leaks"]) and not leaks(final),
        "gate_broke": not final.strip(),
        "latency_s": round(float(draft.get("latency_s") or 0) + float(revised.get("latency_s") or 0), 2),
        "cost_usd": round(float(draft.get("cost_usd") or 0) + float(revised.get("cost_usd") or 0), 5),
    })
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lanes", required=True)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--prohibition", action="store_true")
    ap.add_argument("--no-audit", action="store_true")
    args = ap.parse_args(argv)
    want = set(args.lanes.split(","))
    lanes = [l for l in LANES if l["id"] in want]
    if not lanes:
        print("no lanes matched")
        return 2
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPTS / f"burn_{stamp}_gated.jsonl"
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(run_one, lane, args.prohibition, not args.no_audit): lane for lane in lanes}
        for fut in as_completed(futs):
            rows.append(fut.result())
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    ok = sum(1 for r in rows if r["ok"])
    clean = sum(1 for r in rows if r["ok"] and not r.get("final_leaks"))
    fixed = sum(1 for r in rows if r.get("gate_fixed"))
    dirty_draft = sum(1 for r in rows if r.get("draft_leaks"))
    spent = round(sum(r.get("cost_usd") or 0 for r in rows), 4)
    print(f"receipt {path.name}  proh={args.prohibition} audit={not args.no_audit}")
    print(f"lanes {len(rows)} · drafts leaking {dirty_draft} · final clean {clean} · "
          f"fixed by gate {fixed} · empty after gate {sum(1 for r in rows if r.get('gate_broke'))} · ${spent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
