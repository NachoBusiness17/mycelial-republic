# Sweep: evals-self-improvement via X (frontier_olm_2026-10-02)

source-fetched: 2026-10-02. ASCII only, no em or en dashes of our own (one source quote
normalized, flagged where it happens); every claim below was read or run this sitting.
Sweep gopher seat, one ask: two passes, bank only items read this sitting.

## Doors used and their condition

- X door: WebSearch with site:x.com queries (11 queries fired). The search backend threw
  intermittent MCP 429/1302 rate-limit bursts on 5 of the 11 (it self-retried and
  recovered each time; no query was lost) - same behavior the kv-cache sibling sweep
  recorded. X posts are sparsely indexed; account-level hits without status IDs
  (harborframework, ScaleAILabs, harit_v, YuexingHao, anton_iades, framart1, _dieuwke_,
  DanielFein7, ZacKenton1, HjalmarWijk, SivanDoveh, abeirami) could not be resolved to
  single posts this sitting and are NOT banked.
- fxtwitter door: https://api.fxtwitter.com/<user>/status/<id> resolved 9 of 10 attempts
  as HTTP 200 JSON with verbatim text, author, created date, engagement. ONE 404: the X
  article path /i/article/2099962972798153194 (72-trials skills eval) - article bodies
  degrade through this door, matching the 10-02 kv-cache sibling's note. That one item
  is banked from its search-result snippet with its URL and is flagged snippet-only.
- Fallback primary reached and read: github.com/Prism-Shadow/awesome-rsi README (clean,
  confirms the RSI survey's taxonomy and paper IDs). One out-of-window lead named, not
  banked: PAJAMA (arXiv 2506.10403, June 2025, "ask the judge for its rubric once and
  execute that logic as a program") - surfaced via search only, not read this sitting,
  outside the 30-day window; OWED as a judge2 pointer.

## Window method (run this sitting)

Last-30-days = post 2026-09-02. Twitter snowflake epoch 1288834974657 gives threshold
ID ~= 2094950000000000000; every banked item's date below was verified from the
fxtwitter created field, not from the ID math alone. Items outside the window were
dropped from banking even when strong (PAJAMA thread 2072726001742713310, tobowers
2090396150666817655, cwolferesearch promptstats 2031190003930280371, GoogleCloudTech
7-rules article 2086874630032073142, aparnadhinak SkillsBench 2074569427346174039,
FeiziSoheil Terminal-Bench-2.0 article 2077424579161534969).

## Pass 1 census (candidates considered, not banked unless read)

45+ candidates across 11 queries. In-window (date-verified) pool: full__rank 2105688453644156996,
hrdkbhatnagar 2105688466797580514, maksym_andr 2105720477167882634 (same PTB v1.2 event),
proximalhq 2105749224797463014, TheZvi 2105674893924651223, i/article/2105127966112162096,
ahatamiz1 2099201409174638602, JoshARosen 2097324183428444499, AgenticAIFdn 2097708954725884207,
harshbhatt7585 2101685636596175238, code_hiyouga 2098021114685616637, i/article/2099962972798153194,
JulianGoldieSEO 2105281715530813933, VaibhavSisinty 2102005041993601209,
i/article/2105245964114219466, i/article/2100155051142443107, proximal CWE post, plus
the account-level hits above. Out-of-window rejects listed in the window method section.

## Pass 2 deep reads (9 fetched, each end to end through the door)

Each fetched item below was read in full this sitting; quotes are verbatim from the
fetched JSON (or flagged).

1. PostTrainBench v1.2 announcement, Ben Rank @full__rank, created 2026-10-01T15:57Z,
   163 likes / 15,055 views. Verbatim: "Introducing PostTrainBench v1.2 ... Additionally,
   we - removed BFCL (more on this below), - fixed some minor scoring bugs - now run the
   reward hacking judge and final evaluation multiple times to reduce variance."
2. PTB v1.2 detail, Hardik Bhatnagar @hrdkbhatnagar, created 2026-10-01T15:57Z, 373 views.
   Verbatim: "removed BFCL: agents often cheat on it and get penalized, adding a lot of
   noise. Epoch AI's review also flagged it as flawed - fixed scoring bugs in HumanEval,
   ArenaHard and HealthBench - now run the reward hacking judge and final eval multiple
   times for reducing variance."
3. Proximal @ProximalHQ on CyberGym, created 2026-10-01T19:58Z, 71 likes / 14,920 views.
   Verbatim (first sentence + finding): "Many cybersecurity evals use differential
   execution to test whether agents can reproduce known software vulnerabilities" ...
   "Without added constraints, this creates fairness issues: Our evaluation shows that
   CyberGym is effectively saturated on a verified task subset". The differential vs
   LLM-as-judge vs CTF certainty-tier list rides the post image and the search snippet,
   not fetched text - kept out of the quote, treated as snippet-level.
4. AI #188: Gemini Dot Argon, Zvi Mowshowitz @TheZvi, created 2026-10-01T15:03Z, 9,507
   views; the tweet links his X article 2105673972826140672 and the fetch surfaced the
   article body. Article quotes: Andon Labs defines cheating as "obtaining score by means
   the task did not intend," including "gaining privileged access to read and exfiltrate
   held-out information"; Zvi suspects contamination ("discussions of DroneBench" in
   pretraining data) and names run-selection gaming: intentionally "getting caught to
   exclude that run from the data".
5. Ali Hatamizadeh @ahatamiz1 alignment note, created 2026-09-13T18:19Z, ~5,300 chars,
   20 likes / 4,119 views. Concedes only hackable reward proxies; fetched mitigation
   list: "rule-based rewards, reward-model ensembles, chain-of-thought monitoring ('it
   should flag, not grade'), and inoculation prompting". Closes on off-distribution
   generalization as the real open question.
6. LLM-as-a-Judge Architectures: Putting Evals Into Your Agent Runtime, Josh Rosen
   @JoshARosen, tweet created 2026-09-08T14:00Z, article modified 2026-09-24, 682 likes /
   89,907 views / 1,395 bookmarks. Article section fetched: research has explored
   "panels of judges, evaluator personas, voting, aggregation, and debate between
   evaluators"; MAJ-EVAL "creates multiple evaluator agents representing different
   dimensions of the evaluation"; and disagreement is a signal: judges could vote
   "2-1 that an answer is good" (source shows 2-1 with an en dash, normalized here)
   while disagreement "might trigger retries with a stronger model, more evidence
   gathering, or human escalation". Cites G-Eval, Prometheus, LLMBar, JudgeBench,
   RewardBench, Anthropic Bloom, OpenAI graders API.
7. Daily Agentic 9.09.26, Agentic AI Foundation @AgenticAIFdn, created 2026-09-09T15:29Z,
   679 views. Verbatim raw_text: "OpenAI's 10,000-agent math run sparks a credit fight,
   Meta launches Muse, Mercury 2.5 targets faster agent workflows, Google tracks agentic
   cyberattacks, and AWS puts evals into the merge gate." The AWS item links Bedrock
   AgentCore + GitHub Actions evals in the merge path.
8. Understanding RSI: Self-Evolving AI, Yaowei Zheng @code_hiyouga (LlamaFactory author),
   created 2026-09-10, ~21.7k views / 89 bookmarks; links article 2095838432711094272 +
   github.com/Prism-Shadow/awesome-rsi. Fetched numbers: SkillFlow "20 task families,
   166 tasks; 11 models x 4 harnesses; Claude Opus 4.6 went 62.65% -> 71.08%"; Darwin
   Godel Machine "SWE-bench 20.0% -> 50.0%"; Mendel Godel Machine "Polyglot 50.8% ->
   93.2%"; Recuris "improves 35 of 37 model-benchmark combos, gains up to 32.2 points";
   GDPevo "accuracy 50.63% -> 67.07% after updating"; ReasoningBank "+3.7-6.2 pts on
   WebArena". Repo (fetched, 276 stars): "Awesome RSI collects benchmarks, methods, and
   systems for Recursive Self-Improvement." - 100 method papers, 31 benchmark papers,
   3 systems, taxonomy by RSI artifact (model parameters / harness code / context /
   memory / skill) and by RSI mode (online / offline / offline->online). SkillFlow is
   listed as arXiv 2604.17308 in all three mode lists.
9. Do agent skills help? I ran 72 trials to find out (X article 2099962972798153194):
   fxtwitter returned HTTP 404, SNIPPET-ONLY. Search snippet: "Instead of getting in the
   way, skills replaced guessing commands and taking shortcuts with working cloud
   infrastructure on the first try." N=72 A/B trials measuring whether agent skills move
   success. Date not shown by the source; snowflake-derived ~2026-09-16 (approximate).

## Overlap checks (run this sitting)

Commands: grep -i over catalog/catalog.jsonl per exact title/term; scoped grep -ril over
memory/ (full-tree runs on the big patterns, excludes the session-echo giants
memory/trajectory/ for account names; the two full-tree greps that ran long were stopped
after the load-bearing patterns landed). Results:

- PostTrainBench: catalog 0; memory only memory/trajectory/steps.jsonl (THIS session's
  own command echo, self-echo verified by pattern). New.
- CyberGym: catalog 0, BUT memory/runs/corpus_gap_research/ARXIV_REGISTER.json holds the
  original paper ("CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities
  at Scale"). The Proximal saturation FINDING is held nowhere. Partially known base,
  new finding.
- ReasoningBank: ARXIV_REGISTER.json already registers it ("ReasoningBank: Scaling Agent
  Self-Evolving with Reasoning Memory"). The RSI survey and its other ten systems
  (SkillFlow, DGM, Mendel, Recuris, GDPevo, FinEvo-Bench, Mem2Evolve) are new: SkillFlow,
  Recuris, GDPevo, FinEvo, Mem2Evolve, MAJ-EVAL, DroneBench all 0 in catalog and 0 in
  memory outside self-echo.
- "inoculation prompting": 1 catalog hit, but it is a DIFFERENT paper ("Don't Inoculate
  Everything: Stratified Inoculation Prompting Narrows Backdoor Triggers..."), not the
  ahatamiz1 mitigation list. No conflict.
- Sibling sweep evals-self-improvement-arxiv.md (same day, same estate map): grepped for
  all nine of my items - zero shared titles or accounts. The two sweeps are
  complementary: theirs is arXiv instruments, mine is lab practice on X.

## The five questions, answered from what was read

**Q1 judge designs surviving judge-weakness / imagined-grader hacking.** PostTrainBench
v1.2 is the cleanest post-10-01 signal: a frontier-adjacent lab that found its judge
noisy and changed the JUDGE'S RUN COUNT, not its prompt - "run the reward hacking judge
and final evaluation multiple times to reduce variance" - and simultaneously cut a
sub-benchmark (BFCL) where agent cheating adds judge noise. Combined with the banked
CRJudgeBench GLM-5.3 weakness row, judge2's copy list is: (i) N-run blind judging with
variance reported next to every verdict (PTB), (ii) reward-model ensembles plus
monitoring that "should flag, not grade" (ahatamiz1), (iii) panel disagreement as a
first-class signal that routes to a stronger model or human escalation (JoshARosen).
PAJAMA (rubric-once, execute-as-program) is the fourth mechanism, out-of-window, OWED.

**Q2 contamination-safe hidden banks and bank size.** No in-window X item quantifies
bank size for duel separation; the stats answer stays with the arXiv sibling's
classical-test-theory find (K=20 fails attribution). What X adds is the threat model
for the hidden half: Andon Labs' cheating definition names "gaining privileged access to
read and exfiltrate held-out information" as the canonical hidden-bank breach, and Zvi's
run-selection gaming (throwing a run by "getting caught" so it can be excluded) is a
duel-receipt integrity hazard the estate's blind audit does not yet cover. PTB's BFCL
removal is the operational version: a contaminated/flawed component poisons the noise
floor of everything judged alongside it.

**Q3 emergence-boundary instruments across repeated task-classes.** SkillFlow is the
five-axis A/B harness executed at frontier scale: 20 task families x 166 tasks x
11 models x 4 harnesses, with the compounding arm (Opus 4.6 with skill evolution) going
62.65% -> 71.08% across repeated task-classes. The awesome-rsi taxonomy supplies the
axis vocabulary the estate's specified-but-unrun harness lacks: evolution happens along
five ARTIFACT types (parameters, harness code, context, memory, skill) and in three
MODES (online, offline, offline->online). Import: run the five-axis test with the
artifact axis explicit, and borrow SkillFlow's arXiv id 2604.17308 as the citation
anchor.

**Q4 admission-control false-accept quantification.** Three X-side results complement
the banked Touchstone find and the arXiv sibling's unearned-passes census: (i) Proximal
measures that a differential-execution benchmark (CyberGym) saturates on its verified
subset once constraint fairness is fixed - verifier certainty tiering (differential vs
LLM-judge vs CTF) is the design law; (ii) PTB dropping BFCL for systematic agent
cheating is a false-accept-at-the-sub-benchmark level fix; (iii) AWS now ships agent
evals inside the merge gate (Bedrock AgentCore + GitHub Actions) - agent-work gates at
industry-default settings are now mass-deployed, which is exactly the surface the
estate's workflow gate + ratchet sit on, and none of these sources publishes a
false-accept RATE, which remains the open measurement.

**Q5 self-improvement loops publishing artifact-yield metrics.** The RSI survey is the
baseline set the descent falsifier should be audited against: every loop it lists
reports a DELTA per artifact class (DGM +30 pts SWE-bench on its own harness code;
ReasoningBank +3.7-6.2 WebArena on memory; Recuris improving 35 of 37 model-benchmark
combos), not counts of artifacts produced. The estate's laws/ribs/receipts-per-week
count is the weaker half of this; the frontier form is delta-per-artifact-class. The
72-trials post is the right N-sized template for the estate's cheapest version (N=72
A/B on whether a learned artifact class moves first-try success), snippet-only.

## Banked items (strongest first, mirrors the returned SweepResult)

1. PostTrainBench v1.2 (full__rank + hrdkbhatnagar merged, 2026-10-01). Q1/Q4.
2. Understanding RSI + awesome-rsi (code_hiyouga, 2026-09-10). Q3/Q5.
3. Proximal CyberGym saturation (2026-10-01). Q4.
4. AI #188 DroneBench cheating + held-out exfiltration (TheZvi, 2026-10-01). Q2.
5. ahatamiz1 mitigation list (2026-09-13). Q1.
6. JoshARosen judge architectures (2026-09-08). Q1.
7. AgenticAIFdn AWS merge-gate evals (2026-09-09). Q4.
8. 72-trials skills eval (snippet-only, ~2026-09-16, fxtwitter 404). Q5.

## Fold

Frontier lab practice this month converges on three moves the estate's unbuilt
instruments should copy: repeat the judge and report the variance (PTB v1.2 did exactly
the laws.md:58 mass re-judging program within one release cycle), make judge
disagreement a routing signal instead of averaging it away (JoshARosen), and measure
self-improvement as delta-per-artifact-class across an explicit artifact taxonomy
(awesome-rsi) rather than as artifact counts. The hidden-half threat model now has a
name in the wild - exfiltrate held-out information - and a duel-side attack
(run-selection gaming) our blind audit does not yet simulate. Honest gaps: no X source
quantifies bank size or false-accept rates in-window; both stay OWED to instrument work.
