---
name: codex-lens-pilot-design-20260918
description: Codex second-seat round 2 (operator pasted full outputs) — project understanding + reusable Lens_v1 draft + 12-case/4-condition transfer pilot (32-call screening); verified residual chain_guard gaps (unmarked mismatch ok:true, recompute-fail → healthy, tip-missing → healthy, exit 0 always); identity-portability tests are two OPPOSING hash assertions measuring bytes not behavior; five capabilities proposed; PASS/FAIL/UNKNOWN law queued
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

The operator pasted the Codex second seat's full follow-up (outputs at
C:/Users/foste/Documents/Codex/2026-09-17/do/outputs/): Project_Understanding_
and_System_Design_20260918.md, Project_Lens_v1.md (reusable project-context
draft with linked source manifest), Lens_Evaluation_Pilot.json, and isolated
guard fixture evidence — the working answer to "did you ever run my response
by your AI," now extended from audit into forward design.

**Verified against the live tree (fixtures + source):**
- My chain_guard tip_stale fix WORKS for the marked-mismatch case (fails
  correctly), but Codex proved residual paths: unmarked mismatch returns
  ok:true/unmarked; recompute failure, missing tip, and empty chain each
  return healthy; main() always exits 0 regardless of verdict. QUEUED:
  apply the PASS/FAIL/UNKNOWN law — unavailable verification must yield
  ok:false/state "unverified", and the verdict must reach the consumer.
- The two "identity portability" tests are OPPOSING assertions:
  test_identity_schema_portability asserts full_hash == schema_hash while
  verify_identity_coupling asserts full_hash != schema_hash. Both measure
  document hashes, not behavior. Rename as artifact-integrity/determinism
  tests; add real behavioral transfer tests.
- Extend existing boundaries, not parallels: mag/context_pack.py +
  mag/context_admission.py + mag/mcp_server.py already do assembly/budget/
  serving; mag/state_quantizer.py is NOT the 24/12/12 compiler (that was the
  inline night-fold build — implementation receipt owed).

**The five proposed capabilities:** (1) evidence registry distinguishing
reported / inspected / reproduced / live-verified (reading a file supports
that the file says it; not the phenomenon) with supersedes/contradicts/
unresolved relations; (2) versioned context compiler producing narrative +
mechanical views from the same evidence, stable pack hash, timestamps in a
separate envelope; (3) controlled transfer evaluation — 4 conditions
(current pack / size-matched plain brief / compiled lens / lens+retrieval),
12 cases, 32-call screening, rubric (source accuracy, task completion,
constraint+authority, uncertainty+revision, useful transfer — terminology
frequency is NOT understanding), pre-registered promotion rule; (4) event
history with rebuildable current views (canonical event + correction event +
derived view; never rewrite history to make the past agree); (5) traces with
explicit UNKNOWN and one trace ID per task.

**Next milestone defined by outcomes, not Sep-20:** fresh model explains the
goal AND the older identity claim without erasing the change; every critical
claim resolvable to citation+version; integrity gate rejects synthetic
mismatch and reports unknown; bounded pilot vs baselines; one useful task
survives a model change with less re-briefing.

Related: [[codex-witness-fold-20260918]], [[the-ask-is-a-lens-20260918]],
[[matthew-steiniger-correspondence]], [[thought-quantizer-v02-20260918]]
