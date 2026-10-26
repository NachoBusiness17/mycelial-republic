# Sweep: evals-self-improvement via reddit - 2026-10-10

source-fetched: 2026-10-10. Actor: sweep-evals-self-improvement-reddit (frontier_olm fill).

## Doors scoreboard (all probed this session)

- `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` via WebFetch -> page shell only, zero posts (login wall: "accounts are required to access old Reddit").
- `www.reddit.com/r/LocalLLaMA/top.json` -> HTTP 403 Blocked.
- `api.reddit.com/r/LocalLLaMA/top?t=month` -> HTTP 403 Blocked.
- `old.reddit.com/r/LocalLLaMA/top/?t=month` (HTML) -> welcome shell, no posts.
- Thread HTML `www.reddit.com/r/LocalLLaMA/comments/1pe1bd4/...` via WebFetch -> JS shell ("Reddit"); via webReader -> "Prove your humanity" bot-check page.
- `www.reddit.com/r/LocalLLaMA/top.rss` via webReader -> same bot-check.
- WORKING DOORS: redlib mirrors. `redlib.catsarch.com` via webReader (thread + search pages render full text); `red.artemislena.eu` via WebFetch (search pages expose permalinks; thread pages render fully). WebSearch fallback used for older-thread discovery and one permalink resolution. No quote in this file comes from a door not listed as working.

## Pass 1 - broad sweep

55+ candidates considered across r/LocalLLaMA (top/month listing + 4 in-sub searches: judge eval, self-consistency consensus voting, thinking off benchmark, eval harness false positive), r/MachineLearning (search: LLM evaluation judge benchmark), r/LocalLLM (search: eval judge benchmark), plus WebSearch-surfaced threads. Full candidate lists live in the session transcript; permalinks for all banked and rejected items below.

## Overlap verdicts BEFORE banking (grep receipts)

Instrument: `grep -c -E "<phrases|ids>" catalog/catalog.jsonl` plus targeted greps of `watch/inbox/frontier_olm_2026-09-30|10-03|10-06/sweep/*.md` (the sibling sweeps' banks) and `memory/frontier memory/improve memory/press memory/attention.md memory/rib memory/law` (zero hits for all final phrases).

Already held - NOT re-banked, recorded here so nobody re-sweeps them: 1wmkr01 (Gemma E2B pilot; 10-03 inference-efficiency-reddit item 1), 1wz6mga (error bars; 10-06 evals-reddit item 2), 1wkjs20 (bigmath traces; 10-03 evals-reddit), 1wujph3 (Victoria/Maple; 10-03 quant lane), 1wlmg18 (vision quant eval; 10-06 quant lane), 1wg7dd5 (UkisAI Swift; catalog intake 2026-10-10T14:47Z, raw/swift_qwen3827b.txt), 1wyddlt (Kolibri; 10-06 item 1), jevals repo (catalog "RETRIEVAL RECEIPT - scratch landing - jevals README"). Final 8 below: zero hits in catalog.jsonl and memory/ on title and distinctive phrases.

## Pass 2 - the eight banked items (strongest first)

### 1. ThinkingBox: once vs 20/20, graded on terminal database state - r/MachineLearning [R]
- id 1x17shf · 2026-10-09 (page: "1 day ago") · 6 pts · u/tuhin_k (paper author, Microsoft) · arXiv 2608.19741, github.com/microsoft/thinkingbox
- 507 stateful workflows, 20 independent attempts each from identical clean backends (10,140 trials/model); grading compares terminal backend state + side effects; 477/507 graded on state alone. Metrics kept separate because they get conflated: pass@1, pass@20 (solved at least once), all-20 (solved every time).
- Numbers: Kimi-K3 93.89% pass@20 but 13.41% all-20; Claude Opus 5 79.09% / 47.53%; Qwen3.8-27B 89.35% / 7.50%. "Ranking by pass@20 and ranking by all-20 give you nearly reversed leaderboards." Retrospective ablation over 121,680 trials, 79,853 failed checks: 67.24% of failures terminated cleanly with no final tool error - a completion proxy would score them done; of those, wrong field values 77.61%, unintended extra effects 43.30%, missing required effects 25.36%.
- Estate answer (laws q1): THIS is the adopt-don't-invent prior art for consensus-decode redesign. The flock verdict illusion (0.60-0.67 agreeing 0/3) is the same phenomenon measured small: agreement-strength across attempts is not task success. ThinkingBox maps consensus to the task output space exactly: repeat from identical clean state, grade the terminal artifact, report the pass@k/all-n split. Law 17 (consensus strength is not correctness) now has an outside instrument. Law 31: the clean-failure audit (67% of failures look done) is the falsifier our completion proxies need.

### 2. Which model, which harness? - r/LocalLLaMA
- id 1wy5bmy · ~2026-10-05 ("5 days ago") · 66 pts · u/dh7net · airbench.ai
- Same models re-run across 5 harnesses: qwen3.8-27b-nvfp4 spans 37%-96% by harness; harness averages opencode 94%, omp 91%, pi 71%, hermes 67%, openclaw 56%. Local zcode/4xRTX6k/glm-5.3-flash-NVFP4 hit 100% in 31m13s vs Claude Code Opus 5.5 100% in 14m26s. MTP speculative decoding cost accuracy (nvfp4-mtp 52% avg vs 70% without); top comment (39 pts) challenges the config - strict rejection sampling vs relaxed acceptance in sglang is the suspect condition. 2h kill cap: "I'm killing run after 2h. So I don't know if an answer would be correct after that time."
- Estate answer (laws q10, thinking-off protocol): the outside replication the question wanted - conditions (harness, spec-decode acceptance mode) swing the same model by up to 59 points, dwarfing model-choice deltas. Conditions-suspect economics do NOT disappear under explicit thinking-off; the harness term dominates. Verbatim anchor: "On local hardware, the harness matters as much as the model."

### 3. Benchmarking small confidence scoring decision (Jev, Laya) models - r/MachineLearning [P]
- id 1wu3wep · ~2026-09-30 ("~10 days ago") · 4 pts · u/iam_gkrishna · huggingface.co/goku-san/laya-experts
- Jev ECE 0.013; on support intent a 90%+ confidence threshold raised accuracy 92.3% -> 97.6% at 82% coverage, remainder routed to fallback. Untuned Laya ECE 0.486; same filter dropped 7% of questions for a 2-point gain. Label-description rewrite (criminal intent -> transaction appearance): 65% -> 77% same model. Fixing the time window per account: 63% -> 75%. Single-transaction laundering classification: 54%, about chance. Author's caveats: own runs, per-task thresholds, no independent reproduction. Verbatim: "Calibration is what makes thresholds work."
- Estate answer (q4, meter rows n>=40): a cheaper instrument exists in this shape - a calibrated small decision model with per-task threshold + explicit coverage/remainder-to-fallback routing replaces part of the n>=40 meter with a coverage dial. ECE is the tracked quantity, not raw accuracy. The estate's Jev catalog holdings (43 rows) are model papers; this is the threshold-economics measurement they lack.

### 4. Qwen3.8-27B at 98K on 16GB, with committed rubrics - r/LocalLLM
- id 1wbaad7 · 2026-09-09 (one day outside the 30-day window; the dasbin EXL3 comparison update is later) · 46 pts · u/pyThat
- Adversarial tests written and judged by GPT-5.6 Sol, "rubrics and expected scores committed before Qwen answered". Tests 1-2 ran through the author's agent harness and were flagged contaminated (harness handed the model Python for exhaustive search + interleaved interim output); re-run in fresh sessions with no web/tools/history. Test 6: deterministic 73,677-token archive of 2,500 records with decoys, partial updates, VOID overrides, provenance reconstruction, counterfactuals, arithmetic - 100/100. Effort-matched cross-runtime update (u/dasbin): Test 7 Go concurrency EXL3 88 vs Escha 86; Test 8 binary decoder 99 vs 86 (EXL3 used io.ReadFull; Escha introduced two subtle bugs). Fail-loud config: TRUNCATE=0, "'It boots' is not the same as 'it fits.'"
- Estate answer (q5 + q2): the clean-conditions protocol the estate's thinking-off runs should copy - fresh session, no tools/web/history, rubrics committed before the run, effort-matched comparisons across runtimes. Also the harness-contamination catch is laws-lens law 31 in the wild: the first two evals were theater until the condition was measured.

### 5. VisTW integration: the extractor bug - r/LocalLLaMA
- id 1whln8v · ~2026-09-16 ("24 days ago") · 7 pts · u/piske_usagi · arXiv 2503.10427, Twinkle Eval v2.10.0
- Validation run 253 questions: their integration read 81.01% vs official 80.56%, but one subject sat 36 points low - the prompt format (answer-colon-$letter) made models copy the dollar sign, the extractor failed, fell through to a looser pattern, and pulled a letter from reasoning text, marking correct answers wrong. "A 21-question smoke set showed nothing. It took the full 253." The bug had been suppressing scores across five vision benchmarks. Reasoning VLMs at max_tokens 2048: 19% of responses truncated, costing 19 points. They skip the official third LLM-based parse and report unparsed_rate instead.
- Estate answer (q3, gate false-positive economics): direct evidence that (a) smoke sets cannot price a gate's false-negative rate - the full run is the only instrument, which is the meter-cost question answered from outside (the 21-question smoke set was free and worthless); (b) report-the-parse-failure-rate is the falsifier-carrying alternative to a third LLM parse - unparsed_rate is exactly the "instrument carries a falsifier or it is theater" shape for citation_lint's accepted-debt ledger.

### 6. The "Confident Idiot" Problem - r/LocalLLaMA (older than window; flagged)
- id 1pe1bd4 · 2025-12-04 (outside the 30-day window; included because the second-judge calibration content is the strongest found and zero estate holdings) · u/Proud-Employ5627, comment thread includes u/Hot-Presence-9382 (Dec 18 '25)
- Independence math (top comment): two ~80% judges -> ~4% joint error, "with the caveat". OP's reply: "errors are often highly correlated (Common Mode Failure)... They high-five each other over the same cliff." u/Hot-Presence-9382: "Preference Inversion" - judge score S can correlate with LOWER real-world utility Y; fix is an "Oracle Slice" of ground-truth labels learned into a mapping (affine or isotonic), recalibrated weekly/monthly; cimo-labs/cje tool. u/TheRealMasonMac cites FineWeb-Edu: the jury-based filtered classifier performed WORSE than the Llama3-annotation classifier - hypothesized to retain more low-quality samples. Comment advice: never same model, "make sure the models are not in the same family".
- Estate answer (q2, Ember never sole judge): the debt does not close by doubling judges - correlated errors void the independence math (two-family law 18 is the floor, not the fix). The cheap closure is the oracle slice: one small ground-truth set, one learned mapping, periodic recalibration - judge-count stays flat, calibration becomes the instrument. The FineWeb-Edu jury result is the caution that multi-judge can be net negative without a gold slice.

### 7. Intern-Decision: open decision models claiming better calibration than Jev - r/MachineLearning [P]
- id 1wrgbhi · ~2026-09-27 ("13 days ago") · 1 pt · u/Spico197 · huggingface.co/collections/internlm/intern-decision, github.com/InternLM/Intern-Decision
- 0.8B/2B/4B multimodal decision family; 4B claims > Jev 1.13.0; calibration probed with classic probability problems (next-die-roll should be uniform; Monty Hall) where Jev is called poorly calibrated; "~30 FPS decision calls" on an RTX 4090. OWED: the ECE tables are embedded images the text mirror cannot read - numbers unverified, claim banked as a lead not a measurement.
- Estate answer (q4): the local-sovereignty option for meter rows - open-weights decision models at interactive rates; if Intern-Decision's calibration claim survives one read of its tables, the meter could drop to a 4B local judge with a threshold, per item 3's economics.

### 8. DeepSeek V4.1 Flash vs Haiku 5.5 as sub-agent - r/LocalLLaMA
- id 1x0ixh6 · ~2026-10-08 ("2 days ago") · 0 pts, 50% upvoted · u/dergachoff
- Blind judge (Opus), both A/B orders, tie defined as the two orders disagreeing; author flags Claude-judged-Claude lab bias and reports it anyway: Haiku lost at every effort tier (low 1/0/3, medium 1/1/2, high 0/1/3 W/T/L); "Higher effort made it search more, but still not find more." Titles job: 28 DeepSeek vs 8 Haiku wins, 9 split, 7 identical. One run per setup, "$1 well spent (or not?)". Comment counter-evidence: hallucination reputation "possibly a harness difference".
- Estate answer (q2): a two-order blind protocol is a cheaper second-judge substitute for pairwise verdicts than a second model - order-swap disagreement as the tie condition catches position bias at 2x one judge, not 2x two judges. Small-n honesty (n=4 briefs, single run, stated) is the template for meter rows.

## Answers to the five research questions

1. Consensus-decode -> task output space (open q1): prior art exists and is adoptable - ThinkingBox (item 1). Grade terminal artifact state across N attempts from identical clean state; report pass@k and all-n separately; expect the two rankings to disagree (reversed leaderboards). The estate adopts rather than invents; the flock decode should vote on artifact state, not on token agreement.
2. Multi-judge calibration (open q9, Ember never sole judge): consensus from outside says judge-count is the wrong axis - correlated (common-mode) error voids independence (item 6); a jury can be net-negative without ground truth (FineWeb-Edu, item 6); the cheap closure is a calibrated oracle slice + periodic recalibration (item 6) plus order-swap blind judging for pairwise calls (item 8). Ember stays non-sole; the spend goes to the gold slice, not a second judge.
3. Maat-style false-alarm accounting (q3): the 2609.34017 denominator question maps to the estate's 37/125 accepted citation debts as follows - measure the gate's precision on a known-good sample at full scale, because smoke sets price nothing (item 5: 21-question smoke set missed a 36-point bug the full 253 caught), and keep the failure visible with an unparsed_rate-style counter rather than a healing third parse (item 5). The already-held 1wmkr01 (10-03 bank) supplies the measured price: five right answers given up per wrong one avoided. One denominator still OWED: nobody outside has priced citation_lint's own FP rate; that measurement is the estate's to run.
4. Cheaper meter rows n>=40 (q4): yes, two shapes - calibrated small decision models with per-task thresholds and explicit coverage-to-fallback routing (item 3, ECE 0.013, 92.3->97.6 at 82% coverage), with an open-weights local option at ~30 FPS (item 7, numbers OWED in images); and order-swap protocols where a second full judge would be the naive answer (item 8). The meter does not have to stay the standing cost, but ECE must become the tracked quantity.
5. Conditions-suspect economics under explicit thinking-off (open q10): they change for the better only when conditions are pinned - the measured harness term (same model 37%-96% across harnesses, item 2) dwarfs thinking-mode deltas, and even spec-decode acceptance mode is a live suspect condition (item 2 MTP dispute). The clean-conditions protocol (fresh sessions, no tools/web/history, committed rubrics, effort-matched runtimes, item 4) is what makes a thinking-off reading trustworthy. No outside replication found of thinking-off economics per se inside the window; the UkisAI Swift economics thread (already banked today by the sibling lane, raw/swift_qwen3827b.txt) carries that side.

Laws honored: 17 (consensus strength is not correctness: items 1, 2), 18 (two-family corroboration: item 6 common-mode failure, item 8 same-family bias flagged), 31 (falsifier or theater: item 4 committed rubrics + contamination catch, item 5 unparsed_rate, item 1 clean-failure audit).

## Limits / not verified

- Item 7's calibration tables are images; unverified (OWED above). Item 8 is n=1 per setup by the author's own statement.
- Dates are as rendered on fetched pages (relative "N days ago" against fetch 2026-10-10); items 3, 5, 7 carry approximate dates from relative stamps.
- No reddit page was rendered in an authenticated browser; every quote comes from the redlib mirrors named in the doors scoreboard.
- memory/ overlap greps covered memory/frontier, memory/improve, memory/press, memory/attention.md, memory/rib, memory/law, memory/zknot/LATEST.md, memory/briefs - a full-tree grep of memory/ was abandoned (too slow; killed) and not completed; catalog.jsonl and the sibling sweep banks were fully checked.
