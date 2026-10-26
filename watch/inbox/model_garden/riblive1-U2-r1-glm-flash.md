# riblive1-U2-r1-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

L1: single sanctioned FTS writer
CLAIM: catalog/catalog_fts.sqlite has exactly one sanctioned writer, tools/corpus_fts_rebuild.py, while tools/corpus.py is read-only ("nothing here writes").
STEAL: before writing the FTS db from any new tool, route through this module instead of opening the sqlite file directly.
FALSIFIER: another module found opening catalog_fts.sqlite in write mode outside this file.
SOURCE: tools/corpus_fts_rebuild.py:1 "the one sanctioned writer for catalog/catalog_fts.sqlite"
LEVERAGE: high

L1: tmp-build-then-replace atomic swap
CLAIM: rebuilds write to a .tmp sqlite then os.replace() it into place, so a crash never leaves a half index and a mode=ro reader keeps serving the old file.
STEAL: copy the tmp + os.replace pattern for any artifact a concurrent reader may hold open.
FALSIFIER: a rebuild path that truncates or opens the live db_path in write mode.
SOURCE: tools/corpus_fts_rebuild.py:31-33 "builds into catalog_fts.sqlite.tmp and os.replace()s it into place"
LEVERAGE: high

L1: bytes-plus-mtime freshness gate, hash as audit tier
CLAIM: meta.catalog_bytes and catalog_mtime_utc detect staleness cheaply per search; catalog_sha256 is recorded only for the optional --deep audit tier, so mtimes lies from restores or touches are caught by bytes.
STEAL: gate index freshness on catalog_bytes + mtime first; run sha256 only on --deep.
FALSIFIER: a per-search path that hashes the catalog before checking bytes.
SOURCE: tools/corpus_fts_rebuild.py:11-14 "a stale index is detected by bytes even when a restore or a touch lies with mtimes"
LEVERAGE: high

L1: malformed catalog lines skipped, not fatal
CLAIM: build_index counts JSONDecodeError lines as malformed and continues, so a corrupt catalog line silently drops a row from the index while rows_indexed still reports total lines seen including malformed ones.
STEAL: compare meta rows_indexed against catalog line count after every rebuild; a gap means dropped rows.
FALSIFIER: a malformed line causing build failure, or malformed_lines subtracted from rows_indexed.
SOURCE: tools/corpus_fts_rebuild.py:89-93 "malformed += 1" then "rows += 1" after continue
LEVERAGE: medium

L1: reuse gate, no second copy of the rule
CLAIM: this module loads tools/corpus.py via importlib and calls its _fts_state() rather than duplicating the freshness rule, keeping the gate single-sourced.
STEAL: when extending the gate, edit corpus.py only; this tool inherits it automatically.
FALSIFIER: a local reimplementation of the freshness check inside this file.
SOURCE: tools/corpus_fts_rebuild.py:41-43 "reuses it rather than keeping a second copy of the rule"
LEVERAGE: medium
