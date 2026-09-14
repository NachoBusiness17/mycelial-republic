# LANE D/6 — THE R&D HISTORY FOLDER (2026-09-11, static rebuild)

> **[AUDIT-TYPED]** status: SEEDED — folder live at `docs/rd_history/`, INDEX.md
> carries the schema + 12 real entries mined from the record. Bounds held: two
> files total (this card + INDEX.md); per-experiment files spawn as experiments
> happen, not retro-batched.

## THE PATTERN (generalized from the Viz Lab)

`viz_gallery.html` line 38: Spore (fish) — "attempt 1 — beautiful, wrong, kept
as the record." That is the whole doctrine: every experiment gets a file, its
test, its result, kept honestly whether it won or not. A wrong attempt with a
receipt outranks a right guess with none. This folder is that rule applied to
the whole fleet's functional tests of games/evolutions mapped to game data and
prompts/research.

## FOLDER DESIGN — docs/rd_history/

- One file per experiment: `NN_slug.md` (NN = entry number, date-ordered).
- Required fields: `{name, date, question, test, result, lesson, successor}` + receipts.
- `result:` is tri-state-friendly — SUPPORTED / DISPUTED / UNPROVEN / INCONCLUSIVE /
  "beautiful, wrong" are all valid outcomes. The folder records, it does not rank.
- `successor:` names what it became (page path, card path, or "retired — kept as
  the record"). Lineage over graveyard.
- Every entry cites at least one receipt that exists on disk (run dir, CONVO row,
  `.bak` pair, JSON receipt). No post-hoc polish: what the test showed at the time.
- INDEX.md is the catalog: schema template at top, one table row per entry.

## THE SEEDED INDEX (12 entries, full detail in docs/rd_history/INDEX.md)

| # | Name | Date | Question | Test | Result | Lesson | Successor |
|---|------|------|----------|------|--------|--------|-----------|
| 01 | Spore (fish) | 2026-09-08 | Can the SPORE design render as a living organism? | Render + operator eyeball | Beautiful, wrong — kept as the record | Keep the wrong attempt; it is the reference for the rename | `viz_horse_run.html` (02) |
| 02 | The Horse (running) | 2026-09-08 | What was the fish reaching for? | Re-read fish, rename target, re-render (flash lane, deepseek-v4-flash) | The organism in motion — both drafts kept side by side | Sacred-cow reinterpretation: steal bones, name the reinterpretation | Rocinante arc; `viz_gallery.html` pair |
| 03 | Wipeout fragmentation | 2026-09-08 | Does "song is the level" survive being built three ways? | One-night build storm: v1/v2/sunset/lightmaze | Family kept — each variant isolates one shader mechanic | Fragmentation is emphasis, not forks | wipeout_*.html; `SHADER_PIPELINE_RESEARCH_20260908.md` |
| 04 | Maze arena birth-defect surgery | 2026-09-06 | Why doesn't maze arena run? | Root-cause chain + headless sim harness (kept as regression) | Four stacked defects (sealed wall, inverted bounce, unbounded world, flood y-transform); fixed page answered its own falsifier: field beats bounce ~10x (GPS 4/4@315 vs dumb 2/4@769-2823) | Bogus fields look alive — LAW-061 validate-the-field | Tesuji map grammar; B1 ray-field (06) |
| 05 | Arrakis duplicate MACH | 2026-09-06 | Why does arrakis misbehave? | Backup-first surgery, diff verified | Duplicate `const MACH` shadowed the first (2 in bak, 1 after) | Birth defects stack silently; backup + diff is the method | Same-night fix sweep; error-banner fixture |
| 06 | Maze arena B1 shadow-field | 2026-09-06 | Does the 3-pass GPU ray-field port into our arena? | GLSL reimplemented from description (never pasted), BOTH/RAY/BFS modes side by side | Landed render-only — walkers still read CPU BFS (honest limit kept) | A field earns steering only after measurement | K-ray sensor → steps-on/off measurement |
| 07 | Tesuji T1 field map | 2026-09-06 | Is 5.3-flash a mappable field, not an oracle? | 23 stones / 43 cells, canon+rotation, $0.0218 | 43/43 home; rotation 0.950; predictive 0.977; needles at 32k-128k; one phrasing-dependent shadow | Probes are stones; shadows must reproduce under paraphrase | T2 cells; A6 Rocinante diff; `tesuji_map.html` |
| 08 | Hold-1 blind convergence | 2026-09-06 | Do two unshared chairs rebuild the same prompts the same way? | Lessig x Ponytail independent passes, sealed corpus 47e15c5d | Mechanism convergence total (all 8 targets); fiction-status divergence = the finding | Zero-shared-context convergence is validity | Arm B/C drafts; blind judges on grok sessions |
| 09 | KV-OS encoding dig | 2026-09-11 | Is DeepSeek `encoding/` a novel KV format? | All five HF files read raw; grep hash/cache/page/kv | Boring answer, boring is the answer: chat template as source; 3 vendor claims kept tri-state (interpolation UNPROVEN) | A mystery resolving boring is a result | `KV_OS_CHARTER_20260911.md` — five OS functions |
| 10 | MAX_DISTILL epoch 1 | 2026-08-27 | Does distillation beat raw high-effort? | 40 trials, 4 arms, twin-heldout scoring | INCONCLUSIVE (floor effects A=B=D=2/10; C transport-degraded; GAP_TOO_SMALL); infra laws were real (thinking=low, >=1536 tokens) | Honest INCONCLUSIVE with a receipt beats a claimed win | Epoch 2 at a quiet window; `memory/runs/max_distill/epoch1_report.json` |
| 11 | Eyes receipt | 2026-08-27 | Can blind, eyed, and vision agents be told apart? | Three-condition blind test, JSON receipt | Verified: blind fails honestly, vision reads exact, endowed passes | The loop works because each part fails honestly | Host ollama eye; vision pipeline READ stage |
| 12 | Arena-Bench v0 self-test | 2026-09-05 | Can a game room grade with zero human judgment — and can the grader fail? | `mag/arena_bench.py --selftest`, sealed functional, live-computed ground truth | Split proven: 1.0 honest-ghost vs 0.3675 maru-sycophant; finding: the Blind Gate had no mechanical existence before | A grader that cannot fail cannot grade | Benchmark lane vs Astra-14% baseline; Sep-20 rank |

## RECEIPTS (where each was mined)

memory/runs/game_prompt_lab/CONVERGENCE.md · memory/runs/max_distill/epoch1_report.json ·
memory/runs/eyes_receipt/receipt_20260827T082113Z.json · queue/handoff/zcode/CONVO.md rows
09-05 ~04:5xZ (arena-bench), 09-06 ~03:0xZ (maze fix), 09-06 ~04:0xZ (cartography/LAW-061),
09-06 ~11:5xZ (tesuji T1), 09-06 ~18:1xZ (prompt lab) · watch/TESUJI_MAP_5_3FLASH_20260906.md ·
watch/GAME_SUBSYSTEM_AUDIT_20260909.md · watch/inbox/MAZE_ARENA_B1_20260906.md ·
watch/inbox/v41_paces/LANE6_encoding.md · watch/KV_OS_CHARTER_20260911.md ·
watch/SEVEN_DAY_RECAP_20260909.md (build-storm night) · dashboard/static/arrakis.html +
.bak-fix-20260906 (duplicate MACH diff) · dashboard/static/viz_gallery.html (fish/horse pair).
