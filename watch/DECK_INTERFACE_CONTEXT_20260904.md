# DECK INTERFACE SALON — CONTEXT BRIEF (2026-09-04)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the deck interface is live and the fleet's economics are receipted (32.26M tok $0 night, 27.85 req/s sustained lane, 108 cards/2 nights) — SUPPORTED (cited billing row + probe scripts + intake shelf) · falsifier: none stated in card

The operator built his pro surface: a deck-based fleet interface
(dashboard/static/decks.html + 8 per-deck surfaces at dashboard/static/decks/).
Decks: Mesh3D, Rocinante, Personal, GLM Watch, Legions, GameBuild, Cache Econ,
MAG (the watcher). Mission in his words: "it'll be an interface for you to
gather data" and "we could be searching for invariants."

## WHAT THE FLEET MEASURED (receipts)
- 50-concurrent swarm lane: burst 50/50 OK; sustained 27.85 req/s, 99.89%
  success, ~49K tok/min (scripts/lite_lane_probe.mjs, lite_lane_sustained.mjs).
- Zero-quota night window receipted by billing row: 32,262,464 tokens on
  glm-5.3-flash, $0, 0 credits (23:00-09:00 SGT, "ZCode").
- Pro/Max package rates measured: flash input ~12.3K tok/credit, cache ~50.4K
  tok/credit, output ~3.6K tok/credit → Max budget ≈ 1.72B input tok/week.
- Intake shelf: 108 cards in 2 nights, classified into the 8 decks; genre
  rules earned from 60 scored cards (min_faves bands, mirror-not-feed accounts,
  lookalike handles, bookmark=feed-me gesture protocol).

## THE INTERFACE AS IT STANDS
- Operator scouts X Pro with 8 decks of search columns (genre-tuned
  min_faves thresholds, url: hunters, -min_faves discovery ceilings).
- Gestures: bookmark = feed me; like = noise; paste here = full 72-step
  socratic treatment (sweep, falsifiers, salon, tri-state card).
- Each deck surface now carries INVARIANT HUNT queries — discovery-language
  searches ("turns out", "the fix was", "we measured", anti-pattern) that hunt
  for LAWS being stated, not content being shared.

## THE DESIGN QUESTION
What should the interface between one human's scrolling attention and a
50-concurrent verification swarm actually be? What do search columns
structurally miss? Which human gesture is worth automating first? What is
that automation's own failure mode?
