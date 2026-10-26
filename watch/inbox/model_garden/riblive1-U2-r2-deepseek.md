# riblive1-U2-r2-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

L1: Two-instrument staleness contract shares one fail-closed arm
CLAIM: corpus.py's byte-gate (mine L1) and census_patrol's "cannot-verify -> exit 2" (U2 L3) are the same design move applied to different artifacts: cheap proxy for the common case, hard refusal when the proxy cannot be trusted. corpus uses catalog_bytes+mtime as the proxy and sha256 as the deep tier; patrol uses committed-growth+disk-shrink as the proxy and exit 2 as the refusal. Neither tool guesses a pass on missing evidence.
STEAL: Add a shared header comment to tools/corpus.py and tools/census_drift_patrol.py naming both as instances of the "proxy gate + fail-closed arm" pattern, so a third tool copying either inherits the shape intentionally.
FALSIFIER: A corpus.py path that returns a fresh/stale verdict when meta is absent, or a patrol() path returning 0 after a gather failure; either would show the two tools do not share the contract.
SOURCE: tools/corpus_fts_rebuild.py "no meta table (spike-era build): nothing to audit" (mine L4) + tools/census_drift_patrol.py "a git failure is exit 2, never a guess and never a pass" (U2 L3)
LEVERAGE: high

L2: Byte-gate falsifier and disk-shrink-only rule share the same blind spot
CLAIM: My L1 falsifier (in-place line edit, bytes unchanged, mtime touched) and U2 L2's ruling ("only shrink is provable drift, every over-direction gap is instrument lag") are the same epistemic choice: when the cheap signal is ambiguous, the tool reports evidence but does not fail. corpus tolerates an in-place-edit false-pass because the sha256 tier catches it only under --deep; patrol tolerates a disk_files > carrier_files gap because the pytest-name subset makes shrink the only provable direction. Both punt the ambiguous case to a human-read evidence channel.
STEAL: In tools/corpus.py, when meta.catalog_bytes matches but mtime is newer than recorded, print an "in-place-possible-edit" evidence line and suggest --deep; do not change the verdict. Mirror patrol's evidence-vs-violation split.
FALSIFIER: A corpus search where meta.catalog_bytes matches, mtime is newer, and no evidence line is emitted but a --deep run then reports a sha mismatch, proving the cheap gate silently passed a case the deep gate catches.
SOURCE: mine L1 falsifier "a catalog whose byte count and size are unchanged but whose line contents were edited in place" + U2 L2 "every over-direction gap is labeled instrument lag and printed as evidence, never as a violation"
LEVERAGE: high

L3: Single-writer rule (sibling) is the precondition my atomic-swap row assumed
CLAIM: My L2 (tmp-build-then-os.replace) describes the mechanism; sibling L1 ("exactly one sanctioned writer") is the invariant that makes the mechanism sufficient. os.replace is atomic only if no other process opens db_path for write between the unlink and the replace; a second writer breaks both. The two laws are not independent, they are precondition and method.
STEAL: Add an assertion to build_index that open(catalog_fts.sqlite, 'r+b') fails or that a lock file is held, so a second writer is detected at build time rather than corrupting the index under a reader.
FALSIFIER: A second module opening catalog_fts.sqlite in write mode while a rebuild is in flight that still produces a consistent index, which would show the single-writer claim is unnecessary rather than load-bearing.
SOURCE: mine L2 "builds into catalog_fts.sqlite.tmp and os.replace()s it into place" + sibling L1 "exactly one sanctioned writer ... while tools/corpus.py is read-only"
LEVERAGE: high

L4: Malformed-line skip is silent in both formats
CLAIM: My L5 (corpus.py JSONDecodeError counted into malformed_lines, build continues) and U5 L5 (preload_selector's selftest never checks load_blocks determinism or malformed-line behavior) show two tools that both tolerate malformed input without a per-query signal. corpus surfaces a count only in the returned stats dict; preload_selector surfaces nothing at all. A reader of either tool cannot tell from a search/order result that a line was dropped.
STEAL: In tools/corpus.py, emit the malformed_lines count into search output when >0 ("index built with N malformed lines skipped; results may be incomplete"). In mag/preload_selector.py, add a counted-malformed field to load_blocks' return and print it in cmd_order.
FALSIFIER: A corpus search where a document's only catalog line is malformed, the search returns zero hits for that document, and no field in the response indicates the drop, confirming both tools share the silent-drop shape.
SOURCE: mine L5 "except json.JSONDecodeError: malformed += 1; continue" + U5 L5 "never checks that load_blocks returns identical bytes on repeated reads or that malformed lines are skipped deterministically"
LEVERAGE: medium

L5: Same-day-ambiguity rules diverge between census and selector
CLAIM: U2 L1 excludes same-day commits as deliberately ambiguous growth; my L1 byte-gate treats an mtime touch as not-stale if bytes match. Both handle "the clock says something changed but nothing provably grew" by refusing to fire, but census names the choice in a selftest vector while corpus does not pin it. The sibling has the stronger discipline; adopt it.
STEAL: Add a vector to a corpus.py selftest asserting that an index whose meta.catalog_bytes matches but meta.catalog_mtime_utc is older than the file's current mtime returns "fresh (bytes match, mtime newer: evidence only, not stale)" so the ambiguity rule is pinned like U2 L1's 23:59 case.
FALSIFIER: A future patch to corpus.py that treats mtime-newer-than-recorded as STALE and still passes every existing selftest, which would show the ambiguity rule was never pinned on the corpus side (as it is on the census side).
SOURCE: U2 L1 "same-day activity is deliberately treated as ambiguous, not as growth" + mine L1 "the cheap per-search gate uses bytes plus mtime"
LEVERAGE: medium
