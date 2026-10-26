# B2-116 non-chat groq id classification (2026-09-26)

## Verdict

LANDED. All 9 non-chat / non-routing ids from the live 11 are now registered
under a machine-readable `out_of_routing_scope` list in the providers.yaml groq
block, one per-id class comment, so roster sweeps read the register instead of
re-flagging. One id (openai/gpt-oss-safeguard-20b) is named the sole live
promotion candidate as a safety-judge lane, gated on a consumer existing; it
stays out-of-routing today because a listed model shares the same 1K RPD /
200K TPD per-model denominator and no safety-judge consumer exists in the tree.
No quota, key, or in-routing model bytes changed.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_35_groq_models.json: "ts":
  "2026-09-26T12:33:04Z", "status": 200, "model_count": 11, ids: allam-2-7b,
  canopylabs/orpheus-arabic-saudi, canopylabs/orpheus-v1-english,
  meta-llama/llama-prompt-guard-2-22m, meta-llama/llama-prompt-guard-2-86m,
  openai/gpt-oss-120b, openai/gpt-oss-20b, openai/gpt-oss-safeguard-20b,
  qwen/qwen3.8-27b, whisper-large-v3, whisper-large-v3-turbo.
  Classification: 2 in-routing chat lanes (gpt-oss-120b + qwen3.8-27b), ASR x2,
  TTS x2, prompt-guard x2, safety judge x1, regional text x1, held-back chat
  sibling x1 = 11.
- configs/providers.yaml groq block (post-edit): `models:` still exactly
  [openai/gpt-oss-120b, qwen/qwen3.8-27b]; new `out_of_routing_scope:` list of
  the other 9 with per-class comments; quota note rewritten to point at the
  register; default_model and quota max_calls/max_tokens untouched.
- configs/providers.yaml loader tolerance: models/providers.py:90 parses with
  yaml.safe_load after comment strip and every consumer reads via `.get()`
  (models/providers.py:111-171), so the additive key is inert to routing.
- No code consumer re-flags the roster today: repo grep for
  whisper/orpheus/prompt-guard/safeguard/allam across tools/, mag/, scripts/,
  tests/ returns zero hits outside the burn-wave artifacts; the live-roster
  sweep surface is scripts/endpoint_news.py:124-128 which only prints.

## Work done

1. Re-read B2_35_groq_models.json and the B2_35 surgery receipt in full.
2. Filed a CLAIM line for configs/providers.yaml before touching bytes (claim
   law), then re-read the groq block fresh.
3. Landed the out_of_routing_scope register with per-id classes; rewrote the
   quota note to name the register instead of a bare prose tally.
4. Validated: yaml.safe_load parse green; out_of_routing_scope == 9 ids;
   models list and default_model byte-equal to pre-edit; loader import reads
   groq default_model openai/gpt-oss-120b, quota 100/100000, oors count 9.
5. Decision recorded: safeguard-20b stays out-of-routing until a safety-judge
   consumer exists; promotion path written into the block comment.

## Falsifier

This landing is inverted if any of the following holds: (a) a later /v1/models
pass shows a live id that is in neither `models:` nor `out_of_routing_scope:`
(the register has drifted from the roster; re-run the classification);
(b) a consumer starts calling a registered id through the chat path while it
sits out-of-routing-scope (the register is lying about behavior); (c) the
yaml fails to parse or providers load drops groq after the edit (the additive
key broke a strict reader somewhere).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_35_groq_models.json (read in full, the
classification's byte source); watch/inbox/burn_wave_20260926/B2_35_groq_surgery_20260926.md
(read in full, roster + denominator context); watch/inbox/LINKS.jsonl:312-313
accepted via the B2-35 receipt quotes, not independently re-fetched. No web
calls in this lane; the live probe was re-used from same-day bytes
(2026-09-26T12:33:04Z, 7h fresh at landing).
