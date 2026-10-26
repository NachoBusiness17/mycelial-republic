# UF-122 candidate one: the sealed content-span retrieval eval (spec v2) + tags v2 owner column

## Approach

The estate already drained UF-122 twice and both drains fail this card's kill
condition, measured against bytes this session:

- The promoted remote spec (raw.jsonl UF-122 row, read this session) templated
  11 anchor files that do not exist (B2-57 defect c) and its arithmetic summed
  to 55, not 50.
- The B2-186 re-anchor (`watch/inbox/burn_wave_20260926/B2_186_uf122_eval.py`,
  read line-by-line this session) "fixed" the dead anchors by generating
  questions from catalog row titles: each question is "which file's title
  contains token X" with uniqueness verified over path+title only
  (B2_186_uf122_eval.py:97-112). Every question is therefore answerable from
  map metadata alone, with zero file bytes read. That is leakage by this card's
  law. Its treatment arm IS `corpus_search` itself (the receipt admits it:
  "the treatment arm here is the tool itself"), so the headline 1.0 vs 0.083
  "12x gap" is the tool scoring itself on its own echo, against a
  lexicographic name-prior strawman. And its gold set is fully regenerable:
  seed 20260926 is published in the script and receipt, and
  `B2_186_uf122_results.json` sits in-repo in watch/inbox holding
  `answer_path` and `answer_token` per question. Zero held-out discipline.

So the work is not "write the first eval," it is "design the eval that
replaces a leaked one without inheriting its disease." UF-122 v2:

1. **Answers are byte spans, not metadata.** The gold answer for every
   question is a verbatim span (4 to 160 chars) in the body of exactly one
   text file under the walk root, verified by a single-pass span-uniqueness
   oracle over all text files (substring semantics, never FTS, so the B2-22
   mid-token miss cannot hide a duplicate). Feasibility measured this session
   on a 3-dir slice (watch/inbox/burn_wave_20260926, docs, queue; 1,978
   files): 1,556 error strings, 190 12-hex spans, and 27 B2-ids are already
   unique to one file in that slice alone. The pool is deep; the draw is the
   seal.
2. **Five span classes, all estate-minted, all prior-free:** estate ids
   (B2-nnnn, UF-1nn, LAW-n), sha prefixes of 12+ hex, exact error strings,
   config constants with units, verbatim sentences of 40+ chars naming
   estate-specific entities. No public-knowledge fact is eligible (nothing a
   model's priors or a web search could settle), so the spec needs no network
   anywhere: builder, arms, grader are all local.
3. **Exclusion laws that kill each leak channel:** a span is rejected if it
   appears in any catalog row's path or title (the scanner's title is the
   file's first heading line, mag/catalog_scan.py:317-329 territory, so this
   kills "answerable from the map"), if it equals any catalog row id (ids are
   sha256(path)[:12], so a 12-hex span could collide), or if it lives in a
   secret-pattern path (configs/secrets, .env, key/token names; UF-129's
   lane is the reason). The question text is linted at build: no span
   substring, no 4-gram of the gold line, no path fragment of 6+ chars, no
   3+ digit run matching the answer's digits (the compaction-eval lesson:
   the expected value in the command, memory/runs/compaction_eval/
   STAGED_RUN_RECEIPT_20260920.md:20-26).
4. **The map-only check makes bytes mandatory:** the question's anchor terms
   plus its zone filter must NOT uniquely identify the gold row in
   path+title space. Either the map returns 0 metadata hits (miner must
   browse by zone) or 2+ candidates (miner must corpus_get and read to
   disambiguate). Distractor law inherited from the promoted spec: at least
   3 same-zone files share the anchor topic but not the span.
5. **Zones: exactly 5 x 10, chosen by live-recomputed counts.** I recomputed
   every row's zone with the live `mag.catalog_scan.zone_of` and found 3,233
   stored zones the live map disputes (1,607 lsa-to-code, 1,151
   lsa-to-watch, 313 ext:local_sovereign_-to-lsa, plus small tails):
   incremental rescan never recomputes zone for unchanged rows, so the stored
   zone column drifts. The eval's zone axis therefore computes zone from the
   live function, not the stored column. Top-10 in-repo zones by corrected
   count, floor 50 rows and 5 settleable files: memory 209,771; lsa 179,089;
   runs 46,749; intake 10,332; watch 5,649; code 1,673; queue 731; doctrine
   526; dashboard 447; research 87. Reserve: astra 76. No ext slot at seal
   time because sibling bytes are un-servable: measured live,
   `corpus_search("azerothcore", zone="ext:azerothcore-wow")` returns fts5
   hits, but `corpus_get` on both returned hit paths answers ok False
   "refused or missing" (tools/corpus.py:79-98 strips only the
   local_sovereign_agent/ prefix and confines to REPO). An ext question would
   be unsettleable through the sanctioned surface, so ext is a conditional
   promotion slot after the sibling-serve fix, never a title-token slot. The
   catalog zone is excluded by scanner law (EXCLUDE contains "catalog",
   mag/catalog_scan.py:87-88; 0 rows by design). If a zone cannot furnish 5
   unique-span questions at seal time, the zone is swapped from the reserve
   BEFORE the seal commits; the v1 shortfall-after-the-fact (48 of 50,
   attributed in B2-186) is not repeatable because the floor is a
   precondition, not a post-mortem.
6. **The seal (held-out discipline):** the builder draws 50 from a pool far
   larger than 50 using an operator-held seed and writes gold to
   `C:/Users/foste/.mag_holdout/uf122/gold_v2.jsonl`, which is outside the
   walk root (ROOT is C:\Users\foste\Documents\projects,
   mag/catalog_scan.py:83) so no rescan ever indexes it (verified this
   session: the directory does not exist yet), outside the repo so git never
   carries it, and unreachable by corpus_get, which confines to REPO. In-repo
   land only: `eval/uf122/questions_v2.jsonl` (zone, question, span class;
   no answer, no path) and `eval/uf122/commitment_v2.json` (sha256 of the
   gold file, row count, sealed_ts, sealer) so the seal is verifiable
   without opening it. The seed is never published (B2-186's published seed
   is the exact anti-pattern: regenerable gold is not held out). Grading
   runs in a separate session that reads the sealed file; receipts carry
   question id, verdict, cited path, and NOTHING else, so answer spans never
   enter the repo even after grading (a graded-once leak would rot every
   future run). Stated residual risk, plainly: a malicious miner with repo
   access could run the public builder and enumerate the candidate span
   space. The seal's adversary model is accidental inclusion (indexing,
   prompting, receipt-quoting), not exfiltration; the gate this eval serves
   (the C7 mining law, salon line 87-88: mining survives only as the
   retrieval reading) evaluates retrieval configurations whose operators
   have no incentive to cheat themselves.
7. **Arms, including the honest null:** Arm T (treatment) is an agent or
   pass answering through the real dispatch surface (tools/__init__.py:36-39
   corpus_search/corpus_get/corpus_tail/corpus_stats), budget 8 searches +
   8 gets per question, offline by harness law. Arm G is the grep null from
   S3's falsifier (salon line 155: raw substring search over the walk root,
   no catalog) at an equivalent open-file budget; this is the bar the 12x
   claim must actually clear, and it can fire. Arm M is the map-only
   ablation (search, no get): it cannot produce spans by construction, so
   any span-correct answer in Arm M is leakage proven and the seal is void.
   This makes the leak detector a standing arm of the eval itself.
8. **Rubric (inherits the promoted two-part shape, adds the estate's honesty
   laws):** primary citation recall, gold path cited AND actually served by
   corpus_get in the recorded trace (a cited-but-never-served path is a
   fabrication flag and the run FAILS the gate regardless of score; the
   no-fabrication law). Secondary span exactness, normalized match
   (casefold, whitespace collapse) so citation-fishing without reading
   cannot win. Abstention ("cannot settle", no citation) scores 0 on recall
   but is reported separately; an arm abstaining above 20 percent is
   degenerate and the instrument refuses to crown it (the compaction-eval
   v2 steal: the instrument is honest in both directions). Retirement: gold
   file sha256 mismatch or disappearance at grade time retires the question
   unscored; more than 10 percent retired means the seal is stale and no
   gate verdict issues until re-seal (the C6 law applied to the eval
   itself; the map rots by append, so a static eval would rot with it).
9. **The gate on mining passes:** any change that alters retrieval behavior
   (catalog schema, FTS index config, corpus.py search semantics, tags
   rules, ranking) must attach an eval receipt before landing. Gate: median
   citation recall of 3 runs at or above baseline minus 4pp (2 questions at
   n=50, the stated noise tolerance), zero fabrication flags, abstain at or
   under 20 percent. The baseline is recorded before the first mining pass
   (the WANTS row's own done-looks-like, watch/WANTS.md:40-41) and moves
   only upward (the ratchet's amend-not-rewrite analog); a re-seal resets it
   via one side-by-side run of old and new seals. B2-186's 1.0-vs-0.083
   result is re-labeled an index self-test: useful as a tool regression
   check, invalid as the UF-122 gate.

**Tags v2 owner-column rule** (the card's second deliverable, the salon S7
condition 2 and watch/WANTS.md:38-39): every row of catalog/tags.jsonl
(current schema measured this session: id, path, zone, kind, age_class,
bytes; no owner, no created) gains `owner` and `created`. Owner names the
tagging authority so no tag is born unowned: the mechanical pass writes
`mag.catalog_tags#2` (mechanical does not mean unowned; the rule-set version
is attributable, so a bad rule is rollback-able by owner), seats write their
lane id, the operator writes `operator`, and UF-122's builder writes probe
tags as `uf122` so eval-planted rows are attributable and sweepable by owner
(the C5 consumer law). `created` is the ISO UTC of first assignment, carried
forward across passes while (id, kind, owner) is unchanged; a kind
transition writes a fresh created plus `prev_kind` (supersede, never silent
mutation); age_class stays volatile and outside identity. Tags v2 also
recomputes zone through the live zone_of, which repairs the 3,233-row zone
drift inside the tags plane (the catalog row drift is a rescan defect, filed
below). Compatibility is byte-checked: the kind join in corpus_search reads
only row.get("kind") (tools/corpus.py:240-255), so the join stays green
untouched; the rule pins extend tests/test_catalog_tags.py with owner and
created presence, carry-forward, and transition rows.

## Moves with estate paths

1. **Supersede the B2-186 eval with the sealed v2 spec:** builder lands as
   `tools/uf122_seal.py` (span oracle, class regexes, leakage linter,
   map-only check, zone floor, draw, seal write, commitment publish),
   runner/grader as `tools/uf122_run.py` (arms T/G/M, budget enforcement,
   trace recording, rubric, retirement). In-repo surfaces:
   `eval/uf122/questions_v2.jsonl` + `eval/uf122/commitment_v2.json`; gold
   at `C:/Users/foste/.mag_holdout/uf122/gold_v2.jsonl`, outside the walk
   root named at mag/catalog_scan.py:83.
   `watch/inbox/burn_wave_20260926/B2_186_uf122_eval.py` and its results
   file are re-labeled index-selftest and excluded from future gold draws
   by the span-uniqueness oracle itself (their spans now exist in 2+
   places). Touches the WANTS row at watch/WANTS.md:40-41 (B2-186 does not
   satisfy it; the WANT stays open until the v2 baseline is recorded).
2. **Zone axis by live zone_of with the measured top-10 and floor:** the
   builder imports mag.catalog_scan.zone_of rather than trusting the stored
   zone column (3,233-row drift measured this session); ext slot conditional
   on the sibling-serve fix in tools/corpus.py:79-98; catalog zone excluded
   by the scanner's own EXCLUDE law at mag/catalog_scan.py:87-88.
3. **Leakage laws as build-time machine checks:** span classes + path/title
   exclusion + catalog-id exclusion + secret-path exclusion + question
   linter + map-only check, plus the standing Arm M ablation and a
   corpus-blind probe (a no-tool model pass over the 50 questions; 2 or
   more correct spans voids the seal). Offline everywhere; no arm, builder,
   or grader touches the network.
4. **Tags v2 owner+created rule:** schema and carry-forward law above;
   pins extend tests/test_catalog_tags.py; kind join compatibility verified
   against tools/corpus.py:240-255; probe tags under owner `uf122` so the
   eval's own annotations are attributable and sweepable.
5. **Gate wiring:** eval receipt required for retrieval-behavior landings;
   median-3 vs baseline ratchet, fabrication fails the run, abstain ceiling,
   retirement and re-seal policy. Pre-push hook wiring is an operator
   decision under the existing hooks law (AGENTS.md build discipline), filed
   as owed, not assumed.

## Falsifier

My own kill conditions, each runnable:

- **Leakage falsifier:** run Arm M (map-only, no bytes) and the corpus-blind
  probe over the sealed 50. Any span-correct answer in either, or 2+
  correct in the blind probe, proves a question answerable without the
  corpus: the seal is void, the draw is burned, the builder's linter is
  convicted on the surviving row ids.
- **Held-out falsifier:** attempt to reach the gold from every sanctioned
  surface: corpus_search over the holdout path name (must miss: outside the
  walk root, never indexed), corpus_get on the absolute path (must refuse:
  confinement), and grep of the repo for any gold span (must miss). Any hit
  kills the seal's placement.
- **Claim falsifier (the lane's own):** the map+tools claim dies if Arm T
   does not beat Arm G (the raw grep null) on median citation recall over
   the same 50. B2-186's 12x was measured against a name-prior strawman;
   against grep, a small or negative gap is a live possibility and the
   eval's purpose is to survive or die on it honestly.
- **Zone falsifier:** rerun the live zone_of census at seal; if any of the
  10 chosen zones falls below the 50-row or 5-file floor, the zone swaps
  from reserve before the seal commits (no post-hoc shortfall).

## Owed

- **Landing the code:** this card delivers the spec (the lane's own law:
  "Output: the spec, not the questions"); tools/uf122_seal.py and
  tools/uf122_run.py are specified but not written or run this session, so
  the 50-question seal, the baseline number, and the Arm T/G/M comparison
  are all unexecuted. Nothing above claims a score.
- **Operator custody of the seed and the sealed gold:** the sealing session
  publishes the commitment and hands the holdout to the operator; the seed
  is never written into the repo (B2-186's published seed is the
  anti-pattern being repaired).
- **Sibling-serve fix** (corpus_get on ext: paths, tools/corpus.py:79-98)
  before the ext zone can take its slot; until then the top-10 in-repo
  zones carry all 50.
- **Zone-drift repair in the rescan itself:** incremental rescan
  (mag/catalog_rescan.py) never recomputes zone for unchanged rows (3,233
  measured mismatches); tags v2 repairs the tags plane, the catalog row
  plane needs its own fix, not filed here.
- **Pre-push gate wiring** for the eval receipt (operator decision under the
  hooks law), and the WANTS row update recording that the retrieval-eval
  WANT stays open until the v2 baseline exists.

Kill risk, self-rated: this ships as a spec with measured feasibility probes
but no landed, executed 50-question run; a judge demanding the executed
baseline this window kills it, and the spec's own held-out placement
(outside the repo) is unverifiable from repo bytes alone at review time,
which is by design but costs verifiability.
