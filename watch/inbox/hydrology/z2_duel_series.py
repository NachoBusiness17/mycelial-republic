"""Z2 duel series - the n=21 installment (gap 5 continuation, X4 next step 1).

X4 (watch/inbox/hydrology/X4_DUEL_SERIES.md) landed 10 blind duels and the
receipt's next step is "~10 fresh asks per next window, roughly $1.0 per
window". This driver is that window: 10 more live blind duels,
qwen/qwen3.8-max-prime (A) vs z-ai/glm-5.3-prime (B), ember judge, rows
appended to logs/duel/duels.jsonl by tools/duel_harness.py run_duel
(v1.1: anonymized judge, parity-alternated slot swap, style-control
header counts). Blind-era tally enters at n=11 (glm 7, qwen 3, TIE 1)
and exits this series at n=21 of the n=30 target.

Ask mix per the S5 protocol, fresh task shapes and fresh artifacts so
the pair verdict is not overfit to the X4 ask bank: 3 adversarial-review
(census patrol, workflow gate, DNA doc), 2 planning (chan steer wiring,
n=30 closeout), 2 schema-design (ask-bank manifest, chan.v2), 1 grading
(patrol vs its own docstring), 2 code-analysis (duel harness defects,
FTS rebuild failure modes). Code-analysis is a new shape this series
(defect-finding over source, not review of a design doc). Every ask is
grounded in a real repo artifact read at runtime (byte-true).

Laws honored here (same as X4):
  - BUDGET_CAP $2.50 ABSOLUTE for THIS series (operator): no duel fires
    unless spent + worst-case projection for one duel still fits.
  - Idempotent: ask_ids already in logs/duel/duels.jsonl are skipped, so
    a killed run resumes without double spend.
  - Width 1: duels run strictly sequential (stagger law; no 1302 storms).
  - No em-dashes in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/hydrology/z2_duel_series.py --dry
    .venv/Scripts/python.exe watch/inbox/hydrology/z2_duel_series.py [--limit N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

BUDGET_CAP = 2.50          # ABSOLUTE cap for THIS series (operator)
PROJECTED_PER_DUEL = 0.25  # worst-case projection charged before each fire
A_MODEL = "qwen/qwen3.8-max-prime"     # logical A throughout the series
B_MODEL = "z-ai/glm-5.3-prime"         # logical B throughout the series

RUBRIC_ADV = "section coverage, defect severity, evidence citations, actionability"
RUBRIC_PLAN = "failure mode coverage, sequencing correctness, evidence citations, actionability"
RUBRIC_SCHEMA = "normality and edge coverage, type correctness, migration safety, evidence citations"
RUBRIC_GRADE = "calibration to the artifact, evidence citations, verdict consistency, actionability"
RUBRIC_CODE = "root cause accuracy, evidence citations, severity ranking, actionability"

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
    patrol = read(r"tools\census_drift_patrol.py", 12000)
    gate = read(r"tools\workflow_gate.py", 12000)
    dna = read(r"docs\DNA.md", 6300)
    gaps = read(r"watch\inbox\COVERAGE_GAPS_20260930.md", 5000)
    chan = read(r"mag\chan.py", 12000)
    x4 = read(r"watch\inbox\hydrology\X4_DUEL_SERIES.md", 7000)
    x4_next = x4[x4.find("## Next steps"):] if "## Next steps" in x4 else x4
    harness = read(r"tools\duel_harness.py", 12000)
    fts = read(r"tools\corpus_fts_rebuild.py", 7200)
    ledger_v1 = last_ledger_row()

    return [
        # ------------------------------------------------ adversarial-review
        {
            "id": "z2-adv-census-patrol",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": patrol,
            "ask": "You are an adversarial reviewer. Kill or keep each mechanism of this "
                   "tripwire tool (two-way byte growth measure, carrier-shape grammar "
                   "parse with fail-close exit 2, WARN-only pre-push default, --collect "
                   "deep check with its 20-off tolerance, the daily scheduled task). "
                   "Name the three weakest assumptions the tool makes about the carrier "
                   "bullet and the file tree, and the test or measurement that would "
                   "replace each. What breaks the day a second Tests bullet appears in "
                   "AGENTS.md or the parenthesized census clause is reworded?\n\n"
                   "<SOURCE>\n" + patrol + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "z2-adv-workflow-gate",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": gate,
            "ask": "You are an adversarial reviewer of this submission gate. Kill or keep "
                   "each check (gopher fan-out with named actors, interagent pass-off, "
                   "steering, incremental report salvage, receipt landing, registry rows, "
                   "scenario suite). For each kept check name its cheapest bypass: the "
                   "script shape an LLM author could write that passes the letter of the "
                   "check while defeating its intent. Name what the REGISTRY.jsonl ledger "
                   "structurally cannot see. Three falsifying test predicates total.\n\n"
                   "<SOURCE>\n" + gate + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "z2-adv-dna",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": dna,
            "ask": "You are an adversarial reviewer of this constitution-style document. "
                   "Kill or keep each section: which claims are aspirations wearing "
                   "measurement clothes, which terms are defined nowhere (residual, "
                   "registry, knot, chain, coldest vertex), which daily-path pointers are "
                   "stale-trap candidates (targets that rot faster than the doc). Name "
                   "the three claims most likely to mislead a new agent seat and the "
                   "verifiable statement each should become.\n\n"
                   "<SOURCE>\n" + dna + "\n</SOURCE>\n" + LAWS,
        },
        # ---------------------------------------------------------- planning
        {
            "id": "z2-plan-chan-steer",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan wiring this chan room engine into steer readers per the gap table "
                   "below. Deliver: the first concrete action, the test predicate that "
                   "proves closure, the risk the gap reopens, and the order of work "
                   "against the other gaps in the table. State what must NOT change "
                   "(engine owns posts, watch/room.jsonl is the one surface, SCHEMA "
                   "chan.v1 rows stay loadable, HIDE_EVENTS sludge filtering stays).\n\n"
                   "<GAPS>\n" + gaps + "\n</GAPS>\n\n"
                   "<CHAN_SOURCE>\n" + chan + "\n</CHAN_SOURCE>\n" + LAWS,
        },
        {
            "id": "z2-plan-n30-closeout",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan the n=30 closeout of the duel series per the operator next-steps "
                   "clause below. Deliver: the exact method to compute a simultaneous "
                   "confidence interval on the three-way (A wins, B wins, TIE) tally "
                   "(name the statistical procedure and why binomial alone is wrong once "
                   "ties exist), the alternate-judge retro sensitivity check design over "
                   "already-banked answers, the 70/30 ask-bank split rules including who "
                   "holds the hidden 30 and how leakage is prevented, and the rule for "
                   "when the router row may be rewritten. Failure modes with the control "
                   "for each.\n\n"
                   "<NEXT_STEPS>\n" + x4_next + "\n</NEXT_STEPS>\n" + LAWS,
        },
        # ------------------------------------------------------ schema-design
        {
            "id": "z2-schema-askbank",
            "cat": "schema-design",
            "rubric": RUBRIC_SCHEMA,
            "ask": "Design the JSON schema for the duel ask-bank manifest (the 70/30 hidden "
                   "split artifact). Required behavior: entries carry id, task_shape, "
                   "rubric, ask body, hidden flag, holder, series, created, used_at; "
                   "task_shape is an enum; a used ask can never be re-fired silently. "
                   "Give the schema (draft 2020-12, required vs optional, types, enums), "
                   "the migration rule for the existing ledger (join by ask_id, never "
                   "rewrite banked rows), and three validation predicates a pre-push gate "
                   "would run. The v1 ledger row shape for the join is the last line "
                   "below.\n\n"
                   "<V1_ROW>\n" + ledger_v1 + "\n</V1_ROW>\n" + LAWS,
        },
        {
            "id": "z2-schema-chan-v2",
            "cat": "schema-design",
            "rubric": RUBRIC_SCHEMA,
            "ask": "Design the chan.v2 schema for this room engine's steer-reader wiring: "
                   "what fields a steer subscription needs (which file to watch, event "
                   "filter, post shape, provenance of the reader), the SCHEMA version "
                   "field rules, and the compatibility law (a chan.v1 room.jsonl must "
                   "load under the v2 reader with behavior unchanged). Give the schema, "
                   "one worked v2 example document, and three validation predicates. "
                   "The v1 engine source is below.\n\n"
                   "<CHAN_SOURCE>\n" + chan + "\n</CHAN_SOURCE>\n" + LAWS,
        },
        # ----------------------------------------------------------- grading
        {
            "id": "z2-grade-patrol-vs-docstring",
            "cat": "grading",
            "rubric": RUBRIC_GRADE,
            "context": patrol,
            "ask": "Grade this tool 0-5 per criterion against ITS OWN docstring promises. "
                   "The docstring promises: stale detection when the census date is "
                   "older than CENSUS_STALE_DAYS AND tests/ grew, growth measured from "
                   "bytes two ways, carrier-shape grammar that fail-closes exit 2 when "
                   "the claim shape is broken, a --collect deep check that reruns "
                   "pytest --collect-only and fails at 20 or more off, and a daily "
                   "scheduled task. For each promise: KEPT, BROKEN, or UNPROVEN, with "
                   "the exact function or the test that would decide it. End with the "
                   "single highest-value missing test.\n\n"
                   "<SOURCE>\n" + patrol + "\n</SOURCE>\n" + LAWS,
        },
        # ------------------------------------------------------ code-analysis
        {
            "id": "z2-code-duel-harness-defects",
            "cat": "code-analysis",
            "rubric": RUBRIC_CODE,
            "context": harness,
            "ask": "Find the three highest-severity real defects in this duel harness "
                   "source, ranked by damage to verdict validity (not style, not "
                   "hypothetical). For each: the exact function and line of code, why "
                   "it corrupts or biases a banked verdict or its metering, a "
                   "falsifying predicate (the concrete input or sequence that exposes "
                   "it), and the minimal fix. Candidates you must confirm or eliminate "
                   "from the source itself: key selection via hash of a string tag, "
                   "asymmetric truncation of answers shown to the judge, retry "
                   "semantics after both attempts fail, cost fallback when usage.cost "
                   "is absent. Mark anything you cannot verify from the source alone "
                   "UNPROVEN.\n\n"
                   "<SOURCE>\n" + harness + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "z2-code-fts-rebuild-modes",
            "cat": "code-analysis",
            "rubric": RUBRIC_CODE,
            "context": fts,
            "ask": "Analyze the failure modes of this one-sanctioned-writer FTS rebuild "
                   "tool. For each of: catalog.jsonl moving mid-build, the meta-table "
                   "freshness contract (catalog_bytes and friends), the deep sha256 "
                   "check, a second writer running concurrently, and the exit code "
                   "contract the daily task depends on (which exits mean rebuild, "
                   "incident, or dark surface), state what the tool does, what silently "
                   "goes wrong, and the falsifying predicate. Name the three defects "
                   "that matter ranked by reader impact, each with the minimal fix.\n\n"
                   "<SOURCE>\n" + fts + "\n</SOURCE>\n" + LAWS,
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
    p = argparse.ArgumentParser(description="Z2 duel series (gap 5, n=21 installment)")
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
            "series": "z2", "budget_cap": BUDGET_CAP,
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
        "series": "z2-duel-series",
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
    print("Z2 SUMMARY " + json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
