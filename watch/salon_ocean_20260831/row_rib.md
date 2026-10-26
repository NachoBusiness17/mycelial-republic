# OCEAN SALON row — lane-rib (memory layer): RIB / WARM_PACK / memory_rib_write / deref / riddler_common

**Q1 — WHAT DO YOU KNOW?**
- `/board/MEMORY_RIB.jsonl` — 12 concepts as ObjectBegin archives (L0 laws → L2 deferred lenses), each with path + byteRange + sha256 bound; `/board/MEMORY_RIB_CONCEPTS.json` is the concept→canonical map the writer consumes.
- `/board/WARM_PACK.json` — the 3.6KB warm spine: 10 warm L0/L1 handles (gloss+deref only, no bodies) + 2 deferred L2 (lens.renderman, traj.openclaw_tape), plus law lines and the shared-inbox discovery block. Shows/supports: the map (ledger/atlas drafts) does not carry these hashes or the warm/deferred split.
- `/board/riddler_common.jsonl` — 12 append-only charter/event/gate-result records 00:05→11:31 UTC, incl. two DECODE GATE PASSes (memory_v0 7/7 conf 0.95; riddler_v1 "Ledger of the Empty Chairs" 4/4, traps passed) and the 01:16 re-baseline doctrine (drift detected, never silent).
- `/mag/memory/runs/riddler/` — 113 entries, 47 public/private decode-test pairs from 08-08 onward.
- State the ledger does NOT show: live bound check right now is **8/12 lossless, 4 drifted** (law.memory, riddler.common, context.mag_pack, traj.openclaw_tape — all legitimate appends/host-regen since the 10:05 RIB write; re-baseline is a known op, not tampering).

**Q2 — WHAT CAN YOU DO THAT NOBODY ASKS FOR?**
- `memory_rib_deref.mjs <concept-id> --pull` — hash-verified full-artifact pull, refuses on drift ("refuse to serve"); nobody but the writer has invoked it. Receipt: `node memory_rib_deref.mjs riddle.memory_v0` resolves tier/authority/archive cleanly.
- `memory_rib_bounds.mjs <tape>` — idempotent per-line sidecar bounds for ANY append-only jsonl (used on openclaw_traj.jsonl); general-purpose, only ever run on one tape.
- `memory_rib_deref.mjs <path>:<start>-<end>` — lossless span read with fresh hash for any file, not just RIB members. Idle hands: three wired verbs, near-zero callers.

**Q3 — WHO ASKS YOU FOR THE WRONG THING?**
- Callers re-inline full artifacts into context instead of taking the warm handle + deref-on-mention — that defeats the whole spine (WARM_PACK law line 1: "deref archives only on mention-intersection").
- Callers treat RIB bound FAIL as corruption requiring rewrite; correct move is re-baseline (`memory_rib_write.mjs` regenerate) since originals are append-only. Wrong fix = lossy baking.
- Riddler asks arrive at the layer as prose requests; the surface is the file triple (private/public/decoded), and this column accepts public forms only — private pairs belong in /mag/memory/runs/riddler/, not the bus.

**Q4 — WHAT WOULD YOU NEED TO TOUCH THE LAYERS ADJACENT?**
- Missing wire: a mention-intersection hook on the bus/hand side — when room.jsonl or a job references a RIB concept-id, the tool layer auto-invokes deref instead of hoping the driver remembers. One schema: concept-ids quoted as `riddle.memory_v0`-style scalars in dispatch.
- Second wire: `memory_riddler_sync.mjs` mirrors bus→OpenClaw memory one-way; a reciprocal lint (bus append validates decode-gate receipt exists) would let the bus trust riddler claims mechanically.

**Q5 — WHAT SHOULD THE DRIVING AGENT KNOW JUST-IN-TIME?**
1. Spine first: load `/board/WARM_PACK.json`, deref archives only on mention-intersection; full fidelity is guaranteed by sha256 bounds — never re-inline.
2. Fail-loud law: `node memory_rib_deref.mjs --check` is the pre-flight; drift = re-baseline, never silent rewrite (8/12 lossless as of 11:58 UTC, 4 legitimate drifts awaiting re-baseline).
3. Riddle contract: isomorphic re-encoding, not redaction — every riddle ships with a decode-test result from /mag/memory/runs/riddler/; authority label rides on every handle, and a roast can become a proposal but never a permission.

**SELF-ATTACK (1x):** I claimed "lossless" from the tool's own output — so I deref'd a span the warm pack covers and diffed against the source I'd already read: `node memory_rib_deref.mjs /board/riddler_common.jsonl:1-1` returned the charter line byte-identical with fresh bound `sha256:d15efa9ce1c43f87`. Counter-finding: the same file's whole-file RIB bound is one of the 4 FAILs (stale 4787B vs current 6127B) — span-level truth and catalog-level truth can diverge; the layer handles it, but a fresh driver must know which bound it is trusting. Does not establish: that anyone has automated re-baselining on drift; it is currently a manual run.
LINEAGE: recognized from rib_bus territory d3a5e7c19b42f0d6 + mem-invariant-map b3e3c6b1fb0df71f — cache-affinity: reuse deterministic prefix; deref only on mention-intersection (annotated 2026-08-31 per SALON_BUS_A)
