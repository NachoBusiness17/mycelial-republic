# DUEL1_hidden_4 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Falsification pass: `docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md`

## 1. Blocker (read first)

<blocker>
The spec text was not delivered. The EVIDENCE section is empty, and the only bytes I received from the material are the contract metadata, including a truncated `first_line`:

> `You are a falsification engineer. Below is the full text of docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md (Chain-v2 anchor r`

That is the prompt preamble, not the spec. Without the body I cannot:
- cite any `file:line` claim about the spec (Estate Law 1),
- check that the bytes match `sha256 fc3d0686...8ca1` (UNVERIFIED),
- name a real contradiction, gap, or unfalsifiable clause.

Any specific finding I wrote now would be invented. I will not do that. The contract's `half: hidden` means the ask body is meant to be hidden from me. If so, the correct output is this refusal plus a ready-to-apply procedure, not a guess.
</blocker>

## 2. Verified vs unverified

| Item | Status | Basis |
|---|---|---|
| Path is `docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md` | Verified as a string only | contract metadata |
| Shape is `falsify` | Verified | contract |
| Contents of the spec | **UNVERIFIED** | not supplied |
| sha256 matches the file I would be reading | **UNVERIFIED** | no bytes to hash |
| Anything about anchors, chains, or registry rules | **UNVERIFIED** | inferred from the filename only |

## 3. Deliverable: a falsification protocol a seat can apply as-is

Run it against the pasted spec. Output is one table plus one verdict per row.

### Step 0 - Pin the bytes
```
sha256sum docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md
# must equal fc3d068662e2f20c4190f128e483cd3368dfc46385dd42163dfeae16a02b8ca1
# mismatch => every finding is UNVERIFIED against this draw
nl -ba docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md > spec.numbered
```
Cite only lines from `spec.numbered`.

### Step 1 - Extract claims
A claim is any sentence containing MUST, SHALL, SHOULD, "always", "never", "unique", "immutable", "monotonic", "atomic", or a number (size, count, timeout, version). Record each as:

```
C<n> | line <L> | "<verbatim quote>" | type: invariant|format|ordering|liveness|security|numeric
```

### Step 2 - Attack each claim
For each claim, write a falsifier: a concrete input, sequence, or state that would make it false if the spec is wrong. Then classify:

- **FALSIFIED**: the spec's own text, or a quoted second line, yields a counterexample. Cite both lines.
- **UNFALSIFIABLE**: no observable outcome could contradict it. Report this as a defect.
- **SURVIVES**: the attack was tried and failed. State the attack tried.
- **UNDERSPECIFIED**: the outcome depends on a value or rule the spec omits. Name the missing item.

### Step 3 - Measurement conditions (Estate Law 2)
Any verdict that relies on a measurement must carry:
```
instrument: <tool/command/version>
moment:     <commit sha or file hash, time of run>
context:    <env assumptions: clock source, network, single/multi writer, hash algo>
```
A verdict without this block is invalid.

### Step 4 - Cross-clause checks
Run each of these over the extracted claims:
1. **Pairwise contradiction**: two claims whose conjunction is unsatisfiable.
2. **Definition drift**: one term (e.g. "anchor", "epoch", "height") used with two meanings.
3. **Ordering gaps**: a rule that needs an order (A before B) with no tiebreak for concurrent or equal cases.
4. **Failure paths**: each MUST has a defined behavior when it is violated.
5. **Version boundary**: v1 to v2 transition behavior is defined for records that exist in both.

### Step 5 - Report format
```
| ID | line | quote | verdict | counterexample / missing item | conditions |
```
End with the single highest-severity finding and a one-paragraph patch to the spec text.

## 4. Attack classes for an anchor registry (hypotheses, UNVERIFIED)

These are generic and say nothing about what this spec contains. Use them as prompts for Step 2.

**Good use (positive example)**
> C7 | line 42 | "Anchor IDs MUST be unique." Falsifier: two writers register the same ID within one block. Check whether line N defines a tiebreak. If none: UNDERSPECIFIED, missing a concurrent-write rule.

**Bad use (negative example)**
> "The spec probably lacks replay protection."
This has no line, no quote, and no falsifier. It is a rumor, so reject it.

Classes worth trying:
- **Uniqueness**: scope not stated (global, per-chain, per-epoch).
- **Immutability**: no rule for revocation or correction, so "immutable" conflicts with any "update" clause.
- **Ordering**: monotonic by what? Equal values and reorgs are unhandled.
- **Hash binding**: which bytes are hashed, with what canonical encoding, and is the algorithm pinned?
- **Genesis**: first-anchor rule is missing or special-cased.
- **Liveness**: a timeout stated with no clock source.
- **Migration**: v1 anchors referenced from v2 with no mapping.

## 5. Falsifier for this deliverable

This protocol is wrong or useless if either holds:
1. A seat applies Steps 0-5 to the real spec and every finding is already obvious without the extraction step. Then the procedure adds no discriminating power.
2. The sha256 in Step 0 does not match the file the seat reads. Then the protocol is applied to the wrong artifact.

## 6. Request

Paste the full body of `CHAIN_V2_ANCHOR_REGISTRY_SPEC.md`, ideally with line numbers. I will then return the Step 5 table with `file:line` citations and one landable patch.
