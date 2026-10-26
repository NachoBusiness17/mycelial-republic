"""X4 duel series - the n=1 fix (coverage gap 5, COVERAGE_GAPS_20260930.md row 5).

The W3 duel harness banked one blind verdict (blind rejudge flipped the
v1.0 name-aware verdict, qwen 19-17) and the gap table called it a coin
flip: S5 says n~30-60 before the router row is trusted. This driver is
the first installment: ~10 live duels, qwen/qwen3.8-max-prime (A) vs
z-ai/glm-5.3-prime (B), blind ember judge, one row each appended to
logs/duel/duels.jsonl by tools/duel_harness.py run_duel (v1.1: anonymized
judge, parity-alternated slot swap, style-control header counts).

Ask mix per the S5 protocol (task-shape diversity so the pair verdict is
not overfit to one shape): 3 adversarial-review, 3 planning, 2
schema-design, 2 grading. Every ask is grounded in a real repo artifact
read at runtime (byte-true, gopher driver pattern from
watch/inbox/game_platform_basecamp_20260929/hermes_gopher_burn_20260929.py).

Laws honored here:
  - BUDGET_CAP $3.00 ABSOLUTE: no duel fires unless spent + worst-case
    projection for one duel still fits; actual costs metered from the
    banked rows (usage.cost first, price table fallback).
  - Idempotent: ask_ids already in logs/duel/duels.jsonl are skipped, so
    a killed run resumes without double spend.
  - Width 1: duels run strictly sequential (stagger law; no 1302 storms).
  - No em-dashes in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/hydrology/x4_duel_series.py --dry
    .venv/Scripts/python.exe watch/inbox/hydrology/x4_duel_series.py [--limit N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

BUDGET_CAP = 3.00          # ABSOLUTE cap for THIS series (operator)
PROJECTED_PER_DUEL = 0.25  # worst-case projection charged before each fire
A_MODEL = "qwen/qwen3.8-max-prime"     # logical A throughout the series
B_MODEL = "z-ai/glm-5.3-prime"         # logical B throughout the series

RUBRIC_ADV = "section coverage, defect severity, evidence citations, actionability"
RUBRIC_PLAN = "failure mode coverage, sequencing correctness, evidence citations, actionability"
RUBRIC_SCHEMA = "normality and edge coverage, type correctness, migration safety, evidence citations"
RUBRIC_GRADE = "calibration to the artifact, evidence citations, verdict consistency, actionability"

LAWS = ("Laws: no em-dashes in your output. Cite file paths or section names for "
        "every claim about the provided documents. Mark anything uncertain "
        "UNPROVEN. Be concrete: numbers, names, test predicates. No praise, "
        "no preamble.")


def read(rel: str, limit: int) -> str:
    with open(ROOT / rel, "r", encoding="utf-8", errors="replace") as f:
        return f.read()[:limit]


def last_ledger_row() -> str:
    lines = [l for l in (ROOT / "logs" / "duel" / "duels.jsonl").read_text(
        encoding="utf-8", errors="replace").splitlines() if l.strip()]
    return lines[-1] if lines else ""


def build_asks() -> list[dict]:
    hydro = read(r"mag\hydrology.py", 12000)
    water = read(r"mag\water_graph.py", 12000)
    compass = read(r"docs\ref\MAG_MYCELIAL_REPUBLIC_COMPASS.md", 11000)
    gaps = read(r"watch\inbox\COVERAGE_GAPS_20260930.md", 5000)
    receipt = read(r"watch\inbox\game_platform_basecamp_20260929\W3_DUEL_HARNESS_20260929.md", 7000)
    v11 = receipt[receipt.find("## v1.1"):] if "## v1.1" in receipt else receipt
    day_syn = read(r"watch\inbox\DAY_SYNTHESIS_20260929.md", 20000)
    t3 = next((l for l in day_syn.splitlines() if l.strip().startswith("T3.")),
              "T3 clause not found")
    ledger_v1 = last_ledger_row()

    return [
        # ------------------------------------------------ adversarial-review
        {
            "id": "x4-adv-hydrology-rung1",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": hydro,
            "ask": "You are an adversarial reviewer. Kill or keep each design law of this module "
                   "(integer-only determinism, Q8 head, depth via cross_section, check-valve flow, "
                   "siphon prime/break, inherited tick structure). Name the three weakest numeric "
                   "defaults (HEAD_SCALE, DEPTH_SCALE, conductance, cross_section) and the measurement "
                   "or test predicate that would replace each. Name anything a reviewer from the "
                   "other model family would systematically miss.\n\n"
                   "<SOURCE>\n" + hydro + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "x4-adv-water-graph",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": water,
            "ask": "You are an adversarial reviewer of the parent verdict engine this estate builds "
                   "on. Kill or keep each section: node/pipe model, junction gates, siphons, steam, "
                   "starvation law, tick loop, to_spec round-trip. Find the three weakest behaviors "
                   "(not style) and give a falsifying test predicate for each. Mark anything you "
                   "cannot verify from the source alone UNPROVEN.\n\n"
                   "<SOURCE>\n" + water + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "x4-adv-compass",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": compass,
            "ask": "You are an adversarial reviewer of this vision/compass document. Kill or keep "
                   "each section: which claims are aspirations wearing measurement clothes, which "
                   "terms are defined nowhere, where does the agent loop promise behavior that no "
                   "gate enforces. Name the three claims most likely to mislead a new agent seat "
                   "and what verifiable statement each should become.\n\n"
                   "<SOURCE>\n" + compass + "\n</SOURCE>\n" + LAWS,
        },
        # ---------------------------------------------------------- planning
        {
            "id": "x4-plan-hydrology-rung2",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan rung 2 of the hydrology ladder. Rung 1 (below) replaced the boolean head "
                   "with fixed-point graded head: depth = volume * 1000 // cross_section, head = "
                   "elev * 256 + depth, flow = (dHead * conductance) >> 8. Rung 2 candidates: rain "
                   "input, evaporation/steam coupling, depth-tint export, and a graded surface "
                   "spring. Order the rungs, name the failure modes each introduces against the "
                   "determinism law (integers only, no floats, no RNG, no clocks), and give the "
                   "first test predicate per rung. State what must NOT change (water_graph.py stays "
                   "untouched; spec compat).\n\n"
                   "<RUNG1_SOURCE>\n" + hydro + "\n</RUNG1_SOURCE>\n" + LAWS,
        },
        {
            "id": "x4-plan-duel-to-n30",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan the completion of the duel series from n~12 to n=30 verdicts per the "
                   "operator clause below. Deliver: the ask-bank design (70/30 hidden split, task "
                   "shapes, who holds the hidden 30), the budget schedule to stay under $3 total "
                   "for the remaining duels, the stopping rule (sample-until-CI-excludes-zero), "
                   "how to compute that CI on win/tie tallies, and the failure modes (position "
                   "bias residue, rubric drift, judge parse failures) with the control for each.\n\n"
                   "<OPERATOR_CLAUSE>\n" + t3 + "\n</OPERATOR_CLAUSE>\n" + LAWS,
        },
        {
            "id": "x4-plan-gap-closure",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan a 3-day closure of coverage gaps 2, 9, and 10 from the table below "
                   "(mount the deduped law corpus into agent context, census the two oldest game "
                   "organs for room.py adoption, wire chan.py into steer readers). For each: the "
                   "first concrete action, the test that proves closure, the risk that the gap "
                   "reopens, and the order across the three days. Kill any part of the one-line "
                   "closers in the table that is under-specified and say what replaces it.\n\n"
                   "<GAPS>\n" + gaps + "\n</GAPS>\n" + LAWS,
        },
        # ------------------------------------------------------ schema-design
        {
            "id": "x4-schema-duel-row-v2",
            "cat": "schema-design",
            "rubric": RUBRIC_SCHEMA,
            "ask": "Design the v2 JSON schema for duel ledger rows. The v1 row shape is the last "
                   "line below (fields: ask_id, a_model, b_model, a_cost, b_cost, judge, winner, "
                   "rubric, ts, mode, swap, judge_cost, criteria, rationale, a_chars, b_chars, "
                   "a_headers, b_headers). v2 must add: task_shape tag, rubric score deltas, "
                   "style covariates, blind flag, series id, and a CI block for the series. Give "
                   "the schema (draft 2020-12, required vs optional, types, enums), the migration "
                   "rule for v1 rows (never rewrite history), and three validation predicates a "
                   "pre-push gate would run.\n\n"
                   "<V1_ROW>\n" + ledger_v1 + "\n</V1_ROW>\n" + LAWS,
        },
        {
            "id": "x4-schema-hydrology-v2",
            "cat": "schema-design",
            "rubric": RUBRIC_SCHEMA,
            "ask": "Design the hydrology.v2 spec schema (to_spec/from_spec contract) for the "
                   "module below: what fields rung 2 features (rain schedule, evaporation, "
                   "depth-tint export) require, the version field rules, and the compatibility law "
                   "(a v1 spec must load under the v2 reader with default behavior unchanged). "
                   "Give the schema, one worked v2 spec example, and three validation predicates. "
                   "Integer determinism law governs every field.\n\n"
                   "<RUNG1_SOURCE>\n" + hydro + "\n</RUNG1_SOURCE>\n" + LAWS,
        },
        # ----------------------------------------------------------- grading
        {
            "id": "x4-grade-hydrology-vs-docstring",
            "cat": "grading",
            "rubric": RUBRIC_GRADE,
            "context": hydro,
            "ask": "Grade this module 0-5 per criterion against ITS OWN docstring claims. The "
                   "docstring promises: integer-only math, no floats/RNG/clocks, pools visibly "
                   "fill (head rises with volume), nothing flows uphill, siphons keep their law, "
                   "water_graph.py untouched, tick structure inherited. For each promise: KEPT, "
                   "BROKEN, or UNPROVEN, with the exact line or the test that would decide it. "
                   "End with the single highest-value missing test.\n\n"
                   "<SOURCE>\n" + hydro + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "x4-grade-harness-receipt-v11",
            "cat": "grading",
            "rubric": RUBRIC_GRADE,
            "context": v11,
            "ask": "Grade this receipt section (v1.1 judge blinding, from the W3 duel harness "
                   "receipt) as an AUDIT ARTIFACT: for each claim it makes (blind prompt, parity "
                   "slot swap, verdict remap, style-control header counts, 11 passing tests), is "
                   "it worded so a third party with repo access could re-verify it byte-level "
                   "today? Score each claim VERIFIABLE, VAGUE, or UNVERIFIABLE, name what a "
                   "verifier would run, and give the receipt an overall 0-5 audit-grade with the "
                   "one fix that most raises it.\n\n"
                   "<RECEIPT>\n" + v11 + "\n</RECEIPT>\n" + LAWS,
        },
    ]


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
    p = argparse.ArgumentParser(description="X4 duel series (coverage gap 5)")
    p.add_argument("--dry", action="store_true", help="print the plan, no calls, no writes")
    p.add_argument("--limit", type=int, default=0, help="run at most N duels this invocation")
    p.add_argument("--out", type=Path, default=dh.OUT_DEFAULT)
    args = p.parse_args(argv)

    asks = build_asks()
    done = banked_ask_ids(args.out)
    todo = [a for a in asks if a["id"] not in done]
    if args.limit:
        todo = todo[:args.limit]

    if args.dry:
        print(json.dumps({
            "series": "x4", "budget_cap": BUDGET_CAP,
            "projected_per_duel": PROJECTED_PER_DUEL,
            "asks": [{"id": a["id"], "cat": a["cat"], "rubric": a["rubric"],
                      "ask_chars": len(a["ask"]),
                      "banked": a["id"] in done} for a in asks],
            "to_run_now": [a["id"] for a in todo],
        }, indent=2))
        return 0

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2

    spent = 0.0
    rows: list[dict] = []
    for a in todo:
        if spent + PROJECTED_PER_DUEL > BUDGET_CAP:
            print(f"BUDGET HOLD: spent=${spent:.4f} + projected ${PROJECTED_PER_DUEL} "
                  f"would exceed cap ${BUDGET_CAP:.2f}; stopping before {a['id']}")
            break
        try:
            row = dh.run_duel(
                a["id"], a["ask"], A_MODEL, B_MODEL,
                rubric=[c.strip() for c in a["rubric"].split(",")],
                context=a.get("context"), out_path=args.out,
                keys=keys, mode="live",
            )
        except (RuntimeError, SystemExit) as e:
            print(f"DUEL FAILED {a['id']}: {e}; continuing to next ask")
            continue
        spent += row["a_cost"] + row["b_cost"] + row["judge_cost"]
        rows.append(row)
        if spent > BUDGET_CAP:
            print(f"BUDGET BLOWN at ${spent:.4f} after {a['id']}; halting series")
            break

    tally = {"A": 0, "B": 0, "TIE": 0, "UNPARSED": 0}
    for r in rows:
        tally[r["winner"]] = tally.get(r["winner"], 0) + 1
    summary = {
        "series": "x4-duel-series",
        "duels_run": len(rows),
        "a_model": A_MODEL, "b_model": B_MODEL,
        "tally": tally,
        "spent_this_run": round(spent, 4),
        "budget_cap": BUDGET_CAP,
        "per_duel": [{ "ask_id": r["ask_id"], "winner": r["winner"],
                       "cost": round(r["a_cost"] + r["b_cost"] + r["judge_cost"], 4),
                       "a_chars": r["a_chars"], "b_chars": r["b_chars"],
                       "a_headers": r["a_headers"], "b_headers": r["b_headers"],
                       "swap": r["swap"], "rationale": r["rationale"]} for r in rows],
    }
    print("X4 SUMMARY " + json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
