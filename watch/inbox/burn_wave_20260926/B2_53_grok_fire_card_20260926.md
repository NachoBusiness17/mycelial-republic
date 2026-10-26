# FIRE CARD B2-53: GROK_LANE_PACKET_20260925.md (card only, nothing sent)

## Verdict

FIRE, with three amendments before GO. (1) Scope to Asks 2-4 only: Ask 1 already
ran on the Grok 4.7 seat 09-25 and landed (INTERFERENCE_PREREG_ADVERSARIAL_
GROK47_20260925.md, VERDICT UNSOUND). (2) Attach the reading-list source
(memory/corpus/LINKS.jsonl:32, LINKS-283) to Ask 3: the packet's "LINKS rows"
resolve to zero rows in watch/inbox/LINKS.jsonl and its fallback
memory/live_from_grok.md is a telemetry stub. (3) Date-bound Ask 4 to the
20260925-dated set (37 files), not "about 20": today's census is 52.
Destination: harness/grok_cli.py -> cli-chat-proxy.grok.com, model grok-4.7-build,
the seat with a proven execution receipt on file. Timing: today is Saturday
2026-09-26 and the packet says "last burns Sat night"; the close receipt says
window ends ~09-28. If Sat-night stands, tonight is the fire.

## Evidence

- GROK_LANE_PACKET_20260925.md:3 "For the Grok 4.7 50%-off seat (window ends
  ~09-28; last burns Sat night)."
- Packet Ask 1 context is stale on its face: INTERFERENCE_REPLICATION_PREREG_
  AMENDMENT1_20260925.md:12-13 "At budget 200: one-line 70% (21/30, matches
  their published 21/30 exactly)... interference 100% (30/30, matches published
  exactly). ARM B VERDICT: PASS" (matches packet:14-15).
- Ask 1 ALREADY FIRED: INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md:7-9
  "Path: grok CLI harness (harness/grok_cli.py, headless) ->
  cli-chat-proxy.grok.com... Model: grok-4.7-build | cost $0.02908224"; :45
  "VERDICT: UNSOUND". Chore line names Stone 5.1.
- Packet still owed: BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:56 "Grok seat
  packet (stone 5) awaiting the Grok window (ends ~09-28)."
- Arm C state moved since the packet: close:13-14 "ARM C budget-200: RUNNING,
  1/30 with the first problem SOLVED"; :54-55 completion still open. Any refire
  must restate current Arm C state.
- Ask 2 context byte-true: watch/GAUNTLET_W4_VERDICT_20260925.md:15 "n=10 valid
  trials/arm vs the preregistered >=50"; :16 "40/60 rows carry
  model=\"DEEPSEEK_API_KEY\"". Byte-check: watch/gauntlet_w4_receipts.jsonl is
  exactly 60 lines with exactly 40 DEEPSEEK_API_KEY matches. Watch/
  GAUNTLET_PREREGISTRATION_20260901.md exists.
- Ask 3 pointer defect: watch/inbox/LINKS.jsonl has 0 rows matching
  FlashREINFORCE, 2410.02197, 2505.17508, or 2609.15987. Source actually at
  memory/corpus/LINKS.jsonl:32 "Frontier RL recipes revealed: FlashREINFORCE...
  GPO 2410.02197 + RPG 2505.17508 + BPO 2609.15987" (one row, not "rows").
  Fallback memory/live_from_grok.md is 17 lines of session telemetry ("Last
  prompt preview: (none)").
- Ask 4 scope drift: packet:32 "about 20 files"; census 2026-09-26 = 52
  BURN_*/SEED_SALON_* files (37 dated 20260925, 14 dated 20260926, none 09-24).
- No answers exist: no GROK_W4_RERUN_PROTOCOL, GROK_OCTOBER_FOLD, or
  GROK_BURN_AUDIT file anywhere in watch/inbox (ls grep empty).

## Work done

Read the packet whole (35 lines). Read all four cited files whole (prereg 61,
amendment 35, W4 verdict 27, live_from_grok 17). Read the Stone 5.1 Grok output
whole (50) and the close receipt whole (61). Byte-counted the gauntlet receipts
(60 lines, 40 matches). Grepped both LINKS ledgers for the four recipe ids.
Census-counted BURN_*/SEED_SALON_* files. Confirmed harness/grok_cli.py exists.
Verified the weekday by date command (Saturday). Confirmed no prior answer
filings.

## Falsifier

This card is wrong if: (a) a GROK_W4_RERUN_PROTOCOL_2026*, GROK_OCTOBER_FOLD_
2026*, or GROK_BURN_AUDIT_2026* file exists in watch/inbox (packet already
fired; verified none as of filing); (b) memory/corpus/LINKS.jsonl:32 does not
carry the three arxiv ids (then Ask 3 has no on-disk source and files as owed
instead of firing); (c) the close receipt's Arm C line flips from RUNNING to
complete before fire and the fire ask still carries the stale "running"
context. Any hit: re-card, do not send.

## Bibliography closed

watch/inbox/GROK_LANE_PACKET_20260925.md (35 ln); watch/inbox/INTERFERENCE_
REPLICATION_PREREG_20260925.md (61); INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_
20260925.md (35); INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md (50);
BOOT_LANE_INTERFERENCE_BURN_20260925.md (Stone 5 block); BOOT_LANE_INTERFERENCE_
BURN_CLOSE_20260926.md (61); watch/GAUNTLET_W4_VERDICT_20260925.md (27); watch/
gauntlet_w4_receipts.jsonl (60 rows, counted); watch/GAUNTLET_PREREGISTRATION_
20260901.md (existence); memory/live_from_grok.md (17); memory/corpus/LINKS.jsonl
:32; watch/inbox/LINKS.jsonl (grepped); watch/inbox BURN_*/SEED_SALON_* census.
Nothing sent. Card only.

## GATE SURFACE MIGRATION (B2-425, 2026-09-26T20:47Z)

The "three amendments before GO" gate now has a canonical check:
watch/inbox/OPERATOR_GO.jsonl read via `python tools/operator_go.py
grok-lane-packet` (exit 0 = GO on file with source_transcript; exit 1 =
NO-GO-on-file, the current state). FIRE executes only on exit 0, with the
three amendments attached regardless.
