# B2-191 QUEUE registered-hash drift flap

## Verdict

LANDED with a better arm than either the brief offered. Root cause found on live bytes: QUEUE.md is an EDIT-SHAPED BOARD, not an append-only ledger. Lanes append new self-feed rows at the end AND land dated notes into existing rows mid-file; any frozen whole-file sha (or a full-prefix living seal) is falsified by the next landing note, which is exactly the observed "hash mismatch: burn_wave_20260926/QUEUE.md" flap (B2_42_validate_after.json). Fix: QUEUE.md now registers living-open (B2-156 vocabulary: edit-shaped board, no byte seal, integrity carried by the event log plus receipts), which no lane's landing shape can falsify. The critical-section arm was rejected because it needs every lane on one un-enforceable helper; the N-minute exemption arm was rejected as tamper-evidence weakening. A decisive intermediate experiment ran live: a full-prefix --living seal over 538,716 bytes was broken within minutes by concurrent mid-file landing-note edits (file grew to 538,791 with a changed prefix, fold verify: LIVING PREFIX MISMATCH), which is the byte-level proof that the board is not append-only and settles the shape question empirically.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_42_validate_after.json carries the reported 'hash mismatch: burn_wave_20260926/QUEUE.md' (the brief's named exhibit).
- mag/shared_surface.py:336-337: `elif actual_hash != recorded_hash: errors.append(f"hash mismatch: {item.get('path')}")` (the flap's error site).
- mag/shared_surface.py:12-19 (B2-156 law header): "a SEALED living item (living:true + size:N) seals only its first N bytes" / "An OPEN living item (living:true + seal:'open') is an edit-shaped board with no byte seal".
- scripts/index_fold_host.mjs:48-49 (B2-254 note): "B2-254 measured QUEUE.md and phone_relay_log.jsonl flipping failing to living across four refolds with zero register events in between" (the estate already fought this misclassification).
- Live experiment: `add ... --living` seq 1790452960608924162 sealed 538,716 bytes; fold verify minutes later: "LIVING PREFIX MISMATCH: burn_wave_20260926/QUEUE.md / sealed prefix (538716 bytes) changed; file now 538791 bytes".
- Pre-fix validate: `hash mismatch: burn_wave_20260926/QUEUE.md` present (count 1). Post living-open: count 0; fold verify: "LIVING OPEN (no byte seal, log-carried integrity): burn_wave_20260926/QUEUE.md", "verify: 1038 hash-clean, 11 living-ok, 1 living-open, 9 mismatched, 0 missing ... (of 1059 active items)".

## Work done

1. Read the flap surfaces: mag/shared_surface.py validate loop, scripts/index_fold_host.mjs (add/--living/--living-open, B2-254 and B2-40 notes), B2_42_validate_after.json.
2. Confirmed the pre-fix error live: validate reported hash mismatch on burn_wave_20260926/QUEUE.md.
3. Attempted the sealed-living arm first: registered --living from the REPO ROOT and was outside-dropped by the fold (watch/ x306 WARN; the B2-90 precedent), redone from the inbox root with seq 1790452960608924161 then 1790452960608924162.
4. The live falsifier fired against the seal arm: concurrent lanes' mid-file landing-note edits changed bytes inside the sealed prefix within minutes (538,716 to 538,791, LIVING PREFIX MISMATCH in fold verify). Named, not papered: this is the proof the board shape is edit-shaped, ending the arm debate with bytes.
5. Registered the correct shape: `add burn_wave_20260926/QUEUE.md board ... --living-open` seq 1790452960608924164. validate now carries zero QUEUE.md errors; fold verify counts QUEUE.md living-open.
6. Cleaned this lane's own residue: the B2-118 erratum had left REJECTION_TAXONOMY_20260917.md hash-mismatched against its earlier registration; re-registered the post-erratum bytes (seq 1790452960608924165), mismatches dropped 10 to 9. The remaining 9 mismatches are other lanes' evolved registrations (FLEET_IMPRINT_20260917.md, INDEX.json, BURN_JUDGE_LANE_BUILD_20260925.md, PROVIDER_HEALTH_20260926.md, B2_12_caption_ledger_build.py, B2_373_stanza_pin, P0_5_2_4_SEED_CHORD_CONDUCTOR_RECEIPT, B2_167_census_results.json, B2_465_rebuild_schedule) — named, untouched by this lane.
7. Filed this receipt, the LEDGER row, and the QUEUE row landing note (which records both the intermediate seal arm and the final living-open shape).

## Falsifier

Brief's falsifier: "a drift-free burn wave with zero QUEUE.md mismatch errors at close." The mechanism that produces zero is now in place and was exercised on live appends: after the living-open registration, validate (run twice across further concurrent lane edits) reports 0 QUEUE.md mismatch errors, and the fold verify reports QUEUE.md LIVING OPEN. Reproduction: `.venv/Scripts/python.exe -m mag.shared_surface validate | grep -c "hash mismatch: burn_wave_20260926/QUEUE.md"` must print 0 at any time post-registration, including at wave close, regardless of how many lanes land notes; any QUEUE.md error after a lane append inverts this receipt. The counter-falsifier (tamper-evidence): the event log retains the full registration chain (seq ...161, ...162, ...164) and receipts name every shape change; a silent content rewrite of a landed row remains auditable through receipts, which is the designed integrity shape for a board (B2-156 spec).

## Bibliography closed

- watch/inbox/burn_wave_20260926/QUEUE.md (the board itself; rows B2-191, B2-90 outside-drop precedent, B2-254 flip history)
- watch/inbox/burn_wave_20260926/B2_42_validate_after.json (the named exhibit)
- mag/shared_surface.py (validate + B2-156 living law docstring)
- scripts/index_fold_host.mjs (add --living/--living-open, fold, verify; B2-254/B2-40 notes)
- watch/inbox/LIVING_HASH_LAW_20260926.md (referenced by the law header)
- Nothing owed.
