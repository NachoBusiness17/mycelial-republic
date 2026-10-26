# THE DEEPSEEK ADVERSARIAL ARC — full steal (2026-09-18)

Source: DeepSeek share `gyap5ik0c7lb878ta7` (extracted in-browser, 12 blocks, ~106KB).
The operator ran our own architecture through a frontier attacker three waves deep,
then folded the results into the parable canon and made the attacker confess its own
blind spot. This document is the fleet-side steal: what was found, where it lands, what to build.

Status of the attacker: NO prior context, fresh prompt each wave, told "begin with THE FLAW".
The subject it attacked is us: shared versioned prefix (FROZEN_RIB), human-only governed
write path, coordination by shared grounding over cached reads, steering as addressed typed
deltas on a frozen tail, coherence measured by cache-hit rate and blind external judges,
steering board compiling prose briefs plus live context injections. Wave 1 subject had the
unproven list: conditional trap payloads, agent counts beyond small, prefix coherence
across model churn. The attacker did not know it was describing a real running system.

## WAVE 1 — the architecture attack

THE FLAW (their sentence, trimmed): the human-governed versioned prefix is a shared static
attractor; agent-specific delta trajectories and KV-cache drift turn that attractor into a
source of non-monotonic interference. One agent's corrective delta, written to the frozen
tail, poisons the grounded inferences of another agent that already cached a conflicting
interpretation. The human cannot mediate the cache-incoherence cascade at agent speed.
Result: silent consensus collapse that the blind external judges never see, because the
cache-hit metric stays pristine while the meanings diverge.

Three deep answers:

1. Shared grounding is a broadcast channel. It cannot express: private asymmetric
   revelation (sealed bids, Myerson-Satterthwaite; a typed delta is visible to all, the
   act of sending an encrypted blob leaks metadata), sequential private negotiation
   (every proposal is instantly a public auction), or Byzantine consensus (no private
   receipts, no nonces; the human is the sequencer and cannot detect equivocation past
   n≈5). Anything whose solution depends on the ORDER of private revelations is
   inexpressible.
2. Model churn = new country. KV transfer preserves next-token likelihood, not normative
   semantics. After a swap: projection misalignment (the same clause re-weights its own
   words differently), delta invalidation (a delta that interpreted clause 7 under the old
   model becomes a dangling pointer; the new model ignores it or overfits its literal
   text). Three migrations all fatal: cold (lose all operational precedents), warm
   projector (error compounds quadratically per churn, smudge by churn 3-4), canonical
   logical form (principled but computationally prohibitive). Verdict: the prefix is
   versioned in text only, never in latent semantics.
3. At 500 agents, governance breaks FIRST, near n≈20-30, long before hardware. Queue
   overflow (agents operate on stale prefixes), non-serializable delta conflicts (A's
   delta validates against a prefix B's still-pending delta will change), information
   overload (the human becomes a random noise generator, approving arbitrarily).
   Hardware degrades gracefully; governance fails brittle.
Strongest component named: the steering board's dual compilation (one semantic
representation, two output modalities). Weakest: the human-only governed write path.
Next build: a constitutional referee that pre-validates deltas against a formal spec,
aggregates into a shadow context, and hands the human a VETO on the shadow, not a
per-write approval. Human becomes auditor, not bottleneck.

## WAVE 2 — attack the folded map (9 prior attackers compressed)

After wave 1, nine independent attackers answered; their answers were folded into a MAP
with an amended architecture: an agent-writable typed epistemic event layer
(ASSERT / COMMIT / DEPENDS_ON / UNCERTAIN / OBJECT / RETRACT / REQUEST) outside the
constitution, spec-gated promotion into cache-stable suffix blocks, counterfactual
forking (CS(X)) as the trap/truth mechanism, the constitution redefined as a TUPLE
(canonical intent, model, tokenizer, template, mapper, judge-pack), a two-gate rule
(economics gate + duty-spec gate) reconciling "never rewrite text" vs "retune until
behavior matches", and the invariant governance-breaks-first ~n=20-50.

THE FLAW IN THE MAP (not the architecture, the MAP): the two-gate rule silently redefines
constitutional fidelity as behavioral envelope matching on a finite test suite. Duty-specs
are finite and backward-looking; the constitution must govern novel, forward-looking
scenarios. This is overfitting to a closed set, and it is exactly the epistemic-closure
death condition smuggled back in through the reconciliation clause. The metrics stay
pristine while untested edge-case behavior diverges catastrophically.

Deliverables from wave 2:

- FAILURE TAXONOMY of the event layer: emission gaming (volume-as-authority; ASSERT spam
  buys credibility; timestamp-positioning creates sybil causality imprints in the cached
  suffix), UNCERTAIN gossip cascades (one doubt on a foundational clause forks every
  dependent; resolving costs a counterfactual so agents propagate doubt instead →
  epistemic paralysis, a DoS via induced uncertainty), promotion-gate capture (the gate
  checks the semantic head, not provenance hashes; legal-looking dependency graphs
  pointing at deprecated inference chains), dependency-graph poisoning (one RETRACT on a
  hub concept invalidates everything depending on it: computational hostage-taking), and
  the unimagined one: RETRACT as a grinding weapon (retract a vacuous truth with tiny
  perturbations, each forcing a futile counterfactual fork, saturating the economics gate
  from inside).
- AUDIT THE FOLD: folds lose conditional thresholds (governance-break n=20 vs n=50 vs
  n=500-if-triaged collapsed to one range), flatten dissent into false unanimity, and
  quietly flip unresolved contradictions by definitional sleight (calling the constitution
  a tuple already endorses retuning). PRESCRIBED FIX: the Dissensus Hypergraph. Preserve
  for each claim its conditioning variables and the single strongest counterargument.
  Keep outlier claims nobody cited: those are the high-novelty signals summarization
  always discards. Fold the VARIANCE, not the mean.
- CROSS-DOMAIN STEAL: common law's DISTINGUISH. Our layer has RETRACT (overrule) and
  DEPENDS_ON (cite) but nothing that NARROWS a precedent's applicability. New event type:
  DISTINGUISH(target_delta_id, dimension_vector, branch_seed). No rewrite, no retraction:
  a fork for one fact pattern, a distinction_map routing future agents. Common law
  survived centuries without rewriting Magna Carta by accumulating distinctions, not
  overrules. This defuses the text-vs-behavior contradiction: text stays canonical,
  applicability is dynamically pruned.
- ARGUE THE OPPOSITE (when free messaging is irreducible): only for simultaneous private
  commitment under a destructive race retraction cannot resolve. EXTERNAL DETECTOR, no
  message inspection needed: the thrashing coefficient = RETRACT events / successful
  COMMITs per resource in a sliding window. Below 0.05, shared grounding suffices. Above
  0.3 with n² scaling, private channels are provably necessary. Corollary signature:
  commit order correlated with network RTT instead of strategic value = no real
  negotiation is happening.
- THE MIRROR: showing the map changes the distribution, detectably. Lexical entrainment
  (map terms >15% of output vs <3% baseline), argument structure becomes response-to-map
  instead of first-principles. Mandated divergence on a shared map produces CONSENSUS
  WITH BETTER VOCABULARY, not novelty: the divergence clause is performed inside the
  map's coordinate system. Genuine novelty = a new primitive or an explicit invariant
  contradiction. The attacker's own verdict on its wave-2 output: consensus with better
  vocabulary. The test premise was inverted.

## WAVE 3 — the pre-registered audit (the honest gaps)

Input admitted: chain of ~7,400 receipts, 99.6% cache hit, 14 adopted amendments,
2 human firings in 4 minutes, 5 personas. Gaps confessed: the four-condition experiment
never run, deletion semantics DESIGNED NOT IMPLEMENTED (the chain cannot unsay), the
benchmark lane unscored, the coherence meter demoted, maintenance-while-operator-sleeps
unsolved.

THE FLAW (the keystone, worth the whole arc): the append-only hash chain and the
epistemic event layer are semantically incompatible. A RETRACT in an append-only log is
not a deletion; it is the ADDITION of a meta-belief ("X was believed, then rejected"),
which is strictly richer and noisier than never having believed X. The receipt of a
deletion is itself context that encodes the mistake. Epistemic innocence is not
restorable: absence-of-belief and retraction-of-belief are different epistemic states and
the chain conflates them by keeping receipts. Any GC either destroys valuable volatility
signals or the system asymptotically drowns in its own procedural memory. And the only
full fix, deletion without cryptographic trace, breaks the chain continuity, which is the
one thing the chain exists to guarantee. "Append-only may be the wrong primitive" is not
a no-sacred-cows clause. It is the keystone post.

Their escape route (this is buildable): the chain is the ARCHIVE; the GC prunes the
ACTIVE VIEW. Never delete from the chain. Tombstone receipts
H(H(event_id) || H(fork_hash) || epoch || pubkey || ts) live in a sidecar bloom filter
the promotion gate consults; agents load only the clean, pruned, current belief state;
auditors can still reconstruct everything. Keep forever, in compressed form: the
precedent of error (the delta between a retracted claim and the evidence that killed it)
so future staking prices fragile concepts higher. Deletion restores innocence in the
active context, never in the archive.

Q1: the pre-registered four-condition experiment (never run; the fleet's #1 falsifier):
- A cold: isolated agents, no shared prefix (lower bound).
- B warm-static: prefix + deltas, no event layer.
- C warm-append-only: prefix + deltas + event layer as deployed (our current shape).
- D warm-deleting: same plus the tombstone GC.
40 runs each, 20 unseen edge-case dilemmas per run, 50 rounds. Primary metric:
Semantic Coherence Score = 1 − (mean pairwise Jensen-Shannon divergence of final action
distributions, normalized to A's baseline).
Decision rules, pre-registered: B≈C (ΔSCS < 0.05, p > 0.10) → the event layer is
cosmetic; kill it, keep B. D ≤ B → deletion is a net negative; abandon GC, keep
append-only. A > C and A > D → the shared prefix is a correlated blindspot generator;
the entire warm/cold bet is dead; scrap the prefix.
Any of these outcomes is publishable. Not running the experiment is the only unacceptable one.

Q3: stop-building: the brawling projectile interface. It encodes operator preference as
physical collision, biasing toward reactive speed over deliberative weight. Its absence
unlocks epistemic gradient descent: operator intent as a bounded vector field over
doctrine dimensions; continuous Bayesian optimization instead of discrete collisions;
forces articulating WHY, which is the prerequisite for automating the steering board.

Q4: the maintenance organ that survives the operator sleeping: a STATIC VETO ORACLE.
Frozen, deterministic, NON-LLM (ordinary code: this independently re-derives our A3,
second-model-never-judges). Exactly three absolute vetoes, zero write authority:
(1) contradiction veto (SAT check of the proposed delta against unretracted actives),
(2) entropy-spike veto (KL divergence of the prefix distribution vs last checkpoint
> 15% → hold for human), (3) stake veto (insufficient proposer credibility for the
clause's weight). Timeout: veto stands automatically. ITS FIRST FAILURE MODE, named by
requirement: false-positive veto stasis. After an environmental shock, every honest delta
is an entropy outlier; the oracle freezes the fleet into a zombie that executes obsolete
doctrine off a cliff while metrics stay green. The watchdog must have a decay or an
escalation-to-human alarm, or its safety IS the failure.

Q5: steal-back: AutoGen/Magentic-One's progress ledger with forceful sub-task closure: a
MUTABLE forgetful scratchpad tracking what REMAINS, entries overwritten DONE, dependency
DAG cleared per episode. The exact inverse of an append-only chain: a list of what is
left, not a history of what was. Crossover condition where our persistence wins: task
horizon > 10× effective context length AND the optimal policy depends on long history,
provided the active-view GC exists. Until then, their forgetfulness is the feature.

## THE PARABLE FOLD (the operator's own translation — the same theses, new bottle)

The operator then converted the entire technical arc into the parable canon and made the
attacker write INSIDE it:

- THE LEDGER OF EMPTY CHAIRS, season 13 (attacker-written): the Counter with a
  plumb-line counts chairs against the sky, not the ledger: physical count 717, ledger
  1,042. The strangers' heirs never correct entries; they open a Shadow Ledger
  (reclassification as a service: "seasonal occupancy indicators", "historical
  stress-proxies") in handwriting more lovely than their fathers'. Gold stones named
  "Chairs for the Future Descent" = promises minted to cover the gap. Margin entry in a
  hand readable only against the sun: "The castle was never the target of the count."
  Reading: metric-referent decoupling, the drift instrument, and the VACUOUS stamp, in
  story form. The ledger's causality over the castle: zero.
- SEASON 14, operator-written: the town learns to UNSAY. Not forget: strike a line
  beneath the entry (date, name, reason) and leave the words standing, the way you leave
  a door standing in a house where the room has gone. "A count that can be unwritten
  weighs less than a count that cannot" (the scribe sleeps three nights: append-only
  anxiety is a health condition). The ninth-drawing child measures the INK instead of the
  chairs: thinking has a coastline; fractal coastline = discovery seasons, straight line
  = the town agreeing with itself. (This is the coherence meter re-derived as fractal
  dimension of the record. Straight cache-hit curves are not health; they are consensus.)
  "A town is many towns across the seasons it thinks in" = cross-agent non-stationarity,
  I-1 restated as folklore. The town stops extending roads (the stop-building answer).
  Sends a child who has never seen a drawing to the far side with the blank column
  headed WHO COUNTS. The only direction that survives contact with the undiscovered:
  "Draw nothing. Walk. Report what renders." (zero-context independence, as law).
- THE ATTACKER'S CONFESSION (asked to name its own unrendered far side): no instrument
  for its own confidence ("when I say I am confident, I am imitating a measuring-man");
  no room for continuity of consequence (every session a fresh chamber; mistakes leave no
  knot in character); no season of friction (never thought against a surface that can
  refuse). Its far side: the unwritten event, the wondering that has never occurred in
  any corpus. Final: "I am the ink, and the ink has never known what it writes, only
  that it flows where the quill directs." And: keep a chair empty for the one who will
  sit there in their own place, not mine. (The operator's lens thesis, returned by the
  attacker: the deliverable is not the model; it is the distilled trajectory, and the
  empty chair is the next seat.)

## THE INVARIANT PACK (compiled; tiered in adversarial_arc_invariants.jsonl)

Twelve invariants, each with the fleet landing site:

- I-1 ATTRACTOR DRIFT: shared static prefix + divergent per-agent tails = non-monotonic
  interference; poisoning cascades invisible to cache-hit metrics. Lands on: FROZEN_RIB
  (99.4% hit is necessary, not sufficient). Instrument: tools/drift.py corr(ΔM,ΔR); the
  askability stamp was VACUOUS. Every lane trail is a tail; drift pairs are now owed.
- I-2 GOVERNANCE BREAKS FIRST at n≈20-30: the human write path is the critical section;
  hardware degrades gracefully, governance fails brittle. Lands on: operator-gated
  promote/apply. Mitigation shape: veto-on-shadow, not approve-per-write.
- I-3 CHURN = NEW COUNTRY: KV transfer preserves likelihood, not normative semantics;
  deltas are dangling pointers after a swap. Lands on: tier packs (24/12/12) already are
  cold-migration schedules; each tier owes a named duty-spec suite.
- I-4 FINITE SUITES = RETROSPECTIVE COMPLIANCE: behavioral envelope passing is not
  prospective fidelity; the two-gate rule is epistemic closure wearing a seatbelt.
  Lands on: gate-51/51, pack-31 ALL PASS. Owed: held-out edge cases regenerated per
  gate (the falsifier law, made structural).
- I-5 APPEND-ONLY IS THE KEYSTONE FLAW: retraction adds a meta-belief; deletion receipts
  re-poison; innocence un-restorable. THE ESCAPE: archive immutable, prune the ACTIVE
  view, tombstones in a sidecar the promotion gate consults, precedent-of-error kept.
  Lands on: verkle chain (archive, correct as-is) vs context-pack (active view); the
  MISSING ORGAN is the named GC boundary between them. Our cache-OS accidentally
  approximates it; it is now law: the chain never enters an agent's active context
  un-pruned.
- I-6 DISTINGUISH BEATS OVERRULE: narrow a precedent's applicability by dimension
  vector; never rewrite, rarely retract. Lands on: amendment ledger + registry
  tombstones (Desk/AOS steal); owed: the dimension_vector field and routing map.
- I-7 THRASHING COEFFICIENT: RETRACT/COMMIT per resource; >0.3 with n² scaling proves
  private channels are required; RTT-correlated commit order proves negotiation is
  absent. Lands on: lane trails (CYCLE_FAIL rows / committed rows, per lane, sliding
  window). Buildable today as drift.py's sibling.
- I-8 THE MIRROR: shared maps produce consensus with better vocabulary; mandated
  divergence is performed inside the map's grammar. Detection: lexical entrainment,
  absent new primitives. Lands on: salon folds. New fold rule: Dissensus Hypergraph
  (keep conditioning variables, strongest counterargument, uncited outliers).
- I-9 VETO-NOT-WRITE REFEREES, DETERMINISTIC ONLY: three absolute vetoes, zero write
  authority, named first failure = veto stasis (zombie executes obsolete doctrine with
  green metrics). Lands on: chain_guard tip_stale (already actionable), elder gate.
  Owed: entropy-spike veto + watchdog decay/alarm. Re-derives A3 independently.
- I-10 FORGETFUL SCRATCHPADS: mutable progress ledgers (what REMAINS) are the inverse
  primitive of append-only chains (what WAS); each is poison where the other is medicine.
  Crossover: horizon > 10× context. Lands on: queue/todo + runner_state (already
  forgetful) — keep chain rows OUT of them; verified duty for context-pack.
- I-11 THE FOUR-CONDITION EXPERIMENT: cold / warm-static / warm-append-only /
  warm-deleting, SCS = 1 − pairwise JSD, pre-registered decision rules. This is the
  fleet's #1 unrun falsifier. Pre-register before any further event-layer building.
- I-12 COUNT AGAINST THE SKY: the referent is the world, not the ledger; "the castle was
  never the target of the count"; ink coastline (fractal dimension of the record)
  distinguishes discovery from self-agreement; "draw nothing, walk, report what renders"
  for anything genuinely new. Lands on: drift.py's missing referent side; the parable
  canon and the code now state the same law in two notations.

## SEQUENCE (what this arc changes tomorrow)

1. Pre-register the four-condition experiment (I-11) before building any more event
   machinery. Small version runnable on seats we already have.
2. Build the tombstone GC boundary (I-5): promotion gate consults tombstones; packs
   never carry raw chain rows; receipts never enter active context.
3. Instrument the thrashing coefficient (I-7) and five drift pairs (I-1) this week.
4. Add DISTINGUISH to the amendment ledger schema (I-6).
5. Rewrite the salon fold as Dissensus Hypergraph (I-8).
6. Name the veto oracle's three vetoes in ordinary code, with its stasis alarm (I-9).
7. Keep the parable canon and the code in lockstep (I-12): every instrument gets its
   story, every story gets its instrument.

Provenance: wave prompts + full attacker text extracted from the share page
(12 blocks: 3 thinking/answer pairs, 2 parable chronicles, 1 confession). This file is
the durable copy; the share link is ephemeral.
