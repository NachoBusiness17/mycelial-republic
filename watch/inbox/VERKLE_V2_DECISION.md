# VERKLE V2 DECISION — operator flip call for AH19 append-leaves

**Class:** DECISION MEMO (this file is the receipt) · **Date:** 2026-09-29 · **Fence owner:** operator
**Status: DECISION PENDING — the flag is NOT flipped.** `configs/mag.yaml` line 8 still reads `chain_mode: v1` (verified this moment). Nothing in this memo mutates the chain, the tip, or the config.

**Sources read (bytes, not reports):** `watch/inbox/last_mile_20260930/AH19_AMEND_PERF.md` (AH19 receipt, commit c1fb757da) · `mag/verkle_knot.py` (chain_mode flag fail-closed v1, v2 append path, pointer resolver, consolidation refusal, AG5 atomic tip writes) · live chain measured this moment.

---

## 0. Ground truth (measured 2026-09-29, `verkle_chain.jsonl`)

| fact | value | note |
|---|---|---|
| chain rows | **8,669** | AH19 receipt read 8,626 at its moment; census-denominator law — counts are snapshots, the delta is post-receipt folds |
| amended rows | **2,822** | receipt read 2,821; same law |
| unique sessions | **8,669** | exactly one row per session — the live chain is pure v1 amend semantics |
| chain file | **6.07 MB** | every amend re-save rewrites all of it today |
| tip | n_leaves 8,669, root `a5db8380a40ee087…` | verifies consistent |

Machinery is LANDED and tested (14 AH19 tests + verkle family green: 59 + 39 + 14; ratchet PASS). The only open question is the operator flip. That call is:

## RECOMMENDATION: GO — flip at the next quiet window, after two small precondition repairs, with a pre-flip seal as the rollback. Never mid-day.

Trigger recipe in §4. Rationale below.

---

## 1. What the flip BUYS

- **Write amplification off the spine.** Bench (this machine, `ah19_bench.py`): 100 re-saves of one far-from-tail session at 500 seed rows wrote **35.97 MB under v1 vs 0.08 MB under v2 (471x less)**; at 2,000 rows **144.27 MB vs 0.08 MB (1,800x less)**. At today's 8,669 rows every re-save of a live session rewrites the full 6.07 MB file; v2 writes ONE ~760-byte line, constant, forever. Under v1 this cost grows linearly with chain length for the estate's lifetime.
- **Wall clock.** 1.6x per save at 2,000 rows and the gap widens with n (v1 110 → 331 ms/save from 500 → 2,000 rows; v2 117 → 202 ms — v2's residual cost is the shared O(n) verify gate paid twice, not the write).
- **rib_bus stops taxing the spine.** Before AH19, every `rib_bus.publish_rib` of an UNCHANGED invariant was a full-chain rewrite (`now()` re-keyed the dossier every call). Now the fold minute pins to first-seen `ts` and republish dedupes to a skip. This fix is live regardless of mode, but under v1 a changed rib still pays the 6 MB rewrite; under v2 it pays one line.
- **History becomes canonical.** v2 never unlinks prior knots: amend history (the 2,822 re-saves' worth of intermediate states v1 destroys today) is preserved and auditable. Session pointer `(session_id, session_seq)` gives O(1) latest-per-session with version numbers for free.
- **Future growth.** The spine's per-save cost becomes O(1) bytes instead of O(chain). This is the only window where the conversion is cheap: cost of waiting grows with every row.

## 2. What the flip COSTS

- **The conversion rewrite the mission feared does not exist.** The landed design is **zero-migration**: flipping mid-life is legal, mixed v1→v2 chains verify clean, the verifier handles v1 rows forever, and the v1 prefix is never touched — v2 rows simply append after it (AH19 receipt, "Landed state"; `mag/verkle_knot.py` `_verify_chain_consistent` reads only the last row's root + tip and recomputes over all rows). No full-chain rewrite, no reader migration of the v1 prefix, no downtime conversion pass. (Optional, not required: an O(n) pointer-seeding pass could pre-write `by-session_v2_*` pointers for the 8,669 v1-only sessions; the last-matching-row fallback is already exact for them.)
- **One-line flip + two precondition repairs (the real cost):**
  1. **`mag/verkle_compaction.py` (verkle99) has no v2 refusal.** It REWRITES the chain dropping fold candidates — under v2 that destroys canonical append-only history. `verkle_knot.consolidate` refuses under v2; compaction must gain the same mirror guard BEFORE the flip. Small, test-covered pattern already exists.
  2. **rows ≠ sessions drift in the analytics family** (none fail loudly — they silently change meaning): `cache_map` time-window join (a multi-row session double-counts inside a window), `gene_pool_feeder`/aud_verkles `dup_rate` + `session_diversity`, `knot_untangle` near-duplicate clusters (one session's seq rows will read as "tangled"), `hour_test`/`diary_node`/`persona_recall`. Core readers are already correct (`latest_leaf_for_session` pointer-first, `rib_bus`, `chat_source`, tail/tip reads). Decide at flip time: session-dedupe these readers or file the drift as documented.
- **Formulas that need the pen:** DNA's `residual + registry + leaf = filed workdays` — post-flip the workday unit is the SESSION (leaves-per-session grows without bound); any AGENTS/doc chain-count claim must follow the census denominator law (name instrument + moment; rows and sessions become different denominators the day the flag moves). Deliberate-ask "verkle tip" references are unaffected (tip stays the tail root over all leaves).
- **Storage:** v2 never unlinks — `knots/` grows with every re-save (~2–4 KB per leaf; bounded by save frequency, not sessions). Acceptable; the tool that managed bloat (consolidation/compaction) is exactly what v2 retires, so this is a monitored-forever line, not a fire.
- **rib_bus versioning change:** each publish appends one leaf per (domain, version); rib chains accumulate rows per domain pointer. Intended (version history), but rib readers that counted rows now count versions.

## 3. What it RISKS

- **The chain is the estate's spine** — identity, boot (`mag.hermes_warm_boot` loads the tip into every session), seals, the RIB deliberate-ask. Precedent 2026-09-27: ONE bad root froze EVERY append for hours (memlang anchoring froze, 6 suite failures) while lanes were hot. The blast radius of any spine mistake is all lanes. A mid-day flip repeats that exposure for a benefit that is economics, not correctness — the chain is not broken today; v1 works, it is merely expensive per save and getting worse.
- **Silent semantic drift** post-flip (§2.2) is the dangerous failure class: no error, wrong numbers, discovered weeks later in a chart.
- **Rollback subtlety — read this before trusting "just flip it back":** flipping BACK to v1 after v2 rows verifies fine, but leaves multi-row sessions that v1's consolidation then REFUSES to collapse (conflicting leaf hashes guard). Flip-back is NOT a clean rollback. **The clean rollback is the pre-flip seal.**

## 4. RECOMMENDED TRIGGER (the operator recipe)

**When:** the next QUIET window — no burn waves, no gated workflows, no hourly cron mid-cycle (the 09-27 lesson). Not mid-day.

**Preconditions (land before the window, each testable):**
1. `verkle_compaction` gains the v2 refusal (mirror of the consolidation guard) + test.
2. Analytics drift decided: session-dedupe or tag `cache_map` / `gene_pool_feeder` dup_rate / `knot_untangle`.
3. AH19 family rerun green (`tests/test_ah19_append_leaves.py` + verkle suites).

**The window (minutes, in order):**
1. `python -m mag.seal seal` — **pre-flip seal = THE rollback point.**
2. Verify chain consistent; record tip root + n_leaves (today: `a5db8380a40ee087…` / 8,669) in this memo's addendum.
3. Flip `configs/mag.yaml` `chain_mode: v1` → `v2` (one line).
4. Fire one real save (a rib_bus publish or a session fold). Confirm: appended row carries `session_seq` + `chain_mode:"v2"`; the v1 prefix is BYTE-untouched (byte-prefix law); verify green; pointer file written.
5. `python -m mag.seal seal` — **post-flip seal.** Addendum below gets both seal ids + the first v2 row's ts.

**Rollback:** restore the pre-flip seal (step 1). Not a flag flip-back (see §3).

**Post-flip watch:** first daily cycle (census patrol, FTS, improve) for rows≠sessions drift before trusting any chain-derived count.

---

## Addendum (operator fills at flip time)

- pre-flip seal id / tip root: _pending_
- flip timestamp / first v2 row ts: _pending_
- post-flip seal id / tip root: _pending_
- compaction guard landed (commit): _pending_
- analytics drift decision: _pending_

**Recommendation, one line: GO at the next quiet window after the compaction guard + analytics-drift decision, sealed both ends, pre-flip seal as rollback; do not flip mid-day; the flag is not flipped by this memo.**
