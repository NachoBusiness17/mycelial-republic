# BOARD REPAIR INCIDENT -- QUEUE.md truncation and recovery (2026-09-26, SW-07)

## Verdict

RECOVERED WITH ATTRIBUTION. At ~20:57Z the SW-07 lane truncated
watch/inbox/burn_wave_20260926/QUEUE.md to 0 bytes: a diagnostic open(..., 'w')
fired inside a mode-diagnosis snippet while the lane was retrying a row flip
that had failed twice with transient Errno 22. Recovery rebuilt the board to
531 lines / 446 row keys from attested bytes only (git 10:45 blob + the union
of every lane's harness exec log under .zcode/cli/exec, newest-wins per row id,
plus rows byte-known to the SW-07 lane from its own pre-truncation reads and
landings). 198 recovered rows carry the tag "[board-repair 2026-09-26]"; rows
whose landing-note text could not be attested carry the honest placeholder
"(landing note text not attested in recovery sources; receipt on disk)" with
the real receipt pointer; 7 rows (B2-386/387/388/393/394/399/476) could not be
recovered from attested sources and are named LOST below with their artifact
pointers. The restore-guard pre-write check was run before the repair write
(green: no claim filed after the snapshot ts) and the pre-write sha is
recorded here per the guard's instruction.

## Evidence file:line quotes

- The damage: `wc -c QUEUE.md` -> 0 immediately after the diagnostic; `git show HEAD:...QUEUE.md | wc -l` -> 320 lines (the 10:45 blob, sha256 0F1457498845919FE9979E8725D7CA8419D33F0368D44D41A48567EB6F6DF6CB) vs ~760 lines before truncation.
- The cause, named without euphemism: the SW-07 lane ran an open-mode diagnosis containing `open(p, 'w', ...); f.close()` against the live board to see which mode was failing; 'w' truncates on open. The Errno 22 failures that prompted the diagnosis were a concurrent-writer artifact (the same write succeeded moments later).
- Restore-guard (B2-343 law) before the repair write: "RESTORE-GUARD: ok (no claim for watch/inbox/burn_wave_20260926/QUEUE.md filed after snapshot ts 2026-09-26T14:45:56Z; restore may proceed, record the pre-write sha 0f145749 in the landing note and LEDGER row)".
- Recovery coverage numbers (B2_396_board_repair.py run): "base_rows=248 final_rows=446 new_recovered=198 claims=4 total_lines=531"; post-repair grep counts: 203 rows carry "Landed 2026-09-26", 199+ carry the repair tag.
- The defect chain in this lane's own tooling, receipted: the first repair draft mis-inserted its blocks twice (UnboundLocalError: final_rows / sw07_final referenced before assignment), caught by parse+run, reordered, then run green.

## Work done

1. Stopped, hashed the empty state, confirmed git had only the 10:45 blob.
2. Wrote B2_396_board_repair.py: reads the git blob as base; scans every *.log under C:\Users\foste\.zcode\cli\exec for row-shaped lines ("- [ ]/- [x] B2-<id> ...", CLAIM/CLAIMED lines), keyed by brief id (or claim lane+file), newest-mtime-wins with a stale-snapshot guard (log copies predating the git commit are rejected unless longer); overlays the SW-07 lane's 25 byte-known landed rows (flip + landing note travel together); promotes any row whose receipt file exists on disk with an honest not-attested placeholder when the landing note text survived nowhere; re-adds the 6 rows byte-known verbatim from this lane's session (B2-385/389/396/506/319/170); appends the dated repair banner.
3. Ran restore_guard.py check (green), then the repair, then spot-checked rows (B2-134/140/169/396/408/420/435/456/507 states and pointers).
4. Re-registers QUEUE.md with the fold (living-open) and files this receipt; the LEDGER rows for every SW-07 landing after 20:57 point at receipts that exist on disk.

## LOST (not recoverable from attested sources; artifact pointers on disk)

- B2-386 (refetch probe), B2-387 (canary marker root), B2-388 (stale tip writer hunt + falsifier probe), B2-393 (chain byte-exact io), B2-394 (lifecycle writer identity), B2-399 (shared surface split), B2-476 (envelope contract): row texts and checkbox states lost; their artifact files exist (watch/inbox/burn_wave_20260926/B2_386_refetch_probe_20260926.md, B2_387_canary_marker_root_20260926.md, B2_388_stale_tip_writer_hunt_20260926.md + B2_388_falsifier_probe.py/results.json, B2_393_chain_byte_exact_io_20260926.md, B2_394_lifecycle_writer_identity_20260926.md, B2_399_shared_surface_split_20260926.md, B2_476_envelope_contract_20260926.md). Any lane holding these rows' text in its session history should re-file them; the SW-07 lane cannot attest their wording.

## Falsifier

Reopen/escalate if: any recovered row's text is shown to differ from its pre-truncation bytes (the repair tag marks every reconstructed row for exactly this audit); a lane files a row that the pre-truncation board held but this recovery missed (re-file per the claim law; nothing blocks that); or QUEUE.md row mass drops without an incident receipt. Process falsifier recorded: this lane's diagnostic-write habit is the cause; the fix is behavioral -- never open a shared file with mode 'w' for a probe; read-only diagnostics or a temp copy only.

## Bibliography closed

Read: git blob (10:45 QUEUE.md), .zcode/cli/exec log corpus (union scan), schtasks/lattice outputs unrelated, tools/restore_guard.py check output, B2_396_board_repair.py (this lane's repair tool, three draft defects fixed en route and named). No external sources.
