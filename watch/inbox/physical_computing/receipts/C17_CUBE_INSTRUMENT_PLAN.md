# RECEIPT — C17: the ONE instrumented mycelium cube plan (C17_CUBE_INSTRUMENT_PLAN)

Lane: background wave-lane, fleet repo local_sovereign_agent
Date: 2026-09-16
Mission: build the ONE instrumented mycelium cube plan so falsifier §4.3 (upgraded by
Hermes red-team) can actually die or live: characterize echo-state/fading-memory properties
FIRST, then binary discrimination vs a random-noise baseline. "Beats chance" is vacuous
without the baseline.
Budget law: no paid APIs; WebSearch/WebFetch free; no git.
Status: FILED 2026-09-16 — plan complete, proposal tier (two-eyes pending).

## Progress log

- [step 0] Receipt file created before any other work (interruption protocol).
- [step 1] Context read: pack §4.3 falsifier + §6 red-team upgrade located
  (`PHYSICAL_COMPUTING_PACK_20260916.md` lines 105-107, 140-143; red-team attack 2
  verbatim in `HERMES_REDTEAM_20260916.md` FINAL REPORT: "reservoir computing demands
  fading memory / echo-state property that no one has characterized for fungal substrate...
  'beats chance' is vacuous without a random-noise baseline; the $50 binary-discrimination
  experiment with pre-registered n=100, α=0.05"). Binding numbers inherited: n=100 trials,
  α=0.05, ~$50 class.
- [step 2] SCIENCE BASE — WebSearch fired → **429 rate limit (gen-1's killer), survived this
  time**: the tool degraded to model-knowledge fallback instead of dying. Fallback canon
  (UNVERIFIED until live fetch): Adamatzky lab protocol = differential pairs of
  iridium-coated stainless-steel sub-dermal needle electrodes (ECG/EMG style) inserted
  5–10 mm apart into fruit bodies, differential amplification, 12-bit ADC, sampling
  ~1–10 Hz (up to 100 Hz for spike detail), spike extraction by thresholding on the first
  derivative. MITIGATION adopted: switch citation-hunting to WebFetch against the free
  arXiv API (different tool, no shared limit), space out WebSearch retries.
- [step 3] VOID procedure read: `wave_20260916/receipts/A2_EPISTEMOLOGY_ENGINE.md` —
  delete-as-append via cross-signed `kind:"void"` rows (reason codes MALFORMED / FORGED /
  EVIDENCE_DEAD / EVIDENCE_MUTATED / WARRANT_FAILED), re-anchor rule, admission view.
  Integration section will map sensor rows onto this law.
- [step 5] SCIENCE BASE LANDING (live sources, WebSearch recovered + Europe PMC API):
  - **Adamatzky fungal canon (Europe PMC, verified DOIs/PMCIDs):** "Towards fungal computer"
    Interface Focus 8:6 2018 (10.1098/rsfs.2018.0029, open access PMC6227805);
    "On Boolean gates in fungal colony" Biosystems 2020 (10.1016/j.biosystems.2020.104138);
    "On electrical gates on fungal colony" Biosystems 2021 (10.1016/j.biosystems.2021.104507);
    "Fungal electronics" review Biosystems 2022 (10.1016/j.biosystems.2021.104588);
    "Responsive fungal insoles" Sci Rep 2023 (10.1038/s41598-023-31594-9, open PMC10030783).
    **Honesty flag:** "Fungal sensing skin" Fungal Biol Biotechnol 2021 was RETRACTED
    (10.1016 retraction note 10.1186/s40694-021-00114-7) — do not cite as support.
  - **2026 horizon:** Adamatzky, "Fungal biohybrid substrates for resilient sensing and
    embodied anomaly detection," Biosystems 262:105739 (Feb 2026, not open access) — abstract
    verified via Europe PMC: proposes explicit falsifiable hypotheses (disturbance detection,
    persistence under damage, embodied memory) + lean lab roadmap. Our stage ladder is a
    concrete instance of that roadmap's gap.
  - **Physarum line:** "Slime mould tactile sensor" arXiv 1306.0258; Physarum
    bio-memristor characterization (Plymouth pearl); "electrical correlates of Physarum
    spatial activity" (UWE). arXiv full-text search: ZERO papers match
    "fungal reservoir computing"; ZERO match "reservoir computing"+Physarum in abstracts —
    the trained-readout reservoir claim on fungal substrate has almost no canon to hide behind.
  - **CLOSEST PRIOR ART (2025–26, the pack must position against these):**
    1. Telhan et al., "Morphologically Tunable Mycelium Chips for Physical Reservoir
       Computing" — bioRxiv 2025.08.20.671348 / Sci Rep s41598-026-55550-5; living mycelium +
       PEDOT:PSS electrodes as physical RC kernel; code public:
       github.com/otelhan/NeuromorphicMyceliumChip.
    2. LaRocco et al. 2025, PLOS ONE — shiitake mycelium memristors, switching up to
       ~5,850/s at ~90% reliability (empirical memory, not reservoir task).
    3. "Mycelium as a computational medium" Natural Computing 2025 (10.1007/s11047-025-10040-x)
       — growth modeling toward RC, MNIST in simulation.
  - **Red-team premise CHECK (load-bearing):** formal echo-state/fading-memory
    characterization on living fungal substrate is still unproven in the literature —
    2024–25 theory exists (arXiv 2508.19145 unified fading-memory/echo-states; Sugiura 2024
    "FM nonessential for universal approximation"; Pieters 2022 plants-RC noting bio fading
    memory lacks formal proof) but no living-mycelium experimental ESP measurement surfaced.
    **Stage 1 below is therefore aimed at a real open gap, not a solved problem.**
- [step 6] Pulling instrumentation details from Telhan (Sci Rep OA) + LaRocco (PLOS OA).

- [step 7] Protocol verification ladder closed. Telhan rig fully extracted (GitHub README +
  Europe PMC core: DAQ Digilent AD2/AD3, dt=300 ms/3.33 Hz, NARMA-10, ridge readout on
  [raw, x², sin3x, cos2x], MC(K=10, 3 s lookback) = 0.209/0.052/0.048 across chips, SNR
  5–8 dB, step response relaxes in 1–2 samples, ~0.81 J/sample dominated by conditioning
  electronics, 8-month retest stable). LaRocco verified (5.85 kHz, 90±1%, dehydrates OK).
  Adamatzky "Towards fungal computer" verified at abstract level (Semantic Scholar API):
  spikes of electrical activity as information carrier, thermal/chemical stimulation,
  cluster-level signal propagation, geometry-dependent logic. NOTE: electrode/sampling
  specifics (needle electrodes, 1–10 Hz) live in full texts that bot-block (nature/PMC/RSC
  403/500) — marked UNVERIFIED-BY-BYTE below; street prices verified by search (ADS1115
  $5–12, ESP32 ~$6–13, ECG pads $8–20).
- [step 8] Plan written below; receipt = the artifact. Status → FILED (proposal tier,
  two-eyes pending; stage-0 spend requires operator word).

## Science base — what the canon actually supports (verified vs flagged)

**Source tiers:** [V] = verified this session (API/README/abstract bytes); [F] = flagged,
canon-consistent, NOT byte-verified (bot-blocked full texts).

1. **[V] Telhan, Winiski, Schaak, Siegel, Petrillo, Bayer (Ecovative, DARPA-funded),
   "Morphologically tunable mycelium chips for physical reservoir computing," Sci Rep 16:26421
   (2026) · DOI 10.1038/s41598-026-55550-5 · PMC13500807 · code: github.com/otelhan/NeuromorphicMyceliumChip (MIT).**
   Closest prior art. Design-grow-compute: grown hyphal networks, vacuum-infused PEDOT:PSS,
   **chips are non-living at compute time** — the living-cube reservoir claim stays open.
   Protocol (from repo README): 16 parallel input channels, carrier board with 4x gain +
   OPA552/454 HV conditioning; input = NARMA-10 drive + step/random-pulse/sine, 1–4 V;
   **sampling dt = 300 ms (3.33 Hz)**; readout = ridge regression on [x, x², sin(3x), cos(2x)],
   1000 training samples; **memory capacity MC(K=10, 3 s lookback): 0.209±0.067 /
   0.052±0.023 / 0.048±0.016 across three chips** (≈4x device-to-device spread — the single
   strongest argument for our per-cube noise baseline); NARMA-10 NRMSE ≈ 1.01–1.07, SNR
   5–8 dB; monotonic MC decay with lag ("finite fading-memory behavior"); ~0.81 J/sample,
   conditioning-electronics-dominated. Their measured MCs are our stage-1 comparison bar.
2. **[V] LaRocco et al. (Ohio State), "Sustainable memristors from shiitake mycelium,"
   PLOS ONE 20(10):e0328965 (2025) · PMC12513579.** Living mycelium as memristor: switching
   to **5.85 kHz**, **90±1% reliability**, survives dehydration. Empirical memory + endurance
   without any reservoir task or ESP measurement.
3. **[V] Adamatzky, "Towards fungal computer," Interface Focus 8(6):20180029 (2018) ·
   PMC6227805** — abstract: info encoded in spikes of electrical activity; thermal/chemical
   stimulation of one fruit body changes electrical activity of others (network propagation);
   logic functions depend on mycelium geometry.
4. **[V] Adamatzky canon, Europe PMC census:** Boolean gates (Biosystems 2020,
   10.1016/j.biosystems.2020.104138), electrical gates (Biosystems 2021, 10.1016/j.biosystems.2021.104507),
   "Fungal electronics" review (Biosystems 2022, 10.1016/j.biosystems.2021.104588),
   fungal insoles (Sci Rep 2023, 10.1038/s41598-023-31594-9). **RETRACTED — do not cite:**
   "Fungal sensing skin" (Fungal Biol Biotechnol 2021, retraction note 10.1186/s40694-021-00114-7).
   **[V] Adamatzky, "Fungal biohybrid substrates for resilient sensing and embodied anomaly
   detection," Biosystems 262:105739 (Feb 2026):** proposes falsifiable hypotheses (disturbance
   detection, persistence under damage, embodied memory) + lean lab roadmap — our ladder is a
   concrete instance of exactly that gap.
5. **[V] Physarum line:** slime-mould tactile sensor (arXiv:1306.0258), Physarum bio-memristor
   characterization (Plymouth), electrical correlates of spatial activity (UWE). arXiv
   full-text census this session: **zero hits for "fungal reservoir computing"; zero abstracts
   pairing "reservoir computing" with Physarum/slime-mold terms.** One 2025 modeling paper
   (arXiv:2505.02114) is simulation-only.
6. **[V] Theory, 2024–25:** unified fading-memory/echo-state view (arXiv:2508.19145, 2025);
   Sugiura et al. 2024 (fading memory nonessential for universal approximation); Pieters
   et al. 2022 (plants-as-RC: fading memory in living systems lacks formal proof).
7. **[F] Adamatzky lab instrumentation specifics** (sub-dermal stainless/iridium-coated
   needle electrodes in differential pairs ~5–10 mm apart, mV-scale spikes 0.05–1.8 mV
   Physarum / larger fungal spikes, 1–10 Hz sampling, spike extraction by first-derivative
   threshold): consistent across search summaries but full texts are bot-blocked —
   **verify against PDFs before the electrodes are ordered.** The minimal rig below does not
   depend on the [F] details.

**The gap the red-team demanded, verified open:** living fungal substrate has NO published
echo-state / fading-memory *characterization* — only memristance (LaRocco), spike statistics
(Adamatzky), and non-living infused-chip RC (Telhan). Stage 1 below aims at that gap with
Telhan's own MC methodology so results are directly comparable.

## BOM — cube01 (street prices, 2026-09-16; [V] = price range verified by search today)

| # | Item | Spec | Street | Notes |
|---|------|------|--------|-------|
| 1 | ESP32-WROOM-32 dev board ×1 | 3.3 V logic, USB serial, 12-bit SAR ADC (too noisy alone → #2) | $9 [V: $5–13] | 3-pack $18.04 ≈ $6/ea; drive stimulus GPIO + log |
| 2 | ADS1115 16-bit I²C ADC ×2 | differential, PGA ×16 (±0.256 V), 8–16 SPS, I²C | $12 [V: $5–12 ea] | 2 differential channels; ESP32 SAR ADC kept as spare |
| 3 | Ag/AgCl disposable ECG electrodes + snap leads, 50-pk | pregelled, non-invasive into substrate/fruit bodies | $13 [V: $8–20] | cheaper + less invasive than needle electrodes; 50 pads = months of re-seating |
| 4 | Oyster (Pleurotus ostreatus) spawn | liquid culture syringe $10 (budget) or grain spawn bag $14 | $14 | LC + self-sterilized straw is the $10 floor variant |
| 5 | Containers ×4, 32 oz deli cups w/ lids + polyfill + micropore tape | 1 control (dead) + 3 live triplicate | $6 | gas-exchange via polyfill plug |
| 6 | Breadboard, hookup wire, alligator clips, bias resistors (1 MΩ ref, 100 kΩ) | + 1× bright LED (optical stimulus, in-lid) | $8 | LED ~$2 of this |
| 7 | Stainless skewers/pins (rigid substrate electrodes, Adamatzky-style alt.) | from kitchen stock | $0–4 | skip if ECG pads suffice |
| | **TOTAL** | | **≈ $55** (floor $43, redundancy-max $68) | |

**Spend phasing:** stage 0 is electronics-only ≈ **$31** (items 1,2,3,5,6) — no biology at
risk during rig bring-up. Stage 1 adds spawn ≈ **$24** (items 4,5 triplicate). Redundancy-max
adds a spare ADC + microSD logging (+$13) — microSD optional; USB serial logging is the $0
default. DHT22 temp/RH (+$4) is a stretch item, not required (status rows may be manual).
Fits the Hermes red-team's "$50–$200 budget" envelope with the ~$50-class claim honest at
floor ($43) and planned ($55).

## Pre-registered test ladder (registration binds BEFORE each stage's data closes)

Iron rule: analysis code is committed (hash into a trail row) before the stage's data is
touched for inference. Thresholds below are the registration. No re-tuning-and-rerunning a
failed stage on the same data; a v2 cube attempt = new registration, new receipt.

### Stage 0 — instrumentation sanity (electronics only, ~1 week, ≈$31)
Setup: shorted-input phantom (electrodes clipped together) + sterile dead-substrate control
cube (no spawn) instrumented identically. Log 72 h continuous at 1 Hz, 2 differential channels.
Proceed criteria (ALL must pass):
- S0.1 Noise floor: shorted-input RMS < 1 mV; electrodes-in-dead-substrate RMS < 2 mV
  (electrode half-cell noise dominates; canon fungal spikes are mV-scale [F], so anything
  ≥5 mV signal stands 2.5x+ above floor).
- S0.2 Drift: baseline drift < 1 mV/h after 45-min warmup (Telhan's infused rig measured
  ~10⁻⁶ V/s; we allow 1000x more because ours is $25 of electronics).
- S0.3 Clock: timestamps monotonic, gap fraction < 1%, all gaps logged as explicit gap rows
  (never backfilled).
- S0.4 Stimulus artifact: GPIO/LED stimulus event visible on the record channel with
  measured cross-talk amplitude, documented, subtractable.
Kill = rig-kill, not claim-kill: any failure → fix electronics, re-run stage 0. Max 2 rig
iterations before re-scope (if 3 iterations fail, the ~$55 rig idea itself is dead: file it).
**Output: the stage-0 noise dataset — this is the baseline that makes stage 2 non-vacuous.**

### Stage 1 — fading-memory / echo-state characterization (weeks 2–6 post-inoculation)
The red-team's precondition: characterize memory FIRST, no task claims before this passes.
Setup: cube driven by a **PRBS-7 (127-bit) pulse train via the in-lid LED** (optical
stimulation is canon-adjacent and non-invasive): pulse width 300 s, so one full sequence
≈ 10.6 h; **3 repeats × 2 seeds**, 1 Hz sampling. Voltage/electrical drive reserved as a
secondary modality only if LED drive provably evokes nothing (registered fallback, not a
free retry).
Analysis (code committed first; same MC methodology as Telhan for comparability):
- S1.1 Stimulus-evoked response exists: Mann-Whitney U on stimulus-on vs stimulus-off
  window amplitudes, α=0.05, AND evoked amplitude > 3× stage-0 substrate RMS.
- S1.2 Linear memory capacity MC(k), lags k=1..180 samples (3-min lookback primary,
  30-min exploratory secondary): ridge-regression prediction of input(k ago) from current
  state features [v, v², |filtered derivative|]; 70/30 time-blocked train/test split.
- S1.3 Fading-memory signature: MC(k) significantly > 0 at some k (permutation test vs
  100 input-shuffled surrogates, p<0.05) AND decays with lag (MC(1) > MC(k_max)).
- S1.4 Echo-state sanity: state variance across the 2 seeds differs (state is input-dependent,
  not a free-running oscillator) AND no electrode-polarization runaway (low-frequency drift
  within S0.2 bound during drive).
Proceed = S1.1 + (S1.3 or S1.4 with S1.2 MC_peak > 0.05 — Telhan's chips scored
0.048–0.209, so < 0.05 is "worse than a chip that barely works").
**Kill criteria (claim-kill, honest death of the reservoir wording):**
- K1: S1.1 fails after max 3 cube restarts (contamination restarts don't count as K1 deaths
  but are logged; restarts capped at 3 total) → substrate not drivable by this rig → retreat.
- K2: S1.3 fails — no significant lag-carried information → **the reservoir claim dies at
  stage 1**, which is the red-team's predicted grave and a legitimate outcome; the cube is
  then a sensor/altar (below) and stage 2 never runs.

### Stage 2 — binary discrimination vs noise baseline (pre-registered n=100, α=0.05)
Task (trivial by design, per pack §4.3): discriminate stimulus pattern **A** (LED train,
2 Hz for 60 s) from **B** (sham: marker-only, LED off). Trial = 30-min post-event window,
1 Hz, features pre-registered: [mean, std, slope, spike-count > 3×stage-0-σ, spectral
centroid]. **n=100 trials total, balanced 50/50, order via seeded RNG (seed recorded in
trail BEFORE first trial)**; readout = logistic regression, train on 40, evaluate on 60
held-out.
**THE BASELINE LAW (the "beats chance" repair):** pass requires beating BOTH baselines —
- (i) shuffled-label readout on the same live data (kills training artifacts);
- (ii) the **stage-0 dead-substrate control driven by the identical stimulus schedule
  through the identical electronics** (kills "any old matter responds" / electronics ghost).
Pass criterion: held-out accuracy > max(both baselines) AND exact binomial one-sided
p < 0.025 vs 50% on n=60 (Bonferroni ×2) → numerically ≥ 39/60 = 65%.
Kill criterion: 95% CI on held-out accuracy includes the baseline level → **the pack §4.3
retreat fires: wording downgrades "physical lens for compute" → "physical altar"** —
pre-registered as FINAL for cube v1 regardless of how close it was.
Ceiling on success (also pre-registered): a pass does NOT certify "compute substrate."
Per DAD discipline it certifies "living substrate with task-relevant state," qualifying the
cube for a stage-3 NARMA-10 replication against Telhan's published numbers — a new
registration, not a claim.

### The honest retreat path (written here so it cannot be lost)
At any kill: this repo's first physical-sensor trail still stands (stage-0 noise dataset +
instrumentation lessons, ≈$31 sunk, electronics reusable). The pack §4.3 sentence holds
verbatim: *the wording retreats from "physical lens for compute" to "physical altar" — an
honest downgrade, and the cube still teaches instrumentation.* The dozen-cubes dream loses
nothing: the north star was always gated on cube one dying or living honestly.

## Integration — sensor logs → append-only trail rows (the same law as everything else)

**Artifact boundary (per AGENTS.md + run_trail.py DNA law):** `memory/runs/cube01/` is the
warm working tape for one goal trajectory (NOT a second DNA throne); durable summaries and
this plan live in `watch/inbox/physical_computing/` (the shared write root). The rig's host
laptop directory is cache only.

**Layout:**
```
memory/runs/cube01/
  trail.jsonl          # hash-chained event rows (schema mag_sensor_event.v1)
  raw/                 # hourly append-only CSV chunks, raw ADC bytes, never edited
  state.json           # cube id, seed registry, stage, registration hashes
```

**Row law = grounding_wave v4 (A2_EPISTEMOLOGY_ENGINE.md) applied to sensor data.** Every
row carries `prev` + canonical-JSON `hash`; versioned key sets with `.get` defaults. Row
kinds: `sample-batch` (60 samples = 1 row/min at 1 Hz — bounded row size per shared-surface
law), `stimulus` (schedule id + seed hash, written BEFORE the first pulse of that schedule),
`gap` (missed samples — declared, never backfilled), `status` (manual temp/condensation/
health notes), `calibration`, `witness`, `contest`, `void`.

**Gates, mapped:**
- **G1 STRUCTURAL** — hash chain recomputes; MALFORMED_ROW / HASH_MISMATCH / PREV_MISMATCH
  refusals apply to sensor rows exactly as to claim rows.
- **G2 BINDING** — every `sample-batch` row records `src_sha256_12` of the raw CSV chunk it
  summarizes; a stranger re-hashes the bytes to confirm. Raw chunks are append-only; any
  post-hoc edit stops corroborating (detectable).
- **G3 WARRANT** — feature/computation rows carry a runnable check:
  `.venv\Scripts\python.exe -m mag.cube01_replay --row <hash>` (exit 0 = features re-derive
  from raw bytes; exit 1 = mismatch). The stage-2 statistical claims additionally carry the
  stage's registered permutation/binomial script as warrant — software never auto-truths;
  CORROBORATED still requires two hands.

**VOID procedure applies to sensor rows (A2, verbatim in spirit):** a flatlined electrode,
clock-skew burst, or seed-drift bug is never deleted — the writer appends a cross-signed
`kind:"void"` row naming the affected batch hashes with `reason_code` ∈ {MALFORMED
(hash/prev defect), EVIDENCE_DEAD (electrode dropout / dead channel), EVIDENCE_MUTATED (raw
chunk hash mismatch), SUPERSEDED (recalibration shifts the baseline)}. Next row re-anchors
to the last non-voided row per the A2 re-anchor rule; `verify` reports LINKAGE over the
physical tape plus the ADMISSION view (analysis runs ONLY on the admission view — readers
quote the admission view, never bare PASS). Mechanical witness: the nightly Ollama janitor
may re-hash chains as ONE mechanical witness per A2 §3; at least one seat/human signature
required for CORROBORATED — the drift patrol is the standing daily reader of cube01's
admission view. Contests (e.g., "was that a real spike or crosstalk?") hold rows CONTESTED
until an outside reader sustains or dismisses.

**Registration binding:** each stage's thresholds above are hashed into a
`kind:"registration"` trail row before that stage's data closes; the analysis script's hash
rides the same row. A stage analyzed under a hash that wasn't registered first is VOID by
construction.

## FINAL REPORT

**Deliverable:** the ONE instrumented mycelium cube plan (cube01), above — science base
with verified/flagged source tiers, ≈$55 phased BOM, three-stage pre-registered ladder
with per-stage kill criteria, and trail integration under the A2 row law (VOID procedure
explicitly extended to sensor rows). This receipt is the durable artifact; the plan is a

## CONCERT 001 AMENDMENTS — folded into the plan bytes 2026-09-16 (R3 gap finding: prose revisions now carried by the plan itself)

1. **Dead twin promoted to concurrent Stage-0 instrument.** Not a later control: a spare
   ADS1115 channel runs the killed-substrate twin simultaneously from first power-up,
   pre-registered — living capacity must beat the MATCHED twin, not a historical memory.
2. **SHT31 temp/RH sensor promoted to Stage-1 required**, with a nuisance-regressor confound
   check (LED heat → evaporation → drift can produce a passing-looking capacity curve —
   the "wet cardboard" kill).
3. **Rung 2 re-scoped (8/9 concert hands):** printed two-species lattice → GROWN
   barrage-zone boundary with optically-tracked, adaptive electrode placement. Printed
   boundaries are predicted to fail first; the zone line grows where the electrodes go.
PROPOSAL until two eyes sign it and the operator funds stage 0.

**Headline findings:**
1. **The red-team's premise is verified open:** no published echo-state/fading-memory
   characterization of a LIVING fungal substrate exists (2024–26 theory exists; experiments
   show memristance and spikes only). Stage 1 aims at a real gap, using Telhan's own
   memory-capacity methodology so results compare directly against their chips
   (MC 0.048–0.209).
2. **Closest prior art is Ecovative's DARPA-funded non-living infused mycelium chips**
   (Sci Rep 2026, code public, MIT license) — reusable as analysis-code reference; their
   4x device-to-device MC spread is the strongest argument for the per-cube noise baseline.
3. **The "beats chance" repair is structural, not cosmetic:** stage 2 requires beating TWO
   baselines (shuffled labels + dead-substrate control through identical electronics), n=100,
   α=0.025 Bonferroni — and a failure is pre-registered as final for cube v1 with the pack
   §4.3 "physical altar" retreat firing automatically.
4. **Retraction hazard filed:** one Adamatzky-line paper ("Fungal sensing skin," 2021) is
   retracted; the canon row is flagged so nobody cites it as support.
5. **arXiv census:** zero "fungal reservoir computing" full-text hits — the trained-readout
   claim has almost no canon to hide behind, which is exactly why the ladder is staged.

**Falsifier of this plan itself:** if stage 0 cannot hold S0.1–S0.4 across 2 rig iterations,
the ~$55 rig idea is dead — file "cube instrumentation exceeds hobby budget" and the pack's
mycelium row retreats to simulation + Telhan citation, honestly.

**BOM TOTAL: ≈$55 planned** (floor variant $43 without redundancy; $68 with spare ADC +
microSD). Stage 0 (electronics-only) costs ≈$31; spawn ($24) enters at stage 1 after the
rig proves sane.

**STAGE-0 START DATE PROPOSAL: Monday 2026-09-22** (parts lead time 2–5 days from today's
order; stage 0 needs only electronics — dead-substrate control, no spawn at risk). Fallback
if shipping slips: **2026-09-29**. Post-approval schedule: stage 0 = one week; inoculation
upon spawn receipt (~week of 09-29); stage 1 window October (2–4 wk colonization + 3×10.6 h
PRBS repeats ×2 seeds ≈ 3 calendar days of logging); stage 2 window November (100 trials ×
30 min ≈ 50 h spread over ~2 weeks). Requires: operator word on ≈$31 now (+$24 at stage 1),
and `mag.cube01_replay` (a ~100-line stdlib script, spec in Integration above) — buildable
in one session before stage 0 starts.
