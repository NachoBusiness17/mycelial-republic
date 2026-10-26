# FRONTIER_PROJECTION_FIDELITY_20260906

BATCH7|ra| (ra-frontier) · 2026-09-06 · Commission: "REAL structure, or hallucinated meaning?" — SHADOW WALK (dashboard/static/shadow_walk.html, 9,305 parts, HASH aaad8ddf) and the lightmap family, under the operator's walk-through lens.

---

## ITEM 1 — Frontier dig: structure-vs-artifact in projected volumes

### 1a. t-SNE/UMAP distortion literature (distance preservation failures, cherry-picking)

- **How to Use t-SNE Effectively** — Wattenberg, Viégas & Johnson, *Distill*, 2016. The canonical treatment: t-SNE "adapts its notion of distance"; cluster sizes, inter-cluster distances, and even the NUMBER of clusters are artifacts of perplexity. Interactive demos show identical data producing wildly different structures. (distill.pub/2016/misread-tsne)
- **t-SNE Exaggerates Clusters, Provably** — Bergam et al., Columbia (arXiv ~2021+). Formal proof that t-SNE can emit false-positive clusters: apparent groupings that do not exist in the source data. (cs.columbia.edu/~verma/papers/tsne_false_positives.pdf)
- **Clustering with t-SNE, Provably** — Linderman & Steinerberger, 2019 (PMC7561036). The balanced counterweight: under conditions (early exaggeration, well-separated clusters) t-SNE provably RECOVERS real clusters. Trust is conditional, not absent.
- **Understanding How Dimension Reduction Tools Work** — Wang et al., *JMLR* 22, 2021. Rigorous algorithmic account: t-SNE/UMAP preserve LOCAL structure well, GLOBAL structure poorly. Neighborhood claims survive; inter-biome distance claims do not. (jmlr.org/papers/volume22/20-1061)
- **It's time to stop making t-SNE & UMAP plots** (and the Dec 2024 follow-up "Biologists, stop putting UMAP plots in your papers") — Chari & Pachter, 2021/2024. Measured: displayed positions correlate only weakly with true distances; plots invite over-reading.
- **Dimensionality reduction by UMAP reinforces sample clustering** — Yang et al., *Cell Systems*, 2021. Worse than neutral: UMAP can AMPLIFY weak clustering signals, manufacturing apparent structure.
- **Stop Misusing t-SNE and UMAP for Visual Analytics** — arXiv:2506.08725, 2025. Interview study: practitioners routinely over-interpret spatial artifacts AND cherry-pick parameters/results. The failure is a loop between algorithm and motivated reader. — **This loop is precisely the operator-walking-his-own-volume situation.**
- Cross-entropy test for statistically comparing embeddings — PMC9939422, 2023: quantitative comparison of embeddings instead of eyeballing exists and is cheap.

### 1b. Interpretability's hallucination problem

- **An Interpretability Illusion for BERT** — Bolukbasi et al. (Google), arXiv:2104.07143, 2021. The founding paper: an interpretation method (neuron examination) looks valid and compelling on a narrow sample while masking a distributed, different reality. Illusions are NOT errors — they are locally true, globally misleading.
- **Interpretability Illusions with Sparse Autoencoders: Evaluating Robustness of Concept Representations** — Li, Srinivas, Bhalla et al., arXiv:2505.16004, 2025. SAE features look monosemantic from top-activating examples but fail robustness/steering tests; the illusion survived the field's upgrade from neurons to SAEs.
- **Sparse Autoencoders Do Not Find Canonical Units of Analysis** — ICLR 2025. The decomposition is not unique; "the feature" is partly an artifact of training run and dictionary size.
- **Reflections on Anthropic's SAE research** — Alignment Forum, 2024. Field-level caution: headline "interpretable features" claims repeatedly outrun the control conditions.
- **The Dead Salmons of AI Interpretability** — arXiv:2512.18792 (cited-by lineage): illusion-type results keep being rediscovered per new method generation.

### 1c. Probing-classifier criticism (encoded ≠ understood)

- **Designing and Interpreting Probes with Control Tasks** — Hewitt & Liang, *EMNLP* 2019. High probe accuracy is insufficient: probes can memorize from word types. Fix = control tasks + selectivity. The template for ANY claim that volume position carries meaning: probe against a control, or the probe is a puppet.
- **Probing Classifiers: Promises, Shortcomings, and Advances** — Belinkov, *Computational Linguistics* 48(1), 2022. The synthesis: probing shows information is ENCODED, not that the system USES or UNDERSTANDS it; surface statistics suffice for many "semantic" probe results.
- **Probing Classifiers are Unreliable for Concept Removal and Detection** — NeurIPS 2022. Even "successful" probes can be reading shortcuts, not concepts.

### 1d. World-model / latent-map work, 2024–2026

- **Cognitive Maps in Language Models: A Mechanistic Interpretability Study** — Baumgartner et al., NeurIPS 2025 / arXiv:2511.13371. Trains GPT-2 on grid-world navigation and asks whether a mechanistic cognitive map actually forms — the direct analog of our question, inverted (they probe the model; we probe a projection OF the model's record).
- **Multi-modal Cognitive Maps for Language and Vision Based Navigation** — Stoewer et al., *Neurocomputing*, 2025 (and Stoewer et al., *Sci Reports* 2022 on successor-representation cognitive maps of space AND language). Language structure supports map-like representations — real, but constructed under supervision, not discovered from a dump.
- **Spatial Intelligence from a Cognitive Map Perspective** — preprints.org 202605.1782, 2026. Survey-level: the field still treats spatial structure in language models as a hypothesis under test, never as given.

### 1e. Navigable model surfaces / latent-landscape tools (the closest prior art)

- **LAPEX: Engineering Interactive Latent Space Visualizations** — ACM (dl.acm.org/10.1145/3816764). Navigable latent-space visualization FOR understanding black-box models — but as a look-at interface, not a walk-through world with quests and fog.
- **LatentGandr** — arXiv:2604.19953, 2026. Visual analytics over generative latent space via locally linear dimensions. State of the art is still "extract axes, view" — nobody renders the projection as TERRAIN with locomotion.
- **Latent Terrain** — Zheng et al., *Frontiers in Computer Science*, 2025. Terrain mapping of an AUDIO latent space for gestural exploration — the nearest neighbor to Shadow Walk found; perceptual-instrument framing, no fidelity falsifiers.
- **Walking Inside a DeepSDF Latent Space** (WebGPU showcase) and Stable-Diffusion-Latent-Space-Explorer (GitHub): browser walkable/interpolable latent spaces exist as demos — none publish projection-fidelity controls.
- **Cluster-based permutation caution** — Senior et al., *Psychophysiology*, 2021 (+ FieldTrip FAQ): a significant cluster-based permutation test licenses "structure exists SOMEWHERE," never "this corridor HERE is the effect." Directly shapes what our null model can prove.

**Synthesis of the dig:** every field that renders internal structure as a space has hit the same wall — the space reliably LOOKS meaningful (local continuity), the global geometry and the semantics are where the illusions live, and the fix is always the same shape: controls (null models, control tasks, re-seeds) rather than better-looking renders. No 2026 work found that applies this discipline to WALKABLE model surfaces. The lane is open.

---

## ITEM 2 — The hallucination test, formalized

**The test (one paragraph):** A perceived structure S (a cluster, wall, corridor, void, or "invariant") in a projected volume V built from source data D is **REAL** if and only if S is *predictable from D*: points that are close in V are close under D's own recorded features (neighbor fidelity — trustworthiness/continuity-style rank correlation between volume distance and source distance holds in and around S), AND S *stabilizes*: re-deriving V from D under re-seeded quantization, chunking, and projection parameters reproduces S within tolerance, AND S *aligns*: S's regions correspond to independently recorded source labels (slab identity, law class, epoch) above a chance-corrected baseline measured WITHOUT the HUD or quest markers in view, AND S *separates from the null*: S's structure statistics (cluster count, modularity, corridor straightness, void volume, invariant co-location) exceed the 95th percentile of the same statistics computed on null volumes built from shuffled controls of D that preserve marginals but destroy relational structure. If any limb fails, S is an artifact of the projection pipeline (LAW-061 territory) or of the walker's pattern-hungry perception — and any meaning felt while walking is confabulation until a probe passes.

**The four property candidates, named:**
1. **Neighbor fidelity** — source-close ⟺ volume-close (local; the limb DR literature says CAN hold).
2. **Stability under re-projection** — re-seed → same structures (multi-perplexity discipline, Distill 2016).
3. **Semantic alignment** — volume regions ⟺ source labels (the probing limb; requires control tasks, Hewitt & Liang).
4. **Null-model separability** — real projection beats shuffled control on structure statistics (permutation limb; per Senior 2021, a pass proves existence somewhere, not the walked location).

---

## ITEM 3 — The family, tri-state

### SHADOW WALK (dashboard/static/shadow_walk.html, PTS 9305, HASH aaad8ddf, GX 288 × GZ 64)

- **SUPPORTED (known real):** The 9,305 behavioral parts exist; part-order, law_hits density, and char size are real recorded features of the corpus; the LAY norm-gradient array is real per-slab measurement (the "rising norm gradient" is data, not decoration). The quantization is deterministic, so the volume IS a faithful image of those three features. The HUD's own LAW-061 citation ("preserves nothing about semantics") is accurate as stated.
- **OPEN:** Whether the macro-structures a walker perceives (biomes, voids, gradients) correspond to corpus structure BEYOND the three encoded features; whether operator-felt "invariants" correspond to source-level regularities. This is exactly what the four-limb test decides, and it has never been run. The neighbor-fidelity limb is probably passable (features are smooth over part order); the semantic-alignment limb is the hard one.
- **LIKELY ARTIFACT:** Any semantic meaning felt while walking — per LAW-061 the projection preserves nothing about semantics, so "this corridor feels like the doctrine era" is the player's confabulation UNTIL a semantic-alignment probe passes. Additionally, per the HTML footer itself: **corridors are BFS least-time paths** — an algorithm's construction, not a discovery about the corpus; **quest objectives (BOOT_CHECK → THE CHAIN → THE ROOM → ASCEND) are builder-placed**. Perceived "landmarks" that are actually quest scaffolding are illusion-by-design (the Bolukbasi pattern: locally true, globally misleading — the landmark exists, it just wasn't found).

### LIGHTMAP family (d(θ) shadow maps, gold-marked invariants)

- **SUPPORTED:** The d(θ) shadow maps are computed from real chained data; the gold walls exist in the artifact and the chain behind them is verifiable.
- **LIKELY ARTIFACT (as "discoveries"):** The chain/room/boot_check gold walls were **seeded canonical, not discovered** — the builder marked known ground-truth objects and rendered them as environment. The walk's discovery framing is inverted: the operator (or the fleet) authored the invariants, then walked into them. This does not make them false — it makes them LABELS, not FINDINGS. Their verification status comes from the chain, not from the walk; walking them is a usability test, not evidence.
- **OPEN:** Whether ANY unmarked structure in the lightmaps (un-gold walls, shadow boundaries) carries source-invariant status. Nobody has run a null-map control on the lightmap family.

---

## ITEM 4 — The research board (what makes this publication-grade)

**The gap (our angle):** The entire validation literature treats projections as ANALYTIC surfaces — you LOOK at them, then go check the source data. Shadow Walk is a NAVIGATION surface — you walk it, with locomotion, fog, quests, and score shaping what you sample. The walker is a moving probe with a biased sampling policy; cherry-picking (arXiv:2506.08725) becomes SPATIALIZED — you literally walk toward the interesting bit, then feel meaning where you stopped. Nobody studies projection fidelity under embodied, quest-structured, self-motivated traversal of a model's own behavioral record. That is the paper.

**The instrument (build order):**
1. **Null-model harness** (the falsifier): permute the 9,305 parts preserving marginals (per-part feature distributions), rebuild the voxel volume N times, compute structure statistics on real vs null, report percentile. Inherit the Senior-2021 caution: a pass says "macro-structure exists," never "THAT corridor is the finding."
2. **Stability sweep:** re-seed quantization/chunking/projection; measure structure overlap (multi-perplexity discipline, Distill 2016).
3. **Neighbor-fidelity score:** trustworthiness/continuity metrics volume-wide and per biome (Wang JMLR 2021 tooling).
4. **Blind semantic-alignment probe** (the Hewitt & Liang move): walkers navigate WITHOUT HUD/quests and predict source labels (slab, law class, epoch) from position alone; compare to chance and to control-task (shuffled-label) baselines. THIS is the single test that converts "feels like meaning" into a tri-state verdict.
5. **The study:** n=1 operator is honest as instrument shakeout, never as evidence; the recognition protocol's frontier-model players give cheap width and a second species of confabulation to measure against.

**Venue shape:** arXiv preprint → IEEE VIS / interpretability-workshop track, framed as "walkable interpretability surfaces and their illusions," explicitly inheriting the Bolukbasi → SAE-illusion lineage and extending it from reading interfaces to walking interfaces.

**The bet:** Coarse macro-structure (biome banding, the norm gradient, void mass) WILL survive the null-model control — part-order autocorrelation is real and quantization of autocorrelated features necessarily bands; I place **~70%** on macro-structure survival. Fine structure (specific corridors, specific "invariants") is ~25–30%: corridors are BFS by construction, and semantic alignment has never passed a control-task probe anywhere in the literature we could find. So: the operator is not hallucinating that the land has SHAPE. He is almost certainly hallucinating what the shape MEANS — until probe 4 runs.

---

BATCH7|ra| frontier dig=18 sources cited across 5 literatures, formalization=REAL iff neighbor-fidelity + re-projection stability + semantic alignment (control-tasked) + null-model separability; else artifact/confabulation, family tri-state done (SHADOW WALK + lightmaps, seeded-gold marked honestly as labels-not-findings), board filed watch/FRONTIER_PROJECTION_FIDELITY_20260906.md, my bet=70% macro survives / 30% invariants survive.
