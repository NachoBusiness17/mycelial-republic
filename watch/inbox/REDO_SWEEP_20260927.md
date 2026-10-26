# REDO SWEEP — everything that failed, redone — 2026-09-27

**Operator order:** redo everything that failed and kick it into gear, self-steal framing (each fix lands as a generalized method, not just a patch).

## 1. Stale saved-workflow copies (the silent regression, worst find of the sweep)

The five saved game-dig workflows were saved BEFORE the report-cap crash fix, so any rerun by name would reintroduce the exact crash that killed two veins. All five re-saved from the patched drafts; verified by grep for the shrink symbol. **Generalized method:** saved workflows must byte-sync with amended drafts; a grep for the newest fix symbol is the pre-rerun check.

## 2. Librarian backlog redo (tools/librarian_backfill_20260927_redo.jsonl)

- Zero-padding hypothesis CONFIRMED: 2007.1558 = ARXIV:2007.01558 (Bernhardt 2020, h-BN flakes) and 2008.0277 = ARXIV:2008.00277 (Nielebock 2020, API misuse mining), both now NAMED+RESOLVED. Unpadded forms returned null in the same batch, isolating padding as the sole cause.
- 2026.15906 and 2026.84791 proven NON-EXISTENT (S2 null AND arXiv Atom totalResults=0; YYMM month-26 is structurally invalid). 3841.71428 confirmed mint error (month-41).
- key:Kraska-2018 retires FREE: the identical work was already resolved in the first backfill as arXiv 1712.01208 (The Case for Learned Index Structures). Backlog now: 3 classical keys (Belady 1966, Mattson 1970, LRU-K/Neil) stay owed on S2's keyless search endpoint hard-429ing (batch endpoint passes, search does not: transport fold).

## 3. LLM7 lane goes HOT (pass e receipt)

Unauthenticated /v1/models HTTP 200 with 64 models, free tier confirmed with anonymous limits plus token unlock. Scaleway dead for unauthenticated use (401). Freelane landscape after the full sweep: hot = OpenRouter funded (1000 rpd), Groq cached-token RPDs, Featherless recon-only (22,032 models), LLM7 free (64 models); dead = Chutes (retired Mar 15 2026), SiliconFlow (401), Scaleway (401); owed = Lightning AI tier data.

## 4. LINKS-329 correction filed (the 0.36x drift)

Source fetched live: the true figure is 0.36 PERCENT of the comparator's fee, so the fleet's 0.36x overstated by 100x (the receipt prose saying three orders of magnitude was itself wrong; the burn ledger row 34 already carried the correct 100x). Append-only correction rows landed in both LINKS ledgers, plus two burn-ledger CORRECTION rows (judge-lane-spec-correction, b2-wave-fold-correction) through the wired gate, discharging both stale assertions. Original LINKS-329 byte-verified untouched.

## 5. Symbol dictionary v2 (Coxon mint + siblings field)

Second entry minted in the cold-read shape (canon-anchored pointer, external referent honestly owed), and the schema gains the siblings field, making the mined-at-arrival law's or-siblings clause executable by grep for the first time. Both pass-c steals executed.

## Still owed (unchanged, all ledgered)

Generic validated-path close mode (hook law), Lightning AI tier data, probe20 --live (night box window), State XI fires 2-20, width probes, patrol scheduling (operator-gated).
