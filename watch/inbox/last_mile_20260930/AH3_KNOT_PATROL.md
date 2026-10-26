# AH3 — knot rehash patrol (audit finding #9, 2026-09-29)

**Fence owner:** seat (AH refire lane) · **Files:** `tools/knot_rehash_patrol.py`, `tests/test_knot_rehash_patrol.py` (both) · run read-only against `memory/biography/`

## The disease (finding #9)

The chain gate (`_verify_chain_consistent`, mag/verkle_knot.py) recomputes the
merkle root over the leaf_hash STRINGS the chain rows carry — it never
re-derives one leaf_hash from the knot FILE on disk. An edited knot body sails
through the gate (row strings untouched), and a deleted knot file sails through
too. Audit census: 372 rows reference missing files.

## The patrol (read-only, NO repairs — operator GO only, Q-001)

1. **REHASH arm.** Sample N rows (default 200, `--all`) from
   `verkle_chain.jsonl`, load `knots/<filename>`, recompute with the chain's
   OWN hashers (imported, never reimplemented — one referee per chain):
   - session/usage-digest leaves: `mag.verkle_knot._leaf_hash` over the body
     minus `{leaf_hash, filename, pdf_path}` (the fold adds those AFTER
     hashing; same strip set as `mag/verkle_artifact.verify_leaf`);
   - `leaf_kind == "diary_node"`: `mag.diary_node._leaf_hash`
     (`b"diary-leaf:"` prefix) over the body minus
     `{leaf_hash, filename, type, schema, leaf_kind}` with schema restored to
     `mag_diary_node.v1` — the append path overwrites type/schema/leaf_kind
     post-hash (mag/diary_node.py 617-647 + 474-476). Live chain currently
     carries 0 diary rows; branch pinned by fixture tests anyway.
   Mismatch classes: `body_vs_knot` (edited body — THE audit-#9 incident),
   `knot_vs_row`, `knot_unreadable`, `missing_leaf_hash`.
2. **DANGLING census.** Always the FULL chain, chain_guard's exact predicate
   (filename set and `knots/<filename>` not a file), reported against the
   audit's 372 claim. A torn/unparseable chain line is exit 2, never silently
   skipped (census denominator law). Sampled knots vanishing mid-run are
   live-estate motion, not incidents.

Carrier grammar: `REHASHED n/m MATCH, DANGLING d (audit claim 372, delta ±x)`.
Exits: 0 clean / 1 mismatch / 2 cannot-run. Dangling rows are excluded from
the rehash denominator (census owns them; repairs belong to the
`tools/verkle_dangling_repair.py` lane, not this patrol).

## Refire note

A dead-lane partial (untracked tool + 11 tests) existed from the 5-hour-wall
wave. Refire verified its diary dispatch against `mag/diary_node.py` law
(byte-checked the hash site), added the audit-claim comparison (delta in
carrier + JSON verdict), and added 4 tests: diary clean, diary body edit →
exit 1, audit-claim line, plus the pre-existing hasher-identity pin.

## Live run (2026-09-30, this machine, venv python)

- Sample 200 (seed 20260930): `REHASHED 200/200 MATCH, DANGLING 372 (audit
  claim 372, delta +0)` — exit 0.
- Full pass `--all`: `REHASHED 8276/8276 MATCH, DANGLING 372` — exit 0,
  0 mismatches, 0 rows without filename, 0 vanished mid-run.
- **Dangling census: 372 exactly = the audit's claim (delta +0).**
- Census instrument + moment: `knot_rehash_patrol` full-chain file-existence
  scan; chain read 8,648 rows at the `--json` run (chain grew 8,646 → 8,647 →
  8,648 across this session's reads — live estate, concurrent folds; dangling
  held 372 at every read). Independent cross-check: a pre-build probe pass
  (session-strip over all rows) also read 372 dangling / 0 mismatch.

**Verdict: every present knot file on the live chain rehashes byte-exact to
its committed leaf_hash. The finding's damage is dangling-only (372 files
gone), not body tampering. No repairs performed — operator GO.**

## Tests

`pytest tests/test_knot_rehash_patrol.py -q` → **15 passed** (clean/dangling/
sample/determinism/body-edit/row-disagreement/unparseable-knot/missing-chain/
torn-line/arg-guards/json-shape/hasher-identity/diary-clean/diary-edit/
audit-claim).
