# ATTACK — three-body T1 (ONI lane, battle-tested against bytes)

**Claim 1 (charter = "executable law" in patch 1): AMEND.** /patches/fix_authority_label_gate.json replace block, switchboard_v2.py:279: the gate DENIEDs only `("untrusted-instruction", "external-content")`, and `.search` confirms the else-branch default `"agent-generated"` (line 274) still resolves AUTHORIZED. Two of seven labels, awaiting apply — that is a guard, not "executable law."

**Claim 2 (permission core real + fail-closed): KEEP.** switchboard_v2.py:240-245: `_implicit_authority` → `policy_engine.validate_authority`, fail-closed `_denied`. Runs in-cage; testable today, no host apply.

**Claim 3 (gate tests proposer-chosen string): KEEP.** propose() (:134,:160) = `authority_label or "agent-generated"` — caller-settable; CLASSIFIED (:108, CLI-only cmd_classify :716) never called by propose/grant/execute. Exhaustive grep + sed :129-165 confirm. `propose(authority_label="untrusted-instruction")` reaches AUTHORIZED today — live-cage falsifiable.

**Cage-testability:** Claims 2 and 3 are testable now; only claim 1 is host-apply-dependent.

**Weakest sentence:** Claim 1's "is encoded as executable law in patch 1" — overclaims: unapplied, 2-of-7, anchors nothing to truth.
