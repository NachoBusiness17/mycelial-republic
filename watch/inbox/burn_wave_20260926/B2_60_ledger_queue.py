#!/usr/bin/env python3
"""B2-60: append LEDGER row (json.dumps, append-only) + QUEUE self-feed briefs.

v2: LEDGER row landed in v1 run at 2026-09-26T13:35:30Z (idempotent skip now);
QUEUE briefs renumbered dynamically after concurrent lanes claimed B2-190..204.
"""
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"
QUEUE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

# ---- LEDGER: append once ----------------------------------------------------
row = {
    "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-60-judge-independence",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_60_judge_independence_20260926.md",
    "one_line": (
        "judge-independence sweep under the VisualPrompter Appendix L same-VLM lens: "
        "REGISTRY.jsonl clean (19 rows, all regex gate output) and 8 rule-judge paths "
        "tolerated (lane_runner gate_drop, workflow_gate, steer_compare, ghost_tournament, "
        "arena_bench, run_worth, conductor_eval, wandr stub judge); 3 same-VLM DEFECTS named "
        "with file:line and fixes: quorum p4 author self-vote counts toward its own 2/3 bar "
        "(mag/quorum_window.py:377,398-405), all four .zcode/workflows scripts judge with "
        "same-session-model reviewer agents (zero subagent_model; the-gala.dwf.ts:295-296) "
        "while REGISTRY G3 ok rows certify steering presence not independence, and ghost's "
        "constitutional filter hardcodes the critic and never records the producer "
        "(mag/ghost.py:1970, mag/constitutional_critique.py:196-200); 2 tolerated with "
        "conditions (compaction_eval GEN==JUDGE misnomer, wandr LLM-judge swap clause); "
        "falsifiers pre-registered per defect"
    ),
}

ledger_text = LEDGER.read_text(encoding="utf-8")
if '"B2-60-judge-independence"' in ledger_text and row["ts"] == "2026-09-26T13:35:30Z":
    print("ledger row already present (13:35:30Z), skipping append")
else:
    with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("ledger row appended:", row["ts"], row["slug"])

# ---- QUEUE: dynamic renumber against live concurrent claims -----------------
text = QUEUE.read_text(encoding="utf-8")
used = set(int(m) for m in re.findall(r"B2-(\d+)", text))
n1, n2, n3 = 205, 206, 207
while n1 in used:
    n1 += 1
while n2 in used or n2 <= n1:
    n2 += 1
while n3 in used or n3 <= n2:
    n3 += 1

receipt = "watch/inbox/burn_wave_20260926/B2_60_judge_independence_20260926.md"
briefs = [
    f"- [ ] B2-{n1} Quorum p4 self-vote exclusion: the author chair votes toward the 2/3 bar on "
    f"its own addition (mag/quorum_window.py:377 for chair in p1s, :398-399 denom/need, "
    f":404-405 tallies) while the p3 fold already carries the author chair; implement the "
    f"per-addition eligible set excluding the author (author vote = ABSTAIN) and pre-register "
    f"the falsifier recount of memory/runs/salons/quorum_* VERDICT.md for pivotal self-votes; "
    f"lens {receipt} D1.",
    f"- [ ] B2-{n2} Workflow judge-seat independence: zero subagent_model across "
    f".zcode/workflows/*.ts, so the fresh-reader reviewers judge same-model output "
    f"(the-gala.dwf.ts:295-296, mickey17-v2.dwf.ts:328-329, the-50.dwf.ts:181) and REGISTRY G3 "
    f"ok rows certify steering presence, not independence; give judge agents a cross-provider "
    f"subagent_model and extend tools/workflow_gate.py G3 (:55-59) with a judge-independence "
    f"marker; falsifier = one cross-family reviewer fold vs the same-model baseline "
    f"({receipt} D2 F2).",
    f"- [ ] B2-{n3} Constitutional filter producer record: mag/ghost.py:1970 "
    f"filter_response(output, model=\"deepseek\") hardcodes the critic while the producer model "
    f"is a variable (ghost.py:1125) and CritiqueResult records only model_used "
    f"(mag/constitutional_critique.py:196-200); thread producer_model into CritiqueResult and on "
    f"family match fall back to local heuristics marked same-family-refused; falsifier = 30 days "
    f"of producer logs with zero same-family events closes it ({receipt} D3 F3).",
]

fresh = QUEUE.read_text(encoding="utf-8")
fresh_used = set(int(m) for m in re.findall(r"B2-(\d+)", fresh))
for n in (n1, n2, n3):
    assert n not in fresh_used, f"B2-{n} claimed concurrently"
with QUEUE.open("a", encoding="utf-8", newline="\n") as f:
    f.write("\n" + "\n".join(briefs) + "\n")
print(f"queue briefs appended: B2-{n1}, B2-{n2}, B2-{n3}")
