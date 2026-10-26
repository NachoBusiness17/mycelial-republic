# Steal card: open-local-language-models via reddit (frontier fold 2026-10-07, round 1)

Four confirmed finds from the sweep bank (`sweep/open-local-language-models-reddit.md`, this
seat read it whole this round). This seat re-verified the load-bearing claims with its own
bytes, not the finder's word: the qwen3 tag-digest aliasing was re-tested against the live
Ollama registry and REPRODUCED byte-side today; the OpenShell trust-boundary mechanism was
tested against the estate's own shell door and the boundary measured ABSENT; the gigafish
dataset door, license, and schema were fetched (HTTP 200, README on disk); and the band
candidate's pull door was probed on the registry. Reddit thread bytes themselves were not
re-fetched this round (the doors are dead per the sweep, `sweep/open-local-language-models-reddit.md:8-12`);
quotes below carry the sweep bank's line anchors, and the two claims that matter most were
re-verified at stronger doors than reddit (registry, localhost daemon, HF).

## Steal 1 (re-verified byte-side, LIVE at fetch moment): a tag can silently alias to a different model, flipping the recorded thinking condition

- Find: r/ollama 1wyaxyd (2026-10-05), quote banked at `sweep/open-local-language-models-reddit.md:88-95`:
  "On Ollama, qwen3:4b now has the same digest as qwen3:4b-thinking, which is the 2507
  thinking-only release, so it doesn't have a non-thinking mode to switch to." All three
  off-switches (`/no_think`, `/set nothink`, `--think=false`) silently ignored.
- THIS SEAT RE-VERIFIED, 2026-10-07 (artifacts on disk in this dir):
  - `curl -H "Accept: ...manifest.v2+json" https://registry.ollama.ai/v2/library/qwen3/manifests/{4b,4b-thinking,4b-instruct}`:
    4b and 4b-thinking both HTTP 200, 859B, and BYTE-IDENTICAL (diff empty; sha256
    359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7 for both). The shared
    manifest points both tags at the same model layer (sha256:3e4cb141..., 2,497,280,480 B),
    same template layer (1,506 B), same params layer (120 B). `4b-instruct` is a DIFFERENT
    artifact (sha256 0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0), so
    the recovery door the thread names exists as a distinct digest. The aliasing is not a
    transient from 10-05; it is live at the registry now.
  - Estate daemon side (GET localhost:11434/api/tags, HTTP 200, 7,466B, saved as
    `tags_probe_olmreddit.json`): 17 installed models, ZERO digest collisions across
    distinct installed tags. qwen3 is not installed. So the estate fleet is clean TODAY;
    the steal is the law that keeps it clean.
  - Family check: `qwen3:8b` exists (manifest sha256 500a1f06...); `8b-thinking` and
    `8b-instruct` both 404. The two 404 bodies hash identically (fa197eb7...) because they
    are the same 69B error payload; that is an artifact of hashing error bodies, NOT an
    aliasing match. Named here so nobody re-reads it as one.
- Mechanism for the estate: thinking-mode is the estate's measured axis (AGENTS.md tier
  ladder; the one-bug law, `memory/rib/RIB_MODEL_GATES_20261001.md:115-125`: omission of the
  thinking key is a MEASURED ON state). A tag whose digest silently re-points flips WHICH
  artifact answers, with zero config change and zero error; every recorded condition
  (thinking on/off, template, params) goes stale without any signal. Tags are mutable
  pointers; digests are the identity the condition ledger can actually pin.
- Port move (concrete): the pin surfaces are tag strings today: `mag/ollama_policy.py:16-18`
  (JANITOR gemma:2b, DESK_DEFAULT gemma4-desk, KEEP_ALIVE list), `mag/lanes.py:45,48`
  (clerk/router gemma:2b), `mag/task_router.py:38,147,148` (classify/simple_lookup
  gemma:2b). Add a digest column beside each tag, read back via /api/tags at seat boot
  (the same daemon-read pattern the sibling card ported for thinking defaults,
  `watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models.md:14-23`), and
  REFUSE the rung on tag-to-digest mismatch instead of silently running whatever the tag
  now points at. Never pin a tag whose manifest is byte-identical to another tag's when the
  two tags imply different thinking states.
- Estate organ: gopher fleet (seat boot + the per-model condition ledger).

## Steal 2 (probe EXECUTED this round, boundary measured ABSENT): runtime limits enforced outside the model, harness and shell at different privileges

- Find: r/LocalLLaMA 1ws9ydg (2026-09-28, 761 pts), NVIDIA OpenShell, banked at
  `sweep/open-local-language-models-reddit.md:96-106`. The vendor claim is the wrapper; the
  durable steals are in the comments: u/wren6991 "the shell that the agent runs commands in
  does not need the same privileges as the harness itself. There should be a trust boundary
  in between the two"; u/Future_AGI "runtime limits enforced outside the model are the only
  thing that actually holds". The sweep also banks the honest skeptics (logo-wall BD calls,
  "thin on technical detail") so the steal is the mechanism, not the vendor.
- THIS SEAT EXECUTED THE PROBE against the estate's own shell door
  (`tools/code_execution.py`, entry `run_python` at `:31`):
  - The door's own contract admits the gap: `tools/code_execution.py:44` "Soft refuse
    obvious network imports used maliciously", and the very next words: "still not a full
    sandbox". Enforcement is a five-pattern substring ban (`:45-47`: socket.socket,
    subprocess, os.system, shutil.rmtree, `__import__('os')`).
  - Probe: `run_python` fired a snippet using only `open()` (not on the ban list) writing a
    98-byte marker to an absolute path OUTSIDE the door's tempdir cwd. Result: ok=True,
    exit 0, marker landed on disk in this seat's steal dir, verified by listing, then
    removed. Runner kept at `shell_escape_probe_runner.py`. The tempdir cwd, the filtered
    env (`:61-64`), and CREATE_NO_WINDOW (`:68`, the spawn_sites_no_window law,
    `tools/derived_dag.py:58-61`) are hygiene, not containment: the shell inherits the full
    user. The substring ban is prompt-rule-shaped by construction (os.popen, double-quoted
    `__import__("os")`, or plain `open` all pass).
  - The estate DOES hold an authorization boundary one level up: model_call and lane_spawn
    are the two effect classes policy-forbidden to dispatch headless, board_write the one
    production-legal headless class (`mag/effect_broker.py:376-380`). That authorizes
    EFFECTS; it does not constrain the RUNTIME the shell runs in. The OpenShell steal is
    exactly the missing second layer.
- Mechanism for the estate: deterministic-first, already estate law, now with an industry
  embodiment: the trust boundary must live in the spawn, not the prompt. A lane that shells
  out gets a privilege class strictly below the harness (win32: restricted token or job
  object with CPU/memory/time caps; writable root = its own inbox area), so a compromised
  or drifting model cannot spend harness authority. Bans become redundant, not load-bearing.
- Port move (concrete): wrap the spawn in `tools/code_execution.py` (and the free-lane
  gauntlet queue that feeds it) with a job-object/restricted-token rung whose caps and
  writable root are declared per lane; keep the effect broker as the authorization layer on
  top. The shared-surface contract (write only through the inbox with receipts) stays the
  policy; the spawn becomes the enforcement.
- Probe (falsifiable, cheap): the one this seat already ran; standing form: any lane's shell
  must FAIL to write outside its declared root. Falsifier: a marker lands (today it does;
  that is the measured gap the port closes).
- Estate organ: gopher fleet (the tool-execution lane).

## Steal 3 (contradiction IS the finding): two community benches disagree on the 0.5B-8B band, so UNMEASURED stays the legal cell and the estate battery stays the only court

- Find: r/LocalLLM 1wblnsk (2026-09-09), banked at `sweep/open-local-language-models-reddit.md:107-117`.
  The OP's 18-question manual bench picks Ling3.0-Tiny as a speed pick; the banked 200-task
  tier list (1ww528l, held via the 10-03 bank) puts Ling-3.0-tiny at F tier. The comment
  field names the band's live candidates: Ornith-1.5-9B ("very good for it's size"),
  miniCPM5 2B, Sparx-X2.5-4B, Nanbeige4.2 3B, LFM, and dismisses the OP's bigger picks as
  "too old, old LLMs can't use the tools properly".
- Estate anchors verified this round: RQ1's baseline is the janitor pin gemma:2b
  (`mag/ollama_policy.py:16`; `mag/task_router.py:147-148`) on the one-hot 6GB AMD host
  (`mag/ollama_policy.py:1-3`); the percolator candidate ledger exists at
  `memory/percolator/candidates.jsonl` (30 rows; row shape ts/status/domain/file/row/source/claim,
  read this session). Local daemon: `frob/ling-3.0-flash:latest` IS installed (77.0 GB,
  digest e9709a98..., `tags_probe_olmreddit.json`); that is the flash variant, not the tiny
  the contradiction is about. Catalog overlap for Ornith: 0 (sweep receipt,
  `sweep/open-local-language-models-reddit.md:196-199`).
- Pull-door probes this seat ran: `registry.ollama.ai/v2/library/ornith/manifests/9b` HTTP
  200 (and `latest` 200), so a 9B Ornith is pullable through the estate's own daemon;
  `ornith:1.5-9b` and `ornith:1.5` 404, and `library/minicpm5` 404. Whether `ornith:9b`
  carries the 1.5 weights the comment praised is unresolved until pull (OWED below).
- Mechanism for the estate: this is an anti-steal, banked as law: community testimony
  (even 14-pt upvoted testimony) does not settle the band; two instruments contradicting
  each other on the same model (Ling-3.0-tiny: F tier vs speed pick) is the measured proof
  that no public evidence clears RQ1's bar. The candidates are worth percolator rows; the
  verdicts are not. Every row enters with BOTH community grades attached and the cell
  UNMEASURED until an estate instrument fires.
- Port move (concrete): append candidate rows to `memory/percolator/candidates.jsonl` for
  Ornith-1.5-9B (pull door verified), miniCPM5 2B / Sparx-X2.5-4B / Nanbeige4.2 3B (pull
  doors unresolved, named as such), source = this sweep bank file, claim text carrying the
  contradiction note.
- Probe (falsifiable, cheap, this week): pull `ornith:9b` (one pull, fits the one-hot law
  as the single role model, ~5-6 GB class) and run the ToolCall-15 slice (instrument banked
  per `watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models.md:30`) against
  gemma:2b on identical items, thinking conditions recorded per steal 1's ledger. Falsifiers,
  either direction is a finding: ornith loses on tool-call shape and the "old LLMs can't
  use the tools" dismissal inverts onto the community's own pick; ornith wins and the band
  verdict stays open estate-side.
- Estate organ: percolator.

## Steal 4 (dataset verified live, cc0): distill the expensive evaluator into the cheap student, and score the student at equal TIME, not per-eval

- Find: r/MachineLearning 1wxz5qq (2026-10-05), banked at `sweep/open-local-language-models-reddit.md:130-141`:
  "I distilled the Stockfish value function into a ResNet/ViT model using 1 billion
  positions from the Gigafish dataset." Comments carry the priors: DeepMind prior art
  (arXiv 2402.04494) and the engine-community constraint (u/4plus4equals8): bigger
  evaluators beat NNUE per-eval but lose on speed, "the real optimization is elo at equal
  time". CNN beat ViT early on geometric inductive bias; best result combined both.
- THIS SEAT VERIFIED THE ASSET: `https://huggingface.co/datasets/lukesalamone/gigafish-3.8b-d10`
  HTTP 200 (295,678B page), README fetched and on disk (`gigafish_README.md`, 6,991B):
  license cc0-1.0; 3,919,006,164 unique positions; 3,920 zstd parquet shards, ~101 GB;
  schema is exactly two columns, `fen` (full 6-field FEN) and `eval` (Stockfish 16 depth-10
  evaluation from White's point of view, pawns with 1-2 decimals); train split only. The
  dataset is pullable, license-clean, and schema-known estate-side.
- Mechanism for the estate: this is the quantizer's own pattern applied to a chess value
  function: compress a strong slow judge (Stockfish 16 at depth 10) into a cheap fast
  student you can run locally, and measure the student by quality-per-eval-SECOND (elo at
  equal time), because per-eval quality buys nothing if the eval budget collapses. Two
  transferable laws fall out: (1) on board-shaped/grid-shaped data, geometric inductive
  bias (CNN) beats attention (ViT) early at equal training; (2) the distillation target is
  time-normalized, never raw accuracy. The estate's own thought-quantizer tiers
  (`memory/corpus/quantized_thought/`, flash/frontier/local) are the same trade: frontier
  judgment compressed into a local artifact whose worth is measured per latency, not per
  question.
- Estate fit verified this round: the stockfish door is live held work, master-folded
  TODAY (`corpus/steal/MASTER_STOCKFISH_DOOR_20261007.md:1-5`, folded 11:36Z, counting
  script sha256 58bd72c79c6d), and the QUEEN chess LM is banked frontier material
  (`watch/inbox/frontier_olm_2026-10-07/lens/burns.md:119-122`, silent-expert weld 1782 to
  2697 Elo, commit 33b596fa6). The gigafish asset plugs into that door as the training set
  for an estate value-function student; nothing here re-derives QUEEN (dataset + CNN/ViT
  distillation result are the new artifact; overlap receipt
  `sweep/open-local-language-models-reddit.md:200-201`).
- Port move (concrete): pin the dataset (URL + README sha256 below) as the door's training
  asset row; first experiment = 1M-position sample, tiny CNN student vs tiny ViT student at
  equal steps, scored by eval-rate x accuracy at a fixed wall-clock budget. Score the
  result at equal time or do not score it.
- Probe (falsifiable, cheap): sample pull of one shard (1M rows, ~26 MB compressed class)
  and verify the schema parses (fen valid, eval numeric-parsable); then a one-epoch tiny
  CNN on 100k positions must beat a material-diff heuristic baseline on held-out MSE.
  Falsifier: schema unparsable (asset claim dies) or the CNN cannot beat the trivial
  baseline at the sample size (the distillation lane is dead on estate hardware and the
  door keeps Stockfish uncached).
- Estate organ: quantizer (landing surface: the stockfish door); percolator gets the
  experiment row, not a verdict.

## Estate map (organ per steal; unstated organs are unstated on purpose)

1. Gopher fleet (condition ledger + seat boot): digest pinning beside every tag at
   `mag/ollama_policy.py:16-18`, `mag/lanes.py:45,48`, `mag/task_router.py:38,147-148`;
   boot-time tag-to-digest verify via /api/tags; refuse on mismatch (steal 1).
2. Gopher fleet (tool-execution lane): spawn-level privilege class + runtime caps below the
   harness in `tools/code_execution.py` and the gauntlet free lane; effect broker stays the
   authorization layer (steal 2).
3. Percolator: candidate rows with both community grades attached, cells UNMEASURED; first
   estate instrument = ornith:9b vs gemma:2b on the tool-call slice (steal 3).
4. Quantizer (stockfish door landing surface): pinned cc0 dataset + time-normalized
   distillation scoring (steal 4).
Sovereign mirror, water graph, and context pack are NOT fed by these four finds (no
sovereignty-trigger calibration row, no cost-flow row, no pack-content row); stated so no
organ is padded.

## Probes (two executed this round, two named for the week)

1. (EXECUTED) Registry manifest-hash comparison, qwen3 family: 4b vs 4b-thinking
   byte-identical (sha256 359d7dd4... both), 4b-instruct distinct (0edcdef3...). Standing
   weekly form: hash the manifest of every tag the estate pins; any tag whose manifest
   equals another tag's with a different implied thinking state fires. Falsifier: the
   manifests differ (claim stale/fixed). Today they do not.
2. (EXECUTED) Shell-door trust-boundary probe: `run_python` wrote a marker outside its
   tempdir, exit 0, boundary ABSENT; artifacts `shell_escape_probe_runner.py` + marker
   (created, verified, removed). Falsifier for the port: after the job-object rung lands,
   the same snippet must fail.
3. (This week, cheap) ornith:9b vs gemma:2b on the ToolCall-15 slice, identical items,
   one-hot law enforced, conditions recorded per the digest ledger. Either direction is a
   banked finding (see steal 3 falsifiers).
4. (This week, cheap) Gigafish one-shard sample pull + schema parse + tiny-CNN vs
   material-diff baseline at equal time budget (see steal 4 falsifiers).

## Evidence appendix (every check this round, artifacts in this dir)

- Registry: curl manifest GETs for qwen3 4b/4b-thinking/4b-instruct/8b/8b-thinking/8b-instruct
  and ornith latest/9b/1.5-9b/1.5 (+ library/minicpm5 probe). Saved:
  `manifest_qwen3_4b.json` (859B, sha256 359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7),
  `manifest_qwen3_4b-thinking.json` (859B, same sha256, diff vs 4b EMPTY),
  `manifest_qwen3_4b-instruct.json` (859B, sha256 0edcdef34593eac1...),
  `manifest_qwen3_8b.json` (859B, sha256 500a1f06...),
  `manifest_qwen3_8b-thinking.json` + `manifest_qwen3_8b-instruct.json` (both 69B HTTP 404
  error bodies, sha256 fa197eb7... each; identical because error payloads, not aliasing).
- Local daemon: GET /api/version -> {"version":"0.34.3"}; GET /api/tags -> HTTP 200 7,466B
  saved as `tags_probe_olmreddit.json`; parsed with .venv python: 17 models, 0 digest
  collisions, frob/ling-3.0-flash:latest present (77.0 GB).
- Shell door: `tools/code_execution.py` Read (whole file); probe executed via
  `.venv/Scripts/python.exe` + PYTHONPATH import of run_python; result ok=True exit 0,
  marker 98B landed outside tempdir, listed, then deleted. Runner script kept:
  `shell_escape_probe_runner.py`.
- HF: dataset page HEAD-equivalent GET 200 (295,678B); README via /resolve/main/README.md
  200 (6,991B) saved as `gigafish_README.md`; license cc0-1.0, schema fen/eval, 3.92B rows,
  3,920 shards ~101GB read from the README bytes.
- Repo anchors read this session: `mag/ollama_policy.py:1-30`, `mag/lanes.py:45,48` +
  `mag/task_router.py:38,147,148` (rg), `mag/effect_broker.py:370-412`,
  `tools/code_execution.py` (whole), `tools/derived_dag.py:58-61` (rg),
  `memory/rib/RIB_MODEL_GATES_20261001.md:115-125`, `memory/percolator/candidates.jsonl`
  (row 0 + wc: 30 rows), `watch/inbox/frontier_olm_2026-10-07/lens/burns.md:117-124`,
  `corpus/steal/MASTER_STOCKFISH_DOOR_20261007.md:1-33`,
  `watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models.md` (sibling card,
  whole), `sweep/open-local-language-models-reddit.md` (whole),
  `.zcode/workflows/olm-mine.dwf.ts:86-92,178` (the organ vocabulary + card schema).

## OWED (never asserted as fact)

1. The thread's recovery tag spelling "qwen3:4b-instruct-2507-q4_K_M" was not verified;
   this seat verified only that `4b-instruct` exists as a distinct digest. Exact instruct
   sub-tags (2507, quant suffixes) unprobed.
2. `ornith:9b` exists on the registry, but whether it carries the Ornith-1.5-9B weights
   the comment praised is unknown until pull; `ornith:1.5-9b` 404s.
3. miniCPM5 / Sparx-X2.5 / Nanbeige4.2 pull doors unresolved (minicpm5 404 under
   library/; other namespaces unprobed).
4. Ling-3.0-tiny: no pull door probed (the installed frob/ling-3.0-flash is a different
   size class); the F-tier vs speed-pick contradiction is banked on the two community
   instruments, not on any estate run.
5. Reddit thread bytes were not re-fetched this round (dead doors,
   `sweep/open-local-language-models-reddit.md:8-12`); quotes ride the sweep seat's
   arctic byte-parses. The steal-1 claim was instead re-verified at the registry, which is
   the authoritative door for what a tag points at.
6. The effect-broker authorization path was read (`mag/effect_broker.py:370-412`) but not
   probed end-to-end this round; the shell probe demonstrates the missing RUNTIME layer
   only.
