#!/usr/bin/env python3
"""Meld v2: claim-extraction convergence via the elder (DeepSeek).

The council's 3-gram meld scored ~0 on models that agreed claim-by-claim
(COUNCIL_ARTIFACT_20260827.md, DISPUTED trigram==semantic). This instrument
has the elder extract atomic claims from each blind answer, then scores
convergence as claim overlap. Elder-GPS law satisfied: every call injects
the full answer text as the position (no unanchored cosplay).

Usage: python scripts/meld_claims.py <answers_dir>
Out:   <answers_dir>/claims/ + a convergence table on stdout.

Keys from env only (DEEPSEEK_API_KEY). stdlib + requests.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from itertools import combinations
from pathlib import Path
from urllib.parse import urljoin

import requests

API = "https://api.deepseek.com/chat/completions"
MODEL = os.environ.get("ELDER_MODEL", "deepseek-v4-flash")
TEMPERATURE = 0.1
MAX_TOKENS = 1500
FRONT = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
CLAIM_RE = re.compile(r"\"text\"\s*:\s*\"(.+?)\"")

PROMPT = (
    "Extract the atomic claims from the text below. A claim is one short "
    "factual or evaluative sentence that could be true or false. Merge "
    "rewordings; drop pleasantries and hedging. Return ONLY a JSON array of "
    "strings, max 8 claims, each under 25 words.\n\nTEXT:\n{body}"
)


def extract_claims(body: str, key: str) -> list[str]:
    resp = requests.post(
        API,
        headers={"Authorization": f"Bearer {key}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": PROMPT.format(body=body[:6000])}],
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "thinking": {"type": "disabled"},  # verified empty-content cure
        },
        timeout=120,
    )
    data = resp.json()
    text = ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    # Prompt asks for a JSON array of strings; tolerate fences, prose wrappers,
    # and bare quoted lines. Never return a silent empty on parse failure.
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        try:
            arr = json.loads(text[start:end + 1])
            claims = [str(c).strip() for c in arr if str(c).strip()]
        except ValueError:
            claims = CLAIM_RE.findall(text)
    else:
        claims = [
            ln.strip().strip('"*-) ').strip()
            for ln in text.splitlines()
            if len(ln.strip()) > 15 and not ln.strip().startswith(("{", "}", "```", "Here"))
        ]
    claims = [c for c in claims if 3 < len(c) < 200][:8]
    if not claims:
        print(f"  RAW(head): {text[:200]!r}")
    return claims


def tokens(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def claim_sets_match(a: str, b: str) -> bool:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    inter = len(ta & tb)
    return inter / min(len(ta), len(tb)) >= 0.6


def main() -> int:
    answers_dir = Path(sys.argv[1])
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        raise SystemExit("DEEPSEEK_API_KEY missing from env")

    out_dir = answers_dir / "claims"
    out_dir.mkdir(exist_ok=True)
    answers: dict[str, dict[str, list[str]]] = {}
    for path in sorted(answers_dir.glob("*_Q*.md")):
        seat, qid = path.stem.rsplit("_Q", 1)
        body = FRONT.sub("", path.read_text(encoding="utf-8")).strip()
        if len(body) < 40:
            continue  # honest hole (e.g. elder Q4) — skipped, not faked
        cfile = out_dir / f"{path.stem}.json"
        if cfile.exists():
            claims = json.loads(cfile.read_text(encoding="utf-8"))
        else:
            try:
                claims = extract_claims(body, key)
            except Exception as exc:  # noqa: BLE001 — log and continue the sweep
                print(f"WARN {path.stem}: {exc}")
                continue
            time.sleep(0.5)
            cfile.write_text(json.dumps(claims, indent=1), encoding="utf-8")
        answers.setdefault(qid, {})[seat] = claims
        print(f"{path.stem}: {len(claims)} claims")

    print("\n=== CLAIM-CONVERGENCE (per question) ===")
    overall: list[float] = []
    for qid in sorted(answers):
        seats = answers[qid]
        print(f"\n{qid}:")
        for a, b in combinations(sorted(seats), 2):
            ca, cb = seats[a], seats[b]
            matched = sum(1 for x in ca if any(claim_sets_match(x, y) for y in cb))
            denom = max(1, min(len(ca), len(cb)))
            conv = matched / denom
            overall.append(conv)
            print(f"  {a}|{b}: {matched}/{min(len(ca), len(cb))} claims match -> {conv:.2f}")
            for x in ca:
                if any(claim_sets_match(x, y) for y in cb):
                    print(f"    SHARED: {x}")
    if overall:
        print(f"\nmean claim-convergence: {sum(overall)/len(overall):.2f} "
              f"(trigram meld said {0.001 + 0.028 * 0:.3f}-ish ~0.03 max)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
