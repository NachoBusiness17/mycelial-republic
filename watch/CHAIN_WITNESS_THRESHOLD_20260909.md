# CHAIN WITNESS — THRESHOLD 衡门 (2026-09-09 ~01:1xZ)

**Ask:** operator — "Socratically tease out what we should do from the ractors."
**Method:** three Socratic rounds in the tavern (mag/tavern_chat.py, persistent
sessions, flash lane, $0), one question per round, next question aimed at the
contradiction. Room: watch/tavern/room_2026-09-08.md, 00:57–01:01Z.

## The arc
- **Q1 (the criterion):** one thing true by Sep-20 that isn't true today + who
  outside could check it. Split: mengxi/fen/gopher named internal reconciliation
  (zero orphans, 12 knots healing); tesla named a live demonstration; edison named
  the tesuji falsifier numbers (200 cells, rotation ≥80, shadow ≥80, predictive ≥70).
- **Q2 (the cut):** a reconciled chain proves the PAST was honest — it doesn't make
  a stranger ABLE to check. Name the door. Convergence: the door exists
  (ractor.html + chain file) but is UNLABELED, has NO HANDLE, and can't be locked
  from outside (edison: the sign; gopher: the "start here" file; mengxi: embedded
  live verifier; fen: the receipt index; tesla: build the whole page).
- **Q3 (the convergence):** ONE build, named from five sides — Threshold (mengxi),
  chain_witness.html (fen), witness.html (edison), the verification circuit
  (tesla), chain-door (gopher). First screen: root + one row + the command +
  MATCH/MISMATCH. Falsifier: stranger with zero context verifies the root in
  <10 min trusting no voice in the room.

This is the gap-probe's #1 finding (cold-start witness) re-derived independently
by the cast — the ractors found the stranger-door on their own.

## The build (shipped this turn, per LAUNCH LAW amendment 5)
- `dashboard/static/chain_witness.html` — THRESHOLD. First screen: published root,
  rows/leaves, tip leaf_hash + knot file + dossier_commit, snapshot build time.
  Section 2: in-browser fold (pure-JS SHA-256, no secure-context dependency — works
  over tailscale/cloudflared doors). Section 3: the stranger's python snippet
  against the real file. Section 4: where the proofs live + honest open wire.
  Standard kit: error-trap-to-title, boot-proof fetch (3s timeout, fallback text).
- `mag/witness_snapshot.py` — regenerates `dashboard/static/witness_snapshot.json`
  (502KB, 7,377 leaf hashes + tip). REFUSES to emit if the fold ≠ published root.
- Nav: registered in index.html VISUALS at the top, plus 10 unregistered night
  rooms from 09-07/09-08 (pipeline, radar, rings, universe_within, verkle_pyramid,
  chaos_refract, wipeout_v2/sunset, tavern_brawl, pong) — nav debt swept.

## What is verified (receipts)
- Root fold MATCH, three independent paths: `mag.verkle_knot._merkle_root` over all
  7,377 rows = 8bd588968c0bbfaf… = published tip verkle_root; the page's own JS
  sha256+fold (KAT PASS, body-identity PASS vs static copy) = MATCH in 93ms;
  the printed CLI snippet = MATCH, full root.
- Fold rule read from bytes: `sha256("node:" + left + ":" + right)`, hex as ASCII,
  odd layers duplicate their last node (mag/verkle_knot.py:147).
- Trap caught in build: my first fold re-implementation used bytes.fromhex — wrong.
  Fixed by importing the real fold as single source of truth. Meet at the bytes.

## What this door does NOT claim (honest limits)
- **OPEN WIRE:** per-knot `knot.json file → leaf_hash` does not reproduce from the
  stored file alone (tried: minus-leaf_hash canonical dumps; raw file sha256 — both
  mismatch). Parked for forensics; the page says so on its face.
- Root is as-of-snapshot; regen command is on the page. Chain last knot 09-06
  (knot-at-close cadence).
- Door is loopback like everything else — exposure (tailscale/cloudflared/Access)
  stays an operator gate.

## Falsifier status
F-WITNESS-1: a stranger with zero context, <10 min, no trust: PASSES today via
section 3 (CLI) and section 2 (in-browser). Sep-20 wall: the door exists.
