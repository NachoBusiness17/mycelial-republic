# BREAK-ECONOMICS - hostile second pass on the economics lens (2026-10-03)

Run ractor_engine / 2026-10-03-surface-migration, break stage. Target:
economics.md (read whole this sitting, 166 lines). The ask's findings array
transmitted 4 findings and truncated the 4th mid-sentence; the banked file
carries FIVE findings plus verdict, falsifiers, and moves. I verdict the
banked file's five findings and flag the transmission loss.

Moment of this pass: census run ~20:33-20:41Z 2026-10-03. The lens's moment
was earlier: its census read 1,152 rows / $64.0464; mine reads 1,236 rows /
$64.2864 (driver.beat went cycle 1676 at 19:30:08Z to 1678 at 20:32:58Z
between the two moments). Both moments are named; no contradiction, the
census denominator law applies (memory/runs/hermes_burn/usage.jsonl is a
moving tree).

## Instruments (all run by me this sitting)

- Full-file census of memory/runs/hermes_burn/usage.jsonl via
  `.venv\Scripts\python.exe` json parse (script in %TEMP%, 1,236 rows, 0
  malformed): totals, per-model, per-day, per-id, GLM row dump, A1 stats,
  duplicate (id,turn) groups after 2026-10-02, doubled_key counts.
- Same instrument over memory/runs/route_chat/usage.jsonl (6 rows) and
  listings of memory/runs/model_garden (725-row usage.jsonl), gwap
  (arena-capability 314 rows), opencode_work (1 file).
- Reads: tools/hermes_burn.py, tools/instance_guard.py,
  mag/inference_budget.py, mag/route_chat.py, tools/tavern.py,
  queue/STANDING_RAILS.md, state/CURRENT.md, scripts/descent_driver.sh,
  watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md,
  .../accuracy.md:140-169, watch/inbox/instance_guard_20261002.md,
  watch/inbox/envelope_50w_20261003.md,
  watch/inbox/burn_claims_50wide_20261003.md,
  watch/inbox/frontier_delta_steal_20261003.md,
  watch/inbox/frontier_delta_register_20261003.json (whole),
  watch/inbox/last_mile_20260930/F1_FLASH_VS_MAX.md,
  watch/inbox/parable_day_one_20261003.md,
  memory/runs/opencode_work/work_20260826T052156Z.json,
  configs/providers.yaml (nous block, line 150).
- Scoped repo walks (skip .git/.venv/node_modules/__pycache__/corpus/
  dashboard/catalog/state/logs, files capped): greps for
  automation-b1ce1342, opencode, glm-5.3-max; regex 8-5|8:5|39-lane|39
  judged|winner|ds_chars|deepseek over watch/inbox/frontier* files and
  watch/inbox/frontier_asks/ (60 files); regex 582|9.5M|seat tokens over
  watch/inbox/*.md top level; GALA_DD_SELFSTEAL|substance_floor over
  tools/ scripts/ mag/ *.py; daily-cap shapes over tools/ scripts/
  configs/ queue/; driver.log DESCENT-DRIVER lines; attention.md
  doubled-key alarm lines; playground DONE spend parse; register field
  union + tallies.

## FINDING 1 (engine: GLM-5.3-max unproven, prime 2/7, opus $0.55/delivered) - CONFIRMED, two errata

Byte-checks that reproduce exactly:

- tools/hermes_burn.py:67 is `API_HOST = "inference-api.nousresearch.com"`.
- glm-5.3-prime: 7 rows / $1.6379 / 341,081 tokens, exact.
- glm-5.3-max rows in the hermes_burn ledger: 0 (full-file scan). Also 0 in
  the route_chat ledger (6 rows total, all 10-03 smoke tests, 13-238
  tokens: 5 deepseek-lane + 1 nous-lane failover smoke, the only rows that
  ledger has ever banked).
- GALA_OUROBOROS 10-02: 5 rows, 4x finish_reason=length, content_chars
  present on 3 (1, 1, 10), delivered on the 5th (STAGE_B, fr=stop). The
  arc cost $1.1739 for one delivered judgment (economics.md:34 is exact).
- 10-03 19:25:23.803Z row: completion 16000, reasoning_tokens 15998,
  content_chars 1; STAGE_B 19:33:24.686Z fr=stop content delivered. Exact.
- First-try content delivery across the 7 prime rows: 2/7 holds. The other
  five: two ok=false stubs (content_chars 1, the "STUB ... re-ask owed"
  note), two reasoning-dump channels with content_chars 1 and 10, one
  finish=length content-channel row the estate itself re-staged around.
- The 14-row opus design replay: my sum $7.7430 over 14 rows, $0.5531
  per delivered, matching the lens's $7.74 / $0.55. The topic brief's
  "~$13 for 14 asks at 37K tokens each" does NOT reproduce: the 14 rows
  carry 686,236 prompt+completion tokens, avg 49,017.

Errata (do not flip the finding):

1. The ask's compressed phrase "$1.17 per delivered judgment" splices two
   scopes. Banked file is precise: $1.174 is the 10-02 arc for one
   delivered (economics.md:34); lifetime is $1.6379 / 2 delivered =
   $0.82 per delivered.
2. The move names the wrong organ. plan_call lives at
   mag/inference_budget.py:262-281, not tools/hermes_burn.py. And the
   completion/thinking rail ALREADY EXISTS: the nous-primes FAMILY_TABLE
   row carries thinking_control {"reasoning": {"max_tokens": 6000}} with
   the "reasoning 6000 cap or the answer never gets written" note
   (mag/inference_budget.py:136-149). The actual defect is wiring:
   hermes_burn.py:344 computes plan (rail included) but _call builds the
   request body from model/messages/max_tokens only (tools/hermes_burn.py:112-116),
   so plan.extra_body is dropped on the floor. PRICING (hermes_burn.py:71-76)
   carries only anthropic models, so a GLM arm also needs a pricing row
   before _fire_ask will accept it (hermes_burn.py:289-290). claritas
   already maps glm to the zai face (mag/claritas.py:79).

Lens OWED answered by bytes it never read: watch/inbox/last_mile_20260930/
F1_FLASH_VS_MAX.md:4-5 "Nous lists no glm-5.3-max; z-ai/glm-5.3-prime is
the estate's proven top GLM rung ... the sanctioned max stand-in". The
thesis's named engine is not a Nous model id per the estate's own 09-30
probe receipt. And F1's own duel data (flash swept prime 4-0 at 19.3x
cheaper, F1:39,85) says the GLM re-arm candidate is glm-5.3-flash, whose
uncap law is already in FAMILY_TABLE (inference_budget.py:119-135), not
prime alone.

## FINDING 2 (re-fire was the dominant cash failure, now guarded) - CONFIRMED; the MOVE is dead (organ already exists and is firing)

Reproduced exactly: SYNTHESIS.md:17-27 ($25.5316 of $37.7591, 67.6%, A1 49
refires, 13 twin keys after _landed_skip); my A1 re-derivation = 52 rows /
$21.8518 / avg $0.4202 / all anthropic/claude-opus-5.5 / ts 13:11:41Z to
20:17:25Z on 10-01; state/CURRENT.md:21-24 (instance_guard swept to 5
surfaces; driver bounced, pid 86854, exit-3 proof claimed);
scripts/descent_driver.sh:10-23 carries the pidfile guard bytes (note: the
bash guard is check-then-write, the accepted last-wins window is
documented at tools/instance_guard.py:83-86); STANDING_RAILS.md:17-18 law
3 interrupts-never-cancel, dated 2026-10-03, and parable_day_one_20261003.md:16
banks the 17:00 interrupt that killed the 50-wide wave.

The move ("add a (id,turn) uniqueness tail-check in tools/hermes_burn.py
_bank that alarms on the second non-zero row; 30 min") proposes an organ
that is already in the tree and already in production: tools/hermes_burn.py:153
calls doubled_key_check (tools/instance_guard.py:191-213, tail-bounded at
ledger_key_exists:170-171, alarms into memory/attention.md). It fired 850
times today: 850 ledger rows carry doubled_key=True ($15.2784), 850 alarm
lines sit in memory/attention.md (latest 20:29:15Z).

The lens's own falsifier ("a duplicate non-zero (id,turn) pair dated after
2026-10-02 reopens the finding") technically FIRES: 85 duplicate groups,
all one class - TAVERN ids. tools/tavern.py:157 builds ids as
TAVERN_r<rnd>_<actor> with no run stamp and banks turn=1 (tavern.py:124-126),
so every new run collides with every older run's keys; up to 15 fires of
TAVERN_r2_Pell Quickfinger. This is intentional play spend with a colliding
key namespace, not the A1 re-fire class, but it floods the alarm channel
(850 alarms/day) so a real re-fire hides in noise. The finding's history
stands; the residual money work moved from "build the tripwire" to
"scope the play-lane key namespace".

## FINDING 3 (runway ~1 week, play 65%, meter split) - WEAKENED: the balance premise is contradicted by the estate's own probe receipt

Reproduced exactly: 10-03 TAVERN 665 rows / $16.2003 / 3,377,258 tokens;
tools/tavern.py:223 `--budget-usd` default 5.0; envelope_50w_20261003.md:21,24
(50/50 returned, ~1.0M subagent tokens) and burn_claims_50wide_20261003.md:40
("~1.5M subagent tokens, $0 cash (seat tier)"); SYNTHESIS.md:19-21 (A1 49
refires at $0.13-0.65; my min is $0.1215, a rounding nit).

Weakened:

1. The $180 premise. The lens priced runway off the AGENTS.md driving-
   ladder line and marked the balance OWED. The dogfood-48h run's own
   accuracy receipt already banked the answer: "Nous 'live balance
   $47.54' is probe-true at 00:27:53Z and stale after the night's later
   spend" (watch/inbox/ractor_engine/2026-10-02-dogfood-48h/accuracy.md:155-156).
   My ledger diff: hermes rows after 2026-10-02T00:27:53Z = 1,000 rows /
   $26.5273. If that probe read the same keychain's remaining balance, the
   runway is roughly $21, under one day at the 10-03 pace, not ~7 days.
   Conditions: the probe's instrument and keychain are not re-verified by
   me (F1's duel rode a separate NOUS_SDD_API_KEY, F1:12), and $47.54
   could be spend-to-date semantics. Live re-probe is the single
   highest-value OWED item in this report; it gates the whole cash-rail
   side of the hybrid.
2. "38 playground run dirs today averaging ~$0.43/run": at my moment the
   playground holds 42 dirs (41 named 20261003); only 16 carry DONE files
   with parseable spend, and those 16 sum to exactly $16.2003 (avg
   $1.0125/run). The $0.43 figure is back-derived over a dir count that
   includes empty and in-flight runs. The conclusion (tavern dominates
   the day) is untouched; the per-run number is not instrument-backed.
3. Minor: the ledger's own heaviest day is 10-01 at $37.7591, so
   "$25.11/day pace" quotes the lightest of the three days.

New byte the lens missed both ways: parable_day_one_20261003.md:13 banks
"the $25.11 cap, held to 35 cents" (the estate-level daily cap the lens
marked OWED). But my census reads the 10-03 hermes day at $25.3534 through
20:30:13Z, above the named cap figure, and I found no cap enforcement in
tools/ scripts/ configs/ queue/ (grep scope above). Cap semantics (what it
meters, what breached it) are OWED.

## FINDING 4 (the register cannot price its default rung) - CONFIRMED (the ask truncated this finding mid-sentence; the banked text at economics.md:98-111 is what I verdict)

Byte-true: watch/inbox/frontier_delta_register_20261003.json read whole,
14 rows, field union exactly {id, frontier_chars, frontier_cites,
frontier_unver, flash_chars, flash_cites, flash_unver, contract_parts} -
zero ds_* fields, zero winner/win-rate, zero cost fields of any kind.
watch/inbox/frontier_delta_steal_20261003.md:30-31 ($0.14 per deepseek
arm) and :44-50 (adopted cascade "ds first, flash judge gate, frontier on
CHALLENGE") verified.

Absence claims re-run with my own instrument: regex (8-5|8:5|39-lane|39
judged|winner|win_rate|ds_chars|deepseek, case-insensitive) over the 13
watch/inbox/frontier* FILES plus watch/inbox/frontier_asks/ (60 files):
no 39-lane or 8-5 tally banks anywhere in either. The only banked judge
tally in the estate is different from both the topic's and the lens's
numbers: STANDING_RAILS.md:49-50 "The Delta Register judge pass completes
(30/50 lanes landed, ~20 killed by the interrupt before the no-cancel law
landed)". The lens missed that line.

Sharper than the lens put it: the register's own fields undercut the
frontier arm's dominance. frontier_chars > flash_chars in only 10 of 14
rows, and flash carries FEWER unverified citations in 13 of 14 rows
(frontier_unver < flash_unver in exactly 1 of 14). Whatever the unbanked
8-5 tally said, the banked fields show flash winning the citation-hygiene
axis nearly across the board. "Ds first rests on price alone" stands, and
"frontier on CHALLENGE" rests on an unbanked tally.

## FINDING 5 (hybrid is today's steady state; seat burn unbanked) - CONFIRMED with one evidence sentence KILLED

Confirmed: driver.beat = 2,742 lines, first BEAT 2026-10-01T21:31:24Z
cycle=1, last BEAT 2026-10-03T20:32:58Z cycle=1678, and
state/descent_driver.pid holds 86854 (matches CURRENT.md:23-24); driver.log
tail shows live cycles ("HERMES-BURN: PASS - 28/28 asks; ledger total
$64.29"). The topic's "ran all night unattended past cycle 1600" is
byte-true. The unbanked-seat claim reproduces under my instrument: regex
(582|9.5M|seat tokens) over watch/inbox/*.md top level = 56 hits, all
unrelated numeric substrings except the steal doc's numberless phrase at
frontier_delta_steal_20261003.md:31. The 9.5M / 13 / ~582K numbers bank
nowhere in the bytes I searched; they are topic-given.

KILLED sentence: economics.md:126-127 "no repo reference to
automation-b1ce1342 exists - grep over the repo returned empty". My scoped
walk (top-level md + configs/ docs/ mag/ tools/ queue/ scripts/ memory/
watch/, files<3MB) hits 14 files, including watch/inbox/
parable_day_one_20261003.md:9 ("the hourly arena cron, 8 cycles,
automation-b1ce1342"). The receipt that names the cron also names the cap
(:13) and the 121 chain-verified agreement rows from 23 play sessions
(:10). The cron's width/model/cap ARGUMENTS still live outside the repo
(no in-repo enforcement found; grep scope above), so the lens's deeper
point survives in weakened form: the id is referenced, the mechanism is
not banked.

## ADDITIONS (what the lens missed)

1. The runway number is ~$21, not ~$180/1-week. accuracy.md:155-156 banks
   the $47.54 probe at 2026-10-02T00:27:53Z; my ledger diff shows
   $26.5273 spent since. Falsifier: a fresh balance probe reading
   materially above ~$25 remaining, or proof the $47.54 was
   spend-to-date. Move: one balance probe banked in the dawn report,
   10 min; it decides whether the cash rails run at all this week.
2. The GLM fix is a one-line wiring fix, not a new floor: send
   plan.extra_body through hermes_burn._call (tools/hermes_burn.py:112-116,
   344-345) plus a z-ai/glm PRICING row; the 6000 rail already exists at
   mag/inference_budget.py:139 and claritas already knows the face
   (mag/claritas.py:79). The GALA GLM rows were banked by a producer
   script that greps empty in tools/ scripts/ mag/ (unlanded), so the
   fix has no existing home in the play path; the rails path is the
   place. Falsifier: a hermes_burn-fired GLM row with reasoning_tokens
   <= 6000 and finish=stop. Move: 30-45 min, then the staged arm.
3. The stage arm should be glm-5.3-flash, not prime-only: F1
   (last_mile_20260930/F1_FLASH_VS_MAX.md:39,85) already swept prime 4-0
   at 19.3x prime's cost, and the flash uncap recipe is tabled
   (inference_budget.py:119-135). Falsifier: prime beating flash on the
   staged arm, or a Nous model list containing glm-5.3-max. Move: same
   sitting as addition 2, zero extra cost.
4. The doubled-key tripwire is live and flooded: 850 alarms / $15.2784
   flagged on 10-03 because tavern ids carry no run stamp
   (tools/tavern.py:124-126,157). The lens's move 2 is already built
   (tools/hermes_burn.py:153 + tools/instance_guard.py:191-213). Real
   move: run-stamp the tavern ids (TAVERN_<stamp>_r<N>_<actor>), 15 min,
   then one cron-day watching for a clean alarm channel.
5. The register's banked fields already argue against frontier dominance:
   flash has fewer unverified cites in 13/14 rows, frontier wins chars in
   only 10/14, and the only banked judge tally is 30/50 lanes
   (STANDING_RAILS.md:49-50), not 39 or 8-5. Falsifier: the 30 landed
   judge rows scored with a winner column showing frontier winning
   citation hygiene. Move: extend the lens's ds_* move with winner +
   unver-delta columns from the 30 landed lanes, 45 min.
6. The topic's 16x window-token ratio is unbanked arithmetic whose ledger
   side measures differently: the 14 opus design rows carry 686,236
   tokens (avg 49,017, not 37K), so even granting the unbanked 582K seat
   operand the ratio is ~11.9x, and the 582K itself banks nowhere (grep
   scope above). Falsifier: the lens's move 3 (usage_seat.jsonl) banking
   >= 500K window tokens per deliverable. Move: the lens's move 3
   stands; treat 16x as OWED until then.

## OWED (never asserted by this pass)

- Live Nous balance: not probed (the $47.54 figure is probe-true only at
  its own moment per accuracy.md:155-156; keychain identity not re-verified).
- Arena cycle count ("8 cycles"): receipt-backed at
  parable_day_one_20261003.md:9 but not re-counted by me;
  arena-capability.jsonl (314 rows) carries ts_utc nested in payloads my
  census did not parse.
- The GALA GLM producer script: not located in tools/ scripts/ mag/
  (grep scope stated above); possibly an unlanded seat-inline script.
- The $25.11 cap: semantics and enforcement location unverified; the
  10-03 hermes day reads $25.3534 through 20:30:13Z against the named
  cap figure.
- The 39-lane / 8-5 tally: not found in frontier_delta files nor
  frontier_asks/ (60 files); watch/inbox/frontier_olm_*/ dirs not searched.
- The deskinned 9.5M / 582K seat-burn operands: banked nowhere I searched.
- usage.jsonl is a moving tree: 1,152 rows / $64.0464 at the lens moment,
  1,236 / $64.2864 at mine; per-model counts drift accordingly (fable
  rows +9 at $0.00 marginal, the zero-cost DND0 stub rows).

Filed by break-economics, hostile second pass, 2026-10-03. Zero em-dash
bytes.
