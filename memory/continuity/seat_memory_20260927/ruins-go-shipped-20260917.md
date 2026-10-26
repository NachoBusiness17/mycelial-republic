---
name: ruins-go-shipped-20260917
description: "RUINS GO shipped 2026-09-17 — 30+ playable levels (12 chapters + bred, ALL PASS); evolution loop proven; rejection taxonomy mined (41 rejections, only 2 merit); traits wired into step() (vision/berserk); D&D layer + classes + arcade live"
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator order (2026-09-17, dropping the LCG Steam URL): "this should be our next version
of the maze — a duplication of this game and its puzzles as translated to programming",
then "steal the game and fill it with our shit."

**Shipped (commit 1ca274ab5):**
- Canonical engine `dashboard/static/games/ruins_go_engine.js` — one copy, HTML loads it,
  harness requires it. Ten laws: step-clock, one-height ledges, block pushes, crank-latch
  + plate bridges, collapse-behind, spear odd-tick parity, greedy snakes REFUSING the exit,
  lizard patrols, mirroring twin (denied→waits, holds plates), exit + optional gems.
- 12 levels / 4 chapters, inscriptions = fleet doctrine lines. UI `ruins_go.html` (iso
  canvas, pack autoload). Gate `test_ruins_go.js` at repo root — 51/51: 27 law minis +
  BFS solvability + deterministic replay; `--pack-all` validates all pack files.
- D&D layer v1 (commit f10546570): seeded stat blocks (mulberry32, MONSTER_TABLE with
  mud-boon traits thorns/chain/berserk/arc/vision), 8 tiny tales, classes Squire/Rogue
  (BFS first-move sight)/Monk (bits survive death)/Bard (tick parity visible).
- FLEET ARCADE index.html (discovery gap closed, commit 161cafffe).

**Design lessons the hard way:** greedy pursuer corners in open/simply-connected space —
snake levels need RING rooms (snake's refuse-the-exit law parks it as guard); lizard
patrol over only gate cell with period-2 oscillation is unpassable — exit goes under the
patrol's far end.

**Evolution loop proved same night:** 4/4 promoted gen-1 after the loop carried laws +
verified examples + verdict feedback (was 0/8 one-shot drafting). Then gen-2 passes:
"The Queen of Venom" + "The Unstamped Seal" FAILED gen-1, read BFS verdict, self-corrected,
PASSED gen-2. Decoration config (verified skeleton + one delta) went **9-for-9 undefeated**.

**AMENDMENT 001 + pack-wipe incident (commit b197eb7a6):** sloppy probe write overwrote
pack to one level — restored from HEAD + promotion receipts. Amendment 001 filed:
transport-deaths-never-count-as-attempts. My hand-designed twin-boss honestly REJECTED
(exhausted @8) — the gate ranks the human's work the same as the model's.

**BOSS BRED (commit eab20cc48):** "the mirror toll" · 5 moves — glm via rotation law
(union 404'd twice), gen-2 after union transport walls. The level I hand-designed and
failed twice; the machine bred it. Gate: ALL PASS.

**FINAL STATE (2026-09-18, commit 3d12289f9):**
- Pack: **30 levels ALL PASS** (12 hand-designed + 18 model-bred). Dual-window breeding
  (union + glm on same briefs) produces DISTINCT levels, not duplicates — both windows'
  variants kept by id-dedupe = population growth from concurrency.
- Combo puzzles + D&D encounters landed: "the far shore" (10m, filling the 10–14
  difficulty hole), "The Weight Remembers" (11m), "the keeper's no", "the odd middle",
  "the examined no", "the falsifiers ledger" (glm naming levels after our laws unprompted).
- Standing: 19 promoted runs / 18 merit-rejected; research 118/118 COMPLETE, 0 dead.

**REJECTION TAXONOMY (commit 3d12289f9):** 41 rejections mined — only **2 merit**
(BFS unsolvable: sealed path, parity trap). **39 infrastructure** (200-error-body 16,
404 window-end 11, empty_content 12, schema 2). The gate isn't strict — the pipe is
unreliable. These receipts ARE the negative examples for the astra training corpus.
Filed: watch/inbox/REJECTION_TAXONOMY_20260917.md.

**TRAITS WIRED INTO STEP() (commit 1f3a23c94):** vision snakes pathfind toward player's
start cell + current position; berserk lizards move twice per player step. Gate 51/51
held, pack 25 ALL PASS after. Stat blocks are now MECHANICAL, not display-only.
Thorns + chain traits queued (need skip-flag + tick-offset design).

**CANON DROPS FILED (commit b1413d3c7):** Steiniger EUT double-slit, Fauvel Bitcoin
steganalysis, Amdahl "There Are No Electrons". All in watch/inbox/canon_drops_20260917/.

**OPEN RANKED (audit + Elder pass 1):**
1. thorns + chain traits (skip-flag + tick-offset design)
2. mud duplicate fork at static/mud.html
3. maze_arena seeded harness (10 Math.random sites)
4. Degeneracy probe (UF-109) + citation battery (UF-47) — the Elder's meters

Related: [[lara-croft-go-links-row-20260917]], [[ox-alpha-was-glm53-flash]],
[[no-token-caps-100k-windows]], [[the-librarian-fleet-imprint-20260917]],
[[dd-layer-cross-game-transfer-20260917]], [[games-audit-fix-wave-20260917]].
