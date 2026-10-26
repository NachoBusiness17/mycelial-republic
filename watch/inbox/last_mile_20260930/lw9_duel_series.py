"""LW9 duel series - the n=30 closeout installment (Z2 next step 1, last mile).

Z2 (watch/inbox/hydrology/Z2_DUEL_N30.md next steps) says: one more window,
~9 fresh asks (~$1.0) reaches n=30. This driver is that window: 9 more live
blind duels, qwen/qwen3.8-max-prime (logical A) vs z-ai/glm-5.3-prime
(logical B), ember judge, rows appended to logs/duel/duels.jsonl by
tools/duel_harness.py run_duel (v1.1: anonymized judge, parity-alternated
slot swap, style-control header counts). Blind-era tally enters at n=21
(glm 12, qwen 8, TIE 1; ledger 22 rows, unblinded row 0 excluded) and
exits at n=30 of the n=30 target.

OWED DEBT (noted here, operator law 2026-09-28 DRIVING LADDER): glm-side
answers should come from this account's Task agents when possible. The
harness is API-shaped (Nous inference API both halves) and the qwen side
needs Nous regardless, so pragmatic v0 fires BOTH halves through Nous;
the glm half riding Nous is ~$0.04/duel of pennies waste. The real fix is
a harness refactor to a pluggable contender-source interface; owed in the
LW9 receipt, not papered over here.

Ask mix per the S5 protocol, fresh task shapes and fresh artifacts so the
pair verdict is not overfit to the X4/Z2 ask banks: 2 adversarial-review
(violation ratchet, shared surface contract), 2 planning (duel harness
contender-source refactor, warm boot resilience), 2 schema-design
(warm_state.json v2, duels.jsonl row v3), 1 grading (freshness_check vs
its own docstring), 2 code-analysis (hermes_warm_boot failure modes,
mag/shared_surface.py defect hunt). Every ask is grounded in a real repo
artifact read at runtime (byte-true).

Laws honored here (same as X4/Z2):
  - BUDGET_CAP $1.50 ABSOLUTE for THIS series (operator): no duel fires
    unless spent + worst-case projection for one duel still fits.
  - Idempotent: ask_ids already in logs/duel/duels.jsonl are skipped, so
    a killed run resumes without double spend.
  - Width 1: duels run strictly sequential (stagger law; no 1302 storms).
  - No em-dashes in anything this file writes.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/lw9_duel_series.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/lw9_duel_series.py [--limit N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import duel_harness as dh  # noqa: E402

BUDGET_CAP = 1.50          # ABSOLUTE cap for THIS series (operator)
PROJECTED_PER_DUEL = 0.16  # worst-case projection charged before each fire
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
    ratchet = read(r"tools\violation_ratchet.py", 12000)
    contract = read(r"watch\inbox\SHARED_SURFACE_CONTRACT.json", 3800)
    surface = read(r"mag\shared_surface.py", 12000)
    rib = read(r"memory\rib\RIB_DRIVING_LADDER_20260928.md", 4200)
    harness = read(r"tools\duel_harness.py", 12000)
    warmboot = read(r"mag\hermes_warm_boot.py", 4100)
    warmstate = read(r"memory\warm_state.json", 900)
    freshness = read(r"tools\freshness_check.py", 12000)
    ledger_v1 = last_ledger_row()

    ag_clause = (
        "AGENTS.md warm boot clause (byte-true): 'Warm boot: run "
        "python -m mag.hermes_warm_boot at session start to load chain tip "
        "+ Vercel URLs + session brief into memory/warm_state.json. Vercel "
        "URLs may return 302 SSO redirects - verify with curl -I before "
        "reporting live.'"
    )

    return [
        # ------------------------------------------------ adversarial-review
        {
            "id": "lw9-adv-ratchet",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": ratchet,
            "ask": "You are an adversarial reviewer. Kill or keep each mechanism of this "
                   "pre-push violation ratchet (baseline registry keyed by debt name, "
                   "changed-only scope, prune recovery, baseline-update --by attribution, "
                   "the check exit contract). Name the three cheapest ways NEW debt slips "
                   "past it (file renames, moved code, branch-shape games, baseline "
                   "stalemate) and the measurement that would close each. What happens "
                   "the day the baseline file is edited by hand?\n\n"
                   "<SOURCE>\n" + ratchet + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "lw9-adv-shared-surface",
            "cat": "adversarial-review",
            "rubric": RUBRIC_ADV,
            "context": surface,
            "ask": "You are an adversarial reviewer of this machine contract plus its "
                   "validator. Kill or keep each rule (hash preservation, bounded "
                   "pointers, receipt before promotion, classify before reuse, "
                   "switchboard-only effects). Name the three weakest guarantees the "
                   "validate command actually enforces versus what the contract prose "
                   "implies, and the falsifying input for each gap. Who can silently "
                   "become the sole copy of durable work under this contract as "
                   "implemented?\n\n"
                   "<CONTRACT>\n" + contract + "\n</CONTRACT>\n\n"
                   "<VALIDATOR_SOURCE>\n" + surface + "\n</VALIDATOR_SOURCE>\n" + LAWS,
        },
        # ---------------------------------------------------------- planning
        {
            "id": "lw9-plan-harness-refactor",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan the owed refactor of this duel harness so the glm-side "
                   "contender can be sourced from a local Task agent instead of the "
                   "Nous API, per the operator driving-ladder rib below (only Hermes "
                   "is funded; glm answers should come from this account's own Task "
                   "agents when possible; the qwen side and the judge still need "
                   "Nous). Deliver: the contender-source interface (function shape, "
                   "timeout, empty-content handling), what must NOT change (blind "
                   "judging, slot swap parity, ledger row shape, no model rotation), "
                   "the test predicate proving a mixed-source duel is byte-comparable "
                   "to an all-API duel, and the sequencing against the metering "
                   "(Task-agent answers have no usage.cost). Failure modes with the "
                   "control for each.\n\n"
                   "<RIB>\n" + rib + "\n</RIB>\n\n"
                   "<HARNESS_SOURCE>\n" + harness + "\n</HARNESS_SOURCE>\n" + LAWS,
        },
        {
            "id": "lw9-plan-warm-boot-resilience",
            "cat": "planning",
            "rubric": RUBRIC_PLAN,
            "ask": "Plan making this warm boot resilient, grounded in the clause and "
                   "source below. The clause admits Vercel URLs may return 302 SSO "
                   "redirects and must be verified with curl -I before reporting "
                   "live; the operator still wants session start to be one command. "
                   "Deliver: the first concrete change, what warm_state.json must "
                   "record when a fetch 302s or times out (stale markers, fetched_at, "
                   "per-field provenance), the rule for when stale state is better "
                   "than no state, the test predicates, and what must NOT change "
                   "(single command, no new daemon, chain tip still loaded). Failure "
                   "modes with the control for each.\n\n"
                   "<CLAUSE>\n" + ag_clause + "\n</CLAUSE>\n\n"
                   "<SOURCE>\n" + warmboot + "\n</SOURCE>\n" + LAWS,
        },
        # ------------------------------------------------------ schema-design
        {
            "id": "lw9-schema-warm-state",
            "cat": "schema-design",
            "rubric": RUBRIC_SCHEMA,
            "ask": "Design the warm_state.json v2 schema for this warm boot: per-field "
                   "provenance (which fetch produced each value), fetched_at "
                   "timestamps, a staleness contract (how old before a field is "
                   "marked STALE and who enforces it), and the compatibility law (a "
                   "v1 reader must still load v2 with behavior unchanged for v1 "
                   "fields). Give the schema (draft 2020-12, required vs optional, "
                   "types), one worked v2 example document, the migration rule for "
                   "the existing v1 file, and three validation predicates a gate "
                   "would run. Current v1 state and writer source below.\n\n"
                   "<V1_STATE>\n" + warmstate + "\n</V1_STATE>\n\n"
                   "<WRITER_SOURCE>\n" + warmboot + "\n</WRITER_SOURCE>\n" + LAWS,
        },
        {
            "id": "lw9-schema-duel-row-v3",
            "cat": "schema-design",
            "rubric": RUBRIC_SCHEMA,
            "ask": "Design the duels.jsonl row v3 schema extending the v1 row below: "
                   "judge provenance fields (judge model, judge_cost already exist; "
                   "add alternate-judge rejudge linkage), position-bias audit fields "
                   "(slot_winner, slot_chars both sides), and a series field for "
                   "ask-bank 70/30 split bookkeeping. Required behavior: a rejudge "
                   "row can never overwrite the original verdict, joins are by "
                   "ask_id plus judge fingerprint, old rows stay loadable. Give the "
                   "schema, one worked v3 example, the migration rule (append-only, "
                   "never rewrite banked rows), and three validation predicates. The "
                   "v1 row shape and the harness that writes it are below.\n\n"
                   "<V1_ROW>\n" + ledger_v1 + "\n</V1_ROW>\n\n"
                   "<HARNESS_SOURCE>\n" + harness + "\n</HARNESS_SOURCE>\n" + LAWS,
        },
        # ----------------------------------------------------------- grading
        {
            "id": "lw9-grade-freshness",
            "cat": "grading",
            "rubric": RUBRIC_GRADE,
            "context": freshness,
            "ask": "Grade this freshness checker 0-5 per criterion against ITS OWN "
                   "docstring promises. The promises: BOOT_4_7.md and state/ boot "
                   "docs go STALE at more than 7 days while the repo has a "
                   "heartbeat, refresh means today's truth or register frozen with "
                   "reason plus date, and the check exits nonzero on stale. For "
                   "each promise: KEPT, BROKEN, or UNPROVEN, with the exact "
                   "function or the test that would decide it. End with the single "
                   "highest-value missing test.\n\n"
                   "<SOURCE>\n" + freshness + "\n</SOURCE>\n" + LAWS,
        },
        # ------------------------------------------------------ code-analysis
        {
            "id": "lw9-code-warm-boot",
            "cat": "code-analysis",
            "rubric": RUBRIC_CODE,
            "context": warmboot,
            "ask": "Analyze the failure modes of this warm boot script. For each of: "
                   "a Vercel URL answering 302 SSO, the chain-tip endpoint being "
                   "down, warm_state.json existing but half-written from a killed "
                   "prior run, and clock skew on the host, state what the code does, "
                   "what silently goes wrong, and the falsifying predicate. Name the "
                   "three defects that matter ranked by damage to the session brief "
                   "an agent trusts at boot, each with the minimal fix. Mark "
                   "anything you cannot verify from the source alone UNPROVEN.\n\n"
                   "<SOURCE>\n" + warmboot + "\n</SOURCE>\n" + LAWS,
        },
        {
            "id": "lw9-code-shared-surface",
            "cat": "code-analysis",
            "rubric": RUBRIC_CODE,
            "context": surface,
            "ask": "Find the three highest-severity real defects in this shared "
                   "surface validator, ranked by damage to the durable-write "
                   "guarantee (not style, not hypothetical). For each: the exact "
                   "function and line of code, why it lets a session become the "
                   "sole copy of durable work or a bad promotion pass validation, a "
                   "falsifying predicate (the concrete input or sequence that "
                   "exposes it), and the minimal fix. Candidates you must confirm "
                   "or eliminate from the source itself: hash verification skipping "
                   "absent files, pointer bound checks, receipt ordering, exit code "
                   "contract on partial failures. Mark anything unverifiable from "
                   "source alone UNPROVEN.\n\n"
                   "<SOURCE>\n" + surface + "\n</SOURCE>\n" + LAWS,
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
    p = argparse.ArgumentParser(description="LW9 duel series (n=30 closeout)")
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
            "series": "lw9", "budget_cap": BUDGET_CAP,
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
        "series": "lw9-duel-series",
        "duels_run": len(rows),
        "a_model": A_MODEL, "b_model": B_MODEL,
        "tally": tally,
        "spent_this_run": round(spent, 4),
        "budget_cap": BUDGET_CAP,
        "per_duel": [{"ask_id": r["ask_id"], "winner": r["winner"],
                      "cost": round(r["a_cost"] + r["b_cost"] + r["judge_cost"], 4),
                      "a_chars": r["a_chars"], "b_chars": r["b_chars"],
                      "a_headers": r["a_headers"], "b_headers": r["b_headers"],
                      "swap": r["swap"], "rationale": r["rationale"]} for r in rows],
    }
    print("LW9 SUMMARY " + json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
