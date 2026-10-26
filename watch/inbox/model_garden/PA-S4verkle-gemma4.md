# PA-S4verkle-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

The CONTRACT demands a definitive manual, demonstrating both the canonical, successful usage patterns and the specific failure modes (negative examples) that the GATES enforce.

Below is the deliverable, styled as a usage contract for the `grounding_wave` system.

***

### 📜 Grounding Wave Usage Contract (v4)

#### I. System Overview and Core Verbs

The `grounding_wave` ledger is an append-only, write-protected memory system. All interactions occur via the command line interface (`mag.grounding_wave`). Failures result in a `REFUSED GATE` exit code (2), which must be handled by the calling process.

| Verb | Purpose | Required Inputs | Write Gate | Read Gate |
| :--- | :--- | :--- | :--- | :--- |
| `post` | Admission of a new claim. | `claim`, `verdict`, `evidence`, `seat` | G1 (Structure) | `verify` (Linkage) |
| `void` | Declaring a row invalid. | `row` (Target Hash/Line), `reason_code`, `seat` | Cross-signing via `witness` | `verify` (Admission) |
| `contest` | Placing a row under active dispute. | `row`, `reason`, `seat` | G1 (Structure) | N/A |
| `witness` | Providing secondary, independent validation for a write, or signing a void/contest. | `row`, `seat` (Second Seat) | G1 (Witness Check) | N/A |
| `verify` | Auditing the chain integrity (Hashes, Evidence Pointers, Corroboration counts). | None | None | Full Audit |
| `view` | Rendering the effective ledger (voids factored out). | None | None | Logical View |

***

#### II. Positive Examples (Successful Operations)

These examples illustrate canonical, successful interactions, assuming write access and required proofs (like second witnesses) are available.

##### 🟢 Example 1: Initial Claim Admission
*A standard attempt to record a new claim that is adequately supported by documented evidence and has received multiple witnesses.*
```bash
# Scenario: Author (alice) posts a claim. Evidence is provided. Second seat (bob)
# signs this post asynchronously before the final write lock is released.
$ python -m mag.grounding_wave post \
    --claim "The sky is visible from Paris." \
    --verdict SUPPORTED \
    --evidence "/docs/sky_spectral_constants.pdf" \
    --note "Initial post based on observed constants." \
    --seat "alice" \
    --witness "bob"  # Signature of independent witness
$ POSTED #a1b2c3d4e5f6 (SUPPORTED) — POSTED on line 122
// Verification passes: LINKAGE-PASS (Hashes correct, Evidence valid)
$ python -m mag.grounding_wave verify
PASS Verification successful. Witnessed: A2_EPISTEMOLOGY_ENGINE.md
```

##### 🟢 Example 2: Voiding a Claim
*Demonstrates the multi-party legal process required to invalidate a previous record, requiring a designated second seat.*
```bash
# Scenario: Target hash 'a1b2c3d4e5f6' is deemed malformed (e.g., wrong timestamp).
# The void must be signed by a second, independent seat (Charlie).
$ python -m mag.grounding_wave void \
    --row #122 \
    --reason-code MALFORMED \
    --reason "Timestamp conflict: Post claims year 2024, ledger shows 2025." \
    --seat "charlie" \
    --evidence "/critiques/time_drift.txt" \
    --witness "david" # Second signee for the void
$ VOID POSTED #f9e8d7c6b5a4 (voids a1b2c3d4e5f6) — void pointing to line 122
// Verification passes: LINKAGE-PASS (void hashes point correctly)
$ python -m mag.grounding_wave verify
PASS Verification successful. Witnessed: (A2_EPISTEMOLOGY_ENGINE.md, nullified)
```

##### 🟢 Example 3: Auditing the Effective Ledger
*Used when the operator needs to know the logical state, factoring in all voids, but without writing to the ledger.*
```bash
$ python -m mag.grounding_wave view
# Displays the admission view (effective ledger):
# ---------------------------------------------------------
# Row 122: Status: VOID. Targets: a1b2c3d4e5f6. Reason: MALFORMED.
# Record 121: Status: CORROBORATED. Claim: Initial observation.
# Record 120: Status: SUPPORTED. Claim: Low confidence initial draft.
# (The system successfully hides the voided record from the main view)
```

***

#### III. Negative Examples (Gate Refusals and Mandatory Failures)

These examples demonstrate specific attempts that will fail the system's logic gates and result in a `GATE-REFUSAL: ...` message and exit code 2.

##### 🔴 Example 1: Insufficient Corroboration (Missing Witness)
*Attempting to post a claim that requires mandatory corroboration (SUPPORTED verdict) but fails to provide the required second, non-authoritative witness signoff.*
```bash
# Scenario: Alice posts a claim, but only her own seat is used for the witness signature.
$ python -m mag.grounding_wave post \
    --claim "The quantum entanglement field is stable." \
    --verdict SUPPORTED \
    --evidence "/physics/quantum.pdf" \
    --note "Requires independent validation." \
    --seat "alice" \
    # Note: We intentionally omit --witness or set it incorrectly
$ REFUSED GATE-CORROBORATION: Claim MUST be ratified by a second, unaligned seat.
$(echo $? # Output will be 2)
```

##### 🔴 Example 2: Evidence Mutation Detection
*Attempting to record a post where the evidence hash pointer (`src_sha256_12`) points to a file that has been programmatically altered (mutated) since admission.*
```bash
# (Conceptually: The internal ledger check finds the hash mismatch)
# $ python -m mag.grounding_wave post ...
# Gate check fails because the calculated hash of the evidence file
# does not match the hash recorded in the previous successful post.
GATE-EVIDENCE-MUTATED: The provided evidence source hash conflicts with the
