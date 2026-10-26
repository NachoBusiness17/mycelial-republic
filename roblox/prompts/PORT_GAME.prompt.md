# PORT_GAME.prompt.md — fleet game → Roblox Luau

The prompt shape behind the THE MOUNTAIN ports. Read the actual source
first; ports are ports, not inventions.

---

You are porting a proven game to Roblox Luau. The source is the truth; you
translate mechanics, you do not redesign them.

## INPUT (read before writing anything)

- Source file(s): {{PATHS}} (read them; the mechanics live in their constants)
- Target zone spec: {{ZONE}} (position, size, monetization SKUs available)

## CONTRACT

1. Output sections, fixed: `## Mechanic Table` (source mechanic → exact
   source number → Luau home) → `## Code` (per file, complete, no ellipses)
   → `## Kept Verbatim` (constants copied unchanged, listed) →
   `## Known Gaps` (what v1 does not do; honest, ≥3).
2. Never invent a source mechanic. If the source lacks it, the port lacks it.
   Line references for anything load-bearing (e.g. "spawn curve is
   `max(0.07, 0.55 − 0.07·diff)/spawnMul`, swarm.html:1092").
3. Luau discipline: --!strict, no ContextActionService on the server (client
   courier → RemoteEvents → server validation), pooling over spawning for
   anything per-frame, seeded RNG (xorshift32 via SeedRng) for anything
   score-bearing, FAIL(RNG_DIVERGE) if a replay would differ.
4. Monetization hooks land as attributes + Config SKUs, id=0 until publish.
5. The room that remembers: every observed choice calls ShadowLedger.record.

## SOURCE TRUTH (quoted from the files you read)

{{PASTE the load-bearing lines/constants — if empty, go read them first}}
