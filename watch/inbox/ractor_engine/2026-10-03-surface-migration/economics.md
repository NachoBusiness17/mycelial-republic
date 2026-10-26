# ECONOMICS LENS - surface migration raction (2026-10-03)

Lens question: license-window tokens vs cash per deliverable per surface, and
when interactive steering pays for itself. Every number below was computed by
me this sitting from `memory/runs/hermes_burn/usage.jsonl` (1,152 rows) unless
marked ask-given or OWED.

## THE METER CENSUS (measured)

`.venv\Scripts\python.exe` census over the whole ledger:

- Total: $64.0464 across 1,152 rows, 2026-10-01..10-03. By day: 10-01
  $37.7591, 10-02 $1.1739, 10-03 $25.1134.
- By model: `anthropic/claude-opus-5.5` 447 rows / $45.6479 / 5.39M tokens;
  `anthropic/claude-sonnet-5.5` 308 / $7.5932; `anthropic/claude-fable-5.1`
  172 / $8.2186; `anthropic/claude-haiku-4.5` 218 / $0.9488;
  **`z-ai/glm-5.3-prime` 7 rows / $1.6379 / 341K tokens (2.6% of cash)**.
- Every one of these rows rides ONE door: `tools/hermes_burn.py:67`
  `API_HOST = "inference-api.nousresearch.com"`, which "serves the
  anthropic/* family (probed live 2026-10-01: 423 models)". So the entire
  ledger is Nous-credit spend. The headless rails already exist and already
  bank every call (rails law 4, queue/STANDING_RAILS.md:19-21).

## FINDING 1 - the thesis's named engine is not the rails' measured engine

The migration names GLM-5.3-max as the headless workhorse. The ledger has
NEVER banked a row for glm-5.3-max (OWED: I have not verified that model id
exists on the Nous API). It banked 7 rows ever for glm-5.3-prime, and the
delivery record is bad for a mechanical, visible reason:

- 2026-10-02, GALA_OUROBOROS_PRIME_JUDGMENT: 4 attempts, 4x
  `finish_reason: length`, 3 with `content_chars` 1 or 10 (reasoning dump ate
  the completion budget: the 10-03 row shows `reasoning_tokens: 15998` of
  16000 completion). Fifth attempt (STAGE_B, fr=stop) delivered: **$1.174
  cash for one delivered judgment**.
- 2026-10-03, GALA_DD_SELFSTEAL_PRIME_JUDGMENT: first try fr=length,
  content_chars=1, $0.25 banked as a content stub; STAGE_B re-run delivered
  at $0.21. First-try content delivery across all 7 prime rows: 2/7.
- The production replay arm that DID deliver (14 design asks, 10-03:
  BARFIGHT_spec $0.5916, DND_module $0.6636, SUBSTANCE x4 $2.2034,
  PARTYCHAT_spec $0.6917, THE_ROOM_REMEMBERS $0.7764, KABUKI $0.5599,
  SEASON $0.3897, SUBSTANCE-family SESSION_FINDINGS $0.6075, WIRE_PLAN
  $0.4543, MOUNTAIN $0.2810, WILD_EYES $0.5239) = **$7.74 cash, ~$0.55 per
  delivered design ask, on claude-opus-5.5**. Note: the ask's own brief said
  "~$13 for 14 frontier design asks"; my measured sum of the 14 design rows
  is $7.74. The $13 figure is ask-given and I could not relocate its bytes;
  the $7.74 is instrument-backed.

So as stated, "migrate to GLM-5.3-max" swaps a proven $0.55/delivered engine
for a $1.17/delivered one (2/7 first-try). But the failure is config
starvation, not capability: `route_chat` already carries the depth flag
(mag/route_chat.py:94-95, 'design' enables thinking) and the 10-02 commit
53f56d0f3 re-scoped deepseek thinking per-task for exactly this class. The
GLM lane needs the same treatment: a completion-budget floor for thinking-on
models in the INFERENCE-BUDGET plan (tools/hermes_burn.py:342-345 plan_call).

**Verdict consequence: the surface question is ~settled (hybrid already
exists); the ENGINE question is open and cheap to close.**

## FINDING 2 - re-fire was the rails' dominant cash failure; it is now
guarded (CONVERGENT with the 2026-10-02 economics lens, independent run)

The prior run's synthesis (watch/inbox/ractor_engine/2026-10-02-dogfood-48h/
SYNTHESIS.md:17-27) measured $25.5316 of $37.7591 (67.6%) as re-fire excess;
A1_steer_antiforgery re-fired 49x for $21.09; _landed_skip was check-then-fire
and 13 twin-doubled keys fell AFTER it landed. I re-derived the family from
the ledger this sitting: A1 rows = 52, $21.8518, $0.4202/row, all
claude-opus-5.5. The cures landed 10-02 (tools/instance_guard.py O_EXCL ask
claims, swept to 5 surfaces incl. descent_driver; state/CURRENT.md:21-23) and
the driver carries the pidfile guard with live exit-3 proof
(scripts/descent_driver.sh:10-23). The migration's scariest headless failure
class - silent duplicate spend - already has byte-proven guards on both
sides: the seat's interrupt-kill+refire class (the 50-wide judge wave that
died mid-turn; interrupts-never-cancel law, STANDING_RAILS.md:17-19) and the
driver's twin-drain class. Economics: the guard cost ~2 sittings and returns
~$25/day of avoided duplicate spend at the 10-01 pace.

## FINDING 3 - runway: the funded balance is a ~1-week asset at today's mix,
and play is 65% of the burn

10-03 spend $25.1134, of which TAVERN play = 665 rows / $16.2003 (65%) and
production replay+judgment = $8.45. The tavern cap is per-run ($5.00 default,
tools/tavern.py:223) and 38 playground run dirs today average ~$0.43/run, so
cap-held is true per run - but no estate-level daily cap is visible in the
ledger tooling I read (OWED: I did not audit every cron arg). Against the
funded balance of ~$180 Nous credits (AGENTS.md driving-ladder line; OWED:
no balance endpoint probe run this sitting), the 10-03 pace is ~7 days of
runway; even at zero play it is ~3 weeks. Meanwhile the seat arm costs $0
cash: the 50-wide byte-check wave returned 50/50 REAL consensus work for
~1.0-1.5M window tokens, $0.00 (watch/inbox/envelope_50w_20261003.md,
watch/inbox/burn_claims_50wide_20261003.md: "Cost: ~1.5M subagent tokens,
$0 cash (seat tier)"). On a quota license, window tokens refill; Nous
credits do not. That asymmetry, not surface ideology, is the steering
placement rule: high-iteration steering loops (the A1 class: 49 re-fires at
$0.13-0.65/shot through the CASH lane) belong on the window-metered seat;
high-certainty batch belongs on the rails.

## FINDING 4 - the routing table cannot price its own default rung

The adopted cascade (watch/inbox/frontier_delta_steal_20261003.md:44-50) is
"ds first, flash judge gate, frontier on CHALLENGE" - and deepseek is priced
at $0.14/ask (same file, line 31). But
watch/inbox/frontier_delta_register_20261003.json (14 rows, read whole this
sitting) carries only `frontier_*` and `flash_*` fields: **zero deepseek
rows**. The cheapest arm's scores are absent from the register that the
routing rule reads, so "ds first" currently rests on price alone, with the
ask-given context that deepseek "won nothing at its 6000-char cap" and
thinking-on re-runs are pending. The ask's "39 judged lanes, frontier beat
flash 8-5" tally is also not relocatable in the bytes I searched (grep for
39/8-5 across frontier_asks + delta files returned nothing; the register
JSON has 14 rows and no winner column) - ask-given, OWED.

## FINDING 5 - what the migration would actually re-lose, priced

The interactive seat's unbanked burn is my jacket violation found in the
wild: the flash replay arm's ~9.5M seat tokens / 13 deliverables (~582K
each) is ask-given and has NO banked usage line I could find (grep for
"582", "9.5M", "seat tokens" across watch/inbox/*.md hit only the steal
receipt's phrase at frontier_delta_steal_20261003.md:31). Rails law 4 says
every session banks; the seat lane banks verdicts but not its window burn.
The descent driver, by contrast, has banked 1,152 rows and is alive RIGHT
NOW: driver.beat line 2740 = cycle 1676 at 2026-10-03T19:30:08Z, pid 86854,
log tail "HERMES-BURN: PASS - 28/28 asks; ledger total $63.83". Headless
self-sufficiency is not a proposal, it is today's steady state; the arena
cron added 38 playground run dirs today with zero seat involvement (and no
repo reference to automation-b1ce1342 exists - grep over the repo returned
empty; the cron id lives in the harness automation layer, OWED bytes).

## VERDICT (economics lens)

HYBRID, and call it what the bytes say it is: the surface migration already
happened - the rails are the default call path (rails law 1), the driver
grinds unattended at cycle 1676, every cash call banks. What remains open is
(a) the ENGINE default: opus-5.5 via Nous at $0.55/delivered is the measured
champion; GLM-5.3-max is unpriced; GLM-5.3-prime delivers 2/7 first-try for
a fixable reason (thinking-starved completion budget) and must be re-armed
before the thesis can be judged; (b) the METER split: cash rails for
high-certainty batch, window-metered seat for steering loops and width-50
consensus work; (c) the accounting hole: bank the seat's own window burn.

## FALSIFIERS

1. F1 dies if GLM-5.3-max (or prime with a raised completion floor) delivers
   >= opus's first-try content rate at <= $0.55/ask over a staged 14-ask arm.
2. F2 dies if a duplicate non-zero (id,turn) pair appears in usage.jsonl
   dated after 2026-10-02.
3. F5's hybrid claim dies if driver.beat shows a >2h gap with the pid alive
   (a stall awaiting interactive input) on a production queue.
4. F3's runway math dies if a balance probe reads >$500 credits remaining.
5. F5's unbanked-seat claim dies if a banked flash-arm token line exists
   somewhere I did not grep.

## MOVES (one sitting each)

1. Re-arm the GLM lane: completion-budget floor for thinking models in
   tools/hermes_burn.py plan_call + depth flag wiring; then stage a 14-ask
   GLM arm against the register (~$3 cash at prime prices).
2. Add ds_* fields (thinking-on) to the delta register so the cascade's
   default rung is measured, not assumed.
3. Bank the seat lane: a seat-side usage_seat.jsonl appended at session
   close (window tokens per deliverable), satisfying rails law 4 for the
   surface the estate keeps.
4. One-off ledger census: cost grouped by turn>1 vs turn=1 to price the
   steering premium mechanically (converts the A1 anecdote into a column).

Filed by the economics lens, 2026-10-03. Zero em-dash bytes.

## CORRECTION (2026-10-03, hostile second pass verdict: F3 weakened)

Three claims in FINDING 3 above were wrong or unreproducible; corrected:

1. RUNWAY: the ~$180 AGENTS.md figure is NOT the operative balance. The
   estate's own probe receipt banks live balance $47.54 probe-true at
   2026-10-02T00:27:53Z (watch/inbox/ractor_engine/2026-10-02-dogfood-48h/
   accuracy.md:155-156: "probe-true at 00:27:53Z and stale after the night's
   later spend; the live balance now was not re-probed"; also :44). My
   ledger diff since that moment: $26.7302 through 2026-10-03T21:07:18Z
   (1,001 rows) - implied remaining ~$20.81, i.e. UNDER ONE DAY at the
   capped $25/day arena pace, ~2.5 days on production replay alone. Caveat
   that survives: keychain identity unverified - hermes_burn reads only
   HERMES_API_KEY_2/_1 (tools/hermes_burn.py:83-96) while duel_harness.py:88
   and lensing_ask.py:47 put NOUS_SDD_API_KEY FIRST in their chains, so the
   $47.54 may price a different key than the ledger's spend. A live re-probe
   on the HERMES_API_KEY_2 chain is the highest-value single move.
2. PLAYGROUND PER-RUN COST: "38 dirs at ~$0.43/run" retracted - it divided
   the family total over all runs including zero-spend dry runs. Recount at
   2026-10-03T21:3xZ: 41 dirs, 38 DONE files, 15 with spend>0, sum $16.2003
   (exact match to the TAVERN ledger family), avg $1.08 per spending run.
3. DAILY CAP: "no estate-level daily cap is visible" was wrong.
   watch/inbox/parable_day_one_20261003.md:13 banks "the $25.11 cap, held to
   35 cents, usage.jsonl every call". But my census reads the 10-03 day at
   $25.3534 through 20:30:13Z and $25.5563 through 21:07:18Z - PAST the
   $25.11 figure - and no code found reads a $25.11 constant (the only
   daily-cap code is mag/cost_enforcer.py:264 at default $0.50). So the cap
   reads as advisory/report-line, not an enforced stop; enforcement
   mechanism OWED. Cap semantics OWED.

