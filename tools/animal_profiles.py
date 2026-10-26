#!/usr/bin/env python3
"""animal_profiles - the living per-animal behavioral layer (2026-10-01).

OPERATOR DOCTRINE (three statements, one law):
  1. "model gates... behavioral data baked into the rib"
  2. "stop pretending the harness for each animal should be the same"
  3. "the animal itself grows from version to version - make it self improving
     and behavioral like you do with me; api doesn't tell us the real width
     for z.ai - we've written the rules of what we can get away with"

The RIB (RIB_MODEL_GATES) is the distilled snapshot a seat inhales at boot.
This tool is what keeps it TRUE: raw behavioral observations accumulate per
animal (never edited, append-only), and a distill pass regenerates the rib
from evidence - so version drift, new failure modes, and measured envelope
changes flow into boot doctrine on the next cycle without anyone relearning
them the expensive way.

Feeds (all existing, none new):
  logs/duel/duels.jsonl            win/loss + per-criterion behavior
  tools/quota_ledger_report.py     walls, deaths, window shapes
  watch/inbox/STEALTH_MINED_FINDINGS.jsonl   free-lane behavior (cached tokens...)
  cost rollup                      per-model price truth
  the 1302/1308/1310 receipts      transport/envelope failures
  mag/gps_mcp/gps_ledger.db3       pass_rate + momentum per model
  work-shape censuses              e.g. watch/inbox/last_mile_20260930/
                                   F4_FLASH_CENSUS.md (flash-vs-max blind
                                   pairs, third-family judge, 2026-09-30)

Outputs:
  memory/behavioral/animals/<slug>.jsonl   append-only raw observations
  --distill: regenerate the RIB from the accumulated evidence (the rib's
             per-animal rows carry last-updated + observation counts - a
             stale rib is a smell, same law as boot freshness)

Laws:
  - Observations are receipts, never vibes: every row cites its source file.
  - Fingerprint column (Amendment 10): behavior rows carry the fingerprint
    when known - same name + different fingerprint = different animal, no
    inherited trust.
  - The envelope rows ARE "the rules of what we can get away with" - measured
    (walls, clean shapes), because the API will not tell us.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEHAV_DIR = ROOT / "memory" / "behavioral" / "animals"
RIB = ROOT / "memory" / "rib" / "RIB_MODEL_GATES_20261001.md"


def slugify(model: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in model.lower()).strip("_")[:60]


def observe(model: str, kind: str, detail: str, source: str,
            fingerprint: str | None = None, ts: str | None = None) -> Path:
    """Append one behavioral observation. Never edits history."""
    BEHAV_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": ts or datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "model": model,
        "fingerprint": fingerprint,
        "kind": kind,      # transport | rail | failure | envelope | verdict | price
        "detail": detail,
        "source": source,  # receipt/file path - a row without one is void
    }
    p = BEHAV_DIR / f"{slugify(model)}.jsonl"
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return p


def distill() -> str:
    """Regenerate the rib's evidence block from accumulated observations.

    v0: emits the summary table (per animal: kinds observed, counts, newest
    ts, sources) to stdout for the rib's EVIDENCE footer. Full rib rewrite
    is a deliberate act (the rib is sealed config) - this gives the distiller
    the material; the orchestrator/mates apply it with a seal update.
    """
    if not BEHAV_DIR.exists():
        return "no observations yet"
    lines = []
    for p in sorted(BEHAV_DIR.glob("*.jsonl")):
        kinds: dict[str, int] = {}
        newest, n = "", 0
        sources = set()
        with p.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                n += 1
                kinds[r.get("kind", "?")] = kinds.get(r.get("kind", "?"), 0) + 1
                if r.get("ts", "") > newest:
                    newest = r.get("ts")
                if r.get("source"):
                    sources.add(str(r["source"]).split("/")[-1])
        if n:
            ks = ", ".join(f"{k}x{v}" for k, v in sorted(kinds.items()))
            lines.append(f"- {p.stem}: {n} obs [{ks}] newest {newest[:10]} "
                         f"sources={len(sources)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--distill"]:
        print(distill())
        return 0
    if argv[:1] == ["observe"]:
        # File one behavioral row from the shell (F4 2026-09-30: the living
        # layer must be reachable from PowerShell/cron/other seats without
        # each caller hand-writing Python; census lanes file their verdict
        # and price rows this way).
        import argparse
        p = argparse.ArgumentParser(
            description="append one behavioral observation (never edits history)")
        p.add_argument("--model", required=True, help="animal id, e.g. deepseek/deepseek-v4.1-flash")
        p.add_argument("--kind", required=True,
                       choices=["transport", "rail", "failure", "envelope",
                                "verdict", "price"],
                       help="observation kind")
        p.add_argument("--detail", required=True, help="what was observed (cite numbers)")
        p.add_argument("--source", required=True,
                       help="receipt/file path backing the row (a row without one is void)")
        p.add_argument("--fingerprint", default=None,
                       help="model fingerprint when known (Amendment 10)")
        args = p.parse_args(argv[1:])
        path = observe(args.model, args.kind, args.detail, args.source,
                       fingerprint=args.fingerprint)
        print(f"observed -> {path}")
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
