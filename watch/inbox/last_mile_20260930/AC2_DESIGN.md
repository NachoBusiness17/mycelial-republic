# AC2 — Mountain destruction visual design (2026-09-30)

Seat: Explore (read-only); banked to disk by orchestrator after AD2 flagged this file's absence.
Built by AD1 (physics) + AD2 (visuals) from this design; the fracture grammar quoted here is
byte-identical to what landed.

## Engine facts (as of design time)

Deterministic, integer, zero RNG; events are the render channel (`last_events` in game.gd, parsed by
water_particles.gd `_on_event`); pools/pipes drawn in game.gd `_draw()`; particles use the hash-based
sine-table idiom (`_unit`) for deterministic randomness; juice.gd adds shake/audio off events.

## The five-part design

1. **STARVED**: amber pulse ring + dust-tint on the gated node (parse "holds"/"STARVED"), droplet
   trickle ring at the waste basin (parse the "at {basin}" tail).
2. **Siphon break**: parse "breaks (intake dry)" — shrinking (implosion) ring at src, crest dot in
   game.gd `_draw` dims, droplets in corridor get a kick toward dst pool.
3. **Boil**: steam column — spawn pale droplets with upward velocity at any `n.steam > 0` node
   (client-only field term); existing STEAM_RING at crown covers condensation.
4. **Pipe fracture (new physics)**: add `stress:int` to Pipe; in `_move`, `p.stress += flow` when
   `flow == cap`; threshold = `120 + hash(pipe.name) % 240`; on exceed: `p.fractured = true,
   p.open = false`, spill this tick's flow to the lowest-elev node other than dst, emit
   `"Pipe X FRACTURES (stress N): spray to Y."`. Deterministic per pipe, no RNG.
5. **Renderer**: fracture event spawns persistent spray emitter (outward droplet velocities + crack
   decal: jagged `draw_polyline` jittered by `_unit(hash(pipe))`, rust color); pipe line renders
   broken (two stubs with gap at jitter point).

All additions additive, event-grammar-driven, one session of work. LANDED same day by AD1+AD2.
