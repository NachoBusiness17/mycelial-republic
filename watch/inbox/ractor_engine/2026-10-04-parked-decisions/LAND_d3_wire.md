# LAND_d3_wire - D3 carrier-enforced explicit-off, landed 2026-10-04

Lane: D3-wire. Verdict landed: carrier-enforced explicit-off
(SYNTHESIS.md:11-17, won the hostile pass 5-3 with 2 concessions).

Honest basis note: the working tree already carried UNCOMMITTED prior-sitting
work for verdict items 1, 3, 5 and the flagless-mechanical test flip. This
sitting re-verified every one of those bytes against the verdict (git diff vs
HEAD plus direct reads), kept them, and landed the MISSING arms: the design
gate (item 2), the design-pin flip, the design-refusal tests, and the suite
run. Nothing was assumed from the prior sitting's presence; everything below
is byte-verified in this tree at the line refs given.

## Per-item changes

**Item 1 - unconditional mechanical disabled.** mag/route_chat.py: the
lane_cfg.get("disable_thinking") condition is gone. `wire_thinking`
(mag/route_chat.py:134-166) sends thinking:{type:disabled} for
depth=mechanical off the carrier's own ruling, not lane config. One scoped
carve-out, D3 falsifier (1) in code: `_thinking_forbidden`
(mag/route_chat.py:115-125) skips the key only where a 400 was MEASURED
(qwen-flash forbidden_keys carries "thinking", mag/inference_budget.py:191).
Call site mag/route_chat.py:263-268 with cause comment. Evidence carried in
the docstring: d4 probe 3-arm result (omitted = 18 reasoning tokens on a
one-word ask, disabled = 0) and the founding $0.464 burn on a flagless lane
(memory/runs/hermes_burn/usage.jsonl:1151-1152).

**Item 2 - design gate (landed THIS sitting).** mag/route_chat.py:131
`DESIGN_MIN_TOKENS = 32_000`. wire_thinking raises RuntimeError for
depth=design unless (a) the lane attests capability
(attested=bool(lane_cfg.get("disable_thinking")), passed at
mag/route_chat.py:266-267; providers.yaml disable_thinking is demoted from
enforcement to design-depth attestation per SYNTHESIS) AND (b)
max_tokens >= 32000 (raises at mag/route_chat.py:157-163). Refusal message
names cause + evidence (the 15998-of-16000 founding burn, usage.jsonl:1151).
The refusal fires before any network byte and banks an error row through
route_chat's exception path (a08-rails-laws r10 closed loop).

**Item 3 - closed-loop ledger.** The _bank dict
(mag/route_chat.py:308-310) carries `depth`, `thinking_sent` (the wire shape
actually sent) and `reasoning_tokens` (usage.completion_tokens_details,
pattern per tools/hermes_burn.py:381), so the off state is verified from the
response, not assumed from the request (openrouter/auto measured IGNORING
the disabled key, providers.yaml:219-223, is catchable post-hoc from rows).

**Item 4 - test pins.** tests/test_route_chat_depth.py:
- Design pin flipped (was design-enabled-ungated): test_design_wires_
  thinking_enabled (:83-90) now pins enabled ONLY on the attested deepseek
  lane (configs/providers.yaml:371 disable_thinking: true) at
  max_tokens=32_000.
- Omission-as-contract pin already replaced by
  test_lane_without_flag_still_sends_disabled (:122-130, the flagless-
  mechanical-disabled case; prior sitting, re-verified).
- Added THIS sitting: test_design_refuses_unattested_lane (:93-106) and
  test_design_refuses_thin_headroom (:109-119); both also assert the banked
  ok:false error row. test_wire_thinking_pure_payload (:154-165) pins the
  payload plus both refusal arms offline.
- Module docstring rewritten to the D3 contract (:1-18).
- All four expected verdicts held: the old design pin went RED at the gate
  and was flipped in the same sitting; nothing else went red.

**Item 5 - inference_budget cure.** mag/inference_budget.py deepseek row
(prior sitting, re-verified): thinking_control={"thinking": {"type":
"disabled"}} (:82), "thinking" dropped from forbidden_keys (:83-84), notes
rewritten citing the d4 probe and naming the refuted AH10 omission note
(:88-91). Companion flips in tests/test_inference_budget.py: ask-level
thinking:{type:enabled} is now OVERRIDDEN by the explicit off switch instead
of stripped (:75-84), and the model_garden row asserts the same (:331-341);
hermes fake_call signatures gained extra_body (:200-240).

## Test verdicts (instrument named)

Command: `.venv/Scripts/python.exe -m pytest tests/test_route_chat_depth.py
tests/test_route_chat_banks.py tests/test_route_chat_fence.py
tests/test_inference_budget.py -q -p no:cacheprovider`
Result: **35 passed in 4.72s**, zero failures, zero skips of note, on this
tree at the line refs above.

Also parse-checked mag/route_chat.py via ast (OK). Em-dash/en-dash scan over
all four code files: clean.

## Files touched

- mag/route_chat.py (design gate + gate call site + docstring; items 1-3)
- tests/test_route_chat_depth.py (pin flips + 2 new refusal tests + pure
  payload + docstring; item 4)
- mag/inference_budget.py and tests/test_inference_budget.py (item 5;
  prior sitting, byte-verified this sitting, unmodified by me)
- This receipt.

Not touched (other lanes own them): tools/hermes_burn.py,
tools/dungeon.py, law docs.

## Blockers

None blocking. Two standing notes, both already on the SYNTHESIS residue
list and NOT bundled here: (1) the ratchet is RED tree-wide on
tools/social_rsi.py:578 (residue 4; separate accept-or-fix by name).
(2) openrouter/auto ignoring the disabled key is not curable at the request
byte; the banked reasoning_tokens column is the detection surface, and any
enforcement beyond that is falsifier territory.
