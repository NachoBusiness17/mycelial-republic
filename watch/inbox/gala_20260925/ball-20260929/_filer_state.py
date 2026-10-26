# estate-filer, ball-20260929 fold: append ONE STATE entry to next-window-handoff.md
import io, sys, datetime

HANDOFF = r"C:\Users\foste\Documents\projects\local_sovereign_agent\memories\session\next-window-handoff.md"

now = datetime.datetime.now(datetime.timezone.utc)
stamp = now.strftime("%Y-%m-%d %H:%M") + "Z"

entry = (
    "- BALL CLOSE " + stamp + " - GALA ball-20260929 banked: fold_gate.sh script count "
    "8/0/1 danced/refired/buried on watch/inbox/gala_20260925/ball-20260929/lanes (9 lanes: "
    "7 division B + 1 A + 1 C, GATE PASS rc 0, byte_checks_cited 46, mined_rows 29). "
    "The 1 counted burial is abliterate-p1.json: it closed done (banked v3 battery run exit 0, "
    "receipt watch/inbox/ball2/abliterate-p1.md) but carries its evidence under battery/results/"
    "ratchet keys instead of ok/checks/rows, so the gate's danced rule cannot see it; shape "
    "mismatch flagged for the next gate pass, NOT hand-overridden. Decisions changed: 8 by lane "
    "content (the gate's key-name map counts 7; bare-spawn-descent carries no decision_changed/"
    "decision/decision_ledger key, its decision lives in baseline_update + conversions: tests/ "
    "bare spawns 21 -> 0, accepted register 41 -> 22). B-division finish: 7/7 finished per lane "
    "JSON (fold-gate ok, driver-v2 done, quantizer-hygiene ok, abliterate-p1 done, mcp-bridge-r1 "
    "ok, bare-spawn-descent done, attention-ledger ok); division A heads-abliteratus ok. "
    "Graves filed: 19 (grave-supersede division C; 19 receipts + machine rows in "
    "watch/inbox/ball2/graves/, 23 index_events rows under writer gala-grave-supersede-20260929, "
    "queue/handoff untouched). 8 LINKS rows (GALA-ball-20260929-*) appended to "
    "memory/corpus/LINKS.jsonl after src dedupe (0 prior ball-20260929 rows; ledger 190 -> 198, "
    "whole-ledger re-parse OK). Per-lane receipts: watch/inbox/ball2/<lane>.md (heads-abliteratus: "
    "check file in lanes/, no ball2 receipt); lane JSONs + check evidence: "
    "watch/inbox/gala_20260925/ball-20260929/lanes/. Ghost for the next window (driver-v2 lane): "
    "an out-of-repo actor kills stealth driver instances ~every 10 min and deletes "
    "state/fuel/stealth_driver.jsonl (owner: boot-lane/process owner; cross-process mutex held, "
    "v2 proof heartbeat banked).\n"
)

BAD = {"\u2014", "\u2013", "\u2212"}
for ch in entry:
    if ch in BAD:
        print("EMDASH FOUND in entry"); sys.exit(3)

with io.open(HANDOFF, "r", encoding="utf-8") as fh:
    body = fh.read()
if "ball-20260929" in body:
    print("REFUSING: an existing ball-20260929 mention is already in the handoff (dedupe)"); sys.exit(4)

with io.open(HANDOFF, "a", encoding="utf-8", newline="\n") as fh:
    if body and not body.endswith("\n"):
        fh.write("\n")
    fh.write("\n" + entry)

print("STATE entry appended to %s (%d chars)" % (HANDOFF, len(entry)))
