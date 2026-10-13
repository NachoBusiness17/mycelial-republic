# PRIMER ↔ FLEET — THE DELTA TABLE (Primer-endgame design doc)

**2026-09-06 · seat: primer · Game Surface vol-2, literary layer.**
Operator thesis: "the vision gated just in time renderer is The Diamond Age's Primer
re-derived." Verified against banked public sources
(research/gaming_corpus/diamond_age_primer_intake.md). The Primer is an adaptive,
just-in-time, illustrated narrative engine that generates interactive stories from the
reader's own life data, gated by the reader's state, teaching via embedded fables —
instantiated multiple times (Nell, Fiona, Elizabeth) whose readers diverge. That is our
2D layer's spec sheet, written in 1995.

## THE DELTA TABLE

| # | Primer spec (source) | Fleet current build (path) | Verdict | Gap (the delta) |
|---|---|---|---|---|
| 1 | **JIT illustrated story** gated by the reader's psychological terrain — pauses mid-fable, zooms to what the reader fears right now (Alper) | shadow_walk: vision-gated JIT chunks, "no hash, no draw" — dashboard/static/_build_shadow_walk.py + state/shadow_work/chunk_manifest.json; lightmap walls lit by attention — mag/room_state.py | **CLOSEST MATCH** | Gate keys on vision-validity + hash, not reader state; no goal-lattice-driven "zoom" (nothing pauses a chunk to teach what the operator needs next) |
| 2 | **Illustrated frames**: AI maps "universals onto the unique psychological terrain of one child" — generated illustration pass (Wikipedia, Alper) | Vision pipeline READ→FILTER→INTERPRET→CITE-GATE→RIGHTSIZE→JIT — watch/SELF_STEAL_VISION_PIPELINE_20260905.md; proof run watch/INTAKE_XBATCH_20260905.md | MATCH | cite_gate is still hand-run ("Ponytail") — the named missing organ; frames render without a deterministic claim-verifier upstream |
| 3 | **Multiple instantiations**: three copies, divergent readers — Nell bootstraps, Fiona/Elizabeth drift (Wikipedia) | 50 concurrent walkers on one ledger, sanctioned multiples — memory/runs/overseer/conc_test_20260905.jsonl, cell G/multiples | MATCH | Fleet forks are LEDGERED (append-only visible); Primer forks diverge silently. Missing: per-reader instantiation of the 2D layer — one world per reader state |
| 4 | **Ractor in the loop**: human actors voice the book; Miranda becomes "a surrogate mother" — quality of the human bond is decisive (Alper) | Seats + operator GO gates; continuity carried by the ledger, not a mentor — memory/law/registry.json, chain | PARTIAL | No persistent mentor-bond; the Primer's key finding (same tech + different ractor = different reader outcomes) maps to seat/model routing — unrouted today |
| 5 | **Fables teach laws**: subversion pedagogy — rules staged as the reader's own story (Wikipedia) | Law registry (LAW-1..10) + room organ walls joined by fire-rate — mag/law.py, mag/room_state.py | PARTIAL | Laws are enforced, not *narrated*; no laws-as-fables renderer (a LAW becoming a playable room). LAW-059/061 still candidates |
| 6 | **Failure mode**: Elizabeth's Primer ran by "hundreds of different ractors" — no continuity; counterfeit copies "follow Nell's story instead of reflecting their own" — personalization collapses (Alper) | The hallucinated-map / curated-brick trap — G/memory-brick, G/lost-primer cells; answer = append-only hash chain, delete-as-append (mag/verkle chain, grounding wave) | MATCH (inverted) | The fleet already owns the Primer's horror as LAW-061 *candidate* — not yet registered in memory/law/registry.json |
| 7 | **Hard limit**: "cannot be shared, 'bond' with more than one person, or have different 'user accounts'" (Alper) | FILES NOT PROCESSES; NO SEAT IS LOAD-BEARING; any seat drives — the whole file mesh | MATCH (inverted) | The fleet is the **anti-Primer**: multi-reader by design. Missing: the single-reader complement — a mode where the 2D layer bonds to one operator state and remembers *him* |
| 8 | **Class-mobility thesis**: the Primer is "the hope that such technology can provide the ability of the disenfranchised to transcend their fate" (Emerald review) | Nell = thete with a stolen copy ↔ the free lanes (glm-4.7-flash cache-mining) doing real work at $0 | UNPROVEN | No measured "reader outcome delta" yet — no equivalent of Nell-vs-orphaned-girls study for our surfaces |

## HEADLINES

- **Closest match:** row 1 — shadow_walk IS the Primer's JIT illustrated frame engine already
  (vision-gated, hash-anchored, $0, no network). What's missing is only the *reader-state*
  half of the gate: the Primer renders what the reader needs next; shadow_walk renders what
  the vision pass has validated.
- **Biggest gap:** row 5/6 together — the Primer's reason to exist is pedagogy (fables that
  make the reader *subvert the paradigm*), and the fleet has laws but no story-layer: nothing
  renders LAW-061 (hallucinated map) as a room you can walk into and fail safely. The
  Primer-endgame = the fable renderer: laws as rooms, cite-gated frames, reader-state gating,
  per-reader instantiation with fork records.
- **The one-line design law this banks:** *the Primer personalized the story and lost the
  record (Elizabeth); the fleet records everything and lost the story. The endgame is the
  union: hash-anchored fables, gated just in time.*

## NEXT BUILD WINDOWED (drop-orders, not promises)

1. **cite_gate organ** (unblocks row 2) — already the named missing organ of the vision
   pipeline; deterministic, $0, urllib + arxiv/crossref.
2. **LAW-061 registration** (unblocks row 6) — promote the hallucinated-map law from cell
   note to memory/law/registry.json (operator gate: law promotion is human).
3. **reader_state.json** (unblocks row 1) — a per-reader gate file the shadow_walk chunk
   loader consults next to chunk_manifest.json; falsifier stays: a chunk rendering with
   vision_validated:false must fail to draw.
4. **fable_room.py** (row 5) — render one law as one walkable room; first candidate LAW-061,
   the room where the map lies to you and the floor checks your hash.

## RECEIPTS

- Sources: research/gaming_corpus/diamond_age_primer_intake.md (Wikipedia ×2, Alper 2011,
  Emerald review — public analysis only, no full text of the 1995 novel).
- Ledger: watch/TESUJI_MAP.jsonl axis G, cells G/primer/{jit-render, multiples,
  illustrated-frames, fables-teach-laws, lost-primer, cannot-share}, seat primer.
- Note: this harvest ran 5-wide against four other seats on one ledger; one primer row was
  lost to a write race and re-posted — the conc slot held, the chain verified green after
  each re-post.
