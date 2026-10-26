# WALKTHROUGH RUNBOOK - live install demo - walkthrough_20260109

Lane: WALKTHROUGH. Written for the operator driving the demo live tonight.
Every wall-time below is REAL, measured this morning on this box (receipt:
INSTALL_TEST_RECEIPT.md in this directory). No invented numbers.

## SCOPE (say this out loud, do not skip)

Tonight's path is the REPO INSTALL: clone + venv + mag.cmd commands, proven
green on a fresh clone this morning. The one-command CLI/Electron installer is
the 10/30 conference demo, NOT tonight. Never promise it. If asked: "the
installer wraps exactly what you are watching me type by hand."

## Measured facts (this box, this morning)

| Step | Command | Wall | Exit |
|---|---|---|---|
| Full clone (--no-local, honest stranger) | git clone <repo> dest | 35 min 05 s | 0 |
| Shallow clone (--depth 1) | git clone --depth 1 <repo> dest | 26 min 34 s | 0 |
| Plain local clone (hardlinks) | git clone <local-path> dest | 30 min 57 s | 0 |
| venv + all deps | powershell -ExecutionPolicy Bypass -File scripts\ensure_venv.ps1 | 4 min 34 s | 0 |
| doctor | mag.cmd doctor | 0.9 s | 0 |
| context-pack | mag.cmd context-pack | 12 s | 0 |
| improve --status | mag.cmd improve --status | 0.6 s | 0 |
| bonds (real write) | mag.cmd bonds | 0.3 s | 0 |
| models | mag.cmd models | 0.6 s | 0 |
| GSTD nodes API | browser / curl | 0.4 s | HTTP 200 |

Why every clone flavor is 25-35 min: the repo carries 57,940 files / 26 GB on
disk (14.37 GiB git pack). Depth does not save you; the tip content itself is
the mass. All three variants were measured while the estate's automation was
writing to the same disk, which is also tonight's condition.

DISK LAW: the clone is PRE-STAGED during preflight. The on-stage arc starts at
ensure_venv.ps1. Do not clone on stage unless the slot is 45+ minutes (see
Long-form variant at the end).

## PREFLIGHT CHECKLIST (do these T-30, before anyone is watching)

1. Free space: `Get-PSDrive C` -> need 35+ GB free (clone 26 GB + venv 0.74 GB,
   plus headroom). This morning's baseline: 448.7 GB free.
2. Pre-stage the demo clone (fresh, NO venv inside it yet):
   `git clone C:\Users\foste\Documents\projects\local_sovereign_agent %TEMP%\mag_walkthrough_demo`
   Start it T-30; it needs its 30 minutes. Verify after: `dir` shows mag.cmd,
   main.py, scripts\ensure_venv.ps1, and NO .venv directory.
   (Already-built proof clone from this morning's test was deleted; stage a new
   one so the on-stage venv build is genuinely fresh.)
3. Ollama up + models present:
   `curl http://127.0.0.1:11434/api/tags` -> HTTP 200, list must contain
   gemma:2b and gemma4:latest (15 models present this morning). If down: start
   the Ollama app, wait for green icon, re-curl.
4. GSTD moment pre-check: open https://platform.gstdtoken.com/api/v1/nodes in
   a browser tab NOW. Confirm the JSON lists gstd-desktop with
   gstd_earned ~0.90, tasks_completed 14, reputation 57. Leave the tab open.
5. Terminal prepared: one PowerShell window, font zoomed for the room
   (Ctrl+= a few times), cwd = the demo clone, pinned on top. Dark background
   recommended; the pack output is dense.
6. Quiet the disk: close browser tabs you do not need, pause big downloads.
   The estate's own automation keeps running (that is fine, it is the point).
7. Windows Update / restart dialogs: dismiss or postpone. Notifications off
   (Focus assist). Screen sleep off for 30 min.
8. AV: nothing needed on this box (Defender default showed no slowdown this
   morning). If a third-party AV is ever added and pip drags, add the venv
   folder to its exclusions; not needed tonight.
9. Have this folder open in Explorer: watch\inbox\walkthrough_20260109\ (the
   receipts are your abort material).

## LIVE SCRIPT (minute by minute, pre-staged clone)

### 00:00 - The stage (30 s)

Terminal shows the clone root. Say:
"This is the whole product: one repo, local-first. Local Ollama models do the
work, remote specialists are scarce and budgeted. No cloud account needed for
what you will see."

Optional beat: `git log -1 --oneline` (shows the automation commit cadence:
the repo files itself around the clock).

### 00:30 - The install (4-5 min, THE honest centerpiece)

Type, do not paste-blind, narrate as you go:

```
cd %TEMP%\mag_walkthrough_demo
powershell -ExecutionPolicy Bypass -File scripts\ensure_venv.ps1
```

Expected output flow (measured 4 min 34 s warm; say "about five minutes,
longer on a machine that has never downloaded these wheels"):
- `Creating .venv...`
- pip: `Installing collected packages: ...` (94 packages, incl langgraph,
  pandas, scikit-learn, faster-whisper, cryptography)
- `OK` <- the import gate (langgraph + httpx + reportlab)
- `Use: mag.cmd doctor   or   .\mag.ps1 doctor`

NARRATION SCRIPT for the dead air (the point of the wait):
- The requirements list is the architecture: langgraph (the agent loop),
  ollama bindings (local models), httpx (remote seats), reportlab (the PDF
  dossiers), faster-whisper (local voice), cryptography (the ed25519 seals).
- "Nothing here phones home to work. The venv is the seat. mag.cmd just points
  at it."
- If pip prints red stderr progress noise or a pip-upgrade notice: cosmetic,
  the exit line `OK` is the verdict.

### 05:00 - DEMO MOMENT 1: the seat boots (under 1 min)

```
mag.cmd doctor
```

Expected (0.9 s):
- `status=degraded live_stale=True` <- SAY THIS IS THE HONEST STATE: no lab
  process is running yet on a fresh install, and doctor refuses to pretend.
- `L0_ollama: ok=True` + the 15 local models listed
- `L1_openrouter: ok=False ... Set OPENROUTER_API_KEY` <- expected: .env is
  gitignored, a fresh clone has none. Remote lanes are opt-in with keys.
- `L2_grok: ok=True grok CLI on PATH`
- exit code 0.

Then:

```
mag.cmd context-pack
```

Expected (12 s): the full pack prints, ending with:
`BOOT-REGEN: ok (zknot=0.0d warm_boot=0.0d rib_boot=0.0d lawpack=1.639d) - all components regenerated and fresh`
Say: "It rebuilt its own memory organs from the repo's tracked state and
compressed the whole estate into one brief any AI can load cheaply. This pack
IS the product surface: FIND, FILE, LOAD."

Note in passing (do not dwell): the tail may say `census patrol dark` - the
scheduled patrol task is not registered on a fresh install; informational.

### 06:00 - DEMO MOMENT 2: the system thinks and files (under 1 min)

```
mag.cmd models
```

Expected (0.6 s): `"ok": true, "ollama_up": true`, 15 tags, roles table with
`"present": true` per role (biographer -> qwen-desk:latest, clerk -> gemma:2b,
...). Say: "It sees its fleet and knows who is present."

```
mag.cmd bonds
```

Expected (0.3 s): `"ok": true` + paths. Then prove the write:
`notepad memory\bonds_active.md` (or `type` it). 1,004 chars, freshly created
by the command they just watched. Say: "That is FILE: durable state on disk,
not chat vapor."

If time allows, `mag.cmd improve --status` (0.6 s, `"ok": true`) shows the
self-improvement surface honestly empty on day zero.

### 07:00 - DEMO MOMENT 3: the GSTD node, earning (browser)

Switch to the pre-opened tab: https://platform.gstdtoken.com/api/v1/nodes

Say: "This box is also a node on the GSTD network. Watch the first entry."
Point at:
- `"node_id": "gstd-desktop"` - this machine, LIVE on the network
- `"gstd_earned": 0.9014930...` - earned, on-chain visible
- `"tasks_completed": 14`, `"reputation_score": 57`
- `"capabilities": [...15 models...]` - the same fleet doctor just showed

The kicker line: "The same local models that booted the harness a minute ago
are the ones the network pays for. Local-first, and it earns."

Optionally refresh the tab to show last_seen ticking.

### 08:00 - Close (30 s)

What they saw: clone (pre-staged, receipt has its 35-minute truth), a 5-minute
one-command venv, a seat that boots and tells the truth about itself, a
context pack that briefs any AI cheaply, real durable writes, and a node
earning on the network. What they did NOT see: any cloud dependency.

If asked about the one-command installer: it is the 10/30 conf demo. Tonight
was the repo itself.

## PITFALLS TABLE (symptom -> one-line fix)

| Symptom | Fix |
|---|---|
| `Missing Mag venv. Run: powershell ...ensure_venv.ps1` | You skipped the venv step; run exactly that command |
| `No module named 'langgraph'` | You used bare `python` (PATH may resolve to another venv); use mag.cmd or .\.venv\Scripts\python.exe only |
| `...cannot be loaded because running scripts is disabled...` (Activate.ps1) | Use `powershell -ExecutionPolicy Bypass`; better: skip activation entirely, mag.cmd never needs it |
| doctor `status=degraded` | EXPECTED on a fresh install before any lab run; keep talking |
| doctor `L0_ollama: ok=False` | Ollama app not running; start it, re-run; if models missing: `ollama pull gemma:2b` and `ollama pull gemma4:latest` (multi-GB, do NOT do live) |
| doctor `L1_openrouter: ok=False` | No .env (gitignored, by design); remote lanes are opt-in, not needed tonight |
| doctor shows `port_8765: true` but heartbeat dead | The REAL Mag lab of the main install is live on localhost; cosmetic cross-talk, one sentence: "that port belongs to my main install" |
| context-pack tail: `census patrol dark` | Scheduled task not registered on fresh installs; informational, not an error |
| pip red stderr noise / NativeCommandError records | Cosmetic PowerShell wrapping; the `OK` line and exit 0 are the verdict |
| Clone sits at `Updating files: n%` for many minutes | 57,940-file checkout, 25-35 min measured here; it is working, do not kill it |
| `disk full` / clone fails | Need 35+ GB free; clear TEMP or use another drive for the clone |
| GSTD JSON does not load | Refresh; if still down, degrade per ABORT below |

## ABORT / DEGRADE PLAN (if it breaks live)

Ranked. Each fallback keeps the demo alive with something TRUE.

1. venv step stalls over 8 minutes: kill it, re-run the same script; it is
   idempotent and pip resumes from its cache. Worst case: run the rest of the
   demo against the MAIN install's own venv via mag.cmd from the source repo
   (doctor / models / context-pack are its own documented commands; they were
   green all morning).
2. Any mag.cmd command fails in the clone: switch cwd to
   C:\Users\foste\Documents\projects\local_sovereign_agent and run the same
   command there. Do NOT delete or rebuild the main install's .venv on stage.
3. Local machine totally unusable: drive the GSTD browser moment (independent
   of the repo), then show the receipts:
   - watch\inbox\walkthrough_20260109\INSTALL_TEST_RECEIPT.md (this morning's
     byte-backed fresh-clone proof: every step, every timing)
   - watch\inbox\NIGHT_SHIFT_20261004_CLOSE.md (the 4,358-test census receipt:
     the estate passing its own gates)
   - watch\inbox\GALA_20260925.md + watch\inbox\ENVELOPE_50W_HIT_20260926.md
     (the 50-wide concurrent workflow envelope: capability at scale)
   - corpus\steal\ZCODE_RATCHET_LANDED_20260924.md (the self-ratchet origin)
4. GSTD API down: the numbers are banked in INSTALL_TEST_RECEIPT.md section 6
   (gstd-desktop: 14 tasks, 0.9015 GSTD, rep 57, version 3.5.0); read them
   from the receipt and say "snapshot from this morning, on-chain verifiable".

HARD RULE under any failure: never claim a step worked that did not run. The
receipts exist so you never have to.

## LONG-FORM VARIANT (only if the slot is 45+ minutes)

Start the clone on stage at 00:00 (`git clone <path> %TEMP%\mag_walkthrough_live`),
and use its measured 26-35 minutes as the deep-narration slot: the compass
(docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md arc), the DNA (residual + registry +
leaf), the lanes table, and a scroll through AGENTS.md's census line (the repo
audits itself, 4,358 tests). Then continue with the venv arc above. The
audience seeing Updating files crawl for half an hour is only honest if you
tell them the number in advance.

## POST-DEMO CLEANUP

```
rmdir /s /q %TEMP%\mag_walkthrough_demo
```
Frees ~27 GB (26 GB tree + 0.74 GB venv, both measured). Say the number out
loud; it is the last honest stat of the night.
