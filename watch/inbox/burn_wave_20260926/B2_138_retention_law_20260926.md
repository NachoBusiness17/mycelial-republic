# B2-138 pack retention law (2026-09-26)

## Verdict

LANDED. The operator-prune cadence and the INDEX missing-file handling are
filed as watch/inbox/PACK_RETENTION_LAW_20260926.md (INDEX register seq
1790458967636139794), in force before pack #2 lands (2026-10-04 window).
Decision shape: a prune is operator-only and tombstoned, never erased. The one
legal route from registered-present to registered-absent is an appended
op:invalidate event whose reason names the prune date, the successor pack
(name + sha prefix) and the surviving copy (place + sha prefix); the register
line stays in the log forever. Cadence: watch/inbox keeps the TWO newest dated
packs, OneDrive the FOUR newest, prune only after the successor passes its
gates (registered + hash-clean + OneDrive sha-identical). `indexed item
missing` on an active item stays a hard ERROR: it is the unlogged-erasure
detector and this law deliberately does not weaken it. No code changed in this
lane: the existing fold invalidate op is the no-erase-compatible path
(spec before behavior change); the cadence tripwire is spec'd and self-fed
as B2-518.

## Evidence file:line quotes

- watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc on disk this lane: 1,706,469,664
  bytes, sha256 82a4efed7745a3ace2dec8fa8915d765b9508ae7946384bd8b6aa70c3f4e35e9
  (computed by sha256sum over the bytes), equal to the INDEX registration
  82A4EFED...E35E9 (ESSENTIALS_PACK_20260926.tar.gz.enc item, class artifact).
  Erratum named: the B2-54 card (line 11) prints "1,706,466,964 bytes", a digit
  transposition of the true size; trust bytes.
- scripts/index_fold_host.mjs:12-13: "Events are never erased (history is never
  rewritten); INVALIDATE marks an item inactive instead of deleting its
  REGISTER line." The fold (op === 'invalidate' branch) removes the path from
  active items; the register event stays in the log.
- mag/shared_surface.py:289-290: `if not target.is_file():` /
  `errors.append(f"indexed item missing: {item.get('path')}")` - the hard
  error this law keeps as the unlogged-erasure tripwire; validate iterates
  ACTIVE items only, so an invalidated pack is green by construction.
- scripts/index_fold_host.mjs:712: add "die(`file does not exist: ${file}`)" -
  no fabricated re-register over absent bytes is even possible via the writer.
- scripts/index_fold_host.mjs:745-767: the invalidate CLI (writerGuard,
  appendOp, refold, WARN channel) already provides everything the prune needs.
- watch/inbox/ESSENTIALS_RESTORE.md:37: "Three copies minimum, one off the
  Drive account entirely." :39: "Refresh weekly (dispatcher automation) or
  after any landmark day." The two-newest/two-verified-copies floor sits inside
  this custody law.
- watch/inbox/burn_wave_20260926/B2_54_cron_arm_card_20260926.md:18 (Prompt A):
  "never delete prior packs (operator prunes)" - the operator-only clause's
  source.
- watch/inbox/EVENTS_DRIFT_LAW_20260926.md rule 3: "does not roll back
  (no-erase law)" - same law family; the pack prune is the delete-shaped
  sibling: tombstone, never rewrite.
- OneDrive surface: /c/Users/foste/OneDrive/ holds ESSENTIALS_PACK_20260926.tar.gz.enc
  and ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc (names verified this lane;
  bytes NOT sha-verified this lane - the law's precondition P2 requires the
  sha compare at prune time, which is why the drill is self-fed).
- Cron arm status: unknown to this lane. The B2-54 card verdict is "Card only;
  nothing was armed", no Windows scheduled task matching pack/essential exists
  (schtasks query, this lane), and a ZCode cron is not observable from here;
  the law binds whichever path lands pack #2.

## Work done

1. Read the brief row, the B2-54 card, ESSENTIALS_RESTORE.md, the fold
   (scripts/index_fold_host.mjs), mag/shared_surface.py, EVENTS_DRIFT_LAW and
   the QUEUE claim/self-feed conventions.
2. Verified pack #1 against INDEX by bytes: sha256sum over the 1.7GB file
   matches the registered sha; size erratum in the card named above.
3. Confirmed the machinery answer exists: invalidate tombstones without
   erasure; validate's missing-item error checks active items only; add dies
   on missing files. No code change needed for the law to be executable.
4. Wrote watch/inbox/PACK_RETENTION_LAW_20260926.md (scope, no-erase basis,
   cadence, order of operations, missing-file handling, falsifier) and
   registered it: fold add seq 1790458967636139794, 1080 active items.
5. Filed this receipt, the LEDGER row, the QUEUE landing note on row B2-138,
   and self-fed B2-523 (retention tripwire gate), B2-524 (first prune drill
   after pack #2), B2-525 (cron arm-status audit) UNCHECKED. Erratum, corrected
   in place: first drafted as B2-518/519/520 and renumbered at apply time when
   a concurrent self-feed took that band (renumber law B2-167; the B2-214
   correction precedent).

## Falsifier

The law is inverted if any of these holds: (1) a dated pack file is deleted
while its newest event is op:register and `mag.shared_surface validate` does
not error `indexed item missing` (the detector was weakened; the law's
section 4.1 forbids exactly this); (2) an invalidate lands for a pack whose
successor failed P1 or P2 (precondition order broken); (3) the Sunday cron or
any lane deletes a pack (operator-only clause broken); (4) watch/inbox holds
three or more dated packs after a completed weekly refresh and nothing names
the lapse once B2-523 lands (cadence unenforced). Drill arm: B2-524 executes
the order of operations against pack #1 after pack #2 verifies; any
`indexed item missing` error during that drill inverts this receipt.

## Bibliography closed

watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc (bytes hashed this lane);
watch/inbox/INDEX.json (pack registrations read); watch/inbox/index_events.jsonl
(ops census via grep: register/invalidate/amend/note/autoseal families);
scripts/index_fold_host.mjs (fold, add, invalidate, verify read whole);
mag/shared_surface.py (validate loop read whole); watch/inbox/ESSENTIALS_RESTORE.md;
watch/inbox/burn_wave_20260926/B2_54_cron_arm_card_20260926.md;
watch/inbox/EVENTS_DRIFT_LAW_20260926.md; watch/inbox/burn_wave_20260926/QUEUE.md
(header laws + rows B2-54, B2-124, B2-138, B2-191); watch/inbox/burn_wave_20260926/
B2_191_queue_drift_flap_20260926.md (QUEUE living-open shape); configs/events_key_schema.json
(reason key registered); /c/Users/foste/OneDrive/ listing (names only);
schtasks query (names only, no matching task). No web calls.
