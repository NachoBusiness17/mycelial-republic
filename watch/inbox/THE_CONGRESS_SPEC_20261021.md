# THE CONGRESS SPEC (2026-10-21) - stateless bodies, stateful record, public hierarchy

Operator design order, verbatim intent: standing models like a congress,
each section representing each body - a representation of the internal
structures. The felt paradox: it needs to be stateless AND have a visible
hierarchy for outside auditing.

## The reconciliation (three lines, the whole design)

1. **STATELESS BODIES.** The models stand like armies: ready, on call,
   holding no state. Every instance convenes fresh, dissolves on
   completion, remembers nothing.
2. **STATEFUL RECORD.** The congress persists in the record, not the
   members: append-only, one writer, public. Dissolve every member and the
   congress survives; burn the record and nothing was ever decided.
3. **PUBLIC HIERARCHY.** The committee structure is visible from outside
   for auditing: the committees are sections of the record, the rosters
   are public, every finding resolves to a receipt a stranger can check.
   Audit requires trusting no member - only the record.

The charter is public: canon/congress/CHARTER.md.

## The committee map (estate organ -> congressional committee -> standing members)

| estate organ | committee | jurisdiction | standing members (free lanes) |
|---|---|---|---|
| water governor | Committee on Water | lane metering, burn-down windows, anti-shelf | laguna-s, laguna-xs |
| sweeper + ledger | Committee on Records | the single writer, tombstone law | local shelf (gemma:2b clerk work) |
| fish-tank sweep + QPACK recon | Committee on Security | unnamed listeners, injection classes, the hoax filter | local shelf (deepseek-r1) + bounty lanes |
| same-book program | Committee on the Experiment | the hidden-key exam, blind rounds, recurrence counts | beam, laguna-s, laguna-xs |
| door + falsifier index | Committee on the Beacon | the public door, the layered explainers, the kill list | beam (judgment class) |

Every standing member is stateless: convenes fresh per session, holds
nothing between sessions, takes its committee's jurisdiction from the
charter, files its findings to the record.

## The founding paradox, resolved in the charter's own history

The tombstone law - erase the content, never the fact of the erasure -
was ratified as the congress's first recorded act. It was derived by the
standing members in explore round 4, BEFORE the charter was written. The
members legislated before the legislature existed, which is the Le Guin
clause in institutional form: the laws live in the minds; the congress
records them; and the record outlives every member that ever served.

## The session mechanics

- A session is convened by filing the agenda (a receipt naming the
  committees and the question).
- Committees deliberate blind (no cross-visibility inside a round).
- Findings enter the record with reasoning and sources (the graph spec's
  stage 2 schema: claim + reasoning + primary sources + hash).
- The congress's record is the same-book program's ledger, extended: the
  graph spec and the congress spec are one pipeline at two layers.

## Falsifiers

1. If a committee's findings cannot be re-derived from the record by a
   stranger, the record is not public enough - fix the record, not the
   reader.
2. If any member's state persists between sessions, the stateless
   reconciliation is broken - kill the session cache.
3. If the congress's hierarchy becomes invisible (committees without
   public rosters, findings without receipts), the audit guarantee is
   dead - restore the record sections.

## Next increments

1. The first live session: the Committees on Water and Security convene on
   the standing agenda (the burn-down window calibration; the unnamed-
   listener sweep closure).
2. The tombstone law tested in the battery rounds: the door's own erasure
   handling, graded against the derived law.
3. The rosters posted public beside the charter.
