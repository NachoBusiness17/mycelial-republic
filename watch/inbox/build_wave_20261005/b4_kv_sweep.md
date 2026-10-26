# B4 KV slot pilot unblock + f16/q8_0/q4_0 KV-type sweep (build-it-all wave, 2026-10-05)

Lane B4. Receipt written 2026-10-05T07:21:20Z. Laws honored: venv python for
python, direct .exe for llamacpp, no em/en-dashes in new text, no git commit.

## 1. COMMON_PATHS fix (task 1)

The mine card's finding verified with `ls`: `tools/llamacpp/llama-server.exe`
IS in-tree (plus llama-bench.exe and siblings, Vulkan + CPU backends), and the
pilot's COMMON_PATHS (was lines 39-48) missed it, so `find_llama_server()` fell
through to `NOT_INSTALLED` exit 3 on a machine that actually has the binary.

Fixed files:

- `tools/kv_slot_pilot.py`: COMMON_PATHS now checks
  `PROJECT / "tools" / "llamacpp" / "llama-server.exe"` FIRST, with a comment
  naming the fix and this receipt. Spec-first: `tools/kv_slot_pilot.md` status
  (was "STAGED, binary absent") rewritten to UNBLOCKED with a new vendored-path
  row in the section 0 table and an updated section 10 honest-limits block
  (replay still first-run-untested; longest stored sessions exceed the pilot's
  fixed `-c 32768` context, a known limit to cure before the full replay).

Function-level proof (venv python, import + call):

```
find_llama_server -> C:\Users\foste\Documents\projects\local_sovereign_agent\tools\llamacpp\llama-server.exe
VENDORED PATH RESOLVES: PASS
```

## 2. Gate contract (reported, both)

- `py_compile`: `./.venv/Scripts/python.exe -m py_compile tools/kv_slot_pilot.py`
  -> PY_COMPILE: PASS
- ratchet: `./.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
  -> `scope=8 changed files; hits=2; registered=2; NEW=0` -> RATCHET: PASS,
  no unregistered (new) debt.
- Extra: `tools/citation_lint.py check --changed` -> zero findings in lane B4
  files (remaining output rows are pre-existing sibling rib findings, untouched).

## 3. Environment (named once, denominator law)

- Binaries: vendored `tools/llamacpp/` build `d2e54583c` / b11149, Vulkan
  backend on AMD Radeon RX 5600 XT (fp16: 1, matrix cores: none, int dot: 0)
  plus CPU backend (Ryzen 7 3800XT). Same binaries the pilot now finds.
- Model: Ollama `deepseek-r1:1.5b`, existing blob reused in place, no download:
  `sha256-aabd4debf0c8f08881923f2c25fc0fdeed24435271c2b3e92c4af36704040dbc`
  (1,117,320,512 bytes; bench metadata reads it as qwen2 1.5B Q4_K - Medium,
  1,777,088,000 params).
- All arms: `-ngl 99 --flash-attn on`, matched K/V type per arm (f16, q8_0,
  q4_0), context 4096 or bench default.

## 4. Exact commands (as run, from tools/llamacpp/)

llama-bench (3 reps, CSV, moments 2026-10-05T07:11:00Z to 07:13:22Z):

```
./llama-bench.exe -m C:/Users/foste/.ollama/models/blobs/sha256-aabd4deb....dbc \
  -ngl 99 -fa on -ctk f16 -ctv f16 -p 512,2048 -n 128 -r 3 -o csv
# same with -ctk q8_0 -ctv q8_0, and -ctk q4_0 -ctv q4_0
```

llama-server (one launch per arm, single cold /completion call, final clean run
finished before 2026-10-05T07:21:20Z). Arm ports 8095, 8096 and 8097 with
`-c 4096` and `--parallel 1`, per the launch banners recorded in
b4_server_f16.log, b4_server_q8_0.log and b4_server_q4_0.log. The payload
tokenizes to prompt_n 1322 with n_predict 64 (b4_server_f16_completion.json,
b4_server_q8_0_completion.json, b4_server_q4_0_completion.json). Payload body
file: see section 9. Per-arm command shape (placeholders for arm port and the
section 9 payload path, so no number sits next to a cited file):

```
./llama-server.exe -m C:/Users/foste/.ollama/models/blobs/sha256-aabd4deb....dbc \
  --host 127.0.0.1 --port <arm-port> -ngl 99 --flash-attn on -ctk f16 -ctv f16 \
  -c 4096 --parallel 1
curl -s http://127.0.0.1:<arm-port>/completion -H 'Content-Type: application/json' \
  --data @<payload file from section 9>
# same per arm with q8_0 / q4_0; kill-until-zero between arms (see 8)
```

## 5. Measured rows: llama-bench (throughput instrument)

TTFT ms below is the bench test's avg_ns (wall time of the prompt-processing
test), i.e. TTFT for that prompt length; t/s is avg_ts.

| Arm (K=V) | pp512 t/s | TTFT@512 ms | pp2048 t/s | TTFT@2048 ms | tg128 t/s |
|---|---|---|---|---|---|
| f16/f16   | 671.84 | 762.9 | 364.18 | 5623.6 | 153.44 |
| q8_0/q8_0 | 1277.25 | 401.4 | 363.15 | 5640.0 | 139.10 |
| q4_0/q4_0 | 1307.74 | 391.7 | 372.80 | 5493.6 | 132.28 |

## 6. Measured rows: llama-server /completion (server instrument, clean run)

Prompt = 1322 tokens, cold, single shot per arm; TTFT is timings.prompt_ms.

| Arm (K=V) | TTFT ms | prefill t/s | decode t/s (64 tok) |
|---|---|---|---|
| f16/f16   | 2538.0 | 520.9 | 55.86 |
| q8_0/q8_0 | 4120.3 | 320.9 | 100.76 |
| q4_0/q4_0 | 3983.7 | 331.9 | 110.90 |

## 7. Findings (instruments disagree; name the instrument before quoting)

- llama-bench runner: quantized KV nearly doubles short-prefill speed
  (pp512 671.8 -> 1277.3 / 1307.7 t/s, TTFT@512 762.9 -> 401.4 / 391.7 ms)
  and costs ~9-14 percent decode (153.4 -> 139.1 / 132.3 t/s). pp2048 is flat
  across arms (~364-373 t/s), so the quant prefill win fades at longer prompts.
- llama-server continuous-batching path: the direction flips. f16 prefill is
  fastest (520.9 t/s, TTFT 2538 ms) but decode is SLOWEST (55.9 t/s); q8_0/q4_0
  KV nearly double decode (100.8 / 110.9 t/s) at a ~1.6x TTFT cost.
- Pilot implication: the pilot doc's q8_0 KV default is the right call for the
  replay workload (long prefix, restore-once, then decode-heavy turns, KV bytes
  halved), but fresh-cold-prefill-heavy clients on this GPU may prefer f16.
- The two instruments never ran the same prompt shape; never difference their
  t/s against each other (census denominator law applies to benchmarks too).

## 8. Incident log (why the banked server rows are run 3)

- Run 1 (invalid, discarded): Git Bash `$!` is not a Windows PID, so
  `taskkill //F //PID $SPID` missed; all three arms shared port 8090 and the
  q8_0/q4_0 completions hit the warm f16 server (prompt_n=1 tells).
- Run 2 (invalid, discarded): a GPU-stuck llama-server survived
  `taskkill //F //IM` and held VRAM; q8_0/q4_0 arms ran contended
  (decode 16.0 / 32.8 t/s tells).
- Run 3 (banked): precondition `tasklist` count zero before every arm,
  `taskkill //F //IM` swept in a loop until zero after every arm.
- Respawner identified AFTER banking: the "new PID each sweep" pattern is the
  operator's own Ollama service. Its internal runner is also named
  llama-server.exe
  (`C:\Users\foste\AppData\Local\Programs\Ollama\lib\ollama\llama-server.exe`,
  parent the Ollama app, observed loading the qwen2.5:7b blob, spawned
  2026-10-05T07:21:34Z). The blanket `taskkill //F //IM llama-server.exe` was
  killing Ollama's runner too; Ollama restarts it, which reads as respawning.
  HAZARD + corrected law for future sweeps: kill only the server you spawned,
  resolved to its own Windows PID via a commandline match (vendored
  tools/llamacpp path or the arm port), never by image name; precondition
  checks must distinguish vendored test servers from Ollama's runner by
  executable path. The operator's runner was left alive at close.
- Residual caveat on run 3: a mid-arm Ollama runner spawn cannot be fully
  excluded as a contention source (preconditions were verified zero at every
  arm launch, and the banked pattern, quantized-KV decode about 2x f16, is the
  expected KV-bytes direction; run 2's contended arms showed the OPPOSITE,
  quant decode far BELOW f16, so the run 3 signature is not a contention one).

## 9. Artifacts

- Raw bench CSV (all 3 arms): `watch/inbox/build_wave_20261005/b4_llama_bench_raw.csv`
- Server run log (all 3 runs' markers, audit trail): `watch/inbox/build_wave_20261005/b4_llama_server_raw.log`
- Per-arm server stdout: `b4_server_f16.log`, `b4_server_q8_0.log`, `b4_server_q4_0.log`
- Per-arm completion JSON (clean run 3): `b4_server_{f16,q8_0,q4_0}_completion.json`
- Payload: `b4_payload.json` (6600 chars, fixed text)
- Fixed pilot: `tools/kv_slot_pilot.py` + `tools/kv_slot_pilot.md`

## 10. Limits / follow-ups

- KV memory bytes per arm were not measured (no VRAM probe); the q8_0 halves /
  q4_0 quarters KV property is a design fact, not a row here.
- The pilot's full 10-session replay is still unrun: fix the `-c 32768` context
  vs multi-MB sessions mismatch (size filter or bigger context) first; then the
  slot save/restore speedup measurement is one command with the now-found
  binary: `.venv\Scripts\python.exe tools\kv_slot_pilot.py --model deepseek-r1:1.5b`.
