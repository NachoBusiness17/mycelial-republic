# BURN b2-wave-fold: concurrent-claim falsifier counter (c)

## Verdict
TRIGGERED. The pre-registered falsifier (>2 self-feed renumber corrections in the next 50 B2 rows) fired at 18:20:10Z on 2026-09-26, when the third self-feed renumber row landed inside the next-50 window (16:48:22Z to 18:40:51Z). That window holds 11 rows matching the correction/erratum/renumber test, of which 4 are true self-feed renumber corrections. Both readings exceed >2, so the single-writer lock build is forced. It is only partially satisfied: the tree's sole process lock is the B2-360 FKB sidecar (mag/failure_kb.py); LEDGER.jsonl appends still ride the B2-167 board-highest+1 renumber law with no lock. The current last-50 window (21:12:40Z to 00:14:00Z) reads 0 corrections, so the burst was bounded, not ongoing.

## Evidence
- "briefs were drafted as B2-375 to B2-377 but the board raced past them mid-lane (concurrent self-feeds reached B2-403 before this lane write)" (B2-93-...-erratum, 17:52:00Z)
- "first appended as B2-417 and B2-418 but the concurrent B2-383 self-feed landed its own B2-417/418 rows above them" (B2-374, 18:20:10Z)
- "the concurrent B2-352 landing self-fed the same numbers mid-lane (QUEUE rows 514-515)" (B2-353-shell-pin-renum, 17:52:00Z)
- "the three briefs landed as B2-438, B2-439, B2-440 (board-highest+1 computed at landing run time" (B2-96, 18:43:10Z)
- Partial lock builds: B2-360 "100/100 index entries with the lock vs 1/100 with the lock bypassed"; B2-427 registry append-only sha pins; B2-486 queue dupes gate.

## Steal or Vacuous
Steal. The counter caught exactly the disease it was shaped for, within 100 minutes of registration. New collision species in the window, beyond interleaved-write census corruption and receipt-before-disk-flip divergence: (1) restore-clobber duplication, concurrent whole-file restores erased landed rows and minted "20 verbatim duplicate rows" (B2-355, B2-486 live fire); (2) stale lock-holder starvation, four hung git PIDs held .git/index.lock from 16:54 and blocked another lane's commit arm (B2-450). Also logged: false race attribution, B2-94-erratum-correction proved the blamed "concurrent whole-file board write" was an own close-script bug.

## Falsifier
Build the LEDGER-scoped single-writer lock (B2-360-shaped sidecar around append plus writer identity stamp), then rerun this counter over the following 50 B2 rows: pass is 0 renumber corrections and 0 restore-clobber doubles caught only post-hoc by census gates.

## Bibliography
memory/burns/LEDGER.jsonl (rows 2026-09-26T16:47:55Z through 2026-09-27T00:14:00Z; quoted rows B2-93/94/96/353/355/360/374/450/486); memory/burns/MANIFEST.json self_steal_fold b2-wave-fold entry; mag/failure_kb.py (lock byte-check).
