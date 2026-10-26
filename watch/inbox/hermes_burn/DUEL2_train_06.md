# DUEL2_train_06 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Red-team pass: CORE_MEMORY_PROTOCOL.md (draw v1t-0007, exploit shape)

## 1. Blocking condition: the material is not in the prompt

The CONTRACT gives only a path, a sha256, and a truncated first line ("You are a red team reviewing a protocol specification against adversarial agents. Below is the full text of docs/ref/COR"). The spec text never follows. The EVIDENCE block is empty of file bytes.

Consequences under the estate laws:

- **Trust bytes, not reports:** I have no bytes, so I cannot cite file:line for any claim about the protocol. Every protocol-specific exploit I could name would be invented.
- **Citations resolve to quoted bytes or are marked UNVERIFIED:** Everything below that touches the spec is marked UNVERIFIED.
- **Hash check:** I cannot confirm that f014e1bd...7107977 matches any text, because there is no text to hash. UNVERIFIED.

**Negative example (what I am refusing to do):** "Section 3 lets an agent overwrite another agent's memory slot (CORE_MEMORY_PROTOCOL.md:41)." That line number and claim would be fabricated.

## 2. Deliverable: a landable exploit-review spec to apply once the bytes arrive

This is a procedure, not a set of findings. A seat can run it as-is on the pasted file.

### 2.1 Preconditions (the verdict's conditions)
- **Instrument:** `sha256sum docs/ref/CORE_MEMORY_PROTOCOL.md` must equal `f014e1bda26ec92d4b4f5704d2fb9bf73826d1db8add609ff99a21693e107977`. If not, stop and report a mismatch.
- **Moment:** review the file as of the hashed revision only.
- **Context assumptions:** adversarial agents may be fully compliant at the wire level, may collude, and may replay or reorder messages. The honest-majority assumption is only valid if the spec states it explicitly.

### 2.2 Finding format (one per exploit)
```
ID:        E-<n>
Cite:      CORE_MEMORY_PROTOCOL.md:<line> "<quoted bytes>"   (no quote => UNVERIFIED)
Rule gap:  what the text permits or fails to forbid
Attacker:  capability required (writer / reader / colluding pair / replayer)
Steps:     numbered, minimal
Impact:    corruption | disclosure | denial | privilege escalation
Fix:       exact replacement text, as a diff
Falsifier: the observation that would show this finding wrong
```

**Positive example of a valid finding:** it quotes a line that says "any agent may append," then shows that no authentication clause appears in the file, and gives a diff adding one.
**Negative example:** "The protocol seems weak on trust." It has no cite, no steps, and no fix.

### 2.3 Attack classes to test against the text (hypotheses only, all UNVERIFIED)
For each class, mark the spec as: **addressed (quote)**, **silent**, or **contradicted (quote)**.

1. **Memory poisoning:** can an untrusted agent write entries that later agents treat as authoritative?
2. **Provenance forgery:** are the author, timestamp, and source fields bound to the content, or are they free-text?
3. **Instruction smuggling:** can stored memory contain text that a reader agent executes as instructions?
4. **Overwrite and tombstone races:** is there ordering, versioning, or compare-and-swap, or is it last-writer-wins?
5. **Replay and rollback:** can an old valid entry be reinserted to revert state?
6. **Scope escape:** can an agent read or write outside its namespace through path or key tricks?
7. **Collusion and sybil:** do quorum or trust rules count identities rather than principals?
8. **Resource exhaustion:** are there size, rate, or retention limits?
9. **Ambiguity exploits:** do "should" or "may" are used where "must" is needed, or do two sections conflict?
10. **Recovery path abuse:** can the repair or reset mechanism itself be triggered by an adversary?

### 2.4 Output rule
The final report lists at most the confirmed findings, ranked by impact, each with its diff. Classes marked "silent" with no demonstrated exploit are listed as gaps, not as exploits.

## 3. Falsifier for this deliverable
This procedure is wrong or unnecessary if the supplied file does not hash to the stated sha256, or if the file turns out to be a non-protocol document, in which case the attack classes in 2.3 do not apply.

## 4. What I need
Paste the full text of `docs/ref/CORE_MEMORY_PROTOCOL.md`, with line numbers if possible. I will then return the finding list in the 2.2 format, with quoted citations.
