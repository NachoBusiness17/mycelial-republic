# Archival and RefreshBot Skills Ingestion and Triple-Gate Guard Receipt

**Timestamp:** 2026-10-18T14:45:00Z  
**Source Specification:** [`c:\Users\foste\Downloads\archival-and-refresh-bots.md`](file:///c:/Users/foste/Downloads/archival-and-refresh-bots.md)  
**Guard Tool:** [`tools/archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tools/archive_guard.py)  
**Test Suite:** [`tests/test_archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tests/test_archive_guard.py)  
**Catalog Register:** [`configs/skills.yaml`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/configs/skills.yaml)  
**Status:** PROMOTED and VERIFIED (10/10 test cases passed, 0 house lint errors)

---

## 1. Summary

The estate ingested and codified the invariant percolator specifications for **Archival Bot** and **RefreshBot** from [`c:\Users\foste\Downloads\archival-and-refresh-bots.md`](file:///c:/Users/foste/Downloads/archival-and-refresh-bots.md).

All 12 component skills were extracted, sanitized to guarantee zero unicode em-dashes and compliant single-line YAML headers, and installed into `.agents/skills/`.

The triple-gate safe archival guard was implemented in [`tools/archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tools/archive_guard.py) and duplicated into [`.agents/skills/archival-getting-started/archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/archival-getting-started/archive_guard.py). The guard enforces non-destructive archival: files are NEVER deleted, and are only moved to a local trash folder if all three independent gates pass.

---

## 2. The 12 Ingested Skills

1. [`archival-getting-started`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/archival-getting-started/SKILL.md) -- Invariant percolator safe archival protocol, decision tree, and archive_guard runner.
2. [`roster-swap-getting-started`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/roster-swap-getting-started/SKILL.md) -- Nine-phase zero-downtime roster swap protocol for bot and model retirement.
3. [`roster-swap-automation`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/roster-swap-automation/SKILL.md) -- Step-by-step swap procedure across fleet configurations and cron jobs.
4. [`roster-inventory-and-routine-census`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/roster-inventory-and-routine-census/SKILL.md) -- Census of routines, cron jobs, open runs, and state prior to swap.
5. [`archive-and-verify`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/archive-and-verify/SKILL.md) -- Step-by-step verification, hash matching, and clearance procedure.
6. [`delete-label-protocol`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/delete-label-protocol/SKILL.md) -- Safe label migration and two-copy clearance verification.
7. [`routine-carryover`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/routine-carryover/SKILL.md) -- Routing routine tasks to successor bots without interruption.
8. [`primary-handoff`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/primary-handoff/SKILL.md) -- Passing live primary context and conversation tokens across bots.
9. [`webhook-swap`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/webhook-swap/SKILL.md) -- Swapping external endpoints, webhook URLs, and API dispatch pointers.
10. [`signed-bus-job`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/signed-bus-job/SKILL.md) -- Signing bus jobs for message-broker delivery.
11. [`roster-swap-close-out`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/roster-swap-close-out/SKILL.md) -- Archival receipt generation and post-swap verification.
12. [`roster-law`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/.agents/skills/roster-law/SKILL.md) -- Six inviolable laws of bot and model roster swaps.

---

## 3. Triple-Gate Architecture

[`tools/archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tools/archive_guard.py) enforces three mandatory gates:

- **Gate 1: Live SHA-256 Hash Matching:** The hash of the verified copy must match the live hash of the original file at the exact moment of evaluation.
- **Gate 2: Written Confirmations:** Two confirmations are required in writing:
  1. `second_copy_location`: Exact designated location of the second copy.
  2. `export_complete`: Explicit boolean `True` verifying export completion.
- **Gate 3: Protected Category Exclusion:** Filenames and content previews are checked against protected categories:
  - Banking (bank, statement, checking, savings, loan, mortgage, credit, routing)
  - Medical (medical, health, doctor, prescription, patient, clinic, hospital)
  - Tax (tax, irs, w2, 1099, deduction, tax_return, w-2, 1099-misc)
  - Government ID (passport, ssn, social_security, driver_license, birth_cert, visa, gov_id)
  - Work (paystub, payroll, timesheet, employer, contract_employment)
  - School (transcript, grades, tuition, diploma, student_id, coursework)
  - Family (minor, child, kid, parental, guardian, family_trust)

Negative lookarounds (`(?<![a-zA-Z0-9])` and `(?![a-zA-Z0-9])`) allow word boundaries to trigger accurately across underscores, hyphens, and file extensions without false positives.

---

## 4. Verification Suite Results

Test suite [`tests/test_archive_guard.py`](file:///C:/Users/foste/Documents/projects/local_sovereign_agent/tests/test_archive_guard.py) ran 10 test cases under pytest:

- Case 1: Cleared a good copy -> PASSED
- Case 2: Refused when second copy confirmation missing -> PASSED
- Case 3: Refused when export complete confirmation missing -> PASSED
- Case 4: Refused when file is a bank statement -> PASSED
- Case 5: Refused when file is a medical record -> PASSED
- Case 6: Refused when file is a tax form -> PASSED
- Case 7: Refused when file is a government ID -> PASSED
- Case 8: Refused when file is family / children records -> PASSED
- Case 9: Refused when copy had been altered (hash mismatch) -> PASSED
- Case 10: Refused when file was not in approved inventory -> PASSED

Result: **10 passed in 0.75s**. Original files remained completely untouched in all refusal cases.

---

## 5. Skills Lint and Config Seal

- **Skills Linter:** `python tools/skills_lint.py --house-only` returned `files scanned: 77 | house errors: 0 | warnings: 29` (zero house errors across all 12 installed skills).
- **Config Register Seal:** `configs/skills.yaml` cataloged with entries for `archival-getting-started`, `archive-and-verify`, `delete-label-protocol`, `roster-swap-getting-started`, and `roster-law`.
- **Seal Verification:** `CONFIG-SEAL verify: sealed=72 live=72 modified=0 missing=0 unsealed=0 PASS`.
