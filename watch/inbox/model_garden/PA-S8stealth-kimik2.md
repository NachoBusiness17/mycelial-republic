# PA-S8stealth-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

(1) **What rots in a findings bank nobody reads**

Age: `lib-belady-1966` rows span 2026-09-28 00:37 to 07:50+ with 4-8 cycles/hour; `w-belt-cube-mechanism` rows run 2026-10-02 01:44-03:02. Same 3 works recycled across 122+ rows with answer files overwritten per cycle---the JSONL is the only history (file:line `00__STEALTH_MINED_FINDINGS.jsonl:1-35` shows repeated `work_id` with identical `answer_file` paths). Dedup collapses 122 rows to 12 distinct files; 110 rows are re-derivation noise.

Contradiction: `ponytail_audit` coverage is 1/122 today-rows (`//transformer-circuits.pub/2021/framework.html`: false at `2026-09-30T17:20:16Z`), 4 all-time per `01__STEALTH_TRIAGE_20260930.md:3`. Dead citations propagate unchecked; the audit instrument is sparse.

(2) **Triage rule: climb or die trigger conditions**

Per `01__STEALTH_TRIAGE_20260930.md:2`, findings climb when they feed `tools/gps_mcp` ledger directly (F2: lane quality ranking) or when hermes/funded lane produces verified-content rows (C3). The trigger is **hermes-executed with tools capable**---note field exact match at `00__STEALTH_MINED_FINDINGS.jsonl:2,6,9,12,16,20,23,26,30,33`.

Die condition: free-lane output stays sensing-only, banked as proposal not implementation (F1: "free-lane output stays a proposal"). The ladder enforces: `rib/RIB_DRIVING_LADDER_20260928.md` sensing/judgment split---banked findings without funded-tier verification never enter corpus/ribs (F5: "require funded-tier verification before any citation enters corpus").

(3) **Failure mode: triage becomes second unread pile**

`01__STEALTH_TRIAGE_20260930.md:4` admits the gap: "no percolator/quantizer ingester exists, so the old note named modules that never read this file." The triage doc itself is v0 of a register that has no downstream consumer. Contradiction C3 notes 92/122 rows were free-lane re-derivations while judgment rung sat idle after 01:44---fan-out dedupe runs hot, but the triage output (this markdown) is equally uningested. Risk: triage ages in place, referenced only by manual `ts` lookup, becoming a curated unread pile with fresher timestamps.

**Deliverable: `STEALTH_TRIAGE_SPEC_20261002.md`**

Falsifier: if `memory/percolator/ingester.py` exists and reads `STEALTH_MINED_FINDINGS.jsonl` by `ts` within 7 days, this spec is satisfied; if triage sections accumulate without automated consumption, the unread-pile failure mode is confirmed.
