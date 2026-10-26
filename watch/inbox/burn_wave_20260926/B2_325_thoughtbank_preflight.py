"""B2-325 Rocinante thought-bank size preflight (byte-derived, re-derivable).

Source named: the fleet's exportable reasoning bank is the durable prose
artifact set, not tool trajectory:
  1. watch/inbox/**/*.md receipts >= 400 bytes (one reasoning part per file;
     below 400B is a pointer stub, not a part);
  2. memory/burns/LEDGER.jsonl one_line rows (compressed verdicts);
  3. memory/runs/**/VERDICT.md + FOLD.md (salon/quorum reasoning docs);
  4. memory/trajectory/steps.jsonl face=="milestone" rows (reasoning-flavored;
     the 22,380 face=="bash" rows are tool trajectory, the WRONG corpus class
     for a reasoning recipe, and are excluded).

Dedup rule named: sha256 of whitespace-normalized text across ALL units, so a
receipt and a LEDGER one_line quoting it collapse to one part. Deliberately
NOT a per-source dedup.

Count is exactly what a QLoRA export must yield or explain. Re-run:
  .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_325_thoughtbank_preflight.py
Writes: watch/inbox/burn_wave_20260926/B2_325_thoughtbank_preflight_results.json
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "B2_325_thoughtbank_preflight_results.json"


def norm(text) -> str:
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)
    return " ".join(text.split())


def main() -> int:
    seen = {}
    per_source = {}

    units = [p for p in (ROOT / "watch/inbox").rglob("*.md") if p.stat().st_size >= 400]
    per_source["inbox_receipts_md_ge400b"] = len(units)
    led = [json.loads(l) for l in open(ROOT / "memory/burns/LEDGER.jsonl", encoding="utf-8") if l.strip()]
    per_source["burns_ledger_rows"] = len(led)
    sv = [p for p in (ROOT / "memory/runs").rglob("*.md") if p.name in ("VERDICT.md", "FOLD.md")]
    per_source["salon_verdict_fold_docs"] = len(sv)
    steps = []
    for l in open(ROOT / "memory/trajectory/steps.jsonl", encoding="utf-8"):
        s = l.strip()
        if s:
            try:
                r = json.loads(s)
                if r.get("face") == "milestone":
                    steps.append(r)
            except Exception:
                pass
    per_source["trajectory_milestones"] = len(steps)
    per_source["trajectory_bash_rows_excluded"] = 22380

    def add(text, label):
        h = hashlib.sha256(norm(text).encode("utf-8")).hexdigest()
        seen.setdefault(h, label)

    for p in units:
        add(p.read_text(encoding="utf-8", errors="replace"), str(p.relative_to(ROOT)))
    for r in led:
        add(r.get("one_line", ""), "ledger:" + str(r.get("slug")))
    for p in sv:
        add(p.read_text(encoding="utf-8", errors="replace"), str(p.relative_to(ROOT)))
    for r in steps:
        add(r.get("result"), "milestone:" + str(r.get("step_hash")))

    out = {
        "schema": "thoughtbank_preflight.v1",
        "ts_source_scan": "2026-09-26",
        "per_source_raw": per_source,
        "raw_union": sum(per_source[k] for k in
                         ("inbox_receipts_md_ge400b", "burns_ledger_rows",
                          "salon_verdict_fold_docs", "trajectory_milestones")),
        "unique_after_dedup": len(seen),
        "dedup_rule": "sha256 of whitespace-normalized text across all sources",
        "regime_note": "arXiv 2511.00130 measured 8..8192 samples (peak 8192); "
                       "B2-74 recipe assumed ~10K parts",
    }
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
