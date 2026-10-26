# C15 Lane 1 — VENDOR CSV ESS AUDIT (zero training, zero GPU) — receipt

Lane: physical_computing / C15 `C15_EXTROPIC_REPLICATION_DESIGN.md` Lane 1 (GO'd 2026-09-16).
Claim under test: arXiv 2510.23972 / npj Unconventional Computing — DTM (denoising
thermodynamic model) on MNIST/Fashion-MNIST reaches "performance parity with GPUs ...
approximately 10,000 times less energy." Lane 1 audits the co-author research repo's OWN
published figure CSVs (`pschilliOrange/dtm-replication`, `figures/**.csv`: FID +
autocorrelation logs) for effective-sample-size honesty: their autocorrelation →
ESS per raw sample → implied ESS/Joule vs (a) the 10,000× energy claim and (b) the salon
Landauer ceiling ≈ 1.05e13 samples/J (receipt `SALON_FREE_20260916.md`; C15 flagged the
vendor-implied 7.7e13 samples/J sits ~7× ABOVE it — step 0 re-derives the ceiling from
k·T·ln2 at 300 K and names the assumption that drives the gap).
Method: read-only `git clone` (a download, not a repo write) to %TEMP% — pre-flight showed
`artifacts/` is NOT gitignored, so the repo tree must not hold the clone. stdlib + numpy
(venv 2.4.6). No paid APIs, no repo git operations. Append-as-you-go.

## Progress log

- [t0] Receipt created before work. Pre-flight: `git check-ignore -v artifacts/` → NOT
  ignored ⇒ clone target = %TEMP%\dtm-replication. venv numpy present (2.4.6). Context
  loaded: C15 design receipt (pre-registered thresholds incl. KILL-2: ESS/raw-sample
  < 0.01 ⇒ >100× inflation), SALON_ESS_20260916, X_MINE_PHYSICAL_20260916.

- [t1] CLONED `pschilliOrange/dtm-replication` (shallow, read-only) to `%TEMP%\dtm-replication`
  — 218 files, no LICENSE (run, don't redistribute — C15 §1.6). Inventory: 44 figure CSVs in
  3 folders (`MEBM_DTM_ACP_ablation` 3 = Fig 5b; `degree_ablation` 24 = Fig 5c upper;
  `chain_depth_ablation` 17 = Fig 5c lower), + 1 example training log (Fashion-MNIST,
  grayscale-7, preset 8048) + training/eval code. NO LICENSE file. Clone kept for Lane 2.

## §1 What the CSVs actually contain (method reconstructed from code)

- Each CSV: `epoch, autocorr_step_0..k, free_fid, clamped_fid` — one scalar autocorrelation
  PER diffusion step PER epoch. NOT full ACF curves; full lag curves exist only as
  `autocorrelation_vs_lags/` PNGs in un-shipped run folders. CSVs only ship the scalar.
- Scalar = `max(0, mean(ACF over last 1/16 of lags))` (`step.py:445`) — a TAIL ACF at large
  separation, i.e. residual correlation after the chain has run. This is their mixing-time
  proxy and it is exactly what the paper's energy model needs ("Mixing times were computed
  by fitting an exponential function to the large-lag behavior of the autocorrelation
  function", arXiv 2510.23972).
- Measurement protocol (`DTM.compute_autocorr`): 512 chains (32 reps × 16 chains, n_cores 2),
  states recorded every 4 Gibbs sweeps after warmup, projected to 32 latent dims. Window per
  folder: Fig 5b/degree = 800 rec (sep up to 1600 sweeps, tail mean at sep ≈ 1554);
  chain-depth W = 2W rec (sep up to 3200–4800).
- Per-lag noise floor ≈ 1/√512 ≈ 0.04 before dim-averaging → tail values ≥ 0.01 are
  meaningful, all DTM-family tails in the CSVs qualify as measured ("fit"), none are
  floor-censored except exact zeros early in training.
- ESS estimator (ours, from their scalar): exponential tail-fit τ = sep_mid / ln(1/T); ESS
  per raw sweep = 1/(1+2τ). This mirrors the paper's own large-lag exponential method, so
  the audit is like-for-like. Caveat discovered below: τ_fit is window-dependent → tails
  are heavier than exponential → τ_int (integrated) is likely LARGER than τ_fit.
- Config pinned from the figure scripts: Fig 5b = Fashion-MNIST binarized, side-70 torus
  grid = 4,900 cells (884 visible: 784 px + 100 label), DTM/DTM+ACP 8 diffusion steps,
  MEBM 1 step; degree/depth ablations = 4 steps, grids 44–90.

## §2 The numbers (full 181-row table: `C15_LANE1_ESS_TABLE.csv`, same directory)

### 2.1 FID quality half — best free FID per model (their custom FID metric)

| Model | best free FID (clamped) | @epoch | final free FID | fate |
|---|---|---|---|---|
| MEBM (1-step, no denoise chain) | 37.08 (35.52) | 6/150 | 183.08 | collapses |
| DTM (8 steps, no ACP) | 29.68 (29.08) | **8**/144 | 185.19 | collapses after ep 8 |
| DTM+ACP (8 steps, adaptive corr penalty) | 26.84 (25.82) | 86/149 | 28.96 | stable to 150 |
| best ablation (deg20, grid90, 20 ep) | 22.37 (22.22) | 10/19 | 31.89 | — |
| degree sweep (best per degree) | d8: 60.1 · d12: 29.1 · d16: 24.3 · d20: 22.4 | | | degree ↑ ⇒ FID ↓ |

- Their own script header claims "FIDs well below 30" — CSVs confirm 22–30 at best epochs.
- **Quality half of "parity" is internally supported** on their metric — but ONLY the ACP
  variant is stable; plain DTM's best FID is a 1-epoch window (ep 8) followed by collapse
  to 185. The "GPU-parity" comparison itself is NOT auditable from the CSVs: no GPU
  baseline rows exist in the repo (their Fig 1/5 GPU numbers are not shipped as data).

### 2.2 ESS half — mixing time from their own tail ACFs (best-epoch, worst-step to best-step)

| Model set | τ_fit (sweeps) | ESS/sweep | ESS per 8-sweep record | sweeps per independent sample | vs paper K_mix=250 |
|---|---|---|---|---|---|
| **DTM+ACP Fig 5b (headline)** | **261–373** | 1.3–1.9 ×10⁻³ | 1.1–1.5% | 520–770 | ×1.04–1.5 above |
| DTM no-ACP Fig 5b | 241–673 | 0.7–2.1 ×10⁻³ | 0.6–1.7% | 480–1350 | ×1.0–2.7 |
| MEBM Fig 5b | **4057** | 1.2 ×10⁻⁴ | 0.1% | 8100 | ×16.2 |
| degree ablation (18 runs) | 270–2680 | 1.9e-4–1.8e-3 | 0.15–1.5% | 560–5350 | ×1.1–10.7 |
| chain-depth warm 800 (sep 3104) | 721–3096 | 1.6–6.9 ×10⁻⁴ | 0.13–0.55% | 1450–6190 | ×2.9–12.4 |
| chain-depth warm 1200 (sep 4654) | 926–1716 | 2.9–5.4 ×10⁻⁴ | 0.23–0.43% | 1850–3410 | ×3.7–6.9 |

- **Honesty finding 1 (favors vendor):** their logged tails are NOT floor-censored; the
  mixing measurements are real, and the headline DTM+ACP model's τ (260–373 sweeps) is
  within ×1.5 of the K_mix=250 the energy table assumes. The paper does not pull 250
  from thin air.
- **Honesty finding 2 (against vendor):** τ_fit GROWS with the measurement window
  (same-config family: warm400 τ≈300–2680 @sep1554 → warm800 τ≈720–3100 @sep3104 →
  warm1200 τ≈930–1720 @sep4654). A true exponential would give a window-invariant τ.
  The tails are heavier than exponential ⇒ the exponential tail-fit systematically
  UNDERSTATES the integrated autocorrelation time ⇒ their K_mix=250 is the optimistic
  edge of their own evidence, and the honest ESS discount for typical runs is ×2–6,
  not ×1.
- **Honesty finding 3:** ESS per raw sweep ≈ 10⁻³ ⇒ if anyone counts raw Gibbs sweeps (or
  even 8-sweep records) as "samples", samples-based numbers inflate 500–6000× (or
  60–300× per record). The paper's own energy table does NOT do this — it charges
  K_mix=250 sweeps per sample — but every second-hand citation of "samples/J" without
  the K_mix discount inherits exactly this >100× trap. Pre-registered KILL-2
  ("ESS/raw-sample < 0.01") fires only under the sweep-as-sample reading; under the
  paper's own accounting the inflation is ×1.5–6, not >100.

## §3 Energy arithmetic audit (their model × their data)

Paper model (arXiv 2510.23972): `E = T_steps · K_mix · L² · E_cell`, E_cell ≈ 2 fJ,
K_mix = 250 (DTM), Fig 5b config T=8, L²=4900:

- **E_img = 8 × 250 × 4900 × 2e-15 = 1.96×10⁻⁸ J/image → 5.1×10⁷ raw images/J.**
- Honest ESS/J from their own CSVs: best case (τ=373) **3.4×10⁷ independent images/J**
  (×1.5 penalty); typical ablation (τ≈500–1500) ×2–6 penalty; MEBM (τ=4057) ×16 penalty
  (the paper handles this correctly — it charges MEBM its own measured, much larger,
  mixing time, "several orders of magnitude larger", which our ×16 floor confirms).
- **10,000× check:** implies GPU baseline 1.96×10⁻⁴ J/image ≈ 5.6×10⁸ FLOP/image at H100
  FP16 (~2.9×10¹² FLOP/J) — plausible for a small diffusion model. The ratio is
  arithmetically coherent BUT rests on two unmeasured constants (E_cell = device
  projection; K_mix = at the optimistic edge of their own CSVs) and excludes
  encode/decode/verify (DAD §4.2). A ×1.5–6 K_mix correction does not dent a 10⁴×
  projection; an E_cell correction of ×100 (still only ~7×10⁷ kT·ln2 per update —
  well within real-device reality gaps) eats it entirely. **The 4 orders of magnitude
  live in E_cell, not in the software evidence.**
- Cross-consistency: Z1T's 1.3×10⁻¹⁴ J/pbit-sample ≈ 6.5 cell-updates at 2 fJ — the two
  vendor documents agree with each other within an order of magnitude.

## §4 Step 0 — Landauer ceiling re-derivation from first principles (pre-registered)

- k·T·ln2 at 300 K = 1.380649e-23 × 300 × 0.693147 = **2.871×10⁻²¹ J/bit**.
  Absolute ceiling: **3.48×10²⁰ flips/J**.
- Vendor implied (C15 flag): 1.3×10⁻¹⁴ J/pbit-sample → 7.7×10¹³ samples/J
  = **4.5×10⁶ kT·ln2 per sample** → **4.5×10⁶× headroom below the absolute ceiling**.
  The DTM image rate (5.1×10⁷ images/J) sits 5.6×10⁶× below even the dynamics-minimum
  ceiling below. **No physics violation anywhere.**
- Defensible workload ceilings (independent images/J):
  - Entropy minimum — one 8-level 28×28 image = 784 px × 3 bits = 2,352 irreducible bits
    ⇒ 1.48×10¹⁷ (perfect mixing, zero overhead — unattainable ideal).
  - Dynamics minimum — their own protocol needs K_mix × L² = 250 × 4900 = 1.225×10⁶
    cell-flips per independent sample ⇒ 2.84×10¹⁴.
- **THE SALON NUMBER DOES NOT SURVIVE.** `SALON_FREE_20260916.md` lane lead (cerebras-oss,
  explicitly "LEADS, NOT FACTS"): "ESS/J hard ceiling ≈ 1.05×10¹³ samples/J" implies
  9.5×10⁻¹⁴ J/sample = **3.3×10⁷ Landauer bits/sample** — with no derivation published.
  That is **14,104× stricter than the 2,352-bit entropy minimum** and **27× stricter than
  the 1.225×10⁶-flip dynamics minimum**. The C15 flag "vendor's 7.7×10¹³ sits ~7× ABOVE
  the ceiling ⇒ physically implausible" was an artifact of the unverified lead, not of
  the vendor's arithmetic. **Pre-registered step-0 branch fires: correct the salon
  number** (C15 §2: "if it doesn't survive, we correct the salon number — also a win").
  Correction filed back into the canon: the gap driver is the bits-per-independent-sample
  assumption; any ceiling between 2.8×10¹⁴ (dynamics-min) and 1.5×10¹⁷ (entropy-min)
  independent images/J is defensible; the salon's 1.05×10¹³ is not.

## §5 VERDICT (Lane 1, pre-registered thresholds applied)

**PARTIAL-SUPPORT, OPTIMISTIC-EDGE — the vendor's own CSVs do not contradict the
sampling-efficiency story by orders of magnitude, but they cap it:**

1. **FID parity:** internally supported on their own metric (best 22–30, "well below 30"
   as claimed) — but stability REQUIRES the adaptive correlation penalty (plain DTM
   collapses 29.7 → 185), and the comparison against actual GPU numbers is not in the
   shipped data. UNVERIFIED-BY-THESE-CSVs, not falsified.
2. **Sampling efficiency:** K_mix=250 in the energy table is within ×1.04–1.5 of the
   best model's own measured τ (260–373 sweeps) — honest at the optimistic edge — but
   typical runs sit ×2–6 above it, window-dependence of τ_fit shows the tails are
   heavier than exponential (so the fit flatters them), and ESS/raw-sweep ≈ 10⁻³ means
   any "samples/J" citation without the K_mix discount inflates >100× (KILL-2 condition,
   reading-dependent). The honest headline: **~3–5×10⁷ independent images/J claimed ≈
   ~1–3×10⁷ ESS/J from their own data** — a ×1.5–6 haircut, not a ×100 collapse.
3. **10,000× energy:** arithmetically coherent as a projection; the entire 4 orders of
   magnitude live in the unmeasured E_cell (device physics), while the software-visible
   half (K_mix) is real, logged, and at best marginally favorable to the vendor. The
   "could reach" verb in the abstract is doing load-bearing work — correctly flagged in
   C15 §3.
4. **Ceiling:** KILL-4 (ceiling ⇒ vendor physically implausible) does NOT fire — the
   salon ceiling itself was the error. Struck and replaced (§4).

**The paper's own data is more honest than the rumor of it.** The mixings are measured,
logged per epoch, and consistent with the energy model's one software-side assumption —
at that assumption's optimistic edge, with a fit methodology that flatters it.

## §6 What Lane 2 must measure that CSVs cannot

1. **Full ACF curves** (Geyer initial-positive-sequence τ_int, not tail-fits) — the repo
   ships only the 1/16-tail scalar per epoch; the `autocorrelation_vs_lags/` curves were
   never committed. Heavy-tail suspicion (§2.2 finding 2) is testable only with curves.
2. **τ_mix under the GENERATION protocol** (fresh chain per image vs persistent chains;
   gen warmup 800) — energy per INDEPENDENT image end-to-end, not per CD-training step.
3. **Joules and seconds per Gibbs sweep on our hardware** (THRML/JAX sim, DAD-metered:
   encode → simulate → decode → verify) — turns ESS/sweep × J/sweep into measured ESS/J.
4. **Same-metric GPU/digital baseline** (repo ships precomputed FID stats: `bw/gs`
   MNIST + Fashion-MNIST) — B1 plain-Gibbs and B2 tuned digital sampler close the
   FID-parity gap the CSVs leave open.
5. **ACP necessity and cost** — does stability (no FID collapse) require ACP, and what
   τ penalty does ACP pay for it? The CSVs hint ACP trades a little mixing for a lot of
   stability; only a run can separate them.
6. **Run-to-run variance** — degree-12 vs warmup-400 sets are same-config replicates and
   agree to ~1–4% on FID but diverge on grid90; a real error bar needs seeded repeats.

## Status: CLOSED

- Method: read-only `git clone` to `%TEMP%\dtm-replication` (outside repo tree; repo
  `artifacts/` verified NOT gitignored so kept out), analysis via venv python 2.4.6 numpy
  heredoc (no repo writes), companion table `C15_LANE1_ESS_TABLE.csv` (181 rows) filed in
  this directory. $0; no paid APIs; no repo git operations; no training, no GPU.
- Sources: github.com/pschilliOrange/dtm-replication @ master (cloned 2026-09-16);
  arxiv.org/abs/2510.23972 (+ HTML v2 energy model: E_cell≈2 fJ, K_mix=250,
  exponential-fit mixing); docs/ref/EXTROPIC_Z1T_DIGEST_20260904.md (1.3e-14 J/sample
  provenance); SALON_FREE_20260916.md (ceiling lead, struck per §4).
- Lane 2 may reuse the %TEMP% clone (smoke_testing → reduced config per C15 §4).
