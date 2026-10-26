# Backup archaeology — the Aug-19 draft of the brain (2026-09-04)

Digger: zcode gopher (orphan-mine card). Backup: `C:\Users\foste\Documents\backups\local_sovereign_agent`.
Law framing: SACRED COWS, NOT LEGACY SHIT — this backup is one draft of the brain. Verdict up
front: **the live tree already kept every cow.** The dig's premise (orphaned files) is DISPUTED;
what the backup actually is: a sealed era-snapshot whose unique asset is the pre-recommit knot
hashes and the last git bundle. Details below, tri-state, evidence attached.

---

## 1. DATING — SUPPORTED

- Backup **is** a git repo. Tip: `e3e1b92` 2026-08-19 09:55 EDT ("move saelis-31b model weights
  out of repo; exclude models from backup"). Branch: `mag/run-beta1-factory-build-audi-20260806T231709Z`.
- 10 uncommitted changes, all = the models/ extraction (logs/.gitkeep + models/*.py deleted) —
  i.e. the backup was sealed **mid-chore**, right after the tip commit.
- Newest working-tree mtimes: `backup_to_drive.cmd` + `.gitignore` 10:09, `local_sovereign_agent.bundle`
  10:24, heartbeat last beat 10:56Z (06:56 EDT). **Sealed ≈ 2026-08-19 10:24 EDT.**
- Lineage position: last activity before sealing = steal-game-features / kabuki / ask-for-matthew
  research (handoff/ 08-18/19). Git HEAD in LIVE continues to `47d3907e` 2026-08-25 20:43 ("fuel_feed
  wired into autodrain") — and `e3e1b92` **is an ancestor of live HEAD**. Clean line, no fork.
  In the SPORE lineage this is the **close of the ghost/marathon era, pre-fleet, 6 days before
  Sancho day one (08-25)**.

## 2. GONE (in backup, absent from live) — SUPPORTED, and it's nearly empty

Checksummed: 3,445 curated common files (memory/ and mine/ run-history excluded from "curated").

| Item | What it carried | Disposition |
|---|---|---|
| `local_sovereign_agent.bundle` (13MB git bundle, branches archive/* codex/* cursor/*) | The branch-pack of the era | **DUPLICATE** — live `.git` (37 branches, 23 matching those patterns) carries them; tip is ancestor of live HEAD |
| 1,116 `memory/biography/knots/*.knot.json` | Pre-recommit knot set (backup 15,138 knots vs live 28,384) | **RESOLVED** — not lost: same session_ids live in live knots under new filenames. Spot-proof: backup knot `2026-08-03_0517_session_mag-agen_71bcb2a2` vs live `..._5bcbbb3d` — same schema, 25/28 fields identical; only `dossier_commit`/`leaf_hash`/`filename` differ. A re-commit pass re-hashed the leaves. **Caveat: the pre-recommit leaf_hash values exist ONLY in the backup** — if any old receipt cites one, the backup is the only verifier. |
| 19 `memory/runs/*`, 2 `memory/mail/*` | Run artifacts | Not inspected in depth; runs dir is append-heavy in live — presumed superseded. UNPROVEN whether any is uniquely load-bearing. |
| 1 file in `mine/` (agentops survey route.ts) | Scraped repo content | Noise. DUPLICATE-by-origin (re-scrapable). |
| `models/` (saelis-31b stack: providers, quota, registry, remote…) | Moved out of repo deliberately BY the tip commit itself | RETIRED BY DESIGN — re-downloadable from HF `slashreboot/saelis-31b`. Not a loss. |

**The card's hypothesized orphans — CONSTITUTION.md, THE_MACHINE.md, HANDOFF_MAG_AGENT_TODOS.md,
the `_afk*.py` series — are ALL present in live, byte-identical** (not in the 170-file diverged
set). The live tree is a strict superset at path level. The sacred-cows law was already being
practiced before it was written down.

## 3. DIVERGED (in both, materially different) — SUPPORTED: 170 files, additive evolution

Breakdown: mag/ 102, dashboard/ 17, top-level 10, watch/ 10 (volatile state — pid/json/session,
noise), tests 8, docs 5, queue 4, configs 4, rest scattered.

- **AGENTS.md (87L → 99L)**: live ADDS the "Shared artifact boundary" section (watch/inbox +
  SHARED_SURFACE_CONTRACT + validate command). Nothing dropped. Signal loss: none.
- **TOOLS.md (3784L → 3788L)**: same inbox-boundary block added. 472 tools both sides. No loss.
- **LOAD.md, CONSTITUTION.md, THE_MACHINE.md, HANDOFF_MAG_AGENT_TODOS.md, README.md**: byte-identical.
- **docs/CURRENT_BUILD_STATUS.md**: live prepends a HISTORICAL SNAPSHOT banner (points to
  watch/ORPHAN_AUDIT.json) — an honest retirement of a status doc, content intact beneath.
- **queue/todo.md**: live ticks items DONE 2026-08-26 (dossier sanitization — which found and
  redacted a live xAI key; provider liveness 12 lanes; republic_os round). Evolution, not loss.
- **mag_launch.py / mag/process_supervisor.py**: live adds the single-authoritative-supervisor
  guard (`MAG_RUNTIME_ROLE`, `_mag_launch_active`, the L8 double-supervision law). This is the
  RESPAWN LAW (08-26) being wired into the elders before their retirement — the bones got the
  fix, then the daemons were retired.
- **.env**: diverged, expected (lane/key rotation). Not opened — secrets law.
- The other ~95 mag/ divergences = six days of live builds (08-19 → 08-25): inbox/shared_surface,
  fuel_feed/autodrain, RIB anchors, quota gates. No backup-only function found in spot checks.

## 4. PRECURSORS — the bones and their reinterpretations — SUPPORTED

| Backup-era organ (name) | Live reinterpretation | Status |
|---|---|---|
| THE_MACHINE.md (08-17: two grok seats + ollama deepseek-1.5b glue + training loop + Mirror Sea game) | The workspace AGENTS.md standing wave + watch/FLEET_CONTRACT_V5; the "seats on contracts" idea became the seat/room mesh | File kept as fossil; concept evolved |
| CONSTITUTION.md (pointer to ../mycelial-republic, fork-equality, T0–T3 tiers, handoff.v1) | ../mycelial-republic/docs/CONSTITUTION.md **still exists**; laws recovered into FLEET_CONTRACT_V5_DRAFT_20260901.md §1 ("CONSTITUTION — standing laws, known set + recovered 20, deduped") and the operator-corrections skill | Bone carried forward twice over |
| HANDOFF_MAG_AGENT_TODOS.md (v2 merge queue #8–#11, verkle-audit cadence, MagImproveDaily tasks) | The queue/ system; live AGENTS.md:49 still points to it "if implementing" | Still wired, not orphan |
| _afk*.py (AFK keep-alive ticks: keep_gate campaign, chasm_state persist, party_subchain append, Calcifer the hearth, babel-fish lore) | mag/afk_cadence.py + mag/afk_loop.py (evolved, live); game_campaign.py now 3,119 lines | Ghost ticks became cadence organs |
| _afk_full_blast.py's MOVE chord ("Do not salon in Cursor… Grok strategizes, VS Code materializes if seated") | The seat discipline + one-builds-one-verifies mesh law | The chord is recognizably the embryo of fleet cadence |
| party_subchain / verkle_lance / steer / chasm_state / wave | All still present and evolved in live mag/ | Never left |
| training_rows.jsonl + steer feedback (THE_MACHINE loop) | memory/pile/training_rows.jsonl still present | Bone intact |
| flock_field/flock_grid (magnetic-field swarm, landed 08-14) | Still in live mag/ | Never left |
| git history as truth | Live git went quiet after 08-25 20:43; truth moved to files + verkle chain ("chat is vapor") | Reinterpretation, by design |

## 5. GAPS / hygiene notes (small, honest)

1. **Live tree carries literal backslash-prefixed duplicate files** (`mag/\chord_lens.py`,
   `docs/\FRAMEWORK_LOAD.md`, biography knots `\2026-…`) — a buggy rename/copy pass left a
   second copy under a `\` name. Harmless so far, but it double-counts in scans and one of them
   could someday shadow a real import. Candidate for a janitor sweep.
2. **Pre-recommit leaf hashes** (see GONE caveat) — if the chain-freeze moment (room that
   remembers) ever needs to cite pre-Aug-19 leaves, the backup is the only witness. Keep the
   backup; do not prune it after "everything is duplicated" — that claim is true at path level,
   not at hash level.
3. `memory/law/registry.json` and `memory/percolator/invariants.json` carry **no references** to
   the elder docs — the elders live on through docs/ and AGENTS.md:49 only. If HANDOFF's merge
   queue is ever declared dead, an explicit retirement note in the law registry would close it
   cleanly (name the reinterpretation, then retire the draft).

**Bottom line:** no bones left unsteal. The Aug-19 draft is fully contained in the live brain
except one thin, real asset — the pre-recommit hash lineage — and one convenience — the sealed
git bundle. The backup earns its disk space as a notarized era boundary: the morning the ghost
era ended and six days later Sancho began.
