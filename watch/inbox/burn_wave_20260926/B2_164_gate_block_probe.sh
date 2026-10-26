#!/bin/sh
# B2-164 falsifier driver: runs the landed workflow_gate_scenarios pre-push
# block VERBATIM (sed-extracted from githooks/pre-push lines 210 to EOF) in
# four directions, plus a range-arm positive and negative on real gate
# history. Mutations to tools/workflow_gate.py are guarded single-string
# replaces, restored and sha256-verified after each direction. Results are
# appended as one JSON line to B2_164_gate_block_results.json by the caller
# (this script prints tagged lines the caller captures per direction).
# Run from the repo root with the repo's own venv on PATH expectations
# (.venv/Scripts/python.exe is called by the block itself, relative paths).
# No set -e on purpose: the T1 red direction exits 1 by design and the driver
# must survive it to print EXIT=1.
REPO=$(pwd)
BLOCK=$(mktemp)
sed -n '210,$p' githooks/pre-push > "$BLOCK"
GATE=tools/workflow_gate.py
PRE_SHA=$(sha256sum "$GATE" | cut -d' ' -f1)

mutate_gate() {
  .venv/Scripts/python.exe - "$1" <<'PYEOF'
import sys
mode = sys.argv[1]
path = "tools/workflow_gate.py"
with open(path, encoding="utf-8") as f:
    text = f.read()
if mode == "red":
    old = "     lambda t: bool(re.search(r'report\\(\\s*\\w+\\s*\\)\\s*;', t)),\n"
    new = "     lambda t: False,  # B2-164 falsifier mutation\n"
elif mode == "dirty":
    old = "import argparse\n"
    new = "import argparse  # B2-164 falsifier dirty-tree marker\n"
elif mode == "restore":
    # reverse of whichever mutation stands; try red first, then dirty
    pairs = [
        ("     lambda t: False,  # B2-164 falsifier mutation\n",
         "     lambda t: bool(re.search(r'report\\(\\s*\\w+\\s*\\)\\s*;', t)),\n"),
        ("import argparse  # B2-164 falsifier dirty-tree marker\n",
         "import argparse\n"),
    ]
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new, 1)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            print("restored")
            raise SystemExit(0)
    print("nothing-to-restore")
    raise SystemExit(0)
count = text.count(old)
if count != 1:
    print(f"MUTATION-GUARD-FAIL mode={mode} count={count}")
    raise SystemExit(3)
text = text.replace(old, new, 1)
with open(path, "w", encoding="utf-8", newline="") as f:
    f.write(text)
print("mutated")
PYEOF
}

run_block() {
  # $1 = CAPTION_PUSH_INPUT value; runs the verbatim block, tees output
  CAPTION_PUSH_INPUT="$1" sh "$BLOCK" 2>&1
  echo "EXIT=$?"
}

case "$1" in
  t3_skip)
    # gate clean vs HEAD, empty stdin: expect skipped arm, exit 0, no SCENARIOS
    run_block "" ;;
  t4_range_pos)
    # real history: range 5c6b1b4a..77ff6138 touches the gate, tree clean
    run_block "refs/heads/b2_164_t4 77ff6138bc1c108435e316b530c792a7b1088c27 refs/heads/b2_164_t4 5c6b1b4a57198dd5f3fe1feb4cca6eac07a8acbf" ;;
  t4_range_neg)
    # empty range: local equals remote parent, no gate change in range
    run_block "refs/heads/b2_164_t4 5c6b1b4a57198dd5f3fe1feb4cca6eac07a8acbf refs/heads/b2_164_t4 5c6b1b4a57198dd5f3fe1feb4cca6eac07a8acbf" ;;
  t2_green_dirty)
    mutate_gate dirty
    run_block "" ;;
  t1_red)
    mutate_gate red
    run_block "" ;;
  restore)
    mutate_gate restore
    sha256sum "$GATE" | cut -d' ' -f1 ;;
  presha)
    echo "$PRE_SHA" ;;
esac
rm -f "$BLOCK"
