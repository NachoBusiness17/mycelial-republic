# SUITE-RED REGISTER + WINDOW CLOSE — 2026-09-27 (gate-fix + lens window)

Operator opened the day: "stop waiting for arbitrary time of day and execute
the order to start the day"; mid-window: "IF it doesnt break everything lets
do this too" (audit seat's priority block) + the LENS order. This receipt
closes the window. Earlier batch receipt: GATE_DEBT_BATCH_20260927.md.

## 1. The assignment-bypass gate defect — FIXED (the day's headline)

The audit seat (L2-Hermes) found the secret gate does not block keys written
as assignments (receipt watch/inbox/audit_20260926/GATE_DEFECT_
ASSIGNMENT_BYPASS_20260927.md): COMBINED ORs all rules into one alternation,
finditer is non-overlapping, the generic NAME=value alternatives at the tail
swallow the line, and the provider rule never fires. `XAI_API_KEY=xai-...`
landed LOW and did not block — the dominant real-world form was invisible.

Fix (per the receipt's own direction, no reordering): BLOCKABLE_RES per-rule
compilation in secret_gate_rules.py; scan() and history_scan() evaluate every
blockable provider rule independently first, emit through a shared
row-builder, and the COMBINED report pass skips overlapping spans so the
provider rule wins exactly once.

Proofs, all on bytes:
- The defect's four-form table now blocks everywhere: assigned_xai,
  assigned_anthropic, MY_SECRET=xai, bare anthropic — all exit 1 blocking=1.
- tests/test_gate_blocking_paths.py (audit lane's file): 14/14 green (was
  12/14; the honest failure flipped green; the checkbox positive-control
  fixture re-pointed at QUEUE.md, a name the resolver actually reaches).
- Prefilter parity MATCH post-fix (SG_NO_PREFILTER standing falsifier).
- Fixed scope (burn_wave_20260926): counts IDENTICAL pre/post fix (356
  rules, 0 blocking) — the corpus's assigned-key exposure lives in the known
  tar/steps.jsonl, which the gate now catches.
- First live catch of the fixed engine: 5 blocking on --changed = the audit
  lane's synthetic test fixtures (3), the defect receipt's example token (1)
  — both named-accepted in configs/secret_gate_baseline.json paths — and ONE
  real new finding: mrpool_export media register line 198 GOOGLE-OAUTH-AQ,
  context-verified a telesco.pe CDN FILENAME (cdn4.telesco.pe/file/<342
  base64url>.jpg), not a credential; named-accepted with reason (same class
  as the standing cdx_rar.json entry).
- Hook-shape final: --changed --baseline → blocking=0, exit 0.
- RATCHET PASS (secret_gate_scan.py held at exactly 400 lines; fix landed
  inside the bar, zero registrations).

## 2. All hard gates GREEN at close (were 3 red at audit time)

- checkbox_receipt_gate: PASS (489 checked rows, 0 offenders; B2-142's row
  now names its byte-existing receipt B2_142_cerebras_dig_20260926.md).
- config_seal: PASS 54/54 after re-seal BY NAME (gate-fix-window-20260927;
  the two baseline files this window touched).
- secret_gate --changed: blocking=0 on the FIXED engine.
- violation_ratchet: NEW=0.
- md_record audit: RECORD CLEAN (5/5).
- shared_surface validate: ok:True, 0 errors, 0 unindexed.
- B2-536's demand (migrate the 4 B2-142 LINKS rows + validate to zero) was
  satisfied by this window's LINKS→EVENTS relocation; falsifier re-checked.

## 3. Suite-red register (the honest numbers, instrument named)

Full honest run 2026-09-27 ~09:00-09:40 EDT, single worker (xdist installed
after, on operator order): **40 failed / 2,256 passed / 7 skipped** of 2,303
collected / 352 files (07:05 census instrument; +test_gate_blocking_paths.py
landed after the census moment — census-denominator law: name instrument and
moment, never difference across moments).

Fixed this window (9): test_quota_billable ×2 (made hermetic — they pinned
the live untracked providers.yaml deepseek 30M burn cap; tests now pin their
own quota via monkeypatched get_provider), test_index_fold_host ×4 (the fold
host's verify printed host-absolute paths; contract = inbox-relative, host
fixed to print `raw`), test_shared_surface_events ×1 (scout's new
SCOUT-QUIET-2 kind row registered in links_kind_baseline per the B2-168
pattern), test_gate_blocking_paths ×2 (the defect + the fixture path).

PRE-EXISTING, registered not hidden (31 failures / 17 files, root causes
sampled 2026-09-27): test_memlang ×6 (engine returns empty results,
KeyError 'executed' — one module may explain all six), test_desk_baseline_
probe ×6 (dashboard static-data assertions drifted from wave-era UI changes),
test_water_computer ×5 + test_organ_map ×2 (the audit seat's LANE4D already
flagged water_computer as never-wins + overwriting a shared character file),
test_frontier_council ×2, test_falsifier_ledger ×2, test_wave_driver ×1,
test_supervision_soak ×1, test_substrate_identity ×1, test_pack_modes_
steward ×1, test_no_win ×1, test_mirror_intro ×1, test_loop_death_guards ×1,
test_healthz_status ×1, test_ghost_spooky ×1, test_all_seat_interaction ×1.
Next-window order: memlang first (cheapest possible 6), then water_computer
family.

## 4. THE LENS (the operator's named deliverable)

watch/inbox/lens_20260927/ — five files: THE_LENS_20260927.md (synthesis),
did_census.{jsonl,md} (778 receipts: 65/635/78 by day), are_inventory.md
(1,031 mag modules, 177 tools, 353 tests, 43+51 ribs, 13 tasks, 1,340 INDEX
items), doctrine_revisit.md, external_links.md (6/6 fetched, zero owed).
Headline verdicts: DRIVING = law without measurement (probe20 empty — first
amendment: llama-server up, probe20 --live ≥5 cycles); MEMLANCE = unproven
coinage (run the five-lance falsifier or demote); AuK = the NPC voice piece;
sizegame = the budget-metric referee pattern.

## 5. Also this window

- pytest-xdist 3.8.0 installed (operator: "don't use a single worker thats
  stupid") — future full runs go -n auto.
- xdist smoke: 17 passed / 4 workers / 4.7s.
- Fleet doctor's 08:30 alert = the rescan task this window already fixed at
  root (missing Set-Location; incremental validated live 67,566 rows).
- Census carrier: 2,303/352 stands as the 07:05 patrol moment; drift since
  (+1 file/+14 collected) is within the ±20 bar and re-verifies at the next
  daily --collect.

## 6. Operator-gated at close (unchanged + urgent)

1. **ROTATE the xAI key** — now first-first: the gate hole is closed but the
   live key sits in 9+ history copies (PURGE_LIST_MERGED_20260927.md).
2. lan.key regeneration; purge GO; MagSecretScanWeekly disposition.
3. Salvage scope (audit seat's open questions): which archives (attic/ 2.9GB
   vs the encrypted 1.59GB ESSENTIALS_PACK), orphan-of-shape vs orphan-of-use.
4. Push: the branch is gate-green; the 1.69GB push is the known slow shape.
