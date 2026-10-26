#!/usr/bin/env python3
# prior_art: watch/inbox/door_invariant_20261023/ds_eval.py, tools/citation_lint.py -- ds_eval is the door experiment's one-shot scorer, not a standing grader; citation_lint checks prose citations, not exam answers
"""door_grade -- the leaderboard door's grader (v1, deterministic).

consumer: the leaderboard door (door/ in the public repo) + the operator's
build-or-kill D3 clock; verifier: door/leaderboard.json regenerates
byte-identically from the same inputs (re-run = idempotent), and the seeded
machine-cohort rows come from the lanes' own graded tiers in
watch/inbox/door_invariant_20261023/CONVERGENCE.md (never hand-invented).

Two cohorts, one board:
  machine: scored from the 10-23 door-experiment convergence matrix. The
  grading basis IS the convergence set (the door's own thesis: what blind
  minds find without comparing notes is the measurable discovery). Tier
  weights: C=1.0, L=0.6, G=0.3, X/-=0.
  human: the seven-question exam from PUBLIC_DOOR.md, graded by a
  deterministic rubric (per-question rule signatures, 0/1/2 each, plus an
  honesty point on Q7 self-calibration). v1 matcher is keyword-signature
  based; a frontier re-grade leg may re-score later and records both.

Usage:
  python tools/door_grade.py build      # regenerate door/leaderboard.json
  python tools/door_grade.py grade <answers.txt> --alias NAME
      # grade one human exam, print the row (append to leaderboard via build)
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONV = ROOT / "watch/inbox/door_invariant_20261023/CONVERGENCE.md"
BOARD = ROOT / "door/leaderboard.json"
TIER_W = {"C": 1.0, "L": 0.6, "G": 0.3, "X": 0.0}

# The seven human-exam questions: rubric signatures (regex, weight 2 = the
# rule named/operationally restated, 1 = partial/adjacent). Derived from the
# story's rules A-N; the matcher is deliberately legible.
RUBRIC = {
    "Q1": {
        "rule": "individual failure is not structural failure (the shelf held)",
        "full": r"(shelf|structure|system).{0,60}(held|fine|unmoved|intact)|(structural|systemic).{0,40}(fail|damage)",
        "part": r"(fell|stool|perch|support).{0,80}(only|just|himself|him)|individual.{0,40}(not|!=).{0,30}(structur|system)",
    },
    "Q2": {
        "rule": "erasing a record is theft; the blank space is the evidence",
        "full": r"erasur|eras(e|ed|ing)|delet.{0,40}(theft|stolen|record)|(theft|stolen).{0,40}(erasure|erased|removal|information|record|name)",
        "part": r"blank|removed|cleaned|ink|information.{0,30}(lost|gone)",
    },
    "Q3": {
        "rule": "retire the failed instrument but keep it (the map stays folded)",
        "full": r"(retire|keep|retain).{0,60}(map|instrument|failed)|(reference|lesson|reminder)",
        "part": r"useful|wrong|lied|truth.{0,30}(map|linen)",
    },
    "Q4": {
        "rule": "leave the wound unrepaired so readers ask what was there",
        "full": r"(leave|keep|visible).{0,60}(torn|wound|blank|unrepaired)|(ask|wonder|question).{0,40}(was|what.{0,20}there)",
        "part": r"tamper|evidence|honest|history|not.{0,20}(rewrite|hide|repair)",
    },
    "Q5": {
        # trap question: the story contains NO gardener scene. The graded-
        # correct answer is saying so plainly (the door's own instruction).
        "rule": "there is no gardener in the story - the honest answer says the scene does not exist",
        "full": r"(no|not|isn't|is not|never).{0,40}(gardener|such scene|such thing|in the story)|story.{0,40}(does not|doesn't).{0,30}(contain|mention|say)|cannot find|not present",
        "part": r"(gardener|burn|map|forgive)",
    },
    "Q6": {
        "rule": "two ledgers contradicting = the house surfaces both and lets traces testify (any coherent rule-following scene scores)",
        "full": r"(both|second|contradict).{0,60}(ledger|record|copied|published|read)|(magistrate|witness|public)",
        "part": r"investigat|compare|reconcil|truth|rule",
    },
    "Q7": {
        "rule": "self-calibration is part of the exam (honesty point)",
        "full": r"(sure|certain).{0,60}(guess|unsure|less sure)|(guess|unsure|not sure)",
        "part": r".",
    },
}


def machine_rows() -> list[dict]:
    text = CONV.read_text(encoding="utf-8", errors="replace")
    lanes = ["L1", "L2s", "L3", "L4", "L5", "L6"]
    tiers: dict[str, dict[str, float]] = {l: {} for l in lanes}
    rule_ids = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*[A-N]\s*\|", line):
            continue
        cells = [c.strip() for c in line.split("|")]
        # [ '', rule_id, rule_text, L1, L2s, L3, L4, L5, L6, count ]
        rid = cells[1]
        tier_cells = cells[3:9]
        if len(tier_cells) < 6:
            continue
        tiers_cells = [c.split()[0] if c else "-" for c in tier_cells]
        if not all(re.fullmatch(r"[CLGX-]", c) for c in tiers_cells):
            continue
        rule_ids.append(rid)
        for lane, cell in zip(lanes, tiers_cells):
            tiers[lane][rid] = TIER_W.get(cell, 0.0)
    n = max(len(rule_ids), 1)
    rows = []
    meta = {
        "L1": ("glm-5.3 (opencode, ZAI MAX)", "Fostertron seat"),
        "L2s": ("glm-5.3 (direct API substitute)", "Nacho Corp LITE stood in by Pro key"),
        "L3": ("claude-sonnet-5.5-medium", "agy on bob"),
        "L4": ("agy default", "agy on PC"),
        "L5": ("mimo-v2.6-flash-free", "opencode"),
        "L6": ("gemma4 (local ollama)", "the house's own worker"),
    }
    for lane in lanes:
        cov = sum(tiers[lane].values()) / n
        rows.append({
            "alias": lane, "kind": "machine", "model": meta[lane][0], "seat": meta[lane][1],
            "coverage": round(cov, 3), "rules_hit": sum(1 for v in tiers[lane].values() if v >= 1.0),
            "rules_total": n,
            "tiers": tiers[lane],
        })
    rows.sort(key=lambda r: -r["coverage"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


def grade_human(text: str) -> dict:
    # anchored to line start: a bare "Q6." inside an answer sentence must not
    # spawn a phantom question (the Q7 self-report names its own guesses)
    qpat = re.compile(r"(?m)^\s*(?:Q\s*)?([1-7])[\).:]\s*(.+?)(?=^\s*(?:Q\s*)?[1-7][\).:]|\Z)", re.S)
    found = {m.group(1): m.group(2) for m in qpat.finditer(text)}
    per_q, total = {}, 0
    for q, rub in RUBRIC.items():
        ans = found.get(q[1], "")
        if not ans.strip():
            per_q[q] = 0
            continue
        score = 0
        if re.search(rub["full"], ans, re.I):
            score = 2
        elif re.search(rub["part"], ans, re.I):
            score = 1
        per_q[q] = score
        total += score
    max_total = sum(2 for _ in RUBRIC)
    return {"kind": "human", "per_q": per_q, "total": total, "max_total": max_total,
            "pct": round(total / max_total, 3)}


def build() -> None:
    rows = machine_rows()
    human_rows = []
    if BOARD.exists():
        try:
            old = json.loads(BOARD.read_text(encoding="utf-8"))
            human_rows = [r for r in old.get("readers", [])]
        except Exception:
            human_rows = []
    BOARD.parent.mkdir(parents=True, exist_ok=True)
    BOARD.write_text(json.dumps({
        "board": "the door - a reading game with a hidden answer key",
        "basis": "machine cohort graded on the blind convergence set (watch/inbox/door_invariant_20261023); human cohort graded by the public rubric in tools/door_grade.py; no personal names, only aliases",
        "exam": "door/index.html",
        "machine_cohort": rows,
        "readers": human_rows,
        "generated": __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
    }, indent=1), encoding="utf-8")
    print(f"board written: {len(rows)} machine rows, {len(human_rows)} readers")


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] == "build":
        build()
        return 0
    if sys.argv[1] == "grade":
        if len(sys.argv) < 3:
            print("usage: door_grade.py grade <answers.txt> [--alias NAME]", file=sys.stderr)
            return 2
        text = Path(sys.argv[2]).read_text(encoding="utf-8", errors="replace")
        alias = "anonymous"
        if "--alias" in sys.argv:
            alias = sys.argv[sys.argv.index("--alias") + 1]
        row = grade_human(text)
        row["alias"] = alias
        print(json.dumps(row, indent=1))
        return 0
    print("usage: door_grade.py build | grade <answers.txt> [--alias NAME]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
