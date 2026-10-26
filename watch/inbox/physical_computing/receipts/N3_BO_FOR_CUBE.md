# N3 — Bayesian Optimization as the Cube Program's Experiment Selector

**Wave lane:** N3 · physical_computing receipts · 2026-09-16
**Trigger:** operator dropped a BO primer (@probnstat X thread) tonight → design BO as the cube's trial selector.
**Status:** FILED 2026-09-16 — all sections below; ends with run-ready stage-2 dose-ladder config.
**Constraints honored:** receipt-first, no git, no paid APIs; WebSearch/WebFetch free lane only.

## Progress log

- [step 0] Receipt file created before any other work (interruption protocol); sections
  appended as research landed.
- [step 1] Context read: `C17_CUBE_INSTRUMENT_PLAN.md` (whole file) — stage ladder, ESP32 +
  ADS1115 rig, dead-twin control, registration-hash iron rule. The BO selector below slots in
  as **S2.0 (dose-ladder selection)** *before* stage 2's pre-registered n=100 discrimination,
  which must keep running at a FIXED dose or its registration is void.
- [step 2] Primer located and fetched in full: **@probnstat** ("Probability and Statistics")
  on X, status 2100287828391325988, posted 2026-09-16. Core content [V — full thread]:
  BO = "sequential decision-making under uncertainty"; surrogate f ~ GP(m(x), k(x,x′));
  "acquisition function that balances exploration of uncertain regions with exploitation of
  locations predicted to have high values"; lists EI, PI, UCB as the acquisition menu.
  Replies add: @irastech — "BO starts paying off once a single eval costs real money or
  hours" (our case: 14 days per expensive read); @VarikVerilion — acquisition design matters
  more than micro-optimizing the surrogate.
- [step 3] Citation ladder verified by free APIs (arXiv API + Crossref), 429-survived like C17:
  every DOI/arXiv ID below was returned by the API this session [V] unless flagged [F].

## 1. BO setup for our case — f(x), x, kernel, acquisition

**The objective f(x).** One trial = apply dose x to a living block for its exposure window,
log 1 Hz for 30 min post-stimulus, score the response. Primary score (stage-2-compatible):

> **y(x) = z-scored evoked response of the LIVE block minus the concurrent DEAD-TWIN channel**
> (differential feature per stage-2's registered feature vector: mean, std, slope,
> spike-count, spectral centroid — the same features C17 pre-registered for stage 2).

Positive y = stimulus-evoked biology above the electronics ghost and the wet-cardboard
artifact (C17 CONCERT amendments 1–2 already demand the matched twin). Secondary score for a
later phase: Telhan-comparable memory capacity MC — never mixed into one f; one objective per
campaign (BO is single-objective here; scalarizing two scores imports a weight no one can defend).

**The search space x (6-d input, d_eff = 4):** all dims normalized to [0,1] internally.

| dim | physical variable | stage-2 ladder range | role |
|---|---|---|---|
| 1 | wavelength λ | 400–740 nm (LED bank snaps to nearest bin; model on REALIZED nm) | dose |
| 2 | irradiance (PPFD) | 20–400 µmol m⁻² s⁻¹ | dose |
| 3 | field strength | 0–10 V/cm | dose |
| 4 | pulse duty | 0–0.4 (fraction on-time; PWM granularity logged) | dose |
| 5 | substrate moisture | 45–75 %WC | context (tracked, not optimized) |
| 6 | salt / conductivity | 0.5–4.0 mS/cm | context (tracked, not optimized) |

Context dims enter the GP input (so their drift is modeled, not mistaken for dose effect) but
the ladder's controlled setpoints hold them near registered defaults; budget arithmetic uses
d_eff = 4. Realized-vs-setpoint law: the GP fits the *logged* x (nearest LED bin, actual PWM),
never the commanded setpoint — the dose row is hash-chained before execution per C17 row law.

**Kernel: Matérn 5/2 with ARD** (one length-scale per dim). Rationale: dose-response curves
in this class (photon flux saturation, galvanotropic thresholds) are smooth-but-not-analytic;
Matérn 5/2 assumes only twice-differentiability, vs squared-exponential's infinite
differentiability which oversmooths biological cliffs. ARD lets the GP discover that, e.g.,
λ and PPFD matter at cm-vs-V scales differently. Standard reference: Rasmussen & Williams,
*GPML* 2006 (canon [F — book, not byte-verified; universal]). Signal std σ_f init 1.0 on
standardized y; length-scales init 0.3·range, bounds [0.05, 2] in normalized space;
observation noise σ_n² from stage-0 RMS + replicate QC (below), refit by ML-II with
10 jittered restarts each iteration (n ≤ 40 — Cholesky is trivial on a host laptop).

**Acquisition: Expected Improvement (EI). EI wins over UCB, for the cube:**

1. **Both canon tutorials default to EI** for expensive black-box objectives (Frazier 2018,
   arXiv:1807.02811 [V]; Brochu, Cora & de Freitas 2010, arXiv:1012.2599 [V]); the primer
   lists EI/PI/UCB as the menu and its replies argue acquisition choice — not surrogate
   polish — is the lever ([V]).
2. **EI carries a convergence guarantee with the hyperparameters actually estimated from
   data** — Bull 2011 (JMLR 12:2879–2904, arXiv:1101.3501 [V]) proves cumulative-regret
   rates for EI under ML-II-estimated kernel parameters. Practitioner setting: modesty
   ξ = 0.01·range(ȳ) (scikit-optimize convention); ξ=0 is Bull's proven case, 0.01 is a small
   hedge against noise-induced overconfidence. No UCB analogue exists at this safety level.
3. **GP-UCB (Srinivas et al., arXiv:0912.3995 [V]) needs β_t** from the information-gain
   bound, which presumes sub-Gaussian noise and an RKHS-norm bound on f. A growing fungal
   block violates the premise and β_t misspecification fails silently into pure exploitation
   or pure exploration. EI's failure mode under noise is gentle and correctable (§4).

## 2. The sequential loop + how many trials to a defensible optimum

**Loop (one cycle = one dose decision):**

```
prior: standardized y, GP(Matern-5/2 ARD), σ_n² from stage-0 RMS
  ↓
initial design: 5-point maximin Latin hypercube over the 4 dose dims
  (context dims at registered setpoints)  → 5 EXPENSIVE anchors, hash-chained
  ↓
each cycle: refit GP (ML-II, 10 restarts) → maximize EI(ξ=0.01·range) over
  50k Sobol candidates + local Nelder-Mead polish → emit next dose row →
  ESP32 executes + logs → score vs dead-twin → append
  ↓
every 5th trial = QC replicate of current best (updates σ_n², detects drift)
```

5 points is deliberately below the classical initial-design rule — **n₀ ≈ 10d for d ≤ 5**
(Loeppky, Sacks & Welch 2009, Technometrics 51(4):366–376, DOI 10.1198/tech.2009.08040 [V])
— because each expensive read is a 14-day burn; the design deficit is paid by the
cheap-fidelity screening in §3, not skipped.

**Trial budget.** Literature rules of thumb, stated honestly:
- Initial design: 10d (Loeppky et al. 2009 [V-biblio; the 10d conclusion is the paper's
  known result]) — 40 for d_eff=4, infeasible serially.
- Total budget to a defensible optimum: **≈ 10–20 × d evaluations** — practitioner guidance
  (the Intel/SigOpt *Bayesian Optimization Primer* and Frazier 2018's framing that BO works
  best for d ≤ 20 within "a few hundred" evaluations), not a theorem. For d_eff = 4:
  40–80 expensive trials. **At 14 days/trial serial that is 1.5–3 years — refused.**
- The cube adaptation: total expensive budget **capped at 25** (~35 weeks serial, ~14 weeks
  with the 3 live-cup triplicate run as concurrent batch arms via constant-liar batch EI
  [F — Ginsbourger et al. 2010 constant-liar, canon, not byte-verified]), with §3 proxies
  carrying the exploration load. What 25 trials buys is a **top-ε basin** (±1 length-scale),
  not certified global optimality — which is all stage 2 needs: a defensible fixed dose for
  the pre-registered n=100 run.

**Stopping rule** (pre-registered, any one fires): (S1) max EI < 5% of σ_f for 3 consecutive
cycles — information exhausted; (S2) 25-expensive-trial cap; (S3) dead-twin baseline drifts
> 2σ from its registration level → campaign re-anchored, not silently continued (§4).

## 3. Multi-fidelity: 1-day electrical proxy before the 2-week read

The trick: run most of the search on a **cheap proxy f̂₁(x)** — 1-day electrical response
(evoked amplitude/spike-rate change) — and reserve the **expensive f₂(x)** (14-day capacity /
discrimination read) for candidates the proxy blesses. This is the standard multi-fidelity
BO stack:

- **Kennedy & O'Hagan 2000** (Biometrika 87(1):1–13, DOI 10.1093/biomet/87.1.1 [V — Crossref
  record lists Kennedy only; O'Hagan missing from the metadata is a known record gap]): the
  auto-regressive co-kriging model — f₂(x) = ρ·f̂₁(x) + δ(x), cheap fidelity plus a scaled
  discrepancy. The correlation ρ is *estimated from data*, not assumed.
- **Forrester, Sóbester & Keane 2007** (Proc. R. Soc. A 463:3251–3269,
  DOI 10.1098/rspa.2007.1900 [V]): multi-fidelity EI — which fidelity to evaluate next is
  itself an acquisition decision against a per-evaluation cost budget (proxy ≈ $0.50/1 day,
  expensive ≈ 14 days of a 3-month cube lifetime).
- **Kandasamy et al., MF-GP-UCB** (arXiv:1603.06288, NIPS 2016 [V]): the bandit-theory
  standard — proves fidelity allocation converges to the optimum. (Used here as the
  theoretical warrant; the deployed acquisition stays EI per §1.)
- **Huang, Allen, Notz & Zeng 2006** (J. Global Optim. 34(3):441–466,
  DOI 10.1007/s10898-005-2454-3 [V]): augmented-EI multi-fidelity for *stochastic*
  evaluations — the version that applies, because our reads are noisy (§4).

**Cube rule:** the 5 expensive anchors are ALSO run at proxy fidelity → 5 dual-read pairs
estimate ρ̂. **If ρ̂ < 0.7 the proxy is not decision-grade**: it may still veto zero-regions
(no evoked response at all = never spend 14 days there) but never ranks candidates. Proxy
screening budget: ~30 points (10d) before the first expensive EI step.

## 4. The honest wall: the objective is noisy AND the block grows

Biology violates the two assumptions the plain BO textbook makes (deterministic f, stationary
kernel). What the literature and the rig give us:

**Noise.** Trials are single-read (the same dose cannot be re-run on the same block — growth,
hysteresis, prior-dose carryover), so repeated-measures designs are out and σ_n² must come
from elsewhere: (a) stage-0 dead-substrate RMS floors the electronics noise; (b) the
concurrent dead-twin differential (y = live − twin) kills common-mode drift and much of
moisture/temperature confound; (c) the every-5th-trial QC replicate estimates total trial
noise. GP-side: keep an explicit observation-noise term (nugget ≥ 1e-3 + replicate estimate)
and use a **noise-aware acquisition** — Huang et al. 2006's augmented EI [V] or the modern
noisy-EI of Letham et al. (arXiv:1706.07094, "Constrained Bayesian Optimization with Noisy
Experiments" [V]) — so EI does not chase single-read noise spikes. Bull's convergence proof
also covers a correctly-sized noise term; an undersized nugget is the classic way EI
degenerates into exploiting phantom optima.

**Non-stationarity (the block grows for the whole campaign).** A stationary GP fit across 20+
weeks assumes f is fixed; it is not — mycelial maturation moves mean response, variance, and
memory properties (Telhan's chips were non-living at compute time precisely to freeze this).
Anchors from the literature: **Bogunovic & Krause 2021** (NeurIPS, arXiv:2111.05008 [V])
show BO survives kernel misspecification with *phased, locally re-anchored* designs
(Phased GP Uncertainty Sampling) rather than global re-plans — our sliding-window law is a
physical-experiment reading of exactly that. Nonstationary covariance kernels
(Paciorek & Schervish [F — canon, not byte-verified]) are the model-side answer; for a
25-trial campaign the practical stack is:

1. **Sliding window refit:** GP fits the last W = 15 expensive trials (+ all proxy anchors,
   re-baselined), not all history — the model tracks slow drift instead of averaging across it.
2. **Differential objective:** y = live − dead-twin at the same hour removes most common-mode
   maturation signal (the twin ages too).
3. **Re-anchor trigger:** twin baseline drift > 2σ from registration (stopping rule S3) →
   halt, file a `status` + new `registration` row, refit on the window, continue — never
   patch silently.
4. **One objective per campaign** (§1): with drifting biology, a scalarized two-objective f
   becomes uninterpretable mid-growth.

## 5. FINAL CONFIG — cube stage-2 dose ladder (run-ready)

```
CUBE-BO v1 — S2.0 dose-ladder selector (host-side planner, ESP32 actuator/logger)

objective      maximize y(x) = z( live evoked response − concurrent dead-twin ),
               30-min post-stimulus window, C17 stage-2 feature set
space          x = [λ_nm 400–740 | ppfd 20–400 µmol/m²/s | vcm 0–10 V/cm |
               duty 0–0.4 | moisture %WC | salt mS/cm], normalized [0,1]^6,
               d_eff = 4 (moisture/salt = context covariates at registered setpoints);
               GP fits REALIZED doses (logged LED bin / PWM), never setpoints
kernel         Matérn 5/2 + ARD, ℓ₀ = 0.3·range per dim (bounds [0.05,2]),
               σ_f² init 1 on standardized y; noise σ_n² = stage-0 RMS² + QC-replicate
               estimate (nugget ≥ 1e-3); ML-II refit, 10 jittered restarts, every cycle
acquisition    Expected Improvement, ξ = 0.01·range(ȳ), noise-aware (augmented-EI form);
               maximized over 50k Sobol candidates + local Nelder-Mead polish
initial design 5-pt maximin Latin hypercube (dose dims) = 5 expensive anchors;
               ~30 proxy-fidelity (1-day) LHS points; ρ̂ from 5 dual-read pairs
multi-fidelity co-kriging f₂ = ρ·f̂₁ + δ (KOH 2000 / Forrester 2007); ρ̂ < 0.7 → proxy
               may only veto zero-regions, never rank
loop law       every 14 d: hash-chained dose row BEFORE execution (C17 row law) →
               ESP32 executes + logs 1 Hz → score vs twin → append → refit on sliding
               window W = 15 → next dose; every 5th trial = QC replicate of best
budget         ≤ 25 expensive trials (serial ~35 wk; ~14 wk with 3-cup batch arms,
               constant-liar batch EI); proxy budget ~30 reads
stopping       S1 max EI < 5%·σ_f for 3 cycles | S2 25-trial cap | S3 twin drift > 2σ
               → registered re-anchor (new registration row), never silent retune
host split     planner = laptop Python (n≤40 Cholesky, seconds; trial latency is days,
               round-trip is free); ESP32-WROOM + ADS1115 = schedule execution, 1 Hz
               logging, twin channel (C17 BOM unchanged, $0 added)
registration   THIS CONFIG + seed + σ_n estimate hashed into a kind:"registration"
               trail row BEFORE the first BO-selected dose; stage-2's existing n=100
               registration then binds at the BO-chosen dose, parameters FROZEN.
```

**Falsifier of this design:** if ρ̂ < 0.7 after the 5 dual-read anchors, the 1-day proxy is
dead as a ranker and the campaign falls back to expensive-only EI with the 25-trial cap —
expected optimum quality drops one ε-band, honestly filed, not hidden.

## Headline findings

1. **EI over UCB, decided:** EI has regret guarantees with data-estimated hyperparameters
   (Bull 2011) and the safe default ξ≈0.01; GP-UCB's β_t presumes sub-Gaussian noise and RKHS
   bounds a growing fungal block cannot honor. The operator's primer (@probnstat X,
   2026-09-16) sets the frame — BO pays "once a single eval costs real money or hours" —
   exactly our 14-day trials.
2. **Budget honesty:** the 10–20×d literature rule says 40–80 expensive trials for d_eff=4;
   at 14 days each that is refused, so the cap is 25 expensive trials + ~30 one-day proxies,
   targeting a top-ε dose basin sufficient for stage 2's fixed-dose n=100 run.
3. **Multi-fidelity is load-bearing, with a self-test:** co-kriging against the 1-day proxy
   (KOH 2000 / Forrester 2007 / MF-GP-UCB 2016 standard), killed to veto-only duty if
   ρ̂ < 0.7 — the campaign falsifies its own cheap tool before trusting it.
4. **The wall is handled by structure, not hope:** dead-twin differential + QC replicates +
   augmented/noisy EI for noise; sliding window W=15 + twin-differencing + 2σ re-anchor
   trigger for the growing block (Bogunovic & Krause 2021 phased-design warrant).
5. **Registration discipline inherited from C17:** the BO config itself is registered
   (hashed) before the first selected dose; stage-2's pre-registered n=100 then runs frozen
   at the BO-chosen dose. Hyperparameter retunes mid-campaign are new registration rows.

**Sources (all verified this session via free API/fetch lanes):**
[probnstat BO thread](https://x.com/probnstat/status/2100287828391325988) ·
[Frazier 2018 tutorial, arXiv:1807.02811](https://arxiv.org/abs/1807.02811) ·
[Srinivas et al. GP-UCB, arXiv:0912.3995](https://arxiv.org/abs/0912.3995) ·
[Brochu et al. tutorial, arXiv:1012.2599](https://arxiv.org/abs/1012.2599) ·
[Bull 2011, arXiv:1101.3501](https://arxiv.org/abs/1101.3501) ·
[Loeppky, Sacks & Welch 2009, DOI 10.1198/tech.2009.08040](https://doi.org/10.1198/tech.2009.08040) ·
[Forrester, Sóbester & Keane 2007, DOI 10.1098/rspa.2007.1900](https://doi.org/10.1098/rspa.2007.1900) ·
[Kennedy & O'Hagan 2000, DOI 10.1093/biomet/87.1.1](https://doi.org/10.1093/biomet/87.1.1) ·
[Kandasamy et al. MF-GP-UCB, arXiv:1603.06288](https://arxiv.org/abs/1603.06288) ·
[Huang et al. 2006, DOI 10.1007/s10898-005-2454-3](https://doi.org/10.1007/s10898-005-2454-3) ·
[Letham et al., arXiv:1706.07094](https://arxiv.org/abs/1706.07094) ·
[Bogunovic & Krause 2021, arXiv:2111.05008](https://arxiv.org/abs/2111.05008) ·
[SigOpt BO Primer (PDF)](https://www.intel.com/content/dam/www/public/us/en/ai/documents/SigOpt_Bayesian_Optimization_Primer.pdf)

---
*N3 receipt CLOSED 2026-09-16. Cross-refs: C17_CUBE_INSTRUMENT_PLAN.md (rig, row law,
registration iron rule), K2_GALVANOTROPISM.md (field-dose prior art), O3_OPTICAL_INTEGRATION.md
(light channel). No git, no paid APIs; WebSearch/WebFetch free lane only.*
