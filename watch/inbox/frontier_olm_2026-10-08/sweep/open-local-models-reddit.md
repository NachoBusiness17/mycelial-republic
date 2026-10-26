# SWEEP: open-local-models via reddit - source-fetched: 2026-10-08

Seat: sweep-open-local-models-reddit (frontier gopher, dynamic workflow actor_3_3).
Window: last 30 days (2026-09-08 through 2026-10-08). Repo: C:/Users/foste/Documents/projects/local_sovereign_agent.
Dedupe base: the day-7 reddit lane bank (watch/inbox/frontier_olm_2026-10-07/sweep/open-local-language-models-reddit.md, read in full this session) plus the 10-02..10-06 sibling banks named below.

## Door status (degraded doors recorded; no fabricated fallbacks)

- Recipe primary door `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50`: WALLED for
  WebFetch (live re-confirmation this session: HTML "Welcome to Reddit / Skip to main
  content" stub, zero JSON; identical to lens/doors.md:62 of this folder's lens).
- **The curl+UA bypass OWED at lens/doors.md:64 is now MEASURED, verdict NEGATIVE.** curl
  with a Chrome 126 browser UA on the same old.reddit JSON URL: HTTP 302 to
  `old.reddit.com/login/?reason=lor2&dest=...`, which 404s "Not Found" after -L. The
  www.reddit.com JSON variant with the same UA: HTTP 403 with a 189,908-byte HTML body.
  Reddit JSON is dead from this box on BOTH instruments today; do not spend more probes on
  it until Reddit changes the wall.
- WORKING DOORS this session, all verified live:
  1. RSS `www.reddit.com/r/<sub>/top/.rss?t=month` via curl + browser UA: 200 for all four
     subs (LocalLLaMA 59,974 B; LocalLLM 77,094 B; MachineLearning 76,210 B; ollama
     113,630 B) after 429 retries spaced 18-55 s. Parsed locally with repo venv
     xml.etree (sweep/tmp/parse_rss.py). 100 entries projected, raw kept in sweep/_raw/.
  2. arctic-shift API (`arctic-shift.photon-reddit.com/api/posts/ids?ids=...` and
     `/api/comments/search?link_id=...&limit=100&sort=desc`): 8 pulls, all HTTP 200, clean
     with 12 s spacing (83487 + 197953 + 214890 + 33189 + 79837 + 42188 + 201977 + 188678 +
     205757 B). All reddit quotes below are byte-verbatim from my own local parse of these
     JSON payloads, not from a fetch-model summarizer.
  3. HN Algolia `search_by_date` RE-VERIFIED (the clause lens/doors.md:54 left open):
     three queries (`ollama` nbHits 80, `"open weights"` nbHits 17, `llama.cpp` nbHits 24,
     numericFilters created_at_i>1788825600 = 2026-09-08T00:00Z, epoch computed with repo
     venv python) all HTTP 200. The 10-06 seat had already executed this endpoint (10-06
     open-and-local-models-x.md records it EXECUTED, ANSWERED); this is an independent
     same-day re-verification.
  4. fxtwitter: StepFun tweet resolved primary-side (HTTP 200). github releases.atom
     (ollama) via curl+UA: HTTP 200, byte-parsed locally. WebFetch on runtimewire.com and
     devblogs.microsoft.com: worked; those two quotes carry the fetch-layer discount noted
     inline.

## Pass 1 - candidates considered (100 RSS entries + ~40 HN stories + 16-thread arctic batch)

Already HELD by prior banks (checked per ID, NOT re-banked): 1wmzky1, 1wcbid7, 1wj6c4l,
1wmxfjs, 1wt5f4e, 1wv1u54, 1whqwdq, 1wyefkt, 1wqxbwa, 1wc6tka, 1wgzpli, 1wyruu5 (day-7
bank); 1wlhh08/1wlh7us hemmingway-1 (banked TWICE: 10-06 finetuning-adaptation-arxiv.md
item 22 and 10-07 finetuning-adaptation-reddit.md item 1 via the 1wm88t6 crosspost);
1wijo3e Jev open prior art (10-06 finetuning-adaptation-reddit.md section 2; 10-05 bank
notes "estate has memory/runs/jev_salon/ - overlap, skipped"); 1wdasar Spanda (10-03
evals-and-self-improvement-reddit.md, twice, with the full calibration ladder: Qwen 1.5B
AUROC ~0.58 / Mistral 7B ~0.71 / Qwen 27B ~0.89 / 120B collapsed 0.09, and the T>=0.5
sampling condition); 1wt0tot Qwen3-4B MMO swarm (09-30 swarm-orchestration-reddit.md item
8, with the load-shed quote and the license resolution); 1wvz1ex iPhone second GPU (10-05
open-local-language-models-reddit.md item 8); 1wuv6oh Hillock (same project held as 10-03
agent-memory item 13 via 1vnhojf "Hillock v0.4"); Step 5 Preview tease (10-06
open-and-local-models-x.md: "estate-resolved via fxtwitter Oct 2"); Ollama 0.35 Jev-style
decision models (day-6 register rows); Clef open weights (day-6 deep read 1wvz1ex-adjacent
1wv4zzi); Ollama v0.40.0 (day-7 DIGEST.md:18).

Considered and dropped with reasons: 1wk9fag Alibaba medical open model (off-scut, size
unknown from title, SCMP not fetched); 1wdbvlt HF security.txt (security area, not this
lane); 1wepx7w + 1wzpzh3 + 1wma856 + 1wymgu6 (image/meme tier, no text body); 1wvxih5 M4
Max benchmark (over-band personal bench; 30-day Qwen 3.8 thread already held via 1whqwdq);
1wth4iz Anthropic GLM ad (hosted discourse); 1wffmri uncensored list thread; 1wiijww /
1wq653p / 1wo3fyy / 1wxk0xi / 1wj0arv / 1wexswf / 1wms2s9 / 1wxgqir / 1wkl0wz (consumer
setup and app threads); 11 hardware threads (1wz6ist, 1wze6g5, 1wy1o7y, 1wpfxje, 1wdramg,
1wr8et1, 1wo77e7, 1wpawqj, 1wqg3ld, 1whf7ov, 1wtc4j9); 1wlgrft Qwen-Image-2.1 (image-model
release, out of lane); 1wz3wq6 / 1wf3i1m / 1wk979c / 1wkocvj / 1wf4yqe / 1wrtokp (meta);
49878572 jeva.cpp (snippet-tier, repo not fetched); 49911995 Magnitude (engine, not
model); 49835080 IttyBittyAI Qwen2.5:0.5B (demo of pre-window model); 49938916 justine.lol
matmul + 49859982 prompt-lookup drafting + 49812339 transformers-runs-llama.cpp-quants
(inference/quant lanes, not this lane); 49794230 SoTA Feed tracker (a release-tracker
product, noted for RQ5 only); 49978040 Mistral Le Chonk 1T (over-band landscape);
49676085 / 49711455 / 49769183 / 49922248 / 49702607 / 49698231 / 49747378 / 49662740 /
50003460 / 49863937 / 49845314 / 49876817 (discourse/snippet tier).

NEW this sweep (surfaced before but never banked, or brand new): 1wo6o0f, 1wx0jtb
(+article), 1wbfrut, 1wi32jg (+tomshardware), 1wuqsyy, Ollama v0.40.1/v0.40.2 (released
TODAY), Windows ML devblog (Oct 7), plus the 1wt0tot comment-level delta (held thread).

## Pass 2 - deep reads (8 threads end to end: OP + top comments; minimum was 5)

Byte-parsed via arctic JSON (OP + comments sorted by score): 1wijo3e (78 of ~200 live
comments), 1wlhh08 (99 of 131), 1wo6o0f (92 of 240), 1wdasar (15 of 15), 1wt0tot (36 of
36), 1wx0jtb (17 of 17), 1wbfrut (93 of 199), 1wvz1ex (pulled 205 KB, not analyzed;
thread held). Fetch-layer reads: runtimewire DwarfStar article (full);
devblogs.microsoft.com WinML post (full); HN item 49736660 (thread JSON with comments);
api.fxtwitter.com StepFun tweet (full text); github ollama releases.atom (last 8 releases
with bullets). 1wbfrut's headline is an i.redd.it IMAGE: unread from this seat, claim
stays title-tier (stated per item).

## The eight banked items (strongest first)

1. **Ollama v0.40.1 AND v0.40.2 landed today (2026-10-08); v0.40.1 carries a Windows-only
   Clef decision-model correctness fix.** releases.atom bullets (byte-parse):
   "llama: fix clef head reads past 2GiB on windows by @Gigrise in #18777" and "manifest:
   avoid symlinks on Windows by @dhiltgen in #18852" (v0.40.1, updated 2026-10-08T02:09:43Z);
   v0.40.2 (2026-10-08T16:53:47Z) hides duplicate/downgrade guards from the model list.
   Day-7's bank read "Ollama's newest remains v0.40.0", so this is a 24-hour runtime delta.
   Estate bearing (RQ2/RQ3): the estate box is Windows; Clef-class decision-model heads
   misread past 2GiB on Windows until today, the same per-OS/per-backend correctness class
   as b11475's Metal bug (day-7 item 1): serving choice carries correctness, not just
   speed. The manifest-symlink change touches the same manifest layer the estate's P3
   digest-pinning gate reads at boot; re-run the weekly manifest-hash standing form after
   any upgrade past v0.40.0.
2. **Jev astroturf meta-thread, moderator-confirmed (r/LocalLLaMA 1wo6o0f, 2026-09-23,
   1182 pts, 240 comments).** OP verbatim: "Jev is a paid product that dumped a lot of
   venture capitol money into shill their product here and in other subreddits. Obvious
   shill posts are obvious." Moderator u/ttkciar (34 pts): "The moderators have been
   removing off-topic Jev posts, while leaving posts up when they are about Jev in an
   on-topic way, for example developing local equivalents to Jev." u/FormerKarmaKing (4
   pts): "The simultaneous launch of so many breathless YouTube videos was the real smell
   to me." This answers the day-7 OWED ("Jev's vendor identity beyond this is not
   established", DIGEST.md:17) at community tier: paid VC-funded product with a coordinated
   promotion push. Any estate cell that would ever cite hosted-Jev numbers should carry the
   marketing-condition flag; the open stack (llama.cpp /v1/systemone, Ollama nimble,
   jeva.cpp fork) is the clean instrument surface. Overlap: the priority-contest thread
   1wijo3e is held (day-6 finetuning bank section 2), JevBench snapshot held (Laya 58.4 vs
   Jev 86.6), Laya mechanism held (09-30 swarm bank via 1wrzjib, 322M typed-output decider,
   ~3.1s/forward on 2 vCPU); this astroturf thread sat in day-6's pass-1 ID list only.
3. **Windows ML ships experimental llama.cpp support (devblog, 2026-10-07).** Fetch-layer
   quote: "Windows adds experimental llama.cpp support to Windows ML so you can run GGUF
   models locally." Task APIs (text generation, speech recognition) plus an
   OpenAI-compatible local endpoint; the article's example model is Qwen2.5-0.5B (in-band).
   HN secondhand titles ("MS announces DeepSeek V4 Flash and Nemotron locally") are a
   title-vs-page MISMATCH: the devblog names neither DeepSeek nor Nemotron; NVIDIA appears
   only as a llama.cpp collaborator. Estate bearing: a third serving stack on the estate's
   own OS with its own behavioral surface; if the estate ever A/Bs serving choice (RQ2),
   WinML is now a fourth arm next to Ollama/llama.cpp-native/vLLM. Overlap: catalog 0,
   memory 0, no prior bank (clean).
4. **DwarfStar ds4 (antirez), first full estate read (r/ollama 1wx0jtb, 2026-10-03 + 
   runtimewire article, pub 2026-10-02).** Narrow MIT-licensed C engine supporting ONLY
   DeepSeek V4/V4.1, GLM 5.x, Qwen3.8 Flash Next; compresses routed experts to ~2-bit while
   keeping shared/critical paths higher precision; treats the KV cache as persistent data,
   saving prompt-prefix state to SSD and restoring matching prefixes after restart;
   project-published numbers 39.4 tok/s (M5 Max 128GB, 2,048 ctx) / 27.6 tok/s at 65,536;
   verbatim: "AI is too critical to be just a provided service." Community economics
   pushback is the lesson: hardware ROI math (EUR 5,889 M5 Max vs subscriptions) and the
   privacy-only defense ("only reason for a local model is full privacy. Economics of
   local models are out the window"). Estate bearing: the SSD-prefix-restore idea converges
   with the estate's ReFold reversible-folding bank (day-7 item 15) and the day-7 Curie
   17B SSD-serving OWED (pass-1 only until now; this is the same class, read). Overlap:
   surfaced 10-03 pass-1 ("1wwolhh antirez ds4 engine"), 10-04 title-level ("bodies not
   fetched"), 10-06 pass-1; never an item; the runtimewire hit in the 10-05 quant bank is
   a DIFFERENT article (Bartowski per-tensor maps); catalog 0, memory 0.
5. **Held-thread comment delta: the Qwen3-4B workhorse role-split and an explicit
   small-tier benchmark wish (1wt0tot, comment field).** OP u/kristiantalley679 (author,
   3 pts, byte-verbatim): "The 4B does goals, trades, reflection, the plausibility checks,
   and the short in-character replies when nobody is watching a character. Gemma or
   Mistral at the small tier is worth a benchmark. Would love to see one." u/WolpertingerRumo
   (16 pts): Qwen is "a great workhorse, not for conversation", pointing at Gemma/muse/
   Ministral for the conversational tier. The thread is held (09-30 swarm item 8), but the
   bank's quote was the load-shed line; this role-split datum is new. Estate bearing
   (RQ1): a field practitioner running 400+ agents independently wishes for exactly the
   estate's unmeasured comparison (gemma vs peers at the small tier); the band question is
   open in the wild too, and Qwen3-4B keeps field-validating as the 4B workhorse shape.
6. **Mozilla report: open-closed gap ~4.4 months, "drastically cheaper" (1wi32jg +
   tomshardware, 2026-09-16).** Fetch-layer verbatim: "Mozilla's fit on METR task-horizon
   data puts the open-closed gap at around 4.4 months, in line with Epoch AI's four-month
   estimate." Estate bearing (RQ4/RQ5 context): the cheap-open-rung thesis the garden
   prices keeps getting external support; a 4-month gap on task-horizon is the backdrop
   for the per-animal re-measure debts (grok-4.7 champion cell, fable-5.1 plan_call): the
   dollar alternative is not standing still. Report-tier, not instrument-tier; cannot fill
   a cell (INSTRUMENTS ONLY, memory/rib/RIB_MODEL_GARDEN_ROUTING.md:47-53). Overlap: ID
   sat in 10-05/10-06 pass-1 lists only; gap number not previously banked (checked).
7. **Consumer VRAM reality at the band's floor, on a thread whose own headline is
   UNVERIFIED (1wbfrut, 2026-09-09, 1187 pts).** The headline ("Deepseek Has Soft Retired
   Deepseek V4 Pro") is an i.redd.it image this seat could not read: the retirement claim
   stays title-tier and is NOT banked as fact. What IS readable and banked is the comment
   field: u/Due-Memory-6957 (17 pts, byte-verbatim): "All these models people are calling
   medium and sometimes even small are actually huge", with the Steam-survey framing that
   modal consumer VRAM is 8-16GB and RAM 16GB, "not enough to run Deepseek flash even at
   Q2" on split GPU+CPU. Estate bearing (RQ1): the community's own floor math keeps
   confirming the estate's 0.5B-8B band as the honest local band; and IF the retirement is
   real it is a family event (RIB_MODEL_GARDEN_ROUTING.md:54-57) for any DeepSeek-hosted
   row, so an estate-side check of the DeepSeek model list is owed. Confidence capped 0.55
   for the unverifiable headline.
8. **Gemma 5 watch-row, rumor-tier (r/LocalLLM 1wuqsyy, created 2026-10-01, 405 pts, 135
   comments).** OP selftext (byte-verbatim): "Gemma is based on Gemini and going by the
   latest Gemini release, those of us who appreciate abilities other than coding should be
   eating good when Gemma 5 comes out (end of year maybe?)." No announcement exists; this
   is expectation-setting only. Estate bearing: the janitor fleet is gemma:2b + gemma4
   (AGENTS.md), so a Gemma 5 drop would be a fingerprint/family event forcing re-measure
   rows across the local rungs (RIB expiry law); park this as a watch-row so the seat that
   owns lanes.yaml pins sees it coming. Confidence 0.45 (rumor tier, image-post OP).

## RQ verdicts (grounded in the reads above)

- **RQ1 (0.5B-8B releases beating gemma:2b on lane scut): still unmet; band stays
  UNMEASURED and that stays legal.** No new in-band release with instrument evidence
  surfaced in-window: the new open reads are over-band (hemmingway-1 27B, held; Step 5
  27B-active, held; Mistral 1T) or same-product churn (Hillock). Field data keeps the
  Qwen3-4B workhorse shape and explicitly wishes for the estate's missing comparison
  (item 5). The decision meter remains n=0 (mag/verb.py:493 meter_valid False; lens/
  burns.md:85-86); nothing read changes that. The estate battery remains the only court.
- **RQ2 (harness/serving vs weights): two fresh per-OS correctness datapoints on the
  estate's own platform.** v0.40.1's Windows Clef head fix (item 1) and the b11475 Metal
  bug (held) are the same disease on different backends; Windows ML adds a fourth serving
  arm (item 3); ds4's narrow-engine thesis (item 4) is the vendor-side extreme of the same
  law. The split of gemma:2b's janitor pass-rate into serving-vs-weights shares is NOT
  computable from public evidence; it needs the estate's own A/B (not run here; reported
  as not run).
- **RQ3 (alias classes surviving P3 pinning): no new aliasing reports read this window.**
  Adjacent delta: v0.40.1 changed Windows manifest handling (item 1); the digest-pinning
  gate's weekly manifest-hash form should re-run over the local registry after any daemon
  upgrade. Which local tags still alias byte-identically is an estate probe; not measured
  from this seat.
- **RQ4 (grok-4.7 champion re-measure Q5; fable-5.1 plan_call re-measure Q6): nothing
  public touches either cell.** The only fable-relevant datum is hemmingway-1's vendor
  self-benchmark (held, marketing-conditioned); it cannot fill a cell. Both re-measures
  remain estate probe debts; this sweep neither confirms the suspect cells nor re-routes
  dollars. Mozilla's 4.4-month gap (item 6) is the backdrop, not a verdict.
- **RQ5 (does the hn.algolia-first mix feed the garden's 30-day expiry): yes, measured.**
  Latency evidence from this session: v0.40.2 (released 16:53:47Z today) was in my
  releases.atom pull within hours; Step 5's "Open weights on Oct 15." (fxtwitter verbatim)
  was caught 25 days ahead, and the 10-06 seat had already resolved the same tweet Oct 2.
  Reddit-side the mix needs pacing (RSS 429 retries at 18-55 s; arctic 12 s spacing), and
  the JSON doors are dead on both instruments (curl+UA bypass measured NEGATIVE, door
  status above): the garden's candidate flow survives on RSS + arctic + HN. The grid
  itself still fills from estate instruments only (RIB:47-53); doors nominate, never fill.

## Overlap receipts (instrument: rg 15.2.0; -i -c over catalog/catalog.jsonl 1,195,926
rows; -i -l over memory/; ID-level greps over all frontier_olm_*/sweep/*.md)

- v0.40.1/clef-head-fix: catalog "0.40.1" 612 = substring noise in unrelated version
  strings (inspected: vast_charges.jsonl, derived_dag_index); prior banks stop at v0.40.0.
  NEW.
- 1wo6o0f / astroturf / ttkciar: zero hits across all frontier_olm banks as an item;
  ID present in day-6 same-area pass-1 list only. Jev holdings disclosed in item 2.
- Windows ML / winml: catalog 0; memory hit is unrelated corpus HTML (dlb_ml.html);
  banks 0. NEW.
- DwarfStar / 1wx0jtb: pass-1 and title-level mentions only (10-03, 10-04, 10-06 quant
  banks); the 10-05 runtimewire hit is the Bartowski article, not this one; catalog 0,
  memory 0. First full read.
- 1wt0tot: thread held 09-30 (swarm item 8); the role-split OP comment and the
  WolpertingerRumo workhorse line are the new deltas (checked the banked quote).
- Mozilla / 1wi32jg: ID in 10-05/10-06 pass-1 lists; gap figure not previously banked.
- 1wbfrut: ID in 10-04/10-06 pass-1 lists; comment-tier band datum new, headline
  unverified (stated).
- 1wuqsyy: ID in 10-02/10-06 pass-1 lists; never banked.
- Dropped as held this session (verified, not assumed): 1wlhh08 (banked twice), 1wijo3e
  (day-6 section 2 + jev_salon note), 1wdasar (10-03 twice), 1wt0tot (09-30), 1wvz1ex
  (10-05 item 8), 1wuv6oh/1vnhojf Hillock (10-03 item 13), Step 5 (10-06 fxtwitter),
  hemmingway comment deltas and the 1wt0tot shed quote stay with their original banks.

## OWED (never asserted as fact)

1. 1wbfrut's retirement image: unread (no OCR instrument from this seat); the DeepSeek V4
   Pro retirement is title-tier until an estate seat reads the screenshot or the provider
   docs.
2. Step 5's "Open weights on Oct 15." is the tweet's promise; the drop itself unverified
   until it lands (7 days out).
3. 1wijo3e's comment tail: 78 of ~200 live comments parsed; deeper tail unparsed.
4. 1wvz1ex comments pulled (205,757 B) but not analyzed; raw kept at _raw/ for the next
   seat (thread held).
5. Estate probes named in the RQ verdicts (meter run, alias re-hash, serving-vs-weights
   A/B, DeepSeek model-list check) are on-estate instruments, not runnable from a sweep
   seat; reported as not run.
6. Fetch-layer quotes (runtimewire, devblogs, tomshardware) carry the WebFetch
   summarizer discount; byte-exact re-pulls are the honest next step before any of them
   routes dollars.
7. The first overlap-grep loop (grep -i -c over catalog.jsonl) ran long in background and
   was abandoned for rg; no output from it was consumed. All overlap fields above come
   from the rg receipts only.

## Machine receipts (all run this session)

- curl probes: old.reddit JSON (WebFetch stub + curl 302/login/404 + www 403), RSS x4
  subs (200s after 429 pacing), arctic-shift x9 (200s, 12 s spacing), HN Algolia
  search_by_date x3 + items/49736660 (200s), api.fxtwitter.com StepFun (200),
  github ollama releases.atom (200).
- Local parses (repo venv python, no trusted fetch-model conversions): sweep/tmp/
  parse_rss.py (100 entries), sweep/tmp/parse_arctic_ops.py (16 OPs),
  sweep/tmp/parse_arctic_comments.py (8 threads), inline JSON/atom readers for HN items,
  fxtwitter, releases.atom. Raw payloads: sweep/_raw/ (rss_*.xml, arctic_ops_batch1.json,
  arctic_comments_*.json, hn_*.json, hn_item_49736660.json, fx_stepfun.json,
  ollama_releases.atom).
- Dates: created_utc / atom updated / tweet created_at read directly from payloads;
  epoch 1788825600 for the window start computed with repo venv python.
