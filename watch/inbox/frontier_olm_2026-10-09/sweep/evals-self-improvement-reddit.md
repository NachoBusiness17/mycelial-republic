# sweep: evals-self-improvement via reddit (2026-10-09)

source-fetched: 2026-10-09

## Door degradation (stated plainly)

- Recipe door `old.reddit.com/r/*/top.json` returned only Reddit's login-wall stub for all four
  subreddits (r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama). Verified twice: first via
  WebFetch ("welcome/skip-navigation placeholder", no posts), then via the mcp web-reader on
  `old.reddit.com/.../top.json` ("## Log in to use old Reddit") and on a www.reddit.com thread URL
  ("Reddit - Prove your humanity").
- WebFetch on www.reddit.com thread HTML: empty shell. Redlib mirrors: redlib.catsarch.com 429,
  redlib.perennialte.ch 403, rl.bloat.cat ECONNRESET. r.jina.ai proxy: 403 via WebFetch, network
  error via reader. pullpush.io: indexed record empty for 1wo76lo. arctic-shift.photon-reddit.com:
  HTTP 522 down on four attempts (two reads + two date probes). Wayback: no snapshot of 1wo76lo.
- Sanctioned fallback used, per the recipe: WebSearch (site:reddit.com equivalent queries). The
  search backend returned verbatim page excerpts for each thread banked below. This is a DEGRADED
  read: search-engine excerpts of the thread pages, not full-page fetches. No item below is banked
  from anything but text the search backend pulled from the thread's own page; the five-plus
  "deep reads" are multi-query excerpt pulls (2-3 distinct queries per thread), not end-to-end
  page loads. Confidence is capped accordingly.
- Dates: absolute timestamps could NOT be verified through the degraded door (arctic-shift down).
  Date anchors that ARE verified this session: r/LocalLLaMA "Harness x model combination: more
  data!" (1x0owom) was dated by the search result as around Oct 8, 2026; 1x0rx51 shares the 1x0
  id prefix and sorts newer than 1x0owom, so it is inside the 30-day window. All other items come
  from the 1w id cluster (newer than the verified 2026-07-22 anchor thread 1v3a2le, "NeurIPS 2026
  reviews out 22 July"), but a 30-day window cannot be proven for them; each carries the flag.

## Pass 1 (broad sweep, 30+ candidates considered)

Considered from ~10 searches: 1vysgf4 (r/LocalLLM skeptical of judge scores), 1ivd069, 1pm2zsb,
13xlply (2023, rejected out-of-window), 1v3a2le (Jul 2026, rejected), 1fbclkk/1fnhm67/1fjxkxy
(Sep 2024, rejected), 1wcxxm8, 1wcj5q3, 1x0owom, 1uo8lik, 1sm08m6, 1wo76lo, 1rfb7kl, 1up5owd,
1x0rx51, 1wvouoq, 1uzcfu2, 1vvgyvk, 1vr0v0d, 1wactmx, 1b933of (2024, rejected), 1vr1429,
1w2v97w, 1nqo0oo (2025, rejected), 1rpxtmf, 1wa20xz, 1wyejpd, 1s63az9 (1s cluster, likely
pre-window, rejected from items), 1wevcyx, 1whh9xa, 1wy4rjx, 1thlbhz, 1ses04t, 1vorwfg, 1ruf7l9,
1uenk8t, 1t0cqmz (1t cluster, rejected from items), b3ayhh/zay9gt/bmwer6/fbl9ho/fqt1oy/ptsbvb
(2019-2022, rejected), 1wli359, 1wemcdc, 1r3weq3 (Jan 2026, rejected from items), 1s1h4fo (Feb
2026, rejected), 1rkrbqo, 1nujohr, 1swsqgt (1s cluster, rejected from items), 1t81626 (1t
cluster, rejected from items), 1pe1bd4, 1sdy7rd (1s cluster, rejected), 1wo-cluster AA saga
(1vv80xa, 1w78wbm, 1wa3o5j, 1vhoyw1, 1wcws96), 1vgnmny, 1t9whrt, 1w9ad9q, 1sqvcz2, 1vst6ua.

## Pass 2 (deep reads, multi-query excerpt pulls)

### 1. "21 LLM judges, 541,000 verdicts, 9 providers. Raw agreement overstated real accuracy by 33-41 points on every model tested" - r/PromptEngineering (1wo76lo)

https://www.reddit.com/r/PromptEngineering/comments/1wo76lo/21_llm_judges_541000_verdicts_9_providers_raw
Verbatim (search excerpt): "Raw agreement overstated real accuracy by 33-41 points on every model
tested." Second pull: "recommends calibrating judges on held-out human-labeled sets and measuring
kappa deflation for your benchmark (e.g., MT-Bench)."
Read for RQ1 (LENS 2 blind multi-family judging / consensus illusion). This is the frontier
number for our consensus-illusion law: 21 judges x 541k verdicts x 9 providers and raw agreement
STILL overshoots true accuracy by 33-41 points everywhere - i.e., judge consensus is correlated,
not independent; agreement is not verdict. The thread's own fix (calibrate on held-out human
labels, measure kappa deflation) is compatible with our law but weaker: our LENS 2 already
demands blind multi-FAMILY judging, which attacks the correlation at its source (same-family
judges share training data and therefore share failure modes) rather than measuring it after the
fact. Frontier verdict: methods exist and are quantitative, but they treat the disease as a
calibration nuisance; the estate's multi-family + blind law is the stronger instrument. RQ1
answer: partial pass as instruments, fail as law.
Overlap: catalog scan (all 444k+ lines, venv python substring pass over candidate titles and
phrases incl "21 LLM judges", "541,000 verdicts") = zero hits; memory/ tree walk = only my own
trajectory-step echo in memory/trajectory/steps.jsonl. Genuinely new.

### 2. "Why decontamination reports can't fix benchmark contamination, and what an evaluator has to do instead" - r/LocalLLaMA (1wli359)

https://www.reddit.com/r/LocalLLaMA/comments/1wli359/why_decontamination_reports_cant_fix_benchmark
Verbatim (search excerpt): "The usual answer is a decontamination report: the lab searched its
training data and found noth[ing]". Second pull: the author explains why that approach "can't
work" for three stated reasons (n-gram/substring searches missing paraphrased or semantically
similar content).
Read for RQ1 (contamination audits). Frontier verdict lands exactly on our "trust bytes, not
reports" doctrine: an insider decontamination report is structurally incapable of proving
absence; the evaluator must hold fresh/hold-out material the labs never saw (the thread points at
rolling-fresh-issue benchmarks like SWE-rebench). Maps 1:1 to the census patrol's
self-measurement and to why our pre-push gates run OUR fixtures, not vendor attestations. RQ1
answer: frontier methods concede the audit-instrument failure; our receipt law is ahead.
Overlap: zero hits in catalog/memory for title and phrase.

### 3. "What it took to get an LLM judge from garbage to 27 of 30 agreement with humans (live, at a conference)" - r/AI_Agents (1x0rx51)

https://www.reddit.com/r/AI_Agents/comments/1x0rx51/what_it_took_to_get_an_llm_judge_from_garbage_to
Verbatim (search excerpt): judge agreed with "27 of the 30 human verdicts" only after notably
"giving it the 14-day policy at all". Presented live at a conference. In-window: id sorts newer
than 1x0owom (dated ~Oct 8 by search result).
Read for RQ1 (judge calibration). The step-change fix was not prompt sugar - it was injecting the
GOVERNING CONTEXT (the policy document) into the judge. Without the law, the judge is garbage;
with it, 27/30. Direct validation of the estate pattern where every judgment ask carries the
deterministic estate-law block (claritas face + law block) before any verdict is trusted. RQ2
aside: the 30-case human sample is small and unpowered - the frontier presents n=30 as a
calibration victory; our harness would demand the conditions-suspect re-measurement before
crowning it. RQ1 answer: calibration is real but context-starved judges fail silently.
Overlap: zero hits in catalog/memory.

### 4. "LLM-as-judge is the wrong default. Here's what works" - r/AI_Agents (1swsqgt) [context item, 1s cluster, likely pre-window]

https://www.reddit.com/r/AI_Agents/comments/1swsqgt/llmasjudge_is_the_wrong_default_heres_what_works
Verbatim (search excerpt): "The agent's final answer can look correct. Wrong tool, wrong args,
lucky recovery. End-to-[end]..." plus "pass rates wobble 5-10 points" run to run.
Read for RQ1/RQ4. Outcome-only judging cannot see process drift: wrong tool, wrong args, lucky
recovery scores the same as competence. This is the verdict-first argument: the verdict must
carry the receipt (trace), not just the outcome - our "no number without its receipt" law
formalized. Kept OUT of the top-8 items (window unprovable, likely Feb-Apr 2026 by id anchors),
kept in the bank as the cleanest statement of the failure mode. Companion: r/LLMDevs "LLM-as-judge
is not a verification layer" (1sdy7rd, same cluster).
Overlap: zero hits in catalog/memory.

### 5. "Observations from a metacognitive feedback loop (one hour of my AI agent running on its own)" - r/AI_Agents (1wevcyx)

https://www.reddit.com/r/AI_Agents/comments/1wevcyx/observations_from_a_metacognitive_feedback_loop
Verbatim (search excerpt): "Self-reflection is useful, but if the agent can explain yesterday's
failure beautifully and still repeat it tomorrow, nothing really improved."
Read for RQ3 (does any frontier self-improvement loop beat our triad). This is the estate's
DESCENT-protocol falsifier in civilian form: a loop whose ledger grows but whose behavior does not
is spend theater. The thread's observation - reflection is prose, improvement is a landed
mechanism - is exactly the day-8 mine diagnosis (32 sweeps banked into no DIGEST = the bank is
the bottleneck, not discovery). Frontier loops in this sweep are all capture-traces-plus-reflect
(1s63az9: "capture agent traces, run the agent a few times to collect data, then run an
improvement skill in your coding agent"; 1uenk8t: "most agentic loops never improve without a
feedback memory layer") - none of them couple reflection to an enforcement ratchet, a citation
lint that fails the push, or a census patrol with named instruments and moments. RQ3 answer: no
frontier loop beats the triad as a MEASURED mechanism; what the frontier has that we under-use
is the honest falsifier phrased for operators ("explained beautifully, still repeated"). The
ratchet + citation-lint + census-patrol triad remains ahead because each leg is an enforcement
site, not a memo. The unbanked-fold lesson stands: fold or it did not happen.
Overlap: zero hits for the thread; the phrase "metacognitive feedback" alone has ONE catalog hit
(catalog/catalog.jsonl:444567) but that row is a different document (local arxiv txt
state/arxiv/2026-09-18/2609.20143v1.txt, "Designing Against..."), not this thread. No re-bank.

### 6. "My trading agent's reflection loop was learning from noise" - r/AI_Agents (1wekbmy)

https://www.reddit.com/r/AI_Agents/comments/1wekbmy/my_trading_agents_reflection_loop_was_learning
Verbatim (search excerpt): "Reflections written from PnL alone conflated bad luck with bad
decisions."
Read for RQ3/RQ2. The self-improvement signal must be separated from luck before it is banked -
a reflection written from a raw outcome signal learns noise. This is the RQ2 lesson for the
emergence A/B harness in experimental-design form: without controls that isolate the condition,
your "lessons" are the variance. Feeds the same conclusion as item 5 from the instrumentation
side.
Overlap: zero hits in catalog/memory.

### 7. "Harness x model combination: more data!" - r/LocalLLaMA (1x0owom)

https://www.reddit.com/r/LocalLLaMA/comments/1x0owom/harness_x_model_combination_more_data
Verbatim (search excerpt): "I'm testing harness x model combination for my local setup, but more
importantly, I created a website for a[nyone to test their config]". Search result dates it
around Oct 8, 2026 (in-window).
Read for RQ2 (what experimental designs can the A/B harness borrow so re-measurement stops being
suspect). The community's answer to "conditions are suspect" is factorial measurement with shared
data: vary harness AND model, publish the grid, let anyone re-run their config - interactions,
not single-condition deltas. Cross-cluster corroboration from search excerpts: SWE-rebench thread
"it won't be that the model returned the wrong answer but that the harness failed" (1r3weq3, Jan
2026, out of window, context only) and "The environment around them (aka the harness) matters
much more" (1t9whrt, context only); dev.to reports the same model swinging 30-50 points on
Terminal-Bench 2.0 by harness (secondary, unverified here). Borrowable design for our A/B harness:
pin instrument versions in the receipt (we already stamp instruments and moments per census law),
run condition x instrument as a grid not a pair, publish the grid so a skeptic re-measures the
same cell. The census-carrier law (name instrument, moment, delta) is the same law wearing
estate clothes.
Overlap: zero hits in catalog/memory.

### 8. "Artificial Analysis is not 'broken', and they prove it." - r/LocalLLaMA (1wcxxm8)

https://www.reddit.com/r/LocalLLaMA/comments/1wcxxm8/artificial_analysis_is_not_broken_and_they_prove
Verbatim (search excerpt): "Look at the individual evaluation scores, understand what the
evaluations measure, a[nd ...]". 235+ upvotes; the defense responds to "Artificial Analysis
'Intelligence': A meaningless benchmark" (1vv80xa) and the r/singularity v4.3 update thread
(1wa3o5j); cross-referenced from r/DeepSeek (1wcws96).
Read for RQ1/RQ2 (instruments vs oracles). The whole saga is the estate's composite-index trap
fought in public: a single aggregated "intelligence index" is where consensus illusion and
condition confounds hide; the defense's own argument ("look at the individual scores") concedes
the composite is the problem. Lesson for the estate: keep verdicts at receipt granularity; any
rollup (rollup.json, estate index) must stay navigable to the receipt or it inherits the AA
complaint. RQ1 answer: frontier practice still ships oracles with marketing names; the
instrument-law is ours.
Overlap: zero hits in catalog/memory.

## RQ verdicts (worked from the banked reads only)

- RQ1 (do frontier eval methods satisfy LENS 2?): Partial pass as instruments, fail as law. The
  21-judge study proves the consensus illusion numerically (33-41 points of raw-agreement
  inflation) but fixes it by calibration against human labels; LENS 2's blind multi-family
  design attacks the correlation at the source. Contamination auditing is conceded broken
  (1wli359); the evaluator-side fresh-holdout duty is our census law.
- RQ2 (A/B harness designs): borrow the factorial grid (harness x model, published, re-runnable,
  1x0owom) + instrument pinning + the luck/condition separation discipline of 1wekbmy. Seeds and
  power analysis never surfaced on reddit as agent-eval practice in-window (only generic ML
  threads, out of window); the estate's named-instrument-moment law is ahead of what reddit does.
- RQ3 (self-improvement loops vs the triad): nothing found beats ratchet + citation-lint +
  census-patrol as a MEASURED enforcement mechanism; frontier loops are reflect-and-hope with
  honest falsifiers (1wevcyx) and noise-separation warnings (1wekbmy). The day-8 mine's 32
  unbanked sweeps remain the estate's own proof that the bank, not discovery, is the bottleneck.
- RQ4 (451-of-1,053 modules with no invariant; generation-first vs verdict-first): the sweep's
  evidence is one-sided for verdict-first instruments (decontamination conceded broken; outcome
  judges blind to process; single-pass judges flip). The percolator's own stance was NOT directly
  read in this ask (no percolator file opened; that leg is OWED, not asserted); nothing in the
  frontier material supports generation-first without a verdict rail.
- OWED (named): absolute timestamps for the 1w-cluster items (arctic-shift down all session);
  full-thread comment sentiment (only OP-adjacent excerpts were readable); the percolator
  side of RQ4 was not opened here.

## Method notes

- Local overlap checks ran as: venv python substring passes over catalog/catalog.jsonl (whole
  file, line-numbered) and an os.walk over memory/ with 12 title/phrase terms; grep/git/head are
  not on this sandbox's PATH (exit 127 twice) so python did the scanning. The only echo found was
  this session's own trajectory steps.
- Search backend 429/1302 storms recurred all session; queries were spaced one per round and
  several threads therefore carry single-fragment reads. Nothing below was banked without at
  least one verbatim page excerpt in hand.
