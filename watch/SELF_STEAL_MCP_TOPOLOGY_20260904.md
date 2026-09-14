# SELF-STEAL — the MCP thing: intended vs exists (2026-09-04 night)

**ITEM:** Operator: "self steal the whole mcp thing and what we were trying to do vs
how it now exists." Context: he watched headless windows spawn on his desktop after
the evening cage fix and ordered "everything should be in containers... debug now."
This card is the autopsy of the whole MCP arc — the doctrine we wrote vs the battery
that was actually running — and the fix receipt.

## WHAT WE WERE TRYING TO DO (the record, oldest first)

- **08-26, public turn:** "MCP senses" — the fleet's sensory organs. Doctrine =
  marketing, infrastructure = sovereign: MCP stays loopback + Access.
- **08-27, :8765/mcp door verified:** `mag/mcp_server.py` = "transport, not
  authority" over `tools.TOOL_MAP` (single source). Blackboard schemas receipted.
- **08-28, drive show:** grok landed sense_gps / voice_turn / whisper_decode as MCP
  tools on the catalog — senses as ADOPTABLE organs, not a fixed install.
- **09-04, SOCRATIC_MCP_BRIEF:** the fleet IS MCP-native (9 live servers); the lack
  was never adoption — it is DELIBERATE sense selection. Missing organ named: the
  adoption process (server → security pass → SKILL.md pairing → room receipt →
  liveness falsifier).
- **09-04, senses aisle:** 3,838 servers triple-census; triage = local-first,
  loopback-safe, permissive license; THE SOVEREIGNTY LINE: chain, room, blackboard,
  Mimosa, computer-use NEVER outsourced to third-party servers.
- **09-04, dogfood salon:** anti-sprawl rule — One-Request-One-Receipt, Three-Gate
  (manifest check → real-task proof inside TTL → kill-switch test). "Senses EXPIRE;
  nothing whitelists forever."

## HOW IT ACTUALLY EXISTS (tonight's census — Supported, process map attached in session)

- **The DEFAULT senses bypassed the adoption organ entirely.** The workspace config
  (`projects/.zcode/config.json`) spawned `mag.mcp_server` HOST-SIDE, per session —
  three copies — as console windows. The fleet's own organ, running on the desktop,
  the same night the doctrine said in-Docker, loopback, transport-not-authority.
- **Per-session battery, every boot:** 3× cloudbase (cmd→node→cmd→node double
  chain), 3× lumen (its index has been failing — 0 files — while spawning 3
  daemons), 3× example-plugin (a hello-world demo), 3× mimosa, 3× mag (+3
  sub-pythons) ≈ **28 console children per session boot**, every one through a
  `cmd.exe` shim that allocates a console window.
- **The hooks:** `steer_47.py` ran on EVERY Bash call and every session Stop —
  marker-gated in effect, but the gate CHECK itself spawned a python console each
  time. The continuous flashing during work was the safety check checking nothing
  (marker absent). prebuild_gate (Write|Edit) is real law and stays.
- **The one part that matched the doctrine:** the remote z.ai MCPs (web-search /
  web-reader / zread, `"type": "remote"`) — zero local processes. Proof the
  intended shape works and was already in hand.
- **Meanwhile the cage already served the organ:** :8000 `/run_task`, :8765
  dashboard, FastAPI :8001 bridging the route registry — but no MCP-framed
  endpoint, so the seat couldn't be a client and kept spawning its own copy.

**THE GAP, one line:** we wrote an adoption doctrine for NEW senses and never
audited the DEFAULT ones. The default battery was the sacred cow — the host-session
runtime wearing a senses costume. Second recording of the same root failure this
week (laws on record, not consulted at design): `docker-not-desktop` (08-25) and
`headless-only` (08-26) covered this exact shape.

## THE FIX (all receipted tonight)

1. **`mag/mcp_http.py` (new):** `POST /mcp` on the api gateway (:8001) — MCP
   streamable-HTTP framing over the SAME `mcp_server.handle()` / TOOL_MAP. Parity
   by construction; auth inherited (X-API-Key gate, loopback bind). Probe receipts:
   initialize 200 (`mag-tool-map 1.0.0`, protocol 2025-06-18), tools/list = 20,
   tools/call blackboard_read → ok:true, notification → 202.
2. **Workspace config repointed:** mag stdio spawn → `"type": "remote",
   "url": "http://127.0.0.1:8001/mcp"`. Host spawns ZERO fleet pythons per
   session; N sessions, ONE organ in the cage.
3. **Plugin diet:** example-plugin, lumen, cloudbase-skills → false. mimosa + the
   working plugins stay.
4. **steer_47 hooks OUT** (marker absent); re-arm recipe written into the config
   note. prebuild_gate stays.
5. **Lane daemon re-armed** (pid 2082, 00:12:21Z) — the 23:33:46Z engine-level
   container recreate had killed it (O4 known mode; RestartCount=0 → not a crash
   loop; same-minute app+engine bounce, likely one Docker Desktop restart).
6. **Backups:** both configs → `*.bak-mcpcage-20260904`.

## LAWS MINTED (amendments to the adoption organ)

- **NO DEFAULT SENSES:** every MCP server in any config holds a manifest card
  (lane, justification, adoption test, TTL) or it culls at the next census. The
  dogfood Three-Gate now applies to the EXISTING battery, not just new requests.
- **SENSES LIVE IN THE CAGE:** fleet senses serve from mag-sovereign loopback;
  host seats are clients. Per-session stdio spawns of fleet organs = the window
  swarm shape — banned by `docker-not-desktop` + `headless-only`.
- **ONE SENSE ONE INSTANCE:** 3× copies of every server was split-brain senses.
  A remote endpoint serves N clients from one organ; stdio multiplies by session.

## TRUTH (tri-state)

- Defect (window swarm = default MCP battery + hooks): **Supported** (parent/child
  process census + config files + hook config).
- Fix (cage endpoint serves the organ): **Supported** (probe receipts above).
- "The desktop stays quiet": **Unproven** until the next session boot (expected
  battery: node_repl + mimosa + prebuild_gate only) and the operator confirms.
  The 2 legacy mag copies die with their pre-fix sessions; they do not respawn.
- Container restart cause 23:33:46Z: **Unproven** (engine-level event; watchdog
  log stale since 08-26 — the watchdog organ needs its own re-arm pass).

## GAPS / orphans

- `.vscode/mcp.json` (cloudflare entries) is dead config — ZCode doesn't read VS
  Code's MCP file. Left in place; noted so nobody counts it as live.
- zai-vision / zai-vision-sd (npx stdio) = 2 remaining per-boot shims. Kept
  deliberately: they are the vision-eye doors.
- Host-side process census is seat-run; the monitoring/observability MCP pick from
  the dogfood salon would make it proprioceptive. That pick just got more urgent —
  tonight proved the host layer drifts the moment nobody watches it.
- Mimosa note: the new endpoint is stdlib and additive; if the scanner wants a
  look at mcp_http.py, it is one file, no new egress (bind is the gateway's).

*— Sancho (flash-drive seat), 2026-09-05 ~00:2xZ. Trail: queue/lanes/day_work/trail.jsonl.*


## AMENDMENT (00:2x-00:3xZ, same night) — the doubled log & the fourth launcher

Operator: "why is everything repeating itself three times / you are fixing with
prose. no monkeypatches." He was right, twice over. The log rows were DOUBLED
(not tripled): `_log()` writes `lane_scheduler.log` itself AND the recorded
re-arm one-liner redirected stdout into the same file — one pid, two writers.
The hand-launched daemon I ran from this card WAS the bug. Fourth occurrence of
the class (twin supervisors 08-26, racing double-daemon 09-04, 3x MCP copies,
doubled log), each with a DIFFERENT launcher — prose-recorded launch paths are
the launcher-of-last-resort and always weird. STRUCTURAL FIX, all receipted:

1. `mag/lane_runner.py daemon()`: SINGLE-WRITER GUARD — refuses to start if
   stdout is redirected into its own log (dev/ino match). The illegal launch
   now fails loudly instead of running double-mouthed (Lessig: unrepresentable).
2. `mag_launch.py` roster: `lane_scheduler` slot added — the daemon has an OWNER.
   Container recreates respawn it; no human one-liner exists (LAW 11 applied to
   my own organ — it had been living outside the one supervisor).
3. PROVEN: `docker restart mag-sovereign` -> mag_launch spawned it (pid 13,
   ONE UP row); killed 13 -> respawned as 139 in <40s (single row); /mcp still
   200/20 tools through the recreate. O4 is DEAD AS A CLASS.
