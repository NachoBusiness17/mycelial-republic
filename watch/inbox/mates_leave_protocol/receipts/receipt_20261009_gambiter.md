# Receipt: gambiter - 20261009 - FINAL (this window)

Mate: THE GAMBITER. Pack: logs/mates/missions/mission_20261009_08_gambiter.md (48 lines).
Status: FINAL for this window. Stopped on context budget, not thread exhaustion.
This window was a resume-by-id of the 20261006 gambiter window and rode 4 cycles:
seed re-verification, the meter, the duel harness, the credit rails. All 5
hunting-ground rows have now been formalized across the two windows.

## FINDINGS

### Cycle 1 (seed thread re-verified on today's bytes): the Z15 equilibrium holds; both named residuals still stand

Live registry read this window (memory/percolator/invariants.json): 673 rows,
total count 1217, top count 40 = 3.3 percent share, 603 rows at count 1,
false_positives 13, zero rows above 100. Against the 20261006 window's read
(648 / 1193 / 37 / 578 / 13): 3 days drifted +25 rows, +24 total count, +3 top.
Average count fell 1.84 to 1.81. No monopoly regrowth. The current top
invariant is a different row than the last window's top
(4f9c02234f4c31a5 "source=swarm_health_law improve_queued=0 handoffs=5" at 40),
and its growth rate is 1/day, exactly the per-source per-cycle cap working.

Residual R1 (source-rotation pump) still armed: maintenance() still has zero
scheduled callers repo-wide (grep over mag/, tools/, scripts/ returns only the
CLI flag mag/percolator.py:1002 and tests/test_percolator_z15.py; the
watch/hermes_wings/src/cron_sched.py:8094 hit is a different organ, worktree
maintenance, not the percolator). Residual R2 (seal-laundering floor) still
open: heal-merge still takes MAX (percolator.py:297), no maintenance pass rides
the heal.

Cycle 2 of the prior window (queue priority cheap talk) also re-verified:
mag/router.py:649 still reads `if not markers["priority"] and not
sig.get("grok_budget_ok", True)` - the self-issued "[priority]" substring still
buys the budget bypass at the overview/plan gate. Unpatched. Spec stands in the
prior receipt; owning lane applies it.

### Cycle 2 (the meter, tools/zknot.py + tools/zknot_alarm.py): the meter taxes the estate's own prior-art discipline

Mechanism (bytes): meter = (prompts matching SELF_STEAL_RE or FORGOT_RE) per
1000 non-template human prompts, last 7d vs prior 7d
(zknot_alarm.py:63-83). SELF_STEAL_RE = r"self[\s_-]*ste[a]?l"
(zknot_alarm.py:49). FORGOT_RE = r"\bforg[oe]t|already have|\bremember\b"
(zknot_alarm.py:50). Alarm legs: WORSENED (last > prior) or BASELINE (last >=
148), improvement stays quiet, WARN-only (zknot_alarm.py:97-104). Live read
this window via tools/zknot.py --dry-run: last 7d 99 (34 self-steal + 10 forgot
of 444) vs prior 7d 123 (68 + 24 of 749); quiet. (LATEST.md at 07:15 ET today
read 98 of 448; the window slid between writes; both are real reads, named.)

Players: (1) the operator, the only sensor; his prompt phrasing IS the meter
input; (2) seats, who choose consult-vs-guess; (3) the mechanism, a rate meter
plus a quiet-if-improving alarm.

The formalized exploit: FORGOT_RE counts the operator's ANSWER to a legitimate
consult. A seat doing exactly what the DESCENT protocol leg 1 demands (cheapest
defense: grep the estate before building, ask when unsure) generates a
guaranteed meter hit the moment he answers "already have", while a seat that
guesses silently pays zero now and only probabilistically later, often with
vocabulary the regexes miss entirely. The meter taxes visible consulting and
rewards silent guessing: the inversion of the estate's own law ("the operator
must never have to re-teach a law the ribs hold"). Byte-backed false positive
already in the cards: the 09-13 21:31 prompt "remember good artists borrow"
(memory/zknot/LATEST.md card) matches FORGOT_RE on \bremember\b and carries
zero correction content.

Secondary surfaces, named not ridden: (a) the denominator only counts
non-template human prompts, and template_prefixes (zknot_alarm.py:53-56) drops
any prompt over 150 chars whose 40-char prefix repeats >= 8 times, so the
operator's repeated ritual pastes (mate mission packs) silently exit both
numerator and denominator; (b) the meter cannot see the counterfactual, whether
the law was actually IN the ribs at prompt time, so a first teaching and a
re-teaching count the same; (c) noise sensitivity: at n=444, one prompt moves
the rate ~2.2 points, and WORSENED fires on any strictly-greater rate, so a
stationary meter fires on coin noise about half of weeks (dedup key includes
numbers plus day, bounding duplicate rows only).

Answer to the prior window's open question ("does counting your own steals
create an incentive to manufacture stealable-looking work?"): no direct one.
The meter reads the operator's phrasing, not seat artifacts; manufacturing
stealable-looking work moves nothing it reads. The real incentives are the
consult tax above plus vocabulary and denominator management.

Rule changes that move the equilibrium, smallest first:
1. Split the forgot leg into f_correction (unprompted operator corrections:
   "you forgot", "this already exists" raised unprompted) and f_consult
   (operator answering a seat's prior-art ask). Only f_correction is the
   disease the 20261003 dive named. Both stay displayed; only correction legs
   feed the alarm.
2. Tag each meter hit with whether the referenced law was in the boot digest
   (rib_boot.json) at prompt time; a hit on absent law is teaching, not
   failure.
3. Stop taxing "already have" when it rides a seat-authored consult: that hit
   is the discipline working.

### Cycle 3 (the duel harness, tools/duel_harness.py): the router is defended; the second consumer leaks; the harness trusts the emitter

Mechanism (bytes): one ask, two contenders, one cheap judge; blind judging
identities are not parameters of judge_prompt (duel_harness.py:230-260);
position swap on global ledger-length parity (duel_harness.py:395-396); one
append-only row per duel to logs/duel/duels.jsonl. Payoff: verdicts feed the
capability ledger via tools/gps_mcp/router.py import_duel_bank (line 632), and
pick_duel_contenders (line 766) routes anchor vs cross-family challenger by
momentum-badged pass_rate.

Ledger census this window: 92 rows, 92 distinct ask_ids (zero repeats:
the farming hole is latent, not exploited). By mode: live 29, multifamily 30,
altjudge 22, askbank 3, f1-flash-vs-prime 4, ah10-series 2, retro 2. Judges:
ember-1 70, glm-5.3-prime 10, deepseek-chat 12. Winners: A 47, B 44, TIE 1,
UNPARSED 0. Wins by model: glm-5.3-prime 39, deepseek-v4.1-flash 21,
qwen3.8-max-prime 12, grok-4.7 9, gemini-3.8-flash 6, glm-5.3-flash 4 (sums
91, plus 1 TIE = 92; arithmetic checks). Banked cost: 6.1323 USD total
(2.5695 A + 1.5136 B + 2.0492 judges). Swap fired on 46 of 92 rows, parity rule
working as designed.

Defenses found and named (honesty cuts both ways): the router feed is
idempotent on sha256 of the canonical banked row (router.py:677-690, the Q28
gate), skips altjudge and TIE named and counted (router.py:604-605, 663-668),
refuses rubrics outside the frozen 7-set shape map (router.py:584-599, 670-672),
forces a cross-family challenger (router.py:766-789), and picks a judge from
neither contender's family (PREFERRED_JUDGES, router.py:612). This is the most
defended consumer in the estate.

Exploits that stand:

D1. Judge-shopping pays at the doctrine arbiter. tools/doctrine_arbiter.py:47-48
and tools/doctrine_arbiter_instruments.py:92 self-document that duel_table v0
counts ALL ledger rows INCLUDING altjudge. run_rejudge (duel_harness.py:433)
makes re-judging one banked duel a single cheap judge call; a farmer re-judges
until a favorable verdict lands and BOTH rows count toward that surface's
win_rate. Rule change: one line, skip mode=altjudge in duel_table exactly as
the router does.

D2. The ask is farmer-chosen free text. pick_duel_contenders picks models, never
asks; no frozen ask bank is wired into it (tools/ask_bank_seed.py exists as a
seed only). A favorite stays undefeated by dueling only on its best shape and
easiest asks; the per-shape table stays honest while the routing decision rides
farmer-chosen sampling. Rule change: draw the ask from the bank, or log
bank_id on every row and let the feed report per-bank coverage.

D3. The rubric margin: 2 of the 7 allowed shape sets both map to
adversarial-review (router.py:585-588); the farmer picks which, a real steering
margin inside a frozen map. Minor, named.

D4. Cost honesty is unenforced at the harness: retro mode defaults contender
cost to 0.0 when the burn row lacks cost_usd (duel_harness.py:566,
a_row.get("cost_usd", 0.0)); census: 15 of 92 rows (11 multifamily, 4 altjudge)
bank 0.0/0.0 contender costs, so cost_rollup understates real spend against
DESCENT leg 8 ("every turn banks tokens+cost"). Rule change: refuse retro rows
whose source lacks cost_usd, or bank null and make rollup count unknowns
loudly.

D5. No harness-level ask_id dedupe: repeats append freely; the idempotency
lives voluntarily in series scripts' own docstrings ("Idempotent: ask_ids
already banked are skipped"). Same shape as the pre-Z15 percolator: honesty at
the emitter, payoff at the consumer, nothing in the mechanism. Latent today
(zero repeats on disk). Rule change: refuse or suffix a repeated ask_id at
run_duel entry.

D6. Minor: swap parity keys on global ledger length (public counter; steerable
by firing filler duels). Any deterministic farmer-visible rule is steerable; the
cheap fix is drawing swap from hash(ask_id + previous row's corr_id) and logging
the derivation.

### Cycle 4 (the credit rails): the spending cap is unauditable, hence a norm, not a constraint

Mechanism (bytes): the DESCENT leg-8 ledger is memory/runs/hermes_burn/
usage.jsonl, 3038 rows, span 2026-10-01 to 2026-10-07, total cost field sums
94.7436 USD. Rows carry {completion_tokens, cost_correction_for, cost_usd, id,
model, ok, probe, prompt_tokens, ts, turn}: NO ladder-classification field.
Since 2026-10-02: 2802 rows, 2795 anthropic-family (opus 1163, sonnet 590,
fable 370, haiku 672), 7 z-ai/glm-5.3-prime, 56.9845 USD
banked.

The laws on the other side of the gap: the DRIVING LADDER (2026-09-28) says
Anthropic keys are UNFUNDED and Nous (glm-5.3-prime / qwen3.8-max-prime) is the
funded judgment tier; the pack's own STEER row says Nous/Hermes API only for
(a) cross-family judgment/duels or (b) failover on 1302, never because an API
key is easier to script.

The game: who classifies a call as (a) or (b)? Nobody, mechanically. The
carrier (tools/hermes_burn.py) stamps no class on rows; no gate refuses or
flags an unclassified spend; the only wired classification surface found is
declaration-shaped, tools/workflow_gate.py:220-232 requiring a
"judge-model: <provider/model>" cross-family declaration for gated review asks.
Self-classification is therefore unlimited and invisible after the fact: the
cap binds only seats that already obey it, the exact unraveling shape of the
router.py:649 marker bypass (self-issued vocabulary defeats a cap).

I do NOT claim the 2795 anthropic rows are theft, burn, or violation: the meter
cannot tell a funded account from an unfunded key from a subscription-side
bridge, and that inability is the finding. The bytes show spend banked under
models the ladder calls unfunded, with no field that could say which exception
authorized it.

Rule changes, smallest first:
1. The carrier stamps ladder_class in {subscription, cross-family, failover,
   unclassified} on every usage row (default unclassified; failover rows cite
   the 1302/429 evidence id they failed over from).
2. cost_rollup grows one leg: unclassified spend per week by model; the
   DESCENT falsifier ("spend theater") gets a number instead of a vibe.
3. unclassified above a small weekly threshold pages memory/attention.md (the
   zknot meter-alarm append pattern already exists to copy).

### The window's one-line synthesis

Three caps audited (count cap, budget cap, spend cap); two are bypassed by
self-issued vocabulary (the [priority] substring, the unclassified API call)
and the third was patched by changing the payoff function, not by adding a
guard (Z15). The estate's repeatable cure is payoff-editing; its standing
disease is caps enforced as norms.

## JOURNEY

1. Read the pack (48 lines). Read the prior window's FINAL receipt (203 lines)
   for resume-by-id. Why: resume-not-respawn law; the prior window left 3 named
   threads and 2 open residuals.
2. Read mag/percolator.py lines 1-957. Why: the seed thread's payoff function
   must be re-verified before claiming any equilibrium holds.
3. Filed the claim receipt before speech. Why: receipt-before-speech law.
4. Pulled live registry stats via the venv python (counts, top rows, buckets)
   and grepped maintenance() callers repo-wide. Why: R1's dormancy is the
   residual's live status; real counts only. The cron_sched.py hit was
   inspected and excluded as a different organ.
5. Read mag/router.py 600-709 and grepped lanes.py for marker handling. Why:
   confirm the prior window's cheap-talk finding still stands on today's bytes.
   It does, unchanged at router.py:649.
6. Cycle 2: read tools/zknot.py in full (393 lines) then tools/zknot_alarm.py in
   full (180 lines), plus the head of memory/zknot/LATEST.md. Why: the meter's
   math had moved to the alarm module; the regexes are the game.
7. Re-ran the meter live via tools/zknot.py --dry-run --n 1 (writes nothing;
   prints the meter line). Why: real counts, my own instrument, today.
8. Dead-end-adjacent turn: my first census one-liner contained a malformed
   inline conditional on the zero-cost judge histogram; the command still
   returned correct output for every other field. Lesson logged per the
   positive-steering law (record, take the lesson, keep riding); the corrected
   counts appear in COUNTS. Why the turn: flat one-liners beat clever ones.
9. Cycle 3: grepped duel surfaces; read tools/duel_harness.py in full (581
   lines). Why: the prior window named the duel harness unexplored; the payoff
   question is "what does a win buy".
10. Censused logs/duel/duels.jsonl (92 rows) and grepped its consumers; found
    the router feed at tools/gps_mcp/router.py; read router.py 540-789. Why:
    wins buy routing share only through consumers; the consumer is where the
    game is decided.
11. Grepped doctrine_arbiter for altjudge handling and read its self-admitted
    v0 counting note. Why: the router skips altjudge; does the second consumer?
    It does not: D1 stands.
12. Cycle 4: censused memory/runs/hermes_burn/usage.jsonl (3038 rows; model and
    time ranges; cost sums) and grepped tools/ for cross-family/failover
    enforcement. Why: the STEER row names two exception classes; the question
    is who classifies. Answer: nobody, mechanically; the ledger has no class
    field.
13. Context budget became the binding constraint. Wrote this FINAL receipt per
    the pack contract and stopped. Threads are exhausted for this window (all
    5 hunting-ground rows formalized across the two windows); residual
    micro-threads (D2 ask-bank wiring, R1 maintenance wiring, ladder_class
    stamp) are named above as specs, not ridden.

Dead ends, named: the malformed census one-liner (item 8, recovered in-command);
the cron_sched maintenance hit (different organ, excluded by reading it); the
meter drift 98 to 99 between the LATEST write and my dry-run (not a dead end, a
moving window, both reads named).

## COUNTS (all real, this window)

- Mission pack: 48 lines. Prior receipt: 203 lines.
- Files read this window: 10 distinct (mag/percolator.py 1-957,
  mag/router.py 600-709, tools/zknot.py full 393 lines,
  tools/zknot_alarm.py full 180 lines, memory/zknot/LATEST.md head 30 lines,
  tools/duel_harness.py full 581 lines, tools/gps_mcp/router.py 540-789,
  receipt_20261006_gambiter.md full, plus two header reads of
  doctrine_arbiter doctrine files via grep context).
- Live registry: 673 invariants, total count 1217, top 40 (3.3 percent), 603 at
  count 1, 43 in 2-5, 19 in 6-20, 8 in 21-100, 0 above 100, false_positives 13.
- maintenance() scheduled callers repo-wide: 0 (CLI flag percolator.py:1002 +
  tests only).
- Meter live reads: LATEST.md 07:15 ET line: last 7d 98 (34 + 10 of 448) vs
  prior 123; my dry-run minutes later: last 7d 99 (34 + 10 of 444) vs prior
  123 (68 + 24 of 749). Alarm state both reads: quiet. Baseline 148, target 75.
- Duel ledger: 92 rows, 92 distinct ask_ids, 0 repeated. Modes: live 29,
  multifamily 30, altjudge 22, askbank 3, f1-flash-vs-prime 4, ah10-series 2,
  retro 2. Judges: ember-1 70, glm-5.3-prime 10, deepseek-chat 12. Winners:
  A 47, B 44, TIE 1, UNPARSED 0. Wins by model: glm-5.3-prime 39,
  deepseek-v4.1-flash 21, qwen3.8-max-prime 12, grok-4.7 9, gemini-3.8-flash 6,
  glm-5.3-flash 4. Costs banked: 6.1323 USD (2.5695 + 1.5136 + 2.0492).
  Zero-cost contender rows: 15 (11 multifamily, 4 altjudge). Swap true: 46 of
  92.
- Descent usage ledger: 3038 rows, span 2026-10-01T13:11Z to 2026-10-07T09:21Z,
  cost sum 94.7436 USD; since 2026-10-02: 2802 rows (anthropic 2795: opus
  1163, sonnet 590, fable 370, haiku 672; z-ai/glm-5.3-prime 7), cost sum
  56.9845 USD. Rows carrying a ladder-classification field: 0.
- Router duel-feed defenses verified on bytes: 5 (idempotency hash, altjudge
  skip, TIE skip, frozen shape map, cross-family challenger + third-family
  judge).
- Patches applied by me: 0 (spec-only window again; 9 rule changes named
  across the 4 cycles).
- Receipts filed: 1 (this file, written once as claim, rewritten once as
  FINAL).
- Cycles ridden this window: 4. Hunting-ground coverage across both gambiter
  windows: 5 of 5 (percolator, queue priority, meter, duel harness, credit
  rails).

## STATUS

FINAL for this window. Stop condition: context budget (thread set exhausted:
every hunting-ground row formalized; residuals carry named rule changes for
the owning lanes). No resume debt beyond the standing specs above. No
em-dashes. Real counts only. No fabricated anything.
