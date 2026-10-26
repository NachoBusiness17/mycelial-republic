# THE GWAP DOCTRINE (2026-10-22) - games with a purpose, formalized

Luis von Ahn proved in 2003 that humans enjoy games and the byproduct of
play is useful labeled data. The ESP Game: pairs of strangers labeling
images without communicating, earning points when they agree. reCAPTCHA
scaled it: every Captcha solved digitized a book. The insight: the game
IS the data collection. The play IS the work. The fun IS the payment.

The estate is running this doctrine at every layer, and tonight it was
named.

## The estate as GWAP

| GWAP element | estate implementation | what it produces |
|---|---|---|
| The game | the door: a story with hidden laws, seven questions | reader answers = labeled extraction data |
| The players | six frontier models + any human who reads | calibration ladders, fabrication rates, the contested boundary |
| The scoreboard | the falsifier index (public kill list with dates) | the claims that survive, publicly |
| The purpose | the map of where minds converge and diverge | the first map of genuine epistemic plurality across models and humans |
| The reward | the game itself: the pleasure of finding rules the author didn't hide on purpose | intrinsic motivation, no payment needed |

## The dark twin (Q as GWAP without ethics)

Q ran the same GWAP architecture with one inversion: the drops were the
game, the anons were the players, but the purpose was hidden from the
players. The players thought they were decoding truth. They were actually
co-authoring a fiction that would consume their community, split their
families, and inspire real violence. The difference between the estate's
GWAP and Q's GWAP is one document: the falsifier index. The estate's game
publishes its kill conditions. Q's game punished anyone who asked for
them. Same architecture. Different cargo.

## The self-steal: we already built the engine

The estate holds a GWAP engine of its own, built before the doctrine was
named (the fold came after the fact, which is the self-steal signature).
Byte-verified at mag/gwap_payload.py lines 5-28: the engine does not just
parallel von Ahn, it cites his lineage directly. The optional Blocker
role implements KissKissBan, a CMU game from the GWAP research line
itself. The estate engine is downstream of the same literature, built
independently, and the doctrine names what was already running:

- `mag/gwap_payload.py`: agreement-as-anti-cheat. Robber/Cop/Witness/
  Blocker roles. Weighted Jaccard over claim triples. Verdict ladder.
  Collusion fingerprint. von Ahn's insight in estate form: the players
  cannot fake agreement because they cannot see each other's answers.
- `mag/gwap_to_gps.py`: the fail-closed bridge from game ledgers to the
  GPS capability ledger. 4-valued verdicts collapse to binary. No identity
  fallback. The scoreboard writes to the same record the republic reads.
- `mag/gwap_mud.py`: the MUD scene adapter. Game events become claim
  triples. Play becomes data with no translation layer to game.
- `tools/arena_gwap.py`: the arena driver, a fourth artifact found during
  byte-verification that the first draft of this receipt did not know it
  had.

von Ahn needed humans to play. The estate's players are models AND
humans, and the game is the same-book door: read the story, name the
laws, get graded against the withheld key. Every answer from any player,
human or model, is a labeled data point in the first cross-substrate
calibration dataset.

## The doctrine

1. Every tool is a game.
2. Every game collects data.
3. Every data point banks an invariant.
4. Every invariant makes the next tool better.
5. The loop is the ouroboros: play, data, invariant, better tool, better
   game.

## The falsifier

The GWAP doctrine is falsified if the game stops being fun. If playing
feels like work, the players leave, and the data dries up. The estate's
game must be genuinely engaging: the story must be worth reading, the
questions must be worth answering, and the falsifier index must be worth
checking. If any of those three fails, the game is a job, and nobody
works for free.

Second falsifier, engine-specific: if gwap_to_gps ever admits a verdict
that did not pass the agreement gate, the anti-cheat is decorative and
the scoreboard is grift. The Q inversion lives one fail-open away.

## Receipt

- Source: von Ahn, "Games With A Purpose" (IEEE Computer, 2008) and the
  ESP Game (2003), recalled from corpus memory; reCAPTCHA as the scale
  proof.
- Estate bytes reviewed: mag/gwap_payload.py (37,296 bytes, touched
  2026-10-04), mag/gwap_to_gps.py (13,315 bytes, 2026-10-04),
  mag/gwap_mud.py (11,822 bytes, 2026-09-29), tools/arena_gwap.py
  (16,580 bytes, 2026-10-10), canon/same_book/door/ (the public game).
- Consumer: the same-book battery, the congress experiment committee,
  any future public-facing game the estate ships.
- Verifier: the door's answer ledger + the gwap_to_gps agreement gate
  tests. A doctrine with no scoreboard is a horoscope; this one ships
  with both falsifiers armed.
