# probe20 live: the estate's first real drift-pair rows (burn lane 10/10, reset-evening 2026-09-27)

Driving doctrine first amendment delivered: THE LENS verdict was "law-without-measurement"
(memory/runs/probe20/ empty). This lane measured. No synthetic rows were written
(pre-registered falsifier stands binding and untested, which is the honest good case).

## Model served

- gemma:2b blob from the local ollama store:
  `C:\Users\foste\.ollama\models\blobs\sha256-c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12`
  (1,678,447,520 bytes, first 4 bytes verified `GGUF` before serving; manifest digest match).
- Server: `tools/llamacpp/llama-server.exe --model <blob> --port 8080 --host 127.0.0.1 -ngl 99`.
  Health 200 within ~6 s of launch. Log shows no explicit Vulkan device banner at default
  verbosity; prompt eval ~31 ms/token is CPU-plausible, so GPU offload is UNVERIFIED bytes-wise
  (workload did not need it; small model, cycles ran 4 s each).
- PID (kept RUNNING at close, per lane order): **40708** (listening 127.0.0.1:8080, health=200
  re-verified after the last cycle).

## Cycles run and series

- 6 live cycles, >=50 s pacing between cycles (spacing, not bursts).
- Series: `memory/runs/probe20/gemma4_A_series.jsonl`, **6 rows**, pair A
  (lane=gemma4:A-conf-margin-vs-correctness), all rows carry
  `probe_version_hash bfce1f28dae4...` (v1 seed, never mixed).
- Rows (cycle: mean margin, correct/20):
  0: -1.8506, 13/20 | 1: -1.8742, 12/20 | 2: -1.8741, 12/20 | 3: -1.8741, 12/20 |
  4: -1.8741, 12/20 | 5: -1.8741, 12/20.
  Cycle 0 vs 1 differ by one task flip (t-class near the TRUE/FALSE boundary); cycles 1-5 are
  byte-identical margins (pre-sampling logprobs are deterministic for a fixed prompt/server).

## Verdict (eval fired at 5 rows, re-fired at 6)

- raw drift_check: **ALIGNED**, corr(delta-M, delta-R) = 1.0 (metric deltas track the single
  referent flip perfectly).
- enforced verdict: **INSUFFICIENT** via runner noise floor: net |delta referent| 0.050 < 0.10
  across the window; the one-flip VACUOUS escape is blocked (BURN _c override, working as
  designed). Real measurement, honest kill: one task flip is not drift, and the runner refused
  to let corr=1.0 dress it up.
- Falsifier outcomes: none fired. No LIVE-UNREACHABLE, no LIVE-BAD-RESPONSE, no synthetic rows.

## Instrument alignment (spec-before-behavior, receipt carried in code)

- Served binary confirmed the line-60 debt: request param `n_probs` unchanged, but response
  fields were renamed across llama.cpp versions. The client read `probs[].tok_str`; the server
  returns `completion_probabilities[0].top_logprobs[].token`. Byte-verified via smoke POST
  before any row was written (20 candidates, keys: bytes/id/logprob/token).
- Fix: `tools/probe20_run.py` reader renamed to the served shape, NO fallback branch
  (no-fallback-creep law), comment on N_PROBS carries the confirmation date and evidence.
  Docstring semantics unchanged; measurement values are untouched server logprobs.

## Headless spawn audit (standing law, mid-lane order)

- Zero subprocess.run/Popen call sites authored this session. llama-server and all python
  invocations went through the harness Bash exec channel (harness owns process creation there).
  The one code file touched (probe20_run.py) is spawn-free (stdlib urllib only).

## Law check

- Trust bytes: blob magic checked, response shape checked against the wire, counts from
  `wc -l` (6 rows), PID from `netstat -ano`.
- No synthetic rows: all 6 rows are live POST responses; falsifier untouched.
- No em-dashes in this receipt. One writer per file: series appended only by probe20_run.py;
  this receipt is the lane's only write into burn_reset_20260927/.
