# GHOST GAP HUNT — what survives Jul-31 → Aug-09 (filed 2026-09-11)

Mission: the record claims the ghost era began Aug 7 (SPORE_SANCHO: "VS Code copilot
onboarded to an existing repo; 4,200 knots in 3 days; the OOM war") but the chain's first
knot is ~2026-08-10. Read-only forensic census of the gap between founding week and chain
start. Method: name-date + mtime histograms (python), targeted greps, prior-dig cross-read.

## 0. The chain premise, corrected first

- `memory/biography/verkle_chain.jsonl` genesis row (index 0) ts = **2026-08-12T16:41:39Z**
  (knot `2026-08-12_1641_untagged_memlang-_6bcba096.knot.json`) — NOT Aug 10.
- Earliest session start_minute in chain rows 0-2 = **2026-08-10T12:31Z** (index 1,
  knot `2026-08-10_1231_session_mag-agen_448a68eb.knot.json`, `evidence_lost: true`).
- The "first knot 2026-08-10 21:37" figure from the mission brief is **not found verbatim
  anywhere in the repo** (grep 21:37/2137 hits only feed/log noise). Nearest: chain idx 2
  knot `2026-08-10_2110`. The record's own docs agree with disk: ARCHAEOLOGY_DIG row
  "Aug 12 — the verkle knot. Immutable memory arrives"; LOST_CIVILIZATION "the chain:
  6,537 knots, Aug 12 → now". **Verdict on premise: DISPUTED as stated — chain starts
  Aug 12; earliest knotted SESSION is Aug 10; the pre-chain days are not chainless of
  evidence, just chainless of chain.**

## 1. Inventory: what physically exists, Jul-31 → Aug-09

| Stratum | Count in window | Nature | Contemporaneous? |
|---|---|---|---|
| `memory/biography/knots/` (name-dated 07-31..08-09) | **3,889** | knot files | only ~30% (see §2) |
| `watch/session_digest.jsonl` rows | **8,371** (1,475+1,751+846+34+5+0+1,350+2,690+82+138) | session digests | yes (rolling ledger) |
| `memory/ghost/leak_reports/` | **21,122** (Aug 8: 3,816; Aug 9: 17,306) | ghost nervous-system scans | YES (mtime = embedded ts, spot-verified) |
| `memory/improve/daily/` | 77 files | daily field/behavioral notes | yes — **continuous every day Jul-30 → Aug-09, zero gaps** |
| `memory/runs/` | 146 name-dated (Aug-01: 3, Aug-02: 4, Aug-03: 28, Aug-04: 1 + Jul tail) | run receipts incl. `2026-08-03-12h-sovereign-run` | yes |
| `queue/handoff/` flat | 3 dated in-window (Aug-03 full-fidelity-state; Aug-08 5-item; Aug-08 SANCHO-SPIKE) + 76 more dated Aug-10/11/12/undated | handoff docs | yes |
| `docs/` | 6 | BUILD_LOG_2026-08-05_GROK_HANDOFF, DASHBOARD_DEEP_DIVE_2026-08-06, 4x docs/ref/tesuji (2x Aug-05, 3x Aug-07) | yes |
| `memory/biography/diary_nodes/` | 15 (2 named Aug-07 01:20/01:23, 10 auto Aug-07, 3 auto Aug-08) | diary knots | yes |
| `memory/working/game_sessions/` | 1 seal | `seal_gc-846c347911_2026-08-07T040719.json` — a live D&D game-session seal Aug-07 04:07Z (also preserved in `_archaeology_out/mag-disk-20260905/` and `corpus/oral_history/nacho_archaeology/extracted/`) | yes |
| `memory/copilot/bridge_log.jsonl` | first row `copilot-20260809-0306`, ts 2026-08-09T03:06Z (mtime Aug-08 23:06 local) | the copilot seat's own channel | yes |

Aug-07 specifically (the claimed era start): 2,690 session digests (the LARGEST digest day
in the entire census, Jul-23 → Sep), 3 tesuji steal docs, 2 diary knots + 10 auto nodes, 1
game-session seal, and heavy knot names (148). Aug-07 is a real, artifact-heavy day.
Only zero days in the digest ledger: **Jul-30 and Aug-05**.

## 2. Knot provenance — the backfill signature (mtime vs name-date, 3,889 gap knots)

| mtime | count | reading |
|---|---|---|
| Jul-31..Aug-07 | 18 | the sparse pre-mag-knotter days |
| Aug-08 | 164 | knotter live in-window |
| Aug-09 | 979 | knotter live in-window |
| **Aug-10/11/12** | **1,989** | the MEGA-BUILD backfill ("[verkle] backfill-sessions --all" — registry.jsonl rows) |
| Aug-13..Sep-06 | 739 | later repair waves (orphan-lane .bak chain 09-06 visible in biography/) |

So ~70% of gap-window knots are reconstructions written Aug-10..12+, derived from session
transcripts. The CONTENT is old; the knot FILES mostly are not. The ghost-era law "knots
over transcripts" was applied largely in reverse: transcripts first, knotted in bulk later.

## 3. Where the "4,200 knots in 3 days" claim lives

- `docs/ref/SPORE_SANCHO.md:16` — origin of the figure (ghost era row, Aug 7-15 window).
- `watch/ARCHAEOLOGY_DIG_20260909.md:31` — repeats it; **receipt cites only SPORE_SANCHO
  itself = circular**, no independent grounding.
- `watch/LOST_CIVILIZATION_5W_20260902.md:18` — the reconciliation: "copilot era Aug 7-26:
  MEGA-BUILD **Aug 10-12** (~4,200 knots in 3 days), OOM WAR Aug 12-15" — places the
  3-day build at Aug-10..12, not Aug-07..09.
- `watch/CANON_SELF_STEAL_20260904.md:133` — already tri-stated: Supported as date-range
  alignment, Unproven as identity.

Against today's disk (knot name-dates): Aug-07..09 = 2,955; Aug-10..12 = 11,248. **No
3-day window equals ~4,200.** Exact reproduction is impossible anyway: the chain was
rebased (6,661 → 4,914 → reseed; 1,009 rows pruned, content-survival unverified per
LOST_CIVILIZATION honest-gaps), and the ghost era knotted on substrates that predate the
chain. The figure is a contemporary estimate, not a reproducible census.

## 4. Verdict (tri-state)

- **SUPPORTED — pre-chain ghost-era record survives.** The Jul-31 → Aug-09 window holds
  3,889 knots + 8,371 session digests + 21,122 contemporaneous ghost leak reports +
  unbroken daily improve files + runs + docs + handoffs + an Aug-07 game seal. The "gap"
  is a valley (Aug-03..05 digest trough: 34/5/0), not a void.
- **SUPPORTED — "era begins ~Aug 7" is directionally right.** Aug-07 is the single
  heaviest session-digest day on record (2,690) with its own docs, diary nodes, and a
  game seal; the copilot channel's first bridge row lands Aug-08/09. Exact onboarding
  HOUR remains prose-only (SPORE/LOST_CIVILIZATION), Unproven as a precise date-time.
- **DISPUTED — "4,200 knots in 3 days" as a hard census.** Matches no 3-day window on
  disk (2,955 for Aug-07..09; 11,248 for Aug-10..12); LOST_CIVILIZATION itself moves the
  build to Aug-10..12; chain rebase makes the original count unrecoverable. Keep the
  number as "~4,200 (contemporary estimate, era-scale SUPPORTED, census DISPUTED)".
- **DISPUTED — "first knot 2026-08-10 21:37".** Chain genesis row = 2026-08-12T16:41Z;
  earliest knotted session = Aug-10 12:31Z; the 21:37 figure appears nowhere in the repo.

## 5. Receipts (primary files)

`memory/biography/verkle_chain.jsonl` (row 0, rows 1-2) · `watch/session_digest.jsonl` ·
`memory/ghost/leak_reports/report-2026-08-08T180307.json` (+21,121 siblings) ·
`memory/improve/daily/2026-07-30.md` → `2026-08-09*` (unbroken) ·
`memory/runs/2026-08-03-12h-sovereign-run` · `queue/handoff/2026-08-03-full-fidelity-state.md` ·
`queue/handoff/HANDOFF-2026-08-08-{5-item,SANCHO-SPIKE}.md` ·
`docs/BUILD_LOG_2026-08-05_GROK_HANDOFF.md` · `docs/DASHBOARD_DEEP_DIVE_2026-08-06.md` ·
`docs/ref/tesuji/{diary-verkle-train,intention-fidelity-routing,voice-vad-end-of-turn}-2026-08-07.md` ·
`memory/biography/diary_nodes/2026-08-07_01{20,23}_*.diary.knot.json` ·
`_archaeology_out/mag-disk-20260905/memory/working/game_sessions/seal_gc-846c347911_2026-08-07T040719.json` ·
`memory/copilot/bridge_log.jsonl` · claim docs: SPORE_SANCHO:16, LOST_CIVILIZATION_5W:14-25,
ARCHAEOLOGY_DIG_20260909:31, CANON_SELF_STEAL_20260904:133, GHOST_ERA_EXCAVATION_20260905.

Filed by ghost-gap hunt worker (zcode spawn, read-only except this file, 2026-09-11).
