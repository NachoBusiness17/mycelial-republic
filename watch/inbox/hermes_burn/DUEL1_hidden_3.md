# DUEL1_hidden_3 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Contender pass: ab1-cml-defects (draw v1h-0010)

## 1. Blocker: the material was not delivered

The CONTRACT names `docs/ref/COMMON_LANGUAGE_SPEC.md` (sha256 `56b93e2d975db0a260b4b5df24331ba08d00fff2dde4c03c3c0e5af7b682ad30`). It gives only a truncated first line: `You are an adversarial specification reviewer. Below is the full text of docs/ref/COMMON_LANGUAGE_SPEC.md (COMMON LANGUA`. The EVIDENCE section is empty. The spec body is not in my context.

Under the estate laws, every claim about the code needs a file:line citation that resolves to quoted bytes, or it must be marked UNVERIFIED. With no bytes, I cannot cite anything in the spec. I therefore report **zero verified defects**. Inventing defects would break the "trust bytes" law and would corrupt the contender store for blind judging.

- **Verified:** only the path, the hash string, and the truncated first line, all as given in the CONTRACT.
- **Not verified:** that the file matches the hash, its length, its section structure, and every statement in it.
- **Measurement conditions:** none taken. There is no instrument, no moment, and no file context.

## 2. Landable deliverable: a defect-report format a seat can apply once the bytes exist

Each defect entry must use this shape:

```
ID:        D-<n>
Class:     one of [CONTRADICTION, UNDEFINED-TERM, AMBIGUOUS-MUST/SHOULD,
           MISSING-CASE, UNTESTABLE-CLAIM, DANGLING-REFERENCE,
           INCONSISTENT-EXAMPLE, SCOPE-GAP]
Cite:      COMMON_LANGUAGE_SPEC.md:<line>[-<line>]  "<quoted bytes>"
Second cite (for CONTRADICTION / INCONSISTENT-EXAMPLE): <line> "<quoted bytes>"
Why it breaks: <one or two sentences, step-by-step if it needs derivation>
Minimal repro: <input or reading under which two implementers diverge>
Fix:       <exact replacement text>
Falsifier: <what observation would show this is NOT a defect>
```

**Positive example (shape only, not a claim about the file):**
`Cite: SPEC.md:41 "terms MUST be unique" / SPEC.md:88 "aliases may repeat a term"`. This has two quoted lines and a repro, so it is acceptable.

**Negative example:** "The spec is vague about naming." This has no line, no quote, and no repro, so it is rejected.

## 3. Procedure for the seat

1. Run `sha256sum docs/ref/COMMON_LANGUAGE_SPEC.md` and confirm it equals the hash above. If it differs, the review applies to a different artifact and must say so.
2. Number the lines with `nl -ba`, and cite only those numbers.
3. Build a glossary of every defined term, then flag each term used but not defined, and each term defined twice.
4. Collect every MUST, SHOULD, and MAY sentence. Flag any normative sentence that cannot be checked by a test.
5. Check every cross-reference (section, file, or ID) against its target.
6. Check each worked example against the rules stated earlier in the file.
7. Rank the defects by whether two honest implementers would diverge, and keep the top ones.

## 4. Falsifier for this deliverable

This response is wrong to withhold defects if the spec text was in fact supplied somewhere I cannot see. In that case, resend the file body and I will produce the cited defect list in the format above. The format itself fails if a seat applies it to the real file and cannot reach a verdict for some defect because a required field has no source.

**Request:** please paste the full text of `docs/ref/COMMON_LANGUAGE_SPEC.md`.
