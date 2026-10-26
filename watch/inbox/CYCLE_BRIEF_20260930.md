# CYCLE BRIEF 2026-09-30 v1 (the steering surface)

## ANIMAL PROFILES (the fleet's own model knowledge at dawn -
memory/behavioral/animals/ distilled; a stale rib is a smell)
- claude_opus_5_5: 2 obs [pricex1, transportx1] newest 2026-09-30 sources=2
- deepseek_v4_1_flash: 1 obs [railx1] newest 2026-09-30 sources=1
- grok_4_7: 1 obs [verdictx1] newest 2026-09-30 sources=1
- ling_3_0_flash_sante: 1 obs [envelopex1] newest 2026-09-30 sources=1
- nous_primes_lane: 1 obs [railx1] newest 2026-09-30 sources=1
- qwen3_7_flash: 1 obs [failurex1] newest 2026-09-30 sources=1
- zai_coding_plan: 1 obs [envelopex1] newest 2026-09-30 sources=1

stale-row law: any animal whose newest ts predates the last
wave gets an observation mission below (ribs stay true).

## DOCTRINE SCORECARD (measured, not obeyed - doctrine_arbiter R10)
EXPIRED = named for retirement (operator gate; never auto-removed)
DOCTRINE SCORECARD 2026-09-30T23:20:04+00:00 (ledger C:\Users\foste\Documents\projects\local_sovereign_agent\memory\doctrine\LEDGER.jsonl, 3 item(s))
  rib-driving-ladder-duel  VINDICATED rib            duel_table.win_rate >= 0.55 [model=z-ai/glm-5.3-prime]
    vindicated 2026-09-30T23:17:15+00:00 | measured 0.6111111111111112 (2026-09-30T23:17:15+00:00)
  spec-parity-standing     VINDICATED spec_amendment parity_gate.parity_ok == True
    vindicated 2026-09-30T23:17:15+00:00 | measured True (2026-09-30T23:17:15+00:00)
  spec-anomaly-clean       PENDING    spec_amendment anomaly_counts.anomaly_count <= 0
    deadline 2026-10-07 | measured 98 (2026-09-30T23:17:16+00:00)
SUMMARY: VINDICATED 2 | EXPIRED 0 (retire candidates) | PENDING 1 | VOID 0 | RETIRED 0
## QUOTA LEDGER (HOLD/GO - the fleet self-throttles on this)
day verdict **RED** | live signal **AMBER**
```
# Quota ledger - 2026-09-30 (v0, harness-side instrument)
- Fires on the day: **349** (completed 300 / failed 34 / running 15); wall moments **7** (26 deaths coded 1302/1308)
- Current trailing-5h window: **61 fires**, 15 running, 1 walls in the last hour → current shape **AMBER**
- Peak rolling-5h window: **138** at 2026-09-30T12:28:48.146000+00:00; peak in-flight width **26** at 2026-09-30T00:38:52.179000+00:00
- Tokens (ROUGH): 714,810,462 recorded on 300 fires + 49 unrecorded × mean 2,382,701 ≈ **831,562,811** total (cache-inclusive, fire-time attributed)
```
**RECOMMENDATION: today's shape: 6-8-wide staggered (hold-line floor; day verdict RED) - STAGGERED, never at-once**

## CLIMB QUEUE (next 3 pitches from the execution order -
source: THE_LENSING section 4 PRIORITY ORDERING, the post-lensing reorder)
### 1. P6 THE STRANGER
- status: invite drafted NOT SENT (identity discipline: Adam's GitHub username unconfirmed): BLOCKED ON OPERATOR DOOR
- gate (lens, verbatim-order): Adam clones the-mountain at a tag and runs sovereign mode per PLAYER_ONE. Then one shared session over TLS with a pinned cert, with tape capture armed and identity bound by an SSH-key signature.
- evidence: LW2_ADAM_INVITE.md (watch/inbox/last_mile_20260930/)
### 2. P3 reduced
- status: artifact LANDED (mountain-e0ff8cec0.zip 28.9 MB); lensing demands tagged-commit rebuild + one clean-machine run receipt: OPEN
- gate (lens, verbatim-order): CI red-blocks on server tests. The zip is built from the tagged the-mountain commit, with one clean-machine run receipt. Ship via GitHub Release or itch butler. No custom delta rail.
- evidence: B5_BUILD.md (watch/inbox/last_mile_20260930/)
### 3. P2 re-scoped
- status: SRP6 port LANDED (B4, commit 066ba7ef0); lensing demands transport integrity + group/hash upgrade-or-retire: OPEN
- gate (lens, verbatim-order): Transport integrity first (TLS or K-bound frame MACs), then stranger-grade password handling. SRP6 group and hash upgraded or explicitly retired from this server path. Plaintext hello deleted in both 
- evidence: B4_SRP6_PORT.md (watch/inbox/last_mile_20260930/)

standing gates: paid asks fire only on operator GO (AA1 law);
the stranger door is an operator door (one Discord ask).

## OPERATOR GATES (human doors - machine burning does not clear these)
# GATE DIGEST: operator gates at one glance
Generated 2026-09-30 17:25 by `tools/gate_digest.py` (byte scan of receipts, mtimes,
configs; never hand-edit this file, regenerate it).
**OPEN 5 / CLOSED 1. Oldest open: Adam invite to the-mountain (no GitHub username) (0d 11h)**
## Open gates (each row is ONE operator action)
| # | Gate | Open for | Why blocked | The ONE action | Birth receipt |
|---|------|----------|-------------|----------------|---------------|
| 1 | Adam invite to the-mountain (no GitHub username) | 0d 11h | No GitHub username for Adam exists in the estate; both handle guesses (AdamCrigler, ItsCommodore) 404. An invite to a guessed handle would grant a possible stranger push access. Onboarding lineage since 09-24. | Ask Adam on Discord (ItsCommodore) for his GitHub username, verify it (gh api users/NAME), then: gh api -X PUT repos/NachoBusiness17/the-mountain/collaborators/NAME -f permission=push | `watch/inbox/last_mile_20260930/LW2_ADAM_INVITE.md` |
| 2 | ZAI_Pro key rotation (rides with the other 6 leaked keys) | 0d 9h | Seven live keys, incl. ZAI_API_KEY_Pro, were exposed in the steps.jsonl leak (audit finding #1); the on-disk leak copy persists and the backup repo holds copies. AG1 containment (untrack, redaction, pre-commit gate) protects future rows only; provider-side rotation is the operator-only real fix. | Rotate ZAI_API_KEY_Pro at the provider console and replace the value in .env; same for ALIBABA x2, VERCEL_KEY, HERMES x1/2, GROQ (audit finding #1) | `watch/inbox/last_mile_20260930/AG1_SECRETS_CONTAINMENT.md` |
| 3 | Nous portal check (402s vs ~$171 rib arithmetic) | 0d 3h | Prime models 402 on reservation while ribs say ~$171 of the $180/$220 pool should remain; the API has no balance endpoint. Only the portal separates old-account-402 from a genuinely dry pool. | Log into portal.nousresearch.com, read credits + top-up history for BOTH key pairs (repo .env pair, old SDD/NACHO pair) against the COST_TRUTH section 4 table; top up if dry | `watch/inbox/last_mile_20260930/AJ9_NOUS_402.md` |

## STEALTH TAIL (last 8 findings - triage targets)
- 2026-09-30T21:47:22 | openrouter | meta/muse-glimmer-30b | finish=stop cached=38 | findings register row; impfeed topic harvests STEALABLE ideas weekly (arch-03 D6 fix: no percolator/
- 2026-09-30T22:09:31 | hermes | ling-3.0-flash-sante:free (v | finish=stop cached=? | hermes-executed, tools capable
- 2026-09-30T22:15:51 | openrouter | stealth/space-bunny-alpha | finish=stop cached=128 | findings register row; impfeed topic harvests STEALABLE ideas weekly (arch-03 D6 fix: no percolator/
- 2026-09-30T22:21:32 | openrouter | inclusionai/ling-3.0-flash-s | finish=stop cached=0 | findings register row; impfeed topic harvests STEALABLE ideas weekly (arch-03 D6 fix: no percolator/
- 2026-09-30T22:27:12 | openrouter | meta/muse-glimmer-30b | finish=stop cached=38 | findings register row; impfeed topic harvests STEALABLE ideas weekly (arch-03 D6 fix: no percolator/
- 2026-09-30T22:46:30 | hermes | ling-3.0-flash-sante:free (v | finish=stop cached=? | hermes-executed, tools capable
- 2026-09-30T22:52:09 | openrouter | stealth/space-bunny-alpha | finish=stop cached=128 | findings register row; impfeed topic harvests STEALABLE ideas weekly (arch-03 D6 fix: no percolator/
- 2026-09-30T22:58:02 | openrouter | inclusionai/ling-3.0-flash-s | finish=stop cached=0 | findings register row; impfeed topic harvests STEALABLE ideas weekly (arch-03 D6 fix: no percolator/

## ANOMALY COUNTS (exit 1 = rows named below)
SURFACE steps C:\Users\foste\Documents\projects\local_sovereign_agent\memory\trajectory\steps.jsonl (38430 rows)
  [x] hash_shape: 1 row(s) violate [0-9a-f]{16} -> 6165 (step_hash=None)
  [x] malformed_json: 36 of 38430 rows -> 7176 (Expecting value: line 1 column 1 (char 0)), 7549 (Extra data: line 1 column 5 (char 4)), 7724 (Expecting value: line 1 column 1 (char 0)), 7801 (Extra data: line 1 column 406 (char 405)), 8036 (Expecting value: line 1 column 1 (char 0)), 10775 (Expecting value: line 1 column 1 (char 0)), 10820 (Expecting value: line 1 column 1 (char 0)), 13049 (Expecting value: line 1 column 1 (char 0)), 20833 (Expecting value: line 1 column 1 (char 0)), 23156 (Expecting value: line 1 column 1 (char 0)), 23181 (Extra data: line 1 column 2 (char 1)), 23192 (Expecting value: line 1 column 1 (char 0)), 23472 (Extra data: line 1 column 311 (char 310)), 23600 (Expecting value: line 1 column 1 (char 0)), 23715 (Expecting value: line 1 column 1 (char 0)), 24018 (Expecting value: line 1 column 1 (char 0)), 25109 (Extra data: line 1 column 5 (char 4)), 28379 (Expecting value: line 1 column 1 (char 0)), 29714 (Expecting value: line 1 column 1 (char 0)), 30373 (Extra data: line 1 column 2 (char 1)) (+16 more)
  [x] ts_non_monotonic: 1 descent(s) in 1 run(s) of 38430 rows -> 28456 (2026-09-28T17:03:53.648+00:00 -> 2026-09-28T17:03:53.647+00:00)
SURFACE oral_law_index C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\operator_model\ORAL_LAW_INDEX.jsonl (183 rows)
  [x] ts_sort: 60 descent(s) in 37 run(s) of 183 rows -> 2 (2026-08-30T16:27:16.6196893Z -> 2026-08-30T13:12:13.0401769Z), 4 (2026-09-04T16:39:59.3892627Z -> 2026-08-29T09:13:49.1755879Z), 6 (2026-09-01T00:09:09.5295017Z -> 2026-08-26T20:15:19.4956516Z), 8 (2026-09-08T10:46:49.2337564Z -> 2026-08-12T23:34:18.6503663Z), 12 (2026-09-01T17:38:41.9984068Z -> 2026-08-31T03:38:45.0312867Z), 13 (2026-08-31T03:38:45.0312867Z -> 2026-08-30T16:27:16.1730653Z), 14 (2026-08-30T16:27:16.1730653Z -> 2026-08-28T22:50:48.9529008Z), 16 (2026-09-05T19:42:08.3131854Z -> 2026-08-30T16:27:16.5784802Z), 17 (2026-08-30T16:27:16.5784802Z -> 2026-08-06T17:30:53.320314Z), 21 (2026-09-09T16:22:49.0876153Z -> 2026-08-31T03:38:43.3996981Z), 24 (2026-09-08T03:45:25.9172395Z -> 2026-08-29T13:25:18.237106Z), 26 (2026-09-02T00:34:18.519093Z -> 2026-09-01T03:36:47.8269474Z), 27 (2026-09-01T03:36:47.8269474Z -> 2026-08-06T11:19:13.9122686Z), 28 (2026-08-06T11:19:13.9122686Z -> 2026-08-04T12:33:28.6016188Z), 30 (2026-09-02T00:34:28.2877309Z -> 2026-09-01T03:37:52.525329Z), 31 (2026-09-01T03:37:52.525329Z -> 2026-08-31T03:38:44.6312725Z), 34 (2026-09-02T00:43:39.4883584Z -> 2026-08-30T01:56:10.026704Z), 35 (2026-08-30T01:56:10.026704Z -> 2026-08-29T13:18:15.907798900Z), 37 (2026-09-06T02:26:24.222212800Z -> 2026-08-29T08:33:17.129887700Z), 41 (2026-09-06T03:02:12.923433200Z -> 2026-09-05T19:29:25.923103100Z) (+40 more)
  [ ] dup_thread_id: 0 duplicated id(s) over 183 rows
SURFACE burns_ledger C:\Users\foste\Documents\projects\local_sovereign_agent\memory\burns\LEDGER.jsonl (693 rows)
  [ ] verdict_enum: rows=693 OTHER=14 REVIEW=89 fallback_unknown=0 -> 48 ('prereg gated; one red finding: shipped r'), 58 ('swept: UF-127 landed (honest self-flagge'), 59 ('56pct figure confirmed in RESEARCH_GAP_A'), 61 ('7/7 fixes hold at HEAD 77b887483, zero r'), 62 ('69 pending candidates triaged: 3 real (p'), 63 ('gap DISSOLVES, nothing owed: canonical d'), 65 ('close landed with count correction: brie'), 74 ('0/7 signals fired post-ledger (2026-09-1'), 84 ('simulation landed, live proof still owed'), 86 ('fire-ready with three amendments: scope '), 87 ('closed, no rebuild: watch/inbox/PROVIDER'), 89 ('card landed, nothing armed (card only pe'), 145 ('ATTRIBUTED to mechanism, writer named by'), 237 ('TEMPLATE LANDING ONLY, flip NOT executed'), 48 ('prereg gated; one red finding: shipped r'), 51 ('landed: 235 register events appended (wr'), 53 ('landed: grounding_chain f0e992d3e run li'), 56 ('landed: wave-2 audit FIX-1 (T42 endpoint'), 57 ('confirmed: all six region cosines (incl.'), 58 ('swept: UF-127 landed (honest self-flagge') (+83 more)
  [ ] evidence_paths: 0 missing, sample 50/693

## YESTERDAY
- synthesis: PRESENT (DAY_SYNTHESIS_20260929.md)
- receipts: see watch/inbox/last_mile_* newest

## MISSIONS (pre-written prompts for the mates' next cycle -
drawn from the sections above; the mates paste, they do not interpret)

### MISSION 1 - climb lane (STRANGER-PREP)
> PROMPT: "wire the instrumented first contact so it fires the moment the operator returns Adam's GitHub username: TLS stream with pinned cert on the authoritative server, server-side tape capture ARMED before connect, and SSH-key challenge verification against github.com/<user>.keys. Sources: THE_LENSING sections 4-5, LW2_ADAM_INVITE.md."
> FALSIFIER: a session tape whose challenge signature verifies against the published key, replaying byte-identically.
> RECEIPT: watch/inbox/last_mile_20260930/P6_STRANGER-PREP.md

### MISSION 2 - climb lane (BUILD-RAIL-REDUCED)
> PROMPT: "rebuild the artifact from a TAGGED the-mountain commit (not the roblox_to_godot twin), embed the commit sha in the artifact and print it at boot, bank ONE clean-machine run receipt (fresh machine, record SmartScreen/AV), ship via GitHub Release or itch butler. Sources: THE_LENSING sections 4-5, B5_BUILD.md."
> FALSIFIER: clean-machine run receipt naming the tagged sha; no custom delta rail.
> RECEIPT: watch/inbox/last_mile_20260930/P3_BUILD-RAIL-REDUCED.md

### MISSION 3 - climb lane (TRANSPORT-INTEGRITY)
> PROMPT: "close the auth debt the lensing named: TLS or K-bound frame MACs on post-auth frames, upgrade-or-retire the WoW 256-bit group + SHA1, delete the plaintext hello path in both trees. Sources: THE_LENSING sections 4-5, B4_SRP6_PORT.md."
> FALSIFIER: an on-path injection attempt FAILS and is named in a receipt; grep finds no live plaintext hello.
> RECEIPT: watch/inbox/last_mile_20260930/P2_TRANSPORT-INTEGRITY.md

### MISSION ANIMAL-OBSERVE - behavioral lane
> PROMPT: "the day recorded 7 wall moment(s) and day verdict RED: append one observation row per wall code to memory/behavioral/animals/ via tools/animal_profiles.py observe (kind=failure/envelope), every row citing its receipt source; contradictions with the rib go to memory/attention.md."
> FALSIFIER: animal_profiles --distill newest ts = today for every animal that hit a wall.
> RECEIPT: watch/inbox/last_mile_20260930/ANIMAL_OBSERVE.md
