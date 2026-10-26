#!/usr/bin/env bash
# measure lane finish-line check bundle (2026-09-30). Raw output = measure.check.txt
R=/c/Users/foste/Documents/projects/local_sovereign_agent
cd "$R" || exit 9
echo "== MEASURE CHECK BUNDLE =="; date -u +"moment: %Y-%m-%dT%H:%M:%SZ"

echo "== 1. surface row counts (wc -l) =="
wc -l watch/inbox/luncheon_watchlist_20260929_signals.jsonl
wc -l memory/corpus/LINKS.jsonl
wc -l watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl

echo "== 2. graves count =="
ls watch/inbox/ball2/graves/ | wc -l
ls watch/inbox/ball2/graves/ | head -21

echo "== 3. lane json counts =="
for d in wave5-repair ball-20260929 ball3-suite-green ball4-luncheon-follow; do
  echo -n "gala_20260925/$d/lanes/*.json: "
  ls watch/inbox/gala_20260925/$d/lanes/*.json 2>/dev/null | wc -l
done

echo "== 4. fold_gate.sh reruns x4 =="
cd "$R/watch/inbox/gala_20260925" || exit 9
for spec in "wave5-repair/lanes 12" "ball-20260929/lanes 9" "ball3-suite-green/lanes 3" "ball4-luncheon-follow/lanes 4"; do
  echo "-- fold_gate.sh $spec"
  bash fold_gate.sh $spec 2>&1 | grep -E "lanes_json_count|lanes_parsed_ok|by_division|byte_checks_cited|mined_rows|ballroom_count|GATE (PASS|FAIL)"
  echo "rc=$?"
done
cd "$R" || exit 9

echo "== 5. schtasks cadence =="
powershell -NoProfile -Command "schtasks /Query /FO CSV | Select-String -Pattern 'MagCensusPatrolDaily','MagFtsIndexDaily','EstateWalkDaily','MagImproveDaily','MagGapSentinelDaily','MagGateCanaryDaily'" 2>&1

echo "== 6. git commits in window =="
git log --since="2026-09-28 00:00" --oneline | wc -l
git log --pretty=format:"%ad" --date=short --since="2026-09-28 00:00" | sort | uniq -c
git log --before="2026-09-28 00:00" -1 --pretty=format:"boundary: %h %ad" --date=iso

echo; echo "== 7. verkle chain reads =="
.venv/Scripts/python.exe -c "
import json
rows=[json.loads(l) for l in open('memory/biography/verkle_chain.jsonl','r',encoding='utf-8',errors='replace') if l.strip()]
print('total rows:',len(rows))
for r in rows:
    if r.get('index')==8279:
        print('ask number row: index',r['index'],'n_leaves',r['n_leaves'],'ts',r['ts'])
print('tip: index',rows[-1]['index'],'n_leaves',rows[-1]['n_leaves'],'ts',rows[-1]['ts'])
print('amended rows:',sum(1 for r in rows if r.get('amended')))
"

echo "== 8. the 191.8M negative check =="
echo "-- grep -n '191' watch/inbox/frontier_olm_20260928/DIGEST.md (expect no hits):"
grep -n "191" watch/inbox/frontier_olm_20260928/DIGEST.md
echo "grep rc=$? (1 = no match)"
echo "-- grep -c -i 'token' DIGEST.md (content mentions only):"
grep -c -i "token" watch/inbox/frontier_olm_20260928/DIGEST.md
echo "-- the story chapter's carrying line:"
grep -n "191.8" watch/inbox/48h_synth/STORY.md

echo "== 9. headline quote pins =="
grep -n "19F/2529P" watch/inbox/ball3/quantizer-fallout.md
grep -n "14 failed, 2452 passed" watch/inbox/wave5_repair/suite-burn.md
grep -n "2,568 hermetic green" watch/inbox/HERMES_PRIME_JUDGMENT_20260929.md
grep -n "902 chars / 12 rows" watch/inbox/wave5_repair/render-pipe.md
grep -n "usage" watch/inbox/HERMES_PRIME_JUDGMENT_20260929.md | head -1
grep -n "usage" watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md | head -1
grep -n "usage" watch/inbox/GROK47_LUNCHEON_INTEL_20260929.md | head -1
grep -n "0.0248" watch/inbox/DAY_SYNTHESIS_20260929.md | head -1

echo "== 10. record-law dash scan on measure.md =="
.venv/Scripts/python.exe -c "
b=open(r'watch/inbox/48h_synth/measure.md','rb').read()
print('bytes:',len(b))
print('U+2014 em dash:',b.count(b'\xe2\x80\x94'))
print('U+2013 en dash:',b.count(b'\xe2\x80\x93'))
print('U+2192 arrow:',b.count(b'\xe2\x86\x92'))
"
echo "== END MEASURE CHECK BUNDLE =="
