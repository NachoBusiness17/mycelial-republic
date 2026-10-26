# B2-443 receipt: census the workflow-child error surface the tally cannot see (2026-09-26, lane SW-03)

## Verdict

LANDED as the asymmetry census (the record, per the brief's second branch; the --dwf-run tally mode is registered as the owed extension). The blind spot is real and now measured: 896 model.network.failed events across 375 sess_dwf-* actor sessions in 27 workflow runs (CLI logs 09-20..09-26) are INVISIBLE to tools/provider_error_tally.py, whose _belongs() requires sessionId equality/prefix or a parentSessionId match, and dwf child lines carry neither. Of the 896: 850 carry statusCode 429 with retryable:true, and 817 of those carry the z.ai plan rate-limit statusMessage "[1302][Rate limit reached for requests]" (the 1302 storm the 9/25 tether receipt measured for Task subagents, here on the workflow transport where nothing absorbed it). Terminal-actor cut (no model.network.completed after the actor's last failure): 11 terminal actors across 2 runs, named here as the record: sess_dwf-dwfrun-dd7232ea-b7ae-4090-a308-af889729f209 (7 actors / 7 failures) and sess_dwf-dwfrun-6d7af824-b74a-4e29-8d9e-e3274cc6436c (4 actors / 5 failures). Neither run is named in any receipt or tally output (greps recorded below): the falsifier was TRUE before this receipt and is now named by it.

## Evidence file:line quotes

- tools/provider_error_tally.py:63-67 (_belongs): "if line_session_id == session or line_session_id.startswith(session + \"-\"): return True; return isinstance(parent_session_id, str) and parent_session_id == session" (the attribution a dwf child can never satisfy: its sessionId is sess_dwf-* and its log lines carry no parentSessionId field).
- Sample dwf failure line (log zcode-2026-09-22.jsonl, 2026-09-22T02:27:18.231Z): "\"event\": \"model.network.failed\" ... \"sessionId\": \"sess_dwf-dwfrun-dd7232ea-...-actor_1_13\" ... \"querySource\": \"workflow_child\", \"attempt\": 1, \"providerId\": \"account:zai-individual-coding-plan\", \"modelId\": \"GLM-5.3-Flash\"" (workflow_child source, attempt 1: no absorbed-retry budget).
- Failure payload (this lane's probe): "\"reason\": \"rate_limited\", \"retryable\": true, \"statusCode\": 429, \"statusMessage\": \"[1302][Rate limit reached for requests][...]\"".
- Counts (this lane, over ~/.zcode/cli/log/zcode-2026-09-2*.jsonl): 896 model.network.failed on sess_dwf-* sessionIds; 375 actor sessions; 27 runs; 850 with 429 retryable:true, 817 with the 1302 statusMessage, 34 other-429, 45 unclassified; terminal actors 11 across runs dd7232ea and 6d7af824.
- Coverage greps (this lane): dd7232ea / 6d7af824 / a6dc4dec / 4c7ad095 appear in NO tally output or failure receipt; the only file hits for the terminal runs are watch/inbox/index_events.jsonl / INDEX.json register events and an unrelated SMITH_MAP receipt, none carrying error coverage.

## Work done

- Swept seven daily CLI logs for sess_dwf-* model.network.failed events; classified the payload kinds (429/1302 split above) from context.statusCode and context.statusMessage.
- Built the terminal-actor cut with the correct success counterpart (model.network.completed after the actor's last failure) after calibrating the event vocabulary on one full run's event stream.
- Proved the tally blind spot from the attribution predicate, and checked receipt coverage for the named runs (none).
- Filed this census as the record; the tally extension (--dwf-run mode: accept a dwfrun id, attribute by sessionId prefix sess_dwf-<runid>, report per-actor terminal cuts) is registered as the owed build so the next storm is measurable by tool, not by ad-hoc sweep.

## Falsifier

The brief's falsifier, closed forward: a dwf run with terminal 429 actor failures that no receipt or tally names is now impossible to miss silently ONLY if this census is superseded by the --dwf-run mode (owed) or the next storm's lane reruns this sweep; until then the standing record names dd7232ea and 6d7af824 as the known unnamed runs. Additional kills: (a) a _belongs change that starts matching dwf children without the tally gaining a dwf mode would double-count parent-family rows (the mode must be opt-in), (b) the terminal cut depends on model.network.completed being the success counterpart; a renamed success event would inflate the terminal set (recalibrate on the vocabulary probe).

## Bibliography closed

- tools/provider_error_tally.py (_belongs, _default_log_path, --session contract)
- ~/.zcode/cli/log/zcode-2026-09-2{0..6}.jsonl (the seven daily logs swept)
- corpus/steal/TETHERED_LINK_STEAL_20260925.md (maxAttempts asymmetry pointer; the 1302 shape)
- watch/inbox/burn_wave_20260926/QUEUE.md (B2-99 AGENTS.md reconciliation row pointer, the brief's context)
- corpus/steal/VERIFIER_BYTES_LAWS_20260926.md (the only receipt mentioning a sampled run id; carries no error coverage)
- watch/inbox/burn_wave_20260926/B2_99 AGENTS.md row (queue, referenced)
