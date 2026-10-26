#!/usr/bin/env bash
# GALA fold gate: counting script; prose folds around its numbers (Law 5).
# The verdict is the exit code and these printed sections, never model opinion.
# Args: LANES_DIR EXPECTED_LANE_COUNT
#
# Root cause receipt (2026-09-29 ball-20260929 fold-gate lane): the filer's
# "exits 127" was never a defect of this file - it exists, is git-tracked
# (a5dd96176), and its LF shebang is correct. 127 was the Windows spawn
# resolution: bare `bash` can land on C:/Windows/System32/bash.exe (WSL
# launcher), and WSL-side bash cannot exec this script's Windows venv python
# (line below), dying "No such file or directory" rc=127 mid-run. The saved
# the-gala workflow spawns `bash fold_gate.sh LANES N` from the estate cwd
# (the-gala.dwf.ts:269), so the estate-root bash.exe shim (receipt:
# watch/inbox/gala_20260925/wave5-repair/fold-gate-repair.md) routes the spawn
# to Git Bash. The guard below fails loud, naming the cause, if the gate is
# ever run under a non-MINGW/MSYS/CYGWIN bash again.
set -u
PY="C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe"
DIR="$1"; EXPECT="$2"
UNAME_S="$(uname -s 2>/dev/null || echo UNKNOWN)"
case "$UNAME_S" in
  MINGW*|MSYS*|CYGWIN*) ;;
  *)
    echo "GATE FAIL: wrong bash: $UNAME_S - this gate is Windows Git Bash only"
    echo "(WSL or Linux bash cannot exec the Windows venv python; spawn via the"
    echo " estate-root bash.exe shim from the estate cwd, or run git-bash directly)"
    exit 2 ;;
esac
echo "== SECTIONS BEGIN (script-written numbers, authoritative) =="
count=$(ls "$DIR"/*.json 2>/dev/null | wc -l)
echo "lanes_json_count: $count (expected $EXPECT)"
if [ "$count" -ne "$EXPECT" ]; then echo "GATE FAIL: lane count mismatch"; exit 2; fi
"$PY" - "$DIR" <<'EOF'
import json, sys, glob, os
d = sys.argv[1]
files = sorted(glob.glob(os.path.join(d, "*.json")))
bad = []
divs = {}; ok = 0; changed = []; checks = 0; rows = 0
# Ballroom count (danced/refired/buried), mapped 1:1 onto the saved the-gala
# workflow's own bankLane branches (the-gala.dwf.ts:233-248):
#   danced: ok truthy, OR ok absent/false but rows or checks banked (the
#           workflow banks an ok-false result that carries evidence as danced)
#   buried: parseable JSON, no ok, no rows, no checks - exactly the
#           "empty on refire" shape the workflow buries (dwf.ts:240)
#   refired: not recoverable from the GalaLaneOut schema (the workflow holds
#           it at runtime); counted from an optional per-lane "refired": true
#           marker, else 0. A counted burial is a real outcome the fold
#           reports; it does NOT fail the gate (exit != 0 would summon the
#           dwf's gate-repairer at every honest burial - ts:270-277).
danced = 0; refired = 0; buried = 0; stuck_files = []; banked_files = []
for f in files:
    try:
        with open(f, encoding="utf-8") as fh:
            j = json.load(fh)
    except Exception as e:
        bad.append((os.path.basename(f), str(e)[:80])); continue
    if not isinstance(j, dict):
        # Shape guard (operations lane ractor50, 2026-09-30): a top-level JSON
        # list (tool byproduct or raw dump, e.g. _bridge_list_raw.json /
        # _full_list_raw.json found live in the ractor50 archive) crashed this
        # section with an AttributeError traceback; it must fail loud naming
        # the file instead. Checks unweakened: such a file still exits 2.
        bad.append((os.path.basename(f), "not a lane JSON object: top-level " + type(j).__name__)); continue
    div = j.get("division", "?"); divs[div] = divs.get(div, 0) + 1
    ok += 1 if j.get("ok") else 0
    checks += len(j.get("checks") or [])
    rows += len(j.get("rows") or [])
    nrow = len(j.get("rows") or []); nchk = len(j.get("checks") or [])
    name = os.path.basename(f)
    if j.get("refired"):
        refired += 1
    if j.get("ok") or nrow > 0 or nchk > 0:
        danced += 1
        if not j.get("ok"):
            banked_files.append(name + " (ok absent/false, evidence-banked: " + str(nchk) + " checks, " + str(nrow) + " rows)")
    else:
        buried += 1
        stuck_files.append(name + " (no ok, rows=0, checks=0 - the empty-on-refire buried shape)")
    dc = str(j.get("decision_changed", j.get("decision", j.get("decision_ledger", "no"))))
    if dc != "no":
        changed.append(name + ": " + dc[:100])
print("lanes_parsed_ok: " + str(ok) + "/" + str(len(files)))
print("by_division: " + json.dumps(divs))
print("byte_checks_cited: " + str(checks) + "  mined_rows: " + str(rows))
print("decisions_changed: " + str(len(changed)))
for c in changed:
    print("  changed: " + c)
print("ballroom_count (danced/refired/buried): " + str(danced) + "/" + str(refired) + "/" + str(buried))
for s in stuck_files:
    print("  stuck: " + s)
for b in banked_files:
    print("  banked: " + b)
for b, e in bad:
    print("  corrupt: " + b + ": " + e)
if bad:
    sys.exit(2)
print("== SECTIONS END ==")
EOF
rc=$?
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
echo "GATE PASS"
