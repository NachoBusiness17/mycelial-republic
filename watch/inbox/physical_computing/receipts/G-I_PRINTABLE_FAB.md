# G-I PRINTABLE FAB — receipt (append-as-you-go)

- **Lane:** wave / physical_computing
- **Gap:** G-I — multispecies lattice assumes printable substrate (spent oats + nutrient traces, printed lattice, then inoculated). Verify printability.
- **Date:** 2026-09-16
- **Method:** WebSearch/WebFetch only (free tier law). No git. No paid APIs.
- **Status:** IN PROGRESS — receipt written first, appended as research lands.

## Questions to answer (Socratic teases)

1. What 3D-printed living mycelium work exists (Blast Studio, academic myco-composite printing, paste-extrusion of myceliated substrate) — paste consistency, printer class, print parameters?
2. Can nutrient traces be printed as GRADIENTS (multi-paste printing, or post-print inoculation zoning)?
3. Hobby-tier printer conversion path (paste extruder on a Prusa-class machine — cost, files, communities)?

## Working notes

(appending below as research lands)

### Batch 1 — core myco-printing literature (2024-2025)

- **Mycofluid (PMC/NIH, published 2025, work 2024):** paste of primarily **spent coffee grounds**, printable on a **hobbyist 3D printer**, remains living substrate for fungal growth. DIRECT HIT on our exact question (waste substrate + hobby printer + living paste). → https://pmc.ncbi.nlm.nih.gov/articles/PMC12038323/ — need paste recipe + nozzle/layer params. (Note: first WebSearch call hit rate-limit 429s; retried OK — wave-lane free tools work, just flaky.)
- **MDPI Biomimetics 8(2):257 "Three-Dimensional Printing of Living Mycelium-Based Composites":** key engineering insight = paste needs **form-stabilization** (workable but holds shape layer-by-layer). → https://www.mdpi.com/2313-7673/8/2/257
- **ResearchGate figure, paste-extrusion settings:** shrinkage high, mechanical performance low → mitigated by pairing mycelium with biochar; documents scaled-down MBC paste-extrusion settings. → https://www.researchgate.net/figure/The-3D-printing-paste-extrusion-settings-and-design-customization-by-scaling-down-the_fig1_374935563
- **Canterbury thesis:** extrusion-based printing where paste is printed layer-by-layer as scaffold for mycelial growth. → https://ir.canterbury.ac.nz/bitstreams/60f2e5b0-1038-46e5-a9ea-c8d789dd40fd/download
- **MyCera (YouTube):** mycelium + **clay** paste — mycelium as bio-binder / reinforcement in a printable mineral carrier. Alternative carrier-class recipe. → https://www.youtube.com/watch?v=RMdPgJJPOew
- **eCAADe 2021 multi-material mycelium composites:** two-phase multi-material process → relevant to Q2 (gradients / multi-paste). → https://papers.cumincad.org/cgi-bin/works/paper/ecaade2021_059
- Alternative path noted: **binder jetting** (Texas A&M, fungus + farm waste) — not our path (industrial printer class) but recorded for completeness. → https://www.mycostories.com/post/fungal-3d-printing-breakthrough-how-mushrooms-could-revolutionise-sustainable-manufacturing

### Batch 2 — Blast Studio (the flagship living-mycelium print studio)

- **Official:** Tree Column — 3D-printed living sculpture, used coffee cups + mycelium. → https://www.blast-studio.com/tree-column
- **Dezeen (2022-01-18):** London studio, method for 3D printing with **living mycelium**, 2 m column, designed to be harvestable (oysters). → https://www.dezeen.com/2022/01/18/blast-studio-tree-column-mycelium-design/
- **3D Printing Industry:** printing-with-mycelium method detail. → https://3dprintingindustry.com/news/blast-studio-has-3d-printed-a-living-building-column-made-of-fungi-202586/
- **3D Natives:** → https://www.3dnatives.com/en/tree-column-3d-printed-column-from-mycelium-and-waste-270120224/
- **Self-repair angle:** partially drying mycelium → planned self-repairing structures (Surfaces Reporter). → https://www.surfacesreporter.com/articles/133920/3d-printed-mycelium-column-made-from-waste-coffee-cups-can-replace-concrete-blast-studio
- **Growth timeline:** prints sit in humid environment ~1 month to grow/bind (Untapped Journal). → https://untappedjournal.com/stories/blast-studio-design-recycle-waste-natalia-rachlin
- **Studio video "Lovely Trash":** → https://www.youtube.com/watch?v=W8tpiWSZfm0
- MDPI Biomimetics page returns 403 to WebFetch — will pull the science from PMC mirror of related work / ResearchGate / encyclopedia.pub mirror instead.

### Batch 3 — Mycofluid deep dive (THE reference recipe) + hobby extruder market

**Mycofluid (PMC12038323) — full extraction:**
- **Paste recipe (wt%):** spent espresso grounds 54.9 · brown rice flour 13.7 (carb source, PF-Tek lineage) · ground grain spawn 5.5 (inoculant, Reishi/Ganoderma chosen over oyster for contamination resistance) · food-grade xanthan gum 1.1 (rheology modifier + binder) · water 24.7 (added last until printable). Total moisture 52% (authors note 60–75% usually recommended).
- **Consistency test:** 10 mL syringe test — 8 mL of paste extruded onto glass must stand free with a slight tilt. Rheology: shear-thinning (0.1–2.5 s⁻¹ confirmed).
- **Printer class:** custom open-source "Fungibot" = 1 L polycarbonate plunger reservoir (70 mm ID) → flexible hose → **8 mm auger extrusion printhead** on a **Jubilee motion platform**. ~$200 extruder + ~$1500 platform. Build volume 300×300×300 mm. **Nozzle 5 mm.** Sliced in **PrusaSlicer** (presets in Supplementary S1 — i.e., stock slicer toolchain works). Open-loop, no clog sensing.
- **Sterilization:** 70% IPA wipe-down of everything; **no laminar hood required** — spent coffee is "relatively sterile due to the coffee-making process."
- **Inoculation:** spawn mixed INTO the paste (same as Blast Studio). Living-from-print.
- **Incubation:** lidded container, sprayed once daily, aired, warm low-light corner. **Day 5 loose viable growth, day 10 full colonization.** Dry ≥24 h at 22°C to kill/set.
- **Open time:** paste refrigerates "several days"; no hard print-time limit but paste stays malleable during incubation (handle gently).
- Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC12038323/

**Hobby paste-extruder market (Q3) — price ladder:**
- **Budget heads ($100–165):** Funssor clay/paste pellet extruder nozzle assembly from $161.08 (https://funssorlab.com/products/clay-paste-pellet-extruder-for-3d-printer-ceramic-biomaterial-filament-extruder-nozzle-assembly-kit); Funssor worm-gear screw extruder upgrade kit from $102.39 (https://funssorlab.com/products/funssor-clay-paste-screw-extruder-system-upgrade-kit-worm-gear-pusher-motor-for-diy-ceramic-3d-printer-assembly-kit); Blurolls clay/ceramic paste printhead w/ NEMA7 motor + replaceable nozzles (https://www.blurolls3d.com/products/blurolls-clay-paste-3d-printer-diy-printhead-ceramic-extruder-pellet-kit-nema7-motor-replaceable-nozzle).
- **Mid kits (~$490–600):** StoneFlower3D Basic Ceramic Kit 0.5 L = **€600** (print head + nozzles + 0.5 L ram extruder, mounts on desktop FDM) https://www.stoneflower3d.com/store/ceramic-3d-printing-kit/ · PRO 1.5 L = €900. AliExpress full kit explicitly Ender 3/Prusa i3 compatible (https://he.aliexpress.com/i/1005012504192770.html). Amazon 500 mL DIY syringe kit (https://www.amazon.com/Ceramic-Clay-Printer-Extruder-500ML/dp/B0GJRPTDQF). Ubuy listing ~€490.
- **Communities:** Prusa forum thread "clay extruder easily attached to the i3?" (https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-others-archive/is-there-a-clay-extruder-that-can-easily-be-attached-to-the-i3/) · r/Ceramic3Dprinting MK3S conversion thread (https://www.reddit.com/r/Ceramic3Dprinting/comments/1975r2j/prusa_mk3s_conversion/) · r/3Dprinting DIY clay/concrete extruder (https://www.reddit.com/r/3Dprinting/comments/4q9gl7/diy_clayconcrete_extruder_prusa_i3/) · HE3D TC-series clay upgrade kits assembly video (https://www.youtube.com/watch?v=KXiR0p5tgGs).
- Prusa sells no official paste extruder; third-party kits explicitly target Prusa i3/MK mounts.

### Batch 4 — gradient / multi-paste printing (Q2) first returns

- **SPECS (HardwareX 2021, open source):** syringe-pump extruder + curing system for Reprap-class printers; swappable syringe volumes and needle sizes → basis for N-paste zoning. → https://www.hardware-x.com/article/S2468-0672(21)00004-3/fulltext
- **Hybrid multi-head paste/ink printer (2023, T&F Open Agric?):** FOUR print heads operable individually or together for multi-material paste + ink printing. → https://www.tandfonline.com/doi/full/10.1080/21870764.2023.2247210
- **Dual extrusion for soft materials (2025, ResearchGate 389938228):** dual-extrusion soft-material system with flow-rate compensation. → https://www.researchgate.net/publication/389938228
- **BCN3D+ dual paste extruder (open hardware):** prints any paste requiring extrusion force ≤100 N — practical reference for dual-paste on hobby gantry. → https://bcn3d.com/dual-paste-extruder-last-of-the-upgrades-for-the-bcn3d/
- **Multinozzle precedent:** Abilgaziyev et al. — 5 distinct materials/colors simultaneously (PMC multimaterial AM review).
- **Twin-screw extrusion design (Beijing Univ. Chem. Tech.):** in-line mixing mechanism → in-principle route to continuous composition gradients.

### Batch 5 — Blast Studio technical media + MDPI mirror

- **Blast Studio YouTube channel** (process documentation): https://www.youtube.com/channel/UCzJU0ZO1Q8_-zbtYFY_kjZA
- **"Urban Stomach" machine video** — their machine that turns shredded/boiled coffee cups into printable paste objects: https://www.youtube.com/watch?v=sQPFRRDt25E
- **Medium walk-through** of Tree Column production (shred → boil → sterile pulp → mix mycelium → print): https://medium.com/@v.shestakov1/02-blast-studio-3d-printed-mycelium-column-c1584c297be9
- **Key find:** MDPI Biomimetics 8(2):257 "Three-Dimensional Printing of Living Mycelium-Based Composites" (2023) has a PMC full-text mirror — PMC10296363 — which documents **Blast Studio's own method** as an academic reference. → https://pmc.ncbi.nlm.nih.gov/articles/PMC10296363/ (fetching next for parameters)

### Batch 6 — recent 2024-2026 sweep + living-bioink frontier

- **TU Delft / Shaping Matter Lab (Advanced Functional Materials, 2025, DOI 10.1002/adfm.202530836):** 3D-printed **living** *Ganoderma lucidium* mycelium via DIW of a hydrogel bioink (sodium alginate + κ-carrageenan + agar + cellulose thickener, loaded with hyphal fragments), CaCl₂-crosslinked after printing. Key Q2 evidence: **gelatin masking enabled localized deposition — different regions of one structure functionalized independently**; modular block-swap = self-repair precedent. → https://www.mycostories.com/post/tu-delft-3d-prints-living-mycelium-that-assembles-its-own-functional-materials
- **Mycelial Hut, Yong Ju Lee Architecture (SeoulTech campus, Nov 2025):** robotically 3D-printed **molds**, mycelium grown inside (indirect mold-and-grow, NOT printed paste); wooden frame + mycelium skin panels; multiple substrate mixes screened. → https://www.designboom.com/architecture/yong-ju-lee-bio-integrated-pavilion-mycelium-robotic-3d-printing-seoul-11-05-2025/ · https://www.voxelmatters.com/3d-printing-mycelium-seoul-bio-hybrid-pavilion/
- **Cambridge 2026 paper ("Rooted in waste"):** feasibility of 3D-printing **upcycled cat litter** into a resource-efficient mycelium composite screening system — second confirmed waste-granular-substrate printability result (analog class to spent oats). → https://www.cambridge.org/core/services/aop-cambridge-core/content/view/1611A00488FBE0449BDC8EABEF5CD331/S2977905726100468a.pdf/rooted-in-waste-feasibility-of-3d-printing-upcycled-cat-litter-for-developing-a-resource-efficient-mycelium-composite-screening-system.pdf (PDF fetch unsupported by WebFetch; title/venue verified via search — flagged as light-verification)
- **Biogenic Architecture (Canada):** 3D-printable mycelium biocomposites from mushroom roots + plant fibers. → https://www.biogenicarch.ca/3d-printing
- **Henning Larsen "Growing matter(s)":** mycelium living-material installation. → https://henninglarsen.com/projects/growing-matters
- **Open-source DIY extruder files (Q3):** Bricoleur clay extruder **~$30 build**, files on Thingiverse (https://www.thingiverse.com/thing:1413969) · CERA-1 open-documentation paste extruder + printer framework (https://sites.google.com/site/openprojectspage/cera-1-clay-extruder) · StoneFlower full-metal extruder schematics + materials list (https://www.stoneflower3d.com/projects/clay-extruder-prototype/) · "Easiest Way to Print With Clay" DIY extruder video w/ files (https://www.youtube.com/watch?v=Q3A4NqTPOYY) · Instructables Ender-3 clay conversion (https://www.instructables.com/Ender-3-Clay-Printer-Conversion/) · auger extruder experiments (https://www.youtube.com/watch?v=65m_zIly-H4) · universal paste extruder demo (https://www.youtube.com/watch?v=x8ILdNDrXrc) · WASP as the pro reference class (https://www.3dwasp.com/en/ceramic-3d-printing-wasp-clay/)

---

## VERDICT (final)

### Q1 — Is a spent-oats + nutrient-trace lattice printable? YES, hobby-tier, with one recipe-swap caveat.

**Paste recipe class (proven, transfer as-is):** Mycofluid class = ~55 wt% spent granular substrate (documented: spent coffee grounds; our spent oats are the same class — post-boil/steam grain, relatively sterile, similar particle scale; cat litter analog also confirmed feasible, Cambridge 2026) + ~14 wt% starchy flour (nutrient) + ~5.5 wt% grain spawn (if printing living) + ~1 wt% xanthan gum + water to ~50–60% moisture. Target consistency: shear-thinning; passes the "8 mL in a syringe stands free under slight tilt on glass" test (Mycofluid printability gate). Blast Studio's parallel class = shredded/boiled paper pulp + mycelium (their structural route); TU Delft's lab class = alginate/carrageenan hydrogel bioink with hyphal fragments (overkill for us).

**Printer class:** a Prusa-class FDM gantry + bolt-on paste extruder (syringe/ram/auger). Reference build: Fungibot = Jubilee motion platform + 1 L plunger reservoir + 8 mm auger head (~$1,700 all-in), **5 mm nozzle**, sliced in stock **PrusaSlicer** (paste presets published in the paper's supplement). Sterility = 70% IPA wipe-down of reservoir/head/nozzle; **no laminar hood needed** — the cooked substrate itself carries the sterility budget. Colonization: day 5 loose growth, day 10 full colonization, in a lidded tote, misted daily.

**Cost verdict:** on an existing Prusa — **$30** (DIY Thingiverse extruder) to **~$100–165** (Funssor/Blurolls heads) to **€600** (StoneFlower 0.5 L ram kit) for the conversion; ~$1,700 only if building a dedicated Fungibot-style machine from scratch.

**Caveat to close the gap:** the exact spent-oats paste (moisture %, particle grind, whether to add the 1% xanthan) needs one bench iteration — the *class* is proven on coffee grounds and cat litter, but nobody has published the oats recipe. That's a $0 experiment, not a feasibility risk.

**Also verified:** both process orders exist — mycelium-in-paste (Blast Studio, Mycofluid) and print-then-grow (Mycelial Hut mold-cast). Our spec's "print lattice, then inoculate" is the *lower*-risk variant: a spawn-free paste prints cleaner, and post-print inoculation is standard bulk-substrate practice.

### Q2 — Can nutrient traces be printed as gradients? YES in principle, but discrete zoning is the proven hobby route.

- **Multi-paste hardware exists at every tier:** BCN3D+ dual paste extruder (open hardware, any paste ≤100 N extrusion force: https://bcn3d.com/dual-paste-extruder-last-of-the-upgrades-for-the-bcn3d/) · SPECS open-source multi-syringe pump extruder (https://www.hardware-x.com/article/S2468-0672(21)00004-3/fulltext) · 4-head hybrid paste/ink printer (2023: https://www.tandfonline.com/doi/full/10.1080/21870764.2023.2247210) · 5-material multinozzle precedent (Abilgaziyev et al.) · dual-extrusion soft-material system with flow-rate compensation (2025: https://www.researchgate.net/publication/389938228).
- **Mycelium-specific zoning precedent:** TU Delft demonstrated localized, region-independent functionalization within one living printed structure (gelatin masking + sequential particle addition); eCAADe 2021 multi-material mycelium composites exist (paper is bot-gated on CumInCAD — abstract-level only, flagged).
- **Post-print inoculation zoning** (our spec's own mechanism) needs no new hardware: print the lattice with zone voids, then hand-pack/inject different spawn or nutrient-laced pastes per zone. Blast Studio's stated next step — in-situ printing "inoculated with different varieties of mushrooms" — endorses exactly this direction.
- **Recommendation for the lattice:** v1 = zoned inoculation (discrete patches, syringe-applied, free); v2 = dual-paste head alternating trace-enriched and plain pastes (~$100–165). True continuous gradients = lab-tier (microfluidic mixing heads, twin-screw designs) and buys nothing for a multispecies lattice — species care about *where* zones are, not smoothness between them.

### Q3 — Hobby conversion path (Prusa-class, with links)

1. **$30 DIY entry:** Bricoleur open-source clay/paste extruder, files on Thingiverse — https://www.thingiverse.com/thing:1413969 (video: https://www.youtube.com/watch?v=Q3A4NqTPOYY)
2. **~$100–165 bolt-on heads:** Funssor worm-gear screw extruder kit — https://funssorlab.com/products/funssor-clay-paste-screw-extruder-system-upgrade-kit-worm-gear-pusher-motor-for-diy-ceramic-3d-printer-assembly-kit · Funssor paste/pellet head — https://funssorlab.com/products/clay-paste-pellet-extruder-for-3d-printer-ceramic-biomaterial-filament-extruder-nozzle-assembly-kit · Blurolls NEMA7 printhead — https://www.blurolls3d.com/products/blurolls-clay-paste-3d-printer-diy-printhead-ceramic-extruder-pellet-kit-nema7-motor-replaceable-nozzle
3. **~€490–600 complete kits (explicitly Prusa/Ender-compatible):** StoneFlower3D Basic Ceramic Kit 0.5 L, €600 — https://www.stoneflower3d.com/store/ceramic-3d-printing-kit/ · AliExpress Prusa i3/Ender 3 kit — https://he.aliexpress.com/i/1005012504192770.html · Amazon 500 mL syringe kit — https://www.amazon.com/Ceramic-Clay-Printer-Extruder-500ML/dp/B0GJRPTDQF
4. **Free plans/schematics:** CERA-1 — https://sites.google.com/site/openprojectspage/cera-1-clay-extruder · StoneFlower full-metal prototype schematics — https://www.stoneflower3d.com/projects/clay-extruder-prototype/ · Instructables Ender-3 conversion (maps 1:1 to a Prusa) — https://www.instructables.com/Ender-3-Clay-Printer-Conversion/
5. **Communities:** Prusa forum clay-extruder thread — https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-others-archive/is-there-a-clay-extruder-that-can-easily-be-attached-to-the-i3/ · r/Ceramic3Dprinting MK3S conversion — https://www.reddit.com/r/Ceramic3Dprinting/comments/1975r2j/prusa_mk3s_conversion/ · r/3Dprinting DIY extruder — https://www.reddit.com/r/3Dprinting/comments/4q9gl7/diy_clayconcrete_extruder_prusa_i3/ · HE3D kit assembly video — https://www.youtube.com/watch?v=KXiR0p5tgGs
6. **Slicer:** stock PrusaSlicer is sufficient — Mycofluid authors sliced paste prints with it (presets in their Supplementary S1, PMC12038323).

### Verification limits (honesty ledger)

- MDPI Biomimetics 8(2):257 and its encyclopedia.pub mirror returned 403 to WebFetch; europepmc 403; CumInCAD bot-gated; PMC10296363 timed out twice. The MDPI/Blast-Studio academic paper's parameters therefore rest on search snippets + secondary coverage, NOT full text. The parameter load of this receipt rests on PMC12038323 (Mycofluid), which was fetched in full.
- Cambridge 2026 "Rooted in waste" PDF could not be fetched (application/pdf unsupported) — title/venue/finding from search result metadata only.
- Spent-oats paste recipe specifically: unproven in literature (class proven; exact recipe = one bench iteration owed).
- WebSearch rate-limited (429) repeatedly; all searches eventually landed on retry.

### Sources

Mycofluid (PMC12038323) · MDPI Biomimetics 8(2):257 / PMC10296363 · Blast Studio (site, Dezeen, 3DPI, 3D Natives, Untapped, Medium, YouTube ×3) · TU Delft AFM 2025 via Mycostories · Mycelial Hut via designboom + VoxelMatters · Cambridge 2026 · StoneFlower3D · Funssor ×2 · Blurolls · AliExpress · Amazon · Ubuy · Prusa forum · Reddit ×2 · Instructables · YouTube ×4 · BCN3D · HardwareX SPECS · T&F 2023 · ResearchGate ×2 · WASP · Biogenic Architecture · Henning Larsen · eCAADe 2021 · Mycostories (binder jetting) — all URLs inline above.

**Bottom line: G-I CLOSED. Printable — paste recipe class proven on waste grain analogs, Prusa-class + $30–600 paste head, gradients practical as zoned inoculation (v1) or dual-paste (v2), continuous gradient unnecessary at hobby tier.**

