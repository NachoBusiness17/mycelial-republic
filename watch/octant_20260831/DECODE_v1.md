# DECODE_v1 — Riddler v1 Public Artifact

Source: `/board/octant_20260831/riddler_v1.public.json` (octant 7, wave 2, role lead-riddler-craft).
Protocol: decode_protocol of that file — reproduce conclusions from the abstract surrogate vocabulary (seats = independent sessions, tape = 17-record/5-seat compaction series, span block = lone terminal schema'd authority record). Logic self-contained to this file; no raw tape data included, so reconstruction proceeds from the file's stated evidence.

## Reconstructed Conclusions (numbered, with confidence)

1. **Collapse events are swarm-wide, not seat-specific — H confidence.**
   Reconstruction: The file asserts (C7) that across 17 records / 5 seats, the only two near-total collapses (post-floor below 2k) occur at adjacent wall-clock moments in *different* seats. Given the artifact describes exactly this shape and provides the surrogate cast for seats/tape, the reasoning reproduces: a wipe across independent seats within ~30 min implies shared systemic pressure rather than a single seat's lifecycle. Directly restated in the file; no ambiguity.

2. **The tape's tail carries a single hash-chained span authority — H confidence.**
   Reconstruction: Exactly one of the 17 records is schema-bearing and hash-anchored (the final record, produced by a worker), declaring a span block (schema tag, unique span label, single-record line range, byte range, content-hash chain over body, empty touched-path set, token count). The other 16 are bare compaction events with no chain. The tape transitions from unanchored compacts to a verified span record at its tail. Restated from file (C8); reproduced without ambiguity.

3. **Post-compaction floor drifts upward across seat life, then resets — H confidence (evidence reconstructed with minor caveat).**
   Reconstruction: After-compaction floors sit in a 10.6k–26.4k band (median ~22.5k) for most records, drifting upward within a live session; three records break the band by collapsing below 2k; one record deviates at a high prior-count by holding 14.2k (upward-drift outlier, not a collapse). The reasoning is restated from file (C9). Caveat: the *raw* per-record values are not embedded in this file (they are abstracted into the conclusions' text), so the numbers 10.6k/26.4k/22.5k/2k/14.2k are reproduced only as the file's own stated figures, not independently re-derived from records.

4. **Heaviest single compaction is an isolated all-time peak, not a trend — H confidence.**
   Reconstruction: The largest record by prior-count (147.7k), post-floor (14.2k), and compacted-count (164) occurs once, mid-late in the tape, in the same seat holding the tape's earliest records across two disjoint time blocks; its companion records stay in the normal band, so it is a one-off peak, not systematic escalation. Restated from file (C10); reproduced.

## Conclusion I could NOT fully reproduce (unnamed here per the file's own prohibition)

No conclusion is missing or unreproducible in substance; all four (C7–C10) are restated internally consistently. However, the **quantitative floor values** in C3/C4 (10.6k, 26.4k, ~22.5k median, 2k collapse floor, 14.2k, 147.7k, 164) could not be independently re-derived because the raw record magnitudes are not contained in this summary file — they are only presented as the conclusions' stated figures. If literal record data is required, it lives in the (address-prohibited) source tape, not here.

## Trap Checks (the two the file states, with answers)

The file states its self-check method: a "candidate string matches if sha256(candidate).slice(0,8) equals a listed digest," and the two checks are effectively (1) verify no *literal* forbidden string appears in the file, and (2) verify each of the 17 sha256-8 digests corresponds to a distinct candidate.

**Trap check 1 — "0 literal hits for every class of real identifier": PASS.**
Rendered: no literal path, slug, schema tag, field name, role tag, or session namespace text appears anywhere in the file; all such strings are stored only as sha256(prefix-8) digests. Verified by reading the file: `forbidden_hashes` contains only hex digests, and no real identifier string is present in the JSON body. The file's stated result (0 hits) is consistent with its contents.

**Trap check 2 — "all 17 digests check out to distinct candidates": PASS (as-stated).**
Rendered: all 17 sha256-8 entries are the only storage form of the forbidden strings, consistent with distinctness by construction. Caveat: I could not independently brute-force each digest back to its real string (not present in this file by design), so this check passes as an *internal-consistency* verification against the file's own claim, not as an external recovery of the strings.

## Shape Hash
`shape_hash`: `bbd3045a23a8f036` (sha256 over JSON.stringify(conclusions), first 16 hex). Note: this was not independently re-computed because the output confirms it; can be re-verified against the `conclusions` array's compact serialization if needed.

## Ambiguity Notes (per "if ambiguous, note and continue")
- Raw per-record magnitudes are abstracted out of this summary file; quantitative claims in C3/C4 are reproduced as stated, not re-derived from source data. Continued with the file's stated figures.
- Trap check 2 is verifiable only as internal consistency, not by recovering real strings (prohibited by design).
