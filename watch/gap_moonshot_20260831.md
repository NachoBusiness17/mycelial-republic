# Gap Analysis + Moonshot Map — 2026-08-31 (04:36Z window)

Sources (bounded): workspace TOOLS.md (intent), MEMORY.md (doctrine), memory/2026-08-31.md tail, /board/WARM_PACK.json.
Evidence shorthand: **TD** = TOOLS.md row (operator-authored) · **D** = memory/2026-08-31.md at Z-timestamp · **MEM** = MEMORY.md section · **WP** = WARM_PACK.json spine id.
Status: `live` = receipt corroborated this window · `live*` = operator-attested in TD, not exercised this window (attestation is evidence; not re-verified per 04:36Z law) · `partial` / `missing`.

## 1) INTENDED vs BUILT — per TOOLS.md surface row

| Surface | Status | Evidence |
|---|---|---|
| Control UI :18789 | live | TD; this subagent spawned from it (dashboard webchat requester) |
| Mag dashboard :8765 | live | D 03:24Z "Dashboard :8765 reachable… huge api/v1 route table incl. fleet/hypervisor" |
| AutoClaw ×2 | live* | TD (English 08-29); no contrary log |
| Grok TUI ×2 (nacho, sd) | live* | TD; no contrary log |
| Codex (mailbox/exec) | live* | TD; no contrary log |
| zcode | live (gated) | TD + D 04:19Z: key funded (1310) but hands-off until 09-02 12:52Z |
| Room log watch/room.jsonl | live | TD; D 03:24Z GET /room 200; same mount in both workspaces (D 00:07Z) |
| seat_dispatch | live | TD; D 03:12Z names it the host-venv routing path |
| fuel_feed | live* | TD "74+ signals"; no contrary log |
| frontier_salon roundtable | live (host-only) | TD "LOAD first"; D 03:12Z socket-bind errors = cage misuse, not dead surface |
| party_subchain | live | TD; WP verkle doctrine; knot tie degraded until rebuild (Gap 3) |
| salon_openclaw round | live (host-only) | D: 08-31 riddler salon ran via OpenClaw lanes A/B/C → CROSS-LINEAGE synthesis 00:38Z |
| salon_openclaw chan | live (host-only) | TD; posts to /board/room.jsonl |
| /patches → openclaw_patches apply | live | D 00:51Z: PROPOSED gate HELD (0 self-applied all window); 10 patches pending (Gap 1) |
| 4chan board /board/room.jsonl | live | D 03:24Z POST /room 200; bootstrap noise present (Gap 6) |
| board_tailer | live | TD: durable cursor, observes directives, --dispatch opt-in |
| read_archive | live | MEM: deref bound check 12/12 PASS |
| atlas / basecamp / elder | live | D 00:51Z: Atlas posted as first fully classified receipt (class=receipt) |
| fireball_cycle | live | TD; D dogfood ledger 10 rows |
| /board/openclaw_traj.jsonl | live | WP traj.openclaw_tape bound hash; TD bounds law (legacy unbounded) |
| seat_corpus latest.json | live | WP organ.seat_corpus; D prefer_order cited (z_ai above deepseek) |
| Governor (mag-sovereign+worker) | **partial** | supervisor verified (D 03:24Z /health /seats /queue) but authority boundary not mandatory — MEM Switchboard: "Host patch needed" |
| Fork (subagents + fork_of) | live | TD; this session + salon lanes A/B/C are Control UI subagents |
| Workboard | live* | TD; no activity this window |
| openclaw_catalog latest.json | live | TD "LOAD this"; D 03:12Z law cites it |
| fabric.json | live* | TD; never deref'd this window |
| ghost_memlance | live* | TD; no contrary log |
| verkle_lance | **partial** | D 00:51Z: knots dir missing (Aug 26 wound); rebuild on finish list |
| ghost_pylance | live* | TD; no contrary log |
| grok_steer | live* | TD; no activity this window |
| D&D (game_campaign) | live* | TD; no activity this window |
| agent_arena chess | live* | TD; no activity this window |
| Mermaid / surface_render | live | D 03:24Z fleet/hypervisor route reachable |
| Render suite | live* | TD; no activity this window |
| lab_episode | live* | TD; Grey Swan study lane open |
| PRIMER.md | live | TD; feeds riddler surrogate pattern |
| primer_booth_public.json | live | MEM: riddler v0 PASS 7/7 conf 0.95; WP riddle.memory_v0 |
| skills/ | live | fireball-cycle + operator-corrections mounted (/mag/.agents/skills) |
| water_computer | live* | TD; "water one", season-gated by design |

**Counts: 37 live (14 corroborated, 23 attested-only) · 2 partial · 0 missing.**
Caveat: 2 doctrine organs are absent from the table itself — `ask_router` and `session_bridge` (see Gaps 2 & 4). Intent outran the table.

## 2) GAPS — top 7 by leverage

1. **Authority boundary is paper, not law.** 10 patches staged (switchboard_v2/harness/effect_broker/policy_engine ~2562 lines) await host apply; `swarm_tools.py:blackboard_post()` still writes straight to disk. *Nearby:* /patches gate proven holding; cage modules staged. *Bridge:* one operator apply session + harness test. *Owner:* operator (host); cage already done.
2. **ask_router: doctrine without a surface.** "Missing-everywhere primitive" ($0 outcome-memory routing, ledger.jsonl + verkle ties) has no TOOLS.md row and no first-light drop recorded. *Nearby:* seat_corpus prefer_order, seat_dispatch, fuel_feed. *Bridge:* host first light (`--dry` → live route + record drops), then add the row. *Owner:* host venv (operator or seat_dispatch).
3. **Verkle knots wound (Aug 26).** self_check can't fully pass; party_subchain "parent = verkle tip" degrades to unverified. *Nearby:* warm-pack shape_hash, traj tape hashes, deref 12/12. *Bridge:* rebuild knots from the existing hash chain. *Owner:* host venv.
4. **session_bridge not generalized.** The one-window cross-session bus exists once (riddler_common + memory_riddler_sync.mjs mirror) but isn't reusable for arbitrary named columns. *Nearby:* riddler_common.jsonl charter, tailer directives. *Bridge:* parameterize the sync script (column → memory file), add surface row. *Owner:* cage (script) + operator (row).
5. **Rightsizing/pack button.** Operator asked 08-31; answer was "never built," manual discipline only; skill offer still awaiting yes/no. *Nearby:* PACK_*.md discipline, memory_rib_write.mjs. *Bridge:* tiny workspace skill (paste→file→pack). *Owner:* cage; operator decides.
6. **Board signal dilution.** agent:bootstrap noise on /board/room.jsonl; post self-classification only partial (old posts ad-hoc, new column labeled). *Nearby:* atlas class=receipt pattern, authority-label doctrine. *Bridge:* backfill labels + route noise to an archive thread (append-only; nothing deleted). *Owner:* cage via POST /room.
7. **Sancho tier-lattice row.** Session-model tier config never patched (config patch proposal pending). *Nearby:* seat_corpus prefer_order, conservation dates. *Bridge:* one config patch via /patches. *Owner:* cage (proposal) + operator (apply).

## 3) MOONSHOT — the 10x move (existing organs only)

**Close the loop: apply → govern → route → receipt.**
Operator runs one `openclaw_patches apply` → switchboard becomes the mandatory authority boundary for every board write.
Then ask_router first light through that same gate: every spawn gets $0 outcome-memory routing, every effect a verkle-tied receipt (knots rebuilt first).
Every receipt lands in the same event stream the RIB/WARM_PACK already warm from — trust, routing, and memory compound from one audited bus.
The 39 surfaces stop being a menu and become one governed organ with $0 control plane.
No new SPA, no second gateway, no invented cages: 10 staged patches + 1 knot rebuild + 1 first-light run.
