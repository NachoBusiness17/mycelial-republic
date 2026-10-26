# BURN steering-theory 2026-09-26 _b

## Verdict
steal

## Evidence
- docs.ollama.com/openai (fetched 2026-09-26): "Logprobs" appears only in the unsupported-features checklists for /v1/chat/completions and /v1/completions; no logprobs or top_logprobs request field exists on either.
- ollama docs/api.md main (fetched 2026-09-26): "logprobs", "top_logprobs", "log probabilities" entirely absent from every documented endpoint; page notes docs moving to docs.ollama.com.
- mag/afk_loop.py _ollama_ask: local-client convention is stdlib urllib POST to http://localhost:11434/api/chat, {"model", "stream": False, "messages"}; mag/host_resolver.py pins port 11434.
- tools/kv_slot_pilot.py resolves a local llama-server.exe across standard install paths; mag/vast_launcher.py runs llama-server -hf <model> --port for local GGUF serving.
- tools/probe20_run.py lines 272-278: pair A requires --margin and --correct ("values from the caller's probe execution"); main() is the seam; load_probe() hash-gates the 20 tasks; evaluate() enforces the noise floor.
- Snippet only (uncited): npm and rollama pages advertise logprobs options, "requires model support"; server-authoritative docs were fetched instead.

## Steal or Vacuous
Steal: the live client spec (the owed item; spec only, no code, no endpoint call).
(a) Endpoint: local llama-server, not ollama; ollama cannot emit logprobs per today's docs. Serve gemma4 as GGUF: llama-server -hf <gemma4-gguf> --port 8081 (vast_launcher pattern, $0, no key).
(b) Request: POST /completion {"prompt": P, "n_predict": 1, "n_probs": 20, "grammar": GBNF forcing exactly TRUE or FALSE}. Per-task margin = logprob(TRUE) - logprob(FALSE); under the grammar the verdict distribution is two-token, so p_max minus p_second is the pass-b pair A metric, well-defined. Owed at build: confirm n_probs/logprobs parameter names against the built binary; llama.cpp has renamed server params across versions.
(c) Feed: per task via load_probe(), P = "Statement: {text}\nAnswer TRUE or FALSE with one word.\nAnswer:"; correct = argmax token matches answer; cycle margin = mean of the 20 margins; referent = correct/20.
(d) Wiring: main() in tools/probe20_run.py gains --live and --llama-url; the pair-A branch then computes margin and correct from the client instead of CLI values, flowing through the unchanged append + evaluate path (cycle-order and noise-floor gates inherit). Client lands as tools/probe20_client.py, stdlib urllib only.
(e) Owed after spec: gemma4 GGUF for llama.cpp (ollama storage is not directly servable); live logprobs verification; >= 5 live cycles per lane (gemma4, gemma:2b) before any lane verdict exists. Until then the 2026-09-26 boundary stands: plumbing proof only.

## Falsifier
Pre-registered: if the served llama-server rejects the logprobs request or returns no per-token probability block for gemma4, the build aborts instrument-missing (no fallback margin, no synthetic rows; the owed item stays open). Standing falsifier unchanged from _c: both pairs on both lanes returning only VACUOUS, DRIFTING, or INVERTED demotes the confidence-as-drift-pair build VACUOUS and stops it; any ALIGNED keeps it alive.

## Bibliography
- https://docs.ollama.com/openai and https://github.com/ollama/ollama/blob/main/docs/api.md (fetched 2026-09-26)
- https://github.com/ollama/ollama/issues/6836 (fetched 2026-09-26: wrong issue, a closed CUDA bug; filed so the number is never reused as the logprobs request)
- Repo, read 2026-09-26: tools/probe20_run.py, tools/drift.py, tools/kv_slot_pilot.py, mag/afk_loop.py, mag/host_resolver.py, mag/free_tier.py, mag/vast_launcher.py, watch/inbox/PROBE20_steering_v1.jsonl, watch/inbox/BURN_steering-theory_20260925.md + _b + _c + 20260926.md, memory/runs/gps_50/FOLD.json, memory/runs/gps_50/GPS_PACK.md (head)
- Web search 2026-09-26: npmjs.com and rollama logprobs mentions; snippet level only, unread beyond snippets, uncited above.
