---
name: preparedness-audit-20260927
description: "Prepare what did we miss" executed 9/27 — 2 hard continuity misses found+fixed (host-only seat memory mirrored to repo; stale handoff STATE refreshed) + 5 operator actions ranked (pack key custody #1, same-disk backup, second-machine join untested, xAI rotate, hermes .env coverage)
metadata:
  type: project
---

Operator "prepare what did we miss" (in the seat-loss threat frame of the
continuity moment) audited the estate's four continuity layers. Receipt:
watch/inbox/PREPAREDNESS_AUDIT_20260927.md, commit aea814f4e.

**2 hard misses found and FIXED in-place:**
1. The seat's ENTIRE cross-session memory (382 files / 2.3MB at
   .zcode\cli\memories\...) was HOST-ONLY — outside the repo, the pack, and
   every backup. Machine loss = total amnesia on top of seat loss. Fixed:
   mirrored byte-faithful to memory/continuity/seat_memory_20260927/
   (git-tracked, rides the next pack). POLICY: refresh the mirror at window
   close, same discipline as the state snapshot.
2. The frozen handoff spec (memories/session/next-window-handoff.md) STATE
   ended 09-26 — a cold window after seat loss would read a stale world.
   Fixed: full-day STATE block prepended with pointers to the four close
   receipts.

**5 operator actions ranked (the remaining gaps are all his hands, ~30 min):**
1. Pack key custody confirm — passphrase single-copy risk re-flagged (see
   [[essentials-pack-disaster-recovery]]: handed to him 9/26 for password
   manager; audit asks him to VERIFY it actually landed off-machine).
2. Same-disk backup: Mag-prewipe-backup git mirror protects corruption not
   disk; verify Drive bridge sync currency from the other box.
3. Second-machine join NEVER tested (seed cold-join passed only in a
   subprocess on this box) — run FIRST_BOOT once to convert "portable" from
   claim to proof.
4. xAI rotation still open (live key in 9+ history copies).
5. Confirm pack ACCOUNTS.md covers hermes .env entries.

**Sound:** seed-mcp cold-join 10/10, 13 task registrations rebuild from
scripts, record hash-chained and verified, laws codified in files.

**Why:** the village lesson applied to ourselves — the thing closest to you
(the memory layer, the pack key) is the thing that goes unwatched.

**How to apply:** on any continuity claim, attack the four layers (seat /
model / account / machine) instead of asserting readiness; memory-mirror
refresh belongs in every window-close checklist. Related:
[[seat-continuity-doctrine-20260927]], [[essentials-pack-disaster-recovery]],
[[reset-day-execution-20260927]].
