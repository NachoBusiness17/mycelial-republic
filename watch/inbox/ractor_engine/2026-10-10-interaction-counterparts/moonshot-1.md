# MOONSHOT-1: THE INTERACTION THESIS (counterpart realism) - 2026-10-10

Lens: moonshot (no sacred cows, the 10x read, every swing grounded in one real organ).
Topic: MIMESIS (arXiv 2610.09484) and whether realistic-counterpart training is this
estate's highest-leverage next organ, on 6 GB hardware + funded API tiers.

## What I verified myself this session

- MIMESIS exists and its abstract matches the ask's core claims. I fetched
  https://export.arxiv.org/abs/2610.09484 live this session. Abstract-verified
  claims: a purpose-built user simulator trained on human conversations with
  explicit reasoning supervision and 13 realistic behavioral patterns; a 9B model;
  SOUL-Index 65.7 surpassing the strongest frontier model; +13.4 behavioral
  fidelity vs Claude-Opus-5; agent training against the frozen 9B simulator beats
  GPT-5.5-as-user training across EIGHT environments under ALL NINE unseen user
  simulators; and Coached On-Policy Self-Distillation (CSD), where a coach converts
  the simulator's private reasoning traces and subsequent utterances into concise
  coaching notes, dense token-level supervision beyond sparse task rewards, with
  further gains across all nine evaluation user models. The framing claim that
  matters most to us: off-the-shelf assistant LLMs as users are "overly
  cooperative, explicit, and behaviorally homogeneous compared with real users."
- The estate has ZERO prior contact with MIMESIS: grep for "2610.09484" and
  "MIMESIS" over catalog/catalog.jsonl and state/arxiv/2026-10-09/* returned
  nothing (exit-level empty), and no state/arxiv/2026-10-10/ harvest directory
  exists. This lens is first contact, not a re-derivation.
- ASTRA v4 spine read in full: memory/continuity/seat_memory_20260927/
  astra-v4-converged-training-brief.md:15-16 fixes the order harness_audit ->
  curator -> validate -> QLoRA SFT -> RS-DPO+HyPO -> GRPO -> budget-matched eval
  -> canary promotion with rollback. Every stage trains or selects the AGENT on
  agent-side tapes. No stage models the counterpart. Reward law at :28: "no
  learned reward model, no model-as-judge."
- Substrate law re-verified: requirements.txt (read in full this session) carries
  no torch, peft, transformers, bitsandbytes, or unsloth; box-burn law
  memory/continuity/seat_memory_20260927/box-burn-90-percent-law.md:17 (RX 5600 XT
  gfx1010, "ROCm will never support it", Vulkan inference-only, QLoRA named as the
  future GPU sink); the 10-09 fold digest states "40 GiB training is banked
  capability, not on-box capability on the pinned 6 GB box"
  (watch/inbox/frontier_olm_2026-10-09/DIGEST.md:58) and names the 6 GB box
  explicitly at :57.
- The win-rate instrument exists and is API-native: mag/seed_percolator.py:7-12
  (fitness = paired blind win-rate vs frozen baseline, >=55 pct threshold, min 30
  pairs per epoch, null-variant canary halting a biased judge), judge() at :64
  (deepseek blind judge), paired_run() at :78 (glm-4.7-flash body). Prompt-space,
  zero training stack, rides the funded/free lanes today.
- The counterpart surfaces the estate runs today are exactly the MIMESIS-diseased
  kind: seven FIXED salon shapes, "never invent new ones without the operator"
  (.agents/skills/salon/SKILL.md:24-27); salon receipts sampled this session
  (watch/salon_receipts/agent_mesh_triangulation.json: S5/S6/S7 lane outputs with
  gates). Behavioral homogeneity by design.
- The tape census (the ask's "interlocutor tapes"), measured this session:
  - THE BIG ONE the ask under-sells: ~/.zcode/cli/db/db.sqlite is 4,474,716,160
    bytes (4.47 GB), schema session/message/part/todo/workflow_run etc. (table
    list read this session), holding 7,276 sessions and 231,881 messages; role
    split via json_extract: assistant 192,492 / user 39,400. This is the full
    operator-machine interaction archive, source of the zknot distills
    (tools/zknot.py:57 names the DB). CAVEAT I must carry: user-role rows include
    tool-result and templated rows in harness schemas (zknot drops "templated
    cron"; the 10-08 tape header says 46 human of 46 user_msgs after filtering),
    so 39,400 is a ceiling, true human-turn count unmeasured. That measurement IS
    the first probe.
  - memory/zknot/: 27 files, 229 KB, verbatim operator prompt first-lines per
    session (e.g. 2026-10-08 tape: 46 prompts, his voice intact: "what would a
    huge deepseek burn look like", "i dont want it i just want this codified into
    law so nobody can fuckwith it not even me").
  - The correction corpus, the estate's unique genre: .agents/skills/
    operator-corrections/SKILL.md (laws 1-12) + LAWS_COMPILED_20261003.md (128
    lines, laws 21-66) + memory/law/registry.json (165 lines) +
    memory/law/enforcement_trail.jsonl (1,490 enforcement rows, sampled this
    session). SKILL.md:86-89 states the extraction shape verbatim: "failure
    traces with contrast (wrong move vs corrected move, the MAX_DISTILL shape)
    so the cheap brains get the laws too."
  - Mine receipts: watch/inbox/STEALTH_MINED_FINDINGS.jsonl = 1,516 rows spanning
    2026-09-28T00:37Z to 2026-10-10T05:02Z (12 days, first and last rows read
    this session). HONESTY: these are machine lane registers (lane/model/finish/
    answer_file), not human turns. They are the agent's side of the conversation
    log, not interlocutor tape in the MIMESIS sense.
  - Salon vault: watch/salon_receipts (45 files) + watch/salon_responses (4) +
    watch/salon_inbox; the human turns inside are the operator's brief questions
    only.

## Findings (5), each with evidence, falsifier, one-sitting move

### F1. THE 4.47 GB ORGAN NOBODY TRAINS ON
The estate's rarest asset is not the seat tapes every training plan points at
(docs/SKILLS_CATALOG.md:10 names "room.jsonl rows, seat session tapes, and intake
cards" as THE corpus; steal card finetuning-adaptation-arxiv.md repeats it); it is
the 39,400-user-role-turn interaction archive in ~/.zcode/cli/db/db.sqlite, and
every stage of the ASTRA v4 spine is agent-side, so the human half of every tape
is treated as noise. MIMESIS's whole result says the half we discard is the half
that generalizes. The 10x swing: the next organ is not a better agent, it is the
COUNTERPART, trained (or at prompt level, distilled) on the operator's own turns.
No lab has this operator; we have him at 4.47 GB resolution.
- Falsifier: sample 200 user-role rows from the DB and hand-classify with zknot's
  own cron/templated filter; if under half are human-authored, the corpus thins
  by an order of magnitude and the thesis downgrades to the 229 KB zknot distill
  (still workable, but small-data).
- Move (one sitting, ~20 min, $0, zero deps): sqlite census of message roles +
  lengths + per-session human-turn counts, banked to
  watch/inbox/ractor_engine/2026-10-10-interaction-counterparts/tape_census.md.

### F2. MIMESIS'S CHEAPEST HALF IS ALREADY THE ESTATE'S NATIVE GENRE
CSD (verified in the abstract: a coach turns the simulator's private reasoning
into concise coaching notes, dense supervision beyond sparse rewards) is a
word-for-word description of what operator-corrections already is: laws extracted
from failure traces with wrong-move-vs-corrected-move contrast (SKILL.md:86-89).
The estate can run the CSD shape on funded API tiers with NO RL, NO GPU, NO
training stack: a glm-5.3-prime / grok-4.7 coach reading a failure plus the law
corpus and emitting the coaching note, which then conditions the next attempt.
This slots into the ASTRA spine between preference (RS-DPO+HyPO) and GRPO as a
dense-feedback injector without touching the "no model-as-judge" reward law
(brief :28), because the coach supervises the TRACE, not the reward.
- Falsifier: 20 historical failures through the coach; if its notes match
  already-banked laws <30 pct of the time (redundancy check: the corpus already
  covers it) OR are novel-but-wrong >20 pct (hallucination check), the coach adds
  nothing and the CSD port dies at the cheapest possible gate.
- Move: 20-row coach-redundancy A/B on the funded tier, <$2, receipts into
  memory/runs/hermes_burn/usage.jsonl per the descent protocol.

### F3. THE GATING PROBE IS ALREADY RANKED #1 LOCAL, AND IT IS MISSING ONE CLASS
The 10-09 fold digest ranks the 100-row fall-composition census first under "Run
locally today, zero new deps, zero spend" (DIGEST.md:67), inputs re-measured by me
(memory/percolator/explore.jsonl 1,976 rows, candidates.jsonl 31 rows). But its
binary is process-failure vs content-failure, both agent-side. It cannot see the
third class the operator himself named on tape: work that died because the
counterpart killed it ("we need to collect things we wanted that were killed
outright and map why things die how and give us compost for the future", zknot
10-08 tape, his 23:31 prompt). Interaction-caused death is exactly the class a
realistic-counterpart organ would train against.
- Falsifier (both ways, pre-registered): if interaction-caused falls are <10 pct
  of the 100-row sample, counterpart realism is NOT the highest-leverage organ
  locally (the operator kills little; the thesis demotes); if >30 pct, it crowns
  ahead of the SFT port and owns the curator stage's row source.
- Move: add the third tag to the named census BEFORE it runs. Same one seat-hour,
  same inputs, same CPU-only shape.

### F4. SUBSTRATE LAW FORCES THE PROMPT-SPACE GHOST, AND THE NINE-SIMULATOR CLAIM BECOMES A CROSS-SEAT TEST
A 9B anything cannot train on this box (no training stack in requirements.txt,
Vulkan-only GPU, 40 GiT training is "banked capability, not on-box", DIGEST.md:58).
The only buildable MIMESIS shape here: simulator = a prompt-space operator-ghost
on funded tiers (glm-5.3-prime / qwen3.8-max-prime / grok-4.7 per the driving
ladder), agent = the local gemma tier, instrument = seed_percolator's paired blind
win-rate (mag/seed_percolator.py:7-12, :64, :78), which already rides API lanes.
MIMESIS's verified transfer claim (better agent performance "under all nine unseen
user simulators") maps to an estate-falsifiable cross-counterpart test: steer
seeds against the ghost, then blind-judge on held-out counterpart personas the
ghost never saw (the seven salon shapes, a hostile attacker, the raw funded-tier
default user). Transfer holds but zknot-held-out performance does not = the ghost
learned style, not intent, and dies.
- Falsifier: the percolator's own promotion grammar: >=55 pct win-rate over min 30
  fresh pairs (seed_percolator.py:7-9) plus the null canary (:10-11). A ghost arm
  that cannot clear 55 pct against a cooperative-user arm is realism without
  leverage, pre-registered cannot-resolve per the calibrated-judge steal
  (DIGEST.md:56).
- Move: 30-pair first epoch, ~$3-5 funded spend, one sitting, metered.

### F5. THE SWING: ON A SOVEREIGN ESTATE THE SIMULATOR IS THE PRODUCT, NOT THE SCAFFOLDING
Meta built MIMESIS because it needs millions of scalable users. This estate has
ONE user whose attention is the scarcest resource in the republic (overnight
windows run blind of his judgment; dawn lists queue for his pen,
state/CURRENT.md:39-44). A verified operator-ghost converts every 03:00Z window
into "the operator was in the room": his redirect patterns, his no-sacred-cows
reflex (law 10), his two-strike bail (law 2), his stop-when-verified (law 3),
applied live at prompt level through the percolator, which ALREADY updates living
prompts epoch over epoch. Living Weights ships weights that update in use
(ask-given, unverified); our Vulkan lane cannot, but living PROMPTS are running
today, and the ghost graduates to weights exactly when the ASTRA spine's QLoRA
stage finally fires. The Lyapunov amplify/suppress framing (ask-given, unverified)
is the right shape for the pattern census: his redirects and GO/kill calls are the
unstable directions to amplify; apology spirals (law 8) and act-before-consult
(law 1's root cause) are the stabilities to suppress.
- Falsifier: the one judge that matters. 10 held-out zknot prompts, the ghost
  answers on the funded tier, the OPERATOR plays Turing judge at his next
  interactive window. If he spots the ghost instantly or rejects its calls, the
  whole thesis is a mirror-game and dies by the only signature that counts. If he
  cannot tell and endorses the verdicts, the organ is crowned with his own pen.
- Move: one sitting, zero build: assemble the 10-prompt ghost Turing pack and file
  it to the dawn list.

## Answer to the operator's question, plainly

Is realistic-counterpart training the highest-leverage next organ? My read: it is
the highest-leverage CHEAP organ, and it is mispriced as "training". On this box
the buildable form is a prompt-space operator-ghost coached by the law corpus
(F2 + F5), feeding the existing percolator (F4), gated by two one-sitting probes
(F1 tape census, F3 interaction-fall tag) that cost $0. It is NOT higher-leverage
than the already-ranked fall census; it is the census's missing third column. The
weight-borne MIMESIS (9B simulator, GRPO against it) lands only when the ASTRA
QLoRA spine itself lands, and then the ghost's distilled corpus is already banked.

## Blind spots (honest)

- MIMESIS read at abstract depth only. The 13 patterns' names, the SOUL-Index
  construction, the RL recipe, and the Meta SIL attribution are unverified
  (paper PDF not fetched this session). Everything I cite from it is the
  abstract's own text.
- Open Env Arena, Living Weights/TensorFold, and Clark's Lyapunov spectrum
  (2610.12426) are ask-given; I verified none of them.
- The 39,400 user-role figure is a ceiling; the tool-result/cron fraction inside
  it is unmeasured (that is F1's probe, not a number I have).
- Salon receipts were counted and one was sampled; their content depth unread.
- No probe was run this session (census, coach A/B, Turing pack are named, not
  executed); all findings are scoping claims on verified bytes.
- Cost envelopes ($2, $3-5) derive from the driving ladder's funded credits, not
  from measured burn on these specific probe shapes.
- The zknot tapes are first-line distills; full-turn style (follow-ups, pasted
  content) lives only in the sqlite, unmeasured by me.

Session instrument receipt: files read with files.read per the world-read law
(single known paths); listings via ls; greps scoped and named above; the sqlite
census ran .venv/Scripts/python.exe with plain SELECTs (read-only) against
~/.zcode/cli/db/db.sqlite; MIMESIS fetched via curl from export.arxiv.org. No
em-dashes. Banked by moonshot-1, ractor_engine workflow, 2026-10-10.

## CORRECTION PASS (hostile second pass, same day): F1 and F4 amended, not withdrawn

The hostile pass verdicted F1 and F4 weakened. Both critiques re-verified against
bytes this session; both findings survive in corrected form.

### F1 corrected: the honest operator-turn number is ~5,844, not 39,400

My headline was wrong ~6.8x. The user-role ceiling is mostly machine traffic.
My own re-census this session (read-only URI mode against the live DB, moment
2026-10-10T02:17Z, file 4,483,244,032 bytes; counts drift, the DB is live):

- origin x kind over ALL user-role rows: real_user/user_prompt 19,032;
  agent_runtime 20,357 (todo_reminder 13,905 + background_notification 6,279 +
  system_reminder 127 + compact_summary 30 + subagent_notification 16);
  origin-null 66; system 3.
- real_user/user_prompt split by session.task_type and parent: interactive
  MAIN sessions 11,224; CHILD sessions 7,808 (workflow_child 4,630 +
  subagent_child 2,941 + fork 234 + selection_side_chat 3) = machine-authored
  child asks wearing the real_user label.
- Top-5 interactive mains by turn count are DAEMON DRIVERS by title:
  "Flash-lane burn dispatcher every 20 min until midnight" 2,009; "FORGE DAEMON
  20-min world-building cycle (2B burn window)" 1,506; "Sancho cadence, every 4
  hours" 1,157; "24x7 free burn churn (fires every 2 hours)" 360; "OLM mine
  daily burn 10:00" 348. Sum 5,380 of 11,224. Remainder: 5,844 candidate
  operator turns = 14.8 pct of the user-role ceiling.

My original falsifier's under-half clause FIRED decisively (15 pct << 50 pct);
the thesis survives on the smaller honest number exactly as the gate
prescribed. The organ design changes with it: not bulk-training on the DB, but
pattern distillation from a hand-verified subset (the 26 zknot tapes remain the
verified floor), mined out of the 5,844-turn remainder. Citation fixed: the DB
path line is tools/zknot.py:62, not :57. Next pre-registered gate: hand-classify
a 200-row random sample of the 5,844 remainder with zknot's templated-cron
filter; under 2,000 extrapolated verified-human turns kills bulk pattern
distillation as a primary organ (ghost falls back to the zknot hand-verified
corpus), above it the DB stays the mining substrate.

### F4 corrected: the venv DOES carry an undeclared training stack; the constraint is VRAM, not stack absence

pip list this session (.venv/Scripts/python.exe -m pip list): torch 2.13.0,
transformers 5.15.0, peft 0.21.2, accelerate 1.6.0, datasets 5.0.1, all
installed and all ABSENT from requirements.txt (read in full this session),
the inverted fresh-venv gap disease that requirements.txt:15-16 already
documents in the other direction (cryptography, pandas). My "no training
stack" leg is struck. The prompt-space-ghost conclusion stands on the VRAM leg
alone, now sharpened by a fresh probe: the venv torch is the +cpu build with
cuda available False and device count 0 (run this session), so CPU-only toy
training works, GPU training works nowhere (RX 5600 XT gfx1010, ROCm never,
Vulkan inference-only, box-burn law :17), and the 40 GiB LoRA-over-GGUF class
stays off-box (DIGEST.md:58). Net effect on the thesis: the weight-borne half
gains a possible on-box rehearsal path (CPU LoRA smoke on a 2b toy, night
window, amd_window_guard) that the original finding wrongly priced as
spine-build-first; the 9B simulator stays off-box regardless. Added substrate
falsifier: if a 100-step toy LoRA cannot complete inside one night window on
this torch+cpu build, the ghost's weight-borne graduation depends wholly on
rented or funded tiers. Added zero-cost move: pin the undeclared stack into
requirements (or a requirements-training.txt) before the fresh-venv gap
disease silently eats it.

### Findings F2, F3, F5: untouched by the critique, stand as banked above.
