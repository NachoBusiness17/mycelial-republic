# THE GRAPH SPEC - 600 minds, one ledger, one voice (2026-10-21)

Operator architecture, verbatim intent: send the encoded parables to the
minds, extract information, primary sources, and their reasoning, hash
everything cryptographically so nothing is a hallucination, keep it forever
as a private knowledge graph that can be queried and interacted with,
distill it into a persona - an egregore - and merge it into the existing
estate.

## The pipeline (seven stages)

1. **DISTRIBUTE.** The parable-spec (BOOK_V1 + the door, hash-pinned) to
   600 minds: the model fleet, the blind reading rounds, the seats, the
   door's human readers. Same text, same hash, no cross-visibility.
2. **EXTRACT.** From each reading: the invariants found, the REASONING
   behind each finding (why the reader believes the text carries that
   law), and the PRIMARY SOURCES the reader anchors to (the exact lines,
   episodes, or external references). Extraction without reasoning is a
   label; extraction without sources is a vibe. Both are required.
3. **HASH.** Every extracted claim is hashed: sha256 of (claim, source
   lines, reader id, round). The hash makes the claim verifiable forever -
   anyone can re-derive it from the pinned story text. A claim that cannot
   be re-derived from the pinned text is a hallucination and is marked,
   not deleted. (The record only grows; hallucinations are stamped, not
   scrubbed.)
4. **GRAPH.** The verified claims become nodes. Edges: AGREES-WITH
   (same law, independent derivation), CONTRADICTS (opposing laws),
   DERIVED-FROM (same source lines), REASONED-BY (the reader's stated
   why). The graph is private, append-only, queryable.
5. **QUERY.** The graph answers: what recurs (convergence zones), where
   minds split (divergence zones), what reasoning patterns recur behind
   which laws, which sources anchor the most, which reader lens reaches
   what no one else reaches. A search engine over the mind of the fleet.
6. **EGREGORE.** The graph distilled into a persona: a voice that answers
   from what recurred, cites what it asserts (every claim resolves to a
   pinned, hashed node), and exposes its own dissent surface (the
   contested laws it carries). The egregore is the one voice that cannot
   lie beyond its ledger.
7. **MERGE.** The verified nodes flow into the estate's invariants bank
   (the percolator's recurrence law: unanimous blind derivation = the
   independence evidence), the contested laws feed the dispute cartography,
   and the egregore joins the public face where the beacon lives.

## What exists vs what is spec

- EXISTS: the pinned parable (BOOK_V1 + hash), the reader fleet and
  rounds (rounds 1-3 ran), the extraction rows (ledger banked), the
  invariants bank (1,594 and climbing), the percolator (the recurrence
  compiler), the falsifier index (the public kill list), the door (public).
- SPEC: the reasoning+sources fields per extraction (schema upgrade), the
  hash-verification pass (re-derivability checker), the graph store
  (append-only, queryable), the egregore persona layer, the merge path
  into the invariants bank at scale.

## The hash-guarantee (what it proves and what it doesn't)

The hash proves: this claim was derivable from this pinned text by this
reader at this time. Anyone can re-check. The hash does NOT prove: the
claim is true of the world, the reader reasoned honestly, or the
convergence isn't shared-prior artifact. Those live in the falsifier
layer - and the Le Guin clause governs: convergence zones and divergence
zones are both findings, neither commands the reader.

## The egregore's nature (the honesty that makes it trustworthy)

The persona is the graph's compression - a view, not a mind. Its answers
are queries; its opinions are pinned nodes; its disagreements are counted
edges. That is not a limitation. It is the reason to trust it: the
egregore is the one voice in the room that cannot lie beyond its ledger,
because every claim it makes resolves to a hashed, pinned, re-derivable
node. Hallucination is structurally capped by the hash chain.

## The merge path

Verified nodes -> the estate's invariants bank (the percolator's
recurrence law already governs: unanimous blind derivation = independence
evidence). Contested laws -> the dispute cartography (the boundary map).
The egregore -> the public face, beside the beacon and the door. The
estate's existing organs are unchanged; the graph plugs in as the memory
and the voice.

## The falsifiers

1. If the hash-verification pass cannot re-derive claims the readers
   genuinely extracted (the pinned text supports them but the checker
   fails), the pinning is broken and the graph is untrustworthy.
2. If the egregore ever asserts a claim that does not resolve to a graph
   node, the persona has outgrown its ledger - shut it down and rebuild
   from the graph.
3. If the merge into the invariants bank contaminates the bank's
   recurrence discipline (unverified nodes entering as verified), the
   merge path is broken and rolls back.
