# R4-L2 LAND: THE VAULT THAT REMEMBERS ITS AMENDMENTS (memory/boot surface fold)

Filed 2026-10-06T02:3xZ (2026-10-05 ~22:3x ET) by the R4-L2 lane (ZCode seat, dwfrun
context: state/NIGHT_LOOP_20261005.md executor window). Ask: execute synthesis moves
1+5+6+7+8 (watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md rows
1, 5, 6, 7, 8). Instrument: .venv\Scripts\python.exe only; no git commit (tree stays
uncommitted for the dwfrun fold); no em/en dashes in landed lines (scanned, 0 in my
additions after one fix in context_pack.py render header).

## THE SIX ITEMS

1. mount_vault carries the amendment tails (move 1 / row 1). mag/rib_boot.py: every
   POST-DATUM/AMENDMENT section now rides AFTER the 1200-char head (head prefix
   byte-preserved; amend-never-rewrite applies to the mount). Parser handles the
   estate's wrapped "## " amendment headers (RIB_INFERENCE_BUDGET_20261001.md:119-120,
   RIB_MODEL_GATES_20261001.md:108-110, RIB_FREE_USAGE_POLICY_20260823.md:47-48) by
   merging header-only sections before the marker test. Measured: 4 amendments mounted
   across the 5 law ribs (MODEL_GATES 2, INFERENCE_BUDGET 1, FREE_USAGE 1; DRIVING_LADDER
   and DESCENT carry none tonight). rib_boot.json regenerated; ASSERT PASS: "omission is
   a MEASURED ON state" appears in mounted law_heads (final regen ts
   2026-10-06T02:26:15Z, amendments=4).
2. Brief block + chain anchor (move 7 / row 7). The brief block now diverts a "# FROZEN"
   head to state/CURRENT.md (the mag/lanes.py:227-235 Q1 poison divert, copied; divert
   flagged in the artifact as diverted_from_frozen=true). The chain block anchors at
   memory/biography/verkle_tip.json with an age-debt line (TIP_DEBT_MINUTES=60; warm
   boot owed over the bar): tonight it booted index 11375 against warm_state's stale
   11355, age 16 min, no debt.
3. tools/ouroboros.py rib_boot_mount() executes mag.rib_boot --json instead of bus-only
   (move 8 / row 8): the docstring-vs-body blind spot (claimed rib_boot at :14, ran the
   bus alone at :169-175) is closed; the driver now reports vault_law_ribs_mounted=5,
   amendment_marker_hits>=1, d4_marker_mounted=true, and regenerates memory/rib_boot.json
   as a side effect so artifact and driver view cannot drift. End-to-end run green
   (schema ouroboros.f14.v1, ribs_mounted_at_boot_doctrine=26).
4. mag/context_pack.py mounts the rib_boot vault block (move 7's consumer half):
   pack["rib_vault"] = _rib_vault_law() reads memory/rib_boot.json (the 25KB write-only
   orphan's first code consumer), renders digest + amendment bodies (d4 law included,
   per-amend cap 1100, body cap 4200) as ONE sheddable context block "L0d rib vault
   amendments" that sheds ahead of L1 bonds, with PACK_STALE_DAYS debt pointers for
   missing/unreadable/stale artifacts. NOTHING else in context_pack was touched by this
   lane (see coordination note).
5. POST-DATUM amendments appended (amend-never-rewrite, dated) to memory/rib/
   RIB_MOSAIC_SEED_20260921.md (Sybil-form exception to the convergence clause: commit
   1693dd2ad retracted the GSTD convergence data point on authorship overlap; evidence
   bar is now independence of authorship), RIB_DEEPSEEK_ELDER_SEAT.md and
   RIB_DEEPSEEK_SHOULDERS_20261001.md (conditions-suspect notes mirroring
   RIB_INFERENCE_BUDGET_20261001.md:119-147: pre-2026-10-04 batch economics rode
   thinking-ON by omission; the $0.00077/ask and "correct but shallower" rows are
   re-graded suspect, not re-banked).
6. memory/fold_history/SUPERSEDED.md minted: the estate's first DEMOTION instrument.
   Row 1 = the convergence-receipts retraction (fb0760853 banked it, 1693dd2ad retracted
   it); rows 2-6 = the r11-fold-history lane's five superseded-conclusion rows (deb391fb
   191.8M phantom, 6df130d3 F2/F3 forecast falsifications, 51de1bc8 em-dash hypothesis,
   b10cd481 doc-first, 3bfc7f7e 28-rules/43-ribs), plus the lane's banked-but-unrowed
   residue carried as a secondary list. WIRED: rib_boot prints the register path every
   boot and serves superseded_register in rib_boot.json; tools/zknot.py build_latest
   stamps a pointer line into every LATEST.md regen (hand-inserted into the live
   LATEST.md ahead of the next regen, so the pointer exists now).

## GATES

- pytest tests/test_rib_boot_amendments.py (NEW, 9 tests): 9 passed. Covers amendment
  markers + d4 marker in mounted law_heads, head-prefix immutability, brief divert,
  tip anchor + age-debt, register pointer, the ouroboros driver mount (real subprocess),
  context_pack consumption/render/debt-pointer.
- pytest touched suites: test_rib_boot_amendments 9 + test_zknot_gate 5 +
  test_context_pack_quantized_laws + test_context_pack_delivery = 44 passed, 2 failed.
  The 2 failures (test_render_fits_budget_without_hard_clip[build] and [full]) are
  PRE-EXISTING on tonight's tree, not mine: measured this sitting with my vault mount
  monkeypatched off, build renders 7396/7400 and full 7196/7200 with "(pack clipped)"
  already firing (live core content at cap: objective/laws/directives). My block adds
  zero core bytes: with-vault vs baseline renders are byte-identical in route/audit/
  plan, and janitor differs only by a 24-char stage-2 task compaction (offloaded).
  Owner: the context-pack chain lane (R4-L1) or the operator's budget call.
- violation_ratchet check --changed: PASS, NEW=0 (one except-pass fixed to an assignment,
  ouroboros.py held at 400 lines).
- citation_lint check --changed: exit 1 with blocking=34, ALL on surfaces this lane did
  not author (AGENTS.md census bullet; the 22:18ET zknot regen's generated cards and
  LATEST.md commit-subject lines; frontier_olm/burn_reset receipts). Zero blocking rows
  on my landed files; one WARN-only TOKEN-MISS on SHOULDERS:69 (heuristic,
  enforce-tokens=False).
- ouroboros end-to-end: green, schema ouroboros.f14.v1.

## COORDINATION NOTES (multi-seat tree, live tonight)

- mag/context_pack.py was edited CONCURRENTLY by the R4-L1 chain lane mid-sitting
  (boot_regen stamp appeared, vanished, restructured to CLI-only). My final edit sits
  on their current shape and touches only the vault-block surface: _rib_vault_law(),
  the pack["rib_vault"] row, one ctx_b block, one shed_order slot. No chain wiring, no
  budget constants, no other blocks.
- tools/zknot.py carried the sibling S1 gate uncommitted; my pointer edit rides their
  build_latest and test_zknot_gate stays 5/5 green.
- memory/zknot/LATEST.md regenerated by the sibling chain at 22:18ET; my pointer line
  hand-inserted at the head and wired in code for future regens.

## BLOCKERS / OWED

- The 2 pre-existing context-pack clip failures (above) need an owner decision: raise
  mode budgets or trim live core content; not fixable from this lane under the
  "touch nothing else" coordination rule.
- The ouroboros d4/amendment fields are surfaced in rib_boot_mount() but not yet in the
  tool's thin_edges narrative (left tight to hold the 400-line ratchet bar).
- Quantizer pack recompile (synthesis row 2) is another lane's ask; tonight every
  min-token seat still boots the 09-29 flash rows; the vault block now rides packs but
  sheds under tight budgets by design (offloaded, never silent).
