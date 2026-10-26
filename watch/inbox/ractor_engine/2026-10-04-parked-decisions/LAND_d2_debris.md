# LAND_d2_debris - D2 verdict debris cures landed 2026-10-04

Lane: dungeon-debris. Verdict source: `SYNTHESIS.md` (D2: accept-the-debt-standing,
re-specified as governed debt; debris cures land, the split itself is deferred).
All bytes verified in this tree before edit; gates run after. No em-dashes.

## Per-item changes (tools/dungeon.py only)

1. **Dead shadowed play() deleted.** The FIRST `def play()` (old :447-449,
   s0+s1 only) removed. The live second def (now :733) carries the
   `if self.full: self.campaign()` hook and is untouched. `grep -n "def play("`
   after: exactly one hit, :733.
2. **Stale self-citation corrected.** The campaign() comment cited the
   party-wide dict as "dungeon.py:447 at HEAD 37e2fba7e". Byte truth at that
   commit: `git show 37e2fba7e:tools/dungeon.py` line 447 is `note = ""`;
   the dict declaration `carried: dict[str, str] = {}` is line **421**. The
   cite now reads :421 with a one-clause correction note (old :447 held
   `note = ""` at that commit and, pre-fix, named the deleted shadow play()).
3. **Dead reasoning fallback fixed.** :211 `msg.get("content") or
   msg.get("reasoning") or ""` -> `reasoning_content` (d4-probe class, same
   bug as mag/route_chat.py:253-257). Two-line cause+evidence comment added.
4. **Always-true guard dropped.** Old `if self.warden_hp <= 0 or
   self.persuades >= 2 or True:` (both leading disjuncts dead) replaced by
   the unconditional S1-loot assignment, one-line cause comment, body dedented,
   explanation comment preserved.

## Line count (instrument: `wc -l tools/dungeon.py`)

- Before this lane: **771** (post 3-strike void breaker; the go-wave stamp of
  756 accepted_lines had drifted +15, flagged as GROWTH by the SYNTHESIS run).
- After this lane: **771** (net zero).
- Honesty note: the verdict predicted a shrink. The deletions removed 5 lines
  (4 dead-play + 1 guard line); AGENTS.md-mandated cause+evidence fix comments
  added 5 (2 reasoning_content + 2 cite correction + 1 guard cause). The
  honest re-stamp number is 771, and that is what the baseline carries.

## Baseline re-stamp (configs/violation_baseline.json, entry af1d7045681fee89)

- Deviation named: the verdict's `baseline-update --by` command is a no-op for
  this entry - `cmd_baseline_update` (tools/violation_ratchet.py:284-316) only
  ADDS fingerprints not already registered, and the file-too-long fingerprint
  is `fingerprint(rule, file, detail)` with detail fixed at ">400 lines"
  (:149), invariant under line-count change. The honest re-stamp required a
  direct entry edit, which is what landed.
- New stamp: `accepted 2026-10-04`, `accepted_lines 771`, `by ractor-d2-debris`.
- SPLIT TRIGGER registered in the entry note: the split fires when
  tools/dungeon.py next grows past 771 lines, or on any D2 falsifier in
  SYNTHESIS.md ((a) second engine-loop correctness bug in one wave,
  (b) growth past +50 over this count or top-grower status,
  (c) the next substantive campaign edit).
- GOLDEN-VECTOR PRECONDITION registered: any split sitting must first retarget
  tools/prepush_golden_vector.py (DEFAULT_TARGET tools/dungeon.py; 7/11
  tokens pinned to SCENES/campaign bytes) to scan both files, re-census the
  pure ceiling, and pass 11/11 before lifting.

## Gates (all green, this tree, this sitting)

1. `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py -q -p no:cacheprovider` -> **15 passed in
   0.86s**.
2. `.venv/Scripts/python.exe tools/prepush_golden_vector.py` -> **GOLDEN-VECTOR:
   ok - 11/11 golden tokens**, exit 0.
3. `.venv/Scripts/python.exe tools/dungeon.py --help` -> exit **0**.
4. `.venv/Scripts/python.exe tools/violation_ratchet.py check` -> **RATCHET:
   PASS, NEW=0**; no GROWTH line for tools/dungeon.py (the 771 stamp matches
   byte truth). Remaining GROWTH prints (percolator, estate_bridge,
   concept_predictor, duel_harness, env_contract, gps ledger, hermes_burn) are
   pre-existing, print-only, out of this lane. Note: the social_rsi.py:578
   NEW=1 debt the SYNTHESIS saw has since been accepted by another lane; the
   tree moved between sittings.
5. Dash law: `grep` for em/en dash bytes over both written files -> 0 hits.

## Files touched

- `tools/dungeon.py` (4 debris cures, 771 -> 771)
- `configs/violation_baseline.json` (one entry re-stamped + split trigger note)
- this receipt

Not touched (lane boundary held): mag/route_chat.py, law docs, hermes_burn.
Not committed (per lane instructions).

## Blockers

None. All seven verdict items executed; no sub-item filed as blocked.
