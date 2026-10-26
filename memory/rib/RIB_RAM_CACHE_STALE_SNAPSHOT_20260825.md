# RIB_RAM_CACHE_STALE_SNAPSHOT — the in-memory corpus fast-path silently goes stale (2026-08-25)

**Schema:** rib.ram_cache_stale_snapshot.v1 · date 2026-08-25
**Tool tested:** `mag/ram_cache.py` (in-memory corpus fast-path, schema ram_cache.v1)
**Method:** exercised the real behavior (load/corpus/corpus_text/status + the loop-pass call path),
found the ONE failure mode, shipped the ONE capability extension. Testable, not prose.

## The ONE failure mode — STALE SNAPSHOT (never auto-invalidates)
`load_corpus()` caches at module level and only re-reads disk when `refresh=True` is passed
explicitly. The sole production caller, `republic_loop.py` S0-ram-cache, calls
`ram_cache.load_corpus` with **no refresh** every pass. So after the first load, every subsequent
loop pass returns `cached: True` from a **frozen snapshot** — new steals / RIBs / research packs
written to disk between passes are **invisible** to lensing / novelty / gpu_process_data /
vram_memory.hot_region until the process restarts.

**Proof (reproduced):**
```
initial load cached: True
write new file to memory/steal/
loop-pass load cached: True          # still cached
new file visible in corpus: False    # MISSED
new file visible in text: False      # MISSED
```
The cache is a one-shot snapshot that silently goes stale. The whole point of the tool (RAM
fast-path for the corpus) becomes a correctness hazard: the system reasons over an old corpus.

## The ONE capability extension — AUTO-INVALIDATION via mtime fingerprint
Added a cheap staleness fingerprint: `_fingerprint()` returns the newest mtime across the three
watched corpus dirs (`memory/research_packs`, `memory/steal`, `memory/rib`). `load_corpus()`
records the fingerprint on load; on every non-refresh call it compares the live fingerprint and
**auto-reloads when disk is newer** — so the fast-path is preserved (still `cached: True` when
nothing changed) but the cache can never serve a stale snapshot.

**Proof (reproduced, single process):**
```
fresh load cached: False
no-change load cached: True          # fast path preserved
write new file to memory/steal/
after-new-file load cached: False    # auto-invalidated
new file in text: True               # NOW VISIBLE
```

## Testable acceptance (how to verify)
1. `load_corpus(refresh=True)` → `cached: False`; `load_corpus()` immediately after → `cached: True`.
2. Write a new `*.md` into `memory/steal/` (mtime strictly newer), then `load_corpus()` →
   `cached: False` and the new file's marker is present in `corpus_text()`.
3. Delete the probe file, `load_corpus(refresh=True)` → back to `cached: True` on next call.
4. `python -c "from mag import ram_cache; print(ram_cache.status())"` → `cached_in_ram: True`.

## Cost / honesty
- `_fingerprint()` is one `iterdir` per dir (no full re-read) — microseconds, $0, deterministic.
- Worst case unchanged: falls back to disk, never breaks the cadence.
- No new deps, no new state beyond one float in the module cache.

## Secondary finding (not the ONE, noted for completeness)
`counts.n_chars` reports the sum of per-doc lengths (362696) but `corpus_text()` returns the
`"\n\n"`-joined text (363332) — a 2×(n_docs−1) under-report. Cosmetic; not the load-bearing failure.
