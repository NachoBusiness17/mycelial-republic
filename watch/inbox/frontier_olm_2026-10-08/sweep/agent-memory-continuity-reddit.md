# Sweep: agent-memory-continuity via reddit (frontier_olm_2026-10-08)

source-fetched: 2026-10-08. Seat: sweep-agent-memory-continuity-reddit. Area: agent memory
continuity (knot promotion, identity keys, ledger writer, compaction continuity, embeddings
vs keyed lookup).

## Doors (exact, no fabrication)

- Reddit direct: BLOCKED. `old.reddit.com/*/top.json` and comment pages return a
  login-wall placeholder to WebFetch; `www.reddit.com` returns HTTP 403; `r.jina.ai`
  proxy over old.reddit also returns Reddit's network-policy block. Zero thread bytes
  came from reddit itself this sitting.
- Working door A: `api.pullpush.io/reddit/search/submission/?ids=<ids>` (public archive,
  no auth). Returns created_utc, selftext, permalink. Worked on every call; the bulk
  `?ids=` list is capped (HTTP 400 at 14 ids, OK at 5-6). The archive has NOT indexed
  the freshest posts: `1wztoe2`, `1wzgr8b`, `1wyow7y`, `1ww2b90` all returned EMPTY.
- Degraded door B (per recipe): WebSearch `site:reddit.com` snippets. Works, with
  z.ai 1302 rate-limit bursts needing spacing. Unarchived threads (1wz*/1wy* band) were
  read ONLY at snippet grade through this door; flagged per item.
- Working door C: pullpush search endpoint (`?subreddit=..&q=memory&since=..`) is the
  instrument that would enumerate the full 30-day pool; it returned HTTP 429 on three
  tries spaced over ~25 minutes. Not obtained. So the in-window candidate census is
  thin by instrument, not by choice: 76 threads considered total, 20+ dated by
  pullpush created_utc, of which in-window (2026-09-08..2026-10-08) confirmed: 3
  archived (1wws6o6 Oct 4, 1wwna5h Oct 3, 1wldz7u Sep 21) plus 3 in the unarchived
  1wz/1wy ID band dated only by band position. The "30 in-window candidates" bar was
  NOT met on dated instruments; stating it plainly.

## Deep reads (what was actually fetched and read this sitting)

1. 1r8cnwq (8 agent memory systems) - pullpush full selftext (out of window, 2026-02-18;
   read for evidence, banked flagged as out-of-window).
2. 1wws6o6 (repopedia code knowledge graph) - pullpush full selftext.
3. 1wwna5h (Engram SQLite FTS5 memory) - pullpush full selftext.
4. 1wldz7u (Athena Ollama agent) - pullpush full selftext (weak item; not banked).
5. pi-optchat (1wzgr8b) - GitHub README fetched end to end
   (https://github.com/jonaslsaa/pi-optchat) plus search snippets of the thread
   (~150+ upvotes per search listing).
6. 1wztoe2 (147 rules) - search snippets only (thread unarchived, reddit blocked);
   snippet-grade, flagged.
7. 1wyow7y (mem0 vs Memori) - search snippets; thin question thread; not banked.

## Banked items (strongest first)

### 1. "147 rules live in my agent's memory file. 71 of them are cited by nothing in code" (r/LLMDevs 1wztoe2)

Verbatim (search snippet): "147 rules. 76 are cited by at least one file that runs. 71
are cited by nothing. cited doesn't mean enforced. uncited does mean unenforced"

Direct external analogue of lens/graph.md:25: 162 of 400 knots share one label and 379/400
are isolated; here 71/147 memory rules are cited by nothing. The proposed mechanism is a
citation-existence audit over memory rules, and its asymmetry is the steal: uncited
GUARANTEES unenforced (deletable or wire-it), cited does NOT guarantee enforced (that
needs behavior evidence). Mapped to Q1: the cheapest knot-promotion instrument is exactly
the P1 cite-allowlist gate's whole-repo path verification (frontier_olm_2026-10-08/lens/
burns.md:115-116) pointed inward: a knot label/claim gets an edge when a module, doctrine
row, or receipt cites it by resolvable path; knots that nothing cites are retire
candidates, not priors. Q2 gets the same answer shape: the identity key is the citation,
not a smarter label.

Overlap grep this sitting: "147 rules" 0 hits in catalog/catalog.jsonl; "cited by nothing"
0 hits; "uncited" untested. Adjacent banked estate work (do not re-derive): P1
cite-allowlist gate + citation_lint PHANTOM-NUMBER (commit 6685db6bc), census-carrier
tripwires. Delta: applying the gate's direction to memory-graph priors instead of pushed
prose.

### 2. pi-optchat: endless chat as a summary tree (r/PiCodingAgent 1wzgr8b; README fetched)

Verbatim from fetched README: "Memory: every message is logged and summarized into a
binary tree." Also: "Each profile folder is a local Git repository, committed after each
turn and on clean shutdown."

Q4 evidence, the strongest continuity primitive found: instead of compaction, a bounded
memory view (sawtooth merges 128,000 to 64,000 bytes) over a summary tree whose originals
stay byte-addressable via zoom(id)/date/search; subagents launch with a frozen view.
Mechanism-level convergence with the estate's ReFold reversible sheds
(frontier_olm_2026-10-08/lens/burns.md:118-120, restore door proved 4290 chars) but
generalized to whole-conversation history and shipped with a per-turn git-commit log.
The per-profile JSONL + git repo is also an append-ledger answer to Q3: continuity state
committed after each turn is a writer instrument that already exists in the wild,
weakening the "no writer instrument exists" premise of the burns-ledger incident
(lens/burns.md:31-38) - the estate could mint a minimal writer from exactly this shape
(append JSONL + git commit per turn) without breaking amend-never-rewrite
(RIB_MD_RECORD_20260921.md:6-26 via lens/laws.md:33-34).

Overlap grep this sitting: "OptChat" 0, "pi-optchat" 0, "summary tree" 0, "endless chat"
0 in catalog. Adjacent banked: ReFold P5 (6685db6bc). Delta: originals-addressable tree +
frozen child views; ReFold sheds fold documents, OptChat folds conversation.

### 3. Engram: SQLite FTS5 + BM25 memory for coding agents (r/LocalLLaMA 1wwna5h, 2026-10-03)

Verbatim (pullpush selftext): "That is a small set, so it works as a regression gate,
not a benchmark." Also: "Everything is plain Markdown on your disk."

Q5 retire-class confirmation from a shipped tool, not a paper: recall path is keyed/lexical
(BM25 over a disposable FTS5 index rebuilt from markdown), embeddings strictly optional and
fused via reciprocal rank fusion only when a local model is present; no network at recall
time. Matches the estate's own falsifier result: string keys 100.0 percent vs
embedding-kNN 99.05, McNemar p=0.5, 60x over latency budget (lens/burns.md:129-131), and
the estate already runs the same instrument family (corpus FTS5 daily rebuild, AGENTS.md
B2-465). Steal candidate: the recall@5 >= 90 percent bar over 20 seeded queries as a
standing regression gate for corpus_search, and "index is disposable, markdown is the
store" as the durability law.

Overlap grep this sitting: "Engram" 38 catalog hits - ALL estate-internal collisions:
mag/engram.py (template+delta session compressor, read in full this sitting - a DIFFERENT
mechanism), memory/research_polished/memory_engram.md, riddler_engram.v1.json, plus
agent-session transcripts. The utsapoddar/engram FTS5 memory tool itself: not previously
banked. Delta survives the name collision.

### 4. repopedia: tree-sitter call graph in one SQLite file with an MCP server (r/LocalLLaMA 1wws6o6, 2026-10-04)

Verbatim (pullpush selftext): "grep tells who mentions it in the code base, not who
actually calls it." Also: "it asks the graph directly and gets the exact answer with
file:line in one call."

Q1 linker evidence: the property that makes a graph edge "verified" in this tool is that
every edge resolves to file:line, so the agent stops burning grep rounds. The estate's
knowledge_graph.v2 (2,938 nodes / 1,256 edges, lens/graph.md:4) has annotated edges but
no file:line-resolution duty on knot/doctrine/steal edges; a repopedia-style rule (edge
must carry a resolvable path:line, checked by the cite-allowlist gate) is a concrete
mint for promoting the 379 isolated knots. Q2: the caller/callee pair IS the identity
key - two nodes are distinct iff they resolve to different file:line, which is exactly
the collision-free key the 162 `autonomous_janitor` labels lack.

Overlap grep this sitting: "repopedia" 0, "call graph" 0 in catalog; "blast radius" 3
hits, unexamined (flagged, not cleared). Adjacent banked: graph.md lens work is the same
seam from the inside; day-7's ml3 GPS ROUTER (commit 19bac820a1) is the nearest estate
instrument.

### 5. "Analyzed 8 agent memory systems end-to-end" (r/LocalLLaMA 1r8cnwq) - OUT OF WINDOW, flagged

Date: 2026-02-18 by pullpush created_utc. Banked despite age because it answers Q2 with
the only named identity-key design found this sitting. Verbatim (pullpush selftext):
"Hindsight runs four retrieval methods in parallel on a single PostgreSQL database and
gets more out of it than systems running six containers." Also: "Graphiti has arguably
the best data model - bi-temporal edges, two-phase entity dedup with MinHash + LLM."
(second quote's dash normalized to ASCII hyphen).

Q2: the two-phase dedup (cheap MinHash blocking, then LLM confirm) is a mintable
identity-key design for the 162 duplicate `autonomous_janitor` knot labels: phase 1 =
payload-hash/nearest-neighbor blocking over knot text, phase 2 = model confirm, all
before any edge is minted. Q5: Hindsight running four retrieval methods over keyed
Postgres (not a vector DB) beating multi-container stacks is more keyed-lookup-wins
evidence. The "four architectural bets" framing (LLM-driven memory, explicit structures,
infrastructure-first, upstream data access) is a useful map for the estate's own
knowledge_graph vs warm_state vs zknot split.

Overlap grep this sitting: "Mem0" 1,652 and "Letta" 1,123 catalog hits (heavily mined
already - the systems themselves are known); "Graphiti" 3 hits including
watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/graphiti.readme.md (28,280
bytes, fetched 2026-10-01, catalog shows it); "MinHash" 0, "bi-temporal" 0, "analyzed 8
agent memory" 0 - the thread and its dedup detail are NOT banked. Confidence tempered by
age and by pullpush being a snapshot archive.

## Anti-rebank notes honored

- 1wlbqnl ("Building better memory for your agents", 2026-07-28) is ALREADY in the
  estate as register row 20 of the day-6 mine (40 percent of sessions made zero memory
  calls; watch/inbox/frontier_olm_2026-10-06/DIGEST.md section 3, read this sitting).
  Not re-banked.
- Day-6 memory-continuity confirmed set (arXiv 2610.03902 use-stage failures, 2609.36457
  consolidation tense-flattening inside mem0/Graphiti/Letta, cohorte belief retirement,
  C57 typed relations + C70 tiers from thread 1wl3828) was read this sitting from the
  day-6 DIGEST and none of it is re-claimed here; the banked items above are the NEW
  delta against that set.

## ERRATUM (appended after submit; late-arriving grep batch)

The first overlap grep batch completed AFTER the result was submitted. Its memory/-side
arms amend item 5's overlap claim: `grep -rl MinHash memory/` returns 2 hits, and one is
load-bearing - `memory/runs/engram_20260913/E06_associative_recall.md:7-9` already
specifies "256-perm MinHash of normalized task text" + "LSH banding (32 bands x 8 rows)
over MinHash - O(1) candidates, exact-Jaccard second pass". So the estate HAS a banked
blocking-then-confirm dedup design (the engram fold's recall index); what stays new in
item 5 is narrower: the thread's application of that shape to ENTITY dedup inside a
knowledge graph, plus bi-temporal edges. The catalog-side zeros I reported ('MinHash' 0,
'bi-temporal' 0 in catalog/catalog.jsonl) remain true as stated. Second hit
(memory/ghost/noise/ox_artifact.jsonl) is an incidental substring in a noise artifact,
not a design echo. 'bi-temporal' memory/-side hits are agent-session transcripts only
(orc-t07cf6a2b23, orc-t61dc81118b); 'extract-store-retrieve' hits
memory/trajectory/steps.jsonl once.

Second late batch adds trace-level ancestry only, no banked contradiction: the '8 agent
memory' and 'NOW.md' hits in memory/trajectory/steps.jsonl are sibling dwfrun session
traces, not artifacts - a 2026-09-29 seat ran the same dedup phrase list with hits=0
(line 33679) and a 2026-10-04 seat carried 1r8cnwq in its pass-1 candidate listing
(line 50589) without banking it (catalog title grep stays 0). Per the convergence law,
session-trace ancestry is not banked content; this seat's contribution to 1r8cnwq
remains the pullpush full-selftext read, with the engram-E06 delta narrowing above.

## Gaps / owed from this sweep

- The pullpush search endpoint (in-window pool enumeration) never returned; a re-seat
  with the same recipe should try it first, spacing calls.
- Threads 1wztoe2 and 1wzgr8b deserve full-body reads once reddit doors or a fresher
  archive are reachable; the 147-rules mechanism paragraph (how "cited" is counted) is
  snippet-grade only.
- Athena (1wldz7u) read but not banked: "It's still an experiment, not a
  production-ready platform" (verbatim, pullpush selftext); bounded-history + persistent
  memory framing adds nothing the day-6 set lacks.
