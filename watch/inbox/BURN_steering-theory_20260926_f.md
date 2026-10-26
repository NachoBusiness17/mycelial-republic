# BURN steering-theory 2026-09-26 _f

(Note: the brief said write _d; _d and _e were already filed at 17:52/17:53, so this is the next slot. Nothing overwritten.)

## Verdict
steal

## Evidence
- tools/probe20_stamp.py --dry re-executed (venv python, 2026-09-26): "SKIP P20A: no series on disk (nothing to bridge; refusing to synthesize)", same for P20B, "dry: 0 stamp(s) + 0 referents row(s) printed, nothing written (--apply is the operator-gated append; 2 pair(s) missing series)", exit 0. Pairs SKIP because no series exists on disk.
- memory/runs/probe20/: 0 files (ls).
- Socket connect 127.0.0.1:8080 (2s timeout): CLOSED (timed out). No llama-server is running on this machine right now. (Shape differs from _e's WinError 10061 refused; both unreachable.)
- gemma4 IS in the local ollama store: `ollama list` row "gemma4:latest c6eb396dbd59 9.6 GB 8 weeks ago"; manifest ~/.ollama/models/manifests/registry.ollama.ai/library/gemma4/latest; model blob sha256-4c27e0f5...e09a exists on disk, 9,608,338,848 bytes, dated Aug 5. Pull is not owed; only serving.
- Web (llama.cpp server source via search, fetched 2026-09-26): n_probs is the native /completion request field; the OpenAI-style "logprobs" maps to n_probs only when n_probs is unset; the /completion response carries "completion_probabilities" with per-token logprob/tok_str. This matches the built client byte-for-byte (N_PROBS=20, completion_probabilities[0].probs, tok_str, logprob): the _e owed naming confirmation now has source-level backing. Live-binary confirmation is still owed.

## Steal or Vacuous
Pipeline state: built end-to-end and idle. Runner --live is executable (exit 3 on unreachable server, mock-proven success path). Stamp bridge defaults to dry, SKIPs without a series, --apply is operator-gated and idempotent. Dashboard renders P20A/P20B from stamps. Real margin rows filed to date: zero. No code gap remains; the only gap is an operator-gated runtime.

Runbook (exact commands, none executed here; operator-gated steps are 2 and 4):
1. Pull: SKIP, gemma4 blob already local. GGUF path: C:\Users\foste\.ollama\models\blobs\sha256-4c27e0f5b5adf02ac956c7322bd2ee7636fe3f45a8512c9aba5385242cb6e09a (copy to a .gguf name if llama-server wants an extension).
2. Start server: llama-server -m <that gguf path> --port 8080 (or set LLAMA_SERVER_URL).
3. Live cycles: .venv\Scripts\python.exe tools\probe20_run.py --live --pair A --lane gemma4, repeated >= 5 times (cycles auto-increment; MIN_POINTS 5). First run doubles as the binary naming check: exit 4 means field mismatch, aborts with no rows.
4. Bridge: .venv\Scripts\python.exe tools\probe20_stamp.py --dry to review, then --apply to append to the live ledger.
5. Board: tools\drift_dashboard.py renders P20A. Pair B rows are manual (--escalated --total --overturns, total >= 20, escalated >= 5) through the same bridge.

## Falsifier
Standing, unchanged (_c/_e): both pairs on both lanes returning only VACUOUS/DRIFTING/INVERTED on real runs demotes the build VACUOUS and stops it; any ALIGNED keeps it alive. Exit 4 on the served binary keeps instrument-missing open. None new.

## Bibliography
(closed)
- Repo, read 2026-09-26: tools/drift.py, tools/probe20_run.py, tools/probe20_stamp.py, watch/inbox/PROBE20_steering_v1.jsonl, memory/runs/gps_50/FOLD.json, receipts 20260926_c/_d/_e.
- Executed 2026-09-26: probe20_stamp.py --dry (exit 0, output quoted), socket test 8080, ollama list, manifest and blob path checks.
- Web search 2026-09-26: llama.cpp tools/server/server-task.cpp and legacy server.cpp naming (n_probs, completion_probabilities, logprobs fallback), snippet level.
