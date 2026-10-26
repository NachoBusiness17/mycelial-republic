#!/usr/bin/env python3
"""DOLLAR BURN sweep - target list builder + manifest generator (2026-10-01).

Mission: per-file organ-compliance sweep. Three grep sets over mag/ tools/
server/ scripts/ (+ root main.py), union = sweep targets; one DeepSeek
adjudication per file via tools/ds_workhorse.py (batches of ~50, file-backed).

Organs (from watch/inbox/WIRING_DEBT_CENSUS_20261001.md rows 9, 6, 3):
  a) LLM fire path without importing mag.inference_budget
  b) remote URL fetch without a browser User-Agent header
  c) shared jsonl/json write without atomic tmp+replace

No em-dashes in any file this script writes (lane law).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = Path(__file__).resolve().parent
SCAN_DIRS = ["mag", "tools", "server", "scripts"]
EXTRA_FILES = ["main.py"]

HEAD_CAP = 20000   # chars of numbered head kept per file
TAIL_CAP = 8000    # chars of numbered tail kept per file
BATCH = 50

FIRE_RES = [
    re.compile(r"chat/completions"),
    re.compile(r"/v1/"),
    re.compile(r"api\.openai\.com|api\.deepseek\.com|api\.anthropic\.com|api\.x\.ai|api\.together\.xyz"),
    re.compile(r"openrouter"),
    re.compile(r"^\s*(?:import openai|from openai)", re.M),
    re.compile(r"\bAsyncOpenAI\b|\bOpenAI\s*\(|\bAnthropic\s*\("),
    re.compile(r"^\s*import httpx|from httpx", re.M),
    re.compile(r"api\.nousresearch|api\.groq\.com|generativelanguage\.googleapis"),
]
FETCH_RES = [
    re.compile(r"^\s*import urllib\.request|from urllib", re.M),
    re.compile(r"\burlopen\s*\("),
    re.compile(r"\brequests\.(?:get|post|head|put|request|Session)\s*\("),
    re.compile(r"^\s*import requests\b", re.M),
    re.compile(r"\bhttpx\.(?:get|post|AsyncClient|Client)"),
]
WRITE_MODE = re.compile(r"['\"][wa](?:\+?b|b\+)?['\"]")
WRITE_RES = [
    # open(...'w'/'a') where the same line names a .json/.jsonl surface
    re.compile(r"\.open\s*\(|(?<![\w.])open\s*\("),
]

QUESTION = (
    "file {path}: does this file (a) fire LLM calls without importing "
    "mag.inference_budget (b) fetch remote URLs without a browser User-Agent "
    "(c) write shared jsonl/json surfaces without atomic tmp+replace - answer "
    "per organ YES-compliant / NO-violation / NA with the line number, 3 lines total"
)


def scan_file(path: Path) -> dict | None:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    lines = raw.splitlines()
    hits = {"fire": [], "fetch": [], "write": []}
    for i, ln in enumerate(lines, 1):
        if any(r.search(ln) for r in FIRE_RES):
            hits["fire"].append(i)
        if any(r.search(ln) for r in FETCH_RES):
            hits["fetch"].append(i)
        # write set: an open( call AND a write/append mode AND .json/.jsonl named
        # on the line, or a write_text(/write_bytes( on a .json/.jsonl line
        is_open = any(r.search(ln) for r in WRITE_RES)
        json_named = ".json" in ln or ".jsonl" in ln
        mode_w = bool(WRITE_MODE.search(ln))
        wt = ".write_text(" in ln or ".write_bytes(" in ln or "write_text\n" in ln
        if json_named and ((is_open and mode_w) or wt):
            hits["write"].append(i)
    if not (hits["fire"] or hits["fetch"] or hits["write"]):
        return None
    rel = path.relative_to(ROOT).as_posix()
    return {
        "id": rel,
        "bytes": len(raw.encode("utf-8", errors="replace")),
        "nlines": len(lines),
        "fire_lines": hits["fire"][:40],
        "fetch_lines": hits["fetch"][:40],
        "write_lines": hits["write"][:40],
    }


def numbered_excerpt(raw: str) -> str:
    lines = raw.splitlines()
    numbered = [f"{i}| {ln}" for i, ln in enumerate(lines, 1)]
    total = sum(len(n) + 1 for n in numbered)
    if total <= HEAD_CAP + TAIL_CAP:
        return "\n".join(numbered)
    head: list[str] = []
    hb = 0
    for n in numbered:
        if hb + len(n) + 1 > HEAD_CAP:
            break
        head.append(n)
        hb += len(n) + 1
    tail: list[str] = []
    tb = 0
    for n in reversed(numbered):
        if tb + len(n) + 1 > TAIL_CAP:
            break
        tail.insert(0, n)
        tb += len(n) + 1
    cut = len(numbered) - len(head) - len(tail)
    return "\n".join(head) + f"\n[... {cut} middle lines truncated for budget ...]\n" + "\n".join(tail)


def main() -> None:
    files: list[Path] = []
    for d in SCAN_DIRS:
        base = ROOT / d
        if base.is_dir():
            files.extend(sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts))
    for extra in EXTRA_FILES:
        p = ROOT / extra
        if p.is_file():
            files.append(p)

    targets = [t for t in (scan_file(p) for p in files) if t]
    targets.sort(key=lambda t: t["id"])

    with (WORK / "targets.jsonl").open("w", encoding="utf-8") as f:
        for t in targets:
            f.write(json.dumps(t) + "\n")

    # build manifest items
    payload_bytes = 0
    items = []
    for t in targets:
        p = ROOT / t["id"]
        raw = p.read_text(encoding="utf-8", errors="replace")
        body = QUESTION.format(path=t["id"]) + "\n\n" + numbered_excerpt(raw)
        payload_bytes += len(body.encode("utf-8", errors="replace"))
        items.append({"id": t["id"], "text": body})

    for bi in range(0, len(items), BATCH):
        chunk = items[bi:bi + BATCH]
        with (WORK / f"manifest_{bi // BATCH + 1:02d}.jsonl").open("w", encoding="utf-8") as f:
            for it in chunk:
                f.write(json.dumps(it) + "\n")

    n_fire = sum(1 for t in targets if t["fire_lines"])
    n_fetch = sum(1 for t in targets if t["fetch_lines"])
    n_write = sum(1 for t in targets if t["write_lines"])
    n_batches = (len(items) + BATCH - 1) // BATCH
    in_tok = payload_bytes / 4
    out_tok = len(items) * 130
    proj = in_tok / 1e6 * 0.27 + out_tok / 1e6 * 1.10
    print(json.dumps({
        "scanned_py_files": len(files),
        "targets": len(targets),
        "fire_set": n_fire,
        "fetch_set": n_fetch,
        "write_set": n_write,
        "batches": n_batches,
        "payload_bytes": payload_bytes,
        "projected_cost_usd": round(proj, 4),
        "over_cap_1.50": proj > 1.5,
    }, indent=1))


if __name__ == "__main__":
    main()
