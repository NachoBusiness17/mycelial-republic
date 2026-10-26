# SYNTHESIS: the standing fleet ractored (2026-10-02-workflow-dogfood)

Synthesis seat, moment 2026-10-04 (this run's own launch record is dwfrun-ed1dbbae, slug 2026-10-02-workflow-dogfood). Inputs: the surviving findings of all lenses, hostile passes, and steering rounds of this run, PLUS fresh byte verification executed this sitting (instruments listed at the bottom; every claim below is either verified by those commands or marked as relayed from the ask's surviving findings).

## The verdict first

The ask presumed 12 saved workflows. The byte-truth answer: there is no 12. The saved layer holds 19 name-plates (`ls .zcode/workflows/*.dwf.ts` = 19, this sitting), the fire journal holds 101 launch records (`ls .zcode/workflow-runs/dwfrun-*.mjs | wc -l` = 101, plus 2 dwfeval), and the two layers do not agree. Six of the twelve named workflows (the-gala, drop-dig, wide-dig, salon-mine, librarian-expedition, fill-ball) are ONE byte-identical 19,213-byte engine behind six badges: their code sections from `const ESTATE` to EOF all hash c5020d3220 while their whole-file MD5s all differ (8bf79d38ca / 3de12e6903 / 8cf2b646c4 / 81b1b08c83 / 3fd31e2e67 / e9ef5d993e), because only the description block differs. Whole-file hashing would have hidden this forever. Any manifest of this fleet must hash the code section, never the file.

**Minimum viable fleet = 5 engines + 1 composite:**

1. **the-gala**, the battery chassis: the saved body ran 30 of 101 journal fires (`GALA_ROOT` in 30/101 payloads, verified this sitting), 21 on the current cluster plus 8 on its v1 predecessor per the corrected lens census (relayed: md5-of-payload.lowered clustering, an instrument this seat did not re-run).
2. **olm-mine**, the only daily cadence (~9 body fires across 09-29..10-03, 5 receipt dirs under `watch/inbox/frontier_olm_*`).
3. **ractor-engine**, the audit lens-set (6 receipt dirs in 3 days under `watch/inbox/ractor_engine/`, including this run).
4. **mickey17-v2** (2 launches on its own saved bytes, both under other missions' names, per the corrected census; its whole-file hash 692d2b1616 is also the Gap-analysis-100m draft, the "borrowed fire").
5. **the gap-analysis + fill-ball composite** (the register IS the lane table; gap-analysis has 3 fires on its amended saved code, code-section f0c9a6d29d, distinct from mickey's 6184aa75f1).

Wide-dig merges into drop-dig's citation-resolution shape (drop-dig fired once as its own body). Everything else is museum or profile: **9 of 19 saved bodies have zero launches of their current bytes** (tree-doctrine-dig, the-50, music-cut, game-mechanics-deep-dig, and the 5 patched game-dig veins), scoped to the 101 surviving dwfrun records read 2026-10-03/04. My own grep confirms 0 of 101 payloads carry any `music_cut_gate` signature, and the tree-doctrine string appears in only 3 records, at least one of which is this raction itself (dwfrun-ed1dbbae) and one the sibling fleet-meta run: they mention the names, they do not run the bodies.

## The thesis: three ledgers, one truth

No single lens could see this because each lens trusted a different ledger. The fleet keeps three, and they disagree:

- **Name plates:** `.zcode/workflows/*.dwf.ts`, 19 saves, gitignored at `.gitignore:198` (`.zcode/`; `git ls-files .zcode` = 1 tracked file, `git check-ignore -v` on a dwfrun record matches, rc=0), so the ratchet, citation lint, and freshness gates NEVER scan fleet bytes.
- **The gate registry:** `memory/workflows/REGISTRY.jsonl`, 75 rows (63 mid-raction; the fleet is being dogfooded live). It is a submission ledger, not a fire ledger: digest d2a6783b55be rides 7 rows (positions including 13, 19, 22-25, 75), and a 12-row PASS sweep at 2026-10-04T02:33:47-02:34 minted fresh gate evidence for exactly the ask's 12 named workflows (samples read: olm-mine at 02:33:47Z, gap-analysis at 02:33:48Z) in a window where the journal shows zero launches. **The gate certifies saves the journal proves never fire.** That is the theater finding, and it is structural, not an incident: the registry measures gate-worthiness of bytes, the journal measures execution, and no instrument joins them.
- **The disk journal:** `.zcode/workflow-runs/`, 101 dwfrun + 2 dwfeval records, oldest 2026-09-19 11:53, header-marked "safe to delete once the run has settled", self-ignored by its own `.gitignore` (`*`), read by no estate instrument. ListWorkflowRuns tool failures were three times recorded by prior passes as ledger-absence; the ledger was on disk the whole time.

The triangulated claim none of the lenses stated alone: the fleet's real membership is defined by the journal, its official membership by the gate, and its imagined membership by the name plates, and all three disagree. Until a manifest joins them, "the standing fleet" is a suggestion the gate notarizes.

## CONVERGENT findings (independently re-derived across lenses, highest rank)

1. **One engine, six badges** (lens 1 whole-file grouping + the code-section pass + the corrected journal clustering: 30/101 payloads carry GALA_ROOT). Verified this sitting: the six code sections hash identical at 19,213 bytes.
2. **Bank-path hardcode vs documented contracts** (CONVERGENT, lens 1 and lens 4): six bodies hardcode `watch/inbox/gala_20260925` while their arg docs promise six different roots. Verified: `drop-dig.dwf.ts:94` `const GALA_ROOT = ESTATE + "/watch/inbox/gala_20260925";` also :345 (lane artifacts) and :360 (receipt); `fill-ball.dwf.ts:88` same constant. One 09-25 party folder is the de-facto mega-bank of the whole 10-01 wave; any consumer following a documented contract greps the wrong tree.
3. **The gates do not reach the fleet** (CONVERGENT, lens 3 + git check this sitting): the struck 191.8M phantom survives as provenance in three saved descriptions, verified at `fill-ball.dwf.ts:7`, `gap-analysis.dwf.ts:8`, `olm-mine.dwf.ts:8`, because `.zcode/` is gitignored and citation lint never sees the bytes.
4. **The audit organ out-runs the fill organ** (CONVERGENT with the 10-01 dogfood-gaps synthesis and lens 5): ractor-engine spent 6 ractions in 3 days auditing everything including itself, while its own never-fired-organ finding stays unfired: `mag/percolator.py:23` and `:87` document the `--candidates` ingest built by fillball-1001 (GAP_REGISTER rank 6), `ingest_candidates` at `mag/percolator.py:544`, yet `memory/percolator/candidates.jsonl` holds 16 rows, 0 promoted, mtime 2026-10-02T04:17:43Z (verified this sitting), and the 14 newer rows (9 + 5) in `watch/inbox/frontier_olm_2026-10-02/` and `-2026-10-03/percolator_candidates.jsonl` were never ingested. The loop filed the ingest and then lapsed it.
5. **Sibling convergence is live:** the target directory held 14 lens files at synthesis write time (accuracy, break-* x6, dogfood, economics, moonshot-1/2, operations, security; no SYNTHESIS.md existed before this one) and REGISTRY grew 63 to 75 rows during the raction. This chapter is being co-derived by siblings in the same window; dedupe read before any rib promotion.

## Corrections this synthesis banked

- "No run ledger exists" (two prior lens passes) is WITHDRAWN: `.zcode/workflow-runs/` exists; the introspection-tool failure was misread as ledger-absence for the third time.
- tree-doctrine-dig "fired once" is WITHDRAWN: its single body launch (dwfrun-15738edf, 09-25 14:59) predates its 09-26 01:30 save; never-fired-as-saved.
- salon-mine is upgraded to repeat-fired (5 launches, 3 post-save, per the corrected census).
- the-50's reset-day relaunch question is answered NEGATIVE (draft mtime 09-19 14:16; the only journal record that day is dwfrun-2656afad at 11:53, pre-draft); only the token count stays open.

## Honest residue (OWED and scoped absences)

- **OWED:** the 191.8M-era token count behind THE-50's program. The relaunch question is closed; the count is not verifiable from any instrument run this sitting.
- **Scoped absences:** every "never fired" claim is scoped to the 101 surviving dwfrun records + the 75-row REGISTRY + the watch/inbox banks, read 2026-10-03/04. A launch surface that writes no dwfrun record provably exists: the 09-29 mickey17 24-wide wave (`watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md`, 598 lines, 24 miners) left zero journal records and zero gate rows. Journal absence alone can never ground a universal.
- The journal is garbage-collectable by its own header and doubly gitignored; the census behind this chapter DECAYS until the first move below lands.
- Relayed, not re-run: the lens cluster ids (8479acceeb etc.) are md5-of-payload.lowered first-10-hex from the corrected pass, which re-measured all ten vein pairwise ratios 0.9618-0.9869. Its other claims were verified directly by this seat; that specific instrument was not.

## Fleet card (what the next CreateWorkflow should pick)

KEEP: the-gala (battery chassis), olm-mine (daily mine), ractor-engine (audit lenses), mickey17-v2 (arena/one-shot dogfood), gap-analysis+fill-ball (register+fill loop). MERGE: wide-dig into drop-dig. RETIRE (amend-not-delete, the RETIRED.md Q7 precedent): the-50 (its program lives in the-gala), tree-doctrine-dig (doctrine template), music-cut (its job is already banked by gala lanes: `watch/inbox/buildall/music-cuts/style-profile.json` 17:59 and `filter-disco.md` 18:05 on 10-03 vs music-cut.dwf.ts saved 17:55, with 0/101 payloads carrying its gate signature, making its first real fire a second implementation), and the 5 game-dig veins (85% byte-twins, all 34 fires inside one 36-hour burst ending 09-27 01:36, game-mechanics-deep-dig.dwf.ts parameterizes the identical shape). STAMP: the five diverged gala-body saves as gala-chassis variants in their descriptions.

## Instruments this sitting

- `ls .zcode/workflows/*.dwf.ts` = 19 files; the 12 named workflows all present.
- `ls .zcode/workflow-runs/dwfrun-*.mjs | wc -l` = 101; `dwfeval*` = 2.
- `wc -l memory/workflows/REGISTRY.jsonl` = 75; 12 rows match "2026-10-04T02:3", samples PASS; 7 rows carry digest d2a6783b55be.
- `.venv/Scripts/python.exe C:\Users\foste\AppData\Local\Temp\dwf_fleet_verify.py`: whole-file + code-section md5 table (six-way c5020d3220 identity at 19,213 bytes), phantom greps (3/3 True at fill-ball:7, gap-analysis:8, olm-mine:8), drop-dig :94/:345/:360 and fill-ball :88 gala hardcodes (all True), MUSIC_CUT_GATE_HITS 0/101, GALA_ROOT_PAYLOADS 30/101, TREEDOC_PAYLOADS 3 (mentions, not bodies), candidates.jsonl 16 rows / 0 promoted / mtime 2026-10-02T04:17:43Z, olm candidate files 9+5 rows, percolator.py :23/:87/:544 confirmed.
- `git ls-files .zcode | wc -l` = 1; `git check-ignore -v .zcode/workflow-runs/dwfrun-2656afad-*.mjs` matches `.gitignore:198` (.zcode/), rc=0.

---

Rewrite receipt: this file was first written by the synthesis seat at 2026-10-04 00:44 EDT (10,682 bytes); the run script reported it missing, `ls -la` this sitting proved it present, and it was rewritten byte-for-byte from the submitted chapter to clear the doubt.
