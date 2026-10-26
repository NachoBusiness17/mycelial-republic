# Frontier sweep: open-local-language-models via x - 2026-10-05

source-fetched: 2026-10-05
seat: sweep-open-local-language-models-x (workflow subagent)
instrument: WebSearch (site:x.com queries), curl to api.fxtwitter.com / export.arxiv.org / api.pullpush.io / reddit .rss, Read on local files
dedupe: rg against catalog/catalog.jsonl + memory/ per item; sibling banks at frontier_olm_2026-10-04/sweep/* checked

## Door health (probes actually run this session)

| Door | Probe | Result |
|---|---|---|
| www.reddit.com top.json (browser UA) | curl 2026-10-05 | 403 text/html |
| api.reddit.com top.json (default UA) | curl | 403 text/html |
| oauth.reddit.com top.json (no creds) | curl | 403 text/html |
| old.reddit.com top.json (default UA) | curl | 302 (not JSON) |
| api.pullpush.io search/submission | curl x2, 25s apart | 429 application/json, body: "Rate limit exceeded. This website does not provide free scraping resources for agents." |
| **www.reddit.com/r/LocalLLaMA/top/.rss?t=month (browser UA)** | curl | **200 application/atom+xml, feed updated 2026-10-05T14:49:17+00:00** |

RQ4 ANSWER (closes `watch/inbox/frontier_olm_2026-10-05/lens/doors.md` OWED line 73): **no unauthenticated JSON recipe exists** - www, api, and oauth-noauth all 403, old 302s, and PullPush speaks JSON but 429s agent traffic by policy. The working free recipe is the **Atom RSS door**: `https://www.reddit.com/r/LocalLLaMA/top/.rss?t=month` with a browser User-Agent returns fresh structured post titles + canonical comment URLs. Not JSON; that is the honest shape of the answer. The only clean JSON path left unprobed is oauth.reddit.com WITH app credentials (never held by the estate; operator decision to register a Reddit app).

fxtwitter door: resolved 5/5 single posts this session (GoogleDeepMind, JeffDean, leopardracer article payload, ArtificialAnlys, fastinoAI) - code 200 full JSON each time.

arXiv door: re-proven with `search_query=all:"small language model" AND all:"agent"`, sortBy=submittedDate desc - 200 Atom, 8 entries, freshest 2026-10-02.

## Pass 1 census (33 candidates considered, window 2026-09-05..2026-10-05 unless noted)

X/status: GoogleDeepMind/status/2039735446628925907 Gemma 4 launch (Apr 2, context); GoogleAI/status/2039735543068504476; GoogleDeepMind/status/2039736203193241623; JeffDean/status/2062353800657342903 12B (Jun 4, context); ArtificialAnlys/status/2063059212532642193 12B WER; MichaelGannotti/article/2068712370201837908 31B DGX Spark; leopardracer/status/2043631410045452360 35B Mac Mini (Apr 13, context); startupideaspod/article/2097373018729435442 GGUF guide; AiBattle_/status/2102246552475439118 Qwen 4 at Apsara (DUP: banked by 10-04 sibling); ItsmeAjayKV/status/2102608867998007586 (DUP: 10-04 sibling deep read); AlibabaGroup/status/2104532863454712134; ivanfioravanti/status/2102247405920158103; DataChaz/status/2103059083599458543; koltregaskes/status/2102276830778773732; testingcatalog/status/2102324410468245529; fastinoAI/status/2099888422139900052 (post body is only a link to article 2099876065246416896); abacaj "200+ tok/s, 5-16x faster than Gemma 4, Qwen3.5, gpt-oss" (no status id, snippet-grade); x.com/i/article/2095551879593984390 "Open Weight Models of the Summer" (article, not resolved).
Search-summary-only, UNVERIFIABLE, NOT BANKED (no resolvable URL; exact-phrase re-search returned zero): "Qwen3.8-2.4T-A95B open weights Sep 10", "MiMo-V2.6-Pro AA score 46 Sep 22", "Muse Spark open weights coming soon", "sub-4B model scoring 53.9 across 34 benchmarks" (Sep 11 field notes).
r/LocalLLaMA month-top RSS entries (my own fetch): Ternary Bonsai 2 27B (1wj6c4l, Sep 17); DeepSeek V4-1 Flash is out (1wcbid7, Sep 10 - DUP: banked by 10-04 sibling); Qwen 4 Announced at Apsara (1wmxfjs, Sep 22 - DUP: 10-04); Friends Don't Let Friends Use Ollama (1wa26pn, Sep 7); iPhone second GPU Qwen 3.8 27B (1wvz1ex, Oct 2); Don't buy a $9K RTX 5090 (1whf7ov, Sep 15); Mozilla report "China's open-weight AI models now just 4 months behind" (in feed, unattributed URL in this pass); Anthropic GLM advertisement (1wth4iz, Sep 29).
arXiv: 2610.03213 task-tool intent matching (DUP: already cataloged today at state/arxiv/2026-10-05/2610.03213v1.txt); 2610.02858 HAD (NEW); 2610.01569 UAV swarms (considered, weaker fit); 2610.00954 tokenomics of agentic SLM ensembles (considered).

## Pass 2 deep reads (6 fetched and read end to end; minimum was 5)

1. api.fxtwitter.com/GoogleDeepMind/status/2039735446628925907 - full JSON, created Thu Apr 02 2026, 3,974,618 views. Verbatim: "Meet Gemma 4: our new family of open models you can run on your own hardware. Built for advanced reasoning and agentic workflows, we're releasing them under an Apache 2.0 license."
2. api.fxtwitter.com/JeffDean/status/2062353800657342903 - full JSON, created Thu Jun 04 2026. Verbatim: "Check out our Gemma 4 12B model: it's a super capable open weights model that can run directly on your laptop."
3. api.fxtwitter.com/ArtificialAnlys/status/2063059212532642193 - full JSON, created Sat Jun 06 2026, 461 likes. Family map verbatim: "Gemma 4 12B is the largest in the Gemma 4 family to support transcription, alongside Gemma 4 E4B and Gemma 4 E2B, with Gemma 4 31B and Gemma 4 26B A4B supporting text, image and video input only. These models are available on a variety of platforms including Hugging Face, Ollama and LMStudio." Also: 12B scores 8.8% AA-WER (#58), far from Voxtral Mini Transcribe 2 (3.6% WER, 4B params).
4. api.fxtwitter.com/leopardracer/status/2043631410045452360 - article payload read: "How my $600 Mac Mini Runs a 35B AI Model." Preview verbatim: "I moved everything to a headless Mac Mini M4, the base $599 model with 16GB of RAM. Started with smaller Qwen models for message classification and context". Apr 13 2026, 10,022,277 views, 7,713 bookmarks.
5. arxiv.org/abs/2610.02858 "Harness-Aware Distillation for Small Language Model Agents" (Choi, Moon, Nam, Lee; 2026-10-02). Verbatim: "Across multiple long-horizon agent benchmarks and models, HAD outperforms on-policy distillation baselines with the same fixed harness." No numeric results on the abs page.
6. arxiv.org/abs/2610.03213 "Toward SLM-based agentic task-tool intent matching" (2026-10-02). Verbatim (raw XML I fetched): "Conventional authorization schemes can determine whether an agent is allowed to invoke a tool, but cannot assess the agent's underlying cognition". SLMs as per-call task-tool relevance classifiers over a multi-tool dataset spanning distinct MCP servers; prompt-optimization + SFT + GRPO.

## RQ answers

- **RQ1 (releases changing the ladder shape, 7B-70B, at what VRAM):** the window's downloadable movers are Ternary Bonsai 2 (27B, <6GB, in-browser WebGPU - density outlier), DeepSeek V4-1 Flash (Sep 10, already banked by 10-04 sibling), and Qwen 3.8 27B (runs split across an iPhone + 24GB MacBook, Oct 2). Gemma 4's 26B-A4B (4B-active MoE) and 31B dense are the standing Ollama-available rungs but launched Apr 2, outside the 90d window. Qwen 4 (Max/Flash/Plus/27B) was ANNOUNCED at Apsara Sep 22 but is in-training, not downloadable - do not re-tier on it yet. The "Qwen3.8-2.4T-A95B open weights" claim could not be verified (see unbanked list).
- **RQ2 (who beats gemma:2b / gemma4 janitors at same footprint):** candidates surfaced: Ternary Bonsai 2 27B at <6GB (different weight class, same footprint envelope), Gemma 4 E4B/E2B (in-family upgrades, on Ollama), FunctionGemma 270M (banked by 10-04 sibling, not re-banked). No tool-call-shaped benchmark comparison of these vs gemma:2b was found this session - OWED a BFCL-style head-to-head on the estate's own janitor prompts.
- **RQ3 (arXiv: small local models as agent executors vs hosted):** the fresh wave (Oct 1-2) is pro-SLM-in-the-loop: 2610.02858 shows the distillation recipe that moves teacher-agent capability into small local students with the harness fixed; 2610.03213 uses SLMs as low-latency on-prem per-call tool-intent verifiers - exactly the janitor-as-oversight shape; 2610.01569 runs whole swarms on local SLMs. None of the three claims small beats hosted frontier; the pattern is small-local for volume/latency/privacy, hosted for judgment - matching the driving ladder.
- **RQ4:** answered above (RSS door).
- **RQ5 (mine/raw 97,865 rows):** NO for current questions. File mtimes span 2026-08-05 to 2026-09-09 (find -printf newest = ./agent_bleeding_edge/getzep ... 2026-09-09; oldest ./mesh_comm/permissionlesstech/bitchat ... 2026-08-05). rg -uu fixed-string counts: "gemma 4" 41 files, "gpt-oss" 173, "qwen3.8" 22, but "qwen 4" 0, "ternary bonsai" 0, "apsara" 1 (unrelated). Staleness boundary: **2026-09-09** - anything announced after that date (Qwen 4, Bonsai 2, MiMo-V2.6, the Sep 10 open-weights wave) cannot be in the corpus. Instrument note: plain rg returned 0 for even "ollama" because each cloned repo's .gitignore suppresses it; -uu is required for honest counts (control: ollama 948 files).

## Banked items (8, strongest first)

See submit_result payload. Ordering: HAD (new + actionable), AA family map (new primary), GDM launch (new primary, context-dated), Bonsai 2 (partial dup, pointer), RSS door (OWED closure), Mac Mini 35B, Friends-Ollama (janitor-stack critique lead), iPhone-GPU.

## OWED / not done

- Per-thread reads of the four Reddit primaries (1wj6c4l, 1wa26pn, 1wvz1ex, 1wcbid7): titles + URLs are verbatim from my RSS fetch, but JSON thread bodies are unreachable unauthenticated; opening them needs the oauth-credentials decision or the .rss per-comment door (unprobed).
- Tool-call head-to-head of candidate janitors vs gemma:2b on estate prompts.
- oauth.reddit.com with credentials; PullPush paid tier. Neither probed (no creds).
- "Qwen3.8-2.4T-A95B", "MiMo-V2.6 score 46", "sub-4B 53.9": stay UNVERIFIED - search summaries carried no resolvable URLs and exact-phrase re-searches returned zero.
