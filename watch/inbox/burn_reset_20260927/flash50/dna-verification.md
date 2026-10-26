# DNA.md verification census (f-23)

Item f-23, census gopher fire-f-23, 2026-09-28. Scope: read `docs/DNA.md` fully (147 lines, 5,798 bytes; `wc -l` / `wc -c`), verify every factual claim against the current tree. Every check below was run in this session. Read-only session: no state mutated, verkle tip and CURRENT.md untouched (tip read once, `cat memory/biography/verkle_tip.json`).

## Verdict

The DNA's load-bearing architecture is still true on disk: all 20 named doc/dir targets exist, and 14 of 15 code/pipeline claims verify against live code. Three real drifts: (1) the file itself is truncated mid-word on its last line; (2) the named `session_end_hook` trigger does not exist anywhere in live code or hook config, and the live mechanism is a polling daemon whose log phase is literally named "session_end_summary_fallback"; (3) the two commitment IDs on line 3 are orphaned, appearing nowhere outside DNA.md itself.

## Drift findings

### D1. File truncated mid-word (last line)

`docs/DNA.md` ends at line 147 with `Skip forever-keeping every P` + CRLF. Verified by byte dump: `tail -c 120 docs/DNA.md | od -c` ends `...e v e r y space P \r \n`. The sentence is cut off mid-word (context suggests "every PDF", the export-layer sticker the doc keeps demoting). The Backup DNA section's final bullet is unreadable as written.

### D2. `session_end_hook` does not exist; the live trigger is daemon polling

DNA "Create / Required (SessionEnd)" (docs/DNA.md:75-82) names the pipeline `hooks -> session_end_hook -> summarize_session -> residual/{id}.json -> session_card -> registry.jsonl -> chain leaf + tip -> kpi.json`.

- `grep -rln "session_end_hook" mag/ dashboard/ configs/ hooks/ scripts/ main.py mag.cmd .claude` finds it only in `dashboard/data/ESTATE_INDEX.jsonl` (a data index row, not code). There is no `hooks/` dir at root. `.claude/` contains only `settings.json`, and it has no `hooks` key (only env vars).
- The real triggers, all verified:
  - `mag/daemon.py:33-51` `_maybe_summarize_ended_sessions`: a background loop polling `watch/last_seen_session.txt` for a session switch, then calling `summarize_session(prev, use_llm=True, force=False, amend=True)` and logging phase `session_end_summary_fallback` (mag/daemon.py:45) plus a periodic live amend of the open session. The module docstring: "Sovereign Mag background loop."
  - Mag agent seats: `mag/chat_source.py:423,444` (`file_agent_seat`, "FILE one Mag agent seat into residual DNA + Verkle leaf") calls the same `summarize_session`.
  - Backfill: `main.py:2647-2651` `backfill-sessions` -> `mag.records.backfill_sessions` (mag/records.py:171), whose loop calls `summarize_session(..., force=True, pdf=True, amend=True)` at mag/records.py:202.
- Tension with DNA's own Rule (docs/DNA.md:4): "Fidelity lives in files + chain, not in a process that must stay awake." The primary close-out mechanism is now exactly such a process (the daemon). Mitigated in practice: `pack_status` completeness, not the trigger, decides incompleteness, and the fallback commands rebuild crashed sessions (all four verified, below).

### D3. Commitment IDs are orphaned

`grep -rn "dna-residual-003"` and `grep -rn "coldest-vertex-001"` over `mag/ configs/ memory/biography/registry.jsonl memory/biography/kpi.json memory/knowledge_graph.json docs/DNA.md` return exactly one hit each: docs/DNA.md:3 itself. Neither ID is knotted, registered, or referenced by any machine-readable store. The commitment header is decorative.

### D4. Backup DNA list mixes path conventions (ambiguous, would misdirect a backup)

DNA "Backup DNA" (docs/DNA.md:139-147) prefixes only `memory/biography/residual/`; the other five artifacts are listed bare: `registry.jsonl`, `knots/`, `verkle_tip.json`, `verkle_chain.jsonl`, `kpi.json`. At repo root none exist: the existence loop returned MISSING for all five bare paths. All five exist under `memory/biography/` (verified: `memory/biography/registry.jsonl`, `memory/biography/knots`, `memory/biography/verkle_tip.json`, `memory/biography/verkle_chain.jsonl`, `memory/biography/kpi.json`, plus `memory/biography/derived/`). A reader taking the doc literally would back up nothing but residual.

## Verified TRUE (claim -> evidence)

| DNA claim (line) | Evidence this session |
|---|---|
| Rule: fidelity in files + chain (4) | Full write path is file-based: mag/biography.py + mag/registry.py + mag/verkle_knot.py + mag/records.py (cited per row below). Caveat: D2 trigger tension. |
| docs/HOW_TO_MAG_DASHBOARD.md (8) | EXISTS |
| docs/ref/OPERATOR_CARD.md (9) | EXISTS |
| memory/agent_state/LATEST.md (10) | EXISTS |
| docs/ref/DASHBOARD_DESIGN.md (11) | EXISTS |
| Contracts in docs/ref/memory_verkle_map.md (14) | EXISTS; its line 15 carries the law verbatim: "tip = sessions only - residual = DNA - prompt is never memory" |
| docs/archive/ (16) | EXISTS (dir) |
| docs/templates/REF_LEAF.md, FEATURE_COMPOSE.md, MODEL_TESUJI.md (17) | ALL EXIST |
| docs/ref/strike_origin.md (18) | EXISTS |
| docs/ref/run_trail_lattice.md (19) | EXISTS |
| configs/modules.yaml + mag.cmd compose-status (20) | modules.yaml EXISTS; `compose-status` is a main.py command (main.py:658, 3710-3728, impl mag/modules.compose_status per mag/improve.py:1709) and mag.cmd forwards all args: it ends `"%PY%" "%ROOT%main.py" %*`, so `mag.cmd compose-status` resolves |
| docs/ref/lessig_1_6.md + memory/portable_bags/ (22) | BOTH EXIST |
| docs/ref/MIRROR_PRESENTED.md (23) | EXISTS |
| docs/ref/MAG_OS_v2.md, MAG_Card.md, MAG_Activation.md (24) | ALL EXIST |
| API GET /api/v1/mag-os (24) | Routed at dashboard/rest.py:5133 `("GET", "/api/v1/mag-os", h_mag_os)`, handler def at dashboard/rest.py:855 |
| docs/ref/MAG_v2_PLAN.md (25) | EXISTS |
| memory/improve/pins/LATEST.md (26) | EXISTS |
| Cold layer: SessionEnd must write; amend cannot strip core (42) | Write path verified below; core protection is real: mag/registry.py:126 docstring "Shared coldest vertex: core block that amend cannot strip." Trigger half is D2. |
| Sticker layer under derived/, export on demand (44, 49, 67) | memory/biography/derived/ EXISTS; visual is gated: mag/biography.py:554-556 sets `vis_meta = {"ok": True, "skipped": True, "reason": "export_on_demand"}` unless `visual=True`; PDF gated on `write_pdf` (mag/biography.py:458 comment "residual + leaf always; PDF/assets only when requested (export layer)") |
| Lean complete = residual + card + content_commit + chain leaf (89-95) | mag/biography.py:361 docstring "Always (lean): residual + card + content_commit + chain leaf (+ md narrative)"; mag/biography.py:318 `pack_status` docstring states the same; executed by mag/session_dossier.py:427 `write_session_pack` ("Build residual DNA + chain leaf") + mag/verkle_knot.py `append_verkle_knot` (:540-555 wires dossier to leaf hash/root) |
| residual/{id}.json canonical (76) | mag/registry.py:419 `publish_residual` -> memory/biography/residual/ has 4,003 `*.json` files (`ls memory/biography/residual \| wc -l`) |
| session_card (77) | written inside write_session_pack / write_derived_md (mag/registry.py:227); cards exist flat in memory/biography/ as `{sid}.md` (dir listing shows id.md beside each id.json) |
| registry.jsonl hot row (78) | mag/registry.py:27 `REGISTRY = BIO / "registry.jsonl"` = memory/biography/registry.jsonl; 3,918 lines (`wc -l`); first row schema `mag_session_registry.v1` with session_id/title/one_liner |
| chain leaf + tip (79) | mag/verkle_knot.py:34-35 `CHAIN = BIO / "verkle_chain.jsonl"`, `TIP = BIO / "verkle_tip.json"`; tip is written atomically (comment mag/verkle_knot.py:375-377 re torn tip write fix 2026-09-25). Live tip: schema verkle_tip.v1, n_leaves 8,259, root 58add4df..., last leaf 2026-09-28_2223 (today). `wc -l memory/biography/verkle_chain.jsonl` = 8,259: tip and chain agree exactly. Tip note field: "Tip is the chain tail. An amended older session does not become the boot" (supports the sessions-only spine) |
| kpi.json (80) | mag/records.py:16 `KPI_PATH = BIO / "kpi.json"`, writer `write_kpi` mag/records.py:138-166, called from summarize_session (mag/biography.py:567-575) and pack-status (main.py:2634). On disk: ts 2026-09-28T22:21:59Z, source "summarize", n_sessions 4,004, complete 68.4 pct, n_leaves 8,253 (kpi snapshot trails the 8,259 tip by 6 leaves: two different moments, not a contradiction) |
| Optional derived md/pdf/visual_pack via POST /api/v1/export {session_id, pdf?, visual?} (86-87) | Route dashboard/rest.py:5291 `("POST", "/api/v1/export", h_post_export)`; handler dashboard/rest.py:4202-4219 reads exactly `session_id` (or session/id alias), `pdf`, `visual`; defaults pdf=True only when neither given; delegates to mag/biography.py:253 `export_session_artifacts` ("On-demand human render layer from existing residual (no re-summarize required)") |
| Fallback commands (100-103) | ALL in main.py: pack-status :431/:2630 (which also calls write_kpi at :2634), backfill-sessions :442/:2647 -> mag/records.py:171, refresh-session-cards :461/:2657, migrate-lean-registry :465/:2669 |
| Board kanban Now / Open / Filed / Export ready, only primary surface (112, 121) | dashboard/static/board.js:9-13 `COLUMNS` exactly: now "Now", open "Open", filed "Filed", stickers "Export ready" ("Residual yes - PDF optional") |
| What was that day -> drawer cold read; sticky panels latest card + brief + attention (113-114) | board.js:163-165 renders `b.latest_brief` and `b.attention`; :110 reads `board.records_kpi` |
| Memory health -> kpi stats strip (115) | board.js:110 `records_kpi` consumed |
| Advanced menu (Operate, Visual, Tapestry) (116) | dashboard/static/app.js:560 `loadOperate()`, :651 `loadTapestry()` |
| Optional OS daily backfill-sessions (134) | command exists (row above); scheduler registration not checked (out of scope) |
| Spine edges: dig/pins/bonds (14) | mag/bonds.py exists (surfaced in the verkle_tip writer grep); pins = memory/improve/pins/LATEST.md (EXISTS). `dig` surface not individually located this session: not verified. |

## Measured store counts (context, each from a command above)

- memory/biography/registry.jsonl: 3,918 lines
- memory/biography/residual/: 4,003 json files
- memory/biography/kpi.json: n_sessions 4,004 (its own ts 2026-09-28T22:21:59Z)
- memory/biography/verkle_chain.jsonl: 8,259 lines == tip n_leaves 8,259
- registry rows trail residual files by 85. DNA does not claim equality (lean registry is a migration target, `migrate-lean-registry`), so this is reported as a measured delta, not a broken claim.
- Adjacent but distinct: `memory/ingest/registry.jsonl` (found via `find . -maxdepth 3 -name registry.jsonl`) is the chat-ingest DB (mag/session_dossier.py:303), not a second session-DNA store.

## Not verified (stated plainly)

- No end-to-end SessionEnd was executed (no live session closed); every pipeline stage is verified by reading its writer and its on-disk output, not by running a close.
- `POST /api/v1/export` and `GET /api/v1/mag-os` verified as routes + handlers in dashboard/rest.py; no live server was started to curl them.
- The daemon's scheduled cadence (who runs mag/daemon.py and how often) was not traced.
- `dig` edge surface named in the Spine line was not located.
- Whether some external harness (Claude Code, Codex) registers a SessionEnd hook outside the repo was not checked; inside the repo, no hook config exists.

## Method (commands as run)

`wc -l/-c docs/DNA.md`; `tail -c 120 | od -c`; existence loop over 26 claimed paths; `find` for registry/kpi/verkle/knots locations; scoped `grep -rn` for both commitment IDs and `session_end_hook`/`summarize_session`; `sed` reads of mag/biography.py:347-600, mag/daemon.py:1-60, mag/chat_source.py:415-450, mag/records.py:195-215, mag/registry.py and mag/verkle_knot.py grep maps, dashboard/rest.py handler + route greps, main.py command greps, mag.cmd head, dashboard/static/board.js:8-20; `cat memory/biography/verkle_tip.json` (read-only), `wc -l` chain, `head`/`tail` registry rows, kpi.json head + mtime.
