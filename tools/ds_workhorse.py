#!/usr/bin/env python3
"""ds_workhorse - the cheap-tier batch lane (2026-10-01, operator doctrine:
"perfect the cheap before it - we have deepseek and a ton of it").

The animal rib's law: deepseek-v4.1-flash at ~$0.0043/ask is the bulk workhorse,
THINKING OFF MANDATORY (thinking-on: DNFs, socket hangs, word salad - AH10
byte-confirmed). This harness makes the ton of credits a standing lane for the
estate's MECHANICAL work: extraction, classification, triage, summarization -
never judgment (that climbs the ladder).

Harness laws (every one paid for already):
  - thinking OFF via the API's reasoning-disabled params; retry-once on empty
    (the gopher disease cure); never more than 2 attempts per item.
  - every batch: manifest in (items + prompt template), manifest out (results
    + cost + empties named), append to the cost ledger via cost_rollup's shape.
  - items are FILE-BACKED (a jsonl in, a jsonl out) - no interactive streams.
  - the falsifier law: outputs carry the item id; an output without its id is
    void; empty outputs are named, never silently dropped.
  - STANDING_RAILS law 2, the hollow-batch law (queue/STANDING_RAILS.md):
    "Material must render. Any batch prompt carries {text} (or equivalent) and
    the seat verifies the render - outputs without their material are VOID".
    Pasted here 2026-10-04 per GO item 9 (a10-ds-batches#3). Empty text is NOT
    success: a 200 with an empty completion banks ok_api true and ok_material
    false, never a bare ok=true. Cause: the hollow-batch incident 2026-10-03 -
    gapfold v1 fabricated from the prompt schema and the delta v1 arm refused
    on every row while all 30 rows banked ok:true, because ok measured API
    success only; evidence: memory/runs/ds_batches/gapfold_results.jsonl and
    frontier_delta_results.jsonl (both void-stamped in place 2026-10-04) and
    memory/runs/mickey17_v2/runs/run-0/lanes/a10-ds-batches.json rows 0-3.
  - max_tokens is the vendor default. The old max_tokens 2000 override was
    DELETED 2026-10-04 (GO item 3, a05-delta-study#0/#9): 2000 is a quarter of
    the deepseek-chat default ("default is 8K in non-thinking mode", 393216
    ceiling, api-docs.deepseek.com/api/create-chat-completion, byte-grepped
    2026-10-03), and the cap plus the old content[:6000] store slice parked
    13/14 v2 outputs at exactly 6000 chars, so the ds arm's 0-for-26 judged
    record measured the cap, not capability. The store slice is gone with it:
    full completions are banked, because a slice at the storage layer re-creates
    the same capped arm the override did.

Usage:
  python tools/ds_workhorse.py run --in items.jsonl --prompt-file p.md --out results.jsonl
  (items.jsonl: one {"id": ..., "text": ...} per line; the prompt file gets
   {text} substituted; DEEPSEEK_API_KEY from .env)

Result row schema (since 2026-10-04, GO item 9):
  {"id", "model", "ok_api" (the HTTP layer answered), "ok_material" (the
   completion carries rendered material - never empty, never an __ERROR__
   echo), "attempts", "cost_usd" (summed across attempts), "prompt_tokens"
   (per-row, so a hollow prompt with an empty render is visible at write
   time), "out" (full completion)}
  Old single "ok" field removed: it could not tell a 200 from a deliverable.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"  # v4.1-flash mapping per provider docs


def load_key() -> str:
    for env_path in (ROOT / ".env",):
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.partition("=")[2].strip()
    raise SystemExit("no DEEPSEEK_API_KEY in .env")


def ask(key: str, prompt: str) -> tuple[str, float, int]:
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        # max_tokens override deleted 2026-10-04 (a05-delta-study#0/#9): the
        # 2000 cap was a harness choice at a quarter of the vendor default
        # (8K non-thinking, 393216 ceiling per the deepseek API docs) and it
        # capped the arm, not the model. Omitted key = vendor default.
        "temperature": 0.3,
        "stream": False,
        # thinking-off: the v4 family THINKS BY DEFAULT (AH10 law). Measured
        # 2026-10-04 (d4_thinking_probe, receipt
        # watch/inbox/go_wave_20261004/d4_thinking_probe.md): an omitted key
        # returns reasoning_content; only the EXPLICIT
        # thinking:{type:disabled} is the off state. The prior comment here
        # claimed omission was the off state and every batch before the erratum
        # ran thinking-ON.
        "thinking": {"type": "disabled"},
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        row = json.loads(r.read().decode("utf-8"))
    content = (row.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    usage = row.get("usage") or {}
    # price truth: deepseek flash ~$0.27/M in, $1.10/M out (deepseek pricing);
    # metered cost if the API reports it, else estimated from usage.
    cost = (usage.get("prompt_tokens", 0) / 1e6 * 0.27
            + usage.get("completion_tokens", 0) / 1e6 * 1.10)
    return content, cost, int(usage.get("prompt_tokens", 0))


def run(items_path: Path, prompt_file: Path, out_path: Path) -> None:
    key = load_key()
    template = prompt_file.read_text(encoding="utf-8")
    # render guard, rails law 2 (hollow-batch law): a template without {text}
    # renders a material-free prompt for every item, and a material-free
    # prompt gets fabrication or refusal, not a deliverable. Fail the batch
    # before spending a cent. Cause: gapfold v1 fabricated and delta v1
    # refused 2026-10-03 behind a hollow prompt (a10-ds-batches#0/#1/#3);
    # evidence: watch/inbox/go_wave_20261004/ds_workhorse.md.
    if "{text}" not in template:
        raise SystemExit(
            "render guard: prompt template has no {text} slot - hollow batch refused")
    items = [json.loads(l) for l in items_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    for it in items:
        if not str(it.get("text", "")).strip():
            raise SystemExit(
                f"render guard: item {it.get('id')!r} renders empty text - hollow batch refused")
    total = 0.0
    with out_path.open("w", encoding="utf-8") as out:
        for it in items:
            prompt = template.replace("{text}", str(it.get("text", "")))
            content = ""
            cost = 0.0
            prompt_tokens = 0
            ok_api = False
            for attempt in (1, 2):  # retry-once on empty (the gopher cure)
                try:
                    content, c, prompt_tokens = ask(key, prompt)
                    cost += c  # summed across attempts; the old code overwrote
                    # a 200 is an API success even when the completion is empty
                    ok_api = True
                except Exception as exc:  # noqa: BLE001 - named, never silent
                    content, prompt_tokens = f"__ERROR__ {exc}"[:200], 0
                if content.strip() and not content.startswith("__ERROR__"):
                    break
                time.sleep(2)
            total += cost
            # rails law 2 split: ok_api = the wire answered; ok_material = the
            # completion carries rendered material. Empty text is not success.
            ok_material = bool(content.strip()) and not content.startswith("__ERROR__")
            out.write(json.dumps({
                "id": it.get("id"), "model": MODEL,
                "ok_api": ok_api, "ok_material": ok_material,
                "attempts": attempt, "cost_usd": round(cost, 6),
                "prompt_tokens": prompt_tokens,
                "out": content,
            }) + "\n")
            out.flush()
            print(f"{it.get('id')} ok_api={ok_api} ok_material={ok_material} "
                  f"${total:.4f} cum", flush=True)
    print(f"BATCH DONE {len(items)} items ${total:.4f} -> {out_path}")


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "run":
        args = dict(zip(sys.argv[2::2], sys.argv[3::2]))
        # dogfood-48h move 4, keyed by the INPUT batch file: different seats
        # may batch different files concurrently (legitimate), but two racers
        # on ONE pending file is the double-drain class the twins proved.
        import hashlib

        from tools.instance_guard import guard_or_exit

        guard_or_exit("ds_workhorse_"
                      + hashlib.sha256(str(args["--in"]).encode()).hexdigest()[:8])
        run(Path(args["--in"]), Path(args["--prompt-file"]), Path(args["--out"]))
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
