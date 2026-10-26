# Phase 1 attack (a) — state-sync-not-lockstep for the water sim (P4)

Date: 2026-10-20 · Attacker: Beam/DeepSeek (free lane) · Target: ROUTE_V0.md §P4 + §1 thesis · Lane: provider-chat, read-only.
Source of truth: ROUTE_V0.md as written 2026-09-30. No code was run; this is a doc-level adversarial read.

## Attack

1. **Per-tick state size unknown.** The route cites Quake 3/Valve lineage and asserts snapshot+delta suffices, but never quantifies water board state (grid cells x fields x precision x tickrate). At LAN tickrates (60-128 Hz) a fine water grid can exceed bandwidth. The claim needs a measured byte budget, not a lineage citation. (Unproven — no measurement exists in the route.)

2. **Falsifying measurement.** Instrument per-tick delta size and peak snapshot size under worst-case water activity (many simultaneous disturbances), then compare against LAN bandwidth headroom at target tickrate. If deltas exceed budget or diverge from client-side prediction, "snapshot+delta suffices" is falsified.

3. **Honest fallback.** Interest management (spatial culling of water regions per client) plus baseline/keyframe deltas with delta compression; if still too large, reduce simulation fidelity or tickrate for water specifically — not lockstep, which the route correctly rejects for continuous state-heavy physics.

## Verdict

- Assumption (a) is currently Unproven: the lineage is sound (Fiedler correctly rejects lockstep for continuous physics), but the sufficiency claim has no measurement behind it. The route's own ATTACK SURFACE names this; this attack confirms it and prescribes the measurement.

## Amendment proposed (for ROUTE_V1)

- Add a pre-P4 measurement gate: instrument one water-board session's per-tick delta and peak snapshot BEFORE building the transport. If it exceeds budget, interest management becomes a P4 sub-pitch, not a fallback.
