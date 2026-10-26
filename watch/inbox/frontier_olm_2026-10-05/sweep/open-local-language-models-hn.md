# Sweep: open-local-language-models via HN (2026-10-05)

source-fetched: 2026-10-05
seat: sweep-open-local-language-models-hn (workflow subagent)
doors used: HN Algolia (search_by_date + search), HN item pages, arXiv export API,
Ollama library/blog pages, HF blog, developer blog, plus two bash probe batteries
(curl for the Reddit door, find/grep for the mine/raw shelf).

## Instruments actually run this sitting

Pass 1 (broad, 30+ candidates): six Algolia probes with
`numericFilters=created_at_i>1788552000` (30-day cutoff, epoch computed this sitting:
now=1791144000, d30=1788552000, d90=1783368000) on queries: local llm, ollama, Qwen,
"open weights", gemma, Llama model, Jev model, tool calling local model, Mistral release,
plus one 90-day probe (70B) that returned noise (substring matches, no 70B releases).
Roughly 90 listing lines, ~65 distinct candidates in the 2026-09-05..10-05 window.
Pass 2 (deep reads, fetched end to end): HN items 49953495, 49848269, 49736660,
49911995; target pages huggingface.co/blog/ggml-org/decision-models-in-llamacpp,
ollama.com/blog/ollama-now-supports-jev-style-decision-models, ollama.com/library/clef,
seangoedecke.com system-one post, developers.googleblog.com Olmo 3 7B post, and one
arXiv id_list feed (2608.29665, 2609.33446, 2609.19169). All quotes below come from
those fetches; WebFetch quotes pass through the fetch tool's extraction model, so each
carries that one step of mediation (noted per confidence).

## Answer 1: 90-day open-weight releases vs the ladder

The window's shape-changer is not one model, it is two waves.

Wave A, decision models (System One / "Jev" shape): a model family that reads input
once and emits typed probabilities (choice / noul / score) in a single forward pass
with zero output tokens. Sizes now span 144M (Julia-1, mmBERT-small, ~3 ms on one RTX
PRO 6000), 421M (Laya, ~5 ms), 4B (Kev-4B and lev, both Qwen3.5-4B base, 12-36 ms),
9B (nimble, Bespoke Labs, 91 ms per decision on an M5 Max), up to 27B (OpenJev and
Clef, both Qwen3.8-27B base, ~43 ms). Sources: ggml-org decision-models blog and
Ollama 0.35 blog, both fetched this sitting. This creates a rung BELOW the gemma:2b
scut janitor: gate, route, classify, and check work moves to sub-1B CPU-class models,
and none of it needs the remote specialist.

Wave B, frontier-class at consumer footprint: "Run Qwen 3.8 Flash Next (125B) on
consumer hardware (RTX 4090) at 100T/s" (HN 49953495, 862 points, 386 comments,
2026-10-04). Submitter: "On my machine (Nvidia 4090, 128GB DDR5, Ryzen 7950x3d) I'm
getting 124 tokens per sec." A commenter goes further: "It is at parity with 4.7 as
far as I can tell and basically where Opus 4.8 was. And I run it at home on $1500 of
GPU at 125 t/s." Countervailing evidence in the same thread: another user ran the
"exact same GGUF and vision adapter weights on llama.cpp" and got worse quality
numbers (median error 46.5 vs 154.8 through Strata), so the claim is engine-bound and
contested. If it holds under the estate's own battery, the judgment tier's "remote
specialist scarce" wall moves: a 125B near-frontier model at 24 GB VRAM + 128 GB RAM
becomes hostable.

Also in the 7B-70B class this window: Clef, a 27B decision model from Cloudflare,
"fine-tuned from Qwen3.8-27B", 18 GB download, Apache 2.0, multimodal, served from
Ollama's library (fetched page); Ai2's Olmo 3 7B, which Google reproduced end to end
on TPUs, quote: "It is a strong, modern 7B model trained at real production scale.
Ai2 exposes the complete model flow, including data, code, configurations, checkpoints,
logs, and evaluations." Listing-level (seen in Algolia lines, not deep-read):
Qwen3.6-35B-A3B-Q6dense at 190 tok/s decode on Strix Halo (49941824), a claimed
Qwen3.8-Flash-Next 177B at 11-15 tok/s on 1 RTX 5070 12 GB + 32 GB RAM (49951188),
StepFun Step 5 Preview 600B/27B MoE with open weights promised Oct 15 (49796998),
and a llama.cpp fork claiming 2-4x multiGPU speed for MoE larger than VRAM (49845314).

## Answer 2: who beats the gemma janitors on tool-call-shaped work

For gate-shaped work (the scut tier's real diet), decision models beat gemma:2b on
footprint and latency by construction: 144M-9B models answer in 3-91 ms on CPU or
Apple Silicon with structured typed output, where gemma:2b must generate tokens.
The ggml-org blog names the exact endpoints and sizes (Julia-1 144M, Laya 421M,
Kev-4B, lev 4B, OpenJev 27B, Clef 27B, all GGUF via /v1/systemone). Ollama ships it
in 0.35 with nimble 9B, tev1 4B and tev1:0.8B. The Ollaya thread (618 points) adds
the economics: "~1.5bn tokens is about $40 ... can be tested/deployed at
~$0.00003/req" and one user reports "Saves me about 75% of costs for the section its
working in." JevBench numbers from the same thread: decider-4b v2 64.13, Jev 1.13
63.29, Laya 421M 30.25.

For generative tool-call JSON at 2B-4B (the gemma4 short-worker slot), no fetched
page this sitting directly benchmarks gemma:2b or gemma4 against a named challenger.
The candidates the evidence points at: Kev-4B / lev (Qwen3.5-4B base) for structured
decisions, and Qwen3.5-4B itself as the generative base. HN listing-level support:
an HDC-based function caller ranked #2 on BFCL V4 at "$2.08 vs. Opus at $87"
(47341829, 2026-03-11) and FC-Eval, a CLI to benchmark local or cloud LLMs on
function calling (47412836). OWED: a direct gemma-vs-Qwen3.5-4B tool-call battery;
nothing banked today substitutes for it.

## Answer 3: arXiv on small local models as agent executors

The proven arXiv door answered: search `all:"local llm" AND all:agent`, sorted by
submittedDate descending, returns totalResults 48. Three reads:

- HESP (2609.33446, 2026-09-27): local LLMs as SOC alert-triage agents across five
  open-weight models (7B-72B), with controller-side stopping. Fetched feed quote:
  "HESP keeps a ledger of competing explanations, selects read-only probes by
  expected information gain per cost." Reported result: Qwen2.5-7B lifted from 0.125
  to 1.000 verified completion, Llama-3.1-8B from 0 to 0.917. The lesson: the small
  local model executes fine when a deterministic controller owns when-to-stop.
- DFT audit (2608.29665, 2026-08-30): Qwen3:4B ran an autonomous DFT pipeline under
  a "strict neurosymbolic architecture where agents propose and deterministic code
  disposes"; extractor at 95.7% precision against 201 expert judgements.
- SiliconBench (2609.19169, 2026-09-12): nine Apple Silicon serving engines graded
  on speed, memory, and fidelity for chat AND agent serving on Qwen3, Qwen3.5, and
  Gemma 4; only three stacks passed the gates. Agent-shaped serving still breaks
  engines that pass chat benchmarks.

Pattern across the freshest 15: local models are executors wrapped in deterministic
scaffolds (ledgers, verkle-style probes, code disposal); hosted-API agents appear as
the quality ceiling, local wins on cost and privacy. This validates the estate's own
janitor-first shape rather than threatening it.

## Answer 4: the Reddit door (closing the doors.md OWED)

Probed live this sitting with curl and a descriptive User-Agent
(MagResourceHarnessSweep/1.0), against r/LocalLLaMA top.json:

- https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3 -> HTTP 403, HTML block
  page ("theme-beta" shell), not JSON.
- https://oauth.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3 (no bearer) -> HTTP
  403, same HTML shell.
- https://api.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3 -> HTTP 403, same shell.
- https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3 -> HTTP 302; with -L it
  lands on HTTP 200 HTML titled "Welcome to Reddit" (the interstitial doors.md saw).
- https://gateway.reddit.com/desktopapi/v1/subreddits/LocalLLaMA -> HTTP 301; with -L
  it lands on HTTP 200 but an HTML app shell, not subreddit JSON.
- Mirror class: redlib.perennialte.ch -> HTTP 403 Cloudflare challenge ("Just a
  moment..."); redlib.catsarch.com -> TLS failure from this host (schannel
  SEC_E_UNSUPPORTED_FUNCTION), no response.
- https://www.reddit.com/r/LocalLLaMA/top/.rss -> HTTP 429 (rate limited, not JSON).

Verdict: no unauthenticated JSON recipe returns JSON from this host today. The OWED
narrows to exactly two untested recipes: (a) oauth.reddit.com WITH a real bearer from
a Reddit app id/secret (needs operator credentials), and (b) an external render
proxy. Do not cite www/oauth/api/old/gateway/redlib as working; each was probed and
failed here.

## Answer 5: mine/raw shelf vs current questions

Ran this sitting:

- `grep -c 'local_sovereign_agent/mine/raw' catalog/catalog.jsonl` -> exactly 97,865
  catalog rows (matches corpus.md's count).
- `find mine/raw -type f | wc -l` -> 103,033 files on disk (5,168 more than cataloged).
- Per-dir: agent_platform 75,279, agent_bleeding_edge 15,759, mesh_comm 5,685,
  steal_protocol 4,494, narrative_corpus 1,816.
- Staleness boundary: newest mtime 2026-09-09T23:41:33Z (disk and catalog max agree),
  oldest 2026-08-05. The shelf is a snapshot frozen at 2026-09-09: 26 days stale.

Does it answer "best local model" questions? No. The shelf is agent-framework and
infra source (zep, agentops, A2A, phoenix under agent_bleeding_edge; a large
agent_platform subtree), useful for framework-design questions as of early September.
It cannot contain the Jev wave (late Sep), Qwen3.8 Flash Next (Oct), the Step 5
teaser, or any current model leaderboard. Content probes found only old qwen3
references (arize phoenix docs). Boundary stated exactly: credible for
framework/architecture mining up to 2026-09-09; blind to everything after.

## Overlap with estate holdings (grepped this sitting)

- catalog.jsonl: "Flash Next" 0, "SiliconBench" 0, "HESP" 3 (needles near-miss, not
  the paper), "Ollaya" 1, "clef" 1, "Magnitude" 7, "decision model" 13, "Olmo" 8.
- The estate already holds a Jev concept shelf: `corpus/library/jev_steal_library/`
  (3 files: SHA256SUMS, jev-persona-eval-harness.md mapping Jev onto the
  persona-conditioning eval harness, and a consolidated bibliography). The "jev"
  needle hits catalog 144 times, mostly that shelf. Checked the bibliography for my
  banked pages: Ollaya 0, decision-models-in-llamacpp 0, ollama-now-supports-jev 0,
  clef 0, Strata 0, HESP 0, SiliconBench 0, 2608.29665 0, seangoedecke 0,
  Magnitude 0. So the estate knows the concept but holds none of today's specific
  sources.
- memory/ bounded git grep (Ollaya, Flash Next, HESP, systemone) returned only
  coincidental hits (dlb_* ai_canon chapters, one seat-memory rib file); no prior
  holding of these items.

## Secondary reads (fetched, below the top 8)

- Magnitude Launch HN (49911995, 194 points, 99 comments, 2026-09-30): a
  self-optimizing inference engine for agents; commenters measured it against local
  baselines and the baseline won: "with my 5070ti, llama.cpp seems to be about
  20-30% faster at decode" and on Mac "Decode: 175 tok/s [rapid-mlx] vs Decode:
  161 tok/s [Magnitude]". Confirms llama.cpp/Ollama as the local serving floor.
- seangoedecke.com on System One models: "a new 'System One' language model that
  only outputs decisions: the answers to a set of user-provided multiple-choice
  questions", and the pattern he suggests matches the estate's compile-then-run
  doctrine: prove a prompted task, then distil it to a small task-specific
  classifier.
- nandakishor_ml prior-art thread (49736660, 97 points, 2026-09-17): open Jev-shaped
  prior art exists (arXiv 2503.23303 from March 2025 plus 2510.01237); one commenter
  measured a local variant at "712ms P50 latency versus 0.14ms locally on intent
  routing". Zero-shot generality, not the architecture, is Jev's actual moat.

## Banked verdict for the ladder

1. Add a decision-model rung below the scut janitor: Julia-1/Laya (sub-500M, CPU,
   milliseconds) for route/gate/classify; nimble 9B or Kev-4B where a probabilitied
   gate needs more headroom. This is sensing+gate work leaving gemma:2b entirely.
2. Keep gemma4 as the generative short worker until a direct tool-call battery runs;
   Kev-4B/lev (Qwen3.5-4B base) are the named challengers. Battery is OWED.
3. The specialist wall is testable: Qwen 3.8 Flash Next 125B on RTX 4090 + 128 GB RAM
   at ~124 t/s is claimed and contested in-thread. It changes "remote specialist
   scarce" only if the estate's own battery reproduces quality through llama.cpp
   (the thread itself shows engine-dependent quality regression).
4. The Reddit door stays closed without operator Reddit app credentials; do not
   pretend otherwise (probe receipts above).
5. mine/raw stays a framework shelf with a hard 2026-09-09 boundary; model-tier
   questions need live doors (Algolia, arXiv), which both answered this sitting.

No em-dashes in this file. Every quantity above traces to a fetch or command listed
in the instruments section.
