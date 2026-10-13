## Finding — what your cell yields
The docs_register domain (STACK_V1.md) claims to be a de-riddled register: a self-description that honestly states what it over/under-claims. **This claim is DISPUTED by the repo shape.** The artifact does not exist as a single file; instead, the register is distributed across multiple surfaces, with the closest artifact being the hash-chained grounding_wave.md ledger that records tri-state claims (Supported/Disputed/Unproven) with falsifiers and evidence paths. The register’s core promise—honest self-description—is not met by a single authoritative STACK_V1.md; instead, the house uses a living ledger (grounding_wave.md) that is itself the register and falsifier engine.

## Evidence — what in the repo supports it (file/shape, no invention)
- grounding_wave.md (dashboard/static/grounding_wave.md) is the active register artifact: it is a hash-chained ledger of tri-state claims with falsifiers, evidence paths, and receipts. It is the only file in the repo that functions as a register with falsification discipline (lines 3–6, 13, 25–27, 209–214).
- The claim that STACK_V1.md is the self-description register is **not supported by any file named STACK_V1.md** in the repo. No such file exists in docs/, docs/register/, or any subdirectory (verified by directory listings).
- The grounding_wave.md ledger explicitly states its role as the register: “GROUND circuit ledger — one verified claim per post, hash-chained, tri-state only” (line 3–4). It is the canonical register artifact for the house.
- The falsifier discipline is enforced in the ledger: rows auto-demote from Supported to Unproven if they lack a second witness (e.g., lines 9, 15, 21, 27, 105, 117, 123, 135, 141, 165, 171, 177). This is the register’s operating principle.
- The docs_register domain’s claim to be a de-riddled register is **over-claimed**: the register is not a single markdown file but a distributed, hash-chained ledger with tri-state discipline and falsifiers. The repo shape contradicts the claim.

## Risk if wrong — what the audit breaks on if this is missed
If the audit accepts the over-claim that STACK_V1.md is the register, it will miss that the actual register is the grounding_wave.md ledger with falsifier discipline. This risks:
- Misidentifying the authoritative register surface (a single file vs. a living ledger).
- Overlooking the tri-state falsifier engine that the house uses to police its own claims.
- Failing to verify that the register’s falsifier discipline (second witness, auto-demotion) is enforced in practice.
- Missing the fact that the register is hash-chained and append-only, not a static markdown file.

## The act — the concrete prep step (file/spec/number)
Create a minimal, audit-ready artifact that clarifies the register’s actual shape and falsifier discipline:

File: `docs/audit_prep/REGISTER_CLARIFICATION_20260912.md`
Content:
```markdown
# Register Clarification (docs_register domain)

## Claim
The docs_register domain claims to provide a de-riddled register (STACK_V1.md) that honestly states what it over/under-claims.

## Verdict
DISPUTED by repo shape.

## Evidence
- No file named STACK_V1.md exists in the repo (docs/, docs/register/, or any subdirectory).
- The active register artifact is the hash-chained grounding_wave.md ledger (dashboard/static/grounding_wave.md), which records tri-state claims with falsifiers and evidence paths.
- The ledger enforces falsifier discipline: rows auto-demote from Supported to Unproven if they lack a second witness (see lines 9, 15, 21, 27, 105, 117, 123, 135, 141, 165, 171, 177).
- The register is a living ledger, not a static markdown file.

## Falsifier
If a single authoritative STACK_V1.md file is found in the repo, this cell is proven wrong.
```

Then, update the site build to include this clarification in the audit bundle:
- Add `docs/audit_prep/REGISTER_CLARIFICATION_20260912.md` to the audit_bundle manifest.
- Ensure the file is included in the dist_audit/site build.

## Falsifier — what would prove this wrong
Discovery of an authoritative STACK_V1.md file in the repo (docs/, docs/register/, or any subdirectory) that serves as the de-riddled register for the docs_register domain. Until then, the cell stands as DISPUTED by repo shape.
