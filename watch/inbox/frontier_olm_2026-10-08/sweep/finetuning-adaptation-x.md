# SWEEP: finetuning-adaptation via X (frontier_olm 2026-10-08)

Seat: sweep-finetuning-adaptation-x. Ask: five research questions over the X door
(WebSearch site:x.com, single posts resolved through api.fxtwitter.com JSON). Raw
fxtwitter payloads and extracted article bodies kept under
`watch/inbox/frontier_olm_2026-10-08/sweep/tmp/` (ftx_*.json, *_article.txt).

## Door status, stated plainly

1. WebSearch: opened 429-stormed (three parallel queries, all MCP 429 code 1302, the
   estate's known rolling-throughput envelope). Re-paced serial with 45s+ gaps: 10
   queries total, 7 clean, 3 needed re-issue. No query was fabricated as successful.
2. fxtwitter door: FLAKY UNDER BURST, fine under spacing. One burst of 9 sequential
   curls returned 404 (34-byte bodies) for 8 of 9; the same IDs resolved with 15s
   spacing, 10/10 OK on the retry round (sizes 2.1KB-107KB, code 200). vxtwitter was
   probed once as an alternate (junfan, 1.4KB) but not needed; every banked item below
   resolved through fxtwitter proper.
3. Article bodies: fxtwitter's `article` field carries FULL article content as draft-js
   blocks. This seat extracted and read four complete articles this way (PorTAL 17,053
   chars; junfan IROS 51,263; superalesha GLM merge 18,425; cyrusasg flywheel 12,922;
   plus fastino 31,973 and sergio 12,303 read for context). This overturns the 10-02
   sweep's "article endpoints DOWN" note for this seat: the share-post status resolves
   and the article rides inside it.

## Pass structure

- Pass 1 (broad): 10 queries, 44 candidate items considered (list in session log; the
  searches surfaced 9-12 candidates each). In-window (2026-09-08..10-08) subset: 15.
  Notable out-of-window items recorded so nobody re-mines: h100envy Gemma-270M phone
  loop (Jul 16; already recorded out-of-window by the 10-02 sweep with Pratyaksh
  overlap), Aleph soft-prompt (Jul 29), atlas Mnemosyne (Aug 5), fastino Nemotron
  article (Aug 14; ALREADY HELD as the 09-28 capture
  `watch/inbox/frontier_olm_20260928/sweep/_raw/nemotron35_fastino_article.md`,
  verified this sitting at lines 103/123: "QLoRA defaults (rank around 16-32...) got
  within a few points of the tuned configuration"), SergioPaniego LFM2.5-2.6B distill
  (Aug 10; LFM2.5 substance already touched by the 10-01/10-02 sweeps).
- Pass 2 (deep): 11 items fetched and read whole through the door (8 posts + 6 article
  bodies, 4 of them full-length). Only items read by this seat are banked below.

## Banked items (8, strongest first)

1. **@itsharmanjot: Edge0, a 35B model on iPhone with runtime-applied LoRA**
   (2026-09-10, https://x.com/itsharmanjot/status/2097998695157641661)
   source-fetched: 2026-10-08. Post read whole (2,132 chars, tmp/ftx_harmanjot.json).
   Quote: "LoRA adapters are applied at runtime rather than merged. One read-only base
   model can serve multiple adapter sets." Streaming MoE keeps the working set 1-2.5GB
   by memory-mapping experts on SSD with a prerouter predicting next-token routes.
   Overlap: "Edge0" = 0 hits in catalog/catalog.jsonl and watch/inbox; @itsharmanjot
   appears only in an unrelated Sep 4 Obscura intake (catalog id e5f84c719e1a) and the
   10-04 inference sweep's REJECTED Jul 8 Qwen4-Coder post. New.
   Why: Q3's transfer question answered at serving level. This is the ReFold shed
   pattern applied to adapters: read-only base + small addressable deltas applied at
   load, never merged. Steal: per-seat sampler deltas and any future LoRA deltas as
   sha-addressed unmerged overlays.

2. **Ramp Labs: PorTAL, portable task adapters (article read in full, 17,053 chars)**
   (2026-07-01, share-post https://x.com/RampLabs/status/2072381992285647280,
   article id 2072381992285647280; OUT OF 30-DAY WINDOW, disclosed)
   source-fetched: 2026-10-08. tmp/ftx_portal.json + tmp/portal_article.txt.
   Quote: "learning a task adaptation once, in a base-agnostic form, and transferring
   it to new frozen models by refitting only a small per model component."
   Numbers: refitting a thin converter recovers ~98% of LoRA's lift on unseen
   Qwen3-8B, ~94% on Gemma-3-4B; Cross-LoRA recovers only ~14%.
   Overlap: "PorTAL" and "Cross-LoRA" = 0 hits catalog/memory/watch (trajectory
   self-matches excluded). New. The companion framing article (@AkashBajwa96 "The
   Stable Era", Jul 6, read in full, tmp/akash_article.txt) adds: SOTA holds the top
   of the public leaderboard ~35 days on average, so "adaptation is perishable capex".
   Why: the strongest public argument that per-base finetuning is the WRONG asset
   class for a fleet riding fast-moving tags; portable/sampler-level adaptation
   survives base swaps. Feeds Q2 (LoRA justification) and Q4 (technique map).

3. **@cyrusasg (Decagon): A Failure-Informed Data Flywheel for Post-Training**
   (2026-09-08, https://x.com/cyrusasg/status/2097358742950207767, article read in
   full, 12,922 chars, tmp/cyrus_article.txt)
   source-fetched: 2026-10-08. Quote: "the quality ceiling is often less constricted
   by the optimizer or the architecture, but rather by the dataset." Their sampler
   law: "a dimension is only promoted into the sampler if it shows a measured accuracy
   gap across its values."
   Overlap: "Failure-Informed" catalog hit is a DIFFERENT item (FIRE 2609.26048
   runtime engineering); "decagon"/"cyrusasg" hits only in trajectory self-matches and
   an unrelated 10-04 harvest file. The 10-02 sweep ran a flywheel-themed query but
   banked tobi's 0.8B flywheel instead. New.
   Why: Q1's A/B law. The P6 marker-penalty toggle should be promoted to ON only if
   the paired duty_fuzz battery shows a measured accuracy gap across its values;
   Decagon's rule is the public version of the estate's own gate thinking.

4. **@AGTPinsights: Cua-S1-4B-0.2, frozen 4B base + LoRA + two-stage SFT-then-RL**
   (2026-09-23, https://x.com/AGTPinsights/status/2102867556193407088)
   source-fetched: 2026-10-08. Post read whole (tmp/ftx_agtp.json).
   Quote: "Training happened in two stages: supervised fine-tuning to teach the
   decision format, then agentic RL in live cua-bench-basic environments where only a
   fully completed task earns reward." Frozen Qwen3.5-4B base, LoRA adapters, RLOO on
   live computer-use tasks, 92.9% vs 60.1% on GUI-360, Apache-2.0.
   Overlap: "Cua-S1" = 0 hits catalog/watch/memory. @AGTPinsights appears in
   memory/working/decks_snapshot.json as a source handle, not this post. New.
   Why: Q2's copy-verbatim recipe IF the five-gate hardware law ever opens: cheap
   format-SFT then completion-only RL on live tasks; base stays frozen and shared.

5. **@junfanzhu98: IROS research night article (read in full, 51,263 chars)**
   (2026-09-29, https://x.com/junfanzhu98/status/2104813943394799994, article
   x.com/i/article/2104812568288120833, tmp/junfan_article.txt)
   source-fetched: 2026-10-08. Quote (article line 69): "Without pretrained Wan2.2
   weights: 4.6%. Full fine-tuning (87.4%) does not beat LoRA." (LoRA rank 32 on
   q,k,v,o + FFN reaches 89.1% on Meta-World.)
   Overlap: the 10-01 sweep held this same post as an honorable mention judging
   "snippet mismatch" from the pointer tweet alone; this pass extracted the article
   body through the fxtwitter article field and the claim IS there. Same post, new
   content, prior judgment overturned.
   Why: Q2. Pretrained structure is the scarce resource; full fine-tuning destroyed
   1.7 points vs LoRA on a 5B policy. Another "adapters over full FT" vote.

6. **@superalesha: GLM-5.3 Flash merge pilot failed (article read in full, 18,425
   chars)** (2026-09-07, https://x.com/superalesha/status/2096976602127044995,
   article x.com/i/article/2096546474255372288, tmp/glm_merge_article.txt; 1 day
   OUT OF 30-DAY WINDOW, disclosed)
   source-fetched: 2026-10-08. Quote: "We did not install a merged checkpoint across
   all routed layers after that result." The pilot: held-out relative output error
   ~0.146 for pruning alone vs ~0.449 for the aligned merge candidate; a control that
   just shrank surviving outputs beat the merge too.
   Overlap: the raw fxtwitter JSON of this exact status was fetched into the 10-01
   sweep's intake (catalog id d5399eecbf4d, 43,771 bytes) but never read or banked
   ("did not install a merged" = 0 hits repo-wide; the 10-07 quant sweep cites a
   different superalesha post from 08-20). First read here.
   Why: Q3's restore-door breakage class. Merging deltas into the base destroyed
   quality on a MoE; unmerged deltas on a read-only base (Edge0 pattern) avoid the
   entire failure mode. Adapter sheds must stay deltas, never bakes.

7. **@omarsar0 (elvis): Microsoft paper, small coding agents WITHOUT frontier
   distillation** (2026-09-09, https://x.com/omarsar0/status/2097696747338232069)
   source-fetched: 2026-10-08. Post read whole (tmp/ftx_elvis.json).
   Quote: "They show that it's possible to build competitive small coding agents
   without traditional distillation from frontier models."
   Overlap: omarsar0 hits in memory are X-citation-convention docs, not this post.
   The underlying paper was not fetched (post is the unit; paper chase OWED).
   Why: Q4. Distillation is the curriculum's most-taught adaptation technique and
   public 2026 evidence says the small-model frontier is explicitly building an
   alternative (on-policy RL + own-harness data). Any estate adaptation ask should
   price the no-distillation path first.

8. **@Aleph__Alpha: soft-prompt tuning, 80 steps, 1.5 minutes for 7B**
   (2026-07-29, https://x.com/Aleph__Alpha/status/2082471263088304149; OUT OF 30-DAY
   WINDOW, disclosed)
   source-fetched: 2026-10-08. Post read whole (tmp/ftx_aleph.json).
   Quote: "With only ~80 tuning steps (~1.5 minutes for a 7B model), soft-prompt
   tuning adapts models to benchmark formats without expensive post-training."
   Overlap: "soft-prompt tuning" = 0 hits catalog/memory/watch. New.
   Why: Q1/Q4. Prompt-tuning is the cheapest adaptation axis the curriculum teaches
   and the estate has zero instruments for; this is the public price anchor (minutes,
   not GPU-days) for format adaptation, which is exactly what the P6 logit_bias
   profile does at inference time for free.

## Research question verdicts (X-door edition)

- Q1 (marker-penalty logit_bias on gemma:2b): no in-window public X counterparty found
  (three dedicated searches; logit_bias content on X is sparse and old). Adjacent
  public evidence supports the profile's existence but demands the A/B: fastino's held
  capture (nemotron35_fastino_article.md:103) says levers that moved results were data
  and curriculum, not optimizer; my full extraction adds "Adding chain-of-thought made
  the result worse" and "one explanatory line before the structured answer cost roughly
  22 F1 points" (tmp/fastino_ft_article.txt) for executable-output tasks. Decagon's
  law (item 3) is the promotion gate. The toggle A/B itself stays OWED estate-side.
- Q2 (LoRA/PEFT under the five-gate law): nothing in-window argues for a local finetune
  pass; public consensus is frozen base + rank 16-32 adapters + data quality first,
  and two independent in-window items (Cua, junfan) show adapters matching or beating
  full FT. The five-gate law (RIB_GPU_LADDER_20261001.md:10-23 via lens/laws.md:98-99)
  stays unbroken by public evidence; if a gate opens, Cua's two-stage recipe (item 4)
  is the copy target, and PorTAL (item 2) says keep the adaptation portable.
- Q3 (ReFold transfer): transfer CONFIRMED as a pattern (Edge0: one read-only base, N
  unmerged adapter sets at runtime) and the breakage class is measured (superalesha:
  merged candidate 0.449 vs pruning-alone 0.146). Law: adapter/sampler deltas live as
  sha-addressed sheds applied at load; merging is the restore-door killer.
- Q4 (technique map vs 52,313 taught rows, lens/corpus.md:35): LoRA/PEFT (Cua, junfan,
  fastino), distillation (FTC-probe discourse, LFM2.5), soft-prompt tuning (Aleph),
  RLVR/agentic RL (Cua), portable adapters (PorTAL) all active publicly; estate
  instruments exist only for sampler profiles (P6) and shed storage (ReFold). The
  eliminate-before-frontier map for any future adaptation ask: (a) does the P6
  sampler profile cover it at zero training cost, (b) does a shed-covered delta
  cover it, (c) only then LoRA, and PorTAL's 35-day-perishable math (item 2) must be
  answered first.
- Q5 (EmbeddingGemma residency): thin. No in-window X post justifies keeping an
  embedding model resident; the closest public item (atlas/Mnemosyne, Aug 5,
  out-of-window, vendor promo) argues the OPPOSITE: 50MB local context store with
  embeddings offloaded to a remote API. GPS-embed is dead by falsifier
  (lens/burns.md:129-131); no public counter-evidence found. The residency question
  stays an estate-internal RAM-cache-law call (RIB_RAM_CACHE_STALE_SNAPSHOT_20260825
  via lens/laws.md:103-105). OWED.

## Honorable mentions, read but not banked

- @h100envy Gemma-270M phone finetune loop (Jul 16, 7,163 likes): out-of-window,
  already recorded by the 10-02 sweep with content overlap vs Pratyaksh.
- fastino Nemotron article (Aug 14): full body read this pass
  (tmp/fastino_ft_article.txt) but ALREADY HELD as the 09-28 capture
  (nemotron35_fastino_article.md, catalog id dda2a3bfa052); the held capture carries
  the rank-32 and data-quality lines (lines 103/123) though not the FinQA 14.39-64.86
  and 22-F1-point details, which this pass's extraction adds to tmp/.
- @SergioPaniego LFM2.5-2.6B RL-then-distill article (Aug 10): out-of-window; the
  RL-builds-teacher, distill-transfers pattern is the 2026 consensus pipeline.
- @atlas_cloud_ai Mnemosyne memory (Aug 5): out-of-window vendor promo; the
  local-context + remote-embedding split is the only public Q5-adjacent design found.

## OWED (not asserted)

- The P6 logit_bias toggle A/B on gemma:2b itself (estate instrument, not public).
- The Microsoft paper behind omarsar0's post (post-only read here).
- Any in-window X evidence on logit_bias marker penalties or embedding-model
  residency: searched, none found; absence is the finding.
