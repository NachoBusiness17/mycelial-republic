# Sweep: finetuning-and-adaptation via reddit — 2026-09-29 (ask stamp 2026-09-28)

Area: finetuning-and-adaptation. Seat: sweep-finetuning-and-adaptation-reddit (frontier sweep gopher).
All deep reads performed in this session via the safereddit.com redlib mirror; nothing banked that I did not read end to end.

## Door status (degraded, disclosed)

- Recipe door `old.reddit.com/r/*/top.json?t=month&limit=50` (r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama): all four returned a "Welcome to Reddit" skeleton with zero JSON payload — Reddit blocks this fetcher. HTML door `old.reddit.com/r/LocalLLaMA/top/?t=month` same skeleton. `www.reddit.com` thread pages returned only the word "Reddit". `mcp web_reader` on a thread returned Reddit's "Please wait for verification" wall.
- Fallbacks tried: `redlib.catsarch.com` HTTP 429; `redlib.perennialte.ch` HTTP 403; `rl.bloat.cat` ECONNRESET; **`safereddit.com` WORKS** and became the working door for both listings and full threads (top-month, search, and thread bodies with comments).
- WebSearch `site:reddit.com` used as the sanctioned fallback for discovery; the search provider intermittently returned MCP 429/1302 rate limits (paced one query at a time after the parallel burst).

## Pass 1 census

Enumerated 150 posts: r/LocalLLaMA top-month (25), r/LocalLLaMA search "finetune OR finetuning OR LoRA OR QLoRA" t=month (25), r/LocalLLaMA search "distill OR distillation OR synthetic data" t=month (25), r/LocalLLaMA search "dataset OR training data OR cleaning OR dedup" t=month (25), r/ollama top-month (25), r/LocalLLM top-month (25), r/MachineLearning top-month (25). All 1w* IDs = last 30 days. r/LocalLLM and r/ollama tops were hardware/quota drama; the finetune meat was in r/LocalLLaMA searches + r/MachineLearning.

## Pass 2 deep reads (8 threads, end to end)

1. `1wspn24` Jeff 0.8B/2B System-1 decision models (2026-09-28)
2. `1wsgrma` ImaJev-4b (2026-09-28)
3. `1wg7dd5` UkisAI Swift-Qwen3.8-27B (2026-09-14)
4. `1wm1gab` mini-AGI continual-learning (2026-09-21)
5. `1wss436` 5 finetunes vs base (2026-09-28)
6. `1wdp9qc` CodeFinetuner (2026-09-11)
7. `1wdl2qa` Qwen3.8-27B-Humanlike-Chat (2026-09-11)
8. `1wdasar` Spanda hallucination gate r/ollama (2026-09-11)

## Answers to the five research questions

**Q1 tape-to-model recipes + data scale for first gains.**
Published pipelines that turn a corpus you already own into a tuned small model converge on: structured parsing of the raw material into training shapes, LoRA, held-out eval, GGUF. CodeFinetuner (`github.com/cuolm/codefinetuner`): "raw code -> tree-sitter parsing into Structure-Aware FIM examples -> LoRA fine-tuning -> evaluation (CodeBLEU, edit similarity, exact match, perplexity, ...) -> GGUF conversion"; Qwen2.5-Coder-3B is the sweet spot, 1.5B "can't retain much on huge codebases", 7B works better; its eval runs the base model per-example so the delta is measured, and it warns test-set gains differ from real editor usefulness because the editor samples differently than the greedy eval. Humanlike-Chat is the closest personal-tape analog: 125,217 real messages across 1,396 conversations (chat turns real, reasoning synthetic) turned into a rank-256 LoRA on an abliterated Qwen3.8-27B; the overbaked LoRA collapsed tool-calling and persona diversity, fixed by dropping LoRA strength to 0.6-0.7. Data-scale signal: Jeff 2B went 46.5% untrained to 83.1% trained on ~271k classification questions (2B: ~3.5 hrs on one RTX PRO 6000); ImaJev's cautionary counter-scale: a first big fine-tune on ~500k short decisions made a 9B model WORSE (JevBench hard 64.9 to 42.3) because it had "basically learned to pattern-match" — scale without difficulty-shaped curation actively harms. Swift adds the negative result: plain cross-entropy SFT "did not work at all" for their objective; a custom loss plus on-policy distillation was needed.

**Q2 corpus cleaning gates the estate's judging doctrine lacks.**
Concrete gates observed in published pipelines that go beyond a single judge pass: (a) ImaJev's two-model consensus filter — generate hard questions with open-weight models, "keeping only answers where two AI models agreed"; (b) CodeFinetuner's base-vs-finetuned per-example comparison with quantitative metrics (CodeBLEU, edit similarity, exact match, perplexity) as a built-in gate, not a vibe; (c) Humanlike-Chat's failure mode is the counter-example — released "checkpoint 863 on vibes" with no held-out test set and a rank-256 LoRA that broke tool-calling; (d) Spanda's cheap consistency gate: sample 5 paths at T=0.7, exact-match entropy, zero VRAM; Qwen 27B AUROC ~0.89, Mistral 7B 0.71, and the crucial caveat that a 120B frontier model collapsed to 0.09 ("Confident Mode Collapse": identical wrong answer 5/5) — consistency is not truthfulness, and commenters pushed on exactly that; (e) community replication as an adversarial gate: GoblinEngineer's McNemar test on Swift (z=4.02, p<0.0001) found the finetune answers where the base abstains (106 vs 55 flipped) — a behavior delta an accuracy benchmark hides. None of the published pipelines ran provenance tags as a gate; that remains an estate differentiator. Note: the estate already frames "semantic entropy spike" as a router-drift probe (`memory/percolator/explore_deepseek_drain.jsonl:4`), so Spanda is adjacent-but-new: theirs is a per-answer train/no-train gate, not a router signal.

**Q3 does a fine-tuned 2B beat a prompted frontier model on narrow chores, and by how much?**
Yes on narrow classification-shaped chores, with honest ceilings. Jeff-2B matched frontier-API Jev's published 83.0% on its 4,599-question bench at 83.1%, ~28 ms/decision vs ~212 ms API — but BBH 64-68% vs Jev's 94%, ~50% vs ~73% on JevBench hard: "A small model is a classifier, not a planner" (the author's own lesson, exactly the janitor/scurry shape vs judgment-climb split the driving ladder already encodes). ImaJev-4b ranked #1 of 91 on JevBench and ahead of GPT-5.6 Luna on DecisionBench — but the author discloses the #1 rank weights accuracy, calibration, speed, and cost equally; on accuracy alone it is #3, and they concede they cannot beat 30B models on raw intelligence. The 2B sibling scores 72% vs 84% on the image benchmark (easy/medium equal to 4B, hard lags). Counter-evidence on OOD: base Qwen3.6-35B beat all five community finetunes on Aider Polyglot (37.4% first-try vs Occamy's best 30.8%), with the rebuttal that the harness (Aider's old tool-calling wire) disadvantages modern-tool-calling finetunes — benchmark rank can invert with the harness.

**Q4 synthetic distillation from the funded tier inside ~$180-220 credits?**
The published cost curves say the frontier-tier teacher is the expensive route and a local teacher suffices for classifier-shaped chores. ImaJev spent ~$1,200 on rented 4xH100 for its 1.2M-example set — 6-7x the estate's whole budget. Swift trained on an 8xH100 box (unpriced, same order of magnitude). The estate-fit counter-examples trained with NO closed-model outputs: Jeff authored ~31k questions with a LOCAL Qwen3.8-Flash-Next on two DGX Sparks plus 236k public-dataset-derived and 10k code-built questions, all on one RTX PRO 6000 (2-3.5 hrs), and the chess variant used 600k Stockfish-labeled positions (3.5 hrs, one GPU; held-out puzzles 6% untrained to 56% fine-tuned). Logit distillation remains costly per u/Minute_Laugh8065: KL on final logits "beats layer MSE; needs same tokenizer; costly — teacher forward pass on billions of tokens." Verdict from the evidence: within $180-220 credits, published results support glm-5.3-prime/qwen3.8-max-prime as JUDGE/labeler on a few thousand hard examples (the ImaJev consensus pattern at 1/300th scale), not as a bulk generator; bulk volume should come from local teachers and code-built data.

**Q5 continual adaptation from a fleet's own filed workdays (the DNA cycle).**
mini-AGI (`github.com/volotat/mini-AGI`) is the closest public artifact: continual learning trained from scratch on a 7.8B-character single stream, batch 1, on an 8GB VRAM laptop; dynamic MoE experts added and pruned during training; the forgetting fix is "slow down update of params that are used most often (trunk) and keep everything else at the normal speed". The thread's sharpest lesson is the critique the estate's DNA cycle should steal: u/TurboBanano — with trunk at 0.1x, part of "no forgetting" is just "not much learning"; test on a genuinely novel subject before calling it adaptation. A commenter's own MoE-growth attempt measured inserted layers contributing ~23x less than originals — naive growth under-delivers. Secondary: the Jeff voice pipeline logs decisions explicitly "for future training data" — the tape-loop instinct is spreading into practice, but at miniature scale (one lane, one task), not fleet-wide day-cycle form. Nobody published a fleet-scale filed-workdays-as-next-training-set loop; the estate's DNA cycle remains unclaimed territory.

## Overlap check (run this session)

- `rg -i -n "ImaJev|Swift-Qwen3\.8|mini-AGI|CodeFinetuner|Humanlike-Chat|Spanda|semantic entropy" catalog/catalog.jsonl` — zero hits in catalog.
- `rg -i -l ... memory/` — hits only in `memory/trajectory/steps.jsonl` (my own grep commands being logged as trajectory steps, verified lines 36155-36156) and one genuine pre-existing row `memory/percolator/explore_deepseek_drain.jsonl:4` using "semantic entropy" for a router-drift probe (2026-08-28) — different concept from the Spanda per-answer gate; recorded as partial overlap on item 8.
- No re-banking: none of the 8 items exist in the estate corpus.

## Caveats

- All quotes are as rendered by the safereddit redlib mirror of the live threads; direct reddit.com was unreachable from this seat (door status above). Dates are mirror-relative ("22h ago", "18d ago") converted from fetch day 2026-09-29.
- Comment scores in one mirror render looked like a rendering artifact (all "1"); noted where relevant, scores not load-bearing anywhere.
- Swift/Qwen/ImaJev/Jev are this season's model names as they appear on reddit; I did not independently verify the HF repos exist beyond what the threads link.
