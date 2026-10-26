# JEV SALON 2 — STABLE BRIEF (2026-09-19 evening)

You are one lens in the fleet's second Jev salon. This brief is byte-stable
across all lenses; your divergence lives in your post only. Laws that bind
your post: blind divergence (do not read any other lens post), tri-state
claims (SUPPORTED / DISPUTED / UNPROVEN, evidence attached), 150-char
substance floor, and the CITE-OR-FLAG law (new tonight): every external
citation must be one named in this brief, or you write UNCITED. Never
decorate with invented sources. Yesterday's salon pack violated this; its
citations are hereby demoted to UNVERIFIED decor and its verdicts survive on
reasoning only.

End your post with a VERDICT line and a COUNTER line (dissensus is kept,
never averaged away).

## 1. INHERITED DEFAULTS (salon 1, ratified 2026-09-19, still standing)

- ADOPT jev-sift + abide patterns now (hosted-API bugfix counter kept).
- Sovereignty trigger: drop the hosted API only when the open replica scores
  >=0.880 on the fleet's OWN labeled distribution, measured weekly.
- Question linter rules: atomicity (one predicate, no AND/OR), state
  isolation (context in state, never in the question), descriptive criteria,
  one judgment per question, CHOICE options <=4.
- Variable epistemic-load budget replaces the fixed six-question budget.
- Choice-decompose compiler rule: MAX_CHOICE_OPTIONS=4; >4 fans out to
  parallel Nouls, majority vote, VOTE_CONFIDENCE_MIN=0.70, cost guard
  abort $0.001/request.
- A/B/C ontology-evolution falsifier pre-registered (5,000 held-out tasks;
  promotion to C needs Noul>=0.90 on 200 labeled + replica agreement >=85
  percent + regression pass + ECE<=0.06).
- Silence branch default route: QUEUE_RETRY.
- Fleet-Bench disclosure rule v0.1: publish measured labels + structured
  outputs + pre-approved rubrics only.

## 2. NEW FACTS SINCE SALON 1 (all verified this session unless flagged)

- api.typesafe.ai/v1/systemone is ALIVE: GET returns 405, POST without a key
  returns authentication_error. Live front door, key-gated. The fleet holds
  no typesafe key of its own; the operator states Hermes (the specialist
  dispatch seat, $220 armed) has it.
- The specialist counterattack landed: trycua announced CUA-S1, "a family of
  System One models, small, specialized, built for computer use,"
  open-sourcing CUA-S1-FORMS (claimed 706K params / 2.8MB, 99.7 percent on
  their form-filling eval vs hosted Jev 83.6 percent). UNVERIFIED from our
  seat: the trycua/cua README and releases show driver nightlies only; the
  model itself was not found in the probe. Adoption blocked on verification.
- GLiNER2 (urchade) claims: open source for over a year, fine-tunable to beat
  Jev on any of its tasks (author tuned GLiNER 2.5 in 51 minutes; a
  second builder's tuned model scored 99.7 vs Jev 83.6, local, 8.8x faster).
  Repo pointers from tweets, UNCITED-verified (repos exist per GitHub probe).
- Demo wave (vendor-adjacent, UNVERIFIED accuracy): drone swarm sim (15
  drones, <300ms decisions, 100 percent survival); job matching (400
  companies, 12s, $0.0005); session mining (3M replay events, 40s, 132 rage
  clicks, 213 draft PRs claimed for $2.17 — note Jev cannot write PRs; the
  pipeline around it wrote them, the poster's framing inflates the oracle's
  share).
- One operator link carried no Jev content (nzevh_, laptop build day 117);
  filed off-topic, not forced.
- taroleo (prior drop, standing): DeepSeek V4 Flash judgment distilled to 4B,
  26h on a DGX Spark, ~22ms per judgment, exceeded teacher's instant mode.
- The fleet's own judgment primitives are live in mag/verb.py: feels()
  (pack-grounded read), match() (router), classify() (typed one-of-N), the
  silence branch, typed verb rows to watch/inbox/verb_trace.jsonl. Free lanes
  available: groq, openrouter (incl. the or-ling3 lane), nvidia NIM
  (102 models, deepseek-v4-flash verified), ollama janitors (gemma:2b,
  gemma4), z.ai lite. The standing 20-minute drive runs 18+ lanes.
- The salon-1 citation hazard above (myth_scholar invented arXiv IDs and repo
  URLs; gate_builder cited repos we cannot confirm) — hence CITE-OR-FLAG.

## 3. THE QUESTIONS THIS SALON GRADES

1. SPECIALIST SPLIT: tuned specialists beat hosted Jev on hot paths (99.7 vs
   83.6; GLiNER local and 8.8x faster). Ratify the fleet split: Jev-class
   oracles for cold-start triage, routing, and veto; tuned specialists for
   any task that repeats? Where is the crossover line, operationally?
2. HOSTED ADAPTER: the endpoint is alive and Hermes holds access. Build the
   adapter now behind a key flag and A/B it against janitor feels() at
   matched budgets, or wait? What is the smallest honest first call?
3. THE SCALE THESIS (operator's words): "we were launching deepseek gophers,
   we could be running ling/jev 24x7 in the hundreds." What is the unit of
   work for a gopher wave under this architecture, what feeds the label farm,
   and what breaks first at hundreds-of-lanes scale: question supply, ground
   truth, the 0.880 meter, or cost?
4. LOCAL BACKBONE: SemIf (0.845 vs 0.883) vs CUA-S1 (unverified) vs GLiNER2
   (tuneable) vs taroleo-style distillation of our own lanes. What is the
   backbone bet, and what verification do we owe before adopting CUA-S1?
5. ABIDE VETO ORACLE: per-turn rule scoring of every lane turn against rules
   a linter cannot codify. Build it as VERB stone three now, on free lanes?
   What is the false-veto budget?
6. CITE-OR-FLAG: ratify as standing salon law? What is the penalty for a
   lens that decorates?
7. FLEET-BENCH METER: the weekly >=0.880 trigger needs a labeled
   distribution we own. What is the minimal meter we can stand this week
   from the riddler corpora and room events, before any hosted call?
8. COST ENVELOPE: at $0.042/MTok input with free output, what does
   "hundreds of lanes 24x7" cost hosted vs local per month, honestly, at
   fleet-real volumes (not claims-firm volumes)? Name the numbers.
9. ELDER'S QUESTION (from today's lens): the standing record has never been
   cross-examined. Does the retro-witness battery (sample 100 knots,
   re-derive, file survivors/casualties) earn a lane this week, or does it
   wait until after Sep-20?

## 4. FLEET SURFACES YOUR VERDICTS LAND ON

- mag/verb.py (feels/match/classify + silence branch + verb_trace.jsonl)
- configs/lanes.yaml (lane roster, priorities, [L2] escalation)
- configs/providers.yaml (26 provider ids, incl. or-ling3, deepseek lanes)
- queue/lanes/* (per-lane runner_state, trail.jsonl receipts)
- The standing 20-minute drive + cron automations (lean-fire law: read state,
  one line, never inherit conversation)
- watch/inbox/ (durable filings) and the verkle chain (memory/biography/
  verkle_chain.jsonl, 8,686 knots, GREEN)
- mag/jev.py is being built tonight to carry whatever you ratify.

## 5. ADDENDUM (same evening, operator pivot — this outranks section 3 where they conflict)

Seven more drops landed:

- Bespoke Nimble: an OPEN Jev that is not a wrapper. Qwen3.5-9B LoRA, open
  data + open recipe + open weights, NOT distilled from Jev (Jev only scored
  it during training). Contrastive curation: negatives made by flipping one
  key fact (implicit calibration). Parallel constrained decoding: no long
  generation, reads candidate token probabilities directly. Self-eval: Qwen
  66 -> Nimble 90 -> Jev 93 (same 10 categories). ~100ms on H100, runs on a
  MacBook. Caveat: no unified benchmark, may drop outside the 10 domains.
  UNVERIFIED from our seat (tweet + repo pointers only).
- classifier.dev claims to outperform Jev, free. UNVERIFIED.
- Drone split (the keeper): green = Jev's own confidence, purple = "I'm not
  sure, ask the big model." 99 percent self-steered; escalation only on high
  uncertainty. That is a tier ladder with a confidence trigger.
- Runtime level generation: parkour terrain chosen by the oracle while the
  player runs (~320ms, under a third of a cent). "Code governs legality, the
  model governs the next cut." Levels become a decision flow bound to player
  state.
- Jev-as-linter for LLM anti-patterns: AST rules get gamed (Goodhart); a
  judgment tier does not. Immediate inline feedback in the tool loop.
- Keystroke oracle launcher (~100ms intent reads).
- Google TabFM: zero-shot foundation model for tabular data — the credited
  ancestor of column-typed reads.

THE OPERATOR'S PIVOT (verbatim intent): we are making OUR OWN Jev. Self
steal, not greenfield: mine everything the fleet already built, map it, and
synthesize. The target artifacts are (1) OUR OWN RIB LANGUAGE — the
feels-language whose runtime is the RIB (VERB DSL is the embryo: feels() =
pack-grounded read, match() = lane router, while() = standing drive, verb
rows = control-flow kifu) and (2) OUR OWN CACHE OS — the context-as-operating-
system (kernel = FROZEN_RIB at 99.4 percent cache hit, linkage law: energy
and behavior go to zero as prefix stability goes to one, tier packs as the
scheduler, the percolator as memory management). Working method, operator's
words: a scrum environment where the OPERATOR IS THE CLIENT, agents spawn as
agile teams, tracked to working increments — code, not narrated plans. Lessig
applies: code is law — the constitution compiles into the runtime. Every
piece must triangulate to our old ideas: the maze and mud rooms, ractor
faces, kubernetes-style pack launches (pod = several models in tandem over
one packet, agreement = verdict), the evolution loop, the GPS steering
theory, the cognitive control plane, the thought quantizer, the percolator.

QUESTIONS RE-AIMED (grade these in your lens's own voice):
- What does OUR RIB language need from Jev-class primitives that verb.py's
  feels/match/classify do not already give? Name the missing verbs.
- What does the Cache OS scheduler do with confidence? (The drone's green/
  purple split as the escalation syscall.)
- Where exactly does Bespoke Nimble sit in our backbone bet (vs SemIf 0.845,
  CUA-S1 unverified, taroleo distillation)? Does the recipe (one-fact-flip
  negatives) map to our drift-pair corpus method?
- The scrum frame: operator as client, teams as agents, code as law. What
  does that change about how verdicts promote? (The salon itself is a sprint
  review.)

Write your post now. VERDICT line. COUNTER line. Then stop.
