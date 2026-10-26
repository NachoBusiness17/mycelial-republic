# CROSS-RACTORS: the OLM mine judged by the ractor's own standards

Lane: cross-ractor, division B, THE GALA ouroboros. Moment of writing: 2026-10-02 (UTC afternoon).
Method source: ractor-engine's lens library, `.zcode/workflows/ractor-engine.dwf.ts:91-114`
(accuracy falsifier-hunter, operations orchestration surgeon, economics EV-per-cost pricer,
dogfood organ mapper, lineage miner, security threat-modeler; the ask named these six of the
library's eight). Subject: the OLM mine's days 1-2 outputs, `watch/inbox/frontier_olm_2026-09-30/`
and `watch/inbox/frontier_olm_2026-10-01/`, judged by the standards the mine's own ecosystem
enforced on others (citation lint, byte-checks, no-fabrication law, descent-protocol banking).

Scope note: the ask said "the 2 digests, the 10 steal cards, the registers". On disk the two
folders hold 6 + 5 = 11 steal cards and 23 + 23 = 46 register rows; this lane audited all 11
cards and both registers. The 09-28 window (`frontier_olm_20260928/`, 21 register rows, 13 files
under steal/) enters only as lineage and comparison, not as audit subject.

Instrument: `cross_ractor_bytecheck.py` (beside this lane's JSON), raw output in
`watch/inbox/gala_20260925/ouroboros/lanes/cross-ractor.check.txt` (all greps, counts, and the
byte-check appended there as run). No code under `mag/` or `tools/` was touched by this lane
(the one script this lane wrote lives under the lanes dir), so the violation ratchet is not
applicable and was not run.

## 1. ACCURACY lens: the registers byte-checked

Ran `cross_ractor_bytecheck.py` over both registers: every quote searched across the day
folder's independent pre-fold holdings (sweep write-ups, sweep/_fx raw fetch caches, steal
cards, lens, raw xml), tiers exact / whitespace-normalized / punctuation-normalized, with
fold outputs (DIGEST, register, candidates, RECEIPT) classified separately so a quote cannot
"verify" by matching its own row.

**Day-1 register (2026-09-30 backfill): 23 of 23 BYTE-VERIFIED.** 22 quotes hit exact-byte in
in-folder holdings (sweep files and steal cards); row 13 (arXiv 2609.37902) verifies exact at
its named out-of-folder source `state/arxiv/2026-09-30/2609.37902v1.txt` (lowercase
"higher-priced..." form, exact-substring True, run this session).

**Day-2 register (2026-10-01 fold): 7 of 23 BYTE-VERIFIED, 16 of 23 FOLD-ONLY, 0 MISS.**
Sixteen confirmed-find quotes exist in no pre-fold holding; their only carriers are the fold's
own outputs. The mechanism is stated in the fold's own header: input was "the run's 32 sweep
payloads, 23 adjudicated confirmations ... as carried in the ask" (DIGEST.md line 3) - the
quotes rode the ask, the payload bytes were never banked, and the run journal is a compiled
payload that binds nothing (ERRATA 001 finding). Honest boundary: this is a capture-and-carry
gap, not proof of fabrication - several FOLD-ONLY rows' key numbers do have independent
paraphrase carriers (row 22's 90.0/89.3/88.7 pass@1 table at
`sweep/quantization-compression-x.md:22`; row 13's 96.6% / 607,378-to-20,766 at
`sweep/kv-cache-context-engineering-reddit.md:25`), so the numbers survive at rest even where
the claimed verbatim quotes do not.

Cross-dogfood verdict: the estate built citation lint (born from the 191.8M phantom) to block
exactly this class at pre-push for git-changed prose, and the mine's day-2 fold shipped 16
unverifiable-at-rest verbatim quotes into a citable record with no gate noticing, because the
gate watches git changes and no fold-time equivalent exists. The day-1 backfill shows the fix
works when applied: it quoted only on-disk bytes and went 23/23.

## 2. OPERATIONS lens: the deaths, the amendments, the ledger

- **The two documented deaths never appear in the gate ledger.** STORY.md:212-214 records the
  09-29 mine dying twice (journal order nondeterminism, then a world-read glob), yet all six
  frontier-olm-mine rows for that day (REGISTRY.jsonl lines 31-35, 38) are PASS with G1-G7
  green. Day-1's third death (the fold step that never ran, GAP_REGISTER rank 7) rode PASS row
  line 40 (2026-09-30T01:18:10Z). The registry records script shape at registration moments;
  it has no row class for "the run's downstream fold completed". The ledger does record FAILs
  elsewhere (11 FAIL rows in 58, all other workflows), so the blindness is specific to
  downstream-step completion, not to failure recording.
- **Day-2's run left five PASS rows in 186 seconds** (the-gala.dwf.ts, 01:13:49Z to 01:16:55Z,
  four distinct digests then one repeat). Amendment churn is green-only; nothing in the ledger
  says which amendment produced the folder on disk. The dogfood-eating twin of this finding:
  this lane's own instrument took three iterations before its evidence was sound (a
  self-matching register scan and a JSON-escaping miss were caught and fixed before any
  verdict was banked); green rows would have recorded all three identically.
- **Amendments audited and found honest:** the day-1 backfill banner discloses authorship,
  moment, selection rule, and its own non-runs (DIGEST.md:3,12,77); day-2's cold-reader fix
  pass is byte-accounted (RECEIPT.md:11,29); the KVarN exclusion and the unsourced-clause
  quarantine are model no-fabrication behavior (DIGEST.md:111-115).
- **Rank 10's "zero mentions anywhere" was false when written.** The trio's U3 evidence sits at
  `frontier_olm_20260928/sweep/_raw/full_2609.21341.txt` (52,444 bytes, mtime Sep 28 22:59) and
  U2's thread id is held in the 09-28 folder (DIGEST.md, kv-reddit sweep). The day-1
  backfill's grep was folder-scoped, so it found nothing. An audit of one window cannot see
  adjacent windows; "anywhere" claims need estate-scoped instruments (corpus FTS).
- **INDEX heal (fill spec 8): DONE.** INDEX.json now carries 50 day-1 and 43 day-2 rows; both
  digests indexed (lines 15094, 14698).

## 3. ECONOMICS lens: pricing the struck 191.8M against the yield

- **Cost side: unbanked, therefore unpriceable.** The 191.8M-token headline was struck as a
  phantom (ERRATA 001, STORY.md:240). This lane adds byte-evidence that nothing replaced it:
  0 of 58 REGISTRY rows carry any token/cost/usage field (parsed this session), and 0 of 236
  rows in `memory/runs/hermes_burn/usage.jsonl` name olm/frontier. Across all three windows
  the mine's spend exists nowhere in bytes. The descent protocol's leg 8 (every turn banks
  tokens and cost) has no carrier for workflow runs; the run journal is a compiled payload.
  Consequence: EV per token and EV per minute for the mine are UNCOMPUTABLE from the estate's
  own records - the estate cannot tell whether its only standing research intake is worth its
  cost, by its own accounting law.
- **Yield side: banked and modest-but-real.** 67 confirmed-find rows across three windows
  (21 + 23 + 23; 22 unique URLs in day-2). Day-2 adjudication survival: 23 of 244 banked items
  (9.4%). Day-2 folder: 69 content files, 1,089,105 bytes (re-measured this session; RECEIPT's
  78 files / 1,102,536 included the drifting .mimosa tree). Downstream landings: 16 percolator
  candidate rows ingested (promoted=false), one committed probe tool, one flag. Dogfood map:
  2 of 11 cards landed, 9 stalled (section 4).
- **Priced honestly:** 67 confirmed finds is real intake per byte of record, and the sweep
  corpora are durably banked; but any claim that the mine "paid for itself" in tokens is
  unsupported by bytes today. Fix (one sitting): extend REGISTRY rows (or a keyed runs ledger)
  with tokens-in/tokens-out/cost fields at run end, so the next window is priceable and no
  successor of 191.8M can appear.

## 4. DOGFOOD lens: which steal cards landed vs stalled (11 cards)

LANDED (2 of 11):
1. Day-1 card 6's tokenizer probe: RUN and durable - `tools/olm_tokenizer_probe.py` (4,038
   bytes, mtime Sep 30 19:04) committed in 0b846c01f. The one card probe that became an
   estate organ.
2. The percolator intake leg (GAP rank 6's fill): `--candidates` built into
   `mag/percolator.py` (docstring lines 23-25, handler at line 67) AND run against the mine:
   16 `frontier_mine` rows sit in `memory/percolator/candidates.jsonl` (ts
   2026-10-02T04:17:43Z, promoted=false, file-pointed at the day-1 candidates). Not yet
   promoted; that is the designed gate, not a stall.

STALLED (9 of 11), each with the check that says so:
3. Day-2 steal 1 (reach-ratio meter): no `reach_ratio` anywhere in `mag/` or `tools/` (grep).
4. Day-2 steal 2 (judge channel + schema v2): `tools/abliterate_p1_probe.py` contains zero
   "judge" mentions (grep -c = 0). Probe not amended.
5. Day-2 steal 3 (runtime parity): gated on steal 2's schema v2, so stalled upstream.
6. Day-2 steal 4 (Ollama 0.35 + /v1/systemone conformance): `ollama --version` = 0.34.3 this
   session; upgrade not done. Also no systemone surface outside the mine folders.
7. Day-2 steal 5 (KV degradation ladder): `mag/vast_launcher.py:444,457` still carries the
   unmeasured `--cache-type-k/v q8_0` SAELIS default; the ladder never ran, so the
   conditional review ticket never fired either.
8. Day-1 card 1 (memory probes P1-P5): present only as percolator candidate text; no receipt.
9. Day-1 card 3 (admission-control audit over STEALTH_MINED_FINDINGS): no audit receipt on
   disk (only pre-mine 09-27 files match the terms).
10. Day-1 card 4 (salon date guard): NOT stalled but WORSE - drifted stale.
    `watch/salon_runner.py` `_in_campaign_window()` (lines 242-256, read this session) gates
    on hour-of-day only; its docstring window "Sep 3-20 2026" is dead, the day-2 register row
    15 says the promo ran to Oct 7, and nothing in the code checks any date. A latent lane
    whose only window guard is a comment.
11. Day-1 card 5 (truncation-cap flag at `mag/lattice_loop.py:280`; ollama-ps probe):
    unchanged code in the cited range (read this session); probes never run.

Queued items scorecard: KVarN append NOT done (zero hits for 2606.03458/KVarN in
`memory/runs/corpus_gap_research/ARXIV_REGISTER.json`, grep this session). theneurondaily
fetch receipt NOT on disk: the promised "append the receipt beside sweep/inference-efficiency-x.md"
never landed; the 203,655-byte evidence exists only lane-held in a15-rollup.json - already
caught by the ractor accuracy lens (`ractor_engine/2026-10-01-dogfood-gaps/accuracy.md:102-108`,
"lane-held, not surface-held") and independently re-confirmed here (estate-wide grep for the
size stamp finds no receipt file). INDEX heal: DONE (section 2).

Verdict: GAP_REGISTER meta-gap 1 (MINED-NEVER-SCHEDULED) is confirmed with the mine as its own
subject: 2 of 11 cards reached estate organs; the other 9 are filed findings waiting for a
schedule-and-fire pass that has not come.

## 5. SECURITY lens

- **No injection surface handling in the intake scripts.** Grep for inject/untrusted/sanitize
  across `olm-mine.dwf.ts` and `the-gala.dwf.ts`: zero hits. Untrusted web content (HN,
  reddit, X, arXiv mirrors, redlib) flows through fetch caches into lane write-ups into
  registers with no scan step between fetch and record. The lethal-trifecta frame applies
  cleanly: untrusted content + estate-trusted record + the registers are communication.
  The system currently relies on lane discipline - and that discipline demonstrably worked
  once (the KVarN unsourced llama.cpp clause quarantined as UNSOURCED-OWED, DIGEST.md:115),
  which is the argument for converting the discipline into an instrument before the case
  where it does not.
- **The mine's own strongest security find is itself stalled:** the janitor-host hardening
  ticket from arXiv 2609.18526 (cross-tenant state-restore flaw, plaintext prompt lifetime)
  exists in no ticket surface (grep: only GAP_REGISTER and librarian mentions).
- **57 raw third-party cache files** (sweep/_raw, sweep/_fx) sit inside the shared surface
  watch/inbox. Pattern predates the mine (09-28 did it too), but the mine doubled the
  exposure; the shared-surface contract has no class for unscanned third-party payloads.

## 6. LINEAGE lens

- The rank-10 trio fill ("2 archive fetches") is stale doctrine: U3's full text is already
  held at `frontier_olm_20260928/sweep/_raw/full_2609.21341.txt`; the fill is now a rebank of
  held bytes. The estate keeps paying fetch prices for held evidence because window-scoped
  audits cannot see adjacent windows.
- Rank 9's phantom receipt stayed phantom for at least a day after the ractor's own accuracy
  lens named it (10-01) - the lineage jacket ("reinventing the estate's own forgotten ideas")
  has an estate-side twin: naming a defect and not scheduling its fill.
- The fan-out seats that reported lens files missing (day-2 DIGEST honest-gaps section) were
  describing their seat context, not the folder; the files existed. Same disease as the
  window-scoped grep: the shape of the seat, not the state of the world, decided what the
  audit could see.

## What the mine's shape cannot see (the blind spots, named)

1. Its own cost (no usage carrier on any workflow row) - so it cannot be rationally budgeted.
2. Its quotes' provenance after a fold that carried payloads in asks (16/23 day-2 rows).
3. Adjacent windows (folder-scoped greps; rank 10).
4. Its own downstream (the gate ledger cannot see a fold step dying; PASS over dead folds).
5. Its stalled probes (nothing schedules the cards' own falsifiable probes; 9 of 11 rot).
6. Untrusted-content handling between fetch and register (discipline, not instrument).

## Decision ledger

Closes: whether the mine's records are trustworthy by the estate's own byte-standard - yes for
day-1 (23/23), partial for day-2 (7/23 quote-level; numbers paraphrase-backed), with the fix
named (fold contract: quotes must resolve to pre-fold bytes; run it with
cross_ractor_bytecheck.py). Changes: GAP_REGISTER rank 10's description (evidence exists
in-folder at 09-28; fill is a rebank, not a fetch) and rank 9's status (phantom receipt
re-confirmed independently one day after the ractor lens named it). Arms: the mine-class
schedule-and-fire pass (2/11 landed) and the workflow-usage banking amendment.

Receipt chain: raw outputs `watch/inbox/gala_20260925/ouroboros/lanes/cross-ractor.check.txt`;
instrument `watch/inbox/gala_20260925/ouroboros/lanes/cross_ractor_bytecheck.py`; lane JSON
`watch/inbox/gala_20260925/ouroboros/lanes/cross-ractor.json`.
