# SWEEP: finetuning-adaptation via X (frontier_olm 2026-10-06)

- Seat: sweep-finetuning-adaptation-x (dynamic-workflow gopher)
- Moment: source-fetched: 2026-10-06
- Window: 2026-09-06 .. 2026-10-06. Snowflake bounds computed locally with the repo
  interpreter: floor 2096387904107446272 (2026-09-06T00:00Z), ceiling 2107621927941046272
  (2026-10-07T00:00Z). Every ID-bearing candidate was date-decoded, not date-guessed; one
  search-surfaced post (v_shakthi 2095339203781640399) decoded OUT of window (Sep 3) and was
  dropped on the decode, not the summary.
- Estate map (feeds): skills_pack.py + skill_ledger.py (the prompt monoculture; skill_ledger.py
  docstring lines 4-10 already carries the "home-grown LoRA classifier, target ~500-5000 rows"
  plan), the memlance skills, and the decision-model rung claim (lens/burns.md:92-95, five
  sweep-level rows, none confirmation-passed).
- Sibling concurrence: sweep-finetuning-adaptation-hn ran the same owed confirmation pass in
  parallel (their file landed mid-window in this directory); where our verdicts touch the same
  bytes they are cross-checked below. My bank is X-door only; zero overlap with their 8 HN-door
  banks (Laya, CUA-S1, Red Hat benchmark, Jeff, llama.cpp /v1/systemone, Synthpop, Mini-AGI,
  nimble - grep of their file for my candidates returned nothing).

## Door status, stated plainly

1. WebSearch X door: DEGRADED, bursty. Query 1 (site:x.com fine-tuned/LoRA) returned after two
   1302 storms with 10 x.com candidates; query 2 died 3x 429/1302 with zero results; query 3
   (catastrophic forgetting) returned 10 candidates; query 4 (multi-LoRA) returned 8 (7
   out-of-window, 1 unattributed article). The site: operator was partially honored. Receipts:
   the four tool-result blocks in this session's log.
2. fxtwitter single-post door: HEALTHY. 10 resolves attempted, 10 HTTP 200 with full text and
   dates (TeksEdge, sairahul1 x3, JulianGoldieSEO, fastinoAI, v_shakthi, dair_ai, BSPK,
   richmondalake).
3. fxtwitter article door: SELECTIVE, worse than 10-05. Direct article-id URLs
   (api.fxtwitter.com/<user>/status/<article-id>) 404 for all 4 tried. Through POINTER tweets,
   the article object carries full DraftJS content blocks for 2 of 4 (sairahul1 guide 61,674
   chars of JSON; dair_ai papers 27,302) and only title+preview for the other 2 (BSPK,
   fastinoAI). This independently confirms the sibling's today-finding that zafstojano's article
   body is not exposed today: the 10-05 single-article recovery does not generalize; the door is
   per-article, not recovered.
4. AINews mining door: DEAD for fresh content. news.smol.ai/issues index (737,533 bytes fetched
   this sitting) lists newest issue 26-09-10-not-much; nothing after Sep 10, so the 10-05 X
   cohort's clustering on 09-09..09-11 is now explained: the miner itself stopped.
5. Reddit RSS door (confirmation side-duty): alive but hard-throttled from this host - 9s pacing
   429ed 4 of 6 threads; 55s pacing confirmed 3 of 4; the last thread needed a solo retry after
   cool-down. All six 10-05 reddit threads eventually confirmed live this sitting.

## The owed confirmation pass (RQ1, my X slice + cross-checks)

Ran with three instruments this sitting, all in this directory as receipts:
`_confirm_fx_arxiv.py` (6 X statuses through fxtwitter + 8 arXiv IDs through one
export.arxiv.org API call), `_confirm_hn.py` + `_confirm_hn2.py` (Algolia items API + corrected
canonical URLs; my first two guesses for the duane.sh, Clef, and Raspberry Pi URLs 404ed and
were replaced by the Algolia-returned canonical URLs - recorded, not hidden),
`_confirm_reddit.py` + `_confirm_reddit2.py` (RSS with pacing).

- X 6/6: posts live, snowflake dates match the 10-05 stamps, quote needles hit in fetched JSON
  for omarsar0 ("performance dropped on all seven tasks" + the planning-strategy line),
  ArtificialAnlys ("license: mit" + "552b parameters"), Sumanth_077 ("34 of 64 harness changes"
  + "2 of 9 final harness versions"), shikibmehri ("army of agents" + "optimal reward signal for
  each token of training"), ValsAI ("1m context window and 384 max output tokens" + "temperature
  1, default top-p"). zafstojano: post live, article title "Recursive Synthetic Improvement"
  live in the article field, body NOT exposed today - pointer-partial, matching the sibling's
  independent finding on the same object.
- arXiv 8/8: IDs live in one batched call; 7 quote-verified at abstract level; 2609.17848's
  numbers re-verified in the FULL html (arxiv.org/html/2609.17848v1, 134,404 bytes: "88.0%
  versus 80.4% on xlam" and "47.6% versus 44.1% on glaive" both HIT), upgrading the sibling's
  confirmed-pointer note on that fragment to a full-text byte-verify.
- HN 8/8: threads alive via items API (Ask-HN quotes, Cactus "360b"/"n-gram"/"engram" all hit);
  external pages alive at canonical URLs: duane.sh post CONFIRMED including "every system
  appears in every position equally often" (context extract pulled: "claude opus 5.5 judge · 631
  excerpts"), dirac.run post CONFIRMED (401,975 / 212/300 / apache-2.0), shrewd README
  CONFIRMED (locked test set + statistical bound), Clef blog CONFIRMED (rank-256 + qwen3.8-27b),
  FrogNano abstract CONFIRMED (online task synthesis + 1,500), Raspberry Pi Needle article 3 of
  4 needles (the "returns an empty function_calls list" detail is not on the news page - one
  sub-claim degraded, the rest confirmed).
- Reddit 6/6: all live via RSS; quote needles hit for unswallow, Spanda, CodeFinetuner
  ("sweet spot" + "codebleu"), RustVulkan ("2e-7" + "lora"), hemmingway-1 ("1330" + "eq-bench"),
  FunctionGemma ("270m" + "90.9" + distillabs).

VERDICT (RQ1): all 28 items survive; 27 full and 1 pointer-partial (zafstojano body) from my
slice, zero dead, zero quote drift found anywhere. The sibling's independent pass over the same
28 (their file, "OWED CONFIRMATION PASS" section) reached the same shape (27+1) with one extra
catch I did not hit: the HN 49966238 story TEXT was edited since 10-05 (quotes survive on the
canonical dirac.run page). The 10-05 finetuning-adaptation set is register-promotable with two
pointer caveats (HN3 quote-source = dirac.run page; X2 body quotes unre-verified today).

## Pass 1 (broad sweep census, honest accounting)

Candidates considered this sitting: 28 re-enumerated 10-05 items (each refetched and scored -
they are from the window and were considered) + 13 fresh in-window X candidates (TeksEdge
09-24, sairahul1 09-18/09-19 x2, JulianGoldieSEO article 09-30, fastinoAI 09-15, dair_ai 09-13,
richmondalake 09-22, BSPK 09-06, the unattributed multi-LoRA X article 09-15, sairahul1's
Dario-Amodei framing post 09-19, plus 4 article objects through pointer tweets) = 41 in-window
items considered; plus 16 out-of-window candidates snowflake-decoded OUT and recorded so the
next sweeper does not re-mine them (v_shakthi 09-03; behrouz_ali 07-13; willccbb 01-09;
MichaelElabd 01-17; LangChain 08-25; hamandcheese 02-07; trajectorylabs 08-11; tanayj article
06-08; pirroh article 07-06; svpino 01-24 and 02-24; _akhaliq 12-23; rohanpaul 01-24 and
01-09; brianzhan 01-09; and 2605.17774 baseline 05-18). Fresh in-window census is 13, under the
30 floor alone; combined with the 28-item confirmation enumeration the floor is met at 41, and
the shortfall is stated rather than papered: the X search door's 1302 storms, the dead AINews
miner, and the article door's selectivity are the three causes.

## Pass 2 (deep reads actually performed)

1. sairahul1 "How To Fine-Tune a Small LLM on Your Own Data (Full Guide)" - article body read
   END TO END (10,850 chars rendered from 61,674 chars of DraftJS JSON through the pointer
   tweet's article.content field; the direct article URL 404s). This RESOLVES the 10-01
   sibling's degraded bank (their item 8: "article body 404 both doors - snippet-only fallback")
   and partially cures the 09-28 sweep's OWED "cyi12 1.5B/200-500-examples post (status id
   never surfaced)" - the claim's carrier is now a resolvable URL with the full text read.
2. dair_ai "Top AI Papers of the Week" (Sep 7-13) - article body read end to end (11,751
   chars); FrogNano entry corroborates the HN-banked row; Procedural Graphs and STAIR are
   agent-memory/retrieval area, not banked here.
3. TeksEdge Macaron-V1.1 post (Sep 24) - full text read through fxtwitter.
4. arXiv 2605.17774 full text - 50,061 chars pulled from arxiv.org/html/2605.17774v2. ESTATE-HELD:
   the 09-30 sibling sweep banked it (their finetuning-adaptation-x.md:13, abstract read end to
   end with the AT-F1 0.65-vs-0.47 and 82.6% numbers). NOT re-banked. My full-text increment,
   for whoever runs the RQ2 A/B: "the serialized tool catalog accounts for approximately 2,200
   of the 2,400 prompt tokens... Description-free inference removes this catalog section
   entirely, reducing the prompt to approximately 128 tokens" - the prompt route spends 91.7%
   of its input budget on the catalog; that is the exact token-budget line the estate's
   skills_pack-vs-QLoRA comparison turns on.

## Overlap ledger (greps actually run, background task exec_7c6931b0, output in session log)

- "Macaron-V1.1": catalog 0; memory only trajectory self-noise; watch .md 0. The bare "Macaron"
  catalog hit is 2609.30535 "Feeding BabyLMs Macaroni" (unrelated). The TeksEdge HANDLE is
  estate-mined (3 status JSONs pulled 10-01, catalog rows 8af80da0fd85/9c792de672cb/9be545e927fd;
  percolator candidate row for status 2099875895846515068 = Google Open Knowledge Format) but
  THIS post (2103001487240487265) is not held anywhere. NEW.
- "sairahul1": surfaced by 10-01 (banked degraded, item 8) and 10-02 (dedup list) siblings.
  This bank is the article-body recovery increment, with that overlap stated.
- "200-500 good examples": the 09-28 sibling carried the same claim as the cyi12 OWED lead.
- "Internalizing Tool Knowledge" / "2605.17774": 09-30 sibling bank. Held.
- "richmondalake": 0 hits catalog + memory/continuity + memory/runs. NEW.
- "amber dock": 0 anywhere except this seat's own falsifier files (the memlance seed).
- BSPK 2096576384080695513: the 10-02 sibling's bank item 6, same article id; their body read
  was also door-down; my probe got title+preview only. HELD, not re-banked.

## Banked items (3, strongest first)

### 1. @TeksEdge: Macaron-V1.1, one 744B base + four 2B LoRAs (2026-09-24, status 2103001487240487265)
Verbatim: "Macaron-V1.1 isn't four enormous specialist models but it has specific LoRAs. 744B
GLM-5.3 base + 2B Chat LoRA + 2B Agent LoRA" (post continues: Coding and GenUI LoRAs, "One giant
shared base intelligence w/ four relatively tiny" adapters). The production-scale existence
proof for the estate's rung-under-gemma:2b lead: specialists are 2B-adapter swappable on ONE
frozen 744B base, which is the same shape as the estate's frozen-janitor + skills_pack design,
with weights instead of prompts as the swap unit. Steal: the estate's case-law graft does not
need a new base model - it needs an adapter slot next to skills_pack.py, and the serving
question (llama.cpp multi-adapter) is the same one the sibling's llama.cpp /v1/systemone bank
already opened. Caveat: single post, no model card or eval linked from it; treat the 744B+4x2B
split as the author's claim. Overlap: NEW per the ledger above. Door: fetched whole.

### 2. @sairahul1 guide article body RECOVERED (2026-09-18, status 2100882424343265527, article 2100822963528560640)
Verbatim from the body: "A 1.5B parameter model fine-tuned on 200-500 good examples can
outperform a frontier model prompted generically at your specific task." The body (read end to
end) is the prompt-vs-weights practitioner law set: fine-tuning "makes a model consistently
better at one narrow task", "Only start fine-tuning after your prompt-only baseline fails at
something specific", split "by company, not by page" because mixing them makes the model
"memorize company-specific language and appear to generalize. It does not.", "Never change the
test set after looking at results", numeric strings "evaluated independently from text quality",
and "Public availability does not mean training permission." Steal: the estate's 300 case-law
rows are the 200-500-examples regime; the guide's own law says skills_pack (prompt route) must
be the baseline arm and the QLoRA arm must beat it on a company-split heldout to justify
existing. Resolves the 10-01 sibling's degraded item 8 and the 09-28 cyi12 OWED lead. Overlap:
stated above. Door: body fetched whole via pointer tweet.

### 3. @richmondalake, Day 1 of 100 Days of Continual Learning (2026-09-22, status 2102345177272647982)
Verbatim: "Most production agents are as capable on day 300 as they were on day 1. The weights
don't change. The prompt rarely changes. The memory, where there is one, just accumulates." and
"The agent has sat through thousands of interactions and learned nothing from any of them."
This is the exact disease the estate's memlance + skill_ledger machinery attacks, stated from
the production side; a 100-day public experiment series worth following for instruments (his
definition line names the guard: continual learning is acquiring "without losing what it learned
before", i.e. the 2609.10750 triangle). Overlap: NEW (0 hits). Door: fetched whole; thread
replies not pulled (day-1 post is self-contained).

## Held / not banked, with reasons

- dair_ai digest: corroborates held rows; its new items are memory-area.
- BSPK, fastinoAI Sep-15 sequel, JulianGoldieSEO Julia-1 marketing article: article bodies not
  exposed by the door (title+preview only); Julia-1 itself is already covered estate-side by the
  sibling's HN row 49860793 and the ggml-org roster (144M mmBERT-small).
- sairahul1's Cuban/Amodei framing posts (09-19): hype register, no instruments.
- Unattributed "How to Serve 100 Fine-Tuned Models on One GPU" X article (2099772866225148024,
  Sep 15): no author handle surfaced, cannot resolve through fxtwitter; OWED lead for the next
  window (multi-LoRA serving is the Macaron item's open half).
- v_shakthi 09-03: out of window on snowflake decode.

## Research question verdicts (X-door edition)

- Q1 (owed confirmation pass): ANSWERED, 28/28 survive, 27 full + 1 pointer-partial; see the
  section above for per-item needle receipts and the two pointer caveats.
- Q2 (prompt pack vs QLoRA on gemma:2b at equal token budget; VRAM gate): the hardware gate is
  MEASURED FAIL on this host: PowerShell CIM read this sitting returns "AMD Radeon RX 5600 XT",
  AdapterRAM 4293918720 bytes (32-bit-capped field; vendor-nominal 6 GB per the sibling's check),
  RDNA1, no nvidia-smi - the GPU-ladder five gates (lens/laws.md:57, L30: arch, VRAM, price
  trigger, software, workload "must ALL hold") fail at arch (RDNA1 != SM90/SM100), VRAM (6 GB <
  24 GB), and software (no CUDA/ROCm training stack), so the QLoRA arm cannot run locally; the
  prompt arm runs at $0 and the finetune arm needs a cloud/CPU-LoRA lane (operator-gated). The
  A/B itself was NOT run - what the window adds is the published prior: 2605.17774 (estate-held,
  re-confirmed alive in full text) shows the QLoRA arm BEATING the informed prompt baseline at
  4B on ~1,700 examples (AT-F1 0.65 vs 0.47, judge 3.88 vs 2.88) while cutting input 82.6%, and
  the catalog spends 2,200 of 2,400 prompt tokens on tool descriptions; against it, the sibling's
  Jeff-thread classical baselines (embeddings+logistic, SVM+bag-of-words at <1 ms) are the
  deterministic-grammar counterweight (L20: deterministic first, $0). The estate-shaped A/B
  remains un-run and is the next probe: skills_pack route vs LoRA route vs classical route on
  the same case-law heldout, CPU-served.
- Q3 (which confirmed methods apply to the decision-model rung and the 2b janitor class): after
  confirmation, the applied set composes three rungs - (a) scoped specialists at 706k-421M
  params on synthetic data, served by llama.cpp /v1/systemone (sibling banks), (b) 0.8B-2B
  Apache-2.0 decision models (Jeff, Gutsy, nimble, sibling banks), (c) the 2b-janitor recipes:
  LoRA r=32 on 0.6B-4B tool-calling (2609.17848, byte-reconfirmed in full text this sitting),
  the CPU-minute trigger ladder (2610.02142), the synthetic/OOD triangle (2609.10750), and now
  the Macaron shape: frozen base + swappable 2B adapters as the production architecture (my item
  1). Training-materials holding (27 rows, corpus.md:33, disk-verified by the sibling) and
  162-PDF papers_reference (corpus.md:27, stale on disk per the sibling's find count of 76)
  carry no additional method rows; corpus/papers holds 2 ledger files, no paper bodies
  (corpus.md:41).
- Q4 (memlance fired-per-turn falsifier, descent leg 7): DESIGNED AND RUN this sitting on the
  local janitor, $0, two instruments in this directory (`_memlance_ab.py`, `_memlance_delayed.py`).
  Immediate form (seed card beside a neutral probe, gemma:2b, temp 0.7, N=5/arm): lance 4/5 vs
  control 0/5 - outputs enact the seed's distinctive content ("Amber Dock", "Thirdday",
  "dredging") unprompted. Delayed form (seed ONLY in the system context, 3 unrelated turns
  between plant and probe, probe seed-free, N=3/arm): lance 2/3 vs control 0/3 after one
  instrument fix - the first probe was degenerate (0/3 vs 0/3, gemma:2b refusing a "real-time
  info" task after arithmetic fillers; reported, not hidden). The skill's own bar
  (.agents/skills/memlance/SKILL.md Falsifier: fewer than 2 of 5 => Disputed) is met in the
  immediate arm and matched in the delayed arm; the sibling's independent temp-0/seed-42 run hit
  2/5 with a diagnostic refusal-flip. VERDICT: leg 7 is NOT prompt theater at the model layer;
  the steering mechanism is real but fragile at 2B (one refusal flip, one style miss across the
  two seats' runs). The MESH-layer claim (seed planted in boot files, cited unprompted in a
  LATER session by a different seat) was NOT tested by either seat and stays OWED - that is the
  five-lance fleet run.

## OWED (could not resolve, not asserted)

- zafstojano article 2097606900745457664 body: not exposed by fxtwitter today (both seats
  concur); the 10-05 section-summary remains the deepest read on file.
- Multi-LoRA serving X article 2099772866225148024: author handle never surfaced.
- fastinoAI "American Open Weight Models: The Opportunity Ahead" (Sep 15): preview only; body
  not exposed; the estate holds the Aug 6 predecessor.
- The mesh-layer memlance falsifier (five lances through real seat boots).
- The skills_pack-vs-QLoRA-vs-classical A/B on the case-law heldout (un-run; hardware-gated).
- richmondalake's remaining 99 days: a watching brief, not a debt.
