# R6 — SWARM→APK SPAN (shadow work vol-2 night shift, 2026-09-06)

Seat: R6-swarm · Astra abridged (inventory → themes → active-arc → USAGE → promotions → cells)
Region: swarm span — `watch/` swarm cards, `memory/runs/swarm_worker/` (the swarm queue),
`memory/swarm_surface/`, `corpus/apk/`, the android-farm cards. READ-ONLY on corpus; $0; no daemons.

## 1. INVENTORY

**corpus/apk/ (the "9M android bridge")** — 1 artifact: `aurora_store_76.apk`, 9,360,088 bytes,
1,079 zip entries (666 xml, 230 png, 2 dex, 4 native .so, Kotlin builtins) = Aurora Store
(open-source Play client), Kotlin app. NOT inert cargo: per `watch/X_HARVEST_DOCTRINE_20260905.md`
it is **installed on golden body emulator-5554** — the "UI-as-API" door: a real body inside the
attestation perimeter speaks walled APIs from inside. X app install still "in flight"; login =
operator's one hand. Utilization: 1/1 deployed. The bridge carries ENTITLEMENT, not bytes.

**watch/ swarm cards (6/6 indexed into MEMORY.md):**
- `SWARM_DOCTRINE_20260901.md` — when-to-swarm law: ~$0 marginal on cached lanes; right lanes, right shapes.
- `SWARM_RESEARCH_LEDGER_20260831.md` (390 ln) — every swarm artifact mapped as claims, VERIFIED/CORRECTED/ATTESTED.
- `SWARM_LENS_PROTOCOL.md` — 6 gates; reportable subset ≠ automatic output (the format-eater in theory).
- `SWARM_SCALE_PLAN_20260904.md` — first 50-flight op: night-window replay of 228 open explore signals.
- `SWARM_SNAPSHOT_DFHACK_20260905.md` — mag/swarm_snapshot.py renders the 14-day fortress board (DFHack lens).
- `INTAKE_ALESKANDER_OPENSWARM_20260904.md` — external swarm witness (100+ agents via openswarm).

**The swarm queue (ground truth):** `memory/runs/swarm_worker/`
- `queue/` = **exactly 1,275 task files** (matches the 09-05 measurement). Status: **480 failed / 223 done / 572 cancelled** — done rate 17.5%, cancelled 44.9% never reaped.
- `results/` = 743 (`swarm_worker.result.v1`): 263 ok / 480 not-ok. Median result len ~587 ch (a fixed error template); ok-results include in-session deterministic resolutions ("[rightsized local] deterministic/RIB task (scut) — resolved without a deep model call").
- `results_incoming/` = 44 unmerged · `blackboard/` = 183 · `pheromone/` = 97 · `queue_backup_20260827_preRepoint/` = 715.
- `memory/swarm_surface/sent.jsonl` = **2,103 dispatch rows** (sw-* ids, surface+lens+anchor). Three ledgers (sent 2,103 / queue 1,275 / results 743), no reconciler.
- Task format: `{task_id, goal, provider, domain, tag, status}` — goal is prose; the tag (castle-foundation 613, orphan-sense 428, ox-fold-foundation 66…) is the real handler address.

**Android farm cards:** `ANDROID_FARM_SURFACE_20260904.md` (2 emulators live, mock GPS OK,
4 bodies fit in RAM, AutoGLM-Phone driver, UI-as-API read) + `ANDROID_EMULATOR_SELF_STEAL_20260904.md`
(headless-in-docker law, phonesalon run 001 typed a real prompt over adb, guest quota wall receipted).

## 2. THE LESSON MAP — the format-eater, fixed and proven at width 50

- **The finding (09-05, MEMORY.md):** "done ≠ produced — 1,275 swarm tasks, freeform goals no-op
  with empty results; shape goals to handler formats or run in-session; check task files before
  trusting done." Tonight's byte-check CONFIRMS the denominator (exactly 1,275) and the shape:
  goal-only prose ("SHADE NOVEL ORPHAN … fold it into an invariant or resolve the orphan.")
  no-ops with a boilerplate error; tasks whose tag addresses a real handler land.
- **The fix, proven tonight:** every walker prompt that landed carried an explicit OUTPUT CONTRACT.
  - 50 `shadow_slab.py` walkers: one slab each, deterministic CSV columns so the 50 outputs tile —
    **50/50 slab CSVs on disk** (`state/shadow_work/`), zero losses, at width 50 (ceiling experiment executed).
  - 6 region-walkers (R1–R6, this shift): inventory → connections → USAGE → top-3 promotions,
    ≤8-line return. All landed.
- **Triangulated law (three independent strata agree — swarm ledger 08-31, swarm_worker bytes,
  tonight's width-50):** a task lands when it carries **goal + format + verdict**; it no-ops when
  it carries goal alone. SWARM_LENS said it as theory ("reportable ≠ produced"), the queue said it
  as scars (17.5% done), the walkers proved it as practice (100/100 with contracts).

## 3. THE TIE — swarm tasks ↔ Shadow Walk quests

Same contract shape, three names. A quest is goal + format + verdict; a swarm task is goal + tag +
result.ok; a walker prompt is ask + output contract + falsifier.
- `DRAGON_HORDE_BRIDGE_20260906.md`: Shadow Walk consumes `shadow_walk_content.json` — 64 curated
  BATCH6 entries as encounters/loot/boss rooms.
- `mag/shadow_quest.py` already owns the generator shape (surface → lens → roll → tackle → fold,
  deterministic, $0) — it just lacks a real content source.
- **The promotion is mechanical:** point the quest generator at `memory/runs/swarm_worker/` —
  1,275 REAL tasks. done+ok → loot/encounters (263 real result payloads, each a verified artifact);
  failed/cancelled → boss rooms and shadow bodies (the Format Eater is the first boss: it eats
  misshaped goals); tag → region (castle-foundation, orphan-sense, ox-fold as biomes).
  The game then IS the backlog audit — which also dissolves the DRAGON_HORDE falsifier
  ("game and fleet state drift apart"): quests are fleet state, verbatim, hash-addressed.

## 4. USAGE / UTILIZATION

| Surface | Size | Consumed downstream | Verdict |
|---|---|---|---|
| corpus/apk | 1 file, 9.36MB | 1/1 installed on golden body (X_HARVEST doctrine) | UNDER-hauled: second lane (X app) unbuilt |
| swarm_worker queue | 1,275 tasks | 223 done consumed; 572 cancelled never reaped, 44 results unmerged | MOST-UNDERUTILIZED: 82% of the backlog is unharvested quest/lore material |
| swarm_surface/sent.jsonl | 2,103 rows | dispatch ledger only | unreconciled vs queue/results |
| watch swarm cards | 6 files | all indexed (MEMORY.md), snapshot live on dashboard | well-utilized |
| farm cards | 2 files | 2 emulators live, phonesalon proven | live arc |

Structural scar found en route: MEMORY.md card links are dead as files (`reference-swarm-queue-format-eater.md` MISSING) — the index IS the memory; cards exist only as index lines.

## 5. PROMOTIONS (top-3, exact next use)

1. **swarm queue → quest generator source** — extend `mag/shadow_quest.py surface()` to read
   `memory/runs/swarm_worker/queue/*.json` (goal→quest text, ok→loot vs boss, tag→biome) and emit
   into `shadow_walk_content.json`. $0, deterministic, reuses the existing shape; gives the game
   1,275 real quests instead of 64 curated ones.
2. **apk bridge → Shadow Walk mobile companion** — the farm already runs golden body 5554 with
   Aurora; sideload/wrap Shadow Walk onto a farm body; the phonesalon adb input loop is proven
   ("input text", %s-escape, session walls receipted). The dumb-agent-with-eyes plays the fleet's
   own dungeon — and THE RUN gets a phone-in-hand proof surface before Sep 20.
3. **the cancelled 45% reap** — 572 cancelled tasks: one width-50 night-window pass with the FIXED
   grammar (goal+format+verdict, free lanes per SWARM_DOCTRINE) — replay or formally write off
   into GROUNDING_WAVE so "done ≠ produced" closes with a receipt either way.

Bonus scar-fix: regenerate the missing MEMORY.md cards from the index (link-rot) — half-hour, $0.

## 6. CELLS POSTED (axis R, seat R6)

- `R/swarm/inventory` — SUPPORTED — 1,275/743/2,103 counted in bytes; apk = 1,079 entries, deployed.
- `R/swarm/format_eater` — SUPPORTED — freeform no-op vs contracted 100/100 at width 50; three strata converge.
- `R/swarm/quest_bridge` — UNPROVEN — contract isomorphism named; generator rewiring not yet built.
- `R/swarm/apk_bridge` — UNPROVEN — Aurora on golden body receipted; mobile companion is a promotion, not a build.
