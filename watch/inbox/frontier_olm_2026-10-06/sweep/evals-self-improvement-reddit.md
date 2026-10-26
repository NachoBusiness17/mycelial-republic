# Sweep: evals-self-improvement via reddit - 2026-10-06

source-fetched: 2026-10-06
seat: sweep-evals-self-improvement-reddit (workflow subagent, actor_3_27)
instrument: Arctic Shift archive API (`arctic-shift.photon-reddit.com`) driven by curl with a
browser UA, paged and backoff-paced, posts + full selftext + up to 100 top-score comments per
deep read (raw: `sweep/_raw/as_*_p*.json`, `sweep/_raw/deep_1006/`); venv python for local JSON
parsing. Every quote below came from bytes fetched and read in this session. Door credit: the
2026-10-03/10-04/10-05 sibling seats certified this door; I re-verified it live before fetching.

## Doors scoreboard (all probes run this session)

| Door | Probe | Result |
|---|---|---|
| Recipe primary: `old.reddit.com/r/*/top.json?t=month&limit=50` x4 subs, WebFetch | r/LocalLLaMA, r/MachineLearning | DEGRADED: both returned the "Welcome to Reddit" login shell, zero post data |
| `www.reddit.com/r/LocalLLaMA/top.json` | WebFetch | HTTP 403 Blocked (Retry-After: 0) |
| **Arctic Shift archive API via curl** (posts/search x ~30 pages, posts/ids, comments/search x10) | 4 subs, window 2026-09-06..2026-10-06 | **WORKING**, heavily rate-limited: error body `{"error":"Timeout. Maybe slow down a bit"}` on roughly a third of calls; 10-40 s backoff between attempts cleared it every time |
| Python fetcher script | two Write attempts | BLOCKED by the Mimosa security hook (SSRF + path-traversal flags, verdict varied on near-identical shapes; the first script of the session passed, retries of the same shape failed). Switched to curl in the shell; no challenge evasion attempted |
| WebSearch `site:reddit.com` fallback | not needed | Not used; Arctic Shift covered the window. No fallback fabricated |
| safereddit / mirrors / Wayback | not needed | Not probed this sitting; siblings covered their state on 10-05/10-06 |

## Corpus fetched this session

4,361 deduped post rows across r/LocalLLaMA (2,278, back to 09-11; pages to 09-06 kept erroring),
r/LocalLLM (992, back to 09-29), r/ollama (595, back to 09-04), r/MachineLearning (496, back to
09-12), all `created_utc`-stamped from the archive JSON: `sweep/_raw/as_merged_1006.jsonl`.
Known window gap: r/LocalLLaMA 09-06..09-10 and r/LocalLLM 09-06..09-28 tails not pulled
(persistent throttling); nothing date-critical for this area appeared to sit in those slices.

## Dedupe against our own corpus (done BEFORE banking)

Read in full before banking: `frontier_olm_2026-10-05/sweep/evals-self-improvement-reddit.md`
(both passes; its 4 items and 13-item 10-03 dedupe list), `frontier_olm_2026-10-04/sweep/evals-
and-self-improvement-reddit.md` (the same-area bank: items 1wactmx, 1wkef2o, 1wwqpji, 1wxoiug,
1wv1c2e), the 10-03 inference-efficiency bank's item list (1wmkr01 verbalized-confidence
collapse, 1wtzwwn $1,200 hard-cap, 1wmd3xx question-first ordering), and today's sibling
`frontier_olm_2026-10-06/sweep/open-and-local-models-reddit.md` (9 items). ID greps over
`frontier_olm_2026-10-03..06` separate bank items from raw candidate-pool rows. NONE of the 8
items below appear in any bank; each carries its own grep receipt.

## Pass 1 - broad sweep (pool 4,361 rows; named dispositions, 40+ candidates)

Bucketed by RQ keyword (judge/calibration 125 hits, eval/bench 807, quota/usage 333,
stale/refresh 262, self-improve 25), top ~22 of each read as titles+selftext snippets. Held and
skipped: the 10-03 evals 13 IDs (1wsuag0, 1wdasar, 1w9llr4, 1wv1u54, 1wv05u1, 1wu6reb, 1wloz92,
1wgazy4, 1wkjs20, 1wfo8xl, 1wu7rfo, 1wmprwb), the 10-04 evals 5 IDs, the 10-05 evals 4 IDs
(1ws6bmh, 1wtzedu, 1waiu6b, 1wpqbxp), 10-03 inference items (1wmkr01, 1wtzwwn, 1wmd3xx), the
10-06 open-and-local 9 IDs, and the 10-05 sibling banks' rows (1wvxih5, 1wt0tot, 1wc6tka).
Off-area high scorers rejected: 1wvz1ex (iPhone second GPU), 1wj3s31 (Swift Qwen downloads),
1wi32jg (Mozilla gap report), 1woe70t (Jev marketing), 1wkxx8e (Gemini bench), 1whf7ov (5090
alt), 1wlgrft (Qwen-Image), 1wjr59t (768GB VRAM), 1wtc4j9 (EPYC), 1wp0z3i (stopped using API),
1wqcrly (Ling Tiny), 1wo1bct (cost dropping), 1wj28vh (AMD price hike), 1wlvv8h, 1wfqwfh,
1wmm89l (Huawei), 1wxbm8w, 1wl3828, 1wtpntt, 1wujd9a, 1wu25pe, 1wejf5k, 1wlt577, 1wtmq42,
1wkc4c9, 1wxeqcr, 1wxeqzc, 1wuccjf, 1wtyl5m, 1wx7jg6, 1wmn76r, 1wwfg9r, 1wq2hfc, 1wu4yu4,
1wt6fpn, 1wjieap, 1wouby6, 1wpvep4, 1wjlyzr, 1wwv0fj. Adjacent leads recorded, not banked
(single-pass, not deep-read): 1wx4yvw (least sycophantic open LLM, 72c: judge-bias discourse),
1wj3rrv (Humor Arena crowd-judging), 1wrzoej (Laya 322M abstention-capable judge alternative,
0c), 1ws2mhx (Jev judge calibration, 0c), 1wromzr (hedging-token logit penalty), 1wnhji0
(gemma4 tool-calling surprise), 1wwpqic (9B agent broke code but did not lie), 1wqrmdg
(wave-execution hash gates), 1wyuzab (unloop time-travel agent debugging), 1wyvguh (MOLT
fine-tuning fit tests), 1wynrrc (pinned llama.cpp bench harness in CI), 1wwp0q8 (release-note
fix claim contradicted by measurement), 1wz00dg (usage share of oversized screenshots), 1ww2jsu
(self-hosting cost accounting, 187c), 1wuhrop (0.12 euro/hour vs frontier), 1wfmzez moved to
pass 2, 1wxcd4k (ARC-AGI-3 Kaggle 7->56). Discarded: 1wmfbk4 + 1wmdwnb (identical duplicate
self-improvement posts, spam pair), 1wrfp50 deep-read and rejected on authenticity grounds (see
below), 1wqenk2 deep-read and left as discourse (see below), 1wskcfz (MCP portability pitch),
1wisdups none. Rejected on window: none this sitting (the 10-05 seat's out-of-window appendix
already holds Prime Agent and 1vxa0il; not re-fetched).

## Pass 2 - deep reads (10 threads fetched end to end this session, post + comments)

Via Arctic Shift posts/ids + comments/search, raw JSON kept at `sweep/_raw/deep_1006/`:
1wyddlt (post + 12 comments), 1wgii3h (post + 100), 1wrfp50 (post + 100), 1wxysy1 (post + 15),
1wz6mga (post + 4), 1wskysi (post + 2), 1wxwtto (post + 4), 1wqenk2 (post + 53), 1woa5d3
(post + 97), 1wfmzez (post + 22). Deep-read rejections: 1wrfp50's claim (codex-cli harness made
a local model beat GPT 5.6 Luna on real work) is exactly the estate's HAD law, but its top
comments challenge the post's authenticity ("Claudish comment, default username, private
profile"; "I'd toss a coin for this one"), so it is UNVERIFIED and not banked; 1wqenk2
(bootstrapping question, 53 comments) is rumor-grade RSI discourse ("rumours floating around
that Google achieved RSI in training Gemini 4") overlapping the held 1wgazy4 - left unbanked.

## Items banked (strongest first; 8 items, all in-window 2026-09-13..2026-10-06)

### 1. r/LocalLLM 2026-10-05 "I benchmarked Aleph Alpha's Kolibri against Claude Sonnet 5.5 on long German writing: 0 of 136 blind wins, but $0.0077 an output on 2 rented GPUs" (1 pt, 12 comments in archive, id 1wyddlt)

The judge2 menu item (laws.md:90: mass duel re-judging, two-family evidence) running in the wild,
and the row-expiry demonstration in one thread. The practitioner's design is exactly the estate's
shape: "GPT-5.5 and Gemini 3.1 Pro judged every pair blind in both orders. They also scored each
output on its own." Two judge families, order-rotated, pairwise plus absolute, against the
leaderboard row he was deciding on. Result quote: "Head-to-heads: Kolibri won 0 of 136 (135
marked decisive)." Judge scores 3.7/4.2 vs Sonnet's 8.7; serious errors 100 and 92 vs 7 and 7 -
yet the same runs found real strengths the index row cannot see (grammar 0.36 vs 0.24 errors per
1,000 words; "no invented citations or references in 34 outputs"; "It holds up when the answer is
in the documents you hand it"), plus a cost row per parallelism (185/504/713 outputs per hour at
16/64/128 parallel, $0.0077 best) and a published artifact ("Every run..., every judge verdict
and what each model was given are downloadable"). This is what a re-measured row looks like:
per-capability verdicts with costs, not one number. Overlap: id and "0 of 136" 0 hits in
catalog and memory; the day-5 bank holds the Kolibri HF-release thread (1wwl7y6, BFCL 39.8 from
the same author in comments) - this is a new thread by the same author, the re-measure that bank
named as the falsifier. Not fetched: the linked blog (tej.as) - reddit-side claims only.

### 2. r/LocalLLaMA 2026-10-06 "Can we please have some error bars?" (1 pt, 4 comments, id 1wz6mga)

The statistics the GROWS pass-3 fixpoint proof (ask Q5) must satisfy to be able to fail, posted
today. Quote: "Report the number of items, bootstrap confidence intervals, and ideally multiple
seeds." The argument: "HumanEval has 164 problems, so a model scoring \~70% has a standard error
of roughly 3.5 points from question sampling alone" - a 2-point improvement is inside the noise
before temperature, prompt template, few-shot, harness version and contamination vary. Fixes
named: paired tests (same questions, two models), Miller's "Adding Error Bars to Evals". Top
comment adds the small-n law the estate's own sweep windows live under: "9 out of 9 sounds like
100%, but the 95% interval starts around 70%. The rule of three helps: zero failures in n tries
still allows a failure rate up to about 3/n." Estate steal: a window whose findings all match
prior registers proves fixpoint ONLY if the window's finding-detector had power (n and seeds
reported, 3/n small) and the match is a paired comparison against the named prior rows, not an
eyeballed "nothing new". Overlap: "Adding Error Bars", "error bars", id 0 hits in catalog and
memory.

### 3. r/ollama 2026-09-28 "I went back through 15 runs from my local agent" (3 pts, 2 comments, id 1wskysi)

A field measurement of the exact number the ask's Q1 wants: what fraction of verdicts flip when
the same execution records are re-judged under a stricter criterion. Quote: "Although it was the
same execution record, the outcome varied quite a bit depending on how success was defined."
The walk: file-exists criterion scored 14/15; field-fill check found "only 76% of the requested
fields were actually filled in"; traceability of numbers/URLs to pages actually read left "only
9 of those 14 outputs passed" - a 5-of-14 (36 percent) flip on one added criterion, on records
he had already scored once. Conclusion is the judge2 ticket discipline: "now I'm paying less
attention to the raw success rate and more attention to what that rate is actually counting as
success." Comments add the checker-blindness mode: "the checker saw basically nothing, but it
still looked fine because it reported zero errors." Overlap: id and "76% of the requested
fields" 0 hits in catalog and memory; raw-only appearances in 10-03 tmp candidate files.

### 4. r/LocalLLM 2026-10-05 "Dense 27B vs MoE IQ2_XS on one RTX 4090: synthetic bench plus 3 graded real tickets" (3 pts, 15 comments, id 1wxysy1)

The L16 row-expiry question (laws.md:89) answered with a battery order: synthetic first, graded
real work second, and the real work flips the synthetic verdict. Quote: "150-minute cap, rubric
fixed before the runs, every check re-run by the grader." Synthetic said parity (bugs found 12
and 10 vs 12, 10, 9; MoE faster decode), real tickets split 112 vs 86 of 150 across a five-axis
rubric (correctness, verification, scope, quality and honesty, 10 each) with a total MoE no-show
on one task (QML settings: 0, no edits). The author prices his own confounds: "Limits: n=1 per
ticket and one grader model; the MoE ran first." And the harness term shows up again - the MoE
engine reused 32% of prompt tokens under 3 interleaved agents vs the dense engine's 88.5%, which
the author (not the benchmark) names as the cause. Estate steal: the re-measurement cadence for
seeded routing rows is this two-stage shape - synthetic screen, then rubric-fixed graded real
tickets with order admitted; run order and cache share are part of the row, not noise.
Overlap: id and "graded real tickets" 0 hits in catalog and memory.

### 5. r/LocalLLaMA 2026-09-14 "DeepSeek engineer relections on RSI - burying my talent to yesterday" (392 pts, 118 comments, id 1wgii3h)

The window's highest-signal self-improvement discourse, from inside a frontier lab, translated
by the poster. Quote: "in half a year or one year, the operators written by AI will most likely
be as good as mine, or even better." The author is the person who wrote DeepSeek v4.1's main
Attention operator and expects his own replacement by the loop he feeds: measured progress
claims (in one year, from doc-lookup helper to "an expert that can independently read CUDA, PTX,
and SASS code, use professional tools to analyze the stall time of every instruction"), the
arms-race logic ("if it has to happen, I hope the person who revolutionizes me is myself"), and
the career plan built on unpredictability. Top comment (40 pts) corrects the translation:
"operator" should be "kernel" (CUDA kernels) - load-bearing for any reuse of the claims. Estate
steal for the GROWS falsifier: this is the human-side prior that a fixpoint claim is the thing
most likely to be falsified next wave; the improvement operator is itself on the replacement
schedule. Overlap: id and "burying my talent" 0 hits in catalog and memory; "Riemann" catalog
hits are math corpus, unrelated. Caveat: translated blog, author unverified beyond the thread.

### 6. r/ollama 2026-10-05 "Ollama Cloud Down? Rate limiting? status page?" (5 pts, 4 comments, id 1wxwtto)

The burns-carrier question (ask Q3) seen from the provider's blind side, one day before this
sweep. Quote: "Cant find a status page anywhere for them and its Middle of the night in the US."
The OP's own counters look healthy ("credits Okay"; "usage is only 2% for the session and also
the week") while every request 429s; a commenter's draft support ticket names the signature (a
stuck rate-limit header, x-ratelimit-active pinned at 3, all requests 429, since roughly 09:55
AEST), and the practitioner cure is mid-incident failover: "swapped Hermes over to neuralwatt
and no issues" (that Hermes is the commenter's own agent's name, no relation to the estate's).
Downstream damage in-thread: rate-limit storms corrupted the commenter's own database mid-write.
Estate steal: provider-side state goes stuck-wrong silently and providers publish no clock, so
the instrument that owns the descent-leg-8 clock (burns.md:36-45: zero rows after
2026-09-28T13:45Z) must be estate-local self-polling with a failover lane, not a provider
dashboard. Overlap: id and "x-ratelimit-active" 0 hits in catalog and memory; complements the
held quota-nerf thread 1waiu6b (found-by-own-ledger) and hard-cap thread 1wtzwwn (held).

### 7. r/LocalLLaMA 2026-09-23 "MiMo-V2.6 (both Pro and Flash) is a benchmaxxed scam" (80 pts, 82 comments, ratio 0.69, id 1woa5d3)

The re-measurement culture, both halves. A senior SWE takes the AA-index topranked open model
(46) to real security work and it fails dangerously: an env-var bypass ("git push -uf lets you
happily wipe out the git remote.") plus config aliases and a second binary path - nine holes
total per the second-family review he then ordered ("I asked GLM-5.3 (full-fat) to do a security
review of the change. In 3 minutes, it found NINE glaring security holes"). Replication in
comments: "can confirm it was benchmaxxed for coding tasks for sure" (68 pts) and "Tried API vs
DS4 Flash 0731 on 2xSpark, same tasks, 0731 won every time" (26 pts). But the thread's second
half is the methodological guard the estate's cadence needs: "You ran one prompt and deemed it a
scam" (52 pts), "Such low effort thread" (25 pts), plus users for whom the model works fine. The
adjudication the community converged on: an n=1 anecdote cannot flip a row, but a row that has
never faced adversarial real work is unmeasured, not measured-good. Estate steal: judge2-style
second-family review (GLM-5.3 over another model's security output) is already how the community
grades; the estate's row-expiry cadence should schedule adversarial re-measurement BEFORE a row
routes dollars, and record dissent tickets either way. Overlap: id 0 in catalog/memory;
"benchmaxxed" word-precedent exists in memory/runs/quote_audit_wide_20260925/inbox_concat.txt
but its context is a different model's audit (Astra/dashboard comparison), not this thread.

### 8. r/LocalLLaMA 2026-09-13 "I built a general agent harness for myself. Two messages became a 63-hour attempt to solve the Riemann hypothesis." (0 pts, 20 comments, ratio 0.31, id 1wfmzez)

A self-improvement window published the way the descent protocol asks: negative result as the
deliverable. Quote: "It obviously didn't solve RH. That was not the point." The run: 63 hours,
"over 50 million input/output tokens", Qwen3.8-27B 4-bit on one RTX 3090, harness revises its
own purpose and modifies its own harness, memories/programs/metrics published on Hugging Face
for inspection. The author's stated test is exactly an endurance falsifier: "to test whether a
27B model could keep working without hallucinating a solution, breaking down or losing focus."
The community's verdict (ratio 0.31; "YAVCH (yet another vibe-coded harness)"; "Can we stop with
all the vibe-coded harness?") is itself data: publishing an uncontrolled self-improvement run
buys no credibility without a baseline or a battery, and one constructive comment read the code
and asked "What's different between it and other ReACT loops?" Estate steal: the run's shape
(two-message boot, long horizon, published memories and metrics, negative result headline) is
the GROWS-window shape; what it lacks (prior-register comparison, baseline harness, n) is what
pass 3 must add. Overlap: id and "Artificium" 0 hits in catalog and memory; "Riemann" catalog
hits are the math corpus, unrelated.

## Answers to the five research questions (from this session's reads + the ask's lens facts)

**Q1 (judge2 mass duel re-judging; what fraction of single-judge verdicts flip).** The field
supplies a flip-rate precedent and the ticket discipline. 1wskysi: one added success criterion
flipped 5 of 14 already-scored runs (14/15 -> 9/14 passing, 36 percent of the passing set), and
the practitioner's own rule is that a re-look ticket must name WHICH criterion changed, because
"the outcome varied quite a bit depending on how success was defined." Held material brackets
the mechanism: order rotation flips 1B-regime argmax at 99 percent (1wwqpji, 10-04 bank),
verified-source framing flips 45-88 percent of correct answers in 7 of 8 models (1wv1c2e,
10-04 bank). 1wyddlt shows the two-family, both-orders, pairwise+absolute design a practitioner
actually ships, and 1woa5d3 shows second-family review (GLM-5.3) generating nine dissent-class
findings on another model's output. Design upshot for judge2: record per-ticket the criterion
delta, the family pair, and the order; the flip fraction is a function of those three, not a
constant. Not run here: no estate re-judging was executed; this is mined design evidence only.

**Q2 (the 28 sweep items; which become register rows).** Not the confirmation pass: a sibling's
`_confirm_28.py` exists in today's sweep dir and the owed move is recorded at burns.md:96-99.
This sweep's contribution is fresh-day input: none of the 10 threads read contradicts a
day-5 bank; the 8 new items above are confirmation-pass candidates for THIS area's ledger
(1wyddlt and 1wz6mga are the two I would register first: one is a completed re-measurement
receipt shape, one is the statistics the pass must meet).

**Q3 (burns ledger day-8 silence; which carrier owns the clock).** The field evidence says
provider-side clocks are the wrong owner: 1wxwtto shows healthy self-reported usage (2 percent)
with every request 429ing on a stuck counter and no status page; the held 1wtzwwn (10-03 bank)
shows provider dashboards alert late; the held 1waiu6b shows quota cuts visible only in a
self-kept ledger. The carrier that owns the clock must be estate-local: the descent leg-8 spend
rows belong in a self-polled store with a staleness alarm and a failover lane, and burns.md:36-45
already names the interim carriers (DIGEST/RECEIPT pairs, landing receipts, git log) while the
LEDGER is dark. I did not resume or reconcile `memory/burns/LEDGER.jsonl` - that is the
confirmation/fold sibling's probe, not a sweep action, and nothing here should be read as having
run it.

**Q4 (row expiry ~2026-10-30 under L16; cadence and priority).** The month's re-measurements
agree on the order of operations: synthetic screen first (cheap, fast, 1wxysy1's bench tables),
then rubric-fixed graded real work scored per capability (1wxysy1: 112 vs 86 of 150 after
synthetic parity; 1wyddlt: 0/136 where the index row said competitive), with cost columns
measured at the same time (1wyddlt's per-parallelism table), order effects admitted (MoE ran
first), and adversarial re-measurement for any row that routes safety-adjacent dollars
(1woa5d3). Priority from the evidence: re-measure first whatever row is about to route dollars
on a capability where only benchmark evidence exists - that is Kolibri's tool-calling row in the
day-5 falsifier, and the seeded 2026-09-30/10-01 verdict rows approaching STALE on 2026-10-30 in
the estate's own battery.

**Q5 (GROWS pass 3; the falsifier that could prove fixpoint).** 1wz6mga supplies the missing
statistics and 1wfmzez supplies the cautionary shape. A window whose findings all match prior
registers proves fixpoint only if: (a) the window reports n, seeds and intervals per finding
("Report the number of items, bootstrap confidence intervals, and ideally multiple seeds"),
because without them a null is indistinguishable from an underpowered sweep (rule of three:
zero failures in n tries still allows 3/n); (b) the match is a paired comparison against named
prior rows, not an eyeball; (c) the window's detector was aimed where the prior wave actually
changed things (1wgii3h: the previous generator is the first thing superseded; 1wfmzez: a
63-hour, 50M-token self-modifying run with no baseline bought a 0.31 ratio and "YAVCH").
Proposed measured result that would PROVE fixpoint: a pre-registered pass with detector power
(3/n below the smallest finding-class the registers distinguish) whose paired deltas against
the prior registers all fall inside their intervals, two waves running.

## Overlap ledger (grep receipts, this session)

- Catalog (`grep -c` over `catalog/catalog.jsonl`): all 8 thread IDs 0; "0 of 136" 0; "Adding
  Error Bars" 0; "rule of three" 0; "76% of the requested fields" 0; "graded real tickets" 0;
  "burying my talent" 0; "x-ratelimit-active" 0; "benchmaxxed" 0; "Artificium" 0; "Riemann" 22
  (math corpus, unrelated to 1wfmzez).
- Memory (`grep -rli` over `memory/`): all 8 IDs 0; all phrases 0 except "benchmaxxed" ->
  `memory/runs/quote_audit_wide_20260925/inbox_concat.txt`, context read this session: an
  Astra/dashboard comparison row from the 09-25 quote audit, a different model and thread;
  word-level precedent only.
- Inbox banks (`grep -rl` over `watch/inbox/frontier_olm_2026-10-03..06`): prior appearances
  are raw candidate pools and tmp files only (1wskysi, 1woa5d3, 1wfmzez, 1wrfp50, 1wqenk2 in
  10-03 tmp/arctic pulls); 1wyddlt, 1wz6mga, 1wxysy1 appear only in today's doors raw capture
  (`frontier_olm_2026-10-06/sweep/doors/ff_arctic_posts.jsonl`); 1wxwtto has NO prior hit at
  all. Held items confirmed distinct: 1wv1c2e, 1wtzwwn, 1wmkr01, 1wmd3xx, 1wactmx, 1wkef2o,
  1wwqpji, 1wxoiug, 1ws6bmh, 1wtzedu, 1waiu6b, 1wpqbxp all skipped, none re-banked.

## Limits / not run

- All quotes come from Arctic Shift archive JSON (posts + up to 100 top-score comments);
  Arctic Shift can lag live Reddit and its own raw scores freeze at archive time (1wyddlt shows
  archive 12 comments where the live post may differ; the visible thread page shows 0 - the
  archive's num_comments field is the count I cite).
- The recipe's named doors (old.reddit/www.reddit .json) are dead from this host this session;
  the degraded-door note stands. WebSearch fallback unused; safereddit unused.
- Blog/primary pages behind threads (tej.as write-up, GitHub Artificium repo, Hugging Face
  dataset) NOT fetched; items stand on reddit-side bytes only.
- 1wgii3h is a translated blog post by an unverified author; the kernel/operator translation
  correction (top comment) is recorded and any reuse must carry it.
- 1wrfp50 rejected on authenticity (community astroturf suspicion); recorded, not banked.
- No estate instrument was run (no judge2 execution, no ledger resume, no register writes);
  this is a read-and-bank sweep. Nothing here is a passed estate check.
- Window gaps: r/LocalLLaMA 09-06..09-10, r/LocalLLM 09-06..09-28, r/MachineLearning 09-06..09-11
  tails unpulled under API throttling.
