# SWEEP: open-and-local-language-models via arXiv - 2026-10-04

source-fetched: 2026-10-04

Seat: sweep-open-and-local-language-models-arxiv (workflow child). All quotes below are
verbatim from pages I fetched this sitting (curl of export.arxiv.org Atom XML, curl of
arxiv.org/html full texts, hn.algolia.com JSON, arctic-shift.photon-reddit.com JSON).
No em or en dashes in my own prose; quoted source text is normalized to ascii only where the
source used a typographic dash, and that normalization is flagged at the quote.

## Instruments run (exact commands)

- arXiv API: `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/arxiv_sweep.py` ran 20
  queries (`all:`/`ti:`/`cat:` forms, sortBy=submittedDate, sortOrder=descending, max_results=25,
  1.5s sleep between calls), batches over: openweight, opensrc_lm, small_lm, ondevice, local_llm,
  edge_llm, qwen, gemma, phi4, smollm, llama_ti, quant, specdec, moe, kvcache, testtime, arena,
  distill, slm_eff, instruct_tiny. Server totals per query (in-window variants attempted first,
  several queries returned their totals without the date filter because the date-filtered form
  was not the winning shape; per-query returned rows are the sweep census): openweight total=132,
  small_lm total=51, ondevice total=88, local_llm total=15, edge_llm total=21, qwen total=88,
  gemma total=125, quant total=17, specdec total=37, moe total=17, kvcache total=72, testtime
  total=17, arena total=84, distill total=13, slm_eff total=15, instruct_tiny total=40, smollm
  total=70, phi4 total=5, llama_ti total=0, opensrc_lm total=5. Candidate rows kept: well over 60
  distinct in-window titles across 2026-09-04..2026-10-04; the pass-1 list lives in the raw
  outputs at C:/Users/foste/AppData/Local/Temp/arxiv_sweep.py runs (logged to this session's
  stdout logs) and the strongest are named below.
- Deep reads (full HTML fetched with `curl -sL https://arxiv.org/html/<id>` then tag-stripped and
  read): 2610.02001v1 (138k chars), 2609.32042v1 (115k), 2609.34326v1 (97k), 2609.07370v1 (47k),
  2609.31540v1 (41k). Verbatim abstracts for 2610.02001, 2609.32042, 2609.07370, 2609.34326,
  2609.37887, 2609.31540, 2609.38006, 2609.15309 pulled in one id_list= call.
- HN Algolia: `search_by_date?query=...&tags=story&hitsPerPage=6` for Qwen3.5, Gemma, ollama,
  GLM-5, gpt-oss. Note: a hook stopped bare `python3`; rerun with
  `.venv/Scripts/python.exe` (AGENTS.md python-env law).
- Arctic Shift reddit substitute: `https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LocalLLaMA&limit=4&sort=desc`
  answered valid JSON first try, newest post created_utc 2026-10-04 (id 1wxgwog). The `after=7d`
  param was NOT proven (it returned the same newest post), so only the limit+sort shape is
  certified from this seat.
- Overlap: single-pass `LC_ALL=C` scans of catalog/catalog.jsonl (1,040,765 lines, 296,517,251
  bytes, read in one python pass per pattern set) and an os.walk scan of memory/ for 14+ phrases;
  per-item results in the overlap fields. A first 12-phrase loop of per-phrase `grep -c` over the
  296MB catalog was too slow and was killed; the single-pass scanner replaced it (faster
  substitute, same phrases, same data - reported as what it is).

## Door findings (RQ5, doors)

- arXiv API sortBy=submittedDate&sortOrder=descending is PROVEN from this seat via curl (doors.md
  today marked the sortBy variant UNPROVEN after a 60s WebFetch timeout; the minimal no-sortBy
  recipe stays valid). Feed clock on first probe: 2026-10-04T14:48:31Z.
- old.reddit.com/r/LocalLLaMA/top.json was NOT re-probed this sitting (no attempt made; doors.md
  verdict stands as the latest probe).
- Arctic Shift is the working reddit engine, re-certified independently by this seat's own curl
  (recipe above), consistent with frontier_olm_2026-10-04/lens/burns.md section 3 ("Arctic Shift
  archive API is the working reddit engine") and with the sibling sweep file
  open-and-local-language-models-reddit.md banked the same morning.
- Durable substitute trio for LocalLLaMA-class intel, all live this sitting: (1) Arctic Shift
  posts search, (2) HN Algolia search_by_date paging, (3) arXiv API date-sorted listing sweeps.
  The reddit door is no longer OWED.

## RQ1: what beats the janitor fleet at comparable consumer VRAM

Release intel: the Qwen3.5 family is real and multi-tier (arXiv title hits: Qwen3.5-Omni
Technical Report 2604.15804, outside the 30-day window; in-window ecosystem papers use
Qwen3.5-0.8B / 4B / 27B tiers; Mingbird's LRAB matrix drives qwen3.5:4b under Ollama). HN hits
this sitting: "Fine-tuning Qwen3.5-4B to replace Gemini Flash-Lite in a RAG pipeline"
(2026-09-29, objectID 49897103), "Moe Routing Atlas - which experts fire in Qwen3.5/3.6 35B-A3B"
(2026-09-29, 49894258; en dash in the Algolia title normalized to "-" here), "Kev: Tiny Jev-like
family of decision models built on top of Qwen3.5" (2026-09-21, 49783999, 463 points). The Qwen3.6-35B-A3B existence evidence is DUPLICATED by the
sibling lane open-and-local-language-models-hn.md (banked this sitting from objectID 49941824,
Gufo-Qwen3.6-35B-A3B-Q6dense on Strix Halo); this seat's independent hit is a second witness and
is not re-banked as an item. Estate tie-in: memory/thinking/app_reasoning.jsonl holds a tri-state
note asking whether Qwen3.6 27B and Qwen3.8 27B are plausibly real; the two HN titles plus the
Mingbird paper's qwen3.5:4b Ollama tag upgrade the Qwen3.5 half of that tri-state to attested;
Qwen3.6 remains HN-title-attested only (no arXiv surface found this sitting).

Capability shape: the strongest single public artifact is Mingbird (2610.02001, 2026-10-01): a
controlled 4-harness x 4-model x 18-task matrix (288 cells, all published) on one Windows machine
with 32GB shared memory driving gemma4:e2b, qwen3.5:4b, gemma4:12b, and ornith-1.5:35b
(35B-A3B MoE, ~3B active, ~26 tok/s at 128K context) through stock goose, opencode, agent-mini,
and Mingbird. Headline: Mingbird 0.886 overall vs 0.631 goose, 0.479 opencode, 0.405 agent-mini;
"Mingbird is the only harness without a small-model cliff (2B: 0.821 vs. 0.017 to 0.271)" (en
dash in the source normalized to "to" here) and the
frontier probe spans 0.997 to 0.478 across harnesses. Note for precision: the estate's scut tag
is gemma:2b (google/gemma-2-2b-it per configs/lora_pipeline.yaml:4) while the paper's low tier is
gemma4:e2b ("2B by Ollama tag: 5B total, 2.3B active per token", protocol section) - different
animals, do not cross-map numbers. Actionable: harness configuration, not model swap, is the
first lever for the janitor fleet; the paper's per-cell CSV (published, Apache-2.0 repo) is the
cheapest public prior for the UNMEASURED (gemma4:e2b, qwen3.5:4b) x task-class cells before any
funded probe.

## RQ2: UNMEASURED (model, tier) routing cells

The law stands: cells fill only from estate instruments with a named receipt
(RIB_MODEL_GARDEN_ROUTING.md instruments-only clause, read this sitting via
watch/inbox/frontier_olm_2026-10-04/lens/laws.md:31); no leaderboard or paper can lawfully fill a cell.
What public evidence CAN do, and did this sitting: (a) rank probe priority (Mingbird says the
harness arm of each cell is the bigger variance source, so instrument the harness config before
the model swap); (b) supply deterministic grader designs so the instrument is cheap to build
(PolAgentBench's commit-stamped trajectory grading; Touchstone's intrinsic checks; 2610.02142
"Keyword Harnesses Fail Open" warns keyword graders credit tool use that never happened - it
appeared in a sibling lane's overlap-check echo and is excluded here as likely-claimed); (c) give
routing-mechanism priors: REGEXROUTE shows 128 surface regex features match the strongest neural
encoder (76.43 pct vs 76.41 pct) and Qwen2.5 encoders 0.5B to 72B barely move routing accuracy -
relevant to mag/route_chat.py: a local, interpretable, zero-encoder router is a public-evidence
GO for building the instrument, not a substitute for measuring it. Genuinely requires a live
probe: everything that routes dollars.

## RQ3: the pending qwen A/B probe

Exact open comparison (burns.md section 3, probe ledger): "Probes ... 5 (qwen2.5:7b Q4_K_M vs
q8_0 A/B) re-owed UNRUN." New public evidence does NOT resolve it: PolAgentBench (2609.32042,
already a percolator candidate at memory/percolator/candidates.jsonl with its license erratum
already recorded in memory/runs/ds_batches/frontier_delta_items.jsonl) measures three OTHER
models (Bielik-11B, Bielik-Minitron-7B, Llama-PLLuM-8B) in Polish on agentic tool use and finds
only the 3-bit to 2-bit cliff replicates (Q8_0, Q6_K, Q5_K_M, Q4_K_M all sit on each model's
healthy plateau) while failure modes are model-specific. My additive read for the probe: expect
no collapse at either precision, so the A/B's expected delta is small and must be graded on
trajectory failure modes, not pass rate alone; and one model showed a Q4_K_M-localized dip in one
capability bucket, so single-metric reads can miss real regressions. BCC (2609.37887) adds a
second public lever: "At equal cache memory, giving keys higher precision than values yields
lower NLL and higher prediction agreement on GPT-2, Qwen2.5, and SmolLM2" - precision mix, not
just weight bits, is a live variable the probe could hold or vary. Conclusion: spend can wait or
shrink; if the operator wants the cell filled, the estate instrument is a one-family,
deterministic-grader A/B, and public evidence only scopes it.

## RQ4: free-lane forcing vs pay-funded

Nothing on the arXiv door speaks to provider rate-limit windows or token ceilings; I did not
fetch provider docs this sitting (Google AI Studio quota pages, Groq rate-limits page,
OpenRouter rate-limit headers docs are the named published sources - NOT RUN, stated as owed).
Estate-side tension stands as cited in the lens: RIB_FREE_USAGE_POLICY_20260823 (forcing free
lanes throttles them into empty 429s) vs the 2026-09-30 instrument census (459 stealth rows,
zero 429s) with the grid's CONTRADICTION marker (read this sitting via
watch/inbox/frontier_olm_2026-10-04/lens/laws.md:72).
The published data that could turn this into measured law is docs-class, not paper-class; it
needs its own fetch pass, which this arXiv door did not run.

## Already banked (do not re-confirm; found by my greps this sitting)

- 2609.07370 "Beyond Fluent Generation" = CONFIRMED FIND, watch/inbox/frontier_olm_20260928/
  register.jsonl row 15, DIGEST.md:63 and :195 already carry the 5-of-1,000 strict-parse rule.
- Touchstone 2609.31540 = CONFIRMED FIND, watch/inbox/frontier_olm_2026-09-30/register.jsonl
  row 12 (full text read at that carrier's sweep file line 61). My deep read adds only detail:
  the seven-SLM ensemble aggregates rule atoms across models with a weighted-majority retention
  rule, and the TeleQnA knowledge-only control is the stated boundary case.
- PolAgentBench 2609.32042 = percolator candidate (memory/percolator/candidates.jsonl) with the
  CC0 attribution already refuted as MIT code plus CC BY 4.0 data
  (memory/runs/ds_batches/frontier_delta_items.jsonl).
- Abstract snapshots already cataloged: 2610.02001 (state/arxiv/2026-10-02/), 2609.31540
  (state/arxiv/2026-09-28/), 2609.38006 + 2609.37887 (state/arxiv/2026-09-30/, BCC also in the
  10-03 carrier's _raw pull). None of these four carry a register row.
- KaliBench 2610.02206 and STEPQuant 2609.38169 = round-2 register rows (burns.md); Jev /
  System-1 decision-model family = banked today (git 993a5977b and the 10-04 X-card intel);
  excluded from items. The 09-30 carrier also full-text-read 2609.37902 "You Cannot Pick a
  Provider From the Price List" (43 days, 28,151 timed calls, price spread 8.8x, latency spread
  68x, per its sweep bullet at watch/inbox/frontier_olm_2026-09-30/sweep/
  open-and-local-language-models-arxiv.md:62), which is the closest estate-held prior for any
  future RQ4 provider-side measurement pass.

## Strongest new items (also returned in SweepResult, strongest first)

1. REGEXROUTE 2609.34326 (2026-09-28): 128 regex features replace neural encoders in LLM
   routing at equal accuracy. New (catalog=0, no register row; memory hits are this session's
   own command echoes in memory/trajectory/steps.jsonl).
2. Mingbird 2610.02001 (2026-10-01): harness-not-model binding constraint, measured on
   gemma4:e2b + qwen3.5:4b, 288 published cells. Abstract snapshot known; full-text findings new.
3. Elo-per-token 2609.15309 (2026-09-14): agents' marginal Elo per token falls below the
   independent-sampling reference past a measurable inflection; splitting a fixed token budget
   across sessions beats one long session (+264 Elo). Kin to the estate's cost-per-blind-point
   champion metric. New (catalog=0).
4. Behavioral Capacity Certificates 2609.37887 (2026-09-29): behavior-charging theory for
   quantized models; forward-only bit-width screen; K>V precision asymmetry result on Qwen2.5.
   Abstract snapshots known; not registered.
5. HARISSA 2609.38006 (2026-09-29): one local model, hidden-state cascade (prefill-state
   efficiency gate + answer-state safety deferral), beats FrugalGPT-class cascades at equal
   latency. Abstract snapshot known; not registered.

## Named pass-1 candidates held for the next window (not probed deeply this sitting)

2610.00954 Tokenomics of Agentic SLM Ensembles (catalog=0); 2609.19169 SiliconBench
unified-memory serving benchmark (catalog=0); 2609.18526 Illusion of Local Privacy (catalog=0);
2609.34045 Kafila heterogeneous consumer-machine serving (catalog=0); 2610.01236 Learning to
Ask SLM-LLM under a budget (catalog=0); 2609.32114 NPU hybrid-attention note naming the
"Qwen3.5 and Kimi series"; 2609.24698 tree-structured speculative decoding adapted to
DeepSeek-V4 (release signal); 2609.39437 open-weight geographic faithfulness benchmark.
