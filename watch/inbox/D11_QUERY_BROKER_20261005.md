# D11 LANDED - the three-signal query broker (2026-10-05)

Door: D11-query-broker - "three-signal query broker (FTS + lattice +
embedding fusion)"; the door's OWED-first was the embedding pre-check:
nomic-embed-text IS pulled (Ollama 17 models live, probed 2026-10-05),
so the embedding signal measures the real model.

## What landed

**tools/query_broker.py** - retrieve-then-fuse, every signal named:

- FTS: tools/corpus.corpus_search over catalog/catalog_fts.sqlite. Query
  terms normalized (non-alnum split, 1-char drops: "pass@K coverage!"
  -> "pass coverage") because the scan needs ALL terms as substrings.
- LATTICE: memory/lattice/nodes.jsonl scored by token overlap on
  title+theme+path - deterministic, $0, the graph surface. The store
  was August-vintage; reseeded through the sanctioned builder this
  morning: 28,518 nodes / 28,539 edges now live.
- EMBED: RAW nomic-embed-text vectors (768 dims, NOT the flock bucket
  reduction - retrieval wants all dims), cosine re-rank over the
  FTS+lattice candidate union (two-stage: recall via the cheap signals,
  precision via embedding), warm-once then a 24-candidate budget. The
  broker owns its embed call with a 60s timeout: flock's
  _ollama_embed hardcodes timeout=8s and a cold nomic load measures
  6-10s+ on this host - 8s silently zeroed the signal TWICE before the
  fix (probed: 6.4s cold). DOWN => ABSENT with a note; the
  hash-geometric fallback is NEVER silently used for retrieval (the
  door's falsifier, made law).
- FUSION: Reciprocal Rank Fusion, k=60, no weights to tune; missing
  signals contribute nothing; every row carries per-signal ranks +
  carried_by so a later judgment layer sees which signal carried what.
- The recall floor is NAMED: map_asof/map_age_hours ride in the fts
  meta - artifacts newer than the catalog census are invisible to the
  signal no matter the query (proven live: today's EG20 receipt is not
  in the 871,790-line catalog yet; "passatk" = 0 catalog hits while
  "arena" = 3).

**tests/test_query_broker_20261005.py** - 10 passed: exact RRF
arithmetic, missing-signal contribution, term normalization, the named
recall floor, lattice determinism + overlap-only, embed-absent (down
embedder AND empty recall), cosine re-rank order, end-to-end two-signal
answer with the embedder down. The RRF test's first failure was the
module's honest 6-place rounding vs float tolerance - the arithmetic
was right.

## Live proof (both demos fused)

"gwap mud tricks": FTS 3 + embed re-rank -> the true steal receipt at
#1 (embed#1 fts#2) - the archive copies ranked below the original.
"bernays diary talk": BOTH cheap signals live, and the fusion did its
job: the LATTICE knot ranked #1 (embed#1 lattice#1) ABOVE the raw FTS
file copies - the graph signal promoted what FTS alone ranked second.
Per-signal ranks printed on every row.

## Findings banked along the way (not swept)

- The FTS index reads "stale" continuously on this tree: catalog.jsonl
  is a moving surface (871,790 lines, siblings landing); the B2-102
  gate says stale, the 09:00 daily rebuild heals, minutes later it is
  stale again. The broker reports engine+state per query and the scan
  fallback answers - no hide.
- The catalog census lags new artifacts (today's receipts invisible).
  The broker names map_asof; the cure (a rescan cadence decision) is
  the patrol's class, not smuggled in here.
- The lattice store had silently rotted to August (744-era vintage
  while the estate grew) - the reseed through seed_lattice_store() is
  the sanctioned writer and the store now carries the full estate.
  The reseed should ride the same daily cadence as the FTS rebuild or
  the lattice signal decays again (filed as the follow-up).

Banked by GLM-5.3 window, 2026-10-05 (compute-grind block).
