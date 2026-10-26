# GSTD MCP SERVER LIVE - 2026-10-12 (babystep: the organs go on the wire)

**The instrument:** `tools/gstd_mcp.py` - stdlib JSON-RPC 2.0 line-delimited server, exact idiom of the estate's gps-mcp. Smoke-tested green end to end (initialize, tools/list, both tools/call).

**Tools (v0.2.0, read-only by law):**
- `lattice_read` - the VRAM hot lattice snapshot: per tailnet cell (DESKTOP/BOB/T90) hot models, VRAM MB, TON balance, on-chain reputation; SettlementMaster v6 stats (baseRate, taskCount, totalSettled); freshness = snapshot age (fresh < 1800s).
- `consensus_run_status` - the latest local consensus harness run: verdict, consensus vs noise rates, models, tasks. Tonight's read: consensus-20261011T235925Z, STRUCTURE, 0.8462 vs 0.3227.

**Architecture (the security posture IS the design):** the server performs ZERO network I/O. It serves two literal-path files written by trusted instruments - `lattice.json` (written by hot-lattice.ts, freshness = mtime) and the harness's own summary.json. Settlement is deliberately NOT exposed on the wire: settlement runs through the gated bridge (settle-consensus.ts, STRUCTURE-or-refuse), never via MCP. The wire reads; the bridge writes. Mimosa forced this shape twice tonight (SSRF findings on the first draft) and the forced shape is better: organs write files, servers serve files, money never moves over the tool wire.

**Why this matters (the cron question):** with the organs on the MCP wire, the old-days pattern - eight DeepSeek agents churning constantly - reconnects to the rail: workers (ds_workhorse, pennies) answer, the harness certifies, the gated bridge settles on v6, reputation accrues on-chain. The swarm pays for itself through the 85/10/5. Cron shape per the operator's own law: boot-trigger + the standing drain (nightcrew pattern), never timed windows.

**Next rungs:** gstd drain lane in the nightcrew pattern (INBOX rows -> workers -> consensus gate -> settle); settle tool behind GSTD_MCP_ALLOW_SETTLE for trusted clients; bob/t90 ignition flips cells COLD->HOT in the same snapshot.
