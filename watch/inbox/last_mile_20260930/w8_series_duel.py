"""W8 multi-family duel SERIES - 12 duels, 4 families, 3 task shapes (2026-09-30).

Mission (operator): V1 attempted 4 families on ONE ask and aborted zero-spend
(grok-4.7 died twice on the harness 300s socket limit; the patched relaunch
never landed rows: logs/duel/duels.jsonl holds zero v1mf rows, see
v1_run_20260930.log). W8 is the real SERIES:

  glm      z-ai/glm-5.3-prime        NOT re-paid: contender text authored by
                                     THIS ACCOUNT's session model (GLM-5.3)
                                     from the ask text alone, before any
                                     contender fired; banked at cost 0.0 with
                                     provenance in W8_MULTIFAMILY.md.
  grok     x-ai/grok-4.3             V9 cheap pick, 1.25/2.50 per M
  ds       deepseek/deepseek-v4.1-flash   $0.63/M per operator (probe-metered)
  qwen     qwen/qwen3.7-flash        probe-metered ~0.13/M out; this model
                                     400s on the `reasoning` param, so it
                                     rides call_qwen (same body minus that
                                     param; verified live 2026-09-30)

Design: 3 shapes x 4 duels = 12. Per shape ONE identical ask goes to all 4
families (glm authored, 3 fired). The 4 duels per shape are the cycle pairs
(glm-grok, grok-ds, ds-qwen, qwen-glm): every family appears exactly twice
per shape, once as logical A and once as logical B, and every pairing meets
once per shape (3 samples per pairing across the series). Answers are reused
across the 4 duels of a shape, so within-shape variance is judge sampling,
not answer sampling (disclosed in the receipt). tools/duel_harness.py v1.1
judges BLIND (contenders appear as A and B only; identities are not
parameters of judge_prompt), parity-alternated slot swap, style counts.

Laws honored:
  - BUDGET_CAP $3.00 ABSOLUTE for THIS run: keys are probed live first
    (V9 law 5: HERMES_API_KEY_1 was near-empty; a dead key is dropped, not
    rotated into by luck); no shape fires unless spent + projection fits;
    halt after any row that blows it.
  - Idempotent: ask_ids already banked in logs/duel/duels.jsonl are skipped;
    fired contender answers cache to w8_contenders_20260930.jsonl so a
    killed run resumes without re-paying.
  - Width 1, strictly sequential (stagger law).
  - No em-dashes in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/w8_series_duel.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/w8_series_duel.py
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/w8_series_duel.py --shape adv
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

BUDGET_CAP = 3.00            # ABSOLUTE cap for THIS run (operator)
PROJECTED_PER_SHAPE = 0.60   # 3 contender fires + 4 judge calls, charged before each shape
KEY_PROBE_MODEL = "deepseek/deepseek-v4.1-flash"  # cheapest known live model, probe cost ~1e-5

HARNESS_SRC = ROOT / "tools" / "duel_harness.py"
CACHE_PATH = HERE / "w8_contenders_20260930.jsonl"
OUT_DEFAULT = dh.OUT_DEFAULT

GLM = "z-ai/glm-5.3-prime"
GROK = "x-ai/grok-4.3"
DS = "deepseek/deepseek-v4.1-flash"
QWEN = "qwen/qwen3.7-flash"
FAMS = {"glm": GLM, "grok": GROK, "ds": DS, "qwen": QWEN}
CYCLE = [("glm", "grok"), ("grok", "ds"), ("ds", "qwen"), ("qwen", "glm")]

RUBRICS = {
    "adv": ["root cause accuracy", "evidence citations", "falsifying predicates", "actionability"],
    "schema": ["normality and edge coverage", "type correctness", "migration safety", "evidence citations"],
    "plan": ["dependency ordering", "gate metric soundness", "risk identification", "actionability"],
}

GLM_ANSWER_FILES = {
    "adv": HERE / "w8_glm_adv.md",
    "schema": HERE / "w8_glm_schema.md",
    "plan": HERE / "w8_glm_plan.md",
}

LAWS = ("Laws: no em-dashes in your output. Cite file paths or section names for "
        "every claim about the provided documents. Mark anything uncertain "
        "UNPROVEN. Be concrete: numbers, names, test predicates. No praise, "
        "no preamble.")


def call_long(model: str, prompt: str, key: str,
              max_tokens: int = dh.CONTENDER_TOKENS) -> dict:
    """dh.call with the socket timeout raised 300s -> 900s (V1 fix receipt:
    grok reasoning models can outlive the harness default)."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "reasoning": {"max_tokens": dh.REASONING_CAP},
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


def call_qwen(model: str, prompt: str, key: str,
              max_tokens: int = dh.CONTENDER_TOKENS) -> dict:
    """Same as call_long minus the reasoning param: qwen3.7-flash rejects it
    with HTTP 400 'Provider returned error' (verified live 2026-09-30);
    without it the model answers fine (456-token probe produced content)."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


def call_ds(model: str, prompt: str, key: str, max_tokens: int = 0) -> dict:
    """ds-specific caller: thinking DISABLED, ignores the passed max_tokens.

    Fix receipt (2026-09-30, w8_run_20260930.log + 5 manual diags): on the
    schema and plan asks deepseek-v4.1-flash with thinking on burned the
    ENTIRE completion budget on hidden reasoning and returned zero content:
    4500/8000 total-token caps with the reasoning param, 8000 without it,
    and the original 16000 budget died twice on the 900s socket (metering
    lost). Diag 5 set reasoning {"enabled": false}: 38s, finish stop,
    10704 chars, $0.0021. So thinking-on DNFs 2 of 3 shapes for this
    family on this gateway; thinking-off is its only bounded-time
    configuration and is what the router row must record. max_tokens 8000
    bounds the worst case to ~120s at the measured 67 tokens/sec."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8000,
        "temperature": 0.4,
        "reasoning": {"enabled": False},
    }).encode()
    req = urllib.request.Request(
        dh.BASE, data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


CALLERS = {"grok": call_long, "ds": call_ds, "qwen": call_qwen}


def build_ask_adv() -> str:
    src = HARNESS_SRC.read_text(encoding="utf-8", errors="replace")
    return (
        "You are an adversarial code reviewer. Below is the full source of "
        "tools/duel_harness.py, a harness that fires one ask at two model "
        "families and has a third judge model score the two answers blind, "
        "appending one row per duel to a ledger jsonl. Name the THREE most "
        "severe real defects in this source: for each, the defect name, the "
        "exact function or code location, the evidence inside the source "
        "text that damns it (quote the exact code or comment), and a "
        "falsifying test predicate (a test that fails on the current source "
        "and passes once the defect is fixed). Then name the ONE most "
        "important MISSING SAFEGUARD with the same rigor. Rank by damage if "
        "unfixed. Judge only what is in this source; mark anything you "
        "cannot prove from the source UNPROVEN. Do not invent defects to "
        "fill the quota.\n\n"
        "<SOURCE>\n" + src + "\n</SOURCE>\n" + LAWS
    )


def build_ask_schema() -> str:
    return (
        "You are a schema designer for a model router. Real context: a duel "
        "ledger at logs/duel/duels.jsonl appends one row per duel with "
        "exactly these fields: ask_id, a_model, b_model, a_cost, b_cost, "
        "judge, winner (one of A, B, TIE, UNPARSED), rubric, ts, mode, swap "
        "(boolean), judge_cost, criteria (list of {criterion, a, b, note}), "
        "rationale, a_chars, b_chars, a_headers, b_headers. A separate price "
        "receipt lists per-model input and output dollars per million tokens "
        "with an as-of date. The estate now needs router family rows. "
        "Deliver: 1) a complete JSON Schema (draft 2020-12) for ONE "
        "router_families.json entry: family_id, model_id, prices "
        "(input_per_M, output_per_M, as_of, source), duel record per task "
        "shape (adversarial-review, schema-design, planning, code-analysis, "
        "grading) with wins, losses, ties, unparsed, rows_judged, plus "
        "totals, a quality gate block (metric name, metric value, decided, "
        "decided_min, gate passed), and provenance (ledger path, ledger "
        "sha256, row count, receipts). 2) The edge cases the schema must "
        "decide and how it decides them: a family with zero duels, UNPARSED "
        "winner rows, TIE rows, missing price, a cost of exactly zero, a "
        "task shape outside the known list. 3) An idempotent migration: how "
        "router_families.json is derived from duels.jsonl such that "
        "re-running never double counts. 4) Three validation predicates a "
        "test could pass or fail on. 5) One fully worked example instance "
        "with realistic values. Cite the ledger field names you rely on.\n\n"
        + LAWS
    )


def build_ask_plan() -> str:
    return (
        "You are a planning engineer. Real current state: (a) "
        "logs/duel/duels.jsonl holds duel rows with fields a_model, b_model, "
        "a_cost, b_cost, winner (A, B, TIE, UNPARSED), mode, swap, "
        "judge_cost, produced by tools/duel_harness.py; (b) a price table "
        "receipt exists at watch/inbox/last_mile_20260930/V9_NOUS_PRICES.md "
        "with per-model input and output dollars per million tokens; (c) no "
        "router exists yet; (d) the harness has a CLI but no programmatic "
        "query API. Goal: a family router that, given a task shape "
        "(adversarial-review, schema-design, planning), picks the cheapest "
        "model family whose duel-proven quality clears a gate. Deliver: 1) "
        "FIVE ordered implementation steps, each naming the file it touches "
        "and what it adds. 2) The gate metric: the exact number computed "
        "from duel rows that decides a family clears the gate per shape, "
        "including how TIE and UNPARSED rows count and the minimum sample "
        "before the gate is trusted. 3) The TWO highest risks with "
        "mitigations (consider judge bias, position bias, stale prices). 4) "
        "The rollback plan if the router picks badly. 5) The first test "
        "predicate to land. Be concrete: file paths, function names, "
        "formulas.\n\n" + LAWS
    )


ASK_BUILDERS = {"adv": build_ask_adv, "schema": build_ask_schema, "plan": build_ask_plan}


def probe_keys(keys: list[str]) -> tuple[list[str], float]:
    """One tiny call per key; drop a key ONLY on an HTTP auth/quota code.

    Fix receipt: the first probe asked for max_tokens=8 through call_long,
    the model's reasoning tokens consumed the whole budget, content came
    back empty, and dh.fire's empty-content check condemned a LIVE key
    (abort NO LIVE KEYS, zero contender spend, w8_run_20260930.log). The
    probe's job is auth/quota liveness, so only an HTTP error code
    condemns; empty probe content is inconclusive, not death. Reasoning
    is capped at 24 under a 48-token completion so content can appear.
    Probe spend (~1e-5/key) is counted against the budget.
    """
    import urllib.error
    live: list[str] = []
    spent = 0.0
    for i, key in enumerate(keys):
        body = json.dumps({
            "model": KEY_PROBE_MODEL,
            "messages": [{"role": "user", "content": "Reply with the single word ok."}],
            "max_tokens": 48, "temperature": 0.4,
            "reasoning": {"max_tokens": 24},
        }).encode()
        req = urllib.request.Request(
            dh.BASE, data=body,
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.load(r)
            spent += dh.cost_of(KEY_PROBE_MODEL, resp.get("usage", {}))
            live.append(key)
            print(f"key {i} live (probe ok)")
        except urllib.error.HTTPError as e:
            print(f"KEY {i} DEAD (HTTP {e.code}), dropping")
        except Exception as e:  # noqa: BLE001 - network hiccup: not a key verdict
            print(f"key {i} probe inconclusive ({e}); keeping")
            live.append(key)
    return live, spent


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
    p = argparse.ArgumentParser(description="W8 multi-family duel series (12 duels, 4 families, 3 shapes)")
    p.add_argument("--dry", action="store_true", help="print the plan, no calls, no writes")
    p.add_argument("--shape", choices=["adv", "schema", "plan"], help="run only this shape")
    p.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = p.parse_args(argv)

    shapes = [args.shape] if args.shape else ["adv", "schema", "plan"]

    # Operator/metered fallbacks (fire() prefers usage.cost from the API).
    dh.PRICE[GROK] = (1.25, 2.50)
    dh.PRICE[DS] = (0.63, 0.63)
    dh.PRICE[QWEN] = (0.13, 0.13)

    tasks = {s: ASK_BUILDERS[s]() for s in shapes}
    glm_texts = {s: GLM_ANSWER_FILES[s].read_text(encoding="utf-8") for s in shapes}
    done = banked_ask_ids(args.out)
    plan_pairs = []
    for s in shapes:
        for fa, fb in CYCLE:
            ask_id = f"w8-{s}-{fa}-{fb}"
            plan_pairs.append({"ask_id": ask_id, "shape": s, "a": fa, "b": fb,
                               "banked": ask_id in done})

    if args.dry:
        print(json.dumps({
            "run": "w8-multifamily-series", "budget_cap": BUDGET_CAP,
            "projected_per_shape": PROJECTED_PER_SHAPE,
            "shapes": shapes,
            "ask_chars": {s: len(t) for s, t in tasks.items()},
            "glm_chars": {s: len(t) for s, t in glm_texts.items()},
            "glm_provenance": "session-authored (this account, GLM-5.3) from ask text alone, cost 0.0",
            "contenders_to_fire": [GROK, DS, QWEN],
            "pairs": plan_pairs,
            "cache": sorted(cache_load()),
        }, indent=2))
        return 0

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    keys, spent = probe_keys(keys)
    if not keys:
        print("NO LIVE KEYS - aborting without contender spend")
        return 2

    cache = cache_load()
    rows: list[dict] = []
    for s in shapes:
        if spent + PROJECTED_PER_SHAPE > BUDGET_CAP:
            print(f"BUDGET HOLD: spent=${spent:.4f} + projected ${PROJECTED_PER_SHAPE} "
                  f"would exceed cap ${BUDGET_CAP:.2f}; stopping before shape {s}")
            break

        answers: dict[str, tuple[str, float]] = {
            "glm": (glm_texts[s], 0.0),
        }
        for fam, model in FAMS.items():
            if fam == "glm":
                continue
            key = f"{s}#{fam}"
            if key in cache:
                answers[fam] = (cache[key]["content"], 0.0)
                print(f"reuse cached {key} chars={len(cache[key]['content'])}")
                continue
            try:
                text, cost = dh.fire(model, tasks[s], keys, f"w8-{s}:{fam}",
                                     caller=CALLERS[fam])
            except (RuntimeError, SystemExit) as e:
                print(f"CONTENDER FAILED {key}: {e}; aborting run")
                return 1
            cache_bank(key, model, text, cost)
            cache[key] = {"key": key, "model": model, "content": text, "cost": cost}
            answers[fam] = (text, cost)
            spent += cost

        for fa, fb in CYCLE:
            ask_id = f"w8-{s}-{fa}-{fb}"
            if ask_id in done:
                print(f"skip banked {ask_id}")
                continue
            a_text, a_cost = answers[fa]
            b_text, b_cost = answers[fb]
            try:
                row = dh.run_duel(
                    ask_id, tasks[s], FAMS[fa], FAMS[fb],
                    a_text=a_text, b_text=b_text,
                    a_cost=a_cost, b_cost=b_cost,
                    judge_model=dh.DEFAULT_JUDGE, rubric=list(RUBRICS[s]),
                    context=None, out_path=args.out, keys=keys,
                    caller=call_long, mode="multifamily",
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
        break  # budget blown mid-shape: stop everything

    print(f"W8 SPENT THIS RUN ${spent:.4f} (cap ${BUDGET_CAP:.2f}); "
          f"duels banked this run {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
