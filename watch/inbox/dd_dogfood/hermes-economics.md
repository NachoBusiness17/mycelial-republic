# HERMES BURN ECONOMICS - the full-ledger audit (GALA dd-selfsteal, hermes-burn-economics lane)

Moment pinned: 2026-10-03T19:24:20Z, ledger `memory/runs/hermes_burn/usage.jsonl` at 1,150 rows,
newest row ts 2026-10-03T19:08:04Z. The ask said 1,099 rows; that was a live-tree snapshot from
~18:55Z this session (the playground driver kept firing while this audit ran: 1,099 at the first
read, 1,149 at the second probe, 1,150 at the pin). All numbers below are from the pinned 1,150-row
read; the raw instrument output is `watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-burn-economics.check.txt`
(script: `hermes-burn-economics.analysis4.py` in the same dir; earlier probes kept as
`hermes-burn-economics.check2.txt` / `check3.txt`).

## Headline

- Total billed: **$63.5824** over 1,150 rows (prompt 6,549,546 + completion 2,207,640 + reasoning
  1,570,233 = 10,327,419 tokens).
- Total quantified waste: **$25.9998 = 40.9 percent** of everything billed.
- Goodput (definition: total minus quantified waste): **$37.5826 = 59.1 percent**.
- Usable-finding units (definition: a landed deliverable): 90 hermes_burn ask outputs (95 md files
  minus 5 DAY1_*/_ASSEMBLED meta receipts) + 38 playground run receipts (16 tavern + 22 dnd0 dirs,
  each with transcript.jsonl + play.md/session.md; 35 carry DONE, 33 carry GWAP_BANKED, 3 dnd0 runs
  have no DONE) + 1 ouroboros lane = **129 units**.
- Cost per usable finding: **$0.4929 gross**, **$0.2913 productive-only**.
  (The check.txt line reads 130 units / $0.4891 / $0.2891 because the instrument counted a
  non-run `.mimosa` scanner dir inside watch/inbox/playground/; corrected here to 38 run dirs.)

## Where the money went

Per day: 10-01 **$37.7591** (236 rows; the T1 stranger-audit + duels day), 10-02 **$1.1739** (5 rows;
the GLM ouroboros judgment asks), 10-03 **$24.6494** (909 rows; the ARENA DAY playground arc).

Per model (cost / rows / ok): opus-5.5 $45.6479 / 447 / 336; fable-5.1 $8.2186 / 172 / 98;
sonnet-5.5 $7.5932 / 308 / 255; glm-5.3-prime $1.1739 / 5 / 3; haiku-4.5 $0.9488 / 218 / 218
(haiku: zero failures all day - the only model that never missed).

Per plan family (top, cost / rows / distinct ids): A1 $21.8518 / 52 / 1 (one ask, 52 fires);
PLAYGROUND(tavern+dnd0) $16.9064 / 895 / 86; T1W1 $2.7438 / 4; DUEL2 $2.4329 / 40 / 28;
SUBSTANCE $2.2034 / 4; B2 $1.4796 / 6 / 1; C1 $1.4664 / 6 / 1; GALA $1.1739 / 5 / 3; T1W2 $1.1465 / 11 / 4.
Full table in the check file.

## The waste ledger ($25.9998)

1. **A1 stale-force-flag re-burn theater: $21.0932** (81 percent of all waste).
   `A1_steer_antiforgery` turn-1 fired 49x ($20.9891, first fire $0.3880 at 13:11:41Z) and turn-2
   3x ($0.8627) on 10-01, all ok=true, one landed deliverable. 50 post-producer fires are pure
   re-burn. Matches the documented disease (tools/hermes_burn.py:55-58 "A1 45x at $20.53 after
   landing"; DAY1_RIB_WARMTH.md:91-112). Closed by CARRIER-PATCH 1 (landed beats force).
2. **The descent-driver twins: $1.1292 actual double-spend** (byte-verified, see next section).
3. **Other queue re-fires: $3.3057**: B2_drift_rows_attribution 6 fires (+$1.2330),
   C1_censorship_mechanisms_crossfamily 3+3 fires turn1+turn2 (+$1.0582), T1W2_S5/S6/S7/S8
   repeats (+$0.1658/$0.1221/$0.2073/$0.5193). Caveat: T1W2_S8_stealth's true producer was its
   fire3 ($0.5193, content channel, 2,536 completion tokens; the landed file is 3,145 bytes);
   fire2 was an ok-marked empty-content fire ($0.0035). The producer rule books fire3 as waste,
   so S8 waste is overstated by at most $0.5158 (true S8 waste: $0.0035).
4. **Billed failures: $0.4717**: two z-ai/glm-5.3-prime STUB rows on 10-02 (finish_reason=length,
   ~20k completion tokens bought content_chars=1; $0.2213 + $0.2304, rows carry the "STUB: content
   under substance floor" note) + three in-run DND0 opus retries ($0.0200).

Not counted as waste (verified, not assumed):

- **Playground run-collision repeats: 665 fires / $14.9034 - productive spend, ledger-blind.**
  The 895 TAVERN_/DND0_ rows repeat only 86 ids because `tools/tavern.py:157` emits
  `f"TAVERN_r{rnd}_{p['name']}"` while its own docstring (tools/tavern.py:10) promises
  `TAVERN_<run>_r<round>_<actor>` - the run identifier is dropped, so every run re-collides on the
  same ids. Each fire is a distinct game run with its own receipt dir (transcript + play receipt),
  so the money bought real play, but the ledger cannot tell runs apart.
- **89 refused rows: $0.0000** (verified: N1_parables_songmap 42 rows + DUEL1_hidden_5 46 rows +
  T1W2_S8 1 row all sum exactly $0). The cost was >2h of driver retry time (documented
  tools/hermes_burn.py:173-177), closed by CARRIER-PATCH 2 (refused is terminal).

## The descent-driver twins, byte-verified against e3c7d341c

Commit e3c7d341c claims: "two same-second descent-driver twins (PIDs 54504+40632, born 20:40:13Z)
double-drained the shared hermes_burn queue ~12h (13 doubled keys, $2.25 vs $1.09 real)".

Ledger bytes at the pinned moment confirm it exactly: the 13 doubled keys are
DUEL2_train_{02,03,04,05,06,08,09,10,11,12,13,14}_r2 (12 keys; 07 never doubled) plus
N1R_parables_songmap - each fired twice, the second fire 1-59s after the first, all between
21:40:20Z and 21:54:04Z on 10-01, inside the twins' lifetime. Both-fires sum **$2.2521**
(documented $2.25); single-pass real **$1.1229** (documented $1.09); the actual double-spend
waste is **$1.1292**. The ask's "$2.25" is the both-fires total; the true excess is half of that.

Cross-check on the day-1 window: this audit reads 10-01 = $37.7591 and non-playground re-fire
waste = $25.5281 - the instance_guard receipt (watch/inbox/instance_guard_20261002.md:26-27) says
"$25.53 of the window's $37.76 was re-fire excess". Two independent instruments, same bytes.

## Which plans produced receipts, which produced nothing

172 distinct ask ids were paid. 170 landed a receipt somewhere: 81 as watch/inbox/hermes_burn/
outputs, 86 as playground per-run receipt dirs, 3 as the GALA ouroboros lane
(watch/inbox/gala_20260925/ouroboros/). Exactly two ids never landed:
`N1_parables_songmap` and `DUEL1_hidden_5` - both refusal-terminal at $0.00 billed, both re-armed
and landed under new ids (N1R_parables_songmap.md, DUEL1_hidden_5_r2.md). **No paid ask lineage
ended with nothing.** Every dollar of waste in this ledger is duplication (re-fires of landed
asks) or hollow-ok failures, not orphaned work.

## Open defect this audit hands forward

The remaining live ledger bug is not a money leak, it is ledger integrity:
`tools/tavern.py:157` (and its dungeon twin) drops the run id from the banked ask tag, so
809 of 1,150 ledger rows carry `doubled_key: true` and 809 false INSTANCE-GUARD alarms spam
memory/attention.md (counted by grep at the pin). Any economics query over this ledger is wrong
without the collision adjustment; the ingest tripwire (tools/instance_guard.py:191) is blinded by
false positives. Fix shape: include the run id in the tag at tavern.py:157 and the dungeon
equivalent, one line each; the playground driver was still firing at the pin moment (newest row
19:08:04Z), so the row count and alarm count are already stale by the time this file is read.

## Decision ledger

Closes: the descent-driver-twins double-spend question. Quantified: the twins cost $2.2521 billed
for $1.1229 of real work ($1.1292 excess), and the total hermes_burn ledger waste is $25.9998 of
$63.5824 (40.9 percent), dominated by the A1 force-flag hole ($21.0932) that CARRIER-PATCH 1
already closed; post-patch days (10-02, 10-03) show zero non-playground re-fire waste. Changes:
the honest cost-per-usable-finding baseline for the descent protocol's spend-theater falsifier is
$0.29 productive ($0.49 gross), and the next money-adjacent fix is the tavern/dungeon run-id tag
collision (ledger integrity), not another driver guard.

Filed by the hermes-burn-economics lane, 2026-10-03. No em-dash bytes. Instrument: read-only
python over the ledger + directory censuses; no estate files modified outside the lane's own
archive dir and this receipt.
