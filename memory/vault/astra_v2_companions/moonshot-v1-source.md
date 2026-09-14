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

## THE BUILD (six builds, in order)

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
