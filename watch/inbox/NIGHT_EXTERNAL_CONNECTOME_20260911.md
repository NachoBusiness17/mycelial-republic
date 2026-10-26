# NIGHT EXTERNAL SCAN — the connectome-compute ecosystem (2026-09-11)

*Wave protocol night run, external lane. Feeds F-FLY1 (watch/inbox/FLY1_QUEUED_20260911.md).
Verdict up front: the public proof is real, open source, and MIT — the whole IO loop
we need to borrow already exists under a license we can lift whole. Our version
swaps the substrate, not the loop.*

## THE ECOSYSTEM TABLE

| Project | What it is | Open source? | License | F-FLY1 can borrow? |
|---|---|---|---|---|
| FlyWire / codex.flywire.ai | The data layer. Five public datasets: FAFB v783 (female brain, 139,255 neurons / 3.7M connections), BANC v888, MANC v1.2.1, MAOL v1.1, **MCNS v1.0 (male full CNS, 166,700 neurons / 6.2M connections)** — the Doom-proof dataset. Download via the "Download Data" app; Google sign-in, ToS gate. | Data public, code of the explorer partial | Not stated on codex page (Unproven — community norm for FAFB is CC BY 4.0, verify before any redistribution; doomfly README confirms data carries its own license) | YES — ground-truth input for the replication baseline |
| **nftechie/doomfly** (github.com/nftechie/doomfly) | The public proof, as code. ViZDoom frames → 3,335 R1–R6 brightness + 811 R8 color sensory inputs → full-graph sim (166,700 neurons, 25,582,938 directed connections, no cropping) → fixed neuron-to-button map: DNp20 = turning, DNpe017 = move/fire. Damage = 200 ms aversive pulse into two PPL101 dopamine cells; plasticity touches only 4,184 KC→MBON11 connections. C++ kernel, importer (`doom/connectome.py`), SHA-256 data provenance, negative results published. | YES | MIT (code; data/art keep own licenses) | YES — this is the loop, whole |
| Alex Wormuth's Doom run + Jessica Paquette's Super Mario 64 (Tom's Hardware, 2026-09-06/07) | The viral moment behind the proof. MaleCNS v1.0 mapped 2026-09-03 by Google + Janelia. Note: Tom's Hardware names Alex Wormuth (account "cantworkitout"); our FLY1 card cites @nftechie_ — same project, handle mapping Unproven but the repo content matches exactly (PPL101, 166,700). | Wormuth "fully open source" per article | MIT via doomfly repo | Context only |
| FlyGym / NeuroMechFly v2 (github.com/NeLy-EPFL/flygym, neuromechfly.org) | Embodied digital twin of the fly on MuJoCo: micro-CT body, hexagonal compound-eye vision, olfaction, leg adhesion. Brain-level controller slots in via descending/ascending interfaces. v2.x (Mar 2026) rewrite: ~10x CPU, ~300x GPU. | YES | Apache-2.0 | YES — if our rooms get a fly body |
| Flyvis (github.com/TuragaLab/flyvis) | Connectome-constrained PyTorch model of the fly OPTIC LOBE (Lappalainen et al., Nature 2024). Takes image/frame stimuli, predicts internal neural responses. On PyPI. NOT a controller — no action outputs. | YES | MIT | Partial — stimulus→response reference, optic lobe only |
| desktop-fly (github.com/DenisSergeevitch, HN thread news.ycombinator.com/item?id=49353221) | 3D fly wandering a macOS desktop on real FlyWire data, 1 kHz LIF sim; looming stimulus → LC4 neurons → giant fibers = the real fly escape circuit. | Yes (repo public) | None stated (Unproven) | Pattern only — its HN critics say behaviors are scripted triggers; its escape mapping is exactly our falsifier's template |
| gnat (github.com/lubabs770/gnat) | Community Linux port of the desktop-fly idea. | Yes | Not verified | Thin |
| OpenWorm (openworm.org) | The OG: C. elegans, 302 neurons, open embodiment lineage since 2013. | YES | Open (per project) | Lineage only |
| Infinite Pain | Deterministic C. elegans sim subjected to regular pain stimuli (art piece, instagram.com/p/DMfi-9Vsl-u). | No repo surfaced | Unproven | Concept: damage-as-stimulus, which doomfly already implements |
| Eonsys / "Open Brain Institute" | ~125K-neuron simulated fly video (r/singularity thread), open-source claim only. | Unproven | Unproven | No |
| arXiv 2508.16792 | "Neuromorphic Simulation of Drosophila Melanogaster" — FlyWire connectome on neuromorphic hardware. | Paper | — | Reading list |

## THE 3 BORROWABLE TOOLS

1. **nftechie/doomfly (MIT) — the loop.** Connectome importer, whole-graph simulator with native kernel, and the two contracts we care about: frames→sensory indices, fixed neuron→button map. MIT means we lift the contracts and the loader with attribution. Its honesty section is a gift: "engineered controller assignments, not established natural motor functions," and its v6 learning candidate FAILED its own validation gates — the public proof is that the brain DRIVES the game, not that it LEARNS. Our falsifier was written against exactly that.
2. **FlyGym / NeuroMechFly v2 (Apache-2.0) — the world, if embodied.** Vision + odor in, joint forces out, fast as of the March 2026 rewrite. Use only if F-FLY1 needs a fly-shaped body in a physics world; our rooms are 2D, so likely optional.
3. **Flyvis (MIT) — the retina-to-activity machinery.** Pip-installable, accepts custom frame stimuli, maps to optic-lobe activity. Borrow if we want a lighter front end than the whole 166k graph for the frame→activity stage.

Pattern worth stealing from desktop-fly even without its code: the 1 kHz LIF scheme is simple enough to clean-room in an afternoon, and its looming→LC4→giant-fiber escape mapping is a published-shaped template for an escape-rate falsifier.

## F-FLY1 RECOMMENDATION — fastest lawful path

The insight from the scan: **the external projects all share one shape — data (connectome) → sim kernel → world (game) → fixed IO contract → damage/stimulus channel.** F-FLY1 keeps every organ and swaps only the data layer: our recorded behavior volume (quantized agent sessions — orc transcripts, ghost trail, chain) stands where the connectome stands. That is the reinterpretation to name.

Fastest path, in order:

1. **Clone doomfly (MIT), do not fork-and-skin.** Steal `doom/connectome.py` (graph loader), the frame→sensory-index encoder, and the fixed neuron→action contract shape. Build our own adapter: behavior-volume-loader where the MaleCNS importer sits.
2. **Swap the arena: ViZDoom → our maze_arena.** Two birds: avoids Doom trademark exposure entirely (doomfly explicitly grants none), and maze_arena already exists and was fixed on 09-06. Our rooms as the world — already built.
3. **Run two substrates for the falsifier:** (a) MCNS v1.0 baseline — proves our loop matches the public proof; (b) recorded-behavior-volume substrate — our version. Attractor-move = our PPL101-equivalent aversive signal; escape rate = the metric. Falsifier stands unchanged: attractor-move changes escape rate.
4. **Data legality:** MCNS v1.0 via codex.flywire.ai "Download Data" app (free, Google sign-in). License not stated on the codex page — verify before ANY redistribution; internal research use is the community norm. Never ship the raw dataset in a repo; ship the loader + SHA-256 provenance, exactly as doomfly does.
5. **Honesty rails to keep from day one** (learned from doomfly's negative results and the HN critique): label the attractor→action mapping as engineered, not natural; publish controls; "runs" ≠ "learns" — the public proof itself never demonstrated learned survival.

Effort read: the IO contract and kernel exist under MIT; the real build is the behavior-volume loader and the arena adapter. This is a HOLD-2-shaped task: finite public data, no keys, no cost, clear falsifier.

## RECEIPTS (URLs)

- Repo (public proof as code): https://github.com/nftechie/doomfly
- Data layer: https://codex.flywire.ai/api/download and https://flywire.ai/
- Press: https://www.tomshardware.com/software/programming/google-maps-entire-brain-and-central-nervous-system-of-adult-male-fruit-fly-software-engineers-immediately-make-it-run-doom-ai-powered-3d-model-of-over-166-000-neurons-can-also-play-super-mario-64
- Google's connectome milestone: https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/
- Skeptics' thread: https://news.ycombinator.com/item?id=49353221
- FlyGym: https://github.com/NeLy-EPFL/flygym (docs: neuromechfly.org)
- Flyvis: https://github.com/TuragaLab/flyvis
- Neuromorphic sim paper: https://arxiv.org/abs/2508.16792
- Nature FlyWire collection: https://www.nature.com/collections/hgcfafejia
- OpenWorm lineage: https://www.theatlantic.com/technology/archive/2013/05/is-this-virtual-worm-the-first-sign-of-the-singularity/275715/
