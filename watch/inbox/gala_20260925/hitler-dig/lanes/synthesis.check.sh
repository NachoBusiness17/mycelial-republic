#!/usr/bin/env bash
# synthesis lane (division A) check bundle - hitler-dig, gala_20260925. Raw output = synthesis.check.txt
R=/c/Users/foste/Documents/projects/local_sovereign_agent
cd "$R" || exit 9
echo "== SYNTHESIS CHECK BUNDLE (hitler-dig, division A) =="
date -u +"moment: %Y-%m-%dT%H:%M:%SZ"

echo ""
echo "== 1. head receipt presence (expect ABSENT; absence is a finding, not a pass) =="
ls watch/inbox/hitler_dig/synthesis.md 2>&1
echo "rc=$?"

echo ""
echo "== 2. dig lanes dir contents (sibling-lane receipts expected absent at first write) =="
ls -la watch/inbox/gala_20260925/hitler-dig/lanes/ 2>&1

echo ""
echo "== 3. prior-receipt presence (the sources this lane starts from) =="
for f in watch/inbox/gala_20260925/ouroboros_RECEIPT.md memory/runs/salons/unified_fold_20260906/SALON_ARTIFACT.md memory/rib/RIB_DRIVING_LADDER_20260928.md watch/inbox/ractor50/accuracy.md watch/inbox/burn_wave_20260926/B2_216_collect_delta_20260926.md tools/citation_lint.py tools/ouroboros.py; do
  if [ -f "$f" ]; then echo "PRESENT $f ($(wc -c < "$f") B)"; else echo "ABSENT $f"; fi
done

echo ""
echo "== 4. founding-phantom zero-hit re-verification (expect grep -c 191 = 0) =="
n=$(grep -c "191" watch/inbox/frontier_olm_20260928/DIGEST.md 2>/dev/null)
echo "grep -c 191 in watch/inbox/frontier_olm_20260928/DIGEST.md: $n (rc=$?; 0 with rc=1 = zero hits confirmed)"

echo ""
echo "== 5. ESTATE GREP (2 dirs, per-ask) =="
for d in corpus/steal memory/corpus; do
  for t in apophenia numerolog genealog; do
    c=$(grep -rli "$t" "$d" 2>/dev/null | wc -l)
    echo "$d :: $t :: files_with_hits=$c"
  done
done
echo "-- numerology hit detail (memory/corpus, expected exactly secret_teachings_of_all_ages.txt):"
grep -rli "numerolog" memory/corpus/ 2>/dev/null

echo ""
echo "== 6. quote byte-check (T0/T1, the mined rows' evidence) =="
.venv/Scripts/python.exe watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.check.py
echo "bytecheck rc=$?"

echo ""
echo "== 7. citation_lint --selftest (the phantom-number engine's own battery) =="
.venv/Scripts/python.exe tools/citation_lint.py --selftest
echo "selftest rc=$?"
