# B2-78 receipt: gap-analysis denominator refresh (2026-09-26)

## Verdict

LANDED. All 8 gap rows of watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md were
re-derived from ledger bytes this lane (instruments named in Work done; every
number below is from a fresh recount, probes saved next to this receipt). The
proven drift is confirmed and sharpened: the seed's union-driver denominator
(143 attempts / 88.8% ok) is superseded twice over, first by the
XIDIG-SWARM-DENOMINATOR-DRIFT ALERT row ratio (184 attempts / 156 ok = 84.78%),
then by the B2-77 receipt's id-deduped instrument (128 unique completed ids of
131 touched = 97.71% completion ratio, 1,652.2 recorded tokens per completed
dig), which this lane independently reproduced byte-for-byte and cites as the
newer instrument wherever the two disagree. Two further drifts are newly filed:
the COVERAGE header's own denominator is short (bytes force 274 rows on or
before 2026-09-18, not the claimed 245), and three of the five completed
gap-dig answers in DAY_PACK are unverified model text with placeholder or
uncheckable citations, so "dig completed" does not mean "floor landed".

## Evidence

- Union drive recount (watch/inbox/union_fullsend_20260917/raw.jsonl, 184
  lines, 0 malformed): 156 ok rows, 28 fail rows, row ratio 156/184 = 0.8478.
  Attempt matrix: (1, ok)=140, (1, fail)=25, (2, ok)=16, (2, fail)=3. The 184
  rows touch 131 unique ids, exactly the queue.jsonl id count, no duplicate ids
  in the queue, no queue id without rows. 128 ids have at least one ok row
  (completion ratio 0.9771); never-ok ids are exactly UF-129, UF-130, UF-131.
  15 ids carry more than one ok row, top UF-121 with 6. state.json done holds
  exactly the 128 ok ids (no done-without-ok, no ok-without-done). All four
  B2-77 pins reproduced: attempts per completed dig 184/128 = 1.438, recorded
  tokens 211,484 (35,371 prompt + 176,113 completion), all-in per completed dig
  1,652.2, first-completion floor 177,434 = 1,386.2, refire waste 34,050
  (16.1% of recorded spend). Sharpening this lane adds: all 156 ok rows carry
  usage, and the 28 duplicate completions reuse the ORIGINAL attempt ordinal
  (same id, same attempt), so (id, attempt) is not a unique row key; the
  refire did not increment attempt because state.done never advanced in the
  recorded 11:28:14Z crash window (driver FIX comment,
  scripts/union_fullsend_day.py lines 74-81). All 28 failure rows carry usage
  None, so provider spend on failed attempts is still invisible (B2-77
  falsifier g stands).
- COVERAGE header: LINKS.jsonl is 337 lines (284 kind-less link rows + 53
  event-kind rows still cohabiting per the B2-28 split debt, B2-168 enforcement
  open); pack index memory/lenses/corpus_index.json count field is byte-unchanged
  at 107. Rows with ts on or before 2026-09-18: 274, and the backdate check
  found ZERO rows appended after the first post-09-18 row that carry an
  on/before-09-18 stamp, so the ledger bytes force 274 as the end-of-seed-day
  count against the seed's claimed 245 (29 rows; the analysis artifact's graph
  was generated 2026-09-18T05:50Z, same-day appends landed after it).
- Instrument divergence, disclosed: the seed's per-domain keyword lists were
  not persisted with the artifact, so the domain pass was re-run with the
  lists named in this receipt's probe
  (watch/inbox/burn_wave_20260926/B2_78_denominator_recount.py) on both the
  seed-era subset and current bytes. Seed-era counts under this instrument do
  NOT reproduce the seed's numbers (for example retrieval: seed 36 vs 11 here,
  finetune: seed 34 vs 11, steering/persuasion: seed 9 vs 31, prompt-cache:
  seed 18 vs 4, security/keys: seed 9 vs 5, swarm/orchestration: seed 4 vs 6),
  so seed-vs-current per-domain deltas are indicative only and are not claimed
  as instrument-continuous. The one canonical-based count that needs no
  keyword list: x.com/twitter.com rows are 151 of 284 link rows = 53.2%
  (seed: 138 of 245 = 56%).
- Named cluster checks on current bytes: A2A rows 0, AutoGen rows 0, CAMEL
  rows 0 in LINKS.jsonl (the comms gap row's "zero on A2A/AutoGen/CAMEL
  schemas" still holds for the ledger); XIDIG-SWARM ids 6 (5 laws + the
  DENOMINATOR-DRIFT ALERT, LINKS lines 321-326, ts 2026-09-26T11:53:49Z);
  XIDIG-WIN ids 5 (LINKS lines 327-331, verified-live Microsoft Learn quotes;
  the "63 reparse points per path" figure is a platform-law quote, not an
  estate measurement); qlora-mentioning rows 2.
- UF-124..UF-131 from queue bytes + raw bytes + state bytes: UF-124 steering
  ok (2 ok of 3 attempts), UF-125 comms ok (3/3), UF-126 swarm economics ok
  (3/3), UF-127 prompt-cache ok (3/3), UF-128 windows reparse ok (3/3),
  UF-129 secret-scanning DEAD (0 ok of 4), UF-130 qlora DEAD (0 of 4), UF-131
  gardenfors DEAD (0 of 3). DAY_PACK.md carries failure records, not answers,
  for UF-129/130/131 (lines 2223-2250) and answers at lines 2056, 2089, 2144,
  2176, 2190. The seed's DISPATCHED line ("UF-124..UF-131, one dig per gap")
  maps 7 of 8 rows; the 8th dig UF-131 is the gardenfors conceptual-spaces
  fetch, while the seed's own 8th gap row (retrieval eval) names UF-122, which
  is completed (state done, DAY_PACK line 405).
- Dig-answer trust grades read off the bytes: UF-124's answer cites
  "ICLR 2023 (https://openreview.net/forum?id=XYZ)", a placeholder id, so its
  prior-art baseline is unverified; UF-125's answer gives "A2A v1.3 / registry
  gRPC v0.9 / 1.2MB" figures that no byte on disk corroborates and that sit in
  a different version shape from the verified A2A probe receipt (a2a-sdk 1.1.5,
  a2a-cli 0.2 from PyPI, watch/inbox/A2A_FIRST_PROBE_20260925.md, verdict
  PASS); UF-126's LiteLLM pricing figures are uncorroborated; UF-127's provider
  matrix self-flags unverified ("verify against current pricing pages; my
  figures predate 2026"). Only the probe and receipt bytes are floor.
- Operation-status bytes per row: memlance: no 5-lance falsifier artifact
  exists anywhere in the repo (find over "*lance*" names only the skill dir
  and tests fixtures), so row 1's falsifier is still pending. Kernel amendment
  ceremony: zero grep hits in docs/, mag/, configs/, watch/inbox .md, so row
  4's ceremony is still undefined. Secret scan (B2-73, UF-129 redo): local
  gitleaks-pattern + entropy scan ran over corpus/ + watch/inbox/, persisted
  results array is empty (zero findings), and this lane's mirror census
  (watch/inbox/burn_wave_20260926/B2_78_scanscope_census.py) re-derives the
  scope the run printed only to stdout: 64,212 files seen, 38,234 text-scanned,
  25,872 binary-skipped, 106 large-skipped; no receipt .md and no LEDGER row
  exist for B2-73. QLoRA (B2-74, UF-130 redo): receipt
  B2_74_qlora_recipe_20260926.md landed, 5 sources quoted from fetched bytes.
  Gardenfors (B2-75, UF-131 redo): receipt B2_75_gardenfors_fetch_20260926.md
  landed with chapter jsons on disk. Junction policy (B2-76): LANDED per
  memory/burns/LEDGER.jsonl 2026-09-26T16:28:52Z and receipt
  B2_76_junction_policy_20260926.md (mag/catalog_scan.py v2->v3 spec, live walk
  485,998 rows, 1 real junction tag 0xA0000003, catalog/junctions.jsonl, 9/9
  tests), and that row formally leaves the seed's "-189,106" pruned-rows
  attribution Unproven by design; the earlier probe bytes
  (B2_76_junction_probe_results.json) hold 77,274 dirs scanned, 1 reparse
  point found.

## Work done

1. Ran the recount instrument
   (watch/inbox/burn_wave_20260926/B2_78_denominator_recount.py, .venv python,
   read-only) over raw.jsonl, queue.jsonl, state.json, LINKS.jsonl and
   corpus_index.json; output saved as B2_78_denominator_recount.json.
2. Re-derived all 8 gap rows. Refreshed table (seed denominator -> byte
   denominator, operation status):

   | Gap | Seed rows/number | Byte denominator 2026-09-26 | Operation status |
   |---|---|---|---|
   | Steering/priming prior art | 9 rows, falsifier pending | keyword pass 32 current rows (instrument divergence named); UF-124 dig ok but answer graded unverified (placeholder citation) | STILL STARVING: memlance 5-lance falsifier not on disk, no verified literature baseline |
   | Multi-agent comms protocols | 30 rows, zero A2A/AutoGen/CAMEL | A2A/AutoGen/CAMEL LINKS rows still 0/0/0; VERIFIED floor landed outside the ledger: A2A_FIRST_PROBE_20260925.md (a2a-sdk 1.1.5 live card decode, PASS); UF-125 dig ok, answer unverified | PARTIALLY FED: hands-on interop receipt exists; ledger floor still zero; dig text untrusted |
   | Swarm orchestration economics | 4 rows; driver 143 attempts / 88.8% ok | 6 XIDIG-SWARM rows; drive: 184 attempts / 156 ok = 84.78% row ratio, superseded by B2-77's 128 of 131 unique ids completed = 97.71% and 1,652.2 tokens per completed dig (reproduced this lane to the digit) | FED: ALERT filed, B2-77 v2 spec landed (S1-S6); v2 build briefs still open |
   | Prompt-cache invalidation | 18 rows, no provider matrix | keyword pass 4 current rows; UF-127 dig ok with a self-flagged unverified provider matrix | STILL STARVING: matrix exists only as self-doubting model text; kernel amendment ceremony still undefined |
   | Windows reparse/storage law | 4 rows; junction pruned 189K rows | 5 XIDIG-WIN verified-live rows; B2-76 LANDED (policy + live walk 485,998 rows, 1 junction, probe 77,274 dirs / 1 reparse point); seed's -189,106 attribution formally Unproven | FED: research floor + scanner policy landed; mirror-vs-duplicate diff now runnable |
   | Secret-scanning/rotation | 9 rows; 60 filed artifacts never key-scanned | UF-129 DEAD in drive (0/4); B2-73 redo: 0 findings over 64,212 files seen / 38,234 text-scanned (census re-derived this lane) | FED with a hole: scan + zero-findings on disk; no receipt, no census row, no rotation policy doc |
   | QLoRA small reasoning corpora | 34 generic rows | UF-130 DEAD in drive (0/4); B2-74 redo receipt landed, 5 fetched sources quoted; 2 qlora LINKS rows | FED by redo; Rocinante Oct 27 deadline stands |
   | Retrieval eval design | UF-122 pending, undrained | UF-122 COMPLETED (state done, DAY_PACK line 405, 50-question spec verified by B2-57); seed's 8th dig slot was actually UF-131 gardenfors, DEAD in drive, redone by B2-75 | SUPERSEDED: "pending, undrained" is stale; eval spec exists; nothing shows it gates mining yet |

3. Filed the two new drift findings on top of the ALERT: the COVERAGE header
   row-count drift (274 vs 245 on the seed's own date, zero backdated appends)
   and the dig-answer trust grades (completed does not mean verified; UF-124's
   openreview id "XYZ" is the sharpest single example). The B2-77 receipt is
   cited as the newer instrument for every swarm-row number and supersedes the
   ALERT's row-ratio framing wherever both exist.
4. Self-fed 3 briefs under Open, unchecked, per the self-feed law (dig-answer
   citation audit; verified prompt-cache matrix; B2-73 receipt + rotation
   policy).
5. QUEUE.md B2-78 row annotated with this landing per the flip-carries-a-pointer
   law; the row was found pre-checked [x] with no receipt on disk before this
   lane (the B2-238 disease); this landing earns the check. LEDGER.jsonl row
   appended via .venv python json.dumps. Receipt registered in INDEX.json.

## Falsifier

This refresh dies if: (a) any recount of raw.jsonl by id yields a completed-id
count other than 128, or an attempt-row count other than 184 (matches the
B2-77 falsifier a; both instruments agree); (b) the LINKS backdate check is
re-run and finds backdated appends that move the 274 figure, or the seed's 245
is produced from end-of-day 09-18 bytes under a named row class; (c) a
byte-check of UF-124's openreview id "XYZ" resolves to a real paper with the
claimed effect sizes (it would un-grade the trust verdict); (d) the A2A probe
receipt's PyPI versions (a2a-sdk 1.1.5, a2a-cli 0.2) are contradicted by an
installed-state check of the estate .venv; (e) the B2-73 results file is found
non-empty or its census differs from 64,212 / 38,234 / 25,872 / 106 under the
mirror probe on unchanged scope bytes; (f) corpus_index.json count moves from
107 without a pack receipt; (g) any future prose cites the drive with 143, or
88.8 percent, or 84.8 percent alone, without naming which numerator and
denominator it uses (B2-77 falsifier f, restated as the standing law).

## Bibliography closed

- watch/inbox/RESEARCH_GAP_ANALYSIS_20260918.md (the 8 rows and COVERAGE
  header refreshed; line 21 denominator superseded)
- watch/inbox/LINKS.jsonl lines 321-326 (XIDIG-SWARM rows incl.
  XIDIG-SWARM-DENOMINATOR-DRIFT ALERT, byte-verified this lane) and lines
  327-331 (XIDIG-WIN rows)
- watch/inbox/union_fullsend_20260917/raw.jsonl, queue.jsonl, state.json,
  DAY_PACK.md lines 405, 2056, 2089, 2144, 2176, 2190, 2223-2250
- watch/inbox/burn_wave_20260926/B2_77_driver_v2_spec_20260926.md (the newer
  instrument: 128 unique completed ids, 1,652 tokens per completed dig)
- watch/inbox/burn_wave_20260926/B2_78_denominator_recount.py +
  B2_78_denominator_recount.json (recount instrument and output)
- watch/inbox/burn_wave_20260926/B2_78_scanscope_census.py (B2-73 scope census
  probe, run output in the receipt Evidence block)
- watch/inbox/A2A_FIRST_PROBE_20260925.md (verified A2A interop floor)
- watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md,
  B2_75_gardenfors_fetch_20260926.md, B2_76_junction_policy_20260926.md,
  B2_76_junction_probe_results.json, B2_73_secret_scan.py,
  B2_73_secret_scan_results.json
- memory/lenses/corpus_index.json (pack count 107, byte-checked)
- memory/burns/LEDGER.jsonl (B2-76 row read; this lane's row appended)
- watch/inbox/burn_wave_20260926/QUEUE.md (contract header, B2-78 row,
  self-feeds)
