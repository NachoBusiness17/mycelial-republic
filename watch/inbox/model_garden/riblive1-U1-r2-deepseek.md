# riblive1-U1-r2-deepseek (deepseek-chat @ deepseek, turn 1, channel: content)

L1: Same-day ambiguity rule has no frozen witness, so >= is one edit away
CLAIM: L1 (mine) says commits strictly after census day are the only growth, but no vector in census_patrol_selftest.py or tests/test_census_drift_patrol.py currently pins the 23:59 same-day case to added_since == 0; the rule lives only in the ">" at tools/census_drift_patrol.py. Sibling (L4) treats same-day mismatch as evidence text and never exit 1, so both views agree the ambiguity is deliberate, yet neither view produced the bytes that would stop a "fix" to ">=".
STEAL: Land the L1 steal before any other patrol change: one vector asserting added_since == 0 for a 23:59 census-day commit, cited to tools/census_drift_patrol.py: "if commit_day is not None and commit_day > census_date".
FALSIFIER: A patched patrol() using ">=" that passes every vector in census_patrol_selftest.py and tests/test_census_drift_patrol.py unchanged.
SOURCE: tools/census_drift_patrol.py "commit_day > census_date"; mine L1; sibling L4.
LEVERAGE: high

L2: Exit 2 and byte-contract refusal share one shape: cannot-verify never passes
CLAIM: My L3 reserves exit 2 for missing carrier, unparseable claim, unparseable date, future census, and git failure; siblings (L4) emit "no meta table (spike-era build): nothing to audit" without raising, and (L3) treats a None collected claim as UNVERIFIABLE exit 2. The connection neither side named: both tools distinguish migration state from mismatch, and both refuse to certify absent bytes. The one gap is that corpus_fts_rebuild check(deep=True) on a meta table missing only catalog_sha256 falls through both branches silently, while census_drift_patrol has no equivalent meta-partial case because its claims are single-clause.
STEAL: Add a meta-partial branch to tools/corpus_fts_rebuild.py check(deep=True): if meta has catalog_bytes but not catalog_sha256, return an explicit "byte contract incomplete: rebuild required" rather than falling through, mirroring the census tool's exit 2 for unverifiable bytes.
FALSIFIER: A spike-era index with catalog_bytes but no catalog_sha256 where check(deep=True) returns success on the bytes and never reports hash absence.
SOURCE: sibling L4 "no meta table (spike-era build): nothing to audit"; sibling L3 "None collected claim as UNVERIFIABLE exit 2"; mine L3 "exit 2 is reserved for cannot-verify".
LEVERAGE: high

L3: Two "malformed input skipped and counted" rows disagree on whether the count is a verdict input
CLAIM: Sibling (L5) counts JSONDecodeError lines into malformed_lines, continues, and returns the count in stats with no assertion; my L2/L4 family treats every unparseable byte as exit 2 rather than a count. These are contradictory dispositions for the same shape of fault, and the contradiction is load-bearing: the census claim is a single line whose loss breaks the gate, while a catalog line is one row among many whose loss degrades search recall silently. The unifying rule the sibling block lacks: per-row degradation is acceptable only when the count is surfaced as an assertion at the call site, which sibling L5's own STEAL already proposes but does not require.
STEAL: In the invoke path of tools/corpus_fts_rebuild.py, promote malformed_lines from a returned stat to a checked condition: fail the run if malformed_lines > 0 on a rebuild unless --allow-malformed is passed, matching census_drift_patrol's fail-closed posture for unverifiable bytes.
FALSIFIER: A rebuild where malformed_lines > 0 and the invoke path returns success without the caller seeing a nonzero signal.
SOURCE: sibling L5 "malformed += 1 then continue"; mine L3 "exit 2 for every unverifiable byte"; sibling L1 (malformed dropped not fatal, byte gate still claims fresh).
LEVERAGE: high

L4: Disk-count asymmetry (census) and byte-count freshness (fts) are the same "cheap witness catches the lie" move
CLAIM: My L2 says only disk_files < carrier_files is provable drift because item-bearing files are a subset of pytest-named candidates, and over-direction gaps are instrument lag printed as evidence. Sibling L1 says catalog_bytes detects a stale index even when a restore or touch rewrites mtimes, with sha256 as the audit tier. Both pick one cheap, asymmetric witness and treat the other direction as instrument noise rather than a violation. The connection neither side named: both witnesses are one-directional because they assume their candidate set is a subset of their claimed set, and both inherit the same falsifier shape, a real tree/table where the subset premise fails.
STEAL: In tools/census_drift_patrol.py and tools/corpus_fts_rebuild.py, name the subset premise explicitly in each comment block (candidate files superset of item files; catalog bytes superset-stable across touches) so a future falsifier is directed at the premise, not at the threshold.
FALSIFIER: A tests/ tree where pytest-named candidates are fewer than item-bearing files, or a catalog where a content edit leaves byte count and mtime unchanged, either of which falsifies the corresponding subset premise.
SOURCE: mine L2 "only shrink is provable drift"; sibling L1 "detected by bytes even when a restore or a touch lies with mtimes".
LEVERAGE: high

L5: Single-writer discipline (fts) has no census-side analogue, and that absence is a hole
CLAIM: Sibling L1 says catalog/catalog_fts.sqlite has exactly one sanctioned writer, tools/corpus_fts_rebuild.py, with tools/corpus.py read-only, and any new tool must route through the module. My round-1 laws name census_drift_patrol.py as the reader of the AGENTS.md census claim, but no law names who writes that bullet; the census carrier is edited by hand or by an unwritten tool, and the patrol can only observe drift after the fact. The fts stack's single-writer rule is the missing contract on the census side.
STEAL: Write the analogous single-writer law into AGENTS.md for the census bullet: the parenthesized "N tests / M files (YYYY-MM-DD census" clause is written only by a named command, and hand edits to the clause require a B2 receipt in the same PR, mirroring tools/corpus_fts_rebuild.py:1 "the one sanctioned writer".
FALSIFIER: A git log showing the census bullet's parenthesized clause edited in a PR with no invoking command and no receipt, proving the single-writer rule is not yet enforced for census.
SOURCE: sibling L1 "the one sanctioned writer for catalog/catalog_fts.sqlite"; mine L4 "the census claim parses only from the parenthesized clause".
LEVERAGE: medium
