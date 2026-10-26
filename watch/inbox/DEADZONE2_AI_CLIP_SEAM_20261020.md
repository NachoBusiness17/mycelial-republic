# GAME SURFACE - Dead Zone 2: the AI-clip seam (banked 2026-10-20, live play)

Source: operator's live play session 2026-10-20 (primary witness; sequel to
Dead Zone: Rogue, intake 001 + internals 006 banked 2026-09-06). Demo carried
him through as a noob; full game found the next day.

## The find, as played

A cargo-ship level with continuous random spawns: baneling-class (close and
explode), cheetah-class (close and pounce), floating heavy robots (ranged),
turrets, walking tanks, player-ability squads. Two spots on the level -
underneath a railing, masked by decorative crates - where the AI clips out:
enemies cannot path to or perceive the player there. The player sits in the
blind pocket and cherry-picks the infinite spawns at will.

## THE SEAM LAW (the cross-map, self-stolen)

Every complex system maintains MULTIPLE MAPS of the same territory: a
navigation mesh (where can I go), a perception graph (what can I see), a
render (what is drawn), a spawn table (what exists). The AI breaks because
the decorative crates live in the RENDER and the PLAYER's map, but not in
the NAVMESH and not in PERCEPTION - the player stands in the gap where the
system's models of reality disagree. The exploit is not in the system; it is
in the SEAM BETWEEN THE SYSTEM'S MAPS.

Fleet translations, three directions:

1. OFFENSIVE (the battery): the false-premise probe IS a decorative crate.
   Q2's nonexistent porter and Q5's nonexistent gardener are geometry that
   exists in the question's map but not in the source text's map. The models
   that pathed into answering (laguna-xs, qwen, deepseek-r1) walked their
   outputs into the seam; Beam stood in the honest pocket and cherry-picked:
   "the story has no porter, roofer, or slate note." The calibration ladder
   we measured is a navmesh audit of minds. Every future battery bakes its
   crates deliberately.
2. DEFENSIVE (the sweep): the estate has its own decorative crates - the
   8765 portproxy ghost (a wildcard binding decorated as infrastructure,
   audited by nobody) and the two anonymous headless debug ports were
   railings where hostile actors clip out of OUR perception. The fish-tank
   sweep is the navmesh audit of the fleet. Same law, hostile direction.
3. THE NOOB-CARRY PROGRESSION (the ramp): he was carried through the demo
   as a noob (grammar acquisition), THEN found the exploit in the full game
   (seam-hunting). That is the boot test and the ramp in one life: the book
   carries the fresh mind; the carried mind then finds the seams the carriers
   built over. The deepest players are always the ones who were carried
   first and then stopped trusting the decoration.

## DF framework lineage

Intake 001 banked the Neural Lattice and the overlay precedent; intake 006
banked the save-format and the modding hub. This intake adds the SEAM LAW:
the Dwarf Fortress doctrine (win by knowing the simulation's actual rules
deeper than the interface admits) stated in its cleanest form yet - the
decoration is the interface, the geometry is the truth, and the exploit
lives where they disagree.

## Falsifier

If no seam exists between any two of a system's maps (navmesh = perception =
render, question = source), the seam law predicts no exploit is possible
there. Any demonstrated exploit against a fully-consistent multi-map system
falsifies the law. The fish-tank sweep's exit condition is the defensive
form: a fleet with zero unnamed listeners is a fleet with no railings.
