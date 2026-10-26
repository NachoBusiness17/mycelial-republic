# DUEL2_train_08_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Falsification spec: CORE_MEMORY_PROTOCOL.md (sha256 f014e1bd...7977)

<conventions>
- The evidence has no line numbers, so I cite by section label (L1..L5, ROPE, RESTATED) plus quoted bytes. File:line is UNVERIFIED for every citation.
- Each measurement names its instrument, its moment, and its context assumptions. Where the document gives no value (timeouts, memory-class kind list, read log), I mark the value ASSUMED and the claim cannot be judged without it.
- Pass and fail values are explicit. Each predicate has a negative control, meaning a case that must NOT trigger the fire condition, so the harness cannot pass by rejecting everything.
- Statuses: FIRES-ON-DOC (the document's own text already satisfies the fail condition), TESTABLE (a pass/fail experiment is defined), UNPROVEN (cannot be operationalized from this document).
</conventions>

---

## P1. Law 1: destructive read + mandatory write-back

<claim>L1 Test: "after any read cycle, the read fragment's hash exists in the chain post-read."</claim>

<defect>
As worded, the test is vacuous. A fragment anchored before the read already has its hash in the chain, so "exists post-read" holds with no write-back at all. The literal test cannot distinguish a correct implementation from one that never writes back.
</defect>

<predicate id="P1a" status="TESTABLE">
Strengthened form: for each read R of fragment F with hash h, there is a row with hash == h, kind == re-anchor, and seq > s0 (the tail seq sampled immediately before R). A decay-flag row referencing R also satisfies it, per L1 "or the read is flagged as decay".

- **Instrument:** chain tail-seq query plus row scan.
- **Moment:** s0 sampled before each read starts. Rows scanned after the read returns plus T_close. T_close = 5 s is ASSUMED; the document gives none.
- **Context:** quiescent chain with a single reader, so concurrent writers cannot supply a false seq > s0 row. N = 100 reads, split across the three read paths the document names: Q-knot reconstitution, lessons lookup, fragment verification.
- **PASS:** 100/100 reads have at least one qualifying row.
- **FAIL:** any read with 0 qualifying rows.
- **Negative control:** a mutant whose read path never writes. The literal L1 Test passes it 100/100. P1a must fail it 100/100. If P1a passes it, the harness is wrong.
</predicate>

<predicate id="P1b" status="TESTABLE">
Corrupted fragment. Flip one byte of F on disk, then read it.

- **PASS:** at least 1 decay-flag row, and 0 re-anchor rows for that read.
- **FAIL:** a re-anchor row exists for a fragment whose recomputed hash != the recorded hash. That would launder decay into a fresh anchor, contradicting "re-verified (hash)".
- **Negative example:** an uncorrupted fragment must yield a re-anchor and no decay flag.
</predicate>

<predicate id="P1c" status="UNPROVEN">
Crash between read and write-back (SIGKILL after data returns, before the write). The document says the read "is flagged as decay" but names no actor that flags it when the reader dies. The experiment is runnable: kill, wait T_sweep, query for a decay row. PASS is a decay row appearing within T_sweep. FAIL is no row ever. T_sweep and the sweeper are not in the document, so the claim is unjudgeable as written.
</predicate>

<predicate id="P1d" status="UNPROVEN">
"any read cycle" presupposes a read log, and the document defines none. Without one, reads cannot be enumerated and "any" cannot be checked. Also unprovable from this text: "The drain-status bug was exactly this missing write-back". It needs drain code and history, not in evidence.
</predicate>

---

## P2. Law 2: X-Y coincident-current addressing

<claim>L2 Test: "any event row missing organ or canonical is rejected at the stream gate (the event_stream emit already requires organ + kind; add canonical enforcement for memory-class events)."</claim>

<defect>
The parenthetical says canonical enforcement is still to be added ("add"), while the section header says "IMPLEMENTED". As written, enforcement of the Y-wire is a to-do, not a fact. "Memory-class" and "rejected" are undefined: the document does not say whether rejection is an exception, a DENIED row, or a silent drop.
</defect>

<predicate id="P2a" status="FIRES-ON-DOC">
Selector matrix at the stream gate. Use one kind from the gate's memory-class set (ASSUMED non-empty; if the set is empty the claim fires vacuously). Instrument: the event_stream emit call, with chain tail seq and a byte hash of every store the emit path touches (chain, indexes) read before and after. Moment: quiescent, same process.

| organ | canonical | expected | PASS | FAIL |
|---|---|---|---|---|
| set | set | accepted | tail seq +1 | rejected |
| set | absent | rejected | tail seq unchanged, store hashes identical, non-ok result | tail seq +1 or ok result |
| absent | set | rejected | same as above | same as above |
| absent | absent | rejected | same as above | same as above |
| set | "" or whitespace | rejected | same as above | accepted |
| set | non-existent canonical id | rejected | same as above | accepted (coincidence of strings, not of a real address) |

- **Negative control:** a non-memory-class kind with no canonical must be ACCEPTED. The document scopes enforcement to "memory-class events". Rejecting it is over-enforcement, which is also a fail.
- **Half-select side effects:** "it flips nothing" is falsified if any store hash changes after a rejected emit (for example an index updated before the gate).
</predicate>

<predicate id="P2b" status="UNPROVEN">
"no organ can write a memory alone" in the strong sense would require organ A to be unable to supply organ B's name. The document describes the organ field as "the organ's claim", a self-asserted selector, and gives no identity or authentication mechanism. Operationalizable only as field presence (P2a), not as unforgeability.
</predicate>

---

## P3. Law 3: the sense wire

<claim>L3: "A flip without a sensed pulse (an unreported change) = the divergence event that wakes the seat."</claim>

<predicate id="P3a" status="TESTABLE, parameters ASSUMED">
Inject an unreported flip: mutate a memory's state directly, bypassing event emit.

- **Instrument:** chain scan for a divergence-kind event, and the seat's wake signal.
- **Moment:** inject at t0 and poll until t0 + T_detect. T_detect is NOT in the document (ASSUMED 60 s).
- **PASS:** one divergence event referencing the mutated memory, and a seat wake, within T_detect.
- **FAIL:** none within T_detect.
- **Negative control:** a flip emitted through the normal event path (reported) must produ
