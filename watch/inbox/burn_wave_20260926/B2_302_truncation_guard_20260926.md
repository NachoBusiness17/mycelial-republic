# B2-302 Builder truncation guard (SW-07, 2026-09-26)

## Verdict

LANDED. The chat() helper in watch/inbox/burn_wave_20260926/B2_71_hill_build.py now detects finish_reason == "length" and refires ONCE at a raised budget (x3, capped 16000); the truncated call is discarded and counted in the module-level TRUNCATION_STATS (discarded_truncated / refires) so any build receipt can total honestly; a second truncation returns with truncated_final: true instead of posing as a complete section. Offline probe proves the shape: a length-truncated first call refires [2500 -> 7500], returns the full section with refired true and discarded_truncated_calls 1, stats {"discarded_truncated": 1, "refires": 1}; the double-truncation path flags truncated_final. The sibling harnesses named in the brief (other builder seats) get the pattern by reference; this file is the build-book harness the brief names first.

## Evidence file:line quotes

- QUEUE.md row: "together DeepSeek-V4-Flash reasoning burned a 2500 max_tokens budget into a 91-byte mid-sentence section (B2-71 first V0 pair, discarded and disclosed in B2_71_hill_build_20260926.md Falsifier; sibling evidence B2-231 version_deepseek.md erratum), so add finish_reason=length detection plus one automatic refire at a raised budget to the chat() helper in B2_71_hill_build.py".
- Pre-fix bytes: chat() read `j["choices"][0]["message"]` and never touched choice.get("finish_reason") -- a length-truncated answer was indistinguishable from a stop.
- New chat() docstring: "CAUSE: together DeepSeek-V4-Flash reasoning burned a 2500 max_tokens budget into a 91-byte mid-sentence section ... FIX: detect finish_reason == 'length' and refire ONCE at a raised budget (x3, capped at 16000); the truncated call is discarded and counted in TRUNCATION_STATS".
- Probe transcript (offline, transport faked at _one_call, no network): first call finish_reason length -> refire at 7500; result carries refired true, discarded_truncated_calls 1; TRUNCATION_STATS {"discarded_truncated": 1, "refires": 1}; double-length path returns truncated_final true.

## Work done

- B2_71_hill_build.py: split the transport into _one_call(); chat() became the guard wrapper; finish_reason surfaced on every result; TRUNCATION_STATS counter added at module scope with the dump instruction in its comment.
- Offline probe run (fake transport, zero external calls) verifying: one refire at raised budget, honest counters, and the truncated_final honesty flag on double truncation.
- No live provider call spent; the guard is proven by structure + probe.

## Falsifier

Reopen if: a future build receipt totals sections without dumping TRUNCATION_STATS while a length truncation occurred (the counter makes the omission visible); or chat() returns a length-truncated content without truncated_final true after its refire (probe re-run must fail). Residual: builder harnesses outside this file (other seats) still lack the guard until they copy it -- the QUEUE row named B2_71_hill_build.py as the target and "any builder-seat harness" as the spread, which stays open as pattern-adoption, not as a defect here.

## Bibliography closed

Read: watch/inbox/burn_wave_20260926/B2_71_hill_build.py (chat() + call site), watch/inbox/burn_wave_20260926/B2_71_hill_build_20260926.md Falsifier section (cited via the row), QUEUE.md B2-302 row, offline probe output. No external sources.
