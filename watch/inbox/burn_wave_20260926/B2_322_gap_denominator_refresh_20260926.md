# B2-322 receipt (2026-09-26)

## Verdict

LANDED. The union-driver denominator in RESEARCH_GAP_ANALYSIS_20260918.md is refreshed from artifact bytes (184 attempts, 156 ok = 84.78 pct, 128 unique completed ids of 131 touched, 1.438 attempts per completed dig; the 143/88.8 the cell carried was stale), and the file now carries a per-row landed-or-stale census for all 8 gap rows with every number derivable on demand.

## Evidence file:line quotes

- watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md:21 before edit: "| Swarm orchestration economics | 4 | union driver (143 attempts/88.8% ok) | ...". After edit: the B2-322 byte-refresh cell quoted in the file itself.
- Derivation from watch/inbox/union_fullsend_20260917/raw.jsonl bytes (this lane, json.loads every row): 184 rows, 156 with ok true, ratio 0.8478; 131 distinct nonempty ids among 184 attempts; 128 distinct ids with at least one ok row; 184/128 = 1.438 attempts per completed dig. Every figure recomputable from the same bytes.
- The brief's own numbers (184/156/84.78/128/131/1.438) reproduce exactly from those bytes, so the brief itself was byte-derived and is confirmed.
- Per-row census (appended to the file): prompt-cache LANDED (4 verified LINKS rows, writer zcode-sw-10-b2-340, receipt B2_340_prompt_cache_matrix_20260926.md); multi-agent comms PARTIALLY FED (A2A 1 hit + A2A_FIRST_PROBE_20260925.md on disk; autogen 0, camel 0 in 345 LINKS rows); QLoRA partially fed (B2-74 redo receipt on disk, 5 fetched sources); retrieval eval STALE (no UF-122 artifact found in the watch/inbox sweep); steering, windows/storage, secret-scanning floors still owed with keyword-recount drift named (3 vs 9, 4 vs 4, 2 vs 9; patterns declared in the file so the recount is comparable only to itself).
- watch/inbox/LINKS.jsonl at census: 345 rows (the 2026-09-18 doc's own header said 245, so domain counts from the old pass were computed against a smaller ledger; drift named, not silently mixed).

## Work done

1. Re-derived the driver denominators straight from raw.jsonl (no intermediate trust), confirmed the brief's numbers, and refreshed the table cell in place with the derivation source and date.
2. Swept the other 7 gap rows against their named artifacts on disk (LINKS keyword recount + artifact existence checks: A2A probe, B2-74 receipt, UF-122) and appended the per-row landed-or-stale census with the recount method declared.
3. Marked this lane's own B2-340 landing as the closure of the prompt-cache row (self-consistent census: the same burn wave closed one gap row).

## Falsifier

The brief's falsifier: any refreshed denominator that cannot be re-derived from its artifact bytes on demand. Guard: every number in the refreshed cell and census names its artifact (raw.jsonl, LINKS.jsonl, named receipts); re-running the derivation script against those bytes must reproduce 184/156/84.78/128/131/1.438 or the refresh is falsified. The census's LANDED/PARTIALLY rows falsify if their named artifacts vanish (prompt-cache LINKS rows deleted, A2A probe moved) - the artifacts are the evidence, not the prose.

## Bibliography closed

- watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md (line 21 refreshed; per-row census appended)
- watch/inbox/union_fullsend_20260917/raw.jsonl (184 rows, derivation source)
- watch/inbox/LINKS.jsonl (345 rows at census; keyword recount patterns declared in the file)
- watch/inbox/A2A_FIRST_PROBE_20260925.md; the B2-74 redo receipt; watch/inbox/burn_wave_20260926/B2_340_prompt_cache_matrix_20260926.md; watch/inbox/burn_wave_20260926/B2_77_driver_v2_spec_20260926.md (self-feeder pointer)
