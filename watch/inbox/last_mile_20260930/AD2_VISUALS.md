# AD2 — destruction visual grammar (2026-09-30)

Lane: AD2. Files owned and changed: `roblox_to_godot/systems/water_particles.gd`
(event parsing, registries, emitters, crack decals, steam column) and
`roblox_to_godot/scripts/game.gd` (broken pipe stubs, crest-dot dim overlay).
`water_graph.gd` / `water_graph.py`: NOT touched (AD1's ownership, held).

## What was built (AC2 sections 1-3 + 5)

1. **STARVED** — `"Junction X STARVED: ..."` (both grammar shapes): amber pulse
   ring (`STARVE_RING`, radius breathing off `sim_clock` through the 64-entry
   sine table, phase from `hash(node)`) + dust tint circle on the gated node,
   both fading over `STARVE_LIFE` 2.2s; droplet trickle emitter at the waste
   basin parsed from the event tail (`" spilled to waste at <basin>"` — the
   `"held at the junction"` shape has no basin and no trickle).
2. **Siphon break** — `"Siphon X breaks (intake dry)."`: shrinking ring at the
   src pool (negative-growth splash, r 30->6), crest-dot dim envelope
   (`siphon_dim`, bright->dark fade 1.1s drawn in game.gd over the already-dark
   unprimed dot), and every live droplet inside the corridor (r 20) kicked
   toward dst (`SIPHON_KICK` 130 px/s, proximity-scaled).
3. **Boil steam column** — pale droplets (`STEAM_COL`) launched upward
   (`STEAM_RISE` 55 px/s + `STEAM_BUOY` 70 px/s^2) at any node with
   `steam > 0`, rate `STEAM_RATE` 16/s per steam unit; reads graph state (not
   events), so the column lives exactly the boil->condense window; buoyant
   droplets are exempt from the pool-gather pull so the column leaves its pool.
4. **Fracture** — `"Pipe X FRACTURES (stress N): spray to Y."` (AD1's engine
   emits this exact grammar; verified 1 occurrence in water_graph.gd):
   idempotent fracture registry keyed by pipe name with hash-fixed fracture
   point t in [0.35, 0.65], gap `min(8+2*stress, 16)`; persistent spray emitter
   aimed at Y (`FRACTURE_RATE` 2.5/s scaling with stress, hash-jittered spread
   +-0.4 rad); crack decal = jagged `draw_polyline` (8 points, jitter from
   `_unit(hash(pipe)+i*prime)`, byte-stable frame to frame); game.gd renders
   the pipe as two stubs with the gap in cold dead steel. Re-parse-safe (feed
   cursor replays up to 3 tail events); unknown pipes/targets rejected silently.

Zero RNG everywhere: all jitter/phase/rate-spread via the existing `_unit`
hash-sine idiom and `sim_time` bases. No wall clock.

## Design-doc gap

`watch/inbox/last_mile_20260930/AC2_DESIGN.md` does not exist on disk (repo-wide
find + content grep). Grammar built from the mission's quoted event strings,
which match AD1's landed engine grammar byte-for-byte. Flag for the operator:
the design doc AC2 cites was never landed by its owner.

## Verification (byte-run, Godot 4.3 console exe, headless)

- `--check-only --script` water_particles.gd: exit 0, no errors.
- `--check-only --script` game.gd: exit 0, no errors.
- Throwaway probe (V4 run-then-delete idiom, `ad2_probe.gd`, FakeGraph host
  to stay off the sibling's in-flight engine file; deleted after):
  **9/9 PASS** — starved marks x2, basin trickle parsed, dim armed, fracture
  fields (t band / gap 16 / stress 5), re-parse idempotent + unknown-pipe
  reject, steam column alive+upward (7 droplets), persistent spray (140
  droplets), decay windows closed, fracture persistent. Exit 0.
- Canonical smoke lane, final bytes: `--headless --path roblox_to_godot
  --quit-after 60` -> exit 0, BANNER ONLY, zero script errors; `--quit-after
  300` -> exit 0, banner only, zero errors. T/H/authoritative stages skipped
  per mission (sibling mid-engine-edit).

## Sibling incident (evidence, not blame)

During this lane's verify window AD1 landed water_graph.gd (07:16:59 EDT) in a
momentarily unparseable state — tab-indented new statics on the space-indented
file, `Parse Error: Used space character for indentation instead of tab ...
at water_graph.gd:67`; HEAD's version parse-checked clean, so the breakage was
inside that diff. Never touched per ownership. The file re-parse-checked clean
on the same size/mtime before my final smokes (md5
61da178dd6257aa9888eaf1445caa535); the 60f/300f results above are against
those final bytes. No commit made (mission: no commit).
