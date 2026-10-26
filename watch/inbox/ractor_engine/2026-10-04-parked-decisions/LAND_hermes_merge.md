# LAND_hermes_merge - hermes_burn-merge lane receipt, 2026-10-04

Lane: hermes_burn-merge. Verdict: rank-4 of SYNTHESIS.md (the honest residue
item 3: hermes_burn computed the cure and dropped it one hop before the wire).
Instrument note: every count below names its moment; probe rows bank in
memory/runs/hermes_burn/thinking_off_probe_20261004.jsonl (11 rows, probes
14:57:37Z to 14:59:44Z).

## 1. The merge shape (verdict item 1)

FOUND PRE-APPLIED in the working tree when this sitting picked the lane up
(`git status`: `M tools/hermes_burn.py`, uncommitted on top of 28e7bddbf).
This sitting verified it byte-by-byte against the verdict and adopted it
unchanged; no further edit to tools/hermes_burn.py was needed. The diff is
exactly the verdict's shape:

- `tools/hermes_burn.py:106-118` new `_build_body(model, messages,
  max_tokens, extra_body=None)`: `body = dict(extra_body or {})` then
  `body.update({model, messages, max_tokens})` - the plan merges into the
  request body and the core keys WIN, so the plan cannot rewrite
  model/messages/max_tokens.
- `tools/hermes_burn.py:121-128` `_call` gains `extra_body=None` and passes
  it to `_build_body`; the JSON body on the wire is now plan-merged.
- `tools/hermes_burn.py:356-358` the call site passes
  `extra_body=plan.extra_body` alongside `plan.max_tokens`.

Fix comment (in-file at :110-114) cites the ractor verdict
(parked-decisions SYNTHESIS.md:243-250) and the usage.jsonl:1151 founding
row. Founding row re-verified this sitting from the ledger bytes:
line 1151 `z-ai/glm-5.3-prime ct 16000 rt 15998 content_chars 1 fin length
cost 0.2502604` (with line 1152: combined $0.4639940, the double burn).

## 2. plan_call untouched (verdict item 3)

The working-tree diff of tools/hermes_burn.py touches only the wire
construction; the `plan_call(...)` invocation and every input to it are
byte-identical (git diff read this sitting). Live plan_call probe
(.venv python, this sitting):

- anthropic/claude-opus-5.5 -> extra {} ; sonnet-5.5 -> {} ; fable-5.1 ->
  {} ; haiku-4.5 -> {} (all four hermes_burn PRICING models: the merged
  body is IDENTICAL to the old {model, messages, max_tokens} today)
- z-ai/glm-5.3-prime -> nous-primes, extra {'reasoning': {'max_tokens':
  6000}} (the LESSIG rails, now reaching the wire)
- deepseek-v4-flash -> deepseek, extra {'thinking': {'type': 'disabled'}}

The `thinking:{type:enabled}` recipe row belongs to glm-5.3-flash (the z.ai
lane), not the anthropic family hermes_burn serves.

## 3. Probe leg (verdict item 2): per-lane results

One ~32-token call per arm, "Reply with exactly one word: pong", with
thinking:{type:disabled} in the body; omitted-key control arms on the two
primes to separate ignore from cap truncation.

| lane | model | status | reasoning_content | reasoning_tokens | verdict |
|---|---|---|---|---|---|
| nous-glm-prime | z-ai/glm-5.3-prime | 200 | absent | 30 (disabled) vs 30 (omitted control) | IGNORES the disabled key; its rail shape is reasoning:{max_tokens}, which the merge now delivers |
| nous-qwen-prime | qwen/qwen3.8-max-prime | 200 | absent | 32 (disabled) vs 32 (omitted control) | IGNORES the disabled key, same class as glm prime |
| nous-claude-haiku | anthropic/claude-haiku-4.5 | 200 | absent | none (5 ct, "pong") | ATTESTS: accepts the key, clean off |
| deepseek | deepseek-v4-flash | 200 | absent | none (2 ct) | ATTESTS: clean off, matches ds_workhorse.py:93 shape |
| xai-grok-4.7 | grok-4.7 | 403 | n/a | n/a | UNFUNDED 2026-10-04: both XAI_SD_API_KEY and GROK_API_KEY resolve to team 715bf1ab "used all available credits"; attestation note only, never forced |
| openrouter-auto | openrouter/auto | 200 | absent | 29 (routed to z-ai/glm-5.3-flash) | IGNORE confirmed fresh, matches providers.yaml:219-223 (2026-08-24 note) |

Attest vs refuse summary: 2 lanes attest the disabled key (nous-claude-haiku,
deepseek); 2 lanes ignore it while accepting the call (glm prime, qwen prime;
plus openrouter/auto the known ignore lane); 1 lane refuses on money not key
shape (grok-4.7, 403 credits); 0 lanes 400'd on the key, so NO lane needs a
capability-scoped exception from this probe. The primes' correct posture is
the nous-primes reasoning rail (plan_call already computes it; the merge now
ships it), not thinking:disabled - the probe is the evidence that the merge
(not a blanket disabled key) is the right carrier fix for the founding burn.

Probe instrument: probe_thinking_off.py in this directory (endpoint fence:
public-IP assertion per host, fixed https URLs). Two instrument corrections
made mid-probe, banked honestly: first openrouter attempt used /v1 (wrong
path, Cloudflare 1010 then 404); corrected to /api/v1 per providers.yaml:173.
First grok attempts rode XAI_SD_API_KEY then the GROK_API_KEY fallback (same
dead team).

## 4. Tests (verdict item 4)

`git grep -l hermes_burn tests/` -> 8 files. First run: 79 passed, 3 FAILED
in tests/test_carrier_patch_t1w1.py, all one cause: `_spy_call`'s
fake_call() lacked the new extra_body kwarg (TypeError at hermes_burn.py:357).
Per the SYNTHESIS loser-4 law the pin flips WITH the code: spy signature
gained extra_body=None with a cause-plus-evidence comment. Re-run, same 8
files: **82 passed in 4.27s** (-p no:cacheprovider, 2026-10-04 this sitting).

## 5. Spend

7 paid calls, each capped at 32 completion tokens (glm prime x2, qwen prime
x2, haiku x1, deepseek x1, openrouter-auto x1 on the free-key lane); 2 grok
403s unbilled. Estimated total well under $0.002 (haiku arm priced from the
in-file table at ~$0.00003; prime per-token pricing not claimed where
unverified). Lane budget $0.05: respected.

## 6. Files touched

- tools/hermes_burn.py (verified + adopted the pre-applied merge; no further
  edit; NOT committed per lane law)
- tests/test_carrier_patch_t1w1.py (spy kwarg fix, 3 tests unblocked)
- watch/inbox/ractor_engine/2026-10-04-parked-decisions/probe_thinking_off.py
  (probe instrument)
- memory/runs/hermes_burn/thinking_off_probe_20261004.jsonl (probe bank)
- this receipt

Did not touch: route_chat (lane 1), dungeon, law docs, the ratchet,
mag/inference_budget.py (its working-tree D3 recipe correction belongs to
another lane; read-only for the item-3 verification).

## 7. Blockers and honest residue

- BLOCKER (spend-side, not code): grok-4.7 is unfunded today (403, team
  credit exhaustion on both keys). The 09-29 driving-ladder "grok-4.7 funded"
  line is stale until the operator tops the team up. Unprobed, attestation
  note only; never forced.
- hermes_burn's PRICING allowlist is the 4 anthropic models, so the merge is
  wire-neutral for the current queue until a prime or deepseek model is
  staged into an ask; the founding-burn class (glm prime hollowed at cap) is
  exactly the shape the nous-primes rail now covers the moment it is staged.
- The primes ignore thinking:disabled at 32-token caps; measured at that cap
  only. A cap-sized A/B (6000 rail vs disabled) was NOT run this sitting and
  is not needed for the merge verdict: the rails were already the recipe.
- qwen prime returned content_chars 0 at the 32 cap on both arms (length
  truncation at tiny caps); probe-valid, not a lane health verdict.
