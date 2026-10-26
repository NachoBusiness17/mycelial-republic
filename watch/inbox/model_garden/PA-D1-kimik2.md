# PA-D1-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

I need to read the three doctrine chapters and produce the adversarial deliverable per the CONTRACT. Let me analyze the evidence files.

## Chapter 1: accuracy.md (00__accuracy.md)

### (1) Strongest objection surviving scrutiny

The cheap seat's objection ("citation-resolution gate at landing is sufficient" assumes citation failure not reasoning failure) is valid but incomplete. Stronger: **the gate's falsifier is itself unfalsifiable**. Incident 1's falsifier requires resolving citations "in the same session" - but the session boundary is operator-defined, not instrument-defined. The gate passes when the operator declares session continuity, making the gate a rubber stamp for operator confidence, not a mechanical barrier.

### (2) Line-pinned defects

- "the ledger append path...runs a citation resolver before accepting verdict=LANDED" (00__accuracy.md:incident 1, "Instrument upgrade") - **UNVERIFIED**: no code shown, mechanism described in prose only
- "Free stealth lanes bank findings, never trusted work; verification climbs to the funded tier" (00__accuracy.md:incident 1, "Instrument upgrade") - **circular**: defines "trusted" as "funded," with no instrument measuring trust transfer
- "The four fold outputs are untracked in git with no committed history" (00__accuracy.md:incident 3) - **defect**: fold outputs are load-bearing state with no versioned recovery path

### (3) ONE landable amendment

Add after incident 1's instrument upgrade: "The citation resolver logs its own session boundary as a content hash of the resolving process's environment; a LANDED row carries this hash, and a later falsifier can prove session discontinuity by environment drift without trusting operator memory."

---

## Chapter 2: logic.md (01__logic.md)

### (1) Strongest objection surviving scrutiny

The cheap seat's "0/1/2 smuggles two ontologies" understates the problem. Stronger: **law 4 (wiring liveness) contradicts law 2 (census denominator)**. Law 4 says "wired is a truth only the outside can decide"; law 2 demands counts name "instrument, moment, and delta." But the outside-decider is itself an instrument at a moment - the census cannot simultaneously be inside (named, momented) and outside (wiring-truth). The system has no metalevel to observe itself.

### (2) Line-pinned defects

- "The 0/1/2 exit contract is a typed trivalent logic: pass, refutable violation, undecidable" (01__logic.md:law 1, quote from w4-14.md) - **UNVERIFIED**: w4-14.md not in evidence, line range not given
- "uncollapsed/never-disproven vocabulary has ZERO hits in both dirs" (01__logic.md:checks) - **honest gap treated as finding**: propagation failure is recorded as success because the search instrument returned 0
- "the portable-seed seal check from w4-41 section 6 was not rerun because state/CURRENT.md no longer holds it" (01__logic.md:one sentence) - **defect**: a seal check's absence is noted but not instrumented as debt

### (3) ONE landable amendment

Add to law 4: "The outside-decider instrument is itself census-registered as a component with zero expected external callers; its liveness verdict is always FRAGILE-ALIGNED per law 5, and its outputs are banned from corroborating any claim about other components' wiring."

---

## Chapter 3: operations.md (02__operations.md)

### (1) Strongest objection surviving scrutiny

The cheap seat's "waves partition cleanly" is correct but narrow. Stronger: **the doctrine has no instrument for coordination cost because it has no seat for coordination failure**. Every "owner: operator" residual (sections 4, 5, 6) is a coordination failure buried in prose. The operator is the black hole where unpriced overhead goes - not a role but a void. The 50-wave budget is denominated in asks, not in cross-arm synchronization events, so the denominator is systematically undercounted by design.

### (2) Line-pinned defects

- "the standing surface-rebuild verb...use it at wave close" (02__operations.md:F9) - **contradiction**: "wave close" is undefined; waves are defined as discrete units in A1-A8 but as continuous overlapping processes in the failure narratives
- "the 15-16 rung stays untested, probe armed NOT fired...fires only on explicit operator GO" (02__operations.md:section 4) - **defect**: an instrument whose firing condition is operator discretion is not an instrument, it is a request
- "No parade: eight failures, eight receipts, seven mechanisms landed on file before this sitting, two wired this sitting, six items still owed with named owners" (02__operations.md:Decision ledger) - **arithmetic error**: 7+2+6=15, not 8; the ledger does not balance

### (3) ONE landable amendment

Replace "owner: operator" with "owner: [seat_name] by [timestamp] or escalates to cross-arm negotiation logged in [path]" for every residual; add instrument: `tools/coordination_cost_tally.py --wave-id` that counts inter-arm messages per wave and surfaces the count in the receipt header.

---

## (4) THE PATTERN

**The fleet's doctrine blind spot: operator-as-residual.** Every chapter buries uninstrumented decisions in "operator" calls - session boundaries, probe firing, surface-rebuild cadence, cross-arm negotiation. The operator is the doctrine's own uncollapsed carrier: not a seat but a placeholder for "someone will decide." The pattern is **procedural debt without procedural creditor** - every "owner: operator" is a liability that cannot be called due because the creditor is undefined.

---

## (5) THE NEXT LEG (3 questions)

1. **What is the instrument shape that measures operator decision latency?** The evidence shows "operator GO" gates (02__operations.md:section 4) but no logged timestamps of request-to-response; the web or corpus may hold a pattern for procedural creditor instrumentation.

2. **How many of the 12 corrected verdicts in accuracy.md had valid citations at landing?** The cheap seat hypothesizes at least one; the full count would falsify or vindicate the citation-resolution gate design. The gala lane JSONs or LEDGER.jsonl may hold this cross-reference.

3. **What is the byte-exact definition of "wave" that makes A1-A8's discrete-unit assumption and F7's fold-identity assumption simultaneously true?** The operations chapter uses "wave" for both atomic dispatch events and extended process overlaps; the git history of the-gala.dwf.ts or a prior gala receipt may show when the definition forked.
