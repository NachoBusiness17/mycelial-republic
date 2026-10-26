# B2-297 living-downgrade detector 2026-09-26

## Verdict

LANDED and the disease is LIVE on the board: mag/shared_surface.py validate now carries a KNOWN_LIVING_PATHS watchlist (LINKS.jsonl, burn_wave_20260926/QUEUE.md, phone_relay_log.jsonl per LIVING_HASH_LAW_20260926.md section 4) and warns "living downgrade: <path> ... a plain re-register dropped it ... re-register with add --living or --living-open before the next append hard-fails" when one of them folds to an INDEX item without item.living, plus a living_files.downgraded counter. First live run: the detector FIRED on the production board, burn_wave_20260926/QUEUE.md's current registration carries NO living flag, exactly the last-register-wins drop the brief predicted (a stale whole-file refresh stands there now, so the board's next non-living append would hard-fail a verify). Owed to the fold owner: re-register QUEUE.md with --living-open.

## Evidence file:line quotes

- mag/shared_surface.py items loop (pre-edit, ~line 281): `if item.get("living"):` ... else plain whole-file hash compare `errors.append(f"hash mismatch: ...")`; no surface named a living path that had LOST its flag.
- watch/inbox/LIVING_HASH_LAW_20260926.md section 5 (last-register-wins) and section 4 (the three living shapes/named files: LINKS.jsonl, phone_relay_log.jsonl append-only originals; burn_wave_20260926/QUEUE.md edit-shaped board).
- Live validate output 2026-09-26: `living downgrade: burn_wave_20260926/QUEUE.md is a known living file but its registration carries no living flag (a plain re-register dropped it, LIVING_HASH_LAW section 5 last-register-wins); re-register with add --living or --living-open before the next append hard-fails`; LINKS.jsonl and phone_relay_log.jsonl currently still living (no warning for them).

## Work done

1. Claim law: mag/shared_surface.py working-tree-modified and tests/test_shared_surface_events.py untracked (B2-102/156/399 lanes), CLAIMs B2-297 landed (20:47:31Z, 20:49:21Z) before edits; edits rebased on fresh bytes (env-redirect tripwire arm, B2-399 scan_events_log split).
2. KNOWN_LIVING_PATHS constant with the law citation; downgrade warning arm after the items loop; living_files.downgraded counter in the summary.
3. Two fixture-first pins (downgrade warns + counter 1; still-living does not warn + counter 0) using the file's _mk_surface pattern, keyed on the real burn_wave_20260926/ shape.
4. Rebased one pre-existing pin (test_static_item_mismatch_still_errors asserted the exact living_files dict) to include downgraded: 0, rebase named in a comment per the claim law.
5. Suite: 23 passed. Em-dash 0 on added lines. Live validate re-run shows the warning (fires on the real board).

## Falsifier

Dies if: (a) a known living path sits in INDEX without item.living and validate stays silent (the detector regressed); (b) the warning fires for a path that IS living (false positive); (c) QUEUE.md's flag is restored (fold re-register with --living-open) and the warning keeps firing (stale watchlist keyed on wrong bytes); (d) a fourth living file is added to the law and the watchlist is not extended (watchlist rot; the law doc is the source of truth).

## Bibliography closed

Read whole: mag/shared_surface.py (validate path, items loop, B2-156 living counters, B2-358 tripwire, B2-399 split), watch/inbox/LIVING_HASH_LAW_20260926.md (whole), tests/test_shared_surface_events.py (surface fixture + living pins). Bytes: live validate output quoted, 23/23 pytest. Nothing synthesized; the live QUEUE.md downgrade named as owed to the fold owner, not silently fixed.
