# R4-L1 LANDING: the law pack, the daily trigger, and the regen chain (2026-10-05)

Lane: URGENT R4-L1 (time bomb first). Ask source: SYNTHESIS moves 2+3 at
`watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md`.
All commands ran under `.venv/Scripts/python.exe` (or mag.cmd, which does).
No git commit (lane law). No em/en-dashes in landed files (verified by scan).

## 1. The pack: recompiled NOW (the 2026-10-06T15:18Z time bomb defused early)

- BEFORE: compile_report.json read `compiled 2026-09-29T15:18:39Z`, stats
  `in 401 / kept 374 / packed 374`, packs flash 12 / frontier 24 / local 338
  (banked from the pre-compile file read this sitting; SYNTHESIS row 2's
  "12 rows" was the flash tier).
- RECOMPILE: `.venv/Scripts/python.exe tools/thought_quantizer.py compile`
  exit 0 at 2026-10-06T02:00:48Z: `in 648 / kept 620 / packed 620`,
  packs flash 12 / frontier 24 / local 584. kept==packed (linker law) True;
  error-quoting laws kept 74.
- WEEK'S LAW VISIBLE (the gate): `grep -c "2026-10-04\|2026-10-05"
  instructions_flash.jsonl` = 9 of 12 flash rows dated 10-04/10-05 (e.g. the
  10-05 law "Verify via OUR systems before declaring done (get_errors + read
  the actual file ...)"; local tier carries 2 further 10-05 rows). Honest
  note: the literal d4 rib marker string "omission is a MEASURED ON state"
  appears in NO compiled pack because the percolator feed never banked it
  (it lives in the rib vault; R4-L2's rib_boot/context_pack seam carries it,
  not this pack).

## 2. Min-rows assertion (an empty compile can never serve as law)

`tools/thought_quantizer.py:119` `MIN_KEPT_LAWS = 1`; the
`census["kept"] < MIN_KEPT_LAWS` refusal in the same compile_packs pass
fires BEFORE any pack file is written, so a
zero-keep compile (empty --in, shape drift) can neither write empty packs
nor stamp a fresh compile_report that would un-hide the consumer debt
pointer. Pins: `tests/test_thought_quantizer.py` (empty compile refused;
previous good packs byte-unchanged; floor constant).

## 3. Daily recompile task (the MagFtsIndexDaily pattern)

- `scripts/lawpack_daily.ps1`: Set-Location to repo root (PATH LAW), the
  absolute venv python, check -> recompile-if-stale -> post-check + flash
  row floor (bytes, not reports), log to `logs/lawpack.log`, single-writer
  alert row to `watch/inbox/lawpack_alerts.jsonl` + best-effort
  memory/attention.md, nonzero Last Result on failure.
- `scripts/register_lawpack_task.ps1` + run_hidden.vbs launcher (no desktop
  console pop). Registered via
  `MSYS_NO_PATHCONV=1 powershell ... register_lawpack_task.ps1`:
  task `MagLawPackDaily`, DAILY 09:30 (after Improve 08:00, Census 08:30,
  FTS 09:00), schtasks /Query reads Status: Ready, Next Run 10/6/2026 9:30
  AM. Hand-fire proof: exit 0, log row "PRE check exit=0 ... verdict=fresh,
  no write" (the pack this lane compiled is serving).

## 4. The regen chain wired into mag.cmd context-pack (exit 2 on age or truncation)

- `mag/boot_regen.py` (new): `run_boot_regen` at line 128 fires the three
  organs as ONE idempotent chain under the same venv interpreter (zknot ->
  `python -m mag.hermes_warm_boot` -> `python -m mag.rib_boot`), then stamps
  ages (`component_ages` line 80) for all four components (the three above
  plus the law pack's compile_report, aged by its own compiled stamp, the
  consumer's logic). Verdict grammar (`_verdict` line 110): ok / skipped /
  step-failure / missing / age, all against the ONE decay bar
  PACK_STALE_DAYS=7. MAG_BOOT_REGEN_SKIP=1 skips firing but never the age
  gate.
- `main.py:3524` fires `regen = run_boot_regen()` in the context-pack
  branch BEFORE building the pack; `main.py:3552` `_regen_exit` prints the
  verdict stamp and returns
  exit 2 on any verdict other than ok/skipped. A zknot exit 2 rides in as
  step-failure, so the S1 gate below escalates to context-pack exit 2.
- `mag/context_pack.py:1211` renders the component-age stamp line into the
  L0 policy header when the CLI report is present (CLI-chain only by
  design: in-process builds stay byte-stable so the calibrated pack-budget
  gates in tests/test_context_pack_delivery.py are not tipped by a
  live-mtime line).
- LIVE RUN (the gate): `mag.cmd context-pack` exit 0; trailing line
  `BOOT-REGEN: ok (zknot=0.0d warm_boot=0.0d rib_boot=0.0d lawpack=0.012d)
  - all components regenerated and fresh`; header stamp present in
  `memory/context_pack_latest.md`:
  `boot_regen: ok · zknot=0.0d · warm_boot=0.0d · rib_boot=0.0d ·
  lawpack=0.012d (bar 7d, mag/boot_regen.py)`.

## 5. S1 no-silent-truncation gate (the [:3] rewrite's disease)

- The [:3] rewrite now NAMES every qualifying session it cuts:
  `name_omitted` at tools/zknot.py:228 (cap 10 + "+N more", date + short id
  + title), assembled by `build_latest` at tools/zknot.py:248 into an
  explicit "Not carded above" block.
- `s1_gate` at tools/zknot.py:280 is the fail-closed law: dropped sessions
  without the omission mark => main refuses at the s1_gate call site in
  tools/zknot.py, keeps the previous LATEST, files a `truncated-unnamed`
  receipt row.
- LIVE PROOF: the chain-fired run's receipt row (memory/runs/zknot/
  runs.jsonl, 2026-10-06T02:18:16Z) reads `status ok, qualifying 19,
  dropped_named 16, written 5`; `memory/zknot/LATEST.md` carries the
  omission block. The 2026-10-05 disease row (qualifying 18, LATEST 3
  cards, zero omission tokens) can no longer recur silently.
- Pins: `tests/test_zknot_gate.py` (naming, cap+count, gate truth table,
  redaction of titles inside the omission block).

## 6. Gate numbers

- pytest (this lane's touched files): tests/test_thought_quantizer.py +
  tests/test_zknot_gate.py + tests/test_boot_regen.py = 32 passed, 0 failed.
- Ratchet: `check --changed` reads NEW=2, BOTH in sibling-owned files
  (an except-pass in mag/rib_boot.py and a file-too-long in
  tools/ouroboros.py, both at the line numbers the ratchet's own output
  names; a no-flag run also surfaces an except-pass in tools/fold_gate.py
  from tonight's committed fold-gate wave). Scoped to THIS lane's files
  inside the gate roots (tools/thought_quantizer.py, tools/zknot.py,
  mag/boot_regen.py, mag/context_pack.py): hits=2, NEW=0. main.py is
  outside the ratchet's mag/+tools/ roots (its NEW rows in a forced scan
  are not gate-visible).
- test_context_pack_delivery.py attribution (not this lane's files; run as
  a safety check): 2 failures pre-exist at HEAD (verified in a detached
  git worktree at 55cdaaa4f: shed-ladder + objective-bounds); 3 budget
  hard-clip failures are live-tree only and come from this week's untracked
  rib/doctrine growth - the sibling R4-L2 seat measured the same clips this
  sitting (documented in its _rib_vault_law docstring in
  mag/context_pack.py). This lane's in-process render delta is zero bytes
  (boot_regen key absent in-process; the clip persists with rib_vault
  removed too - measured).

## Residue / notes for the next seat

- The context-pack CLI's full-mode render still ends "(pack clipped)" from
  the same live-content growth; rebalancing MODE_CONFIG budgets is an
  operator/owner decision, not this lane's.
- Sibling R4-L2 landed `rib_vault` into mag/context_pack.py mid-flight;
  this lane preserved it byte-for-byte and only removed its own dead
  `_boot_regen_stamp` call.
- Daily lane order on the host now: Improve 08:00, Census 08:30, FTS 09:00,
  LawPack 09:30.
