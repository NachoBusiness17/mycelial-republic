# DEEP-MIRROR-ARCHITECTURE: the sovereign mirror as a prediction engine, not a persona

- Date: 2026-09-28
- Ask: design the architecture that copies the operator's thinking and decision-making so the estate runs autonomously: data sources, extraction, representation, evaluation.
- Operator order the mirror serves (verbatim, quoted in `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:3-4`): "the whole purpose of the sovereign mirror was to copy my thinking and decision making with you to run autonomously."
- Method: every path and count below was read or counted in this session on the live tree at branch `mag/run-beta1-factory-build-audi-20260806T231709Z`. Nothing is estimated. Gaps are named as gaps.

---

## 0. Thesis

The obvious design, fine-tune a model on the operator's text until it talks like him, is the wrong design and the estate has already half-proven it is. A talking mirror is unfalsifiable: it imitates the operator's voice and still makes every decision wrong when it matters. The design that fits this estate is a **mirror whose unit of copy is the decision, not the voice**, and whose truth condition is **prospective prediction accuracy on operator choices**, scored like a forecaster (Brier), not like a chatbot.

Three estate laws already pin this shape and I inherit them rather than invent:

1. `docs/ref/MIRROR_PRESENTED.md:6-11`: the mirror loads the person **as presented** (L0), procedures stay empty of content until L0 loads (L1), and model judgment is always **labeled** as model judgment (L2). Anti-echo table at `docs/ref/MIRROR_PRESENTED.md:36-40` forbids dressing the model's inference as the operator's insight. A mirror that paraphrases the operator into smooth consensus is the product's named anti-goal (`MIRROR_PRESENTED.md:14-17`).
2. `mag/behavioral_lensing.py:26` (module header LAW): "Alignment steers are suggestions. The Sovereign (operator) decides." The mirror therefore predicts; it never self-authorizes gated classes.
3. The CORRECTION card (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:26-32`): when the operator corrects, the mirror does not apologize, it mints LAW (rib + load-bearing AGENTS.md line + enforcement in code). This is the estate's existing update rule; the mirror is the loop that runs it continuously instead of on correction.

So: **mirror = compiled policy (rails and cards) for stable preferences + a learned preference scorer for judgment calls + a pre-registered prediction ledger that is the only thing allowed to call the mirror "working."**

---

## 1. Data sources (sensing layer): what the estate already writes

I verified all of the following on disk this session:

| Source | Path | Volume (measured) | What it carries |
|---|---|---|---|
| Decision log | `memory/decisions_log.jsonl` | **213,259 rows** (`wc -l`); ~59,202 timestamped 2026-08, ~154,020 timestamped 2026-09 (substring counts on the timestamp field) | `{timestamp, context, steer_input, outcome}`. This is a ready-made (state, action, result) triple stream. Late rows carry `maps_to=` annotations (verified on the 2026-09-28 tail rows: `maps_to=republic-ambassador:empower`, `maps_to=skill:mesh-comm`). Written through `mag/decision_framework.py:23` (`DECISIONS_PATH`). |
| Seat behavior telemetry | `logs/behavioral_events.jsonl` | **215,576 rows** | `{ts, kind, detail, tool, error, phase, session_id, provider, model}`, the GA4-shaped event log (the mapping is documented in `mag/behavioral_analytics.py:15-24`, including "conversion = steer success (silence < 0.3 = agent adopted the steer)"). |
| Room tape | `watch/room.jsonl` | **13,852 rows, 4,682,421 bytes** | Typed multi-seat traffic (receipts, folds, steals, heartbeats) with ts + seat + session ids. |
| State pile | `memory/pile/state_summaries.jsonl` | **144 rows** (81,772 bytes) | `{id st-*, ts, kind, tier, goal, outcome, lessons[], state_hash, classified}` captured at escalation/close by `mag/state_snapshot.py` (callers wired per its docstring). |
| Pile drain | `memory/pile/classified.jsonl` (**154 rows**) and `memory/pile/training_rows.jsonl` (**270 rows**) | counted this session | `tools/pile_classify.py` classifies the pile with local gemma4 and emits instruction-tuning rows of the shape `{"instruction": "Classify this state: ...", "output": "{category, lesson_kind, tags, outcome}", "meta": {"source": "pile_classify", id}}` (verified on the first row). |
| Operator corrections | `.agents/skills/operator-corrections/SKILL.md` | **20 numbered laws** | Laws compiled from the failure ledger, each dated and many carrying TEETH (enforcement in code). `mag/mind_mine.py` v2 already mines corrections into a lesson-ledger and states the doctrine outright ("the operator's corrections ARE the training data", header line 9). |
| Card deck | `memory/rib/` | **43 rib files**; `RIB_BEHAVIOR_CARDS_20260928.md` alone defines 9 input-shape cards (LINK-DROP, GO, CORRECTION, TERSE-EVAL, X-DROP, STEAL-ORDER, FUNDING-STATEMENT, RESOURCE-ORDER, GENESIS-TESTIMONY) | The v1 mirror card deck: input shape -> warmed invocation. Every card claims EVIDENCED status from the record. |
| X history | `memory/runs/x_history_mine/20260926/` | Pilot P1 receipt: **131 posts harvested**, mycelium graph nodes 233 -> 364, artifacts 105 -> 236, edges 142 | Multi-pass pipeline (p1 fx harvest, p2 DNA topic edges, p3 classify v2, replies harvest, deeper scavenge) with per-pass receipts and `HANDOFF_TRACK_B_20260927.md`. The operator's public thesis corpus is at `@NachoQuixotic` per `docs/ref/MIRROR_PRESENTED.md:28`. |
| Handshake ledger | `state/handshakes.jsonl` | **7 rows**, schema `handshake.v1` `{gate, unlocked_at, unlocked_by, what, promised_use, first_use}` (first row verified) | Operator unlock events = revealed preferences about what he considers worth driving. |
| Biography / chain | `memory/biography/residual/` + registry + verkle chain (8,212 leaves per the Q-001 receipt measurement) | Day-level residuals per the DNA contract (`docs/DNA.md:34-46`) | What the operator did per day, hashed. |
| Workflow registry | `memory/workflows/REGISTRY.jsonl` | exists (row count not taken) | Every gated dispatch as a row: what the estate was allowed to do and did. |
| Open decisions | `watch/inbox/burn_reset_20260927/queue/Q-001.md` | live now | The operator-gated verkle fold: 247 fold candidates / 790 kept, execute double-gated on operator GO (`mag/verkle_compaction.py:17-20` landing gate per the Q-001 receipt). |

**Gaps, stated plainly:**

- `tools/pile_classify.py` docstring says training rows "feed `train/prepare.py`". **The `train/` directory does not exist** (`ls train/` returned nothing). The fine-tune leg of the corpus organ (`.agents/skills/code-agent-data/SKILL.md` Stage 2/3) is unlanded. The mirror v1 must not depend on it.
- The seat transcript stores `cli/agents` and `state/v2/sessions` are empty on this tree, and the 09-17 tide transcript is already recorded as unrecoverable (Q-022 receipt). Some raw operator register is permanently lost; the mirror builds forward, and the loss is itself a finding for the retention law.
- The decisions log has no per-row author field. I found 167,015 rows containing the substring "operator" but did not attribute authorship row by row; attribution is an extraction task (Section 2), not a fact I can assert today.
- The behavior-cards rib names miners "x_history_mine, oral_history" (`RIB_BEHAVIOR_CARDS_20260928.md:9`). `x_history_mine` exists as a one-off run directory under `memory/runs/`, not a maintained module; **no `oral_history` artifact exists anywhere in the repo** (repo-wide grep). That card-deck citation is forward-looking, and the mirror plan must schedule the oral-history capture or the card will cite a ghost forever.

---

## 2. Extraction (distillation layer)

The estate's gap is not data, it is **labeled decision records**. 213k log rows but no option sets; 43 ribs but no measured per-card accuracy. Extraction is four passes over sources that already exist.

### 2.1 Decision records (`decision_record.v1`)

The unit of mirror training data. Proposed schema, assembled from fields the sources already carry:

```
{id, ts, context, context_hash, state_features, options[], chosen, rejected[],
 author, authority_class, confidence, receipt_path, maps_to}
```

- `state_features` from what the pile already captures: tier, funding state, queue depth, time-of-day, session load (`mag/state_snapshot.py` capture fields).
- `options[]` and `rejected[]` are the hard part and the valuable part. Three feeders: (a) receipts that record an escalation ruling with an explicit alternative (Q-001 is a fully-formed one: GO vs NO-GO on the live fold, with the ruling text preserved); (b) CORRECTION events, where the corrected move and the wrong move form an explicit pair; (c) handshakes (`promised_use` vs `first_use` = did he drive it).
- `authority_class` is the sovereignty field: `operator-gated` / `seat-decidable`. The estate already maintains this boundary informally (chain-tip rewrites are operator GO per the Q-001 double gate; queue work is seat-decidable per the GO card). Extraction must make it explicit per decision class, because Section 4's eval treats it differently: on operator-gated classes the mirror's job is to predict the operator, on seat-decidable classes the mirror's job is to decide.

### 2.2 Contrast pairs (the negative half)

`.agents/skills/code-agent-data/SKILL.md:27-31` already defines the signal: "TRAINING-GRADE: wrong move vs corrected move in one tape (contrast is the signal)". `mag/mind_mine.py` v2 mines corrections into a lesson-ledger mapped to standing laws, and admits heuristics ("If a law has little evidence we say so"; unmapped corrections labeled "unspecified", header lines 12-13 and the honesty block). The mirror consumes the same pairs as **pairwise preference data**: corrected move > wrong move, same context. This is the DPO/Bradley-Terry shape (Rafailov et al. 2023; Bradley & Terry 1952; Christiano et al. 2017) without needing any new infrastructure: `training_rows.jsonl` already exists in instruction format and the pile drain is idempotent by id (`tools/pile_classify.py` docstring).

### 2.3 Card induction (shape mining)

`RIB_BEHAVIOR_CARDS_20260928.md` is the hand-built v1. The mirror's mining job is to do to the room tape and decisions log what P1-P3 did to X history: cluster operator inputs by shape, count evidence per cluster, and emit card candidates with boundary conditions (what makes an input NOT that card). Inducted cards enter the deck as CANDIDATE and promote to EVIDENCED only on the rib's own bar (demonstrated repeatedly). The 9 existing cards give the induction 9 labeled seeds.

### 2.4 Compilation to rails (the estate's signature move)

The STEAL-ORDER card says it: "implement as RAILS in code" (`RIB_BEHAVIOR_CARDS_20260928.md:46-50`). Where a preference is stable and cheaply checkable, the mirror does not keep it in a model at all; it compiles it into a gate. Precedents: law 13's teeth (host-spawning designs must cite law-or-exemption or get DISPUTED), the ratchet at pre-push, the workflow gate at submit, the census patrol carrier check (all in `AGENTS.md` build-discipline section). The architecture consequence: the mirror is **mostly a compiler with a small learned residual**, not a large learned policy. Every time extraction finds a preference that fires identically across contexts, it graduates from scorer to rail, and the eval for that class stops being statistical and becomes a gate.

---

## 3. Representation (three tiers, per the presented-not-interpreted law)

| Tier | Form | File shape | Reads as |
|---|---|---|---|
| L0 presented | Verbatim decision records + quotes with provenance | `mirror/records/*.jsonl` (each row carries receipt_path + ts; no paraphrase field at all) | "Here is what he actually did and said, byte-backed." |
| L1 procedure | Rib cards (human legible) + decision JSONL (machine legible) + prompt fragments | `memory/rib/RIB_BEHAVIOR_CARDS*.md` (already v1); `mirror/behavior.jsonl`; memlang fragments per the memweave doctrine (feed structures, not prose) | "Here is the compiled policy any seat can load warm." |
| L2 labeled model judgment | Mirror predictions and mirror drafts | every row carries `speaker: mirror` and lands in the prediction ledger (Section 4); **never** written into L0/L1 | "Here is what the mirror thinks he would do. He has not done it yet." |

The memweave/rib doctrine (`memory/rib/DOCTRINE_MEMWEAVE_20260810.md`, and the CLIPPY warm-boot order in `AGENTS.md`) already solves injection: cards ride the boot, not the chat. The mirror adds exactly one new artifact class, the **prediction ledger**, and it is L2 by construction.

Sizing honesty: the learnable residual is small. 144 pile rows, 270 training rows, 7 handshakes, 20 correction laws, 9 cards. This is a few-shot regime. The mirror v1 is therefore a **retrieval + card-matching system over a small compiled deck**, with a fine-tuned scorer only as a later upgrade once `train/` exists. Any claim that a personalized model is trained today would be fabrication; the parts exist (`training_rows.jsonl`), the trainer does not.

---

## 4. Evaluation: does the mirror predict the operator's choices?

The only honest headline metric for a mirror is **prospective prediction of choices**, pre-registered and scored after the fact. The estate already owns the discipline: the salon replicate experiment hard-coded its verdict thresholds before generation ("ANALYSIS (pre-registered stats; grades as committed above)", `artifacts/salon_ess_replicate_20260916.py:210-217`, thresholds `rho < -0.3 => SUPPORTED / rho > 0.3 => REFUTED` verified in source). The mirror reuses that discipline on decisions.

**E0 Retrodiction (offline, cheap, first):** hold out the most recent K days of `decisions_log.jsonl`; for each held-out row the mirror (built without seeing the holdout) must produce the `outcome`/decision given `context`; score top-1 match against the majority-class baseline. Power caveat stated up front: rows lack explicit option sets, so first-run E0 scores on the subsets that DO have explicit alternatives (CORRECTION pairs, escalation rulings like Q-001, handshake keep/abandon). Report the denominator; never silently switch denominators (this is the estate's own B2-216 census law applied to mirror metrics).

**E1 Pre-registered live predictions (the flagship):** for every OWED-operator decision, the mirror files `prediction + probability + rationale` in the prediction ledger BEFORE the operator decides; scored with Brier score when the decision lands. Live case available today: **Q-001, will the operator GO on the verkle live fold (247 folded / 790 kept)?** The mirror's evidence is already on disk: the ruling that a workflow dispatch is NOT operator GO, the roam verdict "needs-operator", the operator's history of gating chain-tip rewrites. A mirror worth the name predicts NO-GO (or GO) with a calibrated number here, before being told.

**E2 Discriminative pairing (low-frequency gold):** on natural interactions, the mirror drafts the operator's likely response alongside the seat's default; the operator picks which reads as his. Each pick is one labeled preference. Expensive in operator attention, so it rides existing surfaces (TERSE-EVAL moments, card confirmations) rather than adding prompts.

**E3 Card precision:** every card invocation from the deck is logged with whether the warmed lane matched the operator's intent (his follow-up is the label; his correction is a miss). Per-card precision lives in the deck itself as an evidence column. Cards under threshold get re-derived, not defended (NO SACRED COWS, law 10, applies to the mirror's own cards).

**E4 Drift:** rolling E0/E1 accuracy by month. The estate has already generated the canonical drift event: the DRIVING LADDER superseded the tier ladder on 2026-09-28 (`memory/rib/RIB_DRIVING_LADDER_20260928.md`, "supersedes the tier-ladder line above" per `AGENTS.md`). A mirror frozen a week earlier fails every funding-class prediction this week. Drift detection is therefore not optional polish; the mirror needs a `supersedes` chain on preference-bearing ribs and re-scoring on every supersede (concept drift in the Gama et al. 2014 sense, with the estate's own dated laws as the labeled change-points).

**E5 Authority recall (the sovereignty gate):** on operator-gated classes the mirror must achieve 100 percent recall on "needs-operator" (predict that this class is gated and route to the operator), because a mirror that predicts choices but self-authorizes a chain-tip rewrite has failed catastrophically regardless of its accuracy score. The Q-001 precedent (workflow dispatch is not operator GO) becomes the labeled test case. This eval has priority over accuracy: the mirror's failure budget is spent on wrong predictions, never on wrong authority.

Literature anchors, honestly scoped: E0 is behavioral cloning's offline validation and its known trap (Pomerleau 1989; Ross, Gordon, Bagnell 2011: the clone is only good on the demonstrator's state distribution, exactly where autonomy will not stay); the estate's answer to covariate shift is E1/E2 (aggregating operator labels on states the mirror actually faces, DAgger's remedy) plus rails for high-risk classes. E1 scoring is Tetlock-style forecasting discipline (Brier). The card deck over a memory hierarchy is the Generative Agents pattern (Park et al. 2023: memory stream, reflection, retrieval), with the estate's difference being that reflection outputs must pass evidence counts before entering the deck. The corrections-as-constitution is Constitutional AI's shape (Bai et al. 2022) executed since August in `.agents/skills/operator-corrections/`.

---

## 5. Failure modes the design must name before it ships

1. **The echo costume** (`MIRROR_PRESENTED.md:36-40`): the mirror dressing its own inference as the operator's voice. Guard: L2 labeling is structural (Section 3), and E3 treats intent-miss as data, never as embarrassment.
2. **Cloning the confounder:** the record shows what the operator accepted under constraints (funding, energy, the 1301 moderation surface). A mirror of "what he chose while under-funded" is not a mirror of "what he chooses." Guard: `state_features` carry the constraint state, and E4 watches for accuracy that depends on constraints the estate has since removed (the funding flip to Hermes-only on 09-28 is the live instance).
3. **The filtered-surface trap:** the operator's charged-register material must not be re-rendered at density into mirror training prompts (law 17: charged material lives in FILES, referenced by path). The mirror's extraction step inherits this: summarize in neutral analytic register, store paths, never paste the charged field into a lane payload.
4. **Preference capture by the classifier:** pile classifications are gemma4 outputs (`tools/pile_classify.py` runs a local model). Training the mirror on model-classified operator data bakes the classifier's errors into "the operator." Guard: L0 rows keep raw records; classification is metadata; E0 scores against raw held-out choices, never against classifier output.
5. **The infinity rule:** mirror outputs escape (versions fork, artifacts publish). Per law 20 there are no recall operations; the mirror's artifacts carry centerline markers (chain hash + doctrine line) so any escaped mirror is recognizable as the house's.

---

## 6. Build sequence (each step lands behind an existing gate)

1. **Ledger first:** create the prediction ledger schema + Q-001 as prediction zero (L2, labeled mirror). No model needed; this is the eval harness, and it starts earning calibration data immediately.
2. **Decision-record miner:** pass over `decisions_log.jsonl` + escalation receipts + CORRECTION events emitting `decision_record.v1` with author attribution and authority class. Lands as a `mag/mirror_mine.py` sibling of `mind_mine.py`, honest-mode inherited (counts and quotes extractive, unmapped labeled "unspecified").
3. **Deck v2:** append inducted cards as CANDIDATE with evidence counts and per-card precision columns (E3 wiring) to `RIB_BEHAVIOR_CARDS`; the deck file is the deliverable, the model is not.
4. **Rail graduation:** for any preference firing identically across >=N contexts, propose a gate (ratchet/gate-scenario row) instead of a scorer. The gate lands through the existing pre-push gates, never by loosening them.
5. **Trainer (last, optional):** land `train/prepare.py` to consume `training_rows.jsonl` (the format already exists), only when the row count justifies a fine-tune; until then the mirror is retrieval + cards and says so.

---

## 7. What this item did not do

- No code was written; this is an architecture receipt, per the ask.
- No E0 run: the decision-record miner (build step 2) does not exist yet, so there is nothing to score. The counts in Section 1 are the only measurements taken this session.
- Row-level author attribution on `decisions_log.jsonl` was not attempted; the 167,015 substring count is reported as a substring count only.
- The prediction on Q-001 itself is deliberately NOT filed here: filing a mirror prediction is L2 work that belongs in the prediction ledger with a probability and a scoring date, which is build step 1, not this receipt.
