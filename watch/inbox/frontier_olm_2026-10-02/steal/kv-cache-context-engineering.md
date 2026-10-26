# STEAL CARD: kv-cache-context-engineering (round 3, critique applied) - 2026-10-02

Area: kv-cache-context-engineering
Primary source: https://arxiv.org/abs/2606.03458 (KVarN: Variance-Normalized KV-Cache
Quantization Mitigates Error Accumulation in Reasoning Tasks, Muller et al., Huawei,
submitted 2026-06-02)
Banked by: steal-kv-cache-context-engineering (Mag Resource Harness steal gopher)
Input: 7 confirmed finds from the round-1 ask (4 KVarN confirmations across arxiv/HN/x/reddit
doors, llama.cpp PR #21038, PrefixWall 2603.10726, r/LocalLLaMA 1s720r8).

Round 3 status: the round-3 critique verified the round-2 substance (all five fixes and all
three improvements hold under re-run; the embedded JSON parses and its chars byte-matched the
file) but blocked approval on a cluster of citation-anchor defects and one non-reproducible
count. Every defect was re-derived against the tree THIS sitting (section 0), confirmed, and
corrected. One meta-lesson banked with the fixes: the x-sweep anchor error originated in the
round-1 critique and the round-2 card copied it instead of counting its own sed output; the
estate's citation_lint exists for exactly this class.

## 0. Round-3 corrections applied (each re-derived this sitting)

1. X-SWEEP ANCHORS WRONG (critique fix 1): `grep -n "vLLM v0.23.0|53.3 pct|public
   carrier|1s720r8" kv-cache-context-engineering-x.md` pins the README bullet at :32
   ("- The GitHub README (fetched): full vLLM fork (Apache 2.0, vLLM v0.23.0 base, 506"),
   the 53.3-pct AIME25 note at :34-35, and the 1s720r8 carrier at :36-40. The round-2
   card's ":29-30" and ":33-37" (inherited from the round-1 critique's own anchors) point
   at the arXiv-abstract bullet's author list. ALL occurrences corrected (round-2 section
   item 4, round-2 check 1, section 6's resolved item and 53.3 note). Self-note: the
   round-2 sed output itself had the README bullet as its 8th printed line of a block
   starting at 25, i.e. :32; the card copied the critique instead of counting.
2. FLASH50 OFF-BY-ONE (critique fix 2): `grep -n "issuecomment-4141323088|issuecomment-
   4146397570" flash50/work/llama-kv-cache.cpp` returns :1444 and :1464. Round 2's check 3
   said ":1443"; corrected (round-2 section item 8 already carried 1444,1464 correctly).
3. BURNS LENS ANCHORS OFF BY ONE (critique fix 3): `sed -n '93,101p'` of lens/burns.md
   shows the five-steal sentence spanning :97-99 with "KV degradation" ending :98 and
   "ladder" on :99, so the ladder is named at :98-99 (not :97-98), and the stale KVarN
   UNCONFIRMED line spans :99-100 (not :98-99). Corrected in section 4 and section 6.
4. COUNT DOES NOT REPRODUCE (critique fix 4, worst defect): round 2 claimed
   `grep -rln "2609.18526" watch/inbox memory docs` "returns 10 files". Re-run this
   sitting WITHOUT the round-2 command's `head -10` (which was piped and its truncation
   reported as the count): 38 paths (29 under watch/inbox, 8 under memory, 1 under docs),
   full list captured, INCLUDING THIS CARD ITSELF (self-hit) and two holdings round 2 did
   not name: the estate holds the flaw paper's own PDF
   (memory/runs/gathering_expedition/p2_2609.18526.pdf) and its source receipt
   (docs/report_v1/sources/receipts/paper_2609.18526.md). The OWED conclusion survives
   unchanged: nothing among the 38 establishes vendor fix-absence; the named anchors
   (open-local-language-models.md:189-193 flaw bank) are all real hits.
5. GARBLED ANCHOR (critique fix 5): round 2's steal 4 cited "(ARXIV_REGISTER.json:73
   CANDIDATES path"; `sed -n '73p'` of the register returns the literal four chars of
   indentation plus "{". The candidates path is mag/percolator.py:73 (CANDIDATES_REVIEW,
   verified by sed this sitting); steal 4 corrected.
6. PROBE REFINEMENTS (critique fix 6): (a) the pre-registered branches left the
   0.4-to-0.8 mean-steps-gap band firing nothing; an INCONCLUSIVE branch is added (rerun
   with 3 repeats per arm or escalate to 32-step depth; the executor is never branchless).
   (b) Arm R's knob-witness spot check moves from session-1 shallow end to max chain depth
   (step 8, 4K) and is DEMOTED to corroborating: the 10-01 card's own reasoning
   (quantization-compression.md:147-148, re-verified this sitting: "Context is pinned
   deliberately: KV bytes and the KV-quant delta scale with context, and at short prompts
   the delta on a 1.7 GB model sits inside VRAM noise") means a shallow-end check can read
   inside-noise and VOID a good run; Arm N's pinned-8K witness (:141-142) is the PRIMARY
   precondition for both arms.

## 1. Checks run THIS sitting (round 3; rounds 1-2 substance stands per the critique's re-run)

1. `grep -n "vLLM v0.23.0\|53.3 pct\|public carrier\|1s720r8"
   watch/inbox/frontier_olm_2026-10-02/sweep/kv-cache-context-engineering-x.md`: :32 README
   bullet, :34 the 53.3-pct note, :36 the 1s720r8 carrier bullet, :54/:139/:147/:160
   downstream mentions. Confirms correction 1.
2. `grep -n "issuecomment-4141323088\|issuecomment-4146397570"
   watch/inbox/burn_reset_20260927/flash50/work/llama-kv-cache.cpp`: :1444 and :1464.
   Confirms correction 2.
3. `sed -n '93,101p' watch/inbox/frontier_olm_2026-10-02/lens/burns.md`: five-steal list at
   :97-99 (ladder named :98-99), stale KVarN line :99-100. Confirms correction 3.
4. `grep -rln "2609.18526" watch/inbox memory docs > /tmp/ow18526_hits.txt; wc -l`:
   38. List captured and inspected; includes this card (self-hit), the held flaw PDF, its
   source receipt, the 10-01 open-local card, 10-01 DIGEST, 10-02 lens/burns.md, the four
   10-02 sweep records, 09-30 and 09-28 sweeps, gala/librarian/ouroboros artifacts,
   memory LINKS.jsonl, percolator candidates, mickey17 gap-analysis lanes, trajectory
   steps.jsonl. Confirms correction 4.
5. `sed -n '73p' memory/runs/corpus_gap_research/ARXIV_REGISTER.json` returns "    {";
   `sed -n '73p' mag/percolator.py` returns the CANDIDATES_REVIEW line. Confirms
   correction 5.
6. `sed -n '145,149p' watch/inbox/frontier_olm_2026-10-01/steal/quantization-compression.md`
   confirms the VRAM-noise reasoning at :147-148 used by correction 6b.
7. Standing from rounds 1-2 (critique re-verified round 2; not re-run here): PDF hash
   c437782e...7571739 / 874,189 bytes; ARXIV_REGISTER.json 934 results, row 933 the only
   kvarn row; PR #21038 live fetch (merged 2026-04-01, full AIME25 table,
   LLAMA_ATTN_ROT_DISABLE, tg128 ratios 0.88-0.93); HN 48399974 live fetch (143 pts,
   "It's not better quality: 59.3% vs 59.4% fp16 on AIME 25"); ollama 0.34.3 on PATH;
   mag/vast_launcher.py:444,457 q8_0 KV flags; hn sweep :27 anchor correct; f-10.md:856-874
   span; quantization-compression.md:193 ceiling line; the moved receipt
   sweep/_fx/arctic_refetch_1s720r8.json (4,596 bytes, mtime preserved).

## 2. What the finds establish (after verification)

- KVarN is real and vLLM-native; the estate-relevant claim is the error model: KV
  quantization error accumulates across autoregressive timesteps, driven primarily by
  "incorrect token scales", and the field evaluates KV quant "under prefill-like settings"
  (sweep :76-80). Quality vs FP16 is parity-within-noise (59.3 vs 59.4 AIME25, live HN
  fetch): the win is memory and speed, not accuracy.
- The 2026-04-01 mainline llama.cpp rotation merge (PR #21038, fetched live round 1,
  re-verified by the round-2 critique) makes the same point on our serving stack's own
  codebase: unrotated q8_0 KV costs 6.2 AIME25 points vs F16 (31.7 vs 37.9); one Hadamard
  rotation before caching recovers to 37.1; q4_0 goes from unusable (2.0) to usable (21.7);
  tg cost 7-12 pct (ratios 0.88-0.93; 202.37/229.42 = 0.882 at the worst). Within-fold
  note: the hn lane's 11:39 verdict still called the unrotated-q8 finding unsourced (hn
  sweep :27); the PR's own AIME25 table is the primary that settles it.
- PrefixWall (arXiv 2603.10726; abstract numbers live-verified by the round-2 critique:
  "up to 70% higher cache reuse and 30% lower inference latency", "selectively isolates
  prefixes") is the strongest response to the shared-KV side-channel class: selective
  per-prefix isolation, not sledgehammer cache-disable. Vendor fix status for the banked
  2609.18526 state-restore flaw remains OWED (section 6).
- The citation loop closed cleanly: the 10-01 suppression (DIGEST.md:115) held the clause
  out of circulation for a day; the PR plus the 1s720r8 thread (two in-fold artifacts:
  x sweep :36-40 and the moved _fx receipt) sourced it; the register append fired
  (ARXIV_REGISTER.json row 933 of 934, byte-verified round 1 and by the critique).

## 3. The steals (mechanisms)

1. AMEND the 10-01 KV ladder probe with an accumulation arm (full REV 3 instrument in
   section 5). The banked probe (quantization-compression.md:131-153) is a 20-prompt
   single-turn needle bank: exactly the prefill-style gate KVarN says misses KV quant
   damage. The relay arm measures the accumulation axis the paper names.
2. Rotation-default for estate llama.cpp serving. Port move: pin the llama.cpp build in
   the SAELIS launch receipt (mag/vast_launcher.py:444,457 serves q8_0 KV at 262K ctx on a
   pulled llama-server of unmeasured vintage; pre-merge builds sit in the 31.7 pct world,
   post-merge in 37.1) and treat rotation as default-on for long-reasoning serving, opt-out
   by LLAMA_ATTN_ROT_DISABLE, at 7-12 pct tg cost. Same vintage check for the host's
   ollama 0.34.3 (probe phase 0).
3. PrefixWall banks as the defense SHAPE for multi-principal serving (selective per-prefix
   isolation), the strongest available response to the 2609.18526 flaw class (the estate
   even holds the flaw paper's own PDF, memory/runs/gathering_expedition/p2_2609.18526.pdf,
   per the 38-path grep). Design-bank only: the estate is single-principal today
   (mag/auto_quantize.py:5). Vendor fix-absence is OWED, not asserted; the design-bank
   does not depend on it.
4. Percolator receipt row: clause-suppression worked end to end. The UNSOURCED-OWED ruling
   held the clause for a day, two primaries sourced it, and the register row landed
   (ARXIV_REGISTER.json row 933; the candidates path is mag/percolator.py:73; promotion
   stays with percolate(), never ingestion, mag/percolator.py:70-72).
5. ANALOGY ONLY, quantizer organ (convention per 10-01 card :117-121): KVarN attributes
   compounding damage to per-step scale misestimation, not bit-width. mag/auto_quantize.py
   (:9-24: variance determines resolution, anomalies never quantized, chain root
   recoverable) has no accumulation-axis check for chained consumers (quantized aggregate
   to invariant to context pack). Design-bank: gate such streams on end-to-end consumer
   drift, not per-bucket error. No code port; auto_quantize is NOT a KV quantizer.

## 4. Estate map (organ per steal)

- Janitor/specialist serving tier (real landing spot for steals 1 and 2): the relay probe
  runs on gemma:2b (b50d6c999e59, on box per the 10-01 card's `ollama list`; ollama 0.34.3
  on PATH verified round 1); the SAELIS recipe gets the build-pin + rotation-status line.
  Corroboration already in-tree: the flash50 vendored bytes (llama-kv-cache.cpp:1444,1464,
  commit 1ba61713d, f-10.md:858-872) show the estate has carried the rotation code,
  unrecognized, since 09-29.
- Context pack (mag/context_pack.py:35 _emit_pack_offload): inherits the accumulation
  lesson as an input only: the relay arm measures degradation as a function of chain
  depth, the same axis the pack's shed decisions live on. No code change claimed; the
  reach-ratio port belongs to the sibling agent-memory card.
- Sovereign mirror (docs/DOCTRINE_MAP.md:78, per 10-01 card :114-116): receives PrefixWall
  as the isolation-policy rung for any future multi-principal mirror; the 2609.18526 flaw
  it answers is banked at open-local-language-models.md:189-193 with the same organ.
  Design-bank.
- Percolator (mag/percolator.py:70-73): receives steal 4 as a candidates.jsonl receipt row.
- Quantizer (mag/auto_quantize.py): analogy-only design-bank (steal 5), labeled as such.
- Water graph (hydrology: mag/field_flow.py) and gopher fleet: NO find feeds either as a
  code port, recorded as no-feed per the 10-01 convention (:127-129); the relay arm merely
  uses the gopher shape (chained steps) as its instrument.

## 5. Probe (REV 3; falsifiable, cheap, this week; the StealCard JSON carries this one)

Phase 0 (minutes, config): determine rotation status of the host stack: read the llama.cpp
build string from `ollama serve` debug output or the 0.34.3 release notes; record pre- vs
post-2026-04-01. For SAELIS the fix is a recipe line: pin `llama-server --version` into the
launch receipt.

Phase 1: on gemma:2b, identical seed and temperature, three KV arms (f16, q8_0, q4_0), two
instruments:

- Arm N (needle, prefill-style, unchanged 10-01 instrument): 20 pinned-context prompts
  (~8K filler, ceiling confirmed at probe time per quantization-compression.md:193) with
  one exact-match needle task. Its `ollama ps` SIZE delta between f16 and q8_0 at the
  pinned context (:141-142) is the PRIMARY knob-efficacy precondition for the whole run.
- Arm R (relay, accumulated): 20 sessions x 8 chained steps; step k's prompt embeds step
  k-1's emitted answer verbatim under a deterministic transform relay; per-step budget
  512 tokens (input + answer), 8 steps = 4K total, half the ~8K ceiling. Per-step scorer:
  a reference implementation computes each step's expected output from the seed; step k
  scores 1 iff the emitted answer matches exactly after whitespace strip. Arm R carries a
  CORROBORATING witness only: one `ollama ps` SIZE spot check per KV arm at MAX chain
  depth (step 8, 4K), not at the shallow end, where the 10-01 card's own reasoning
  (:147-148) puts a 1.7 GB model's f16-vs-q8_0 delta inside VRAM noise.

KNOB-EFFICACY PRECONDITION: Arm N's measured `ollama ps` SIZE at pinned context must drop
measurably from f16 to q8_0 to q4_0 (:141-142). If that delta is absent, the KV-cache-type
knob is no-op-ing (e.g. flash attention off): the run is VOID, no branch fires, fix the
serving invocation and rerun. A weak or inside-noise Arm R depth-8 witness does NOT void
the run while Arm N's primary witness holds; a working knob can no longer void a good run.

Pre-registered branches (evaluated only if the precondition holds); the branch set is
exhaustive, the executor is never branchless:

- PASS (paper transfers): Arm N replicates (q8_0 flips 0/20 vs f16) AND Arm R's
  mean-steps-correct gap (f16 minus q8_0) is at least 0.8 of 8 steps (10 pct of the chain)
  AND on the majority of failing q8_0 sessions steps 1-2 score correct with
  first-divergence at step 3 or later (the accumulation signature, scoreable by the
  per-step scorer). Action: single-turn KV gates are declared insufficient; the ladder is
  re-specced with the relay arm as its quality instrument and its stop rule taken from the
  fold's RQ4 hand-off, the 2609.27981 per-request exceedance certificate (sweep :83-84,
  :136-145): certify each KV arm with law-critical reach as the utility, fall back to f16
  when nothing certifies; file the SAELIS review ticket.
- FALSIFIED (conditional on the precondition): Arm N replicates AND Arm R holds within
  noise of f16 (mean-steps gap under 0.4 of 8, i.e. under 5 pct). Action: file KVarN's
  accumulation thesis as scale-dependent on this stack (gemma:2b, 8 steps, 4K); re-probe
  at 32-step depth before discarding.
- INCONCLUSIVE (the band round 2 left branchless): mean-steps gap in [0.4, 0.8) of 8
  (5-10 pct). Action: rerun Arm R with 3 repeats per arm and majority-combine, or escalate
  straight to 32-step depth; either outcome re-enters PASS or FALSIFIED on the rerun's
  gap. No ladder or config change may be claimed from an INCONCLUSIVE run.
- PRE-EMPTED: Phase 0 finds the build carries the rotation and Arm R holds. Action: the
  estate is already in the 37.1 pct world; bank as verified-safe, keep rotation default.
- ESCALATE: Arm N itself drifts (q8_0 flips >= 2/20): the 10-01 falsifier fires first
  (:142-145): immediate review ticket against the unmeasured SAELIS q8_0 default.

Cost: ~543 local inferences (60 Arm N + 480 Arm R + 3 spot checks), $0, one afternoon.
Step 1 remains the Ollama KV-knob verification with the raw llama-server fallback
(quantization-compression.md:149-151).

## 6. Degradations (honest)

- COUNT ERRATUM (round 3): round 2's "10 holdings" for 2609.18526 was its own `head -10`
  truncation reported as a count. The real number on this tree this sitting is 38 paths
  (29 watch/inbox, 8 memory, 1 docs), including this card itself. Instrument lesson banked:
  never report a piped truncation as a census.
- OWED: whether any vendor has shipped a fix for the 2609.18526 llama.cpp state-restore
  flaw. The 38-path grep banks the flaw everywhere but establishes absence nowhere; the
  nearest holdings are the flaw paper's own PDF (memory/runs/gathering_expedition/
  p2_2609.18526.pdf) and its source receipt (docs/report_v1/sources/receipts/
  paper_2609.18526.md), neither of which speaks to vendor fix status. Owner: the next kv
  or open-local lane with a browser door.
- Carried on the ask's word: PrefixWall's mechanism internals beyond the abstract (the
  critique's live fetch verified the headline numbers, not the body); the r/LocalLLaMA
  thread body beyond the moved _fx receipt's metadata (author, created_utc, issuecomment
  pointer all byte-verified; comment bodies not present in the submission-only receipt).
- Resolved (round 2, anchors corrected round 3): the README vLLM version. Primary
  (in-fold README fetch, x sweep :32-33): v0.23.0. Secondary (HN comment): 0.22. Resolves
  to the README. The x sweep's README note also carries "AIME25 53.3 pct parity" for the
  kvarn_k4v2_g128 preset (:34-35), a different number from the HN comment's 59.3/59.4;
  different presets or benchmark cuts, unreconciled, cited rather than guessed.
- Not re-run this sitting: the sweep's PyMuPDF extraction numbers (17 pages, 54,824 chars,
  zero llama.cpp/AIME25/q8); corroborated by the hn lane's independent pypdf zero-hit
  check (hn sweep :27) and the critique's corroboration, not re-executed here.
- Not run: Phase 1 of the probe (executor's instrument; the card says so itself). The
  returned StealCard JSON's chars field is measured from this file post-write; the embed
  below is the exact returned JSON.
- The lens/burns.md:99-100 stale status line (KVarN UNCONFIRMED, clause do-not-repeat) is
  superseded by this card's primaries but not edited in place; the fold that owns the lens
  should refresh it from this card.

## 7. Machine-readable card (identical to the returned StealCard JSON)

{"area": "kv-cache-context-engineering", "steal": "KVarN's error model (arXiv:2606.03458, CONFIRMED from two primaries, both verified live or by hash in rounds 1-2 and re-verified by the critique): KV-quantization error accumulates across autoregressive decode timesteps, driven primarily by incorrect token scales, and the field gates KV quant under prefill-like settings, so the estate's banked 20-prompt single-turn needle probe (watch/inbox/frontier_olm_2026-10-01/steal/quantization-compression.md:131-153) is exactly the instrument class that misses the failure. Port: AMEND that probe with a chained 8-step relay arm (step k conditions on step k-1's emitted answer, 512-token per-step budget, per-step deterministic scorer) at the same three KV arms, gated by Arm N's pinned-8K ollama-ps VRAM knob-efficacy precondition with Arm R's depth-8 spot check corroborating only, so a silent knob no-op can never read as falsification and a working knob can never void a good run. Second steal: the previously UNSOURCED llama.cpp kv-rotation clause is SOURCED (PR #21038 fetched live: merged 2026-04-01, Hadamard rotation before caching, AIME25 Q8_0 31.7 to 37.1 vs F16 37.9, Q4_0 2.0 to 21.7, opt-out LLAMA_ATTN_ROT_DISABLE, tg cost 7-12 pct from the 0.88-0.93 bench ratios), and the estate has carried the post-rotation code unrecognized since 09-29 (watch/inbox/burn_reset_20260927/flash50/work/llama-kv-cache.cpp:1444,1464, commit 1ba61713d): rotation becomes the default-on rung and the SAELIS q8_0 KV recipe (mag/vast_launcher.py:444,457) must pin its llama.cpp build vintage. Third: PrefixWall (2603.10726, abstract numbers live-verified by the round-2 critique) banks as the selective per-prefix isolation defense shape for the shared-KV side-channel class, design-bank only, single-principal estate today (mag/auto_quantize.py:5); the estate holds the 2609.18526 flaw paper's own PDF (memory/runs/gathering_expedition/p2_2609.18526.pdf) but vendor fix-absence stays OWED, not asserted. Fourth: the percolator gets a receipt row proving clause-suppression worked end to end (10-01 DIGEST:115 held the clause; two primaries sourced it; the ARXIV_REGISTER.json append fired, row 933 of 934, byte-verified; candidates path is mag/percolator.py:73). Quality context from the live HN fetch: KVarN is parity-within-noise vs FP16 (59.3 vs 59.4 AIME25): the win is memory, not accuracy.", "source_url": "https://arxiv.org/abs/2606.03458", "estate_map": "Feeds the janitor/specialist serving tier and the KV degradation ladder instrument (lens/burns.md:98-99), with design-banks to percolator, sovereign mirror, and quantizer. Concrete port moves: (1) relay-arm amendment to the banked KV-ladder probe on gemma:2b, inheriting the 10-01 card's Ollama-knob-verification step and pinned-8K VRAM witness (quantization-compression.md:141-142, :147-148, :149-151); (2) a build-pin + rotation-status line in the SAELIS launch recipe (mag/vast_launcher.py:444,457 serves --cache-type-k q8_0 --cache-type-v q8_0 at -c 262144 on a llama-server of unmeasured vintage), same vintage check for host ollama 0.34.3, with the flash50 vendored bytes (llama-kv-cache.cpp:1444,1464, commit 1ba61713d, classified f-10.md:858-872) as in-tree corroboration that the rotation code is already held; (3) percolator receipt row to memory/percolator/candidates.jsonl via the alpha-budget path (mag/percolator.py:70-73); (4) PrefixWall as the isolation rung in docs/DOCTRINE_MAP.md:78 sovereign-mirror terms, design-bank only, answering the 2609.18526 flaw banked at open-local-language-models.md:189-193; (5) mag/auto_quantize.py gets an ANALOGY-ONLY design-bank (per-step scale misestimation compounds; variance-determined resolution at :9-24 has no accumulation-axis check for chained consumers), labeled per the 10-01 convention (:117-121). Water graph (hydrology, mag/field_flow.py) and gopher fleet: no-feed, recorded per convention (:127-129).", "probe": "Two-phase, ~543 local inferences, $0, one afternoon. Phase 0 (minutes): read the llama.cpp build string from ollama serve debug output or the 0.34.3 release notes; record pre- vs post-2026-04-01 rotation merge. Phase 1 on gemma:2b, identical seed and temperature, three KV arms (f16, q8_0, q4_0), two instruments: Arm N, the unchanged 10-01 20-prompt pinned-context (~8K, confirm at probe time per quantization-compression.md:193) needle bank, whose ollama-ps SIZE delta f16 vs q8_0 (:141-142) is the PRIMARY knob-efficacy precondition; Arm R, 20 sessions x 8 chained steps, per-step budget 512 tokens (8 steps = 4K, half the ceiling, no truncation confound), step k's prompt embedding step k-1's emitted answer verbatim under a deterministic transform relay, scored per step against a reference implementation's expected output (exact match after whitespace strip), with a CORROBORATING-only ollama-ps SIZE spot check per KV arm at max chain depth (step 8, 4K), not the shallow end, where a 1.7 GB model's delta sits inside VRAM noise (:147-148). PRECONDITION: absent Arm N delta means the KV-cache-type knob no-ops (flash attention off), the run is VOID, no branch fires, fix the invocation and rerun; a weak Arm R witness never voids while Arm N holds. Exhaustive branches (never branchless): PASS if Arm N replicates (q8_0 flips 0/20 vs f16) AND Arm R mean-steps-correct gap (f16 minus q8_0) >= 0.8 of 8 AND the majority of failing q8_0 sessions score steps 1-2 correct with first divergence at step 3 or later, then the ladder is re-specced with the relay arm as quality instrument and the 2609.27981 per-request exceedance certificate (sweep :83-84, :136-145) as its stop rule, SAELIS review ticket filed; FALSIFIED (conditional) if Arm N replicates AND the gap < 0.4 of 8, thesis filed scale-dependent, re-probe at 32 steps before discarding; INCONCLUSIVE if the gap is in [0.4, 0.8): rerun Arm R with 3 repeats per arm (majority-combined) or escalate to 32-step depth, re-entering PASS or FALSIFIED on the rerun gap, no change claimable from an INCONCLUSIVE run; PRE-EMPTED if Phase 0 finds rotation present and Arm R holds (estate already in the 37.1 pct world); ESCALATE if Arm N itself drifts (q8_0 flips >= 2/20), firing the 10-01 falsifier first (:142-145) against the unmeasured SAELIS q8_0 default. Not run this sitting: Phase 1 is the executor's instrument; only config, fetch, hash, grep, and line checks executed.", "chars": 25055}
