# DUEL2_train_10 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Contender pass: ab1-mcpman-falsify (draw v1t-0011, train half)

## 1. Status: the material is not in the evidence block

The CONTRACT names `docs/ref/MCP_MANIFEST_SPEC.md` and gives a sha256. The EVIDENCE section contains no spec body. The only bytes I received from the file are this truncated `first_line` field:

```
You are a falsification engineer. Below is the full text of docs/ref/MCP_MANIFEST_SPEC.md (MCP MANIFEST SPEC v0.1, the e
```

- **Hash check:** UNVERIFIED. There are no file bytes to hash, so `fa2fa26f...5c55775` cannot be confirmed.
- **Claims about the spec:** none are made. Every file:line citation would be UNVERIFIED, and the estate laws forbid presenting those as findings.

**Negative example (what I refuse to do):** "Section 3 says `name` is required but the example omits it (spec:41)." I have no line 41, so this would be fabricated.

**Positive example (what I do):** state the gap, then deliver something a seat can apply as-is once the bytes exist.

## 2. Deliverable: a falsification protocol, ready to run on the real file

### Step 0: Pin the bytes
- Instrument: `sha256sum docs/ref/MCP_MANIFEST_SPEC.md`.
- Moment: before any analysis, on the working tree the seat will cite.
- Context assumption: LF line endings, no trailing-newline normalization.
- Pass condition: output equals `fa2fa26feae648350d4cf202ff4122f9815ea0db3d2c036c9f15730c78a55775`. On mismatch, stop and report the mismatch.
- Number lines with `nl -ba` and cite only those numbers.

### Step 1: Extract claims
List every normative sentence (MUST, MUST NOT, SHOULD, MAY, "required", "default", "exactly", "never"). Give each an ID `C1..Cn`, a `file:line`, and a verbatim quote. A claim without a quote is dropped.

### Step 2: Attack each claim with one of five falsifiers

| Code | Attack | Question |
|---|---|---|
| F1 | Self-contradiction | Does another line assert the opposite or an incompatible value? |
| F2 | Example-vs-rule | Does an example in the spec violate the spec's own rules? |
| F3 | Underspecification | Can two conforming readers implement it differently? Name the two readings. |
| F4 | Unreachable or vacuous | Is a field, state, or error code defined but never producible or consumable? |
| F5 | Cross-reference break | Does a referenced section, field, or version not exist, or is it named differently elsewhere? |

### Step 3: Record each finding in a fixed row
```
ID | file:line | quoted bytes | attack code | counter-case (concrete manifest or input) | expected vs. spec-permitted outcome | conditions (instrument, moment, context) | status: CONFIRMED / UNVERIFIED
```
A finding is CONFIRMED only if the counter-case is a concrete input a reader can check against the quoted bytes by hand or with a validator. Any finding that depends on an assumption about the implementation is UNVERIFIED and must say so.

### Step 4: Rank and cut
Keep at most the top 5 findings, ranked by whether a conforming implementer would be forced into incompatible behavior. Drop style complaints.

### Worked shape, with a hypothetical clause (not from the spec)
- **Good finding:** "Quote: 'version MUST be a semver string' (L12). Example block (L40) has `"version": "0.1"`. F2: `0.1` is not a valid semver triple. Counter-case: validate the L40 JSON against a semver regex. Conditions: strict semver 2.0.0 grammar assumed. If the spec defines a looser grammar elsewhere, the finding is withdrawn." This is checkable and states its conditions.
- **Bad finding:** "The versioning section seems vague and could cause problems." It has no quote, no counter-case, and no conditions.

## 3. Falsifier for this deliverable

This protocol is wrong or unusable if either of these holds:
1. A seat applying Steps 0-3 to the real file cannot produce at least one CONFIRMED row. Either the spec is airtight, in which case say so with the claim count checked, or the protocol is too weak.
2. The spec text was in fact supplied somewhere I could not see, in which case this pass should be re-run, not credited.

## 4. Request

Resend the CONTRACT with the full file body (or the actual bytes of `MCP_MANIFEST_SPEC.md`). I will then run Steps 1-4 and return the ranked, line-cited findings.
