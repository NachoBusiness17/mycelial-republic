# W4 OPUS FIRED: the deliberate ask to anthropic/claude-opus-5.5 (2026-09-30)

Status: FIRED ONCE, RETURN EMPTY (finish=length, all completion tokens consumed
by reasoning, answer body never started). Banked honestly per mission law:
one call, whatever comes back. No retry fired. No verdict on the baseline was
delivered; the baseline stands unbeaten by default.

## 1. What was fired

- Model: anthropic/claude-opus-5.5 via Nous inference API
  (https://inference-api.nousresearch.com/v1/chat/completions).
- Ask shape: the AMENDED ask, not the build-ask. Amendment 1 INVERTED shape
  (spec deltas + eval contract + escalation boundaries + adversarial critique,
  no commodity code), constructed per Amendment 2 (XML tags: context,
  baseline, output_contract, acceptance_tests, the_ask; context-first
  ask-last; effort max explicitly requested; mandatory hostile second pass
  with anti-sycophancy framing; verbosity contract: section caps, tables over
  prose, no preamble; falsifiable acceptance gates 1 to 5; flag-my-instructions-
  wrong clause), with Amendment 3's adopted contract lines binding (typed
  task_shape, exploration lifecycle, confidence contract, >= 20 named test_
  acceptance predicate) and the G6 fifth line resolved per the mission as
  option (b): the spec-design ask fires, the build-ask does not.
- Baseline pasted verbatim: watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md
  (full file, amendments included, no truncation).
- Call params (gopher driver pattern): single user message, max_tokens 16000,
  temperature 0.4, reasoning {"max_tokens": 6000} (LESSIG RAILS cap), one call,
  no retry, no model rotation.
- Exact fired prompt: embedded in watch/inbox/last_mile_20260930/w4_fire_opus.py
  (PROMPT_TEMPLATE + baseline). sha256 b805548a93fddb575af09c77c84a013398f6aa2ed
  0a558af79079183e002f4f7, 31070 bytes, metered 12729 prompt tokens.

## 2. The full return (verbatim banked)

- HTTP status: ok. Seconds: 194.6.
- usage: {"prompt_tokens": 12729, "completion_tokens": 16000, "total_tokens":
  28729, "completion_tokens_details": {"reasoning_tokens": 16000}}.
- Metered cost: $0.370916 (usage.cost; cost_details source openrouter_list,
  catalog rates $4/$20 per M, matches predicted arithmetic exactly; no Nous
  markup). Under the $0.50 Tier A named cap and the $2.00 mission absolute.
- finish_reason: "length". content: null (0 characters of answer body).
- reasoning_tail (last 600 chars of the thinking channel, verbatim; contains
  one em-dash, which is the model's own byte, preserved as evidence):

```text
p sampled shadow-run comparing the ledger and cascade arms on a small percentage of live traffic to confirm the key conditions still hold, though that doubles cost on that sample. A simpler alternative is expiry plus a quarterly rerun of the harness against the fixture corpus, which is much cheaper.

I also realize I can't see JUDGED.md directly, so any claims about clause 5 mapping to named blind spots are unproven — better to lean on clauses 1-4 for my deltas and flag that honestly. Now shifting to thinking through where I might be wrong myself, and which instructions I suspect are flawed.
```

- Raw row: watch/inbox/last_mile_20260930/W4_OPUS_RETURN_raw.json (the complete
  response record). No W4_OPUS_RETURN_20260930.md content file exists because
  there was no content to file.

## 3. Diagnosis (the failure is budget mechanics, not ask quality)

The LESSIG RAILS bug re-learned on the Anthropic-via-Nous route. Amendment 3's
dogfood ledger documented it on the Nous primes (fires 1-2, $1.44 tuition:
reasoning burns max_tokens, fixed by reasoning {"max_tokens": 6000}) and that
fix bound there. On anthropic/claude-opus-5.5 it does NOT bind:
completion_tokens_details shows reasoning_tokens = 16000 = the ENTIRE
max_tokens budget, i.e. the reasoning cap field was ignored by this route and
the max-effort request (explicitly solicited per the differentiation brief,
xhigh = 7 index points over medium) drove thinking appetite past the whole
completion budget. The answer body never started. The reasoning tail shows
the model WAS substantively engaged with the real ask (harness rerun
economics vs sampled shadow-run; honest UNPROVEN flag that JUDGED.md was not
in its context; clause 1-4 delta mapping; beginning section F
self-doubt), so the ask was legible and the one-shot contract held; the
length cap is what killed the deliverable.

## 4. Verdict on the baseline

NONE DELIVERED. No diff against BASELINE_SPEC section 10 was produced. The
frontier's verdict on our baseline remains uncollected; per the diff
contract, an empty return beats nothing, so the estate baseline stands as
the operating spec. This is an honest EMPTY, not a hidden failure: bytes
banked above.

## 5. Fix for the next firing (operator decision; not executed under this
mission's one-call law)

- Raise max_tokens to >= 32000 (thinking + body both must fit; at 12729 in,
  32000 out worst case the predicted cost is $0.69, still under $2).
- Or fire the anthropic/claude-opus-5.5:batch variant (catalog same rates,
  batch typically 50% off, 24h fuse) with the raised cap.
- Or drop the explicit max-effort request (the differentiation brief trades
  7 index points of quality for a thinking budget that fits 16000).
- Keep the ask bytes identical (sha256 above) so the retry is byte-stable
  against this receipt.

## 6. Ledger

- Spent this firing: $0.3709. Mission cap $2.00 absolute: 18.5 percent used.
- Credits context at mission start: ~$170 Nous. This lane's burn: $0.3709.
- Artifacts: w4_fire_opus.py (exact ask + driver), W4_OPUS_RETURN_raw.json
  (full return), W4_fire_log.txt (one-line fire log), this receipt.
- Em-dash count in estate-authored sections: 0 (the one em-dash in section 2
  is inside verbatim banked model bytes, flagged, preserved as evidence).
