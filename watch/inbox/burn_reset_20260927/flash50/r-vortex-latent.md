# r-vortex-latent: NNs compressing vortex-street flows into ~8-value latent loops

Item: deep-dive on neural nets compressing vortex-street flows into ~8-value latent loops.
Three questions asked: (1) architectures used, (2) cheapness of reproduction, (3) does the
loop structure imply a low-dim attractor coordinate system.

Evidence legend used below, because every claim is graded:
- [FETCHED] = I pulled and read the page/paper text this session (WebFetch or webReader).
- [SEARCH] = surfaced in web-search summaries only, not read in full text.
- [THEORY] = standard textbook mathematics, no fetched source.
- OWED = could not verify this session.

Note on the seed: `watch/inbox/burn_reset_20260927/work/fan_vortex-latent_meta_muse-spark-1.3.md`
(read this session) is a DISPATCH-ERR 403 stub with no content, so the "~8-value" figure in the
item has no prior banked anchor in the repo. The verified cluster below is 2, 9 and 10; no
fetched source uses exactly 8. Exact-8 attribution: OWED.

## 1. Who has done this, and with what

| Work | Flow | Latent size | Dynamics in latent space | Evidence |
|---|---|---|---|---|
| Lusch, Kutz, Brunton, Nature Comms 9:4950 (2018), arXiv:1712.09707 | cylinder wake via the Noack mean-field model (3-state ODE), NOT raw CFD grids | 2 on-attractor (one complex-conjugate eigenfunction pair), 3 off-attractor (pair + one real eigenvalue) | strictly linear; rotation at omega "extremely close to the true constant -1", i.e. the true shedding frequency | [FETCHED] via ar5iv full text |
| Hasegawa, Fukami, Murata, Fukagata, Fluid Dyn. Res. 52(6) 065501 (2020) | 2D circular cylinder, unsteady shedding, several Reynolds numbers (Re = 100-1000 per search summary) | latent dim exists but NOT verified this session | LSTM trained on latent sequence | [SEARCH] (Keio Pure abstract snippet; direct fetch of AIP/Keio/SemanticScholar pages failed or was empty) |
| Racca, Doan, Coletti, Brunton, Ciarella, "Predicting turbulent dynamics with the convolutional autoencoder echo state network", J. Fluid Mech. (2023); preprint arXiv:2211.11379 | 2D Kolmogorov flow, Re = 30 quasiperiodic and Re = 34 turbulent; plus the 3D minimal flow unit. Caution: a search snippet mislabeled this as cylinder wake; the fetched Cambridge page says Kolmogorov flow | latent sizes tested 18, 36, 54, and 9; 9-dim latent captures 99.997% (quasiperiodic) and 99.78% (turbulent) of energy; state space is 4608-dim (48x48x2) for the 2D case | Echo State Network (reservoir, only output matrix trained by ridge regression), run closed-loop, so the whole CAE+ESN is an autonomous dynamical system | [FETCHED] (Cambridge JFM page + arXiv abstract page) |
| Carl et al., "Reduced-Order Modeling of Unsteady Fluid Flow Using Machine Learning", Phys. Fluids (2024), arXiv:2402.05372 | 2D flow over a cylinder between two solid walls, explicitly a von Karman vortex street; input fields 384x128x2 | latent dim 10 for the cylinder case (4 for the lid-driven cavity companion case) | ensemble of 96 bagged bidirectional LSTMs (3 hidden layers x 36 units, dropout 0.15, window 30) to fight autoregressive error compounding | [FETCHED] (arXiv HTML full text) |
| Agostini, Phys. Fluids 32, 067103 (2020) | flow dynamical systems incl. vortex-dominated regimes; AE compresses fields, second network predicts latent evolution | not verified | not verified | [SEARCH] (AIP/HAL snippets) |
| "Data-driven oscillator model for multi-frequency turbulent flows", arXiv:2604.11745 | 3D supersonic turbulent cavity flow; autoencoders extract "representative oscillators" whose dynamics are learned | not stated in abstract | learned oscillator dynamics per latent mode | [FETCHED] abstract; the phrase "oscillatory flows appear as cyclic trajectories" is [SEARCH]-level |

So the honest answer to "~8-value": the published practice for shedding/oscillatory flows
clusters at 2 (Koopman pair), 9 (CAE-ESN), 10 (CAE-eLSTM). "~8" sits inside that band but no
source I could fetch names 8.

## 2. Architectures (the pattern that repeats)

1. Spatial compressor: a convolutional autoencoder (multiscale in Racca: three parallel
   3x3 / 5x5 / 7x7 filter streams, periodic padding to respect boundary conditions, tanh,
   ~200k parameters [FETCHED]; plain conv stacks ending in a 10-dim FC bottleneck in Carl
   [FETCHED]). The AE is what turns 4608- or 98,304-dim fields into single-digit/low-double-digit
   codes.
2. Temporal model on the code: one of three families:
   - LSTM (or bagged bidirectional LSTMs) doing autoregressive next-step prediction (Hasegawa
     [SEARCH], Carl [FETCHED]);
   - Echo State Network run closed-loop, making the full stack an autonomous dynamical system
     (Racca [FETCHED], and the arXiv:2211.11379 abstract says exactly this [FETCHED]);
   - Koopman eigenfunction networks that make the latent dynamics LINEAR (Lusch [FETCHED]).
3. Boundary-condition and physics-aware design details that keep codes faithful: periodic
   padding (Racca [FETCHED]), Re-conditioned training across a parameter sweep (Hasegawa
   [SEARCH]), and the Lusch auxiliary network that outputs eigenvalues as a smooth function of
   the latent radius y1^2+y2^2 so the rotation frequency is continuous in amplitude [FETCHED].

## 3. Cheapness of reproduction

Verified data points:
- Racca's own tutorial version trains in about 15 minutes on a desktop (i7-10700K CPU plus a
  Quadro RTX 4000), and CAE+ESN prediction runs at least 100x faster than solving the equations;
  the arXiv:2211.11379 abstract states the prediction costs less than 1% of the solver's
  computational time. [FETCHED, Cambridge + arXiv]
- Carl et al.'s 2D cylinder data is small by ML standards: 50 designs x 750 snapshots each,
  45/5 train/test; the cost went into 96 bagged LSTMs on an 8x A100 DGX, but inference is 27x
  faster than the CFD (48.4 s vs 1305 s). [FETCHED]
- Lusch's wake example is trivially cheap: it trains on 15,000 on-attractor and 20,000
  off-attractor trajectories of a 3-state ODE. [FETCHED]
- The upstream CFD for 2D shedding is laptop-scale 2D DNS (course-grade reproductions of the
  Hasegawa pipeline exist; the "cae_cylinder" GitHub repo training on Basilisk `ibmcylinder`
  output surfaced in search with batch 512, lr 1e-3/1e-4, but my direct fetch of the repo
  returned 404, so those repo details are [SEARCH]/unverified).

Verdict: this is one of the cheapest real-fluid ML-ROM targets in existence. Everything except
the 3D cases reproduces on a single workstation: hours of CFD, minutes of AE training, a
linear/reservoir layer for the dynamics. The real difficulty is not compute; it is the two
verified failure modes: (a) autoregressive error compounding, which is why Carl et al. bag 96
LSTMs [FETCHED], and (b) finite chaotic predictability, 1.5 to 3 Lyapunov times in Racca's
turbulent case, after which trajectories diverge but statistics still match (Kantorovich metric
up to 3x smaller than the training set's spread) [FETCHED].

## 4. Does the loop imply a low-dim attractor coordinate system?

Short answer: the loop is strong evidence that the flow sits on a low-dimensional attractor and
that the learned latent basis contains a rotation plane carrying the shedding phase; it does NOT
mean the attractor is 8-dimensional. The 8-10 values are code bandwidth, not attractor dimension.

The dimension accounting, each step grounded:
- A strictly periodic 2D vortex street is a limit cycle: a 1-dimensional attractor [THEORY].
  A quasiperiodic variant (two incommensurate frequencies) is a 2-torus. Racca's Re = 30 case
  shows exactly this: the local dissipation rate has "a toroidal structure" and the average
  dissipation is a limit cycle [FETCHED].
- Takens' embedding theorem: a d-dimensional compact attractor embeds generically in roughly
  2d+1 coordinates, so a pure cycle needs about 3 [THEORY].
- Koopman theory does better for this specific structure: a limit cycle is represented by ONE
  complex-conjugate eigenvalue pair, i.e. 2 real coordinates rotating at the shedding frequency.
  Lusch et al. learned exactly this from wake data: a single conjugate eigenfunction pair, with
  latent omega equal to the true shedding frequency, and one extra real coordinate only for
  off-attractor transients [FETCHED]. This is the cleanest published statement that the
  vortex-street "loop" is a 2-coordinate rotation under a near-identity coordinate change.
- What the extra dims buy: the decoder must reconstruct a 4608-dim or 98,304-dim field, so the
  code carries reconstruction bandwidth beyond the attractor's dimension. Racca's practice makes
  this explicit: latent sizes were chosen "to be larger than the Kaplan-Yorke dimension"
  (N_KY = 3 quasiperiodic, 9.5 turbulent) [FETCHED], and a 9-dim CAE code recovers what ~100
  POD modes do, because a nonlinear code folds the coherent-structure family far more tightly
  than a linear one [FETCHED]. Hasegawa-style sweeps over Re add parameter coordinates to the
  same code [SEARCH].
- Cross-checks that make the loop meaningful rather than an AE artifact: energy capture vs
  latent size (9 dims -> 99.78% turbulent energy [FETCHED]), long-horizon statistical closure
  [FETCHED], and agreement between independent coordinate systems (the leading POD pair
  rotating at the Strouhal frequency [SEARCH-level], the Koopman conjugate pair [FETCHED], and
  the CAE loop all point at the same 2-D rotation plane).
- Caveat kept honest: a closed loop in one particular autoencoder's latent space alone does not
  prove the attractor dimension, because an encoder can fold a higher-dimensional process into
  a deceptively tidy cycle. The proof-shaped evidence is the size-sweep + energy + statistics
  bundle above, plus the oscillator decomposition of arXiv:2604.11745, where multiple learned
  oscillators (one per dominant frequency) each persist on its own cycle in a multi-frequency
  flow [FETCHED abstract]. Adjacent unread lead: the "phase autoencoder" work
  (arXiv:2506.12777) on extracting reduced phase dynamics from rhythmic spatiotemporal patterns
  [SEARCH, not read].

## 5. Bottom line

- Architectures: conv AE (2-10 latent dims) + LSTM ensemble / closed-loop ESN / Koopman-linear
  dynamics; the Koopman variant shows the minimal case is 2 real values.
- Cheapness: verified 15-minute desktop training and 100x-27x inference speedups; the whole
  pipeline reproduces on a workstation, the frontier cases are only expensive in ensembling and
  3D.
- Loop structure: it is the latent shadow of the physical limit cycle, implies an effectively
  1-2 dimensional attractor coordinate system (one rotation plane for phase, plus amplitude and
  parameter axes), and is best read as Takens/Kaplan-Yorke-consistent headroom: ~2 coordinates
  of dynamics in a 9-10 dimensional code.
- OWED: (a) any verified "exactly 8" latent-dim citation; (b) Hasegawa 2020's latent dimension
  and grid sizes (paywalled/full-text fetches failed this session); (c) full text of
  arXiv:2604.11745 and Agostini 2020 beyond abstracts/snippets.

## Sources (all opened this session unless marked [SEARCH])

- Lusch, Kutz, Brunton 2018, ar5iv full text: https://ar5iv.labs.arxiv.org/html/1712.09707 (journal: https://www.nature.com/articles/s41467-018-07210-0, page is SSO-gated to fetchers)
- Racca et al. 2023 JFM page: https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/predicting-turbulent-dynamics-with-the-convolutional-autoencoder-echo-state-network/1E0F75CD94FCB3A1354A09622F8D25CD
- Racca et al. preprint abstract: https://arxiv.org/abs/2211.11379
- Carl et al. 2024, arXiv HTML: https://arxiv.org/html/2402.05372v1 (landing: https://arxiv.org/abs/2402.05372)
- Data-driven oscillator model: https://arxiv.org/abs/2604.11745
- Hasegawa et al. 2020 [SEARCH]: https://keio.elsevierpure.com/en/publications/cnn-lstm-based-reduced-order-modeling-of-two-dimensional-unsteady
- Agostini 2020 [SEARCH]: https://pubs.aip.org/aip/pof/article/32/6/067103/1068957/
- Phase autoencoder [SEARCH]: https://arxiv.org/html/2506.12777v1

Banked by flash gopher r-vortex-latent, 2026-09-28. No em-dashes used.
