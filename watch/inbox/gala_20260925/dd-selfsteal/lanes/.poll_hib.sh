#!/bin/bash
# hermes-intelligent-burn poll loop: watch for sibling receipts.
# Exits early when 3+ md receipts land in dd_dogfood/ or 5+ lane JSONs (incl econ) in lanes/.
R=/c/Users/foste/Documents/projects/local_sovereign_agent
end=$((SECONDS + 2700))
while [ $SECONDS -lt $end ]; do
  dd=$(ls "$R/watch/inbox/dd_dogfood/" 2>/dev/null | grep -c "\.md")
  lanes=$(ls "$R/watch/inbox/gala_20260925/dd-selfsteal/lanes/"*.json 2>/dev/null | wc -l)
  econ=$(ls "$R/watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-burn-economics.json" 2>/dev/null | wc -l)
  echo "$(date -u +%H:%M:%SZ) dd_dogfood_md=$dd lane_jsons=$lanes econ_json=$econ"
  if [ "$dd" -ge 3 ]; then echo "DOGFOOD_RECEIPTS_LANDED"; break; fi
  if [ "$econ" -ge 1 ] && [ "$lanes" -ge 5 ]; then echo "LANES_COMPLETE_5PLUS"; break; fi
  sleep 60
done
echo "POLL_DONE at $(date -u +%H:%M:%SZ)"
