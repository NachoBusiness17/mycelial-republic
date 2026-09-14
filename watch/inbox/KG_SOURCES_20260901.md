# KG PRIMARY SOURCES — 2026-09-01

Private knowledge graph ingestion. Primary artifacts behind 4 X posts, fetched live where possible. Every claim traces to a fetch/x_search actually run this session. UNVERIFIED where not proven.

---

## TARGET 1 — MerchantBench paper (Qwen e-commerce agent benchmark) ✅ VERIFIED

- **Source URL:** https://arxiv.org/abs/2607.28956
- **Fetched:** live web_fetch, 2026-09-01T22:03:53Z, HTTP 200
- **Exact title:** "MerchantBench: Benchmarking LLM Agents for Long-Term Coherence in E-Commerce Operations"
- **arXiv id:** 2607.28956 (cs.AI) · DOI 10.48550/arXiv.2607.28956
- **Authors (13):** Qiming Shi, Yulong Tao, Linbo Jin, Zhaolu Kang, Yibo Dou, Jiawen Zhu, Tianjun Pan, Shaokang Fu, Chengyu Wang, Siyue Li, Yaping Cheng, Di Weng, Chengfu Huo
- **Dates:** Submitted 31 Jul 2026 (v1); last revised 4 Aug 2026 (v2)
- **shasum:** `629255e5c1939e901db518b352769f9d418ef12cf8c5b7b9504c4e59f2a94abe` (saved at `KG_SOURCES_20260901_src/arXiv_2607.28956_abstract.txt`)
- **Abstract (5-sentence condensation / verbatim core):**
  1. LLM agents are increasingly evaluated as autonomous tool users, yet most benchmarks focus on bounded tasks with immediate success criteria.
  2. Real-world deployments often require Long-Term Coherence — preserving purposeful behavior across extended horizons while adapting decisions to accumulated evidence — which requires a persistent environment where actions constrain future choices, feedback arrives at heterogeneous delays, and incoherent behavior has measurable cumulative effects.
  3. Seller-side e-commerce offers a suitable setting via recurrent, interdependent decisions over Product Sourcing, Listing and Pricing Control, Cash-Flow Management, and Mixed-Latency Feedback Adaptation.
  4. MerchantBench is a 365-day order-level simulation grounded in 98,843 real e-commerce product records, equipped with 26 tools; it couples promptly observable Upstream Supplier Events with delayed Downstream Order Outcomes, requiring agents to follow order lifecycles and revisit earlier decisions.
  5. Evaluating eight LLMs under two agent frameworks in 48 runs (each 365 simulated days) reveals a substantial gap: the best LLM configuration attains only **27.3%** of the mean final net assets achieved by human participants.
- **Key benchmark numbers in abstract:** 365-day simulation; 98,843 real product records; 26 tools; 8 LLMs × 2 frameworks; 48 runs; best LLM = 27.3% of human mean final net assets.
- **PROVENANCE:** fetched-live (arxiv.org, HTTP 200).

---

## TARGET 2 — Orin coding agent ✅ VERIFIED (repo located + confirmed)

- **Pointing X post:** https://x.com/DivyanshT91162/status/2094852398632345664
- **Repo URL:** https://github.com/thetombrider/coding_agent  (**Project name = Orin**)
- **Verbatim post (x_search):** "I was going through some coding agent repos and found Orin. Honestly, the 'ask for permission before doing risky stuff' part caught my attention. You can give it a task, let it explore the codebase and figure things out, but it doesn't have to blindly start changing files or running commands. It can just stop and ask you first. There's also a pretty neat '/undo' system, so the agent's changes can be rolled back, even when they came through bash. And apparently you can run the whole thing in '--faux' mode just to see the terminal UI without even having an API key. Small detail, but I really like that. Not every coding agent needs to feel like you handed an AI the keys to your computer. REPOO👇" — followed by reply linking the repo.
- **What it is (from live repo README fetch):** Orin is a terminal-based coding agent. Give it a prompt and it reads, edits, and runs your code on its own, pausing for approval before anything risky ("safe by default — nothing is written or run without your approval"). Uses a per-turn BM25 retrieval pass (via Ratel) over the full tool catalog to expose only relevant tools (cuts per-turn token cost). Expensive model thinks; a cheap model does grunt work. Config/sessions/keys/checkpoints live under `~/.orin/`. Ships shadow-git snapshots before every tool execution, slash commands include `/undo`/`/restore`, approval modes (`normal | allow-all | plan`), `--faux` offline demo (no API key), and native OTLP / Langfuse-Grafana-Tempo-Jaeger trace export. MIT license. Competitors called out: opencode (SST), pi.dev, Claude Code. Repo contents: `.ratel/`, `docs/`, `scripts/`, `src/`, AGENTS.md, CONTRIBUTING.md, LICENSE, README.md, SPEC.md.
- **Star count:** NOT VISIBLE in fetched page (GitHub star badge is an image/SVG not rendered in the markdown extraction). Recorded UNVERIFIED.
- **shasum:** `45899c07b9cbe34aa29c3488c0d71ff24f0b62966251294990d26a1051f1b0c9` (saved at `KG_SOURCES_20260901_src/Orin_coding_agent_repo_fetch.log`)
- **PROVENANCE:** repo = fetched-live (github HTTP 200); post text = x-search-only (reported by grok-4-1); star count = unverified.

---

## TARGET 3 — System prompt leak ✅ VERIFIED (primary artifact fetched raw + live)

- **Pointing X post:** https://x.com/elder_plinius/status/2094862439653462387
- **Verbatim post (x_search):** "🚰 SYSTEM PROMPT LEAK 🚰 — Here's the Fable 5.1 system prompt!! 🙌 Coming in at a WHOPPING 270,000+ characters, this prompt is definitely on the longer side. There have been a handful of notable edits/additions since Opus 5's version. FULL PROMPT: https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/Claude-Fable-5.1.md — According to Fable, here's an overview of everything that's changed since last time: …" (long diff narrative, see below).
- **Primary leak artifact:** https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/Claude-Fable-5.1.md (repo: `elder-plinius/CL4R1T4S`, public, 70 issues / 54 PRs at fetch).
- **Raw file actually downloaded live:** 275,723 bytes; sha256 **`c57de521ca050e24634697b388fe840350481f238d3080cb2ef223cb8571196a`** (saved at `KG_SOURCES_20260901_src/Claude-Fable-5.1_RAW_system_prompt.md`). File head confirms: "…This iteration of Claude is Claude Fable 5.1, the newest mode…"
- **Which product leaked:** **Claude Fable 5.1** (Anthropic), model string `claude-fable-5-1`, Mythos-class, shares weights with Mythos 5.1. Leaked by the `CL4R1T4S` dump site (elder-plinius).
- **3 most notable diffs vs Opus 5 (2026-07-24 capture), per post + leak narrative:**
  1. **Size / section removals:** now 270,000+ characters, ~46 tool schemas (vs 30 in July); removed `<fable_safeguards_routing>`, `<default_stance>`, `<thinking_behavior>`, the June export-control suspension notice, and "Claude Design" from access surfaces; knowledge cutoff moved to end of June 2026.
  2. **`<refusal_handling>` expanded:** new illicit-substance guidance (harm-reduction info OK, no dosing protocols, redirect to dancesafe/tripsit/psychonautwiki); pre-1929 carve-out for reproduction of lyrics/poems/passages; a long block on visual works — no drawing known characters/logos/covers even via SVG/code (with Sonic banner and Very Hungry Caterpillar examples); weapons paragraph shortened.
  3. **`<user_wellbeing>` roughly doubled + memory redesign:** wellbeing block now forbids claims about mental state/motivation, naming undisclosed diagnoses, self-harm substitutes, "don't affirm self-harm works"; `<memory_filesystem>` redesigned as a background pass after each turn with in-turn writes only on explicit request, plus "Calibration"/"horizon test" sections; privacy taxonomy restructured into `<protected_attributes>/<sensitive_information>/<never_store>` with new edge cases; `<reply_after_tool_calls>` added.
- **PROVENANCE:** post + diff narrative = x-search-only (reported by grok-4-1); primary artifact = **fetched-live (raw GitHub, HTTP 200, sha256 computed)**.

---

## TARGET 4 — "4 Layers of an Agent System" post ✅ VERIFIED (verbatim via x_search)

- **Pointing X post:** https://x.com/RishiUvaach/status/2094779809830510790
- **Author:** @RishiUvaach (Rishi Uvaach-style handle)
- **Date:** status id mirrors 2026-09-01 window (exact timestamp not exposed by x_search; recorded as 2026-09-01 per task framing) — *exact per-second timestamp UNVERIFIED*
- **Verbatim core claims (from x_search):**
  - "An agent burns tokens, declares the task complete, and then fails the tests. That is often an architecture problem, not a prompting problem."
  - Four layers: **Loop / Graph / Harness / Meta-harness.**
  - **Loop** — "repeats until evidence says stop": smallest unit of agency; should stop on *external evidence* (passing test, build, validated output), not merely the model believing work looks correct.
  - **Graph** — "decides what runs next": branches, retries, specialist-agent handoffs, fallback paths, shared state; turns repeated execution into a structured workflow.
  - **Harness** — "gives the model an operating environment": tools, APIs, files, memory, permissions, context, logging, execution env. "Model capability and agent capability are not the same thing … a better prompt cannot compensate for a missing capability."
  - **Meta-harness** — "governs multiple agent harnesses": orchestration, governance, isolation, shared policies, movement of context/workflows across agents (e.g. Claude Code, Codex, internal + domain agents); names **Omnigent** as one open-source implementation.
  - Closing tagline: "Loop makes the work verifiable. Graph makes the workflow structured. Harness makes the model operational. Meta-harness makes multiple agent environments governable."
- **PROVENANCE:** x-search-only (reported by grok-4-1). Post text not independently fetched live; exact timestamp unverified.

---

## RECEIPTS

- **Timestamp (UTC):** 2026-09-01T22:04:30Z
- **Tools used:** web_fetch (arxiv, GitHub blob, GitHub raw via node https), x_search (grok-4-1-fast-non-reasoning; three queries), exec (sha256sum, node fetch, file save), write.
- **Verified live (fetched primary artifacts, sha256 computed):**
  - arXiv 2607.28956 abstract page — HTTP 200 — `629255e5…`
  - Orin repo github.com/thetombrider/coding_agent — HTTP 200 — `45899c07…`
  - Claude Fable 5.1 raw system prompt (CL4R1T4S) — HTTP 200 raw — 275,723 bytes — `c57de521…`
- **Verified via x_search only (verbatim claims reported by grok-4-1, not independently re-fetched):**
  - Orin X post text; Fable 5.1 leak post text + diff narrative; "4 Layers of an Agent System" post text.
- **Could NOT verify / gaps:**
  - Star counts for thetombrider/coding_agent and CL4R1T4S (GitHub star badges render as images, absent from markdown extraction) — **UNVERIFIED**.
  - Exact per-second timestamps of the four X posts (x_search returned post body + IDs only, not ISO timestamps) — approximate to 2026-09-01.
  - The full 750KB-blob page for the leak on the GitHub web UI was truncated by web_fetch; the *raw* file was downloaded directly instead (integral, hashed) — so the blob page truncation is not a data gap.
  - Cross-check note: the X post claims "270,000+ characters"; raw file = 275,723 bytes (UTF-8 multibyte ⇒ character count will be lower than byte count; not byte-for-byte re-reconciled) — **minor discrepancy left as-is, noted**.

### Related (already captured, NOT re-fetched)
- AnnatarXBT swarm-as-knowledge-graph post — already extracted elsewhere; not re-fetched per instructions.
