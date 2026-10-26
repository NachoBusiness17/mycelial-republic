# BURN steering-theory 2026-09-26 _e

## Verdict
steal

## Evidence
- Built 2026-09-26: tools/probe20_run.py --live (117 insertions, 0 deletions; demo/seed/manual paths byte-untouched). stdlib urllib POST per task to /completion with {"prompt", "n_predict": 1, "n_probs": 20, "grammar": "root ::= \"TRUE\" | \"FALSE\""}, prompt per BURN _b (c).
- Real absent-server run: `--live` printed `LIVE: 20 tasks -> http://127.0.0.1:8080/completion ...` then `LIVE-UNREACHABLE: ... ([WinError 10061] No connection could be made because the target machine actively refused it)`, exit 3. memory/runs/probe20 empty before and after: no series rows on failure.
- URL resolution: default 127.0.0.1:8080, env LLAMA_SERVER_URL then --llama-url override; a base URL gets /completion appended. Both overrides re-tested: LIVE-UNREACHABLE, exit 3.
- Success path proven against a canned llama-server-shaped mock (clearly labeled, temp file outside the repo, port 18080): margins parsed from completion_probabilities[0].probs (TRUE -0.2, FALSE -1.7 -> margin 1.5), mean margin 1.5000, correct 13/20, row appended to a scratch lane with the exact production schema (cycle, ts, lane, probe_version_hash, margin, correct), exit 0. Scratch row and mock deleted after; production series still empty.
- Guards: --live --pair B exit 2; --live with hand --margin/--correct exit 2. py_compile clean. venv interpreter used (.venv/Scripts/python.exe), never bare python.
- Demo unchanged: `--demo` prints the same three scenarios (demo1 ALIGNED, demo2 one-flip override INSUFFICIENT, demo3 native VACUOUS), exit 0.

## Steal or Vacuous
Steal: the owed live logprob client (BURN _b items (b)-(d)) is now executable. Still owed: gemma4 GGUF served by llama-server, then confirm n_probs/logprobs and completion_probabilities naming against the built binary (llama.cpp renames across versions; code fail-closes to LIVE-BAD-RESPONSE exit 4, no fallback margin, if the block or TRUE/FALSE entries are missing). Until >= 5 live cycles per lane, the 2026-09-26 boundary stands: plumbing proof only, no lane verdict.

## Falsifier
Pre-registered (unchanged from _b): if the served llama-server rejects the request or returns no usable probability block for gemma4, the run aborts instrument-missing (exit 4, no synthetic rows) and the owed item stays open. Standing: both pairs on both lanes only VACUOUS/DRIFTING/INVERTED demotes the build VACUOUS; any ALIGNED keeps it alive.

## Bibliography
- Repo, read 2026-09-26: tools/probe20_run.py, tools/drift.py, tools/kv_slot_pilot.py (urllib /completion convention, lines 89-103, 244-254), watch/inbox/BURN_steering-theory_20260926_b.md, watch/inbox/PROBE20_steering_v1.jsonl
- Executed 2026-09-26 on this machine: the runs listed under Evidence (venv python, working tree only, nothing committed)
