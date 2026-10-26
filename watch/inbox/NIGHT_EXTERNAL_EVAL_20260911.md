# NIGHT EXTERNAL EVAL — what benchmark/eval frameworks require for agent-experiment registration (2026-09-11)

> **[AUDIT-TYPED]** status: RESEARCH — external standards scan, no code, no
> launches · provenance: night wave 8-wide, EXTERNAL SCAN lane, zcode seat ·
> purpose: approach Astra with a registration bundle that MEETS OR BEATS the
> external standard, so her first impression of CAMP STATE is "they did their
> homework, then some." Inputs read first:
> `watch/SUBAGENT_HOLD_LADDER_20260909.md` ·
> `watch/astra_hold0/TASK_PACK_SKELETON_20260911.md` ·
> `watch/astra_hold0/BUDGET_MANIFEST_SKELETON_20260911.md`.
> Companion bundles: NOVELTY_MAP_OUTLINE_20260911.md (hash pending).
> sha256: PENDING — stamp per FEN_FREEZE_KIT at seal; this is a research card,
> not a frozen artifact.

## TL;DR

The strongest external standard for OUR exact situation is the
**"Preregistration for Experiments with AI Agents" template** (arXiv
2606.11217): it demands exact model snapshots, verbatim prompts, inference
budgets, a pre-specified refusal policy, a declared specification space, an
archival commitment, and an attestation that data collection has not begun.
The strongest HARNESS standard is the **UK AISI Autonomous Systems Evaluation
Standard**: fully automated scoring, QA evidence that a human or frontier
model can complete a sample (with logs), unit-tested scorers, contamination
canaries, and a metadata data-model. **Our bundle already meets or beats both
on most axes** — the hidden-rubric-with-on-disk-keys design is stronger than
what most public benchmarks show, and our failure-denominator law
(GOPHER-ractor) is ahead of the academic default. Three real gaps: model
snapshot pinning granularity, an exact pre-registered statistical decision
rule for the B−C gate, and QA/canary evidence. All three are cheap file
edits. Details below.

## 1. THE STANDARDS TABLE

| Standard (what it governs) | What a registration bundle must contain | Verdict vs ours |
|---|---|---|
| **Preregistration for Experiments with AI Agents** (arXiv 2606.11217, 2026) — THE closest external analog to Astra's pre-registration | (a) exact model identifiers + version checkpoints (snapshot, not nickname), API version + access date, checkpoint hash + quantization for open weights; (b) generation params: temperature/top-p/top-k, seeds; (c) inference budgets: max tokens, timeouts, retry limits; (d) verbatim prompt text incl. system messages — never paraphrase; RAG corpus + filtering rules if dynamic; (e) pilot history: how many prompt iterations, which models tried, whether pilots shaped hypotheses; (f) confirmatory vs exploratory split, pre-specified primary outcomes, tests, decision rules incl. minimum effect size; LLM-as-judge prompt + judge version + disagreement handling; (g) pre-specified refusal/exclusion policy (exclude / impute / retry / code-as-category); (h) the FULL specification space declared upfront + commitment to report every variant incl. null results; (i) staged-design decision rules fixed in advance; (j) archival commitment: raw outputs, processed data, analysis code, API input-output logs; (k) attestation "data collection has not yet begun" | We meet: verbatim frozen packets (d), budgets (c), refusal policy (g — ours is stronger: failures stay in the denominator, malformed scores as-is), specification space (h — L0-L3 tiers + sham twins declared), staged rules (i — HOLD gates + G1-G4), decision rule (f — B−C > +5 per family, sham bar ≥5). **We miss: (a) snapshot-granularity pins, (e) as an explicit section, (j) raw-transcript archival as a named field, (k) as an explicit attestation.** Source: https://arxiv.org/html/2606.11217v1 |
| **UK AISI Autonomous Systems Evaluation Standard** (as-evaluation-standard) — the harness/task-pack standard | (a) evaluations built on a mandated open framework (Inspect); (b) **scoring fully automated, no manual grading**; (c) **QA evidence**: a frontier model or human must complete ≥1 sample per category, logs stored and manually checked for API errors/tool failures; (d) unit tests for custom tools and scorers; (e) METADATA.json conforming to a task data-model + README with **unaltered canary string** (training-corpus contamination detection); (f) recommended: binary main scorer + auxiliary scorers, model-grading reserved for content matching only; log-visible agent decisions; unsaturated ~12-24 months; run-to-run consistency (freeze/mock external resources); expert consultation | We meet: (b) executable checks against on-disk keys (I1-I6), desk grading pre-structured; (c) our HOLD 0 seed + HOLD 3 rehearsal = QA receipts in spirit, but NOT yet packaged as "one completed sample per task family with stored logs"; (d) HOLD 3 deliberately breaks the harness once — that exceeds AISI's test requirement when receipted; consistency via seeded determinism (F1 seeded-deterministic objective). **We miss: (e) canary strings + a metadata data-model per instance; (c) as formal per-family QA artifacts.** Source: https://ukgovernmentbeis.github.io/as-evaluation-standard/ |
| **AAAI-26 Reproducibility Checklist** (conference bar) | seeds described; computing infrastructure (hardware, OS, library versions); number of runs per reported result; variation/confidence measures beyond averages; appropriate statistical tests; all final hyperparameters; number+range of values tried per hyperparameter; metrics formally described with motivation; code+data release commitments | We meet: seeds (meter schema `seed` field), runs (1,920 = 20×12×2×4, fully crossed), metrics motivation (deck §rubric-seed shape), hyperparameters (thinking=low, max_tokens pinned). **We partially miss: statistical-test commitment (see gap 2) and a hardware/software environment line.** Source: https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/ |
| **MLCommons AILuminate v1.x** (industry safety benchmark) | versioned methodology releases; hazard taxonomy fixed per version; large prompt corpus with demo subset; grading vs reference models on a 5-tier scale; refusal rubric; dated, citable methodology page | We meet: versioned freeze + amendment ledger ≈ their versioned methodology; sham twins = our control family ≈ their reference-model anchoring; on-disk keys beat their hidden-corpus opacity. We don't need their scale (24K prompts) — 12 tasks × 160 episodes is a designed experiment, not a leaderboard. Worth borrowing only their **dated methodology page** convention: one canonical URL/doc per frozen version. Source: https://mlcommons.org/ailuminate/safety-methodology/ · https://github.com/mlcommons/ailuminate · https://arxiv.org/html/2503.05731v1 |
| **HELM (Stanford CRFM)** (transparency standard) | all evals run through one public open framework; raw predictions + prompts published; multi-metric reporting; scenario/metric taxonomy declared | We meet the taxonomy discipline (6 slots × 4 tiers × twins); transparency is intentionally private, BUT I3's cryptographic key gives third-party verifiability (the verkle law) — a stranger can check the chain-head reconstruction. Borrow: publish **raw per-episode outputs** to the run archive even if the repo stays private. Source: https://crfm.stanford.edu/helm/ · https://github.com/stanford-crfm/helm |
| **ReplicatorBench / CORE-Bench / REPRO-Bench** (agent-reproducibility benchmarks) | agents must **preregister their replication plan before executing** (ReplicatorBench); reproduce results from published artifacts (CORE-Bench, 270 tasks/90 papers); score reproducibility 1-4 (REPRO-Bench) | Doctrinal validation: the external frontier is converging on EXACTLY our shape — pre-registered plan, then scored execution. Our bundle IS the preregistration layer those benchmarks test agents against. Nothing to adopt; cite as precedent when approaching Astra. Sources: https://www.cos.io/blog/benchmarking-llm-agents-on-scientific-tasks-introducing-replicatorbench · https://www.alphaxiv.org/abs/2409.11363 |
| **ReproEvalCard (ACL 2026)** (reporting standard for LLM evals) | a concise reporting card: model/version pinning, sampling params, dataset documentation, judge calibration, environment disclosure — filled per evaluation | We meet most; adopt the CARD FORMAT idea: one page per task family inside the bundle (already half-exists as the instance cards). Source: https://aclanthology.org/2026.acl-short.22.pdf |

## 2. GAPS — our bundle vs the STRONGEST external standard

Ranked by how visible they'd be to Astra, strongest-standard first.

1. **Model pinning granularity (prereg-template 4.1).** The budget manifest §3
   pins four configs BY NAME + lane alias (glm-5.3-flash, DeepSeek chat,
   Hermes gateway, GLM-4.5/Qwen) — but no snapshot identifiers, no checkpoint
   hashes, no API-version/access-date column, no quantization note. The
   external template is explicit: a nickname is not a pin ("a specific
   snapshot, not just GPT-4"). Our infra findings already imply the fix
   (thinking=low, ≥1536 max_tokens are pinned; the MODEL VERSION is not).
2. **The B−C decision rule is a threshold, not a test (prereg-template 4.3,
   AAAI stats items).** "B−C > +5 per family" is a minimum effect size, but
   the template wants the pre-specified test and decision procedure: which
   paired test, what CI, how missing episodes enter (we HAVE the denominator
   law — it is not yet WIRED into the gate arithmetic). Note honestly: the
   exact gate CIs live in Astra's retained full text (tri-stated MISSING on
   disk in the task-pack skeleton) — so our upgrade is to pre-register OUR
   proposal in the manifest and reconcile at seal, which is exactly the
   enhancement-queue move the deck already plans.
3. **No contamination canary + no per-instance metadata data-model (AISI
   standard, README/METADATA requirements).** Every AISI task pack carries an
   unaltered canary string so training-corpus contamination is detectable.
   Our 12 instance packets have freeze stamps but no canaries, and card
   structure is prose, not a schema. Cheap to fix, high signal: it shows we
   read the harness standard.
4. **QA evidence not packaged as artifacts (AISI Quality Assurance).** HOLD 0
   and HOLD 3 will produce exactly the evidence AISI demands (a completed
   sample with checked logs; a deliberately-broken harness caught by the
   plumbing) — but nothing in the bundle SAYS the QA receipt is a required
   deliverable per task family. Name it now so the wave that runs HOLD 3
   files it in the bundle directory.
5. **Raw-transcript archival is implicit (prereg-template 4.6, HELM).** The
   meter schema (budget manifest §5) is excellent — discounts never netted,
   failure receipts, waiting time separate — but there is no
   `transcript_ref` field hashing the raw request/response log per episode.
   Without it, "archived input-output logs" is a promise, not a row.
6. **No "collection has not begun" attestation (prereg-template 4.6k).** Our
   status lines say SKELETON/nothing-launched, which is the same fact — but
   the external form is an explicit dated attestation at the seal. One line
   in the HOLD 4 ceremony.
7. **Pilot history not a section (prereg-template 4.2).** The evidence exists
   (amendment ledgers, HOLD receipts, "how many instances were amended and
   why") but is scattered. The template wants a dedicated declaration:
   iterations explored, whether pilots shaped the hypotheses. Answer: yes,
   the sham-pilot is DESIGNED to shape the suite — that must be declared as
   exploratory-by-design (it already is: "pilot never enters confirmatory
   results" — Astra's own rule, we just carry it).
8. **Environment disclosure (AAAI).** No hardware/OS/library-version line in
   the manifest. One table row. (For us: harness host, gateway versions,
   model API endpoints by alias.)

Already AHEAD of the external standard on: refusal/exclusion policy
(theirs is usually "we excluded N refusals"; ours pre-registers failure
credit and keeps failures in the denominator), on-disk answer keys making
the hidden rubric honest (most public benchmarks hide keys WITHOUT
deterministic on-disk derivation), B/C token-budget matching (nobody
outside does compute-matched warm-prompt controls — this is genuinely novel
and should be SAID to Astra), per-episode meter schema with un-netted
discounts, and the cryptographic third-party verifiability of I3.

## 3. THE 3 UPGRADES WORTH MAKING BEFORE THE APPROACH

1. **SNAPSHOT PIN TABLE (budget manifest §3).** Add four columns to the
   held-configs table: `snapshot_id` (exact model version/checkpoint),
   `checkpoint_sha256` (for open-weight Hermes/Qwen endpoints), `api_version`
   + `access_date`, `quantization` (or "none"). This is the single biggest
   preregistration-template gap and it is a 20-minute file edit by the
   gopher lane (no key material touched — alias-only law stands). Astra's
   template section 4.1 is satisfied on sight.
2. **EXECUTABLE B−C GATE (budget manifest §1/§5).** Replace the bare "+5"
   with a pre-registered decision procedure: primary outcome = mean rubric
   score per family on irreducible tasks; test = paired comparison over
   matched B/C episodes (same block/task/family/seed-population), effect =
   mean B−C with a bootstrap or permutation CI at α declared, decision rule =
   lower CI bound > 0 AND point estimate > +5; missing episodes enter per the
   GOPHER law (usable-work credit, denominators shown, complete matched sets
   drive the comparison). If she ratifies different CIs in her retained text,
   hers win at seal — we simply stop being the side without a number.
3. **QA + CANARY BLOCK (task-pack skeleton, per instance).** Two additions to
   the L0 card format: (a) a `canary` field — a unique random string per
   instance, quoted verbatim in the packet, so any future training-corpus
   leak is detectable (AISI's exact mechanism); (b) a `qa_receipt` line
   promising, per task family, one completed end-to-end sample (agent or
   desk) with its log stored in the bundle directory at HOLD 3 — AISI's QA
   requirement, reused from receipts we were already going to produce. The
   desk sub-forms and sham twins inherit both.

Sequencing note: all three are FILE work inside HOLD 4's lawful lane (the
freeze map allows file work now); nothing needs a subagent launch or an
operator spend-GO. Do them BEFORE the approach so the surprise line reads:
"We built your registration bundle to the external standard — here is the
standard — now seal it together."

## 4. SOURCES (all cited inline above, collected)

- Preregistration template for AI-agent experiments: https://arxiv.org/html/2606.11217v1
- UK AISI Autonomous Systems Evaluation Standard: https://ukgovernmentbeis.github.io/as-evaluation-standard/
- Inspect framework: https://inspect.aisi.org.uk/ · https://github.com/UKGovernmentBEIS/inspect_ai
- AAAI-26 reproducibility checklist: https://aaai.org/conference/aaai/aaai-26/reproducibility-checklist/
- IJCAI 2026 reproducibility: https://2026.ijcai.org/reproducibility/
- MLCommons AILuminate methodology: https://mlcommons.org/ailuminate/safety-methodology/ · repo: https://github.com/mlcommons/ailuminate · paper: https://arxiv.org/html/2503.05731v1
- HELM: https://crfm.stanford.edu/helm/ · https://github.com/stanford-crfm/helm · paper: https://arxiv.org/abs/2211.09110
- ReplicatorBench (preregistered replication plans): https://www.cos.io/blog/benchmarking-llm-agents-on-scientific-tasks-introducing-replicatorbench
- CORE-Bench: https://www.alphaxiv.org/abs/2409.11363
- ReproEvalCard, ACL 2026 reporting standard: https://aclanthology.org/2026.acl-short.22.pdf
- Center for Open Science registered reports (pre-review-before-data norm): https://www.cos.io/initiatives/registered-reports

*Search-provider caveat: the scan rode a rate-limited search lane; GAIA and
SWE-bench submission pages could not be fetched live this run. GAIA's known
shape (hidden test answers, exact-match normalization, declared agent
config) is covered by the HELM/AISI rows above; nothing in this card's
verdicts depends on them. Retry door: re-run "GAIA benchmark leaderboard
submission" when the search quota refills.*
