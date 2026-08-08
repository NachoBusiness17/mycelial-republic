"""Classify corpus — the auto-producer for the skill-ledger labeled_rows counter.

Local models are proven at classification (bench: all 4 passed). So this runner:
  1. reads text items from a file/dir,
  2. CLASSIFIES every item with a LOCAL model (bulk, free, private, T0/T1-safe),
  3. AUDITS a sample (~--audit-pct) with deepseek-v4-flash to catch drift,
  4. records every row via mag/skill_ledger.record_labeled_row → counter ticks.

Usage:
  python tools/classify_corpus.py --file path/items.txt --limit 100 --audit-pct 10
  python tools/classify_corpus.py --dir memory --pattern "*.md" --limit 200
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root

from config import ROOT

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LOCAL_MODEL = "gemma4:latest"      # proven at classification, fast, free
AUDIT_MODEL = "deepseek-v4-flash"  # cheap control on the sample
DEFAULT_LABELS = ["code", "note", "plan", "research", "ops", "governance"]


def _call(provider: str, model: str, system: str, user: str, *, max_tokens: int) -> str:
    from models.providers import chat_provider

    tier = "T2" if provider == "deepseek" else "T1"
    res = chat_provider(provider, system, user, model=model, temperature=0.0, max_tokens=max_tokens, tier=tier)
    return str(res.get("text") or "").strip()


def classify(item: str, labels: list[str], model: str, *, provider: str = "ollama") -> tuple[str, float]:
    system = (
        f"Classify the text into EXACTLY one of: {', '.join(labels)}. "
        "Reply with only the label word, nothing else."
    )
    out = _call(provider, model, system, item, max_tokens=16)
    low = out.lower().strip(" .:[]\"'")
    best = None
    for lbl in labels:
        if lbl in low:
            best = lbl
            break
    if best is None:
        best = labels[0]
    return best, 1.0 if out else 0.0


def read_items(path: Path, *, limit: int) -> list[str]:
    items: list[str] = []
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip().lstrip("-*0123456789. ")
            if len(line) >= 12:
                items.append(line)
    elif path.is_dir():
        for p in sorted(path.rglob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            # chunk into non-empty lines
            for line in text.splitlines():
                line = line.strip()
                if 12 <= len(line) <= 400:
                    items.append(line)
    return items[:limit]


def run(
    items: list[str],
    *,
    labels: list[str],
    audit_pct: float,
    max_audit: int = 25,
) -> dict[str, Any]:
    from mag.skill_ledger import progress, record_labeled_row

    n_audit = min(max_audit, int(len(items) * audit_pct / 100.0)) if audit_pct else 0
    audit_idx = set(random.Random(2026).sample(range(len(items)), n_audit)) if n_audit else set()
    mismatches = 0
    for i, item in enumerate(items):
        label, conf = classify(item, labels, LOCAL_MODEL, provider="ollama")
        audited_by = None
        if i in audit_idx:
            audit_label, _ = classify(item, labels, AUDIT_MODEL, provider="deepseek")
            audited_by = AUDIT_MODEL
            if audit_label != label:
                mismatches += 1
                label = audit_label  # trust the audit on disagreement
        record_labeled_row(
            text=item,
            label=label,
            classifier=LOCAL_MODEL,
            confidence=conf,
            audited_by=audited_by,
            source="classify_corpus",
        )
        if (i + 1) % 25 == 0 or i == len(items) - 1:
            print(f"  {i+1}/{len(items)} classified (audit={audited_by or '-'})", flush=True)
    p = progress()
    return {
        "ok": True,
        "items": len(items),
        "audited": len(audit_idx),
        "audit_mismatches": mismatches,
        "local_model": LOCAL_MODEL,
        "audit_model": AUDIT_MODEL,
        "labels": labels,
        "progress": p,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="", help="source file of text items")
    ap.add_argument("--dir", default="", help="or a directory of .md files")
    ap.add_argument("--pattern", default="*.md")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--audit-pct", type=float, default=10.0)
    ap.add_argument("--labels", default=",".join(DEFAULT_LABELS))
    ap.add_argument("--seed", type=int, default=0, help="0 = use memory/working.md lines")
    args = ap.parse_args()
    labels = [l.strip() for l in args.labels.split(",") if l.strip()] or DEFAULT_LABELS

    if args.file:
        src = ROOT / args.file
    elif args.dir:
        src = ROOT / args.dir
    else:
        src = ROOT / "memory" / "working.md"

    items = read_items(src, limit=args.limit)
    if not items:
        print(f"no items found from {src}")
        return 2
    print(f"classifying {len(items)} items from {src} → labels {labels}")
    res = run(items, labels=labels, audit_pct=args.audit_pct)
    print(f"\nDone: {res['items']} items · {res['audited']} audited · "
          f"{res['audit_mismatches']} mismatches (escalated to audit label)")
    print(f"Counter → {res['progress']['labeled_rows']}/{res['progress']['labeled_target']} "
          f"({res['progress']['labeled_pct']}%) labeled rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
