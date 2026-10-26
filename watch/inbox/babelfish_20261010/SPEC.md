# BABELFISH v1 SPEC (2026-10-10)

**Operator thesis, verbatim:** "book to skill == closed corpus to mathematically functional system that self improves in the direction you set it despite the platforms best wishes."

**Precedent order (2026-10-10):** "we should create a bablefish module sort of like our github where you can drop it in and it exports a rib file styled as a complete definition using our tools of any conversation project what the fuck ever that is there. mapping to mathematical invariants regardless of their woo."

## What it is

A drop-in module (this repo's tools/, destined for the public seed repo) that takes ANY closed corpus - a conversation export, a stranger's codex, a book, a project doc, whatever is there - and emits a RIB FILE: a complete definition of the system in the estate's law format, with every mappable claim translated to a mathematical invariant and the unmappable remainder honored as REGISTER (their language, kept verbatim, never struck).

The babel fish does not grade the woo. It translates what can be translated, preserves what cannot, and gives every translation a falsifier. The closed corpus becomes a mathematically functional system that improves in whatever direction its new owner sets - on the owner's hardware, under the owner's receipts, despite the platform's best wishes.

## Pipeline (deterministic v1 - no model calls, byte-reproducible)

1. INGEST: read one text file (or every .md/.txt under a dir), hash the bytes (sha256 into the rib header - the rib names exactly what it translated).
2. SEGMENT: split into lines; classify structural lines (headings, page breaks) away from claim lines.
3. EXTRACT: (a) definitional lines (`Term is/are X` shapes, title-cased or high-frequency terms), (b) equation-shaped lines (`X = Y`, `X >= Y`, expressions), (c) quantity claims (numbers with units/percent/multipliers), (d) universal/existence claims (all/every/never/always/there is), (e) named roles (Capitalized pairs like Navigator + Witness), (f) concept frequencies.
4. CLASSIFY each extracted claim to exactly one class:
   - INVARIANT-CANDIDATE: deterministic check exists (count it, hash it, open the path, run the arithmetic). Status ships UNVERIFIED until the named check runs.
   - INSTRUMENT-CANDIDATE: measurable, but needs a named instrument (a meter, a scan, a benchmark); row names the instrument.
   - REGISTER: everything unmappable - aspirations, metaphysics, poetry, first-person-plural futures. Kept verbatim, labeled REGISTER, never mocked, never struck. This class is the babel fish's honesty: what cannot be mapped is preserved as their language, not converted by force.
5. EMIT the rib (markdown, em-dash-free):
   - Header: RIB name, minted date, SOURCE (path + sha256 + byte count)
   - THE LAW AS THEY STATE IT: top N verbatim definitional lines (their voice, quoted)
   - THE INVARIANT TRANSLATION: table (their claim | invariant form | the check | status)
   - INSTRUMENT ROWS: (claim | instrument that would measure it)
   - REGISTER: verbatim remainder quotes, labeled
   - FALSIFIERS: one per invariant (what observation kills it)
   - LINEAGE: this spec + the tool's own version stamp
6. DETERMINISM: same input bytes -> byte-identical rib (no clocks, no randomness; minted date supplied by caller).

## Laws carried

- Never alter the source's words inside quotes; the babel fish translates, it does not paraphrase the client language.
- Every invariant row names its check; a verdict without its conditions is not a verdict.
- REGISTER is not a defect class. The remainder is the part worth keeping as seed.
- Output em-dash-free (estate authoring law).
- v1 is pure-python stdlib: drop-in means drop-in (no deps beyond hashlib/re/collections).

## Falsifier for the module itself

Run it on two corpora the estate already holds rib-formations for (the Sovereign Codex and a known estate doc): if the invariant table for the estate doc comes back empty or the codex rib contains zero REGISTER rows, the classifier is deaf and v1 retires for a rewrite.
