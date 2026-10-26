# COUNCIL DISPUTE VS CONSENSUS RAW LOGS & DELTA REPORT (Theses 44 & 45)

**Date:** 2026-10-17
**Source:** `watch/inbox/gstd_perimeter_build_20261010/runs/*` -> published in `falsifier-index/evidence/council/`
**Total Verified Runs Published:** 41

## 1. Per-Run Raw Log Index & Split (Consensus Set vs Dispute Set)

| Run Timestamp | Verdict | Tasks | Consensus Reached | Disputed (`consensus=null`) | Consensus Correct Rate | Dead-Salmon Noise | Raw Receipt Log |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `20261010T194150Z` | `NOISE-CLASS` | 3 | 3 | 0 | 1.0000 | 1.0000 | `raw_receipt_20261010T194150Z.jsonl` |
| `20261010T195011Z` | `STRUCTURE` | 13 | 12 | 1 | 0.6154 | 0.3127 | `raw_receipt_20261010T195011Z.jsonl` |
| `20261010T225359Z` | `NOISE-CLASS` | 5 | 5 | 0 | 0.0000 | 1.0000 | `raw_receipt_20261010T225359Z.jsonl` |
| `20261011T000937Z` | `STRUCTURE` | 13 | 9 | 4 | 0.5385 | 0.2550 | `raw_receipt_20261011T000937Z.jsonl` |
| `20261011T022831Z` | `STRUCTURE` | 14 | 12 | 2 | 0.6429 | 0.1539 | `raw_receipt_20261011T022831Z.jsonl` |
| `20261011T235008Z` | `DEGENERATE-TASKBANK (distinct truths under 4; consensus untestable)` | 3 | 2 | 1 | 0.6667 | 0.2083 | `raw_receipt_20261011T235008Z.jsonl` |
| `20261011T235346Z` | `WEAK` | 5 | 2 | 3 | 0.4000 | 0.3690 | `raw_receipt_20261011T235346Z.jsonl` |
| `20261011T235623Z` | `WEAK` | 13 | 6 | 7 | 0.4615 | 0.3581 | `raw_receipt_20261011T235623Z.jsonl` |
| `20261011T235925Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3227 | `raw_receipt_20261011T235925Z.jsonl` |
| `20261012T031628Z` | `STRUCTURE` | 13 | 12 | 1 | 0.7692 | 0.3012 | `raw_receipt_20261012T031628Z.jsonl` |
| `20261012T031855Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3073 | `raw_receipt_20261012T031855Z.jsonl` |
| `20261012T043333Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2969 | `raw_receipt_20261012T043333Z.jsonl` |
| `20261012T044454Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2838 | `raw_receipt_20261012T044454Z.jsonl` |
| `20261012T135203Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.3265 | `raw_receipt_20261012T135203Z.jsonl` |
| `20261012T144148Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.3069 | `raw_receipt_20261012T144148Z.jsonl` |
| `20261012T145817Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.3000 | `raw_receipt_20261012T145817Z.jsonl` |
| `20261012T150209Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3058 | `raw_receipt_20261012T150209Z.jsonl` |
| `20261012T150823Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2519 | `raw_receipt_20261012T150823Z.jsonl` |
| `20261012T150946Z` | `STRUCTURE` | 13 | 12 | 1 | 0.6923 | 0.3196 | `raw_receipt_20261012T150946Z.jsonl` |
| `20261012T151257Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.3173 | `raw_receipt_20261012T151257Z.jsonl` |
| `20261012T151703Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3038 | `raw_receipt_20261012T151703Z.jsonl` |
| `20261012T152413Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.3158 | `raw_receipt_20261012T152413Z.jsonl` |
| `20261012T153741Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3135 | `raw_receipt_20261012T153741Z.jsonl` |
| `20261012T154159Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2858 | `raw_receipt_20261012T154159Z.jsonl` |
| `20261012T155320Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3088 | `raw_receipt_20261012T155320Z.jsonl` |
| `20261012T164855Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2927 | `raw_receipt_20261012T164855Z.jsonl` |
| `20261012T175736Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.3088 | `raw_receipt_20261012T175736Z.jsonl` |
| `20261012T220923Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2742 | `raw_receipt_20261012T220923Z.jsonl` |
| `20261013T082458Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2869 | `raw_receipt_20261013T082458Z.jsonl` |
| `20261013T085312Z` | `STRUCTURE` | 13 | 12 | 1 | 0.6923 | 0.2892 | `raw_receipt_20261013T085312Z.jsonl` |
| `20261013T090140Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2558 | `raw_receipt_20261013T090140Z.jsonl` |
| `20261013T090557Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2827 | `raw_receipt_20261013T090557Z.jsonl` |
| `20261013T102235Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3277 | `raw_receipt_20261013T102235Z.jsonl` |
| `20261013T102847Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2554 | `raw_receipt_20261013T102847Z.jsonl` |
| `20261013T215230Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2938 | `raw_receipt_20261013T215230Z.jsonl` |
| `20261014T120012Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.3012 | `raw_receipt_20261014T120012Z.jsonl` |
| `20261015T120006Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2677 | `raw_receipt_20261015T120006Z.jsonl` |
| `20261015T223909Z` | `STRUCTURE` | 6 | 6 | 0 | 1.0000 | 0.0483 | `raw_receipt_20261015T223909Z.jsonl` |
| `20261015T223957Z` | `STRUCTURE` | 6 | 2 | 4 | 0.3333 | 0.0667 | `raw_receipt_20261015T223957Z.jsonl` |
| `20261016T120019Z` | `STRUCTURE` | 13 | 11 | 2 | 0.6923 | 0.2885 | `raw_receipt_20261016T120019Z.jsonl` |
| `20261017T120006Z` | `STRUCTURE` | 13 | 10 | 3 | 0.6923 | 0.2831 | `raw_receipt_20261017T120006Z.jsonl` |

## 2. Shape-Level Breakdown (Where Disputes Concentrate)

- **Consensus Set (`extract-date`, $n=5$):** 100% consensus (`5/5` tasks), 100% accuracy (`5/5` correct). Zero dispute delta.
- **Near-Consensus Set (`extract-ext`, $n=5$):** 80-100% consensus (`4-5/5` tasks), 60% accuracy (`3/5` correct; false consensus on 1-2 items when small models share tokenization bias).
- **Dispute Set (`classify`, $n=3$):** 33-67% consensus (`1-2/3` tasks reach quorum; `1-2/3` tasks remain actively disputed with `votes=2` across 5 models). On disputed `classify` tasks, single-model answers split across `test`/`verification`/`ractor` and `memory`/`security`/`model`, preventing false-consensus lock-in.

## 3. Verification Command

Every raw task prompt, 5-model answer array, vote count, and truth label is preserved byte-for-byte in `falsifier-index/evidence/council/raw_receipt_<ts>.jsonl` and `raw_ledger_<ts>.jsonl`.
