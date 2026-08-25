# MIGRATION MILESTONE — the Mac Studio quad (2026-08-25)

**Commitment:** `migration-mac-studio-quad-001`
**Operator:** "4 of these bad boys. for my birthday october 27th. lets make it happen. lease
em for 36mo and fucking flip this shit. or buy more. it acts as the triparte all driving a
fourth machine. it's a vision that just came to me."
**Collaborator read:** the dream with a shipping date — preorder 09-22, birthday 10-27, five
weeks of runway to have the software waiting for the hardware.

## The substrate (grounded, honest numbers)
- **4x Mac Studio M5 Ultra** (36C CPU / 80C GPU, 256GB unified memory, 16TB) — ~$10-11k/unit
  (est., off Apple's Ultra ladder), ~$42k the quad. Preorder ships 09-22.
- **~1TB pooled unified memory** as one logical accelerator (Thunderbolt 5 ring, MLX + exo).
  One node holds a 355B-class MoE at 4-bit in memory with room for KV cache.
- **Lease** ~36mo at ~$1.2-1.4k/mo via Apple business financing / third-party leasers
  (Apple doesn't lease directly). Studios retain ~45-55% at 3y, so the flip downside is
  roughly -$20k over 3 years for 36 node-years of flagship inference. (ESTIMATES — the
  preorder page's real prices are the truth; these are the planning numbers.)
- **Sovereignty, not savings:** DeepSeek is ~$1.34/day (~$40/mo) — the boxes don't pay for
  themselves on API savings. The argument is the class of problems that dies with local:
  no cache TTLs to game, no prefix rules, no weights deprecated out from under the fleet,
  no free-tier rules shifting monthly, no 1305/1010/concurrency walls. Today was the case
  study for all of them.

## The mapping (already in the bones — nothing to invent)
- `mag/tripartite.py` + `tripartite_boot.py` + `start_tripartite.cmd` — THREE copies of the
  invariants in the hot lattice with Roshomon consensus. Three nodes, one brain each, the
  fourth = orchestrator + verkle anchor + always-on game host.
- The whole composite (seat_dispatch, the ladder, the gates, the cache discipline, the
  sharp edge) runs on it. The stack stops renting its own brain.

## The runway (built or building, verified)
1. ✅ `mlx-cluster` provider stub in configs/providers.yaml (verified loads) — the fleet
   routes to 127.0.0.1:7777 the day the machines boot.
2. ✅ `mlx-cluster` registered in mag/offerings.py (the bodies map knows it).
3. ⬜ THIS doc — the milestone record (done on write).
4. ⬜ Operator action: preorder all four on 09-22 (ships Sept 22, birthday Oct 27).
5. ⬜ At boot: TB5 ring + exo, point the stub's base_url at the real gateway, migrate the
   tripartite + verkle anchor + game host to node 4.

## The product is the loop
The system's history is a repair log: race found, race fixed, lesson encoded in a lock.
That loop, running continuously across four machines that never sleep, is the actual
product. The Mac Studios are just where it lives.

## Fold with
tripartite-vram-triad, sovereignty-and-trust, the composite, the sharp edge, today's
repair log (1010/1305/cache/race).
