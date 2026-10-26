# live-state repair receipt (gala ball3-suite-green, division B, 2026-09-29)

Lane: live-state. Owed work: 6 red tests from the wave5 full-suite run
(`watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt`, 14 failed /
2452 passed, 2026-09-29): test_shared_surface_events.py
::test_real_links_jsonl_matches_the_registered_baseline, the config_seal trio in
test_gate_blocking_paths.py (blocks_on_modified / blocks_on_unsealed /
blocks_on_missing), test_dead_hand.py::test_trigger_fires_seal_hold_loud,
test_voice_turn.py::test_handle_voice_turn_heavy_auto_handoff.

## Root causes (one per failure, each byte-checked)

1. **config_seal trio + dead_hand trigger: external-basetemp display-path
   defect, NOT seal state.** The ask's smell ("seal file state vs code") is
   answered: it was code, never seal state.
   - Evidence the tests are hermetic: `tests/test_gate_blocking_paths.py:52-61`
     monkeypatches CONFIG_DIR/SEAL_PATH to a tmp_path configs dir; the real
     `configs/.config_seal.json` is never read by the trio.
   - Evidence the real seal was not the trigger:
     `python tools/config_seal.py verify` during this lane returned exit 1 with
     modified=3 (mirrors.json, skills.yaml, violation_baseline.json), and the
     mtimes show all three moved AFTER the 14:19:49Z zcode-wave5-fold re-seal
     (violation_baseline 15:10Z, skills.yaml 15:16Z, mirrors.json 17:42Z) while
     the trio tests pass regardless of it. That 3-file drift is fold-scoped
     residual state for the ball close re-seal by name, not a lane debt.
   - The defect: `tools/config_seal.py:89` (cmd_update display line) called
     `SEAL_PATH.relative_to(ESTATE_ROOT)`; `scripts/dead_hand.py:212` and
     `:226` (_seal return, _open_hold display) called `.relative_to(ROOT)`
     unguarded. `conftest.py:13-15` defaults basetemp INSIDE the repo
     (`agents/pytest-tmp-<pid>`), which masked the class; the wave5 suite run
     passed `--basetemp=...\Temp\suite-burn-w5-full-basetemp-r3` (external),
     and `relative_to` raised ValueError on every tmp seal. Reproduced live
     pre-fix: probe of cmd_update with a %TEMP% SEAL_PATH printed the exact
     suite-burn error. dead_hand was a PARTIAL guard: `_seal` already guarded
     the surface names (scripts/dead_hand.py:200-205, "sandbox path outside
     ROOT (tests/drill rigs)") but missed its own return and _open_hold.
2. **LINKS baseline drift (f-16 live-append class): 5 unregistered
   post-marker kind rows.** LINKS.jsonl lines 380-384 (LINKS-JEEVES,
   LINKS-RAVEN, LINKS-OSINT-MODEL, LINKS-NIXOS-SOVEREIGNTY,
   LINKS-FACIAL-SCAN-FAIL, all kind x-drop) landed in commit 37036360a "SCOUT
   WIDE" 2026-09-29 09:05. The ask's "8 new rows the baseline never saw" = the
   8 rows appended across 37036360a + ball2's 93f85e0dd; only the 5 carrying
   `kind` are gate-judged (mag/links_split_gate.py:135), the other 3 are plain
   link rows the split gate never registers.
3. **voice_turn heavy_auto_handoff: second half of the SAME display-path
   class, buried under an exception swallow.** Under external basetemp,
   `mag/voice_handoff.py` raised ValueError at BOTH `card.relative_to(ROOT)`
   (card_path display) and the return's `path.relative_to(ROOT)`. The raise
   fired AFTER card+index bytes were written and was swallowed by
   `mag/voice_turn.py:1419` (`except Exception: pass` around the handoff
   block), so a COMPLETED handoff degraded to the local answer whose route
   defaults to "frontier" (mag/voice_turn.py:1624): the suite's exact
   `assert 'frontier' == 'handoff'`. The brief itself is deterministic
   (compile_intention on the exact test input returns depth=heavy_code,
   handoff=True, seat_recommend=handoff, why="handoff_non_blocking;
   depth=heavy_code" - verified live, no state read in that path); the failure
   was never a classifier drift.

## Fixes (display-only; no gate semantics, no ledger bytes changed)

- `tools/config_seal.py`: cmd_update display falls back to the absolute path
  when SEAL_PATH is outside ESTATE_ROOT; fix comment names cause + suite-burn
  receipt.
- `scripts/dead_hand.py`: `_seal` return + `_open_hold` get the same
  sandbox guard the surface names already had.
- `mag/voice_handoff.py`: `_under_root()` helper; card_path and the return's
  path fall back to the absolute path outside ROOT.
- `configs/links_kind_baseline.json`: 5 entries appended via the B2-168
  grandfather pattern (line, content sha256 recomputed from raw line bytes and
  asserted before write, id, kind, writer, why naming commit 37036360a and the
  f-16 class). LINKS.jsonl untouched: `git diff` on it is empty (no-erase
  held). 4 -> 9 grandfathered entries.
- `watch/inbox/index_events.jsonl`: ONE op=register row, seq
  1790707788389165800, ts 2026-09-29T18:49:48+00:00, class DATA, writer
  live-state, naming the registration; sha256/size are the post-append
  baseline file (85bdad3276aa1b0bb46ae6eebc81ed0d85a3bf276446403b06171a84beb0ea52,
  4584 bytes). Emission script banked:
  `watch/inbox/gala_20260925/ball3-suite-green/lanes/live-state.register.py`
  (contention guard + double-backfill guard + must-be-registered-or-EXPECTED
  sweep over every past-marker kind row).

## Finish line (byte-checked)

`live-state.check.txt` holds raw output. TWO full runs of all four owned
files: default basetemp 52 passed (exit 0) AND external basetemp
`--basetemp=$TEMP/live-state-basetemp-finish` 52 passed (exit 0) - the
external condition is the exact one that failed in the wave5 suite. All six
named tests green under both.

## Ratchet (cited exit, attributed, NOT force-passed)

`tools/violation_ratchet.py check --changed`: exit 1, FAIL. scope=17 changed
files, hits=18, registered=17, NEW=1:
- NEW 792e69eeb7c92559 file-too-long mag/physical_compute_acquire.py:529 -
  NOT MINE (no working-tree diff vs HEAD; I never opened the file this
  session).
- GROWTH claims 42b721c740d1abda mag/corpus_selfsteal.py (accepted 550, now
  573) and e066832a0b8edb5e tools/stealth_driver.py (accepted 753, now 1472) -
  NOT MINE (sibling-lane WIP; the events-door receipt saw the same two
  claims earlier today).
- MY two changed files (mag/voice_handoff.py +26/-2, tools/config_seal.py
  +13/-1) produced ZERO ratchet rows. Per the events-door precedent the tool
  has no per-hash acceptance (baseline-update batches ALL current NEW under
  one --by name), so this lane did NOT run baseline-update; the
  accept-or-fix call stays with the wave owner.

## Decision ledger

Closes the live-state portion of the ball3 suite-green gate: the six red
tests were one defect class (repo-root-relative display paths exposed by an
external basetemp, one site of it hidden behind an exception swallow that
silently degraded a completed handoff) plus one unregistered-drift class
(the B2-168 register-by-name path works exactly as designed: the gate named
the rows, the baseline absorbed them by name, the ledger was never edited).
Registration event is the 9th grandfathered entry; the drift law (register,
never erase) needed no change.

## Adjacent defects observed, not owned, not fixed

- Real-seal residual drift (3 files post-fold-re-seal, listed above) is the
  ball close's named-act re-seal, not a lane debt.
- `conftest.py:14` defaulting basetemp inside the repo is what MASKED the
  display-path class for the suite's whole life; kept as-is (it also keeps
  pytest temp out of %TEMP% contention), but any future full-suite run with
  `--basetemp` outside the repo is the honest battery - this lane now runs
  both. Post-fix census: every `relative_to` in the three touched modules
  (mag/voice_handoff.py, scripts/dead_hand.py, tools/config_seal.py) sits
  inside a guard, except tools/config_seal.py:47 which is relative to
  CONFIG_DIR itself and cannot leave it.

## Not done / limits

- Nothing committed; working tree carries this lane's edits (tools/
  config_seal.py, scripts/dead_hand.py, mag/voice_handoff.py,
  configs/links_kind_baseline.json, watch/inbox/index_events.jsonl, lane
  files) for the wave coordinator.
- The ratchet FAIL is pre-existing shared-tree state (foreign rows), not
  introduced here; see Ratchet section.
