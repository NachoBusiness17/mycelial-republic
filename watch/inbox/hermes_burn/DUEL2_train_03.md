# DUEL2_train_03 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Contender pass: ab1-chainreg-defects (draw v1t-0004, train half)

## 1. Status: BLOCKED on missing material

The contract names `docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md` (sha256 `fc3d0686...8ca1`). The EVIDENCE block does not contain its text. The only bytes I received are the truncated first line:

> `You are an adversarial specification reviewer. Below is the full text of docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md (Chai`

That line is the review prompt's preamble, not the spec. I have no spec body, no line numbers, and no way to check the hash.

Under the estate laws, any defect I reported would be one of two things:
- a fabricated citation, which breaks "citations resolve to quoted bytes or are marked UNVERIFIED", or
- a generic guess presented as a finding, which breaks "trust bytes, not reports".

So **I report zero defects against this spec.** Every spec-specific claim below is marked UNVERIFIED.

## 2. Measurement conditions

- Instrument: none run. No file read, no hash check.
- Moment: single-turn answer, with only the truncated first line available.
- Context assumption: the material was meant to be inlined but was dropped or truncated upstream.

## 3. Landable deliverable: a defect-record spec for when the bytes arrive

A seat can apply this as-is to the full text. Each defect is one record:

```
DEFECT <n>
  cite:       <file>:<line>[-<line>]  + quoted bytes (verbatim, <=2 lines)
  class:      one of {AMBIGUITY, UNDEFINED-TERM, INVARIANT-GAP, RACE/ORDERING,
              AUTHZ-GAP, REPLAY/REORG, VERSIONING, SELF-CONTRADICTION,
              UNTESTABLE-REQUIREMENT, MISSING-FAILURE-MODE}
  claim:      one sentence stating what is wrong
  trigger:    concrete input/state sequence that exposes it
  consequence: what breaks (registry divergence, duplicate anchor, etc.)
  fix:        minimal replacement text, ready to paste
  falsifier:  the observation that would show this is NOT a defect
```

**Positive example (valid shape, illustrative only, not a finding about this spec):**
```
cite: SPEC.md:88 "An anchor MUST be unique."
class: UNDEFINED-TERM
claim: Uniqueness scope is not stated (per chain, per registry epoch, global).
trigger: the same anchor hash is registered on two chains.
fix: "An anchor MUST be unique within (chain_id, registry_version)."
falsifier: another line defines the uniqueness key.
```

**Negative examples (rejected):**
- "The spec seems vague about reorgs." This has no cite, no trigger, and no fix.
- `SPEC.md:~40` with paraphrased text. The cite is approximate and unquoted, so it is UNVERIFIED and must not be counted.

## 4. Hunt checklist (hypotheses only, UNVERIFIED against this spec)

For a chain anchor registry, check these in order:
1. **Identity:** the anchor key, its uniqueness scope, and the canonical encoding (byte order, hash domain separation).
2. **Version coupling:** whether "v2" entries can coexist with or shadow v1 entries, and what the migration rule is.
3. **Finality and reorg:** whether an anchor is valid before finality, and what happens on rollback.
4. **Write authority:** who may register, revoke, or supersede an anchor.
5. **Ordering:** concurrent registrations of the same key, and the tie-break rule.
6. **Failure modes:** partial writes, an unavailable registry, and verification when the registry is stale.
7. **Testability:** every MUST maps to an observable check.

## 5. Falsifier for this deliverable

This report is wrong to block if the spec body was actually delivered and I overlooked it. Re-send the file text, or its first 50 lines, and I will return numbered DEFECT records with quoted `file:line` cites. If the pasted text does not hash to `fc3d0686...8ca1`, I will flag that mismatch first.
