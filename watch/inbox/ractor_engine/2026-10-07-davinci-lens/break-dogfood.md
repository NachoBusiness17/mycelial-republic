# break-dogfood.md - hostile second pass on the dogfood lens (2026-10-07 da Vinci refire)

Subject: watch/inbox/ractor_engine/2026-10-07-davinci-lens/dogfood.md (filed Oct 6 23:49),
findings F1-F5 plus six blind spots. Pass instrument: every evidence cite re-run or
re-read THIS sitting (moment 2026-10-07 ~00:30-01:15Z local window, tree shared and
moving). Nothing accepted from the lens's own claims without an independent re-run; the
only CONVERGENT reliance is named inline. Instruments: file reads, greps, one sha256sum,
two citation_lint runs, one git check-ignore, one registry grep. Zero subprocess spawns
of mine exercised the win32 CREATE_NO_WINDOW law.

## Verdicts

### F1. Two fires died on the args-loss bug; the engine still accepts an undefined topic (gala/engine organ). CONFIRMED.

- Receipt cites byte-exact: watch/inbox/ractor_engine/ractor-topic/dogfood.md:3-4 reads
  "Topic arg: `undefined` (the engine passed no topic; same as the 2026-10-02 run" and
  watch/inbox/ractor_engine/ractor-topic/accuracy.md:3-4 reads "Topic arg arrived
  undefined" (the receipt this run's accuracy.md:3-5 points at). Both dead fires'
  write-ups sit in ractor-topic/ beside dogfood_20261002_prior_run.md (ls this sitting).
- Script bytes exact: .zcode/workflows/ractor-engine.dwf.ts:85 builds SLUG from
  `args.topic || "topic"`; :140-143 selects lenses and :143 logs "Riding N lenses on: "
  without any fail-closed check; topic is declared at :29. I read the full 362-line
  script this sitting: no topic guard exists anywhere in it, which cures the lens's own
  blind spot 6 (it had read only the named sites).
- Gate teeth absent: re-ran `grep -rn -i "topic" tools/workflow_gate.py` this sitting,
  zero match lines. configs/workflow_gate_scenarios/ holds exactly nine cards (G1
  multiplicity, G2 passoff, G3 steering, G4 salvage, G5 deliverable, G6 receipts, G7
  laws, G8 width_exception, G8 width_shape) and none is topic-shaped.
- Mtime: ls reads .zcode/workflows/ractor-engine.dwf.ts at Oct 5 20:53, matching the
  lens claim. One precision defect the lens should absorb: "before the dead fires" is
  true only of the second dead fire. The 2026-10-02 fire predates the current bytes.
  Registry digests sharpen it into a stronger fact: memory/workflows/REGISTRY.jsonl
  rows read digest 45790164653b (2026-10-04T10:22:52Z submit), then digest d8d63f619ab9
  on both 2026-10-06T00:53:10Z and 2026-10-06T22:29:05Z submits. So the args-loss bug
  SURVIVED the Oct 5 rewrite, and the same bytes rode the second dead fire and this
  refire. The structural claim stands; the timeline sentence was loose.

### F2. The founding primary is banked in the shared inbox and invisible to the librarian (librarian organ). CONFIRMED.

- Primary: _checks/pg5000.txt reads 1433832 bytes and 32784 lines, sha256sum
  83e79e107270ea7cbbc4b478913978738ae3d763081e54bc173a663d08ca5b10, matching the pin at
  accuracy.md:20. Salai anchors byte-exact on the pinned hash: grep -n returns
  :30302 "Giacomo came to live with me on St.-Mary" and :30310 "of the fact.--Thief,
  liar, obstinate, glutton." (sed 30300-30314 read this sitting confirms the passage).
- Catalog census reproduced exactly: mtime Oct 6 03:36 (ls -la catalog/catalog.jsonl);
  wc -l reads 1130965 rows; grep -c pg5000 = 0; grep -c watch/inbox = 47000;
  grep -n -i "vinci\|leonardo" returns exactly 6 rows (:438367, :438368 shown by the
  lens; the full set is :438367, :438368, :438375, :438596, :438597, :438598, all
  alpaca_eval text-davinci configs in one tree, so "the other 4 sit in the same tree"
  is true). The only da Vinci the librarian knows is an OpenAI model name: byte-true.
- Falsifier attack: the corpus_search clause I could not run directly (see Not run);
  the structural proof carries it: the search index is built from catalog rows and the
  catalog holds zero pg5000 rows, so no catalog-backed search returns the notebooks.

### F3. The tri-state accuracy law is oral: order text and run prose, zero boot surfaces (percolator organ). CONFIRMED.

- Exact-scope grep reproduced byte-exact: `grep -rn -i "INTERPRETIVE\|ELABORATED"` over
  mag/, tools/, configs/, memory/law/ (include *.py *.json *.yaml) returns exactly one
  hit, tools/oral_law_dedupe.py:11, the unrelated wording-drift comment.
- Instrument gap cured, absence survives: the lens's claim was "zero law surfaces the
  seats boot with" but its grep skipped memory/rib/, memory/rib_boot.json, state/ and
  docs/ (all load-order surfaces per AGENTS.md). I re-censused them this sitting: every
  hit is unrelated prose (memory/rib/RIB_CASTLES_FOUNDATIONS_20260810.md:23 story-pane
  row, state/arxiv digests, docs/ref/canon texts, state/fuel/record_briefs.jsonl rows);
  no tri-state law row anywhere. grep -i "interpretive\|elaborated" on
  memory/law/registry.json exits 1 (zero rows). The claim is true on a wider instrument
  than the lens ran; the quantifier law is satisfied by this pass, not by the lens.
- Instrument half wired: githooks/pre-push:24-25 run citation_lint check --changed with
  exit 1 on failure. Cites at state/CURRENT.md:55-56 (publish-time re-derivation law,
  no instrument attached) and ractor-topic/dogfood.md:103-105 (yesterday's identical
  finding) are byte-exact.
- Lint claims reproduced: my run of `.venv/Scripts/python.exe tools/citation_lint.py
  check --files .../accuracy.md` prints "ok records=1 anchors=12 numbers-checked=2
  blocking=0 warns=4", exit 0, exactly the output claimed at accuracy.md:142-145; the
  same command on dogfood.md prints "ok records=1 anchors=21 numbers-checked=0
  blocking=0 warns=5", exit 0, matching the reported move's "exit 0, blocking=0,
  21 anchors" and corroborating the lens's Close claim (the result line lives in the
  run submission, not the file; my re-run makes the number byte-backed here).

### F4. The lens library is an inline Record in a gitignored script (context pack organ). CONFIRMED.

- .zcode/workflows/ractor-engine.dwf.ts:89-116 is the LENS_LIBRARY span (comment at
  :89-90, const at :91, close brace at :116); the dogfood persona sits at :104-105 as
  cited. `git check-ignore -v` returns ".gitignore:200:.zcode/
  .zcode/workflows/ractor-engine.dwf.ts", exit 0, and .gitignore:200 reads ".zcode/".
- No tracked home: grep -rln "LENS_LIBRARY" over mag/, tools/, configs/ returns zero
  (exit 1). memory/lenses/ holds exactly corpus_index.json, default.json, grok-free.json
  (ls this sitting), a different organ as the lens said. Falsifier empty: git ls-files
  shows no tracked file the script imports for LENS_LIBRARY; the full script read shows
  it imports nothing (self-contained const).
- The move is undersized, not wrong: see Addition 4. The estate already runs a tracked
  ractor-persona organ, corpus/ractor_ribs/ (16 persona dirs: BAUDRILLARD through
  WALLAS, each with case_law.jsonl and invariants.md, tracked per git ls-files; grep
  -ci leonardo over the tree = 0), plus tracked skill files (.agents/skills/elder-lens/
  SKILL.md). configs/ractor_lenses.json invents a second convention where one exists.

### F5. No wired X hand; the attention market holds zero rows for this order (attention market + transport organ). WEAKENED.

- Confirmed half: grep -n -i "vaultmother\|davinci\|leonardo" memory/attention.md exits
  1 at my moment (zero rows; the open-loop hazard is still live, nobody has filed the
  row yet). The X_INTEL_* receipts exist (ls watch/inbox/ shows at least five). The
  Amenti precedent cites are byte-exact: watch/inbox/AMENTI_TRANSLATION_20261005.md:35
  is the "Paste-ready reply (her register, first person...)" header and :51-53 is the
  lines-held no-endorsement close. THREAD_POSTS_v0.md (Oct 6 23:55) is NOT the
  self-contained paste bundle the move asks for: it cites estate-internal paths
  (:47-48, sources/pg5000_richter_notebooks.txt) and its OWED (:54-58) holds the
  verbatim bank open, so the move survives unchanged.
- Killed half: "the estate has no wired hand: X is sensing-only ... no X egress exists
  to bridge" is a universal claim carried by tools/-scoped instruments (ls tools/ grep
  = zero, re-run exit 1; grep api.x.com/api.twitter over tools/ = zero). My wider
  census over mag/ and scripts/ returns two files: mag/x_oauth.py, a full X WRITE
  client (docstring :15 "python -m mag.x_oauth post", POST_URL
  "https://api.x.com/2/tweets" at :49, SCOPES including tweet.write at :51, media
  upload at :268, reply at :288, delete at :327-333) and mag/x_control_surface.py:464
  defining post_to_x(). The lens's own falsifier was scoped to survive it ("an
  X-output tool appearing under tools/"), but the finding text is universal and dies
  by the quantifier law the lens itself quotes. What survives: no tools/ lane posts,
  x_oauth requires user-context OAuth keys (its :3 docstring), and no sanctioned
  effect path exists for THIS order; the transport story is "a posting client exists
  in mag/, unkeyed-into-this-order", not "no hand exists". Whether user-context keys
  are banked I did not check (secrets; see Not run).

## Blind-spot adjudication

- BS2 (her thread text unread) is STALE and, five minutes after filing, false:
  _checks/x_thread_fetch_20261007.html (banked Oct 6 23:54, dogfood.md filed 23:49)
  carries her verbatim sentences at :86-88 ("I loved someone named Salai. Andrea
  Salaino. He came to me at 10 years old ... I kept him around for 25 years." and
  "He was my mirror ... the only person who was not afraid of me."), with the same text
  in the og:description meta at :9/:13. THREAD_POSTS_v0.md (moonshot-1's independent
  WebFetch, 23:55) converges on the same lines. This kills the accuracy lane's F3
  premise as a run-level fact: its own falsifier ("an unauthenticated curl returning
  the thread's text in the response body") triggered in the same run directory. The
  register mapping no longer rests only on the operator briefing; reply bodies remain
  truncated (THREAD_POSTS_v0.md:26-35) and the verbatim bank stays partially OWED.
- BS1 (settings-only-amend locus outside repo bytes): stands; I did not read harness
  surfaces either. Honest as written.
- BS4 (crawler scope unknown): resolved this sitting, see Addition 5.
- BS6 (partial script read): cured by my full read; no hidden guard exists.

## Additions

1. Thread text is in-run: the "operator briefing only" caveat is superseded by bytes
   the same run banked. Evidence: _checks/x_thread_fetch_20261007.html:86-88 plus
   THREAD_POSTS_v0.md:19-24 convergence on "il Salaino :: little devil", 25 years,
   mirror, not-afraid. Falsifier: both fetches carrying crawler placeholder text rather
   than her post (the og:description and article body would then diverge; they do not).
   Move (10 min): promote the verbatim Salai lines into the rebuild manifest's voice
   protocol with fetch-mode labels, and retire the briefing-only caveat from the kit.
2. The X write hand exists in mag/: F5's universal is dead. Evidence: mag/x_oauth.py:49
   and :51, mag/x_control_surface.py:464. Falsifier: those files being unwired to any
   surface or keyless in practice (key state unverified, secrets). Move (5 min): rewrite
   F5's transport claim to "posting client exists in mag/, user-context OAuth required,
   no sanctioned effect path for this order"; keep the attention-row move.
3. The schema guard already exists and already failed: .zcode/workflows/ractor-engine
   .dwf.ts:32 declares topic `required: true`, and two dead fires rode anyway. Evidence:
   the declaration plus ractor-topic/dogfood.md:3-4. Falsifier: a harness that enforces
   required args at fire time. Move (0 min, fold into F1): cite :32 in F1's evidence so
   the cure is specified as runtime fail-closed, preempting the "the schema already
   requires it" objection.
4. A tracked ractor-persona organ already exists: F4's move invents configs/ractor_
   lenses.json while corpus/ractor_ribs/ holds 16 tracked persona dirs with
   case_law.jsonl + invariants.md and no LEONARDO. Evidence: git ls-files + ls
   corpus/ractor_ribs/ this sitting. Falsifier: ractor_ribs being dead bytes no seat
   consumes (I verified tracking, not consumption). Move (10 min): land the da Vinci
   lens card as corpus/ractor_ribs/LEONARDO/ or extend F4's move to justify the second
   convention.
5. The crawler-scope OWED resolves YES: mag/catalog_scan.py:87-88 EXCLUDE = {".git",
   ".venv", "venv", "node_modules", "__pycache__", ".mimosa", ".ruff_cache",
   ".pytest_cache", ".idea", ".vscode", "catalog"} and :246 skips EXCLUDE plus dot-dirs
   only, so _checks/ is in walk scope. Evidence: the file read plus the 47000
   watch/inbox catalog rows proving the inbox is historically crawled. Falsifier: the
   scan ROOT not covering watch/ in this layout (root not traced by me). Move (part of
   F2's 20 min): the seed row is the fast path; the next sanctioned crawl also lands it.
6. The kit ships a forked anchor set: the two lanes cite different line ranges for the
   same passage on the same hash (dogfood :30302/:30310, byte-exact; accuracy.md:31
   ":30303-30312", off by one at both ends). Evidence: sed -n '30300,30314p' on the
   pinned file this sitting. Falsifier: any third reading of the same hash. Move
   (5 min): the rebuild manifest pins ONE canonical anchor set (dogfood's) per hash.
7. The primary is dual-banked under two names: _checks/pg5000.txt and sources/
   pg5000_richter_notebooks.txt are hash-identical (same sha256, computed on both this
   sitting). Evidence: sha256sum outputs. Falsifier: a hash divergence (none). Move
   (part of F2's 20 min): register one canonical row (path + hash), not two.

## Not run / OWED (marked, never asserted)

- corpus_search falsifier clause: mag/corpus_query.py exposes no CLI (grep for
  argparse/main/__main__ returns zero); I ran no FTS query. F2 stands on the catalog
  zero-row census, which the index is built from.
- The catalog scan ROOT (walk start) not traced; only the EXCLUDE rule and the
  historical 47000-row inbox coverage are verified.
- External history verdicts (Codex Leicester terms, 1476 record, Amboise itinerary,
  Ceceri legend): not re-run; out of this pass's scope. I verified only that the cites
  dogfood relies on (accuracy.md:20, :39-40, :67-79, :118-127) carry the claimed text
  at the claimed lines.
- Whether mag/x_oauth.py holds banked user-context keys: not checked (secrets).
- A memory/-wide persona-string sweep: launched this sitting, abandoned unfinished
  (slow tree); non-essential, since F4's claim scope was mag/ and tools/ and both were
  verified zero.
- Sources/ doors (pg28420_vasari_lives_vol4.txt, codex_flight_of_birds_1893_djvu.txt):
  presence verified by ls; contents not read by this pass.

## Close

Em-dash census on this file: zero (grep count of the U+2014 byte sequence returned 0 at
close). Citation lint on this file at close: `.venv/Scripts/python.exe
tools/citation_lint.py check --files
watch/inbox/ractor_engine/2026-10-07-davinci-lens/break-dogfood.md` printed "ok
records=1 anchors=22 numbers-checked=1 blocking=0 warns=6", exit 0; the 6 warns are
TOKEN-MISS heuristics plus one SHORTHAND-UNRESOLVED on the ".dwf.ts" bare basename in
Addition 3, WARN-only by the standing mode. Verdict line: 4 confirmed, 1 weakened,
0 killed; 7 additions.

Filed by break-dogfood, hostile second pass, 2026-10-07, one seat one sitting.
