# VC2_CHAIN_STATE — verkle crawl, knotted-state half

**Date:** 2026-09-16 · **Lane:** wave · **Agent:** VC2 (chain/ledger auditor)
**Method:** bytes-only audit via `.venv\Scripts\python.exe` (no git writes, no paid APIs). Receipt appended as evidence lands.

## Scope

Enumerate every CHAIN and LEDGER the fleet maintains: health, last entry, growth tonight (2026-09-16), and the maintenance action owed.

## Audit log (appended as gathered)

### Chain 1 — watch/GROUNDING_WAVE.jsonl (grounding chain) — **RED**

- **Rows:** 124 (0 unparseable) · **Bytes:** 136,261 · **Span:** 2026-09-05T23:08:25Z → 2026-09-16T13:16:40Z
- **Growth tonight (2026-09-16):** 3 rows (122, 123, 124)
- **Verdict histogram:** 59 SUPPORTED / 64 UNPROVEN / 1 none
- **Verify status — RE-CONFIRMED FAIL.** Canonical `mag.grounding_wave.verify()` returns: `FAIL row 122: prev-hash mismatch (chain broken)`.
  - Row 122 (2026-09-16T04:17:37Z) is a **skeleton row**: only `prev/ts/claim` — no `hash`, no `verdict`, no `evidence` — AND its `prev` (`8ccd3924…`) does not match row 121's hash (`bfe89d61…`). Doubly broken.
  - Rows 123/124 are a **repair attempt** ("wave row corrected per canonical hash convention"): they re-post the same claim fully formed (SUPPORTED, evidence, hash), and 124→123 links correctly — **but row 123's `prev` is an empty string**, deliberately orphaning 122 instead of re-chaining through it. So the strict walk now breaks at BOTH 122 (prev mismatch) and 123 (prev ≠ 122's nonexistent hash). The chain is forked: canonical tip = 1–121 → 123 → 124 (`8d2cc3dd…`); 122 dangles as a side-branch.
- **DRAFT block:** no DRAFT verdicts in the file itself (4 rows — 24, 78, 80, 108 — mention "DRAFT" only in claim/note prose). The operative DRAFT block is `watch/inbox/wave_20260916/drafts/` — 7 files (10,895 B), all W1-union-alpha's 429-killed first attempt + probe scraps, frozen since 16:55 local. Status: graveyard, already superseded by `receipts/W1_WORLD_SKELETON.md`.
- **Evidence rot:** evidence strings are free-form (paths + parentheticals + commands), so no strict count; a crude scan shows ≥10 early rows citing `state/overseer_latest.json`, which no longer exists on disk. Blocked behind the 122 break — `verify()` short-circuits before the evidence audit.
- **Maintenance owed:** one operator-blessed bench command — either re-chain row 122 onto 121's hash (backfill hash/verdict/evidence) or excise it and stitch 123.prev = 121.hash, then re-run `verify()` to restore LINKAGE-PASS. Precedent exists: "row-175 surgical rechain" of 2026-09-06 (row 27).

### Chain 2 — state/fuel/ (lite pacing + quota) — **AMBER**

**lite_pacing.jsonl** (11,511 B)
- **Rows:** 86 · **Span:** 2026-09-06T06:31Z → 2026-09-16T20:55Z (schema lite_pacing.v1, `day/door/tokens`)
- **Growth tonight:** 16 rows today. Per-day tail: 09-14=21, 09-15=29, 09-16=16.
- **Today's spend:** **25,418 tokens** across 4 doors — lane_runner 11,512 (7 fires) · concert001 7,823 (4) · scale_salon 5,780 (3) · research_fanout 303 (2). Lifetime total 122,782 tokens.

**lite_quota_log.jsonl** (22,281 B)
- **Rows:** 85 · **Span:** 2026-09-05T04:24Z → 2026-09-16T23:02Z (schema lite_quota.v1, weekly/session snapshots)
- **Growth tonight:** 19 rows today. Weekly pool: reset mid-day 09-15 (5,979/10,000 → 0); as of last snapshot (09-16T23:02Z): **weekly used=1/10,000 (1%)**, session 1/2,000. Next reset ≈ 09-22.
- **Health:** green as a file (appending, fresh, parseable).

- **⚠ Cross-ledger discrepancy (the amber):** pacing says 25,418 tokens / 16 fires today; quota says 1 unit used this week. The two ledgers are not measuring the same economy (units or source differ — provider-reported vs local accounting), so "budget remaining" cannot be derived from either alone.
- **Maintenance owed:** reconcile the two — decide which is source of truth for the 10,000/week budget and make the other derive from it (or document the units).

### Chain 3 — memory/trajectory/steps.jsonl (trajectory tape) — **GREEN**

- **Rows:** 5,670 (0 unparseable) · **Bytes:** 6,108,168 (~6.1 MB) · schema `trajectory_step.v1` (`ts/session_id/face/command/result/step_hash`)
- **Span:** 2026-09-05T17:07Z → **2026-09-16T22:48Z** (fresh — minutes before this audit)
- **Growth tonight:** **313 rows today** (154 since 12:00Z wave-start); hourly activity continuous 00Z–22Z, peak 38 rows @13Z.
- **Distinct session_ids:** **36 all-time · 7 in today's wave** — top today: `sess_727c2fc5` (160 steps), `sess_712a3b7b` (69), `sess_f2600e4d` (45), `sess_f8f2909b` (30), + 3 minor (≤4 steps each). **7 windows are in the wave.**
- **Face histogram:** 100% `bash` — every step is a shell command with exit + output excerpt.
- **Health:** green — appending live, parseable, per-step hashed (`step_hash`).
- **Maintenance owed:** rotation/compression policy — 6.1 MB in 11 days is fine now, but it is the fastest-growing chain in the fleet; set an archive threshold before it becomes the next oversized tail.

### Chain 4 — watch/inbox/LINKS.jsonl (link registry) — **GREEN**

- **Rows:** 174 (0 unparseable) · **Bytes:** 95,715 · **Span:** 2026-09-14T07:24Z → 2026-09-16T20:05Z (`seq/ts/url/canonical/canonical_sha256/writer`)
- **Growth tonight:** **146 rows today** (84% of the entire ledger landed in the last ~36h).
- **Writer histogram (all 174):** `zcode-journal-window-20260915` **100** · `canon-fungal-20260916` **26** · `zcode-estate-walk-20260914` 12 · `zcode-rashomon-20260914` 10 · `free-resource-scout` 7 · `backfill-20260916` 6 · `backfill-zenodo-20260916` 4 · `zcode-maze-refraction-20260914` 3 · `zcode-xmine-20260916` 3 · `zcode-jev-20260916` 2 · `dedupe-test` 1.
- **Writers tonight (146):** journal-window 98, canon-fungal 26, free-resource-scout 7, backfill 6, backfill-zenodo 4, xmine 3, jev 2 — a 7-writer night.
- **Health:** green — appending, deduped via `canonical_sha256`, multi-writer with attribution.
- **Maintenance owed:** purge the `dedupe-test` row (or mark it as a fixture); consider re-homing the 20260914 walkers' history if the registry is meant to be wave-scoped.

### Chain 5 — watch/inbox/index_events.jsonl → INDEX.json (shared-surface index) — **AMBER**

**index_events.jsonl** (68,838 B)
- **Rows:** 173 parseable + **3 corrupt** (lines 94–96: `"seq":NEXT` placeholder never resolved to a number — invalid JSON, all three register/amend `workspace_snapshot_20260901_1345Z.tar.gz` on 09-01, day one) · **Span:** 2026-09-01T03:18Z → 2026-09-16T17:27Z
- **Growth tonight:** **17 events today.** Op histogram: register 158 · amend 9 · invalidate 2 · note 3.
**INDEX.json** (47,399 B): derived_at **2026-09-16T12:04Z** at event_count=156 → **17 events / 5h24m of drift** (incl. registers for THE_SCALE_FINAL, HERMES_PLUGIN_CATALOG_AUDIT, JOURNAL_20260916). active_items=140 vs 150 distinct files ever registered. Carries **23 fold_warnings**, dominated by writer `sancho`/`sancho-salon` seq nonce gaps.
- **Health:** amber — the event log itself is fine and appending; the derived index is stale and the log's head contains 3 permanently unparseable rows every reader must skip.
- **Maintenance owed:** re-derive INDEX (`mag.shared_surface validate` + derive); fix or quarantine lines 94–96; chase the sancho nonce gaps (seq discipline violation by that writer).

### Chain 6 — state/ other ledgers (verkle knots + activity + small ledgers) — mostly **GREEN**, one **AMBER**

**memory/biography/verkle_chain.jsonl — the verkle knot chain — GREEN (the flagship)**
- **Rows:** 8,473 knots (0 unparseable) · **Bytes:** 5,932,593 · **Span:** 2026-08-10T21:37Z → **2026-09-16T23:06Z** (2 min before this audit)
- **Growth tonight:** **111 knots today** (daily tail: 09-12=160, 09-13=213, 09-14=157, 09-15=103, 09-16=111)
- **Tip integrity — verified by bytes, not reports:** `memory/biography/verkle_tip.json` says `n_leaves: 8473` (**==** chain row count) and `last_leaf_hash: 4d32f869…` (**==** last row's `leaf_hash`, knot `2026-09-16_2306_autonomous-janitor_autonomo_tfd21de5.knot.json`). Tip in sync with chain.
- **Backups:** daily `memory/biography_backup/biography_backup_20260916/verkle_chain.jsonl` (5,894,176 B, 07:38 today) plus seals. But `memory/biography/` itself carries **8+ stale `.bak-orphanlane/knotnight-2026090x` files** (~41 MB of litter).
- **Maintenance owed:** sweep the `.bak-*` litter out of `memory/biography/` (backups already exist in `biography_backup/`); keep the daily backup rotation as is.

**state/shared_activity.jsonl — fleet heartbeat/activity ledger — AMBER (bulk)**
- **Rows:** 84,289 · **Bytes:** 23,425,632 (**largest ledger in the fleet**) · **Span:** 2026-08-04T16:07Z → **2026-09-16T23:10Z** (live, seconds before audit)
- **Growth tonight:** **2,481 rows today**; 92% of today is `seat:"heart"` governor_autorun heartbeat (2,274 rows) — body 177, mind 12, mag 6, local 6, api 3, grok_tui 3.
- **Health:** amber — the chain is alive and healthy but is 23 MB of mostly scut heartbeat; it is the fleet's biggest storage consumer per unit of signal.
- **Maintenance owed:** throttle/rotate the heart heartbeat (sample every Nth tick or split heart-scut into its own rolling file) before this becomes a multi-100-MB tail.

**Small state/ ledgers (one line each):**
- `state/kvos_blocks.jsonl` (751,793 B, 3,991 rows) — **AMBER/stale**: last write 09-10 (dedup census: 9,019 blocks, 2.4% dup); owed a refresh run.
- `state/operator_mode.jsonl` (19,082 B, 49 rows) — green: appended today 21:21Z, mode=`running` (autonomous scope).
- `state/m12_armed_nights.jsonl` (1,810 B, 3 rows) — green-ish: last night opened 09-14, closed today 14:49Z, 0.0 min floor method.
- `state/capacity_ladder.jsonl` (3,127 B, 5 rungs R0–R4) — stale since 09-12, fine (config-like census).
- `state/decisions_done.jsonl` (14 ids), `state/handshakes.jsonl` (7 gates, last hermes-nous-220), `state/art_queue.jsonl` (**0 bytes — empty**) — dormant, no action.
- `dashboard/static/vislab/health.json` (18,103 B, 09-14) — health snapshot file, 2 days stale; owed a health-cycle run if vislab is still in service.

### Chain 7 — memory/runs/*/raw.jsonl (run tapes) — **GREEN**

- **Tapes:** 9 `raw.jsonl` across 360 run dirs · **Rows total: 299** · **Bytes total: 516,691**
- **Growth tonight:** **7 of 9 tapes written today** — d23_salon50_night 56 rows (95,602 B), u4_union_verdict_column 33 (81,006 B), p2_demo_salon 24, e_union_alpha 19, scale_salon 12, rs_worldbuild_salon 9, u5_union_witness 5. (research_50_wow 77 and salon_50 64 are from 09-15.)
- **Health:** green — small, active, per-run scoped (the blast-radius pattern working as designed).
- **Maintenance owed:** none. The other 351 run dirs carry their docs/receipts without tapes, by design.

---

## Chain health table

| # | Chain | Bytes | Rows | Last entry (UTC) | Tonight | Health | Owed |
|---|---|---|---|---|---|---|---|
| 1 | watch/GROUNDING_WAVE.jsonl | 136,261 | 124 | 09-16T13:16 | +3 | **RED** | surgical rechain of row 122 (or excise + stitch 123.prev) |
| 2 | state/fuel/lite_pacing.jsonl | 11,511 | 86 | 09-16T20:55 | +16 | AMBER | reconcile units vs quota log |
| 2 | state/fuel/lite_quota_log.jsonl | 22,281 | 85 | 09-16T23:02 | +19 | AMBER | (same discrepancy) |
| 3 | memory/trajectory/steps.jsonl | 6,108,168 | 5,670 | 09-16T22:48 | +313 (7 windows) | GREEN | rotation policy |
| 4 | watch/inbox/LINKS.jsonl | 95,715 | 174 | 09-16T20:05 | +146 | GREEN | purge dedupe-test row |
| 5 | watch/inbox/index_events.jsonl | 68,838 | 173 (+3 bad) | 09-16T17:27 | +17 | AMBER | re-derive INDEX; fix seq:NEXT lines 94–96 |
| 5 | watch/inbox/INDEX.json | 47,399 | 140 items | derived 09-16T12:04 | −17 events drift | AMBER | re-derive |
| 6 | memory/biography/verkle_chain.jsonl | 5,932,593 | 8,473 knots | 09-16T23:06 | +111 | **GREEN** (tip verified in sync) | sweep .bak litter |
| 6 | state/shared_activity.jsonl | 23,425,632 | 84,289 | 09-16T23:10 | +2,481 (92% heart-scut) | AMBER | throttle/rotate heartbeat |
| 6 | state/kvos_blocks.jsonl | 751,793 | 3,991 | 09-10 (stale) | 0 | AMBER | refresh dedup census |
| 6 | state/operator_mode.jsonl | 19,082 | 49 | 09-16T21:21 | today | GREEN | — |
| 6 | state/m12_armed_nights.jsonl | 1,810 | 3 | 09-16T14:49 | closed today | GREEN | — |
| 6 | capacity_ladder / decisions_done / handshakes / art_queue | 6,276 | 26 | dormant | 0 | dormant | none |
| 7 | memory/runs/*/raw.jsonl (9 tapes) | 516,691 | 299 | 09-16T17:39 | +7 tapes active | GREEN | none |
| — | watch/inbox/wave_20260916/drafts/ (DRAFT block) | 10,895 | 7 files | 09-16 16:55 local | frozen | graveyard | delete once W1 stable |

## Total bytes under chain management

**37,162,660 B (~37.2 MB)** across 15 ledgers + tip + DRAFT block.
= chains 1–5 + 7 (12,939,064 B ≈ 12.9 MB) + state/ block: verkle_chain 5,932,593 + verkle_tip 507 + shared_activity 23,425,632 + kvos 751,793 + operator_mode 19,082 + m12 1,810 + capacity 3,127 + decisions_done 412 + handshakes 2,737 + art_queue 0 + vislab health 18,103.
Largest single consumer: `shared_activity.jsonl` (63% of everything, mostly heartbeat).

## Verdict: can a new window replay the standing wave's trajectory?

**Half-yes — the tape exists, but it's split into two halves that must be joined by hand.**

- **YES at the command level:** `memory/trajectory/steps.jsonl` is a genuine replayable tape — hash-stepped (`step_hash`), session-attributed (7 wave windows tonight), every bash command with exit code and output excerpt, in order. A new window can mechanically re-run any wave window's shell actions.
- **YES at the narrative level:** `WAVE_STATE_20260916.md` is explicitly marked "Next window starts here," with a one-line census of all 35 receipts + gen-2 requeue (§4) + memory block (§3). Intent → outcome is reconstructable if the window reads it first.
- **THE GAPS:** (a) no single ordered artifact binds window → prompt → actions → verdict — steps.jsonl carries no prompts/reasoning, the receipts carry no per-step commands; (b) the chain *meant* to witness the night, GROUNDING_WAVE.jsonl, is RED tonight (row 122 break, repair forked at 123); (c) `shared_activity.jsonl`, the only always-on per-seat feed, is 92% heartbeat noise — only 6 mag / 6 local / 3 api / 3 grok_tui rows tonight, too thin to serve as a replay spine.

**One-line answer:** the trajectory is recorded — commands in steps.jsonl, meaning in WAVE_STATE + receipts — but replay requires reading both halves in concert, and the grounding chain that should certify the join is the one chain broken tonight.

---
*Audited by VC2, 2026-09-16 ~23:10Z. All numbers counted from bytes on disk via `.venv\Scripts\python.exe`; no git writes, no paid APIs. Receipt maintained append-only per wave-lane law.*
