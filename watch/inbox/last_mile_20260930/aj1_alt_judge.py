"""AJ1 - alternate-judge replay of 10 banked W8 duel pairs (2026-09-30).

Mission (operator, W8 follow-up #1): every duel verdict in the ledger is
ember-judged only, and LW9 measured slot-A position bias at p=0.0436, so
the verdicts need a second judge. This replays the JUDGE call only on 10
of the 12 banked W8 rows with z-ai/glm-5.3-prime as the alternate judge:
the contender answers are NOT regenerated (loaded from the W8 answer
banks), the prompts are byte-identical to what ember saw (same ask, same
rubric, same swap layout, same ANSWER_LIMIT trims), and the only moving
part is the judge model. tools/duel_harness.py run_rejudge banks each
verdict as mode="altjudge" with rejudge_of pointing at the original row.

Pair selection (10 of 12): all W8 rows except w8-adv-glm-grok and
w8-adv-qwen-glm. Those two are dropped because the adv ask embeds the
full ~20KB harness source (highest per-call cost) AND both dropped rows
flank glm, halving the glm self-judging exposure in the kept set (the
alternate judge is the same model family that authored the glm contender
texts; blinding hides names but self-recognition is possible - disclosed
in AJ1_ALT_JUDGE.md, not hidden).

Ask byte-identity: the adv ask embeds tools/duel_harness.py as it was
when W8 ran. The harness has since gained run_rejudge, so the driver
points the ask builder at the frozen v1.1 blob
(aj1_frozen_harness_v11.py, sha256-matched to the HEAD commit W8 used:
aed6338ad70da357ed6f81432bb7fe84cea83c13e362397c05bea4763cd4a4c9) so the
rebuilt ask is byte-identical to the banked one.

Budget honesty: the operator's "~$0.03" line prices ember judging. The
glm-prime rate card is 10x/12.5x ember's, so the same replays cost more;
this driver meters every call via usage.cost and hard-stops at SPEND_CAP
$0.75, cheapest pairs first (plan, then schema, then adv), so a mid-run
stop still banks maximum coverage. If every Nous call 402s/fails, that is
banked as the diagnostic result and the run stops (operator note).

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/aj1_alt_judge.py --dry
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/aj1_alt_judge.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
import duel_harness as dh  # noqa: E402
import w8_series_duel as w8  # noqa: E402

LEDGER = dh.OUT_DEFAULT
ALT_JUDGE = "z-ai/glm-5.3-prime"
FROZEN_SRC = HERE / "aj1_frozen_harness_v11.py"
FROZEN_SHA = "aed6338ad70da357ed6f81432bb7fe84cea83c13e362397c05bea4763cd4a4c9"
SPEND_CAP = 0.75  # hard stop; glm-prime replays cannot honor the ember-priced ~$0.03 estimate

DROP = {"w8-adv-glm-grok", "w8-adv-qwen-glm"}
# cheapest-first so a budget stop still banks the most pairs
ORDER = [
    "w8-plan-glm-grok", "w8-plan-grok-ds", "w8-plan-ds-qwen", "w8-plan-qwen-glm",
    "w8-schema-glm-grok", "w8-schema-grok-ds", "w8-schema-ds-qwen", "w8-schema-qwen-glm",
    "w8-adv-grok-ds", "w8-adv-ds-qwen",
]


def load_banked() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows[r.get("ask_id", "")] = r
    return rows


def rejudge_id(orig_id: str) -> str:
    return f"{orig_id}|rejudge-{ALT_JUDGE.split('/')[-1]}"


def answers_for_shape(shape: str, cache: dict[str, dict]) -> dict[str, str]:
    texts: dict[str, str] = {
        "glm": w8.GLM_ANSWER_FILES[shape].read_text(encoding="utf-8"),
    }
    for fam in ("grok", "ds", "qwen"):
        texts[fam] = cache[f"{shape}#{fam}"]["content"]
    return texts


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="AJ1 alternate-judge replay of 10 banked W8 duels")
    p.add_argument("--dry", action="store_true", help="plan only, no calls, no writes")
    args = p.parse_args(argv)

    # ask byte-identity: build asks from the frozen v1.1 source blob
    sha = hashlib.sha256(FROZEN_SRC.read_bytes()).hexdigest()
    if sha != FROZEN_SHA:
        print(f"FROZEN SOURCE DRIFT sha256={sha}; refusing (adv ask would not match banked)")
        return 2
    w8.HARNESS_SRC = FROZEN_SRC
    tasks = {s: w8.ASK_BUILDERS[s]() for s in ("adv", "schema", "plan")}

    banked = load_banked()
    w8rows = {i: banked[i] for i in ORDER if i in banked}
    missing = [i for i in ORDER if i not in banked]
    if missing:
        print(f"BANKED ROWS MISSING: {missing}; refusing")
        return 2
    done_rejudge = {i for i in banked if i.endswith("|rejudge-glm-5.3-prime")}
    cache = w8.cache_load()
    texts = {s: answers_for_shape(s, cache) for s in ("adv", "schema", "plan")}

    plan = {
        "alt_judge": ALT_JUDGE, "spend_cap": SPEND_CAP,
        "frozen_source_sha256": sha,
        "pairs": [{"ask_id": i, "shape": i.split("-")[1], "banked_winner": w8rows[i]["winner"],
                   "banked_swap": w8rows[i]["swap"], "already_rejudged": rejudge_id(i) in done_rejudge}
                  for i in ORDER],
        "ask_chars": {s: len(t) for s, t in tasks.items()},
    }
    if args.dry:
        print(json.dumps(plan, indent=2))
        return 0

    keys = dh.load_keys()
    if not keys:
        print("NO KEYS - aborting without spend")
        return 2
    keys, spent = w8.probe_keys(keys)
    if not keys:
        print("NO LIVE KEYS (probe) - aborting without judge spend; bank as diagnostic")
        return 3

    results = []
    for i in ORDER:
        rid = rejudge_id(i)
        if rid in done_rejudge:
            print(f"skip banked {rid}")
            continue
        if spent > SPEND_CAP:
            print(f"SPEND CAP HIT at ${spent:.4f} before {i}; stopping with {len(results)} replays banked")
            break
        shape = i.split("-")[1]
        fa, fb = i.split("-")[2], i.split("-")[3]
        orig = w8rows[i]
        try:
            row = dh.run_rejudge(
                orig, tasks[shape], texts[shape][fa], texts[shape][fb],
                ALT_JUDGE, out_path=LEDGER, keys=keys, caller=w8.call_long,
            )
        except (RuntimeError, SystemExit, ValueError) as e:
            print(f"REJUDGE FAILED {i}: {e}")
            if "402" in str(e):
                print("POOL 402 - stopping (operator flagged this); banking honest diagnostic")
                break
            continue
        spent += row["judge_cost"]
        results.append({
            "ask_id": i, "banked_winner": orig["winner"], "alt_winner": row["winner"],
            "agree": orig["winner"] == row["winner"], "judge_cost": row["judge_cost"],
            "rationale": row["rationale"],
        })
        print(f"running spend ${spent:.4f} / cap ${SPEND_CAP:.2f}")

    print(json.dumps({"rejudged_this_run": len(results), "spent": round(spent, 4),
                      "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
