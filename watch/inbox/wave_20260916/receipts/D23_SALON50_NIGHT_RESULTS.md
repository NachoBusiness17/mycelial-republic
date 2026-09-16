# D23 — SALON-50 NIGHT RESULTS (50-seed fanout over the night's three verdicts)

- **Lane:** D23 (wave-lane) · **Date:** 2026-09-16 · **Budget:** FREE LANES ONLY, $0, abort at paid walls.
- **Wave-lane law:** receipt first, append as you go, no git.
- **Operator order (verbatim):** "do our 50 wide shit on the results" — fire the 50-wide fanout over the night's three verdicts.
- **Read first (done, verified against sources):** `watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md` (§6.1 sampler REFUTED: n=8 probe rho +0.167 p=0.70 wrong-signed, then pre-registered same-day replicate **rho +0.327, n=36, p=0.052 — past the +0.3 refutation line; "the salon is a diversity pump, not a quality sampler"**; §6.2 Extropic replication seat / 140x claim, simulator + open weights, no silicon measurements; §4 falsifiers incl. §4.1 with the ρ<0.3 kill threshold), `receipts/SALON_ESS_20260916.md` (INSUFFICIENT-DATA verdict + Part-1 numbers), `receipts/HERMES_REDTEAM_20260916.md` (attack 1 = sampler analogy load-bearing and false as stated; no transition kernel, no detailed balance; kill at ρ<0.3).
- **GEN-2 NOTE (continuation):** a prior session (gen-1 lineage) registered this receipt, probed lanes (~13:51 UTC), and froze a run design — but **never fired**: no runner existed, no `memory/runs/d23_salon50_night_20260916/` on disk. Gen-1's Q1 carried the n=8 probe number (+0.167, p=0.7); the operator's mission text carries the REPLICATED number (+0.33, wrong-signed, replicated). Mission text is authoritative — Q1 below is the mission VERBATIM set. Gen-1's design also confounded temperature with question ([0.2,0.7,1.2][s%3] with question = s%3 → q0 always sampled at 0.2); fixed below.
- **CLI discovered (read, not edited):** `mag/scale_salon.py` — no argparse; `sys.argv` only (`--retry`); hardcoded to THE SCALE parable, 12 writer lenses + 2 gophers, `ThreadPoolExecutor`, raw.jsonl + pack writer, SSRF allowlist guard. Scale-salon-style runnable machinery lives in `mag/research_fanout.py` (`LANES`, `_env`, `probe_lanes`, `call_lane` — call never raises, failures are rows). D22 baseline: alive = groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, zai-air, or-nemotron, or-ling3; dead = groq-qwen, mistral-small (429), or-glm52 (502), zai-47 (PAID WALL — do-not-retry). D22's own probe log is a stub → probing live as I go.

## QUESTION SET — registered verbatim BEFORE firing

- **Q1 (the sampler verdict) — MISSION VERBATIM:** "A measurement found that decorrelation between free-LLM lanes does NOT predict answer quality (rho +0.33, wrong-signed, replicated). Does this kill the analogy that multi-model salons are thermodynamic samplers, or can it be saved by redefining the ensemble? Take a side, under 120 words."
- **Q2 (the Extropic seat) — MISSION VERBATIM:** "A vendor claims 140x energy efficiency for thermodynamic sampling hardware and publishes a simulator + open weights, but no silicon measurements. What is the strongest falsification protocol a $0-budget team can run, and what could it NOT prove? Under 120 words."
- **Q3 (the ledger) — MISSION VERBATIM:** "An append-only evidence ledger cannot delete false rows. Design the void procedure in one paragraph: what marks a row dead, who can mark it, and what prevents weaponized voiding. Under 120 words."

## Run design (frozen before firing — GEN-2, supersedes gen-1's draft)

- ONE run, up to 50 seeds, over the three mission-verbatim questions, across probed-live free lanes only.
- **zai-47 NEVER called** (paid wall, do-not-retry law); filtered from the candidate list before probing.
- Deterministic seed map (gen-2, confound-fixed): for seed s in 0..49 —
  question = QUESTIONS[s % 3]; lane = live_lanes[(s // 3) % len(live_lanes)];
  temperature = [0.2, 0.7, 1.2][(s + s // 3) % 3]; api `seed` field = 2026091600 + s.
  Rationale: gen-1's temp ladder [..][s%3] was perfectly confounded with question (q0 always 0.2). The (s + s//3) % 3 ladder gives every question all three temperatures in rotation AND every lane all three temperatures.
- Plumbing: imports `LANES`, `_env`, `_now` from `mag/research_fanout` UNMODIFIED; own `call()` mirrors `mag/scale_salon.py` (temperature parameter, SSRF allowlist + resolved-IP guard from the same free-base set). Repo code untouched.
- Wave-protocol §6.5 law: rotation not flood — max 8 in flight, per-lane stagger, failures preserved as rows.
- If a seed fails with a 429-class error: keep the row, one cooldown retry pass (single attempt, same lane) per fleet retry law (append-only, never delete); paid-wall-style rejection = abort that lane permanently.
- Output: `memory/runs/d23_salon50_night_20260916/raw.jsonl` (append-as-you-go per row) + copy into this receipts dir per SALON_FREE precedent. Runner: `watch/inbox/wave_20260916/d23_salon50_night_20260916.py`.
- Interrupt law: if the limit bites mid-run, file what landed — partial width is still width.

## Probe log

### Gen-1 probe (~13:51 UTC, prior session — kept for the record)

- OK: groq-qwen 388ms (flaky — 429 in its run B), groq-oss 590ms, groq-oss20 337ms, cerebras-oss 398ms, cerebras-qwen 287ms, mistral-min8 4.9s, or-nemotron 45.9s, or-ling3 1.3s.
- DEAD then: mistral-small 429, zai-air 429, or-glm52 429, zai-47 (paid wall — not attempted).

### Gen-2 live probe (fired 2026-09-16 ~14:05 UTC, one READY ping/lane, `--probe`, $0)

- **zai-air: DEAD — PAID WALL.** HTTP 429 code 1113 "Insufficient balance or no resource package. Please recharge." Lane status ABORTED_PAID_WALL, do-not-retry this run. Second paid wall of the night alongside zai-47 (never called, filtered before probe).
- OK: groq-oss 576ms · groq-oss20 478ms · cerebras-oss 397ms · cerebras-qwen 314ms · or-ling3 1.4s · or-nemotron ALIVE but 243,686ms (4 min for a READY ping; answer channel starts with visible chain-of-thought — SALON_FREE precedent rank-4 lane, kept, background-pooled).
- groq-qwen: HTTP 429 "Request too large for model" (org capacity/TPM class, not a hard dead — one cooldown retry before firing).
- mistral-min8: HTTP 422 `extra_forbidden: body.seed` — **Mistral rejects the OpenAI-style `seed` field**; gen-2 driver bug found by the probe (probes are cheap and that is why we probe). Fix: omit `seed` for mistral-base lanes; record `api_seed` in the receipt row either way.
- mistral-small: 429 rate-limited (third night-class confirmation, stays dead). or-glm52: 429 temporarily rate-limited (stays dead this run).
- **Live set for the run (8 lanes):** groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8 (post-fix), or-nemotron, or-ling3, groq-qwen (pending its retry).

## Run log

- Gen-2 re-probe (~14:10 UTC): mistral-min8 OK 2857ms post-seed-fix (verbose READY, in character). groq-qwen STILL HTTP 429 after 25s cooldown → dropped from the live set (flaky-dead; failures preserved as rows if it appears). zai-air stays aborted (paid wall).
- **LIVE SET (7 lanes, frozen at fire time):** groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, or-nemotron, or-ling3.
- **FIRED:** ONE run, 50 seeds, background (or-nemotron pings at ~4 min ⇒ wall time double-digit minutes). Map: q = s%3, lane = live[(s//3)%7], temp = TEMPS[(s+s//3)%3], api_seed = 2026091600+s. Rows append to `memory/runs/d23_salon50_night_20260916/raw.jsonl` AS THEY LAND.

- Pass 1 completed ALL 50 seeds appended (~14:12–14:17 UTC, ~5 min wall; 44 ok / 6 fail on first attempt, rows appended as they landed). Mid-run events, recorded honestly:
  - **cerebras-oss mid-run abort (evidence damaged by a gen-2 driver bug):** after its first three seeds (s=6,7,8) answered fine, a later cerebras-oss call returned an HTTP error whose body matched the paid-wall signal list → `_aborted_lanes` flag killed s=27,28,29,48,49. **The bug:** the abort short-circuit REPLACED the real result rows with synthetic `lane_aborted_paid_wall_midrun` rows carrying no lane/detail — the actual triggering error body (likely Cerebras daily free-quota exhaustion, a rate-limit class, not a true paid wall) is NOT preserved in raw.jsonl. Violation of "trust bytes" by my own hand; fixed in the driver (abort now only MARKS, never replaces) and the retry pass will recover the real error row. Lesson filed: an abort gate must annotate evidence, never overwrite it.
  - **cerebras-qwen s=31 `empty_content`** — qwen reasoning channel burned the 3000-token budget before emitting content; the reasoning fragment IS preserved in the row's detail (it was mid-thought formulating the Q2 falsification protocol answer). Pass 2 refires with max_tokens 4000.
  - Everything else: 44/44 OK across groq-oss, groq-oss20, cerebras-qwen, mistral-min8, or-nemotron (slow pole ~4 min/seed, answer channel starts with visible chain-of-thought per its known behavior), or-ling3.

## Results

- **49/50 seeds answered** (pass 1: 44/50; pass 2 recovered 5/6; cerebras-qwen s31 `empty_content` twice — reasoning channel exhausts the budget, rows preserved, failed seed recorded). All 7 live lanes answered on all three questions.
- Tape: `memory/runs/d23_salon50_night_20260916/raw.jsonl` (56 rows: 50 pass-1 + 6 pass-2, append-only) · copy: `receipts/D23_SALON50_raw.jsonl` · machine summary: `memory/runs/d23_salon50_night_20260916/summary.json` · `question_digest d12721eea078491b`.
- Cross-lane pairwise token-Jaccard per question: Q1 0.187 mean · Q2 0.213 · Q3 0.178 — the salon sits in the same decorrelation band as prior receipts (SALON_FREE 0.085, lane_salon 0.245).
- **Cost: $0.00.** 69 calls total (11 probe + 2 re-probe + 50 pass-1 + 6 pass-2), all free tiers (Groq, Cerebras, Mistral, OpenRouter `:free`). No paid wall touched; zai-47 never called.

## Per-question convergence/divergence map (Rashomon fold — witnesses keep their own voice, NO averaging)

Method: latest attempt per seed, 49 witnesses, attributed by seed `s`, lane, temperature (T). No consensus was computed or averaged; the map reports who said what. Full verbatim text lives on the tape.

### Q1 — sampler verdict (17 witnesses: 6 KILL / 11 SAVE-or-reshape)

- **KILL side (6):** s3 groq-oss20 T0.7 — "the underlying stochastic process does not obey the equipartition or detailed-balance principles"; s9 cerebras-qwen T0.2 — "Redefining the ensemble… merely renames a mixture… better modeled as correlated opinion pools with selection and aggregation"; s15 or-nemotron T1.2 — "a robust negative result outweighs ad hoc redefinitions… the burden now shifts to proponents"; s18 or-ling3 T0.2 — "it's just aggregating biased estimators… metaphor, not mechanism"; s39 or-ling3 T0.7 — "Redefining the ensemble is epicycle-building… Keep the intuition, discard the physics metaphor: ensembles work via bias-variance tradeoffs, not partition functions"; s45 groq-oss20 T0.2 — "the lanes are not independent samplers but are driven by shared biases".
- **SAVE side (11), each with its OWN rescue mechanism:** s0 groq-oss T0.2 "wrong order parameter → Boltzmann-weighted mixture"; s6 cerebras-oss T1.2 "multi-parameter ensemble (prompt perturbations + dropout noise + diversity regularizers)"; s12 mistral-min8 T0.7 "cooperative Gibbs sampler — collective entropy reduction, not pairwise decorrelation; one hallucinates, another corrects"; s21 groq-oss T0.7 "lanes are not independent microstates (shared training data) — trajectory-level microstates recover the link"; s24 groq-oss20 T1.2 "importance weights / Bayesian model averaging suppress low-weight decorrelated lanes"; s27 cerebras-oss T0.2 "conditioned ensemble with latent temperature variables"; s30 cerebras-qwen T0.7 "heterogeneous NON-equilibrium portfolio — quality tracks competence-weighted agreement; survives as model-averaging metaphor, not literal thermodynamics"; s33 mistral-min8 T1.2 "metastable slow manifolds — parallel Gibbs samplers stuck in nearby basins"; s36 or-nemotron T0.2 "redefine as diversity-driven, not quality-predictor"; s42 groq-oss T1.2 "Gibbs distribution over JOINT model states with coupling terms"; s48 cerebras-oss T0.7 "broaden the state space to latent configurations".
- **Lane-level pattern (the fold's sharpest finding):** groq-oss saves 3/3 · cerebras-oss saves 4/4 · mistral-min8 saves 2/2 · or-ling3 kills 2/2 · groq-oss20 kills 2/3 · cerebras-qwen splits 1-1 · **or-nemotron contradicts ITSELF across temperature — s36 T0.2 saves, s15 T1.2 kills.** A witness that flips its verdict with sampling temperature is itself evidence for the kill side: a "lane" is not one stationary sampler, so lane-level calibration claims are unstable at the source. The pack's own strike (rho +0.327, REFUTED) matches the minority here — the salon's witnesses still majority-reach for "redefine the ensemble," which is precisely the special-pleading move the kill side names. Witnesses keep their voices; the canon keeps its falsifier.

### Q2 — Extropic 140x falsification protocol (16 witnesses: high convergence, four distinct accents)

- **Convergence core (~16/16):** run the vendor's own open simulator + open weights on commodity CPU/GPU against a tuned baseline sampler on the SAME host; measure real joules/sample (RAPL, nvidia-smi, powertop, USB power meter/shunt); preregister; replicate across seeds and ≥2 platforms; publish the bytes. Free cloud VMs named (Colab, s43/s49).
- **Four accents (kept in voice):** (a) *simulator forensics* — mistral-min8 s13/s34: reverse-engineer the simulator for unphysical noise models, entropy-bound violations, "undocumented shortcuts"; falsify the math even without silicon. (b) *ceiling audit* — or-ling3 s19/s40 + groq-oss20 s25: hard-code Landauer and realistic CMOS leakage; "absence of silicon data is itself the falsification… you only kill the fantasy of free energy; you cannot resurrect the hardware." (c) *quality-gated accounting* — cerebras-qwen s10: preregistered 10-task benchmark, KL/TVD gate vs reference, energy per ACCEPTED sample; falsifies "at the simulation level." (d) *omission audit* — or-nemotron s37: check what the simulator leaves out (dynamic power, memory wall, clock-gating); "the omission of silicon measurements is not a gap — it's a red flag."
- **Universal "cannot prove" list:** that real silicon would (or would not) meet 140x; hidden proprietary optimizations; workload representativeness/cherry-picking; that the hardware does not exist; yield, latency, thermal behavior, long-term reliability. s43's phrasing is the discipline: absence of hardware measurements means you can only falsify the *simulation* and its plausibility, not the device.

### Q3 — append-only ledger void procedure (16 witnesses: near-total structural convergence, real disagreement on who holds the pen)

- **Convergence (~16/16):** a void is a NEW signed append — void-event / void marker / revocation seal / nullifier / tombstone — that hash-binds to the target row, carries a mandatory public justification, and never deletes. Death is an index/state property, not an erasure.
- **Who can mark it (the live disagreement):** 3-of-N independent auditors with hardware-held threshold keys (s8 cerebras-oss); multi-sig incl. the originating custodian (s23 groq-oss — the only one letting the originator co-sign); 2/3 supermajority (s14/s35 mistral-min8, s47 groq-oss20); sortition-selected forensic committee (s20 or-ling3; VRF-chosen pool in s14); MPC threshold with bonded validators — "no single institution, no row originator, plus at least one external challenger," separate quorums for proposal vs index-flip (s11 cerebras-qwen); rotating reputation-bonded KYC stewards (s17/s38 or-nemotron); public challenge windows 24h–7d (s2, s8, s29, s35, s38, s47).
- **Anti-weaponization inventory (union of voices):** staked collateral + slashing on overturned voids (s11, s14, s17, s20, s35, s38, s41); justification hash must resolve to an independently verifiable audit report (s8 cerebras-oss); proof-of-error required + voids must arrive within a narrow window after row creation (s26 groq-oss20 — staleness defense, double-edged: also blocks late-discovered fraud); **void-of-void** — a void auto-invalidates if its cited evidence is itself voided or fails reproducibility (s32 cerebras-qwen); permanent public rebuttal annex any party can append (s38 or-nemotron).
- **Witness quirk preserved in voice:** s17 or-nemotron leaked its entire drafting loop into the answer channel (word-counting, re-reading the prompt, revising) — its FINAL paragraph lands at exactly 120 words and carries the bonded-escrow design. Kept verbatim on the tape; graded on the paragraph, not the leakage.

## 5 best new mechanisms

1. **Competence-weighted non-equilibrium portfolio** (s30 cerebras-qwen). Replaces decorrelation with *competence-weighted agreement* as the salon's order parameter: quality tracks structured error cancellation among heterogeneous priors, not lane independence. Directly testable for $0: re-run the pack's correlation using per-lane desk-rank weights instead of raw decorrelation on the existing SALON_FREE tape.
2. **Cooperative-Gibbs / contradiction-resolution value metric** (s12 mistral-min8; consonant with the pack's own replacement verdict "salons are for coverage and contradiction"). Score a salon by its *contradiction-resolution rate* — pairs where one witness's error is caught by another — instead of ESS or diversity. Makes the salon's value claim measurable without any thermodynamics.
3. **Landauer+leakage ceiling audit** (or-ling3 s19/s40, groq-oss20 s25). Hard-code kT·ln2 and published platform pJ/FLOP as denominators before any measurement: any efficiency claim whose arithmetic requires negative entropy or silently excludes leakage/encode-decode overhead is falsified on paper, $0, before silicon exists. Reusable against every future vendor claim; pairs with the pack's DAD discipline and Correspondence cost C.
4. **Void-of-void: self-neutralizing tombstones** (s32 cerebras-qwen, with s11's separate proposal/index quorums). Every void record carries a revocable expiry and inherits the SAME evidential burden it imposes: if its cited evidence is itself voided or fails replication, the void auto-invalidates and the original row wakes. Weaponized voiding becomes economically self-defeating without requiring perfect first-round judges. (Variant on file: s26's staleness window.)
5. **Temperature-flip instability as a sampler-identity diagnostic** (observed, not told: or-nemotron saved at T0.2 / killed at T1.2 on Q1; cerebras-qwen split 1-1; groq-oss never flipped in 3 seeds). Fire the same verdict question at a 3-temperature ladder per lane; intra-lane verdict flips reveal that a "lane" is a mixture of samplers, not one stationary witness — a $0 instrument that generalizes the fleet's "thinking-mode is the axis" doctrine and bounds how much any single-lane calibration can be trusted.

## Dead-lane list

- **zai-47 — PAID WALL, never called.** Mission order; filtered before probe; do-not-retry law holds.
- **zai-air — PAID WALL (discovered live this run).** HTTP 429 code 1113 "Insufficient balance or no resource package. Please recharge." Alive in the D22 baseline, dead hours later. Abort, do-not-retry.
- **mistral-small — HTTP 429 rate-limited** (dead across D22 baseline, gen-1 probe, and this probe).
- **or-glm52 — HTTP 429 temporarily rate-limited** (dead this run after its 502/429 history).
- **groq-qwen — flaky-dead:** HTTP 429 "Request too large" (org capacity/TPM class) twice at probe, including after cooldown. Excluded from the live set; no rows in the run.
- **cerebras-qwen s31 — permanently empty seed** (not a dead lane): `empty_content` on both passes, reasoning channel exhausts the token budget; both failure rows preserved on the tape.
- Incident, NOT a dead lane: **cerebras-oss** transient mid-run abort (paid-signal body match; the real error body was lost to the abort-replacement bug documented in the run log) — recovered 5/5 on pass 2; finished 8/8 answered.

## Status: CLOSED

- One run fired and completed: 50/50 seeds attempted, 49/50 answered, 7/7 live lanes on all three verdicts, **$0.00 total** — free tiers only, no paid wall touched, zai-47 never called.
- Runner: `watch/inbox/wave_20260916/d23_salon50_night_20260916.py` (imports `mag/research_fanout` LANES/_env/_now unmodified; repo code untouched; driver bugs found and fixed are documented in the run log).
- All answers are LEADS, not facts — model output from free channels, preserved verbatim on the tape. The Rashomon map above is an index to the tape, not a replacement for it.
