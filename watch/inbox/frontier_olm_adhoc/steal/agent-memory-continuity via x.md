# STEAL CARD: agent-memory-continuity via x (frontier_olm_adhoc) - rev 2

source-fetched: adhoc. Seat: steal-agent-memory-continuity-x (workflow child). Moment:
2026-10-11. Inputs: 2 confirmed finds delivered by the round-1/round-2 asks, first
banked at sweep layer by the 2026-10-11 adhoc x-door run (items 1-2 at
watch/inbox/frontier_olm_adhoc/sweep/agent-memory-continuity-x.md:95-112). Card JSON
landed next to this .md per the sibling pattern (steal/kv-cache-context-engineering.json
is the shape). House laws: ascii only, no em or en dashes, every claim cites bytes read
or commands run this sitting; anything not verified is OWED.

## Revision ledger (round-2 critique -> this rev)

1. FIX 1 (re-bank, the big one): round 1 presented v0.9.30's capture machinery as
   the unbanked steal. FALSE: the parked v0.9.29 clone already documents all of it
   in its own README (every line re-read this sitting; citations below). The true
   steal is the unifying shape plus the one new public item (stale-session sweep).
   The round-1 claim "the v0.9.30 delta was unbanked before this sweep family" is
   struck and corrected in Find 1 below.
2. FIX 2 (wrong organ): round 1 ported the 32-obs cap "to the water graph's
   evidence layer". No such layer exists: we_have/evidence/banked are knowledge
   graph node fields (mag/knowledge_graph.py:221; the 9/6/6 emptiness measured at
   watch/inbox/frontier_olm_adhoc/lens/graph.md:19), while mag/water_graph.py is
   the hydraulic flow engine (tanks/pipes/junctions; my grep for the three field
   names over it returns exactly one hit, the word "evidence" inside a test
   comment at mag/water_graph.py:303 - zero field usage). Retargeted to the
   knowledge graph's evidence layer.
3. FIX 3 (missing provenance): round 1's "dead-salmon control law" paraphrase
   carried no citation and misworded the rib. The law is
   memory/rib/RIB_TEN_MINUTE_SELF_20261010.md:50-51 ("Dead-salmon curation before
   any fold: reverts and fixups are pitfalls detected but NOT bypassed - compost,
   never training food. No phantom pitfalls in the corpus."); the instrument is
   dead_salmon() at tools/consensus_harness.py:217, called at :311.
4. FIX 4 (probe honesty): probe A re-scoped to the live increment (the live graph
   holds ZERO why_context edges; the 117 live only in the heal log); probe B
   re-scoped battery-first (no consuming eval exists today).
5. Two letter-level corrections to the critique itself, recorded for honesty:
   (a) tools/graph_heal.py is not apply-function-free - apply_heal() exists at
   :232-238 (appends this pass's planned edges, called at :342); what is missing
   is replay of the PERSISTED heal log into build(), which is the port. (b) The
   water-graph grep is one comment hit, not zero (mag/water_graph.py:303).
   Both corrections were verified by grep this sitting and change no conclusion.

## Find 1 (re-banked): agentmemory - the shape that unifies, plus one new sweep

Source: https://github.com/rohitg00/agentmemory/releases/tag/v0.9.30 (2026-10-06);
release body byte-verified at watch/inbox/frontier_olm_adhoc/sweep/_amh_rel30.json:43.

HELD (prior art in the parked clone at
C:/Users/foste/Documents/projects/library_parked/agentmemory, parked at v0.9.29,
CHANGELOG.md:39): the entire capture machinery is in the parked README - the
capture-inbox flow (README:1736, "The server writes the event to a capture inbox
in the state store"), dead letters (README:1743), retries with doubling backoff
up to AGENTMEMORY_CAPTURE_MAX_ATTEMPTS (README:1746), the offline spool law
including server-down behavior, next-start send, and event-id idempotency
(README:1748, "Event ids make this safe", plus the drain command and the
POST /agentmemory/capture/drain endpoint at README:1718 and
C:/Users/foste/Documents/projects/library_parked/agentmemory/docs/plugins/codex-local.md:94), the vector pending log with force-kill survival
and restart-resumed backfill (README:1024), the 32-observation provenance cap
(README:1750, "the newest 32 observations", auto-trimmed on boot), and monthly
audit scopes (README:1321). Round 1 grepped the version string, found 0.9.29, and
concluded "delta unbanked" without grepping the mechanism text - the exact
failure class the standing law at steal/kv-cache-context-engineering.md:30-40
exists for. STANDING LAW ADDENDUM this card records: overlap checks against
parked/upstream repos must grep mechanism text, not version identifiers; a
version delta is not a mechanism delta.

NEW in v0.9.30's public surface, verified this sitting: "stale session sweep"
(grep -c "stale session|stale-session" over the parked README and
docs/plugins/codex-local.md = 0; the parked clone's four "stale" hits are npx
cache staleness at README:90, memory staleness at :254 and :972, and stale-process
port cleanup at :1510 - none is the sweep). The release bullet also ships it
alongside graph compaction and bucketed vector index (_amh_rel30.json:43).

THE STEAL (the increment over both banks): not the machinery, the unification.
agentmemory's parts are one law there and three scattered mechanisms here. The
estate holds the heal-log mirror (tools/graph_heal.py:250-258 writes "a mirror of
every why_context edge currently in the graph") and holds apply_heal() for this
pass's ops (:232-238), but build() (mag/knowledge_graph.py:602) never drains the
persisted log - knowledge_graph.py's only heal mention is the history comment at
:232, and the measured result is the 117-to-0 wipe documented at
mag/knowledge_graph.py:233-234. Today's live graph proves the wound is open:
grep -c "why_context" memory/knowledge_graph.json = 0 (run this sitting), while
the 117 edges survive only in
memory/corpus/quantized_thought/graph_ghosts/heal_log.jsonl (wc -l = 117, first
row graph_ts 2026-10-06T18:06:27Z). The estate's own lens already demands this
port: "cross-links do not survive regeneration (why_context vanished 10-06 ->
10-11), so durability of any manual weaving must be settled with the graph
builder first" (watch/inbox/frontier_olm_adhoc/lens/graph.md:28).

Organ: sovereign mirror (knowledge graph + heal log). Port move: build() gains a
heal-log drain as its last step - re-apply authored why_context edges from the
newest heal log, idempotent by edge id (from/to/text hash plays agentmemory's
eventId; README:1748's idempotency law is the pattern), edges whose endpoints
dangled after replay land in a dead-letter file (README:1743 pattern) instead of
vanishing. Secondary ports: the 32-obs provenance cap bounds the evidence fields
on knowledge-graph nodes (the we_have 9 / evidence-banked 6 emptiness at
lens/graph.md:19; note the lens's own law at :28 - land new holdings as
we_have/evidence/banked fields, not singleton nodes); the stale-session sweep
joins the fold-hygiene cadence the quantizer/percolator run (agentmemory sweeps
sessions, the estate sweeps fold batches - the shape is a scheduled reaper for
stale authored state, not an on-demand cleanup).

## Find 2 (substance unchanged, provenance added): arXiv 2610.11152

Source: https://arxiv.org/abs/2610.11152 (2026-10-08), "Do LLMs Learn from Rewards
in Context? Rethinking the role of reward in In-Context Reinforcement Learning".
Quotes byte-verified this sitting by grep over the fetched full text
(watch/inbox/frontier_olm_adhoc/sweep/_amh_full_11152.html): "flipping, randomizing,
or removing the reward leaves the improvement curve almost unchanged"; "shuffled or
corrupted trajectories work as well as real ones"; and the direct memory-design
implication, "ICL factors such as input distribution and demonstrations may matter
more than RL elements such as reward shaping and exploration".

The mechanism: if corrupted trajectories teach as well as real ones, the teaching
signal lives in the distribution and format of the input, not the reward semantics
attached to it. A pitfall-bypass corpus built from raw trajectory-reward pairs is
placebo unless a corrupted-input control proves otherwise. This converges from the
outside with the estate's own law, now cited: dead-salmon curation before any fold
(memory/rib/RIB_TEN_MINUTE_SELF_20261010.md:50-51, instrument dead_salmon() at
tools/consensus_harness.py:217 called at :311) - the estate discovered the same
class independently and enforces it before folding.

Organ: quantizer (the fold corpus) with the percolator (fold-candidate selection).
Port move: the fold falsifier the rib already demands - "a fold built only from
the controlled pitfall-bypass corpus must beat prompt-only on held-out pitfalls,
or the JIT framing overclaims" (RIB_TEN_MINUTE_SELF_20261010.md:58-59) - gains a
shuffled-pairing arm per this paper, and fold selection weights distribution
coverage (which pitfall classes the corpus covers) over reward magnitude (how
loud the failure was).

## Probes (falsifiable, re-scoped per FIX 4)

- Probe A (find 1, scratch-copy, one command class): the wipe half is already
  measured (mag/knowledge_graph.py:233-234) and the live graph already sits at
  zero, so re-measuring it proves nothing new. The live increment: on a scratch
  copy of memory/knowledge_graph.json, replay the 117-row heal log (or re-author
  a handful of edges), snapshot the authored-edge count, run build(), count
  again - prediction, 0 survive (the known class); then run the heal-log drain
  step as designed - prediction, full restoration, idempotent on a second drain
  (double replay adds no duplicates). Falsifiers: if the drain restores nothing
  (log stale vs current schema), the port design is wrong before any code lands;
  if plain build() already survives authored edges, the steal is moot.
- Probe B (find 2, battery-first): no consuming instrument exists today - the
  fold-vs-prompt-only falsifier lives as rib law (RIB_TEN_MINUTE_SELF_20261010.md:
  58-59) but there is no pitfall-bypass corpus, no fold batch, and no consuming
  eval in tools/ or memory/corpus/ (the sweep lists the RQ3 batteries under
  not-run, agent-memory-continuity-x.md:195-197). So the probe's first leg IS
  building the minimal battery: one pitfall-bypass fold batch plus a held-out
  pitfall eval, runable on the local free lane. Leg two: shuffle the batch's
  (revert, fixup) pairing and rerun. The paper predicts shuffled approx equals
  real; a significant gap falsifies the transfer to estate data. Either outcome
  banks a law; the battery, once built, also serves the rib's own falsifier.

## Overlap verification (commands run this sitting)

- grep -n -E "0\.9\.(29|30)" over the parked CHANGELOG.md: line 39 only
  ("## [0.9.29] - 2026-08-16"); no 0.9.30 entry.
- Mechanism-text grep over the parked README + docs/plugins/codex-local.md: every
  held-feature line cited in Find 1 read directly (sed -n per line); "stale
  session|stale-session" count 0 (exit 1).
- grep -rn "v0\.9\.30" over catalog/ + watch/inbox/frontier_olm_adhoc/ +
  memory/frontier/: only the sweep's own artifacts (agent-memory-continuity-x.md:
  77,84,95,103 and _amh_rel30.json). Zero catalog rows.
- grep -c "2610\.11152" catalog/catalog.jsonl: 0 (exit 1). Find 2 appears only in
  the 10-10 x-sweep pass-1 candidate list (its line 15, per the banked file's own
  note at agent-memory-continuity-x.md:110-112); never banked as an item.
- Live-state reads: grep -c "why_context" memory/knowledge_graph.json = 0; wc -l
  heal_log.jsonl = 117.

## Checks run / not run this sitting

- Run: all greps and seds above (commands inline in the ledger and Find sections);
  code reads mag/knowledge_graph.py:219-222,228-240,602 and tools/graph_heal.py:
  232-258; rib read RIB_TEN_MINUTE_SELF_20261010.md:50-62; lens reads
  watch/inbox/frontier_olm_adhoc/lens/graph.md:19,28; citation lint and ascii
  check on THIS card, results in the JSON twin's lint note.
- Not run: probes A and B (this card is the design, not the bench); any pytest;
  any build() execution on a graph copy; any WebFetch of the two source URLs
  (byte evidence is the sweep's banked fetch artifacts plus the parked clone,
  cited above).

## OWED

- The build()-drains-heal_log wiring is mag/ seat work; this card claims the
  design and the falsifiers, not the landing.
- The X door stayed dark this carrier too (fourth consecutive; syndication token
  / x-history miner, per agent-memory-continuity-x.md:199-204). Both finds
  arrived through fallback doors (GitHub REST, arXiv html), so "via x" names the
  lane, not the transport.
- The parked clone sits one release behind; when it reparks at 0.9.30+, the
  stale-session sweep's implementation (not just the release bullet) becomes
  readable prior art for the fold-hygiene reaper.
