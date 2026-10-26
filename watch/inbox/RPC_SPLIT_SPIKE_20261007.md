# RPC SPLIT SPIKE 2026-10-07 (steal-map P3, desktop half; bob off-limits, no remote exec)

- Probe: `watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md` P3 "llama.cpp RPC
  spike: split a small model desktop+bob, measured tokens/sec vs single-host".
  This lane ran the DESKTOP half only: two LOCAL rpc-server instances, split
  proven and measured. The bob join is banked as the one-liner below for his
  seat's next boot (this lane did not touch bob).
- Class note: gemma-2b (2B) is the same class the ALoDLM receipt names as the
  garden's first DLM candidate (`watch/inbox/ALODLM_2610.04198_20261006.md`
  S1, "1.7B first"). What this run adds to that door: the box now has a
  working llama.cpp CPU serving path for 2B-class GGUF at the numbers below;
  whether ALoDLM ships a GGUF conversion is UNVERIFIED here (this build serves
  GGUF only) and stays with the S1 sitting.

## Build provenance

- No existing build on PATH (llama-server / llama-cli / rpc-server all
  absent), no scoop, no choco. Downloaded the official release:
  `llama-b11457-bin-win-cpu-x64.zip`, sha256
  `ED20ED40E10C04D0853D8ACF8700F0E6C1BB8212F0CC70C3A0DA13DCBBC1B802`.
- Unpacked at `C:\Users\foste\llamacpp_rpc_spike\` (outside the repo tree).
- `llama-server.exe --version`: `version: 0.6.0-dev (build 11457, commit
  5ad1c5da0)` built with Clang 20.1.8 for Windows x86_64.
- The RPC server binary in this release layout is `ggml-rpc-server.exe`
  (default host 127.0.0.1, default port 50052, default threads 8; log line
  "Starting RPC server v8.0.0"). The client flag is `--rpc SERVERS
  (comma-separated list of RPC servers (host:port))` with env
  `LLAMA_ARG_RPC` (verified via `llama-server.exe --help`).
- CPU build chosen honestly: the box is AMD Ryzen 7 3800XT 8c/16t + AMD
  Radeon RX 5600 XT, no NVIDIA, so the CUDA zip is dead weight. The Vulkan
  zip (5600 XT offload) is the follow-up steal, not run this sitting.
- Model: Ollama `gemma:2b` weights blob copied to
  `C:\Users\foste\llamacpp_rpc_spike\gemma-2b-it-q4_0.gguf`, size
  1,678,447,520 bytes (manifest layer
  `sha256:c1864a5eb19305c40519da12cc543519e48a0697ecd30e15d5ac228644957d12`).

## Measurement (fixed prompt "Count from 1 to 50, one number per line.", n_predict 64, temperature 0, cache_prompt false, default n_threads = 8, same binary and flags both sides)

Baseline, single-host CPU (llama-server local, from `server_baseline.log`):

- run 1: prompt eval 34.27 tok/s; generation 6.48 tok/s (154.43 ms/token)
- run 2: prompt eval 43.93 tok/s; generation 6.01 tok/s (166.33 ms/token)

Split, two LOCAL rpc-servers (`ggml-rpc-server.exe` on 127.0.0.1:50052 and
127.0.0.1:50053) + `llama-server --rpc 127.0.0.1:50052,127.0.0.1:50053`
(from `server_split.log`):

- run 1: prompt eval 24.30 tok/s; generation 6.25 tok/s (159.97 ms/token)
- run 2: prompt eval 28.48 tok/s; generation 5.94 tok/s (168.38 ms/token)

## The split is real (placement proof, not a silent fallback)

- `rpc_50052.log` byte-records `Accepted client connection` (a live RPC
  session); both server logs show 61 / 65 accept+close pairs across the two
  llama-server sessions. The exact per-call connection mechanics of the v8.0.0
  protocol were not probed this sitting; the counts are recorded as measured.
- Working set DURING a live split session (tasklist at the moment both servers
  held the model): rpc :50052 = 694,352 K, rpc :50053 = 1,103,512 K. Sum is
  about the full 1,600 MiB model resident on the two RPC instances, split
  unevenly by the default scheduler. Post-session both drop to ~7 MB, so the
  numbers above are the residency moment, not idle.

## Verdict (measured, small-model class, one box)

- Generation: split 5.94 to 6.25 tok/s vs single 6.01 to 6.48 tok/s, within
  noise. Splitting a model that already fits one host buys ZERO generation
  throughput on this box (one memory subsystem, IPC added per layer).
- Prompt eval: split 24.30 to 28.48 tok/s vs single 34.27 to 43.93 tok/s,
  25 to 35 percent SLOWER through the two-hop localhost RPC path.
- The exo door therefore does NOT open via single-box splitting of small
  models. It opens where the RPC contract actually pays: a model that does
  not fit one host's RAM/VRAM, or desktop+bob with two separate memory
  subsystems behind one endpoint. The bob one-liner below is the join for
  that case, and the exo-vs-RPC choice stays open until a cross-machine run
  measures it (bob's seat, next boot).

## THE BOB-SIDE ONE-LINER (join the pool on his next boot)

Bob side (PowerShell, from the spike dir after dropping the same zip's
`ggml-rpc-server.exe` + its DLLs there; `-H 0.0.0.0` so the desktop can reach
him through tailnet/LAN; allow TCP 50052 in Windows Defender Firewall on
first-run prompt):

```powershell
.\ggml-rpc-server.exe -H 0.0.0.0 -p 50052 -t 8
```

Desktop client side (join bob + the local instance into one pool; the
verified env var is `LLAMA_ARG_RPC`, the ask's `RPC_SERVERS` name does not
exist in this build):

```powershell
$env:LLAMA_ARG_RPC="127.0.0.1:50052,BOB_HOST_OR_TAILNET_IP:50052"
.\llama-server.exe -m gemma-2b-it-q4_0.gguf --tensor-split 1,1 --port 8791
```

(Or the flag form: `--rpc 127.0.0.1:50052,BOB_HOST:50052`. `--tensor-split`
apportions model bytes across the two pool members; defaults are equal.)

## Honest gaps

- No bob-side execution (task forbids remote exec); the one-liner is untested
  cross-machine until his seat runs it.
- The 5600 XT sits idle in this measurement (CPU build); the Vulkan build is
  one sitting away and would change the single-host baseline more than the
  split mechanics.
- The bench harness is `C:\Users\foste\llamacpp_rpc_spike\bench.sh` (2 runs
  per config); a 3-run median and a Vulkan pair would tighten the numbers.
- Both local rpc-servers were stopped at lane end (pids 27108 and 12404
  killed); nothing is left listening on 50052/50053.
