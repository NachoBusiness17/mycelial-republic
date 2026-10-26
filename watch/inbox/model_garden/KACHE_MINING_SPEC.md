# KACHE MINING SPEC - positions in WEIGHT space (2026-10-02)

**Schema:** kache.spec.v1 · **lane:** KACHE-1 · **status:** spec + first experiment (E1) firing
same session per the operator upgrade ("now thats our moonshot we need run").
**Mission (operator, verbatim bones):** "this was originally my idea behind kache mining -
physically tracking our positions within model weights, comparing them against each other using
memlance and our local weights on disk, allowing us to then actually stage things inside the
shape of ideas."
**Method:** bytes-first. Every claim names the file read this session. Local assets read live:
`ollama list` (17 models, moment 2026-10-02T01:1xZ), the GGUF blobs under the ollama store,
the OBLITERATUS drop receipt, the memlance skill + organs, tonight's field-theory pair.
No commits; venv interpreter only; budget cap $2 for the whole lane (E1 is $0 local).

## 0. THE GENERALIZATION (one paragraph)

Tonight's GPS/field-theory work (STEERING_FIELD_THEORY.md, COLD_VERTEX_LAYER.md) tracks
position in SURFACE space: which file, which ledger cell, which task-shape coordinate the
estate's attention sits on, with pass_rate as elevation. The origin idea behind kache mining
generalizes the same ledger one level down: position in WEIGHT space, the coordinates inside
each model where an idea is actually active. The two ledgers join on (prompt, family,
outcome): the surface GPS says where the WORK happened; the weight GPS says where IN THE
MODEL the idea lived while it happened. Same law, different terrain, and the second terrain
is one we own outright on disk.

## 1. WHAT "POSITION IN WEIGHT SPACE" MEANS FOR OUR ASSETS

- **Position = the activation vector.** For model M, prompt p, layer L: the position is the
  residual-stream activation h^L(p), a d-dimensional vector (d = M's hidden size) at the last
  prompt token. A battery prompt is a probe lowered into the terrain; the vector it returns
  is where the model stands on that idea. This is the same object Anthropic's
  interpretability line decomposes with SAEs (STEERING_FIELD_THEORY sec 6, honestly cited
  there as a different-but-parallel space); we do not need SAEs for row zero, raw h^L is the
  coordinate.
- **Movement directions = difference-in-means.** The OBLITERATUS drop
  (watch/inbox/ABLITERATUS_DROP_20260929.md) banks the recipe: collect activations on two
  prompt classes, mean them, subtract (harmful minus benign = the refusal direction, Arditi
  et al. 2024), distill with SVD, then either project it out of the weights permanently or
  add it at inference as a steering vector. Generalized off refusal: mean(act|class A) minus
  mean(act|class B) is a DIRECTION for any contrast the estate cares about (format-law
  compliance, hedging-off, estate-law recall). A direction is a trail; a steering vector is a
  bounded impulse along it.
- **The terrain = the GGUF bytes on disk.** `ollama list` read this session: 17 models
  owned locally. The kache-relevant readers, smallest first: deepseek-r1:1.5b (1.1GB),
  qwen2.5:3b-instruct (1.9GB), gemma:2b (1.7GB), gemma2:2b-instruct-q5_K_M (1.9GB, blob
  sha256:b21594fe...), qwen2.5:7b and qwen2.5-coder:7b (4.7GB), gemma4:latest (9.6GB, blob
  sha256:4c27e0f5...), up to qwen2.5:32b (19GB) and athena-class (32GB). Every one is a
  file we can read offline, $0, no API. The host venv carries torch 2.13 CPU +
  transformers 5.15 + numpy + sklearn (checked this session), and the ollama server's embed
  endpoints are flag-gated ("server does not support embeddings"), so the sanctioned capture
  instrument is transformers loading the SAME GGUF blobs ollama serves.
- **Positions are (model, layer)-relative.** There is no shared origin across families; a
  gemma position and a qwen position are coordinates in different charts. That is the
  "comparing them against each other" problem, and sec 3 is its solution.

## 2. THE MEMLANCE ROLE - THE POSITION LEDGER

- **The double reading of the name.** The skill (.agents/skills/memlance/SKILL.md) defines
  memlance as the aimed seed thrown across the mesh (AIM / FORGE / THROW / WITNESS / TALLY).
  The kache coinage adds the storage reading: a LANCE is also a columnar vector store's name
  (the Lance format: columnar, versioned, built for vectors). Memlance for kache mining is
  both at once: the aimed throw (choose the prompt, hit the layer) AND the columnar ledger
  the throw lands in.
- **Row shape (kache.capture.v1), append-only, sha-stamped, the estate ledger idiom**
  (spawn_manifest.jsonl / usage.jsonl laws):
  `{ts, model_id, model_digest, layer, layer_depth_pct, prompt_id, prompt_sha256,
  battery_ref, instrument, torch_dtype, dim, norm, vector_path, provenance}` with vectors as
  .npy sidecars. Roots: memory/runs/kache/captures.jsonl + memory/runs/kache/vec/.
- **The skill procedure maps onto capture:** AIM = pick the prompt battery + anchor layers;
  FORGE = capture and hash; THROW = the query that later bends a routing or staging decision;
  WITNESS = a downstream seat cites the position row unprompted; TALLY = hit-rate of
  position-informed routing vs the GPS-only baseline.
- **Why memlance and not a new organ:** mag/ghost_memlance.py already proves the shape
  (index / select / trace_state / verify; deterministic; every state carries provenance and
  a verified flag; "never fabricates a memory state from memory-of-memory" = never trust a
  vector without its capture bytes), and mag/mem_lands.py already binds read and write into
  one flow with content-addressed signatures. Kache rows extend that index with vector
  sidecars; verify() gains a byte check (re-hash the .npy, recompute the norm). No parallel
  instrument is invented.

## 3. COMPARING POSITIONS ACROSS MODELS - the cross-family position map

"Same prompt, different family = same idea, different coordinates." Three rungs, cheapest
first, none needing a shared basis:

1. **GEOMETRY COMPARE (RSA).** For one battery of n prompts, build each model's n x n
   pairwise cosine matrix S_M over captured positions. Compare S_A vs S_B entrywise
   (Spearman over the upper triangle). High correlation = the two terrains fold the same
   idea-neighborhoods even though no axis is shared. This is representational similarity
   analysis; CKA is the fancier sibling and stays unbuilt until RSA earns it.
2. **IDEA ADDRESSES (where in EACH model an idea lives).** Per model, fit a tiny linear
   probe on captured hidden states labeled by prompt class; per-layer probe accuracy is the
   idea's LAYER address, the learned weight is its local direction. The address table across
   models is the position map proper: "format-law lives at layers 6-13 in gemma2:2b, later
   and narrower in gemma4."
3. **POSITION TO BEHAVIOR BRIDGE (the falsifiable join).** The garden grid already banks
   per-family behavior on byte-identical contracts (BATTERY.md law 1, GRID_*.json). Join:
   for prompt pair (i, j), does activation proximity predict answer convergence across
   models? If yes, the weight-space map buys routing power, not just cartography.

Cold-vertex mapping (COLD_VERTEX_LAYER.md): a prompt class with zero captures and no probe
is UNCOLLAPSED, not absent; and where two models' geometries disagree (the RSA's weakest
entries) is the coldest, highest-variance region of idea space - the improbability drive's
second terrain.

## 4. STAGING INSIDE THE SHAPE - the tesuji

"Actually stage things inside the shape of ideas" = choose the coordinates first, then move
the model (or pick the model) so the work starts there. Three actuators, coarse to fine:

1. **MODEL + FACE (coarsest).** Pick the family whose terrain holds the idea at its most
   accessible address (the sec 3 probe table). The claritas face (mag/claritas.py) is the
   coarse position selector: it moves the model's starting region for the ask, and its reach
   is a measured per-family property (STEERING_DOGFOOD: kimi obeyed a sealed steering
   envelope 4/4, glm-flash 0/4 at low effort - conductivity is terrain hardness).
2. **PROMPT SELECTION.** The battery shows which prompt shapes already sit in the target
   region; staging the work in one of those shapes starts inside the region. The garden does
   this implicitly today; kache makes it a coordinate choice with a receipt.
3. **STEERING VECTORS (finest).** Capture a difference-in-means direction for the target
   property, add it scaled at inference at the address layers (the OBLITERATUS
   inference-time paradigm, no retraining). This is the same bounded-additive-impulse law as
   steer_seal in surface space (STEERING_FIELD_THEORY L3a), now with a measurable move:
   cosine distance traveled at the address layer.

**The staging loop:** capture candidate staging positions (ledger row) -> pick or patch the
region (face / prompt shape / vector) -> MEASURE THE MOVE (cosine before and after) -> verify
behavior with the standing graders -> bank the move (direction, scale, measured move,
behavior delta). **Boundary laws:** inference-time vectors only by default; permanent
projection (editing the weights) is a quantize-target decision on the deliberate-ask ladder
and an operator gate; model text proposes, the switchboard/effect broker authorizes effects
(shared-surface contract).

## 5. THE CHEAPEST FIRST EXPERIMENT - KACHE-E1 ($0, local, row zero)

**Claim to test:** prompt-similarity in activation space predicts cross-model answer
convergence. Run THIS session per the operator upgrade; design frozen here before the run.

- **Models:** gemma2:2b-instruct-q5_K_M + gemma4:latest (operator-named pair), read as the
  same GGUF blobs ollama serves (embed endpoints are flag-gated; transformers + torch CPU
  are in the venv, checked this session). Sanctioned fallback if an arch will not load:
  swap to the smallest loader-friendly family (deepseek-r1:1.5b / qwen2.5:3b-instruct) and
  SAY SO; never hand-patch weights to make a load pass.
- **Battery:** 10 short prompts shaped on the battery axes (format-law B6 descendant,
  arithmetic, comparison, primality, definition, haiku, shell-command, enumeration,
  string-op, count). Byte-identical to both models.
- **Capture:** last-token hidden state at 3 anchor layers (25 / 50 / 75 percent depth) per
  model, chat template applied = the bytes ollama serves. 2 models x 10 prompts x 3 layers
  = 60 ledger rows + 60 .npy sidecars under memory/runs/kache/.
- **Behavior side:** the same 10 prompts generated through ollama chat (temperature 0,
  short caps) on both models; the on-disk garden B6 outputs cover the REMOTE families'
  format-law behavior and are cited, but the local pair never ran the battery, so the local
  answer side is fired fresh (still $0, local).
- **Measure:** per model per layer, the 10x10 cosine matrix; RSA (Spearman) between the two
  models' matrices per layer; the bridge join over the 45 prompt pairs: X = mean activation
  cosine of the pair (per layer), Y = cross-model cross-prompt answer similarity (mean of
  sim(A_i, B_j) and sim(A_j, B_i), char-trigram cosine), Spearman(X, Y).
- **Prediction:** pairs close in BOTH weight charts converge more than pairs close in one
  or neither. **Falsifier:** no positive correlation at any anchor layer, or RSA ~ 0 (the
  charts do not share geometry at this battery size) -> the routing leg dies, the ledger leg
  survives as cartography; kache stays a map until a bigger battery says otherwise. n=10 is
  row zero: directional, not powered; the receipt says so in those words.
- **Cost:** $0 (no network), wall-clock capped ~20 minutes by operator order; honest
  partial beats none.

**Successor rungs (not this session):** repeat with 2 more local families (cross-FAMILY
gemma-vs-qwen is the stronger claim than same-family gemma2-vs-gemma4); join against the
garden grid's real remote-family answers; first difference-in-means direction capture
(format-law axis) as the E2 staging probe.

Filed by lane KACHE-1 seat, 2026-10-02. Spec before run (build discipline); E1 result lands
in watch/inbox/model_garden/KACHE1_RECEIPT.md, not edited into this spec's design section.
