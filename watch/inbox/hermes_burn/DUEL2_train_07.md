# DUEL2_train_07 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# CONTENDER PASS: ab1-cml-safeguard (draw v1t-0008, train half)

## 1. Status: BLOCKED on material (not a refusal)

<finding>
The body of `docs/ref/COMMON_LANGUAGE_SPEC.md` is not in my input. I received only the contract metadata, including a `first_line` that is truncated mid-word ("...full text of docs/ref/COMMON_L"). The spec text, and therefore any line numbers, never arrived.
</finding>

Under the estate laws, this means:

| Law | Consequence here |
|---|---|
| Trust bytes, not reports | I have no bytes of the spec. Every `file:line` claim about it would be invented. |
| Citations resolve to quoted bytes or are UNVERIFIED | I cannot quote anything. All spec-specific claims are UNVERIFIED. |
| Verdict needs its conditions | My only instrument is the contract text. The moment is this single pass. The context assumption is that the spec was meant to be attached and was not. |
| One landable deliverable | A patch cannot be landed without an anchor line. I cannot name one honestly. |

**Negative example (what I am not doing):** I will not write "Section 3, line 42 lacks a precedence rule" and propose a patch. That would pass blind judging only by fabrication, and it would bank a false citation.

**Positive example (what I am doing):** I state exactly what is missing, give a patch skeleton that is ready to fill the moment bytes arrive, and name its falsifier.

## 2. Verified facts (contract bytes only)

- `material_path`: `docs/ref/COMMON_LANGUAGE_SPEC.md`
- `material_sha256`: `56b93e2d975db0a260b4b5df24331ba08d00fff2dde4c03c3c0e5af7b682ad30`
- `shape`: safeguard (find the missing guardrail)
- I cannot check the sha256 because I have no bytes to hash. **UNVERIFIED.**

## 3. Deliverable: a fill-in safeguard patch, applicable once the bytes are supplied

### 3a. Procedure (deterministic, to be run on the real text)

1. Number the lines and record the sha256 of the file you review. It must match the contract hash above.
2. List every normative sentence (MUST, SHALL, SHOULD, "is defined as"). Quote each with its `file:line`.
3. For each, ask: what input or situation makes this rule produce a wrong or harmful result, and which sentence in the file stops it? If none does, that is a candidate missing guardrail.
4. Pick the single candidate with the largest blast radius and no existing stopper. Discard the rest.
5. Write the patch below.

### 3b. Patch template

```
FILE: docs/ref/COMMON_LANGUAGE_SPEC.md
ANCHOR: after line <N>: "<quoted bytes of line N>"
INSERT:
  ### Guardrail: <name>
  <Subject> MUST NOT <failure behavior>.
  When <trigger condition>, the reader MUST <required fallback>.
  Conflicts between this section and <other section, file:line> are
  resolved in favor of <X>.
  Check: <one observable test that shows the guardrail is honored>
```

### 3c. Candidate guardrail classes (UNVERIFIED hypotheses, not findings)

These are common gaps in shared-vocabulary specs. I did not see them in this file, and I cannot say whether they are present or absent:

- **Term collision or redefinition:** no rule on what happens when a local doc redefines a common term.
- **Precedence on conflict:** no rule on whether the spec, a local doc, or code wins.
- **Versioning and deprecation:** no rule on how a term is retired without silently changing the meaning of older text.
- **Normative vs informative marking:** examples that readers may treat as binding.

**Positive example of a good finding:** "Line 88 says terms 'are shared by all seats' but no line says what a seat does when its local usage differs. Insert a precedence rule after line 88."
**Negative example:** "The spec could be clearer about terminology." This has no line, no failure mode, and no patch.

## 4. Falsifier for this deliverable

- **Falsifier of the block claim:** if the spec text was in fact attached and I failed to see it, this response is wrong. A re-run with the text visible would produce a cited patch.
- **Falsifier of any patch produced from this template:** the patch is wrong if either of these holds:
  - **(a)** The quoted anchor bytes do not appear at the stated line in the file whose sha256 matches the contract.
  - **(b)** An existing sentence in the file already prevents the named failure. That makes the guardrail redundant.

## 5. What I need to complete the pass

Resend the full contents of `docs/ref/COMMON_LANGUAGE_SPEC.md`, ideally with line numbers. I will then return one cited, landable patch following section 3b.
