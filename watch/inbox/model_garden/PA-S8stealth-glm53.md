# PA-S8stealth-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# STRANGER AUDIT: STEALTH FINDINGS BANK + TRIAGE RULE (v1 spec)

## 1. What rots (observed in bytes)

- **Duplication:** 122 rows collapse to 3 topics x 4 lanes, "12 distinct answer files, overwritten per cycle" (01__STEALTH_TRIAGE_20260930.md, sec 1). 44 rows for `w-kabbalah-epistemics` re-derive one answer; the JSONL is append-only, so no row ever dies. Overwrite risk is worse: answer files like `w-belt-cube-mechanism_openrouter1.md` are clobbered each cycle (00__STEALTH_MINED_FINDINGS.jsonl, ts 2026-10-02T02:33:44Z), so the "finding" and its history diverge silently.
- **Age:** the 09-28 haul (first rows ts 2026-09-28T00:37:48Z) sat until a human-written v0 triage on 09-30. No ingester existed: "no percolator/quantizer ingester exists, so the old note named modules that never read this file" (00, note field x92 rows).
- **Contradiction:** standing law "substance_chars=0 is the norm" vs 92/92 free rows finish=stop with 1.3-8.0 KB answers; `cached_tokens=0` on all 62 ling:free rows vs the "~98% cache-hit" FROZEN_PREFIX claim (01, sec 3 C1/C2). Contradictions rot into law drift unless triaged.

## 2. Triage rule (the deliverable)

Each scheduled triage pass applies these triggers to every banked row:

- **CLIMB (to funded/verification):** (a) repo-byte check passes, as F1 (`mag/percolator.py:353` verified, `rewards.jsonl` absent); or (b) two-lane independent convergence on a NEGATIVE, as F4; or (c) row feeds a live meter (`record_verdict` seed, F2). Climb requires naming instrument, moment, and context assumptions - e.g. cache numbers are openrouter-reported, moment 2026-09-30, valid only if the meter logs successes and failures.
- **DIE:** (a) dedupe class `work_id+class` already in register (the n* law: 122 rows = ~12 findings); (b) age > 72h with no climb trigger; (c) any citation carrying `ponytail_audit: {url: false}` (ts 2026-09-30T17:20:16Z) is barred from corpus promotion permanently.
- **CONTRADICT (hold, re-measure):** row contradicts a rib - do not amend law from free-lane bytes; spawn a funded verification task (C1 caveat: "check the impfeed error path before rewriting law").

## 3. Failure mode guard

The known rot risk is that `STEALTH_TRIAGE_20260930.md` itself becomes a second append-only bank: its own continuation plan is "append a dated section to this file (v1+)" (01, sec 4) - the same append-only pattern that made the JSONL unreadable. Guard: every v(n+1) must (a) diff against v(n) TOP5 and explicitly re-rank or kill each item, and (b) mark consumed rows `TRIAGED` in the JSONL so the bank shrinks or the register grows, never both.

**Falsifier:** if v1 triage runs and the 09-28 rows are still unmarked/climbless after 72h, or a v1 TOP5 item repeats a v0 item without re-verification, the rule fails and the bank is confirmed dead weight.
