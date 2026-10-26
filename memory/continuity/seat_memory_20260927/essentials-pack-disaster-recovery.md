---
name: essentials-pack-disaster-recovery
description: Encrypted essentials pack built 9/26 (the only real off-machine
  backup); key custody law; hard finding that no cloud bridge existed before
  this
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

HARD FINDING 2026-09-26: before this day the fleet had NO off-machine backup.
The `local` backup remote is a bare repo on the same physical disk, and the
TWO_MACHINE_SYNC_20260919 Drive-junction protocol was never executed on this
host (no junction, no Drive client). Operator: "so much on dish that just
vanishes when we lose the computer and i have no money to replace it."

Built in response: `watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc` —
AES-256 + PBKDF2, passphrase at `configs/secrets/pack_key.txt` (gitignored),
passphrase handed to operator in chat for his password manager / phone.
Selection: code + configs + .env + docs + ledgers + memory canon + vault +
watch/inbox receipts + seed zip; excludes .git (7.4G), .venv, .mimosa,
memory/ghost, biography backups, memory/runs, media corpora, mrpool media
(ledger kept), per-file cap 80M. Restore recipe: `watch/inbox/ESSENTIALS_RESTORE.md`.
Seven-day recap travels inside the pack (`watch/inbox/RECAP_7D_20260926.md`).

**Why:** fidelity layering — the encrypted pack is the survives-everything
layer; the Drive whole-folder mirror (when the operator fires bridge card
[[queue B2-42]]) is the byte-identical layer including .git history.

**How to apply:** refresh weekly (Sunday cron recipe in ESSENTIALS_RESTORE.md;
arming blocked from the burn session by one-automation limit, brief B2-44).
Key custody: password manager first, paper second; chat transcript never the
only copy. Any pack must verify roundtrip (decrypt | tar -t count == list
count) before claiming done. AUDIT RE-FLAG 9/27
([[preparedness-audit-20260927]]): the preparedness pass ranked key custody
confirmation the #1 operator action — verify the passphrase actually landed
off-machine, don't assume the chat handoff stuck. Related:
[[two-machine-drive-bridge-20260919]], [[seed-3-2-0-public-pack-20260925]].
