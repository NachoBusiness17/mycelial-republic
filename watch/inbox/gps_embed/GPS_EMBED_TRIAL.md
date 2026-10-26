# GPS_EMBED_TRIAL: EmbeddingGemma 2 x the verdict ledger (2026-10-06 lane)

Operator order: "do it - pull EmbeddingGemma 2 and wire the vector-keyed GPS trial."
Filed falsifier: if embedding-NN does not beat string keys on held-out accuracy OR costs
>5 ms/ask, the substrate dies; a win banks the win and the flip-to-default still needs the
operator GO. Verdict at the bottom. Every number below is instrument-tagged.

## 1. PULL (bytes banked)

- Model: google/embeddinggemma-2 (Apache 2.0, 740M params: 270M text backbone + 170M vision
  + 300M audio; text tower only exercised here). HF API search hit: `google/embeddinggemma-2`
  (7,562 downloads, 943 likes at pull).
- Path taken: the venv's transformers 5.15.0 predates the `embedding_gemma2` architecture
  (verified: no `transformers.models.embedding_gemma2`; CONFIG_MAPPING_NAMES lacks both
  `embedding_gemma2` and `embedding_gemma2_text`), and the google repo ships no remote-code
  .py files, so `trust_remote_code=True` cannot load it either. Ran the order's sanctioned
  minimal ONNX path: the official export `onnx-community/embeddinggemma-2-ONNX` (fp32
  primary, q4 as the timing arm) under onnxruntime CPU 1.x. Media towers never execute:
  the graph declares image/video/audio feature inputs as required, so they are fed
  zero-sized tensors; the graph emits L2-normalized `sentence_embedding` [batch, 768]
  (mean pooling + 512-to-768 projection inside the graph).
- Files (instrument: `python -m tools.gps_mcp.gps_embed pull-info`, sha256 over full bytes),
  cached under `models/embeddinggemma-2-onnx/` (gitignored per .gitignore line 36):

| file | bytes | sha256 |
|---|---|---|
| onnx/model.onnx | 421,421 | bc47de15f81208a5c99e5ab10f746d5e33b51ea228b7dc0bef9c133a94f1c1c3 |
| onnx/model.onnx_data | 1,084,170,240 | 9fd452bfc6916e5a92f080f8dada35598ca4512b21c65897d4c5974d5f9630a2 |
| onnx/model_q4.onnx | 490,742 | f9eeba97acddf139b8ee2ddf04bc30dceafa88de93fadf74d7644e0d61a477a9 |
| onnx/model_q4.onnx_data | 174,028,800 | c3975f2d1ab7a1878ae31a7d7a9b7804a827aff3800b60dfceafce21cac3df49 |
| tokenizer.json | 32,170,530 | 4d777ef5bdc1aa36227abdfb77c3e49e7b9c892d16e1b6bda41c393504828be4 |

- Embedding config: task prefix `task: clustering | query: {text}` on every compared input
  (model card, symmetric-task rule), output 768-d, rows verified norm==1.0. Determinism
  verified bit-identical in-session and across fresh session loads
  (tests/test_gps_embed_trial.py::test_embedding_round_trip_determinism).

## 2. LEDGER EMBED (sidecar banked)

- Source: `tools/gps_mcp/gps_ledger.db3` verdict_log, sha256
  63f2069ca52c3c16719a3ceb87ebadd0724c572e63d6e516ae06def24d7c7949 (read-only opens;
  production bytes untouched; trial worked on a byte copy). Census (instrument: sqlite
  GROUP BY): 703 rows, 10 distinct task_shapes, 13 model_ids, 47 distinct
  (task_shape, verdict, model_id) groups.
- Sidecar: `memory/runs/gps_embed/vectors.db3` (instrument:
  `python -m tools.gps_mcp.gps_embed embed`): `shape_vectors` (10 rows, one 768-d float32
  vector per distinct shape, 392.1 ms to embed all 10), `vectors` keyed
  (task_shape, verdict, model_id) per the order (47 rows, n_rows preserved), `meta` with
  onnx sha + prefix. Idempotence proven: rebuild is INSERT OR REPLACE, byte-identical
  vectors, no growth (test_sidecar_build_idempotence).

## 3. TRIAL (instrument: `python -m tools.gps_mcp.gps_embed_trial`, results at
memory/runs/gps_embed/trial_results.json)

Design. Split: per-shape deterministic 30% holdout, seed 20261006 (493 train / 210 held
rows, n>=100 satisfied). Oracle per ask: the production capability table's own winner rule,
shape_table[0] (pass_rate desc, momentum, n, model_id) computed on the FULL ledger; a route
is correct iff it names that model. Route A (string key, ledger semantics today):
task_shape_has_history on the train ledger then shape_table[0]; unseen shape routes to the
exploration model flash-mid-1 (router.py rule). Route B: kNN cosine k=3 over train-shape
vectors, majority vote of neighbor winners, distance-tie to nearest.

DEFECT RECORD (fixed at landing, the buggy reading is struck): the first timing pass
measured cache hits on both arms (route_b reused a precomputed query vector, route_a read
a precomputed winners dict) and reported 0.1 ms/ask for an embed that costs tens of ms.
The landed instrument embeds the query text fresh on every B ask and re-runs shape_table
on every A ask. Accuracy was unaffected (same vector bits); only the timing was wrong.

Numbers (instrument: trial run 2026-10-08T00:4xZ, warm, batch=1, perf_counter_ns over all
210 held asks; second run cited where it moved):

| metric | A string-key | B kNN embed (fp32) |
|---|---|---|
| held-out accuracy | 210/210 = 1.000, Wilson 95 [0.982, 1.000] | 208/210 = 0.9905, Wilson 95 [0.966, 0.997] |
| ms/ask mean | 1.12 (1.44 second run) | 74.4 (96.9 second run; machine under cron load) |
| ms/ask p50 / p95 | 1.22 / 1.72 | 70.1 / 99.1 |
| paired | A right B wrong = 2, B right A wrong = 0 | McNemar exact p = 0.5 |

- B's only misses: the 2 grading rows. Anatomy (trial_results.json misses): grading
  self-matched at cosine 1.000 (winner z-ai/glm-5.3-prime = the oracle), but planning
  (0.933) and schema-design (0.909) both carry winner deepseek/deepseek-v4.1-flash, so the
  filed k=3 majority rule outvoted the exact match 2-1. Structural, not a fluke: with 10
  shapes, cross-shape neighbors regularly outvote exact hits.
- q4 arm (same asks, quantized graph): 61.4-85.9 ms/ask, accuracy 1.000 (quantization
  wiggle moved grading's vote the other way), leave-one-out neighbor agreement with fp32
  10/10. Still >> 5 ms.
- kNN arithmetic alone (query + neighbors precomputed): 0.097 ms/ask. The cost is all in
  the per-ask query embed.
- Cold-start arm (leave-one-shape-out: train = other 9 shapes, asks = held shape rows;
  the only regime where string keys cannot work and vectors must pay for themselves):
  A 0.000 (exploration route never equals the oracle), B 0.0284 row-weighted (1 shape hit:
  schema-design via planning's deepseek winner). The winner label is NOT semantically
  smooth across shapes: winners are idiosyncratic to which models happened to duel on a
  shape (legality-water-graph-v1's winner is a bespoke legality-propagator; arena's is a
  claude model), so semantic proximity of shape names does not transfer winner identity.

## 4. VERDICT (the filed falsifier)

KILL. Ground 1 (accuracy): embedding-NN does not beat string keys on held-out rows
(A 210/210 vs B 208/210; both discordant pairs favor A; McNemar exact p=0.5). Ground 2
(cost): fp32 74-97 ms/ask and q4 61-86 ms/ask, both far over the 5 ms/ask bar (the kNN
arithmetic alone is 0.097 ms; the query embed is the whole cost). Ground 3 (the thesis's
own regime): on unseen shapes (LOSO) vector transfer scores 2.84% vs the exploration
baseline 0% - winner identity is not a function of shape semantics in this ledger, so
there is nothing for the embedding to generalize. No flip-to-default requested; the
string-key router stays. The substrate is dead as filed; if the ledger ever grows
semantic shape families with shared winners, the sidecar and instrument are banked and
the trial reruns with one command.

## 5. Tests, gates, artifacts

- Tests: tests/test_gps_embed_trial.py, 7 passed in 77.46s
  (instrument: `.venv/Scripts/python.exe -m pytest tests/test_gps_embed_trial.py -q`):
  wilson/mcnemar/knn-vote/split invariants (model-free), embedding round-trip determinism
  (same input twice = same vector, in-session and fresh-session), padding-mask invariance,
  sidecar build idempotence. Model-dependent tests skip cleanly on seats without the pull.
- Violation ratchet: PASS with NEW=0 after splitting the lane into three files under the
  400-line law (gps_embed.py 298, gps_embed_trial.py 363, gps_embed_stats.py 122). The
  first cut was one 479+ line file; the ratchet caught it, fixed by split, debt never
  accepted. (tools/hermes_burn.py GROWTH is a pre-existing other-lane claim, untouched.)
- Artifacts: tools/gps_mcp/gps_embed.py (pull+embedder+sidecar+CLI),
  tools/gps_mcp/gps_embed_trial.py (trial+verdict), tools/gps_mcp/gps_embed_stats.py
  (model-free arithmetic), memory/runs/gps_embed/vectors.db3 (sidecar),
  memory/runs/gps_embed/trial_results.json (every number above, machine-readable).
- Blockers: none. Everything filed ran; nothing faked. No git commit (lane law).
