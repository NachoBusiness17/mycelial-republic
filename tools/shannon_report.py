#!/usr/bin/env python3
"""shannon_report -- is the lens map carrying information, and at what cost per bit?

Treats every answer as a symbol from an alphabet of decisions. Then:

  H(X)          entropy of the decision distribution (bits)
  H(X|lens)     entropy left after knowing which lens asked
  I(lens;X)     how many bits the lens actually determines
  eps           erasure rate (calls that returned nothing = symbols lost)
  C             capacity of the observed channel = (1-eps) * H_max, bits/call
  eta           bits per 1k completion tokens (what one dollar of thinking buys)

    python tools/shannon_report.py [--file receipt.jsonl]
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cluster(key: str) -> str:
    k = (key or "").lower()
    if re.search(r"consumer|reader|pipeline|spawn|build.*(consumer|reader)|process via", k):
        return "build-consumer"
    if re.search(r"schema|definition|define|canonical|dedupe|cluster", k):
        return "define-schema"
    if re.search(r"prune|archive|delete|drop|discard|expire", k):
        return "prune"
    if re.search(r"freeze|stop|pause|halt|do not|don't|quarantine|hold", k):
        return "freeze-intake"
    if re.search(r"measure|audit|instrument|baseline|triage", k):
        return "measure-first"
    if re.search(r"demand", k):
        return "demand-first"
    return "other"


def H(counts: Counter, n: int) -> float:
    if n <= 0:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in counts.values() if c)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None)
    args = ap.parse_args(argv)
    files = sorted(glob.glob(str(ROOT / "memory" / "runs" / "lens" / "*.jsonl")))
    if not files:
        print("no lens receipts")
        return 2
    path = Path(args.file or files[-1])
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    ok = [r for r in rows if r.get("ok") and r.get("decision_key")]
    n = len(rows)
    n_ok = len(ok)
    eps = 1 - n_ok / n if n else 0.0

    syms = Counter(cluster(r["decision_key"]) for r in ok)
    h_x = H(syms, n_ok)
    k = len(syms)
    h_max = math.log2(k) if k > 1 else 0.0

    per = defaultdict(Counter)
    for r in ok:
        per[r["lens"]][cluster(r["decision_key"])] += 1
    h_cond = sum((sum(c.values()) / n_ok) * H(c, sum(c.values())) for c in per.values())
    mi = h_x - h_cond

    chars = sum(r.get("chars") or 0 for r in ok)
    toks = chars / 4.0
    cost = sum(r.get("cost_usd") or 0 for r in rows)
    mean_conf = [r["confidence"] for r in ok if isinstance(r.get("confidence"), (int, float))]

    print(f"receipt {path.name}")
    print(f"calls {n} · answered {n_ok} · erasure eps = {eps:.2f}")
    print(f"alphabet {k} symbols: {dict(syms.most_common())}")
    print(f"H(X)          = {h_x:.2f} bits   (H_max {h_max:.2f}, normalised {h_x / h_max if h_max else 0:.2f})")
    print(f"H(X|lens)     = {h_cond:.2f} bits")
    print(f"I(lens;X)     = {mi:.2f} bits   ({mi / h_max * 100 if h_max else 0:.0f}% of the lens-free entropy)")
    print(f"capacity C    = (1-eps)*H_max = {(1 - eps) * h_max:.2f} bits per call")
    print(f"tokens        ~{toks:.0f} completion tokens ({chars} chars)")
    if toks:
        print(f"efficiency    = {h_x / (toks / 1000):.3f} bits per 1k tokens "
              f"({mi / (toks / 1000):.3f} bits of lens-signal per 1k)")
    if cost:
        print(f"cost          ${cost:.4f} → ${cost / h_x:.2f} per decision-bit, "
              f"${cost / (mi if mi > 0 else 1):.2f} per bit of lens-signal")
    if mean_conf:
        print(f"confidence    mean {sum(mean_conf) / len(mean_conf):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
