"""D6 ask-bank duel - first live draw from the hidden 70/30 bank.

Mission (operator, 2026-09-30): dogfood AJ2. Draw ONE hidden ask
(tools/ask_bank.py draw --hidden --reveal) and fire a 3-round duel,
z-ai/glm-5.3-prime (logical A) vs google/gemini-3.8-flash (logical B),
fireworks/ember-1 blind judge, slot swap alternating by ledger parity
(run_duel v1.1 position-bias control). The drawn ask is FRESH: it has
never sat in any prompt-visible path, so neither contender can have it
cached or learned from the receipt corpus. This is the cleanest
contamination-free signal the estate has produced; V1 multifamily
(plain-sight W8 material) is the contrast arm.

Secrecy law (AJ2 convention): the revealed ask is captured from the
draw subprocess into memory and piped into the contender prompts ONLY.
This script never prints the full ask; the receipt quotes at most the
first line. Dry mode computes the would-be draw WITHOUT appending to
the draw ledger and without revealing the body.

The verdict feeds tools/gps_mcp/gps_ledger.db3 as real traffic via
CapabilityLedger.record_verdict (the meter feeding itself): duel
winner -> verdict 1, loser -> verdict 0, TIE or UNPARSED -> no verdict
row (no ground truth; disclosed, never faked). task_shape is
"askbank-v1-<shape>" so future draws of the same shape pool into one
router row. evidence_hash is the sha256 of the exact banked duels.jsonl
line, so every gps verdict joins its duel row.

Laws honored:
  - BUDGET_CAP $0.50 ABSOLUTE for THIS run (operator): no round fires
    unless spent + worst-case projection fits; halt after any spend
    that blows it. DNF honest: a failed round is reported as DNF and
    skipped, never faked.
  - Idempotent: ask_ids already banked in logs/duel/duels.jsonl are
    skipped; contender answers cache to d6_contenders.jsonl so a killed
    run resumes without re-paying.
  - Width 1, strictly sequential (stagger law).
  - No em-dashes in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/d6_askbank_duel.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/d6_askbank_duel.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

BUDGET_CAP = 0.50          # ABSOLUTE cap for THIS run (operator)
PROJECTED_PER_ROUND = 0.16  # 2 contenders worst-case + 1 judge call, charged before each round
ROUNDS = 3
A_MODEL = "z-ai/glm-5.3-prime"        # logical A throughout
B_MODEL = "google/gemini-3.8-flash"   # logical B throughout
FAMS = {"glm": A_MODEL, "gem": B_MODEL}
JUDGE = dh.DEFAULT_JUDGE
RUBRIC = ["section coverage", "defect severity", "evidence citations", "actionability"]
GPS_DB = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
CACHE_PATH = HERE / "d6_contenders.jsonl"
DRAW_NOTE = "D6 ask-bank duel first live draw (glm-prime vs gemini-3.8-flash, 3 rounds)"

# Operator-published blended rate, METER FALLBACK ONLY (fire() prefers
# usage.cost from the API; V1 multifamily used the same entry).
dh.PRICE[B_MODEL] = (3.38, 3.38)


def call_long(model: str, prompt: str, key: str,
              max_tokens: int = dh.CONTENDER_TOKENS) -> dict:
    """Streaming contender call, same params as dh.call, SSE transport.

    V1 multifamily proved this shape for exactly these two contenders
    (the gateway holds non-streaming sockets for whole generations and
    long answers die on read timeouts; streaming keeps the socket alive
    per-read). Judge calls stay on dh.call (ember answers in seconds).
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


def draw_hidden_live() -> tuple[str, str, str]:
    """Draw one hidden ask with reveal, capturing output (never printing).

    Returns (draw_id, ask_id, full_rendered_task). The subprocess prints
    the full ask to ITS stdout; capture_output=True keeps it out of every
    prompt-visible log. Citation line lands on stderr.
    """
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "ask_bank.py"), "draw", "--hidden",
         "--reveal", "--note", DRAW_NOTE],
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


def draw_hidden_dry() -> dict:
    """Compute which hidden entry the live draw would pick, no append.

    Mirrors cmd_draw's selection exactly (least-drawn first, then file
    order) using ask_bank's own loaders. Prints ask_id/shape/first_line
    only; the body stays unrevealed in dry mode.
    """
    from ask_bank import first_line, hidden_dir, load_jsonl
    rows = load_jsonl(hidden_dir(ROOT) / "hidden.jsonl")
    ledger = load_jsonl(hidden_dir(ROOT) / "draws.jsonl")
    drawn = [r["ask_id"] for r in ledger if r.get("half") == "hidden"]
    entry = min(rows, key=lambda e: (drawn.count(e["ask_id"]), rows.index(e)))
    return {"would_draw": entry["ask_id"], "shape": entry["shape"],
            "first_line": first_line(entry["body"]),
            "hidden_draws_so_far": len(drawn)}


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


def banked_rows(out_path: Path) -> dict[str, str]:
    """ask_id -> exact banked json line (for gps evidence hashes)."""
    rows: dict[str, str] = {}
    if out_path.is_file():
        with open(out_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.rstrip("\n")
                if line.strip():
                    try:
                        rows[json.loads(line).get("ask_id", "")] = line
                    except json.JSONDecodeError:
                        continue
    return rows


def shape_of(ask_id: str) -> str:
    return ask_id.rsplit("-", 1)[-1]


def gps_task_shape(ask_id: str) -> str:
    return f"askbank-v1-{shape_of(ask_id)}"


def feed_gps(rows_banked: dict[str, str], duel_ids: list[str]) -> list[dict]:
    """Record each duel verdict as real gps traffic; return row states.

    winner -> 1, loser -> 0, TIE/UNPARSED -> no row (no ground truth).
    evidence_hash = sha256 of the exact banked duels.jsonl line.
    """
    from gps_mcp.ledger import CapabilityLedger
    ledger = CapabilityLedger(GPS_DB)
    fed: list[dict] = []
    for ask_id in duel_ids:
        line = rows_banked.get(ask_id)
        if not line:
            continue
        row = json.loads(line)
        if row.get("winner") not in ("A", "B"):
            fed.append({"ask_id": ask_id, "fed": False,
                        "reason": f"winner={row.get('winner')} -> no verdict row"})
            continue
        shape = gps_task_shape(ask_id)
        eh = hashlib.sha256(line.encode("utf-8")).hexdigest()
        winner_model = row["a_model"] if row["winner"] == "A" else row["b_model"]
        loser_model = row["b_model"] if row["winner"] == "A" else row["a_model"]
        r_win = ledger.record_verdict(winner_model, shape, 1, eh)
        r_lose = ledger.record_verdict(loser_model, shape, 0, eh)
        fed.append({"ask_id": ask_id, "fed": True, "task_shape": shape,
                    "evidence_hash": eh[:16] + "...",
                    "winner": {"model": winner_model,
                               "pass_rate": round(r_win.pass_rate, 4),
                               "n": r_win.sample_size},
                    "loser": {"model": loser_model,
                              "pass_rate": round(r_lose.pass_rate, 4),
                              "n": r_lose.sample_size}})
    return fed


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="D6 ask-bank duel (first live hidden draw)")
    p.add_argument("--dry", action="store_true", help="print the plan, no calls, no writes")
    p.add_argument("--out", type=Path, default=dh.OUT_DEFAULT)
    args = p.parse_args(argv)

    if args.dry:
        print(json.dumps({"run": "d6-askbank", "budget_cap": BUDGET_CAP,
                          "projected_per_round": PROJECTED_PER_ROUND,
                          "rounds": ROUNDS, "a_model": A_MODEL, "b_model": B_MODEL,
                          "judge": JUDGE, "dry_draw": draw_hidden_dry(),
                          "cache": sorted(cache_load()),
                          "gps_db": str(GPS_DB)}, indent=2))
        return 0

    draw_id, ask_id, task = draw_hidden_live()
    first_line = next((l for l in task.splitlines() if l.strip()), "")[:120]
    print(f"DRAW {draw_id} ask_id={ask_id} chars={len(task)} first_line={first_line!r}")

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2

    banked = banked_rows(args.out)
    cache = cache_load()
    spent = 0.0
    duel_ids: list[str] = []
    dnf: list[str] = []
    for r in range(1, ROUNDS + 1):
        if spent + PROJECTED_PER_ROUND > BUDGET_CAP:
            print(f"BUDGET HOLD: spent=${spent:.4f} + projected ${PROJECTED_PER_ROUND} "
                  f"would exceed cap ${BUDGET_CAP:.2f}; stopping before round {r}")
            break
        answers: dict[str, tuple[str, float]] = {}
        for fam, model in FAMS.items():
            key = f"{fam}#r{r}"
            if key in cache:
                answers[fam] = (cache[key]["content"], 0.0)
                print(f"reuse cached {key} chars={len(cache[key]['content'])}")
                continue
            try:
                text, cost = dh.fire(model, task, keys, f"d6-r{r}:{fam}",
                                     caller=call_long)
            except (RuntimeError, SystemExit) as e:
                print(f"CONTENDER FAILED {key}: {e}")
                continue
            cache_bank(key, model, text, cost)
            cache[key] = {"key": key, "model": model, "content": text, "cost": cost}
            answers[fam] = (text, cost)
            spent += cost
        if len(answers) < 2:
            missing = [f for f in FAMS if f not in answers]
            duel_id = f"d6ab-r{r}-glm-gem"
            print(f"DNF round {r}: contenders missing {missing}")
            dnf.append(duel_id)
            continue
        duel_id = f"d6ab-r{r}-glm-gem"
        if duel_id in banked:
            print(f"skip banked {duel_id}")
            duel_ids.append(duel_id)
            continue
        try:
            row = dh.run_duel(
                duel_id, task, A_MODEL, B_MODEL,
                a_text=answers["glm"][0], b_text=answers["gem"][0],
                a_cost=answers["glm"][1], b_cost=answers["gem"][1],
                judge_model=JUDGE, rubric=list(RUBRIC),
                context=None, out_path=args.out, keys=keys,
                mode="askbank",
            )
        except (RuntimeError, SystemExit) as e:
            print(f"DUEL FAILED {duel_id}: {e}; DNF")
            dnf.append(duel_id)
            continue
        spent += row["judge_cost"]
        duel_ids.append(duel_id)
        if row["winner"] == "UNPARSED":
            print(f"DNF round {r}: judge output unparseable, no verdict")
            dnf.append(duel_id)
        if spent > BUDGET_CAP:
            print(f"BUDGET BLOWN at ${spent:.4f} after {duel_id}; halting run")
            break

    banked = banked_rows(args.out)
    fed = feed_gps(banked, duel_ids)
    tally = {"A": 0, "B": 0, "TIE": 0}
    for did in duel_ids:  # `did`, not `ask_id`: shadowing the bank ask_id here
        # mislabeled every gps row task_shape on the first live run (D6
        # receipt fix 2026-09-30: rows landed as askbank-v1-gem, the duel
        # id's model suffix, instead of askbank-v1-safeguard)
        w = (banked.get(did) and json.loads(banked[did]).get("winner")) or "?"
        if w in tally:
            tally[w] += 1
    print(json.dumps({
        "run": "d6-askbank", "draw_id": draw_id, "ask_id": ask_id,
        "task_shape": gps_task_shape(ask_id),
        "spent_this_run": round(spent, 4), "cap": BUDGET_CAP,
        "duels": duel_ids, "dnf": dnf,
        "tally_logical": {"glm_prime_wins": tally["A"],
                          "gemini_flash_wins": tally["B"], "ties": tally["TIE"]},
        "gps_fed": fed,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
