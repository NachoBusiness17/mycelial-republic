# INTAKE CARD — E_OPORE BACKEND ENGINEERING ROADMAP TREE + GUMROAD FUNNEL (X @e_opore, 2026-09-02)

Genome: research-socratic six steps (INGEST / MAP / ASSERT / ATTACK / MEASURE / CORRECT) per
docs/ref/verb_genomes/research_socratic.md + L0 contract. Spawned by operator paste, 2026-09-04.

## ITEM
https://x.com/e_opore/status/2094995862875217977 — "BACKEND ENGINEERING ROADMAP" by
Dhanian 🗯️ (@e_opore), published 2026-09-02T03:48:31Z. A 20-section ASCII tree of ~250
leaf-node topics: 01 CS Foundations → 02 Programming Fundamentals → 03 Choose Your
Language → 04 Web & HTTP → 05 API Engineering (REST/GraphQL) → 06 Databases
(SQL/NoSQL/Redis) → 07 Data Access → 08 Auth & Security (JWT/OAuth) → 09 Architecture
(monolith/microservices/event-driven) → 10 Caching → 11 Async Processing (retries,
idempotency, DLQs) → 12 Real-Time (WebSockets) → 13 File & Media → 14 Testing → 15
DevOps (Docker/K8s) → 16 Observability → 17 Scalability → 18 Reliability (circuit
breakers, bulkheads) → 19 System Design (CAP) → 20 Production Projects. Terminal line:
"Grab Backend Engineering Ebook: codewithdhanian.gumroad.com/l/ungqng" — the post's
only call to action.

## RECEIPTS
- webReader (attempt 1): root post captured full-text via X's crawler view (og
  metadata), title + published timestamp + full tree; no replies in that view.
  Attempt 2 on the twitter.com mirror: rate-limited (429) twice.
- WebFetch on x.com: timeout at 60s. X conversation = walled to this seat's fetchers
  this turn (three paths tried).
- WebSearch: independent hit on the post URL + the author profile — profile shows a
  Dec 26 2025 "COMPLETE FULL STACK DEVELOPER ROADMAP" in the same tree format. Author
  = serial roadmap-poster: Supported.
- THREAD LAW (Amendment 2) honored and walled: replies/community notes UNFETCHED —
  the crawler view carries the root only. Tri-stated below; not scored from them.
- Coverage falsifier ($0, grep over docs/ + memory/): "circuit breaker" 38 files,
  "idempoten*" 107, "OpenTelemetry/otel" 58, "exponential backoff" 17, "CAP theorem" 4,
  "dead letter" 4, "consistent hashing" 1, "hexagonal architecture" 0, "presigned" 0.
  (Raw "WAL" count 4386 is substring noise — matches "walk" in the maze-walker corpus;
  honest write-ahead-log coverage = the Desk salon gap filings, file-count tier ~4.)

## SCORE — F:1 P:0 C:3 W:1 N:0 = 5/25 → REJECT/REMEMBER band

## READ (the socratic middle)
[SOCRATIC] assumption attacked: "a detailed tree implies a curriculum" — it is a topic
INDEX (250+ nouns, zero links, zero resources, zero order-of-study edges, zero
exercises; "Redis" listed under both Databases and Caching — a category slip a real
curriculum would not make). Instrument: the $0 corpus-vocabulary grep spanning the
tree's two halves. What survives: the convergence datum below; the item as a teaching
artifact does not.

ASSERT (steel-man, one sentence): "A backend engineer becomes production-ready by
walking a complete ordered map of the field — CS foundations through 18 specialty
areas to 11 portfolio projects — and this tree is that map."

ATTACK (two named failure causes, with evidence):
1. TAXONOMY ≠ CURRICULUM — the payload is an index of nouns, not a teaching artifact.
   Evidence: the post's own text (no links, no resources, no depth markers; the Redis
   double-listing). Contrast: yesterday's AMISHA listicle (INTAKE_AMISHA_AI_ROADMAP_
   20260903.md, 6/25 REMEMBER) at least linked 40 real resources; this is the same
   genre strictly weaker. A checklist cannot produce an engineer; it produces the
   feeling of a plan — bookmark-farming without receipts (genre rule, three same-day
   data points as of 09-03, this is the fourth).
2. FUNNEL-SHAPED PAYLOAD — the tree is the free sample of a paid product. Evidence:
   the terminal gumroad CTA is the post's only action; the author's profile shows the
   same format deployed Dec 2025 on a full-stack roadmap. The ebook — the actual
   product — is paywalled and unaudited: Unproven.
3. (bonus, structural) The item claims nothing falsifiable — per L0 falsifiability it
   cannot enter the claim ledger above Unproven by construction.

MEASURE (ran, $0): corpus-coverage grep (8 distinctive terms, receipts above). Result:
the roadmap's operations half is strictly BELOW corpus coverage (we live idempotency,
circuit breakers, OTel, backoff as built organs — dispatch circuit breaker shipped
after the 09-03 board runaway); its theory-exam half (hexagonal architecture,
consistent hashing, presigned uploads, CAP) is corpus-thin but consumes nothing —
no live arc, lane, or opcode wants interview-exam nouns. One genuine convergence:
the tree's sections 11 (retries, idempotency, DLQs) and 18 (circuit breakers,
bulkheads) independently name the exact organs the Desk salon found missing in the
fleet's own loop (retry-dedup identity, WAL-before-side-effect) — an industry-canonical
beginner map arriving at our gap list is convergent confirmation the Desk backlog
ordering is the real curriculum. Calibration, not build: the roadmap adds zero
mechanism to gaps we already filed.

## TRI-STATE
- Post exists, content as quoted: **Supported** (webReader full-text fetch 2026-09-04
  + independent WebSearch hit on the status URL).
- Author is a serial roadmap-poster with an ebook funnel: **Supported** (profile hit
  showing the Dec 2025 full-stack roadmap in the same format + the post's own gumroad
  CTA).
- Implicit claim "walk this tree and you are production-ready": **Disputed for this
  fleet** (coverage falsifier: ops half below corpus, theory half consumerless);
  **Unproven for its target persona** (a human beginner) — no independent evidence,
  replies walled.
- Replies / community notes / author follow-ups: **Unfetched — Unproven** (X crawler
  view carries root only; WebFetch timeout, mirror 429s). Per Amendment 2, walled is
  tri-stated, not scored.
- Ebook quality (the product being sold): **Unproven** — paywalled, not opened.

## DOGFOOD
1. INVARIANT PASS: contradicts nothing. Reinforces receipts-over-claims (a taxonomy
   with zero receipts) and the genre rule (curriculum/listicle → REMEMBER unless a
   corpus-unknown resource is named — none is, there are no resources at all). One
   honest extension: the gap-organ convergence above strengthens the Desk salon's
   filing (repetition is emphasis, from outside this time).
2. STOCKFISH PASS: PLACEMENT FAILED — candidate consumers each refused: QLoRA
   training food (needs fleet corpus, not public curriculum), seat-onboarding shelf
   (BOOT_4_7.md 7-file read order strictly exceeds it), Desk gap backlog (already
   filed, no new mechanism), marketing register (not our doctrine's voice). The
   placement failure IS the finding.

## VERDICT
**REMEMBER (5/25)** — file and forget. Two counters (L0): FORBIDS — scoring any
curriculum-tree/funnel post above REMEMBER without a corpus-unknown resource named
(genre rule now extends to the roadmap variant: index-of-nouns = weaker than
listicle-of-links, which already routes REMEMBER). PAID RENT — the $0
corpus-vocabulary grep is now the standing cheap falsifier for the whole curriculum
genre (AMISHA's per-resource sweep was expensive; this one measured 8 terms in one
command), and the convergence datum pays rent on the Desk gap list.

THE CROP: what this pass did not see — (1) the replies/community notes (walled; a
logged-in X scout pass via X_SCOUT_DOCTRINE could sweep them if the operator ever
cares); (2) the Gumroad ebook's public preview page (next chair: one fetch of
codewithdhanian.gumroad.com/l/ungqng would audit the funnel's actual table of
contents for free); (3) the author's other roadmap trees (not opened — a sweep only
if a future item from this account surfaces something non-canonical).

## ROUTE
No wire. Typed room.jsonl row appended (kind: intake.card); driver drops the REMEMBER
row on cadence. Nothing owed, nothing scheduled. Re-open condition: any future
roadmap-class post that names a resource grep-verified absent from the corpus.
