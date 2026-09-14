# W0 bash-local — falsifier receipt (2026-09-07, zcode)

Build #1 of the trajectory spine (watch/TRAJECTORY_LENS_20260905.md): the
bash-local envelope wrapper. Organ: `mag/bash_local.py` (`python -m mag.bash_local
"<command>"`). Tape: `memory/runs/trajectory/steps.jsonl`. House pattern stolen
from mag/grounding_wave.py — hash-chained jsonl, verify subcommand, $0-local,
no docker/config changes. `bash-local` PATH shim intentionally NOT installed
(no host config edits); `python -m mag.bash_local` is the contract.

Row shape (Schema v1): {schema_version (int, MANDATORY — writer gate refuses
without it), ts, session_id (env WORLDLINE_SESSION or per-process), input,
output (stdout tail 4KB), tool_result ({stderr_tail 2KB, exit_code}), reasoning
(env WORLDLINE_REASONING, default ""), timing {start,end,duration_s},
prev_step_hash (per-session chain, genesis 0*16), step_hash (sha256 over
canonical content EXCLUDING step_hash, first 16 hex)}. Tape = untrusted
sidecar: envelope write failure prints a stderr WARN and passes through the
command's real exit code. The command is the contract.

## FALSIFIER (a) — coverage: every wrapped command emits one chained row — PASS
Session w0-falsifier-20260907, three commands:
- `echo hello-w0`            -> row 775d88bcaf4b6a07 <- 0000000000000000, exit 0
- `python -c 'print(1)'`     -> row 82b7f6ef152d14d6 <- 775d88bcaf4b6a07, exit 0
- `python -c '...exit(3)'`   -> row 62de34b5ed584507 <- 82b7f6ef152d14d6, exit 3
  (real exit code passed through — the failing command failed honestly)
All rows schema_version=1; chain links verified by `verify`.

## FALSIFIER (b) — schema gate — PASS
- Writer gate: `build_row(..., schema_version=None)` ->
  `ValueError: schema gate: row rejected — schema_version is mandatory`
- Verifier gate: hand-crafted row WITHOUT schema_version appended to a COPY of
  the tape (real tape left clean) -> `verify` reports:
  `row 4: REJECTED — no schema_version` and exits 1.
  Copy deleted after the test.

## FALSIFIER (c) — coverage positive path — PASS
5 commands wrapped, 5 rows landed, 0 commands ran bare. Final authority pass
(unwrapped): `PASS 5 rows, 2 session(s), tip=63b5ef76bf0e86d1 on steps.jsonl |
all rows valid, chains intact`.

## DOGFOOD — SELF-SEALED (session w0-dogfood-20260907)
The wrapper's own verification pass ran THROUGH the wrapper:
- row f758941565b1d63b <- 0000000000000000 — input `python -m mag.bash_local
  verify`, captured output `PASS 3 rows, 1 session(s), tip=62de34b5ed584507 |
  all rows valid, chains intact`
- row 63b5ef76bf0e86d1 <- f758941565b1d63b — row-count/hash census, exit 0
These two step_hashes are the self-sealed proof: the first rows describing the
verification of the thing that wrote them.

## State
Tape at land time: 5 rows / 2 sessions, chain intact, verify PASS. Next in the
spine (per card, not built here): #2 T1 rejoiner, #3 trajectory_step table
(rejects schema-less writes — this tape is its first tenant).
