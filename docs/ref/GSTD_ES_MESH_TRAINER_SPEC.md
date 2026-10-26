# GSTD ES MESH TRAINER SPEC (the mesh-native trainer, the pennies-leasing shape)

Landed: 2026-10-07, run `ml-moonshot-20261007`, lane ml6-es-mesh-trainer.
Skeleton module: `tools/gstd_es_trainer.py`. Tests:
`tests/test_gstd_es_trainer.py`. Rides the P3 FLEET LANE wire
(`docs/ref/GSTD_FLEET_LANE_SPEC.md`, `tools/gstd_fleet_provider.py`); the P4
"federated training" slot of `docs/ref/GSTD_DOGFOOD_PLAN.md` is the phase this
spec fills, with the gradient-free shape instead of weight sync.

## 1. The drop this comes from

`watch/inbox/LINKS.jsonl` row seq 1791377243089599 (2026-10-07, the
che_shr_cat thread): ES finds parameter neighborhoods 3.9x wider than PPO, and
in an 18-setting continual benchmark ES won the stability-plasticity
trade-off in 8 settings while gradient RL won ZERO. The mesh-native reading
banked in that row: ES needs no gradient sync, so each mesh node evaluates
fitness locally and only the score travels. That is the first training shape
that fits a mesh that settles pennies per task: the estate leases node
minutes for pennies and pays in kilobytes, not megabytes.

## 2. What travels and what never travels

- TRAVELS OUT: one task submit per genome evaluation, through
  `tools.gstd_fleet_provider.submit_task`. The payload is a fleet `probe`
  whose prompt is the base task plus the rendered cue vector (a few hundred
  bytes). Nothing else.
- TRAVELS BACK: the completion bytes, through `gfp.poll_task`. The trainer
  derives ONE float per evaluation from those bytes (fitness, section 4).
- NEVER TRAVELS: gradients, weight deltas, LoRA artifacts, optimizer state,
  population state, the genome vector itself. The ledger stores the integer
  seed per generation; any perturbation is re-derived locally from that seed
  by `sample_perturbations`. The update (`update_mean`) consumes returned
  scores and locally re-derived eps and nothing else:
  theta <- theta + (alpha / (n * sigma)) * sum_i centered_f_i * eps_i.
- This is the no-gradient clause in code: a PPO or federated-learning shape
  must ship a model artifact or a gradient to make the same progress; ES
  ships none. `tests/test_gstd_es_trainer.py` pins it both ways: identical
  completions everywhere (zero variance) move the mean by exactly zero, and a
  mixed-fitness round moves the mean toward the winning perturbation using
  scores only.

## 3. Genomes

Two genome kinds, one vector interface (8 named slots by default):

- PROMPT-CUE (wired): `GENOME` names cue slots (`step_by_step`,
  `answer_first`, `check_work`, `format_strict`, `terse`, `show_example`,
  `restate_task`, `no_preamble`); `render_prompt` includes a fragment iff its
  weight is positive, heaviest first. Same vector, same prompt bytes, so the
  evidence hash downstream is reproducible. Honest limitation, named: weight
  sign flips toggle fragments (a coarse, discrete landscape); continuous
  weighting of fragment emphasis is a wire-time upgrade once real traffic
  calibrates sigma.
- ROUTING-POLICY (staged): `route_device` is the argmax-of-weights steering
  over wallet-carrying nodes, tested; the round loop still round-robins
  devices until routing steering is wired with live node health (the free
  lane health table, per fleet spec section 4).

## 4. Fitness

`fitness(completion, expected) = success - cost_norm`. Success is the same
crude ground-truth check the self-play orchestrator uses (number match within
0.01, else substring). `cost_norm` stays 0.0 until the settlement RFC lands:
the fleet lane computes nothing owed (fleet spec section 6), so the skeleton
refuses to invent a pennies accounting it cannot verify. The cost term is the
first wire-time upgrade, not a silent default.

## 5. What a 3-node ES round costs in bytes (the computed answer)

One generation = 6 evaluations (3 antithetic pairs) over 3 nodes = 2 evals
per node. All numbers are application-layer JSON payload bytes computed by
`round_cost_bytes()` in `tools/gstd_es_trainer.py` (run with `--cost`,
2026-10-07; pinned in `tests/test_gstd_es_trainer.py::test_round_cost_bytes_pinned_defaults`).
The completion default of 276 chars is the fleet spec's own example row
(`docs/ref/GSTD_FLEET_LANE_SPEC.md` section 5, `chars: 276`); the task default
is 120 chars; 3 status polls per task.

| component                          | bytes per task | x 6 tasks |
|------------------------------------|---------------:|----------:|
| submit body (id, kind, prompt+cue, device_hint) | 323 | 1938 |
| completion poll response (task_id, status, result, model) | 372 | 2232 |
| status polls (3 per task)          | 222            | 1332      |
| per task total                     | 917            | 5502      |

HEADLINE: a 3-node ES generation costs 5502 bytes on the wire, 1834 bytes per
node, and settles 6 task credits. Compare every gradient-carrying shape,
which must additionally ship a model artifact or gradient per round; ES's
update round trip is zero bytes because it happens in
`memory/runs/gstd_es_trainer/state.json` on the trainer side. TCP/TLS framing
adds fixed per-request overhead the platform does not bill (the mesh settles
credits per task, not per byte).

The expected rendered-cue length is 119 chars (238 fragment+separator chars
across the 8 slots, halved at mean 0), which is why the submit body stays
under half a kilobyte.

## 6. Wallet gate and laws (all inherited, none reimplemented)

The module holds NO sockets of its own: every byte on the wire goes through
`tools.gstd_fleet_provider`'s gated `submit_task` / `poll_task`, so the
fail-closed per-device wallet gate (`GSTD_WALLET_DESKTOP`, `GSTD_WALLET_BOB`,
`GSTD_WALLET_PIXEL`; absent, empty, and whitespace all read as absent), the
SSRF fixed-literal allowlist, strip-at-load keys, `_scrub` on banked strings,
and retry-never all bind here unchanged. `--round` exits 3 while the gate is
closed (verified 2026-10-07: `WALLET GATE BLOCKED ... live es round refused`,
exit 3), and a blocked round writes no state and makes zero network attempts
(tested by stubbing `submit_task` to explode).

## 7. Honest scope (what the skeleton does NOT do)

- No live round has fired: the gate is closed until P0 wallets paste, same as
  the fleet lane.
- No settlement or balance accounting (cost term 0.0, section 4).
- No routing steering in the round loop (`route_device` staged, section 3).
- No quorum attestation of scores (P4 territory): one node's completion is
  one fitness sample; the evidence hash ties each score to its banked
  `gps_mesh_row.v1` in `memory/runs/gstd_fleet_lane/mesh_ledger.jsonl`, so a
  later quorum layer can re-adjudicate from bytes.
- Fitness is the crude number-match check, not a reward model.

## 8. Falsifier

A wallet-pasted month where `memory/runs/gstd_es_trainer/es_rounds.jsonl`
grew generations but the mean vector in `state.json` never moved away from
all-zeros means the round burns task credits without learning: either every
completion scores equal (fitness is not discriminating; fix the success
check) or scored evals never differ within pairs (the mesh is caching
responses; fix the prompt render). Second falsifier, the pennies-leasing one:
if any future edit adds a weight delta, gradient, or model artifact to the
wire, this spec is violated by definition; the wire carries tasks and
completions only.

## 9. Tests

`.venv\Scripts\python.exe -m pytest -q tests/test_gstd_es_trainer.py` (16
tests, no network): gate fail-closed with zero submit attempts, gate exit 3
on `--round`, deterministic cue render with positive-weight inclusion,
antithetic sampler (pairwise cancellation, deterministic per seed, even-pop
law), score-only mean update (moves toward the high-fitness perturbation,
zero-scores means zero move, zero-variance means zero move), fitness success
and cost term, byte-cost model (construction and pinned literals), happy-path
round banking scores plus evidence hashes and never completions, failed-eval
banking with no retries, state roundtrip with corrupt-file fallback.
