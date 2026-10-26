# STEAL — ROSTER SWAP (self-steal against Mag) — 2026-10-18

Verb: fleet/self_steal@v1 (docs/ref/verb_genomes/self_steal.md:13-29). Seat: Grok Bot executor, Sun 2026-10-18 ~09:45-10:15 ET.
Subject: the "Roster Swap" Grok Bot template (@AdventureNLearn, 2026-10-16, https://x.com/AdventureNLearn/status/2111186419494633562), aimed inward at Mag/estate organs and the box archival skill.
Rules kept: $0, no paid calls, no git, no code changes, no .env/keys/secret_gate_results/free_keys/trajectory reads, no process touched (MagLeaveProtocolDaily showed Status: Running; left alone). Writes: this file + one INDEX line.

Evidence tiers used below, never mixed:
- **[POST]** = what the X post / template page claims. Unproven for us.
- **[BYTES]** = read on disk today, path:line cited. Supported.
- **[REC]** = my recommendation. A proposal; operator authorizes.

---

## Verdict

Roster Swap is a **guided, YES-gated consolidation recipe**, not new technology. Mag + the box archival skill already hold the hard parts: hash-manifest archive and verify (archive_guard.py), never-delete gating, verified-backup rotation (backup_chain.py), a read-only organ inventory (backup_brain.py), handoff assembly (auto_handoff.py), drift tripwires (census_drift_patrol.py), and a revocation switch for signed seats (seat_allowlist.json). What is missing is the **glue**: a seat-roster inventory, a "fresh copy + restore only enabled routines" step, and a retire-label step. Two of those are **Grok Bot app actions** (export transcript, list/re-create routines, create/rename/delete a bot), not anything Mag code can do.

Smallest swap now [REC]: keep **Grok Bot (front door) + Mag (estate brain)** (+ Ghost only if Nacho keeps it as the front door instead of Grok Bot; see Fold), retire **Research, New Bot, Archival Bot, RefreshBot** as seats after archiving them with archive_guard.py `manifest` + `verify` (never `gate`/trash), fold their safety rules in as skills (archival skill is already one), and label retirees "RETIRED-20261018 — owner deletes". Monthly bloat check: yes, as a **read-only routine on Grok Bot**, not a Mag scheduled task.

Surprises (required by the contract):
1. **archive_guard.py would refuse to gate our own transcripts.** Its PROTECTED regex includes `transcript` (archive_guard.py:27, school-transcript intent). Any gate list naming `ghost_transcript.md` / `research_transcript.md` exits 2. `manifest`/`verify` do not check PROTECTED (archive_guard.py:64-98), so archive+verify works; only the trash gate refuses. For a roster swap that is actually correct behavior (we never trash), but it means "gate" cannot be reused as a retirement clearance for chat histories without renaming files or a regex exception. Don't change the regex; just don't gate.
2. **None of Nacho's Grok Bot seats are in Mag's seat registry.** configs/seat_allowlist.json:11 `seats` holds only 11 `mate:*` GLM seats (cartographer … composer), no ghost/research/refresh/archival/new-bot/grok-bot row. So "revoke the old seat" has nothing to revoke on the Mag side — retirement is purely app-side. (Conversely Mag's own roster that could bloat is the mates: configs/mates.yaml:34-161, 11 ids.)
3. **mates.yaml cites a launcher that isn't where it says.** configs/mates.yaml:2 says mates are "launched 08:00 by tools/leave_protocol.py"; no `leave_protocol*` exists under mag/, scripts/, tools/ (rg --files, today). The live MagLeaveProtocolDaily task runs via scripts/run_hidden.vbs → .venv python (action string truncated in schtasks output); its Last Result today 08:12 ET was 267009 (= "currently running"). Unproven what script it launches — a doc-drift item, not a swap blocker.
4. **Mag's backup rotation DOES delete.** scripts/backup_chain.py:256-260 `shutil.rmtree(old, ...)` prunes to KEEP=7 (line 55) verified backups, pinned biography_backup_20261004 exempt (line 65). That is the opposite of Roster Swap's / archival skill's "never deletes itself" law. Fine for rolling chain backups, but **roster archives must not live under memory/biography_backup/** or they inherit auto-prune.

---

## Inventory (paths + sizes, read today)

**[POST]** (verbatim summary): steps = archive every bot's full history → check archives → fresh copies → bring back only routines that were on → label old bots for owner deletion. Optional auto mode runs safe steps (inventory, archive, verify) then stops for YES before copying. Optional monthly bloat check. Every risky step waits for YES; never deletes. "Built from a real roster swap and tested end to end."
**[POST, template page]** WebFetch of https://x.ai/bot/HqggigM5SrZADCuJdj1te returned a public card (no login wall): "Guides you through a safe refresh of your bot roster, one phase at a time: archive and verify history, make fresh copies, carry over only active routines, and **hand off the primary role**. It never deletes anything itself, stops for your YES before every step, and offers an optional Auto mode and monthly read-only bloat check." Only the card text was readable; step internals were not exposed. New vs the post: an explicit "hand off the primary role" phase, and the bloat check is "read-only".

**[BYTES] Box (Linux)**
| Path | Size | Note |
|---|---|---|
| /home/box/agent-data/workflows/archival/SKILL.md | 3,080 B, 33 lines, sha256 c8246750… | Flow 0-5 at :24-30; hard rules :11-19 |
| /home/box/agent-data/workflows/archival/archive_guard.py | 6,305 B, 141 lines, sha256 3340ed82… | manifest :64, verify :94, confirm :100, gate :110, PROTECTED :23-29 |
| /workspace/transcripts-export/ghost_transcript.md | 426,981 B, 6,980 lines, sha256 3769dad5… | exported Oct 17 07:17 ET |
| /workspace/transcripts-export/research_transcript.md | 73,581 B, 898 lines, sha256 6bcd47fd… | exported Oct 17 07:17 ET |
| /home/box/agent-data/agents/<id>/ (7 seat dirs) | mag 2.5M · Research 12M · Ghost 162M · New Bot 228K · Archival Bot 68K · RefreshBot 100K · Grok Bot 116K (du -sh) | names from each profile.json; contents not opened |
| Ghost automations/ | `afk-game-chord` | only automation folder entry seen on disk; Research has an automations/ dir (empty listing). Enabled/disabled state NOT readable this way → Unproven |

**[BYTES] PC (DESKTOP-7C70KSC, repo C:\Users\foste\Documents\projects\local_sovereign_agent)**
| Path | Bytes | mtime | Role in a swap |
|---|---|---|---|
| mag/auto_handoff.py | 5,336 | 2026-08-10 | writes memory/handoffs/latest.md + dated copy (:28, :115-117); editable state memory/handoff_state.json (:29) |
| scripts/backup_chain.py | 13,744 | 2026-10-15 | copy → sha256 verify (:126-146) → BACKUP_COMPLETE.json (:58) → prune KEEP=7 (:55, :256-260); PINNED (:65) |
| tools/backup_brain.py | 11,585 | 2026-10-18 | read-only organ INVENTORY table (:45-70), inventory() EXISTS/MISSING + age_days (:103-116), CLI inventory/drill/report (:226-230) |
| tools/census_drift_patrol.py | 24,856 | 2026-09-29 | freshness tripwire, exit 0/1/2 (:30-32), stale-days bar, "shrink is provable drift" |
| configs/mates.yaml | 11,596 | 2026-10-17 | mate roster (:34-161), harness_probe enabled:false (:141-142) |
| configs/seat_allowlist.json | 3,969 | 2026-10-17 | signed seats; `"revoked": true` cuts a seat (:3), enforced mag/seat_handshake.py:197 |
| mag/seat_handshake.py | 14,215 | 2026-10-17 | revoked check :197 |
| watch/inbox/HYGIENE_WAVE_20261003.md | 8,830 | 2026-10-03 | precedent: "Nothing deleted, nothing rotated for real", .bak-per-edit table |
| watch/inbox/BACKUP_PRUNE_LIST_20261003.md | 12,007 | 2026-10-03 | precedent: "operator review; nothing deleted" label-list, delete operator-gated |
| Task \MagLeaveProtocolDaily | — | next 10/19 08:12 ET | daily mate wave; Status Running (not touched) |
| watch/inbox/HANDOFF_*, BOB_HANDOFF_PACKAGE_20261017.md, WAVE_HANDOFF_20260911.md, … | — | — | prose handoff precedent (seat relief by document) |

Not found where cited: tools/leave_protocol.py (see Surprise 3). Not opened by rule: .env, keys, secret_gate_results/, free_keys/, memory/trajectory/steps.jsonl.

---

## Provenance

- [POST] Roster Swap: @AdventureNLearn, 2026-10-16, Grok Bot template; "built from a real roster swap" — Unproven (no run receipt shown).
- [BYTES] archive_guard.py + SKILL.md: written by Archival Bot on the box, mtime 2026-10-18 09:25 ET (today). Built for owner mail/photos/accounts cleanup (SKILL.md:4-5), not for bot rosters — the roster use is a re-aim.
- [BYTES] backup_chain.py: biography-chain rotation, "sacred-cow fix" for gitignored memory/biography (:3-8), verified-complete + pinned rules added 2026-10-15 (:23-28).
- [BYTES] auto_handoff.py: 2026-08-10, "operator wants handoffs to happen AUTOMATICALLY" (:3), wired into afk_cadence.run_once (:11).
- [BYTES] seat_allowlist.json / mates.yaml: harness2 work 2026-10-17 (mates.yaml:132-142).
- Operator context (from task brief, not bytes): Nacho said today single-purpose bots are pointless; Ghost proposed keep Mag + one front door, retire Refresh/Research/New Bot/Archival as seats, carry role safety rules as skills.

---

## Echo check (repeated patterns = load-bearing)

| Roster Swap step [POST] | Mag / estate echo [BYTES] | Status |
|---|---|---|
| Inventory | backup_brain.py:45-116 (organ inventory, EXISTS/MISSING); archival SKILL.md:26 (inventory, [UNKNOWN] for unreadable); box agents/ dirs + profile.json names | Organ inventory EXISTS; **seat-roster inventory MISSING** as a script (done by hand above) |
| Archive full history | Transcript export = **Grok Bot app action** (ghost/research done Oct 17); archive_guard.py `manifest` :64-79 | Partial: 2 of 4 retirees exported (Ghost, Research). RefreshBot, New Bot, Archival Bot **not exported** |
| Verify archives | archive_guard.py `verify` :81-98 (sha256+size, result.json); backup_chain.py verify :126-146 | EXISTS — reuse archive_guard.py directly |
| Second copy / owner confirm | archive_guard.py `confirm` :100-108 (--second-copy, --complete); SKILL.md:14 | EXISTS |
| Fresh copies | none in Mag — creating a bot is a **Grok Bot app action** | MISSING (app-side) |
| Restore only enabled routines | none in Mag — routines are **Grok Bot app** automations; disk shows Ghost `automations/afk-game-chord` but not enabled state | MISSING (app-side); mates.yaml `enabled:` flag (:142) is the only Mag analog |
| Label old bots for owner deletion | BACKUP_PRUNE_LIST_20261003.md (label list, operator deletes); seat_allowlist `"revoked": true` (:3, enforced seat_handshake.py:197) | Pattern EXISTS; Grok Bot seats have **no allowlist row** to revoke (Surprise 2); rename is app-side |
| Hand off primary role [POST page] | auto_handoff.py :77-119 (memory/handoffs/latest.md); prose HANDOFF_* docs | EXISTS (estate side) |
| Never deletes | archival SKILL.md:12; archive_guard.py:4, :127; HYGIENE_WAVE "Nothing deleted" | EXISTS — but backup_chain.py:260 rmtree is the exception (Surprise 4) |
| Auto mode: safe steps then stop at YES | SKILL.md:22 step cards (one card open, owner approves); census_drift_patrol exit 0/1/2 | Pattern EXISTS; no one-shot "inventory→manifest→verify" runner |
| Monthly bloat check (read-only) | census_drift_patrol.py (freshness bar); backup_brain.py age_days | Pattern EXISTS; no roster-size metric |

The echo: "copy → hash-verify → owner YES → label, never delete" appears four times (archive_guard, backup_chain verify, HYGIENE_WAVE, BACKUP_PRUNE_LIST). It is the estate's law already; Roster Swap is that law applied to seats.

---

## The five bones

1. **Claims** [POST]: a clean restart "without losing anything"; never deletes; every risky step waits for YES; auto mode stops before copying; tested end to end.
2. **Proofs**: [POST] none published (page card only). [BYTES] our own proof surface is real: archive_guard writes `*.result.json` per run (:51-58); backup_chain writes BACKUP_COMPLETE.json (:58).
3. **Assumptions**: that "full history" is exportable (true for Grok Bot transcripts via app export; Mag can't do it); that routine on/off state is listable (app-side); that old bots stay usable until owner deletes (yes — labeling is non-destructive).
4. **Forbids**: deleting anything; copying before YES; restoring disabled routines. For us additionally (archival SKILL.md:15): never gating `transcript`-named files (PROTECTED regex), never touching protected categories.
5. **Costs**: $0 in tokens for archive+verify (local sha256). Real cost is operator time: one export + one YES per retiree, and re-creating any routine by hand in the app. Storage: ~177 MB of seat dirs on box (Ghost 162M dominates) — archive the exported transcripts, not the raw store.db files.

---

## The fold

**Law (L0)** — Supported already, no new law needed: "copy, hash-verify, owner YES, label, never delete" (archival SKILL.md:11-19). Add one clarification [REC]: *roster archives live outside any auto-pruned tree* (not under memory/biography_backup/, because backup_chain.py:256-260 prunes).

**Organ (L1)** [REC, not built — no code changes this run]:
- Reuse, unchanged: `archive_guard.py manifest` + `verify` + `confirm`. Do **not** use `gate` for transcripts (Surprise 1) and do not trash anything.
- Optional later (operator-gated build): a ~60-line read-only `roster_census` that lists box agents/<id>/profile.json name, du size, automations/ entries, transcript-export present/absent, and writes ROSTER_CENSUS_<date>.md. That is the missing "inventory" bone and the monthly bloat metric in one.

**Shelf (L2)** — this report; precedent HYGIENE_WAVE_20261003 + BACKUP_PRUNE_LIST_20261003.

**Canon (L3)** — Ghost's proposal (one front door + Mag; safety roles as skills) matches the template's shape. The archival skill is the first role-as-skill already on disk.

**Poetry** — "tested end to end" and "without losing anything" stay poetry until a receipt exists.

### Smallest roster swap for Nacho, now [REC]

Keep: **Grok Bot** (primary / front door) and **Mag** (estate brain, the PC repo). Ghost: either becomes the front door instead of Grok Bot, or is retired too — operator picks one front door; Ghost's 162M history must be archived either way (its transcript is already exported). Retire as seats: **Research, New Bot, Archival Bot, RefreshBot**.

Step cards (one open at a time, each ends with a YES):
0. **Preflight (read-only, safe/auto):** confirm python3 + archive_guard.py present (done today: sha256 3340ed82…); pick archive root `/workspace/roster_archive_20261018/` (not under any prune tree).
1. **Inventory (safe/auto):** table above is the inventory. [APP] Nacho or the front door lists each seat's routines with on/off state in the Grok Bot app and pastes it into `/workspace/roster_archive_20261018/ROUTINES.md`. Disk only shows Ghost `afk-game-chord`; enabled state Unproven.
2. **Archive (partly app):** [APP] export transcripts for RefreshBot, New Bot, Archival Bot (Research + Ghost already in /workspace/transcripts-export/). Copy all transcripts + ROUTINES.md + Archival Bot's skill folder into `roster_archive_20261018/src/`.
3. **Verify (safe/auto, reuses archive_guard.py):**
   `python3 /home/box/agent-data/workflows/archival/archive_guard.py manifest roster_archive_20261018/src roster_archive_20261018/src.manifest.json`
   copy `src/` to a second location (e.g. PC `watch\LIBRARY\ROSTER_ARCHIVE_20261018\` via CopyFromBox, or Google Drive), then
   `python3 …/archive_guard.py verify roster_archive_20261018/src.manifest.json <copy>` → expect PASS, recount files by hand to match `count`.
   Then `confirm … --second-copy "<where>" --complete` after Nacho confirms in writing. **STOP — auto mode ends here, wait for YES.**
4. **Fresh copy / fold (YES required, app):** no new bots needed under Ghost's plan — instead install role rules as skills on the front door (archival skill already exists at /home/box/agent-data/workflows/archival/; add "research" / "refresh" skills only if their transcripts show rules worth keeping).
5. **Restore only enabled routines (YES required, app):** re-create on the front door only the routines marked ON in ROUTINES.md. Leave everything else off.
6. **Label (YES required, app):** rename each retiree "RETIRED-20261018 — archived, owner deletes" and stop its routines. Nacho deletes them himself whenever he likes. No Mag allowlist edit is needed (they have no rows; Surprise 2).
7. **Handoff:** front door writes a handoff note; on the Mag side `memory/handoff_state.json` CONTEXT can record "roster consolidated 2026-10-18" for auto_handoff.py to carry (operator-gated edit, not done here).

### Monthly bloat check — routine or not? [REC]

Yes, as a **Grok Bot routine on the front door**, monthly, **read-only**: count seats, du of each agents/<id>/, automations entries, last-activity, flag any seat > N MB or idle > 30 days, write one ROSTER_CENSUS_<date>.md, and *post nothing / change nothing*. Not a Mag Windows scheduled task: the data lives on the box and in the app, and Mag already runs a daily wave (MagLeaveProtocolDaily) whose launcher path is itself drifting (Surprise 3). One extra monthly box routine is cheaper than another PC task. Model it on census_drift_patrol's exit contract (0 inside bar / 1 bloated / 2 cannot verify).

---

## Receipt

- Artifact: watch/LIBRARY/STEAL_ROSTER_SWAP_20261018.md (this file) + one line in watch/LIBRARY/INDEX.md.
- Room receipt: Roster Swap = YES-gated archive→verify→fold→label recipe; Mag already has verify/never-delete/handoff/inventory organs; gaps are app-side (export, routines, rename) + no seat-roster census; swap = keep Grok Bot + Mag, retire Research/New Bot/Archival/Refresh after archive_guard manifest+verify, never gate.
- Tri-state: Mag organs cited = Supported (bytes, today). Template internals beyond the public card = Unproven. Enabled-routine state per seat = Unproven (app-side). Ghost-vs-Grok Bot front door = operator decision.
- Forbids: trashing or deleting any seat history; using archive_guard `gate` on transcripts; storing roster archives under memory/biography_backup/.
- Paid rent on: archive_guard.py (reused unchanged for verify) and the PROTECTED-regex catch.
- Falsifiable by: an archive_guard `verify` FAIL on the roster archive; a seat row for any Grok Bot seat appearing in configs/seat_allowlist.json; tools/leave_protocol.py existing at another path the scheduled task actually runs.
- Cost: $0. No git, no code changes, no paid calls, no secrets opened, no process touched.
