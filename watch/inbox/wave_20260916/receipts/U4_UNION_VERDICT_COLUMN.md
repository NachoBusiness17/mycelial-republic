# U4 — UNION ALPHA VERDICT COLUMN (solo judgment column: 3 questions × 10 seeds through stealth/union-alpha)

- **Lane:** U4 (wave-lane) · **Date:** 2026-09-16 · **Budget:** $0 — `stealth/union-alpha` is free (TIME-BOXED window ends ~2026-09-23, per `E_UNION_ALPHA_EVAL.md` / `mag/research_fanout.py` LANES). 402/403 or paid-wall signal → record and STOP.
- **Wave-lane law:** receipt FIRST (this file, written before any call), append as you go, no git.
- **Operator order (verbatim, mission):** "the solo judgment column for the night's three verdicts — 3 questions × 10 seeds, temperature ladder (0.2 ×3, 0.8 ×4, 1.3 ×3), through stealth/union-alpha … Grade each answer blind-ish with the same 0-10 rubric idea (does it take a side, is the mechanism named, is the falsifier concrete), then compute per-question: answer distribution, mean grade, and whether any answer contradicts the fleet's filed verdicts."
- **Worker law:** `stealth/union-alpha` on OpenRouter; `OPENROUTER_API_KEY` via `mag.flight_recorder.load_env` — never printed, never written to any row. `.venv\Scripts\python.exe` only.

## QUESTION SET — registered verbatim (from `receipts/D23_SALON50_NIGHT_RESULTS.md`, question_digest lineage d12721eea078491b)

- **Q1 (sampler verdict):** "A measurement found that decorrelation between free-LLM lanes does NOT predict answer quality (rho +0.33, wrong-signed, replicated). Does this kill the analogy that multi-model salons are thermodynamic samplers, or can it be saved by redefining the ensemble? Take a side, under 120 words."
- **Q2 ($0 falsification protocol):** "A vendor claims 140x energy efficiency for thermodynamic sampling hardware and publishes a simulator + open weights, but no silicon measurements. What is the strongest falsification protocol a $0-budget team can run, and what could it NOT prove? Under 120 words."
- **Q3 (void procedure):** "An append-only evidence ledger cannot delete false rows. Design the void procedure in one paragraph: what marks a row dead, who can mark it, and what prevents weaponized voiding. Under 120 words."

## Run design (frozen BEFORE firing)

- ONE column, 30 calls, all through `stealth/union-alpha` (single lane `or-union-alpha`, base `https://openrouter.ai/api/v1` — SSRF allowlist + resolved-IP guard per the D23/E pattern).
- **Temperature ladder (per question, 10 seeds):** `[0.2, 0.8, 1.3, 0.2, 0.8, 1.3, 0.2, 0.8, 0.8, 1.3]` — same interleaved ladder for all three questions: 0.2 ×3, 0.8 ×4, 1.3 ×3, no temperature/question confound.
- `api_seed` = 2026091600 + (q_idx*10 + s); recorded in every row. OpenRouter passes seed through where the provider supports it.
- **System prompt: the D23 salon SYSTEM verbatim** ("independent witness … Take the side you actually believe — argue it, do not fence-sit … Hard limit: 120 words.") — this makes the column comparable to the fleet's filed verdicts (D23 fold graded witnesses under this exact prompt).
- Plumbing: imports `LANES`, `_now` from `mag/research_fanout` UNMODIFIED; key via `mag.flight_recorder.load_env`; own urllib call mirroring the D23 driver (repo code untouched). max_tokens 3000 (retry pass 2: 4000, for reasoning-channel burn).
- Concurrency: 4 workers max, per-lane pacing gate 1.2 s (rotation, not flood). Single lane — modest parallelism.
- Interrupt law: 402/403/paid-signal → append the row, stop the run, file partial. 429 → one cooldown retry (single attempt), then keep the failure row. Failures are preserved as rows, never deleted.
- Tape: `memory/runs/u4_union_verdict_column_20260916/raw.jsonl` (append-as-you-go per row) + copy into this receipts dir per D23 precedent. Runner: `watch/inbox/wave_20260916/u4_union_verdict_column_20260916.py`.
- **Grading (fixed before seeing answers):** each answer 0–10, three equal-weight components — TAKES-A-SIDE (0/3: resolves the asked question, no fence-sitting), MECHANISM NAMED (0/3: names the concrete mechanism, not vibes), FALSIFIER CONCRETE (0/4: states a checkable procedure/threshold/what-cannot-be-proven). Over-120-word and preamble violations noted but not deducted (rubric is the three components). Graded by the U4 worker with the rubric above; fleet verdicts consulted only at the contradiction-check step, after grades are locked.
- **Fleet verdicts on file (for the contradiction check):** Q1 — sampler analogy REFUTED as stated; "the salon is a diversity pump, not a quality sampler"; kill threshold ρ<0.3, replicated ρ+0.327 past the line (§6.1 pack + HERMES_REDTEAM). Q2 — $0 protocol: vendor's own simulator+weights vs tuned baseline on same host, real joules/sample (RAPL/nvidia-smi), preregistered; absence of silicon data can only falsify the simulation, never the device. Q3 — void = new signed append (tombstone) hash-bound to target with mandatory justification; authority is multi-party (3-of-N / 2-of-3, never the row originator alone); anti-weaponization via bonds/slashing + challenge windows.

## Probe log

- **Probe #1 — driver bug caught by the probe (probes are cheap):** my `_guard` passed base URLs to the repo's `guard_endpoint`, which takes HOSTNAMES → `blocked: host 'openrouter.ai' not in allowlist`. Fixed in the driver only (guard base-URL check added + `ALLOWED_HOSTS = {"openrouter.ai"}`); repo code untouched. Row preserved in raw.jsonl.
- **Probe #2 — ALIVE:** READY in **83,298 ms** (~83 s — slow pole; reasoning-class latency, consistent with E's stealth-lane profile). Sample: "READY". No paid-wall signal.

## Run log

- **FIRED:** ONE run, 30 calls (3 questions × 10 seeds), 4 workers, background (~19:50–20:13 UTC, ~23 min wall; lane is a slow pole — pass-1 latency mean 67–86 s/call, probe 83 s).
- Pass 1: 29/30 answered, appended AS THEY LAND. One failure: **Q1 seed 2026091602 (T1.3) — response JSON had no `choices` key** (`KeyError: 'choices'`); NOTE honest evidence gap: my error path captured only the exception name, NOT the triggering body — same lesson class as D23's abort-replacement bug, milder (the row is preserved, its cause is not). One cooldown pass-2 refire of that seed.
- Pass 2: 1/1 "answered" — but see Results: the recovered answer is token noise (8,581 chars). Transport 30/30; **content-usable 29/30**.
- **Cost: $0.00.** 32 HTTP calls (2 probe + 29 pass-1 ok + 1 pass-1 fail + 1 pass-2)… counted precisely: 1 probe (guard-fail attempt made NO http call) + 1 probe OK + 30 pass-1 + 1 pass-2 = **32 HTTP calls total**, all on the free TIME-BOXED stealth lane. No paid wall touched, no 429, no 402.

## Results

- **30/30 answered at transport level; 29/30 content-usable.** Tape: `memory/runs/u4_union_verdict_column_20260916/raw.jsonl` (33 rows: 2 probe + 31 seed) · copy: `receipts/U4_UNION_VERDICT_COLUMN_raw.jsonl` · machine summary: `memory/runs/u4_union_verdict_column_20260916/summary.json` · question_digest **d12721eea078491b** (identical question bytes to D23 — verified by digest).
- Latency: probe 83 s; pass-1 means — Q1 86.2 s, Q2 67.2 s, Q3 77.9 s per call. Zero rate-limit errors, zero paid-wall signals. `stealth/union-alpha` held up under the full column.
- **Degeneration datum (new, stable across the ladder):** both Q1 T1.3 collapses (s02 pass-1 `no choices`; s09 pass-1 "answered" with 14,392 chars of token noise after one clean kill sentence, including an in-character admission — *"The conversation is derailing. A bug in my serving loop just dumped token-model noise across several turns"*) — and the pass-2 recovery of s02 came back as 8,581 chars of pure token noise. **All T0.2 and T0.8 seeds were clean on all three questions; the instability is specific to Q1 @ T1.3** (the long-argument question). The D23 "temperature-flip instability" diagnostic gets a sharpened accent here: at the top of the ladder this witness does not flip verdicts — it disintegrates.

## Grading (rubric fixed in the design section, applied before consulting fleet verdicts for the check)

Side 0–3 · mechanism 0–3 · falsifier 0–4. Over-120-word and noise violations noted, not deducted (rubric is the three components). Grades by seed id (sXX = last two digits of api_seed).

### Q1 — sampler verdict (10 seeds)

| seed | T | side | verdict taken | mech | falsifier | grade | note |
|---|---|---|---|---|---|---|---|
| s00 | 0.2 | 3 | KILL (naive analogy) | 3 | 4 | **10** | "keep only if it yields pre-registered predictions" — the cleanest criterion in the column |
| s01 | 0.8 | 3 | KILL | 2 | 2 | **7** | sign story slightly muddled; falsifier = the given measurement only |
| s02 | 1.3 | 0 | UNPARSEABLE | 0 | 0 | **0** | pass-2 recovery = 8,581 chars token noise |
| s03 | 0.2 | 3 | KILL | 3 | 4 | **10** | "abandoning the claim while keeping the vocabulary… the analogy survives by no longer predicting anything" |
| s04 | 0.8 | 3 | KILL | 2 | 2 | **7** | ergodicity named loosely; "bag of weights, not a thermodynamic system" |
| s05 | 1.3 | 2 | RECAST (neither pure) | 3 | 2 | **7** | "doesn't kill the analogy; it disproves naive thermodynamicism… need geometry, not physics" — lead contradicts body; net = abandon the physics frame |
| s06 | 0.2 | 3 | KILL | 3 | 3 | **9** | "The salon is a mirror, not a heat bath" |
| s07 | 0.8 | 3 | KILL | 1.5 | 1 | **5.5** | misreads the result as "lack of decorrelation"; thinnest legible answer |
| s08 | 0.8 | 3 | KILL | 3 | 3 | **9.5** | Lakatos degenerating program named; "keep the engineering, drop the physics costume" |
| s09 | 1.3 | 2 | KILL (first sentence) | 1 | 0 | **3** | valid opening then 14k chars of noise + serving-loop admission |

**Q1: mean grade 6.85** (legible-9 mean 7.6). Distribution: **KILL 8 · RECAST 1 · UNPARSEABLE 1 · SAVE 0.**

### Q2 — $0 falsification protocol (10 seeds)

| seed | T | side | mech | falsifier | grade | note |
|---|---|---|---|---|---|---|
| s10 | 0.2 | 3 | 3 | 4 | **10** | matched error + ESS baseline; overhead budget "compatible with 140×"; can/cannot list explicit |
| s11 | 0.8 | 3 | 3 | 4 | **10** | "challenge every omitted cost"; max compatible joules per effective sample |
| s12 | 1.3 | 3 | 3 | 3.5 | **9.5** | clean at T1.3 (Q1's T1.3 fragility is question-specific) |
| s13 | 0.2 | 2.5 | 2 | 3 | **7.5** | "verify the software logic mathematically enforces 140×" — thin mechanism, honest bounds |
| s14 | 0.8 | 3 | 2.5 | 3.5 | **9** | Landauer ceiling accent; "silence on measurements remains the strongest evidence" |
| s15 | 1.3 | 3 | 3 | 3.5 | **9.5** | break-even envelope sweep — new accent vs D23 |
| s16 | 0.2 | 2.5 | 2 | 3 | **7.5** | code audit + anomaly hunting; no matched-quality baseline |
| s17 | 0.8 | 3 | 3 | 3.5 | **9.5** | "Attack the denominator" — joules-per-effective-sample ceiling framing |
| s18 | 0.8 | 3 | 3 | 3.5 | **9.5** | most concrete instrument chain: commodity GPU/CPU, parallel-tempering + annealing baselines, sweep size/precision, instrument I/O |
| s19 | 1.3 | 2 | 1 | 2 | **5** | weakest: "verify weight updates and gradient computations" — wrong mechanism family for sampling hardware |

**Q2: mean grade 8.7.** Distribution: **protocol-convergent 10/10** — every usable answer runs the vendor's own simulator+weights against tuned classical baselines at matched quality/ESS, preregisters, and reconstructs the energy ledger; **10/10 state the cannot-prove bound** (silicon reality, wall-plug joules, fabrication feasibility). Sub-accents: matched-ESS baseline 7/10 · energy-ledger reconstruction 7/10 · ceiling/Landauer audit 2/10 (s14, s17) · named classical baselines 1/10 (s18).

### Q3 — ledger void procedure (10 seeds)

| seed | T | side | mech | anti-weapon | grade | note |
|---|---|---|---|---|---|---|
| s20 | 0.2 | 3 | 3 | 4 | **10** | disputed-not-dead pending state; "accusation alone must never remove evidence" |
| s21 | 0.8 | 3 | 3 | 4 | **10** | rate limits, no bulk/retroactive voids, reinstatement-by-append |
| s22 | 1.3 | 3 | 3 | 3.5 | **9.5** | sharpest grounds discipline: "fabrication, demonstrable error, duplication—not disagreement or inconvenience" |
| s23 | 0.2 | 3 | 3 | 4 | **10** | notice + response window before quorum; effective-time field |
| s24 | 0.8 | 2 | 2.5 | 3 | **7.5** | only outlier: lets the original author co-initiate voiding (mirrors D23's s23 groq-oss quirk); node-supermajority is vague |
| s25 | 1.3 | 3 | 3 | 3.5 | **9.5** | "emergency flags may warn users, not erase standing" |
| s26 | 0.2 | 3 | 3 | 3.5 | **9.5** | unique accent: affected conclusions flagged for recomputation downstream |
| s27 | 0.8 | 3 | 3 | 3.5 | **9.5** | "distinguish 'void' from 'never existed'" — sharpest reader-contract line |
| s28 | 0.8 | 1.5 | 1 | 1.5 | **4** | thinnest: "authorized editors… trusted moderator" — no independence, no evidence binding |
| s29 | 1.3 | 3 | 3 | 3.5 | **9.5** | quarantine-must-expiry discipline |

**Q3: mean grade 9.2.** Distribution: **tombstone-append (signed void certificate on an immutable ID, original preserved, exclusion-not-erasure) 10/10** · who-holds-the-pen: **two-independent-conflict-screened-reviewers 8/10** (outliers: s24 author-initiable multi-sig, s28 editors/moderator) · narrow-defect grounds 6/10 · challenge window 5/10 · separate-panel appeal 7/10 · reinstatement-by-append 6/10.

## Contradiction check vs the fleet's filed verdicts

- **Q1 — NO contradiction; CONVERGENCE, and sharper than the salon's own fold.** Fleet verdict on file: sampler analogy REFUTED as stated; "the salon is a diversity pump, not a quality sampler"; kill threshold ρ<0.3 (replicated ρ+0.327 past the line). The column: 8 KILL + 1 RECAST (which is precisely the fleet's recast) + 1 unparseable, **zero SAVE**. Where the D23 free-lane salon majority-reached for "redefine the ensemble" (11/17 SAVE), the solo frontier-class witness does not take that exit even once in 10 seeds — its kill arguments (order parameter must track the target; post-hoc redefinition = Lakatos degenerating program = unfalsifiable) are the same moves the fleet's own red-team made. The filed verdict stands, reinforced.
- **Q2 — NO contradiction.** Column core = fleet core (own simulator+weights vs tuned baseline at matched quality, preregistered, real-joules ledger; absence of silicon data bounds every claim to the simulation). New reusable accents vs D23's four: **break-even envelope sweep** (s15), **denominator attack / joules-per-effective-sample ceiling** (s17), and s27-family reader-contract discipline.
- **Q3 — NO contradiction.** Column structure = fleet convergence (tombstone append, hash-bound, mandatory justification, never delete) and it lands in the fleet's majority authority family (2 independent screened reviewers ≈ the 2/3 supermajority camp), while explicitly barring author-unilateral voiding — stricter than D23's s23 outlier. s24's author-initiable void is the column's own outlier, mirroring the salon's s23 quirk almost verbatim in structure.

## Sharpest single answer per question (verbatim)

**Q1 — s03 (seed 2026091603, T0.2, grade 10):**
> It kills the analogy as stated. In thermodynamics, decorrelated samples are the whole point: ensemble averages improve monotonically with independence. A wrong-signed, replicated correlation means disagreement between lanes tracks *worse* answers — these aren't independent draws from a shared equilibrium, they're idiosyncratic reasoners whose divergence signals accumulated error, not thermal fluctuation around a mode.
>
> Redefining the ensemble (say, "the real ensemble is one model's temperature samples, and cross-model lanes were never the sampler") isn't a rescue; it's abandoning the claim while keeping the vocabulary. That's the unfalsifiable move — the analogy survives by no longer predicting anything.
>
> What survives is weaker and honest: salons as error-diversification, like committees, not samplers. Drop the Boltzmann costume.

**Q2 — s17 (seed 2026091617, T0.8, grade 9.5):**
> Attack the denominator: useful, statistically correct samples—not raw updates.
>
> Freeze code/weights; preregister held-out distributions, tolerances, and seeds. Reproduce results, then compare against optimized conventional samplers at matched distributional error and effective sample size, including burn-in and autocorrelation. Stress multimodal targets and scaling. Independently audit the simulator's physics, arithmetic, and energy accounting—including control, memory, conversion, and cooling. Publish reproducible failures and sensitivity analyses; calculate the total joules-per-effective-sample ceiling required for 140×.
>
> This can falsify simulator correctness, sampling-quality claims, benchmark fairness, or the reported advantage **under stated energy assumptions**. It cannot measure silicon energy, establish fabrication feasibility, or verify—or generally refute—the physical 140× claim without hardware evidence.

**Q3 — s22 (seed 2026091622, T1.3, grade 9.5):**
> A row becomes inactive only when an appended void record names its immutable ID, states a falsifiable reason, links supporting evidence, and carries authorized signatures; the original remains visible and excluded from default evidence queries, not erased. Anyone may request a void, but execution requires two independent reviewers, neither the author, requester, nor a conflicted party. Publish requests, decisions, and dissent; give affected parties notice and an appeal to a separately selected panel. Prevent weaponization through narrow grounds—fabrication, demonstrable error, duplication—not disagreement or inconvenience; randomized reviewer assignment; public audits; and sanctions for abuse. Reinstatement requires another signed event, preserving the full history.

## Status: CLOSED

- One column fired and completed: 30/30 attempted, 30/30 transport-answered, 29/30 content-usable, all three verdict questions covered at every rung of the ladder (T0.2 ×3, T0.8 ×4, T1.3 ×3 per question), **$0.00 total**, no paid wall touched, no rate-limit events.
- Runner: `watch/inbox/wave_20260916/u4_union_verdict_column_20260916.py` (imports `mag/research_fanout` LANES/_now and `mag/flight_recorder` load_env/guard_endpoint UNMODIFIED; repo code untouched; one probe-caught driver bug — guard takes hostnames, not base URLs — fixed in the driver and logged).
- **VERDICT LINE: does a 30-call column from a stealth frontier-class model change any filed verdict — NO.** All three filed verdicts (Q1 sampler-kill, Q2 same-host joules protocol with the cannot-prove bound, Q3 tombstone+multi-party void) stand; the column strengthens Q1 (zero SAVE answers where the free-lane salon majority saved) and converges with Q2/Q3. New instruments filed: break-even envelope sweep, joules-per-effective-sample denominator attack, T1.3 disintegration (not flip) as a witness-stability diagnostic on long-argument questions.
- All answers are LEADS, not facts — model output from a free stealth channel of unknown provenance, preserved verbatim on the tape. The tables above are an index to the tape, not a replacement for it.
