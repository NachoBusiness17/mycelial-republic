# THREE-BODY T1 WARM PACK (v0 test — shared pre-warm for PROPOSER / ONI / SCRIBE)

## The question (all three bodies answer this)
Is the swarm's authority-boundary doctrine internally consistent across: (a) the riddler charter,
(b) the switchboard state-machine doctrine, (c) the 4 staged patches that enforce it?
Deliverable: verdict + 3 testable claims + the single inconsistency that matters most (if any).

## Warm spine (law, already verified — do not re-derive)
- Riddler law: riddle = isomorphic re-encoding, not redaction; decode gate before publication.
- Charter line: "A roast can become a proposal; it cannot become a permission."
- Switchboard doctrine chain: POSTED→CLASSIFIED→PROPOSED→AUTHORIZED/DENIED/DEFERRED→EXECUTING→COMPLETED/FAILED→RECEIPT_COMMITTED.
- Authority labels (every board item): operator-authored | operator-confirmed | agent-generated | external-content | tool-output | derived-summary | untrusted-instruction.
- Audit verdict (byte-verified 05:00Z): decision core real + fail-closed where it runs; labels unenforced at gate; 6/7 states wired; blackboard_post = unmeshed bypass writer.
- Staged patches (all validated: target exists, unique search match, CRLF-correct, awaiting host apply):
  1. /patches/fix_authority_label_gate.json — sensitive labels never self-grant (fail DENIED)
  2. /patches/fix_policy_engine_failopen.json — missing status → UNKNOWN, never AUTHORIZED
  3. /patches/fix_blackboard_post_provenance.json — bypass writer stamps tool-output/UNMESHED
  4. /patches/fix_harness_receipt_chain.json — harness runs full receipt chain
- Blackboard fact (05:01Z row): 89 entries, newest already carries authority fields (switchboard path), no UNMESHED stamp = patch 3 not yet applied.

## Roles (Kabuki)
- PROPOSER (5.3): reads pack + primary files; writes PROPOSAL.md — verdict, 3 testable claims, one biggest inconsistency. Own voice. ≤400 words.
- ONI (flash): attack pass — reads PROPOSAL.md; finds the load-bearing error; cites bytes. ATTACK.md ≤200 words.
- SCRIBE (flash): registrar — verifies every pointer PROPOSAL cites (exists + actually says what's claimed). REGISTRY.md ≤200 words: per-pointer ok/wrong.

## Gates (SWARM_LENS v0, mandatory)
Ledger-first · primary bytes > lane report · calibration words only · no pointer, no claim.
