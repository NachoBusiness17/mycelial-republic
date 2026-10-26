# sweep: kv-cache-context-engineering via reddit (2026-09-28 window)

source-fetched: 2026-09-28 (wall-clock fetches executed 2026-09-29 ~14:40-15:20 EDT by actor_3_23).

## Doors — honest record

- `old.reddit.com/*.json` via WebFetch: DEGRADED — returned the Reddit landing page, not JSON.
- `www.reddit.com/*.json` via WebFetch: HTTP 403 Blocked.
- `old.reddit.com/top/?t=month` HTML via WebFetch: landing page again.
- `mcp web_reader`: two attempts — 1302 rate limit, then Reddit "Please wait for verification" wall.
- `curl` with custom UA on old.reddit `.json`: HTTP 302 → login wall (`reason=lor2`).
- `r.jina.ai` proxy: target returned 403 ("whoa there, pardner").
- Wayback Machine: snapshots EXIST for 6 threads but the captured pages are the verification wall / empty React shells (11KB each, title "Reddit - Please wait for verification"). Useless.
- **Working door: PullPush API (api.pullpush.io, Pushshift successor)** — full submission + comment JSON for every candidate. All reads below are byte-level PullPush API responses saved under `./%TEMP%/pp*.json` (shell quirk: `%TEMP%` did not expand; files landed in a literal `%TEMP%` dir at repo root). Fallback door per recipe = WebSearch site:reddit.com (used for discovery; search snippets alone were never banked).
- Candidate ID space searched: r/LocalLLaMA, r/ClaudeAI, r/ClaudeCode, r/AIMemory, r/LocalLLM, r/LLMStudio.

## Pass 1 (broad sweep, 30+ candidates considered, all dated via PullPush)

Within the last-30-day window (>= 2026-08-30): 1wlazxc (2026-09-20) in-window; 1vt8v4c (2026-08-20) at 40 days; 1v5k08a (2026-07-24), 1uuue5p (2026-07-12), 1uu8g9f (2026-07-12), 1uohsov (2026-07-06) just outside; then 1u6bwz0, 1tt5gqv, 1tkih6y, 1tfqfvt, 1t96kfh, 1t1dl9y, 1sy7srk, 1suur3s, 1styl6v, 1shhb7j, 1seqize, 1rv3y3n, 1rjpifs, 1qzitx1, 1p05r7p, 1ostdcn, 1nn2nqz, 1ng0fmv, 1mhlj69, 1lh25j3, 1kfn1hg, 1ho4qp1, 1uiq26m, 1uhcf9t, 1rqoixa (all older), plus search-surfaced unread leads (markdown-vs-databases-for-memory 51 upvotes, 1mg5xlb, 1rsm45d, 1t50gya, 1eny4tl, r/LLMStudio TTT thread). Total considered: 37.

**The Reddit KV/prompt-cache corpus has a season: the measured-slot-cache + KV-quant wave is Feb-Jul 2026; September is thin.** The strongest material sits at 40-170 days old. Reported as found; nothing within window was suppressed.

## Pass 2 (deep reads — PullPush JSON read end to end: submissions + top comments)

### RQ1 — prompt-cache design patterns beyond the ZCode playbook, with hit-rate numbers

1. **1wlazxc (2026-09-20, IN-WINDOW) "Pre-caching context overhead (system prompt, tools, skills, ...)"** — Opencode/M2 Ultra harness: first prompt costs 2-3 min of PP because the harness re-sends overhead; proposal: harness pre-submits the overhead on project open. Comments carry the estate-transfer gold:
   - u/ShowerAnnual9741: "the idea works, but only if the prefix is byte-identical every time - that's the part i'd verify first. ... i'd log a hash of the overhead block on a couple of real sessions before building the pre-warm."
   - u/butterfly_labs: built a plugin that strips date/time from the system prompt; "TTFT is now very acceptable (5-10 seconds) on new sessions"; stripping MCP/skills blocks only helps "as long as the prompts are identical."
   - u/pilibitti: pi extension does slot save/load to disk; "yes the prefix must match character by character."
   - **Beyond the playbook:** the playbook's byte-identical-ask law gains a named enemy list (timestamps, working dir, per-session MCP/skills) and a verification instrument (hash the overhead block across sessions before trusting any pre-warm). The measured number: timestamp-stripping alone took TTFT from minutes to 5-10s.
2. **1uohsov (2026-07-06, 55 pts/51c) "Llama-Server is Throwing Away Your Perfectly Good KV Caches"** — slot save/restore restores 2.49 GB of KV in 1.23 s, then discards it: `llama_state_seq_save_file` does not serialize `slot.prompt.checkpoints`; the reuse path can only roll back to a *covering checkpoint* (at or before the rollback target), so a cold restart forces full re-prefill — "~17.5 minutes at 100K context" on 2x P100 with a 27B hybrid at Q6_K/turbo4-KV. A tip-synthesized checkpoint is useless (rollbacks target earlier positions). Fix v2: versioned sidecar `<state>.ckpt` (117 lines). Note: OP self-disclosed Gemini polish of the prose; the mechanics and numbers are OP's own runs; PullPush copy flagged `is_edited: true`.
3. **1uuue5p (2026-07-12) "llama.cpp Agentic Workflows Ctx Checkpoints Fix" (b9978)** — agent loops broke cache hardest: every agent turn created a checkpoint, bypassing min-step spacing and collapsing the coverage window, so any rewind in a tool loop erased all checkpoints → full reprocess. The fix evicts closely-spaced checkpoints from prior tasks to keep the window wide. u/NoMark3945 supplies the regression-test shape: "log reused prefix tokens and time-to-first-token after every tool result; with b9978, latency should stay roughly flat instead of spiking." That is a ready-made estate KPI: reused-prefix-token count + TTFT flatness per tool turn.
4. **1v5k08a (2026-07-24, 60 pts/26c) "CachyLLama's: llama.cpp fork with persistent KV cache"** — SSD-backed persistent KV checkpoints + system-prompt cache + multi-tier cache, survives server restart, handles hybrid/recurrent archs (Qwen 3.5/3.6, Gemma 4, GLM-4.7). Project benchmark (7840U/780M): ~1,243-token prompt 9.3 s cold → 0.41 s warm (~23x); ~5,409 tokens 43.3 s → 0.57 s (~76x); ~15,700 tokens 143.1 s → 0.99 s (~145x). Poster is explicit it is an operator report, not a controlled benchmark.

### RQ2 — structure-not-prose (memweave) evidence

**Gap, honestly: no measured structure-vs-prose attention-fidelity or cache-behavior experiment surfaced on Reddit in this sweep.** Two searches (structured-context queries) returned only loose leads (r/LLMStudio TTT; "markdown files better than databases for AI memory" at 51 upvotes) that I could not fetch end to end (PullPush q-search 429'd; no thread ID resolved), so nothing was banked. Closest read material: 1shhb7j's memory-write taxonomy and 1p05r7p's "contaminated summary" argument (structure/curriculum of context affects drift, both prose-form). **Estate-side replication design assembled from what I did read:** fixed task battery, A/B same-byte-count context in prose vs structured (tables/rows), injected at same slot position; measure (a) reused-prefix tokens + TTFT per tool turn (the b9978 KPI), (b) task accuracy at 100K effective depth (the 1sy7srk depth-sweep harness), (c) drift incidents (1shhb7j's Drift/Temporal/Provenance scenario classes). Not run here — it is a design, marked OWED as an experiment proposal.

### RQ3 — KV quantization/offload for 2B-8B janitor serving

5. **1suur3s (2026-04-24, 149 pts/59c) "Qwen3.6 27B's surprising KV cache quantization test results"** — llama-perplexity methodology on wiki.test.raw; F16 baseline PPL 6.9233; turbo3 KV at 200K context "no loops, no memory loss" on a 27B dense at Q5_K_M; author's generalization: dense >20B above Q4 tolerates V-cache compression; "probably all small models would be totally confused with a highly compressed V cache." Top comment (66 pts, u/Betadoggo_): "PPL and KLD are no longer good references for quality loss ... Q4 kv shows a minimal loss in both metrics but actually causes a huge dropoff in AIME" (post activation-rotation PR). Second-order comment (u/Digger412) quotes YAQA: PPL measures next-token surprisal, KLD measures whole-vocabulary distribution shift — different quantities.
   - **Janitor choice impact:** the estate's janitors are gemma:2b / gemma4 (2B-4B class) — exactly the size class the thread says suffers from compressed V cache. Directive that falls out: q8_0 K-cache at most for janitors, keep V at f16, and never judge KV quant for janitors by PPL — judge by the estate's own task battery (the abliterate-p1 scut battery is the right instrument).
6. **1sy7srk (2026-04-28) "Qwen 3.6-35B-A3B KV cache bench: f16 vs q8_0 vs turbo3 vs turbo4 from 0 to 1M context on M5 Max"** — full measured tables, 3 reps, 8 h wall clock, 128 GB unified memory. Decode tok/s at depth: 0 (f16 89.4 / q8_0 87.4 / turbo3 79.5), 32K (72.6 / 67.8 / 61.5), 128K (44.4 / 40.7 / 36.0), 256K (OOM / 26.6 / 22.9), 512K (OOM / OOM / 13.3), 1M (only turbo3 6.5 survives). PP drops faster than decode at depth. "At 128K the 3-bit cache catches up to the 8-bit" (measured line, read directly). **Context-budget impact:** q8_0 costs ~4-8% decode at typical depths (fine as default); turbo3/4 buy 2-4x the context ceiling at ~10% decode cost — the memory math that decides whether a 262K-context janitor fits beside the specialist on the same box.
7. **1u6bwz0 (2026-06-15, 64 pts) "I'm still surprised on how good the kv quantization has become"** — q4_0 KV including the speculative drafter, still accurate retrieval at 100K context (evidence is screenshots; text is thin — banked as corroboration only).
   - Overlap flag: catalog's 9 "turboquant" hits are LMCache **serde/embedding** TurboQuant (`corpus/library/lmcache-src/docs/design/v1/distributed/serde/turboquant.md`), and `memory/runs/gapwave/hn_x_fanout/local_serving.md` explicitly warns "retrieval lane, not model-serving quantization ... Flagged so the fleet doesn't misfile it." TheReddit/llama.cpp TurboQuant KV-cache line (TheTom's fork) is a different technology — genuinely new here.

### RQ4 — mechanism for KV / ram-cache drift across long sessions

8. **1shhb7j (2026-04-10, r/AIMemory) "No AI memory benchmark tests what actually breaks"** — the published mechanism for *memory-layer* drift: every mainstream benchmark (LoCoMo, LongMemEval, BEAM, AMB) assumes a read-only corpus; production drift comes from the write path: "A temporary agent reverts everything based on stale context. No timestamps, no conflict resolution, no awareness of concurrent writes" (Hermes Agent issue #2670). Commenters add: trust hierarchy (user_stated > LLM-extracted), extraction drift from a 3B enrichment model, and WRIT scenario classes (Drift / Temporal / Provenance / Constraint / Entity / Forgetting). LoCoMo audit numbers cited in-thread: 6.4% answer-key errors, 63% judge acceptance of wrong answers, Mem0 prompt suppressing "missing information" admissions.
   - Serving-layer drift mechanism (read from 1uohsov + 1vt8v4c): KV "drift" across sessions is not mysterious decay — it is (a) checkpoint metadata that lives only in process memory (lost on restart → forced full re-prefill), and (b) snapshot-validity coupling: valid restore requires same model file, quant, backend build, cache type, context size, rope settings, and exact token prefix (u/Other_Many_130, 2026-08-23). Any one changing silently degrades to recompute, which *looks like* cache drift.
   - **Rib status, honestly stated:** I could not locate the exact "ram-cache drift (lens laws.md)" open question in this session (grep of `memory/*.md` for "ram-cache drift"/"ram.cache" returned nothing; `memory/rib/` listing shows no lens-laws file; `.agents/skills/` grep empty). The cited mechanisms above are offered as the candidate cause; marking the rib closed needs a human to point at the rib file.

### RQ5 — context-window engineering at 100K+ scale

9. **1p05r7p (2025-11-18, 385 pts/61c, r/ClaudeAI) "My Claude Code Context Window Strategy"** — Auto Compact OFF dropped initial session context 85k/200k (43%) → 38k (19%); personal rule: initial context never above 20% of window; manual /compact risks "contaminated context" (model misunderstanding baked into the summary, then compounding drift). Top comments echo plan-mode → clear-context loops.
10. **1rv3y3n (2026-03-16, r/ClaudeCode, 57 pts/66c)** — 1M-context models "lose track of the task once they've filled ~40% of their context window"; 200k + work→/compact→work loop outperforms. Counterpoints in-thread (valaquer, davidmatousek): 1M wins when you orchestrate-and-clear with discipline anyway; the sub-agent default is the token hog.
   - **Transfer to the estate's compaction-amend loop:** the published camp split maps cleanly onto amend-not-resume: both camps converge on (a) keep the *prefix* stable and append-only (cache), (b) never let a lossy summary silently replace live state (1shhb7j's timestamps/conflict-resolution + 1p05r7p's contamination), (c) compact on a budget trigger (20% initial / ~40% fill), and (d) measure compaction by TTFT-flatness and drift incidents, not vibes. The estate's fold gate + verkle receipts already implement (b) more strictly than anything in these threads; the missing instrument is (a)'s prefix-hash + (b9978's) reused-tokens KPI on the janitor serving path.

## What actually goes beyond the ZCode playbook

1. Named byte-drift enemies: timestamps, cwd, MCP/skills blocks (1wlazxc) — plus the pre-flight instrument: hash the overhead block across real sessions.
2. The checkpoint-coverage invariant: saves must carry checkpoints from BEFORE the tip; metadata must ride with the KV bytes (1uohsov sidecar pattern).
3. Agent-turn checkpoint storms: min-step spacing must survive per-turn checkpoint creation or every rewind recomputes (b9978) — and the KPI to catch it: reused-prefix tokens + TTFT per tool turn.
4. Persistent-restore economics: 23x/76x/145x cold→warm at 1.2K/5.4K/15.7K tokens (CachyLLama, operator-reported) — the size class the estate's warm-boot path lives in.
5. KV-quant decision table by model size, not vibes: dense >20B tolerates turbo3+V-compress (PPL-verified but AIME-caveated); 2B-4B janitors: q8_0 K / f16 V only, judged on the task battery; q8_0 ≈ 95% of f16 throughput at agent depths; turbo3 buys 2-4x context ceiling at ~10% decode.

## Not run / not found (no fabrication)

- No structure-vs-prose measured experiment found or run (RQ2 gap above).
- The "lens laws.md" rib file not located; ram-cache-drift closure is a proposal, not a filed closure.
- 1wlazxc has 13 comments only (fresh thread, low engagement); its numbers are practitioner-scale, not benchmarks.
- CachyLLama numbers are the project's own; poster flags no controlled benchmark yet.
- Wayback-based reads all failed (verification-wall captures); nothing in this bank came from Wayback.
