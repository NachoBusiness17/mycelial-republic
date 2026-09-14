# THE KABUKI STACK — ocean model + synthesis ractor (build card, 2026-09-05)

Operator, after ranking the personalities (Elder first; Lessig/Ponytail close second;
Economist okay): "we really need to give these things more of an ocean model and a ractor
on top so we can perfect the voice and synthesis of the kabuki."

## THE DIAGNOSIS (why the kabuki sometimes reads thin)
A personality today = one brief file + whatever context the spawning window pastes in.
That's a mask, not a person: no shelf, no memory, no era. The voice lands (Elder) only
where the seat behind it happens to hold the ocean. The fix is not better masks — it is
DEPTH UNDER EVERY MASK plus ONE VOICE ABOVE THEM.

## THE BUILD (two layers)

### Layer 1 — THE OCEAN (per-personality context pack, auto-assembled)
Extend `mag/context_pack.py` with a `personality` mode. For any chair X, the pack =
1. chair brief (docs/ref/ractors/X.md) — the lens,
2. shelf digest (the X-adjacent corpus shelf, TRAINING_INDEX routing) — the reading,
3. zeitgeist era-003 excerpt (already wired) — the era,
4. last 3 canon rows + last panel fold citing X — the live memory,
5. the operator-model excerpt (seat-digest lineage) — whose man he's speaking to.
Budget ~2K tokens. Deterministic. One function: `ocean_pack("WALLAS") -> str`.

### Layer 2 — THE CONDUCTOR (synthesis ractor on top)
The Elder seat role, formalized as a chair: after any panel/salon/multi-voice run, ONE
synthesis pass merges the voices — keeps disagreements as findings, drops duplicated
emphasis (duplication is emphasis per the trajectory lens), outputs the fleet voice.
Rector brief: docs/ref/ractors/CONDUCTOR.md (mint on first use). The conductor NEVER
outvotes the chairs — it only braids.

## THE KABUKI CONTRACT (voice law, three lines)
Every personality speaks from its ocean; the conductor braids; the operator hears one
voice that knows it is many.

## RANKING RECEIPT (2026-09-05, operator)
Elder #1 · Lessig/Ponytail #2 (close) · Economist okay. Feed into every spawn prompt:
Lessig = code-is-law framing (architecture over willpower — already the fleet's spine);
Ponytail = the operator's own register (see operator-model digest).

## FIRST DOGFOOD
PANEL-2's fold (tonight) IS the conductor prototype: 5 chairs → one braided fold. If the
fold reads as one voice that knows it is five, the stack works; if it reads as a
committee, Layer 2 needs the ocean packs first. Falsifier: operator reads the fold blind
and names which chairs spoke without re-reading — if he can't tell, the braid is real.
