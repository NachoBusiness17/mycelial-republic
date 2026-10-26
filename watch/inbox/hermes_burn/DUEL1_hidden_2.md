# DUEL1_hidden_2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Safeguard review: docs/ref/OPERATOR_GATES_SCHEMA.md (draw v1h-0009, ask ab1-gates-safeguard)

## 1. Status: material not received

The CONTRACT names the file and its sha256 (`740686330a8d...27f23f6`), but the EVIDENCE block contains none of the file's bytes. The only text I have is the truncated first line: "You are an adversarial specification reviewer hunting the missing guardrail. Below is the full text of docs/ref/OPERATOR".

Under the estate laws, every claim about the code needs a file:line citation that resolves to quoted bytes, or it is marked UNVERIFIED. I have no bytes, so:

- **I cite no line numbers.** Any file:line from me would be invented.
- **I name no specific missing guardrail as a finding.** Saying "the spec lacks X" requires having read the spec.
- **Everything below is UNVERIFIED** against the file, and is labeled as such.

Measurement conditions for what follows: no instrument was run. This is a reasoning-only pass, at the moment of this answer, with the file text absent from context.

## 2. Deliverable: a landable guardrail clause plus a falsifiable checklist

The ask shape is "safeguard": find the missing guardrail in an operator gates schema. The one deliverable is a clause a seat can paste into the schema, and a check that tells the seat whether the clause is already covered.

### 2a. Candidate clause (UNVERIFIED as to whether the schema already has it)

```
## Gate Safety Invariants (normative)

G1. Fail-closed default. A gate whose state is missing, unparseable,
    expired, or of unknown type MUST evaluate as CLOSED (action blocked).
    It MUST NOT evaluate as open, and MUST NOT be skipped.

G2. Explicit expiry. Every gate that an operator can open or override
    MUST carry an expires_at (or a max_ttl). An open gate with no expiry
    is invalid and MUST be treated as closed (see G1).

G3. Scope binding. An opened gate MUST name the exact action, target,
    and context it authorizes. An open gate MUST NOT authorize anything
    outside that binding.

G4. Authority separation. The identity that requests an action MUST NOT
    be the sole identity that opens its gate, for gates marked
    high-impact.

G5. Auditable override. Every open or override MUST record who, when,
    why (non-empty free text), and which gate id, in an append-only
    record written BEFORE the action proceeds. If the write fails,
    the gate stays CLOSED.

G6. No silent schema drift. A gate definition with unknown fields or
    an unknown schema version MUST be rejected, not partially applied.
```

### 2b. Positive and negative examples

**G1 (fail-closed)**
- Positive: `gate.state` is absent, so the action is blocked and the reason `gate-state-missing` is logged.
- Negative: `gate.state` is absent and the loader defaults to `open`. This is the classic missing guardrail.

**G2 (expiry)**
- Positive: `{id: deploy-prod, state: open, expires_at: 2025-01-01T12:00Z}`. After that time it evaluates as closed.
- Negative: `{id: deploy-prod, state: open}` stays open indefinitely after an operator forgets it.

**G3 (scope)**
- Positive: opening `deploy-prod` for `service=api, env=prod` does not authorize `service=billing`.
- Negative: a gate id alone is treated as global permission.

**G5 (audit before action)**
- Positive: the audit write succeeds, then the action runs.
- Negative: the action runs, then the audit write fails and nobody knows.

### 2c. How a seat applies this

Step 1. Open the file at the pinned hash. Verify with `sha256sum docs/ref/OPERATOR_GATES_SCHEMA.md`, which must equal `740686330a8d27fd5ca0e2ae189cfa07b10872149e1f8b6520d02b27bd7c23f6`. If it does not, stop, because this review does not apply.

Step 2. For each of G1 to G6, search the file for the normative statement. Record one of:
- COVERED, with file:line and the quoted bytes
- PARTIAL, with the quoted bytes and the gap
- ABSENT, meaning no quoted bytes exist (state the search terms used)

Step 3. Paste only the clauses marked ABSENT or PARTIAL into the schema.

Step 4. Rank any remaining ABSENT items by blast radius. Fail-closed (G1) and audit-before-action (G5) rank highest because their absence fails silently.

## 3. Falsifier for this deliverable

This deliverable is wrong or useless if any of these holds:

1. **Full coverage.** The file already covers G1 to G6 with COVERED citations. The clause adds nothing, and the real missing guardrail lies outside this list.
2. **Out of scope.** The schema describes pure data shapes with no runtime evaluation semantics, so G1 and G5 do not belong in the schema and the clause is misplaced.
3. **Incoherence.** Pasting the clause contradicts an existing normative statement in the file (for example, a documented default-open gate).

Any of these should be reported back with quoted bytes.

## 4. What I need to turn this into a verified finding

Resend the file body (or at least the gate-state, override, and expiry sections). I will then name the single missing guardrail with file:line citations and a ready-to-apply patch.
