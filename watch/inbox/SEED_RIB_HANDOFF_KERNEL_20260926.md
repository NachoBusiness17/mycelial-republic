# Handoff-kernel map -> SEED-RIB table of contents (2026-09-26, B2-300)

Feeds B2-150 (SEED-RIB sections). Format carrier: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md
+ tools/seed_rib.py (B2-180). Operator order: mine every handoff surface for
what cold starts actually need; extract the repeated kernel and the stale-trap
history; distill into seed sections with byte counts.

## 1. Surface census (bytes measured 2026-09-26)

| Surface | Bytes | Role in cold start |
|---|---|---|
| memories/session/next-window-handoff.md (frozen spec) | 27,077 | procedure + standing laws + STATE log (STATE section grows unbounded: 27KB against its own "keep it short" law) |
| AGENTS.md | 14,099 | env laws, commands, build discipline, clippy bullets |
| HANDOFF_MAG_AGENT_TODOS.md | 13,415 | master queue; as-of 2026-08-05, 52 days stale |
| queue/todo.md | 30,014 | live board |
| context-pack (mag.cmd, rendered) | 4,703 | policy + thesis + tip + health, pack-first |
| state/CURRENT.md | 1,964 | canonical owed list |
| memory/briefs/latest.md | 2,182 | FROZEN banner: regenerators wore Aug content on a today face (the stale-trap fossil, sealed 2026-09-26) |
| state/START_BRIEF.md | 1,528 | running/queued/health; "landed while away" tail shows 2026-08 steals (stale tail disease) |
| watch/inbox close receipts (*CLOSE*.md) | 11,635 (3 files) | session-close snapshots |

## 2. The repeated kernel (transmitted by every surface)

1. **Env law** (in 4 of 8 surfaces): `.venv\Scripts\python.exe` or `mag.cmd`,
   never bare `python` (Hermes venv on PATH). One sentence, byte-cheap,
   breakage-expensive when lost.
2. **Load order**: FRAMEWORK_LOAD -> compass -> AGENTS.md -> pack (handoff
   procedure step 1 = AGENTS.md load table = context-pack header).
3. **Standing thesis / current climb** (context-pack L0b, CURRENT, brief):
   the objective card; the one thing every window must re-read.
4. **State.now**: what is running, what is queued, top owed (START_BRIEF
   running/queued/health; CURRENT owed list; handoff STATE section; todo head).
5. **Filing law**: durable writes to watch/inbox + receipt + index register +
   checkpoint; residual on disk is truth, chat is heat.
6. **T0/T1 + tier ladder**: local janitors first, pack+goal to remotes, never
   chat history; escalation tags.
7. **Open loops / owed**, each with a pointer and an owner.

## 3. What handoffs got wrong (the stale-trap history, seed must fix structurally)

- **Fossil-in-place**: memory/briefs/latest.md regenerated August content with
  today's face until frozen 2026-09-26 (banner + writers sealed + OS read-only).
  Lesson: a seed section carries its OWN as-of stamp and a verifier seal, never
  a regenerated face.
- **Missing carrier**: BOOT_4_7.md is cited (AGENTS.md freshness gate) but does
  not exist in state/ on disk today; Clippy cited a fossil once before and the
  next-window-handoff.md was created as the fix. Lesson: every seed pointer
  must resolve or be named UNRESOLVED (seed_rib verify never invents bytes).
- **Unbounded STATE**: the frozen handoff's own "keep it short" law lost to a
  27KB log. Lesson: seed sections have byte caps; history moves to pointers.
- **Stale tails**: START_BRIEF's "landed while away" serves 2026-08 rows;
  HANDOFF todos as-of 2026-08-05. Lesson: state sections must be regenerated
  from live ledgers at build time, never hand-carried.

## 4. Proposed SEED-RIB table of contents (byte counts are caps)

| # | Section | Cap | Source of truth at build time |
|---|---|---|---|
| 1 | env.law | 800 B | AGENTS.md python-env block (extracted, dated) |
| 2 | load.order | 1,100 B (amended 600 -> 1,100, 2026-09-26, card seedrib) | AGENTS.md load table (paths + sha256 seals) |
| 3 | thesis.card | 1,500 B | context-pack L0b (regenerated each build) |
| 4 | state.now | 1,500 B | START_BRIEF + CURRENT owed head (regenerated) |
| 5 | filing.law | 800 B | next-window-handoff procedure step 5 + claim laws |
| 6 | tier.law | 500 B | T0/T1 local, ladder, escalation tags |
| 7 | pointers | 2,500 B | seed_rib.v0 pointer entries (path+sha256, UNRESOLVED named) |
| 8 | law.heads | 1,500 B | memory/law/registry.json ids + law-file seals (law_refs) |
| | **kernel total** | **<= 9,700 B** | fits the B2-180 100KB fleet budget with 10x headroom |

Amendment log (caps are law; amendments are dated, never silent):
- 2026-09-26 (card seedrib revision): load.order cap 600 -> 1,100. Full
  64-hex sha256 seals for the 7 load-table file rows cost ~450 B alone; the
  600 cap forced either dropped seals or truncated ones, and a seal that is
  not full is not a seal. Measured content on the landed tree:
  kernel/load.order.md 832 B with all 7 rows full-sealed. The kernel TOTAL
  ceiling stays <= 9,700 B as the binding cap (per-section caps are maxima,
  not allocation; the amended caps sum to 10,200, and a build that hits
  every cap simultaneously still fails the 9,700 total check). Battery:
  watch/inbox/seed_rib_20260926/check_seed_rib.py C6 enforces both.
- 2026-09-26 (card seedrib revision): in the merged tree, section 7
  (pointers) rides as POINTERS.sha256 at the tree root, outside kernel/;
  its 2,500 B cap is unchanged and the section-8 law.heads cap is unchanged.
  Directory-carrier semantics: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md
  v0.1 amendment note.

Build order for B2-150: sections 1-2-5-6 are static law (seal once, re-seal on
change); sections 3-4 regenerate from live surfaces at every seed build
(never hand-carried); sections 7-8 are mechanical outputs of tools/seed_rib.py.
