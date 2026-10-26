#!/usr/bin/env bash
# Quote byte-check for lane grokbot-economics (division A, gala 20261003).
# Each quote must appear VERBATIM, line by line, in its cited estate file.
# Fixed-string grep, single-quoted so backticks are literal. Exit 0 = all 5 quotes byte-found.
cd "C:/Users/foste/Documents/projects/local_sovereign_agent" || exit 1
fail=0
chk() { # chk <label> <file> <line...>
  local label="$1"; shift; local file="$1"; shift
  for ln in "$@"; do
    n=$(grep -cF -- "$ln" "$file" 2>/dev/null)
    if [ "$n" -ge 1 ]; then echo "PASS [$label] line bytes found ($n)x: $ln"
    else echo "FAIL [$label] line NOT found: $ln"; fail=1; fi
  done
}

chk Q1-steal-27-29 watch/inbox/frontier_delta_steal_20261003.md \
 'They route on PREDICTED quality (learned preference routers, confidence' \
 'estimators). We route on MEASURED capability: chain-verified,' \
 'anti-cheat-scored agreement payloads from real production asks. Our'

chk Q2-steal-46-47 watch/inbox/frontier_delta_steal_20261003.md \
 '2. Their cascade as the routing rule: ds first, flash judge gate, frontier' \
 'on CHALLENGE - the gwap verdicts are the gate.'

chk Q3-econ-104-106 watch/inbox/ractor_engine/2026-10-03-surface-migration/economics.md \
 'sitting) carries only `frontier_*` and `flash_*` fields: **zero deepseek' \
 'rows**. The cheapest arm'"'"'s scores are absent from the register that the' \
 'routing rule reads, so "ds first" currently rests on price alone, with the'

chk Q4-grok-48-51 watch/inbox/GROK47_CLI_BURN_RECEIPT_20260925.md \
 'Attempt 2, same driver with tool use explicitly forbidden and' \
 '`reasoning_effort="low"`: OK. exit 0, end_turn, latency 120,125ms, cost' \
 '$0.02908224, usage 26,830 in (1,280 cache-read) / 5,206 out (4,110 reasoning),' \
 'model grok-4.7-build. Total spend all three calls: $0.08604924.'

chk Q5-econ-92-94 watch/inbox/ractor_engine/2026-10-03-surface-migration/economics.md \
 'credits do not. That asymmetry, not surface ideology, is the steering' \
 'placement rule: high-iteration steering loops (the A1 class: 49 re-fires at' \
 '$0.13-0.65/shot through the CASH lane) belong on the window-metered seat;'

if [ "$fail" -eq 0 ]; then echo "ALL QUOTES BYTE-VERIFIED"; exit 0
else echo "QUOTE CHECK FAILED"; exit 1; fi
