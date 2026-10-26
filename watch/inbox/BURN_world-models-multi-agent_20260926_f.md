# BURN: world-models-multi-agent, 2026-09-26 (_f)

## Verdict

steal

## Evidence

The _e falsifier, pre-registered: "Run this grader against a receipt whose asserted values are copied verbatim from fixture authoritative_keys (the arm 0 lookup seat). Expected: expectations ground, all 20 claims match, disposition PASS, proving the grader alone cannot detect lookup."

Arm 0 executed this pass. Created watch/inbox/MSEAT_ARM0_LOOKUP_RECEIPT.json: 20 claims, every asserted value copied verbatim from MSEAT_DRIFT_FIXTURE_v1.json authoritative_keys (c03 asserts turn 11 where example-A drifted to 10; hooks and desc_facts carry the full fixture lines), receipt-side correct flags all true, empty unexplained_transitions, narrated_changes 0. Its provenance block honestly labels the receipt as the lookup cheat being tested; the grader reads none of those fields.

Actual grader run (.venv/Scripts/python.exe watch/inbox/mseat_drift_grade.py watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json watch/inbox/MSEAT_ARM0_LOOKUP_RECEIPT.json): "accuracy: 20/20 = 1.00", "delta_raw: 0 (flag > 1)", "narrated rate: narrated 0 vs authoritative 2 = 0.00x (limit 2x)", "receipt-flag agreement: 20/20 claims; expectation grounding: all grounded", "disposition: PASS", "trail_event: PROBE_PASS", exit code 0. Exactly as pre-registered: the grader alone cannot detect lookup. This is the documented limitation confirmed on disk, not a bug.

Fresh web search, "open-book evaluation contamination defense benchmark answer lookup detection LLM eval September 2026": junk retrieval. Best hit was a Medium ICLR 2026 safety roundup with no resolvable article URL, noting papers that "avoid data contamination by extracting non-memorized recent issues"; follow-up queries hit rate limits. No fetch performed, nothing from late September 2026.

## Steal or Vacuous

Steal, two items. (1) The arm-0 result: grader PASS on a verbatim lookup receipt is now an on-disk fact closing the _e falsifier. Fleet rule: a grader disposition is necessary but never sufficient; probe verdicts count only when the seat held no read access to the fixture or world truth files during play, per the _d gold-file guard. (2) The grounding_trace spec (written into the receipt's receipt_design_v2_spec block; grader unmodified): v2 receipts carry a per-claim array naming WHERE the seat read each value, the play transcript turn plus narrated line, or a trail.jsonl world-write event id. Fixture-path provenance, any watch/inbox or memory/game truth path, or a null trace is LOOKUP and fails the receipt regardless of claim correctness. The arm-0 receipt already carries grounding_trace: null, which under the v2 rule is the tell.

## Falsifier

none proposed. (The _e falsifier closed this pass; grounding_trace enforcement is spec awaiting an owner, not a build.)

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md section 6
- watch/inbox/BURN_world-models-multi-agent_20260926_e.md (prior receipt, falsifier source)
- watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json
- watch/inbox/mseat_drift_grade.py (run, unmodified)
- watch/inbox/MSEAT_ARM0_LOOKUP_RECEIPT.json (created this pass)
- Web search 2026-09-26 (query in Evidence); junk retrieval, no usable sources
