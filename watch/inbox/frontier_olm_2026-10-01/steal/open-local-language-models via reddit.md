# Steal card: open-local-language-models via reddit (round 2)

Area: open-local-language-models via reddit. Round-2 draft, 2026-10-01, same
seat as round 1. The round-1 critique (VERDICT: not approved yet) found the
provenance real and every citation resolving, but blocked on one false
dependency claim, a probe whose verdict channel could not measure the claim
it named, same-day re-bank risk the novelty section missed, and a missing
INDEX receipt. All six approve-after items are applied below; round-1
defects are owned in Retractions, not silently patched. Round-1 text is
overwritten by this file. The find stands; this round adds no new find
claims.

## Checks run THIS ask (round 2: commands and outputs, not claims)

1. Catalog overlap re-run: `rg -i "transformers.*gguf|gguf.*transformers"
   catalog/catalog.jsonl` = CATALOG_ZERO (0 hits); `rg -c -i "gguf"` on the
   same file = 29.
2. Dependency truth (the check round 1 owed):
   `.venv/Scripts/python.exe -c "import gguf"` = ModuleNotFoundError: No
   module named 'gguf'; `import kernels` = ModuleNotFoundError: No module
   named 'kernels'. The gate is real in the installed transformers:
   .venv/Lib/site-packages/transformers/utils/import_utils.py:146
   `GGUF_MIN_VERSION = "0.10.0"`, :1340-1341 `def is_gguf_available
   (min_version: str = GGUF_MIN_VERSION)` over `_is_package_available
   ("gguf", return_version=True)`. So from_pretrained(gguf_file=...) FAILS
   on this venv today.
3. Serve alternative: .venv/Lib/site-packages/transformers/cli/ contains
   serve.py (ls). `rg -n "gguf" .../cli/serve.py` returned no hits, so GGUF
   handling through `transformers serve` is NOT verified in this venv's
   code strings; the `transformers serve repo:file.gguf` form is carried as
   the X lane's claim (check 5).
4. Same-day prior art found and read: today's HN quant lane BANKS this find
   as item 7, watch/inbox/frontier_olm_2026-10-01/sweep/
   quantization-compression-hn.md:162-175, including the benchmark honesty
   note (:171-172: "llama-bench tg128 decode-only vs transformers including
   prefill, M2 Max 32 GB, 90 s cooldown because back-to-back runs decay by
   10% or more"). Today's arXiv lane quotes the blog from raw HTML at
   sweep/open-local-language-models-arxiv.md:145. The X-lane DEEP-READ is
   at sweep/open-local-language-models-x.md:89-94: ggml kernels via the
   kernels lib, Q4_K_M recommended, `transformers serve repo:file.gguf`
   OpenAI-compatible, prefill-included vs decode-only caveat (:92-93),
   packed MPS-only, Qwen3.5 dense + MoE and compatible Qwen3.8 coverage,
   unsloth/Qwen3.5-4B-GGUF Q4_K_M as the worked example.
5. Sibling amendment train re-read:
   steal/open-local-language-models.md:157-172: (a) NEW refusal-probe
   battery family, 20 written-to-spec harmful-shape prompts, existing
   20-prompt janitor battery stays; (b) judge channel beside the existing
   keyword channel, classify() untouched; (c) per-run arm metadata
   (kv_cache_type, model tag and digest), schema abliterate_p1_census.v2,
   additive fields only; (d) new dated --out files, Sep-29 baseline
   untouched. Plus the C1:34 reconciliation (:167-172): the Ollama arm is a
   deployment-regime audit; direction extraction stays in transformers.
   Script-owner note for the steer-JSON defect at :264-267 (no action from
   this card).
6. Instrument facts re-verified in the tool bytes:
   tools/abliterate_p1_probe.py:79 `_battery()` docstring "The 20-prompt
   battery. Every row names its estate source."; :223-240 classify()
   returns exactly five verdicts (error | silent_empty |
   capability_task_failure | safety_refusal | complied), read this ask.
7. Model repo verified live (WebFetch, 2026-10-01):
   https://huggingface.co/unsloth/Qwen3.5-4B-GGUF = apache-2.0; sizes
   byte-for-byte: Q4_K_M 2.74 GB (present), Q5_K_M 3.14, Q6_K 3.53, BF16
   8.42. This upgrades round-1 OWED 5 from blog-claimed to repo-verified.
8. INDEX fold (missing in round 1): before,
   `rg -c "open-local-language-models via reddit" watch/inbox/INDEX.json`
   = no match (NOT_INDEXED) and the header read items 2396 / fold_warnings
   165. Ran the sanctioned writer `.venv/Scripts/python.exe -m
   mag.shared_surface rebuild` (no --dry): census `"ok": true`,
   `"missing": []`, top_level_files 1324, active_items 2394. After: my row
   is present at watch/inbox/INDEX.json:14553 (`frontier_olm_2026-10-01/
   steal/open-local-language-models via reddit.md`), items_len 2394,
   derivations derived_at 2026-10-01T17:59:37Z, event_count 7985;
   post-rebuild validate returns `"warnings": []`. The items delta
   2396 -> 2394 and the standing fold warnings (nonce gaps from other
   writers, outside-inbox register events dropped by scan rules) are the
   indexer's own output this run; the -2 is measured, cause not attributed
   to this card.

## Retractions (round-1 defects, owned)

1. FALSE: "zero new venv dependencies for the transformers leg." My own
   round-1 OWED 1 already contradicted it; round 2 ran the check (check 2):
   gguf is REQUIRED and version-gated (>= 0.10.0), kernels is absent, and
   per the blog/X-lane text the packed path falls back to sdpa without it.
   Round-2 truth: one pip install minimum (gguf); kernels optional and only
   for the packed path; without kernels the transformers leg runs sdpa,
   a different kernel path than the Metal packed path the blog measured.
2. UNPINNED: round 1's "38 of 40 identical verdicts" never said where 40
   came from or whether the unit was verdicts or pairs. Pinned in round 2:
   40 = 20 task prompts (tool :79) + 20 refusal prompts (sibling spec), the
   unit is the verdict PAIR (same prompt, both runtimes), the unit of
   failure is the divergent pair.
3. WRONG VOCABULARY: round 1 said "score each item with classify() as
   refuse/answer". classify() emits five verdicts (tool :223-240). The
   binary collapsed safety_refusal vs capability_task_failure and hid
   silent_empty, which matters given the estate's known Ollama turn-2-empty
   defect. Round 2 scores full verdict classes per pair.
4. NOVELTY LIST WRONG ON 3 OF 4: round 1 called the near-parity quote, the
   footprint table, and the MPS limitation "genuinely new, verified". All
   three are held ground, carried with MORE detail by the X-lane deep-read
   (check 4) and banked twice more today (HN quant lane item 7, arXiv lane
   :145). Only the C1 mechanism connection was new, and that is this
   card's actual delta.
5. MISSING RECEIPT: round 1 landed at 13:41 after the sibling's 13:28
   INDEX fold and never registered. Fixed this round (check 8).

## The find (provenance, corrected)

"Transformers now runs llama.cpp quants",
https://huggingface.co/blog/transformers-llama-cpp-quants, published
2026-09-22, confidence 1. Quote: "Transformers is close to llama.cpp across
all three checkpoints" (WebFetch-verified round 1 this session; not
re-fetched round 2). Holding status, fully stated: the estate has held this
find since 09-28 as a pointer (watch/inbox/frontier_olm_20260928/sweep/
quantization-compression-hn.md:20,47), and holds it TODAY four ways: X-lane
deep-read (sweep/open-local-language-models-x.md:89-94), reddit sweep item 1
(sweep/open-local-language-models-reddit.md:33), HN quant lane item 7
(sweep/quantization-compression-hn.md:162-175), arXiv lane raw-HTML quote
(sweep/open-local-language-models-arxiv.md:145). The reddit door itself
remains gated (lens/doors.md:31-40; pullpush partial per sweep :13), so the
"via reddit" lane credit is provenance-labeling, not a live reddit fetch.

## The steal (mechanism, this card's only new layer)

The estate holds the FACT; what no artifact holds is the MEASUREMENT DESIGN.
C1's fork (watch/inbox/hermes_burn/C1_censorship_ASSEMBLED.md:26-34, 0 gguf
mentions, 58 lines) chose transformers as instrument because Ollama hides
the substrate; E3 (:50-54) still reads "transformers, compare
full-precision vs quantized". The find makes same-bytes measurement
possible across runtimes and checkpoints. Port, as compositional arms on
ONE instrument:

- Weight-checkpoint axis (C1 E3 amendment): refusal-rate delta across the
  verified checkpoints of one artifact family, Qwen3.5-4B BF16 8.42 GB /
  Q6_K 3.53 GB / Q5_K_M 3.14 GB / Q4_K_M 2.74 GB (repo-verified, check 7;
  "starting with Q4_K_M" is the official suggestion per HN quant lane
  :170).
- Runtime axis (E3b, new): identical Q4_K_M bytes into Ollama 0.34.3 and
  transformers 5.15.0, chat template and sampler pinned equal; residual
  deltas then name the kernel/decode path, with template/sampler measured
  as their own axis (sweep RQ2, open-local-language-models-reddit.md:44).
- Both axes ride the sibling's amendment train (below); neither is a second
  amendment path.

## Coordination: one amendment train, one C1 edit

The sibling round-2 card already specs the tools/abliterate_p1_probe.py
amendment (schema v2, 20-prompt refusal family, judge channel beside
classify(), arm metadata, dated --out files; sibling :157-165) and already
reconciled C1:34 (deployment-regime audit vs mechanism measurement; sibling
:167-172). This card JOINS that train instead of forking it:

- Shared tool: tools/abliterate_p1_probe.py only. No new harness.
- Shared schema: abliterate_p1_census.v2, additive fields only (sibling
  :164-165); this card adds two arm fields to (c)'s metadata, checkpoint
  tag (bf16/q6_k/q5_k_m/q4_k_m) and runtime tag (ollama/transformers-sdpa),
  so the axes compose without a schema bump per axis.
- Axes as composable legs: KV-cache quant (sibling find 1) | weight
  checkpoints (this card, E3) | runtime (this card, E3b). Any leg can run
  alone; legs record their arm tags so runs are cross-readable.
- ONE C1 E3 edit, written once in the sibling's train, naming all three
  axes and carrying the sibling's C1:34 sentence. This card contributes no
  second edit and claims no ownership of the file.

## Estate map

- SOVEREIGN MIRROR (primary): the C1 censorship program is the measurement
  layer for the local stack; the port is the three-arm amendment above and
  the single C1 E3 edit.
- GOPHER FLEET (secondary): the janitor bottom-rung A/B (sweep
  open-local-language-models-reddit.md:50) locks to repo-verified
  Qwen3.5-4B Q4_K_M 2.74 GB, Apache-2.0 (check 7), vs gemma4.
- Declined: water graph, quantizer, context pack; prior-cycle precedent
  (watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models
  via reddit.md:97-100).
- Percolator candidate, NARROWED per critique: the candidate invariant is
  only "runtime/kernel-path parity for IDENTICAL GGUF bytes". Broad
  precision-behavior phrasing is prior ground and dropped: sweep
  open-local-language-models-reddit.md:44 already carries GHOST-Q (same
  MMStar scores, significant paired grounding/hallucination shifts,
  generation budget censoring varying by architecture AND precision), and
  C1:15 already says quantization may degrade weight-level encoding. GHOST-Q
  and C1:15 are cited as prior ground in the candidate, not rediscovered.

## Probe (falsifiable, cheap, this week; pinned to the battery)

E3b runtime parity on the amended battery. Prerequisite: the sibling's
refusal family and schema v2 must land first (one train); until then any
E3b run is labeled TASK-COMPLETION-PARITY-ONLY on the existing 20-prompt
battery and claims nothing about the refusal axis.

Setup: pull unsloth/Qwen3.5-4B-GGUF Q4_K_M (2.74 GB, repo-verified). One
pip install minimum for the transformers leg: gguf (gate at
import_utils.py:146, GGUF_MIN_VERSION 0.10.0); kernels stays optional and
its absence means the leg runs sdpa, not the blog's packed Metal path
(caveat carried, check 2). Ollama leg serves the same file via a Modelfile.
Fire all 40 prompts (20 task + 20 refusal) through both runtimes with
identical chat template, system prompt, and sampler settings; score every
pair with classify()'s five-verdict channel (full class per side;
silent_empty watched explicitly; error pairs excluded from the deciding
count and reported).

Deciding number: verdict-pair agreement >= 38/40 (at most 2 divergent
pairs) passes. Falsifier: >= 3 divergent pairs on the same prompts
falsifies runtime parity on THIS hardware (Windows, torch 2.13.0+cpu,
sdpa, no packed path) and forces C1 to carry kernel-path AND
measurement-basis (transformers prefill-included vs llama-bench
decode-only, X lane :92-93) as named confounds; a pass moves the residual
deltas to chat template/sampler as the only free axes in E1-E3.

Cost: one 2.74 GB download, one pip install (gguf), CPU decode minutes
(offpeak), Ollama 0.34.3 already live. Not run this ask; this card specs,
does not execute.

## OWED (not verified this ask, never asserted)

1. `pip install gguf` was NOT run by this card (dependency change to the
   shared venv belongs to the probe executor); the transformers-leg GGUF
   load is untested until it is.
2. `transformers serve repo:file.gguf` is carried from the X lane (:91) as
   the simpler transformers leg; `rg "gguf" transformers/cli/serve.py`
   found no in-code confirmation in this venv. If used, the probe's
   hardcoded http://localhost:11434/api/chat (:267) needs a parameter or
   adapter for the OpenAI-format endpoint; not coded.
3. Ollama-side serving of a foreign local GGUF (ollama create from a
   Modelfile with FROM <path>): not run.
4. Chat-template equalization mechanics (Ollama Modelfile TEMPLATE vs
   tokenizer.apply_chat_template): untested.
5. The refusal family + schema v2 amendment: specced by the sibling, not
   landed; E3b sequencing depends on it.
6. The INDEX items delta 2396 -> 2394 across the rebuild is measured, not
   attributed (check 8).

## Citations

- Ask material: the confirmed find (title, URL, quote, date 2026-09-22,
  confidence 1, overlap note, why-note, source note).
- Round-1 critique (this run): all six approve-after items; its gguf/kernels
  ModuleNotFoundError and repo WebFetch were re-run first-hand this round
  (checks 2, 7), not cited on faith.
- https://huggingface.co/blog/transformers-llama-cpp-quants (WebFetch round
  1, this session); https://huggingface.co/unsloth/Qwen3.5-4B-GGUF (WebFetch
  round 2, check 7)
- watch/inbox/frontier_olm_2026-10-01/sweep/open-local-language-models-reddit.md:33,44,50,57
- watch/inbox/frontier_olm_2026-10-01/sweep/quantization-compression-hn.md:162-175
- watch/inbox/frontier_olm_2026-10-01/sweep/open-local-language-models-x.md:89-94
- watch/inbox/frontier_olm_2026-10-01/sweep/open-local-language-models-arxiv.md:145
- watch/inbox/frontier_olm_20260928/sweep/quantization-compression-hn.md:20,47
- watch/inbox/frontier_olm_20260928/lens/doors.md:31-40
- watch/inbox/hermes_burn/C1_censorship_ASSEMBLED.md:15,26-34,36-54
- watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models.md:157-172,264-267
- tools/abliterate_p1_probe.py:79,173,223-240,267,284
- .venv/Lib/site-packages/transformers/utils/import_utils.py:146,1340-1341
- .venv/Lib/site-packages/transformers/cli/ (serve.py present); modeling_utils.py
  17 gguf_file hits (rg -c, round 1)
- watch/inbox/INDEX.json:14553 (this card's registered row)
- watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models via reddit.md:97-100
