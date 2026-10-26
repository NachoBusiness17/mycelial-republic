# INTAKE — Phi Cookbook showcase post

**Filed:** 2026-09-03 · intake/eval lane · card 24 of the day's tranche
**Item:** https://x.com/GithubProjects/status/2095412682207924710

## ITEM
X post by @GithubProjects (repo-showcase account), 7:24 AM Sep 3 2026: "Phi Cookbook shows how to run Microsoft's small, efficient AI models on everyday devices. Practical examples for coding, reasoning, language tasks. Works on cloud servers or edge devices. Free, open-source with multilingual support." Target repo: **microsoft/PhiCookBook** (via an osp.fyi syndication card).

## RECEIPTS
- **Root post FETCHED** (webReader): full text + stats above (8.2K views, 3 replies, 5 RT / 52 likes / 49 bookmarks). Engagement thin; bookmarks > replies.
- **Author follow-up FETCHED:** one same-thread reply (13h later): "Explore it here:" + osp.fyi card link. It is a syndication card, not added substance; card itself NOT fetched (Unproven).
- **Replies NOT captured:** 3 replies exist, all behind the X login wall. Tri-stated Unproven — nothing in-thread overturns or sharpens the claim. One search pass for the thread text was content-filtered by the search vendor.
- **Repo FETCHED (github.com/microsoft/PhiCookBook):** 3.8k stars, **MIT license**, 976 commits, 8 open PRs, content through Phi-4-reasoning (2025-era; exact last-commit date not surfaced — staleness Unproven). Sections confirmed: **fine-tuning (LoRA/QLoRA, MS Olive, AI Toolkit, Apple MLX, W&B)**, inference (Ollama, HF, NIM, Foundry Local, Jetson/iOS/Android/AI PC), **quantization (llama.cpp, ONNX, OpenVINO, MLX)**, RAG/function-calling/eval.
- **Corpus sweep:** zero hits for PhiCookBook/"Phi-4" anywhere in docs/ref or watch → genuinely new to the corpus. MLX already named in watch/CAMPAIGN_SYNTHESIS_20260903.md: "Stage 5 is Rocinante-gated (Oct 27) or needs a CUDA/**MLX** lane."

## SCORE
**F:3 P:3 C:4 W:2 N:2 = 14/25 — BUILD WINDOWED**

## READ
The post itself is thin — a showcase account re-surfacing a well-known 2025-era Microsoft docs repo, three walled replies, an osp.fyi syndication card as the only follow-up. But the repo underneath happens to sit exactly on two live arcs: its **MLX fine-tuning/quantization sections are the textbook for the campaign's own named fallback lane** ("CUDA/MLX lane" for Stage 5 QLoRA deep compile), and the whole repo is the edge-SLM thesis in vendor voice — small models + good recipes, which is our own dumb-model-with-GPS doctrine. It is a bones-steal (recipes as checklist input to the QLoRA-pack stage and the Oct 27 one-button Rocinante package), not a capability: the fleet does not run Phi models (we run GLM-5.3/qwen/gemma), and training is hardware-gated until Rocinante lands. New to the corpus, but not new to the world — hence windowed, not now.

## TRI-STATE
- Post text, author follow-up, repo existence/license/sections — **Supported** (fetched, receipts above).
- "Runs efficiently on everyday devices" — **Unproven** (marketing claim; we ran no benchmark; Phi-4-era content may be stale by Sep 2026 — unverified).
- 3 replies / osp.fyi card content — **Unproven** (login wall / not fetched).
- Novelty to corpus — **Supported** (zero grep hits); world-novelty — **Disputed** (3.8k-star 2025 repo, widely known).

## VERDICT
**BUILD (windowed)** — 14/25, BUILD WINDOWED band. No premium token touches it now.

## ROUTE
**No wire.** Shelve as a receipt row on the QLoRA-pack shelf (watch/CAMPAIGN_SYNTHESIS_20260903.md, Stage 1/5): when the MLX/CUDA lane preflight starts (Rocinante prep, ~Oct), one free-lane rib_chat mining pass over PhiCookBook's MLX + QLoRA sections → checklist rows into the one-button Rocinante package. MIT license clears the steal-discipline gate (steal-the-bones). Opcode placement: research-mine → QLoRA-pack stage feed; no engine, room, or chain surface consumes it.
