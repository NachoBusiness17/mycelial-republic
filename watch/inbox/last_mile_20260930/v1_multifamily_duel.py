"""V1 multi-family duel - first multi-family calibration of the meter.

Mission (operator, 2026-09-30): the duel harness has only ever run glm vs
qwen. Nous carries 426 models; this run fires the SAME 3 adversarial-review
asks (identical ask text, fresh samples) at 4 families and lets ember judge
every pair blind:

  glm      z-ai/glm-5.3-prime   - NOT re-paid: reuses the banked G3 answer
                                 (GOPHER_BURN_output3_healthy_20260929.jsonl,
                                 already-paid cost $0.0264 on 2026-09-29),
                                 per the operator line "just reuse existing
                                 G3 content". G3 answered a sibling ask on
                                 the same spec (kill/keep each section, not
                                 3 weakest sections + 5 missing predicates);
                                 that ask-mismatch handicap is disclosed in
                                 the receipt, not hidden.
  grok     x-ai/grok-4.7                ($0.77/M per operator)
  gemini   google/gemini-3.8-flash      ($3.38/M per operator)
  ds       deepseek/deepseek-v4.1-flash ($0.63/M per operator)

The ask (same text all 3 rounds): paste the full BASELINE_SPEC from
watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md and demand the 3
weakest sections plus 5 missing predicates. Round-robin judging: 6 pairs
per round x 3 rounds = 18 ember judge calls, every row appended to
logs/duel/duels.jsonl by tools/duel_harness.py run_duel (blind judge,
parity-alternated slot swap, style-control fields).

Laws honored:
  - BUDGET_CAP $2.00 ABSOLUTE for THIS run: no round fires unless spent +
    worst-case projection fits; halt after any row that blows it.
  - Idempotent: pair ask_ids already in logs/duel/duels.jsonl are skipped;
    contender answers are cached to v1_contenders_20260930.jsonl so a
    killed run resumes without re-paying contenders.
  - Width 1, strictly sequential (stagger law).
  - No em-dashes in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/v1_multifamily_duel.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/v1_multifamily_duel.py
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

BUDGET_CAP = 2.00          # ABSOLUTE cap for THIS run (operator)
PROJECTED_PER_ROUND = 0.60  # 3 contenders worst-case + 6 judge calls, charged before each round

ROUNDS = 3
SPEC_PATH = ROOT / "watch" / "inbox" / "gps_baseline_ractor_20260929" / "BASELINE_SPEC.md"
G3_JSONL = ROOT / "watch" / "inbox" / "game_platform_basecamp_20260929" / "GOPHER_BURN_output3_healthy_20260929.jsonl"
G3_ID = "G3-model-test-glm-prime"
CACHE_PATH = HERE / "v1_contenders_20260930.jsonl"
OUT_DEFAULT = dh.OUT_DEFAULT

GLM = "z-ai/glm-5.3-prime"
GROK = "x-ai/grok-4.7"
GEM = "google/gemini-3.8-flash"
DS = "deepseek/deepseek-v4.1-flash"
FAMS = {"glm": GLM, "grok": GROK, "gem": GEM, "ds": DS}
PAIRS = [("glm", "grok"), ("glm", "gem"), ("glm", "ds"),
         ("grok", "gem"), ("grok", "ds"), ("gem", "ds")]
# Incident receipt (2026-09-30): between this driver's 06:28 write and the
# 06:32:32 process start, an external edit renamed the FAMS key "gem" to
# "gemini" (PAIRS untouched), so every gem pair printed "missing contender"
# while gemini answers still fired and cached under gemini#rN (run log
# lines 13-14 vs 20/24/28). PAIRS keys are now cross-checked against FAMS
# at import so a key drift fails fast instead of silently skipping pairs;
# CACHE_ALIAS lets this run reuse the already-paid gemini#rN rows.
assert all(f in FAMS for p in PAIRS for f in p), "PAIRS key not in FAMS"
CACHE_ALIAS = {"gem": "gemini"}

RUBRIC = ["section coverage", "defect severity", "evidence citations", "actionability"]

LAWS = ("Laws: no em-dashes in your output. Cite file paths or section names for "
        "every claim about the provided documents. Mark anything uncertain "
        "UNPROVEN. Be concrete: numbers, names, test predicates. No praise, "
        "no preamble.")


def call_long(model: str, prompt: str, key: str,
              max_tokens: int = dh.CONTENDER_TOKENS) -> dict:
    """Streaming contender call, same params as dh.call, SSE transport.

    Fix receipt: grok-4.7 could not answer the 26K-char spec ask over the
    harness's non-streaming shape - two 300s attempts (run 1) and a 900s
    attempt (run 2) all died on 'The read operation timed out' while a
    tiny probe answered in 1.7s when the lane was idle
    (v9_probe_prices.json row x-ai/grok-4.7), i.e. the gateway holds the
    connection for the whole generation and reasoning models exceed any
    whole-response socket cap. Streaming keeps the socket alive per-read
    (timeout fires only when tokens STOP flowing), params are byte-same
    (model, temperature 0.4, max_tokens, reasoning cap 6000), and the
    final usage chunk carries the metered cost. Judge calls stay on
    dh.call (ember answers in seconds).
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


def build_ask(spec: str) -> str:
    return (
        "You are an adversarial reviewer. Below is the estate's capability-ledger "
        "baseline spec. Name the THREE weakest sections of this spec: for each, "
        "the section name, the verdict KILL or KEEP-WITH-REWRITE, the exact "
        "wording or default that fails, and the evidence inside the spec text "
        "that damns it. Then name the FIVE most important MISSING PREDICATES: "
        "concrete testable checks (a test could pass or fail on them) the spec "
        "should demand but does not, each with the falsifying measurement and "
        "the section it belongs next to. Rank both lists by damage if unfixed.\n\n"
        "<SPEC>\n" + spec + "\n</SPEC>\n" + LAWS
    )


def load_g3() -> tuple[str, float]:
    with open(G3_JSONL, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("id") == G3_ID:
                content = row.get("content") or ""
                if not content.strip():
                    raise ValueError("G3 content empty")
                return content, float(row.get("cost_usd", 0.0))
    raise KeyError("G3 row not found in burn jsonl")


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


def banked_ask_ids(out_path: Path) -> set[str]:
    ids: set[str] = set()
    if out_path.is_file():
        with open(out_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ids.add(json.loads(line).get("ask_id", ""))
                except json.JSONDecodeError:
                    continue
    return ids


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="V1 multi-family duel (first multi-family calibration)")
    p.add_argument("--dry", action="store_true", help="print the plan, no calls, no writes")
    p.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = p.parse_args(argv)

    spec = SPEC_PATH.read_text(encoding="utf-8", errors="replace")
    task = build_ask(spec)
    g3_text, g3_paid = load_g3()

    # Operator-published blended rates, METER FALLBACK ONLY (fire() prefers
    # usage.cost from the API; these entries keep the fallback honest for the
    # three new models instead of the (3.0, 15.0) default pair).
    dh.PRICE[GROK] = (0.77, 0.77)
    dh.PRICE[GEM] = (3.38, 3.38)
    dh.PRICE[DS] = (0.63, 0.63)

    done = banked_ask_ids(args.out)
    plan_pairs = []
    for r in range(1, ROUNDS + 1):
        for fa, fb in PAIRS:
            ask_id = f"v1mf-r{r}-{fa}-{fb}"
            plan_pairs.append({"ask_id": ask_id, "round": r, "a": fa, "b": fb,
                               "banked": ask_id in done})

    if args.dry:
        print(json.dumps({
            "run": "v1-multifamily", "budget_cap": BUDGET_CAP,
            "projected_per_round": PROJECTED_PER_ROUND,
            "ask_chars": len(task), "spec_chars": len(spec),
            "g3_chars": len(g3_text), "g3_already_paid": g3_paid,
            "contenders_to_fire": [GROK, GEM, DS],
            "glm_entry": GLM + " via banked G3 (no new spend)",
            "pairs": plan_pairs,
            "cache": sorted(cache_load()),
        }, indent=2))
        return 0

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2

    cache = cache_load()
    spent = 0.0
    rows: list[dict] = []
    for r in range(1, ROUNDS + 1):
        if spent + PROJECTED_PER_ROUND > BUDGET_CAP:
            print(f"BUDGET HOLD: spent=${spent:.4f} + projected ${PROJECTED_PER_ROUND} "
                  f"would exceed cap ${BUDGET_CAP:.2f}; stopping before round {r}")
            break

        # fire (or reuse cached) contender answers for this round;
        # a family that fails its calls is skipped this round, not fatal
        # (grok lane stalls must not zero the whole calibration)
        answers: dict[str, tuple[str, float]] = {"glm": (g3_text, 0.0)}
        failed: list[str] = []
        for fam, model in FAMS.items():
            if fam == "glm":
                continue
            key = f"{fam}#r{r}"
            if key not in cache and CACHE_ALIAS.get(fam):
                key = f"{CACHE_ALIAS[fam]}#r{r}"  # reuse run-3's paid rows
            if key in cache:
                answers[fam] = (cache[key]["content"], 0.0)
                print(f"reuse cached {key} chars={len(cache[key]['content'])}")
                continue
            try:
                text, cost = dh.fire(model, task, keys, f"v1mf-r{r}:{fam}",
                                     caller=call_long)
            except (RuntimeError, SystemExit) as e:
                print(f"CONTENDER FAILED {key}: {e}; family skipped this round")
                failed.append(fam)
                continue
            cache_bank(key, model, text, cost)
            cache[key] = {"key": key, "model": model, "content": text, "cost": cost}
            answers[fam] = (text, cost)
            spent += cost
        if failed:
            print(f"round {r} families skipped: {failed}")

        for fa, fb in PAIRS:
            if fa not in answers or fb not in answers:
                print(f"skip pair {fa}-{fb} r{r}: missing contender")
                continue
            ask_id = f"v1mf-r{r}-{fa}-{fb}"
            if ask_id in done:
                print(f"skip banked {ask_id}")
                continue
            a_text, a_cost = answers[fa]
            b_text, b_cost = answers[fb]
            try:
                row = dh.run_duel(
                    ask_id, task, FAMS[fa], FAMS[fb],
                    a_text=a_text, b_text=b_text,
                    a_cost=a_cost, b_cost=b_cost,
                    judge_model=dh.DEFAULT_JUDGE, rubric=list(RUBRIC),
                    context=None, out_path=args.out, keys=keys,
                    mode="multifamily",
                )
            except (RuntimeError, SystemExit) as e:
                print(f"DUEL FAILED {ask_id}: {e}; continuing to next pair")
                continue
            done.add(ask_id)
            spent += row["judge_cost"]
            rows.append(row)
            if spent > BUDGET_CAP:
                print(f"BUDGET BLOWN at ${spent:.4f} after {ask_id}; halting run")
                break
        else:
            continue
        break  # budget blown mid-round: stop everything

    print(f"V1MF SPENT THIS RUN ${spent:.4f} (cap ${BUDGET_CAP:.2f}); "
          f"duels banked this run {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
