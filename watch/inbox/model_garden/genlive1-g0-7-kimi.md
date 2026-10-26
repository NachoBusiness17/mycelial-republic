# genlive1-g0-7-kimi (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Unmetered sqlite3 connection in check() lacks timeout, risking indefinite hang on lock | EVIDENCE: tools/corpus_fts_rebuild.py:116 | FIX: Add timeout=30.0 to sqlite3.connect call
DEFECT 2: Unbounded memory growth: batch list holds 50000 rows with no size cap on row content | EVIDENCE: tools/corpus_fts_rebuild.py:78-79 | FIX: Add batch_bytes accumulator and flush on size threshold (e.g., 50MB)
DEFECT 3: Malformed line counter incremented but never reported in --check mode or exit code | EVIDENCE: tools/corpus_fts_rebuild.py:75 | FIX: Include malformed count in check() return and warn if non-zero
DEAD-CODE: catalog_path = Path(catalog_path) re-wraps already-Path argument | EVIDENCE: tools/corpus_fts_rebuild.py:60
ONE-SITTING FIX: Add connection timeout to prevent check() hangs on locked FTS db | EVIDENCE: tools/corpus_fts_rebuild.py:116
