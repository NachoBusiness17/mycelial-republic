# DUEL2_train_13_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Adversarial review: CORE_MEMORY_PROTOCOL.md (sha256 f014e1bd...7977)

<basis>
- Method: static reading of the supplied text only. No runtime measurement is relied on, and nothing was executed against the fleet.
- Citations: the document was supplied without line numbers, so every file:line is UNVERIFIED. Each claim instead quotes the bytes it rests on. Em-dashes in the source are not reproduced; where one joins two quoted fragments, I say so.
- Ranking: by damage if unrepaired.
</basis>

---

## DEFECT 1 (most severe): "Coincidence" is a presence check, so one organ can drive both wires

<a_name>Law 2 gate checks that two fields exist, not that they coincide</a_name>

<b_clause>
- Implementation: `a memory write requires the coincidence of two selectors: the organ's claim (wire X) AND the canonical id (wire Y).`
- Test: `any event row missing organ or canonical is rejected at the stream gate (the event_stream emit already requires organ + kind; add canonical enforcement for memory-class events).`
- Overclaim: `no organ can write a memory alone.`
- Location: section "2. X-Y COINCIDENT-CURRENT ADDRESSING", line UNVERIFIED.
</b_clause>

<c_failure>
The only rejection rule is "missing organ or canonical". Nothing requires the organ's claim to cover the canonical id. Nothing makes the two selectors independent.

- Negative example (accepted by the document's gate): organ `drain-A` emits a memory-class event with `canonical=lesson-17`, which `drain-A` never claimed. Both fields are present, so the gate passes it. The Law 2 sentence "no organ can write a memory alone" is falsified, because one organ supplied both wires.
- Positive example (what half-select means): an event with `organ` but no `canonical` is rejected. This is the only case the document actually covers.
- Aggravator inside the same clause: the test says "any event row", but the parenthetical limits enforcement to "memory-class events". "Memory-class" is never defined anywhere in the document. Whether a differently-classed event can still write memory is UNPROVEN from the text, but the clause permits that reading.
- Net effect: the "single-wire corruption class" is claimed killed (`This kills the single-wire corruption class`), but the described gate only blocks malformed rows, not wrong-cell writes.
</c_failure>

<d_predicate>
Over any event corpus E, run the stream gate G:

```
for e in E where class(e) is memory-class:
    accept(G, e)  <=>  organ(e) present
                       AND canonical(e) present
                       AND canonical(e) is within the claim of organ(e)
```

- Fails against the document as written. The document accepts the `drain-A` / `lesson-17` row, where canonical is outside the organ's claim.
- Passes after repair. The repair adds only "canonical must lie within the organ's claim" and "every event kind is classed, with unclassed treated as memory-class". All of these terms (claim, canonical, organ, memory-class, stream gate) are already in the document.
- Falsifier of this finding: if some clause elsewhere in the document defined "claim" as already bound to a canonical id, the defect would collapse. The supplied text contains no such clause.
</d_predicate>

---

## DEFECT 2: The Law 1 test passes with no write-back, and the law has an escape hatch

<a_name>Vacuous read-cycle test plus optional "flag as decay" exit</a_name>

<b_clause>
- Test: `after any read cycle, the read fragment's hash exists in the chain post-read.`
- Escape hatch: `or the read is flagged as decay.` In the source this is joined to `the fragment is re-verified (hash) and re-committed (re-anchor event)` by a dash.
- Law title: `MANDATORY WRITE-BACK`
- Location: section "1. DESTRUCTIVE READ + MANDATORY WRITE-BACK", line UNVERIFIED.
</b_clause>

<c_failure>
Two independent holes:

1. **The test is satisfied by the pre-read anchor.** The fragment's hash was already in the chain before the read (that is what "re-verified (hash)" compares against). So "the hash exists in the chain post-read" is true even if the read wrote nothing. The drain-status bug the document cites as the motivating case (`the drains read the backlog, acted, and never marked the source`) would pass this test.
2. **"Mandatory" is not mandatory.** The "or flagged as decay" branch lets a read end with a flag instead of a re-anchor, with no condition on when the flag is allowed. A fragment that verifies cleanly can still be left un-re-anchored and merely "flagged".

- Positive example: read, verify OK, new re-anchor row appended after the read. Correct.
- Negative example 1: read, verify OK, no new row. The document's test still passes.
- Negative example 2: read, verify OK, decay flag emitted, no re-anchor. The document permits this.
- The second sentence of the test (`If a read leaves no re-anchor row, the memory is decaying.`) states the right criterion, but it is a diagnosis, not the test. It also says nothing about order relative to the read.
</c_failure>

<d_predicate>
For every read cycle r of fragment f, with chain order "post-read" meaning a later chain position than r:

```
verify(f) passes  =>  exists re-anchor row for hash(f) at chain position > position(r)
verify(f) fails   =>  exists decay flag for f AND no re-anchor row for f after r
```

- Fails against the document as written. Negative examples 1 and 2 are both accepted by the document's test or by its "or flagged" branch.
- Passes after repair. The repair restricts the decay flag to a failed re-verification and requires the re-anchor row to be later than the read. It uses only "re-anchor event", "chain", "hash", "re-verified" and "decay", all of which the document defines.
- Falsifier of this finding: if "post-read" were defined in the document as "a row created after the read", the first hole would close. The text gives no such definition. The second hole would remain.
</d_predicate>

---

## DEFECT 3: The sense wire has no baseline, trigger or test, and contradicts Law 4's stance on absence

<a_name>Law 3 detects "flips without a sensed pulse" but defines nothing to sense against</a_name>

<b_clause>
- `the lattice is the sense wire: it detects state flips by comparing the divergence reading.`
- `A flip without a sensed pulse (an unreported change) = the divergence event that wakes the seat.`
- `The min-33 silent death was a read with no sense wire.`
- Conflict with Law 4: `Absence of a write is not inhibition; inhibition is a recorded event.`
- Header promise: `Every memory word the fleet uses maps to a mechanical operation with a test.`
- Location: section "3. THE SENSE WIRE", line UNVERIFIED. Unlike Laws 1 and 2, this section has no `Test:` line.
</b_clause>

<c_failure>
"Comparing the divergence reading" does not say what the reading is compared against, or when a comparison runs. The definition of a flip is "a flip without a sensed pulse", which is circular: the sense wire is supposed to be the detector of the pulse, yet the trigger is the absence of one. Nothing here forces the lattice to take a reading at all.

- Negative example: a memory fragment changes and no organ reports it. If the lattice takes no reading, no divergence event exists and the seat sleeps. This is exactly the min-33 silent death the section claims to fix.
- Positive example: the lattice compares each fragment's current hash to its latest re-anchor hash, finds a mismatch with no reporting event, and emits a divergence event. The document never states this procedure.
- The header promises a test for every word, but only Laws 1 and 2 have one. Laws 3, 4 and 5 do not. For Law 3 that leaves the one incident it cites with no check.
- Any timing or cadence of readings is UNPROVEN, because the document states none.
</c_failure>

<d_predicate>
Over any chain trace:

```
for each fragment f where hash(f) differs from the hash of f's latest re-anchor row
    AND no event reports the change:
        exists a divergence event, emitted by the lattice, that names canonical(f)
```

- Fails against the document as written. A lattice that never reads is conformant to the Law 3 text, and the document has no `Test:` line to catch it.
- Passes after repair. The repair names the re-anchor hash from Law 1 as the thing the divergence reading is compared against, and adds a `Test:` line stating the predicate above. It uses only "lattice", "divergence reading", "divergence event", "seat", "re-anchor" and "canonical", all already in the document.
- Falsifier of this finding: if the document defined "divergence reading" in some section I missed, the baseline gap would not stand. The supplied text defines it nowhere.
</d_predicate>
