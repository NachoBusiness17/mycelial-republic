# B12 — Rashomon witness URL dedupe audit (2026-09-16)

- **lane:** B12 · wave 20260916
- **class:** AUDIT (read-only pass over audited files; no surface/ledger file touched)
- **writer:** zcode-wave-b12-dedupe-20260916
- **ask:** extract every URL from the Rashomon surface + witness-per-program records, canonicalize with `mag.link_library.canonicalize`, report totals, duplicate clusters, localhost/private hits. Register/write goes through the tool in a later lane — this lane only measures.
- **status:** DONE 2026-09-16 — audit complete, results below; no audited file modified (LINKS.jsonl, surface files, records all untouched)

## Corpus (fixed paths, exactly as scanned by the script)

Rashomon program records:

1. `watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md` (the only `RASHOMON_SURFACE_*.md` on disk)
2. `queue/handoff/ractors/BAUDRILLARD_rashomon_20260904.md`
3. `queue/handoff/ractors/FOUCAULT_rashomon_20260904.md`
4. `queue/handoff/ractors/MCLUHAN_rashomon_20260904.md`
5. `queue/handoff/ractors/PLATO_KIRK_rashomon_20260904.md`
6. `memory/research/ghost-rashomon-proposal-20260809.md`
7. `memory/narrative_corpus/rashomon/tavern_bar_fight_party.v1.md`

Witness-per-program records (where the raw witness URLs actually live):

8. `watch/inbox/SESSION_RECOVERY_FORGE_DAEMON_20260914.md`
9. `watch/inbox/PARABLE_ARC_SYNTHESIS_20260916.md`
10. `watch/inbox/wave_20260916/receipts/B13_CODETAUR_KAN.md`
11. `queue/lanes/research/inbox.jsonl`
12. `watch/inbox/LINKS.jsonl` — rows only (`writer` in {`zcode-rashomon-20260914`, `dedupe-test`}); `url` + `canonical` fields

## Results

- **script:** `artifacts/rashomon_dedupe_20260916.py` · run `.venv/Scripts/python.exe artifacts/rashomon_dedupe_20260916.py` (stdlib + `mag.link_library`, read-only)
- **corpus files scanned:** 11 (3 carry literal http URLs)
- **ledger rows in scope:** 11 (`writer` ∈ {`zcode-rashomon-20260914`, `dedupe-test`})
- **total URL occurrences:** 26
- **distinct raw URL strings:** 14
- **unique canonicals:** 11
- **canonicalize errors:** 0
- **localhost/private/reserved hosts:** 0 — every witness URL is public x.com/zenodo.org; `validate_host_safety` clean

Findings:

1. `RASHOMON_SURFACE_ELEPHANT_20260914.md` itself carries **zero literal URLs** — witness sources appear only as prose refs ("slashreboot.com, Zenodo 17811909"). The raw witness URLs live in the witness-per-program records and the ledger.
2. The ractor Rashomon files (BAUDRILLARD/FOUCAULT/MCLUHAN/PLATO_KIRK 20260904), ghost proposal, tavern narrative, and `queue/lanes/research/inbox.jsonl` carry zero http URLs (the lane pointers use bare status IDs, e.g. `2099236759825707232` — not URLs, regex-blind by design).
3. **3 duplicate clusters** would collapse 14 raw spellings to 11 canonicals — all three are the X `?s=20` tracking-param flavor, exactly the case `canonicalize` was built for.
4. **3 witness URLs are restated across separate files** (same spelling, would each have become a duplicate INTAKE under the pre-ledger regime): NachoQuixotic-2098…490 (PARABLE_ARC_SYNTHESIS + LINKS), codetaur-…7232 (B13 receipt + LINKS), che_shr_cat-…3447 (SESSION_RECOVERY + LINKS).
5. Historical proof in-corpus: cluster 3 (`yifanzhang_`) is the live dedupe-test from 2026-09-14 — the `?s=20` resubmission came back flagged `duplicate_of` the plain row (LINKS seq 1789370680986159).
6. Known limitation (note for canonicalizer v2, out of corpus): `memory/trajectory/steps.jsonl` shows an `api.fxtwitter.com/NachoQuixotic/status/2098136899814662490` wrapper — a different host, so `canonicalize` would NOT collapse it to the x.com canonical. Fxtwitter/vxtwitter wrappers are a future HOST_COLLAPSE candidate.
7. Concurrent-lane check: LINKS.jsonl grew 142→145 lines during this audit — rows from `backfill-zenodo-20260916` (the B6 lane filing Matthew's remaining Zenodo DOIs), not this script. B12 is read-only; ledger append-only behavior confirmed live.

## Cluster table

| # | canonical (sha256 prefix) | raw spellings | sources |
|---|---|---|---|
| 1 | `x.com/mathemetica/status/2099069099943072161` (01230062…) | `…2161` · `…2161?s=20` | LINKS seq 1789371940152993 `canonical` / `url` (witness 9, Asimov) |
| 2 | `x.com/measure_plan/status/2099245923536671011` (C5FDC3F5…) | `…1011` · `…1011?s=20` | LINKS seq 1789371940152994 `canonical` / `url` (witness 10, grokking) |
| 3 | `x.com/yifanzhang_/status/2098886268033945610` (CB3EAB54…) | `…5610` · `…5610?s=20` | LINKS seq 1789370679416062 (witness 6c) + seq 1789370680986159 `dedupe-test` (caught as duplicate 2026-09-14) |

Singletons (1 spelling each): DengHokin-…4010 (w6), mathemetica-…0631 (w3), hijkzzz-…5859 (w6b), che_shr_cat-…3447 (w5), codetaur-…7232 (w4), NachoQuixotic-…2490 (w2), zenodo 17811909 (w1 capstone), NachoQuixotic-…5297 (operator hidden-director thread, cited beside w2 in PARABLE).

## Recommendation

**3 clusters would have been 3 duplicate INTAKEs — plus 3 more witness URLs restated verbatim across 2+ records — and the ledger kills both flavors: 14 raw spellings filed as 11 canonicals, zero register writes needed from this lane (registration already done by zcode-rashomon-20260914; the register/write goes through `python -m mag.link_library add` in the later lane only for any future witness URL).**
