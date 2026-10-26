# STEAL — Hermes plugin for the Mag stack (2026-10-20)
Context: Godot/game distribution is back-burnered. P3 distribution now means a Hermes plugin that someone else can install.
Constraints held: no git writes; no secret files opened; no paid calls; no container restarts; frozen lab not touched; MAG_ALLOW_LIVE_WRITES unset; nothing was installed or enabled in the live HERMES_HOME.
Evidence tiers: **[V]** verified on disk or by running it today · **[D]** doc or source claim (URL or file cited) · **[R]** recommendation · **[X]** design (written, not yet proven in the field).

## 1. Self-steal: Hermes organs in the estate [V]
- **Hermes Agent v0.22.0.** HERMES_HOME is %LOCALAPPDATA%\hermes and the CLI is bin\hermes.exe. The gateway runs as `hermes_cli.main gateway run`.
- **Plugins in HERMES_HOME\plugins:**
  - hermes-ledgerline, hermes-resetwatch and hermes-tailscale (third-party, author Adolanium). They are desktop-only and register no tools.
  - holographic, memory-wiki, tool-slimmer and chrome-profiles.
- **48 skills installed.** config.yaml mcp_servers holds wolfram (disabled) and notion (oauth).
- **Burn lane:**
  - Code: tools\hermes_burn.py; scripts\hermes_burn_247.ps1, register_hermes_burn_task.ps1 and setup_hermes_ollama.ps1.
  - MagHermesBurn247: its last real run on 10-19 FAILED with `NIGHT_ROTATION_20261019: KeyError('contract')`. Ledger total is $94.74. Still open; tracked on the board.
- **mag\mcp_server.py** serves TOOL_MAP over stdio in profiles. The warm profile has estate_warm_read, chain_verify, shared_receipt, propose/review/proposals, fleet_report/notices, leases and lease_*, dirac_*, thought_compile, water_graph_tick, driver_status and estate_bridge.
- **The listener on 127.0.0.1:8766 (tested today through the shim)** is server `mag-tool-map` 1.0.0. Its tools are list_dir, read_file, search_files, blackboard_read, pheromone_trail, scan_measure/probe/grid, mean_field, whisper_decode, corpus_search/get/tail/stats and research_search/sources/stats.
  - These are **not** the warm estate_* tools. The live door is the read/corpus profile.
- **scripts\mcp_stdio_shim.py** is a stdlib pipe from stdio to TCP, loopback only. It imports mag.seat_handshake only when `--sign` is used (lazy import, line 76).
- **Other meaning of "Hermes plugin" in the estate:** git log 10-15 shows commit 189a8239f, "Teknium Hermes plugin + REA MCP". That one is a different artifact and is not this package.
- **Distribution blockers:**
  - These core organs are UNTRACKED: mag/leases.py, fleet_report.py, seat_handshake.py, proposals.py, ratchet.py, warm_surface.py and bintree_v2.py, plus scripts/mcp_stdio_shim.py and lease.py.
  - There are 281 modified tracked files and a push hold.
  - This matches the honest read's ghost addendum.

## 2. Plugin format, current Hermes [D] (cross-checked against installed source [V])
Sources:
- https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- https://hermes-agent.nousresearch.com/docs/integrations/

Hermes has three ways to extend it:

**A. Native Python plugin**
- Layout: `plugin.yaml` plus `__init__.py` with `register(ctx)`.
- Install location: ~/.hermes/plugins/<name>/, or a pip entry point under `hermes_agent.plugins`.
- Plugins are opt-in: `hermes plugins enable <name>`.
- Manifest fields: name, version, description, author, provides_tools, provides_hooks, requires_env, capabilities. Version 2 adds manifest_version, api_version, requires_plugins, python_dependencies, python_runtime, config_schema, license, homepage, tags, requires_auth and oauth.
- API:
  - `ctx.register_tool(name, toolset, schema, handler)`. A handler takes `(args, **kw)`, returns a JSON string and never raises.
  - `ctx.register_skill` registers skills.
  - Hooks are also available.
  - `ctx.get_config` reads from `plugins.entries.<name>.settings`.
- Checks: `hermes plugins validate` and `hermes plugins doctor --ci` (temporary HERMES_HOME, sockets blocked).

**B. Portable Agent Plugins v1**
- Layout: `plugin.json` plus `skills/*/SKILL.md` plus `mcp.json`.
- Install: `hermes plugins install owner/repo --no-enable`.
- The installed source (hermes_cli\agent_plugins.py) enforces these rules [V]:
  - plugin.json `$schema` must equal https://agent-plugins.org/schemas/1.0.0/plugin.schema.json.
  - mcp.json must contain exactly `{$schema: .../mcp.schema.json, mcpServers}`.
  - Each stdio server needs `type: "stdio"`.
  - `command` must be a bare executable or start with `./`.
  - Placeholders expand ONLY for `${PLUGIN_ROOT}` and `${PLUGIN_DATA}`. `${MAG_ROOT}` is NOT expanded.
  - The Hermes extension `servers.<n>` accepts `trust`. It REJECTS `timeout`, even though my earlier doc reading suggested it was allowed.

**C. Plain MCP + skills**
- MCP servers go under config.yaml `mcp_servers`.
- Skills go in ~/.hermes/skills and follow the agentskills.io standard.

## 3. What is portable and what is estate-only [R]
| Capability | A stranger with zero secrets? |
|---|---|
| Hash-chain internal consistency verify (verkle_knot) | yes, against any Mag checkout |
| fleet_report.v1 schema validate | yes |
| Notices list and lease board read | yes (local files) |
| Tri-state/receipt discipline skill and self_steal genome skill | yes (pure text) |
| mag-mcp door on 8766, seat handshake (--sign keys) | estate only |
| Burn lanes, funded keys, GSTD, Telegram/Discord gateway | estate only, never ship |
| The chain contents themselves | estate data, not code |

## 4. v0 as built — watch\inbox\hermes_plugin_v0\ [X, tested locally — see §5]
- **`mag-estate\`** (native plugin, read-only):
  - Files: plugin.yaml (manifest v2, `python_runtime: external`, `requires_env: []`, config `mag_root` with fallback to env MAG_ROOT), schemas.py, tools.py, __init__.py, and README.md.
  - Tools:
    - `mag_chain_verify`: reports tier verified-internal-consistency, with the caveat that no external witness was consulted.
    - `mag_receipt_validate`
    - `mag_notices`
    - `mag_leases`
  - Each tool is a thin wrapper over an existing organ: verkle_knot, fleet_report and leases. No new engine, no writes.
  - Skills: mag-tri-state-receipts and mag-self-steal (the latter is docs\ref\verb_genomes\self_steal.md plus frontmatter).
- **`mag-estate-portable\`** (Agent Plugins v1, "mag-estate-door", estate machines only):
  - plugin.json with server trust set to `untrusted`.
  - mcp.json runs `python ${PLUGIN_ROOT}/bin/mcp_stdio_shim.py --port 8766 --timeout 5`.
  - The shim is vendored as a byte copy of scripts\mcp_stdio_shim.py, because ${MAG_ROOT} does not expand.
  - Same two skills.
- **What v0 does NOT do:** writes (propose, receipt_append, lease acquire), the seat handshake, or any burn or paid lane.

## 5. Tests run 2026-10-20 (local, no network, no paid calls) [V]
1. **Fake-ctx harness (.venv python, MAG_ROOT = repo):**
   - The unconfigured case returns `not_configured`.
   - register() gives 4 tools and 2 skills.
   - mag_chain_verify returns ok, "chain consistent (13138 leaves)".
   - mag_notices returns the 2 in-force notices, each with 0 acks.
   - mag_leases returns held 0.
   - mag_receipt_validate returns ok on a valid SITREP and lists 6 missing-field errors on a bad NOTICE.
2. **`hermes plugins validate mag-estate`:** PASSED on every check (manifest, config schema, register-in-isolation, declared tools match, no collisions, security scan safe).
3. **`hermes plugins doctor mag-estate --ci`:** OK. 4 tools, 0 hooks, rc=0.
4. **`hermes plugins validate mag-estate-portable`:**
   - The first two runs FAILED: `$schema` was missing, then `timeout` was rejected.
   - After the fix it PASSED: trust untrusted, security scan safe.
5. **Vendored shim to 127.0.0.1:8766 (initialize + tools/list):** OK. It lists the 17 read/corpus tools from §1.

## 6. Findings and risks [R]
- **The door exposes `read_file`/`search_files` over the repo.** Even with trust untrusted, an agent could be pointed at secret paths.
  - Not verified today: whether mag-tool-map denies .env or keys. I deliberately did not probe it.
  - Gate any publication of the door on a deny-list check.
- **A stranger cannot use mag-estate until the untracked organs are committed and pushed.** The wrappers import leases.py and fleet_report.py.
- **HermesBurn247 is still red** with KeyError('contract'). This is separate from the plugin, but it is the only Hermes lane that runs right now.

## 7. Needs Nacho
1. Commit and push the untracked organs (COMMIT_PLAN batches). This is the hard blocker for any stranger.
2. Choose a license, and decide whether to publish (own repo `owner/mag-estate` for `hermes plugins install`, and/or a catalog entry).
3. Approve installing and enabling mag-estate in your own HERMES_HOME (copy the folder, `hermes plugins enable mag-estate`, set mag_root). Not done yet.
4. Decide whether 8766 should serve the warm estate_* profile instead of tool-map, and audit read_file's deny-list before the door ships.
5. P6: one external person installs it and runs mag_chain_verify plus mag_receipt_validate. Until that happens, "met a stranger" stays Unproven.
