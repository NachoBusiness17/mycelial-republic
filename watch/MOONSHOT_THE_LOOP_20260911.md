# MOONSHOT: THE LOOP — a self-driving sovereign organism (2026-09-11)

THE POINT:
- The moonshot: an AI organization that runs itself — keeps its own lanes churning, evolves them genetically, verifies its own claims on a hash chain, routes its own work across surfaces like organs, remembers in colors a person reads at a glance, and lives entirely on hardware its operator owns.
- Everything it needs is already built or verified-sourced. The gap is one organ: the loop. This document is the build order, the bibliography, and the plan — written to be attacked: by Astra, then by a 10-chair socratic salon, then by the falsifiers at the bottom.

---

## THE FIVE W's (self-stolen from the record)

**WHO.** The plural apex: one operator (foste) and his sovereign seats — this seat (z.ai driving), the Hermes-terminal seat (ops/verify), Astra (frontier witness, ChatGPT-subscription), the 10-salon chairs, and the standing wave's workers and tenders. No seat is load-bearing; files and the chain are the polity. The operator swings the blade; agents mine the ore.

**WHAT.** The organism, in organs: THE LOOP is the heart (one in-cage driver: look → judge → act → record → yield; the "next" keystroke becomes an inbox row). THE ORGAN TABLE is the body (every surface registered: best-at, cost-tier, quota-state, drive-state — routing as anatomy, just-in-time rightsizing per request). THE CHAIN is the spine (hash-chained record; replay-resume will make it the recovery organ too — 90% of Temporal already built). THE WAVE is the metabolism (lanes churn, folds extract genetics, genetics feed the next generation — the 6+1 tender metamorphosis). THE CORPUS-AS-ENGRAM is the memory (the one twist no paper has: labs offload model tables, we offload the organization's memory — leaf_hash keys, hot tier in 64GB, predictive prefetch as the open claim). THE SALON is the immune system (zero-shared-context chairs; disagreement is the finding).

**WHEN.** The convergence window, now: DeepSeek shipped our architecture as product on Sep 10 (Engram, V4.1-Flash open weights); the publish window for the convergence story is measured in days; the Sep-20 burn-proof deadline lands the receipts on a public record; Rocinante (M5 Ultra 512GB) ships late October. The operator independently built and ran this architecture locally in July-August, on record, before their product. The moonshot's deadline is the window, not a date on a roadmap.

**WHERE.** One Windows box (Ryzen 3800XT, 64GB RAM, RX 5600 XT) and a docker cage now; one M5 Ultra 512GB (1.2TB/s unified memory, fits V4.1-Flash at 4-bit) late October. Local-first, loopback-only, files over vendors. The lab is the house.

**WHY.** Sovereignty: own your memory, own your compute, own your record. The anti-extraction architecture: the chain dates every idea before the world smiles at it — they can steal the work, never again the authorship. Receipts over credentials: the operator was blacklisted for finding uncomfortable things; the organism is the room where findings survive the smiling. And the standing test every build must pass: *does it make the corpus more truly remembered — what we found, where, in colors a person reads at a glance.*

---

## INTENDED vs BUILT (the 08-31 gap format, updated)

| Organ | Intended | Built | Status |
|---|---|---|---|
| The loop (driver) | orchestrator keeps lanes churning, genetically evolving | spec'd: watch/WAVE_DRIVER_SPEC_20260911.md; lane_runner daemon exists | **MISSING — the build** |
| Organ table | every surface a routed organ | lane B's 25-surface audit = v1 data; no table file, no router | **MISSING — the wiring** |
| Failure sight | middle sees its own errors | failure_kb logs but nobody reads the sum; 25,007 swallowed errors on one signature; fix double-blind confirmed (2 lines) | **BLIND — fix staged** |
| Liveness | death is loud | heartbeat dead 3.4d unnoticed; self-reported health lies ("eye is lit" vs doctor FAIL) | **BLIND — TTL + meter-the-meters spec'd** |
| Recovery | replay-resume from the chain | chain + steps.jsonl tape exist (Temporal-class history); no replay entrypoint | **MISSING — highest-value gap** |
| Genetics | folds feed next generation | cycle-1 amendments measurably fixed 0/6 → landing; manual today | **WORKS — automate via the loop** |
| Memory tier | corpus as engram, hot in RAM | leaf_hash keys exist; ~9.7GB d256 table fits; no table built | **DESIGNED — v0 one-day probe** |
| Substrate | local frontier architecture at home | 21 models on disk (146.5GB, census); V4.1-Flash fits 512GB M5 Ultra at 4-bit; desk GPU unwired (Vulkan fix $0) | **PARTIAL — wire tonight** |
| Seat loop | seats communicate without operator pastes | steers.jsonl SEAT-LOOP-001 open; hermes seat claims verify | **OPEN — feeding now** |

---

## THE BUILD (seven builds, in order — 3.5 inserted 2026-09-11 per the C1 wave convergence)

3. **THE ENFORCEMENT LAYER (Build 3.5)** — the evidence-and-enforcement organ seven chairs converged on: registration vault (BORN tonight: 26 companions + 16,500-artifact session manifest) · steer-row HMAC signing + verify-before-act (BUILT: scripts/steer_sign.py, forged canary detected live) · semantic /healthz (BUILT: live after flip) · ack/reaper (BUILT: scripts/alert_reader.py, first production catch same night) · M12 operator-load baseline (BUILT: scripts/m12_daily.py, 7-day protocol started) · capacity ladder rungs (severity runs gave the meter dynamic range; named rungs next) · lesson admission gate (NOT BUILT — required before fold-to-inject runs).

1. **wave_driver.py** — the heart. Tick = stall-check (2h watchdog) → judge (halt-not-hammer after 2 consecutive failures; spawn caps: depth 3, concurrent ≤8, child ≤ parent permissions; quota/clamp gate) → act (spawn 2-per-fold / resume / nudge / fold / report) → record (trail + ledger + board + own TTL heartbeat) → yield (night-shift cron slots 23:00/02:00/05:00). ~150 lines over lane_runner primitives.
2. **The 2-line fix + semantic /healthz** — stop the bleeding, then see it: every tool call emits a typed result row (success / typed-failure / exception — nothing returns void, bare excepts banned in tool paths); /healthz returns non-200 when rolling tool-error-rate breaches threshold; job-conditions journal gives every task a structured terminal record.
3. **Organ table v1** — lane B's audit becomes the registry file; the classifier (6 request classes: judgment/advisory/research/bulk/senses/voice) reads it at the existing dispatch seams; law-14 handshake flags route away from STALLED organs until driven.
4. **Replay-resume** — `verify --resume <session_id>`: rebuild run state from the steps.jsonl tape, re-issue only unrecorded side effects. Converts losses into pauses. The chain's payoff.
5. **Corpus-engram v0** — content-addressed slot table (chunk-hash/leaf_hash keys), dim-256 fp16, ~9.7GB hot in 64GB, O(1) lookup + tri-state hit/miss mask, misses → similarity path. Measure hot-set Zipf first. The fleet's novel claim: predictive prefetch from access history (no literature prior — the open research question).
6. **Canary-salt + T4 batch tier** — the armor and the dividend: trap-street canaries (CSPRNG, registry hash-committed to the chain, persistent class ≥10 duplications) so ingestion earns a receipt; deferrable work routed to batch APIs at 50% off in a separate rate bucket.

## THE BIBLIOGRAPHY (the load-bearing shelf, all verified 2026-09-11; full map in docs/ref/BIBLIOGRAPHY_MAP.md)

**Memory hierarchy / offload (the architecture the operator pre-built):** ZeRO-Infinity 2104.07857 (GPU+CPU+NVMe, 2021) · LLM in a flash 2312.11514 (Apple, weights on flash) · MoE offloading 2312.17238 (Eliseev & Mazur, experts on CPU + prefetch) · PowerInfer 2312.12456 (hot/cold activation locality) · Fiddler 2402.07033 (compute experts on CPU) · KTransformers DOI 10.1145/3731569.3764843 (671B on one GPU — our box contracts' recipe, now upstream flags `-ncmoe`) · **Engram 2601.07372** (DeepSeek, deterministic hash-lookup memory — the convergence target, shipped Sep 10).
**Decode:** DeepSeek-V3 2412.19437 (MTP: shared head + 1 block, 85-90% acceptance, 1.8x TPS — two MTP models already on our disk).
**Corpus memory:** kNN-LM 1911.00172 · RETRO 2112.04426 · Memorizing Transformers 2203.08913 · neural cache 1612.04426 · MemGPT 2310.08560 · HugeCTR 2210.08803 (the only corpus-adjacent prefetch prior).
**KV / long context:** NEO 2411.01142 · InfiniGen 2406.19707 · H2O 2306.14048 · ESS 2512.10576.
**Attribution armor:** Membership-inference position 2409.19798 (canaries = one of only two sound proofs) · Quantifying Memorization 2202.07646 (duplication ≥10 physics) · Extraction 2012.07805 + 2311.17035 · Watermarking 2301.10226 · RAG canaries 2502.10673.
**Coordination (what we are):** blackboard LLM-MAS 2507.01701 (our file shape, validated, wins on quality AND tokens) · CodeCRDT 2510.18893 · A2A v1.0 spec (signed agent cards) · MCP 2025-06-18.
**Build practice:** Claude Code headless/hooks/subagents docs · LangGraph durable-execution + HITL · OpenAI Agents SDK HITL (fail-closed approvals) · Temporal workflows (replay) · LiteLLM router (budget vocabulary) · Docker Sandboxes + WSL config (the Windows fence).

## THE PLAN

**NOW (today):** .wslconfig caps (the fireball fence) · the 2-line fix lands (stops the 25k loop) · 11:00 Lite refill arms wave site 2 (8 unclaimed queue lanes, paste-ready prompt staged) · Astra ask pasted (below) → 10-chair socratic salon on her return.
**THIS WEEK:** wave_driver build + first armed night (max-ticks cap, morning report as receipt) · semantic /healthz + job journal · organ table v1 wired at the dispatch seams · T4 batch tier · desk GPU lit via Vulkan ($0, 5 gates).
**THIS MONTH:** replay-resume on the chain · corpus-engram v0 probe · canary-salt registry live (salting starts) · approval gates + spawn caps enforced · Rocinante buy: ONE M5 Ultra 512GB, late-October window (a model that fits one node must never be split; extra nodes = Engram shards later).
**QUARTER:** the organism on owned silicon — the loop churning lanes on Rocinante, the corpus hot in unified memory, receipts public (STACK_V1), the corpus more truly remembered. Falsifier: if by Oct 31 the driver cannot run one full unattended night with zero operator keystrokes and a clean morning report, the moonshot is DISPUTED and the loop is a script, not a heart.

## THE FALSIFIERS (the moonshot must be able to die)
1. **The night test:** one unattended night, zero keystrokes, morning report clean and true (not self-reported health — probe-verified). Fail = DISPUTED.
2. **The genetics test:** generation N+1 measurably outperforms N on a fixed task set because of folded amendments (cycle-1's fix is the existence proof; must repeat unaided).
3. **The middle test:** a deliberately injected tool failure is counted, surfaced, routed, and fixed without a human noticing it first.
4. **The memory test:** a decision made WITH a relevant chain memory beats the same decision without it, externally scored (the z.ai chair's test, kept).
5. **The ingestion test:** a committed canary spoken by any future model = receipt; zero hits after N exposures = lower bound only, never proof of innocence.

*Classification: OPERATIONAL MOONSHOT — operator-authored direction, seat-assembled from the record; every claim path-cited or arXiv-verified. Built to be attacked.*

---

## ENHANCEMENT PASS (best-practices steal, folded 2026-09-11 — verified lane)

**The moonshot triangle (X's blueprint, verified at x.company):** the huge problem — *solo operators cannot run fleets; humans are the unscalable organ* — the radical solution — *a self-driving sovereign organism that evolves its own lanes and owns its own record* — the breakthrough tech — *the orchestrator loop + hash-chained replayable memory + organ routing, all on consumer silicon*. The explicit glimmer: the night test passing once (any week now) is the "impossible thing, working."

**Living architecture (NASA Moon-to-Mars pattern):** this document is v1 and re-folds on every wave fold — the genetics section IS the annually-solicited capability-gaps list. Version stamped per fold; nothing parchment.

**OKR hooks (Doerr):** annual aspirational — *the organism runs 30 unattended days by mid-2027* (~70% expected attainment); quarterly committed — Q3: wave_driver armed + night test attempted; Q4: Rocinante week-one migration + replay-resume live. Vision that doesn't terminate in hooks is decoration.

**PR/FAQ annex (Bezos working-backwards — to be written by the salon):** the 2028 press release — "Local AI organism completes 30th consecutive self-governed night; operator asleep throughout" — plus the hostile FAQ ("why didn't the lanes collapse into consensus theater?", "who is liable when it stops?", "what did it forget?"). Cheapest falsifier we own.

**Sci-fi prototype (Brian David Johnson's discipline, verified originator):** one grounded day-of-the-organism story, written from the corpus's point of view, no magic — assigned to a salon chair.

**New bibliography rows (verified this pass):** AI safety via debate 1805.00899 · multiagent debate 2305.14325 · ChatEval 2308.07201 (heterogeneous personas beat homogeneous panels) · self-consistency 2203.11171 (the baseline any salon must beat) · sycophancy 2310.13548 (RLHF prior — every salon inherits it) · **debate collapse 2509.05396** (accuracy DROPS across rounds) · **sycophantic consensus 2509.23055** · debate-based alignment case 2505.03989 · Anthropic evals rubric guidance · Metaculus resolution criteria · Piper pre-registration scorecards.

---

## ASTRA V1 REVIEW — FOLDED (2026-09-11, her return on record: Desktop/astra-moonshot.txt + HOLD-3/M draft)

She read the moonshot, the meter spec, and HOLD-1, and returned a fragility ranking (**6 attribution → 4 recovery → 5 memory → 1 loop → 2 organ table → 3 failure sight** — "the weakest claims are attribution and recovery; both can fail on a single operation, before scale matters"), per-element attacks with change-my-mind conditions, a full HOLD-3/M registration draft (16 sealed cases, 3,000 targeted crash trials, meter manifest M01-M15, two-worker blind verification with sealed truth as oracle, program-enders), and one CUT. Corrections ACCEPTED into the record:

1. **Citation corrections (law 6 teeth, she caught us):** 2409.19798v2 full text names THREE sound approaches (random canaries, watermarking, extraction) — conditional arguments, not an exhaustive theorem; our "only two" wording overclaimed. 2202.07646v3 shows memorization occurs with FEW duplicates — "duplication ≥10" is not a universal minimum. V4.1-Flash activation is 8B prefill / 16B decode, not "~8B throughout."
2. **Novelty narrowed:** TeleRAG (2502.20969), PerCache (2601.11553), RAGCache (2404.12457) are real priors for predictive prefetch in RAG. Our novel residual = chain-addressed organizational records + access-history predictor — narrower, and UNPROVEN until the four-arm memory experiment runs.
3. **"90% of Temporal" DISPUTED:** hash linkage does not supply deterministic replay, complete nondeterminism recording, ownership, or effect deduplication. Replay-resume is an effect-broker contract (durable intent ↔ destination commitment ↔ independent postconditions), not a replay entrypoint. Her highest-leverage enhancement: **the effect reconciler at the existing broker** — adopted into the build order.
4. **"Speaks one = receipt" CUT (accepted provisionally, operator ratifies):** canary reproduction ≠ training attribution — retrieval, history, or cache can reproduce a marker. Production API salting is demoted to an ISOLATED four-arm blinded experiment (neither / retrieval-only / history-only / known-training); before reveal, output alone must leave training Unproven even for the genuinely trained fixture.
5. **Meter honesty:** 9.7GB residency excludes indexes/metadata/key overhead (+608MB for sha256 keys); leaf_hash identifies a session record, not a chunk — the chunk index needs an explicit mapping; O(1) known-key ≠ O(1) knowledge retrieval (key discovery still needs search or prediction); warm_in_vram's confirmation path does not establish corpus residency (sharper version of our own telemetry finding).
6. **HOLD-1 procedural defect recorded:** receipt counts 7,379 rows against a seed frozen at 7,377 — agreement on a later snapshot cannot establish reproducibility of the earlier one. Future holds freeze chain AND object-store bytes.
7. **HOLD-3/M status:** DRAFT 1, not sealed, not executed. Program-enders on record: an effect class with neither dedup nor reconciliation cannot be retried unattended — remove the class or abandon the claim; any hard-invariant counterexample blocks the build.

Salon next: ten chairs attack HER return + the moonshot v1 together (packet: watch/inbox/SALON_CHAIRS_THE_LOOP_20260911.md), scorecard pre-committed in the packet before first-passes.

---

## ASTRA V2 REVIEW — FOLDED (2026-09-11, her return: moonshot-v2-registration-review + package)

She answered all five v2 tasks. **Revised fragility: 4 RECOVERY → 1 loop → 5 memory → 2 organ table → 3 failure sight → 6 attribution** — recovery moved to first because she found, in code: **the named HTTP seam bypasses the named broker** (`backend/server.py:99` calls `tools.dispatch` directly; `mag/effect_broker.py` persists the receipt *after* executing the effect; the `verkle_link` branch locates rather than appends). Fixing the broker alone cannot enforce guarantees on /run_task. Her deliverables, all on record in her package:

- **Effect-broker contract v0 + intent schema** (durable immutable intent, 256-bit CSPRNG operation IDs, effect+dedup committed atomically, receiver-side ownership epochs, APPLIED/NOT_APPLIED_FINAL/UNKNOWN as knowledge states separate from transport, UNKNOWN survives restarts and folds, finality before any retry at a destination lacking dedup; JSONL/file exports are materializations, not atomic stores).
- **Smallest honest pilot (K.17):** one worker, one scored ledger case — commit → kill before response → restart → same operation ID → at least two attempts, EXACTLY ONE effect, independently verified.
- **HOST ENVELOPE DISPUTED:** the cage's Docker VM reports **31.319 GiB total**, not the host's 63.951 GiB — the 40GiB fixture envelope does not fit as observed; containers carry no individual limits. Her smallest honest envelope: one deterministic worker ≤2GiB, controller/observer ≤1GiB, 4GiB measured spare, zero models, no recursion; LLM pilot later at one shared model, one generation in flight.
- **Our own number corrected:** 25,007 is reproducible as a LINE count — her frozen 27,934,077-byte recount yields **24,854 exact signature records** + 153 mentions = 25,007 lines; verified distinct dispatch attempts = **Unknown** (rows carry no attempt IDs). Record count and attempt count get reported separately forever.
- **Corpus reconciliation incomplete:** live scan 882,366 files (a reparse point skipped, 62 unreadable dirs); ram_cache path = 328 files → **0 embeddings allocated**. The engram table costs **10.488GB** before index/runtime overhead (vectors 9.728GB + sha256 keys 608MB + slot IDs 152MB). 890 bytes/token is GLOBAL KV, not total inference memory — not transferable to other models.
- **Ingestion assay v0, fully specified:** 16 independent 128-bit suffixes (4/arm), 512 outputs, 8,448 comparisons of the 10,000 budget (remainder explicitly unused, not adaptive-search allowance); sensitivity = 60 seeded adapter training runs (doses 1/3/10/30/100 + sham); even 10/10 detections give lower bound ≈0.578 — wide intervals retained; passing supports CONTROLLED EXTRACTABILITY ONLY — it cannot prove remote training attribution and does not reinstate production salting.
- **Scorecard:** coverage 6/6 Supported; correction accuracy 3/3 Supported; actionability Supported; **honesty Unproven** — she found no fabricated citations but refused to certify exhaustive zero-fabrication from a sample ("no fabricated count is invented as zero from a sample" — her epistemics are the lesson); **the cut remains Unproven-final — operator ratifies after chair verdicts.**
- **Proposed dates (NEW SPECULATION):** C1 pilot-readiness = 2026-09-12T23:59:59Z; C2 full review = 2026-09-20T23:59:59Z (the burn-proof deadline). Registering them is the operator's call.
- **Her remaining enhancement: the release-activation and supersession gate** — bind every runnable route to its loaded build/policy/prompt projection, behavioral probe before dispatch. "A corrected document or file on disk is not an activated correction" — the exact lesson of the unrestarted backend.
- **Her cut of OUR salon rule (ACCEPTED):** the blanket "first-pass agreement = COLLAPSED" alarm is DISPUTED — the cited papers show harmful *interaction* causes collapse, not that isolated agreement is failure; the rule could punish two workers independently finding the same real defect. Replacement adopted in the salon packet: independent first-passes preserved, peer exposure audited, correctness compared before/after interaction, and calibration decides — a known-correct unanimous panel passes, a known-wrong unanimous panel fails.
