# SALON RE-INGEST TIER A — 20260911

Worker: zcode seat, night-run wave rotation. Input: `watch/inbox/DESKTOP_SALON_CORPUS_MINED_20260911.md`
(Tier A list) + the two Desktop saves themselves. Sources (read-only):
- `C:/Users/foste/Desktop/New folder/cognition-salon.txt` (71,298 B, 1,371 lines, saved Sep 8)
- `C:/Users/foste/Desktop/New folder/salon4.txt` (204,898 B, 2,791 lines, saved Sep 2)

Method: cognition-salon read end-to-end; salon4 read structurally in three passes
(Tier A targets: novelty/EpistemicRisk, RDE spec, transfer package — all confirmed on the page,
line refs below). Save-artifact duplication noted in the mining dossier is confirmed
(cognition-salon: the DeepSeek correction block appears at ~L102 and again ~L530; treat as one
content block). This file is the only output. Quotes are verbatim and short; line numbers point
into the Desktop saves.

---

## 1. cognition-salon.txt — feeds TRAJECTORY LENS + TESUJI MAP

Load-bearing idea #1 — Classify trajectories, not models (the lens, stated from outside).
The salon's final conceptual move lands exactly on the trajectory-lens charter thesis:

> "Don't classify models. Classify reasoning trajectories." (L479)

> "the 'mindset' is migrating from being a property of the model to being a property of the
> inference policy." (L483)

And the support claim underneath it:

> "model personality increasingly becomes a property of: base model + post-training + inference
> policy + tools + evaluator + system orchestration." (L345)

Where it plugs in: `watch/TRAJECTORY_LENS_20260905.md` — this is independent, same-week
(Sep 8) external convergence on the lens ("not the first time... duplication is emphasis").
Cheap concrete adoption: add a regime enum to the trajectory envelope
{input, tool_result, output, reasoning, step_hash, timing} — one field, per sealed step:
recognition / search / interaction / verification (idea #2's taxonomy), plus
materialized / latent / environmental / collective (L239-253). Cost: a tag, not an organ.
Tri-state: Supported as argument (in-transcript, evidence-cited to Anthropic unfaithful-CoT work);
the fleet-side benefit is Unproven until a batch runs with the tag and someone diffs it.

Load-bearing idea #2 — Four computational regimes + "The Director" (allocation is the organ).
The salon replaces the East/West metaphor with a four-regime decomposition and then names the
missing piece:

> "AI cognition = recognition + search + interaction + verification, allocated dynamically under
> a compute budget." (L178)

> "**The Director** — The system that decides **which of the other modes to invoke**." (L371-374)

> "The fundamental trade-off in frontier reasoning is not verbosity versus intuition. It is
> computation allocation versus task uncertainty." (L457)

Where it plugs in: the tesuji map (`mag/tesuji_map.py`, `mag/tesuji_probes.py`,
`watch/TESUJI_MAP_5_3FLASH_20260906.md`). The grid currently prices cells; the regimes give the
cells a second axis — what regime the model believes it is in — and The Director is the
system-under-test: a T1/T2 probe family that presents ambiguous prompts and measures whether
5.3-flash escalates (spends) or recognizes (answers cheap). "Probes=stones" gets a target: not
just cost-per-cell but allocation-behavior-per-cell. Note The Director ≈ RDE ≈ router — same
organ seen from two salons (see cross-finding below).
Tri-state: the four-regime split is Supported as a working taxonomy (it is descriptive, not
falsifiable as stated); using it as a probe axis is Unproven until a probe run.

Load-bearing idea #3 — The amortization loop explains cell drift (why tesuji cells rot).
The GLM self-audit round contributes the mechanism that makes the map a moving target:

> "1. **Deliberate:** expensive search during training ... 2. **Amortize:** bake the search into
> weights ... 3. **Intuit:** now the model 'just knows' ... 4. **Gap appears** → deliberate
> again" (L514-517)

> "AlphaZero is the canonical proof: search creates intuition; intuition then skips search." (L519)

Plus the trace-honesty axis that justifies trajectory records over CoT-trust:

> "The chain of thought is not the mind. It is an **interface between computation and
> observation**." (L275-277)

> "whether the trace you see is the computation or **a press release about the computation**" (L160)

Where it plugs in: (a) tesuji dirty-radius invalidation gets a falsifiable mechanism —
provider-side amortization predicts cells flip on provider model updates, so re-probe after any
catalog/pin change (Lite pin glm-5.3-flash, live clamp 1400/day), not on a calendar; (b) the
trajectory lens: record the envelope, never trust the visible reasoning as the computation.
Bonus nugget for `docs/ref/ZAI_API_EXPERT_REFERENCE.md` — GLM debunking its own marketing in
first person:

> "At inference I don't see the future; there is no future until I generate it." (L498)

(blank infilling = pretraining objective, not inference mechanism; modern GLM = decoder-only +
thinking modes). Tri-state: the self-audit is a model describing itself — Supported where it
matches public GLM architecture history, but our own catalog line "thinking can't be disabled on
5.x" vs the salon's "GLM has thinking / direct-response modes" (L106) is a wording tension we
should reconcile against the API reference, not against the salon. Unproven until checked
against `docs/ref/ZAI_API_EXPERT_REFERENCE.md` facts.
Tail note: the Holmes/detective history (L583-1372) ends on the operator's "iterate and create
a journal quality document" (L1372) — lower value per byte, but one line is pure fleet law and
worth keeping: "The mature detective is someone who can destroy their own explanation." (L1346)
— that is the falsifier discipline, stated as detective craft.

---

## 2. salon4.txt — feeds the RIGHTSIZE stage (vision pipeline)

Load-bearing idea #1 — Novelty operationalized as manifold distance, WITH named failure modes.
This is the Tier A headline and it is on the page in the "Socratic Enhancement ... v2.0" pass:

> "Novelty is defined as distance from a learned manifold" (L1690)

> "False novelty: A query far from the manifold but semantically simple (trivial edge case)" /
> "False familiarity: A query near the manifold but epistemically novel (new combination with
> high stakes)" (L1700-1701)

> "The novelty score is always accompanied by a confidence interval and a failure-mode
> annotation." (L1703)

Where it plugs in: RIGHTSIZE (stage 5 of READ→FILTER→INTERPRET→CITE-GATE→RIGHTSIZE→JIT).
The rightsizer's job is "how much render does each cluster deserve" — this gives it its missing
input: a distance score. And the fleet already owns the manifold:
`mag/topic_index.py` (1,040 cards / 23 buckets) IS the learned manifold; nearest-bucket distance
of a new claim cluster = a $0 novelty proxy, no new vector DB needed. False novelty/false
familiarity become the rightsizer's two named, disclosed failure modes.
Tri-state: the manifold idea is Supported (standard OOD detection dressed in salon clothes);
the specific metrics in the transcript (cosine-to-centroid + density estimation) are Unproven
fleet-side — we have not run any distance scoring against topic_index yet.

Load-bearing idea #2 — Fallibility over novelty (the escalation criterion, corrected in-file).
The salon contains its own better half. The v7.0 pass explicitly demotes novelty to a signal:

> "novelty is the wrong escalation criterion" (L1021)

> "The Render Decision Engine estimates fallibility using: 1. Model calibration ... 2. Stakes
> assessment ... 3. Uncertainty estimation" (L1029-1033)

> "The Spore Ledger's 'novelty' metric is retained as a signal but is weighted by stakes." (L1041)

Familiar+high-stakes escalates; novel+low-stakes stays low with disclosure. The escalation
arithmetic is P(error) × severity (L985-989).
Where it plugs in: RIGHTSIZE's gate order. Cite-gate already runs before rightsizing; the
adoption is the decision rule after it: escalate to full render + deep cite when
(error-likelihood × stakes) is high — regardless of novelty — and downshift novel-but-trivial
links to JIT. This prevents the two classic wastes: premium tokens on a spicy-but-empty link,
and a coasting summary on a familiar-looking but load-bearing claim.
Tri-state: the transcript carries both "ensemble interpolation" (v2.0, L1670-1683) and the v7.0
correction "Ensemble interpolation is a quality-smoothing strategy with a cost penalty" (L1056)
→ early-exit instead. The file never declares a winner; v7.0 is the later and sharper argument,
so adopt the fallibility + early-exit reading and mark the ensemble path Disputed-in-source.

Load-bearing idea #3 — The transfer package (the salon output built as an inter-model spore).
The final section is a self-described handoff artifact — a salon product engineered so another
model can continue it:

> "This transfer package contains everything needed for another model to produce a research
> journal-level report." (L2778) — "26 arXiv preprints / 2 conference/journal publications" (L2780-2782)

With deep-citation anchors throughout (【4†L22-L25】 style) and expansion prompts for the
receiving model (L2737-2756).
Where it plugs in: two places. (a) RIGHTSIZE/spec validation — this is the vision pipeline's
output format proven in the wild two weeks before the pipeline was named: trajectory-as-record,
produced for handoff, not for chat. The pipeline's JIT stage should ship cards in this shape
(summary → chronology → bibliography → open questions → expansion prompts for the NEXT model).
(b) The bibliography itself is re-ingest bait: 26 preprints on PEFT, AutoPT swarms
("stigmergic blackboard coordination", L277 — same pattern as our swarm), LLM system design.
Tri-state: DISPUTED until cite-gated — the anchors are model-generated, the arXiv IDs are
future-dated in-universe, and this corpus family has a known fabricated-citation catch
(salon.txt: "Penix-Titus et al., 2021 does not exist"). Never reuse a single ID from this
package without `mag/cite_gate.py` verification. Numbers inside the salon ("message 30 costs 31×
message 1" L2301, "40-60% budget savings" L1383, ">85% cache hit" L715) are salon claims, not
measurements — Unproven, do not promote to fleet facts.

---

## Cross-salon finding — one organ, two names, no build

cognition-salon's "The Director" (decides which regime to invoke, when, for how long) and
salon4's "Render Decision Engine" (decides which LOD to render under
FinancialCost + λ1·EpistemicRisk + λ2·SovereigntyErosion, L2400-2401) are the same organ:
metacognitive resource allocation. The fleet does not have it — routing is currently hand-made
lane mapping. The MAG-CHORD-v4 verdict already governs the temptation: "Do not build a new
subsystem." Adoption is therefore: vocabulary (regime tags, novelty/fallibility/groundability
fields), probe designs (Director probes on the tesuji grid), and two fields in the rightsizer —
not an RDE build. Groundability (salon4 L1164: "A model can be confident ... but ungrounded ...
The user needs to know both") pairs naturally with cite_gate output and the existing
attested/reconstructed/speculative viability rating; it adds the "independently verifiable at
all" axis for the X-harvest. Unproven until a batch labels with it.

---

## 5-line summary

1. Both Tier A saves re-read from source; all mining-dossier claims confirmed with line refs.
   cognition-salon (Sep 8) feeds the lens: "Don't classify models. Classify reasoning
   trajectories" (L479) — independent same-week convergence on TRAJECTORY_LENS_20260905.
2. cognition-salon's three adoptions: trajectory-classification (regime enum on the envelope),
   the four-regime taxonomy + The Director as a tesuji probe family (allocation behavior, not
   just cost), and the deliberate→amortize→intuit loop as the mechanism behind dirty-radius
   invalidation. GLM first-person self-audit (L498) flagged for the ZAI reference.
3. salon4 (Sep 2) feeds RIGHTSIZE: novelty = manifold distance with false-novelty /
   false-familiarity failure modes (L1690-1703), and topic_index (1,040 cards/23 buckets) is
   already the manifold — distance scoring is a $0 add, no new subsystem.
4. The salon's own correction is the better adoption: fallibility over novelty
   (P(error) × severity, L1021-1041) as the rightsizer's escalation rule; ensemble-interpolation
   branch marked Disputed-in-source against v7.0's early-exit argument.
5. Hard gates: salon4's 26-preprint transfer bibliography is model-generated and future-dated —
   cite_gate before ANY reuse (this corpus already caught one fabricated citation in salon.txt);
   all in-salon numbers (31× token cost, 40-60% savings, 85% hit rate) are Unproven claims, not
   fleet measurements. One organ, two names (Director ≈ RDE): adopt vocabulary + probes + two
   rightsizer fields; no RDE build, per MAG-CHORD-v4.
