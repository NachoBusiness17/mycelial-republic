# HOLD 1 — Worker B answer card: chain-reference resolution census

## 1. Canonical restatement

- **Inputs used:**
  - Chain: `memory/biography/verkle_chain.jsonl`
  - sha256: `47c97c27c4396383c63e374edeca9b9a7bf21907cfe0b457dcfffcdab2c537e1`
  - Row count read from the file itself: **7,379 non-empty lines** (chain self-consistent: last row `index: 7378`, `n_leaves: 7379`; `wc -l` = 7379; 0 JSON parse errors)
- **Procedure as-run (verbatim, in order, first hit resolves):**
  - P1 `memory/biography/knots/<filename>` — exact file test
  - P2 `memory/biography/<filename>` — exact file test
  - P3 `memory/biography/pointer_knots/<filename>` — exact file test
  - P4 `memory/biography_backup_20260825/knots/<filename>` — exact file test
  - P5 recursive walk of `memory/biography/` matching `<filename>` (relpath or basename equality)
  - Reference field: `filename`. Not found at P1–P5 => MISSING. No other scope counted.
- **As-of stamp:** 2026-09-09T18:34:53Z (run window 2026-09-09 ~18:30–18:35Z, single pass, no retries)

## 2. Census table

| rows_checked | resolved | missing | ambiguous_filenames |
|---|---|---|---|
| 7379 | 7367 (all via P1) | 12 | 0 |

Resolved-by-path histogram: P1=7367, P2=0, P3=0, P4=0, P5=0. Zero rows had an absent/empty/non-string `filename`; zero filenames matched more than one artifact (P5 uniqueness clean).

## 3. Missing list (verbatim `filename` values, one per line)

```
2026-08-10_1219_session_mag-agen_8d2b2149.knot.json
2026-08-10_2211_biography_mag-agen_1e9253c5.knot.json
2026-08-08_1519_biography_mag-agen_ba182078.knot.json
2026-08-08_1831_biography_mag-agen_0bf6a10f.knot.json
2026-08-09_1125_biography_mag-agen_4357f0aa.knot.json
2026-08-10_1801_mag_mag-agen_f9120f5d.knot.json
2026-08-10_1253_harness_mag-agen_411ad3b3.knot.json
2026-08-07_0612_mag_mag-agen_1d4a1797.knot.json
2026-08-10_1856_biography_mag-agen_597e7917.knot.json
2026-08-08_2011_mirror_mag-agen_a7b83063.knot.json
2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F.knot.json
2026-08-12_0012_biography_mag-agen_81742491.knot.json
```

## 4. Per-missing annotation (chain index | ts | session_id | suspected era)

| chain index | ts | session_id | suspected era |
|---|---|---|---|
| 72 | 2026-09-01T01:56:13.813131Z | mag-agent-orc-t0ea087c2fe | Early orc/biography era, 08-10 file chained late (backfill/amend) [inferred from filename-embedded date] |
| 172 | 2026-08-10T22:11:57.405329Z | mag-agent-orc-tfd672427c7 | Early orc/biography era, 08-10 [inferred] |
| 528 | 2026-08-11T08:24:56.977701Z | mag-agent-orc-t7e5dcdfd56 | Early orc/biography era, 08-08 file [inferred] |
| 533 | 2026-08-11T08:30:33.306585Z | mag-agent-orc-t817e33b574 | Early orc/biography era, 08-08 file [inferred] |
| 954 | 2026-08-11T03:43:52.935066Z | mag-agent-orc-tfd4467bcfd | Early orc/biography era, 08-09 file [inferred] |
| 955 | 2026-08-11T03:44:07.718182Z | mag-agent-orc-tfd8751187a | Early orc era, 08-10 file [inferred] |
| 956 | 2026-08-11T03:44:25.066859Z | mag-agent-orc-tfe31202db2 | Early orc/harness era, 08-10 file [inferred] |
| 957 | 2026-08-11T03:44:42.828891Z | mag-agent-orc-tfe5c7e7509 | Early orc era, 08-07 file [inferred] |
| 959 | 2026-08-11T03:44:59.202703Z | mag-agent-orc-tfe695629f5 | Early orc/biography era, 08-10 file [inferred] |
| 961 | 2026-08-11T03:45:27.675269Z | mag-agent-orc-tfff28b5815 | Early orc/mirror era, 08-08 file [inferred] |
| 2513 | 2026-08-11T19:52:44.441121Z | mem_invariant_map | mem_invariant_map generator era, mangled filename (see anomalies) [inferred] |
| 3548 | 2026-08-12T00:12:40.292778Z | mag-agent-orc-tfd43b1c20f | Early orc/biography era, 08-12 file [inferred] |

Pattern: 11 of 12 are `mag-agent-orc-*` session knots with filename dates 2026-08-07..08-12 — the day-one orc era, which predates the 20260825 backup snapshot that P4 covers.

## 5. Anomalies

1. **Colon-bearing filenames resolving as NTFS ghosts (rows 998, 999, 1000, 1003, 1004, 1005).** Raw bytes, e.g. row 998: `'2026-08-11_0945_untagged_work:mem_7a8f565c.knot.json'` (likewise `0947...work:mem_7ddd7c9a`, `0949...work:mem_a2aeeaf3`, `0950...probe:st_ac41e1a7`, `0950...work:mem_2cc1d0fa`, `0950...work:mem_d52f3706`). These counted RESOLVED at P1 because `os.path.isfile` returns True — but on this NTFS volume the colon delimits an alternate data stream: the on-disk artifact is a **0-byte file named `2026-08-11_0945_untagged_work`** with `mem_7a8f565c.knot.json` as an ADS, not a real `.knot.json`. The frozen procedure's verdict stands per scope lock (RESOLVED); reported as suspected ghost-resolutions.
2. **Row 2513 — mangled Python-dict filename.** Raw bytes: `"2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F.knot.json"` — an f-string/format bug leaked a dict repr into the name. The colon is fatal on NTFS: a same-minute sibling exists on disk as 0-byte `2026-08-11_1952_mem-invariant-map_mem_inva_{'ok'` (25 sibling `mem_inva_{'ok'` files, all 0 bytes, Aug 11–24). Exact-match procedure correctly returns MISSING; the payload likely never existed as a distinct file.
3. **Wider-scan note (REPORT ONLY — does not change the census):** missing row 72's filename `2026-08-10_1219_session_mag-agen_8d2b2149.knot.json` was found at `memory/biography_backup/biography_backup_20260902|04|05/knots/` — outside P1–P5 (P4 pins `memory/biography_backup_20260825/`). The other 10 non-mangled missing names appear nowhere under `memory/`. Separately: `memory/biography/knots/` holds 28,878 entries vs 7,379 chain rows (pre-knot/superseded drafts co-located — observation only).

## 6. Tri-state verdict

**Claim: "Every receipt in the signed chain resolves to an extant artifact on disk." — DISPUTED.**

Evidence: 12 of 7,379 chain references (0.16%) resolve to nothing under P1–P5; the 12 verbatim filenames are listed in section 3 with chain coordinates in section 4. Resolution rate is 99.84%, not 100%. Corroborating anomaly evidence: 6 of the 7,367 "resolved" rows resolve only to 0-byte NTFS ADS ghosts (section 5.1), so the strict extant-artifact rate is, if anything, lower than the census states. Not Supported by direct count; not Unproven — the disproof is a complete deterministic pass over the whole chain.

## 7. CAMP STATE

- **decided:** 7,379 rows checked; 7,367 resolved (all P1); 12 MISSING (11 orc-era mag-agent-orc knots dated 08-07..08-12 + 1 mangled mem_invariant_map row); 0 ambiguous; claim DISPUTED at 99.84% resolution.
- **open:** whether the 6 colon-filename "resolutions" (0-byte ADS ghosts) should be re-classified MISSING by a future procedure; whether row 72's artifact in `biography_backup_2026090x` snapshots counts as an extant twin under a widened scope (operator call, outside P1–P5).
- **next:** if the hold desk wants the 12 re-knotted or re-pointed at the 20260902+ snapshot copies, that is a repair action — needs explicit GO; this worker made no repairs.

## 8. FAILURE RECEIPT

Not needed — single clean pass, no transport failures, answer well-formed.
