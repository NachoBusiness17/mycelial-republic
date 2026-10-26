# B2-98 PROVIDER ERROR VISIBILITY 20260926

## Verdict

The B2-25 falsifier 1 blind spot is closed with bytes: the driver logs every 429/1302 it sees, and a new tally tool turns those log events into a session error tally file (provider_errors.json) sitting next to the agent metadata.json files envelope probes already read. First baseline on this burn's own session (sess_fd5ec147): 1785 driver-visible network failures today, 1780 of them statusCode 429 carrying the [1302] marker, 1741 absorbed by the retry layer before any lane byte could see them, 6 terminal failed turns of which only 1 is a provider error (the B2-214 agent turn that burned all 11 attempts against 1302 at 14:00-14:04Z). The other 5 are cancelled requests (reason cancelled, statusCode null). Per-wave: the three waves B2-25 called clean (129 + 35 + 123 events) carried 287 absorbed 1302 retries while their lane bytes grepped zero. "Zero 1302" in B2-25 meant none-surfaced, and the receipt can now say so with a counter instead of an absence. The wave arm ran on the recorded width-10 wave bytes plus the live refill wave, not a fresh synthetic fan-out; the resolution and the residual are named in Falsifier.

## Evidence

Tool: tools/provider_error_tally.py (new). Source of truth: C:/Users/foste/.zcode/cli/log/zcode-2026-09-26.jsonl, whose model.network.completed and model.network.failed events carry context.statusCode, context.statusMessage (the [1302] marker), context.attempt, context.maxAttempts, context.querySource and parentSessionId. Example failed event: statusCode 429, reason rate_limited, statusMessage "[1302][Rate limit reached for requests][202609261200339ae4c06e515c4458]", attempt 1, maxAttempts 11, parentSessionId sess_fd5ec147-a47d-41ee-91f4-afd899b524ca. Attribution joins the agent registry via metadata.json childSessionId.

Full-day tally (written to C:/Users/foste/.zcode/cli/agents/sess_fd5ec147-a47d-41ee-91f4-afd899b524ca/provider_errors.json at 18:35Z, durable copy watch/inbox/burn_wave_20260926/B2_98_provider_errors_sess_fd5ec147.json):

| measure | count |
|---|---|
| matched events | 8808 |
| network_completed | 7023 |
| network_failed_events | 1785 |
| statusCode 429 | 1780 |
| [1302] in statusMessage | 1780 |
| absorbed_retries (completions at attempt > 1) | 1741 |
| terminal_failed_turns | 6 |
| maxAttempts seen | 11 on all 8808 events |
| top absorber | main session bucket: 105 absorbed, max attempt 8 |

Cross-check: a family-wide event census at 18:37Z counts model.network.retry_scheduled = 1785, the same order as the attempt-derived 1741 (the delta rides the 6 terminal turns and lines written after the tally snapshot; the same census shows the live session had grown to 7071 completed / 1793 failed by then).

Per-wave tallies (windows drawn from the B2-25 createdAt clusters, JSONs in watch/inbox/burn_wave_20260926/):

| wave | window | failed | absorbed | terminal | 1302 |
|---|---|---|---|---|---|
| wave 1, width 10 | 11:24:00Z to 11:46:30Z | 129 | 129 | 0 | 129 |
| wave 2, width 10 | 11:48:00Z to 12:01:00Z | 35 | 35 | 0 | 35 |
| wave 3, width 5 | 12:01:00Z to 12:35:00Z | 123 | 123 | 0 | 123 |
| current refill wave (partial) | 18:19:00Z onward | 144 | 143 | 0 | 144 |

The one terminal provider error, read directly from the log: the B2-214 dungeon-census agent (sess_subagent_agent_c50cf4f4) took failed 429/1302 events at attempts 1 through 11, 14:00:10Z to 14:04:31Z, each answered by retry_scheduled except the last, no completion. Every other 1302 today was absorbed: 129 in wave 1 alone, under the same window B2_25_envelope_remeasure_20260926.md:27 grepped as "0 files with hits".

## Work done

Wrote tools/provider_error_tally.py (stdlib only): attributes the daily CLI log's model.network.failed/completed events to a session family (sessionId equality, sessionId prefix family, or context.parentSessionId), counts failed events, 429/[1302] splits, attempt-derived absorbed retries, terminal turns, maxAttempts and querySource distributions, joins the per-agent registry from metadata.json childSessionId, and writes provider_errors.json into the session dir (the brief's "or" arm: metadata.json itself is product-owned, so the counter lands as the sibling file). Wrote tests/test_provider_error_tally.py: 3 pins over a synthetic log (absorbed/surfaced/1302 split with a foreign-session exclusion, per-agent registry join, since-window filter plus CLI --out round trip), all passing. Ran the tally full-day, per-wave (4 windows), and live. Registered everything in QUEUE.md under the claim law (claim at 18:38:10Z, flipped to CLAIMED at landing; foreign active CLAIMs B2-164, B2-94, B2-100 honored, anchored edits only; one concurrent-write staleness rejection taken and rebased on fresh bytes per the law). Ratchet: python tools/violation_ratchet.py check --changed reads NEW=0 across 44 changed files. Em-dash count on added lines: 0. LEDGER row appended via .venv python json.dumps.

## Falsifier

1. The brief's "re-run one width-10 wave to baseline it" is resolved, not skipped: a lane has no Task-agent seat, and the standing AGENTS.md fan-out width law caps workflow dispatch at max_concurrency 3 pending the B2-99 reconciliation row, so firing a synthetic 10-wide fan-out from inside the lane would break a written law to satisfy a receipt. The baseline instead ran over the exact bytes the falsifier names: the two recorded width-10 waves (11:24Z, 11:48Z) plus the live width-8 refill wave the lane itself rides, all under sess_fd5ec147. The counter is transport-limited the same way: Task-subagent families attribute via parentSessionId; workflow children (sess_dwf-*, maxAttempts 0) carry no parentSessionId and are not counted (fed as B2-443).
2. The absorbed-retries number is derived from completions at attempt > 1, not read from an explicit absorbed field; the independent retry_scheduled event census (1785 vs 1741) bounds the derivation but the two measures are not yet pinned equal in a test (fed as B2-442's neighborhood).
3. Tally numbers are a snapshot of a live log: the full-day figures grew (7023 to 7071 completed) between the tally write and the cross-check minutes later. The per-wave windows are closed in time and stable; the "current refill wave" row is partial by construction and will not match a post-wave rerun.

## Bibliography closed

Read: watch/inbox/burn_wave_20260926/QUEUE.md (header laws, Open section, B2-98 row); watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md (whole, falsifier 1); corpus/steal/TETHERED_LINK_STEAL_20260925.md (maxAttempts 11 asymmetry); C:/Users/foste/.zcode/cli/log/zcode-2026-09-26.jsonl (model.network events, 1302/429 samples, retry_scheduled census, the B2-214 agent's 11-attempt terminal turn); C:/Users/foste/.zcode/cli/agents/sess_fd5ec147-a47d-41ee-91f4-afd899b524ca/metadata.json files (childSessionId registry, createdAt clusters); the six tally JSONs this lane wrote. No web sources. Every figure recomputed from log and metadata bytes this session with .venv/Scripts/python.exe; nothing synthesized.
