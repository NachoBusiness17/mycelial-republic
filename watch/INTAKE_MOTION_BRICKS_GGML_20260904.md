# INTAKE CARD — MOTION-BRICKS.CPP: NVIDIA MOTION PRIOR ON GGML/CPU (item, 2026-09-04)

## ITEM
Operator flagged **!tesuji** (suspected skillful local move): https://x.com/jichiep/status/2095157236658315288?s=20
Richard Palethorpe (@jichiep; LinkedIn richiejp), posted 2:29 PM Sep 2, 2026 — 53.4K
views / 18 replies / 79 RT / 623 likes / **605 bookmarks** (bookmarks ≈ likes =
latent-demand signal, same census shape as the uzu card). Verbatim claims:
"I put motion-bricks.cpp up on GitHub! It generates animations from key-frames
in realtime using a tiny model that easily runs on a desktop CPU and Vulkan.
There are still bugs to iron out and I'm thinking this can be combined with
physical simulation and robotic control policies..."
Thread (fetched whole, not root-only): author reply links the repo
(localai-org/motion-bricks.cpp, "NVIDIA MotionBricks ported to GGML/C++", 37
replies on that reply); author livestream replay "MotionBricks to C++/GGML part
2: it works?"; reply from @miloashfog asking "is there a connection between
them?" linking NVlabs/GR00T-WholeBodyControl — the answer is yes, and the
connection IS the tesuji (see TESUJI ANALYSIS).

## RECEIPTS (consult-first, this turn — thread + repo + upstream, all fetched)
- Repo existence + mechanics **Supported**: github.com/localai-org/motion-bricks.cpp
  fetched this turn — 101 stars, 8 forks, 7 commits, no releases yet. C++23/GGML
  port "for CPU and Vulkan inference, with a stable C ABI suitable for PureGo".
  Full G1 pipeline end-to-end: GGUF loading → root/duration planning →
  pose-token prediction → VQ decoding → feature conversion → style alignment →
  animation output. Skeleton = Unitree G1's 34 joints ("intended for games or
  robotics"). CPU and Vulkan paths claimed to match reference results (author
  claim, source not read — Unproven).
- Weights **Supported**: MotionBricks-G1-GGML on HF, GGUF F32, ~0.73 GB,
  exactly 183,148,382 params, SHA-256-verified + pinned HF revision; loader
  validates revision/tensor counts/joint topology. Arithmetic check PASSED:
  183,148,382 × 4 bytes ≈ 0.73 GB — internally consistent.
- Conversion path **Supported**: NVIDIA checkpoints (Git LFS in
  NVlabs/GR00T-WholeBodyControl) → safetensors → convert_to_gguf.py +
  convert_styles.py (15 style primitives, .mbstyle).
- License **Supported**: source Apache-2.0; weights NVIDIA Open Model License
  (commercial use with attribution + Trustworthy AI terms) — usable, not
  unencumbered.
- Upstream **Supported**: nvlabs.github.io/motionbricks (SIGGRAPH 2026 / ACM
  TOG): 15,000 FPS / 2 ms latency / 350,000+ motion skills / one backbone;
  BONES-SEED dataset (142K+ motions, ~288h production mocap); "core organic
  component of NVIDIA's GR00T Whole-Body Control"; controls a real Unitree G1;
  UE5 authoring "with no animation graphs"; zero-shot transfer claimed.
  Note: 15K FPS is batched throughput, 2 ms is single-stream latency — headline
  conflates them if quoted carelessly; both internally consistent.
- "Realtime on a desktop CPU" **Unproven by us** — author claim + livestream
  titled as a question; no independent FPS number exists on any desktop CPU in
  this card. Kill condition written below.
- Scope **Disputed as general**: README limitations — covers "original
  preprocessed G1 styles" only; direct Kimodo GLB→.mbstyle conversion explicitly
  deferred. This is not a general animation model today.
- Author identity linkage (X @jichiep = the repo author) Supported via author's
  own thread reply + same-author livestream; X→GitHub account mapping not
  separately verified (not load-bearing). Why the port lives under localai-org:
  **Unproven** (org affiliation story not traced).

## SCORE — F:2 P:3 C:5 W:3 N:4 = **17/25 → BUILD WINDOWED**

## READ (the honest why)
FIT 2: no standing organ consumes skeletal animation today — room_game.html and
maze_arena.html walkers are abstract fields, tale-re-encoder is text, the bay
speaks GGUF for LLMs only. This is a new organ TYPE (motor prior), and the
desk-GPU-history lesson (designed-but-never-wired) caps FIT for anything
without a consumer. PULL 3: it touches three live arcs — the trajectory-as-token
thesis (Trajectory-RIB compiler spec gets an external third-domain witness:
NVIDIA packages motion trajectories as first-class latent tokens a tiny model
generates), Rocinante Oct 27 (GGUF, 0.73GB F32, GGML/Metal family — this runs
in the palm of an M5 Ultra), and the dungeon content pipeline ("harvest = NPC
minds" was filed; this is the missing twin: NPC BODIES). Not on this week's
critical path — the QLoRA campaign order is locked on cloud lanes — so PULL
stays 3. COST 5: $0 to file, $0 to run later (Apache code, free-pull weights,
warm GGML box, no GPU required). WINDOW 3: nothing decays except stars
rising; the natural dock is the Oct 27 package lane or the day a dungeon
surface asks for bodies. NOVELTY 4: corpus sweep (memory index + watch/ shelf)
found zero motion/animation/robotics-skeleton entries — not a re-find; the
uzu card is the nearest neighbor (engine-on-GGUF-adjacent-substrate) but that
is LLM spec-decode, this is motion.

## TESUJI ANALYSIS — FOUND (with reasoning)
Surface read (not the tesuji): "a guy ported a model to llama.cpp-style
runtime." The skillful local move is one level down:
1. **The skeleton is the tell.** The port animates the Unitree G1's 34-joint
   skeleton — the SAME skeleton GR00T uses to control the real humanoid. NVIDIA
   shipped one latent motion backbone serving BOTH game animation AND robot
   whole-body control; the solo port makes that backbone run on GGUF/CPU.
   Therefore: game NPC bodies and robot motor skills are THE SAME ARTIFACT.
   The fleet already filed "harvest = NPC minds" (game codex); this is
   "harvest = NPC bodies" — one motor organ, two consumers (dungeon gophers,
   any future embodied fleet), $0.
2. **Third-domain witness for the core thesis.** The Trajectory-RIB compiler
   spec (08-27) recorded witness C confirming "no paper/product packages
   trajectories with acceptance commands first-class." MotionBricks is NVIDIA
   doing exactly that for MOTION: trajectories as first-class tokens
   (pose-token prediction, root/duration planning), tiny backbone, 350K skills.
   The fleet's "quantization for thought" is not a conjecture anymore — it is
   shipping in three domains (our text RIBs, NVIDIA motion, and GGML itself).
3. **The C ABI + PureGo choice is a second quiet move.** He compiled the prior
   small enough to be CALLED AS A LIBRARY from ordinary software, not run
   through an ML stack. That is the fleet's own "dumb bodies code for pennies"
   doctrine, inverted: the intelligence is the pennies. F32-GGUF (0.73GB) also
   means quantization headroom remains — "tiny" is the ceiling, not the floor
   (Q8 ≈ 0.18GB, Q4 ≈ 0.09GB).
Anti-tesuji honesty: if the operator expected something deeper than the
animation↔robotics unification, this pass did not find it — and the second
candidate (the localai-org placement of a kernel engineer's graphics-ML port =
signal that GGML is eating non-LLM inference from the systems direction) is
**Unproven**, an affiliation story the thread does not settle. The tesuji
verdict above stands on the skeleton tell and the third-domain witness alone.

## DOGFOOD
1. **INVARIANT PASS**: reinforces the trajectory-token thesis (third external
   witness, new domain); reinforces receipts-in-code (the loader validating
   pinned revision + tensor counts + joint topology is our hash-chain
   discipline appearing in a stranger's port); reinforces cheapest-lane routing
   (CPU realtime = the pennies lane for motion). No contradictions with known
   laws. One tension filed: "dumb bodies are cheap" gains a new cost class
   (motor priors) the economist has never budgeted — harmless until embodied.
2. **STOCKFISH PASS**: consuming lane/opcode = the DUNGEON content pipeline
   (NPC bodies) + Rocinante Oct 27 manifest (probe card). It does NOT go on the
   QLoRA campaign path (locked order; a motor prior is a distraction there).
   Placement succeeds only as: (a) pinned card + kill-condition probe in the
   Oct 27 package lane, (b) dungeon NPC-body organ queued BEHIND a consumer
   surface that asks for bodies. If no surface ever asks, the correct
   disposition was REMEMBER — that is the falsifiable placement.

## TRI-STATE (final)
- Repo exists as described (GGML/GGUF, CPU+Vulkan, C ABI, 183M/0.73GB pinned) —
  **Supported** (github.com/localai-org/motion-bricks.cpp, fetched 2026-09-04).
- Upstream MotionBricks facts (15K FPS/2ms/350K skills/GR00T core/BONES-SEED) —
  **Supported** (nvlabs.github.io/motionbricks + NVlabs/GR00T-WholeBodyControl).
- Runs realtime on a desktop CPU — **Unproven** (author claim; kill condition
  below).
- General animation generation (any rig, any style) — **Disputed**; Supported
  only inside G1 skeleton + 15 preprocessed styles (README limitations).
- Combinable with physics sim / robot control policies — **Unproven** (author
  forward-intent; upstream GR00T does control a real G1, but the GGML port has
  no sim/control integration yet).

## VERDICT
**BUILD** (windowed): pin the card into the Rocinante Oct 27 package lane and
write the kill-condition probe TODAY, zero code until a consumer exists:
BUILD motion-bricks.cpp on the hands box (GGML CPU backend already warm there),
pull MotionBricks-G1-GGML at the pinned SHA, run the G1 pipeline on a keyframe
task. **PASS** = ≥30 FPS single-stream, pose output within visual tolerance of
reference → the motor-prior organ earns a dungeon slot. **FAIL** = the
desktop-CPU-realtime claim dies, item drops to REMEMBER with receipt. Next
seat can execute this cold from this card.

## ROUTE
Wire: yes, one pointer — Oct 27 package builder lane gets this card; dungeon
content-pipeline queue gets the NPC-body organ as CONSUMER-GATED (do not build
before a surface asks). No driver interrupt; QLoRA campaign untouched. Typed
room.jsonl row left to the main thread per Amendment 1 (spawn holds no path).
One-line room receipt: `intake.motion_bricks_ggml: 17/25 BUILD-WINDOWED —
tesuji FOUND (G1 skeleton = NPC bodies ≡ robot motor skills, one $0 motor
prior); probe card cold-executable; campaign untouched` (2026-09-04).

## THE CROP (what this pass did not see)
Never ran the model — no FPS number on ANY desktop CPU exists in this card.
Did not read the port's source (README-level only): "CPU and Vulkan paths match
reference results" is the author's word. Did not dissect the architecture paper
(arXiv 2604.24833) — the pose-token/VQ internals would decide how expensive
retargeting off the G1 skeleton really is, which is exactly how narrow the
15-style cage is. The localai-org affiliation story is unproven. Next chair:
the hands-box seat (run the probe) or the research lane (paper dissection for
retarget cost).
