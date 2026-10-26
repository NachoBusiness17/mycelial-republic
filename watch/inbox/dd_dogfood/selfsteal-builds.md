# SELF-STEAL 24H BUILDS - what the estate built in the last 24 hours

Lane: selfsteal-24h-builds (GALA division B) - moment 2026-10-03T18:41Z local 14:41 EDT.
Window: 2026-10-02T18:41Z through 2026-10-03T18:59Z (24h). Purpose: the estate's own prior
art for the next build cycle. Every number below was read or computed in this lane's session;
commands are named so any seat can re-run them.

## METHOD (what was read/run)

- `git log --since="2026-10-02T14:41:00-04:00" --shortstat` - 7 commits, 217 files, 15,998
  insertions in window. NOTE: the tree moved under this lane mid-inventory - commit
  53f56d0f3 (2026-10-03T14:53:12-04:00, SACRED COW FELL) landed while the lane was reading
  and modified build #1 below; the receipt reflects the post-53f56d0f3 bytes.
- Full read of the five new code files: `mag/route_chat.py`, `tools/dungeon.py`,
  `tools/tavern.py`, `tools/arena_gwap.py`, `tools/grok_burn.py`, plus `queue/STANDING_RAILS.md`.
- Usage-ledger window accounting over `memory/runs/{hermes_burn,xai_grok,route_chat}/usage.jsonl`
  (python one-liner, ts-parsed, window-filtered).
- DONE-file spend sums over `watch/inbox/playground/*/{DONE}` (awk).
- Window file counts: `find watch/inbox -type f -newermt "2026-10-02 18:41"`.
- Fleet lane trails: per-lane grep for 2026-10-02T2x/2026-10-03T rows.
- Negative checks: `grep -rln route_chat mag/ tools/` (consumers), `schtasks //query` (arena
  cadence), tests coverage grep.

## THE BUILDS (code, tools, configs, protocols - the prior art)

### 1. mag/route_chat.py - the ONE front door for model calls (176 lines, NEW; amended by 53f56d0f3 mid-window)

- Does: resolves lane+model from `configs/providers.yaml` + `mag.model_pick` by goal; enforces
  the dormant-lane gate (B2-133) unless operator GO (`mag/route_chat.py:113`); endpoint fence
  (https + allowlisted host + resolved-IP refusal of private/loopback/link-local/reserved/
  multicast, `mag/route_chat.py:71`); openai-compat call with fail-loud retries; banks every
  call to `memory/runs/route_chat/usage.jsonl` (`mag/route_chat.py:82`, call body at `:88`).
- Mid-window amendment (53f56d0f3, "SACRED COW FELL"): a `depth` flag - "mechanical" default
  keeps the deepseek thinking-off law (AH10, batch-proven); "design" enables thinking
  (`mag/route_chat.py:132`), on the sacred-cow probe result that thinking-on produced 2-3x
  complete deliverables on design asks with zero AH10 failure modes. Plus a key FAILOVER CHAIN
  (`_keys_for`, `mag/route_chat.py:52`, loop at `:139`): the nous lane law, key 1 can 402 while
  key 2 carries the credits - proven live by the 18:49:36Z smoke row below.
- Replaced: the hand-rolled urllib path every tool wrote for itself that day (docstring,
  `mag/route_chat.py:1-9` names hermes_burn's fence, ds_workhorse's lane, grok_burn's xAI
  client, tavern and dungeon carriers). Born from the operator correction "you have a pet
  model harness and never use it by default."
- Cost: ~zero. 6 smoke rows banked (202 tok in / 49 out, $0.00), including one live nous-failover
  row at 18:49:36Z fired by a sibling seat after this lane's window opened - the door is in use,
  and that row is the failover chain working (nous lane, HERMES_API_KEY_2).
- Makes possible: a tool author now writes ONE import instead of an IP-fence + key-loader +
  usage-banker; per-lane call laws are policy enforced at call time; every future call is
  self-accounting; design asks get thinking-on via depth="design" without a bespoke client.
- Honest gaps: zero importers yet (re-verified from repo root after a cwd-corrupted first grep;
  see check file RE-CHECK 1 - the registered debt in STANDING_RAILS migrates one carrier per
  sitting); no dedicated test file landed with it.

### 2. tools/dungeon.py - the dice-law D&D carrier (373 lines, NEW)

- Does: deterministic sha256 dice where the roll preimage carries the chain tip
  (`{tip}:{scene}:{turn}:{actor}`, committed BEFORE the actor speaks, actor never sees it,
  `tools/dungeon.py:110-111`); golden-vector pin check refuses startup unless three pinned
  preimages reproduce (`tools/dungeon.py:114-122`); quirks are CARRIER law not model manners
  (grok speech >1000 chars = NOROLL dossier drift, chatgpt self-verdict tokens = 3-strain
  over-claim tax, saelis CLAIM-before-ATTACK gate, deepseek cheap seat acts twice); em-dash
  strip + 120-word cap enforced by `strip_and_cap` (`tools/dungeon.py:102-107`); hard USD
  budget cap; REAL_SCROLLS turn in-game `[AUDIT <scroll>]` into REAL byte-checks
  (`tools/dungeon.py:80-100`: LINKS.jsonl==405 rows, room.jsonl >1MB, census carrier on
  AGENTS.md) - a hit banks a real verification, a phantom claim is a real catch.
- Replaced: model-rolled dice and trust-based roleplay; the DND_module spec was design-only
  until this carrier executed it.
- Cost: 18 DONE sessions at this lane's check moment (19 by the final re-check - the hourly
  cadence is live and fires mid-inventory; latest per-check sum $0.6679), 214 usage rows; 3
  further run dirs were killed without DONE (dnd0_121850Z, 122038Z, 122155Z).
- Makes possible: fully recomputable play (anyone can re-derive every verdict from preimages),
  in-game audits that byte-check estate claims, and the raw material for the capability pipe.

### 3. tools/tavern.py - the bar-fight carrier (242 lines, NEW)

- Does: N personas, one model per turn, transcript-so-far as context; a separate judge model
  scores escalation 0-5 per persona per round from the transcript only; brawl fires at
  cumulative escalation >= heat where heat = 18 - 2*pressure (`tools/tavern.py:73-76`); budget
  cap hard stop; per-turn usage banked; transcript.jsonl + play.md + DONE per run dir.
- Replaced: the failed pressure-0 calibration - the docstring records that scene 1's falsifier
  FIRED (no brawl in 10 rounds at pressure 0) and pressure is the fix. That is
  falsifier-first calibration working as designed.
- Cost: 15 DONE sessions, 630 usage rows, $15.4776 - the day's largest single line (opus-5.5
  judge + 6-persona casts). Largest single run $2.1754, many runs $0.5-2.1.
- Makes possible: repeatable multi-agent escalation experiments with a judge instrument and a
  tuning knob; a playable stress shape for the hollow-batch / persona-leak laws.

### 4. tools/arena_gwap.py - the gwap->GPS pipe (227 lines, NEW)

- Does: reads playground run dirs, builds per-fighter GWAP payloads (intent = the action the
  fighter DECLARED with the committed roll preimage as qualifier; report = the carrier's
  CONFIRM/VOID of that exact triple), agreement_score = fraction of declared actions the dice
  law confirmed (`tools/arena_gwap.py:112-167`); chain-verifies the SessionLedger; maps
  scene_id -> model_id FAIL-CLOSED (unknown actor skipped with a line, never guessed,
  `tools/arena_gwap.py:82-96`); feeds `mag.gwap_to_gps` into `tools/gps_mcp/gps_ledger.db3`.
- Replaced: nothing - it is a new pipe. Play outputs were dead-end entertainment; they are now
  routing evidence. The operator law it banks: routing dollars follow measured play capability.
- Cost: seat tokens only (adapter makes no model calls).
- Makes possible: anti-cheat scoring in the gwap engine's own grammar (a model cannot claim an
  action the dice did not rule; the carrier cannot rule an action nobody declared) and a
  capability ledger fed by play. 31 of 35 playground dirs carry GWAP_BANKED markers; the
  latest dungeon run banked 6 actors at agreement 1.0 (dnd0_20261003T180142Z).
- Observed asymmetry (mechanism not chased to source): the latest tavern marker banks all six
  personas at agreement 0.0 - consistent with the tavern report channel only filling from
  judge/verdict rows that carry no actor, so persona report claims are empty. Flagged for the
  next sitting; not fixed here.

### 5. tools/grok_burn.py - the funded grok-4.7 carrier (172 lines, NEW)

- Does: fires the three funded GROK_LANE_PACKET asks (adversarial pass on the replication
  prereg, W4 rerun protocol review, October paper fold) with evidence files rendered into the
  prompt, endpoint fence identical in shape to hermes_burn's, skip-if-output-exists,
  usage banked in the hermes row shape (`tools/grok_burn.py:139-168`).
- Replaced: the funded-but-unfired grok rung (the driving ladder named grok-4.7 funded since
  09-29; asks banked as a packet, never executed).
- Cost: 3 rows, 58,044 tok in / 4,643 out. cost_usd is null in the ledger - the xAI per-token
  price is NOT banked (honest accounting gap, flagged).
- Makes possible: a working grok-4.7 carrier; outputs landed watch/inbox/xai_grok47/
  (GROK_PREREG_ADVERSARIAL_20261003.md, GROK_W4_RERUN_PROTOCOL_20261003.md,
  GROK_OCTOBER_FOLD_20261003.md).

### 6. The fifty-wide wave protocol (protocol, receipt-banked)

- Does: wave 1 (`watch/inbox/envelope_50w_20261003.md`) proved transport: 50 Task agents in ONE
  wave on the main-session retry path, 50/50 returned, zero 429/1302 contacts, 5.9-55.4s per
  agent, ~1.0M tokens - and all 50 independently counted LINKS.jsonl at exactly 405 lines
  (50-way byte consensus). Wave 2 (`watch/inbox/burn_claims_50wide_20261003.md`) proved real
  work: 50 flash lanes byte-checking 50 claims from 16 BURN_* filings - 30 REAL / 11 DRIFTING /
  3 FALSE / 6 UNVERIFIABLE, ~1.5M tokens, $0 cash, minutes.
- Replaced: the fan-out width law's practical ceiling of 12 (amended: single-wave Task width 50
  clean; workflow children stay max_concurrency 3, unchanged) and manual per-filing audits.
- Makes possible: any N>=30/50 independent byte-check job becomes a drop-in rail; FALSE and
  DRIFTING rows become tickets automatically. The three FALSE catches include a planted
  tabletop forgery the flash agent refused to score REAL - the protocol caught a lie.

### 7. The frontier delta replay + register (instrument + register, NEW; arms landed in 53f56d0f3)

- Does: the day's 14 design asks (BARFIGHT_spec, DND_module, WIRE_PLAN, THE_ROOM_REMEMBERS,
  etc.) replayed across arms - frontier outputs in watch/inbox/hermes_burn/, flash arm in
  watch/inbox/replay_flash/ (13 files), deepseek arm in watch/inbox/replay_deepseek_thinking/
  (4 files, all landed by 53f56d0f3) - then scored per arm (chars, cites, unverifiable-count)
  into a machine-readable register `watch/inbox/frontier_delta_register_20261003.json` and
  folded against external prior art (RouteLLM, FrugalGPT, confidence routers, CRE-Router) in
  `watch/inbox/frontier_delta_steal_20261003.md`.
- The estate's named delta: others route on PREDICTED quality and static evals; the estate
  routes on MEASURED capability from real asks with chain-verified receipts, and its escalation
  trigger (gwap four-valued verdicts: VERIFIED_AGREE routes cheap, DISPUTE escalates, CHALLENGE
  is judge-owed) is what those papers build whole frameworks for.
- Cost: frontier arm $7.7430 (14 hermes_burn ask rows, exact per-ask table in the usage
  ledger); flash/deepseek arms seat tokens (deepseek arm ~$0.14/ask per the steal receipt).
- Makes possible: a capability-per-cost routing table that regenerates from real work instead
  of benchmark scores.

### 8. queue/STANDING_RAILS.md - the drop-in table (50 lines, NEW)

- Does: the Lessig law in practice - "default to the rails; a bespoke model-call path requires
  a written reason." Four rails laws (default-to-rails, material-must-render or VOID,
  interrupts-never-cancel, every-session-banks) + a ten-row drop-in table mapping what-you-have
  to where-it-lands to what-comes-out + the oroboros clause (rails compose: gap rows become
  threads, threads become builds, builds are gated, sessions bank capability rows, capability
  rows route dollars) + registered debts (each carrier migrates to route_chat one per sitting;
  the Delta Register judge pass re-fires on GO).
- Replaced: per-ask instruction of how to call models and where outputs land.
- Makes possible: the next build cycle starts from the table, not from scratch - this lane's
  whole point.

### 9. watch/inbox/mag_rails_plugin_spec_20261003.md - the ZCode plugin spec (NEW, 53f56d0f3)

- Does: specs six native tools wrapping the rails so a seat stops bash+pythoning into the
  estate: mag_route_chat (the one door), mag_stage_ask (descent driver intake),
  mag_arena_status (one-line arena state), mag_delta_register (the routing table, queryable),
  mag_gwap_bank (arena adapter), mag_sacred_cow (law + falsifier + arm design registration).
- Replaced: nothing yet - it is a spec, seeded per the operator's plugin idea; the build
  target is ZCode plugin tools over queue/STANDING_RAILS.md.
- Makes possible: the rails become first-class tools in the seat's own surface instead of
  shell incantations; the drop-in table becomes the API.

## THE STANDING FLEET'S 24H OUTPUT (not new builds; the floor they held)

- Drift-patrol (standing tool, 3 window commits 125c958eb/de0c84d3c/49b8d85af): config re-seal;
  treadmill quantified (heal 9/9, 9/7); secret-gate catch 3 - a third-party `pk_live...` Stripe
  key at line 139 of an untracked root scrape (hf_decision_models.html) excised before it
  entered history; third catch in three days, all third-party, zero fleet-owned leaks
  (watch/inbox/DRIFT_PATROL_20261003.md:30).
- Fleet lanes: 205 window trail rows (research 86, day_work 66, builder 44, seven more lanes
  1 each); 3 anchored proofs; room.jsonl 72 window rows.
- Windows cadence check: schtasks shows mag-* daily tasks but NO arena/tavern/dungeon task -
  the hourly play cadence in the receipts is seat-driven, not a registered Windows task.

## COST LEDGER FOR THE WINDOW (computed, not estimated)

- hermes_burn (paid tier): 858 rows, $23.9143, 3,404,854 tok in / 605,140 tok out.
  Split: TAVERN 630 rows $15.4776; DND0 214 rows $0.6937; design asks 14 rows $7.7430
  ($0.28-$0.78 each). Models: opus-5.5 x341, haiku-4.5 x206, sonnet-5.5 x194, fable-5.1 x117.
- xai_grok: 3 rows, 58K tok in / 4.6K out, price not banked (null).
- route_chat: 6 rows, ~$0.
- Fifty-wide waves 1+2: ~2.5M seat tokens, $0 cash.
- Total named cash: ~$23.91 (plus unpriced xAI and $0-seat-lane work).

## RECEIPT-COUNT RECONCILIATION (honest)

The ask said "the 1,569 receipts from the last 24h." This lane could not reproduce 1,569 from
any surface it could name. Recounts: 402 new files under watch/inbox in window (169 playground,
136 frontier_olm_2026-10-03, 21 gala, 14 hermes_burn, 13 replay_flash, plus smaller); ~205
fleet trail rows; 858 usage-ledger rows; 72 room rows; 3 anchored proofs. The closest single
all-time surface is the builder trail (1,556 rows lifetime). The 1,569 figure rides the ask
unreproduced; the inventory above was built from the surfaces this lane could actually count.

## EXCLUDED PER THE ASK ("not research")

- ceb7095e9 HITLER DIG (17 files, 1,488 insertions): research verdict + 3 laws minted, not a
  build.
- 831936fb6 SEED SAVER (2 files, 90 insertions): creative landing (song cut + lyric-direction
  law), not a build.

## FOR THE NEXT BUILD CYCLE (the steal)

1. New model-calling code starts at mag.route_chat, never a private urllib path (the debt list
   migrates the five existing carriers one per sitting).
2. Any N>=30 independent byte-check job goes fifty-wide (the wave-2 shape: mechanical unit
   extraction, one-line verdict contract, consensus denominator as health check).
3. Any multi-agent session can become routing evidence via the arena adapter shape (intent vs
   report payloads, fail-closed model mapping) - tavern's 0.0-report defect is the known edge
   to fix first.
4. Play carriers prove the falsifier-first calibration pattern: scene-1 falsifier fired, the
   pressure knob is the documented fix, the knob lives in the scenario file.
5. The rails table is the index: before building, read queue/STANDING_RAILS.md and drop the ask
   into an existing row.
6. Sacred cows get a probe, not a defense: the thinking-off law was batch-proven for mechanical
   asks and had silently annexed design asks; one probe (thinking-on vs off on real design
   asks) re-scoped it to a per-call depth flag in ONE commit. The pattern is now registrable
   via the mag_sacred_cow spec tool.
