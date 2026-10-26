# Mag Estate Resource Audit, 2026-10-23 (~11:50 AM EDT), read-only

Nothing was changed. No processes, models, tasks, config or git were touched. Secrets paths were not opened.

## PC DESKTOP-7C70KSC
- **CPU:** Ryzen 7 3800XT, 16 threads. WMI LoadPercentage read **100%** at the snapshot. A 5 s delta sample showed git at 9%, dllhost 15116 at 7.3%, and powershell at ~8% (that includes this audit), so the load is spiky.
- **RAM:** 64 GB total, **22.7 GB free** at the snapshot. estate_smith logged *avail 1.5 GB* at 09:06, and **pagefile.sys has grown to 63.95 GB** (balloon alert).
- **Disk C:** 1593 GB used, **270 GB free**. Per disk_smith (10/15): docker vhdx 132 GB, zcode_cache 191 GB, hermes_local 145 GB, appdata_temp 83 GB, hiberfil 25.6 GB. gap_sentinel reports local_sovereign_agent growing **28.9 GiB/day (10/20-21)** and 1.1 GiB/day (10/21-22). In logs/, kpi.jsonl alone is **2.9 GB**.
- **GPU:** **AMD Radeon RX 5600 XT, not NVIDIA** (nvidia-smi is absent). The card is 6 GB VRAM per spec. WMI caps the reading at 4 GB, so 6 GB is from the spec sheet, not measured. I could not read live VRAM use without an AMD tool.
- **Docker:** mag-sovereign uses **119.5% CPU and 9.3 GiB** (frozen lab, not touched). mag-mcp 39%/85 MiB. cluster-factorio_0-1 31%/184 MiB. mag-worker 9%/25 MiB. mag-browser 2%/194 MiB. gstd-node and mag-redis are idle.
- **Ollama:** 15 models installed, about 105 GB on disk. Loaded (`ollama ps`): **qwen2.5:7b-instruct-q8_0, 8.6 GB, 49% CPU / 51% GPU, ctx 8192**, expiring in about 9 min. Installed: qwen2.5:7b-instruct-q8_0 8.1G, gemma2:2b-q5 1.9G, gemma:2b 1.7G, Ternary-Bonsai-27B PTQ1 6.6G, athena-class 32G, qwen2.5:7b 4.7G, deepseek-r1:1.5b 1.1G, qwen2.5vl:3b 3.2G, qwen2.5-coder:7b 4.7G, qwen-desk 1.9G, qwen2.5:3b-instruct 1.9G, gemma4-desk 9.6G, gemma4 9.6G, gemma4-hermes 9.6G, nomic-embed-text 274M.
- **Processes:** hermes 5 procs, 236 MB. node 12 procs, 577 MB. ollama 2 procs, 87 MB (the weights sit in the runner). Also running: opencode, ZCode, Discord 605 MB, Docker Desktop.
- **dllhost:** PID 15116, `DllHost.exe /Processid:{DFB65C4C-B34F-435D-AFE9-A86218684AA8}`, started 10/19 00:16. It has used **233,431 CPU-seconds** (about 2.7 CPU-days, roughly 0.7 of a core averaged over 4.5 days), with 8 threads and an 8 MB working set. This AppID is **not registered in HKCR\AppID or HKCR\CLSID**. The other surrogates are normal: WebPlatformStorageServer, Thumbnail Cache, and one unregistered surrogate that is idle.
  - **Verdict: worth investigating.** My guess is a shell or thumbnail/preview handler or third-party extension spinning on a huge folder tree, such as the repo's millions of files. Next read-only step: Process Explorer > PID 15116 > Threads/Image to see the loaded DLL, or search HKLM\SOFTWARE\Classes\AppID and Wow6432Node for the GUID. Ending the process is low-risk (COM respawns it on demand), but that is Nacho's call.
- **Leftover from this audit:** a recursive *.log search I started is still running read-only in the background (PID 14412, powershell). It is safe to let it finish or to end it.

### Scheduled task errors (action, then cause from logs, then recommendation)
| Task | Code | Finding | Rec |
|---|---|---|---|
| MagBreathReplayHourly | 0x1 | Runs `tools.breath_replay_check`. All checks pass except `verkle_knot_in_head`: the tip knot `2026-08-31_0404_constitution..._16115d85.s4.knot.json` is not in HEAD:memory/biography_v2/knots_v2. This is a real content fail, not a runner bug. | **Fix** (commit the knot or repoint the tip). Keep the task. |
| MagCensusPatrolDaily | 0x1 | Runs census + task doctor. exit=1 comes from a FOSSIL-CHECK WARN: queue/lanes/jev/trail.jsonl is 812 h old (bar 720 h). Task doctor flags 8 unhealthy tasks. Working as designed. | **Keep.** Retire the jev lane or raise its bar to clear it. |
| MagGapSentinelDaily | 0x1 | GROWTH alert every day: local_sovereign_agent is over 1 GiB/day. Correct alert. | **Keep.** Fix the growth (kpi.jsonl at 2.9 GB, pytest dirs, caches). |
| MagTipWitnessDaily | 0x2 | Gist publish gets HTTP 403: the token lacks Gists read/write scope. | **Fix:** grant the gist scope, or **drop** if the public witness isn't needed. |
| MagEstateSmithDaily | 0x1 | Alert exit: RAM PRESSURE (1.5 GB avail) and PAGEFILE BALLOON at 64 GB. Correct alert. Its action has an empty working dir, but it still ran. | **Keep.** Act on RAM: reboot to shrink the pagefile, set a fixed pagefile. |
| MagLeaveProtocolDaily | 0x1 | Runs `tools\leave_dispatcher.py`. **No log found** in logs/, so the cause is not determined. | **Investigate:** run it by hand to see stderr. Fix or drop after that. |
| MagLongrunnerPatrolDaily | 0x1 | `ModuleNotFoundError: No module named 'tools'` daily since at least 10/20. **The action has an empty WorkingDirectory** (`wd`). | **Fix:** set the working dir to the repo root (or `Set-Location` in the ps1). Trivial. |
| MagDiskSmithDaily | 0x41306 | 0x41306 = task was terminated. Limit is **PT30M**, and the last good jsonl row is 10/15. My guess is that the walk of 1.6 TB plus millions of files now exceeds 30 min. | **Fix:** raise the limit or narrow the scan. Disk_smith data is stale and feeds the alerts. |
| MagProbeCadence | 0x800710E0 | 0x800710E0 = start refused. The task is **currently Running** and MultipleInstances=IgnoreNew, so new triggers are refused while an instance runs, possibly a hung one. Its wd is also empty. | **Fix:** check why the instance never ends. Set the working dir. Drop if probes now run elsewhere. |
| MagCorpusRescanDaily | 0x800710E0 | Last log run was 10/22 (exit 0). No 10/23 entry; the last run time is 05:29, not the 03:30 schedule. My guess is that a catch-up start was refused (IgnoreNew, or ACOnly/conditions). The job itself is healthy. | **Keep.** Watch tomorrow. Consider dropping to weekly given corpus growth. |
| MagVisionNightly | 0x800710E0 | Same 05:29 refusal pattern. The log says "coverage 1980/1980, no-op" every night. | **Drop** (or weekly). It does nothing and wakes Ollama. |
| (also) MagBreathWatchdog 0x41301 | running | n/a | n/a |
| MagLabKit8765 0xFFFFFFFF, MagPrivateOffice8765 0xC000013A | dead since 8/1 | Stale | **Drop** or disable. |

## bob (laptop)
- **CPU:** Ryzen 3 3200U, 4 threads, 12% load.
- **RAM:** **3.4 GB total, 0.3 GB free.** It is maxed.
- **Disk C:** 97 GB used, 21 GB free.
- **Processes:** ZCode 15 procs, 206 MB WS (heavy CPU time). Antigravity 6 procs, 72 MB. opencode-cli 1. hermes 1. scrcpy, murmure. **No Ollama.**
- **Verdict:** CPU is idle but RAM is **overcommitted**. bob can host at most 1-2 remote-API callers (agy or ZCode lanes). No local models.

## Phones
- **Pixel 11 Pro:** the machine is a phone, so Grok Bot offers no shell/read there. No metrics. Tailscale shows it listed (100.79.122.101), with no ping attempted from me beyond status.
- **Moto G 5G:** tailscale ping pong 107 ms (direct LAN 192.168.86.40). **Unreachable for metrics** (no SSH by instruction).
- **T90:** tailscale ping pong 90 ms (direct 192.168.86.26). **Unreachable for metrics.**
- mag-openclaw: offline 46 days.

## Recommendations
**Ollama/VRAM (about 6 GB):**
- The current hold-rung load, the 7B q8 at 8.6 GB, is **half on CPU**. It is slow and adds to RAM pressure.
- Use **qwen2.5:7b (q4, 4.7 GB)** as the hold rung. It should mostly fit in VRAM at ctx 4-8k (a guess until measured).
- Keep **qwen2.5:3b-instruct (1.9 GB)** warm for gate and beacon tests.
- Both together (about 6.6 GB plus KV) won't fully fit. Keep the 3B warm (long keep_alive) and load the 7B q4 on demand. Or keep only the 7B warm and accept 3B load churn.
- nomic-embed is fine.
- Prune candidates to free about 70 GB of disk: athena-class 32G (cannot run on this box), the three gemma4 9.6G variants (pick one), and the q8 7B once q4 is adopted.

**Spreading Ractor-parable and Door/keyed-verse jobs:**
- These are mostly remote-model callers, so the constraint is RAM per runner and provider quota, not CPU.
- **PC:** the coordinator plus anything needing Ollama (3B gates, 7B hold). Free RAM first: mag-sovereign at 9.3 GB is frozen and idle-by-intent; consider pausing it (Nacho's call). Run the ZAI Fostertron Max heavy lanes here while quota lasts (until November).
- **bob:** 1 lane only (agy/Antigravity or ZCode), e.g. the Door/keyed-verse steady lane on Nacho Business Corp Lite. Don't run both ZCode's 15 procs and Antigravity under load in 3.4 GB.
- **Moto / T90:** once SSH/Termux is restored, thin HTTP callers (curl/python) for Lite or OpenCode lanes, one job each. They are reachable on the tailnet now.
- **DeepSeek (scarce):** reserve for one gating/judge rung, not bulk generation.
- Stagger Ractor-parable and Door so heavy-provider calls don't overlap on the same box.

**Hygiene:** reboot the PC when convenient (pagefile 64 GB, dllhost spin) and set a fixed pagefile. Address the repo growth and 2.9 GB kpi.jsonl.
