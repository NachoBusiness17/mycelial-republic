# G2-1 — STEP-0 PARTITION RECOUNT (counted artifact)

Date: 2026-09-11 · Lane: mickey G2-1, spawned from M1's NEXT ·
Absorbs: watch/inbox/RETROKNOTTER_PREP_20260911.md (fold gate + class definitions; §2 Step-0 is this slot). Read-only: no chain writes, no file moves. Method: full walk of `memory/biography/knots/` (29,165 files), full read of `memory/biography/verkle_chain.jsonl` (7,512 rows), per-file JSON parse + unreferenced test (filename/stem absent from chain text AND filename 8-hex tag absent from all chain hex-token prefixes).

## THE POINT

M1's "21,479 orphan knots staged" is **real and reproduced to the digit** — but it is **not the fold count**. It equals every unreferenced file in knots/ (21,530) minus the 36 zero-byte corrupt (→ 21,494) minus the 15 kpi-only count-witnessed leaves (→ **21,479 exact**). The true foldable knot-leaf partition is **13,693** — which lands **exactly** on the forensics card's never-referenced census. The 7,782-file gap between the two numbers is `by-session_*` INDEX artifacts + strays that fail the staging spec's own fold gate (no date prefix, not knot leaves). A knotter built to fold "21,479" would have knotted an index. That was the trap; this recount disarms it.

## MANIFEST — measured 2026-09-11, chain at 7,512 rows (tip moved +135 since the prep card's 7,377)

| Partition | Count | Composition |
|---|---|---|
| Files in `memory/biography/knots/` | **29,165** | 29,163 at root + 2 in `.mimosa\hook-*` |
| Referenced by current chain | 7,635 | chain has 7,512 rows; some rows reference >1 file |
| **Unreferenced ("staged") total** | **21,530** | the raw orphan pile |
| — parsable knot leaves, dated, foldable | **13,693** | **matches forensics' 13,693 EXACTLY** |
|   · Class 1 (2026-08-16..31) | 2,343 | 2,327 valid (2,326 session_scalar + 1 usage_digest) + 16 zero-byte |
|   · Class 2 (2026-07-10..08-15) | 11,350 | 11,276 valid (11,274 session_scalar + 2 diary_node) + 17 zero-byte + 57 untyped strays |
| — `by-session_*` INDEX artifacts (NOT knots) | 7,892 | 7,889 parsable + 3 zero-byte; variants: 6,272 {chain_index,chain_root,filename} · 1,368 {filename,leaf_hash,schema,session_id} · 249 {filename,leaf_hash} |
| — `sess_*` transcript strays | 2 | untyped |
| — zero-byte total | 36 | 16 in C1 window + 17 dated C2 + 3 by-session |
| Date range of dated orphans | 2026-07-10 → 2026-08-31 | Sep-2026: **0 orphans** — all 1,200 Sept files are referenced (chain is live) |
| By month (dated orphans) | Jul-26: 24 · Aug-26: 13,612 | undated: the 7,892 index artifacts |
| C1 day peaks | 08-24: 674 · 08-17: 329 · 08-25: 324 · 08-23: 234 | full day census held in run notes; zeros on 08-23(4), 08-24(10), 08-25(2) |

## MATCH / MISMATCH vs the claims

- **21,479 (M1): MATCH, exact.** 21,530 unreferenced − 36 zero-byte − 15 kpi-only = 21,479. Equivalent form: parsable unreferenced 21,494 − 15. The arithmetic reproduces from today's disk; M1's exact method is UNPROVEN (both decompositions give the same number), but the count itself is SUPPORTED.
- **13,693 (forensics class-2 census): MATCH, exact.** Independent confirmation of the recount method.
- **16 corrupt in the C1 window (silence dossier): MATCH, exact.** 08-23/24/25 zero-bytes = 4+10+2.
- **2,960 silence files (dossier): DISPUTED → 2,343 today.** The dossier counted ALL Aug-16..31 date-prefixed files at its census time; since then the chain grew 7,377 → 7,512 rows and the 09-08 rebuild's re-knots now reference the difference. This is the census drift the prep card predicted ("different censuses, overlap imperfectly") — the recount number is the fold-eligible one.
- **Counting lesson for the knotter:** 3 knot files carry ALL-DIGIT hex tags (e.g. `94081514`). A tag extractor that discards digit-only 8-hex runs (as a naive date filter does) misbinds them. Tags must be validated against content, not against charset heuristics.

## FORMAT CHECK — are they valid knot JSON?

- **Parse: 100% of non-empty files are valid JSON. Zero parse failures across 29,129 .json files.** 36 zero-byte artifacts are the only corrupt class (gap-dispositions per spec, never folded as content).
- Schema is rich and consistent: session_scalar leaves carry `leaf_hash, dossier_commit, session_id, schema, type, theme_vector_*, tension_index, duration_minutes, ...` (sample: `2026-07-10_1731_mirror_019f4d15_e21de36c.knot.json`).
- **Filename tag binding — TWO regimes coexist (knotter must try both):**
  | Binding | Count |
  |---|---|
  | tag == `dossier_commit[:8]` | 8,258 |
  | tag == `leaf_hash[:8]` | 4,393 |
  | no hex tag in filename | 1,041 — need content-derived addressing at fold time |
  | anomalous (usage_digest, empty dossier_commit) | 1 (+3 all-digit tags resolve to dossier_commit) |
- The 1,368+249 by-session variants each carry the full `leaf_hash` of the knot they index — a ready-made witness index, but NOT foldable content (fails the spec's date-prefix gate).

## VERDICT

**READY — for the retro-knotter BUILD. NOT cleared to APPEND.**

1. Build can proceed against the recounted partition: **13,693 dated orphans = C1 2,343 (2,327 fold + 16 gaps) + C2 11,350 (11,276 fold + 17 gaps + 57 dispositioned strays)**. Kpi-only 15, absent 304, missing 18 stay outside the file-fold per spec §2.
2. Disposition separately (do NOT knot): 7,892 by-session index artifacts + 2 sess_* strays — regenerate/archive, never chain as leaves.
3. Knotter requirements this recount adds: dual-field tag binding (dossier_commit first, leaf_hash fallback), content-hash path for the 1,041 untagged, digit-safe tag extraction, per-file `recovery` stamp per spec §3.
4. This manifest is a SNAPSHOT — the tip moved +135 rows while this slot ran. Re-run the recount at fold time; the falsifier's count reconciliation binds to the fold-moment numbers, not these.
5. Appends stay gated by spec §1 (append lock + second witness / LINKAGE-PASS rename) and operator GO. Nothing here touches the chain.

Staged by mickey G2-1 worker (zcode), 2026-09-11. One file, read-only except this manifest.
