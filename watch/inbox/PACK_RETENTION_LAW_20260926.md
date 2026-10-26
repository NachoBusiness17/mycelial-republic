# PACK retention law (B2-138, 2026-09-26)

Scope: the dated essentials packs `ESSENTIALS_PACK_YYYYMMDD.tar.gz.enc` that the
weekly refresh drops into watch/inbox each Sunday (recipe card:
watch/inbox/burn_wave_20260926/B2_54_cron_arm_card_20260926.md; INDEX registers
each by name+sha). Pack #1 on disk at law time: ESSENTIALS_PACK_20260926.tar.gz.enc,
1,706,469,664 bytes, sha256 82A4EFED7745A3ACE2DEC8FA8915D765B9508AE7946384BD8B6AA70C3F4E35E9,
INDEX-registered, OneDrive copy present. The vault pack
ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc is OUT of scope: it is a one-off vault
archive with no successor stream, so no cadence and no prune apply to it.

This law must hold before pack #2 lands (2026-10-04 window). It binds whichever
refresh path produces pack #2: the armed Sunday cron or the manual Command B
fallback.

## 1. No-erase basis

INDEX.json is a derived fold; the append-only log watch/inbox/index_events.jsonl
is the source of truth; writers append events and never rewrite the file or the
log (INDEX.json `purpose` field). The fold's own header states the rule this
law builds on (scripts/index_fold_host.mjs:12-13): "Events are never erased
(history is never rewritten); INVALIDATE marks an item inactive instead of
deleting its REGISTER line."

Therefore a prune NEVER deletes or edits an INDEX row and NEVER edits the log.
The one legal route from registered-present to registered-absent is a single
appended `op: invalidate` event. The register line (name, class, purpose, sha)
stays in the log forever; the fold merely stops listing the path as an active
item.

## 2. Operator-prune cadence

1. WHO: the operator only, by hand. Lanes and the cron automation never delete
   a pack (B2-54 Prompt A, verbatim: "never delete prior packs (operator
   prunes)").
2. WHEN: at most once per weekly refresh, always AFTER the new pack has passed
   its gates, never during pack build. Skipping a window is legal; deleting on
   a stale verification is not.
3. HOW MANY: watch/inbox keeps the TWO newest dated packs (current + one
   fallback; about 3.4GB steady state). The OneDrive mirror keeps the FOUR
   newest dated packs (about a month of rollback). Older dated packs on either
   surface may be pruned on the same cadence. The custody floor is never
   broken: the newest pack always keeps at least two verified copies
   (watch/inbox plus OneDrive) per the custody law
   (watch/inbox/ESSENTIALS_RESTORE.md:37).
4. Preconditions, byte-verified in order before ANY deletion:
   - P1: the successor pack is registered in INDEX by name+sha AND
     `node scripts/index_fold_host.mjs verify` reports it hash-clean.
   - P2: the successor's OneDrive copy exists AND its sha256 equals the
     registered sha, computed at prune time on both bytes. Presence alone is
     not verification.
   - P3: the doomed pack is not the successor.

## 3. Order of operations (the only legal prune)

1. Verify P1 + P2 + P3.
2. From watch/inbox, append the tombstone FIRST:

       node <repo>/scripts/index_fold_host.mjs invalidate \
         ESSENTIALS_PACK_<old>.tar.gz.enc \
         "operator prune <YYYY-MM-DD>; successor ESSENTIALS_PACK_<new>.tar.gz.enc \
         registered sha <sha-prefix>; OneDrive copy sha <sha-prefix> verified <YYYY-MM-DD>"

   The reason MUST name the prune date, the successor pack (name + sha prefix)
   and the surviving copy (place + sha prefix).
3. Confirm the refold dropped the item from active items (the invalidate
   command prints the new active-item count).
4. Only then delete the file. Between steps 2 and 4 every checker stays green
   (inactive items are not hash-checked), so an interrupted prune is safe in
   both directions: tombstone without deletion is harmless; deletion without
   tombstone is not (section 4.1).
5. Prove the end state: `.venv/Scripts/python.exe -m mag.shared_surface
   validate` and `node scripts/index_fold_host.mjs verify` are green on packs,
   and a one-line watch/inbox receipt names the pruned pack, the successor and
   both sha prefixes.

## 4. INDEX missing-file handling

1. `indexed item missing` on an ACTIVE item stays a hard ERROR
   (mag/shared_surface.py:290). Absent bytes under a live registration are
   unlogged erasure, the exact failure this law makes loud. Never weaken the
   check, never exempt a filename pattern from it.
2. A registered file MAY be absent only when the newest event for its path is
   an invalidate naming the erase; the fold then keeps it out of active items
   and every checker is green by construction.
3. Bytes found missing WITHOUT an invalidate (disk loss, accidental delete):
   restore the identical bytes from a verified copy, after which the original
   registration sha matches again and no re-register is needed; or, if
   unrestorable, the operator files an honest invalidate naming the loss plus
   the owed note. Never re-register a fabricated sha; the fold's add already
   dies on missing files (scripts/index_fold_host.mjs:712).
4. No checker change lands with this law: the existing invalidate op is the
   no-erase-compatible path and this spec binds procedure to it (spec before
   behavior change). The cadence tripwire, a validate WARNING when more than
   TWO active dated packs are registered after a completed refresh, is spec'd
   here and self-fed as QUEUE row B2-518, not coded now.

## 5. Falsifier

- A pack file deleted while its newest event is `op: register` and
  `mag.shared_surface validate` does NOT error `indexed item missing`: the
  missing-file detector broke and this law is falsified.
- An invalidate lands for a pack whose successor failed P1 or P2: the
  precondition law is broken.
- Any cron- or lane-driven deletion of a dated pack: the operator-only clause
  is broken.
- watch/inbox holding three or more dated packs after a completed weekly
  refresh: the cadence lapsed; once B2-518 lands, its tripwire must name it.

Landed by: watch/inbox/burn_wave_20260926/B2_138_retention_law_20260926.md
