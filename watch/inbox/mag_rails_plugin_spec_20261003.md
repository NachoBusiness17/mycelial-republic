# MAG-RAILS: the ZCode plugin spec (seeded 2026-10-03, operator idea)

Operator: "i was thinking about making a plugin for you anyway." This is the
spec of what the plugin exposes, so the seat stops bash+pythoning into the
estate and calls it natively. Build target: ZCode plugin (MCP tools or plugin
skills) wrapping the standing rails (queue/STANDING_RAILS.md).

## THE TOOLS

1. **mag_route_chat**(prompt | messages, goal, lane?, model?, max_tokens?)
   -> text. Wraps mag.route_chat: the one door (dormant gates, key failover,
   fences, per-lane laws, usage banked). The default model-call tool.
2. **mag_stage_ask**(id, contract, evidence_paths, model?)
   -> stages an ask dir under memory/plans/hermes_burn_*/ ; the descent
   driver eats it automatically. Returns the queue position.
3. **mag_arena_status**() -> one line: last session verdicts, gwap ledger
   seq, today's spend vs cap, next cron fire.
4. **mag_delta_register**(ask_id?) -> the register rows (three-arm scores,
   win rates, the frontier-only class). The routing table, queryable.
5. **mag_gwap_bank**(run_dir) -> banks a session as chain-verified payloads
   + feeds the GPS router (wraps tools/arena_gwap.py).
6. **mag_sacred_cow**(law_text, probe_spec) -> registers a sacred-cow probe:
   the law, the falsifier, the arm design. Because cows get examined, not
   worshipped (the thinking-off probe was the first).

## THE SKILLS (slash-commands over the same rails)

- /rails - print the drop-in table
- /arena - status + last brawl excerpt
- /delta <ask> - the register row
- /cow <law> - open a sacred-cow probe

## WHY THIS SHAPE

The rails already exist (route_chat, hermes_burn, ds_workhorse, arena_gwap,
the crons). The plugin is only the NATIVE HANDLE: the seat stops writing
bash+python per sitting, the usage banks uniformly, and the drop-in table
becomes tool calls the harness permission system can see. Lessig for the
seat itself: make the right path the callable path.

## BUILD NOTES

- MCP server over stdio (tools/gps_mcp/ is the in-repo pattern: config.json
  + ledger.db3 next to the file; the plugin server holds no state).
- Every tool wraps an existing function - no new model-call logic in the
  plugin layer (route_chat owns the door; the plugin is a handle).
- The plugin never holds keys; route_chat reads .env/lane config as today.
