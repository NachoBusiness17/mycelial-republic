"""F1 ask-bank duels - glm-5.3-flash vs glm-5.3-prime, the intra-family test.

Mission (operator, 2026-09-30): "can we functionally tell whether 5.3
flash is any better than our 5.3 max" -> the head-to-head. This script
is phase 1: draw THREE hidden asks from the ask bank (the clean
stimulus, no contamination) and duel z-ai/glm-5.3-flash (logical A)
vs z-ai/glm-5.3-prime (logical B, the max stand-in: Nous lists no
glm-5.3-max, prime is the estate's proven top GLM rung) on each,
fireworks/ember-1 blind judge, slot swap alternating by ledger parity
(harness v1.1 position-bias control; swap flips every row this script
banks). Same family on both sides, so this is the G2 intra-family
convergence test: a_chars/b_chars and per-criterion ties feed the
convergence metric computed in the F1 receipt.

Phase 2 (code task) lives in f1_code_duel.py; this file is prose-ask
duels only.

Secrecy law (AJ2 convention, copied from d6_askbank_duel.py): each
revealed ask is captured from the draw subprocess into memory and piped
into the contender prompts ONLY. Never printed whole; the receipt quotes
at most the first line. One draw per duel, consumed in fire order, no
cherry-picking.

Laws honored:
  - BUDGET_CAP $0.30 ABSOLUTE for the WHOLE F1 lane (operator): no duel
    fires unless spent + projection fits; halt on blow. DNF honest.
  - Idempotent: duel ask_ids already banked are skipped; contender
    answers cache to f1_contenders.jsonl so a killed run resumes
    without re-paying. Draw keys are duel ids, so a resumed duel
    reuses its drawn task from the cache (the draw ledger entry is the
    durable record of which ask the duel owns).
  - Width 1, strictly sequential (stagger law).
  - Streaming contender calls (call_long, the V1/D6-proven shape for
    long generations); judge stays on dh.call (ember answers fast).
  - No em-dash in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f1_series.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/f1_series.py
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

BUDGET_CAP = 0.30            # ABSOLUTE cap for the whole F1 lane (operator)
PROJECTED_PER_DUEL = 0.075   # flash + prime + judge worst case, charged before each duel
DUELS = 3
A_MODEL = "z-ai/glm-5.3-flash"    # logical A throughout
B_MODEL = "z-ai/glm-5.3-prime"    # logical B throughout (max stand-in)
FAMS = {"flash": A_MODEL, "prime": B_MODEL}
JUDGE = dh.DEFAULT_JUDGE
RUBRIC = ["section coverage", "defect severity", "evidence citations", "actionability"]
CACHE_PATH = HERE / "f1_contenders.jsonl"
DRAW_NOTE = "F1 flash-vs-prime head-to-head (intra-family convergence test)"


def call_long(model: str, prompt: str, key: str,
              max_tokens: int = dh.CONTENDER_TOKENS) -> dict:
    """Streaming contender call, same params as dh.call, SSE transport.

    V1/D6-proven shape: the gateway holds non-streaming sockets for
    whole generations and long answers die on read timeouts; streaming
    keeps the socket alive per-read.
    """
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": {"max_tokens": dh.REASONING_CAP},
        "stream": True,
        "stream_options": {"include_usage": True},
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    parts: list[str] = []
    usage: dict = {}
    with urllib.request.urlopen(req, timeout=900) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            choices = chunk.get("choices") or [{}]
            delta = choices[0].get("delta") or {}
            if delta.get("content"):
                parts.append(delta["content"])
            if chunk.get("usage"):
                usage = chunk["usage"]
    return {"choices": [{"message": {"content": "".join(parts)}}], "usage": usage}


def draw_hidden_live(duel_id: str) -> tuple[str, str, str]:
    """Draw one hidden ask with reveal, capturing output (never printing).

    Returns (draw_id, ask_id, full_rendered_task).
    """
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "ask_bank.py"), "draw", "--hidden",
         "--reveal", "--note", DRAW_NOTE + " " + duel_id],
        capture_output=True, text=True, check=True)
    cit = proc.stderr.strip()  # [ask_bank v1 draw v1h-NNNN <ask_id>]
    if not (cit.startswith("[ask_bank") and cit.endswith("]")):
        raise RuntimeError(f"unexpected draw citation: {cit!r}")
    parts = cit[1:-1].split()
    draw_id, ask_id = parts[-2], parts[-1]
    task = proc.stdout.strip()
    if not task:
        raise RuntimeError("draw --reveal produced empty task")
    return draw_id, ask_id, task


def cache_load() -> dict[str, dict]:
    found: dict[str, dict] = {}
    if CACHE_PATH.is_file():
        with open(CACHE_PATH, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                found[row["key"]] = row
    return found


def cache_bank(key: str, model: str, content: str, cost: float) -> None:
    with open(CACHE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"key": key, "model": model, "content": content,
                            "cost": round(cost, 4)}) + "\n")


def banked_ids(out_path: Path) -> set[str]:
    ids: set[str] = set()
    if out_path.is_file():
        with open(out_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.strip():
                    try:
                        ids.add(json.loads(line).get("ask_id", ""))
                    except json.JSONDecodeError:
                        continue
    return ids


def run_one(duel_id: str, draw: tuple[str, str, str], keys: list[str],
            cache: dict[str, dict], out_path: Path, spent: float) -> tuple[float, str]:
    """Fire both contenders on one drawn task, duel, bank. Returns (spent, status)."""
    draw_id, ask_id, task = draw
    first_line = next((l for l in task.splitlines() if l.strip()), "")[:100]
    print(f"DUEL {duel_id}: draw={draw_id} ask={ask_id} chars={len(task)} "
          f"first_line={first_line!r}")
    answers: dict[str, tuple[str, float]] = {}
    for fam, model in FAMS.items():
        key = f"{fam}#{duel_id}"
        if key in cache:
            answers[fam] = (cache[key]["content"], 0.0)  # already paid, resumed
            print(f"reuse cached {key} chars={len(cache[key]['content'])}")
            continue
        try:
            text, cost = dh.fire(model, task, keys, f"{duel_id}:{fam}",
                                 caller=call_long)
        except (RuntimeError, SystemExit) as e:
            print(f"CONTENDER FAILED {key}: {e}")
            continue
        cache_bank(key, model, text, cost)
        cache[key] = {"key": key, "model": model, "content": text, "cost": cost}
        answers[fam] = (text, cost)
        spent += cost
    if len(answers) < 2:
        print(f"DNF {duel_id}: contenders missing "
              f"{[f for f in FAMS if f not in answers]}")
        return spent, "DNF"
    row = dh.run_duel(
        duel_id, task, A_MODEL, B_MODEL,
        a_text=answers["flash"][0], b_text=answers["prime"][0],
        a_cost=answers["flash"][1], b_cost=answers["prime"][1],
        judge_model=JUDGE, rubric=list(RUBRIC),
        context=None, out_path=out_path, keys=keys, mode="f1-flash-vs-prime",
    )
    spent += row["judge_cost"]
    status = row["winner"]
    if spent > BUDGET_CAP:
        print(f"BUDGET BLOWN at ${spent:.4f} after {duel_id}; halting lane")
    return spent, status


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="F1 flash-vs-prime ask-bank duels")
    p.add_argument("--dry", action="store_true", help="print the plan, no calls")
    p.add_argument("--out", type=Path, default=dh.OUT_DEFAULT)
    args = p.parse_args(argv)

    if args.dry:
        print(json.dumps({"run": "f1-flash-vs-prime", "budget_cap": BUDGET_CAP,
                          "projected_per_duel": PROJECTED_PER_DUEL,
                          "duels": DUELS, "a_model": A_MODEL, "b_model": B_MODEL,
                          "judge": JUDGE, "rubric": RUBRIC,
                          "cache": sorted(cache_load()),
                          "banked_f1": sorted(i for i in banked_ids(args.out)
                                              if i.startswith("f1ab-")),
                          "ledger_rows": dh.ledger_row_count(args.out)}, indent=2))
        return 0

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    cache = cache_load()
    already = banked_ids(args.out)
    spent = 0.0
    results: list[dict] = []
    for r in range(1, DUELS + 1):
        duel_id = f"f1ab-r{r}-flash-prime"
        if duel_id in already:
            print(f"skip banked {duel_id}")
            continue
        if spent + PROJECTED_PER_DUEL > BUDGET_CAP:
            print(f"BUDGET HOLD: spent=${spent:.4f} + projected "
                  f"${PROJECTED_PER_DUEL} exceeds cap ${BUDGET_CAP:.2f}; stop at {r}")
            break
        # resume from cache when this duel already drew its task
        draw = None
        trow = cache.get(f"task#{duel_id}")
        if trow and trow.get("content_task"):
            draw = (trow["draw_id"], trow["ask_id"], trow["content_task"])
            print(f"reuse drawn task {duel_id}: {trow['draw_id']} {trow['ask_id']}")
        else:
            draw_id, ask_id, task = draw_hidden_live(duel_id)
            with open(CACHE_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps({"key": f"task#{duel_id}", "draw_id": draw_id,
                                    "ask_id": ask_id, "content_task": task}) + "\n")
            cache[f"task#{duel_id}"] = {"draw_id": draw_id, "ask_id": ask_id,
                                        "content_task": task}
            draw = (draw_id, ask_id, task)
        spent, status = run_one(duel_id, draw, keys, cache, args.out, spent)
        results.append({"duel": duel_id, "winner": status,
                        "spent_so_far": round(spent, 4)})
        if spent > BUDGET_CAP:
            break
    print(json.dumps({"run": "f1-flash-vs-prime", "results": results,
                      "spent_this_run": round(spent, 4), "cap": BUDGET_CAP}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
