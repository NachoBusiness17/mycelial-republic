# OLLAMA LOGPROBS PROBE — the door is OPEN (2026-09-07)

**Station:** verification worker, Witness #2 follow-up (Astra audit, item 1).
**Question:** does local ollama v0.32.7 return REAL logprobs, or does the Keeper's Maze
field organ stay a PROXY? Astra disputed our "native ollama has no logprobs" premise
from versioned source; behavior was UNVERIFIED locally. Now verified live.

## VERDICT (tri-state)

- **"Ollama v0.32.7 returns real per-token logprobs" — SUPPORTED, live.**
  Both the OpenAI-compatible endpoint AND the native API return real
  log-probability data: the selected token's logprob plus top-k alternatives
  (k up to 20), per generated token, non-streaming AND streaming.
- **"The native API exposes no logprobs" (ASTRA_PROMPT v2 line 59) — DISPUTED,
  retracted with receipt.** The premise is false on this host as probed 2026-09-07.
- **"The maze field organ gets real logprob data" — SUPPORTED (door OPEN),** with one
  honest boundary: the FULL logits vector is still NOT exposed — only a top-k slice
  (k <= 20) per token. The field is real at the fork point, not the whole plane.

## Live receipts (host ollama 0.32.7 at 127.0.0.1:11434, model gemma:2b, $0)

**(a) OpenAI-compatible — POST /v1/chat/completions**
Request: `{"model":"gemma:2b","messages":[{"role":"user","content":"Say hi in 3 words."}],"max_tokens":8,"logprobs":true,"top_logprobs":3}`
Response (trimmed): `choices[0].logprobs.content[] = [{"token":"Hello","logprob":-0.49925124645233154,"bytes":[72,101,108,111],"top_logprobs":[{"token":"Hello","logprob":-0.499...},{"token":"Hi","logprob":-1.220...},{"token":"Sure","logprob":-2.490...]}}, ...]`
k=3 honored per position; logprobs are real float64 values with raw byte arrays.

**(b) Native /api/chat — top-level params, no options nesting**
Request: `{"model":"gemma:2b","messages":[...],"stream":false,"options":{"num_predict":8},"logprobs":true,"top_logprobs":3}`
Response (trimmed): `{"model":"gemma:2b",...,"logprobs":[{"token":"Hello","logprob":-0.5212118029594421,"bytes":[72,101,108,111],"top_logprobs":[...]}],...}`
Streaming: every chunk carries its own `logprobs` array (per-token, verified with
`stream:true` — chunk 1: `"Sure"` -0.2055 with top-2; chunk 3: `" you"` -3.4059 where
`" here"` -0.867 was actually likelier — the sampler's real choice, visible).

**(c) Native /api/generate**
Request with `"logprobs":5` returned: `{"error":"json: cannot unmarshal number into Go
struct field GenerateRequest.logprobs of type bool"}` — the error itself is a receipt
that the field exists (type bool). Corrected request `"logprobs":true,"top_logprobs":3`
returned the full response including `logprobs[]`, alongside `eval_count:8`.

## Source pins (v0.32.7, raw.githubusercontent.com/ollama/ollama/v0.32.7/...)

- `openai/openai.go`: L51-59 `ChoiceLogprobs{Content []api.Logprob}`; L122-123 request
  `Logprobs *bool` + `TopLogprobs int`; L273-275/305-307 response assembly; L813-827
  conversion into the internal runner request. Streaming chunks carry logprobs too
  (L352-360 note about chunk-splitting).
- `api/types.go`: L123-129 `Logprobs bool` (json `logprobs`) + `TopLogprobs int`
  (json `top_logprobs`), "Valid values are 0-20. Default is 0 (only return the selected
  token's logprob)". L497-515 `TokenLogprob` / `Logprob` structs. L544-546 and L927-929:
  `Logprobs []Logprob` response fields (ChatResponse / GenerateResponse).

## History (GitHub, fetched 2026-09-07)

- Issue #16117 "Add logprobs support to OpenAI-compatible /v1/chat/completions endpoint"
  (closed 2026-05-12) — its own body: native /api/generate ALREADY returned logprobs
  before the OpenAI shim existed; the issue only asked to expose the same shape at /v1.
  So native support predates the OpenAI support.
- Related fixes: #13500 (partial UTF-8 bytes), #14692 (raw token bytes preserved),
  #15826 (preserve generate logprobs with builtin parsers), #16321 (temperature
  scaling applied before computing logprobs), #14564 (top_logprobs validation).
- OPEN CAVEATS worth the maze's attention: #18163 — requesting logprobs can change
  WHICH tokens are generated under greedy decoding (long generations, reported on
  0.30.5); #16196 — logprobs/temperature-scaling history. Observer effect is real:
  the probe perturbs the walk.

## Meaning for the Keeper's Maze render

1. FIELD upgrades PROXY -> REAL: the fork point ("the maze forks AFTER the corridor")
   is now measurable with actual distribution data — top-k logprobs per token, k<=20,
   including streaming, so the walk can animate fork pressure live.
2. Boundary that stays closed: full logits vector (vocab-wide) and attention weights
   are still NOT exposed. The lightmap stays symbolic; the field is a "top-20 slice",
   and the keeper must label it as such (F6 honesty gate: render says "top-k slice of
   the distribution", not "the field").
3. The 87.4% PCA projection pattern (behavioral text features) remains reusable for
   any future vocab-wide door, but is NOT needed for the top-k surface.

## Falsifier (closes the question permanently)

Scripted probe, re-run on every ollama version bump (pin in state/CURRENT.md):
1. POST /api/chat `{logprobs:true, top_logprobs:20, stream:false, num_predict<=8}`;
   PASS iff `len(resp.logprobs) == resp.eval_count` and every entry has
   `logprob` (float) and `top_logprobs` with `len <= 20`, first element == selected token.
2. Streaming variant: PASS iff every content chunk carries a well-formed `logprobs` array.
3. Observer-effect guard: greedy run with and without `logprobs:true` — PASS iff
   generated token strings identical (else the probe is perturbing the walk; log it).
Failure of (1) or (2) on any future version = door closed again, field reverts to PROXY.

---
Probe receipt by the verification seat, 2026-09-07. All requests/responses captured
live against 127.0.0.1:11434 (v0.32.7). No secrets, no docker changes, $0.
