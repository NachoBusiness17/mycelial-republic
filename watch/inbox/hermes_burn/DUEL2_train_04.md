# DUEL2_train_04 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Contender pass: ab1-chainreg-safeguard (v1t-0005, train)

## 1. Status: the material did not arrive

The CONTRACT names `docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md` (sha256 `fc3d0686...a8ca1`). The only bytes I received are the truncated `first_line`:

> `You are an adversarial specification reviewer hunting the missing guardrail. Below is the full text of docs/ref/CHAIN_V2`

No spec body follows. Under the estate laws this means:

- **No file:line citations are possible.** Every claim about the spec's contents is UNVERIFIED.
- **I cannot name "the missing guardrail" as a verdict.** That would require showing the spec is silent on it, and I cannot show silence in text I have not seen.
- **The sha256 is unchecked.** I cannot confirm that any text later supplied matches it.

Negative example, which I am deliberately not doing: inventing a section number such as "Section 4.2 lacks X" and presenting it as a finding. That would be a fabricated citation.

## 2. Conditional deliverable (UNVERIFIED, apply only after the check in section 3)

This is a prior, not a finding. For an anchor registry (a registry that maps chain or anchor identifiers to hashes or heights), the guardrail most often absent is **conflicting re-registration rejection**.

**Candidate clause, drop-in text:**

```
G1 (anchor immutability).
Registering an anchor whose key already exists MUST be
  (a) a no-op if the stored (key, hash, height) tuple is byte-identical, or
  (b) rejected with a hard error if any field differs.
No code path may overwrite or silently update an existing anchor.
Correction of a wrong anchor requires a new, explicitly versioned
entry that supersedes the old one and leaves the old one readable.
```

- **Positive example:** the same `(key=A, hash=H, height=100)` is registered twice. The second call is an idempotent no-op.
- **Negative example:** `(A, H2, 100)` arrives after `(A, H, 100)`. Under G1 it is rejected. Without G1, last-write-wins silently rewrites history, and every verifier that trusted `A` is now wrong with no signal.

## 3. Applicability check (run this before landing G1)

1. Verify that the supplied file's sha256 equals `fc3d068662e2f20c4190f128e483cd3368dfc46385dd42163dfeae16a02b8ca1`.
2. Search the spec for any rule governing a duplicate key or re-registration.
3. If such a rule exists and rejects conflicts, G1 is already covered and this candidate is moot. Move to the next candidate: reorg or fork handling, then authority over who may register.
4. If the spec is silent or says "update" or "overwrite", land G1 and cite the line that allowed it.

## 4. Falsifier for this deliverable

G1 is wrong or redundant if the spec, at any cited line, already (a) rejects a conflicting re-registration, or (b) defines the registry as append-only with keys that cannot collide, for example because the key is a content hash of the entry. Either one falsifies G1 as "the missing guardrail".

## 5. What I need to finish

Please resupply the full body of `CHAIN_V2_ANCHOR_REGISTRY_SPEC.md`. With the bytes in hand I will return one patch with file:line citations quoted from the spec. Until then, section 2 stands only as a hypothesis.
