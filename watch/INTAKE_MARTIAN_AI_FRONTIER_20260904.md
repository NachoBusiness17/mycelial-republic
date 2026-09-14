# INTAKE CARD — MARTIAN "AI FRONTIER" / CAPABILITY-FRONTIER ROUTING (akshay_pachaar, 2026-09-04)

[SOCRATIC] assumption attacked: "82% fewer errors" reads as a router you can deploy — it is
actually an ORACLE CEILING (hindsight selection + perfect judge), a measurement of headroom,
not a product claim · instrument used: whole-conversation fetch (web_reader), corpus sweep
(memory index + watch shelf), external receipt chase (arXiv/OpenReview/product coverage) ·
what survives: the headroom-measurement METHOD and the dashboard pattern; the deployable-router
reading dies on the paper's own conditions.

## ITEM (verbatim)
https://x.com/akshay_pachaar/status/2095575252445405466?s=20 — @akshay_pachaar, Sep 3 2026.
Root post: "Researchers found a surprisingly simple path to 82% fewer LLM errors. Instead of
searching for one universally best model, they combined the strengths of many. 21 LLMs were
evaluated across 16 benchmarks, running every model 10 times on each prompt. Different models
failed on different problems. Even the same model could fail once and succeed on another
attempt. So they calculated what happens when the optimal model is selected for every prompt.
At matched cost, this reduced the average error rate by 54% compared with the best individual
model. It also matched SOTA quality at 85% lower cost. With up to 10 answers and a perfect
judge selecting the best one, the error reduction reached 82%. Model routing itself is not new.
What is new is measuring its true ceiling while correcting the statistical bias created by
selecting lucky results from noisy runs. Production routers do not select perfectly today and
this research reveals how much performance existing models may already contain when used
together. Martian also turned the research into AI Frontier, an interactive dashboard for
exploring the results, and I worked with their team today."
Thread: @withmartian reply — "We got 46% fewer errors than the single best LLM across the 16
most used benchmarks (TerminalBench, LiveCodeBench, etc) ... every benchmark misses the
majority of model capabilities." Sharpest reply: @botzr_research — "The number I would want
before the ensemble math is run to run variance. Same prompt, same model, 10 runs: how much of
one model's failure is a systematic gap versus one bad sample getting outvoted?" (unanswered).
@AGTPinsights: AI Frontier = "compare 44 LLMs side by side on quality, real-world cost, and
reliability, not just leaderboard scores ... backed by an ICLR [workshop]".

## RECEIPTS (what the fetch + chase proved)
- Whole thread fetched via web_reader (login-wall below visible replies — deeper tree walled).
- Paper EXISTS: "The Capability Frontier: Benchmarks Miss 82% of Model Performance",
  arXiv:2606.26836 (Martian; Fowler, Smith, et al.), ICLR 2026 DATA-FM Workshop Oral.
  Single-model correction → 54% error-rate reduction; +single-run correction → 82%; formalizes
  routing-selection bias; Pareto frontier over model SETS.
- Third-party follow-up already exists: "What Does a Routing Oracle Measure Under..."
  (OpenReview 4AcZwTNDJq) — the oracle critique is live in the literature.
- Dashboard EXISTS per third-party coverage (TestingCatalog: 44 LLMs, quality/cost/reliability);
  my guessed path withmartian.com/ai-frontier = 404 (exact URL sits behind X "Show more").
- Vendor production claim: 52.4% error reduction + 92% cost reduction in one customer
  deployment (withmartian.com/post/up-and-to-the-left) — vendor-reported, Unproven-by-us.

## SCORE — F:5 P:3 C:4 W:3 N:3 = 18/25 → **BUILD WINDOWED**
- FIT 5: lands on FOUR open arcs — token-render-manager R1-R5 router spec (build-gated),
  burst-doctrine per-job routing table, Cache Econ deck, flight-recorder telemetry.
- PULL 3: promo-shaped post, three protocol-different numbers under one headline; the METHOD
  pulls, the post itself is marketing.
- COST 4: the falsifier is a $0 replay of our own rows.
- WINDOW 3: night-window legions + 1-day-old flight recorder make the replay runnable NOW,
  but nothing decays.
- NOVELTY 3: routing tables and cascades already in corpus (R1-R5, 85-98% cascade savings);
  what is genuinely new to us: ORACLE-CEILING REPLAY as a calibration instrument + selection-
  bias correction. The dashboard pattern is a CONVERGENCE, not novelty (world arrived where
  the operator arrived yesterday).

## READ
1. INGEST: done, verbatim above. 2. MAP convergences: token render manager (K-of-N cascade,
   "85-98% savings" — same family as the post's 85%-lower-cost arm); burst doctrine per-job
   routing (9 laws); Stockfish ask_router (eval ≠ decision); cache-portability router decision
   table (bulk→Qwen, flash→free, judgment→frontier+cache); Legions honesty row ("50 dumb
   agents agreeing is not verification"); decks.html pro surface (8 decks, mission "an
   interface for you to gather data"). Two lanes (ours 08-27, Martian's ICLR workshop)
   arriving at the same organ = signal.
2. ASSERT (steel-man): because different models fail on different prompts — and the same model
   fails on retries — the per-prompt best model hides up to ~82% recoverable performance that
   single-model single-run benchmarks cannot see, and measuring that ceiling properly requires
   correcting the selection bias that "lucky runs" inject.
3. ATTACK (failure causes, with evidence):
   a. ORACLE ≠ ROUTER: 54%/82% are hindsight numbers ("optimal model selected for every
      prompt"; 82% needs "a perfect judge" + 10 answers = 10x compute + judge cost, which is
      NOT the "85% lower cost" arm). Production routers must predict BEFORE running; the post
      concedes this ("production routers do not select perfectly today") and the follow-up
      paper interrogates exactly what the oracle measures. Judge bias is OUR known failure
      mode too: seed_percolator runs a null-variant canary precisely to halt judge bias.
   b. BENCHMARK ≠ WORKLOAD: headroom measured on 16 benchmarks; our own DESIGN LAW is
      "benchmark must look like the work" (flight recorder), and intake genre rules reject
      eval-by-questionnaire class items. @botzr_research's run-to-run variance question
      (systematic gap vs outvoted bad sample) is unanswered in-thread.
   c. HEADLINE DISSOLVES UNDER TRI-STATE: 82% (perfect judge), 54% (matched-cost oracle
      routing), 46% (Martian's own reply, 16 benchmarks) — three protocols, one number quoted
      at parties. The post is honest in the fine print and misleading in the bold.
4. MEASURE (ran): product-liveness falsifier — paper + dashboard + ICLR venue all confirmed
   via external sources ($0, one search round); guessed URL 404 = exact dashboard path stays
   Unproven. WRITTEN KILL CONDITION for the thesis ON OUR WORKLOAD ($0): replay flight-
   recorder rows; for each row ask "had a different lane served it, per burst-doctrine costs,
   what error/latency/cost delta would hindsight selection buy?" If oracle replay <10% better
   than the current routing table, routing headroom is DEAD for our mix; if ≥25%, a per-prompt
   router arm graduates from R1 calibration to BUILD. Executor needs ≥200 rows/lane —
   recorder is 1 day old; check row depth first.

## TRI-STATE
- Supported: paper + dashboard + workshop venue exist (arXiv:2606.26836; TestingCatalog;
  OpenReview); different-models-fail-differently is consistent with our own lane telemetry.
- Disputed: the headline as read — "82% fewer errors" is an oracle ceiling requiring perfect
  judge + 10 answers, not a deployable router result; deployable arm is 54% at matched cost,
  vendor-reported 52.4% in one production case.
- Unproven: headroom on OUR workload (kill condition written, rows too young); run-to-run
  variance decomposition (thread's own open question); exact AI Frontier URL (404 at guess).

## VERDICT
**BUILD (windowed)** — not a router build; a MEASURE build. The oracle-replay falsifier rides
the flight recorder once row depth ≥200/lane (or the next legions tranche generates it), and
its output becomes the calibration table for token-render-manager R1. The dashboard pattern
 finding (interactive decks as the AI's data-gathering surface — quality/cost/reliability
columns) is same-day convergence with decks.html and feeds the X-scout deck-column design
(PAIR PATTERN): AI Frontier is a candidate EXTERNAL column for the Cache Econ deck.

## ROUTE
- CONSUMES IT: MEASURE spoke (autonomy wheel) over Cache Econ telemetry → R1 router
  calibration; scout deck columns (external dashboard harvest).
- FORBIDS: spawning a "build a router now" off this post — violates the token-render-manager
  operator GO-gate AND Stockfish "eval ≠ decision". This item is ammunition for a specced
  organ, not a new organ. Placement failure IS the finding.
- PAID RENT ON: confirmed the operator's pro-surface mission from the outside (world built
  the same shape for model-shopping the same week we built ours for fleet intake); handed a
  $0 falsifier that upgrades burst-doctrine routing from "9 laws" to "measured ceiling".

## THE CROP
Did NOT see: the paper's bias-correction math (title/claims only — abstract-level); the AI
Frontier dashboard itself (exact URL walled; operator's logged-in browser or scout lane opens
it in 30s); the login-walled deeper reply tree; the flight-recorder row-depth check (replay
underpowered until ≥200/lane). Chair that should sit next: the ECONOMIST (replay cost-arm
math, judge-token budget) with the driver lane executing the replay as a MEASURE spoke.

— Receipt: this file + room row (intake.scored, watch/room.jsonl), 2026-09-04.
