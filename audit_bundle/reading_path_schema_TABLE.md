## Reading Path Schema Table (audit-ready)

**Purpose:** Provide a falsifiable, one-page table that an external auditor (Matthew Steiniger) can use to trace the analyst's reading path through the codebase. 

**Mode:** EXTEND — add a single prep artifact to the existing audit_bundle (1,564 files / 20.5MB).

---

### 1) Finding — what your cell yields

A concise, falsifiable table that maps analyst entry points → canonical files → verification artifacts → falsifier checks. It answers the examiner's one-question requirement: "What path does an analyst follow, and how is it verified?"

---

### 2) Evidence — what in the repo supports it (file/shape, no invention)

- **Entry Points:** `AGENTS.md:7`, `docs/ref/RTFM_20260904.md`, `dashboard/static/claim_check.html`, `memory/biography/verkle_chain.jsonl`
- **Canonical Files:** `audit_prep/verkle_chain_READING_GUIDE.md`, `audit_prep/CLAIM_METRIC_SCHEMA.md`, `scripts/analyze_claim_timing.py`
- **Verification Artifacts:** `audit_bundle/INDEX.json`, `audit_bundle/audit_bundle_manifest.md`, `memory/biography/verkle_chain.jsonl`
- **Falsifier Checks:** `EXTERNAL_AUDIT_FALSIFIER_LEDGER_CELL_20260912.md`

---

### 3) Risk if wrong — what the audit breaks on if this is missed

- The examiner cannot falsify the "reading path" because it is not documented in a falsifiable form.
- The "one hour to first true claim" metric cannot be reproduced or falsified without a defined path and timing instrumentation.
- The audit fails its reproducibility requirement (Steiniger: "hard reproducibility — scripts and figures ride every record").

---

### 4) The act — the concrete prep step (file/spec/number)

Create `audit_bundle/reading_path_schema_TABLE.md` with the following schema:

```markdown
| # | Entry Point | Canonical File | Verification Artifact | Falsifier Check | Status |
|---|-------------|----------------|------------------------|------------------|--------|
| 1 | AGENTS.md (line 7) | AGENTS.md | `memory/biography/verkle_chain.jsonl` (first knot) | Chain continuity (hash, previous_hash) | ✅ |
| 2 | RTFM_20260904.md | docs/ref/RTFM_20260904.md | `audit_prep/verkle_chain_READING_GUIDE.md` §2 | Reading guide matches RTFM structure | ✅ |
| 3 | claim_check.html | dashboard/static/claim_check.html | `scripts/analyze_claim_timing.py` (is_true_claim criteria) | Timing instrumentation present | ⚠️ |
| 4 | verkle_chain.jsonl | memory/biography/verkle_chain.jsonl | `scripts/analyze_claim_timing.py` (first 100 knots) | 0 true claims found in first 100 knots | ❌ |
| 5 | CLAIM_METRIC_SCHEMA.md | audit_prep/CLAIM_METRIC_SCHEMA.md | `scripts/analyze_claim_timing.py` (criteria) | Criteria defined: dominant_theme, tension_index>0.5, operational terms | ✅ |
| 6 | INDEX.json | audit_bundle/INDEX.json | `audit_bundle/audit_bundle_manifest.md` §135 | Bundle manifest references INDEX.json | ✅ |
```

**File:** `C:/Users/foste/Documents/projects/local_sovereign_agent/audit_bundle/reading_path_schema_TABLE.md`
**Size:** ~600 bytes
**Added:** 2026-09-13T22:00:00Z

---

### 5) Falsifier — what would prove this wrong

- Discovery of a prior falsifiable reading path table that predates this audit prep.
- Evidence that the examiner's reproducibility requirement (scripts + figures + timing) was already satisfied before this prep.
- Any instrumented timing system that predates `scripts/analyze_claim_timing.py` (2026-09-13).

If any of these exist, the table is WRONG and the reading path is already falsifiably documented.

---

**Filed by:** zcode (audit seat)  
**For:** EXTERNAL_AUDIT_20260912  
**Examiner:** Matthew Steiniger (/Reboot)