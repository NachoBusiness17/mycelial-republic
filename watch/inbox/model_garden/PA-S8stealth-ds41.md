# PA-S8stealth-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# STRANGER AUDIT: FINDINGS BANK ROT, TRIAGE TRIGGERS, SECOND-PILE FAILURE

## (1) What rots in an unread findings bank

Three decay modes, each with a byte witness in the evidence.

**Age rot.** `00__STEALTH_MINED_FINDINGS.jsonl` spans 2026-09-28 to 2026-10-02. A 09-28 row (`lib-belady-1966`, `nous`, `qwen3.8-max-prime`) and a 10-02 row (`w-belt-cube-mechanism`, `openrouter`, `ling-3.0-flash-sante:free`) sit in the same file with no expiry field, no supersession pointer, no tombstone. Nothing in the row schema says "if unread by T+N hours, this row is dead." Age rot is silent because the row is byte-identical whether it was read or not.

**Dedup rot.** The 09-30 triage states plainly: "122 rows collapse to **3 topics × 4 lanes** (12 distinct answer files, overwritten per cycle - the JSONL is the only history)." One topic re-derived 67 times. The answer files overwrite; only the JSONL row survives. So the bank accumulates N copies of one opinion (rib law, cited in the triage itself) and no row marks itself as a duplicate of a prior row with the same `work_id`.

**Contradiction rot.** `01__STEALTH_TRIAGE_20260930.md` §3 lists C1 and C2 as live contradictions between today's bytes and `RIB_FREE_USAGE_POLICY_20260823`: the rib says free lanes "throttle into empty (429)... substance_chars=0 is the norm," today shows "100% finish=stop, zero 429/empty rows." The rib says "~98% cache-hit FROZEN_PREFIX," today shows `cached_tokens=0 on all 62 rows` for `ling-3.0-flash-sante:free`. Both banks sit in the estate simultaneously; neither row carries a `contradicts:` field. An unread bank cannot resolve this.

The self-admitted consumer gap makes it worse. The row's own note (repeated across dozens of rows) says: "no percolator/quantizer ingester exists, so the old note named modules that never read this file." The 09-30 triage confirms: "no 'MINED findings register' exists anywhere under `memory/`."

## (2) Triage triggers: climb or die

Four trigger conditions. Each names instrument, moment, context.

**T1 - Novelty trigger (climb to FUNDED-TIER-REVIEW).** Fires when a row's `work_id` has no prior row in the last 72h whose answer file byte-overlaps >80% (minhash or shingle Jaccard on the answer file at `answer_file` path, measured at row ingest). Context assumption: answer files are written before the JSONL append (true per the triage: "answer files byte-checked (all 12 present)"). Instrument: `answer_file` bytes, not the row's `note`. Falsifier: a topic whose answer file churns every cycle with confirmed new bytes (e.g., schmidhuber at 01:26Z was a terminal judgment row, not a re-derivation).

**T2 - Contradiction trigger (climb to LAW-CONFLICT, blocking).** Fires when a row's claim parses against any `memory/rib/RIB_*.md` and disagrees. Example from the triage: C1 and C2 above. Instrument: grep the rib text for the claim's key tokens; if the row asserts the opposite, emit `CONTRADICTS: <rib file:line>`. Context assumption: ribs are the law text. Moment: at ingest, not at review. Falsifier: rib is stale (then the rib loses, the row climbs to rib-amendment, not row-discard).

**T3 - Consumer trigger (climb to IMPLEMENTABLE).** Fires when a row's body names a real file:line in `mag/`, `tools/`, or `memory/` and the cited bytes exist. Example from the triage: F1 cites `mag/percolator.py:353 def _compile_invariant` - "function real" (the finding's own line range drifted but the anchor verified). Instrument: open the cited path, grep the cited symbol. Context: the row must carry a `file:line` pair. Rows without file:line never climb T3; they die at T3 or stall at T1.

**T4 - Death trigger (DISCARD).** Fires when any of: (a) row age > 14 days with no T1/T2/T3 fire; (b) `ponytail_audit` has any `false` value for a cited URL (per the triage: "that citation must not propagate"); (c) row is a strict subset of a newer row on the same `work_id` with the same lane. Instrument: the row's own `ts`, `ponytail_audit`, `answer_file`. Moment: nightly sweep at 00:00Z (matches the `02__STEALTH_SWEEP_LATEST.md` cadence).

Positive example: F1 in the triage fires T3 (`mag/percolator.py:353` verified) and T1 (schmidhuber novel), climbs to IMPLEMENTABLE. Negative example: a space-bunny kabbalah row with `ponytail_audit: {"//transformer-circuits.pub/2021/framework.html": false}` (triage §F5, row `2026-09-30T17:20:16Z`) fires T4(b) and dies at ingest.

## (3) The second unread pile

Triage becomes a second unread pile when the triage output itself has no consumer. The evidence already shows the shape: the 09-30 triage is `01__STEALTH_TRIAGE_20260930.md`, sitting in `watch/inbox/model_garden/premium_autopsy/evidence/S8stealth/`, same directory tree as the bank it triages. It is v0. It says: "Next triage: append a dated section to this file (v1+), or promote to `memory/` once an ingester exists." No ingester exists. So the triage doc accumulates dated v1, v2, ... vN in the same unread tree, and the second pile is born with the same disease: no `contradicts:` field between triage versions, no expiry, no consumer.

The failure is structural, not motivational. A triage that writes to `watch/inbox/.../evidence/` is a bank. A triage that writes a row to a queue with a named consumer is not. The 09-30 triage itself names the missing consumer for the **bank** ("no percolator/quantizer ingester exists") but does not name one for **itself**.

Falsifier for this claim: if `memory/` contains a file that greps for `STEALTH_TRIAGE_*` or parses the triage's ranked findings, the second-pile prediction is wrong. The triage state says: "grepped: `mined`, `findings register`, `MINED_FINDINGS`" - zero hits. The grep did not include the triage's own filename pattern. Run it before accepting this section.

---

**Deliverable.** `triage_rules.spec` - four triggers (T1-T4) with instrument, moment, context, falsifier; two carve-outs naming the required `contradicts:` and `consumer:` row fields; one named consumer (`tools/triage_sweep.py` reading the JSONL at 00:00Z, writing discard/climb rows to `memory/triage/queue.jsonl`). A seat can apply it as-is.

**Falsifier for the deliverable.** If a second unread pile forms from `memory/triage/queue.jsonl` because `tools/triage_sweep.py` has no downstream reader, the delivery has reproduced the exact failure it diagnoses. Acceptance test: grep `memory/` for a parser of `triage/queue.jsonl` before shipping. If absent, ship the sweep and the reader as one unit.
