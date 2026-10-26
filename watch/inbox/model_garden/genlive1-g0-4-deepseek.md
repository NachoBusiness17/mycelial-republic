# genlive1-g0-4-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: build_index does not fsync the tmp db before os.replace, so a crash between close and rename can leave a durably-zero-length index; also the directory entry itself is not fsynced | EVIDENCE: tools/corpus_fts_rebuild.py:108 (con.close(); os.replace immediately after, no flush of the page cache) | FIX: open tmp with a file handle and os.fsync it (plus fsync the parent dir) before os.replace.

DEFECT 2: main() rebuild path ignores the --deep flag entirely and rebuild never verifies freshness of catalog reads, so a truncated or partially-written catalog line that is valid JSON silently indexes fewer rows with catalog_bytes/sha256 recorded as the post-hoc truth | EVIDENCE: tools/corpus_fts_rebuild.py:161 (deep parsed, only used in --check branch; build path drops it) and lines 91-96 (rows counted from the same file whose stat is later recorded) | FIX: stat+sha the catalog before opening it, index from that snapshot, and fail the build if the sha changes.

DEAD-CODE: _load_corpus is called twice per main() invocation (once in --check via check(), once in the rebuild path) with an unused duplicate pattern; also check()'s "refused: no index" branch is unreachable because corpus._fts_state() cannot return "fresh" when FTS_DB.exists() is false | EVIDENCE: tools/corpus_fts_rebuild.py:123

ONE-SITTING FIX: add fsync(tmp)+fsync(dir) around os.replace and hoist the catalog stat/sha256 snapshot to before the insert loop so meta records the bytes actually indexed | EVIDENCE: tools/corpus_fts_rebuild.py:108
