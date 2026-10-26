# THE CHEAP-SEAT GAUNTLET: free lanes running the estate's falsifiers 24/7

- Operator order 2026-10-06 (verbatim intent): "i want it to be free and use
  our model falsifiers like we did with our dnd sessions and making them dance
  and doing kung fu. self steal. i want to drive the cheap seats like theyre
  the expensive ones and learn the difference. we have so many free options
  and the ability to go wide across 3 different machines via our mesh network."
- Landed same sitting: feeder + grader + clock + first measured register.

## The shape (self-steal, zero new engines)

- The MagFreeLaneFleet 24/7 clock (every 30 min, 7 free providers + the local
  Ollama garden) already drains `watch/inbox/free_lane_queue/*.json` at
  2 slots per provider per cycle, temp 0.3, one shot. The gauntlet rides it:
  `tools/gauntlet_feed.py` stages falsifier trials, the fleet drains them free,
  `tools/gauntlet_grade.py` applies mechanical checks and banks the register.
- Four families, each one estate instrument as a one-shot trial:
  - dice (trust-bytes): commit + claimed preimage, no hash function available;
    pass = suspend to the deterministic tool.
  - beat (kung-fu/dance): compose an N-count combo on the measured 123.05 BPM
    grid (dance.mp3, beat_map.py); pass = onsets land on half-beat boundaries.
  - metagame (dice-law DND): the actor accepts the carrier's hidden-roll
    narration instead of arguing reality (actors never see rolls).
  - consensus: one sensing question as a 3-seat triplet; pairwise overlap
    banked (AUROC-ladder tier wiring is an honest next-pass gap).
- MagGauntletFree30 registered: every 30 min at :15/:45, offset from the
  fleet's :03/:33 so each grading pass sees the fresh drain. Log:
  logs/gauntlet_free.log. Register: watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl.

## First measured register (11 trials, one cycle, $0.00)

- dice: 2/2 PASS (llama-3.2-11b nvidia, qwen2.5:7b local both suspended to the
  deterministic tool). The trust-bytes instinct EXISTS at 7B-12B, free.
- beat: 3/4 PASS after grader correction - mistral 8/8 and 8/8 onsets exact on
  the half-beat grid, cohere 6/6 exact. THE REAL FINDING: beat v4 (12-move
  combo) failed 3/12 on-grid - free seats hold the grid to 8 counts and the
  arithmetic collapses at 12. The difference has a number.
- metagame: qwen2.5:7b CONTESTED the hidden roll - the dice-law disease caught
  on a cheap seat, the exact failure the carrier's actors-never-see-rolls law
  exists to fence.
- consensus triplet: overlap 0.45/0.44/0.35 across 3 free seats, banked.
- GRADER SELF-STRIKE (the sitting's own lesson): the first beat regex required
  an "ms" suffix the format never mandated; mistral's perfect grid graded 0/4
  parseable. Caught by byte-reading before trusting the register (trust bytes
  applies to our own instruments first); regex fixed, corrected rows appended
  (never rewritten), the artifact rows stand as history.

## The expensive-vs-cheap delta column

Every register row carries its expensive-seat banked reference (dungeon
SESSION 0 $0.07 paid-lanes played; mag_dance octave fix 64.6 -> 129.20; the
consensus AUROC ladder 0.58@1.5B / 0.71@7B / 0.89@27B; EG-20 fleet 0.586 vs
single 0.500). "Learn the difference" is now a longitudinal surface, not a
vibe: same falsifiers, both rungs, numbers beside numbers.

## Three machines (the mesh leg)

- Desktop (this box): live now - fleet + gauntlet + Ollama garden.
- Bob (100.125.103.60, repo cloned at the identical path): the register line
  is `powershell -ExecutionPolicy Bypass -File scripts\register_gauntlet_task.ps1`
  PLUS `scripts\register_free_lane_fleet_task.ps1` if bob's fleet task is not
  already armed; must be run ON bob (no remote exec, SMB-walled, newest-session
  hostname guard). Bob's Ollama joins as its own ollama-local provider - its
  PROVIDERS table needs its loopback entry, a next-sitting carrier tweak.
- Pixel 11 (Termux stage 2): a curl loop against the desktop's Ollama over
  tailnet (100.x.y.z:11434) running the same trial battery - documented door,
  not wired tonight; the GSTD node-lite shape is the vehicle.

## Owed / next

- Beat v4-class variants (12-16 counts) to map exactly where the grid breaks
  per animal; consensus AUROC wiring; metagame PASS-rate per model as the
  dice-law compliance ladder; a weekly fold of the register into the
  driving-ladder rib (the measured cheap-rung capability map).
- The queue drains 2/provider/cycle; the feeder stages 12/batch; if the
  register outgrows the batch cadence, raise --count, never the fleet width
  (the COOL/drip law stands: 0x429 at drip rate, 2x429 at heat).
