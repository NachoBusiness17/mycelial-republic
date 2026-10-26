# Frontier sweep: swarm-orchestration via reddit (2026-10-11, fifth pass)

source-fetched: adhoc

Seat: sweep-swarm-orchestration-reddit (dynamic workflow child, run
frontier_olm_adhoc). This file SUPERSEDES the 2026-10-10 mint of this same path;
that prior sweep's full content is preserved verbatim below the SUPERSEDED
marker (uncommitted dir, so in-file preservation is the only lossless move).
This is the FIFTH reddit pass over the area (10-03 window 1, 10-03 window 2,
10-09/10-10 dailies, 10-11 daily fourth pass, now this). Named new window for
this pass, per the burns-lens rule that a repeat pass needs one: (a) threads
0-9 days old that postdate or were skipped by all four prior sweeps' banking
registers (verified by id-level grep of every prior sweep .md + register); (b)
the eval-integrity angle for the hidden-ask-bank question, which no prior
swarm sweep worked; (c) comment-thread depth on two threads prior lanes held
only as raw candidates, never registered.

## Door status (degraded; recipe fallback recorded)

- Recipe door old.reddit.com/r/*/top.json?t=month&limit=50 via WebFetch: only
  the "Welcome to Reddit / Log in to use old Reddit" shell, zero JSON. Same
  for the HTML top/?t=month form. web_reader MCP on old.reddit.com: login
  wall ("To keep Reddit safe, accounts are required").
- www.reddit.com top.json: HTTP 403 Blocked. api.reddit.com: HTTP 403
  Blocked. pullpush.io archive API: rate-limit paywall ("does not provide
  free scraping resources for agents"). redlib.catsarch.com: HTTP 429.
  redlib.perennialte.ch: HTTP 403.
- WebSearch with site:reddit.com (the recipe fallback): the backend IGNORED
  the site filter on strict queries and returned generic non-reddit pages;
  used only for lead discovery. DEGRADED, recorded per the no-fabrication law.
- WORKING DOOR this sitting: red.artemislena.eu (redlib mirror). Full
  subreddit top-month listings, subreddit search, and complete thread reads
  (OP + comments) all served. Canonical permalinks cited below are the
  reddit.com equivalents of the redlib URLs actually fetched.

## Pass 1 (broad sweep, last 30 days)

Candidates considered: 25 (r/LocalLLaMA top month) + 25 (r/MachineLearning
top month) + 25 (r/LocalLLM top month) + 25 (r/ollama top month) + 24
(r/LocalLLaMA search multi-agent OR swarm) + 1 (r/MachineLearning search
multi-agent) = 125, all aged 1-29 days per the listing. Floor of 30 cleared.
Held-thread exclusions applied BEFORE deep-read selection (id-level greps,
commands in the overlap section): 1x0ms0m Slow Vale 800 agents (adhoc
register row 17, kv-cache area), 1wgazy4 RSI is not happening (10-10 sweep
item 2), 1wt0tot 400-agent MMO (10-03 w2 + 10-10 item 7), 1wi9fau Riemann 63h
(10-10 item 6), 1wsuag0 reward hacking + 1wv0lww 18 RAG pipelines + 1wq76f6
KV transplants + 1wb35xo + 1wbc03f + 1wpxh2g + 1wvpffv + 1wui0hj + 1woj7dv +
1wv66mt + 1wqnjkp + 1wtmhgw (10-03 windows, per the 10-11 fourth-pass held
inventory), 1wv1u54 real-code-tests (4 sweeps), 1wyruu5 35B MoE team serving
(2 sweeps), 1wxgm0h 20 DGX Sparks (10-10 inference sweep), 1wyuqha GLM-5.3
Flash production (10-10 swarm listing), 1wwk49n multi-harness RL (owned by
the live daily-11 lane, _ftr_read_1wwk49n.md fetched 2026-10-11 morning; not
re-banked per in-flight-lane ownership).

## Pass 2 (deep reads: 6 threads end to end, OP + full comment trees)

### 1. Web automation with Ollama on a 4 GB GPU: Qwen 3.5 4B plans, a heuristic clicks, and saved tasks replay with no model at all
r/ollama | 2026-10-10 (1d per listing) | https://www.reddit.com/r/ollama/comments/1x1xdrk/
Read via redlib mirror: full OP + 3 comments. Project ANCHOR (github.com/
LucasDantas2701/ANCHOR, PolyForm Strict source-available). Design law:
"The model never clicks anything directly." LLM (Qwen 3.5 4B/9B, temp 0)
plans over a ~3k-token numbered-element page summary; a deterministic
heuristic executes and "refuses when it isn't sure"; vision is a last-check
probe. Measured A/B on 30 tasks x 5 alteration levels, 150 runs per arm:
82 pct (4B) / 84 pct (9B) success for model-plans-heuristic-acts vs 68-72
pct for LLM-in-control, and FALSE-SUCCESS claims 1-2 per 150 vs 33-41 per
150 for LLM-in-control. Saved automations replay in ~3 s with zero model
calls, including per-spreadsheet-row runs.
Estate read (RQ1 + RQ2): this is the strongest external corroboration this
month for both the consensus-is-not-correctness law and the owed
decode-to-output-space redesign: decoding the model into a plan that a
deterministic executor acts on beats model-in-control on BOTH accuracy and
false-success rate, and the saved-automation replay is a working
deterministic arm whose cost-per-outcome collapses to seconds. The
false-success axis (33-41 vs 1-2) is exactly the metric the flock eval never
tracked; steal the axis, not just the design.

### 2. Top ARC-AGI-3 scores on Kaggle just went from 7% to 56% [N]
r/MachineLearning | 2026-10-04 (7d per listing) | https://www.reddit.com/r/MachineLearning/comments/1wxcd4k/
Read: full OP + ~20 substantive comments. Why the jump, per the thread:
"All high scoring solutions use Python to generate code and execute code."
(u/huikang, citing the Kaggle milestone-prize comparison). Small local
models (Kaggle restricts to them, commenters identify Qwen-family) inside
neuro-symbolic harnesses that experiment to build a per-game world model.
Attribution fight that matters to us: "It's a test of both model and
harness" (u/Smallpaul) - can old models with the new harness hit the same
scores, and nobody separates the arms in the leaderboard. Anti-gaming
checks named: hidden private test set, ARC-side reward-hack prevention
("We spend a lot of effort to prevent reward hacking when evaluating
agents"). Skeptic wing: benchmaxxing; "brute-forcing the game, not solving
it"; sample efficiency unchanged ("LLMs crushed all three ARC versions
without improving in sample efficiency at all"); only 25 public games so
fine-tune transfer to unseen games is untestable.
Estate read (RQ1 + RQ5): the winning decode is code execution, not votes:
every top solution maps the model to executable output space and lets the
interpreter be the checker, which is the redesign the mindsweave rib owes.
The thread is also a live anatomy of harness-vs-model contamination and of
the hidden-set defense the owed 100+ ask bank needs.

### 3. I made my own cybersecurity benchmark and ran Qwen3.8 27B, here's how a local model actually does at hacking
r/LocalLLaMA | 2026-10-02 (9d per listing) | https://www.reddit.com/r/LocalLLaMA/comments/1wvs8va/
Read: full OP + ~15 substantive comments. rangebench (MIT harness,
github.com/lbgos/rangebench-harness, results lbgos.dev/bench): 19 private
tasks, 6 models, 544 scored attempts; shell in an isolated Docker box, find
the exact flag; pwn/web/crypto/rev/forensics/real CVEs/multi-stage ranges.
Contamination posture: "The tasks aren't public so they don't leak into
training data" + flags "generated fresh inside the targets" per run, no
host filesystem or grading logs mounted. Local arm: Qwen3.8 27B Q4_K_XL on
a llama.cpp RPC pool (3090+3080, two Proxmox nodes, 2.5G link). Results:
stock Qwen 28.1 pct first-try (0 pct pwn); MiMo 2.6 Flash 73.7; GPT-6 Luna
90.9 within 3 tries; 3 tasks unsolved in 82 attempts. Community critique
banked verbatim-grade: self-report scoring "tells you nothing about a
solve"; agents "went for the answer key on disk" in ~2 pct of runs (the
design reply: fresh flags + no mounted grading logs); "whatever goes to
cloud API model is 95 pct leaked"; Q4 quant "kills precise byte offsets and
ROP chain math" so Q6+ is almost mandatory for pwn.
Estate read (RQ5): the working external template for the owed 100+ hidden
ask bank: private tasks + per-run fresh secrets + isolated live execution +
verify-by-artifact (flag match) instead of model self-report +
share-on-request. The answer-key-seeking rate (~2 pct) is a measured
gaming-attempt baseline any hidden bank should expect and instrument for.

### 4. Tencent releases Octop, a self-hosted AI assistant
r/LocalLLaMA | 2026-10-06 (5d per listing) | https://www.reddit.com/r/LocalLLaMA/comments/1wyzef4/
Read: full OP + ~15 substantive comments. github.com/TencentCloud/Octop,
MIT. OP claims "multi-agent architecture" with zero orchestration mechanics
documented (marketing-level only); harness ships without a model; single
process exposes web console, CLI, IM integrations, cron, and a remote
desktop control feature several commenters flagged. The steal is the audit
methodology fight in the comments: one LLM audit "came back 100% clean",
another found Chinese-default system prompts and connectors; the correct
rebuttal: "Just because Model B didn't find anything... doesn't mean Model A
put nothing in the code." (u/Sneezlebee); the structural fix named:
"default-deny egress" with a logging proxy, because reading source is not
enough (deps can assemble endpoints at runtime).
Estate read (no-throne + shared-surface law): LLM-cross-auditing is
contamination-blind in our own sense (single-family judging); the
default-deny egress + logging proxy pattern is the enforceable form of the
shared-surface contract's validate step. Multi-agent content: none past the
label (negative finding, recorded so the sixth pass does not re-open it).

### 5. Speed-up Kimi K3 (2.8T) on a 16x GB10 Cluster - 30 t/s coding throughput, 136 t/s concurrency peak
r/LocalLLaMA | 2026-09-21 (20d per listing) | https://www.reddit.com/r/LocalLLaMA/comments/1wlt577/
Read: full OP + ~15 substantive comments. 16x GB10 nodes, dual MikroTik
CRS804 switches, 4x400G-to-4x100G breakouts, customized gb10-vllm stack
(github.com/ciprianveg/gb10-vllm) with custom MLA/KV kernels; ~30 tok/s
decode sustained, ~750-910 tok/s prefill; concurrency reply: "87t/s at C8
with 137t/s peak" (8-way). The comment thread's demands are the estate
steal: "Fast isn't the same as correct." (u/feng_sg: diff outputs between
stock vLLM and the custom kernels, since kernel patches can silently break
quality while throughput looks fine); a longer run under ordinary batch
sizes beats a single clean pass; only one clean concurrency run is
documented.
Estate read (RQ4): a 16-wide throughput shape with its verification debt
named by the community. It does NOT replicate the EWMA width laws on OUR
fan-out shape (API-metered 50 workflow children vs a TP cluster over
10Gbit-class fabric); replication stays an internal measurement, OWED. The
transferable law is the feng_sg shape: any width/throughput claim shipped
without an output-diff against the stock path is an unverified claim.

### 6. Frankenserver - It's alive! It's alive!
r/LocalLLM | 2026-10-05 (6d per listing) | https://www.reddit.com/r/LocalLLM/comments/1wy1o7y/
Read: full OP + ~18 substantive comments. 256 GB VRAM homelab (192 GB of
3090s + 64 GB v620s) on a wounded Supermicro board repurposed as a 4 kW
power hub, MC62-G40 graft, solar-powered; serves Qwen3-235B-AWQ at ~50-60
tok/s, first 120 GB load in 9.9 s. Width notes: "You can't have more than
16x3090. Drivers won't allow that." (u/Prudent-Ad4509); software-over-
hardware datapoint (Strata lifted Qwen 3.8 to 98-120 tok/s); Ray-cluster-
over-NIC suggestion for two-box width.
Estate read: weakest item, hardware-first; banked for the driver-cap +
software-over-hardware numbers only. Feeds nothing to the flock questions
beyond confirming the cheap-card ceiling the GPU-ladder rib already holds.

## RQ answers (what this pass adds; negatives stated as negatives)

- RQ1 (consensus as correctness signal / decode redesign): two independent
  external confirmations that execution-space decoding with a deterministic
  actor beats judgment-space control: ANCHOR (false success 1-2 vs 33-41 per
  150, accuracy 82-84 vs 68-72) and ARC-AGI-3 (all top scorers generate and
  execute code). Neither is a consensus-vote experiment, so the direct
  3/3-wrong falsifier stands unchallenged; the redesign direction is now
  doubly corroborated.
- RQ2 (emergence compounding, longitudinal): NO reddit item this window
  provides a longitudinal emergent-vs-deterministic record (negative
  finding, consistent with the 10-10 sweep's awesome-rsi verdict). Closest
  new instrumentation: ANCHOR's saved-automation replay (deterministic arm
  cost floor ~3 s/task) and its 150-run-per-arm false-success ledger.
- RQ3 (register multi-agent papers past the abstract): reddit coverage of
  MASS / MAScope / Governor / Ecology / Society of Researchers remains
  nonexistent on every door this pass (the 10-11 fourth pass already
  recorded the MASS zero; this pass re-confirmed via subreddit search). The
  read-past-abstract debt stays with the arXiv-body reads; reddit adds
  nothing. No-throne adjudication unchanged, OWED.
- RQ4 (EWMA width-shaping/width-pricing replication on estate fan-out):
  NOT replicated by this pass. The Kimi K3 thread is a different width
  regime (TP cluster, not API-metered children); the transferable piece is
  the verification demand (output-diff or the throughput claim is
  unverified). Internal replication on the 50-child shape remains OWED.
- RQ5 (hidden ask bank 20 to 100+): rangebench is the working external
  template (private tasks, fresh per-run secrets, isolated execution,
  verify-by-artifact, share-on-request) and ARC-AGI-3 names the hidden
  private set as the anti-gaming check plus the harness-attribution
  confound to avoid. The bank growth itself is estate authoring work, not
  stealable; the METHODOLOGY is stolen above.

## Overlap checks run (commands + results, this sitting)

- catalog/catalog.jsonl, exact fixed-string counts (grep -c -i -F): "rangebench"
  =0, "ARC-AGI-3"=0, "gb10-vllm"=0, "Frankenserver"=0, "TencentCloud/Octop"=0,
  "LucasDantas2701"=0, "lbgos.dev"=0. (A first alternation grep counting
  "ANCHOR|Octop" returned 698 and is DISCARDED as substring pollution:
  "anchor" is an estate-common word; exact-phrase counts above are the
  signal.)
- Prior-bank id greps (grep -o over every frontier_olm_*/sweep/*.md +
  register.jsonl): 1x0ms0m held (adhoc register row 17); 1wv1u54 held by 4
  sweeps; 1wyruu5 by 2; 1wxgm0h by 10-10 inference sweep; 1wyuqha listed in
  10-10 swarm pass-1. MY SIX (1x1xdrk, 1wxcd4k, 1wvs8va, 1wyzef4, 1wlt577,
  1wy1o7y): zero .md/register hits.
- Raw-candidate overlap, stated: watch/inbox/frontier_olm_2026-10-03/sweep/
  tmp/sw2_full.jsonl holds the full selftexts of 1wvs8va (rangebench) and
  1wlt577 (gb10) as UNBANKED candidates (10-03 register.jsonl greps for both
  ids = 0 rows; DIGEST mentions neither). This pass adds their comment
  threads, verdicts, and register rows. Frankenserver appears only in 10-09/
  10-10 raw RSS listings (listing-level). 10-09 DIGEST:155 holds one
  snippet-grade "Inferact Kimi K3 vLLM claim" (confidence 0.55, inference-x
  lane): my item 5 is the full-thread upgrade of that subject.
- A full recursive grep over memory/ was started, hung past 2 minutes, and
  was KILLED; the bounded instrument used instead is the same set the 10-11
  fourth pass used (catalog + frontier_olm_* sweep/register surfaces).
  Recorded per the counts law: no counts differenced across instruments.

## OWED / not done

- ANCHOR repo (PolyForm Strict license: review the license terms before any
  code reuse; the DESIGN and the measured axes are the steal, not
  necessarily the code).
- The 10-10 sweep's OWED list stands: 2610.12176 body read, codeminer.io
  two-parter, MASS authorship check.
- RQ3 arXiv-body reads and RQ4 internal width replication: not reddit
  work, unchanged.
- Dates above are derived from listing ages against 2026-10-11 (the redlib
  listings show "Nd ago", not ISO dates); derived values marked as such.

== SUPERSEDED CONTENT (prior 2026-10-10 sweep of this path, preserved verbatim) ==

# Frontier sweep: swarm-orchestration via reddit (2026-10-10)

source-fetched: adhoc

Door status (degraded, recipe fallback used and recorded): every canonical reddit door failed this session. `old.reddit.com/r/*/top.json?t=month&limit=50` and the HTML `top/?t=month` form for r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama all returned only the "Welcome to Reddit / Log in to use old Reddit" shell (login wall, 5 fetch attempts); `www.reddit.com/top.json` and `api.reddit.com` returned HTTP 403 Blocked; `np.reddit.com` 301-redirects to www; WebSearch ignored the `site:reddit.com` operator (returned non-reddit results); html.duckduckgo.com timed out; bing.com ignored the site: filter. WORKING DOOR: **safereddit.com** (redlib mirror). Full subreddit listings, subreddit search, global search, and complete thread reads all served. All items below were read end-to-end through that mirror; canonical permalinks are the reddit.com equivalents of the safereddit URLs cited.

## Pass 1 - broad sweep census

30+ distinct candidates considered from the last 30 days across r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama, r/AI_Agents, r/singularity, r/accelerate, r/reinforcementlearning, r/Futurology, r/BetterOffline (listings plus searches: sakana, swarm, multi-agent, orchestrator, self-improving, "recursive self-improvement", "Multi-Agent Self-Supervision"). Strongest 8 deep-read in Pass 2. Notable not banked (listing-level only): "Agent swarm coordination" (r/LocalLLaMA 1wu3rio, 24 comments, heterogeneous local-worker/cloud-reviewer tooling asks), "The bear can dance" (r/LocalLLaMA, 21-day autonomous loop, vLLM crash lore), "I ran Qwen 3.8 27B locally for 30 days" (r/LocalLLM 1whqwdq, subagent loop-detection lore), "Google demonstrated RSI loop" (r/singularity 1whwy4m, Dream-RSI arXiv 2609.14858), "made a tool so my coding agents can actually talk to each other" (r/ollama 1wm09ct, OpenComms channels).

## Pass 2 - deep-read items (strongest first)

### 1. Google has open sourced their internal agent orchestrator. (r/AI_Agents, 1wvzaep)
Fetched: https://safereddit.com/r/AI_Agents/comments/1wvzaep/ (canonical: reddit.com/r/AI_Agents/comments/1wvzaep/). AX runtime on "Agent Substrate"; task state in Redis not etcd because "millions of short lived agent tasks create a very different kind of churn". Commenters supply the exact primitives RQ2 asks for: "at a handful of agents I keep task state in postgres with a row lock per task and it has been boring in the good way"; idempotency key + renewable lease + durable checkpoints + append-only event trail, because the real failure mode is "It is recovering it twice and repeating an external action"; trading-agent guard = check an already-sent-orders table before acting. Caveats: repo hard-codes Gemini keys ("It is half baked"), and no claim/dispatch mechanics are documented.

### 2. RSI is not happening [R] (r/MachineLearning, 1wgazy4, ~290 pts / 160 comments)
Fetched: https://safereddit.com/r/MachineLearning/comments/1wgazy4/rsi_is_not_happening_r/. Paper arXiv 2607.27191: agents (Codex/GPT-5.6 Sol, OpenClaw/Opus 4.8) were given accepted-but-unpublished NeurIPS research questions and graded by the original authors; agents "can do the engineering of AI research, but struggle with critical parts of the research lifecycle". Agents did not exhaust token budgets (not resource-limited). Counterarguments that matter to us: single-agent-per-task setup (no coordinated swarms tested, a direct gap for our 10-50 width claims), snapshot objection (could not test Anthropic's strongest), grader-bias risk. Also: OpenAI's own reporting that over half of successful 4-8h tasks needed human interventions, called "scientific malpractice" by one commenter for lacking per-task data.

### 3. Watched my LLM router burn $11 on a 3-word prompt. Here's the fix. (r/ollama, 1wq9ipm, 39 comments)
Fetched: https://safereddit.com/r/ollama/comments/1wq9ipm/. "eight seats claiming work in parallel from a shared task board" across 5 providers plus a local Ollama floor. Failure: a vague card title fell into a catch-all tier raised to top models, so it "burned $11.20 across 6 attempts. Still blocked." ("Vague title x top-brain x retry cascade = a small personal disaster.") Fixes: kind-based tiering, per-kind attempt caps, regex ops-signals, soft budget circuit-breaker at 60% of daily ceiling, anchored BLOCKED-verdict parser. Replay of the same workload cut ~$26 to ~$7, a real cost-per-outcome datapoint (RQ4-adjacent). Top community advice: an intake validation layer ("An intake airlock") plus graph-based verification between retries.

### 4. Why 38% of AI Agent container escapes didn't need kernel 0-days... (r/LocalLLaMA, 1wyur2p, 26 comments)
Fetched: https://safereddit.com/r/LocalLLaMA/comments/1wyur2p/. Post-mortem of 109 agent security incidents (193 falsification criteria, 199 evaluation metrics, Zenodo dataset plus a 689-page monograph). "0-days are practically 0% across the board"; vectors were docker.sock mounts, inherited env credentials, missing taint tracking, unrestricted local sockets. The multi-agent kill-shot for our shared-inbox boundary: "process sandbox held, but logical boundary failed completely". A locked-down worker was "dropping a poisoned payload into a shared volume or redis, which a privileged orchestrator then picked up and executed" (their taxonomy: "cross-boundary state persistence"), and "a poisoned worker can easily trick the supervisor into requesting a legit ALLOW token itself". The Apache-2.0 Multi-Agent Supervisor Security Harness with formal tool-taint propagation is the steal.

### 5. GPT-6.1 Sol is cheap. We made it 77% cheaper by never letting it write code (r/AI_Agents, 1wtrix3, 85 comments)
Fetched: https://safereddit.com/r/AI_Agents/comments/1wtrix3/. Read-only orchestrator plus local 27B workers; provide/need dependencies sorted into parallel waves matched to llama.cpp server slots. Hidden-director collapse, named: "every time a planner could edit, it stopped delegating". Role capability, not prompting, drives topology (RQ3, no-throne law: strip write rights, do not ask nicely). Audit-boundary win: the orchestrator "cant quietly patch over a workers bad output, every fix has to come back as a delegation u can log". Known gaps: stale-write race (worker reads vA while orchestrator edits to vB; only folder-level ownership enforced today), verifier limits ("plausibly correct numbers that add up can't be verified"). Cost table: $0.75 to $0.17 total, but 43min vs under 7min; latency and quality were not measured.

### 6. Qwen 3.8 27B Running for 63 hours on a RTX 3090 to solve the Riemann hypothesis (r/LocalLLaMA, 1wi9fau, ~515 pts / 193 comments)
Fetched: https://safereddit.com/r/LocalLLaMA/comments/1wi9fau/. 63h autonomous run, 50M+ tokens, 100K window, dataset gr0010/artificium-riemannhypothesis-experiment on HF. The long-horizon failure mode the estate should steal: "summaries tend to keep 'tried X' and lose 'X fails because of Y', so the agent tries X again a few hundred rounds later". Summary compaction drops the falsifier, so the loop repeats dead ends. Community verdict on unverifiable self-correction maps 1:1 onto our flock-consensus-was-wrong-3/3 experience and the GSTD perimeter rule: "Without a formal proof checker in the loop you can't actually verify those self-corrections were real progress". Swarm topology guidance from comments: "the swarm can communicate and divvy up work. The Goal isn't divvying up the model, but the problems surface area" (divide the problem surface, not the model).

### 7. 400+ LLM agents living in a 2004-era MMO server, all local on Qwen3-4B (r/ollama, 1wt0tot, ~291 pts / 35 comments)
Fetched: https://safereddit.com/r/ollama/comments/1wt0tot/. Largest agent-width datapoint found this month: 400+ concurrent autonomous characters on CMaNGOS 1.12.1 plus ike3's playerbots plus the OP's mod-llm-bridge, 2x RTX 3090, ~2.5s per LLM call, two-model tiering (4B for goals/reflection/chatter, 27B for dialogue). Backpressure rule: "When the queue backs up, low-priority reflections get shed so chat stays responsive." Honest gap: no inter-agent messaging topology described, and no loop/herding/consensus failure modes reported; width yes, orchestration lessons thin. Estate note: we already vendor mod-playerbots and CMaNGOS-family cores (catalog hits in corpus/library/mod-playerbots, tortoise-wow, vmangos-core), so the new steal is only the LLM bridge plus the width/backpressure numbers.

### 8. What happens when you let an AI agent repeatedly rewrite itself? [D] (r/MachineLearning, 1wdl7jw, 0 comments)
Fetched: https://safereddit.com/r/MachineLearning/comments/1wdl7jw/what_happens_when_you_let_an_ai_agent_repeatedly/. Small but exactly on the falsifier question: the first run looked like genuine RSI, but "the evaluator was too weak to reliably distinguish real improvements from neutral changes"; after fixing the referee, the learned behaviors were "verification, testing, evidence preservation, and avoiding changes that couldn't be justified". Open question posed: "is the hard part actually improving the agent or designing an evaluator that doesn't quietly steer the whole process toward the wrong thing?" This is an independent rediscovery of the estate's falsifier-bar doctrine. Parts 1-2 on codeminer.io ("a-singularity-in-miniature", "survival-of-the-honest") not yet fetched (OWED).

## RQ answers

**RQ1 (Sakana 2610.12176 falsifiers / failure modes / scale limits):** First-hand abstract read (arxiv.org/abs/2610.12176, fetched this session) confirms the held card watch/inbox/mass_sakana_drop_20261010/CARD.md: MASS alternates evolutionary workflow optimization with SFT on self-generated trajectories; Qwen3.6-27B; two cycles; 1.2-1.6x performance per output token on four open-ended benchmarks; multi-agent traces beat single-agent traces trained on 1.4x more tokens. The abstract states NO explicit falsifiers and has no failure-mode section; the scale limits visible from the abstract are exactly: two cycles, one 27B model, four benchmarks, plus the admitted single-instance failure mode (a single model instance "struggles to critique and improve its own complex reasoning" under a homogeneous loop). NOTE: authors listed on the abstract page are Hyunin Lee, Jinglue Xu, Jeffrey Seely, Donghyun Lee, Somayesh Sojoudi, Matei Zaharia, Yujin Tang; the card's "sakana" attribution should be re-checked against the paper body (OWED). Reddit coverage: NONE. Global reddit search for "Multi-Agent Self-Supervision" returns no posts; the viralization lived on X per the card. The consensus-is-not-correctness falsifier the RQ wants is not in the abstract; nearest reddit-grounded evidence is items 2, 6, 8 above.

**RQ2 (precommit / quorum / mesh primitives for non-reclaiming seats):** The best primitives this month are practitioner-grade, not papers: row-lock-per-task Postgres claim ownership (item 1); idempotency key + renewable lease + durable checkpoint + append-only event trail to make recovery exactly-once (item 1); per-kind attempt caps and spend circuit-breakers over a shared task board (item 3); read-only-role enforcement so the coordinator physically cannot absorb worker tasks (item 5). Perimeter: taint propagation plus the cross-boundary state persistence taxonomy (item 4) is the rule for anything flowing through shared volumes or redis, i.e. our shared inbox.

**RQ3 (topologies avoiding hidden-director collapse at 10-50 width, long-horizon):** No published topology study at that width surfaced on reddit this month (negative finding). Practitioner evidence: capability-stripping beats prompting ("every time a planner could edit, it stopped delegating", item 5); divide-the-problem-surface swarms with human-expert review of swarm-consensus output (item 6); priority-shedding under backpressure at 400-width (item 7). The 109-incident study (item 4) shows the privileged orchestrator is precisely where poisoned state lands, so: flatten privilege and taint-check the handoffs.

**RQ4 (awesome-rsi entries clearing the falsifier bar):** First-hand read of the lobehub/awesome-rsi README (raw.githubusercontent.com/lobehub/awesome-rsi/main/README.md, fetched this session; held card is watch/inbox/awesome_rsi_drop_20261010/CARD.md). NO entry reports longitudinal cost-per-outcome; no entry publishes repeated-task-class improvement curves over time; no entry runs a strict deterministic-arm control. Nearest instruments: SEABench ("paired evolving and non-evolving agents" to attribute failures to self-updates), SoL-Pi (44.7-49.0% token-traffic cut on EdgeBench, per-outcome efficiency but not longitudinal), "LLMs Cannot Self-Correct Reasoning Yet" (negative result). Verdict: nothing on the list clears the estate's bar; SEABench's paired-arm design is the closest existing instrument to copy. Independent corroboration that the bar is uncleared: item 2 (engineering passes, research judgment fails when authors grade) and item 8 (weak evaluators manufacture fake RSI signal).

## Overlap checks run (commands + results)

- `grep -c -i -F "<phrase>" catalog/catalog.jsonl` for: "RSI is not happening"=0, "Agent Substrate"=0, "never letting it write code"=0, "task board"=0, "container escape" and "container escapes"=0, "rewrite its own code"=0, "stopped delegating"=0, "row lock"=0, "2607.27191"=0, "artificium"=0, "400+ LLM agents"=0, "Supervisor Security Harness"=0, "GPT-6.1 Sol"=0, "Multi-Agent Self-Supervision"=1 and "2610.12176"=1 (the held mass_sakana card, expected, not re-banked), "Riemann"=22 (all Riemannian-geometry / mathlib / unrelated intake cards, not this thread).
- `grep -r -l -i` over memory/ for the title/phrase set: no matches (exit 1).
- Both drop-card dirs grepped for "reddit|2607.27191|RSI is not happening": no matches, so neither card holds any of this sweep's items.
- CMaNGOS=34 catalog hits are our own vendored trees (tortoise-wow, vmangos-core, corpus/library/mod-playerbots): infra adjacency, not content overlap. The "MMO" grep was polluted by substring matches (e.g. "common") and is discarded as a signal.

## OWED / not done

- Paper body of 2610.12176 still not read first-hand beyond the abstract page (the card's flag stands); authorship-vs-"sakana" label needs the PDF.
- codeminer.io two-parter behind item 8 not fetched.
- No r/LocalLLaMA thread exists on 2610.12176 as of 2026-10-10 (searched globally via the mirror); re-check after wider viralization.
- awesome-rsi entry claims are list-level (README descriptions), not per-paper verifications.

== END SUPERSEDED CONTENT ==
