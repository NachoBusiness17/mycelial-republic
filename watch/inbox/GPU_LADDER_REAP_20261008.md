# GPU LADDER REAP 2026-10-08

Operator new-boot ask ("new boot what's going on" + screenshot, then "go"): identify
the 8 idle llama-server.exe entries in Task Manager, reap them, file the receipt.

## What was running

8 llama-server.exe processes, ~45GB combined working set, all leftovers of the
overnight mesh burn's GPU-ladder lane (dwfrun-6a821d9c, the llama.cpp RPC / LM
Studio Vulkan door test in `C:/Users/foste/llamacpp_rpc_spike/`). Every one served
the same `qwen2.5-7b-q4_k_m.gguf`; backends mixed (`llama.cpp-win-x86_64-vulkan-avx2-2.31.2`
and `avx2-2.31.2`), gpu-layers 33 or 0, ctx-size 512 (one at 4096), n-predict 128.
All 8 held `127.0.0.1:8080` simultaneously, a SO_REUSEADDR collision where at most
one could actually serve. Zero CPU, zero disk, zero network at reap time. PIDs
reaped (taskkill /F, 8x SUCCESS): 19692, 20952, 26364, 26564, 29292, 29296, 29992, 30684.

## Evidence

- Free physical RAM 4.9GB before the reap, 29.1GB after (+24.2GB).
- `Get-Process llama-server` count after: 0. Port 8080: zero LISTENING rows.
- The machine was ~5GB from the wall when the operator screenshotted it.

## Gap found and closed (tightening, never loosening)

`configs/longrunner_policy.json` `watch_process_names` carried
python/powershell/node/ollama only, so the MagLongrunnerPatrolDaily 08:45 patrol was
structurally blind to headless llama-server spawns; these 8 sat roughly a day at
~45GB unflagged. Added `llama-server.exe` to the watch list 2026-10-08. The patrol is
alert-only (memory/attention.md, never kills), so a legitimately long LM Studio GUI
serving session will now surface as an alert row; if that proves noisy the operator
rules on an allowlist marker, not on removing the watch name.

## Bun entry verdict

The screenshot's 13GB "Bun" process no longer exists: a post-reap sweep of process
names and command lines (WMI + tasklist + Get-Process) finds zero bun processes. It
exited or released its pages between the screenshot and this window. If it returns,
it will need an elevated eye (it was invisible to non-elevated queries at screenshot
time). com.docker.backend today reads 112MB.

## Still standing

- Control Room dashboard alive, HTTP 200 on 127.0.0.1:8765 via com.docker.backend
  forwarding (the caged mag-sovereign service, tier A per the longrunner law).
- Overnight landings intact: port wave receipts through 01:44 ET, day-7 mine banked
  23:27, Hermes 24/7 burn cycling (m010/m011/m012 work files).
- Operator dawn list unchanged (GSTD wallets, bridge-vote GO, ESTATE_INDEX --apply,
  xAI reissue, et al.).
