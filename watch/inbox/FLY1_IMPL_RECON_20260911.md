# FLY1 IMPL RECON — deeper than the scan (2026-09-11, wave slot 6)

*Follows watch/inbox/NIGHT_EXTERNAL_CONNECTOME_20260911.md + FLY1_QUEUED_20260911.md.
This is the implementation recon: repo verified first-hand, license question chased to
the ToS, our arena read line-by-line for the plug points. Verdict up front: the loop
is liftable under MIT, the data is downloadable under NC-worst-case terms, and
maze_arena already has the exact door the connectome plugs into (MODEL SEAT). The
real build is two loaders and one headless harness. The falsifier needs zero edits.*

## 1. DOOMFLY — verified at source (github.com/nftechie/doomfly, repo + raw README)

- **License: MIT, CONFIRMED.** Exact wording: "Original DOOMFLY code is MIT licensed."
  "Data, game artwork and copied components retain their own licenses" (THIRD_PARTY.md).
  "Independent research project, unaffiliated with and not endorsed by id Software,
  Bethesda or ZeniMax." "No trademark rights are granted." → our ViZDoom→maze_arena
  swap also removes the entire Doom trademark/artwork surface. Clean.
- **Frame→sensory contract:** each ViZDoom frame drives **3,335 R1–R6 brightness
  inputs + 811 R8 color inputs** (4,146 channels total). Pixel positions and color
  responses are "inferred proxies." The exact input registry lives in `doom/datasets.json`;
  no resolution or timestep stated in the README (read the kernel at clone time).
- **Neuron→button map (fixed, explicit):** **DNp20 right-minus-left activity → turning;
  DNpe017 activity → movement and firing.** README's own caveat, which we adopt as law:
  "engineered controller assignments, not established natural motor functions."
- **Damage channel:** 200 ms aversive pulse into **two PPL101 dopamine cells**; plasticity
  touches only **4,184 KC→MBON11 connections**; everything else frozen.
- **Scale:** 166,700 retained neurons, 25,582,938 directed connections, no circuit
  cropping, no replacement-game policy.
- **Honesty rails (published negative result, a gift):** "live experimental training,
  not demonstrated learned survival" — the v6 candidate FAILED its visual, conditioning
  and survival validation gates. The public proof is "brain DRIVES the game," never
  "brain LEARNS." Our falsifier was written against exactly this line.
- **Compute/deps:** Python 3.11 + a C++ compiler; full graph needs "several GB of RAM";
  does not run in a browser or edge function; viewer needs Node 22.13+. Three MaleCNS
  data files per `doom/datasets.json`, verified against
  `data-provenance/malecns_v1/source.lock.json` SHA-256 digests; the download script
  checks every digest before import — steal this provenance pattern whole.
- **Repo shape:** `doom/` (kernel + ViZDoom interface + `connectome.py` loader),
  `doom_learning_v1..v6/`, `doom-ui/`, `tests/`, `data-provenance/`, `licenses/`.
  Five commits on main. FlyWire is never named in the README — the data trail runs
  through datasets.json + source.lock.json instead.

## 2. FLYWIRE MCNS v1.0 — download terms, license verdict

- The scan's URL (`codex.flywire.ai/data_access`) 404s. The live page is
  `codex.flywire.ai/api/download`. It lists five datasets; **MCNS v1.0 = Male Adult Fly
  Brain and Nerve Cord, 166,700 neurons / 6,242,118 connections** — the Doom-proof set.
  Download via the "Download Data" app; **Google sign-in required** (stated rationale:
  abuse/rate-limit/server load); one human step, no keys, no cost.
- **License chase (the scan's UNPROVEN, now narrowed):** the codex page states NO data
  license and defers to flywire.ai/tos. Fetched the ToS: the only explicit license
  clause covers **cell edits and annotations** — "will be made freely available under a
  **CC-BY-NC 4.0** license." No bulk-dataset license section appears on either fetched
  page; a "Citation Guidelines" link exists but its content was not retrievable in this
  pass. Tri-state:
  - "MCNS v1.0 is CC BY 4.0" (community norm the scan repeated) → **DISPUTED**: the only
    explicit FlyWire license wording found is the **NC** variant.
  - "Internal research use, no redistribution, is safe" → **SUPPORTED**: download app is
    public and free, the ToS gates abuse not research, and the NC worst case still
    permits non-commercial research.
  - "Exact license of the bulk files" → **UNPROVEN, one fetch away**: read the Citation
    Guidelines page before ANY redistribution decision. Required at build time.
- **Operational law regardless of the final wording:** never ship the raw dataset in any
  repo; ship the loader + SHA-256 provenance lock — verbatim the doomfly pattern.
- **Discrepancy to resolve at import:** FlyWire says 6,242,118 connections; doomfly's
  README says 25,582,938 directed connections retained. Almost certainly
  connection-vs-synaptic-contact counting (or multiplicity expansion). The importer
  decides; affects RAM/speed modestly, not the design. Log it, don't fear it.

## 3. MAZE_ARENA — the interface the connectome plugs into

Read: `dashboard/static/maze_arena.html` (the 09-06-fixed M2 build; four .bak siblings
in place). Facts that matter for FLY1:

- **World:** 240x135 logical grid (480x270 canvas @2x), SDF walls (10 interior boxes +
  bounded outer walls), cheese beacon → BFS lightmap (Float32Array 240x135, full rebuild
  ~17 ms, frame-budgeted), optional odd-eta handed curl, three rounds (R1 race / R2
  moving walls with dirty-radius refill / R3 walking beacon + gaze law), wall invariants
  (GOLD) vs movers (CYAN). "The red assumption hunts in the dark" — a predator already
  exists in the room.
- **Plug point 1 — MODEL SEAT (already built, zero engine changes):** external brains
  drive an agent by move-list JSON: `{"round":2,"moves":[3,3,4,0,[0.31,1.02]]}` — ints
  0..7 are compass dirs (0=E, CCW, θ=i·π/4), [x,y] pairs are waypoints. The connectome
  brain emits one move per tick through this door. Demo-grade (browser rate).
- **Plug point 2 — headless harness (where the real falsifier runs):** extract SDF +
  lightmap + agent tick into a Node (or Python port) loop, close it with the Python sim
  at tick rate, run hundreds of episodes for escape-rate statistics.
- **Frame→sensory adapter:** maze frame (walls + lightmap rendered at 240x135) →
  doomfly-shaped encoder → 4,146 retinal channels. Our grid is smaller than a Doom frame;
  the downsampling is if anything cleaner.
- **Aversive channel:** predator proximity = our PPL101-equivalent pulse / the attractor
  signal. The damage semantics translate; the neurons are the ones that change.
- **Escape metric:** arena falsifier already on the page ("does the field beat the
  bounce") + F-FLY1's falsifier verbatim: "a player must change the escape rate by
  moving ONE object, blind to doctrine." The attractor-move IS the one object moved.
- The error-banner fixture (added 09-06) is present — keep it for the new brain agent.

## 4. THE LIFT PLAN

**Take from doomfly (MIT, with attribution):** `doom/connectome.py` graph loader; the
frame→4,146-channel encoder shape; the fixed neuron→action contract shape (DNp20
right-minus-left → steering bias, DNpe017 → forward move); the SHA-256 provenance lock
pattern; the honesty rails; the negative-results habit.

**Swap to ours:** world ViZDoom → maze_arena (headless for stats, MODEL SEAT for the
demo); action space Doom buttons → compass move-list 0..7; damage → predator-proximity
aversive pulse; baseline agent → the dumb-bounce walker already in the arena.

**Two-substrate run, one falsifier:**
- **Arm A (MCNS baseline, replication):** MaleCNS v1.0 brain in maze_arena via the
  doomfly loop unchanged except the world adapter. Proves our harness reproduces the
  public proof's shape.
- **Arm B (our substrate):** identical IO loop; where the MaleCNS importer sits, a
  behavior-volume loader — the quantized agent sessions (spec: 9,305 thinking-parts of
  5.3-flash, byte-verified to the GGUF specimen, sha 5ee4f07c, per
  watch/SHADER_PIPELINE_RESEARCH_20260908.md). Same frames in, same action contract out.
- **Shared falsifier, unchanged:** plant ONE attractor, blind to doctrine; measure
  escape-rate delta with vs without. Registered prediction BEFORE the runs. Arms: no-
  attractor, attractor, shuffled-attractor control, dumb-agent floor. In both substrates.
- **Honesty rails day one:** label all mappings engineered; "runs" ≠ "learns"; publish
  controls and negative results — doomfly's own v6 failure is our template for how to
  lose honestly.

**Named gates before build:** (1) Google sign-in through the FlyWire Download Data app
(human step); (2) MCNS bulk files are not on the host tree — and neither is the GGUF
specimen (no *.gguf in the repo; corpus law says CAGE-ONLY) — substrate B's loader needs
a cage export or manifest path; (3) Citation Guidelines fetch before any redistribution;
(4) doomfly kernel timestep read at clone time.

## 5. COMPUTE ESTIMATE

- **RAM:** "several GB" full graph (doomfly's words); budget 8 GB peak, single job at a
  time on a small machine ("do not run many full-graph jobs concurrently").
- **CPU/time:** sparse ~25M-synapse propagation per tick behind a C++ kernel. One maze
  episode = 900–1500 ticks (15–25 s world time @60 fps). Even at a pessimistic ≥1x
  real-time, the study — 2 arms × 3 conditions × ~30 episodes ≈ 180 episodes — lands in
  single-digit CPU-hours on one core. No GPU. The mag container (Linux) is the cleaner
  home for the Python 3.11 + C++ build than MSVC on the host.
- **Disk:** three MaleCNS files; not sized precisely upstream — budget ~5 GB, cage-side.
- **Cost:** $0 model tokens for the sim itself; loader code belongs on the free lanes;
  premium tokens touch only judgment (falsifier design, verdicts).

## CYCLE GENETICS

Inherit the CONTRACT, not the corpse: doomfly's loop under MIT, FlyWire's data under
NC-worst-case discipline, maze_arena's MODEL SEAT as the socket — the falsifier needed
zero edits, only two substrates willing to stand in front of it; whatever fails next
cycle fails honestly and gets published anyway.
