"""BREAK-OPERATIONS probe: fold verdict-walk blindness (F3), reproduced.

Run 1: all three deep_tier2 row_keys FIVE words (runner spelling drift) with
  lowercase unconfirmed/crashed verdicts -> lens claims included=3 excluded=0.
Run 2: correct six-word keys, verdicts Unconfirmed (capital-C) / crashed /
  refuted (out of vocabulary) -> lens claims only lowercase crashed excludes.
Pure file ops + module import; no subprocess spawned.
"""
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(REPO))
import tools.mickey17_v2_fold as fold  # noqa: E402

claims = [
    "alpha beta gamma delta epsilon zeta eta thesis one",
    "alpha beta gamma delta epsilon theta thesis two",
    "alpha beta gamma delta epsilon iota thesis three",
]
rows = [{"claim": c, "quote": "q" + str(i), "source": "s" + str(i), "steal": "st",
         "estate_status": "executed", "leverage": "high"} for i, c in enumerate(claims)]

six = [c.split(" ")[:6] for c in claims]
five = [c.split(" ")[:5] for c in claims]

ARCHIVE = Path(tempfile.mkdtemp(prefix="break_fold_")
               ) / "memory" / "runs" / "mickey17_v2" / "runs"

def build(slug, entries):
    lanes = ARCHIVE / "runs" / slug / "lanes"  # main() appends runs/ itself
    lanes.mkdir(parents=True)
    (lanes / "a.json").write_text(json.dumps({"rows": rows}), encoding="utf-8")
    (lanes / "a.checks.json").write_text(json.dumps(
        {"lane": "a", "supports": [], "counts": {}, "deep_tier2": entries}),
        encoding="utf-8")

def run(slug):
    fold.RUN_ROOT = ARCHIVE
    fold.LANES_DIR = ARCHIVE / slug / "lanes"
    sys.argv = ["mickey17_v2_fold.py", "--run", slug]
    fold.main()

# run 1: five-word keys, honest lowercase verdicts
build("probe1", [
    {"row_key": "a: " + " ".join(five[0]), "verdict": "unconfirmed"},
    {"row_key": "a: " + " ".join(five[1]), "verdict": "crashed"},
    {"row_key": "a: " + " ".join(five[2]), "verdict": "unconfirmed"},
])
print("== run 1: five-word row_keys, lowercase verdicts ==")
run("probe1")

# run 2: correct six-word keys, casing + vocabulary drift
build("probe2", [
    {"row_key": "a: " + " ".join(six[0]), "verdict": "Unconfirmed"},
    {"row_key": "a: " + " ".join(six[1]), "verdict": "crashed"},
    {"row_key": "a: " + " ".join(six[2]), "verdict": "refuted"},
])
print("== run 2: six-word keys, Unconfirmed/refuted vocabulary drift ==")
run("probe2")
