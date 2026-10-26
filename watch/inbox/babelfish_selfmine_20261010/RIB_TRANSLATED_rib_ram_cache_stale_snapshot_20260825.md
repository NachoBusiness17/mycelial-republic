# RIB_RIB_RAM_CACHE_STALE_SNAPSHOT_20260825 - translated by babelfish v1.0.0 (2026-10-10)

**Minted:** 2026-10-10 (caller-supplied; the module reads no clocks).
**Source bytes:** 3,327 | sha256 `e24323226386979c20ff0563a8b4d17a47c2c58a7e11ff54a1205da93fdcd4fa`
**Named roles found:** none detected
**Dominant terms:** true (12), cached (12), load (9), memory (8), file (8), corpus (6), false (6), path (5)

## THE LAW AS THEY STATE IT (verbatim, their voice)

> **Schema:** rib.ram_cache_stale_snapshot.v1 · date 2026-08-25
> **Tool tested:** `mag/ram_cache.py` (in-memory corpus fast-path, schema ram_cache.v1)
> **Method:** exercised the real behavior (load/corpus/corpus_text/status + the loop-pass call path),
> found the ONE failure mode, shipped the ONE capability extension. Testable, not prose.
> explicitly. The sole production caller, `republic_loop.py` S0-ram-cache, calls
> loop pass returns `cached: True` from a **frozen snapshot** — new steals / RIBs / research packs

## THE INVARIANT TRANSLATION (each row names its check; status UNVERIFIED until run)

| their claim | invariant form | the check |
|---|---|---|
| `load_corpus()` caches at module level and only re-reads disk when `refresh=True` is passed | refresh = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| 1. `load_corpus(refresh=True)` → `cached: False`; `load_corpus()` immediately after → `cached: True`. | load_corpus(refresh = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| 3. Delete the probe file, `load_corpus(refresh=True)` → back to `cached: True` on next call. | load_corpus(refresh = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |

## INSTRUMENT ROWS (measurable with a named instrument)

| claim | instrument |
|---|---|
| `ram_cache.load_corpus` with **no refresh** every pass. So after the first load, every subsequent | sample N instances per the universal's domain and count exceptions |
| records the fingerprint on load; on every non-refresh call it compares the live fingerprint and | sample N instances per the universal's domain and count exceptions |
| nothing changed) but the cache can never serve a stale snapshot. | sample N instances per the universal's domain and count exceptions |
| - Worst case unchanged: falls back to disk, never breaks the cadence. | sample N instances per the universal's domain and count exceptions |

## REGISTER (the unmappable remainder - kept verbatim, never struck)

The babel fish preserves what it cannot translate. Register is the
seed, not the defect.

- written to disk between passes are **invisible** to lensing / novelty / gpu_process_data /
- vram_memory.hot_region until the process restarts.
- **Proof (reproduced):**
- ```
- initial load cached: True
- write new file to memory/steal/
- loop-pass load cached: True          # still cached
- new file visible in corpus: False    # MISSED
- new file visible in text: False      # MISSED
- The cache is a one-shot snapshot that silently goes stale. The whole point of the tool (RAM
- fast-path for the corpus) becomes a correctness hazard: the system reasons over an old corpus.
- Added a cheap staleness fingerprint: `_fingerprint()` returns the newest mtime across the three
- watched corpus dirs (`memory/research_packs`, `memory/steal`, `memory/rib`). `load_corpus()`
- **auto-reloads when disk is newer** — so the fast-path is preserved (still `cached: True` when
- **Proof (reproduced, single process):**
- fresh load cached: False
- no-change load cached: True          # fast path preserved
- after-new-file load cached: False    # auto-invalidated
- new file in text: True               # NOW VISIBLE
- 2. Write a new `*.md` into `memory/steal/` (mtime strictly newer), then `load_corpus()` →

## FALSIFIERS

- For each invariant row: run its named check against primary bytes;
  a mismatch kills the row, not the corpus.
- For the translation itself: a second pass over the same bytes must
  produce a byte-identical rib (determinism law).
- Class-deafness: an estate-authored doc must yield nonzero invariant
  rows and a woo corpus must yield nonzero REGISTER rows (spec falsifier).

## LINEAGE

- Translated by babelfish v1.0.0 (2026-10-10); spec watch/inbox/babelfish_20261010/SPEC.md
- Operator thesis: book-to-skill == closed-corpus-to-self-improving-system,
  in the direction you set, despite the platform's best wishes (2026-10-10).
