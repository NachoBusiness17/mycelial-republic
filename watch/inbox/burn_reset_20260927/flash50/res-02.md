# res-02: Top 10 actionable insights from the stealth-mined findings (not yet acted on)

Date: 2026-09-29. Source: `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` (157 lines, read in full) plus the answer files it points to under `watch/inbox/burn_reset_20260927/work/` (19 files read in full; wave-1 `fan_*` stubs of 0-171 bytes read as sizes only). Every claim below names what I read or ran this session. Ranked by impact over effort, impact/effort descending. No em-dashes, no en-dashes.

## What the register actually contains

The JSONL is a dispatch register, not findings. 154 of 157 rows are `work_id: lib-belady-1966` re-dispatches spanning `2026-09-28T00:37:48Z` (line 1) to `2026-09-29T00:17:23Z` (line 156), still appending at read time. Three operator image drops (lines 52, 54, 55). Ten wave-2 mined findings (lines 78-87, note "wave 2 mined finding (10/10 clean)"). The insight-bearing material splits into: (a) the loop's own behavior, (b) one hermes answer that went off-script and found a live estate defect, (c) the answer files' OWED/STEALABLE content, (d) unconsumed image drops.

## The ranked ten

### 1. The work queue has a head-of-line block: sensed-never-done has no closer, so 12 queued investigations starve behind one solved item (effort S, impact high)

Finding: the register re-ran `lib-belady-1966` 154 times over ~24h after the debt was already collected by a sibling (`watch/inbox/burn_reset_20260927/flash50/r-belady-lruk.md`, read in full, banked 2026-09-28 with Crossref + bitsavers primary-source verification; receipt files `docs/ref/BIBLIOGRAPHY_MAP.md` and `docs/report_v1/sources/receipts/belady-1966.md` exist and `git status --porcelain` on all three is clean).
Verified cause: `tools/stealth_driver.py:291-297` `_next_work()` returns the first queue row lacking `done_ts`; the dispatch path writes only `sensed_ts` + `status: "sensed"` (`tools/stealth_driver.py:483-486`) and the code-as-law comment at `:488-493` says the funded tier must flip done, but the only done-writer for any queue is `t_selfimp` (`:740`) on a different file. Live bytes: `state/fuel/stealth_work_queue.jsonl` has 13 rows; row 1 is `lib-belady-1966, status: sensed, sensed_ts 2026-09-29T01:03:28, done_ts: None`; behind it: `lib-mattson-1970`, `lib-lruk-neil`, `w-quant-compare`, `w-schmidhuber-estate`, `w-water-display`, `w-kabbalah-epistemics`, `w-nelson-shuffle`, `w-muse-spark-access`, `w-belt-cube-mechanism`, `w-selfplay-hardware`, `m1`, `m002`, all never sensed. This matches arch-03's D1 and sess-05's "no done-flip verifier" gap (commit messages 6eb666d77, 34ad910fe), still unfixed.
Implement: (a) `_next_work` skips rows with `sensed_ts` newer than a staleness bar (e.g. 24h) so sensing rounds advance instead of re-sensing row 1 forever; (b) add the designed funded-tier verify topic (arch-03 v2 already reserved the slot) that reads the banked answer, verifies at the funded tier per RIB_DRIVING_LADDER, and flips `done_ts` with a receipt pointer; (c) one-time data fix: mark `lib-belady-1966` done pointing at `flash50/r-belady-lruk.md`.
Payoff: 12 starved investigations unblock immediately; ~6-10 wasted free-lane dispatches per hour stop; the register stops being a single-topic tape.
Risk: flipping rows done without verification violates the driving-ladder law (sensed-never-done, code at `tools/stealth_driver.py:488-493`); the flip must ride a funded-tier verify step or an explicit operator rule, never a silent edit. Wrong auto-flip would certify unverified free-lane text.

### 2. The estate's own gap sensor has fired 300+ times for days and nothing closes the loop (effort S to start, impact high)

Finding: hermes (tool-capable lane) went off-script in `work/lib-belady-1966_hermes.md:9-23` and found the lifecycle gap: `mag_temperature_gap` probing `GET /api/v1/lifecycle`, logging `lifecycle_gap:{scribe,lab}: should be on but actual off`, candidates sitting `status: new`.
Verified live: `memory/improve/candidates.jsonl` has 203 rows; 53 from `mag_temperature_gap`; 52 still `status: new`; newest new row ts `2026-09-29T00:38:33Z` (minutes before I read it), `local_feasible: "yes"`. Whole-ledger statuses: new 133, rejected 50, promoted 14, hold 6. `training/loop_gaps.jsonl` has 324 rows including the inverse gap `lifecycle_waste:drainer` ("should be off but still on", token/cpu waste) logged 09-28T00:15, 09-28T12:17, 09-29T00:17, every ~12h. The policy side exists (`mag/lifecycle.py:478-557` `_policy_should`, lab always-on at `:500-501`, scribe wanted at `:503-509`, drainer gate at `:517-524`) and the sanctioned verbs exist (`improve_off`/`improve_on`, `mag/lifecycle.py:156-230`) but their only callers are operator commands (`main.py:4794,4800`).
Implement: start ledger-only: a dedupe/triage pass that collapses the 53 same-shape gap rows into one open incident row and flips stale duplicates to hold with a pointer (dedupe key already exists in `loop_gaps.jsonl` rows). Then the mechanical close: after N consecutive identical probes with `local_feasible: yes`, run the sanctioned on/off verb behind the existing `improve_intentional` flag (`mag/lifecycle.py:71-137`), re-probe, and write the receipt.
Payoff: the estate's own cheap-local pieces (scribe) come back on; drainer waste stops; the candidates ledger stops accreting identical rows (133 unreadable `new` rows today); the hermes answer's own proposed test (restart, re-probe, verify ON, zero API spend) gets a runner.
Risk: auto-restart can flap when should/actual disagreement is intentional; the `improve_intentional` flag exists precisely for that and must gate the auto path. Lifecycle verbs are state changes on the operator's box, so phase 1 (ledger hygiene) is the safe first landing.

### 3. Mined evidence self-erases: 154 dispatches wrote into the same 8 answer paths with no content hash (effort S, impact medium)

Finding: every register row points at one of 8 fixed paths (`lib-belady-1966_hermes.md`, `_nous1..4.md`, `_openrouter1..4.md`); my reads show each file holds only the latest run (e.g. the hermes file's body ts is `2026-09-29T00:09:40`, the last hermes row). The mined rows carry no sha256 (`tools/stealth_driver.py:470-481`), while the drift runner in the same directory already does it right (`work/drift_q033_summary.json:14,27,40` stores per-lane sha256).
Implement: in the register writer, add `answer_sha256` and make the filename ts-suffixed (or archive the prior file before overwrite); backfill is impossible for already-overwritten bodies, so state that loss honestly.
Payoff: the mined corpus stops collapsing 150+ answers into ~8 survivors; dedupe, the percolator consumer (insight 6), and any future training corpus (code-agent-data) become possible on real bytes.
Risk: disk growth; bound it with a retention cap or per-work_id archive cap.

### 4. The or-cache-mechanics OWED is half-answerable from the estate's own register (effort S, impact medium)

Finding: `work/fan2_or-cache-mechanics_meta_muse-glimmer-30b.md` is OWED on OpenRouter caching (TTL, prefix matching, pricing per model). But the register has been measuring cache behavior all along: `cached_tokens` is 149-152 on `stealth/space-bunny-alpha` across dozens of rows (e.g. lines 4, 10, 13), 0 on `ling` rows, and 54/192/194 on `muse` rows when the ask changed (lines 95, 99). Per-model, prefix-sensitive caching is observable in-house every cycle.
Implement: a ~20-line reducer over `STEALTH_MINED_FINDINGS.jsonl` emitting a per-model cached-token histogram into the driver heartbeat/state; then one A/B (byte-stable ask vs perturbed ask) on two lanes to measure the prefix-sensitivity delta; get the pricing half from OpenRouter docs via `mag.cmd research-pack`.
Payoff: a routing law for free lanes (prefix-stable asks ride the caching lane; fresh-prefix asks ride the cheapest lane) that trims the sensing budget with data already on disk.
Risk: `cached_tokens` semantics are provider pass-through and may not be comparable across models; do not convert to pricing claims without the docs.

### 5. The operator's quantization handbook drop is unconsumed (effort S, impact low-medium)

Finding: register line 52 banks `watch/inbox/QUANTIZATION_HANDBOOK_technmak.png` (exists, 915,340 B, mtime Sep 28 06:22 local) with the digest `q=clip(round(x/s)+z), xhat=s(q-z); W8A8/W4A16/KV-cache; storage bit-width != compute bit-width`. `flash50/w3-quantizer-theory.md` (21,709 B, mtime Sep 28 17:01 local, after the drop) contains zero hits for technmak/handbook/W4A16/NF4 (my grep). `mag/quantizer.py` still does not exist (my `ls` errors), so arch-03's D6 hollow-ingest complaint stands.
Implement: fold the poster's content into `w3-quantizer-theory.md` as a cited section (image path + the four pattern families), and let it feed the next quantizer design pass rather than `mag/quantizer.py` scaffolding.
Payoff: the operator's own drop becomes corpus instead of a PNG at rest; one open defect (D6) gets a concrete counterexample closed.
Risk: near zero; it is a documented fold, not code.

### 6. The register's downstream claim is false: nothing ingests the mined findings (effort M, impact medium-high)

Finding: every mined row carries the hardcoded note "findings register row; percolator/quantizer may ingest" (`tools/stealth_driver.py:479`). I grepped: `STEALTH_MINED` appears only in `tools/stealth_driver.py:127,788` (the writer and t_selffeed). `mag/percolator.py` exists (landed `d575bc168`, 2026-09-14) and the quantizer chain exists (`tools/thought_quantizer.py` over `memory/percolator/invariants.json` per commit 748804083), but no hop connects either to the register or to `candidates.jsonl`.
Implement: a harvest topic in the driver: read `MINED_FILE`, dedupe by `work_id + answer_sha256` (depends on insight 3), and emit percolator candidates or `improve` candidates with lane/model provenance intact; keep it append-only through the sanctioned writers (s2-23's lesson: twin writes bypass events).
Payoff: ~150 banked answers become structured signal instead of an append-only orphan; the note stops lying; the selffeed queue (which already feeds on this file via `t_selffeed`, `tools/stealth_driver.py:782-800`) gets higher-quality inputs.
Risk: percolator ingest can launder free-lane sensing into trusted invariants; provenance tags must ride every row and the funnel must land in findings, never in done/laws, per the driving ladder.

### 7. The Belady STEALABLE is a property test the estate can run on its own caches (effort M, impact medium)

Finding: multiple lib-belady answers converge on the same stealable: capacity monotonicity is a property of the eviction policy, not the memory; demand a stack-consistency test before assuming more capacity helps (`work/lib-belady-1966_nous1.md:25`, `nous2.md:22`, `openrouter3.md:21`). The estate already weaponized the idea in one domain: `memory/research_polished/kv_cache_compaction.md:13` sets the bar "any eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is decoration".
Implement: a generic monotonicity harness: run the same access trace across increasing budget and assert misses/latency never increase; first targets are in-house caches where non-monotonicity is already suspected, e.g. the context_pack render ladder (arch-01, commit in git log: rung 3 is all-or-nothing 12.8-15.6k shed and rung 4 hard clip destroys the tail, i.e. more budget shed more useful context) and the FTS catalog fallback path (B2-465).
Payoff: converts a 1966 anomaly into a standing regression test for every cache-shaped knob the estate tunes; would have caught the rung-4 tail destruction mechanically.
Risk: harness generality is a rabbit hole; pin v1 to two named traces and two named caches with a fixed pass/fail contract.

### 8. The headless-agent pattern card validates the stealth-lane redesign and names the missing organ (effort M, impact medium)

Finding: `work/fan2_headless-agent-cli_inclusionai_ling-3.0-flash-vl.md:13-28` banks verified patterns: git-integrated checkpointing (aider history + repo-map), `--output-format stream-json` for programmatic headless runs, and the recommended external session store (transcripts + task state + partial outputs in SQLite/JSONL, orchestrator snapshots, git commits as checkpoints). The stealth lanes have fragments (WORK_STATE, register, answer files) but no coherent session store: no resume, evidence overwrite (insight 3), no done-flip verifier (insight 1), and arch-03's D5 two-concurrent-instances defect.
Implement: consolidate the three artifacts into one per-work_id session record (answer path, sha, sensed_ts, done_ts, verify receipt) with the driver as the single writer and a lock file for single-instance enforcement; this is the same surface insights 1 and 3 patch, so sequence it after them.
Payoff: headless lanes become crash-resumable and audit-able; D5's duplicate-driver hazard gets a durable check; the wave-2 library questions stop needing manual sibling rescues.
Risk: migration churn on a live loop; do it as an additive record, not a rewrite of the queue file.

### 9. Self-play pretraining (arXiv 2609.30063) is real and maps onto t_selffeed as a curriculum engine (effort M, impact medium-high, strategic)

Finding: `work/fan2_solomonoff-pretrain_inclusionai_ling-3.0-flash-vl.md` was OWED (lanes could not verify the paper). I fetched `https://arxiv.org/abs/2609.30063` this session: it exists, "Self-Play Pretraining with Zero Data" (Cowsik, Dolev, Li et al., submitted 24 Sep 2026): an RL generator proposes programs for a universal Turing machine, a cross-entropy learner predicts the bytes, and the generator targets the frontier of the learner's ability. Sibling card `flash50/r-solomonoff-pretrain.md` already deep-verified it (arXiv full text, HN, repos, reproduction REPORT.md). Unacted: `t_selffeed` (`tools/stealth_driver.py:782-800`) picks exactly one next item from the last 8 register rows via Hermes with no ability model and no frontier targeting, which is how `lib-belady-1966` got re-asked 154 times after being solved.
Implement: mine the register for per-topic OWED rate and repeat count; bias the selffeed ask toward the OWED frontier (topics where lanes keep failing) and away from solved ones; keep the m* human-readable review step that already exists in the queue (`m1`, `m002`).
Payoff: the estate's investigation queue grows toward its actual ignorance instead of around it; this is the cheap, sensing-side version of the paper's curriculum loop.
Risk: free-lane sensing cannot verify its own curriculum (driving ladder); OWED-bait could degenerate into junk topics if the frontier metric is gameable; verification climbs must route to the funded tier.

### 10. The contrastive-pair context governor: banked reproducibility, pending operator GO (effort L, impact high, gated)

Finding: `work/fan2_contrastive-wm_inclusionai_ling-3.0-flash-vl.md:37-43` banks the practical path: SPR-style latent self-prediction is the cheapest of the line, single 24 GB GPU, no pixel decoder, 1-2 day runs. The estate's own research organ already holds the matching plan and eval bar: `memory/research_polished/kv_cache_compaction.md:28` is an explicit pending "Operator GO -> build the in-session context governor on the Nimble pattern... trained on the fleet's own contrastive pairs from db.sqlite transcripts", with the eval bar at `:13` (recency null first, matched budgets, cache economics first-class). `flash50/r-contrastive-wm.md` banked the bibliography 2026-09-28. Nothing has been built.
Implement: stage it exactly as the file says: (1) recency-null baseline over real transcripts; (2) LoRA scorer on fleet pairs; (3) threshold ablation and repeated-cycle decay; judgment at the funded tier.
Payoff: replaces the heuristic clip ladder (arch-01 measured 16.5 percent survival at janitor budget with tail loss) with a measured governor; the fleet's own transcripts become training data.
Risk: heaviest lift of the ten (GPU time, eval discipline); explicitly operator-GO-gated; a badly scored governor silently drops the wrong context, so the recency null is not optional.

## Excluded from the ten, with reasons

- `belt-cube-real`, `water-plasma`, `eam-tracking`, `vortex-latent` (wave-2 files read in full): honest OWED/verification answers on operator curiosity topics with no estate mechanism to act on; rank cards already banked for the wave-1 versions (`r-belt-cube.md`, `r-water-plasma.md`, `r-eam-tracking.md`, `r-vortex-latent.md` exist in flash50; headers of two read). EAM content in particular stays a passive-verification topic only.
- `transformer-typing` cartoon note (register line 55): essay, not mechanism.
- chaos-poster note (register line 54) claims a same-second append race froze downstream and "the verify gate caught it": I found 38 rows matching "race" in `memory/burns/LEDGER.jsonl` but not this specific incident, and s2-23 (commit 748804083) already documents the INDEX race convention and twin re-registration. The unacted remnant (serializing shared appends) is real but owned by the f-24 convention lane, so it is not one of my ten.

## Not run / not verified

- The hermes answer's behavioral claims (`pro_fire` 191/200, `swarm_sense` 10 calls, `lib-belady-1966_hermes.md:11`): not verified; my tail counter over `training/events.jsonl` (587,970 rows) read empty kind/tool keys, so the schema keys differ and I stopped there.
- The exact race-incident receipt behind the chaos-poster note: not located.
- Full contents of `r-contrastive-wm.md`, `r-moe-offload.md`, `r-water-plasma.md`, `r-vortex-latent.md`, `r-belt-cube.md`, `r-eam-tracking.md`: headers only.
- `state/fuel/stealth_selfimp_queue.jsonl` health (9,241 B, last write Sep 28 13:54): existence checked, contents not read, no health claim made.
- pytest: not run; no code changed in this item.

## Checks run this session (commands)

- Read `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` in full (157 rows).
- Directory + size listing of `watch/inbox/burn_reset_20260927/work/` and `flash50/` (PowerShell Get-ChildItem).
- Read 19 work files in full (10 `fan2_*`, 8 `lib-belady-1966_*`, `fan_selfplay-sota_*`, `drift_q033_summary.json`).
- `./.venv/Scripts/python.exe` census of `memory/improve/candidates.jsonl`: 203 rows, 53 `mag_temperature_gap`, 52 new, latest new ts 2026-09-29T00:38:33Z; statuses new 133 / rejected 50 / promoted 14 / hold 6.
- Same interpreter census of `training/loop_gaps.jsonl`: 324 rows; `lifecycle_waste:drainer` at 09-28T00:15, 09-28T12:17, 09-29T00:17.
- Same interpreter row-count of `training/events.jsonl`: 587,970.
- `git grep STEALTH_MINED` (only `tools/stealth_driver.py:127,788`); `git grep percolator` callers; `git grep candidates.jsonl` (readers include `mag/improve.py`).
- Read `mag/lifecycle.py:478-562`; grep shows `improve_on/off` callers only at `main.py:4794,4800`.
- Read `tools/stealth_driver.py:280-310, 470-510, 700-745, 770-800`; listed topics/queues by grep.
- Dumped `state/fuel/stealth_work_queue.jsonl`: 13 rows, row 1 `lib-belady-1966` sensed at 2026-09-29T01:03:28, `done_ts: None`.
- `ls mag/quantizer.py` (absent), `mag/percolator.py` exists; `git log -- mag/percolator.py` tip `d575bc168`; `git log -- docs/ref/BIBLIOGRAPHY_MAP.md` tip `d575bc168`; `git status --porcelain` on the three receipt files: clean.
- WebFetch `https://arxiv.org/abs/2609.30063`: exists, "Self-Play Pretraining with Zero Data".
- Grep `w3-quantizer-theory.md` for technmak/handbook/W4A16/NF4: zero hits.
- Read `r-belady-lruk.md` in full; heads of `r-solomonoff-pretrain.md`, `r-contrastive-wm.md`, `r-moe-offload.md`.
- `grep -c race memory/burns/LEDGER.jsonl` = 38.

One-line summary: the register's own mechanics (head-of-line block, evidence overwrite, false ingest note) plus one live sensed-but-unclosed estate defect (lifecycle gaps) are the top unacted insights; the library OWEDs are mostly already collected by sibling rank cards, and the remaining value is wiring the loop closed.
