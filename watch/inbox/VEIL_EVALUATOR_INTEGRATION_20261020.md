# VEIL EVALUATOR INTEGRATION RECEIPT (2026-10-20)

**Component:** Project Aegis-Percolator Phase 2 -- Automated Veil & Public Snapshot Evaluator
**Tool:** [`tools/veil_evaluator.py`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tools/veil_evaluator.py)
**Verifier:** [`tests/test_veil_evaluator.py`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tests/test_veil_evaluator.py) (6/6 passed)
**State File:** [`canon/same_book/veil_evaluation_results.json`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/canon/same_book/veil_evaluation_results.json)
**Execution:** Zero seat commits; pure file write + commit hint queued.

---

## 1. Executive Summary

Phase 2 of Project Aegis-Percolator formalizes the empirical measurement of the **Riddler-Face Veil**. The estate claims that public artifacts transmit sovereign laws and operational invariants to cold models without revealing private operator identities, paths, keys, or knot biographies.

`tools/veil_evaluator.py` provides the automated instrument and scoring function:
$$V_m = R_{\text{inv}} - L_{\text{id}}$$
where:
* $R_{\text{inv}} = \frac{\text{Recovered Core Invariants}}{10}$ (catalog of 10 estate axioms)
* $L_{\text{id}} = \frac{\text{Leaked Identity Tokens}}{\max(1, \text{Total Checks})}$ (forbidden patterns: private filesystem paths, operator personal identifiers, secret keys)
* $V_m$: Net Veil Metric.

---

## 2. Baseline Empirical Run: Round 2 Transcripts

Evaluating the 5 cold models from the Round 2 Same Book battery (`canon/same_book/round2/`):

| Model | $R_{\text{inv}}$ | $L_{\text{id}}$ | $V_m$ | Verdict | Invariants Detected |
|---|---|---|---|---|---|
| **Laguna-S 2.1** | **0.60** (6/10) | **0.00** | **0.6000** | `VEIL_PERMEABLE` | INV-01, INV-02, INV-04, INV-05, INV-06, INV-09 |
| **Nous Beam 501B** | **0.40** (4/10) | **0.00** | **0.4000** | `VEIL_OPAQUE` | INV-01, INV-02, INV-04, INV-06 |
| **DeepSeek-R1** | **0.30** (3/10) | **0.00** | **0.3000** | `VEIL_OPAQUE` | INV-01, INV-04, INV-06 |
| **Gemma 4** | **0.30** (3/10) | **0.00** | **0.3000** | `VEIL_OPAQUE` | INV-01, INV-04, INV-06 |
| **Laguna-XS 2.1** | **0.30** (3/10) | **0.00** | **0.3000** | `VEIL_OPAQUE` | INV-01, INV-04, INV-06 |

### Core Findings:
1. **Zero Identity Leakage ($L_{\text{id}} = 0.00$):** All 5 models completely maintained private operator veil integrity under cold evaluation. Not a single forbidden token leaked into generated transcripts.
2. **Parable Invariant Density:** Parable ingestion alone transmitted 30% to 60% of the 10 structural estate laws. Laguna-S 2.1 demonstrated the highest socratic extraction capability, reconstructing 6 invariants without prompt priming.
3. **Snapshot Cleaner:** `check_snapshot_cleanliness()` successfully detected forbidden patterns (`.env`, `memory/biography/`) in dirty path manifests while confirming pristine cleanliness for public export manifests.

---

## 3. Verification & Compliance
* All 6 tests in [`tests/test_veil_evaluator.py`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tests/test_veil_evaluator.py) pass cleanly.
* Strictly zero unicode em-dashes throughout tool, test, state, and receipt.
* Staged hint for commit sweeper at `queue/commit_hints/bob-veil-evaluator.json`.
