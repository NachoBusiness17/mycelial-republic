# LOGIC LENS - surface migration raction (2026-10-03)

Lens: logic (instrument theorist). Jacket: two instruments disagreeing with no
adjudicator. Topic: migrate the primary orchestration surface from interactive
ZCode sessions to Hermes-launched headless rails (GLM-5.3-max / Nous launching
standing workflows in headless agent surfaces).

## METHOD (what I personally read and ran this sitting)

Read: state/CURRENT.md; queue/STANDING_RAILS.md; watch/inbox/mag_rails_plugin_spec_20261003.md;
watch/inbox/frontier_delta_steal_20261003.md; watch/inbox/envelope_50w_20261003.md;
watch/inbox/burn_claims_50wide_20261003.md; mag/route_chat.py (full);
scripts/descent_driver.sh (full). Ran (venv python, per the seat law): census of
memory/runs/hermes_burn/usage.jsonl (1,152 rows; 911 today; $25.1134 today);
whole-repo grep for route_chat adopters; tools/operator_go.py cross-ref;
driver.beat/driver.log tail + skipped/PASS line counts; machine recount of
watch/inbox/frontier_delta_register_20261003.json under two win rules.

## VERDICT (the logic lens's call): HYBRID, boundary drawn at volition vs hands

The bytes support headless EXECUTION unambiguously (descent driver 1,676
cycles, hourly arena, ds_workhorse, the fifty-wide waves). The bytes do NOT
support headless GENERATION, because every rail self-describes as seat-fed:
descent_driver.sh:7 "The seat stages new legs into the queue dirs; the driver
never invents asks"; STANDING_RAILS.md:42 "The operator drops; the estate
routes." So "migrate orchestration headless" conflates hands (proven headless)
with will (never run headless). The interactive seat's irreplaceable residue is:
ask authorship, operator GO adjudication, and judge verdicts (the judge pass is
30/50 with ~20 lanes killed by an interrupt, STANDING_RAILS.md:49-50, re-fire
owed). Everything downstream of a staged ask is already headless and should be
declared so; the surface to keep interactive is the staging + adjudication end.

## FINDINGS

### F1 (jacket): the spend ledger cannot arbitrate the verdict as-is

The economics of the migration ride ledgers whose success flags contradict each
other. tools/hermes_burn.py:320 sets `ok: True` at row init and lines 356-357
bank the reasoning channel as content when the content channel is empty;
verified live in the ledger: row 2026-10-03T19:25:23Z
GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003 has content_chars 1, finish_reason
"length", channel "reasoning-dump (content stub...)", cost $0.2502604, ok True.
route_chat banks ok=bool(content) instead (mag/route_chat.py:150-155) and its
own first-day ledger is 4 ok:false of 6 smoke rows
(memory/runs/route_chat/usage.jsonl, 16:44-18:49Z). The estate's own
hollow-batch law concedes the class: "outputs without their material are VOID
... and the run still prints ok=True" (STANDING_RAILS.md:12-16). Second
contradiction, same ledger, no adjudicator: 911 of 911 rows banked today are
anthropic/* models at $25.11 cash (opus 362, haiku 218, sonnet 205, fable 124,
glm-prime 2) while the driving-ladder law (AGENTS.md, 2026-09-28) marks
Anthropic keys UNFUNDED. Either the law is stale or the headless night is
off-book spend; no receipt I read adjudicates.
Falsifier: recompute per-deliverable cost with void rows (empty content
channel, or chars below a stated deliverable threshold) excluded from both
ledgers; if the $13/14-asks and ~582K/deliverable figures move less than 10
percent the blindness is immaterial; if they move, the verdict arithmetic is
built on void rows and must be re-derived. Separately: one operator row
adjudicating the anthropic funding status, or the ledger relabeled.
Move (about 30 min): a void-row census over memory/runs/hermes_burn/usage.jsonl
plus the flash replay receipts, corrected per-deliverable number banked; one
line in the driving-ladder rib or an OPERATOR_GO row settling the anthropic
funding question.

### F2: the three-arm instrument is not one instrument; the ds arm is censored

The Delta Study's arms ran at different ceilings: ds_workhorse sends
max_tokens 2000 and truncates output to content[:6000]
(tools/ds_workhorse.py:52,93) while hermes_burn defaults max_tokens 24000
(tools/hermes_burn.py:345). The register carries zero deepseek columns
(watch/inbox/frontier_delta_register_20261003.json, 14 rows, frontier_/flash_
fields only); the thinking-on arm has re-run 4 asks so far
(watch/inbox/replay_deepseek_thinking/, 4 files). "Deepseek won nothing at its
6000-char cap" is therefore a verdict about the cap, not the model. This is the
same error class as the sacred cow felled today (commit 53f56d0f3: thinking-off
was batch-scoped, not a model property) and the routing table the migration
would lean on inherits it.
Falsifier: re-run the 14 asks through the thinking-on arm at matched
max_tokens; if deepseek wins any design ask, the frontier-only class shrinks
and the cascade rule (ds first, flash judge, frontier on CHALLENGE,
frontier_delta_steal_20261003.md:46-47) changes.
Move (about 45 min): matched-cap re-run of the remaining 10 asks, ds columns
appended to the register.

### F3: the headline numbers are hand-sums with no committed scorer, and one flips sign under a second defensible rule

No instrument in the repo computes the migration case's headline figures. The
register holds 14 rows (machine-counted); grep for "9.5M|582" over
watch/inbox/*.md and watch/inbox/replay_flash/*.md returned zero hits; ls
tools/ | grep -i "delta|frontier" returns rollup_delta.py (unrelated). My own
machine recount of the 14 rows: chars-major rule gives frontier 9, flash 4
(excluding the one flash-empty row SUBSTANCE_gaming_corpus), or 10-4 including
it, not the 8-5 in the brief; cites-minus-unver rule gives frontier 4, flash 9,
the opposite sign. The win rule is unstated in the bytes, and the routing table
built on it is rule-fragile. This is the trust-bytes-not-reports disease in the
verdict's own evidence base.
Falsifier: commit the win rule; if delta_score.py under three named rules
yields three different splits, the 8-5 headline is not an instrument output and
the verdict cannot cite it until one rule is anointed and the register
re-scored.
Move (about 30 min): tools/delta_score.py reading the register JSON, printing
win rates under three named rules with the anointed rule flagged; receipt
banked in watch/inbox/.

### F4: the dormant gate exists twice, unwired, and the front door has no callers

The GO contract is duplicated without an adjudicator: route_chat takes
operator_go as an in-process bool defaulting False (mag/route_chat.py:90,
check at 113-115), while the canonical B2-425 instrument reads operator orders
from watch/inbox/OPERATOR_GO.jsonl (tools/operator_go.py:1-20); route_chat
never consults the file. And the "one door" has walked through it almost
nobody: whole-repo grep -rln "route_chat" (excluding .venv/tests) returns
mag/route_chat.py and one gala lane script
(watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-intelligent-burn_check.py);
its usage ledger is 6 smoke rows, 4 of them ok:false. STANDING_RAILS law 1
("default to the rails", STANDING_RAILS.md:10-12) is less than a day old and
adoption is zero; the registered debts (STANDING_RAILS.md:46-48) admit
tavern/dungeon/hermes_burn/grok_burn still self-call. Under a headless
migration every caller is code, and a bool-parameter gate is exactly the kind
automation relaxes to True; the file-backed GO instrument is the headless-safe
form and it is the one the door ignores.
Falsifier: after wiring, a headless rail attempting a dormant-lane call with no
OPERATOR_GO.jsonl row must exit nonzero; prove by firing route_chat at a
dormant lane with the row absent (expected RuntimeError, no ledger row).
Move (about 40 min): wire route_chat's gate to tools/operator_go.py (gate id
= lane name), keep the bool as interactive-seat override only, one test.

### F5: "outgrew the interactive surface" is execution evidence wearing a generation claim

The migration premise is supported by headless execution wins (driver cycles
1,674-1,676 in driver.beat today; envelope_50w_20261003.md 50/50 clean;
burn_claims_50wide_20261003.md 50/50 on real work) but the driver is a queue
consumer that "never invents asks" (descent_driver.sh:7) and the staging end is
the interactive seat by the rails' own text (STANDING_RAILS.md:42). The
overnight evidence is liveness, not throughput: driver.log carries 229,511
"skipped" lines against 47,064 PASS lines, and the recent pass summaries are
all-skip at a constant cumulative $63.83 ("PASS - 2/2 asks", "12/12", "28/28").
No byte I read shows an ask authored, judged, and landed without an
interactive seat in the loop. Meanwhile one of the four standing laws exists
only to patch an interactive-only failure: interrupts-never-cancel
(STANDING_RAILS.md:17-18) responds to the ~20 judge lanes killed by a mid-turn
interrupt (STANDING_RAILS.md:49-50), and no repo instrument enforces
background execution (grep "background" in tools/*.py returns unrelated
files), so that law is seat discipline, not code. That the current surface's
worst production failure needed a new law rather than a guard is evidence FOR
the migration on that axis, honestly counted.
Falsifier: a 48-hour window with zero asks staged from any interactive seat in
which the rails still produce a judged, landed deliverable (for example the
arena's gap register or the percolator emitting the next descent ask). If the
rails starve, the hybrid boundary at generation is confirmed; if they do not,
full migration loses its last structural objection.
Move (about 60 min): tonight, one seat-free leg: a gap-register row emits one
descent ask dir, the driver eats it, the judge scores it, the receipt lands in
watch/inbox/hermes_burn/.

## WHAT STAYS INTERACTIVE AND WHY (logic-lens answer)

1. Ask authorship and staging: the one end no headless instrument has ever run
   (F5). The claim it can move is currently unfalsified but also untested.
2. Operator GO on dormant lanes: must move to the file instrument
   (tools/operator_go.py) so it survives headless; the bool param must not
   (F4).
3. Judge verdicts and adjudication between disagreeing instruments (F1, F3):
   trivalent verdicts need an adjudicator; the judge pass is the adjudicator
   and it is interactive today and incomplete (30/50).
Everything else, execution-shaped, is already headless and should be named
headless rather than "proposed to migrate".

## FALSIFIERS FOR THE HYBRID VERDICT (summary)

- Rails produce a judged landed deliverable from a seat-free-emitted ask for
  48h: the generation boundary falls, full migration becomes defensible.
- Void-row census moves per-deliverable cost by less than 10 percent AND the
  register re-score holds one anointed rule across all asks: the economics
  case is real as stated.
- ds matched-cap re-run wins zero asks: the frontier-only class stands.
- An anthropic funding adjudication arrives (operator row or rib amendment):
  the ledger contradiction closes.

## BLIND SPOTS (honest)

- I did not read tools/hermes_burn.py end to end; the ok-semantics claim rests
  on lines 320/356-357 and one ledger row, not a full audit of every failure
  path that could flip ok to False.
- The cron id automation-b1ce1342 appears nowhere I searched (watch/inbox/,
  queue/, memory/; md+json+jsonl); the "8 cycles today" claim is unverified in
  repo bytes. I machine-counted 16 tavern_* dirs under watch/inbox/playground/
  for today, which does not decompose into cron-vs-manual from anything I
  read.
- The 39 judged lanes figure: I found 14 register rows, 13 replay_flash items,
  4 replay_deepseek_thinking items; I could not derive 39 from any combination
  I tried and found no receipt carrying it. OWED to whichever lens owns the
  Delta Study receipt.
- The nul-file trap, the stale pytest-tmp sweep, claim locks, and .env
  permissions are operations and security lens scope; I did not verify them.
- I did not open configs/providers.yaml; lane dormancy flags (which lanes are
  actually dormant behind the gate) are unverified by me.
- opencode as a headless surface: zero bytes in this repo describe it; my
  architecture comments are about the rails' own texts, not that product.

## OWED (could not verify, not asserted)

- Derivation of "39 judged lanes" and the exact win rule behind "8-5".
- The arena cron's cap semantics beyond tavern.py's per-run budget_usd default
  5.0 (tools/tavern.py:223, hard stop at :132-133): no day-level cap
  instrument found in the two files I grepped.
- Whether any OPERATOR_GO.jsonl rows exist today (I read the reader, not the
  file).

Zero em-dashes. Every number above is machine-derived or path-cited from this
sitting's reads and runs.
