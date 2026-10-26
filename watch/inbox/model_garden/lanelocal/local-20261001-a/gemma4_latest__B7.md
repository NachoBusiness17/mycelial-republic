# garden-v1-B7 | gemma4:latest | series local-20261001-a | instrument=lane-local-script
# finish=length prompt_tokens=4099 completion_tokens=2048 wall_s=76.19 tok_s=26.9 checks=0/4 {'A1-ITEM': 0, 'A1-PATH': 0, 'A2-CONCEPT': 0, 'A3-COUNT': 0}

## System Health Report: Burn Wave 2026-09-26 Commit Deliverable

This report summarizes the set of structural and maintenance fixes (B2-542 through B2-553) landed concurrently for the 2026-09-26 burn wave. Each fix addresses systemic data, state, or process attribution flaws that, if left unfixed, would degrade reliability, portability, or auditability.

***

### B2-542: `ask_router` Receipt Stale State Gap (Self-fed by B2-521)

**Context:** The `ask_router` mechanism uses time-stamped receipts (`receipts.jsonl`). If the system stagnates (e.g., running tests or auditing without live dogfood traffic), the receipt row appears stale relative to the current date (2026-09-26).
**The Fix:** The integration of a mandatory process to run a bounded, live `ask_router` dogfood step (e.g., via `mag/dogfood_audit.py`) ensures that fresh receipt entries are written to `receipts.jsonl`, re-establishing the temporal ground truth for downstream tooling like `mag/elder.py` and test assertions in `test_organ_map.py`.

| Example Type | Scenario | Expected Outcome (Post-Fix) | Contrast/Failure State (Pre-Fix) |
| :--- | :--- | :--- | :--- |
| **Positive** | A full CI run completes, but the explicit `ask_router` dogfood step is executed successfully. | The `receipts.jsonl` file gains a new row with a timestamp matching the current execution date. `test_map_and_elder_surface_callable_orphans` passes. | The test fails because the last recorded timestamp is significantly older than the current test run date. |
| **Negative** | Running the test suite while ignoring the explicit dogfood step. | The test suite continues without warning or failure, as the necessary state is current. | The test suite halts or fails, attributing the failure to a temporal inconsistency (stale receipt). |

***

### B2-543: Atlas LIVE Promotion Clock Rot (Self-fed by B2-521)

**Context:** The `atlas` state within `test_organ_map.py` requires a "LIVE" promotion flag in a row's levels, which is only granted by a recent, durable "fireball dogfood chain" receipt. The last run was too old (Aug 30).
**The Fix:** Either re-running the specific, named "fireball dogfood chain" necessary to generate a fresh, durable `atlas` receipt, *or* updating the test framework to register the promotion window with a named, acceptable manual exception rationale, allowing the test to proceed correctly.

| Example Type | Scenario | Expected Outcome (Post-Fix) | Contrast/Failure State (Pre-Fix) |
| :--- | :--- | :--- | :--- |
| **Positive** | Executing the controlled "fireball dogfood chain" promotion process. | The `memory/runs/atlas` file is updated with a transaction containing the "LIVE" promotion status and the current date's timestamp. `test_map_separates_callable_from_live` passes. | The test fails, citing that the required "LIVE" status is missing or that the transaction timestamp predates the current day's operational context. |
| **Negative** | Attempting to validate the atlas state without performing the required chain promotion activity. | The test framework detects the missing *proof of activity* and halts, requiring the designated remediation step rather than passing incorrectly. | The test passes incorrectly, suggesting the state is valid when its underlying promotion evidence has expired or become inaccessible. |

***

### B2-544: `qdrop_export` Sibling CRLF Normalization (Self-fed by B2-239)

**Context:** The `qdrop_export` directory contains multiple data siblings (`q_caption_ledger.jsonl`, `deep_read_chunks.jsonl`, etc.). The existing B2-239 rule only applies to `q_caption_ledger.jsonl`. All other files are susceptible to arbitrary CRLF contamination, which reads as full-file churn and requires manual intervention.
**The Fix:** Identifying the documented writer for each of the five relevant files (including `.json` receipts). For each file, the writer's native line ending must be confirmed (using its receipt metadata), and the verifier must be updated with a mandatory, bytes-level `\r\n` ending assertion.

| Example Type | Scenario | Expected Outcome (Post-Fix) | Contrast/Failure State (Pre-Fix) |
| :--- | :--- | :--- | :--- |
| **Positive** | A system audit runs across the entire `qdrop_export` directory after the lane closes. | All five files pass verification, each showing its expected non-CRLF (or correctly-normalized CRLF) endings, and the process successfully records the before/after SHA256 pair for the normalization event. | One or more files are found to contain carriage return (`\r`) characters in the content, forcing a misleading full-file churn event during subsequent commits. |
| **Negative** | A developer copies a file from a non-standard source into `qdrop_export`. | The verifier flags the newly arrived file because it fails the defined, canonical line-ending assertion for that file type's expected writer/format. | The file is accepted without complaint, propagating inconsistent line endings and making diffs unreadable. |

***

### B2-545: `.gitattributes` Smudge Guard for SHA-Cited JSONL Artifacts (Self-fed by B2-239)

**Context:** The `core.autocrlf=true` global setting means that *any* checkout operation on a file lacking explicit `.gitattributes` guidance risks silent CRLF expansion/contraction. Since critical data artifacts (like ledger JSONs) are cited by SHA in receipts, they must be protected.
**The Fix:** Extending the `.gitattributes` file to explicitly mark all SHA-cited data artifacts (specifically `watch/inbox/**/*.jsonl` ledgers and registries) as `binary`. This overrides the smudge filter, preventing Git from ever interpreting, modifying, or touching these mission-critical files upon checkout.

| Example Type | Scenario | Expected Outcome (Post-Fix) | Contrast/Failure State (Pre-Fix) |
| :--- | :--- | :--- | :--- |
| **Positive** | A clean clone or `reset --hard` operation is performed by Git on a repository containing a cited JSONL artifact. | The JSONL file remains byte-for-byte identical to its SHA record, and the Git status operation confirms that the file type is recognized as `binary: set` by the attribute checker. | The file undergoes automatic CRLF conversion, changing the contents and thus altering the verifiable SHA hash, breaking the receipt's integrity chain. |
| **Negative** | Attempting to patch a non-JSONL, textual file that is adjacent to a ledger file. | The smudge filter correctly processes the `.txt` file according to its normal rules, leaving the adjacent `.jsonl` artifact untouched and protected. | Contextual confusion leads to the smudge filter interacting unpredictably between artifact types
