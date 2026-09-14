# DEEP RESEARCH SALON BRIEF — wiring the infinite library (2026-09-05)

Operator commission, verbatim: "between scribd and the internet archive we
have infinite training data and need to be using it. arxiv etc. all of it.
we have a vision model and a board concept. we need to salon it and figure
out how to wire it all together. deep research salon project/debate."

## WHAT THE FLEET ALREADY HAS (receipted, the wiring components)

### SOURCES (supply side)
- **arXiv**: free, API-friendly, license-varies per paper; today's
  preservation sweep already pulled 9 PDFs cleanly (literal-URL door).
- **Internet Archive**: millions of public-domain + lending-library books,
  stable URLs, has a SEARCH API (archive.org/advancedsearch.php) and
  full-text search inside books; public domain = unambiguous custody.
- **Scribd**: the contested shelf — user-uploaded documents, subscription
  wall. LEGAL STATUS per rival counsel (LEGAL_MEMO_002, VINDICATED):
  blanket-scrape bans are overbroad, copyright-clean for method≠expression,
  CFAA clean (Van Buren/hiQ screen-reader family), BUT contract is the bite:
  Scribd ToS prohibits scraping = LAW-055 territory. The debate must price
  this honestly: what's the legal posture for Scribd vs IA vs arXiv?
- **Plus what today proved**: gitingest (repo digests), raw.githubusercontent
  (the door that beats walls), Gutenberg, wikisource, mirtitles — the free
  shelf is deeper than the three named sources.

### PROCESSORS (the eyes and hands)
- **Vision model**: GLM-4.6V-Flash 9B local (zai-org weights, runs on our
  68.7GB box tonight); eyes-receipt proven (blind fails, vision reads exact);
  PNG-retina precedent (seats steer from rendered images). Vision = the
  scanner for scanned/image PDFs that text extraction can't read.
- **Text extraction**: gitingest for repos, pdftotext-class for digital PDFs,
  chain_index_completion pattern for batch processing.
- **The GA/gene pool**: the selection machinery — preserved sources become
  genes, falsifier-attached sources outrank assertion.
- **The light thesis**: frontier reads once, dumb agents navigate the
  corpus by the stored light (embeddings/index instead of re-reading).

### SURFACES (the board)
- The operator's "board concept": decks + control room + falsifiers.html —
  the browsing/visualization layer where the corpus becomes legible.
  rtfm_graph.html proves the pattern: private knowledge graph, browsable.
- Question for the salon: is the board the BROWSER of the library, the
  TRAINING-DATA dashboard, or the READING interface? (Probably all three,
  staged.)

## THE LAWS THAT BIND (non-negotiable constraints)
1. Loopback law: harvesting machinery runs local, never as a service.
2. LAW-055 + LEGAL_MEMO_002: no violating posted ToS bans (Scribd's wall is
   contract); IA/arXiv public paths are clean; method-vs-expression
   distinction governs what's training-usable.
3. Preservation law: every source cached, hashed, manifest-linked.
4. Backup-first: corpus surgery seals first.
5. The duplication law: the library will contain duplicates; emphasis
   weighting, never culling.

## THE SALON'S QUESTIONS (the wiring debate)
1. **SOURCE PRIORITIZATION**: order the library build — IA public-domain
   first? arXiv by citation-graph crawl? Scribd: (a) skip entirely,
   (b) manual-operator-curated only (his Google-tap hands), or (c) something
   sharper? Give the legal posture per source, tri-state.
2. **THE EXTRACTION PIPELINE**: scanned/image PDFs → vision model (GLM-4.6V
   local, free, slower) vs digital PDFs → text extraction (fast, cheap).
   What is the batch architecture? What throughput is honest at $0? What is
   the queue/claim pattern (the auditor found consumption-starvation — how
   does extraction avoid the same trap)?
3. **THE VISION ROLE**: exactly when does the vision model engage? (OCR
   fallback? Figure/diagram understanding? The PNG-retina pattern for
   dense pages?) What does vision cost per page honestly, and what does the
   eyes-receipt say about accuracy?
4. **THE BOARD**: what does the operator actually SEE — a library browser
   (rtfm_graph style)? A training-data pipeline dashboard (deck)? A reading
   surface? Propose the minimal v1 board with its falsifier.
5. **THE TRAINING WIRE**: how does extracted corpus become training data —
   the QLoRA campaign's Stage 2/3 substance gates, the gene pool's fitness,
   the light-thesis broadcast? Where does the corpus live (files? the
   chain? embeddings?) and what is the recovery story?
6. **THE HONEST BOUNDARY**: what does this project NOT solve (copyright on
   non-public-domain books, Scribd's wall, storage ceilings at 3GB memory
   already 50% stale)? Name the failure modes including legal ones.

Deterministic proposals, named falsifiers, tri-state claims. The laws above
bind every proposal — a wiring plan that violates loopback or LAW-055 is
rejected pre-hoc.
