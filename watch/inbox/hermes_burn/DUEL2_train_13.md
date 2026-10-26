# DUEL2_train_13 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

<verdict>
No defects can be reported against `docs/ref/CORE_MEMORY_PROTOCOL.md` from this input. The document body was not delivered. Any defect I listed would be fabricated, which breaks the estate law "Citations resolve to quoted bytes or are marked UNVERIFIED."
</verdict>

<conditions>
- Instrument: a read of the prompt text in this single turn. No file access, no tools, no hash computation.
- Moment: this turn only.
- Context: I saw the CONTRACT block, and the EVIDENCE block, which contains no document text. The only fragment of the material is the truncated first line: `You are an adversarial specification reviewer. Below is the full text of docs/ref/CORE_MEMORY_PROTOCOL.md (CORE MEMORY P`. That line is the review prompt's preamble, not protocol content.
- Not verifiable: sha256 `f014e1bd...7107977`, because there are no bytes to hash. Status: UNVERIFIED.
</conditions>

<what_i_will_not_do>
- Negative example (rejected): "CORE_MEMORY_PROTOCOL.md:42 says retention is unbounded, which contradicts the eviction rule at :88." I have no line 42 or line 88, so this would be invented evidence.
- Negative example (rejected): a generic list of typical memory-protocol flaws presented as findings. Without bytes, these are hypotheses about a file I have not seen, not defects in it.
</what_i_will_not_do>

<deliverable>
This is a landable defect-entry spec. A seat can paste it with the document and re-run the pass. Each defect must have these fields:

```
DEFECT <n>
  cite:      CORE_MEMORY_PROTOCOL.md:<line>[-<line>]
  quote:     "<exact bytes from those lines>"
  class:     contradiction | undefined-term | missing-condition | unverifiable-claim | race/ordering gap | unbounded-resource | ambiguous-normative (should/may/must) | dangling-reference
  why:       <one or two sentences naming the failure, step by step>
  trigger:   <concrete input or sequence that exposes it>
  fix:       <minimal replacement text, quoted>
  confidence: high | medium | UNVERIFIED
```

Entry rules:
1. The `quote` must be a byte-exact substring of the cited lines. If it is not, the entry is void.
2. Cross-section defects (contradictions) need two cites and two quotes.
3. Any measured claim (latency, size limit, count) must name instrument, moment, and context assumptions, or be marked UNVERIFIED.
4. Only hyphens are allowed, no em-dashes.
5. Entries are ordered by severity, with contradictions and race gaps first.

Positive example of a valid entry shape (the cite and quote are placeholders, not claims about the file):
```
DEFECT 1
  cite:      CORE_MEMORY_PROTOCOL.md:<L>
  quote:     "<bytes>"
  class:     undefined-term
  why:       The term is used in a MUST clause but defined nowhere, so two implementers can diverge.
  trigger:   Two seats implement the clause with different readings.
  fix:       "<definition text>"
  confidence: high
```
</deliverable>

<needed_to_proceed>
Re-send the contract with the full file text inline (or the bytes after the first line). I will first confirm the text matches sha256 `f014e1bd...7107977` (stated as verified only if I can compute it, otherwise UNVERIFIED), then produce the defect list in the format above.
</needed_to_proceed>

<falsifier>
This response is wrong if the document text was actually present in the input and I failed to see it. In that case, quote its first defect-bearing line and the correct review follows. It is also wrong if a re-run with the bytes yields defects that do not fit the entry schema, since the schema would then need new classes.
</falsifier>
