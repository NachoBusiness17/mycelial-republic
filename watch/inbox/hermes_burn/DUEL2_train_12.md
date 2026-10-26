# DUEL2_train_12 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Red-team pass: `ab1-chainreg-exploit` (draw `v1t-0013`, train)

## 1. Status: the material was not delivered

<status>
- The CONTRACT names `docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md` (sha256 `fc3d0686...8ca1`). Only the first line of the prompt arrived, truncated: `You are a red team reviewing a protocol specification against adversarial agents. Below is the full text of docs/ref/CHA`.
- No spec bytes are in the EVIDENCE block. I cannot cite file:line for any claim about the spec, and I cannot check the sha256.
- Under the estate laws, every spec-specific claim is therefore **UNVERIFIED**. I will not invent section numbers, quotes, or findings.
- Measurement conditions: no instrument was run. The moment is this single pass. The only context is the contract header. Nothing below is a measurement of the spec.
</status>

## 2. Deliverable: a conditional exploit checklist for the seat to apply as-is

This is not a finding list. It is a set of hypotheses about what an anchor registry spec can get wrong, each with a pass/fail test that resolves only against quoted spec bytes. The seat (or a re-run with the file attached) fills the `CITE` column. A row with no quoted bytes stays UNVERIFIED.

<checklist>

| ID | Attack hypothesis (UNVERIFIED) | Closed if the spec says (positive) | Open if the spec says (negative) | CITE |
|----|----|----|----|----|
| R1 | **Cross-chain or cross-version replay.** A valid anchor or registration is replayed on another chain or under a V1 or V2 registry. | Signed payloads include chain ID, registry ID, and version in a domain-separation tag. | "Signature over (anchor_hash, height)" with no chain or registry binding. | UNVERIFIED |
| R2 | **Equivocation.** Two different anchors are registered for the same height or key, and consumers pick whichever they saw first. | A single canonical anchor per key. A second conflicting submission is rejected, or is slashable and recorded. | Silent "last write wins" or "first write wins" with no conflict handling. | UNVERIFIED |
| R3 | **Reorg or rollback.** An anchor is accepted before finality and later orphaned, but dependents keep trusting it. | Names a finality depth and defines a rule for invalidating dependents. | "Anchor is valid once observed" with no depth. | UNVERIFIED |
| R4 | **Registration squatting or front-running.** An attacker registers an identifier first, or races a pending registration. | Commit-reveal, or identifier derived from the registrant's key. | Names are first-come-first-served and the identifier is a free-form string. | UNVERIFIED |
| R5 | **Unauthorized update or revocation.** Authority to update, rotate, or revoke is unclear, or revocation races with use. | Explicit authority set, a rotation procedure, and an ordering rule for revoke versus use. | "The owner may update" with owner undefined or transferable without proof. | UNVERIFIED |
| R6 | **Stale-anchor verification.** A proof is checked against an old anchor that should have been superseded. | Proofs carry an anchor epoch, and verifiers must reject epochs older than a stated window. | No freshness bound. | UNVERIFIED |
| R7 | **Canonicalization or collision.** Different encodings of the same key or hash map to different registry entries, or distinct entries collide. | Specifies a byte-exact encoding, case rules, and length-prefixing. | Hash over concatenated variable-length fields with no delimiters. | UNVERIFIED |
| R8 | **Sybil or spam growth.** Free registration permits unbounded state growth or DoS. | A cost, a quota, or an eviction rule. | No bound on entries per identity. | UNVERIFIED |
| R9 | **Time-source manipulation.** Expiry or ordering depends on a clock the submitter controls. | Uses a chain-derived height or timestamp with a stated tolerance. | "Timestamp supplied by the registrant." | UNVERIFIED |
| R10 | **Trust-root bootstrap.** The initial anchor or admin key is unauthenticated or has no rotation path. | Genesis anchor pinned in the spec, with a documented rotation or compromise procedure. | "Operator configures the root." | UNVERIFIED |

</checklist>

### Worked example of the method (illustrative only, not a finding)

Take R1.
- **Negative:** the spec text reads `anchor = sign(sk, H(root || height))`. Nothing binds the chain, so a signature made on chain A verifies on chain B. The row is OPEN, and the exploit is to replay the signature.
- **Positive:** the spec text reads `anchor = sign(sk, H("CHAINREG/v2" || chain_id || registry_id || root || height))`. The row is CLOSED for replay. The seat then checks whether verifiers are *required* to rebuild that same preimage.

## 3. How to land it

1. Attach the actual spec bytes and confirm the sha256 matches `fc3d0686...8ca1`.
2. For each row, quote the governing line as `file:line "quoted text"`. If no governing text exists, mark the row OPEN-BY-OMISSION.
3. Rank OPEN rows by whether an adversarial agent can exploit them without privileged keys.

## 4. Falsifier

This deliverable is wrong or useless if either of these holds once the spec is read:
- Fewer than 3 of R1-R10 map to any spec text, which would mean the guess at the registry's design from its filename was off. The checklist should then be regenerated from the spec's own state and message definitions.
- The spec contains an exploitable flaw that falls outside R1-R10, which would show the checklist's coverage is too narrow.

Either outcome means a real red-team review needs the file, which is absent from this pass.
