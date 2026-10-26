# UF-122 candidate two: held-out retrieval eval spec + tags v2 owner rule

Written 2026-09-26, this lane. Blind: sibling candidate uf122-one.md not read.
All numbers below were measured this session unless marked otherwise; commands
and outputs cited inline. No em-dashes per record law.

## Approach

One sentence: gate every corpus mining pass on a 50-question citation-recall
eval whose gold answers live in a vault OUTSIDE the catalog walk root and are
provable-after but unreadable-before via salted commitments, where every
question is minted through eight mechanical local screens (I ran the expensive
ones this session: two full 1.79 GB pool scans), and pair it with a tags v2
law that stamps owner+created on every derived tag row and moves asserted tags
to an append-only overlay the nightly retag can never erase.

The claim under test (UF-122 lane prompt, watch/inbox/union_fullsend_20260917/
queue.jsonl line 122): "a catalog map + read tools improve context selection
(measured as citation recall: did the answer cite the file that actually
settles the question)". The original prompt asked for "5 questions x 10
zones" and questions "answerable ONLY by one specific file". Two of its
assumptions are falsified by this session's measurements, and the spec below
corrects both rather than inheriting them:

1. "One specific file" is false in this estate's bytes. I scanned the full
   home-zone text pool (347,120 files, 1,791 MB, files <=256 KB, from
   catalog.jsonl) twice for hand-picked distinctive spans; all 7 failed
   strict uniqueness, with settling sets of 4, 6, 8, 8, 33, 111, and 7 files
   respectively, because the estate ECHOES facts: receipts into
   memory/burns/LEDGER.jsonl (span "12.352s" -> 4 files), receipt numbers into
   tools docstrings ("217,686,016" -> 6 files), catalog ids into pytest
   fixtures under agents/pytest-tmp-* ("a54ff182c7e8" -> 8 files), filenames
   into briefs and context packs ("SEED_SELF_STEAL_AUDIT_20260926.md" -> 8
   files), lane phrases into archaeology harvests ("3-witness" -> 33 files),
   session run-ids into biography derived/residual/briefs
   ("039c63e49dde40268f95c5474052d844" -> 7 files, all echoes of one session).
   Correction: gold is a SETTLING SET (every file whose bytes contain the span
   verbatim), minted with |S| <= 5 after mechanical span-growth; citing ANY
   member scores. A longer span matches a subset of the shorter span's files,
   so growth refinement only re-checks the current hit list, monotonically
   shrinking S. This is more honest than the prompt and mechanically derivable.

2. The prompt's zone list is stale against the map. Measured over
   catalog.jsonl (row histogram; last-row-wins over the 489,314 unique paths
   differs only through the 158 dup rows the manifest counts): the catalog
   zone has 0 rows (the walker EXCLUDEs catalog/, mag/catalog_scan.py:88),
   games has 21 rows / 19 text files, campaigns 14, basecamp 3. Worse, the stored zone column
   mixes scanner generations: 1,031 of 1,054 local_sovereign_agent/mag/ paths
   carry zone "lsa" while ZONE_MAP (mag/catalog_scan.py:107) says mag -> code;
   a row refreshed today (mag/catalog_rescan.py, mtime 2026-09-26T19:14:41Z)
   carries "code". Cause: the incremental arm's signature is (bytes, mtime)
   only (mag/catalog_rescan.py:114-115), so a ZONE_MAP change never re-derives
   zones for unchanged files. Correction: the mint computes strata by applying
   the CURRENT zone_of to unique paths (pure function of the path string), and
   never reads the stored zone column. Strata = 10 largest home (non-ext)
   zones by text-file count with a floor of 50 text files, 5 questions each;
   by current zone_of that is today approximately memory, lsa, runs, intake,
   watch, code, queue, doctrine, dashboard, research (exact table recorded at
   mint). ext:* zones are excluded from the gold pool entirely: they are
   public open-source and harvested content (azerothcore-wow, vmangos),
   pretraining-visible, so a frontier miner could answer without the corpus;
   that is the leakage kill condition, and sibling policy is UF-123's card,
   not this one.

The eval in one paragraph. A MINTER seat samples candidate (file, span) pairs
per stratum from primary surfaces (authored files; excludes corpus/, mine/,
agents/, memory/biography/derived and residual, memory/agent_sessions, .bak
paths, kind=corpus harvested text), runs the eight screens below, writes one
question line per surviving candidate WITHOUT the span or any gold path token
run, then seals: questions + gold + salts go to
C:/Users/foste/.mag_eval/uf122/ (OUTSIDE the projects-parent walk root
mag/catalog_scan.py ROOT walks, and outside the repo the corpus tools confine
to, tools/corpus.py:79-98), while salted commitments sha256(salt + canonical
gold json) land in-repo at catalog/eval/uf122_status.json (catalog/ is
walker-excluded so the map never indexes eval machinery). A MINER (the seat or
mining pass under test) receives questions only, answers with citations
through the corpus surface. A GRADER (deterministic local script, no LLM
judge, no network) re-reads gold, verifies each cited path's live bytes
contain the span, and writes verdicts that contain NO spans and NO gold paths,
only question ids, verdicts, and 12-hex catalog ids (sha of path, not
invertible, tools/corpus.py:101-102). The GATE: `tools/uf122_eval.py check`
exits 0 while a current baseline exists (scored, and pinned to the current
catalog map_sha256) and exit 2 when absent, stale, or map-changed; a mining
pass (any change that alters what the corpus surface returns: scanner, tags,
index, ranking; or any fine-tune corpus selection) requires check=0 to start
and a post-change condition-B re-run showing no regression beyond 2 questions
(0.04) to ship. This mirrors the estate's exit-2-only hard-block law
(AGENTS.md build discipline, githooks/pre-push:10 pattern) and CONSTITUTION.md
line 13 ("Mining proposals never auto-merge"): the gate never blocks thought,
only ships.

The eight screens (all local, all run at mint; S1-S5 also re-runnable at
score). S1 corpus-only: span occurs in >=1 file's bytes (the 1.79 GB pool
scan; measured 56.8-60.2 s per full pass this session, ~30 MB/s, 511
vanished-path read errors consistent with the C6 drift the freshness policy
counts as "vanished", catalog_manifest.json summary). S2 settling set: |S| <=
5 after span growth; S excludes fixture paths (agents/pytest-tmp-*) and boot
files. S3 no-map-leak: span must not appear in ANY catalog path or title
string (one pass over catalog.jsonl; titles are first headings of md files,
mag/catalog_rescan.py:217, so a first-heading gold would be answerable from
the map row alone without corpus_get). S4 no-boot-leak: span absent from the
boot set (AGENTS.md, LOAD.md, CONSTITUTION.md, docs/FRAMEWORK_LOAD.md, the
docs/ref load-order files including MAG_MYCELIAL_REPUBLIC_COMPASS.md, 
memory/briefs/latest.md, queue/todo.md); my demo span
"SEED_SELF_STEAL_AUDIT_20260926.md" fails exactly this way (present in
memory/briefs/FROZEN_ASOF_20260926.md and context packs). S5 no-question-leak:
question text contains no run of >=3 consecutive span tokens, no gold
basename, no primary path (mechanical check over the authored line). S6
idiosyncrasy heuristic: span must contain at least one token with a digit, or
a hex run >=8, or a hyphen-compound not present in any ext:* sibling tree;
heuristic by admission, backstopped by S8. S7 tool-fairness: span lies within
the first 256 KB of the gold file (the corpus_get serve cap, tools/
corpus.py:70) and the file passes the same text sniff (no NUL in head). S8
closed-book probe: all 50 questions asked of a local ollama janitor
(127.0.0.1:11434, endpoint verified responding this session with a model
list; gemma:2b presence individually NOT verified) with no tools; any
span-normalized correct blind answer retires and replaces that question; more
than 5 retirements invalidates the mint. Additionally, at every scored run,
the MINER ITSELF runs a closed-book arm first (same seat, tools off): any
question it answers span-correct blind is retired from that run's
denominator, so the eval only ever scores questions the evaluated seat cannot
answer without the corpus. This per-run blind arm is the strongest honest
leakage defense and replaces any reliance on the small-model probe.

Metrics and bars. Primary: citation_recall = (answers citing >=1 settling-set
file whose live bytes the grader re-verified contain the span) / (scored
questions). Secondary: answer_correctness = normalized span present in the
answer text; correctness WITHOUT citation flags blind-suspect and feeds the
retirement rule. Drifted questions (gold file sha256 at mint != sha256 at
score) leave the denominator and are reported as drift_count (the C6 honesty
made mechanical; the map already lags: tests/test_catalog_tags.py exists on
disk but has 0 rows in the 2026-09-26T19:16:46Z snapshot, verified by grep
over catalog.jsonl returning 0 rows). Engine attribution: each condition-B
search records engine (fts5 vs scan) because B2-22 measured FTS5 missing
mid-token hits (tools/corpus.py:22-27 parity note); a mining pass that flips
engines changes recall and must say so. Baseline = both arms scored at mint
window; condition B is re-run per mining pass. The delta B minus A on
citation recall is the claim under test; A should sit near 0 by construction,
so its real job is the leakage tripwire.

Held-out discipline mechanics (the third kill condition). The vault directory
is outside both the walk root and the repo confinement, so no corpus tool and
no map row can reach it; the grader reads it but never echoes gold; score
output and in-repo status carry commitments and catalog ids only; the salt
and gold publish ONLY on operator command to open a post-run verification
window (anyone can then recompute sha256(salt+gold) against the pre-run
commitments and re-play verdicts). The minter must not be the miner: the mint
receipt records the minter seat id, and a mining pass run by the minting seat
is invalid unless a second minter re-randomizes (the salon's blind-divergence
discipline, CORPUS_MAP_SALON "THE SEVEN SHAPES ... written without seeing
siblings", applied to evals). Gold leaves the vault in exactly one accident
class: an operator pasting it into the repo; the spec's leak falsifier (below)
greps for published spans before any baseline counts.

Tags v2 owner rule (second deliverable, watch/WANTS.md 2026-09-18 block:
"tags v2 with owner column (who authored the tag, when) ... done = tags rows
carry owner+created; kind filter still green"). Current rows are
{id, path, zone, kind, age_class, bytes} written wholesale by run_tags
(mag/catalog_tags.py:118-122) with one anonymous script author and no
provenance, post-hoc, per salon S7's condition "Tags carry owner+date or you
rebuild the eight-map pathology in one table". v2 law, four clauses:

1. Schema: every tags.jsonl row gains owner and created. For derived rows
   owner = "rule:salon-appendix-b@<rev>" where rev bumps when the kind rules
   change (the module docstring already versions them via the pinned test
   file); created = ISO ts when this (id, axis, value, owner) was FIRST
   derived, preserved across nightly retags by loading the prior sidecar and
   reusing created when the tuple is unchanged (NOT the run time, which would
   reset provenance nightly; the run time already lives in the manifest
   tags_ts and the TAG_REPORT header). When a file crosses fresh -> aging the
   age_class value changes, so created correctly restarts: provenance tracks
   the current value's derivation.
2. Durable/derived split (the load-bearing clause): the nightly retag rewrites
   tags.jsonl via temp+replace (mag/catalog_tags.py:126), so any hand-asserted
   tag placed in that file would be erased within 24 h. Asserted tags
   therefore live in a NEW append-only overlay catalog/tags_asserted.jsonl,
   one row per assertion {id, path, axis, value, owner, created, note},
   last-wins per (id, axis), which the retag never touches. Readers join
   derived first, overlay last-wins on top.
3. Backward compatibility by construction: corpus_search's kind filter reads
   only row.get("kind") (tools/corpus.py:250) and ignores unknown columns, so
   the schema widen cannot break the join; the green-filter claim is then
   pinned by extending tests/test_catalog_tags.py (10 existing test functions
   verified present this session) with: every row carries non-empty
   owner+created; created is preserved across two run_tags calls on an
   unchanged base; an overlay row survives a retag; the kind join still
   filters. TAG_REPORT.md gains a "## By owner" section; the dated-report
   preservation flow (write_tag_report, mag/catalog_tags.py:135-149) is
   unchanged.
4. Dogfood symmetry: every UF-122 question row carries owner (authoring
   seat) and created under the same rule, so the eval artifact is the first
   consumer of the v2 provenance law and the owner namespace is shared with
   the violation-baseline --by <who> convention (AGENTS.md build discipline).

## Moves with estate paths

1. docs/ref/UF122_RETRIEVAL_EVAL.md (NEW; spec-first per AGENTS.md "Spec
   before behavior change"): the spec above, including the strata rule
   (current zone_of over unique paths, 10 home zones, floor 50 text files,
   5 each), the eight screens with this session's measured costs, question/
   gold/commitment schema, vault location, grader contract (no spans, no gold
   paths, catalog ids only), metric definitions, retirement and drift rules,
   and the gate semantics.
2. tools/uf122_eval.py (NEW; subcommands mint / screen / probe / run-arm /
   score / check): mint draws per-stratum candidates and runs screens using
   the measured batched pool scan (one pass, all candidate spans, ~60 s per
   full pool); check implements the exit-0/exit-2 gate against
   catalog/eval/uf122_status.json. Landing tests in tests/test_uf122_eval.py
   with a tiny fixture corpus (no 1.79 GB dependency in CI).
3. mag/catalog_tags.py: owner+created columns with prior-created preservation
   (clause 1) plus the append-only overlay catalog/tags_asserted.jsonl
   (clause 2); TAG_REPORT "By owner" section; extend
   tests/test_catalog_tags.py (10 functions there today) with the four
   pinning tests of clause 3.
4. catalog/eval/uf122_status.json (NEW, walker-excluded because catalog/ is
   in the EXCLUDE set, mag/catalog_scan.py:88): commitments, baseline record
   (scored_at, seat, citation_recall_B, denominator, drift_count,
   map_sha256 pin, questions_rev), and the mining-pass log; receipts to
   watch/inbox/ per the shared-surface contract when a baseline lands.
5. The gate hook: a law line in AGENTS.md build discipline ("no mining pass
   without uf122 check=0 and a no-regression re-run") is an operator call on
   the operator's file; until then the gate is enforced at the mining-pass
   lane template (queue lane runner CYCLE receipt must cite the baseline id,
   the same tri-state trail law the elder lane just gained, salon execution
   receipt). Filed as owed, not claimed.

## Falsifier

Three, one per kill condition, each runnable as a command:

1. Leakage falsifier (mint validity): re-run the screens over the minted 50
   plus a red-team pass that greps every surface a miner can read (repo
   working tree, catalog.jsonl paths+titles, the FTS index, published status)
   for each gold span and gold path. ANY hit before the run, OR more than 5
   of 50 janitor blind-solves, OR more than 5 per-run miner blind-solves,
   kills the MINT and forces re-mint. This session already demonstrates the
   screens are load-bearing, not decoration: 7 of 7 hand-picked "distinctive"
   spans failed them (outputs above), so an unscreened mint would leak.
2. No-network falsifier: grep the spec and the tool for any fetch/socket/web
   import or URL except 127.0.0.1:11434 (ollama, local); run one full
   mint+score cycle with the network interface disabled. Any step that fails
   offline kills the spec's local-only claim. Not run this session (design
   lane, tool not yet landed); the two screen passes that exist WERE pure
   local venv python over local bytes.
3. Construct-validity falsifier: the eval must detect a retrieval change
   already known to matter. B2-22 measured FTS5 missing 3 of 10 mid-token
   substring queries (tools/corpus.py:22-27, spike receipt
   watch/inbox/burn_wave_20260926/B2_22_fts5_spike_20260926.md). Force
   condition B through the scan engine, then the fts5 engine, on the same
   questions: if citation recall does NOT move in the measured direction on
   the affected queries, the eval measures noise and dies. Also the S2-style
   audit: sample 100 scored citations, re-verify every grader verdict against
   bytes; any miscount kills the grader.

Held-out falsifier (wrapping kill condition 3): before a baseline counts, a
seat that had access ONLY to what miners see (questions, commitments, repo,
map) attempts to produce any gold span or settling-set path; anything it
recovers breaks the discipline and the vault location or grader output
changes until the red-team recovers nothing.

## Owed

1. Landing: docs/ref/UF122_RETRIEVAL_EVAL.md, tools/uf122_eval.py, the two
   test files, mag/catalog_tags.py v2. This lane ships the design only; the
   want's done-looks-like ("50 questions scored, citation-recall baseline
   recorded before any mining pass", watch/WANTS.md 2026-09-18 block) needs
   the mint run + one scored baseline, which needs an authoring seat and the
   closed-book probe.
2. Estate defects found while grounding (they degrade a mint, filed here as
   debt with evidence, fixes are separate cards): (a) zone column mixes
   scanner generations, 1,031/1,054 mag/ rows say lsa, because incremental
   refresh keys only on (bytes, mtime) (mag/catalog_rescan.py:114-115) and
   never re-derives zones on ZONE_MAP change; a dated rebuild would compact
   generations; (b) tests/test_catalog_tags.py has 0 rows in the current map
   snapshot while existing on disk (grep over catalog.jsonl: 0 rows; ls
   confirms the file), a same-day freshness lag; (c) TAG_REPORT and
   kind_by_zone stats inherit the stale zone column.
3. The mint's stratum table must be recomputed at mint time by current
   zone_of (the approximation in Approach used last-row-wins counts plus
   path-prefix inspection, not a full re-derivation).
4. Closed-book probe model choice: ollama endpoint verified responding this
   session (model list returned); which janitor (gemma:2b per the AGENTS.md
   tier ladder) was not individually verified.
5. AGENTS.md gate law line (operator call on the operator's file) and the
   mining-pass lane-template wiring; until landed, the gate exists only as
   tools/uf122_eval.py check semantics plus this spec.
6. The original UF-122 lane row asked for "the spec, not the questions"
   (queue.jsonl line 122); this candidate honors that. If the judge wants
   exemplar questions, they cost one mint pass and must not be the 50 sealed
   ones.
