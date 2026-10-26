# MORNING TRIAGE - 2026-10-17 (three ghosts, one riddle, the fabric holding)

Classification: RECEIPT (triage)
Producer: zcode-seat-20261016
Commission: the fleet's morning report + "Now what go" + the Lilith drop.

## GHOST 1: the janitor crash-loop (chain noise, $0, every few minutes)

The chain rows are minted by session **autonomous-auto-fkb** (theme
autonomous_janitor) inside a container - each knot has start_minute ==
end_minute (empty runs, crashing instantly on the missing PowerShell). The
session id is the selffeed/fkb organ: the arch-03 design bounded it with 7
rails INCLUDING a 3-fail circuit breaker - the breaker was never wired in
the container's copy. THE FIX: disable the fkb/selffeed job in the
container (the container is Linux; the job is a Windows-ism), or wire the
breaker. Staged for the container owner's pass - the job is identified,
the cure is one config line.

## GHOST 2: the law pack, 9.6 days stale (the compile fails DAILY)

Root cause found in logs/lawpack.log: the lawpack task's compile step -
tools/thought_quantizer.py compile - runs **949 seconds and exits 1**,
every day. The min-rows refusal then keeps the good old pack serving
(correct design: stale-but-good beats empty). The pack isn't broken; the
QUANTIZER is. The diagnosis (what the compile compiles, why it fails at
exit 1 after 15 minutes) is staged as the incident - the daily ALERT rows
are the noise until it's fixed.

## GHOST 3: the paid DeepSeek 8 PM caller - UNIDENTIFIED from estate logs

The drainer's own alarms tell the real story: ZAI_API_KEY_Lite missing,
deepseek prefix drift on the lanes, and **provider_usage.jsonl silent
1288 minutes** - the drainer's provider meter is dead and its 64 done
tasks show ZERO deepseek/openrouter usage. So the 8 PM paid-DeepSeek
labeling was NOT the drainer, and the estate-side logs don't carry it.
The identification needs the DeepSeek account's own usage page (the API
dashboard shows which key called at 20:00) - operator-readable in one
click. Named, not guessed.

## THE LANES (the fleet monitor's report, verified where checked)

- Free-lane fleet: 3 of 7 cloud lanes answering (Mistral, one NVIDIA key,
  local qwen2.5). Consistent with the stolen OpenRouter guidance: the
  free-tier daily caps (50/day on unfunded accounts) exhaust and the
  endpoints go dark until the UTC roll. The paid-tier key holds 1,000/day
  (946 remaining at last check) and answers - the miner rides it.
- Gauntlet: idle is CORRECT (all 18 trials graded - the trials queue needs
  feeding, not the gauntlet).
- Hermes burn skipping every ask at $0: correct (landed-beats-force - the
  queue is drained; the wide root feeds on the next mints).
- Backup, corpus rescan, news: all succeeded overnight.

## THE DROP

@LilithDatura, five words: **"Nobody ever reads the firmware."** Banked in
her palace (known_facts 6 -> 7): the firmware-as-base-layer riddle, landed
the same morning the triage was literally about unread base layers - a
stale law pack nobody re-derives, a ghost janitor nobody sees, a meter
silent for 1,288 minutes. The drop was the triage's thesis statement,
posted before the evidence. Her drops register keeps the score.
