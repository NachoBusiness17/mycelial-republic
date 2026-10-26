# FREE FLEET CELL DRIVE - 2026-10-19

**Classification:** RECEIPT (lane L4-cell-drive)
**Producer:** zcode seat, desktop bench (Windows host, Mag repo)
**Moment:** 2026-10-19T04:37Z (live probes 04:36Z)
**Instruments:** `mesh_router.py map` (repo root), TCP connect probes, byte reads of the cited files. Every claim below names its source; nothing hand-copied.

## 1. What the cells ARE (byte-grounded)

`mesh_router.py` (repo ROOT, not mag/ - there is no mag/mesh_router.py) declares the four BODIES:

| body | hosts | tier | os_kind | role (source) |
|---|---|---|---|---|
| bob | local, ssh `etfag@100.125.103.60:22` | primary | windows | operator's PRIMARY seat by design: full clone of the standing wave + `memory/rib/RIB_BOB_PRIMARY_20261017.md`; runs pocket_mcp + gstd node (device_map 2026-10-19: `gstd_node_running: true`) |
| desktop | ssh `foste@100.96.161.76:22` | bench | windows | heavy model inference + container cage (`.agents/skills/gstd-network/SKILL.md` table); hosts ollama at :11434 for the five-model run line (`corpus/steal/MASTER_GSTD_RUNGS_20261011.md` rung 0) |
| t90 | ssh `u0_a235@100.72.38.3:8022` | medium | termux | Android arm64 edge node: low-power continuous beacon, ~1.9 GB free RAM / ~63 GB storage (gstd-network SKILL table) |
| pixel-11-pro | ssh `u0_a354@192.168.86.32:8022` or `100.79.122.101:8022` | outstanding | termux | second Termux phone cell (BODIES entry; RUNNERS one-pagers name "pixel Termux") |

The GSTD economy framing (mission said DESKTOP rep 15 / BOB rep 5 / T90 rep 1): those exact numbers are NOT byte-found in the repo tonight. The freshest on-repo receipts read lower: `watch/inbox/gstd_perimeter_build_20261010/MULTI_NODE_LIVE.md` (desktop rep 6, bob rep 2-3, T90 rep 0 staged); `watch/inbox/GSTD_MAP_20261016.md` confirms "three cells proven on-chain (desktop/bob/t90)" and MagGstdDrainDaily running as an autonomous A2A worker since 10-13. The 15/5/1 figures are plausibly a fresher drain read; they are declared-only from this seat until a drain log byte backs them.

## 2. How the estate DRIVES the cells (mechanisms found)

1. **mesh_router.py** (body axis): `map` (fresh device_map per body via one-shot JSON-RPC `tools/call` over ssh to pocket_mcp.js), `route` (gate-checked pick: reachable, battery > 30 pct or charging, ram_free, lowest loadavg wins; presence-sealed tools location/camera/sms never route), `fire --shape gstd_beacon|gstd_tasks`, `have` (invariant swarm bitfield, drift detection via sha256, writes `invariant_swarm_manifest.json`), burn rows appended to `BURN_LOG.jsonl`.
2. **GSTD A2A drain**: MagGstdDrainDaily 08:00 (RIB_BOB_PRIMARY lane map) polls app.gstdtoken.com pending tasks, routes via pick_body, banks DONE receipts to queue/gstd_tasks/DONE, master log logs/gstd_drain_daily.log.
3. **Handoff by clone, not by wire**: bob receives work by cloning the standing wave (github.com/NachoBusiness17/mycelial-republic branch standing-wave) + copying `watch/inbox/bob_handoff/` (RIB + README) into memory/rib/ - `watch/inbox/BOB_HANDOFF_PACKAGE_20261017.md`.
4. **Chan rows**: typed {from_lane, to_lane, msg, ref} appended to `watch/room.jsonl` per `.agents/skills/mesh-comms/SKILL.md` (four channels: chan, rib_bus, panels, wants). WANTS intake exists at `watch/WANTS.md` (self-tending cron reads it first when the union queue runs low).

## 3. REACHABLE tonight vs DECLARED-ONLY (the honest split)

Live `mesh_router.py map` run 2026-10-19T04:36:27Z (fresh `device_map.json` written at repo root):

- **bob UP** - pocket_mcp answered in 0.92 s via 100.125.103.60: Windows_NT 10.0.26200, node v22.20.0, RAM 3,523 MB total / 321 MB free, storage 13.9 GB free, 85 invariants, gstd_node_running true, `models: []` (no local models on bob; inference leans on desktop ollama). Gates PASS. The 10-17 rib listed bob's ssh trust as OWED - it now works (BatchMode auth succeeded with no password).
- **desktop DOWN** at the MCP layer - TCP 22 OPEN (probe), but the pocket_mcp remote_cmd answered no MCP reply; captured err is the ssh post-quantum banner. Note: BODIES.desktop points the key at `C:\Users\etfag\Documents\adam_laptop_key`, which does not exist on this foste-seat clone (the key lives at `~/.ssh/adam_laptop_key` here) - path drift between clones.
- **t90 DOWN** - TCP 8022 OPEN (Termux sshd listening), ssh answered `Permission denied (publickey,password,keyboard-interactive)`: `t90_lane_key` is ABSENT from this repo root though BODIES.t90 expects it at HERE/t90_lane_key. Port alive, auth dead.
- **pixel-11-pro DOWN** - both hosts refused connection (100.79.122.101:8022 refused, 192.168.86.32:8022 refused) and `~/.ssh/pixel_lane` is absent here. Device asleep/offline + key missing in this clone.

Also measured: `device_map.json` and `BURN_LOG.jsonl` did NOT exist at repo root before tonight's run - no prior cached fleet map in this working tree, so the map command had not been exercised here recently. Chan surface LIVE (monitor.lane rows landing today in `watch/room.jsonl`); rib_boot doctrine live (`memory/rib_boot.json` regen path); wants intake live.

**Verdict:** from this seat tonight the cell-drive is bob-live, everything else key/path-broken or asleep. The mesh brain (mesh_router) is fully operational code with a live primary body; the mobile legs are DECLARED but not DRIVEN until keys are restored and the phones wake.

## 4. COMMISSIONED (actions taken this window)

1. **Chan rows appended** to `watch/room.jsonl` at 2026-10-19T04:37:42Z, kind `chan.commission`, from_lane `L4-cell-drive`:
   - to_lane `bob`: run the free-fleet census on its own cell (env keys: OpenRouter free-tier quota, Antigravity sf/nacho accounts; GPU truth via nvidia-smi - the bob-GPU door for athena-class probing; bank receipt + one chan row back). Bob's live device_map already shows models=[] so the GPU door is exactly the unknown worth a census.
   - to_lane `t90`: same census at edge scale (Termux env, battery/ram gates, small-model capacity vs the desktop five-model run line, GSTD rep state), with the honest note that ssh auth failed tonight and the census executes when t90_lane_key is restored or via Termux-side self-report.
   - to_lane `pixel-11-pro`: same census on wake, with tonight's connection-refused bytes cited.
2. **Wants filed** in `watch/WANTS.md` (2026-10-19 section): restore `t90_lane_key` + `pixel_lane` keys (done = mesh_router map reads 4/4 UP), execute t90/pixel censuses at their scale, re-light desktop pocket_mcp or correct the BODIES.desktop key path.
3. **Fleet map banked**: `device_map.json` (repo root) now carries the 2026-10-19T04:36Z snapshot as the fresh baseline.

## 5. Falsifier

If a later window runs `python mesh_router.py map` and reads 4/4 UP, this receipt's DOWN rows are superseded (refresh, do not mourn). If bob never answers the chan commission with a census receipt on `watch/inbox/`, the chan-as-control-plane claim is weakened: chan rows reach only seats that read room.jsonl, and bob's clone must be confirmed to sync `watch/` before the chan is trusted as bob's inbox (tonight's evidence: bob answers MCP, not chan).

## NEXT TASK (self-designed)

Bob-side chan reader: a small cron on bob (its clone) that tails `watch/room.jsonl` for rows with to_lane in {bob, t90, pixel-11-pro} and turns `chan.commission` rows into queue items, answering in line - this closes the falsifier above (bob currently answers pocket_mcp but has no proven watch/ sync) and makes the chan a real control plane for the fleet instead of a desktop-side journal. Spec: read the last N rows by byte offset, dedupe by ts+msg, write commissions to queue/todo on the bob clone, one receipt row back per commission.
