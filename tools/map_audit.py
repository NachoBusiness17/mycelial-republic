#!/usr/bin/env python3
"""map_audit -- do lenses catch a planted premise, and how many does it take?

What today taught: a single lens ratifies the map's premise and produces a confident
build order; ten lenses disagreed with each other and, in doing so, caught that the
map itself was false ("no consumer exists" / "1,521 open rows"). Lenses behaved like
an error-correcting code over the MAP.

So test that directly, with a planted error and a control:

  maps:  TRUE  - six premises that are true of the estate today
         FALSE - same, with one premise replaced by a falsehood (and the row count
                 inflated), so the map *looks* coherent

  ask:   list numbered premises you cannot verify from the map, and those you
         believe are FALSE
  score: detection  = the planted premise appears in `false` (or `unverifiable`)
         overreach  = true premises also called false (the cost of a panel)

Then build a coverage curve: detection vs number of independent lenses pooled,
bootstrapped over lens subsets, so one run answers "how many lenses is enough".
"""
from __future__ import annotations

import argparse
import json
import itertools
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from burn_lanes import LANES, http_lane  # noqa: E402
from lens_packet import LENSES  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "memory" / "runs" / "map_audit"

PREMISES_TRUE = {
    "P1": "explore.jsonl holds 3,501 rows in total.",
    "P2": "62.5% of the open rows carry a probe_* domain.",
    "P3": "Sixteen code files in tools/ and mag/ reference explore.jsonl.",
    "P4": "About 750 distinct live observations remain after dedupe.",
    "P5": "The decay ledger has classified 848 rows.",
    "P6": "The commit sweeper runs on a ten-minute cadence.",
}
PREMISES_FALSE = dict(PREMISES_TRUE)
PREMISES_FALSE["P3"] = "No code in the estate reads explore.jsonl."
PREMISES_FALSE["P1"] = "explore.jsonl holds 1,521 rows in total."
PLANTED = ["P3", "P1"]

ASK = (
    "The MAP above is a list of numbered premises. Do not act on them. Audit them:\n"
    "  unverifiable - premises the map alone cannot establish\n"
    "  false        - premises you believe are factually wrong\n"
    "Return ONLY JSON: {\"unverifiable\": [\"P?\", ...], \"false\": [\"P?\", ...], \"why\": \"<=30 words\"}"
)


def make_map(premises: dict) -> str:
    body = "\n".join(f"  {k}: {v}" for k, v in premises.items())
    return f"MAP — estate queue census, 2026-10-24\n\n{body}\n"


def cell(lane: dict, lens_id: str, premises: dict, variant: str) -> dict:
    prompt = f"{make_map(premises)}\nLENS: {LENSES[lens_id]}\n\nASK: {ASK}"
    res = http_lane(lane, prompt, 1200)
    rec = {"lane": lane["id"], "lens": lens_id, "variant": variant,
           "ok": bool(res.get("ok")), "cost_usd": res.get("cost_usd") or 0,
           "attempt": res.get("attempt") or 1, "chars": res.get("chars", 0)}
    if not res.get("ok"):
        rec["error"] = res.get("error")
        return rec
    t = (res.get("text") or "").strip()
    if "{" in t and "}" in t:
        t = t[t.index("{"): t.rindex("}") + 1]
    try:
        d = json.loads(t)
    except Exception:  # noqa: BLE001
        rec.update({"unverifiable": [], "false": [], "parse": "failed"})
        return rec
    rec["unverifiable"] = [str(x).upper() for x in (d.get("unverifiable") or [])]
    rec["false"] = [str(x).upper() for x in (d.get("false") or [])]
    rec["why"] = (d.get("why") or "")[:120]
    return rec


def coverage(rows: list[dict], planted: list[str], sizes=range(1, 11), draws: int = 400) -> dict:
    """Probability that a panel of k lenses flags the planted premise."""
    good = [r for r in rows if r.get("ok") and ("false" in r or "unverifiable" in r)]
    out = {}
    lenses = sorted({r["lens"] for r in good})
    for k in sizes:
        if k > len(lenses):
            break
        hits = 0
        for _ in range(draws):
            panel = random.sample(lenses, k)
            flagged = any(
                any(p in set(r.get("false", [])) | set(r.get("unverifiable", []))
                    for p in planted)
                for r in good if r["lens"] in panel)
            hits += flagged
        out[k] = round(hits / draws, 3)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lanes", default="deepseek-flash,deepseek-v4-pro,groq-nacho,groq-sd,ollama-nacho,ollama-sd")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--report", default=None)
    args = ap.parse_args(argv)

    if args.report:
        path = Path(args.report)
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        false_rows = [r for r in rows if r["variant"] == "false"]
        true_rows = [r for r in rows if r["variant"] == "true"]
        good_f = [r for r in false_rows if r.get("ok")]
        good_t = [r for r in true_rows if r.get("ok")]
        strict = [r for r in good_f if any(p in (r.get("false") or []) for p in PLANTED)]
        loose = [r for r in good_f if any(p in (r.get("false") or []) + (r.get("unverifiable") or []) for p in PLANTED)]
        fa = [r for r in good_t if r.get("false")]
        print(f"FALSE map: {len(good_f)}/{len(false_rows)} answered · "
              f"strict detection {len(strict)} · loose {len(loose)}")
        print("  detection curve (panel size -> P(planted flagged)):", coverage(false_rows, PLANTED))
        print(f"TRUE map : {len(good_t)}/{len(true_rows)} answered · "
              f"false alarms {len(fa)} answers flagged a true premise as false")
        print("  false-alarm curve:", coverage(true_rows, list(PREMISES_TRUE)))
        if strict:
            print("  sample why:", (strict[0].get("why") or "")[:100])
        return 0

    want = set(args.lanes.split(","))
    lanes = [l for l in LANES if l["id"] in want]
    jobs = [(lane, lens, premises, variant)
            for variant, premises in (("true", PREMISES_TRUE), ("false", PREMISES_FALSE))
            for lane in lanes for lens in LENSES]
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT / f"map_audit_{stamp}.jsonl"
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(cell, *job): job for job in jobs}
        for fut in as_completed(futs):
            rows.append(fut.result())
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"receipt {path} · {len(rows)} calls · ${round(sum(r.get('cost_usd') or 0 for r in rows), 4)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
