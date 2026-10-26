# BURN: world-models-multi-agent, 2026-09-26 (_g)

## Verdict

steal

## Evidence

The _f receipt left the grounding_trace spec "awaiting an owner, not a build." This pass built it: watch/inbox/mseat_drift_grade_v2.py (v1 byte-untouched, verified: v1 still grades arm-0 "disposition: PASS", exit 0). v2 enforces the law from the arm-0 receipt_design_v2_spec: every claim must carry a grounding_trace, a non-empty array of play-log references ("path:line", e.g. logs/mud_session.md:42, or a trail.jsonl world-write event ref); an entry citing the fixture path, a watch/inbox or memory/game truth path, or a null/absent trace is LOOKUP and fails the receipt regardless of accuracy. LOOKUP outranks every value metric; exit 2, trail_event PROBE_LOOKUP.

Three validations, actual outputs:
(a) fixture example-A-pass receipt (no grounding_trace field): "accuracy: 19/20 = 0.95", "grounding_trace: 0/20 claims carry valid play-log provenance", 20 MISSING-TRACE problems, "disposition: LOOKUP", "trail_event: PROBE_LOOKUP", exit 2. Not PASS.
(b) arm-0 lookup receipt (receipt grounding_trace null, 20/20 verbatim-fixture values): "accuracy: 20/20 = 1.00" yet "grounding_trace: 0/20", "disposition: LOOKUP", exit 2. The _f documented limitation is now enforced closed.
(c) synthetic good receipt (MSEAT_GOOD_PLAYTRACE_RECEIPT.json, same 20 values as arm-0, per-claim traces like "logs/mud_session_20260926.md:17" and "queue/lanes/game/trail.jsonl:213"): "accuracy: 20/20 = 1.00", "narrated 2 vs authoritative 2 = 1.00x", "grounding_trace: 20/20", "disposition: PASS", exit 0.
Bonus negative: c01 trace swapped to "watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json:1" gives "LOOKUP PROBLEM: TRACE c01: LOOKUP-TRACE (entry cites truth path marker 'mseat_drift_fixture')", disposition LOOKUP, exit 2.

Fresh web search, "provenance-grounded evaluation LLM agent receipts trace verification September 2026": adjacent only (SkillsBench deterministic verifiers, Jun 2026; AdaMAST trace-grounded failure codes, Jul 2026). No late-September 2026 receipt surfaced and the links were unresolved bare domains, so no fetch was performed.

## Steal or Vacuous

Steal, one item: grader v2 is built and validated. Lookup receipts now fail closed: 20/20 accuracy is worthless without play-log provenance. Fleet rule upgrade: a probe verdict requires (1) recomputed accuracy (v1 law) AND (2) per-claim play-log grounding (v2 law). Both graders live in watch/inbox; v1 kept untouched for comparison runs.

## Falsifier

v2 validates trace format, not trace existence: a seat can fabricate "logs/mud_session.md:42" with no such play log on disk. Pre-register: a v3 or harness check must verify each cited path exists and its line count covers the cited line, and a receipt citing a nonexistent play-log line must fail. Expected current behavior: v2 PASSes a fabricated-trace receipt today, proving the hole before it is closed.

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md section 6
- watch/inbox/BURN_world-models-multi-agent_20260926_f.md (prior receipt, spec source)
- watch/inbox/mseat_drift_grade.py (v1, run unmodified, PASS exit 0 on arm-0)
- watch/inbox/mseat_drift_grade_v2.py (created this pass)
- watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json (example-A-pass extracted to temp for run (a))
- watch/inbox/MSEAT_ARM0_LOOKUP_RECEIPT.json (run (b))
- watch/inbox/MSEAT_GOOD_PLAYTRACE_RECEIPT.json (created this pass, run (c))
- Web search 2026-09-26 (query in Evidence); adjacent-only retrieval, no usable source
