# queue/todo.md unchecked-item triage (item f-30, 2026-09-28)

Denominator: `grep -c '^- \[ \]' queue/todo.md` = **63 unchecked** vs `grep -c '^- \[x\]'` = 84 checked, 277 lines. queue/todo.md is gitignored (`.gitignore:41`), so it has no commit history of its own; closure evidence comes from receipts on disk and commits of the artifacts the items name. Every verdict below was checked this session against files I read or commands I ran.

**Verdict: 51 of 63 closeable (done by another lane, superseded, decided, or overtaken). 12 stay open.** Open residue concentrates in: operator-hands items (4), the verkle live fold awaiting operator GO (1), burn-window stragglers (5, two of which are duplicates of one item), one un-built design idea (1), and one half-done fleet wart (1).

## CLOSE (51)

### Decided / superseded inline, checkbox never flipped (10)

| Line | Item | Evidence |
|---|---|---|
| 5 | Cerebras card gate | Line carries "DECIDED 2026-09-26: PARKED" twice (lines 3 and 5). `configs/providers.yaml:699` still says "dormant pending operator GO". Decision recorded; flip the box. |
| 135-142 | FIFTY WIDE 09-15 board, 8 bundle lines | Line 133 declares the section SUPERSEDED 2026-09-17 with stragglers re-seeded as FW-37..49. Q-021 receipt verified both 09-15 boards carry appended SUPERSEDED headers and all 40 `memory/runs/fifty_wide/*` pointers dead (`watch/inbox/burn_reset_20260927/queue/Q-021.md`, FW-06 row). |

### FIFTY WIDE 09-17 board: executed by queue-gopher lanes 2026-09-28 (7)

| Line | Item | Receipt |
|---|---|---|
| 146 | A. FW-01..05 morning verification | `queue/Q-020.md` + `Q-020_FW01..FW05.md` (5 per-item receipts) |
| 147 | B. FW-06..14 census debt | `queue/Q-021.md` (nine items, table of outcomes) + `fifty_wide_20260917/FW06..FW14` receipts on disk |
| 148 | C. FW-15..18 tide machinery | `queue/Q-022.md` (four items; tide located as zcode automation, baseline banked) |
| 149 | D. FW-19..21 patrol debt | `queue/Q-023.md` + `fifty_wide_20260917/FW19/FW20/FW21` receipts |
| 151 | F. FW-27..31 operator gate packets | `queue/Q-025.md` (five packets) + `fifty_wide_20260917/FW27..FW31` receipts |
| 152 | G. FW-32..36 wave stones | `queue/Q-026.md` + `queue/FW32..FW36.md` receipts |
| 153 | H. FW-37..42 game estate | `queue/Q-027.md` ("all six landed") + `queue/FW38..FW42.md` + `Q_037_ws_probe.py` |

(Line 150, section E, is already `[x]` with receipt Q-024.)

### Done by another lane, receipt on disk (28)

| Line | Item | Evidence |
|---|---|---|
| 32 | Auto-promote gate | Q-002 DONE: `tools/auto_promote.py` + `tests/test_auto_promote.py` + `mag/improve.py` wiring + `configs/improve.yaml` `promote.auto` block (`queue/Q-002.md`) |
| 33 | Session cards dir | Q-003 receipt; `memory/biography/cards/` listed this session: multiple `.card.json` files present |
| 104 | Hand-annotate chord/refusal/rope rows | Q-007: 11 new rows banked in quantizer stream format, anchor-verified (`queue/Q_007_rows.jsonl`) |
| 126 | Spider threshold investigation | Q-008 executed: threshold fix landed, affected-file suite `tests/test_v3_modules.py` 9 passed including both spider regression tests; ghost.py spider_blind tripwire deliberately left (receipt says the todo source stays valid as tripwire) |
| 127 | comms_trail into routing | Q-009 Status: DONE; `gather_signals()` has carried `comms_consumption` since checkpoint d575bc168 (`mag/comms_trail.py:190-227` cited in receipt) |
| 129 | Derived DAG index | Q-010: `tools/derived_dag.py` (371 lines) built, index at `memory/derived/derived_dag_index.json` 30,772,308 bytes |
| 130 | Huang gate on roundtable | Q-011: `mag/frontier_salon.roundtable()` refuses escalation without `why` + single-seat baseline |
| 160 | Scanner v3 | `mag/catalog_rebuild.py` docstring: "idempotent full-estate catalog rebuild (v3, landed 2026-09-26). This is the salon Appendix A draft landed at last" (commit 383fed94f) |
| 161 | Catalog freshness budget + FTS5 decision | `mag/catalog_rescan.py` (C6 policy, B2-104) + `mag/catalog_freshness.py` (disclosure arm); FTS5 decided YES: `catalog/catalog_fts.sqlite` 161,345,536 bytes, mtime today 09:00, refreshed by MagFtsIndexDaily (`scripts/fts_index_daily.ps1` present) |
| 162 | Tags v2 owner + 50q eval | Q-031 DONE (owner column spec in `mag/catalog_tags.py`, held-out eval, mining NOT done per law); Q-030 records the ID-collision disposition |
| 194 | Swarm Roblox port | `roblox/src/server/SwarmZone.luau` on disk; games wave line 243 already `[x]`; input wiring via Q-037 |
| 195 | 3-key comparative audit | Q-033: "Comparative drift audit, same prompt x 3 free-tier lanes" |
| 196 | First video-input burn | Q-034: `corpus/library/openai-cookbook/examples/data/bison.mp4` (2,614,862 bytes) through stealth/space-bunny-alpha, no-video control; receipt explicitly says it closes the standing task |
| 197 | mirrors.json per-host diff | `configs/mirrors.json` live, writer `tools/stealth_driver.py:67` (`MIRRORS = ROOT/"configs"/"mirrors.json"`) and `:603` (persist per-host catalog diff); file mtime today 18:50 with churn fields |
| 198 | Reasoning-effort dial policy | Q-036: per-lane effort policy implemented in `tools/stealth_driver.py` + test |
| 203 | Roblox client pass | Q-037: chat remotes STUBBED then FIXED (`roblox/src/server/MudBasecamp.luau:25-29` old say() replaced), swarm shooting input, Wing Chun redirect; 4 source + build |
| 218 | Public gateway host | Q-039: non-localhost bind + shared-secret auth + proof script |
| 223 | v1.1 client polish | Q-040: FOV kick verified, cooldown chips, ContextActionService mobile bindings |
| 224 | Leaderstats page | Q-041: VM/Rebirths/Invariants/Summits scorecard landed |
| 225 | Pet orb model + trail | Q-042: pet made visible |
| 244 | Games polish backlog | Q-043: GnomeCode streamed maze sections, Trove loop ownership, cooldown chips UI, "All three landed" |
| 254 | Play-as-work v4 citation layer | RESOLVED by the v6 master (todo line 257's own UPDATE): `watch/inbox/play_as_work_20260926/VERIFICATION_v6_20260926.md` + `BRIEF_v6_master_20260926.md` on disk; 2 falsified v4 IDs replaced and re-verified |
| 255 | factorioctl go/no-go gate | Superseded by line 257's UPDATE: folds into the U1 substrate decision (FLE primary, factorioctl optional RCON path) |
| 262 | Next-window: read handoff, check smoke | Consumed: `../fle_u1/.fle/inspect_logs/2026-09-27T11-56-56...iron-plate-throughput...eval` exists, dated 09-27 07:56 local, after the 09-26-night handoff |
| 266 | Thought Quantizer v0.3 + recompile | `memory/corpus/quantized_thought/compile_report.json`: compiled 2026-09-28T16:19:05Z, v "0.3", `v3_amendment` = the owed two-pass classification over-refuse fix, packs frontier 24 / flash 12 / local 12 |
| 267 | Gene-pool regenerator or tombstone | TOMBSTONED: `watch/inbox/GENE_POOL_TOMBSTONE_20260927.md` + commit 8763e6809 (no regenerator, zero consumers, revive condition = consumer first) |
| 268 | FOSSIL-IN-FEED law teeth | `tools/fossil_check.py` IS the freshness arm: registry-driven (`configs/fossil_registry.json`), stats mtime vs bar, WARN-only, wired into the 08:30 census patrol, `--recompile` operator-gated |
| 98 | Review memory/attention.md pings | Q-005 (2026-09-28) triaged all 127 pings: RESOLVED not stale, records exist, writer `mag/biography.py:509-526`. Close the line; re-seed as a standing habit one-liner if the operator wants the ritual kept |

### Dirac open loops: all six closed by the 09-27/28 lanes (6 + structural = 6 lines, 272-277)

- Banked invariants ledger: `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` = exactly 6 rows (`wc -l`), first row is loop 3 (`organ:verkle_knot->organ:manifest`), loop receipts `watch/inbox/burn_reset_20260927/dirac_loops45.md` + `dirac_loop6.md`.
- I re-ran the check myself this session, read-only: `./.venv/Scripts/python.exe -m mag.dirac_loop scan` at 2026-09-28T23:08:12Z returned `ok=true, betti1=8, n_loops=6, closed_solved=6, open_gaps=0`, with loop 1 (`context_pack->swarm_surface`) closed over a real 6-organ path and invariant hash.
- Code anchors: loop 6 proof anchoring lives at `mag/water_computer.py:45-49` (`PROOF_FLAG = "water:anchored"`); loop 2 restore consumption at `mag/context_checkpoint.py:732-738`.
- The structural complaint (line 277, scan can never report closed) is answered in behavior: the scan now reports closed_solved=6 via the banked knot rows. Note: a PROPOSED 7th-loop edge sits in `flash50/w3-dirac-loop7.md` (not landed); it is a new item, not a reason to keep 272-277 open.

### Split: fold landed, residuals owed (1)

| Line | Item | Evidence |
|---|---|---|
| 249 | DF fold owed | The named folds are on disk: `roblox/src/shared/SphereKinship.luau`, `DfValue.luau`, `Temptation.luau`, `ProceduralBody.luau` (ls verified). Flip the box on the landed fold; re-seed the inline-owed residuals (supernatural villain plots, per-class attack triggers beyond scorpion-force, Ages of Powers branch) as their own line. |

## KEEP OPEN (12)

| Line | Item | Why still open, checked this session |
|---|---|---|
| 31 | Verkle noise compaction live fold | Q-001 (2026-09-28): plan-only banked, `tests/test_verkle_compaction.py` 9 passed, but execute is double-gated on operator GO ("NO GO on execute" escalation ruling; real numbers 247 folded / 790 kept, not "99"). A lane cannot close this; the operator must GO. |
| 97 | Manual REPL verify | Operator-hands by definition (type !steer/!pause/!continue in a real terminal). No receipt can substitute. |
| 99 | W0.0 archive drop | `C:/Users/foste/Documents/projects/mycelial-republic/data/raw/` verified this session: contains only `.gitkeep` (0-byte). Archive still not dropped; whole republic chain still blocked on the operator. |
| 204 | Roblox Studio publish | Needs the operator's Studio session (rojo serve/connect/publish + SKU ids). |
| 205 | THE CATHEDRAL live Studio smoke | Same Studio gate; fresh debt filed 09-27 with re-check by 2026-10-04. Owner named in the item. |
| 232 | Stone 2b punch list | Sub-items (1)-(6) done per inline status and receipts, but (7) shared_surface INDEX fold rebuild is still OWED: `grep -n "rebuild" mag/shared_surface.py` = no match (single `def main` at :407, no rebuild verb). The 09-27 commit 383fed94f ran a one-time "fold rebuild + 58 register heals" but landed no standing CLI. Close (1)-(6), re-seed (7) alone. |
| 233 | Stone 3 paced FullScan + deep-read | Drain is live and writing today: `state/fuel/full_scan_ledger.jsonl` (4,184,386 bytes, rows through 2026-09-28T13:39Z, some lanes failing with 429/timeout). The owed GLM deep-read rerun + Cooper synthesis after the drain has no receipt. |
| 234 | Stone 7 box burn | Instrument exists (`tools/box_burn_watch.py` + `state/fuel/box_burn_watch.jsonl`), but the GPU unlock wiring (llama-server/Vulkan routing), the Mr Pool 340-video whisper transcriber locate, and the nightly burn driver are not landed (`ls scripts/ | grep -i burn` = decks_nightly/vision_nightly only, no grounding_chain burn driver). Operator-infra. |
| 235 + 237 | Stone 5 Grok passes (DUPLICATE lines) | Packet on disk (`watch/inbox/GROK_LANE_PACKET_20260925.md`); Ask 4 scope frozen (`GROK_ASK4_SCOPE_FREEZE_20260926.md`, B2-141), but the audit itself and asks 1-3 (adversarial falsifier pass, W4 rerun review, October reading list) have no receipts. These two lines are the same item stated twice; merge them into one line while re-seeding. |
| 239 | Sunday close | Close receipt EXISTS (`watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md`, running close) but its own addendum via `watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md` records Arm C-200 killed at 1/30 after 66 minutes, bars frozen, rerun "Owed for the next lane with box time"; Grok/MiMo last burns not receipted. Keep until Arm C lands and the Grok burns close. |
| 250 | Ratchet enablement dials from DF fix taxonomy | Not built: `grep -iE "enablement|dial|always-on|opt-in|manual-only"` over `tools/violation_ratchet.py` + `configs/violation_baseline.json` matches only "dialogue" substrings. Design idea, nothing landed. |

## Method

- Read `queue/todo.md` in full (277 lines); enumerated unchecked lines with `grep -n '^- \[ \]'` (63).
- queue/todo.md is untracked (`.gitignore:41`); `git log -- queue/todo.md` empty, so closure evidence was taken from receipts and from git history of the artifacts the items name (e.g. 383fed94f for catalog modules, 8763e6809 for the gene-pool tombstone).
- Receipt dirs swept: `watch/inbox/burn_reset_20260927/queue/` (Q-001..Q-050 + FW32..42), `watch/inbox/fifty_wide_20260917/` (FW06..FW31), `watch/inbox/burn_wave_20260926/B2_140`, `watch/inbox/GENE_POOL_TOMBSTONE_20260927.md`, `watch/inbox/play_as_work_20260926/`, `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl`.
- Live checks rerun this session: dirac scan (read-only, verdict quoted above); directory listings for `memory/biography/cards/`, `catalog/catalog_fts.sqlite`, `mycelial-republic/data/raw/`, `../fle_u1/.fle/inspect_logs/`, `roblox/src` fold/swarm files; greps for shared_surface rebuild verb, violation dials, mirrors writer, cerebras dormant flag, quantizer compile report (mtime + content), full_scan ledger tail, Arm C closeout.
- Not done / not verifiable here: I did not edit queue/todo.md itself (other lanes hold active claims on it; this triage is the recommendation). The one file I could not check deeper is the content of the FLE smoke eval (binary-ish artifact; existence + post-handoff mtime is the evidence used).
