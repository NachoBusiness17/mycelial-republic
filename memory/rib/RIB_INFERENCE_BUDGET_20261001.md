# RIB_INFERENCE_BUDGET_20261001 - the reasoning-channel burn is ONE bug with ONE reaction

OPERATOR LAW (2026-10-01, priority lane): the reasoning-channel burn bug (the
model spends the whole output budget on hidden reasoning; content returns
empty; money leaves) "has recurred for MONTHS in different jackets". The
one-bug law existed; what did not exist was ONE place that enforced the
reaction. This rib registers the class-kill and its enforcement organ.

AMENDMENT SURFACE: this rib is the enforcement leg of
memory/rib/RIB_MODEL_GATES_20261001.md (per-animal harness profiles). The
gates rib was doctrine-only until now: profiles lived in prose, and every
carrier hand-rolled its params (hermes_burn had ZERO thinking handling,
model_garden none). mag/inference_budget.py is the missing setting
mechanism, and both paid carriers import it.

## THE ONE BUG (the jacket census, honest)

Same mechanism every time: hidden reasoning eats the completion budget, the
content channel comes back empty, the seat pays and re-fires.

- 2026-09-17: glm-5.3-flash (ox-alpha build lane): with ANY max_tokens cap
  (2600/4200/9000/16000) returns empty_content finish=length.
  memory/continuity/seat_memory_20260927/ox-alpha-was-glm53-flash.md
- 2026-09-29/30: gopher disease, Nous primes: 11 of 12 returns zero content,
  $1.43 for one answer. watch/inbox/last_mile_20260930/GOPHER_BURN_RECEIPT.md
- 2026-09-30: deepseek-v4.1-flash thinking-on burns the ENTIRE completion
  budget on hidden reasoning at 4500/8000/16000 caps, socket hangs, DNFs
  (AH10 byte-confirmed). W8_MULTIFAMILY.md
- 2026-09-30: opus-5.5 caps: 16k returns all-reasoning empty; 32k burns 29.5k
  on reasoning and length-caps. RIB_MODEL_GATES_20261001.md (OPUS row)
- 2026-10-01: descent day 1: A1 first burn content-channel empty with the
  deliverable complete in reasoning at 14,960 ctok, then 47 re-fires changed
  nothing ($20.53 of $29.91 was re-fire theater). N1 x42 and DUEL1_hidden_5
  x46 refusal loops the same shape.
  watch/inbox/hermes_burn/DAY1_CROSS_RACTOR.md E1 + DAY1_RIB_WARMTH.md
- 2026-10-01: kimi cold call 234s, 17,617 reasoning tokens billed against 354
  visible: NOT the disease (content arrived). This false-positive guard is
  now law: big reasoning WITHOUT empty content never terminals.
  watch/inbox/model_garden/KIMI1_RUN.md
- 2026-10-01: fable-5.1 burned BOTH 18KB review asks whole (B1/B5:
  finish=length, 12000/12000 reasoning tokens, empty content, $2.03 of the
  $2.03 series). watch/inbox/model_garden/FABLE1.md

## THE FIX SHAPE (single-sourced, terminal, per-family)

mag/inference_budget.py is the ONE source every fire path imports:

1. FAMILY_TABLE: per-animal recipe, every row citing its paying receipt:
   thinking control (the exact param shape per family), forbidden ask params
   stripped (deepseek/qwen/gemini reasoning params), max_tokens floor per
   ask shape (review = 18KB+ rendered body: 24000 default, opus 64000;
   small: 8000 default, deepseek 2000), uncap for glm-5.3-flash, cold-call
   notes (kimi).
2. classify_empty(finish_reason, usage, content) -> EMPTY_REASONING |
   EMPTY_OTHER | NOT_EMPTY. EMPTY_REASONING = content channel empty AND
   finish=length AND burn evidence (reasoning_tokens > 0 or completion >=
   1000). The classifier sees the CONTENT CHANNEL ONLY, never the salvaged
   reasoning fallback: reasoning bytes at finish=length are burned ramble,
   not a deliverable. At finish=stop the carriers' reasoning-channel
   fallback stays sanctioned (the opus assembly path).
3. react(): the ONE sanctioned reaction. EMPTY_REASONING is TERMINAL for
   that (ask, family): mint <ask_dir>/EMPTY_REASONING (same mechanics as
   REFUSED), skip on sight, NEVER refire the same params. The marker names
   exactly two recoveries: re-stage with the family's FAMILY_TABLE recipe,
   or switch family. Re-arm = operator edit of the ask bytes AND marker
   removal.
4. Wired carriers: tools/hermes_burn.py and tools/model_garden.py call
   plan_call before every fire and guard_terminal on every response; both
   skip on the marker at entry. Minimal diffs; the proven rails untouched.
5. Distillability law: sync_to_behavioral() files each FAMILY_TABLE row as
   an animal_profiles rail observation (kind rail, source receipt), so
   `python tools/animal_profiles.py --distill` regenerates the rib evidence
   from the same bytes the module enforces (landed 2026-10-01: 10 rows).
   A recipe changed without its observation and receipt is void.

Tests: tests/test_inference_budget.py (the fable terminal case, the kimi
NOT_EMPTY guard, deepseek param injection, floors per shape, both carriers
wired with mocked transports). 42 green with the two carrier suites.

## THE FALSIFIER

Any future ledger row showing an empty-content re-fire at the same params
for an ask whose EMPTY_REASONING marker exists = this law failed; audit the
carrier that bypassed guard_terminal. Conversely a week where the ledger
grows but no animal row or receipt carries a new recipe forward means the
table is theater.

## THE SONG (searched, honest)

The operator says the estate wrote a song about this lesson. Searched the
parable/Kabuki material byte-side: the five-act score
(watch/KABUKI_THEATER_20260907.md) and the song map
(watch/inbox/hermes_burn/N1R_parables_songmap.md) name cache residue,
knots-as-goodbyes, and the Sherpa clause; no act names the empty-content
burn. The nearest byte-verified estate line on THIS lesson is the gopher
law (GOPHER_BURN_RECEIPT.md): "A burn that returns empty content is not a
burn, it is a metering error." If the operator names the song, quote it
here byte-verified.

## STILL UNWIRED (the other jackets, named for the next wave)

Every other fire surface still hand-rolls params instead of importing the
table. Priority order (paid/judgment lanes first):

- tools/stealth_driver.py: the nous/z.ai lane carries its own
  reasoning_effort knob (REASONING_KNOB_FAMILIES) but no classify/terminal
  reaction.
- tools/duel_harness.py: has the LESSIG REASONING_CAP 6000 rail but no
  empty-burn terminal marker.
- mag/tesuji_fire.py, mag/lane_runner.py, mag/lite_scale.py,
  mag/wave_fire.py: hardcoded reasoning_effort/thinking shapes, no guard.
- tools/ds_workhorse.py: thinking-off by construction (the harvested seed)
  and retry-once on empty, but a thinking-on relapse there would re-fire
  blind: it needs the classifier at minimum.

Rib minted 2026-10-01 by the inference-budget lane (ZCode seat). Evidence:
every path cited above; tests green same session.

## POST-DATUM AMENDMENT 2026-10-04 (r06#0, corpus/steal/MASTER_READ_ESTATE.md D4; appended
## 2026-10-05 by lane e03-rib-vault per the amend-never-rewrite law this rib ships)

The STILL UNWIRED bullet above naming tools/ds_workhorse.py ("thinking-off by construction
(the harvested seed)") is STALE IN THIS RIB: the 2026-10-04 d4 three-arm probe measured the
opposite default. Receipt: watch/inbox/go_wave_20261004/d4_thinking_probe.md. Measured
(deepseek-v4-flash, one-word ask, only the thinking key varied across arms): with the
thinking key OMITTED the model returned reasoning_content (70 chars) and 18 reasoning_tokens;
only the EXPLICIT thinking:{type:disabled} is the off state (arm 2: no
completion_tokens_details at all, 2 completion tokens); thinking:{type:enabled} returned
reasoning too (46 chars, 12 tokens). THE LAW IS NOW: omission is a MEASURED ON state.
Arm 3 is the sanity arm proving the param drives the state in both directions, so arm 1's
reasoning is the default state, not a param echo.

Both code sites named by the probe were cured 2026-10-04 before this amendment, and the
amendment only records them (no rewrite here of the original bullet or of the code):

1. tools/ds_workhorse.py:88-104: dated erratum comment in place after the false
   "omission IS the off state" comment, and ask() now sends the explicit
   "thinking": {"type": "disabled"} on the wire.
2. mag/inference_budget.py FAMILY_TABLE deepseek row: "CORRECTED 2026-10-04" - the
   thinking_control={} + forbidden-keys shape that stripped the off-switch and shipped the
   ON default was replaced; the omission-is-ON state is the named lesson.

Consequence carried from the probe (measured, not judged): every deepseek-v4 batch
ds_workhorse ask() ran before the 2026-10-04 erratum rode thinking-ON by default, including
the shoulders-era receipts, so their conditions are suspect (see RIB_MODEL_GATES_20261001
POST-DATUM amendment, same sitting). The historical ok=false empty-content smoke rows stay
consistent with the ON default: reasoning eating max_tokens is exactly what the default does.
