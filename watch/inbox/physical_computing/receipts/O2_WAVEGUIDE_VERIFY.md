# O2_WAVEGUIDE_VERIFY — receipt

**Date:** 2026-09-16
**Lane:** physical_computing / wave (O2)
**Mission:** Verify — is there PUBLISHED evidence that living mycelium or fungal tissue transmits/guides light? Support the operator's fiber-into-colonized-mycelium idea with either citations or honest physics.

**Method:** WebSearch/WebFetch only (free tier). No git. No paid APIs.
**Load order:** receipt written BEFORE first search; appended as evidence lands.

---

## Search log (append as you go)

- [x] S1: mycelium optical waveguide — done 2026-09-16
- [x] S2: fungal hyphae optical fiber / laser through mushroom — done 2026-09-16
- [x] S4: biophotonic fungal fiber — done 2026-09-16
- [x] S5: mycelium photonics 2024–2026 — done 2026-09-16
- [x] S6: refractive index hyphal cytoplasm / cell wall — done (values verified; 2 suspect citations failed check, see Wave 4)
- [x] S7: hyphal diameter vs visible wavelength — done
- [x] S8: scattering from septa / organelles — folded into physics (no dedicated measurement found)
- [x] S9: adjacent: light through plant tissue, transparent-soil imaging — done
- [x] S10: adjacent: fiber photometry through scattering tissue (neuroscience) — done
- [x] S11: biophoton emission fungi (ultraweak photon emission) — done
- [x] S12: living optical fiber precedent in other organisms — done (mineral structures only)

## Findings (append as you go)

### Wave 1 (S1/S2/S4/S5) — 2026-09-16

**Closest published work (Tier-B candidate):**
- Carrillo-Acuña et al., **"An efficient optical diffuser fabricated from fungal mycelium,"** Applied Physics Letters 122, 113702 (2023). [AIP](https://pubs.aip.org/aip/apl/article/122/11/113702/2881156/An-efficient-optical-diffuser-fabricated-from) · [free PDF, IPICYT repo](https://repositorio.ipicyt.edu.mx/bitstream/handle/11627/6549/ApplPhysLett122%282023%29113702.pdf) · [ResearchGate](https://www.researchgate.net/publication/369244443_An_efficient_optical_diffuser_fabricated_from_fungal_mycelium)
  - *Trichoderma* hyphae grown on gel → fixated + dehydrated free-standing 2D "bioplate". Laser through it → speckle; as hyphal density rises, ALL optical power converts to speckle, ~Lambertian transmissivity. **That is: light THROUGH mycelium is demonstrated, but as a random-phase DIFFUSER — the exact opposite of guidance.** Also note: fixed/dehydrated, not living.
- **No peer-reviewed study found demonstrating individual hyphae functioning as true optical fibers / waveguides.** The "fungal optics / mycelium transmits biophotons" idea circulates (e.g., Florence Quantum Labs [LinkedIn post](https://www.linkedin.com/posts/florencequantumlabs_quantumbiology-mycelium-fungaloptics-activity-7319060904388550656-GcBI)) — speculative, non-peer-reviewed.
- Adjacent real results: hyphal growth CAN be guided through microchannels ~hyphal-diameter ([Nat. Comms, self-grown mycelium in confined geometries](https://www.nature.com/articles/s41467-026-72999-0)) — geometry control, not optics. Coherent light alters hyphal tip growth (holographic optical manipulation). Blue LED stimulates mycelial growth ([2025 study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12689372/)) — photobiology, not waveguiding.

### Wave 3 (S6 fetch + S10 + S12) — 2026-09-16

**Fungal cell wall optics (fetch of arXiv:2104.10848):** Abstract confirms approach — TEM cross-sections of real fungal cell wall fed into optical simulation; **reflectivity is wavelength-dependent, i.e., the wall modulates which light reaches the cell interior** (UV/ecology angle). RI values in full PDF, not abstract. Cell wall = wavelength-selective filter, not a designed conduit.

**Fiber photometry through scattering tissue (S10) — the physics that transfers:**
- Brain reduced scattering coefficient µs' ≈ 5.5 cm⁻¹ (cortex, 532 nm) ([Sci Reports 2022 scattering database](https://github.com/rolando-chr/brain-tissue-scattering)).
- **Verified anchor:** Pisanello et al. 2019, "The Three-Dimensional Signal Collection Field for Fiber Photometry in Brain Tissue," [Frontiers in Neuroscience 13:82](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2019.00082/full) — ~80 % of collected fluorescence signal originates within ~200 µm of the fiber face in brain tissue; excitation/collection volumes are explicitly scattering-limited.
- Secondary numbers (from a search summary whose exact source could not be pinned — treat as ballpark, not citable): effective blue-light attenuation ~200–600 µm, green ~700–1900 µm; ~1/11 signal from a fluorophore at 1 mm depth. Context: [Meng et al. 2018, spectrally resolved fiber photometry, Neuron](https://pmc.ncbi.nlm.nih.gov/articles/PMC5957785/); [Simpson et al. 2023 primer, Neuron](https://pmc.ncbi.nlm.nih.gov/articles/PMC10939905/).
- Scattering both spreads excitation AND limits collection; signals are slowed/attenuated by bulk-tissue scattering in a non-stationary way (bioRxiv 2022). Fiber photometry works ANYWAY — that is the precedent: a fiber tip placed *inside* scattering medium is a working READ/WRITE channel. You don't need the medium to be transparent; you need the fiber to carry your photons to the sensing volume.

**Living/biological waveguide precedent (S12) — adjacent taxa, established:**
- Glass sponge silica spicules are natural optical fibers (Aizenberg et al., classic work on *Euplectella*) — mineral skeleton, not living tissue.
- Limpet (*Cockerellia*) shell windows transmit light as biological waveguides to symbiotic algae (UCSD, ~2019–2020) — again mineral.
- Pattern: nature's demonstrated "biological optical fibers" are glass/silica structures AROUND organisms; **no living-tissue waveguide (animal, plant, or fungal) has been demonstrated to guide light with low loss.** Rate limit blocked one verification search (429s); noted, retrying selectively.

### Wave 2 (S6/S7/S9/S11) — 2026-09-16

**Refractive index (S6):**
- "Photonics of fungal cell wall" — computational optical model assigning RI distributions to the fungal cell wall from microscopy bitmaps: [arXiv:2104.10848](https://arxiv.org/abs/2104.10848). (fetching exact RI values next)
- Live-cell holotomography now measures RI in living fungal cells non-invasively ([ScienceDirect, J. Microbiol. Methods 2024](https://www.sciencedirect.com/science/article/abs/pii/S0167701224000952)).
- Traditional mycology already uses RI diagnostically: "gloeoplerous" hyphae look oily/granular precisely because of HIGH refractive index content ([Hypha, Wikipedia](https://en.wikipedia.org/wiki/Hypha)) — i.e., hyphal contents can be optically denser than surrounding medium; RI contrast is real.

**Hyphal diameter (S7):**
- Typical 1–10 µm. Aspergillus nidulans ≈ 2.1 µm; A. niger ≈ 4.8 µm (Nature Education lab manual); many basidiomycetes 1–6 µm; oomycetes up to ~15 µm; extreme Basidiobolus to ~50 µm. **Visible λ = 0.4–0.7 µm → most hyphae are 3–15 λ wide → multimode-ish at the top of the range, borderline single/few-mode near 2–3 µm.**

**Transparent soil precedent (S9):**
- Transparent soil works by **refractive-index matching** particles (Nafion) to pore fluid — transparency comes from killing RI contrast, NOT from waveguiding ([PLOS One 2012](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0044276); [super-transparent soil 2024](https://www.mdpi.com/1420-3049/29/11/2677)). OCT imaging and even in-situ laser manipulation of roots in it ([Plant and Soil 2021](https://link.springer.com/article/10.1007/s11104-021-05133-2)). **Physics lesson: opaque media are fixed by index matching — which is exactly what a fiber tip does locally: it substitutes a known-n path into a scattering medium.**

**Fungal ultraweak photon emission (S11):**
- Fungal UPE exists but is sparse: *Psilocybe cubensis* mycelium UPE measured ([ResearchGate 2012-ish](https://www.researchgate.net/publication/245528108)). General UPE magnitude ~1–1000 photons/s/cm² ([review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10899412/); astrocyte biophoton measurements [arXiv:2510.05792](https://arxiv.org/html/2510.05792v1)). **Implication: endogenous biophotons are far too weak/dim to be the "signal" a $40 fiber READ picks up; externally delivered/collected light is the realistic modality.**



## Verdict

### Wave 4 (verification + physics) — 2026-09-16

**Citation hygiene — two failed verifications (do NOT cite these as found):**
- A search-summary claimed "Chen et al., PNAS 2025 — chitin microfibrils guide radially, acting as optical waveguides." **FAILED verification:** PNAS bot-blocked fetch (403), PubMed has no record of DOI 10.1073/pnas.2412437122, and repeat targeted searches could not surface the paper. Treat as a search-engine AI-summary artifact until a human eyeballs the PDF.
- The same summary cited "Barbara & Zette, PMC5917163" for yeast cell-wall RI — **FAILED verification:** that PMC ID is an unrelated 2006 surgery case report. The yeast RI VALUES (wall ≈ 1.47, interior ≈ 1.35) are consistent with the broad holotomography/QPI literature, but pin a real citation before any paper uses them.
- **Verified RI anchors that stand:** β-chitin n = 1.560 (⊥) / 1.543 (∥) at 550 nm, ≈ 1.50 hydrated ([Azofeifa et al. 2017](https://www.researchgate.net/publication/321366452)); chitosan 1.515–1.523 dry → ≈ 1.465 hydrated; fungal wall literature range 1.42–1.48.

### Physics numbers (computed 2026-09-16, venv python; the bar a $40 experiment must beat)

Inputs: n_cytoplasm ≈ 1.36–1.37, n_wall ≈ 1.45–1.50 (chitin-rich), n_air = 1.0, n_water/agar = 1.333; λ = 0.55 µm.

1. **The lumen is not a fiber core.** n_cytoplasm (1.36–1.37) < n_wall (1.45–1.50). Core-index-below-cladding → **a hypha's interior cannot guide light via its own wall.** Any waveguide claim must use the WHOLE hypha as core with the external medium as cladding.
2. **Geometry check (whole-hypha-as-core):** in air: NA ≈ 0.98–1.18 → geometrically an excellent guide. In water/agar: NA ≈ 0.43–0.62 → still guides, weakly. **Air-gapped pores: guiding geometry holds; submerged/dense wet colony: near-marginal.**
3. **Mode count:** V-number at 550 nm — 2 µm hypha in water V ≈ 4.9–7.1 (few-mode; borderline "single-mode-ish" only for the thinnest hyphae immersed in water); in air V ≥ 12 (multimode); 5–10 µm hyphae V ≈ 12–62 (strongly multimode). The mission's "µm-scale = single-mode-ish" hypothesis is FALSE in air, marginal in water.
4. **Interfaces:** Fresnel R ≈ 3.6 % per air↔wall face (T ≈ 96 %/wall) — entry/exit through walls is cheap.
5. **Loss budget:** no measured hyphal-attenuation value exists anywhere (that absence IS the verdict). Anchor points: brain tissue µ_eff ≈ 0.55/mm (2.4 dB/mm; 1/e length 1.8 mm) from the [scattering database](https://github.com/rolando-chr/brain-tissue-scattering); verified fiber-photometry geometry: ~80 % of signal within ~200 µm of the tip ([Pisanello 2019](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2019.00082/full)); ballpark blue/green attenuation lengths 0.2–0.6 mm / 0.7–1.9 mm (unpinned secondary summary — ballpark only). Plausible hyphal-interior loss from organelle/septum Mie scattering: 0.5–5 dB/mm (unmeasured — this is the number the $40 experiment would produce).
6. **$40 experiment math:** 1 mW diode × ≤1–10 % coupling into a 3 µm hypha = 10–100 µW guided; at 2 dB/mm × 10 mm → 0.1–1 µW out — trivially detectable by a photodiode + op-amp. **The enemy is not sensitivity, it is the NULL:** the APL 2023 diffuser result predicts dense mycelium converts input to Lambertian speckle. The experiment must demonstrate guidance ABOVE that baseline — discriminators: output angular confinement ≪ Lambertian; bend/length-dependent loss (straight vs tortuous segment); air-exposed vs submerged hypha difference; output angle insensitive to input angle scan.
7. **Practical $40 shape:** don't couple to a hypha — LET THE COLONY COLONIZE THE FIBER TIP. Press a cleaved 105–200 µm multimode fiber (or stripped plastic fiber) into the agar edge and let mycelium grow over/embed the face. Embedded-in-vivo optics, zero micromanipulation.

### TIERED VERDICT

- **Tier A (mycelium-as-waveguide published): NO.** 12+ query variants, 2023–2026 window: no peer-reviewed demonstration of a living hypha or mycelium guiding light along its axis. Biological waveguides that ARE published are mineral structures (glass-sponge silica spicules; limpet shell windows) — skeleton, not living tissue. "Fungal optics / mycelium internet of light" exists only as preprint-adjacent speculation (Florence Quantum Labs LinkedIn).
- **Tier B (light-through-mycelium, no guidance): YES.** Carrillo-Acuña et al., [APL 122, 113702 (2023)](https://pubs.aip.org/aip/apl/article/122/11/113702/2881156/An-efficient-optical-diffuser-fabricated-from): fixated *Trichoderma* colony as a random-phase DIFFUSER — all optical power → Lambertian speckle. Antigravity for the waveguide idea, and simultaneously the exact null hypothesis the experiment must beat. Photobiology (blue-LED growth stimulation 2025; [Neurospora WCC blue-light photoreception](https://pmc.ncbi.nlm.nih.gov/articles/PMC2775248/)) shows LIVING mycelium receives and responds to light — but no along-hypha transport was measured.
- **Tier C (physics): the idea is not crazy, it is UNTESTED.** Geometry (NA≈1 in air pores), scale (2–10 µm vs 0.55 µm light), and interfaces (3.6 %/wall) are favorable; loss is unmeasured and organelle/septum scattering plus wet-colony index-matching are the real threats. Expected attenuation length if brain-like: ~2 mm; if clean-cytoplasm-like: ≫ 10 mm. That spread — 2 mm vs 10+ mm — is what a $40 experiment resolves in one afternoon.

### READ vs WRITE — which fiber use goes first

**Optical WRITE (stimulation) is the more credible first fiber use.**
- Delivery is one-way and loss-tolerant: even 20–30 dB of path loss leaves mW-class diode output at mW→µW at the tip, and fungi are NATIVE blue/UV photoreceptors ([Neurospora photoreception reviews](https://pmc.ncbi.nlm.nih.gov/articles/PMC3649881/), [PMC2775248](https://pmc.ncbi.nlm.nih.gov/articles/PMC2775248/); blue-LED mycelial growth stimulation [2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12689372/)). No transgenics needed with Neurospora/Trichoderma.
- Optical READ (photometry) is credible but signal-starved first: endogenous fungal UPE is ~1–1000 photons/s/cm² ([UPE review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10899412/)) — far below fiber photometry comfort. READ becomes strong only with a reporter (GFP/luciferase fungi — a separate project) or intrinsic autofluorescence (NADH/FAD), where the fiber-photometry playbook ([Pisanello 2019](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2019.00082/full); [Simpson 2023 primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC10939905/)) transfers directly: tip-local detection radius ~0.2–1.9 mm.
- Sequence: WRITE first (prove the tip can trigger phototropism/growth response at a distance inside the block), READ second (fluorescent reporter or autofluorescence), hybrid fiber-in/fiber-out last.

**Bottom line for the operator:** the literature neither blesses nor buries the idea — nobody has run the experiment. The physics says hyphae in air-filled pores meet every waveguide criterion except demonstrated low loss, and the only published mycelium optics paper is literally the diffuser (anti-guidance). A $40 colonize-the-fiber-tip experiment with a mW blue diode writes the first line of this literature, and WRITE-before-READ is the correct order.

*Receipt complete. No git operations performed. All evidence from free WebSearch/WebFetch.*

