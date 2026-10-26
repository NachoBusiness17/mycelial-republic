# FALSIFIER LEDGER — OUTSIDER'S READING GUIDE
**For Matthew Steiniger | Sept 2026**

---

## Finding — what this cell yields

The falsifier ledger (watch/FALSIFIER_LEDGER.md + tesuji_map.py + TESUJI_MAP.jsonl) is the codebase's only mechanical instrument for "armed promises" — claims explicitly bound to test conditions. The rung falsifier (480 produces what 240 could not): **falsifiers are data, not assertions**. Every row is hash-chained; every verdict is recomputable from existing code and corpus; no falsifier is pre-judged.

**Strongest claim:** Falsification is live: F-01 through F-20 are registered (10 ARMED / 7 PASSED / 1 FIRED contested / 1 EXPIRED / 1 PARTIAL). Only a falsifier with a verdict (FIRED, PASSED) is a settled claim. ARMED falsifiers are debt — not settled, not resolved.

**Strongest disagreement with obvious reading:** You might read F-01 (Tesuji predictive) as "prediction accuracy measured and passed." It hasn't fired yet — it's ARMED, pre-registered, waiting for the T1 grid probe to run ($0.03 GO-gated). What looks like measurement data in the note is charter metadata, not verdict. The difference matters: the ledger is honest about what isn't done.


---

## Evidence — what in the repo supports it (file/shape, no invention)

### Entry point
- **`watch/FALSIFIER_LEDGER.md`** (40 lines, last updated Sep 10, 17:55)
  - Seeded by corpus scan: falsifier/falsifies/would retire/would kill across watch/, configs/, mag/ (194 unique falsifier lines from invariant sheet)
  - Schema: `id | falsifier | source | status | last_verified | consulted_by`
  - 20 rows, one per armed promise

### Mechanical substrate
- **`mag/tesuji_map.py`** (173 lines)
  - CLI: `python -m mag.tesuji_map post --axis A1 --cell "..." --probe "..." --verdict {SUPPORTED|DISPUTED|UNPROVEN|SHADOW} --resp-hash <hash>`
  - Ledger: `watch/TESUJI_MAP.jsonl` (hash-chained, like a mini-blockchain; prev/ts/seat/axis/cell/probe/resp_hash/verdict/tokens/ms/note/hash per row)
  - Render: `watch/TESUJI_MAP.md` + `dashboard/static/tesuji_map.json` (regenerated on every post)
  - Verify command: `python -m mag.tesuji_map verify` (checks prev-hash chain and row integrity)

### Ledger anatomy
- **Status vocabulary:** ARMED (test defined, not fired) / FIRED (test killed claim) / PASSED (test ran, claim survived) / EXPIRED (window closed, unresolved) / PARTIAL (multi-leg, some legs PASSED/ARMED, split status)
- **Verdicts (tesuji rows):** SUPPORTED (capability confirmed) / DISPUTED (inconsistent) / UNPROVEN (untested) / SHADOW (refusal/failure cell)
- **Sources cited in falsifier ledger:**
  - watch/TESUJI_MAP_5_3FLASH_20260906.md (charter for A1–A6 axes, probes, grid shape)
  - watch/FILTER_1301_SHADOW_20260910.md (1301-fork moderation incident shadow cell F-04)
  - mag/refeed_guard.py + watch/GROUNDING_WAVE.jsonl (cache re-feed rate falsifier F-05, 94% pass threshold)
  - watch/PYRAMID_VISION_20260911.md + GROUNDING_WAVE rows (coldest-vertex gate, top-5 mass ≥30%, CONFIRMED at 60.7%)
  - configs/riddler_charged_graphs.yaml (charged-register transport, 336-term falsifier, 0 hits)
  - watch/THOUGHT_PRIMITIVE_V0_20260901.md [AUDIT-TYPED 2026-09-08] (reasoning-over-citations predicts riddler decisions)
  - watch/inbox/MAX_DISTILL_EPOCH2_SPEC_20260911.md §5 (three pre-registered epoch-2 arms: F-09 PRIMARY, F-10 SECONDARY, F-11 TERTIARY)
  - watch/ASTRA_CAMPAIGN_LOG.md (program-ender falsifiers, no rescue clause, F-13)
  - watch/salon_source_moon_speak_20260911.md (desk F-H0 rejection counter, F-14)
  - astra hold corpus / ANSWER_2.md / instance grading (separation falsifier F-15, desk review reconstruction bar ≥50%)
  - watch/salon_runner.py (S3 protocol falsifier: every Socratic rebuild ends with "one falsifier: what kills this?" — F-20)

### Tri-state contract
- **Falsifier rows explicitly carry source + status.** Status distribution at seed (2026-09-11): 10 ARMED / 1 FIRED (contested, dispute queue) / 7 PASSED / 1 EXPIRED / 1 PARTIAL.
- **F-16 (I4 re-run):** FIRED but contested — verdict lies in a dispute queue, not settled yet. The ledger shows it publicly.
- **F-02, F-03, F-05, F-06, F-07, F-08, F-17:** PASSED — all cite measurement source or corpus card (GROUNDING_WAVE rows, invariant sheet, wave protocol records).

---

## Risk if wrong — what the audit breaks on if this is missed

### If falsifiers aren't real (only theater)
- **Claim collapses:** "This codebase's identity lives in a signed chain, not process logs." The chain is worthless if promises aren't backed by tests.
- **Audit fails:** Steiniger's frame (falsifiable claims + hard reproducibility) will find that the ledger is a post-hoc narrative, not a pre-registered commitment.
- **Substrate migration (Oct 27) becomes unverifiable:** If F-01 through F-11 don't fire, the Oct-27 move to 4× Mac Studio is built on unmeasured claims.

### If falsifiers are live but the ledger is corrupted
- **Entry point:** Read the TESUJI_MAP.jsonl hash chain. If rows past a certain point show broken prev pointers or hash mismatches, trust ends at that row. Run `python -m mag.tesuji_map verify` in your environment.
- **If verify fails:** The corpus is either corrupted on disk or has been edited in place (no append-only discipline). This is the audit's kill condition.
- **If sources cited don't exist:** Falsifiers with broken source links (watch/TESUJI_MAP_5_3FLASH_20260906.md missing, mag/refeed_guard.py absent) cannot be grounded. This is the audit's second kill condition.

### If ARMED falsifiers outnumber PASSED/FIRED verdicts significantly
- **Current state:** 10 ARMED vs 8 settled (7 PASSED + 1 FIRED). Ratio: 55% debt / 45% settled.
- **Risk:** If the audit opens on Sep 13 and 9 of the 10 ARMED rows have still never fired by Oct 15, the ledger is a wishlist, not a ledger. The house's strongest opening should answer this: deadlines for ARMED rows are in the source docs (F-09/F-10/F-11 fire on epoch-2 completion; F-01 fires on T1 grid run, GO-gated; F-13 fires on campaign end; F-14 fires on 3 desk rejections).

### If falsifiers and tri-state claims contradict
- **Check:** Take any SUPPORTED or DISPUTED verdict in the invariant sheet and find its corresponding falsifier in the ledger. If the falsifier is still ARMED, the claim in the invariant sheet is faster than the ledger — stale signal.
- **Example:** Invariant sheet (2026-09-10) may say "top-5 ≥30% CONFIRMED" but if the falsifier (F-06) is still ARMED, the measurement may not have fired yet. Read the source (GROUNDING_WAVE rows) to settle the order.

---

## The act — the concrete prep step (file/spec/number)

### Prep step 1: Falsifier ledger integrity check (5 min)
```bash
# fence-owner: falsifier-lane auditor - guide command, meant to be re-run per the guide. FW-11 2026-09-28; receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
cd local_sovereign_agent
python -m mag.tesuji_map verify
# Should return: (True, "OK") or identify a broken row number
```
**If broken:** Stop. The auditor cannot trust any derived claims until the chain is repaired. Report the row number and the mismatch type (prev-hash or internal hash).

### Prep step 2: Source map (10 min)
**For each ARMED falsifier** (F-01, F-04, F-09, F-10, F-11, F-12, F-13, F-14, F-15, F-20), verify:
- Source file exists and is readable
- Deadline or trigger condition is explicit (e.g., F-09: "epoch 2 completion"; F-13: "campaign end"; F-20: "per-salon S3 output lands")

**Files to spot-check:**
- `watch/TESUJI_MAP_5_3FLASH_20260906.md` (charter, axis definitions, cell names)
- `mag/refeed_guard.py` (line with the 94% threshold)
- `watch/ASTRA_CAMPAIGN_LOG.md` (program-ender dates, no rescue clause)
- `watch/salon_runner.py:48` (S3 protocol: "one falsifier: what kills this?")

### Prep step 3: Verdict grounding (15 min)
**For each PASSED falsifier**, retrieve the evidence:
- F-02 (rotation ≥ 80%): Source is `watch/INVARIANT_SHEET_V2.md` MEASURED row — find the exact line with 0.950.
- F-05 (Lite re-arm): Source is `watch/GROUNDING_WAVE.jsonl` — scan for the Sep-8 row with 94% label.
- F-06 (coldest-vertex): Source is `GROUNDING_WAVE` rows — sum top-5 family mass, divide by total. Should be ≥30% (measured 60.7%).

**If a PASSED verdict cannot be grounded in the corpus within 3 minutes, mark it UNPROVEN and request a new falsifier run.**

### Prep step 4: Dispute queue resolution (5 min)
**F-16 (I4 re-run) is FIRED but contested.** Locate the dispute queue:
- `watch/inbox/` or wherever the contested denominator case lives
- Read both sides' reconstruction of the rubric from the I4 packet alone
- Note: The falsifier fired (which would retire the claim), but the verdict is contested across seats. This is **intentional opacity**: the ledger shows what happened, not the judge's final say.

### Prep step 5: Three-things check
1. **Ledger is append-only:** No row is edited in place; new verdicts arrive as new rows, chained to the prior.
2. **Falsifiers predate verdicts:** Every PASSED or FIRED falsifier has a charter/definition file dated before the verdict date. (Example: F-01 chartered 2026-09-06, probe grid T1 pending; F-02 chartered same day, verdict measured 2026-09-11.)
3. **Status and source align:** A falsifier marked ARMED must cite a source that defines the test condition; PASSED/FIRED must cite where the measurement lives (file or cord row).

---

## Falsifier — what would prove this wrong

### Kill condition A: Hash chain broken
**Proof:** Run `python -m mag.tesuji_map verify`. If it returns `(False, "row N: ...")`, the chain is corrupted. The ledger is invalid.

### Kill condition B: ARMED falsifier with no deadline
**Proof:** Find an ARMED row whose `source` field does not cite any file, doc, or date. If the falsifier has no trigger condition, it is a wish, not a promise.

### Kill condition C: PASSED verdict with no evidence
**Proof:** For any PASSED falsifier, attempt to locate the measurement cited in the `last_verified` field. If the file is missing or the row/line does not exist, the verdict is ungrounded — downgrade to UNPROVEN.

### Kill condition D: Verdicts older than charter
**Proof:** Pick a PASSED falsifier (e.g., F-05). Find the verdict date in the source field (Sep-8). Now find the charter file (mag/refeed_guard.py or watch/GROUNDING_WAVE.jsonl). If either predates the verdict, the falsifier is retroactive, not pre-registered. Report it as DISPUTED.

### Kill condition E: Falsifier ledger and invariant sheet disagree on status
**Proof:** Take a claim from the invariant sheet marked SUPPORTED. Find its corresponding falsifier in this ledger. If the falsifier is ARMED (not yet fired) or DISPUTED, the invariant sheet is premature. Pull the source and reconcile the timestamps.

### Kill condition F: Consensus violation (F-17 failure)
**Proof:** F-17 claims "20/20 convergence: zero-shared-context workers DISAGREED zero times." Retrieve `watch/inbox/mickey/G5_2_controverted_v2.md` and `W7_B_controverted.md`. Count the rows where G4-2 and W7-B gave different verdicts. If count > 0, F-17 FIRED (falsifier killed the claim). (Current: 0/20 in W7-B, 6/10 soft disagreements in G4-2, but on *different* lines — zero on the 20 hotly controverted ones — so PASSED holds.)

---

## The trap
**Strongest trap for outsiders:** Confusing tesuji_map entries (which are field-map probes of GLM-5.3-flash: "does the model have a predictable behavior pattern on task X?") with falsifier ledger entries (which are armed promises to the auditor: "if this test fires, the claim dies"). The tesuji_map is a hypothesis-testing ground; the falsifier ledger is the legal record. Read FALSIFIER_LEDGER.md first. Tesuji is support structure, not the ledger itself.

**Second trap:** PASSED does not mean verified by the operator — it means the test ran and the claim survived. Read the source citation. The operator's blessing (or skepticism) lives in separate cards (watch/inbox/ or the invariant sheet's DISPUTE/UNPROVEN columns).

**Third trap:** FIRED (one instance: F-16) does not close the case if the verdict is contested. The ledger shows the fire; the dispute queue shows who won. Do not assume FIRED = end of story — follow the `consulted_by` field to the dispute artifact.

