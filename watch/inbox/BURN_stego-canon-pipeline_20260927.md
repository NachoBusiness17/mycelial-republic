## Verdict

steal

## Evidence

- `canon/podcast_corpus/doa_ai_debate/canonical_notes.md` opens: "# DOAC AI EMERGENCY DEBATE - canonical notes (operator-supplied summary, 2026-09-19)". The newest canon arrival (2026-09-19) carries an interpretation layer authored fresh by the operator. No symbol dictionary lookup preceded it; no receipt records a corpus grep before the read.
- `mag/ghost_leak_detector.py` is the only stego surface in `mag/`: `ENTROPY_THRESHOLD = 6.2` with comment "# Shannon entropy above this → suspect stego", and `scan_entropy` docstring: "Scan Verkle chain entries for high-entropy text fields suggesting steganography." It is detection-side only; it never consults an interpretation corpus.
- `memory/corpus/founding_law/crs_r45129_modes_of_interpretation.txt` already sits in canon with named interpretive modes: "textualism, original meaning, judicial precedent, pragmatism, moral reasoning, national identity, structuralism, and historical practices." This is a ready-made dictionary spine for interpretation lookup, unmined by any pipeline.
- `memory/corpus/LINKS.jsonl` rows carry the ledger shape: `{"id": "ADV-ARC", "kind": "steal", ...}` and `{"id": "WORLDLINE-LENS", "kind": "operator-naming", ...}`. A symbol-arrival receipt has a natural home here.
- `memory/corpus/esoteric_canon/` holds symbol-dense full texts (Carroll, Chesterton, Kafka, Duncan's ritual, Steiner) with zero derived symbol entries anywhere in the tree.
- Web search (2026-09-27) was thin: it surfaced "SWAN: Semantic Watermarking with Abstract Meaning" quoting "Early linguistic steganography embeds bits by rewiring surface structure" and a May 2026 "edit-based linguistic steganography" item, but returned no reachable full-text URLs. Filed as owed, not read, not synthesized.

## Steal or Vacuous

The fleet adopts the pipeline law verbatim: when a symbol arrives, check the existing interpretation corpus BEFORE cold-interpreting it, and leave a lookup receipt in `memory/corpus/LINKS.jsonl` (kind: "lookup", pointers to prior entries hit or "no-hit" when the cold read is sanctioned). Seed the symbol dictionary from organs that already exist: `founding_law/crs_r45129_modes_of_interpretation.txt` supplies the mode vocabulary; `LINKS.jsonl` operator-naming rows (VACUOUS, worldline lenses) are the first symbols; esoteric_canon supplies the symbol-dense canon to mine on arrival, not upfront. `ghost_leak_detector.py` stays detection-side and is explicitly out of scope: entropy scanning is a leak vector, not an interpretation corpus. No new daemon; the law runs at canon-arrival time, same trigger that files a manifest entry.

## Falsifier

Pre-registered build: `memory/corpus/symbol_dictionary.jsonl` plus a lookup step at canon arrival. Falsified if, within 14 days of landing, any new canon arrival produces an interpretation note (like canonical_notes.md) with no matching lookup receipt in LINKS.jsonl, or if a lookup receipt cites a prior interpretation that the dictionary does not contain (fabricated hit). Either failure retires the law to the ratchet baseline with the receipt attached.

## Bibliography

- `canon/podcast_corpus/doa_ai_debate/canonical_notes.md` (read in full)
- `canon/podcast_corpus/doa_ai_debate/transcript.txt` (read lines 1-40)
- `mag/ghost_leak_detector.py` (read in full)
- `memory/corpus/MANIFEST.md` (read in full)
- `memory/corpus/founding_law/crs_r45129_modes_of_interpretation.txt` (read lines 1-20)
- `memory/corpus/LINKS.jsonl` (read first 3 rows)
- `memory/corpus/ai_canon/manifest.jsonl` (read first 3 rows)
- WebSearch 2026-09-27: "symbol interpretation corpus lookup pipeline steganography dictionary NLP 2026"; result summaries only (SWAN arXiv item, ResearchGate edit-based steganography May 2026); no reachable full sources, filed as owed.
