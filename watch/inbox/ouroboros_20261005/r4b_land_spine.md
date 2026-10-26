# R4B LAND SPINE: INPUT FEED + CLOCK LEG + GATE MIRROR (ouroboros R4 moves 1+2+5)

Lane: R4b-LA, 2026-10-06 ~05:1x-05:5xZ, executing rows 1, 2 and 5 of
watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md (the
RESUMED run's fold). Build-on note honored: the first-pass L1 lane's
committed work (tools/zknot.py S1 gate, tools/thought_quantizer.py v0.5,
mag/boot_regen.py chain, scripts/lawpack_daily.ps1 + MagLawPackDaily) was
kept and extended, never undone. No git commit (standing lane law).

## Move 1: the vault feeds the compile (fold S1 cured)

The two law stacks now merge at the compile. tools/thought_quantizer.py
(v0.6 law in its header) pulls mag.rib_boot.lawpack_amendment_rows()
(mag/rib_boot.py:186, reading mount_vault() LIVE) beside
memory/percolator/invariants.json: every mounted POST-DATUM/AMENDMENT
section joins the ranking at weight 1.0 under shape vault-amendment, never
the refusal pass, rib rows inserted first so stable-sort ties favor vault
law; a law rib that fails to mount refuses the whole compile (SystemExit
"failed to mount") instead of packing silently without the vault.

Row delta proof, banked in watch/inbox/ouroboros_20261005/r4b_flash_delta.json
(byte source of every number in this section): before, the pack held kept
620 / packed 620 from percolator_in 648 rows in packs frontier 24, flash
12, local 584, with flash_rows_carrying_d4_era_amendment_markers 0 under
compile stamp 2026-10-06T02:00:48Z; after the recompile through the final
(refactored) code, kept 625 / packed 625 with rib_amendments_in 5 and
rib_amendments_kept 5, packs frontier 24, flash 12, local 589, and
flash_rows_carrying_MEASURED_ON 2 (the d4-era marker named by the
SYNTHESIS row 1 test demand). All five mounted amendments sit in the flash
band (flash_rib_sources: MODEL_GATES #1 and #2, INFERENCE_BUDGET #1,
FREE_USAGE_POLICY #1, BEHAVIOR_CARDS #1 - the fifth is a sibling lane's
move-6 rib amendment that landed mid-flight and rode in through the LIVE
vault read, which is the feed working as designed); the five lightest
percolator rows listed in percolator_rows_pushed_out_of_flash slid from
flash into the lower bands (kept==packed held, the L4 linker law).
The daily lane needed no change: scripts/lawpack_daily.ps1 (task
MagLawPackDaily, cf. scripts/boot_regen_daily.ps1 naming its 09:30 slot)
already fires tools/thought_quantizer.py compile, so every future daily
recompile carries the vault feed.

New pins in tests/test_thought_quantizer.py (23 tests total in that file
per r4b_flash_delta.json tests field):
test_rib_amendment_rides_band_one_into_flash (a vault amendment stays in
the flash band against a full court of fresh imperative percolator rows),
test_real_vault_law_reaches_the_real_flash_pack (the demanded assertion:
real invariants + real vault compiled, at least one flash row carries
MEASURED ON or max_concurrency), and
test_unmounted_law_rib_refuses_the_compile (renamed rib refuses before any
pack file is touched). Percolator-side pins kept their exact census
semantics via the injected empty feed.

## Move 2: the clock leg + attribution (fold S2+S3 cured)

mag/boot_regen.py gained a CLI (python -m mag.boot_regen, mag/boot_regen.py:178)
with the SAME exit contract as the context-pack path: exit 0 on ok/skipped,
exit 2 on step-failure/missing/age, so a standalone run can never come back
greener than the chained one. scripts/boot_regen_daily.ps1 mirrors the
lawpack/fts daily shape (Set-Location repo root, absolute venv python,
logs/boot_regen.log START/tool/END stamps, alert row to
watch/inbox/boot_regen_alerts.jsonl + best-effort memory/attention.md block
on nonzero); scripts/register_boot_regen_task.ps1 registers it through the
run_hidden.vbs wrapper (the headed-windows cure law). Registered and
verified live: schtasks /Query /TN MagBootRegenDaily reads Status Ready,
daily 07:15 (next run the morning after landing), task action the hidden
launcher over scripts/boot_regen_daily.ps1, matching the
scripts/register_boot_regen_task.ps1 body. Hand-fired once as proof: exit 0,
verdict "all components regenerated and fresh", wall 8.852s in
logs/boot_regen.log (zknot + hermes_warm_boot + rib_boot all ok).

Attribution: tools/zknot.py gained --actor/--trigger (env fallbacks
ZKNOT_ACTOR/ZKNOT_TRIGGER, else manual) stamped on every
memory/runs/zknot/runs.jsonl receipt row (ok, truncated-unnamed, stopped);
mag/boot_regen.py:148 stamps the zknot step mag.boot_regen + the caller
trigger carried by MAG_BOOT_REGEN_TRIGGER; main.py's context-pack branch
names itself (mag.cmd context-pack) via os.environ.setdefault; the daily
script sets MagBootRegenDaily. The hand fire banked the first natively
attributed row: memory/runs/zknot/runs.jsonl ts 2026-10-06T09:31:21+00:00
actor mag.boot_regen trigger MagBootRegenDaily. The two unattributed
tonight rows named by the fold were stamped in place with an
attributed_post_hoc marker (23:38:34Z actor "tools/zknot.py hand run
(R4-L1 lane)" trigger manual; 02:18:16Z actor mag.boot_regen trigger
mag.cmd context-pack) - attribution reconstructed from the row schemas,
marked as post-hoc, original fields untouched.

## Move 5: the S1 gate mirror - found ALREADY landed, verified, credited

The resumed fold's row 5 claimed "tools/zknot.py has no exit() path (my
rg), so a standalone zknot run is ungated". The bytes disagree: the
first-pass lane already mirrored the gate into the organ - tools/zknot.py
s1_gate at tools/zknot.py:280, the omission block in build_latest
(name_omitted / OMIT_MARK), and the fail-closed branch printing the S1
GATE line and returning exit 2 at tools/zknot.py:383-385, keeping the
previous LATEST.md and filing a truncated-unnamed receipt row. The fold's
instrument was the artifact: an rg for "exit(" misses the actual shape
("return 2" + "raise SystemExit(main())"), so S4 dies as an instrument
finding, not a code gap. Verified this sitting by
tests/test_zknot_gate.py (all green in the suite run below) and the live
02:18:16Z receipt row (dropped_named 16). Nothing was rewritten;
amend-never-rewrite, the credit stays with the first pass.

## Gates

- pytest touched suites green: tests/test_thought_quantizer.py
  tests/test_boot_regen.py tests/test_zknot_gate.py
  tests/test_rib_boot_amendments.py - the combined run passed clean
  (moment 2026-10-06 ~05:4xZ, this seat's own run), including the new
  flash-row assertion.
- tools/violation_ratchet.py check --changed: PASS, NEW=0. The first cut
  of move 1 pushed tools/thought_quantizer.py past the 400-line bar; cured
  by extracting the feed into mag/rib_boot.py (366 lines, additive beside
  a sibling lane's uncommitted CREATE_NO_WINDOW fix, untouched) and
  compressing my own additions - no baseline debt accepted.
- schtasks /Query /TN MagBootRegenDaily verified (above).
- tools/citation_lint.py check --changed run on this receipt's landing.

## Residue / notes for the fold

- mag/rib_boot.py carries a sibling lane's uncommitted change (_run
  CREATE_NO_WINDOW) plus my additive lawpack_amendment_rows; both survive
  each other by construction.
- The vault grew mid-flight (BEHAVIOR_CARDS sixth mount + its CARD INDEX
  amendment) and the live feed picked it up with zero producer change -
  evidence the merge is structural, not a point fix.
- Not run here: the full pytest suite, a real standalone S1 exit-2 live
  fire (unit-pinned instead; forcing a truncation on the live db was
  deliberately avoided mid-round), and MagLawPackDaily's own 09:30 fire
  (tomorrow's first scheduled proof of the feed on a clock).
