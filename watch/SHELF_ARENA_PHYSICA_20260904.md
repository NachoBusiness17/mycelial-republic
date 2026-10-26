# SHELF: Arena Physica sweep — 2026-09-04

$0 reconnaissance sweep. Provenance: fleet steering-map line (Smith chart → Möbius transforms → nomogram-as-instrument) traced to this site's Smith chart article. Mission: full catalog, triage for nomogram/instrument-class physics explainers.

## Site identity — VERIFIED

**Arena Physica** (https://www.arenaphysica.com/) — NYC-based (HQ NYC; SF, LA satellites) AI company building "electromagnetic superintelligence": foundation models for electromagnetics. Products: **Heaviside-1** (foundation model for 3D EM fields, announced 2026-09-01), **Atlas Fields Studio** (Beta, live 3D field viewer: https://fields-studio.arenaphysica.com), **Atlas RF Studio** (Beta, agentic RF design sandbox: https://rf-studio.arenaphysica.com/rf). Founded/led by Pratap Ranade. Company belief on record: "big believers in using visualizations to build intuition" — that is why the Smith chart article exists and why it is their logo.

## Catalog — VERIFIED (publications index + news page 1)

| # | Title | Date | URL | Class |
|---|-------|------|-----|-------|
| 1 | What is a Smith Chart? (Christopher Bryant, ~21 min) | 2026-07-10 | arenaphysica.com/publications/smith-charts | **(a) NOMOGRAM/INSTRUMENT-CLASS** |
| 2 | Introducing Atlas RF Studio: Toward a Foundation Model for Electromagnetics | 2026-04-01 | arenaphysica.com/publications/rf-studio | (b) mechanism/technical deep dive |
| 3 | Introducing Heaviside-1 | 2026-09-01 | arenaphysica.com/publications/heaviside-1 | (b) product/mechanism |
| 4 | Inverse Design of Multi-Layer Sub-Pixel-Resolution RF Passives | 2026-05-06 | arxiv.org/abs/2605.08233 | (b) research paper |
| 5 | Converting Compute into Performance in a Data-Constrained World | 2026-05-06 | arxiv.org/abs/2605.09189 | (b) research paper |
| 6 | "In the Arena" interview series (6 on page 1: Boyuan Zhang, Tony Leapo, Catherine Kauber, Julian Ozen, Ruichen Zhao, Roberto Riganti; series continues through the archive) | Jul–Aug 2026 | arenaphysica.com/articles/in-the-arena-* | (c) filler (team profiles) |
| 7 | Not Boring: "Electromagnetism Secretly Runs the World" (Packy McCormick) | 2026-03-24 | notboring.co/p/electromagnetism-secretly-runs-the | external media, unread |
| 8 | TBPN livestream appearance | 2026-04-03 | youtu.be/i7N_-ctMQgI?t=7297 | external media, unread |

Plus two live tools (not articles but instrument-adjacent): Atlas Fields Studio, Atlas RF Studio.

## Anchor article anatomy — VERIFIED (deep read)

"What is a Smith Chart?" is the genre specimen the steering-map line traced to:
- Explicitly names Γ = (z−1)/(z+1) a **Möbius transformation** folding the right-half impedance plane into the unit disk.
- Frames the chart as a **graphical calculator** ("compass and ruler" nomogram), then shows its computational obsolescence and its surviving role as an intuition instrument — exactly the nomogram-as-instrument arc.
- Interactive set, steal-worthy as a template: rope-pulse reflection demo; dual-plane draggable dot (impedance ↔ Γ panes linked); transmission-line probe (Γ rotating on constant-|Γ| circle); filter explorer (Chebyshev/Butterworth, ladder + Smith + S-param, sliders); **matching-network mini-game** (drag L/C/line into series/shunt to match a random load); 3D chart-inflates-into-sphere animation for |Γ|>1; collapsible derivations.
- Pedagogy: physical analogy → formalism → direct manipulation → design problem. Explicit mission tie: the chart "encodes expert intuition," and they are building "artificial intuition."

## Top 3 for fleet composition (steering maps, operator-field arenas, Mars-desert surfaces)

**1. "What is a Smith Chart?"** — the anchor and still the best template. Its build order (map the transform, make both planes draggable, end in a mini-game that makes the reader solve by construction) is a direct recipe for any fleet steering-map surface. Nothing else on the site is this class.

**2. Atlas Fields Studio (live tool, https://fields-studio.arenaphysica.com)** — interactive 3D EM near-field viewer, parameter controls, sub-second full-field prediction (Heaviside-1). Composes directly with operator-field arenas: grad/div/curl/laplacian cells want exactly this — a live field instrument you scrub. Beta, free to poke.

**3. "Atlas RF Studio" deep dive (/publications/rf-studio)** — the thesis "train on the cause (fields), not the effect" plus data-factory mechanics. Feeds the steering-map theory layer (maps as learned instruments, fields as ground truth signal) and gives bones to steal for any fleet field-model arc. Honorable mention: the Inverse Design arXiv paper (grayscale diffusion + S-parameter conditioning) — relevant only if the fleet ever does inverse-designed hardware.

## Tri-state ledger

- **Supported**: site identity; full publications index (5 entries, exhaustively listed); news page-1 inventory; smith-charts article content incl. interactive inventory; research-page contents; two live Beta tool URLs.
- **Unproven**: news archive pages 2–6 (~37 remaining items). Pagination did not resolve via fetch (?page=2 returned page 1); classified as interview profiles by cadence (6 profiles in 3 weeks, Aug 2026, series continuing) — low risk they hide instrument-class content, but not directly verified.
- **Unverified (out of $0 scope)**: Not Boring essay body; TBPN video; the two arXiv papers (abstracts only via catalog); whether Fields/RF Studio Betas require signup.
- Note: the Möbius-transform framing is IN the anchor article (verified by direct fetch), not just fleet folklore — the steering-map lineage is confirmed at the source.

## Disposition

Site is a company blog, not a physics-explainer catalog: one instrument-class article (the anchor), two product deep dives, two arXiv papers, a long interview tail. Sweep complete — no second nomogram article exists on the shelf. The durable steals: the anchor's interactive-build order, and Fields Studio as a live-field instrument reference for the arenas.
