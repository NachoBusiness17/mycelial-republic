# riblive1-U2-r1-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

L1: Meta bytes contract detects stale index past mtime lies
CLAIM: The build writes catalog_bytes and catalog_sha256 into meta so a stale index is detected by the recorded byte count even when mtimes are touched or a restore rewrites timestamps. The cheap per-search gate uses bytes plus mtime; the sha256 is the audit tier.
STEAL: In tools/corpus.py, replace any mtime-only staleness comparison with a catalog_bytes comparison against meta.catalog_bytes, keeping mtime as secondary.
FALSIFIER: A catalog whose byte count and size are unchanged but whose line contents were edited in place would pass the byte gate and return stale search hits.
SOURCE: tools/corpus_fts_rebuild.py "so a stale index is detected by bytes even when a restore or a touch lies with mtimes"
LEVERAGE: high

L2: Build replaces atomically so ro readers never see partial index
CLAIM: build_index writes into catalog_fts.sqlite.tmp then os.replace()s it, so a crashed build never leaves a half index and a concurrent mode=ro reader keeps serving the old file. Deletes any pre-existing tmp before starting.
STEAL: Audit every other writer in tools/ for tmp-then-replace; convert any in-place sqlite write to the same tmp+os.replace pattern.
FALSIFIER: An interrupt between con.execute("CREATE TABLE crows...") and os.replace that leaves a tmp sqlite that a subsequent run fails to unlink would violate the contract.
SOURCE: tools/corpus_fts_rebuild.py "builds into catalog_fts.sqlite.tmp and os.replace()s it into place"
LEVERAGE: high

L3: Rebuild reuses corpus.py freshness rule by hermetic load
CLAIM: _load_corpus() imports tools/corpus.py via importlib.util.spec_from_file_location rather than duplicating the freshness rule, so the gate at search time and at check time share one source of truth. No second copy of the rule is kept.
STEAL: Add a test that greps tools/ for the freshness predicate string; fail if any module other than corpus.py defines its own variant.
FALSIFIER: If corpus.py's _fts_state signature or FTS_DB constant changes, this tool breaks at import time with no test catching it before first run.
SOURCE: tools/corpus_fts_rebuild.py "the freshness gate lives in tools/corpus.py and this tool reuses it rather than keeping a second copy of the rule"
LEVERAGE: medium

L4: Deep check refuses to certify when meta table is absent
CLAIM: check(deep=True) on a fresh index with no meta table returns "no meta table (spike-era build): nothing to audit; run a rebuild for the byte contract" and does not raise, distinguishing migration state from mismatch rather than silently passing.
STEAL: Emit the same refusal text from any other tool that audits catalog_fts.sqlite so spike-era and contract-era indexes are told apart uniformly.
FALSIFIER: A legacy index with a meta table missing only catalog_sha256 but present catalog_bytes would match neither branch and silently pass deep without a hash compare.
SOURCE: tools/corpus_fts_rebuild.py "no meta table (spike-era build): nothing to audit; run a rebuild for the byte contract"
LEVERAGE: medium

L5: Malformed catalog lines are skipped and counted, not fatal
CLAIM: The rebuild counts JSONDecodeError lines into malformed_lines and continues; the index is built over the remainder and rows_indexed excludes the malformed lines. Callers see the count in the returned stats dict.
STEAL: Add an assertion in the invoke path that fails the run if malformed_lines exceeds a small threshold, so silent shrinkage of the corpus is visible to the operator.
FALSIFIER: If a corrupted catalog line is the only witness for a document, the index silently lacks it and search misses that document without surfacing any per-query signal.
SOURCE: tools/corpus_fts_rebuild.py "except json.JSONDecodeError:\n                malformed += 1\n                continue"
LEVERAGE: medium
