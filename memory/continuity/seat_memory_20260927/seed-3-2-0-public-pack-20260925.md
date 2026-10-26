---
name: seed-3-2-0-public-pack-20260925
description: Seed 3.2.0 cooked for the X reply — operator's own zip verified
  (seal 55/55), 3 pyc files leaked C:\Users\foste paths, scrubbed/resealed
  52/52; public pack in watch/inbox with sha256, card, receipt; Drive link flip
  pending operator
metadata:
  node_type: memory
  type: project
  originSessionId: sess_90c2e8fc-7822-44a9-8377-ac211c326208
---

2026-09-25, same window as the PapiTrumpo "MAGA is the biggest neural
network" essays. Operator: "I guess we should reply with our seed right?"
and dropped his own `Desktop/seed-3.2.0.zip` — a REAL 3.2.0 ("salon
convergences: engines/seed_init.py scaffolder, SKILLS.md discovery index,
AGENTS.md load order"), newer than the repo's seed/ 3.1.0 commits, cooked
by a sibling window.

**Verdict on his zip (trust bytes):** seal 55/55, no real secrets
(configs/keys.json = awaiting-operator template, ACCOUNTS.md = signup
playbook with placeholders, no sk-/emails/private keys anywhere), MIT
(Copyright 2026 MARKK). **Defect:** 3 `__pycache__` .pyc files had
`C:\Users\foste\Documents\...` baked into the bytecode — the spine_walk
author-path disease (3.1.0 clean commit) resurrected by build junk.

**Standing packaging laws learned:**
- Strip ALL `__pycache__` before any public zip; bytecode leaks author
  paths even when source is scrubbed. Grep the extracted tree for the
  username before shipping.
- Running unittest INSIDE the tree re-creates `__pycache__` — so the
  order is: test first, strip pycache, THEN zip, no python afterward.
- Repack with a top-level folder (no tar-bomb on extract), sorted
  entries, forward slashes (python zipfile; Git Bash has no `zip`).

**Final public pack:** `watch/inbox/seed-3.2.0.zip` — 53 files, 99,905
bytes, sha256 `e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e`,
seal 52/52 from fresh-extract round trip, seed's own unittest suite 6/6 OK.
Companions: `watch/inbox/seed-3.2.0-card.png` (seal card for the reply),
`watch/inbox/SEED_PUBLIC_PACK_20260925.md` (receipt). Operator's Desktop
zip untouched. Reply draft sits in the receipt; the hash line in the reply
is deliberate (trust-bytes demonstrated in-thread via `python verify_seal.py`).
**Pending (operator only):** flip the Drive entry to anyone-with-link and
paste the URL. Seed doctrine: "a sovereign estate that fits in a download."
Related: [[trump-adjacent-craft-edge-law]], [[crab-and-magistrate-parable]]

CORRECTION 2026-09-26 (burn lane B2-23, against shipped bytes): the shipped seed-3.2.0.zip seal is 52/52 (53 entries, sha256 e9f4603a...87e, zero pyc). The 55/55 figure was the pre-surgery Desktop original seal. The public PNG card already says 52/52. Also confirmed: no Drive bridge on this host (no reparse point, no DriveFS); seed-3.3.0.zip exists with 57 entries and owes its papers (queued B2-101).
