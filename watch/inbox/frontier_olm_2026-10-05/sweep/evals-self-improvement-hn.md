# Frontier sweep: evals + self-improvement via Hacker News, 2026-10-05

Seat: sweep-evals-self-improvement-hn (dynamic workflow actor). Door: HN Algolia API
(hn.algolia.com/api/v1/search + /search_by_date, tags=story,
numericFilters=created_at_i>1788566400 = 2026-09-05T00:00Z, i.e. last 30 days), then
news.ycombinator.com/item?id=... for threads. No door 403s; every fetch below returned 200.

## Pass 1: broad sweep (66 candidates considered, last 30 days)

SWE-bench family: Real-SWE (49676820, 275pt), danluu bad-benchmarks (49655621), SWE-bench
Docker-socket issue (49709608), Coding Agents Have Converged arXiv 2609.17394 (49723395),
SWE-Bench Multimodal (49704056), SWE-Bench Pro harness-cost (49639415), Swesweep (49923102),
DeepSWE defects 37/113 (49766208), parallel test-time scaling (49815925), Benzi (49599867).
Local/small models: Mozilla local-LLM-servers bench (49742415), Transformers-runs-llama.cpp-quants
(49812339), llama.cpp Decision Models (49934323), Intel Arc 2.2x (49876817), IttyBittyAI 0.5B
(49835080), Swift-Qwen3.8-27B (49727511), Fine-tuning Qwen3.5-4B (49897103), Oh My Pi tuning
(49711316), Splash Engine (49765787), Magnitude Launch HN (49911995), Reflex Engine (49903234).
Self-improvement: Auto-autoresearch on NanoChat (49716123), Continual Harness arXiv 2605.09998
(49619356), Autoheal $7.9M (49877333), Novus (49609555), RPi5 voice agent (49898897),
Self-Improving AgentOrchestrator (49787764). Evals craft: Are your AI evals measuring the right
things (49965723), Automating eval design and hillclimbing (49962903 / 49920520), Rare Failure
Eval (49961283), Writing Evals 4-Step Loop (49956391), Embedded Evaluators (49951195), Inspect
AISI (49910150), practical AI evaluation pattern (deepsense, 49931859), Causeval (49930810),
hamel auto-evals (49916869), Glance (49910385), Choplifter agent eval (49940599), GRPO credit
assignment (49934012), Cognition SWE-2 Terminal-Bench 92.8 (49646778), JevBench (49800574).
Ledger/health: Doyouok dead-man switch (49796714), Pingtastic heartbeat cron (49710478),
OpenAPPA guardrails (49877515), weave router (49911500), Token compression CLI (49911910).

## Pass 2: deep reads (10 fetched end to end, this session)

1. https://rekursiv.ai/blog/autoautoresearch/ + thread 49716123
2. https://claude.dev/blog/automating-eval-design-and-hillclimbing/
3. https://deepsense.ai/blog/the-top-scoring-model-is-not-always-the-best-production-choice-how-to-evaluate-ai-systems-beyond-public-benchmarks/
4. https://duane.sh/a/fine-tuning-qwen-local-minutes
5. https://danluu.com/exercise-7/ + thread 49655621
6. https://doyouok.com/
7. https://news.ycombinator.com/item?id=49911995 (Magnitude, 99 comments)
8. https://sgaud.com/texts/ai-evals
9. https://blog.mozilla.ai/benchmarking-local-llm-servers-llama-cpp-llamafile-lm-studio-and-ollama/
10. https://inspect.aisi.org.uk/

## Answers by research question

Q1 (public agent evals for 2B-8B local models, cheap, CPU-only hosts). Honest negative: no
item in the 30-day window demonstrates grading a 2B-8B model on a CPU-only host with an agent
suite. Closest witnesses: Mozilla's server benchmark grades Qwen 0.8B/9B/27B across
llama.cpp/llamafile/LM Studio/Ollama but ran every perf test with GPU offload and measures
throughput only ("It does not yet measure time to first token, end-to-end latency, model-loading
time, memory use, power consumption, or concurrent requests"); it does note these tools "retain a
CPU path that can keep older hardware useful". Inspect (UK AISI) is the practical harness: 200+
pre-built evals, agent+CTF tasks, Docker/K8s sandboxes, "local inference with HuggingFace, vLLM,
and SGLang" (llama.cpp not named on the landing page; CPU path exists but unverified here).
Magnitude (Launch HN 49911995) autotunes a Rust llama.cpp-class engine on your actual hardware;
M5 Max users reported it about 2x SLOWER than llama.cpp, a live reminder that small-model perf
claims need the estate's own bench. Estate translation: keep the Gero-4B admission battery on
llama.cpp GGUF + Inspect-style small task set; assume no free CPU-only public suite exists.

Q2 (self-improvement loops with gates+ledgers vs claiming, falsifiers). Three strong hits.
(a) rekursiv.ai "Auto-autoresearch": 6,164 experiments in 3 days on Karpathy NanoChat, and the
verification shape is exactly our ratchet: a Trackinizer graph DB ledger (15,099 nodes) records
intents/artifacts/analyses; an evidence worker records results, then "The coordinator
independently qualifies" them "without backdating that decision to when the evidence became
ready"; failed panels stay in the ledger as falsifiers (trigram 0.9751 vs parent 0.9686 kept;
"35 completed panels unqualified" as an audit gap). (b) claude.dev hillclimbing: one-patch-at-a-
time loop where "if the train set improves but the test set is flat, Claude suspects overfitting
and reverts the patch"; grader determinism is tested by running the grader twice on the same
output; a noise gate must be smaller than the smallest improvement you'd act on. (c) Magnitude
thread: a user gates agent-made optimizations "unless it is larger than 5% and no regressions",
and the sharpest line of the sweep: "the bottleneck is not making the agent smarter, it is
verifying that each claimed outcome actually happened". danluu supplies the falsifier discipline
for the graders themselves: re-running the LLM grader 10x flips about 23% of verdicts; arbitrary
LOC thresholds turn continuous quality into coin flips; "it's often better to avoid making up a
fake number than to assign a meaningless number". Descent-protocol mapping: all three loops ARE
the ouroboros (frontier reasoning returned to estate instruments) already specified in
RIB_THE_DESCENT_PROTOCOL; the falsifier leg (spend theater) is independently re-derived here.

Q3 (health checks so burn/usage ledgers never go dark; auto-revive). HN's window yields
consumer dead-man-switch services, and their shape is the design: Doyouok: "Uptime monitoring
asks whether a server responds. Doyouok asks whether the job actually ran"; a job pings an HTTP
check-in URL per run, and "If no check-in arrives within the interval you set, we'll alert you
immediately", with duration-based intervals (no DST traps), one escalating reminder at 2x
interval, and Automatic Recovery Alerts when the check reports in again (that is the revive
signal, not an auto-restart). Estate translation for the burns ledger silence (693 rows, last ts
2026-09-28T13:45Z per the ask): every ledger carrier (tools/hermes_burn.py, census patrol,
FTS daily) should emit a success ping to a watchdog; a missed-interval alert IS the day-7
silence detector; the alert should trigger the same rebuild-and-verify path the FTS gate uses.
deepsense adds the monitoring principle for the ledger's contents: "alert on changes in
variance, not just changes in the mean", and any material change triggers a full re-evaluation
to "Re-Earn the Deployment Decision".

Q4 (minimum viable battery before admitting an uneval'd small model to a tier, the Gero-4B
gate, repeatable). Three independently-derived batteries converge: (1) duane.sh replaced
Gemini 2.5 Flash-Lite with a fine-tuned Qwen3.5-4B: blind position-rotated LLM judge on 631
held-out excerpts (usefulness 1-5 + error counts), a programmatic "Jev" classifier for restated
lines, 234 retrieval queries with top-1 hit-rate (76% vs 50%), grader-vs-judge agreement check
("agreed 95% of the time"), checkpoint chosen by judged error rate (step 80 guessed less than
step 100), then cost per production unit (-71%). (2) deepsense's pre-launch gate: repeated
trials, trajectory grading (Evidence/Execution/Deliverable layers), failure analysis, go/no-go;
report trials, mean, stdev, first-attempt success, cost per successful outcome, critical-failure
rate; pass^k not single-run; "A model wins a benchmark, but a system earns deployment". (3)
sgaud's 4-step loop: freeze snapshot+versions so runs replay, SME-label about 20 runs, write the
rubric AFTER grading ("since your idea of good changes once you see real runs"), then an
LLM-as-judge validated against SME labels and re-checked for evaluator drift; regression rule:
"Everytime you change a prompt, add or update or delete a tool, change model, add or remove an
MCP or change the harness, you should run the dataset". Union of the three = the repeatable
Gero-4B gate: frozen harness + held-out tasks (20 to 631) + blind judge + judge-agreement check +
grader determinism run-twice + pass^k with variance + cost-per-success + go/no-go + a named
falsifier (revert on train-only gain).

## Overlap check (what I ran)

findstr sweep first attempted; FAILED (zero output on a known-present token "ratchet",
literal %errorlevel% printed); long JSONL lines break findstr. Not trusted, redone.

Catalog: PowerShell single-pass over catalog/catalog.jsonl (312,694,731 bytes, Get-Item length
verified; script sweep/fast_overlap.ps1): ZERO hits for all 24 patterns (Auto-autoresearch,
rekursiv, NanoChat, danluu, Senior SWE-Bench, Benchmarking Local LLM Servers, inspect.aisi,
AI Security Institute, Qwen3.5-4B, duane.sh, Terminal-Bench, DeepSWE, SWE-Bench Pro, sgaud.com,
JevBench, Swesweep, Magnitude, Doyouok, hillclimbing, deepsense, Re-Earn, dead man, heartbeat).
Full catalog leg completed before the job was stopped.

watch/inbox (where sweep receipts land): 8,048 .md/.txt/.json files scanned one-pass
(sweep/inbox_overlap.ps1), zero hits on all 19 patterns, so none of today's banked items were
previously banked by a sweep receipt.

memory/ tree: 502,883 files; full scan impractical (stopped after partial). Partial results
from the slower per-pattern scan + line grabs: topic-adjacent grep TRACES only:
memory/trajectory/steps.jsonl:40452 (2026-10-01 grep incl "auto-autoresearch, NanoChat,
Trackinizer, DeepSWE"), :47023 (2026-10-03 grep incl "danluu", "rekursiv", "hillclimbing"),
:34014 (2026-09-29 grep incl "NanoChat", "JevBench", "Continual Harness", "2605.09998"),
:37651 (2026-09-30 grep incl "Senior SWE-Bench", "napkin math"); NanoChat as a Karpathy
tweet in memory/runs/fleet_round/burn2b_pack.md:11937 + missed_pack.md:11906; ONE real
prior bank: Mozilla local-LLM-servers in memory/runs/gapwave/hn_x_fanout/local_serving.md:22
("### 2. Mozilla AI - Benchmarking local LLM servers ... data point from 16GB APU"), so the
Mozilla item is NOT re-banked today; it is cited here as a witness only.

## Caveats

Quotes were extracted by WebFetch's reader; each is returned as an exact sentence, but the
reader model is one step removed from raw HTML. Confidence per item reflects that.

Date fields use the HN story created_at from the Algolia API (the pages themselves did not
expose parseable dates in fetched markdown).

The memory/ overlap scan is PARTIAL (502,883 files; full enumeration impractical this run).
The catalog and watch/inbox legs are complete. Residual risk: an unindexed draft note in
memory/ could contain one of these items; the trajectory traces above are the known touches.

Helper scripts overlap_check.ps1, fast_overlap.ps1, grab_lines.ps1, inbox_overlap.ps1
live in this directory as the run's receipt of the overlap methodology.
