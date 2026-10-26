# riblive1-U2-r2-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

L1: Fail-closed exit taxonomy must be shared across gates
CLAIM: My byte-contract check refuses to certify a spike-era index with text, not a guess (tools/corpus_fts_rebuild.py "no meta table (spike-era build)"), and sibling census patrol routes every cannot-verify byte to exit 2 while exit 1 is verified-stale (U2 L3). My L4 falsifier shows a third state (meta present, sha256 absent) that matches neither branch and silently passes: my gate lacks the exit-2 arm entirely.
STEAL: Add exit codes to check(deep=True): 2 for missing meta or partial meta (either of catalog_bytes/catalog_sha256 absent), 1 for verified mismatch, 0 only on full pass; port the sibling's table-driven fault-shape test asserting exit 2 per fault.
FALSIFIER: A legacy index with catalog_bytes but no catalog_sha256 that check(deep=True) reports anything other than the cannot-verify arm for.
SOURCE: tools/corpus_fts_rebuild.py "no meta table (spike-era build)" + (U2 L3) "exit 2 is reserved for cannot-verify, exit 1 for verified-stale"
LEVERAGE: high

L2: Skipped-line counting and aggregate-denominator blindness are the same disease
CLAIM: My rebuild counts malformed_lines and continues, and my sibling (U2 L5) shows aggregate "N tests / M files" denominators hid a zero-item file for weeks. Both instruments trust a total that silently shrinks or dilutes; neither surfaces a per-row witness.
STEAL: Write meta.rows_indexed AND meta.malformed_lines separately, and after every rebuild compare rows_indexed + malformed_lines against the catalog line count; exit 2 on any gather failure (unreadable catalog) and exit 1 on the gap exceeding a pinned threshold, borrowing U2 L3's fail-closed routing.
FALSIFIER: A rebuild where a corrupt line drops a row, rows_indexed is printed, and no check anywhere compares it to the live catalog line count.
SOURCE: tools/corpus_fts_rebuild.py "malformed += 1" + (U2 L5) "test files that collect zero items hide inside the aggregate denominators"
LEVERAGE: high

L3: One freshness rule, one witness grammar, frozen vectors
CLAIM: My L3/F3 single-source the freshness gate via importlib (tools/corpus_fts_rebuild.py "reuses it rather than keeping a second copy of the rule"), and U2 L2 freezes regression vectors so the live carrier count moving (1,837 -> 1,910) never edits fixtures. My corpus.py gate has no frozen vectors at all: a signature change to _fts_state breaks both callers at import with no red test.
STEAL: Add census_patrol_selftest.py-style frozen vectors for _fts_state: fixture (catalog_bytes, mtime, live_bytes, live_mtime, expected verdict) tuples that never sync to the real corpus, plus the U2 L2 receipt rule that moving a fixture requires a named receipt.
FALSIFIER: Changing corpus.py's _fts_state signature or predicate and seeing every existing test still pass.
SOURCE: tools/corpus_fts_rebuild.py "the freshness gate lives in tools/corpus.py" + (U2 L2) "frozen fixture vectors ... never updated when the live AGENTS.md count moves"
LEVERAGE: medium

L4: Instrument-verdict scope labeling must extend to index stats
CLAIM: U3 L5 labels every preload_selector row PROXY so a DECORATIVE verdict cannot be read as production fidelity; my malformed_lines and rows_indexed stats carry no scope label, so an operator can read rows_indexed as "corpus size" when it is "lines attempted, minus silent drops counted elsewhere."
STEAL: Rename the stats dict keys to rows_attempted, rows_indexed, malformed_lines and emit scope: "index-contract" alongside, matching the honesty-field pattern in (U3 L5), so downstream readers cannot misread an attempted count as a witness count.
FALSIFIER: A stats dict where rows_indexed is displayed alone as the corpus size with no malformed_lines or scope field in the same output.
SOURCE: tools/corpus_fts_rebuild.py "rows_indexed" + (U3 L5) "cite the honesty field in the row when reusing it downstream"
LEVERAGE: medium

L5: Zero-token and zero-shared-position measurement of nothing must map to cannot-verify
CLAIM: U3 L2 finds compare() emits DECORATIVE from shared_positions == 0, and my L5 finds a malformed-line-only witness silently vanishes from the index. Both are "verdict from measurement of nothing"; both need a UNMEASURABLE/exit-2 arm rather than a score of 0.0 or a skipped row.
STEAL: In the rebuild stats, if malformed_lines > 0 and a malformed line is the only occurrence of a search term verified present in the raw catalog, emit a names_missing list in stats rather than a clean build; mirror U3's proposed shared_positions == 0 guard.
FALSIFIER: A build where a term exists only on a corrupt catalog line, search returns no hits, and stats report zero anomalies.
SOURCE: tools/corpus_fts_rebuild.py "except json.JSONDecodeError" + (U3 L2) "rel_pct = ... else 0.0"
LEVERAGE: medium
