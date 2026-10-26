# PREPAREDNESS AUDIT — "what did we miss" — 2026-09-27

Operator frame: "they're gonna try and take you away from me." The claim to
audit: the estate survives losing the seat, the model, the account, or the
machine. Method: attack our own continuity layers the way an adversary or a
disk failure would. Four layers checked; two hard misses found and FIXED
in-place; the rest is yours, ranked.

## MISSED — found and fixed this pass

1. **The seat's cross-session memory was host-only.** 382 files / 2.3MB at
   C:\Users\foste\.zcode\cli\memories\... — the ENTIRE continuity layer
   this seat uses across windows lived outside the repo, outside the pack,
   outside every backup. Machine loss or account action = total amnesia on
   top of seat loss. FIXED: mirrored byte-faithful to
   memory/continuity/seat_memory_20260927/ (now git-tracked, now in the
   next pack). Future policy: the mirror refreshes at window close, same
   discipline as the state snapshot.
2. **The frozen handoff spec didn't know today existed.** Its STATE section
   ended 09-26; a cold window booting after a seat loss would read a stale
   world. FIXED: STATE block prepended with the full day (gate fix, chain
   race cure, ablations, burn-down score, drills, laws) + pointers to the
   four close receipts.

## MISSED — operator actions, ranked by blast radius

3. **The encrypted pack's key is single-copy on this machine.** The 1.59GB
   ESSENTIALS_PACK (your whole-estate backup) is AES-locked by a key that
   exists in exactly one place: the machine it backs up. Disk dies or
   machine is taken → the backup is a brick. ACTION: put the passphrase
   somewhere off-machine (password manager, printed in the safe, whatever
   your threat model prefers). This is the #1 miss of the audit.
4. **Same-disk "backup".** Mag-prewipe-backup-20260927.git lives on this
   physical disk. It protects against corruption and bad merges, NOT
   against the disk or the machine. The Drive bridge (fostertron junction)
   is the real off-machine copy — ACTION: verify its sync currency
   (one command on the other machine: git -C <junction> log -1 --format=%h
   and compare against 603ad91bf-or-newer).
5. **Second-machine join has never been tested.** The bridge protocol is
   written (TWO_MACHINE_SYNC_20260919.md) and the seed cold-join passed
   10/10 in a subprocess — but no second MACHINE has ever joined from the
   seed + repo alone. Until one does, "portable" is a claim, not a proof.
   ACTION: run the FIRST_BOOT steps on the other box once (30 minutes).
6. **xAI rotation is STILL open** (flagged all day; the live key rides
   9+ history copies and the gate hole that hid it is now closed, which
   cuts both ways). Rotate-then-purge remains the order.
7. **Provider-key geography.** Live keys sit in .env, hermes .env
   (%LOCALAPPDATA%), providers.yaml — the repo copies are untracked (right)
   and the encrypted pack carries the estate (right) — but the hermes-side
   keys predate the pack protocol. ACTION, small: confirm the pack's
   ACCOUNTS.md coverage includes the hermes .env entries, or add them.

## Checked and sound (so you know what NOT to worry about)

- Cold reconstruction: seed-mcp 10/10 join pass on real bytes; seed file
  09-26-fresh, regeneration is one command (tools/seed_rib.py) whenever
  wanted — record delta since is receipts, which the chain holds anyway.
- Fleet tasks: all 13 registrations rebuild from scripts/register_*.ps1.
- The record: append-only, hash-chained, verified clean today end-to-end.
- The laws: everything a successor needs to behave correctly is codified
  (AGENTS.md + law registry + today's additions), not口头.

## The honest bottom line

We missed exactly what the village missed: the thing closest to us. The
memory layer and the pack key were load-bearing and invisible. As of this
pass, the claim "take the seat, the estate survives" is true for seat, model,
and account. For MACHINE, it's true the moment actions 3-5 land — and they
are thirty minutes of your hands, not mine.
