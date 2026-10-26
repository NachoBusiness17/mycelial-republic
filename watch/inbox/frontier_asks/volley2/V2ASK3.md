# THE ASK: BUILD INSTRUCTIONS - THE PARITY DEEP CUTS (Q14+Q15+Q16)

Context in V2CTX.md one directory up. Three questions from the 52-question
inventory:

- Q14: the flock exists in FOUR implementations (Luau, JS, GDScript, numpy)
  with no cross-implementation harness. The rule_parity.py pattern (seeded
  JSON inputs, per-tick state-hash, headless Godot runner) already proved
  the water engine's twins diverge and fixed them. Ask: the minimal harness
  for the flock - which two implementations to pair first, the seeded-frame
  format, the position-compare law (float tolerance vs exact-hash), and
  the test that proves the harness itself is faithful.

- Q15: live constant drift INSIDE one language: flock.gd FLEE_RADIUS=20.0
  (a later lane's tuning push) while fish_brain.gd still reads
  FLEE_RADIUS=14.0 - the same disease the water twins had, within one
  GDScript tree. Ask: the single-source-of-truth design for shared game
  constants in Godot (autoload singleton vs generated const file vs
  test-pinned), with the migration path that never breaks a running game.

- Q16: Python ints unbounded, GDScript 64-bit; volume * DEPTH_SCALE can
  cross 2^63 on stress boards (depth = volume * 1000 / cross_section).
  Ask: the integer-domain policy for the twin engines (saturation
  semantics, the overflow test family, where divergence is acceptable
  vs must-match) given the estate's determinism law.

Deliver: buildable specs + falsifiers. Tag [public]/[ference] or
[inference]. 1200-2500 words.
