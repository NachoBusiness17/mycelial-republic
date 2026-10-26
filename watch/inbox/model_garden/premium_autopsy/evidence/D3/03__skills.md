# RACTOR50 LANE: skills - SKILL-USE RETRO (division B, 2026-09-30)

Lane: skills (division B) of the ractor50 wave retro. Archive:
`watch/inbox/gala_20260925/ractor50/lanes/skills.json`. Check output:
`watch/inbox/gala_20260925/ractor50/lanes/skills.check.txt`.

Scope: the estate's 18 census skills (f-02/f-21, 2026-09-28) get a live-loop
verdict each (promote / demote / kill); the wave-invented protocols that
PROVABLY worked get named and specified as one-sitting SKILL.md cards or saved
workflows; every dead-but-buildable skill gets wave proof plus a one-sitting
build spec.

Instruments used this session (all commands logged in the instrument receipt
at the bottom): the two flash50 censuses read in full, the five wave workflow
drafts read, git log/show on the wave commits, steps.jsonl post-census scan,
existence checks on engines and loaders. Nothing under mag/ or tools/ was
modified by this lane.

## 0. Census drift first (name instrument, moment, delta)

f-02/f-21 counted 18 SKILL.md files, 56,713 bytes on 2026-09-28. Today
(2026-09-30) `wc -c .agents/skills/*/SKILL.md` = 65,826 bytes over 20 files.
Delta: +2 skills, +9,112 bytes in the two new cards (frontier-mine 2,398 B;
ractor-essay 6,574 B), +141 bytes across the old 18 (unattributed micro-drift,
below one commit of noise; not investigated further, named honestly). Both
arrivals landed 2026-09-29 and both are wave protocols converted to cards
(frontier-mine: commit 6a1c70ec9 "OLM MINE becomes a daily burn + a skill";
ractor-essay: commit f02fc2c33 "ractor-essay skill formalized from Q-operation
run"). The headline of this retro is therefore already half-proven by the
estate itself: the wave-to-card path works and has run twice since the census.

Second drift: f-02's "two disjoint skill stacks" finding (configs/skills.yaml
touches 0 of the 18) is now stale. Commit f02fc2c33 (09-29) registered the
repo skills into configs/skills.yaml (B1-era registration); byte-check today:
`grep -o ".agents/skills/[a-z-]*" configs/skills.yaml | sort -u` = 19 repo
skills (all except the newest, frontier-mine); 35 `id:` rows total. The
dormant layer gained a real loader surface two days ago.

## 1. Live-loop verdicts: the 18 census skills

Verdict ladder: PROMOTE = give the skill work or teeth this week; DEMOTE =
keep, strip investment, function may live elsewhere; KILL = delete or freeze
the card. Evidence line cites the strongest byte I hold.

| # | skill | verdict | evidence (byte-cited) |
|---|---|---|---|
| 1 | operator-corrections | PROMOTE | The only wired skill: mag/chord.py:66 probes it, mag/invariant.py:197-200 hashes it into instruction_sha, scripts/lattice_render.py:26 parses its laws, scripts/build_fleet_imprint.py:264 reads it, 2 boot docs mandate it (f-02 + f-21). Seats extended it 3 times (laws 17-20). Promote condition: chord strike has zero recorded runs and cite_gate_latest.json is frozen at Sep 7; arm one of the two onto cadence and ACTIVE becomes current, not historical. |
| 2 | chan | PROMOTE | Engine and test alive today (mag/chan.py, tests/test_chan.py exist, byte-checked this session); the only user-invocable card (17 lines); registered in skills.yaml B1 wave. Promote action: none needed beyond keeping it the user door. |
| 3 | agent-harness | PROMOTE | Its doctrine (intake rubric, tri-state claims, claim-contention lock, receipt-at-bytes) is what every gala lane ask already runs: this run's own script (Ractor-50-wave-retro.dwf.ts:149-160) embeds byte-check + verdict-is-exit-code + no-fabrication laws per ask. Promote action: make the card the ask-template source the gate's G7 points at, instead of each script re-embedding the laws. |
| 4 | mesh-comms | PROMOTE | Channels in daily use (room.jsonl typed rows 13,865 lines at census; rib_bus live); its pass-off protocol is codified as gate G2 (tools/workflow_gate.py:51-53). Promote action: cross-link card and gate so the law cites the card and the card cites the gate. |
| 5 | zai-reference | PROMOTE | The funded-lane reference: AGENTS.md driving ladder routes judgment to z.ai lanes daily; 12 verbatim section files real (f-21 Table 1). Promote action: name it in the dispatch-seat boot line so dispatches carry the errors/economics sections. |
| 6 | salon | DEMOTE | Engine alive (mag/salon_50.py, mag/frontier_salon.py, tests/test_frontier_salon.py) but Door B fired exactly once ever (watch/salon_inbox/ holds 1 intake, corpus_map_mcp_20260918.json, no in-repo consumer; f-21 finding 4). The shape-train protocol it encoded lives on as saved workflows (ractor_panel_20260926.dwf.ts). Demote action: kill Door B or wire the runner to a daily item; do not invest in the door. |
| 7 | fireball-cycle | DEMOTE | Engine live (mag/water_computer.py in current working tree, tests/test_water_computer.py) but the card has one 09-09 path mention and zero reads (f-21 Table 3). Demote action: leave dormant; if the game platform (basecamp f02fc2c33) ships the Mountain slice, tie the card into its boot docs then. |
| 8 | frontier-researcher | DEMOTE | The percolator loop it documents runs without it (invariants.json 109,231 B + explore.jsonl fresh at census; f-02). The firehose even ran the loop's truth-audit step as census item f-06 (13 invariants audited, 2 FALSE fossils found). Demote action: the loop's doc layer belongs in the percolator's own README, not a skill card. |
| 9 | frontier-hr | DEMOTE | Zero invocation of any kind ever (0 STEPS, 0 REASON rows; f-21 Table 3); data shelf real (MEGA_DIGEST_SKILLS_DEMAND_20260904.md + FRONTIER_MAP_DEEPSEEK_20260904.md); operator_board ADVISORS surface exists. Demote action: one scheduled ask per quarter or remove the summons; the shelf stays either way. |
| 10 | light-operator | DEMOTE | CANDIDATE doctrine with its own promotion gate unmet (held-out reproduction marked "Not yet run", SKILL.md:26-29; f-02). Demote action: run the held-out reproduction or freeze as CANDIDATE with a date. |
| 11 | verb-genomes | DEMOTE | 12-line index into real docs (docs/ref/verb_genomes/ verified); cited only inside the agent-harness card (f-02). Demote action: fold the index line into agent-harness and delete the standalone card, or leave as-is; no loop exists. |
| 12 | memweave | DEMOTE | Organ and distributor exist (mag/memweave.py, mag/mem_weave_distributor.py) but
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 6300 + tail 2100 of 23182 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
empty, invalid).
- Read: .zcode/workflow-drafts/firehose.dwf.ts (ITEMS f-01..f-30 read),
  mickey17-wave3.dwf.ts, mirror-mine.dwf.ts, stealth-wide.dwf.ts (both
  halves), Ractor-50-wave-retro.dwf.ts (grep for division/GalaLaneOut/check
  lines), flash50/f-06.md, flash50/ladder-02.md (mirror-mine + funding
  statement rows), wave_20260916/receipts/VC1_FULL_CENSUS.md (firehose =
  training/events.jsonl context), burn_reset_20260927/mirror_intro.md
  (disambiguation: a different "mirror"), gala_20260925/AFTERPARTY_CLOSE_20260926.md
  (headline + B2-25/B2-97/B2-476 amendments), gala_20260925/48h-synthesis_RECEIPT.md
  (header + scoreboard).
- Liveness deltas: ls -la queue/lanes/elder/inbox.jsonl (0 bytes, mtime Sep 4);
  grep struck_by over memory/attention.md memory/rib queue state
  watch/room.jsonl (zero non-empty hits); ls -la state/cite_gate_latest.json
  (mtime Sep 7 03:17); head -5 .agents/skills/corpus-harvest/SKILL.md
  (frontmatter NOW present, post-census fix); ls of mag/chan.py,
  tests/test_chan.py, mag/water_computer.py, tests/test_water_computer.py,
  mag/memweave.py, mag/ghost_memlance.py, tools/stealth_fanout.py (all
  present).
- steps.jsonl scan (.venv/Scripts/python.exe, venv per seat law - a bare
  python attempt was blocked by the AGENTS.md python-env seat law and rerun
  with the venv): 131 all-time rows contain .agents/skills paths; post-census
  window (ts >= 2026-09-28T20) sampled per row: most are bulk greps, census
  faces, and this session's own commands; genuine signal rows: ractor-essay
  git-add by its forging session sess_c6ad00b4 (09-29), frontier-mine git-add
  by sess_bb9913b3 (09-30 03:10), one real workflow read of the frontier-mine
  card's cadence section (sess_dwf-dwfrun-3a094ea8, 09-30 21:59).
- grep -o ".agents/skills/[a-z-]*" configs/skills.yaml | sort -u = 19 repo
  skills; grep -c "id:" configs/skills.yaml = 35.
- Not run: the 5-file engine pytest suite (f-21 ran it 09-28; re-running was
  out of scope for a verdict lane and is named as not run); the violation
  ratchet (no code under mag/ or tools/ touched by this lane).
