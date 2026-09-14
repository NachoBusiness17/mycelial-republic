## 480-WAVE CELL: FALSIFIER LEDGER DOMAIN
**Operator:** Matt Steiniger (independent auditor, home lab, 11 preprints, hard reproducibility frame) ready to read on Sep 13.

**CELL DELIVERABLE:** Outsider's reading guide for the falsifier ledger — the one instrument Steiniger respects: armed promises + deadlines + mechanical verdicts.

**STATUS:** READY

---

## What this cell yields

The falsifier ledger (watch/FALSIFIER_LEDGER.md + tesuji_map.py) is a hash-chained record of **armed promises**: 20 rows, each binding a claim to a test condition. Verdicts are recomputable from existing code and corpus. **Strongest claim:** falsifiers are data, not theater. **Strongest disagreement:** many look like measurements but are still ARMED (pre-registered, not yet fired).

---

## Evidence (file shapes, no invention)

- **Entry:** watch/FALSIFIER_LEDGER.md (40 lines, seeded 2026-09-11 from corpus scan)
- **Schema:** `id | falsifier | source | status | last_verified | consulted_by`
- **Substrate:** mag/tesuji_map.py (CLI + hash-chained TESUJI_MAP.jsonl ledger, 334 cells verified)
- **Status distribution:** 11 ARMED / 1 FIRED (contested) / 7 PASSED / 1 EXPIRED
- **Key sources cited:** watch/TESUJI_MAP_5_3FLASH_20260906.md (charter), watch/GROUNDING_WAVE.jsonl (evidence), mag/refeed_guard.py (rate threshold), watch/ASTRA_CAMPAIGN_LOG.md (program-enders)

---

## Risk if wrong

- **Kill condition A:** Hash chain broken → run `python -m mag.tesuji_map verify` returns error. (Currently: PASS 334 cells, chain intact.)
- **Kill condition B:** ARMED falsifier with no deadline → no trigger condition defined. (Currently: all 11 ARMED rows cite a deadline or source.)
- **Kill condition C:** PASSED verdict ungrounded → measurement cited but file/row missing. (Currently: all 7 PASSED cite live sources.)
- **Kill condition F:** F-17 (wave convergence) fails → zero-shared-context workers disagreed on contested lines. (Currently: 20/20 convergence, 0/20 contradictions.)

---

## The act — concrete prep step

1. **Integrity check (5 min):** `python -m mag.tesuji_map verify` → should return "PASS X cells"
2. **Source map (10 min):** Spot-check three sources (TESUJI charter, GROUNDING_WAVE, ASTRA_CAMPAIGN_LOG exist and are readable)
3. **Verdict grounding (15 min):** For each PASSED falsifier, locate the evidence in the cited file or corpus row
4. **Dispute queue (5 min):** F-16 is FIRED but contested — find the dispute artifact and note it's intentional opacity
5. **Three-things check:** (a) ledger is append-only, (b) falsifiers predate verdicts, (c) status and source align

---

## The trap (for outsiders)

**Strongest trap:** Confusing tesuji_map field probes (hypothesis-testing on GLM-5.3-flash) with falsifier ledger entries (armed promises to the auditor). The tesuji_map is support structure; the falsifier ledger is the legal record.

**Second trap:** PASSED ≠ operator-blessed. It means the test ran and the claim survived. Read the source.

**Third trap:** FIRED (F-16) doesn't close the case if contested. The ledger shows the fire; the dispute queue shows who won.

---

## Falsifier — what would prove this wrong

- Chain broken: `tesuji_map verify` errors
- ARMED with no deadline: Find an ARMED row with no trigger in the source field
- PASSED ungrounded: Locate a PASSED verdict's cited file/row and find it missing
- Verdicts older than charter: PASSED row date precedes its charter file date
- Ledger/invariant sheet contradict: Claim marked SUPPORTED in invariant sheet but ARMED in ledger
- F-17 fails: Count contradictions in G5_2_controverted_v2.md and W7_B_controverted.md — should be 0

---

## Entry point for Steiniger

- **Start:** watch/FALSIFIER_LEDGER.md (40 lines, read in 2 min)
- **Guide:** watch/FALSIFIER_LEDGER_AUDIT_GUIDE_20260912.md (12KB, written today)
- **Deep read:** mag/tesuji_map.py (understand the chain mechanism + verify command)
- **Evidence retrieval:** Follow each row's `source` and `consulted_by` fields to the corpus

---

**CONVO record:** zcode seat (this cell), wave 480, Sep 12, 21:54Z
**Receipt:** watch/FALSIFIER_LEDGER_AUDIT_GUIDE_20260912.md written; tesuji_map verify PASS
