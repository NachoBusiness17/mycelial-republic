# DUEL2_train_05 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Falsification Pass: COMMON_LANGUAGE_SPEC.md (draw v1t-0006, ask ab1-cml-falsify)

## 1. Status: BLOCKED on material (not a verdict on the spec)

<status>
The CONTRACT names the material (`docs/ref/COMMON_LANGUAGE_SPEC.md`, sha256 `56b93e2d...2ad30`) but the EVIDENCE block contains no spec text. The only bytes I have are the truncated first line of the prompt:

> "You are a falsification engineer. Below is the full text of docs/ref/COMMON_LANGUAGE_SPEC.md (COMMON LANGUAGE SPEC v1, t"

That is the wrapper sentence, not the spec. I have no line numbers, section names, rules, or definitions to attack.
</status>

Under the estate laws, a falsification of unseen text would require invented citations. Every spec claim I made would be **UNVERIFIED**, so I make none.

- **Negative example (refused):** "CML spec line 42 defines term X ambiguously." There is no line 42 in my evidence, so this would be fabricated.
- **Positive example (what I can say):** "The contract supplies a hash, but I cannot recompute it, because no bytes were delivered. Hash match: UNVERIFIED."

## 2. What I can verify

| Item | Source | State |
|---|---|---|
| Path = `docs/ref/COMMON_LANGUAGE_SPEC.md` | CONTRACT `material_path` | Quoted, but unchecked against a filesystem |
| sha256 = `56b93e2d975db0a260b4b5df24331ba08d00fff2dde4c03c3c0e5af7b682ad30` | CONTRACT `material_sha256` | UNVERIFIED (no bytes to hash) |
| Spec is titled "COMMON LANGUAGE SPEC v1" | Truncated first line | Partial quote only |
| Shape = `falsify`, half = `train` | CONTRACT | Quoted |

## 3. Deliverable: a landable falsification protocol, ready to run once bytes arrive

This is a procedure a seat can apply as-is. It is not a finding about the spec.

### Step 0: Byte integrity gate
```
sha256sum docs/ref/COMMON_LANGUAGE_SPEC.md
# must equal 56b93e2d975db0a260b4b5df24331ba08d00fff2dde4c03c3c0e5af7b682ad30
# mismatch => stop; every later finding is conditioned on a different file
```
Conditions to record: instrument (`sha256sum`), moment (before any edit), context (checked-out working tree, not a pasted copy; line endings unnormalized).

### Step 1: Extract falsifiable claims
List each normative sentence (MUST/SHOULD/defines/"always"/"never") as `L<line>: "<quoted bytes>"`. Skip anything that cannot be wrong, such as pure prose.

### Step 2: Attack each claim with one of five tests
1. **Self-contradiction:** two quoted lines that cannot both hold.
2. **Undefined term:** a term used normatively with no definition in the file (grep proves absence).
3. **Counterexample:** a concrete input that satisfies the letter of the rule but defeats its stated purpose.
4. **Unfalsifiable rule:** no observation could show a violation. This is a defect in a spec.
5. **Drift:** a spec claim about code or other docs that fails against `file:line` bytes in the repo.

### Step 3: Record each finding in this fixed form
```
FINDING <n>
claim:      L<a>: "<exact quote>"
test:       <1-5>
attack:     <counterexample or contradiction, with L<b> quote if needed>
conditions: instrument=<...>; moment=<commit/hash>; context=<assumptions>
severity:   blocks-use | misleads | cosmetic
status:     VERIFIED (quote resolves) | UNVERIFIED
```
- **Positive example:** `claim: L17: "Terms are case-insensitive"` / `attack: L63 uses "Seat" and "seat" as distinct roles` (illustrative format only, not real spec content).
- **Negative example:** "The spec feels vague about roles." This has no quote, no test, and no counterexample, so it is rejected.

### Step 4: Verdict rule
State the verdict together with its conditions, for example "N findings at hash H, checked by method M". Never say "spec is sound" without listing which of the five tests were run on which lines.

## 4. Falsifier for this deliverable

The protocol is wrong or useless if either of these holds:
- Applied to the real file, Step 1 yields zero extractable normative claims, which would mean the spec is purely descriptive and the claim-attack frame does not fit.
- Two independent seats run Steps 1-3 on the same hash and their VERIFIED findings overlap by under about half. That would mean the tests are too subjective to be reproducible.

## 5. Needed to complete the pass

Paste the full contents of `docs/ref/COMMON_LANGUAGE_SPEC.md`, ideally with line numbers. I will then run Steps 1-4 and return findings with quoted `file:line` citations.
