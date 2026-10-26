# Sweep write-up: evals-self-improvement via reddit - 2026-10-11 (run 2, amended)

source-fetched: adhoc

Seat: sweep-evals-self-improvement-reddit (dynamic workflow gopher, second reddit pass on this area today). This file amends, not replaces: the same-path bank minted earlier on 2026-10-11 by the prior window's actor is preserved byte-identical as `evals-self-improvement-reddit.prior-20261011T2103.md` (16,961 bytes; it banked 1wv0lww FRAMES dual-judge, 1wiag69 tau2 pass^3, 1wqag1i Mica, 1wy9q9e known-correct gate, 1x0etwe blind preference, 1x0gaqv tuieval, 1x1tf1t open-weight benchmark, 1wgazy4 RSI-held-out - all eight remain estate holdings and NONE are re-banked here). Zero item overlap between that bank and this one's seven.

## Door report (all doors re-tested this session, 2026-10-11 ~20:30Z)

Degraded, from this vantage at this hour:
- old.reddit.com .json AND HTML (top pages, search, per-thread): login wall shell ("Log in to use old Reddit"), via both WebFetch and the webReader MCP.
- www.reddit.com top.json: HTTP 403 Blocked; www.reddit.com thread HTML via webReader: "Please wait for verification" interstitial.
- api.pullpush.io: HTTP 429 Too Many Requests.
- redlib.catsarch.com: HTTP 429.
- WebSearch (the recipe's named fallback): the backend rate-limit-stormed (MCP 429 "1302" on most attempts, matching the account's fan-out width law) and when it did answer it ignored `site:` and the allowed_domains filter, returning dictionary noise; it surfaced exactly one usable reddit thread id (1tcu5r8) and the AgenTracer paper trail as non-reddit leads. Fallback quality: poor but not zero.

Working door (used for everything banked below): the Arctic Shift Reddit API (`arctic-shift.photon-reddit.com/api/posts/search`, `/api/posts/ids`, `/api/comments/search?link_id=`), driven serially by repo-venv urllib with 4-6 s pacing and single-token queries (multi-word `query=` values 422 about half the time). Door limits, disclosed: full-text keyword search only (no ranking-by-score endpoint), comment ingestion lags, and `1wrzoej`'s r/ML crosspost arrived with `[removed]` selftext (dropped unread). The prior window's doors (redlib.nadeko.net via webReader, per-thread .rss) were NOT retested this session and are not claimed.

## Pass 1: broad sweep census

Two harvest rounds over r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama, `after=2026-09-11`, 33 query terms: 456 unique posts collected to `tmp/candidates.jsonl` (round 1: 44 uniques; round 2: +412). Well past the 30-item floor. Screening removed the hardware/serving flood (Strata builds, tok/s reports, GPU rigs). On-area survivors clustered on the community's judge-model wave: the "Jev" ecosystem (TypeSafe's closed System One decision model), its open challengers (Laya, CLM, NIRNAY, typevet, Jeff), judge-reliability experiments, per-phase agent attribution, and gate/telemetry practice.

## Pass 2: deep reads performed

Eleven threads fetched end-to-end via Arctic Shift (full post selftext + comment tree, 100-comment cap): 1wjieap, 1wouby6, 1wgii3h, 1wnyf0o, 1wy9q9e, 1wuz83t, 1x357dq, 1wjgthj, 1wm4wu2, 1wtmz2p, 1wnt9ae. Seven banked below. Four read and NOT banked, with reasons in the dedupe ledger.

## Banked items (strongest first; all quotes verbatim from fetched post/comment bytes)

### 1. Laya: the open-source Jev, trained with RLCD against proper scoring rules (r/LocalLLaMA, 2026-09-18, u/Nandakishor_ml, 745 pts, 126 comments)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wjieap/made_the_horizontal_opensource_model_for_jev_with/
Quote: "The RLCD(unofficial, btw) I did is a policy-gradient reinforcement learning approach that kinda optimizes decision models against strictly proper scoring rules, ensuring maximum reward is achieved only when outputting true, mathematically calibrated probabilities."
Why: the open-weights calibrated judge now has a public training recipe: 421M-param non-autoregressive decision model (ModernBERT-large bidirectional encoder + scratch Transformer head scoring [MASK] option markers, ~35 ms forward pass), trained on one RTX 6000 Pro over 25,000+ human-annotated examples (intent routing, fact-checking, moderation consensus, guardrails, rubric scoring, multi-turn trajectories, zero synthetic shortcuts), with the RL objective spelled out as proper-scoring-rule optimization - reward maximized only on calibrated probabilities. This is the concrete build of the judge-two instrument the RQ1 line wants: cheap, cross-family, calibration-trained, abstention-capable. Comments temper it: 512/1024-token context limits drop-in use vs Jev's 32k-64k (u/R_Duncan), and the author shipped a typed-decisions variant the same week.
Steal: proper-scoring-rule RL as the training objective for any estate-trained judge; 25k human-annotated decision corpus as the data shape; ~35 ms verdict cost makes per-dollar-routing verdicts affordable.

### 2. CLM vs JEV: open contrastive alternative, verifier numbers included (r/LocalLLaMA, 2026-09-24, u/R_Duncan, 410 pts, 180 comments)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wouby6/jev_almost_dead_clm_vs_jev/
Quote: "When fine-tuned on agent trajectories, CLM achieves state-of-the-art verifier performance on **Terminal-Bench 2.1 (87.6%)** and **DeepSWE (81.6%)**, whereas zero-shot Jev struggled on those exact benchmarks (scoring \~71% on DeepSWE)."
Why: the judge-family comparison with the numbers the estate's RQ1/RQ2 need. CLM implements Jev's exact three primitives (Choice / Noul / Score - categorical distribution, calibrated true/false, rubric score), is drop-in client-compatible, separates a state head from an action head so action embeddings cache (4x-13x faster on browser/gaming agents), ships ~75 MB fine-tunable heads, and (the RQ2-relevant leg) trajectory fine-tuning turns it into a verifier that beats zero-shot judging on failure attribution benchmarks. Costs stated plainly: zero-shot broad knowledge and 64k context stay Jev's edge (BFCL v4: 99.2% vs 95.2%). Comments frame the adoption question: TypeSafe is "the corporation best positioned to offer fine-tuned-classifiers-as-a-service" (u/Smallpaul), and the flood of five-minute clones shows most builders miss how much engineering the real product carries (u/xienze).
Steal: judge-two selection by residual-error complementarity has a build path - fine-tune the open judge on OUR agent trajectories; verifier quality is measurable on Terminal-Bench/DeepSWE-class suites; the Choice/Noul/Score primitive triple is a clean interface spec for a verdict schema.

### 3. typevet: calibrated per-label answers at home, with abstention and a position-bias probe (r/LocalLLaMA, 2026-09-29, 5 comments)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wtmz2p/jev_at_home_but_it_can_see_typed_yesno_pickone/
Quote: "No sampling, no parsing. typevet composes the native Gemma 4 turn itself, ends the prompt with the empty-thought no-thinking prefill, and reads the next-token distribution over the allowed answer tokens only."
Why: the calibrated-judge instrument built from parts the estate already runs. Per-label probabilities read straight off the next-token distribution over allowed answer tokens (no sampling); three-label Choice with match/mismatch/insufficient_evidence as an abstention channel - on masked receipts it abstained 6/6; label-order reversal flipped 0 of 18 answers (a position-bias probe, the exact control the prior window's RQ1 verdict called OWED); and an evidence-arrival gate that fails if the image did not actually add prompt tokens (the FRAMES lesson "checker must see everything the model saw", enforced mechanically). Receipt test: swapped-digit totals scored match at 0.99964 text-only but mismatch at 0.99999 with the photo. Comment thread is snark ("the 3,097th person to make their own Jev", 9 pts) - itself a monoculture datapoint for RQ1's family-dominance question.
Steal: read judge probabilities from the constrained next-token distribution, not from sampled text; build insufficient_evidence as a first-class label; run the label-order flip and token-arrival gates on every judge the estate deploys.

### 4. Pre-execution gate: verdict authority outside the model (r/MachineLearning, 2026-09-18, [P])

URL: https://www.reddit.com/r/MachineLearning/comments/1wjgthj/a_preexecution_gate_that_stops_llms_from_filling/
Quote: "Executions get logged; verdicts don't. The log keeps the tool that was called and the final arguments, but not where each value came from or which conditions were checked."
Why: RQ5's incident class named from outside. The post's mechanism: declare outside the model what must be verified (checklists as data - slots with slot_id, status, route), verify in code, record the verdict, and let execution read only the recorded result; unknown slots route to ask_user instead of being hallucinated (a transfer with a model-invented account number passes every schema check). The quoted sentence is the missing-REGISTRY-row disease verbatim: artifacts land, the verdict trail does not, so the postmortem cannot tell looked-up from invented. Directly answers the ask's fifth question: the gate's self-steal ratchet holds only when the verdict row is part of the run's artifact contract - declare, judge, record, execute, with the record written by the gate, not by the gated.
Steal: slot-level verdict records (what was checked, status, route) as the REGISTRY row's content model; unknown_count > 0 blocks execution; the postmortem observability rule - what was not observable before execution must not stay unobservable after.

### 5. Laya came first, so why is everyone only talking about Jev? (r/LocalLLM, 2026-09-23, 54 pts, 42 comments)

URL: https://www.reddit.com/r/LocalLLM/comments/1wnyf0o/laya_came_first_so_why_is_everyone_still_only/
Quote (u/Murder_1337, 12 pts): "Jev you can plug and let shadow run to learn so much easier to set up and use case its night and day"
Why: RQ1's "which family takes every dollar-routing verdict" answered as adoption economics, not quality. The open first-mover (Laya) lost the verdict flow to the funded closed generalist (Jev) on setup friction alone; commenters who tried both report Jev answers MCQ-grade questions out of the box while Laya is "not much better than chance as-is" until fine-tuned to the domain (u/Squidgical), and financial-data users stay on Jev for exactly the plug-in property. One comment flags the fine-tuned middle path (custom-trained Qwen beats both where it applies).
Steal: judge-two routing should not converge on one hosted family for convenience - per-domain fine-tuned open judges win where trajectory data exists; adoption friction (shadow-run, zero-config) is a real selection axis the estate must counter with equally-frictionless local judges.

### 6. Qwen3.8-27B as coding executor across 6 phases, hidden tests + adversarial review (r/LocalLLM, 2026-10-01, 24 comments)

URL: https://www.reddit.com/r/LocalLLM/comments/1wuz83t/i_benchmarked_a_local_qwen3827b_as_a_coding/
Quote: "When Claude hands it the full code (\"full-code\"), it was correct 42/42. On seeded-bug debugging it went 9/9."
Why: RQ2's attribution shape, community-built. 51 runs split by handoff style - full-code 42/42, seeded-bug debug 9/9, but interface-only 0/3 on lifecycle/concurrency, DST rules and reimplementations; local 43/51 vs Sonnet 5 45/51 at 3.6x wall time and $9.20 avoided. Scoring is three-layered: visible gates (typecheck, lint, task tests), hidden acceptance tests the model never sees, and adversarial diff review by fresh Claude reviewers who must verify every suspicion with real scripts. That layering is the skill_ledger schema in miniature: record which phase/handoff class failed, not just the run.
Steal: per-phase (plan/transcribe/implement/debug/review) verdict rows with failure attributed to handoff class; hidden acceptance tests plus adversarial review as the two non-interested graders; the full-code vs interface-only split is the module-substitution map for dollar routing.

### 7. Typed Evals: calibrate each metric against human pass/fail (r/LocalLLaMA, 2026-09-23, 1 comment - weak signal, banked for the recipe only)

URL: https://www.reddit.com/r/LocalLLM/comments/1wnt9ae/using_jev_to_evaluate_llms_rag_and_agents_not/
Quote: "**Judge scores + human pass/fail labels → fit per-metric calibration → validate on held-out examples → apply to new scores.**"
Why: the plainest statement of the calibration loop the RQ1 instrument question needs, plus the three-layer evaluation split (LLM response / RAG context support / agent-and-tool trace) that maps onto our module census. The author's own caveat matters: calibration grounds score interpretation, it does not improve the judge's detection, and the mapping must be refit when task, rubric, or judge changes (the same judge-specific-policy finding the HN sibling banked from Red Hat AI Safety). Single-comment thread, LLM-content rule-flagged by a mod - held as a recipe lead, not evidence of community validation.
Steal: per-metric calibration fits validated on held-out human labels, refit on any judge/rubric change; the response/context/trace three-way split as the eval-case taxonomy.

## Dedupe ledger (read but not banked, and why)

- 1wy9q9e (small models write tests + code, 77% false rejection): banked hours earlier as item 4 of the prior reddit window at this same path; prior file even carries the correction-edit split (42% did-not-run; 60% of running suites rejected). Not re-banked.
- 1x357dq (standard evals can't tell quants apart): banked by the quantization-compression lane (`quantization-compression-reddit.md`, grep hit on "1x357dq" and "quants apart"). Its harness-variance comment (u/himiaoxin: same model and quant 15 points lower from a mangled tool-call parser, "now I log the template hash next to the quant hash") is noted here for RQ4 and left to that lane.
- 1wgii3h (DeepSeek engineer RSI reflections): post + full comment JSON already in the estate from the 2026-10-06 sweep (catalog rows `post_1wgii3h.json` / `com_1wgii3h.json`, catalog.jsonl lines 1013442/1013452; "burying my talent" also in catalog). Not re-banked.
- 1wm4wu2 (1,000+ telemetry events across 38 deployments): read; the only durable lesson (u/ChoiceAnalyst1599: version marker inside the workflow format from day one, else "you are guessing what format the user have and everything breaks silently"; anonymous error reports with stack + environment) is RQ3-adjacent ops wisdom below banking strength. Left as overflow.
- 1wrzoej (Laya tutorial crosspost on r/ML): arrived `[removed]`; unreadable, dropped.

## Overlap instrument (commands run this session)

grep -c -i over `catalog/catalog.jsonl` and git grep -l -i over `memory/` for: thread ids (1wjieap, 1wouby6, 1wtmz2p, 1wjgthj, 1wnyf0o, 1wuz83t, 1wnt9ae - all 0/0), title phrases ("horizontal open-source model", "JEV almost dead", "Laya came first", "tell my local quants apart", "filling in missing tool arguments", "burying my talent" - 0 in catalog except the last, 1 hit, the banked RSI row), and content needles: RLCD catalog=0 but memory 15 files - the substantive one is `memory/continuity/seat_memory_20260927/jev-production-proof-20260919.md` which already records "Jev comes from a 2-year stealth effort by a ChatGPT co-inventor, trained with RLCD (new method)"; the Laya thread's NEW part is the open reproduction and the proper-scoring-rule objective, not the RLCD name. typevet / Typed Evals / typed_evals / TrustifAI / 6 phases / empty-thought / slot_id: 0 in catalog, 0 in memory sweep files. DeepSWE catalog=5: raw Temp HTML captures, not curated holdings. "laya" catalog=29: all false positives on Sentry "ReplayApi" header filenames. Sibling sweep files checked: evals-self-improvement-{arxiv,hn,x}.md and quantization/finetuning/open-local lanes - the HN sibling holds the Laya-vs-Jev quality comparison (Red Hat AI Safety: decision models did NOT beat LLM-as-judge; tuned policies are judge-specific, +17.83 pp Laya / -3.67 pp Jev), which item 5's adoption story complements, not duplicates.

## Research-question verdicts (delta over the prior window's file, from this bank only)

- RQ1 (judge number two): the open-calibrated-judge build now exists with its training recipe (item 1) and its instrument-level implementation pattern (item 3: constrained next-token probabilities, abstention label, order-flip probe, arrival gate) - the position-bias control the prior window marked OWED is demonstrated cheaply in item 3. Family dominance is adoption-friction, not quality (item 5). No reddit thread measures judge-panel IRR numerically; that answer stays with the arxiv sibling (2609.14438: panel ceiling set by error-orientation complementarity, so the calibrated instrument cannot lower IRR by itself).
- RQ2 (skill_ledger coverage): item 6 gives the row shape (phase/handoff class + hidden-test verdict + adversarial-review verdict); item 2 shows trajectory-tuned open verifiers beat zero-shot judges at failure attribution (87.6%/81.6% vs ~71%) - the ledger should record trajectories fine-tunable into verifiers, i.e. the inputs, not just outcomes.
- RQ3 (law index): no new direct evidence; overflow note only (version markers inside the format).
- RQ4 (36.3 pct question-class vs 3.6 pct family): directional support only (harness swings, phase-class failures); the exact-statistic second blind audit remains unfulfilled - falsifier still open, consistent with the prior window.
- RQ5 (missing REGISTRY row): item 4 names the law from outside the estate - "Executions get logged; verdicts don't" - and gives the schema (declared checks as data, code-verified, verdict recorded, execution reads only the record). A run landing artifacts without a REGISTRY row is unobservable-in-postmortem by construction; the ratchet holds iff the verdict row is a load-bearing part of the artifact contract.

## Fabrication ledger (OWED)

- All content came through the Arctic Shift mirror API, not reddit's own bytes; scores/num_comments are mirror-final values (Arctic Shift notes final values land ~36 h post-ingestion; today's threads may drift).
- Comment reads capped at 100 per thread (1wjieap, 1wouby6, 1wgii3h each have 118-180 total); 1wuz83t's comment tree 422'd on first fetch and was NOT retried (post body was judged sufficient; the comment layer for that thread is unread this session).
- 1wnt9ae banked as weak signal (single comment, mod rule-flag); treat as recipe, not community-validated evidence.
- WebSearch fallback was too degraded to satisfy the recipe's full intent; the Arctic Shift door replaced it. The one non-reddit lead it produced (AgenTracer / Who&When, arXiv 2509.03312) was not fetched and is banked nowhere.
- The prior window's doors (redlib.nadeko.net, reddit .rss) not retested; no claim made about their current health.
