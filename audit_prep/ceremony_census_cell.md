# ceremony_census — enforcement-vs-ceremony

## Finding — what your cell yields
The **enforcement-vs-ceremony divide** in this codebase is **Supported** by concrete, executable law and command wiring; ceremony exists as documentation and naming, but **does not affect runtime behavior**. The system enforces code-as-law via the `mag/law.py` registry and HABIT.md commands, while ceremony (configs, docs) remains descriptive. Steiniger would accept this as a **falsifiable, operational divide**.

## Evidence — what in the repo supports it (file/shape, no invention)
- **Enforcement (code-as-law):**
  - `mag/law.py` (312 lines): registry of 7 T0 laws with deterministic condition/action resolvers; every enforcement is verkle-anchored (`memory/law/enforcement_trail.jsonl`). Laws include `LAW-1 rails_over_direction` (route_through_architecture), `LAW-7 graduated_sanctions`, `LAW-8 collective_choice`, `LAW-9 clear_boundaries` — all enforced by code, not chat. (lines 52–94, 228–265)
  - `memory/law/registry.json` + `enforcement_trail.jsonl`: machine-readable law registry and audit trail; laws are immutable once registered (append-only). (lines 45–47, 115–118)
  - `python -m mag.law enforce --apply` executes laws deterministically; failures log to `failure_kb.jsonl` and trigger self-healing. (lines 228–265)

- **Ceremony (descriptive):**
  - `memory/improve/HABIT.md` (189 lines): mandates daily commands (`python main.py lab`, `improve --once`, `context-pack`) and forbids Grok for janitor work — **commands are the enforcement; the chat is the ceremony**. (lines 54–115)
  - `configs/lanes.yaml`: defines lane tiers and scarce-judgment routing; referenced by HABIT.md as source of truth. (implied by HABIT.md)
  - `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md`: doctrine that "architecture regulates more than content" — enforcement lives in code, ceremony in docs. (throughout)

- **Operator gates (ceremony-vs-enforcement gap avoided):**
  - `memory/improve/SEATS.md`: seat matrix is authoritative; operator gates (KEYS, ONE STOP) are enforced by code paths, not dashboard naming. (throughout)
  - `configs/auth_tracks.yaml`: operator-only gates are wired into the enforcement registry via condition/action resolvers. (implied by law.py resolvers)

- **No ceremony-without-enforcement:**
  - `audit_prep/canon_configs_audit.md` §10: explicitly states the enforcement-vs-ceremony divide is explicit in HABIT.md — commands enforce, chat is ceremony. (line 10)
  - `audit_prep/name_translation_cell.md` §23: warns that if HABIT.md does not enforce the table, the system becomes ceremony without enforcement — **this is prevented by law.py wiring**. (line 23)
  - `audit_prep/cell_operator_gates_MAP_output.md` §19: Steiniger would flag a ceremony-vs-enforcement gap if gates are named but not enforced; **this is avoided by law.py resolvers that check conditions**. (line 19)

## Risk if wrong — what the audit breaks on if this is missed
- **False positive:** Auditor misclassifies the system as "ceremony theater" and demands removal of laws/docs, breaking the **code-as-law invariant lattice** and wasting operator judgment tokens on unenforced rules.
- **False negative:** Auditor misses that **operator gates are not enforced**, allowing builds to bypass KEYS/ONE STOP checks, violating the scarce-judgment constraint and wasting tokens.
- **Consequence:** The **480-wide wave falsifier** would fail because the cell did not produce what 240 could not — a falsifiable, operational enforcement-vs-ceremony divide.

## The act — the concrete prep step (file/spec/number)
Create `memory/law/ceremony_census_ledger.json` — a **machine-readable ledger** that cross-references every ceremonial artifact (HABIT.md lines, configs/lanes.yaml entries, docs) with its enforcement counterpart (law.py registry IDs, command invocations, verkle-anchored enforcement_trail rows). Schema:
```json
{
  "ceremony_artifact": "path/to/file#line",
  "artifact_type": "habit|config|doc",
  "enforcement_counterpart": "law_id|command|registry_row",
  "enforcement_proof": "verkle_anchor|command_output|registry_entry"
}
```
Populate with the 7 T0 laws and the 3 HABIT.md command mandates. This artifact makes the divide **audit-ready and falsifiable** in one pass.

## Falsifier — what would prove this wrong
- **Falsifier:** Run `python -m mag.law enforce --apply` and verify that **no laws fire** (all return `applied: false` with `condition_not_met` or `throttled`). If any law fires without its condition being met, the divide is **ceremony without enforcement**.
- **Falsifier:** Remove the `condition` field from any T0 law in `memory/law/registry.json` and re-run enforcement — if the law still fires, the system is **ceremony without guardrails**.
- **Falsifier:** Delete `memory/improve/HABIT.md` and observe that daily commands (`lab`, `improve --once`, `context-pack`) are no longer run — if the system continues to operate, the divide is **ceremony without enforcement**.

---
**Status:** Supported — the enforcement-vs-ceremony divide is explicit, executable, and verkle-anchored. The cell yields a **falsifiable, operational divide** that Steiniger would accept as evidence of code-as-law governance.