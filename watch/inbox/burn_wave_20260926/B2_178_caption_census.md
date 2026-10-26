# B2-178 caption-structure census (B2-471, 2026-09-26)

Counts only: no caption text is quoted anywhere in this census (metadata law).

## Join
- enrich rows on file: 1234
- distinct items: 1234; duplicate item rows: 0
- raw payload parse failures: 39
- ledger join failures: 0
- joined verdict rows (the denominator for every count below): 1195
- ledger rows total: 2726 (enrich covers the scored subset; ce-NNNN = ledger row number, 1-based, the runner's own assignment)

## Lane distribution
- openrouter-k1: 351
- openrouter-k2: 331
- groq: 210
- cohere: 167
- nous-hermes: 103
- together: 37
- zai-lite: 27
- zai-pro: 8

## Class counts
- photo-scene: 627
- photo-doc: 343
- video-clip: 118
- link-preview: 101
- other: 3
- ?: 2
- doc: 1

## archive_worthy split by ledger status
- have / archive: 1017
- have / not-archive: 57
- have-recovered / archive: 16
- have-recovered / not-archive: 90
- metadata-only / not-archive: 15

Totals: archive 1033, not-archive 162

## Cross-lane disagreements (identical msg_id, 2+ lanes)
- rows scored by 2+ lanes: 0
- class disagreements: 0
- archive_worthy disagreements: 0

## Falsifier check
- every count above is derived from the 1195 joined rows; sum of class counts = 1195 (must equal 1195)
- caption text quoted in this census: 0
