# FRONTIER SWEEP: finetuning-adaptation via X door, 2026-10-09

source-fetched: 2026-10-09. Area: finetuning-adaptation via x. Seat: sweep-finetuning-adaptation-x (dynamic workflow child).

## What this sweep feeds

Model garden (gemma:2b scut + gemma4 short worker janitors), the skills_pack case-law magnet (LENS 3: 287 case_law edges mapped to one module, figure given by the ask), the skill ledger, and the local-first consent boundary (LENS 2). All four research questions answered below from items I fetched and read through the fxtwitter door this session.

## Door health (X door)

- fxtwitter single-status door: 10/10 fetches returned HTTP 200 JSON, including three X long-form articles delivered inside the status JSON (article.content.blocks). Tested with: curl -s https://api.fxtwitter.com/<user>/status/<id>
- The bare article path form 404s: api.fxtwitter.com/i/article/2100640525418115369 returned {"code":404,"message":"Not found"}. Resolution requires the author's status URL that carries the article. This extends the known "fxtwitter timelines 404" negative rows from commit f676ee787: timelines and bare article paths are both dead, single statuses are alive.
- WebSearch backend (Z.ai web_search_prime): the tool's allowed_domains filter was NOT honored by the backend (first two queries returned unsloth.ai/reddit/medium hits); site:x.com inside the query text is what works. 5 of about 12 queries surfaced a transient 1302 rate-limit line and recovered on the auto-retry. Two early parallel queries timed out at 60s.
- The x.com search index skews old: most indexed hits are 2023-2025. Recency was enforced by snowflake-decoding every status ID (id>>22 + 1288834974657 ms, decoded with the repo venv python this session). Every in-window claim below carries a decoded or JSON-stated date.

## Pass 1 census (broad sweep)

11 searches, about 39 candidate items considered, of which 23 carry date evidence inside the window 2026-09-09..2026-10-09; 16 others are older (2024 to mid-2026) and were considered then excluded from banking. In-window census (date = snowflake decode or JSON created_at):

1. 2026-09-11 BrianRoemmele NASA open weights + fine-tuning code (weak fit, census only)
2. 2026-09-17 UnslothAI Docker: train+run 500+ models locally (BANKED #6)
3. 2026-09-17 ElyHahami "On Continual Learning: Can an LLM Know a Life?" (BANKED #1)
4. 2026-09-17 SHOW_ROBOTICS LoRA adapters on robot episodes (profile snippet only, no status ID resolvable through the door; unresolvable, not banked)
5. 2026-09-17 CJ Zafir: Mac-local fine-tune designed by Codex (snippet only, not deep-read)
6. 2026-09-22 jvr0x "How fine-tuning actually works, explained by a 4B pirate" (BANKED #3)
7. 2026-09-23 hrswatigupta "Jev Is Turning Into an Entire Ecosystem" (BANKED #4)
8. 2026-09-23 MichaelGannotti reshare of the pirate article (census only)
9. 2026-09-25 theneurondaily "AI Chips Are Going to Space" (Fastino hosted fine-tuning launch; census only)
10. 2026-09-27 imohitmayank GLiNER2.5-Decide fine-tuned (BANKED #2)
11. 2026-09-30 Canonical Kubeflow+Feast fine-tuning workflow (profile snippet only)
12. 2026-09-30 theneurondaily "GPT-6 Crossed Its Limits & NVIDIA Built a Watchdog" (read; passages banked in this file, JSON slot taken)
13. 2026-10-01 svpino fine-tuned Qwen3 4B beats frontier claim (fetched; NOT JSON-banked: the results live in a video I could not read, so the claim is unverifiable by me)
14. 2026-10-01 DivyanshT91162 pretraining/fine-tune/quantize tool thread (census only)
15. 2026-10-02 riteshpatel1884 "Day 41" study notes (census only)
16. 2026-10-02 StatsPapers ChainLoRA (BANKED #5)
17. 2026-10-03 TheVixhal RL fine-tuning platform (census only)
18. 2026-10-04 0xMovez Unsloth slow-inference cause/fix (census only)
19. 2026-10-05 GithubProjects Gemma multimodal LoRA tuner (fetched; file only, JSON slot cut)
20. 2026-10-05 BrianRoemmele Strata / Unsloth 96GB builds (census only)
21. 2026-10-08 rohanpaul_ai Opus 5 / SWE-bench thread (census only)
22. 2026-10-08 MichaelGannotti "The Digital Daily" No. 009 (BANKED #8)
23. 2026-10-09 HEI U-LoRA conditioned gating, ICML 2026 (BANKED #7)

## Pass 2 deep reads (fetched and read through fxtwitter this session)

Full end-to-end reads: ElyHahami article (7,704 chars, all), Gannotti Digital Daily (7,372 chars, all), GLiNER2.5-Decide article (9,478 chars, all), plus the complete text of 5 short posts (UnslothAI Docker, svpino, ChainLoRA thread, GithubProjects, HEI). Extensive partial reads: hrswatigupta article (intro + clone table + all LoRA/Kev/MacBook passages of 23,441 chars), jvr0x article (first 5,200 of 18,280 chars: setup, method, distillation lessons), theneurondaily article (targeted LoRA/Unsloth/adapter passages from 99,989 chars). Every banked quote below is verbatim from those fetches, except where a dash normalization is noted.

## Research question answers

**Q1: consumer-GPU LoRA/PEFT results since 10-01 that keep us inside T0/T1 (LENS 2 consent)?**
Yes, the boundary holds and the recipes are now minutes-scale and all-local:
- GLiNER2.5-Decide (Sep 27, full read): LoRA r=8, alpha=16, dropout 0.05, 3 epochs, batch 4, 1,500 rows, encoder lr 1e-5 / task-head lr 5e-4, adapter-only checkpoint. Zero-shot 69.7% then adapter 80.3% on a 1,500-pair GLUE QQP eval, passing the closed Jev API (79.3%), while staying about 7.6x faster serial and fully on-device (Apple Silicon MPS). False duplicates 298 then 182. A complete, receipted, consumer-hardware adaptation recipe.
- jvr0x (Sep 22, majority read): Qwen3-4B on a DGX Spark through the Unsloth CLI; 743 context-distillation rows distilled from a locally served Qwen3.6-35B-A3B teacher; 7 min 20 s of training; system-prompt behavior baked into weights; 20 held-out prompts; 10% of rows given a generic system prompt so the behavior does not key off prompt-absence. Behavior adaptation on a desk-side box in minutes.
- Unsloth Docker (Sep 17): one image, train+run 500+ models locally, NVIDIA and AMD, GUI or notebooks, no setup.
- Gemma multimodal tuner (Oct 5): LoRA fine-tuning of Gemma text/image/audio on Apple Silicon behind a CLI wizard (osp.fyi/gemma-tuner-multimodal; tweet read, underlying site not fetched).
- Consent enforcement got an OS-level primitive: MXC went GA on Windows 11 (Gannotti, Oct 8) with a Learning mode that "blocks anything you haven't granted and writes a JSON report of what the agent tried to reach"; Unsloth is listed among tools supporting MXC now. A local fine-tuning job can run under a mechanically enforced file/network allowlist; that is LENS 2 made mechanical instead of promised.

**Q2: adapters or full-parameter for sub-8B, and does the corpus curriculum (LENS 1: 52,313 rows, figure given by the ask) hold primer bytes or is it inference-only?**
Adapter-side remains the frontier default for sub-8B, and 2026 work shifts from expanding rank to using the existing subspace better: U-LoRA (arXiv 2610.05800, ICML 2026, submitted Oct 5, green-door verified this session) gets competitive performance "via input-conditioned strategies, rather than from expanding the subspace"; ChainLoRA (arXiv 2610.00431, Sep 30, verified) does replay-free continual merging over chain-updated task-vector geometry.
As for the corpus: as it stands the 52,313 rows are inference-only bytes, not primer bytes. Two independent reads this session say naive continued-pretraining on passages is the worst injector: jvr0x states flatly that "fine-tuning is bad at teaching new facts and great at teaching behavior", and ElyHahami's benchmark found plain SFT on passages fails QA while extracted-facts and masked-reconstruction objectives work (memorization needs about 2 parameters per token; 1,000 episodes fit in 197K adapter params, 0.0025% of an 8B model). So: corpus rows prime BEHAVIOR cheaply (format, tone, tool habits) but would need a facts-extraction/masked-reconstruction transform before they could prime knowledge into janitor weights.

**Q3: would weight adaptation break the skills_pack precedent magnet (287 case_law edges, ask-given)?**
Not if the ledger stays the fast memory and merges are ceremonies, not drift. ElyHahami's architecture is the answer shape: per-episode micro-adapters + an embedding gate prevent interference "by construction by storing experiences in seperate adapters" (sic), and consolidation ("sleep") batch-replays episodes into base weights via a rank-2048 LoRA merge and then discards the adapters, keeping 94-95% of general capability. Without that structure, every technique they tried exhibits severe forgetting, LoRA included. ChainLoRA supplies the merge discipline for exactly that consolidation step (chain-updated task vectors + adaptive SVD merge, replay-free). Translation for the estate: keep compounding the skill ledger as the system of record; if we ever adapt janitor weights, do it as per-skill adapters with a gated replay/merge ceremony, never as naked continued SFT on the shared weights. The magnet survives; a naive merge is what kills it.

**Q4: which day-8 mine claims (LENS 4: 32 unbanked sweeps, ask-given) are verifiable through the green arXiv door in one funded session?**
I could not locate the 32-sweep inventory locally: memory/frontier/HELP_WANTED.md is 504 chars and holds no sweep ledger (checked this session); the figure remains ask-provided. What I can say from this session's legs: green-door verification is one fetch per claim and effectively free. Two of this sweep's claims were verified through the door in-session (ChainLoRA 2610.00431 and U-LoRA 2610.05800: exact title, authors, submission date, verbatim abstract sentences each). Claims whose evidence lives in a video or image (svpino's fine-tuned-4B-beats-frontier results) are NOT verifiable through the green door and stay unbanked. A funded session could sweep the mine's claims the same way at roughly one arXiv fetch each; sessions cost tokens, fetches do not.

## Overlap with our holdings

Instrument: chunked substring scans with the repo venv python (6.2s over the full 384MB catalog.jsonl; 144-147s over a bounded memory set of about 55,870 text files under memory/{lenses,percolator,frontier,press,mycelium,mesh,rib,runs,improve} plus memory root, 30MB/file cap, first 5MB/file). The full 10.4GB memory tree was NOT byte-grepped: a first full-tree scan was killed after 25 minutes, and raw findstr on this catalog ballooned to two 4.8GB stdout logs before being killed, so line-level grep tools are unsafe on this catalog.

Catalog topic census (occurrence counts, catalog.jsonl): fine-tun 965, unsloth 350, lora 283, jev 232, qlora 17, peft 2, gliner 2, chainlora 0, u-lora 0. The estate already tills finetuning heavily; the question is which specific atoms are new.

Exact-title / distinctive-phrase results per banked item:
- ElyHahami "can an llm know a life" and "2 parameters per token": 0 hits in catalog and bounded memory. NEW.
- GLiNER2.5-Decide: phrase 0 hits; raw substring "gliner" appears twice in catalog (relationship unverified). NEW with caveat.
- jvr0x "4b pirate" and "743 training examples": 0 hits. NEW.
- ChainLoRA "chainlora": 0 hits anywhere. NEW.
- Unsloth Docker "500+ models locally": phrase 0 hits, but "unsloth" has 350 catalog occurrences: topic well-tilled, this release post is the new atom.
- U-LoRA "conditioned gating" / "u-lora": 0 hits. NEW.
- Gannotti "digital daily: thursday, october 8": 0 hits. NEW.
- hrswatigupta "bespoke nimble": ALREADY HELD. Found in memory/runs/gapwave/gap_external_field.md (which points at memory/research_packs/COMPACTION_ALGO_RESEARCH_20260919.md as holding the "Bespoke Nimble recipe") and memory/runs/jev_salon2/economist.md (which already ran MacBook-class energy arithmetic on Bespoke Nimble: about $4.86/mo energy, about $104/mo amortized machine). "kev" word hits include memory/runs/gapwave/laya_digest.md. Residual new atoms in this item: the "pointer head" architecture phrase (0 hits) and the 66%->90% data-curation number. The ecosystem map itself is a re-bank; value is only those two atoms.

## Caveats and non-fabrications

- The 52,313-row corpus figure, the 287 case_law edge count, and the "32 unbanked sweeps" inventory are ask-provided material, not locally verified by this seat (HELP_WANTED.md grep came back empty on day-8/unbanked/sweep).
- svpino's results table is inside a video; I fetched the post text only and did not watch the video. Banked in the census, not in the JSON items.
- SHOW_ROBOTICS and Canonical posts exist only as profile-level snippets in the search index; no single status ID surfaced, so the door could not resolve them. Listed as census rows, not banked.
- jvr0x article: I read the first 5,200 of 18,280 chars; quotes come from the portion read. hrswatigupta: quotes come from the intro, the clone table, and the Layer-1/Kev passages extracted from the full 23,441-char body; not a linear full read.
- The "creator-reported" qualifier on the Bespoke Nimble 66%->90% claim is part of the source's own table and is preserved; the author flags where marketing numbers stop.
- Quote normalization: the GLiNER source text reads "~7-8x" with an en-dash in the original; the seat no-dash law forces a plain hyphen here, no other character changed.
- Raw fxtwitter JSONs are preserved beside this file (elyhahami_continual.json, unsloth_docker.json, svpino_finetune.json, chainlora.json, githubprojects_lora.json, hei_lora.json, gannotti_daily.json, neurondaily_laya.json, hrswati_jev.json, gliner_decide.json, jvr0x_pirate.json, jvr0x_pirate2.json) plus overlap_scan.py, the instrument for the overlap greps.

## BANKED ITEMS (JSON mirror, strongest first)

1. ElyHahami - "On Continual Learning: Can an LLM Know a Life?" - 2026-09-17 - full article read. In-the-weights continual learning benchmark on a fictional-life dataset; all techniques (LoRA, regularization, distillation) severely forget; 2 params/token memorization; per-episode gated adapters + rank-2048 consolidation merge keeps 94-95% capability. The design law for any estate weight-adaptation: ledger stays fast memory, merges are ceremonies.
2. imohitmayank - "GLiNER2.5-Decide fine-tuned: Local System One model, Jev-level accuracy, ~7x faster" - 2026-09-27 - full article read. Complete consumer-hardware LoRA recipe (r=8/alpha=16, 3 epochs, 1,500 rows) that closes a 10-point gap to a closed API and passes it (80.3% vs 79.3%) while about 7.6x faster, fully on-device.
3. jvr0x - "How fine-tuning actually works, explained by a 4B pirate" - 2026-09-22 - majority read. Context distillation of a system prompt into Qwen3-4B weights on a DGX Spark: 743 rows, 7m20s train, held-out prompts, generic-prompt dilution rows. The janitor-behavior bake, minutes not hours.
4. hrswatigupta - "Jev Is Turning Into an Entire Ecosystem" - 2026-09-23 - intro + table + passages read. Nine-layer map of the decision-model ecosystem; local anchors Kev (LoRA + pointer head on Qwen2.5-0.5B, Apache-2.0, trains on a MacBook, 160 ms/six questions) and Bespoke Nimble (LoRA on Qwen3.5-9B, 66%->90% after data-curation, creator-reported).
5. StatsPapers - ChainLoRA thread - 2026-10-02 - tweet + arXiv 2610.00431 abstract fetched. Replay-free continual merging over chain-updated task-vector geometry; the merge discipline for the consolidation ceremony.
6. UnslothAI - Docker image post - 2026-09-17 - tweet read. Train+run 500+ models locally, one image, NVIDIA+AMD, GUI/notebooks. The adaptation rail itself.
7. HEI - U-LoRA conditioned gating thread - 2026-10-09 - tweet + arXiv 2610.05800 abstract fetched. ICML 2026; competitive performance from better use of the existing low-rank subspace via input-conditioned gating, not subspace expansion. The adapter frontier's direction of travel.
8. MichaelGannotti - "The Digital Daily: Thursday, October 8, 2026" - 2026-10-08 - full article read. MXC GA on Windows 11: OS-enforced file/network allowlists for agents, Learning mode writes JSON reports; Unsloth among supported tools. Consent boundary as mechanism. Also Liquid AI d1-3B/d1-omni-600M open decision weights with day-one llama.cpp support, non-Apache license flagged.
