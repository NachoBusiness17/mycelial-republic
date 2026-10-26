# INSTALL TEST RECEIPT - walkthrough_20260109

Fresh-install simulation of the Mag Resource Harness from a local file clone,
run exactly as a stranger following README.md / AGENTS.md / scripts/ensure_venv.ps1
would. Machine: the operator's Windows 10 box (win32 10.0.19045), Git Bash +
PowerShell, source repo at
C:\Users\foste\Documents\projects\local_sovereign_agent (commit 84e29dc32,
drift-patrol, was receiving automation commits during the test).

VERDICT: install WORKS from scratch. Every documented step exits 0 on a fresh
clone with a brand-new venv. One demo-level gotcha dominates: the full git
history is 14.37 GiB packed (26 GB on disk checked out), so a FULL clone took
35 min 05 s; use the shallow fast path for the live walkthrough.

## Environment snapshot (stranger-view prereq checks)

| Check | Command | Result |
|---|---|---|
| Python launcher | `py -3.12 --version` | Python 3.12.10 (real interpreter) |
| Bare `python` (Git Bash PATH) | `where python` | C:\...\Programs\Python\Python312\python.exe FIRST here; on the operator's usual PowerShell the bare `python` resolves into the Hermes venv (AGENTS.md trap) |
| git | `git --version` | 2.55.0.windows.2 |
| Disk free | `Get-PSDrive C` | 448.7 GB free (need ~30+ GB for clone + venv) |
| Ollama | GET 127.0.0.1:11434/api/version | HTTP 200, up |
| Ollama models | GET /api/tags | 15 present incl gemma:2b + gemma4:latest (both required models present) |

## Step log (all wall-times real, this run)

### 1. Full clone (honest stranger number)

```
git clone --no-local C:\Users\foste\Documents\projects\local_sovereign_agent %TEMP%\mag_walkthrough_test
```

- WALL: 2104.8 s = 35 min 05 s
- Checked out 57,939 files; on-disk size 26 GB (includes later venv build)
- Source .git: 14.37 GiB packed (git count-objects -vH), 16,060 loose objects,
  plus 8 pre-existing tmp_pack garbage files in the source (pre-date this test;
  concurrent automation, not touched)
- Progress curve: 2.2 GB @ ~5 min, 3.4 GB @ ~12 min, 6.0 GB @ ~16 min, done @ 35 min
- A GitHub clone moves the same bytes over the network: strictly slower or equal.

### 1b. Shallow fast path

```
git clone --depth 1 --no-local <repo> %TEMP%\mag_walkthrough_shallow
```

- WALL: 1594.4 s = 26 min 34 s; 25 GB on disk; 57,940 files
- VERDICT: depth does NOT save the demo. The tip content itself (57,940 files)
  is the mass, not the history depth.

### 1c. Plain local clone (hardlinks, no --no-local)

```
git clone <local-repo-path> %TEMP%\mag_walkthrough_hardlink
```

- WALL: 1856.7 s = 30 min 57 s; 26 GB on disk
- Even with hardlinked objects, the 57,940-file checkout dominates. Every
  clone flavor on this disk (which carries the estate's concurrent automation,
  same as tonight) is a 25-35 minute ceremony.
- CONSEQUENCE (runbook law): the live demo PRE-STAGES the clone during
  preflight; the on-stage arc starts at ensure_venv.ps1.
- NOTE: the install steps below were verified against the FULL clone working
  tree; trees are content-identical at tip, but the venv/doctor sequence was
  not separately re-run inside the shallow/hardlink clones (timing only).

### 2. venv creation + deps (documented path, unmodified script)

```
cd %TEMP%\mag_walkthrough_test
powershell -ExecutionPolicy Bypass -File scripts\ensure_venv.ps1
```

- WALL: 273.9 s = 4 min 34 s, exit 0
- venv on disk after: 742 MB
- ensure_venv.ps1 found `py` launcher -> `py -3.12 -m venv .venv` (avoids the
  bare-python-is-Hermes trap), then `pip install -r requirements.txt`
- 94 packages installed fresh, incl langgraph 1.2.14, pandas 3.0.6,
  scikit-learn 1.9.1, scipy 1.18.1, cryptography 50.0.2, faster-whisper 1.2.1,
  ctranslate2 4.8.2, textarena 0.7.4, matplotlib 3.11.2, fastapi 0.143.0
- Import gate passed: script's own check printed `OK`
- Final line printed: `Use: mag.cmd doctor   or   .\mag.ps1 doctor`
- CAVEAT (honest): pip's wheel cache on this machine is WARM; a cold-cache
  stranger additionally downloads the wheels (roughly 1-2 GB) before install.
  Unmeasured here; the runbook says "about 5 minutes, longer on a cold machine".
- Cosmetic noise only: PowerShell wraps pip's stderr progress as a
  NativeCommandError record (exit code still 0) and pip prints an upgrade
  notice. Neither affects the result.

### 3. mag.cmd doctor

```
cmd /c mag.cmd doctor
```

- WALL: 0.9 s, exit 0
- Output (fresh clone, no lab running, no .env):
  - `status=degraded live_stale=True` <- HONEST and EXPECTED on a fresh install
  - `missing: integral Mag process (watch+companion heartbeat); fresh live board`
  - `L0_ollama: ok=True` with all 15 models listed
  - `L1_openrouter: ok=False ... Set OPENROUTER_API_KEY` <- expected: .env is
    gitignored, fresh clone has none (`.env.example` IS tracked for copying)
  - `L2_grok: ok=True grok CLI on PATH` (machine-specific; stranger box may differ)
  - Full JSON body incl hallucination_guard + reconnect card prints after
- CROSS-TALK CAUGHT: `port_8765: true, board_api: true` because the REAL Mag
  lab of the source install was live on localhost during the test. On a truly
  fresh machine those read false. Demo note: doctor in a clone sees the port,
  not the clone's own process; heartbeat file decides alive.

### 4. mag.cmd context-pack

```
cmd /c mag.cmd context-pack
```

- WALL: 12 s, exit 0
- Boot-regen chain fired and passed: `BOOT-REGEN: ok (zknot=0.0d warm_boot=0.0d
  rib_boot=0.0d lawpack=1.639d) - all components regenerated and fresh`
- Pack rendered fully (L0 policy, compiled laws, operator directives, RIB
  doctrine, L4 heat) and wrote memory/context_pack_latest.md + .json in the clone
- Honest liveness line at the end: `census patrol dark: no START stamp found in
  census_patrol.log` <- correct: the scheduled task is not registered on a
  fresh install; it is an ops nicety, not an install failure

### 5. Cheap real commands

| Command | WALL | Exit | Result |
|---|---|---|---|
| `mag.cmd improve --status` | 0.6 s | 0 | `ok: true`, empty candidate state (honest fresh), scheduled_task check ok |
| `mag.cmd bonds` | 0.3 s | 0 | `ok: true`, REAL WRITE: memory/bonds_active.md (1,004 chars) + .json created in the clone |
| `mag.cmd models` | 0.6 s | 0 | `ok: true, ollama_up: true`, 15 tags, roles table with `present: true` per role |

### 6. GSTD node demo URL (read-only GET, node and wallet untouched)

```
curl https://platform.gstdtoken.com/api/v1/nodes
```

- HTTP 200 in 0.41 s
- gstd-desktop LIVE in the nodes array: 14 tasks_completed,
  gstd_earned 0.9014930, reputation_score 57, version 3.5.0,
  avg_response_ms 6162, early_adopter 1, 15 capabilities listed
  (gemma4:latest, gemma:2b, nomic-embed-text, ...)
- Also on the board: GSTD Bootstrap Pi (294 tasks, 52.2355 GSTD),
  node-LAPTOP-UTO92FB9 (idle)

## Gotchas a stranger would hit (ranked)

1. FULL CLONE MASS: 14.37 GiB pack / 26 GB tree -> 35 min at local-disk speed.
   Worst gotcha by far. Mitigation: `--depth 1` (fast path, timed above) or
   pre-stage the clone before the audience arrives.
2. README Setup card says bare `python -m venv` + `Activate.ps1`. On the
   operator's normal shell the bare `python` is the HERMES venv interpreter
   (AGENTS.md: "Default shell python is often Hermes"). ensure_venv.ps1 avoids
   this by preferring `py -3.12`. Strangers without the `py` launcher and with
   a polluted PATH can build a venv from the wrong interpreter.
3. Activate.ps1 hits PowerShell execution policy on default Windows installs
   (that is why every doc card carries `-ExecutionPolicy Bypass`).
4. No `.env` in the clone (gitignored, correct): L1 openrouter lane reads
   ok=False until the stranger copies `.env.example` and pastes keys. Doctor
   still exits 0.
5. `status=degraded` from doctor on a fresh install is the honest state (no lab
   process running yet), NOT a failed install. Without a one-line expectation
   in the README a stranger may think they broke something.
6. First-run surfaces that depend on machine state: L2_grok ok only if the
   grok CLI is on PATH; census patrol "dark" line because the scheduled task is
   not registered; port_8765 cross-talk if another Mag lab is already running.
7. AV scan: no AV slowdowns observed on this box for pip/clone (Defender
   default). Not measured under third-party AV; the runbook keeps an AV note in
   pitfalls anyway.

## Named gaps (filed, NOT hot-fixed)

- GAP-W1 (structural): repo mass. 14.37 GiB history makes any full clone a
  30+ minute ceremony. Owner call: document `--depth 1` for demos and/or ship a
  release tarball; a history slimming pass is an operator decision.
- GAP-W2 (doc, one line): README Setup does not mention ensure_venv.ps1 (the
  script the rest of the docs standardize on). Fixed in this session as the one
  trivial README addition (see Source changes below).
- GAP-W3 (doc): no line telling a stranger that doctor `degraded` is expected
  before the first `lab` run. Filed rather than hot-fixed to keep the README
  diff minimal.
- GAP-W4 (cosmetic): doctor's integral probe reads localhost ports, so a clone
  reports the source install's live lab (port_8765 true while heartbeat dead).
  Display-level confusion only; no action taken.

## Source changes (trivial, this session)

- README.md Setup card: added the ensure_venv.ps1 alternative line (doc-only,
  one comment line inside the existing fenced block, fence-owner comment
  untouched). No code, spec, or behavior changes anywhere.

## Cleanup

- %TEMP%\mag_walkthrough_test (full clone + venv) deleted at session end.
- %TEMP%\mag_walkthrough_shallow deleted at session end.
- Logs: %TEMP%\mag_walkthrough_{venv,doctor,ctxpack,improve,bonds,models}.log
  deleted with the clones.
- GSTD node and wallet files: untouched throughout (read-only GET only).

Operator drive path: WALKTHROUGH_RUNBOOK.md in this directory.
