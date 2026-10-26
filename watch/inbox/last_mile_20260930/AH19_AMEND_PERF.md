# AH19 — append-leaves chain model (audit finding #10, 2026-09-29)

**Fence owner:** seat (AH lane) · **Files:** `mag/verkle_knot.py` (append path), `mag/chat_source.py`, `mag/rib_bus.py`, `configs/mag.yaml` (one line), `tests/test_ah19_append_leaves.py`, bench `ah19_bench.py` (this dir)

## The disease (finding #10)

`append_verkle_knot` treats a re-save of an existing session as an AMEND:
`rows[existing_i] = chain_row` then `_rewrite_chain(rows)` — every save of a
live session rewrites the WHOLE `verkle_chain.jsonl` (every row re-keyed with
new prefix roots, O(n) bytes + O(n log n) hashes per save). Live forensics:
2,821 of 8,626 rows were amend rewrites. Every `file_agent_session(amend=True)`
save and every `rib_bus.publish_rib` fold (session_id `rib_bus_{domain}` — the
SAME leaf per domain) paid a full-file rewrite per event: O(n) per append,
hours of aggregate write amplification.

## Design — append-leaves (chain_mode=v2), default v1

- **One flag.** `configs/mag.yaml` top-level `chain_mode: v1` (default, live
  chain untouched until an operator migrates). `verkle_knot.chain_mode()` reads
  it via `mag.policy.load_policy`; unknown values fail-closed to v1.
- **v2 write model.** A save NEVER amends: it appends ONE new chain row
  `{..., session_id, session_seq, chain_mode:"v2"}` and one new knot file;
  prior rows/knots are never rewritten or unlinked (history is canonical).
  The filename carries the seq (`..._{commit8}.s{seq}.knot.json`) so repeated
  saves cannot collide.
- **Session pointer.** `knots/by-session_v2_{sha(sid)[:32]}.json` becomes the
  authoritative latest-per-session resolver: `{session_id, seq, filename,
  leaf_hash}`. seq resolves O(1) from the pointer (no chain scan).
  `latest_leaf_for_session()` = pointer-first, last-matching-row fallback
  (v1 chains keep one row per session by amend, so the fallback is exact).
- **Dedupe.** Identical leaf_hash at the pointer's current seq → skip, same
  contract as v1 but pointer-driven instead of row-scan.
- **Merkle semantics unchanged.** Every row (v1 or v2) is a leaf; root over
  all leaf hashes; tip = chain tail. Mixed v1→v2 chains verify with zero
  migration: flipping the flag appends v2 rows after the untouched v1 prefix.
  The verifier (`_verify_chain_consistent`) handles v1 rows forever — it only
  reads the last row's root + tip and recomputes over all rows.
- **Consolidation refuses under v2** (multiple rows per session are history,
  not bloat) and stays available on v1 chains.
- **rib_bus:** session_id stays `rib_bus_{domain}` (one pointer bucket per
  domain); each publish appends one leaf whose chain `session_seq` IS the
  version (one leaf per (domain, version), version pointer = the domain's
  session pointer). Fold minute is pinned to the rib's first-seen ts so
  republishing an unchanged invariant dedupes to a skip instead of a rewrite.
- **chat_source:** `file_agent_session` surfaces `chain_mode` in its result;
  `amend=True` keeps its residual-pack meaning (per-session JSON, small) —
  only the CHAIN write changes shape under v2.

## Bench (this machine, `ah19_bench.py`, seeded chain, 100 re-saves of one far-from-tail session)

Run: `.\.venv\Scripts\python.exe watch\inbox\last_mile_20260930\ah19_bench.py [seed saves]`

| seed rows | v1 amend ms/save | v2 append ms/save | wall speedup | v1 bytes written | v2 bytes written |
|---|---|---|---|---|---|
| 500 | 110.4 | 116.7 | 0.9x (parity) | **35.97 MB** (100x amplification) | **0.08 MB** (471x less) |
| 2,000 | 330.6 | 202.3 | **1.6x** | **144.27 MB** (100x amplification) | **0.08 MB** (1,800x less) |

Honest reading (cProfile, 30 saves over 500 rows): at small n the per-save wall
is dominated by SHARED O(n) costs — `_verify_chain_consistent` (O(n) chain
parse + merkle) and `_update_topic_evolution` (full-series JSON rewrite) — and
v2 pays the verify gate TWICE (pre-append integrity gate + post-append
self-heal check), which is why 500 rows shows wall parity while bytes collapse
36.0 MB → 0.08 MB. The v1 rewrite itself is O(n log n) hashes + O(n) bytes and
grows with chain length: 110 → 331 ms/save from 500 → 2,000 rows, while v2
grew 117 → 202 ms (the shared O(n) costs, not the write). At the live 8,626-row
scale the v1 amend rewrite alone is the audit's aggregate write amplification;
v2's per-save write is one ~760-byte line, constant, forever. Both runs verify
clean at the end (`chain consistent`); v1 stays one-row-per-session (100
amends), v2 ends at seed+100 rows with `session_seq` 1..100.

## Landed state (2026-09-30)

- `mag/verkle_knot.py` — `chain_mode()` flag (fail-closed v1), v2 append path,
  `(session_id, session_seq)` pointer, `latest_leaf_for_session()`, seq-suffixed
  knot filenames, v2 dedupe-by-pointer, consolidation refusal under v2.
- `mag/rib_bus.py` — fold minute pinned to the rib's first-seen `ts` (persisted
  as `first_ts`; republish of an unchanged invariant = dedupe SKIP, was a
  full-chain rewrite because now() re-keyed the dossier every call); result
  surfaces `chain_mode` + `version` (= chain `session_seq`; the domain's
  session pointer IS the version pointer).
- `mag/chat_source.py` — `file_agent_session` surfaces `chain_mode` +
  `session_seq`; `amend=True` keeps its residual-pack meaning.
- `configs/mag.yaml` — `chain_mode: v1` (default; live chain untouched until
  operator migration — flipping the flag mid-life is legal, mixed v1→v2 chains
  verify with zero migration).
- `tests/test_ah19_append_leaves.py` — 14 tests: byte-prefix no-rewrite, O(N)
  growth (every snapshot a prefix of the final file + bounded per-append
  delta), verify on pure-v2 and mixed v1→v2, v1 amend semantics untouched
  (one row/session, old knot unlinked), flag mapping fail-closed, rib_bus
  dedupe/first_ts/one-leaf-per-(domain,version), chat_source surfacing.
  Verkle family rerun green: 59 passed (verkle/chain/rib suites) + 39
  (ah19+ag5+compaction+chat_source) + 14 (ah19). Ratchet: PASS (0 new debt).
