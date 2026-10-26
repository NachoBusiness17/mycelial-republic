# DUEL2_train_14 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Red-team pass: COMMON_LANGUAGE_SPEC.md - BLOCKED on missing material

## 1. Status

<status>
The CONTRACT names `docs/ref/COMMON_LANGUAGE_SPEC.md` (sha256 `56b93e2d...ad30`). The EVIDENCE block contains only the truncated first line of the prompt: "You are a red team reviewing a protocol specification against adversarial agents. Below is the full text of docs/ref/COM". The spec body is not in my input.
</status>

Consequences under the estate laws:

- **file:line citations:** I can cite none. Every claim about the spec's content is **UNVERIFIED**.
- **Measurements:** I relied on none. Instrument, moment, and context are therefore not applicable. I did not hash or read the file, and I cannot confirm the hash matches any text.
- **Exploits:** I will not invent clauses and then "break" them. That would be a fabricated verdict.

## 2. Deliverable: a landable review protocol, plus hypotheses to test against the text

A seat can apply this as-is once the spec text is pasted. The hypotheses are about the spec's *subject* (a shared language between agents), not about its actual contents.

### 2a. Finding format (each finding must match this)

```
ID:        CML-nn
Clause:    <file>:<line>  "<quoted bytes>"
Attack:    <adversary capability> -> <step-by-step exploit>
Impact:    <what breaks: integrity / authority / availability / meaning>
Fix:       <exact replacement text, patch-ready>
Falsifier: <observation that would show this finding is wrong>
```

**Positive example (acceptable form, hypothetical content):**
`Clause: COMMON_LANGUAGE_SPEC.md:88 "Agents MAY extend the vocabulary locally."` The attack is that agent A defines `approved` to mean "seen". The impact is that A's messages pass B's checks with a changed meaning. The fix is "Local extensions MUST be namespaced and MUST NOT shadow core terms." The falsifier is a core-term shadowing rule elsewhere in the spec.

**Negative example (rejected):** "The spec seems vulnerable to spoofing." This has no quote, no line, no attack steps, and no fix.

### 2b. Hypothesis checklist (all UNVERIFIED, each to be confirmed or killed by quoted bytes)

| # | Attack class | Question to ask of the text |
|---|---|---|
| H1 | Term shadowing / redefinition | Can a participant redefine a core term, and is scope bounded? |
| H2 | Ambiguous grammar | Does any production admit two parses with different effects? Are MUST/SHOULD/MAY used consistently? |
| H3 | Version/capability downgrade | Is negotiation authenticated, and is there a floor version? |
| H4 | Identity and authority claims | Can a message assert its own sender or authority, with nothing external to check it? |
| H5 | Replay and ordering | Are there nonces, sequence numbers, or expiry on state-changing messages? |
| H6 | Free-text injection | Can a free-text field be read as an instruction by a downstream agent? |
| H7 | Unbounded size or recursion | Are there limits on length, nesting, and fan-out? |
| H8 | Undefined failure behavior | What happens on an unknown term: ignore, reject, or guess? "Guess" is the exploitable answer. |
| H9 | Semantic drift between agents | Is there a conformance test or canonical glossary, or does meaning live only in each agent's interpretation? |

### 2c. Procedure

1. Paste the spec with line numbers.
2. For each H-row, search for governing clauses and quote them.
3. A row with no governing clause becomes a finding ("silence is the gap"). A row with a closing clause is marked **CLOSED** with its citation.
4. Emit at most one patch per finding, in the format of 2a.

## 3. Falsifier for this deliverable

This protocol is wrong or useless if, on the real text, fewer than half of H1-H9 map to any clause or to any identifiable absence. That would mean the spec is not a protocol-level language spec, and the checklist should be rebuilt from its actual structure.

## 4. What I need to finish

Please supply the full text of `docs/ref/COMMON_LANGUAGE_SPEC.md`, ideally with line numbers. I will then return concrete, cited findings with patches.
