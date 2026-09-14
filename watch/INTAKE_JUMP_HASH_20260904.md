# INTAKE — Jump Consistent Hash (TrisH0x2A X post)

Date: 2026-09-04 · Genome: research_socratic (six steps) over L0 v1 · Card 50-ish lane, slug checked (no collision)

## ITEM
https://x.com/TrisH0x2A/status/2095605166234042858 (trish, Sep 3 2026 20:09). Verbatim claims:
- "Google solved consistent hashing in just 5 lines of C++"
- "John Lamping and Eric Veach designed it to map keys to buckets with almost no memory"
- "when a bucket is added, only about 1/n of the keys move"
- "the entire algorithm is a tiny loop using a 64-bit LCG and the constant 2862933555777941757ULL"
- "O(ln n) expected time, O(1) memory" (+ code screenshot, not fetched)

## RECEIPTS
- Fetched whole conversation in one pass (mcp__web_reader__webReader, no 403): post + replies visible.
  - @AXDOOMER (976 likes): "Google didn't solve consistent hashing. There was already a MIT paper published in 1997. Google's algo has a huge limitation where the jump hash only works cleanly if buckets are numbered 0..n-1. You cannot remove an arbitrary node the way a hash ring or rendezvous hashing can."
  - @YUglyTruth (157 likes): "Aaaah magic numbers. It works until it doesnt."
  - @mttrdmnd (1.3K likes): "erich veach is the strongest programmer i've ever had the pleasure of interacting with"
- Attribution: Lamping & Veach, "A Fast, Minimal Memory, Consistent Hash Algorithm", arXiv:1406.2294 (2014). Prior art: Karger et al., "Consistent Hashing and Random Trees", STOC 1997 (MIT LCS) — standard literature, corroborated by the AXDOOMER reply.
- MEASURED ($0, this session, N=100k keys, Python re-implementation of the exact LCG constant):
  - ADD 100→101 buckets: **1.005% of keys moved** vs predicted 1/101 = 0.990%. Post claim held.
  - ADD across grown path 90→101: 10.7% moved (paper bound n0/n1·H ≈ 11%). Held.
  - REMOVE middle bucket 3/10 (the operational case): **68.9% of keys move** vs ~10% ring ideal — jump hash has no removal; survivors must be renumbered, remapping everything downstream. Attack QUANTIFIED.
  - REMOVE last bucket 10→9 (only clean case): 10.0%. Confirms "buckets must be 0..n-1, tail-removal only."
  - O(1) state confirmed: pure function, no table, deterministic recompute PASS.

## SCORE
F:4 P:2 C:5 W:2 N:3 = **16/25 → BUILD WINDOWED**

- FIT 4: zero-dep pure function; bolts onto existing organs (queue-claim organ, seat_dispatch/seat-g1..g4 mapping, ractor legions tranches 8→16→50 — 1/n movement on growth is exactly tranche scaling, Rocinante key→Studio placement). Not 5: nothing running today consumes a hash router.
- PULL 2: feeds Rocinante (Oct 27) and legions-scale as fuel; no live arc (shadow fields, QLoRA, coverage, economist, AzerothCore) moves this window.
- COST 5: verified on laptop CPU in <1s; deployment is a 5-line paste; $0.
- WINDOW 2: no starved lane; nearest consumer (owed queue-claim organ) is not blocked on it; Rocinante 8 weeks out.
- NOVELTY 3: corpus-absent (no consistent-hash row in memory index or watch/), but world-old (2014 paper, 1997 prior art, known viral snippet) — a new-to-us steal of a published classic, not a discovery, not a corpus re-find.

## READ
The post is honest about the algorithm and dishonest by framing: "Google solved consistent hashing" erases 17 years of lineage (Karger 1997) and skips the one assumption that matters operationally — jump hash only accepts buckets numbered 0..n-1 and only supports shrinking the tail. For the fleet that assumption is live: our worker pools GROW in tranches (legions 8→16→50) and grow cleanly under jump hash (measured 1/n movement), but our pools also get SICK in the middle (kill a wedged seat-g3, evict a vast blade) — and the measured cost of mid-pool removal is 68.9% reassignment, which is the exact churn the technique was invented to avoid. Second mismatch: our lanes are weighted (quota, price, saturation) and jump hash is strictly uniform — it cannot express "glm-4.7-flash is free and 5.3 is judgment-only." So it is a genuinely excellent tool pointed at a problem we do not have yet (deterministic stateless assignment at Rocinante scale) and the wrong tool for the routing problem we do have today (weighted lane selection, which ask_router already owns). The thread proves the operator's law again: the root post alone would have scored ~20 (BUILD NOW); the top reply — 976 likes of correct pushback — is what cut it. Threads are signal; this card is the payoff receipt.

## TRI-STATE
- SUPPORTED — algorithm facts: 5-line loop, LCG constant 2862933555777941757, O(ln n) expected / O(1) memory, ~1/n movement on add (measured 1.005% @ n=100→101; arXiv:1406.2294).
- DISPUTED — "Google solved consistent hashing": prior art Karger et al. 1997; jump hash supports no arbitrary node removal (measured 68.9% remap on mid-pool removal vs ~10% ring ideal), no weights, integer keys/buckets only.
- SUPPORTED (as signal) — top reply names the real limitation; the correction survives our own measurement.
- UNPROVEN — nothing left standing unverified; the code screenshot itself was not inspected (see THE CROP).

## VERDICT
**BUILD (windowed)** — not tonight, not standalone. BUILD the port into the queue-claim organ when that build opens (deterministic task_id → seat claim across tranche growth), and into Rocinante run/shard→Studio placement on Oct 27. REMEMBER as the standing answer to "stateless assignment with minimal memory" (the files-are-data position, in algorithm form). CALIBRATE nothing — no existing organ needs correction. Kill condition: if the queue-claim organ lands with a different mechanism (lockfile-first was the recorded design) and no assignment problem survives to Rocinante day, this card converts to REMEMBER-only and the BUILD claim dies.

## ROUTE
**No wire tonight.** Wire triggers (either one): (1) queue-claim organ build starts → paste the jump_hash function as the claim opcode, (2) Rocinante multi-node routing lands → key→Studio placement. FORBIDS: never wire it onto weighted-lane routing (quota/price-weighted — jump hash is uniform), never onto any pool where mid-array eviction is the recovery path (68.9% churn, measured).

## L0 CLOSERS
- Receipts: watch/INTAKE_JUMP_HASH_20260904.md · ROOM ROW: {"kind":"intake.verdict","ts":"2026-09-04","item":"x:TrisH0x2A/2095605166234042858","score":16,"band":"BUILD_WINDOWED","verb":"BUILD(windowed)","wire":false,"falsifier":"add 1.005% vs 0.99% PASS; mid-remove 68.9% vs 10% FAIL"}
- FORBIDS: weighted-lane use; mid-pool eviction use (both above).
- PAID RENT: threads-are-signal — the top reply moved this card two bands and cost $0.
- Falsifier (next seat, cold): run the 12-line Python above; if mid-bucket removal remaps <~15% of keys, this card's central DISPUTED is wrong.

## THE CROP
This pass did not see: (1) the post's code screenshot — webReader returned text only; if the viral image contains a subtly wrong variant, that error went uninspected — a vision pass on the image should sit next; (2) a one-grep sweep of mag/, queue/, campaigns/ for hash-based assignment already embedded implicitly in seat_dispatch internals (possible silent convergence); (3) JS port semantics — our consumers are .mjs; C int64 overflow vs BigInt/float division must be proven identical before any wire. Lens that should sit next: the driver seat, at whichever build opens first.
