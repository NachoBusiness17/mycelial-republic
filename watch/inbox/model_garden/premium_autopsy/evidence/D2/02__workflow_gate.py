#!/usr/bin/env python3
"""Workflow gate: fleet dogfood enforcement for dynamic-workflow scripts.

Born 2026-09-25 by operator order: "we need to stop pinging me for workflows,
we need to have a gate that makes sure workflows are being improved, enhanced,
dogfooded, and using our systems like Mickey17 gophers, interagent communication
and steering. Self steal."

The gate runs BEFORE CreateWorkflow submission. It self-steals the ratchet
pattern (exit 2 is the only hard block; every submission registers a row so
improvement is a ledger fact, amend-not-rewrite is visible in digests).

Checks enforced on every script:
  G1 multiplicity   Mickey17 gopher fan-out: per-item named actors in a fan-out
  G2 passoff        interagent communication: an earlier actor's output feeds a later ask
  G3 steering       a reviewer/reader verdict is carried back into a revision ask
  G4 salvage        report() fires inside the fan-out so work survives a dead run
  G5 deliverable    published artifact (markdown/file) plus report-shape return
  G6 receipts       durable receipt lands in watch/inbox, dated (missing date = soft WARN)
  G7 laws           no-fabrication and em-dash law carried inside the asks

Scenario mode (LAW-12 genesis clause, 2026-09-26): the clause in
watch/inbox/BURN_rsi-harness_20260926.md requires one scenario card per
gate G1-G7, each minted from a real memory/workflows/REGISTRY.jsonl FAIL
row, so every future gate change re-proves itself against observed
failures instead of prose. `check --scenarios configs/workflow_gate_scenarios`
validates the card suite READ-ONLY: cards must cite a registry FAIL row
that actually shows their gate failing, each fixture must produce exactly
the card's expected verdict/warns/exit, and the all-pass control must
pass clean. No registry row is written and no file is modified in
scenario mode.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import sys

REGISTRY = os.path.join("memory", "workflows", "REGISTRY.jsonl")
SCENARIO_DIR_DEFAULT = os.path.join("configs", "workflow_gate_scenarios")

CHECKS = [
    ("G1-multiplicity",
     "Mickey17 gopher fan-out: per-item named actors (agent(\"x-\" + item) inside a fan-out)",
     lambda t: bool(re.search(r'agent\(\s*"[^"]*"\s*\+', t)) or bool(re.search(r'agent\(`[^`]*\+', t)),
    ),
    ("G2-passoff",
     "interagent communication: an earlier actor's output (text/json/path) feeds a later ask",
     lambda t: bool(re.search(r'JSON\.stringify\(\s*\w+\)', t))
     or bool(re.search(r'\+\s*\w+\.(text|issues|stdout|path|quotes)\b', t)),
    ),
    ("G3-steering",
     "steering: reviewer/reader feedback carried back into a revision ask",
     lambda t: ("reported these issues" in t)
     or ("cold reader reported" in t)
     or bool(re.search(r'Previous critique', t))
     or bool(re.search(r'\.(issues|feedback|comments|critique)\b[^\n]{0,200}ask<', t, re.S)),
    ),
    ("G4-salvage",
     "incremental report() inside the fan-out (work survives a dead run)",
     lambda t: bool(re.search(r'report\(\s*\w+\s*\)\s*;', t)),
    ),
    ("G5-deliverable",
     "published deliverable (artifact.markdown/file) plus report-shape return (conclusion:)",
     lambda t: ("artifact.markdown(" in t or "artifact.file(" in t) and ("conclusion:" in t),
    ),
    # SPEC t69 (wired from t62 next_steal): a receipt-path mention must also carry a dated stamp (t62 prefilter family, label + YYYY-MM-DD); a missing stamp is a soft-false WARN row with a reason, never a new hard-block exit (0/1/2 contract unchanged).
    ("G6-receipts",
     "durable receipt landing in watch/inbox with a dated stamp",
     lambda t: ("watch/inbox" in t) or ("watch\\inbox" in t),
    ),
    ("G7-laws",
     "no-fabrication and em-dash law carried inside the asks",
     lambda t: ("no em-dashes" in t)
     and ("never fabricate" in t or "no-fabrication" in t or "never synthesize" in t),
    ),
]

# t69: dated-stamp requirement behind G6, same regex family as the
# githooks/pre-push freshness prefilter (t62): label set + colon + YYYY-MM-DD,
# case-insensitive like freshness_gate.STAMP_RE. A receipt mention without a
# matching line is a soft finding, not a gate failure.
G6_STAMP_RE = re.compile(
    r"(?i)\b(source[-_ ]fetched|fetched|observed[-_]at)\s*:\s*\d{4}-\d{2}-\d{2}"
)


G6_SOFT_REASON = (
    "receipt mention lacks a dated stamp (label + YYYY-MM-DD, t62 prefilter family);"
    " soft-warn, not a hard block"
)

# B2-206 (2026-09-26): judge-independence marker behind G3, same soft-warn
# family as G6. The dwf facade gives subagents the session model only ("no
# per-subagent model choice", dynamic-workflows skill), so independence is a
# FIRING contract, not a script line: a workflow with a fresh-reader judge
# seat must declare the cross-family model the operator fires it with
# (CreateWorkflow/AmendWorkflow subagent_model), as a `judge-model:` stamp.
# G3 steering present but no stamp => soft-warn naming the B2-60 D2 finding;
# exit contract untouched. Falsifier from B2-60: one cross-family reviewer
# fold vs the same-model baseline.
G3_JUDGE_MODEL_RE = re.compile(
    r"(?i)\b(judge[-_ ]?model|subagent[_ ]?model)\s*:\s*[a-z0-9][a-z0-9._/-]+"
)

G3_SOFT_REASON = (
    "judge independence undeclared: the fresh-reader seat runs same-session-model"
    " (B2-60 D2, context freshness is not weight independence); declare"
    " 'judge-model: <provider/model>' naming the cross-family subagent_model to"
    " fire with; soft-warn, not a hard block"
)


def run_checks(text: str) -> list:
    """Run the seven gate checks over script text (shared by check paths)."""
    rows = []
    for cid, desc, fn in CHECKS:
        ok = bool(fn(text))
        row = {"id": cid, "ok": ok, "desc": desc}
        # t69: G6 soft-false. Receipt mention present but no dated stamp:
        # mark the row not-ok with a reason, keep it out of the failed set,
        # so the verdict and the 0/1/2 exit contract are untouched.
        if cid == "G6-receipts" and ok and not G6_STAMP_RE.search(text):
            row["ok"] = False
            row["soft"] = True
            row["reason"] = G6_SOFT_REASON
        # B2-206: G3 soft-false. Steering present but no judge-model stamp:
        # the reviewer certifies steering, not weight independence.
        if cid == "G3-steering" and ok and not G3_JUDGE_MODEL_RE.search(text):
            row["ok"] = False
            row["soft"] = True
            row["reason"] = G3_SOFT_REASON
        rows.append(row)
    return rows


def split_rows(rows: list) -> tuple:
    """Return (failed_ids, warned_ids) from run_checks rows."""
    failed = [r["id"] for r in rows if not r["ok"] and not r.get("soft")]
    warned = [r["id"] for r in rows if r.get("soft")]
    return failed, warned


def load_registry_index() -> dict:
    """Index registry rows by (ts, digest); tolerant of malformed lines."""
    index = {}
    if not os.path.exists(REGISTRY):
        return index
    with open(REGISTRY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            index[(row.get("ts"), row.get("digest"))] = row
    return index


def validate_card(card, label: str, known_ids: set, registry_index: dict) -> str:
    """Structural + citation validation. Returns an error string or ""."""
    required = [
        "gate_id", "cited_fail_row", "scenario_input",
        "expected_verdict", "regression_criterion", "rollback_note",
    ]
    for key in required:
        if key not in card:
            return f"missing required field '{key}'"
    gate_id = card["gate_id"]
    if gate_id not in known_ids:
        return f"unknown gate_id '{gate_id}'"
    cited = card["cited_fail_row"
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 14772 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
(card_paths)} cards red (read-only run, no registry row)")
        return 2
    print(f"SCENARIOS: {len(card_paths)} cards validated read-only (no registry row written)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Fleet workflow dogfood gate")
    ap.add_argument("cmd", choices=["check"], help="check a workflow script against the gate")
    ap.add_argument("--script", default=None, help="path to the .dwf.ts workflow script")
    ap.add_argument("--scenarios", default=None, metavar="DIR",
                    help="validate the scenario card suite under DIR, read-only")
    ap.add_argument("--name", default=None, help="run label for the registry row")
    ap.add_argument("--no-register", action="store_true",
                    help="skip the registry append (for hook payload checks: "
                         "a pre-write gate of in-flight content must not mint "
                         "rows pointing at temp files that die immediately - "
                         "seat_law_gate cause, 2026-09-29)")
    args = ap.parse_args()

    if args.scenarios:
        return run_scenarios(args.scenarios)
    if not args.script:
        ap.error("check requires --script PATH or --scenarios DIR")

    try:
        with open(args.script, encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        print(f"GATE ERROR: cannot read script: {exc}")
        return 1

    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    rows = run_checks(text)
    failed, _ = split_rows(rows)

    verdict = "PASS" if not failed else "FAIL"
    print(f"workflow_gate {verdict} digest={digest} script={args.script}")
    for r in rows:
        if r.get("soft"):
            print("  WARN  " + f"{r['id']}: {r['desc']} [{r['reason']}]")
        else:
            print(("  ok    " if r["ok"] else "  FAIL  ") + f"{r['id']}: {r['desc']}")

    if args.no_register:
        return 2 if failed else 0

    row = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "name": args.name or os.path.basename(args.script),
        "digest": digest,
        "script": args.script,
        "verdict": verdict,
        "checks": rows,
    }
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    with open(REGISTRY, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    if failed:
        print("GATE: fix the FAIL items by editing the script file in place (amend-not-rewrite), then re-check.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
