# STEAL CARD - open-and-local-language-models via reddit (2026-09-30, round 2 revision)

Round 2 of round 1, revised against the round-1 critique (verdict overreach, missing
durable probe artifact, anchor drift, seam misdescriptions, missing URLs, coverage gap).
Source marking used below: [run] = I executed it this session; [crit] = the round-2
critique's author states they ran it and reports the number; [ask] = round-1/2 ask
material (the finds, quotes, overlap claims, doors).

Doors [ask]: WebSearch `site:reddit.com` discovery + PullPush public archive API
(api.pullpush.io) deep reads; direct Reddit JSON/HTML doors blocked.

## The finds, now with URLs and first-hand door verification

1. 2026-09-27, "Qwen, where's the small stuff? (1B/2B/4B)"
   https://www.reddit.com/r/LocalLLaMA/comments/1wrez7j/qwen_wheres_the_small_stuff_1b2b4b/
   [ask] quote: "Gemma-4-12B-it is an excellent model, but a lot more memory-hungry than
   Qwen3.5-9B (mostly from its fatter K/V caches)." Named GGUF candidates + parakeet+laya
   sub-second tool-calling.
2. 2026-08-10, "Best Local LLMs - August 2026"
   https://www.reddit.com/r/LocalLLaMA/comments/1vkmhyl/best_local_llms_august_2026/
   [ask] quote: "For agentic coding, Qwen3.8 27B-MLX is the best local model I've tried
   so far: direct Ollama throughput is around 33 tok/s." Tier stacks: Gemma4-31B at
   8-32GB, Qwen3.8-27B FP8 at 32-64GB, DeepSeek-V4-Flash-0731 as agentic pick.
3. 2026-06-14, "Local models in mid-2026"
   https://www.reddit.com/r/LocalLLaMA/comments/1u5fv6n/local_models_in_mid_2026/
   [ask] quote: "It only picks up 24% of the things i've been scanning for but impressed
   considering its a very small model." Also: Q4-QAT at 165tk/s default for crawling and
   summarization; heavy quant + KV quantization breaks programming use.
4. 2026-08-09, "No wonder Qwen and Gemma are so different"
   https://www.reddit.com/r/LocalLLaMA/comments/1vjb15v/no_wonder_qwen_and_gemma_are_so_different/
   [ask] quote: "Qwen: tokenized the input to 1609 tokens Gemma: tokenized the input to
   4258 tokens." Same 330-line HTML, 2.6x context.

Door verification [run, this session]: `curl -s "https://api.pullpush.io/reddit/search/submission/?ids=<id>"`
per id (the comma-combined `ids=1wrez7j,1vkmhyl,1u5fv6n,1vjb15v` form returned HTTP 200
with EMPTY data on my fetch, so per-id is the verified form), all four HTTP 200 with one
row each and titles matching the card; created_utc values 1786372276 (2026-08-10),
1781426548 (2026-06-14), 1786233855 (2026-08-09) match the ask dates. Comment-fragment
verification (quote strings inside 53/100/34 fetched comments) is [crit], consistent
with sweep receipt `watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-reddit.md`
lines 25/34/48 [run, read via sed]. Overlap: round-1 card re-verified only find 1
(grep -c "where's the small stuff" catalog/catalog.jsonl = 0 [run, round 1]); the
critique re-ran all five greps = 0 [crit].

## Estate map (organ by organ, corrected anchors)

- **Percolator** (`mag/percolator.py:1-13` pipeline: raw signal in, noise/theater
  stripped, repeatables compiled to invariants; `mag/percolator.py:16-17` the NOVEL
  branch logs to the EXPLORE queue so it gets explored and folded): all four finds enter
  as sensing rows. Driving-ladder law: external/free lanes are SENSING only, outputs
  banked as findings, never as done/trusted work; verification climbs to the funded tier
  (`memory/rib/RIB_DRIVING_LADDER_20260928.md`, cited in AGENTS.md) - held doctrine,
  cited as constraint, not re-stolen. Bank surface verified present [run, round 1]:
  `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` (free-lane behavior schema: work_id, lane,
  model, cached_tokens, note - read this session; it is the animal_profiles free-lane
  feed, `tools/animal_profiles.py:21`).
- **Quantizer / janitor slot sizing**: `configs/lanes.yaml:6` doctrine "gemma:2b = scut;
  gemma4 = short worker bursts; specialist = judgment", pins at `:31-36` [run, round 1].
  The measured local-model facts the estate already holds live as lanes.yaml comments
  and are RE-BANKED WORK, not steal: `:28` home PC envelope RX 5600 XT ~6GB VRAM / 64GB
  RAM, `:30` "Never stack two 7B/8B models. OLLAMA_MAX_LOADED_MODELS=1 . CONTEXT=8k
  (not 65k)", `:34` "desk_orchestrator: qwen-desk:latest # 69 t/s probe winner on this
  GPU", `:69` never_local ["35b+", "70b", "full 65k context on 8B"]. Find 1's port: the
  KV/memory verdict is a CANDIDATE animal_profiles row (`tools/animal_profiles.py:24-30`
  output contract) and the genuinely new axis is quant-tier-per-task-class from find 3
  (Q4-QAT 165tk/s for crawl/summarize scut, full width for code review) plus the 24%
  honest-pickup bar. SEAM CORRECTION from round 1: this is NOT a column-add on
  `tools/model_bakeoff.py` - every lane there is a remote https endpoint (`:48-72`,
  nvidia/openrouter/groq/cerebras/deepseek/together/z.ai/nous, no local Ollama lane, no
  memory column) [run, read]. The local execution surface is the L0 janitor lane itself
  (configs/lanes.yaml) and a local probe: `tools/olm_tokenizer_probe.py`, landed this
  round (see Receipt).
- **Sovereign mirror** (`mag/ask.py:89` loads MIRROR.md as "sovereign mirror local
  load" [run, round 1]; definition at `docs/BUILD_LOG_2026-08-05_GROK_HANDOFF.md:70`
  "The durable asset is not inference; it is accumulated curriculum, the sovereign
  mirror..." [run, read this session]): find 2's community hardware-tier table files as
  a sensing map beside the mirror's local-stack notes; any rung swap it suggests must
  first survive funded-tier verification per the driving ladder, never direct-swap.
- **Gopher fleet**: find 3's CI code-review chore ports as a measured-pickup chore.
  SEAM CORRECTION from round 1: `mag/gopher_lite.py:4-6` rides ZAI_API_KEY_2, a REMOTE
  z.ai Lite pool, so it supplies the chore-shell pattern only (`:14-16`: one chore per
  tick, deterministic rotation, tiny prompts, temperature 0); the execution surface for
  a LOCAL code-review janitor is the L0 lane (configs/lanes.yaml). The 24% is the
  community's number on their diffs, never assumed ours.
- **Context pack** (`mag/context_pack.py:16` janitor is a valid pack mode [anchor
  corrected from round 1's :10, which is an import]; `:62-67` MODE_CONFIG janitor,
  `max_chars: 4800` at :67): find 4's tokenizer cost would be a janitor line item IF it
  replicated. GUARD NOTE the round-1 card missed: pack-built calls already cap at 4800
  chars, so the 580KB-truncation exposure below applies only to calls BYPASSING the
  pack - not a new hole, an unguarded doorway next to a patched one.
- **Water graph**: no direct feed from these four finds - stated as not-mapped, not
  stretched.

## Probe RUN this session (durable artifact, on the most port-ready steal)

Claim under test [find 4]: the same HTML costs ~2.6x more tokens on Gemma than Qwen.
Durable artifact landed this round (round-1's script was deleted after banking -
critique defect 2): `tools/olm_tokenizer_probe.py`, untracked in tools/, single-process
urllib, no subprocess spawns; core method: POST each model at
`http://localhost:11434/api/generate` with the sample as prompt, `num_predict: 1`, read
`prompt_eval_count` - the server tokenizer the janitor pipeline actually pays. Sample
`corpus/tmp/oni_dig/Breathability.html`, 580090 bytes [run, both rounds]; slice 8000
bytes.

Tested set [run, this session, via `./.venv/Scripts/python.exe tools/olm_tokenizer_probe.py`]:

| tokenizer | count on 8000-byte slice | note |
|---|---|---|
| gemma:2b (server) | 5139 | Gemma-2 generation, google/gemma-2-2b-it per configs/lora_pipeline.yaml:4 |
| gemma4:latest (server) | 5270 | Gemma-4 generation, 8.0B: /api/show general.parameter_count 7996157674 [run] |
| qwen2.5:3b-instruct (server) | 5470 | Qwen2.5 family BPE, GPU-warm stand-in |
| Qwen3-8B tokenizer.json (offline) | 5441 | cached snapshot b968826d..., transformers 5.15.0 in venv |

VERDICT, written to the tested set: every Gemma-family tokenizer locally testable is
CHEAPER than both locally testable Qwen tokenizers on this dense-markup slice
(gemma:2b 5139 and gemma4:latest 5270 vs Qwen3-8B 5441 and qwen2.5 5470; ratios 0.94
and 0.97). The find's 2.6x claim is falsified for every tokenizer locally testable; the
thread's exact pair (Gemma-4-12B-it vs Qwen3.5-9B) and their 330-line sample remain
UNTESTED - neither model is pulled locally, so the claim is not confirmed either.
Doctrine note softened accordingly from round 1: Reddit sensing prices the candidate,
the local bakeoff pays the truth; at n=1 on one dense-markup slice the price did not
survive contact. Caveats that stand: n=1; same-generation-does-not-prove-same-tokenizer
across generations (gemma:2b is Gemma-2, gemma4:latest is 8.0B not the thread's 12B-it,
qwen2.5/Qwen3-8B stand in for Qwen3.5-9B); the thread's own file differs.

Truncation-cap side finding, narrowed per critique: full-file runs return
prompt_eval_count exactly 4098 on BOTH families [run, round 1 and re-run this session];
`ollama --version` = 0.34.3 and /api/show gemma:2b reports gemma.context_length 8192
[run], yet the full-file count stayed 4098 with `options.num_ctx: 32768` requested
[run, twice] and still 4098 after keep_alive 0 unload and cold reload [crit]. Per-
request num_ctx cannot be trusted on this server build: full-file comparisons through
this Ollama are invalid and slice-then-extrapolate is mandatory (the probe's default
mode). Downstream flag raised by the critique, NOT run by me: `mag/lattice_loop.py:280`
passes per-request num_ctx=32768 to ChatOllama on this same server [run, line read].

## Probes NOT run (proposed, with the cheap design)

- Find 1 KV/memory claim: pull one Qwen3.5-9B GGUF, load gemma4:latest vs qwen at
  identical num_ctx, read the `ollama ps` size column. Not run: multi-GB pull [crit
  states the same].
- Find 3 code-review pickup: run a quantized janitor over N real estate diffs, measure
  pickup against the 24% claim. Not run.
- Find 2 "33 tok/s" MLX claim: MLX is Apple-silicon; this win32 x64 host cannot run it;
  falsifiable only on a Metal host or via the funded tier. Out of reach, stated as such.

## Coverage and cross-card

- Sibling card `steal/open-and-local-language-models.md` (arxiv/HN lane, landed earlier
  the same day in this directory) verified present [run, head + 3 grep lines read]; its
  organs are sovereign mirror and cold-boot admission-control, its finds are arxiv
  2609.31540/2609.37902 and the HN Clippy wave. My check of its janitor/tokenizer/sizing
  mentions shows precedent citations and a cold-boot probe, no slot-sizing mechanism
  [run]; the critique's full collision check agrees [crit]. No mechanism collision.
- Unmapped sweep reads flagged to the fold: read 3 (free-tier burn rates, 1ue95bf) and
  read 6 (Clippy echo, 1rw4fp4) are deep-read in
  `sweep/open-and-local-language-models-reddit.md:19` [run] but stolen into no card.
  Note: the sweep receipt itself already articulates the 1rw4fp4 fold at `:75`
  (tool-loop threshold, sandboxed folder grants, empty-key handling, ASR+LLM+TTS local
  tier) [run, read] - the analysis exists, no steal card carries it as a mechanism.

## Re-banked work named (not re-stolen)

Task-class profile SHAPE of find 3's port = held doctrine (configs/lanes.yaml:6 + the
:31-36 role pins). Measured local-model facts (6GB envelope, never-stack, CONTEXT=8k,
69 t/s winner) = lanes.yaml:28/30/34/69 comments. Sensing-only/driving-ladder =
constraint, cited not stolen. Find 1's KV/memory claim = candidate animal_profiles row.
The find 4 kill (with the tested-set verdict above) is this card's real contribution.

## Receipt

Durable artifact: `tools/olm_tokenizer_probe.py` (landed this round, untracked; commit
is an operator call). Every number in the table and the truncation section marked [run]
was executed this session by this seat against the local Ollama server (ollama 0.34.3)
and the repo venv (transformers 5.15.0). Numbers marked [crit] were executed by the
round-2 critique's author and are reported, not re-verified, except gemma4:latest 5270
which I re-ran and reproduced [run]. State note: my checks unloaded/reloaded gemma:2b
and loaded gemma4:latest on the local server (routine janitor churn, keep_alive
expiry); no repo files were edited beyond this card and the probe script. Em-dash
count: 0 (checked). No em-dashes anywhere in this card.
