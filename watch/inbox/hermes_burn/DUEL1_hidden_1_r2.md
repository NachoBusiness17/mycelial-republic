# DUEL1_hidden_1_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Finding: the write-back has no receipt bound to the read

**Source:** docs/ref/CORE_MEMORY_PROTOCOL.md, sha256 f014e1bd...7977. Line numbers are UNVERIFIED because the evidence block carries none. Every citation below is a quoted byte string plus its section heading.

## 1. The missing safeguard

The document states that a read ends with a re-anchor write. It never states that the read is **incomplete, and its content untrusted, until that specific write is acknowledged**. It also never requires a write-back failure to be loud outside the failing write path.

Three gaps follow from this:

- **No read-to-write-back link.** There is no read_id or equivalent tying a re-anchor row to the read that caused it.
- **No ordering or ack gate.** Content can be returned and acted on before the write-back lands.
- **No intent record.** A reader that dies, or whose append fails, between read and write-back leaves nothing a sensor could see.

The physical analogy hides this. In real core, a failed write-back leaves a zeroed cell, so the loss is self-announcing. In the fleet a read is non-destructive: the old fragment and its old anchor stay intact. A failed write-back therefore looks exactly like a healthy read.

## 2. The accident or attack path

Each step names the clause it hides behind.

1. **A read succeeds.** A seat reconstitutes a Q-knot or looks up a lesson, and the content is returned.
   - Hides behind Section 1: "every read of a fleet memory ... ENDS with a re-anchor write". This is a convention with no stated ordering relative to returning content.
2. **The re-anchor append fails silently.** Possible causes are a gate rejection, a dropped connection, or a crash between read and write. A deliberate trigger is a re-anchor payload that lacks `canonical`.
   - Hides behind Section 2: "any event row missing organ or canonical is rejected at the stream gate". The rejection is not required to leave a record.
   - Hides behind Section 5: "content present or event absent". An absent event is the permitted outcome of a failed append, so the honesty assert is satisfied.
3. **The decay flag is the same write path.** Section 1 says "or the read is flagged as decay". The flag channel is unspecified. If it is an event append, it fails the same way. No clause says what happens when both fail.
4. **The reader has already acted.** This is the drain-status bug the document claims to fix: "the drains read the backlog, acted, and never marked the source". The fix is only "ENDS with", so the failure is reproducible.
5. **The sense wire stays silent.**
   - Section 3 detects "A flip without a sensed pulse (an unreported change)". A missing write-back is not a flip, so no divergence event fires.
   - Section 4 says "Absence of a write is not inhibition; inhibition is a recorded event". Nothing records this absence, so it is not even an inhibition.
   - The document's own admission, "The min-33 silent death was a read with no sense wire", describes this class and does not close it.
6. **The Section 1 test passes falsely.**
   - Its text is: "the read fragment's hash exists in the chain post-read".
   - The fragment's original commit row already holds that hash. The predicate is true with zero re-anchor activity.
   - Even under the strict reading, where "post-read" means a row stamped after the read, the predicate is not bound to this read. Another reader's re-anchor of the same fragment satisfies it. Whether the strict reading is intended is UNPROVEN, because the document does not say.
7. **The decay never surfaces.** The "no re-anchor row" alarm is the only decay signal. An attacker or a flaky path that can fail re-anchors can keep a fragment read-but-never-re-anchored indefinitely while the audit stays green.

**Positive example (today, passes wrongly):**
- Read F, with the re-anchor append stubbed to throw.
- The read returns content with exit 0.
- The chain still holds F's original hash, so the Section 1 test is green.

**Negative example (what should happen):**
- The same fault produces a returned error, or a decay row carrying this read's id.
- The consumer receives no content it may treat as anchored.

## 3. The minimal amendment

**Slot:** Section 1 ("DESTRUCTIVE READ + MANDATORY WRITE-BACK"). Insert it as a new paragraph between **Fleet implementation** and **Test**, and replace the Test paragraph with the predicate in section 4 below.

**Exact clause text:**

> **Write-back receipt (fail-closed).** Before any content is returned, a read MUST append a `read_open` event carrying a fresh `read_id`, organ, and canonical; if that append is not acknowledged, the read returns no content. A read is complete only when the chain holds an acknowledged re-anchor event carrying that `read_id`, organ, canonical, and the hash of the exact bytes returned, at a sequence position after the `read_open`. Content from a read lacking that receipt is UNANCHORED and MUST NOT be acted on as memory. The reader MUST then append a `decay_flag` carrying the same `read_id`. If the `decay_flag` append also fails, the reader MUST return an error to its caller in the call result, outside the event chain. An existing anchor of the same hash never satisfies this clause. Any `read_open` with neither a receipt nor a `decay_flag` after deadline T is a divergence event for the lattice (Law 3). T is a deployment parameter and is UNPROVEN by this document.

**Why this is minimal:**
- It adds one write-ahead intent record and one binding key.
- It adds one failure-escalation rule.
- It reuses the existing lattice sense wire for orphan detection and does not add a new mechanism.

**Known limit:** "MUST NOT act" binds only reader code. The document cannot prove how consumers are implemented. That is UNPROVEN, and the clause does not hide it.

## 4. The test predicate

**Replacement Test text:**

> For every read `r` of fragment hash `h`, at least one holds: (a) the chain contains a re-anchor event with `read_id = r.id`, `hash = h`, organ and canonical present, and `seq > r.open_seq`; (b) the chain contains a `decay_flag` with `read_id = r.id`; (c) `r` returned an error to its caller. Otherwise the protocol is violated.

**Instrument and moment:**
- The instrument is a query on the event chain, run after the read call returns.
- The setup is a fault injection that makes the re-anchor append throw or be rejected.
- The context is a single reader with no concurrent writers.
- These assumptions are mine. The document names no harness.

| Case | Today's Law 1 test | New predicate |
|---|---|---|
| Fault injected on re-anchor, read returns content, no flag, no error | PASS (original hash exists) | FAIL (none of a, b, c) |
| Same fault, amended reader returns UNANCHORED, `decay_flag` present | not applicable | PASS via (b) |
| Same fault, `decay_flag` also fails, error returned | not applicable | PASS via (c) |
| No fault, receipt carries `read_id` | PASS | PASS via (a) |
| Two readers of the same fragment, A's re-anchor dropped, B's succeeds | PASS | FAIL for A |

## 5. Falsifier

This finding is wrong if either of two things holds:

- The unquoted implementation behind "re-anchor event" already carries a per-read key and the stream gate already logs its rejections. The document does not show this, so it is UNPROVEN, and the finding judges only the specification text.
- A conforming implementation exists in which a silently dropped re-anchor still fails the new predicate's negation. That would show the predicate is not a strict improvement.
