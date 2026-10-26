# THE INTERPRETIVE LAYER - context as render, not storage (2026-10-16)

Classification: CARD (design; companion to the self-steal + triangulation in this file)
Producer: zcode-seat-20261016
Origin: operator riff - context windows are filled with structural scaffolding
(prompts, tools, skills, MCP schemas) while messages are read once and become
"just a memory state." Why store them as plain text? Keep them as an
interpretive layer that renders to text only when the human is the observer;
everything else lives in permanent state. The window-into-rib-then-back round
trip is the same concept; the human interface is the only stochastic variable.
The invariant percolator ties in.

## THE FORMALIZATION

The context window conflates two layers:
- STATE LAYER: what the seat knows this turn (deterministic, structured,
  hash-addressed, decays by law, cascades on dependency).
- RENDER LAYER: text tokens the model actually reads (stochastic decode,
  observer-facing, expensive).
The proposal: state is primary; text is a projection rendered on demand for
the observer; agent-to-agent and agent-to-self traffic rides the state layer;
window bloat becomes O(settled knowledge) instead of O(conversation length).

## SELF-STEAL - the estate already holds every organ except one

| the design needs | estate organ (state) | fit |
|---|---|---|
| the interpretive compiler | invariant percolator (mag/percolator.py, since 08-11): percolate(text) classifies SIGNAL / THEATER / NOISE, compiles recurrences to content-hash invariants, quarantines noise to the noise file, routes novel signal to the explore queue | EXACT: recurrence = stable truth worth compiling; novelty = explored-and-folded; deterministic, $0, no LLM |
| the state-object format | invariants.json rows: text, count, first_seen/last_seen, decay_as_of, cycle_hits, depends_on | content-addressed, half-life decayed (pheromone evaporation), cascade-aware (CP-1: mined + declared depends_on, BFS invalidation) |
| the law render (window -> rib -> window) | RIB_HANDOFF + rib_boot (first-mounted), SOAK_BEACON (row 0a crown) | the round trip the operator named, already in production since 10/15 |
| the storage doctrine | shared-surface contract law: "prefer an artifact plus bounded pointers and hashes over a copied transcript" | the plain-text ban on hot truth was already codified; transcripts are cache, artifacts are truth |
| the renderer | context-pack (min-token pack per seat) + zknot (recency-weighted session digest) + beacon | render-side exists; no render CONTRACT yet (see correction 2) |
| decay + honest death | half-life decay (Z15), demotion register (SUPERSEDED.md), Landauer fold (erasure is paid; append-only is optimal; compost = deliberate erasure payments) | the thermodynamic constraint is already encoded |
| the anti-exploit law | Z15 self-emission cap: an invariant re-incrementing itself was "memorization as an exploit played by the loop on itself" | the memory-poisoning defense every interpretive layer needs, already litigated |
| MISSING | a render CONTRACT (fixed core render + pinned where behavior depends on it) and the window-close percolation ritual (session -> percolate -> invariants/explore/noise) generalized beyond ribs | the two buildables |

## TRIANGULATION - the field converging from three directions

1. MemGPT / Letta: the OS analogy, window as RAM, store as disk, function-call
   paging. Difference: their paging retrieves VERBATIM pages; the estate's
   compiler produces INVARIANTS - compressed but falsifier-attached.
2. Gist tokens / soft prompts (learned latent compression): the radical
   endstate - state the model understands natively as activations, no text at
   all. Requires model cooperation we do not own from the seat.
3. KV-cache persistence / prompt caching: the literal permanent state is the
   KV cache; today's harnesses expose prefix caching only. The gap between
   the estate's text-layer invariants and persistent KV is harness access.
4. Agent beacons (AGENTS.md, llms.txt, .well-known - gstdcoin's own A2A repo
   ships them): agent-facing render is already diverging from human prose.
5. Harness compaction (this very session runs summarization): emergency
   interpretation at overflow. The proposal is the same move at design time,
   with receipts.

## TWO CORRECTIONS (spore discipline: falsifiers attached)

1. DETERMINISM LIVES IN THE STATE LAYER ONLY IF RENDERS HAVE CONTRACTS. The
   operator said the human interface is the only stochastic variable - sharper:
   the human is the only observer who NEEDS the render, but the render itself
   is also stochastic (same rib, different wording, different downstream
   behavior). So pins go where behavior depends: fixed core render (the estate
   already does this - claritas face + deterministic estate-law block), stoch
  astic shell only where it does not.
2. PLAIN TEXT IS NOT THE MISTAKE - IT IS THE COLD LAYER. Landauer: erasure is
   paid, append-only is optimal, compost is the payment. The bloat sin is not
   storing messages; it is re-rendering the cold store into the hot window.
   Settle, do not delete: hot = O(invariants + pointers), cold = O(messages)
   on disk where bytes are cheap and greppable and hash-anchored forever.

## FALSIFIERS

- Compiled-context seats underperform verbatim-context seats on held-out
  tasks (drift-patrol fresh-reader is the instrument) = the interpretation
  lost decision-relevant signal; the layer needs a recall path.
- A law-class truth silenced by half-life decay when it was load-bearing
  later = decay classes are wrong (law ribs already exempt; event-class decays).
- Percolator FP rate climbing = lexicon rot (FP count is already tracked).
- Longitudinal ablation arm: compiled ARM A must not lose to verbatim ARM B
  across the k=5 chains.

## SMALLEST NEXT WIRE

The window-close percolation ritual: session log -> percolate() -> new
invariants / explore rows / noise file, then the rib carries only the
compiled layer. This generalizes the rib round trip from law to everything,
and it reuses one existing organ with zero new machinery. Second wire: a
render-contract block inside context-pack (beacon + first-mounted rib + top
decayed invariants + open explore pointers + owed).

## ADDENDUM 2026-10-16 (free-lane triangulation returned; SENSING-GRADE)

`watch/inbox/hermes_burn/H247_INTERPRETIVE_LAYER_TRIANGULATION.md` banked:
its one real contribution is the render-contract SHAPE (fixed core template +
interpolated pinned pointers, applied at window close, percolate() feeding
the pointers) and QUANTIFIED falsifier thresholds: the patch is falsified
unless seats show >=10% per-token latency reduction on the drift-patrol
fresh-reader held-out task AND <=2% accuracy loss vs verbatim baseline. Its
prior-works section added nothing beyond this card (the free model mostly
restated evidence and honestly marked its citations UNVERIFIED) - graded
weak-positive, banked as findings per the truth law.

## ADDENDUM 2 (evening): EXTERNAL CONVERGENCE #2

AIPOCH released Open-Science (spotted via @rohanpaul_ai, link drops batch 2):
a session packed into one importable .science file - conversation branches,
file versions, notebook records, verification evidence - opening READ-ONLY
on import until the recipient copies it, engine-agnostic, with approval
controls. That is the horizon object + coverage receipts + the residual law
as a vendor container. Convergences now: VeriHarness numbered our memweave
rule (+0.6/+6.1); Open-Science shipped our session-object. Schema borrow
worth taking: read-only import until copied (cold-layer discipline, stated
as a transport rule). What stays ours: the math-only line, the hash chain,
falsifiers attached, no vendor lock.
