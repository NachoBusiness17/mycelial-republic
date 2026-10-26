#!/usr/bin/env bash
# selfsteal-24h-laws finish-line byte battery, 2026-10-03
# Re-greps every quote and path:line citation in watch/inbox/dd_dogfood/selfsteal-laws.md
# plus the negative checks. Raw output = the evidence file.
cd /c/Users/foste/Documents/projects/local_sovereign_agent || exit 9
MISSES=0
py=.venv/Scripts/python.exe
RECEIPT=watch/inbox/dd_dogfood/selfsteal-laws.md

note() { # name, detail, ok(0/1)
  if [ "$3" = "0" ]; then S=PASS; else S=FAIL; MISSES=$((MISSES+1)); fi
  printf '[%s] %s : %s\n' "$S" "$1" "$2"
}
line_has() { # file, lineno, needle
  [ "$(sed -n "${2}p" "$1" | grep -cF "$3")" -ge 1 ]
}
flat_has() { # file, needle (newline-insensitive, whitespace-squeezed)
  tr -s '[:space:]' ' ' < "$1" | grep -qF "$2"
}

echo "== 01 receipt exists =="
[ -f "$RECEIPT" ]; note "receipt-exists" "$(wc -c < "$RECEIPT") bytes" $?

echo "== 02 em/en-dash scan on receipt (expect 0) =="
D=$($py -c "import sys;d=open(sys.argv[1],encoding='utf-8').read();print(d.count(chr(0x2013))+d.count(chr(0x2014)))" "$RECEIPT")
[ "$D" = "0" ]; note "dash-scan-0" "dashes=$D" $?

echo "== 03 rib one-bug founding incident (rib line 55) =="
line_has memory/rib/RIB_DRIVING_LADDER_20260928.md 55 'now everywhere one bug, many jackets'
note "onebug-rib:55" "grep rc=$?" $?

echo "== 04 rib SPEND verbatim (rib line 41) =="
line_has memory/rib/RIB_DRIVING_LADDER_20260928.md 41 'you literally have HERMES AND GROK 4.7 USE IT I WANT YOU TO SPEND MONEY'
note "spend-rib:41" "grep rc=$?" $?

echo "== 05 negative: paraphrase NOT in rib (expect count 0) =="
C=$(grep -cF 'A VERDICT WITHOUT ITS CONDITIONS' memory/rib/RIB_DRIVING_LADDER_20260928.md)
[ "$C" = "0" ]; note "no-paraphrase-in-rib" "count=$C" $?

echo "== 05b rib SPEND falsifier line 50 =="
line_has memory/rib/RIB_DRIVING_LADDER_20260928.md 50 'a night where zero paid calls landed while judgment-class work rode free lanes is a'
note "spend-falsifier-rib:50" "grep rc=$?" $?

echo "== 06 STANDING_RAILS hollow-batch quote (spans lines 15-16) =="
flat_has queue/STANDING_RAILS.md 'a cheap seat fabricates when evidence is missing, and the run still prints ok=True'
note "hollow-quote" "grep rc=$?" $?

echo "== 07 STANDING_RAILS cited lines 13,17,19,46,49 non-blank =="
R07=0
for L in 13 17 19 46 49; do
  sed -n "${L}p" queue/STANDING_RAILS.md | grep -q '[^[:space:]]' || { echo "line $L blank"; R07=1; }
done
note "rails-lines" "13/17/19/46/49 non-blank rc=$R07" "$R07"

echo "== 08 envelope width quote (line 33) =="
line_has watch/inbox/envelope_50w_20261003.md 33 'Task-agent width 50 (single wave) is CLEAN on the paid max seat'
note "envelope:33" "grep rc=$?" $?

echo "== 09 AGENTS.md width carrier still pre-amendment (proves staleness claim) =="
grep -qF 'measured clean at widths 3, 6, 10 and 12' AGENTS.md
note "agents-width-stale-text" "grep rc=$?" $?

echo "== 10 AGENTS.md census carrier refreshed =="
grep -qF '4,156 tests collected / 497 files (2026-10-02 census' AGENTS.md
note "agents-census-carrier" "grep rc=$?" $?

echo "== 11 blind audit section line 144 + reword law line 154 =="
line_has watch/inbox/blind_audit_ractors_20261002.md 144 'Three named improvements'
A=$?
line_has watch/inbox/blind_audit_ractors_20261002.md 154 'REWORD-RECHECK + FULL COVERAGE LAW: absence claims get re-grepped by'
B=$?
[ $A -eq 0 ] && [ $B -eq 0 ]; note "blindaudit:144,154" "rc144=$A rc154=$B" $?

echo "== 12 blind audit reword quote across wrap =="
flat_has watch/inbox/blind_audit_ractors_20261002.md 'absence claims get re-grepped by underlying quantity, not exact phrase'
note "blindaudit-quote" "grep rc=$?" $?

echo "== 13 ouroboros depth-dilutes quote =="
flat_has watch/inbox/gala_20260925/ouroboros_RECEIPT.md 'receipts grew +1,457 in 2 days while effective dimensionality D fell 4.3 to 4.0'
note "ouroboros-quote" "grep rc=$?" $?

echo "== 14 cross_ractor_bytecheck.py exists =="
[ -f watch/inbox/gala_20260925/ouroboros/lanes/cross_ractor_bytecheck.py ]
note "bytecheck-instrument-exists" "test rc=$?" $?

echo "== 15 hitler-ancestry.json falsifiers at lines 13 and 22 =="
line_has watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json 13 'An estate file, not web content, containing a real genealogical record'
A=$?
line_has watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json 22 'date, place, and document'
B=$?
[ $A -eq 0 ] && [ $B -eq 0 ]; note "ancestry-falsifiers:13,22" "rc13=$A rc22=$B" $?

echo "== 16 routing amendment commit subject =="
git log --format='%s' | grep -qF 'offpeak-idle plan measured DEAD for workflow subagents'
note "routing-amend-commit" "grep rc=$?" $?

echo "== 17 lyric law commit subject =="
git log --format='%s' | grep -qF 'songs need archetypes and want, not findings and findings-citations'
note "lyric-law-commit" "grep rc=$?" $?

echo "== 18 negative: ouroboros queue rows dir still absent (expect exit 2) =="
ls watch/inbox/ouroboros/2026-10-02/ >/dev/null 2>&1; RC=$?
[ "$RC" = "2" ]; note "ouroboros-queuedir-absent" "ls rc=$RC" $?

echo "== 19 negative: engine laws not in any saved workflow =="
C=$(grep -rl 'cross-contradiction' .zcode/workflows/ 2>/dev/null | wc -l)
D=$(grep -rl 'quantifier' .zcode/workflows/ 2>/dev/null | wc -l)
[ "$C" = "0" ] && [ "$D" = "0" ]; note "engine-laws-not-landed" "cross-contradiction files=$C quantifier files=$D" $?

echo "== 20 registry parse: 12 entries, LAW-13 newest, window line =="
$py -c "
import json
d=json.load(open('memory/law/registry.json',encoding='utf-8'))
ids=list(d.keys())
assert len(ids)==12, ids
assert d['LAW-13']['born']=='2026-09-26', d['LAW-13'].get('born')
assert 'closes 2026-10-10' in d['LAW-12']['window']
print('registry ok: 12 entries, LAW-13 born 2026-09-26, LAW-12 window closes 2026-10-10')
"
note "registry-parse" "python rc=$?" $?
line_has memory/law/registry.json 131 'closes 2026-10-10'
note "registry:131" "grep rc=$?" $?

echo "== 21 enforcement trail: 16:19Z cycle has applied LAW-3 and no-executor LAW-10 =="
T=$(grep -c '2026-10-03T16:19.*LAW-3.*applied.: true' memory/law/enforcement_trail.jsonl)
N=$(grep -c '2026-10-03T16:19.*no executor' memory/law/enforcement_trail.jsonl)
[ "$T" -ge 1 ] && [ "$N" -ge 1 ]; note "trail-heartbeat" "applied LAW-3 rows=$T no-executor rows=$N" $?

echo "== 22 instance-guard doubled_key firing live 2026-10-03 =="
K=$(grep -c '"doubled_key": true' memory/runs/hermes_burn/usage.jsonl)
M=$(grep -c '2026-10-03T19:02' memory/runs/hermes_burn/usage.jsonl)
[ "$K" -ge 1 ] && [ "$M" -ge 1 ]; note "doubled-key-live" "doubled_key rows=$K 19:02Z rows=$M" $?

echo "== 23 RIB_ROUTING_CLASSES rows and falsifier =="
for P in '3:Provenance' '11:ROUTE BY QUESTION-CLASS FIRST' '16:TWO EFFECTIVE REMOTE CLASSES' '21:TRANSPORT IS NOT QUALITY' '24:COST-PER-BLIND-POINT' '28:Falsifier'; do
  L=${P%%:*}; N=${P#*:}
  line_has memory/rib/RIB_ROUTING_CLASSES_20261002.md "$L" "$N" || { echo "line $L missing $N"; exit 1; }
done
flat_has memory/rib/RIB_ROUTING_CLASSES_20261002.md 'a future blind audit at the same shape where family explains more variance than question'
A=$?
flat_has memory/rib/RIB_ROUTING_CLASSES_20261002.md 'duplication is emphasis, this row leads'
B=$?
[ $A -eq 0 ] && [ $B -eq 0 ]; note "routing-rib-lines+falsifier" "falsifier rc=$A emphasis rc=$B" $?

echo "== 24 48h_synth falsifier-convention line =="
flat_has watch/inbox/48h_synth/laws.md 'falsifiers are still named at mint time'
note "48h-convention" "grep rc=$?" $?

echo "== 25 cited instruments and receipts exist =="
for F in tools/citation_lint.py tools/instance_guard.py tools/ouroboros.py mag/route_chat.py queue/STANDING_RAILS.md watch/inbox/TRANSFER_TEST_20260906.md watch/inbox/frontier_delta_steal_20261003.md watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.json watch/inbox/dd_dogfood/selfsteal-laws.md; do
  [ -f "$F" ] || { echo "MISSING $F"; exit 1; }
done
note "paths-exist" "9/9 present" $?

echo "== 26 song timing evidence (no assertion, raw mtimes) =="
ls -la --time-style=+%Y-%m-%dT%H:%M watch/inbox/music/CUT_SEED_SAVER.md watch/inbox/music/CUT_THE_HUM.md 2>/dev/null

echo "== 27 citation_lint on this receipt (estate prose gate, self-test) =="
$py tools/citation_lint.py check --files "$RECEIPT"
note "citation-lint-receipt" "rc=$?" $?

echo "== 28 lane JSON parses =="
$py -m json.tool watch/inbox/gala_20260925/dd-selfsteal/lanes/selfsteal-24h-laws.json >/dev/null
note "lane-json-parse" "rc=$?" $?

echo "== 29 registry zero births in window (newest registered_ts <= 2026-09-26 or born field) =="
$py -c "
import json
d=json.load(open('memory/law/registry.json',encoding='utf-8'))
newest=max(v.get('born', v.get('registered_ts',''))[:10] for v in d.values())
print('newest birth date in registry:', newest)
assert newest <= '2026-09-26', 'unexpected window birth'
"
note "no-window-births-in-registry" "rc=$?" $?

echo
echo "MISSES=$MISSES"
[ "$MISSES" = "0" ] && echo "BATTERY EXIT 0" || echo "BATTERY EXIT 1"
exit $([ "$MISSES" = "0" ] && echo 0 || echo 1)
