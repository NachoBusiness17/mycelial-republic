# STEAL — VerkleLance: deterministic knot-lattice intelligence (2026-08-11)

Operator: "we need a verkle lance like pylance so we can use our determinism to map to events tying
them together temporally."

## STEAL ANALYSIS
- SELF: ghostlance (ghost_pylance) = deterministic code-intelligence; ghost_memlance = deterministic
  memory-state selection. verkle_lance = the SAME shape over the VERKLE KNOT CHAIN.
- The determinism IS the temporal map: each chain row has index (position), parent_verkle_root (merkle
  root of all prior) and verkle_root (root up to this). A knot's identity = its content hash; its PLACE =
  the chain of roots that produced it. Events map to knots by session_id/theme/time; roots tie them
  together temporally (parent→child, turtles all the way down).

## Built: mag/verkle_lance.py (verkle_lance.v1, $0, stdlib-only)
- index()      — the knot chain in temporal order (session_id, ts, theme, leaf_hash, parent/root).
- temporal()   — timeline: ordered knots + parent→child root linkage + root deltas.
- trace(key)   — map an event/key to its knot(s) + place (parent/child neighbours).
- link(event)  — tie an event temporally: knot at/before its time, the root that anchors it.
- verify(key)  — content-addressed verdict (in chain? valid hash? root at point? tip root?).
- self_check() — chain consistency: n leaves, tip root valid, order monotonic, orphans.

## Verified (via OUR headless runner, ghostlance surface)
- ghostlance diagnose: syntax_ok, no real errors.
- self_check: 1009 knots, tip_root valid, order_monotonic:true, orphans 0, all content-addressed.
- temporal: genesis (index 0, 04:41Z) → tip (index 1008, 09:50Z). 
- trace('mem_lands'): our MemLands flows ARE chain knots (work:mem_lands:...), parent→child linked —
  the tip knot is a mem_lands flow. Determinism maps events→knots and ties them temporally.
- verify('stateless'): content_addressed:true, in chain, root_at_point matches.

## Lesson / law
- The determinism (content-addressing + chain index) IS the temporal tie — no timestamps needed beyond
  the hash chain. This makes the lattice auditable + replayable (event-sourced).
- Registered as ghost_server RESOURCE memory/verkle.
