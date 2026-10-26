# STEAL CARD: open-and-local-language-models, arXiv/HF batch (round 2, re-homed)

**Frontier sweep:** olm 2026-10-03. Nine confirmed finds, confidence 0.95 to 1.0 (ask material). Doors, per each find's own source line: arXiv export API via curl (primary, after WebFetch 429s), HuggingFace raw card/API, HN Algolia door, GitHub releases API.
**Banking note (round 2 critique, blocker 1 fix, executed this session):** the canonical path `steal/open-and-local-language-models.md` holds the day-3 HN-door round-2 card whose byte-match row is registered at watch/inbox/frontier_olm_2026-10-03/RECEIPT.md:64 ("claimed 16240, measured 16240, match True") and whose RQ2 resolution is cited at watch/inbox/frontier_olm_2026-10-03/DIGEST.md:18. This seat's round-1 draft had overwritten those bytes; they are RESTORED from commit 2206f2354 this session (`git checkout 2206f2354 -- <path>`), the post-restore `wc -c` reads 16240 bytes matching the registered row at watch/inbox/frontier_olm_2026-10-03/RECEIPT.md:64, and the restored working-tree header is the round-2 card header (`head -1`, verified this session). This card is re-homed here under the sibling-convention name. Residual state, reported not fixed: a sibling commit a7ca49be1 swept the stray round-1 bytes into HEAD (`git show HEAD:<path> | wc -c` reads 20151), so the restored 16,240 bytes sit staged in the index and repair the receipt chain on the next commit of this tree; this seat does not commit on its own.
**Provenance tiers:** [PRIMARY] = this seat read or fetched the bytes this session. [FIND] = the detail lives in the ask's confirmed find and was not re-verified by this seat. [RE-BANK] = the substance was already banked estate-side; only the organ mapping or corroboration is new.
**Laws held:** no fabrication (OWED section), no em-dashes, no en-dashes, citations as path:line or URL.

## The steal (the mechanism)

For open and local models the estate's levers are now measured, not vendor-claimed, and the measured order is: task-matched adaptation first, verifiable rewards second, parameter count last.

1. [PRIMARY] In-distribution tool-calling capability is bought with LoRA-SFT, not RL: "SFT with LoRA is the strongest in-distribution method throughout the 0.6B-32B range and best in 15 out of 18 experimental settings", GRPO wins 29 out of 54 cross-dataset settings but its margin over SFT averages under one point, and LoRA outperforms full-parameter fine-tuning at preserving pretrained agentic behavior (state/arxiv/2026-09-17/2609.17848v1.txt:6).
2. [PRIMARY] Without verifiable rewards, open-weight CLI tool use sits far below its cards: "no open-weight model exceeds 42% exact-command accuracy in the unrestricted setting" across 8,504 query-command pairs on 1,642 Kali tools, while SFT+RLVR on an 8B reaches performance comparable to a 685B MoE; deterministic canonicalization plus alias-aware evaluation is what makes the reward runtime-free (state/arxiv/2026-10-02/2610.02206v1.txt:6).
3. [PRIMARY] One epoch of GSPO on a rank-32 LoRA over 1,700 tasks transfers (SWE-Bench Pro 60.1 to 64.8, Terminal-Bench 2.1 67.4 to 82.0); the "One epoch" phrasing was re-verified case-insensitively in the fetched abstract this round after round 1's case-sensitive grep missed the capital O (watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_arxiv4.xml).
4. [PRIMARY] Context is a measured liability, and the diagnostic's own example is the estate's janitor workload ("An agent reconciling a long ledger ... must repeatedly read its state, update the correct record"): seven open-weight models lose 62.8% scaling context 4-128K, 36.5% under input-format variation, 39.9% under local task complexity (same XML, abstract read this session).
5. [PRIMARY, live, corroboration of banked ground] The serving gap is versioned and cheap: the estate daemon runs 0.34.3 (`ollama --version` run live; the same version string sits in memory/percolator/candidates.jsonl:10) while upstream v0.35.1 ships /v1/systemone, Clef, CAPABILITY declarations and the web-search cap raise; this seat's independent fetch of the release JSON corroborates what the sibling HN lane already banked (tag_name "v0.35.1", systemone x2, Clef x5, CAPABILITY x1, "web search" x1, saved at watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_ollama351.json).
6. [PRIMARY, live, corroboration of banked ground] The candidate pool compounds weekly: the Featherless roster reads total_items 51112 with 44 rows in the newest 100 carrying the Gensyn name (watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/featherless_roster_100.json; greps run this session and in round 1), no rate-limit header in the saved response (watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/featherless_headers.txt), and the +471 arithmetic is now firsthand: total_items 50641 is read directly at watch/inbox/BURN_free-resource-landscape_20260928_g.md:9.

**One-sentence mechanism:** grade small local models on canonicalized, verifiable command-shaped tasks (the KaliBench grading shape), adapt them LoRA-SFT-first with short GSPO/RLVR second, size context budgets to the measured context cliff, feed candidates through the owed Ollama 0.35 upgrade and the roster-diff lane, accumulate the scores in the verdict ledger, and never swap a janitor on a self-reported card score.

## Nine finds mapped onto estate organs

### Find 1: LoRA-SFT is the in-distribution tool-calling default (arXiv 2609.17848) -> model-gates rib + worker finetune lane + percolator

- Primary text verified (sweep-saved stub read whole, 1278 bytes per catalog/catalog.jsonl:444218): the 15-of-18, under-one-point, and LoRA-beats-full-FT results quoted above.
- **Organ:** memory/rib/RIB_MODEL_GATES_20261001.md:1-11 holds the doctrine "Every animal below gets its OWN harness". This find adds the per-SIZE adaptation row: for tool-calling animals, LoRA-SFT is the default adaptation and RL is bought only against a measured transfer claim.
- **Port move:** file that row in the gates rib; when any finetune lane opens, it targets the worker-class animals pinned at mag/lanes.py:44-48 (worker and biographer on gemma4:latest) before the clerk/router gemma:2b tier. Compile through the percolator's REPEAT-to-INVARIANT path (mag/percolator.py:14-17).
- Inherited falsifier: any setting where GRPO beats LoRA-SFT in-distribution by more than the under-one-point margin.

### Find 2: KaliBench runtime-free verifiable rewards (arXiv 2610.02206) -> gopher fleet grading + verdict ledger + policy gate

- Primary text verified (sweep-saved stub read whole, 2069 bytes per catalog/catalog.jsonl:870471): the 42% ceiling, the 8,504 pairs, the 1,642 tools, and the 8B-matches-685B result; the pipeline is "deterministic canonicalization and alias-aware evaluation" with "runtime-free verifiable rewards".
- **Organ (amended per round 2 critique, fix 4):** the probe's and grader's scores have an existing ledger this card under-named in round 1: tools/gps_mcp/ledger.py:270 `record_verdict` keeps a per-(model_id, task_shape) running pass-rate ("new_rate = (old_rate * n + v) / (n + 1)", never overwriting history) with the evidence-resolution gate at tools/gps_mcp/ledger.py:291 (evidence_hash never stored on trust; evidence_path or evidence_bytes required). Route the probe results and every Find 2 grader score there; mag/policy_engine.py:6-14 gate 2 (capability grant) then READS the ledger instead of collecting its own counts.
- **Port move:** canonicalize-then-exact-match grader as a runtime-free scorer inside the janitor loop; scores land in record_verdict keyed by model and task shape; capability rows in the policy engine cite ledger aggregates.
- Honesty note: the benchmark's domain is Kali security tooling. This port transfers the GRADING SHAPE, not the security domain; domain transfer is exactly what the probe below tests.

### Find 3: ActionGuard fail-closed tool authorization (arXiv 2609.39450) -> policy engine + effect broker (the authorize seam)

- Verified in the fetched abstract (watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_arxiv4.xml): the title, "fail-closed", "before-tool-call", "ALLOW", ASR/TSR, "139 contextual and 180 obvious injections in a SKILL-INJECT-based setting", and, promoted from [FIND] to [PRIMARY] this round, "three open-source and two commercial Reviewer models. Each condition is repeated three times".
- **Organ:** the estate's own model-proposes/switchboard-authorizes pattern measured on OpenClaw's before-tool-call stage. The estate seam is mag/effect_broker.py:1-11 (reference-monitor pattern enforcing authority status, granted capabilities, and policy validation) plus mag/policy_engine.py:16-19 (require_confirmation effects return DEFERRED and queue to the operator inbox rather than auto-granting, already fail-closed in spirit).
- **Port move:** (a) reviewer context separated from skill text, so a poisoned skill document never carries the authorization decision context; (b) explicit fail-closed DENY at the before-tool-call stage with the verdict banked in the broker's receipt chain (mag/effect_broker.py:10-11).

### Find 4: Long-Transduction context liability (arXiv 2609.38712) -> context budgets for the janitor lanes

- All three numbers verified in the fetched abstract (same XML): the 62.8% context-length drop over 4-128K, 36.5% under input-format variation, 39.9% under local task complexity, across seven open-weight models.
- **Organ:** the janitor and worker lanes run exactly this workload class (ledger reconciliation, repeated state reads and record updates). Context budget today is implicit in the pins: mag/ollama_policy.py:16-18 keeps gemma:2b and the desk models resident under the 6GB cap declared at mag/ollama_policy.py:1.
- **Port move:** (a) chunk long transduction jobs so no single generation spans the measured cliff; (b) format-normalize inputs before dispatch, since the 36.5% axis is free to fix; (c) bank the three numbers as context-budget priors in the model-gates rib next to the Find 1 row.

### Find 5: GSPO rank-32 LoRA transfer template (arXiv 2610.00890) -> quantizer replication template

- Verified in the fetched abstract (same XML): "One epoch of GSPO" (case-insensitive grep count 1 this round), rank-32, 1,700 tasks, 60.1 to 64.8, 67.4 to 82.0. [FIND] remains only the six-benchmarks-plus-two-unseen-harnesses framing beyond the abstract's list.
- **Organ:** the weights side of the quantizer organ is thin: mag/auto_quantize.py:1-24 is analytics-resolution only (L0-L5 storage levels, "LAW: Anomalies are NEVER quantized"), and the existing weight-quant surface is tools/llamacpp/llama-quantize.exe (tracked) plus mag/gguf_cartography.py (exists; contents unread).
- **Port move:** copy the grading template, not the training run: hidden fail-to-pass plus pass-to-pass task grading with held-out harnesses is how a local replication (the deliberate-ask quantize target line in AGENTS.md) should prove transfer, and it reuses the Find 2 grader and the record_verdict ledger.

### Find 6: MoE-CORE expert offloading (arXiv 2610.01950) -> quantizer serving intel, NOT a port today

- Verified in the fetched abstract (same XML): TPOT 38.0-44.8 ms versus 1268.9-1269.1 ms for the vLLM Prefetch configuration on DeepSeek-V4-Flash-W4A8 (and 206.6-220.5 vs 5941.5-5941.8 ms on GLM-5.2-W4A8C8), 21.5 ms under the 84-GB NPU cap with approximate expert substitution and MTP at depth 2.
- **Caveat (amended per round 2 critique, fix 7):** the abstract states the comparison itself is not apples-to-apples: "The main comparison uses 1K- and 128-token output caps for MoE-CORE and vLLM Prefetch, respectively". The headline spread is directionally useful and numerically incomparable; do not quote the ratio as a speedup.
- **Organ:** quantizer serving intel only. mag/ollama_policy.py:1 declares "one-hot GPU on 6GB AMD (RX 5600 XT)"; the paper's appliance class is a different world. Bank as genre intel (coordinated expert residency); spend no build this window.

### Find 7: MiniCPM5-2B janitor swap candidate (OpenBMB) -> janitor lane, WITH prior art attached

- Live-verified via the HF API (saved at watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_minicpm5.json): id openbmb/MiniCPM5-2B, createdAt 2026-09-06, lastModified 2026-09-29, license apache-2.0, tags tool-calling and on-device, safetensors 2516756480 BF16 parameters, pipeline_tag text-generation. [FIND]: the self-reported avg 53.9 card table and the SGLang backend naming (absent from the API payload).
- **Prior art (amended per round 2 critique, fix 3; this is a re-banked candidate, not a fresh discovery):** the estate swept MiniCPM5-2B on 2026-09-11, twice the same day: watch/inbox/STEAL_FOLD_RESEARCH_PIPELINE_20260911.md:67-70 (second drop; "the 2GB edge rig claim stays UNPROVEN until our bench") and :104-107 (official OpenBMB drop; "The P3 edge-rig candidate firms"). The standing gate is banked at memory/runs/gapwave/_owed_live_all.json:936 and memory/runs/mickey17/digest_inbox_09.jsonl:19 ("MiniCPM5 2GB edge-rig claim ... stay UNPROVEN"), and the model is already pinned in the SemIf decision-oracle ladder at memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:34 and :260 (Qwen3-0.6B / MiniCPM5-2B / Qwen3.5-4B reading typed option probabilities). The swap A/B below inherits the UNPROVEN gate: it closes an open estate debt, it does not open one.
- **Organ:** the janitor slot is pinned at mag/ollama_policy.py:16 (MAG_JANITOR_MODEL, default gemma:2b).
- **Port move (loadability-corrected per critique fix 6):** candidate intake only, and not yet runnable as stated in round 1: the official repo serves safetensors BF16 with no gguf tag in the payload; the payload's only gguf hit is a community derivative name in its sibling list (localellm/WebGPU-minicpm5-2b-i1-gguf, unvetted, WebGPU-targeted). Before any A/B: either vet that derivative's provenance or convert safetensors-to-GGUF, AND verify ollama 0.34.3 architecture support for the MiniCPM5 family. The swap decision then consumes a record_verdict score, never the card table.

### Find 8: Ollama v0.35.0/v0.35.1 -> janitor host upgrade + decision-endpoint lane [RE-BANK, execute-nudge]

- **Re-bank labeling (per round 2 critique):** roughly 90 percent of this find is already banked: the percolator candidate memory/percolator/candidates.jsonl:10 (filed 2026-10-02) holds /v1/systemone, the pin sites (mag/ollama_policy.py:16,18; mag/lanes.py:45,48) and the post-upgrade tev1:0.8b probe; the debt is named at watch/inbox/frontier_olm_2026-10-03/lens/burns.md:202-203; and the sibling HN lane banked the release-notes verification the same night, including v0.35.1's Clef 27B + Clef Flash 9B, the web-search 3-to-10 raise, CAPABILITY declarations and the output_tokens: 1 release-note example (watch/inbox/frontier_olm_2026-10-03/sweep/open-and-local-language-models-hn.md:93, also :99). This seat's independent fetch (watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_ollama351.json, tag_name v0.35.1) is corroboration, not news.
- **New here:** only the organ map and the nudge: execute the filed candidate's probe (quiet-window upgrade on the shared janitor host, then one batched CHOICE/SCORE/NOUL POST against tev1:0.8b per the candidate row's own probe). [FIND] guard stays: the release notes name no change to the ordinary generate path the gemma janitors ride; the generate-path A/B remains owed.

### Find 9: Featherless roster live interval -> percolator roster-diff intake [RE-BANK, mapping-new]

- **Re-bank labeling:** the sibling HN lane fired the identical interval live the same night and banked every fact this find carries: total_items 51112 vs the 09-28 receipt's 50641, +471 in 5 days, 44/100 newest rows Gensyn-Swarm 0.5-0.6B fine-tunes, falsifier untriggered, no rate-limit headers (watch/inbox/frontier_olm_2026-10-03/sweep/open-and-local-language-models-hn.md:89, also :101). This card's roster greps and header read (watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/featherless_roster_100.json, featherless_headers.txt) independently corroborate, and the 50641 base is now firsthand here (watch/inbox/BURN_free-resource-landscape_20260928_g.md:9).
- **New here:** the organ mapping only: percolator roster-diff intake feeds candidate names toward the Find 2 grader and the Find 7 swap path; the lane stays recon-only. Pre-registered falsifier (from the find and the 09-27 instrument line): roster delta falls to zero or the endpoint starts requiring a key, and the lane closes.

## The probe (one falsifiable, $0, this week; statistics corrected per round 2 critique, fix 5)

**KaliBench-shape janitor grading run.** Harvest (goal, exact shell command) pairs from this seat's own documented session work (the Checks section is a seed set; the live journal is memory/trajectory/steps.jsonl). Canonicalize both sides with a deterministic alias-aware matcher (lowercase, whitespace and flag-order insensitive; the grading shape at state/arxiv/2026-10-02/2610.02206v1.txt:6). Score gemma:2b (mag/ollama_policy.py:16) and gemma4:latest (mag/lanes.py:45) via /api/generate at temperature 0. Minimum n is 30 with a difficulty control (at least 10 pairs rephrased into unfamiliar phrasing or drawn from an unworked domain, to price the self-harvest bias: the slice is easy and training-adjacent by construction).

**Statistics, honest (round 1 overclaim retracted):** round 1 said "either outcome is decision-grade" at n=30; that does not hold. The 95 percent binomial half-width at n=30 and p=0.42 is 1.96 times sqrt(0.42 x 0.58 / 30), about 18 percentage points, so a point estimate alone decides nothing. Decision rules, all requiring Wilson intervals in the result: branch (a), retiring the 42% ceiling as a routing prior, fires only when the interval's LOWER bound clears 42%, which at n=30 needs an observed score of roughly 60% or better; branch (b), adopting the verifier as the garden capability gate, fires when the interval's UPPER bound sits below 42%, which at n=30 needs roughly 25% or below; anything between is UNDECIDED and the run raises n (at n=100 the half-width at p=0.5 is about 10 points) or banks UNDECIDED as the outcome.

**Routing:** every verdict goes to tools/gps_mcp/ledger.py:270 record_verdict keyed (model_id, task_shape) with the evidence-resolution gate at :291, so repeats accumulate a running pass-rate instead of overwriting; policy_engine gate 2 reads the aggregates.

**Cost:** zero spend, zero downloads beyond nothing (all models resident), one afternoon, local daemon only. Not run yet: this is a proposal, not a banked result.

## OWED (claimed by nobody)

- MiniCPM5-2B third-party score run: the avg 53.9 table is self-reported [FIND]; the estate's own 09-11 UNPROVEN gate (memory/runs/gapwave/_owed_live_all.json:936) remains open until a bench lands.
- MiniCPM5-2B loadability: safetensors-to-GGUF conversion or vetting of the community localellm/WebGPU-minicpm5-2b-i1-gguf derivative, plus an ollama 0.34.3 architecture-support check for the family, before any A/B is runnable (round 2 critique fix 6; verified against the HF payload this session).
- Ollama 0.35 generate-path A/B: open debt at watch/inbox/frontier_olm_2026-10-03/lens/burns.md:202-203; not executed.
- KaliBench per-mode and per-configuration breakdowns beyond the abstract: abstract page not pulled; the stub is abstract-level.
- mag/gguf_cartography.py contents: existence verified; contents unread.
- Featherless rate limit: unmeasured; the header dump proves absence on one response only.
- The probe itself: not run (proposal). The pytest suite: not run; the ask names no test check.
- The receipt-chain repair: the restored 16,240-byte round-2 card sits STAGED at the canonical path; HEAD (a7ca49be1) still carries the stray 20,151-byte round-1 content there until the tree's next commit. This seat does not commit.

## Checks run this session (exact commands; round 2)

- `git show 2206f2354:watch/inbox/frontier_olm_2026-10-03/steal/open-and-local-language-models.md | wc -c` -> 16240, matching RECEIPT.md:64.
- `git checkout 2206f2354 -- watch/inbox/frontier_olm_2026-10-03/steal/open-and-local-language-models.md` then `git status --short -- <path>` -> "M " (staged) and `wc -c` -> 16240, matching the registered row at watch/inbox/frontier_olm_2026-10-03/RECEIPT.md:64, and `head -1` -> the round-2 card header.
- `git show HEAD:<path> | wc -c` -> 20151 and `git log --oneline -3 -- <path>` -> a7ca49be1 is the commit that swept the round-1 overwrite into HEAD.
- `grep -ioc "one epoch" sweep/tmp/hnolm/stealr1_arxiv4.xml` -> 1 (promotion to PRIMARY; round 1's case-sensitive grep missed the capital O).
- `grep -o "three open-source[^<]\{0,80\}" ...` -> "three open-source and two commercial Reviewer models. Each condition is repeated three times and" (promotion to PRIMARY).
- MoE-CORE abstract extraction -> the 1K-vs-128-token output-cap sentence verbatim (caveat added).
- `grep -c gguf stealr1_minicpm5.json` -> 1, and its context is the community derivative name inside the sibling list (loadability OWED shaped accordingly); `grep -o "pipeline_tag[^,}]*"` -> text-generation.
- Reads this round of every newly cited line: RECEIPT.md:64, DIGEST.md:18, STEAL_FOLD_RESEARCH_PIPELINE_20260911.md:67-70 and :104-107, memory/runs/gapwave/_owed_live_all.json:936, memory/runs/mickey17/digest_inbox_09.jsonl:19, memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:34 and :260, tools/gps_mcp/ledger.py:270-295, sweep/open-and-local-language-models-hn.md:89-101, watch/inbox/BURN_free-resource-landscape_20260928_g.md:9.
- Round 1's fetch checks stand with artifacts on disk: the two stub reads (state/arxiv/2026-09-17/2609.17848v1.txt, state/arxiv/2026-10-02/2610.02206v1.txt), the batch arXiv curl (HTTP 200, saved as stealr1_arxiv4.xml), the HF API curl (307 then 200, stealr1_minicpm5.json), the GitHub release curl (HTTP 200, stealr1_ollama351.json), the roster greps on watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/featherless_roster_100.json (total_items 51112; 44 Gensyn occurrences), `ollama --version` -> 0.34.3.
- Final law checks on THIS card, run after writing: em-dash grep, en-dash grep, byte count, and `citation_lint check --files` on this file; results stated in the submission and mirrored in the JSON.

## Grounding (read or fetched this session)

- state/arxiv/2026-09-17/2609.17848v1.txt:6 and state/arxiv/2026-10-02/2610.02206v1.txt:6 (both stubs read whole).
- watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_arxiv4.xml (ActionGuard fail-closed/before-tool-call/ALLOW/139/180/three-open-source-two-commercial; Long-Transduction seven models 62.8/36.5/39.9 plus the long-ledger example; GSPO One epoch/rank-32/1,700/60.1/64.8/67.4/82.0; MoE-CORE TPOT rows plus the 1K-vs-128-token cap sentence).
- watch/inbox/frontier_olm_2026-10-03/sweep/tmp/hnolm/stealr1_ollama351.json and stealr1_minicpm5.json and featherless_roster_100.json and featherless_headers.txt (fetched artifacts, greps named above).
- catalog/catalog.jsonl:444218 and catalog/catalog.jsonl:870471 (catalog stubs, byte sizes 1278/2069).
- watch/inbox/frontier_olm_2026-10-03/RECEIPT.md:64 (byte-match row for the canonical card) and watch/inbox/frontier_olm_2026-10-03/DIGEST.md:18 (RQ2 citation of the canonical card).
- watch/inbox/STEAL_FOLD_RESEARCH_PIPELINE_20260911.md:67-70 and :104-107 (MiniCPM5-2B prior sweeps); memory/runs/gapwave/_owed_live_all.json:936 and memory/runs/mickey17/digest_inbox_09.jsonl:19 (UNPROVEN gate); memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:34 and :260 (SemIf ladder pin).
- tools/gps_mcp/ledger.py:270-295 (record_verdict, running pass-rate, evidence-resolution gate).
- watch/inbox/frontier_olm_2026-10-03/sweep/open-and-local-language-models-hn.md:89, 93, 99, 101 (sibling lane's same-night live fires for finds 8 and 9).
- watch/inbox/BURN_free-resource-landscape_20260928_g.md:9 (total_items 50641, total_pages 507).
- memory/percolator/candidates.jsonl:10 (Ollama 0.35 candidate row) and watch/inbox/frontier_olm_2026-10-03/lens/burns.md:202-203 (upgrade debt).
- memory/rib/RIB_MODEL_GATES_20261001.md:1-11 (per-animal harness doctrine).
- mag/policy_engine.py:6-14, :16-19; mag/effect_broker.py:1-11; mag/ollama_policy.py:1, :16-18; mag/lanes.py:44-48; mag/percolator.py:14-17; mag/auto_quantize.py:1-24 (all read).
- mag/gguf_cartography.py, tools/llamacpp/llama-quantize.exe, memory/trajectory/steps.jsonl (existence verified; contents unread).
- AGENTS.md (deliberate-ask quantize target; model-proposes/switchboard-authorizes boundary; python env law).

Finds 1 through 9 are ask-provided confirmed finds cited to their URLs in place; every [FIND] tag marks a detail this seat did not re-verify; every [RE-BANK] tag marks banked estate ground named above. Everything [PRIMARY] was read or fetched in this session by this seat.
