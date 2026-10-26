# corpus-01: docs/DNA.md full fact-check against live repo state

Item: corpus-01 (source doc: `docs/DNA.md`). Date: 2026-09-28. Method: read `docs/DNA.md` in full (148 lines, 5,798 bytes, CRLF); every cross-referenceable claim checked against the live tree this session with the command or file:line shown. Working tree `docs/DNA.md` is byte-identical to HEAD (`git status --porcelain docs/DNA.md` = clean) and untouched since Aug 6 18:28 (mtime), 2 commits total (eb07ad62e baseline, c5031bf45).

## Verdict summary

20 of 20 referenced paths exist. 17 claim groups verified ACCURATE with live anchors. 3 DRIFTED (one named component absent, one pointer phrasing rotted, one commitment ID unanchored). 3 MISSING/DAMAGE rows (truncated last line rode the publish baseline; backup ecosystem postdates the doc; AGENTS.md one-liner is lossy). The machine DNA describes is RUNNING (tip/chain/registry/kpi all written 2026-09-28 20:15-20:16 local) while its own constitution doc is 53 days stale.

## Fact-check table

| # | DNA.md claim (line) | Verdict | Evidence (read/ran this session) |
|---|---|---|---|
| 1 | Commitment `dna-residual-003` (:3) | DRIFTED: unanchored ID | grep `dna-residual-003` over live tree (excl .git/corpus/agents/.venv/.mimosa): hits only docs/DNA.md itself + binary catalog/receipt_fts.sqlite + orchestrator transcripts memory/agent_sessions/orc-*.json. No code, config, or data file defines or reads it |
| 2 | Coldest vertex `coldest-vertex-001` (:3) | ACCURATE | Second live anchor docs/archive/README.md:5 "Moved here under `coldest-vertex-001` so Mag hangs on residual+card+tip only"; semantics consistent with DNA's coldest-vertex concept |
| 3 | Daily path docs: HOW_TO_MAG_DASHBOARD (:8), OPERATOR_CARD (:9), agent_state/LATEST (:10), DASHBOARD_DESIGN (:11) | ACCURATE | `for p in ...; test -e` : all 4 EXIST |
| 4 | Spine: Verkle tip sessions-only + contracts in docs/ref/memory_verkle_map.md (:14) | PARTIAL DRIFT | File exists (44 lines, read in full) and carries the spine law verbatim-adjacent: line 15 "Law: tip = sessions only · residual = DNA · prompt is never memory"; BUT grep for "pack-first", "artifact.*transcript", "trail integrity" in that file = 0 hits: the three phrases DNA cites as the contracts are not in the cited target |
| 5 | docs/archive/ (:16) | ACCURATE | dir EXISTS |
| 6 | Templates REF_LEAF / FEATURE_COMPOSE / MODEL_TESUJI (:17) | ACCURATE | all 3 EXIST under docs/templates/ |
| 7 | docs/ref/strike_origin.md (:18), run_trail_lattice.md (:19) | ACCURATE | both EXIST |
| 8 | configs/modules.yaml + `mag.cmd compose-status` (:20) | ACCURATE | modules.yaml EXISTS; mag.cmd forwards `%*` to `.venv\Scripts\python.exe main.py` (mag.cmd:1-10); command registered main.py:658, dispatched main.py:3710 |
| 9 | docs/ref/lessig_1_6.md + memory/portable_bags/ (:22) | ACCURATE | both EXIST |
| 10 | docs/ref/MIRROR_PRESENTED.md (:23) | ACCURATE | EXISTS |
| 11 | MAG_OS_v2.md + MAG_Card.md + MAG_Activation.md + `GET /api/v1/mag-os` (:24) | ACCURATE | 3 files EXIST; route table dashboard/rest.py:5133 `("GET", "/api/v1/mag-os", h_mag_os)` |
| 12 | docs/ref/MAG_v2_PLAN.md (:25) | ACCURATE | EXISTS (landed by c5031bf45, the same commit that last touched DNA.md) |
| 13 | memory/improve/pins/LATEST.md (:26) | ACCURATE | EXISTS |
| 14 | Cold layer: residual + card + content_commit + chain leaf; SessionEnd must write; amend cannot strip `core` (:42) | ACCURATE (core half) / DRIFTED (SessionEnd half, row 30) | mag/registry.py:121-126 `attach_cold_core` docstring: "Shared coldest vertex: core block that amend cannot strip." plus mag/modules.py:250 comment "do not touch d[\"core\"] - write_residual -> attach_cold_core preserves it"; residual json on disk carries literal `core` + `content_commit` keys (inspected residual/019f4d15-...json key list) |
| 15 | Matthew-shaped prune rule: Steiniger EUT / Scalar Knots as ops grammar, CC-BY, not product physics; prune theater never core; coarse-grain is the card (:46-47) | ACCURATE | mag/registry.py:125 docstring "Steiniger-shaped ops: protect residual seed; coarse face = card."; docs/archive/FUTURE_PROOFING.md:6 "Use papers as falsifiable grammar... Attribute CC-BY Steiniger" and :25 Scalar Knots table row |
| 16 | Lean complete = residual + card + content_commit + chain leaf; missing PDF/visual not incomplete (:92-95) | ACCURATE | mag/biography.py:358-360 docstring: "Always (lean): residual + card + content_commit + chain leaf (+ md narrative). Optional export layer (only if requested): pdf, visual_pack, chart assets." |
| 17 | residual/{id}.json canonical (:35, :78) | ACCURATE | memory/biography/residual/ holds 4,003 {id}.json files (`ls | wc -l`); writer mag/registry.py:192-215 `write_residual` sets schema mag_residual.v1, coldest_vertex True, path residual/{sid}.json; RESIDUAL_DIR registry.py:25 |
| 18 | registry.jsonl hot row (:80) | ACCURATE | memory/biography/registry.jsonl 6,006,209 bytes mtime 2026-09-28 20:16; rows schema mag_session_registry.v1 (tail inspected); writer `upsert_registry` mag/registry.py:323 |
| 19 | chain leaf + tip (:81) | ACCURATE | memory/biography/verkle_tip.json 496B schema verkle_tip.v1 n_leaves 8270 last knot 2026-09-29_0038 (live); memory/biography/verkle_chain.jsonl 5,794,274B mtime 2026-09-28 20:16; CHAIN = BIO / "verkle_chain.jsonl" at mag/verkle_audit.py:20, verkle_knot.py:34, verkle_lance.py:48, verkle_rib.py:37 |
| 20 | kpi.json (:82) | ACCURATE | memory/biography/kpi.json 59,327B mtime 2026-09-28 20:15; `write_kpi` called at main.py:2634 |
| 21 | Fallback commands: backfill-sessions / migrate-lean-registry / refresh-session-cards / pack-status (:100-103) | ACCURATE | all 4 in main.py: pack-status :431+:2630, backfill-sessions :442+:2647, refresh-session-cards :461+:2657, migrate-lean-registry :465+:2669 (registration + dispatch read) |
| 22 | `POST /api/v1/export` {session_id, pdf?, visual?} (:87, :115) | ACCURATE | route dashboard/rest.py:5291; handler rest.py:4202 `h_post_export` reads body session_id + pdf + visual exactly as documented |
| 23 | UI "Export PDF / Export visual" buttons (:87) | ACCURATE | dashboard/static/board.js:217 `id="bdExportPdf">Export PDF` and :222 `Export visual` |
| 24 | Board kanban Now / Open / Filed / Export ready, only primary surface (:112, :121) | ACCURATE | dashboard/static/board.js:8-13 COLUMNS = now/open/filed/stickers titled exactly "Now", "Open", "Filed", "Export ready"; hints match DNA semantics ("Filed: Lean DNA complete", "Export ready: Residual yes · PDF optional") |
| 25 | Lab live board + companion at :8765 (:65) | ACCURATE | dashboard/server.py:49 `DEFAULT_PORT = 8765`; config.py:168 `port: int = 8765` |
| 26 | Backup DNA list: memory/biography/residual/, registry.jsonl, knots/, verkle_tip.json, verkle_chain.jsonl, kpi.json (:142-145) | ACCURATE (names resolve) / MISSING (ecosystem, row 32) | direct `ls -la`: all six exist under memory/biography/ (knots/ holds *.knot.json); DNA lists them bare without the biography root, resolved by mag/registry.py:24-25 BIO = ROOT/"memory"/"biography" |
| 27 | `hooks → session_end_hook → summarize_session` pipeline (:76-77) | DRIFTED: component does not exist by name | No file, function, or hook config named session_end_hook anywhere live (grep: only .mimosa hook-state session artifacts + corpus transcripts). Harness config C:/Users/foste/.zcode/cli/config.json hooks events parsed: PreToolUse x2 (prebuild_gate.py, md_record_seal.py gate) + PostToolUse x2 (md_record_seal.py seal, mag/trajectory_step.py hook). NO SessionEnd event wired |
| 28 | Close actually works anyway | ACCURATE (rewired) | summarize_session real: mag/biography, imported main.py:2288, CLI `summarize-session` main.py:2287-2340; session-switch fallback mag/daemon.py:23-51 `_maybe_summarize_ended_sessions` via watch/last_seen_session.txt pointer calls summarize_session(prev, amend=True); agent seats via file_dirty_agent_sessions main.py:2292-2303 + daemon.py:53-72 |
| 29 | Optional derived export layer, stickers regenerable (:86-88) | ACCURATE | biography.py:359-360 + rest.py:4202 docstring "On-demand PDF/visual from residual (export layer)"; disk shows {id}.pdf and {id}.visual_pack.json next to residuals in memory/biography/ |
| 30 | DNA.md last line "Skip forever-keeping every P" (:147) | DAMAGE: truncated mid-word, pre-existing | od -c of tail: file ends `every P\r\n` with no continuation; identical tail bytes in baseline eb07ad62e and HEAD, so the truncation rode the clean-publish baseline (intended text likely "every PDF"); file unmodified since Aug 6 |
| 31 | Backup section completeness (:138-147) | MISSING | Chain ecosystem postdates the doc and is absent from it: memory/biography/repair_backups/verkle_20260831T0212Z/verkle_chain.jsonl, five verkle_chain.jsonl.bak-* files (batch-20260906, knotnight-20260912, orphanlane x3), four memory/biography_backup_flag_* snapshot dirs (20260826 x3, 20260926) - all found via find this session |
| 32 | Close ritual coverage | MISSING | AGENTS.md pile habit adds `mag.state_snapshot.capture_summary` at session close (kinds session_end/escalation/run_close per mag/state_snapshot.py:41) and agent-seat close path; DNA's Create section predates both and names neither |

## Cross-doc consistency note

AGENTS.md DNA line reads "residual + registry + leaf = filed workdays" while DNA.md:92 lean set is "residual + card + content_commit + chain_leaf". Same spirit, lossy letter: the AGENTS.md one-liner drops card and content_commit and swaps chain leaf for bare leaf. Not counted as DNA drift; flagged so the next DNA edit aligns the one-liner.

## Patterns (7)

1. **Pointer integrity is 100 percent, prose integrity is not.** All 20 paths DNA references exist, yet the doc still drifted: the drift is in named mechanisms (session_end_hook), cited phrasing (pack-first/artifact/transcript), and commitment IDs (dna-residual-003), not in file pointers. File-exists checks alone would have passed this doc.
2. **The named component rotted, the function survived.** `session_end_hook` exists nowhere; the close pipeline is fully alive as CLI summarize-session + daemon session-switch fallback + agent-file path. Mechanism names in docs are the first thing to rot; check the function, then the name.
3. **The constitution's strongest promises are code-anchored, not prose-anchored.** "Amend cannot strip core" is a docstring (registry.py:124) plus a no-touch comment (modules.py:250); the Steiniger prune rule lives as "coarse face = card" in the same docstring. When a DNA claim sounds aspirational, the enforcement is usually sitting in mag/registry.py.
4. **Two commitment IDs, one bound, one floating.** coldest-vertex-001 has a second live anchor with consistent semantics (docs/archive/README.md:5); dna-residual-003 is referenced by nothing outside itself, transcripts, and a receipt index binary. A commitment ID with no binding is a sticker, not a law.
5. **Damage can be canonicized.** The mid-word truncation "every P" rode the clean-publish baseline eb07ad62e and sat untouched for 53 days (mtime Aug 6, 2 commits). A publish baseline freezes defects the same way it freezes truth.
6. **The doc's operational inventory silently aged.** The Backup DNA list predates the chain's whole safety ecosystem (5 .bak chain files, repair_backups/, 4 biography_backup_flag_ snapshot dirs) and names none of it. Constitution sections that inventory artifacts need the same freshness discipline AGENTS.md applies to census counts (B2-216).
7. **The machine runs while its constitution sleeps.** tip n_leaves 8270 with a knot written 2026-09-29 00:38 UTC, registry 6.0MB, chain 5.8MB, kpi 59KB all written 2026-09-28 20:15-20:16 local: DNA is being produced hourly by code that no longer matches its own doc's vocabulary. Fidelity lives in files + chain, exactly as DNA.md:4 promises; the doc itself is now the stalest file in the estate it describes.

## Verification commands run this session

- Read docs/DNA.md in full (148 lines / 5,798 bytes)
- `for p in <20 paths>; do test -e` : all EXIST
- `ls -la` memory/biography/{kpi.json,registry.jsonl,verkle_chain.jsonl,verkle_tip.json}; `ls memory/biography/residual/ | wc -l` = 4003
- `grep -n "backfill-sessions|migrate-lean-registry|refresh-session-cards|pack-status" main.py`
- `grep -rn "api/v1/export|api/v1/mag-os" mag/ dashboard/` ; sed of h_post_export
- python json load of residual sample key list; head of verkle_tip.json; tail of registry.jsonl
- grep session_end across main.py + mag/; read mag/daemon.py:1-80
- python parse of C:/Users/foste/.zcode/cli/config.json hooks events (PreToolUse 2, PostToolUse 2, no SessionEnd)
- grep -rln dna-residual-003 / coldest-vertex-001 live tree (excl .git/corpus/agents/.venv/.mimosa)
- read docs/ref/memory_verkle_map.md full (44 lines); grep for cited phrases = 0 hits
- read mag/registry.py:121-150 + 192-215; mag/biography.py:350-420; mag/modules.py:250
- grep Export PDF/visual in dashboard/static/board.js; sed COLUMNS board.js:7-14
- grep 8765 dashboard/server.py config.py; head mag.cmd
- od -c tails of docs/DNA.md at working tree, HEAD, and baseline eb07ad62e (identical truncation)

Not run: pytest suite (doc fact-check item, no code changed); no live HTTP call against :8765 (route existence verified from source registration, not a live request).
