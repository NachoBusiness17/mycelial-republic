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
| 12 | memweave | DEMOTE | Organ and distributor exist (mag/memweave.py, mag/mem_weave_distributor.py) but the card's own falsifier (structure must beat prose at equal tokens) has never been run (f-21 Table 3: 0 organic rows). Demote action: run the falsifier once or mark untested. |
| 13 | memlance | DEMOTE | Organ + test exist (mag/ghost_memlance.py, tests/test_memlance_wave.py); the 2-of-5-lances-land falsifier has never fired (f-21). Demote action: the 5-lance experiment is one evening; run it or keep dormant knowingly. |
| 14 | retrocausal-steering | DEMOTE | Invoked once, day of forge (09-18T18:12; f-21); steering-fold receipts real (corpus/steal/STEERING_FOLD_DELTA_20260926.md). Demote action: keep as doctrine-at-rest; its witness-or-it-failed clause is already absorbed into lane discipline. |
| 15 | corpus-harvest | DEMOTE | The harvest protocol moved to the olm-mine saved workflow (daily 10:00 cron, commit 6a1c70ec9). Post-census fix byte-checked: the card NOW has YAML frontmatter (head -5 this session) - the invisible-file class f-02 flagged was found and fixed in the 09-29 lint wave (f02fc2c33). Demote action: point the card at the saved workflow as its engine. |
| 16 | code-agent-data | KILL (rebuildable, see section 2) | The clearest corpse: its own text admits "mining lapsed since Aug and the corpus starved" (f-02 quotes SKILL.md lines 16-17); memory/train_data/ held exactly one file from Aug 18 at census. But the wave record proves the function works (section 2), so this is a rebuild, not a burial. |
| 17 | elder-lens | KILL (salvage window open, see section 2) | Its own falsifier: "a lens is dead if no organ acts on its question within one week". queue/lanes/elder/inbox.jsonl is 0 bytes today, mtime Sep 4, 12 days dark (byte-checked this session). The day-close lens procedure was re-invented 09-30 as the 48h-synthesis lanes (STORY.md / laws.md / measure.md pattern, commit 600b09c4b). Salvage: bank one lens from 48h-synthesis/STORY.md into the elder inbox before ~10-02 and the card resurrects by its own terms. |
| 18 | show-me | KILL | Pure prompt doctrine (its own design, SKILL.md line 9), zero repo-side trace since its 09-03 creation receipt (room.jsonl:5341; f-02). Honest note: no wave runs show-me's function implicitly at any proven scale, so this is NOT a dead-but-buildable case; no wave proof exists, so no build spec is offered. Kill the card; if the operator ever wants the ladder back, the salvage is one paragraph in the agent-harness card. |

Score: 5 PROMOTE / 10 DEMOTE / 3 KILL (one of the kills is kill-and-rebuild,
one carries a salvage window).

## 2. Dead-but-buildable: wave proof + one-sitting build spec

Three of the four dead or door-dead cards have wave proof that their function
works when run as a partition protocol. The fourth (show-me) does not, and is
killed honestly.

### 2.1 code-agent-data (KILL the card, REBUILD from wave proof)

- Wave proof: mirror-mine (mirror-mine.dwf.ts, launched commit 671ed733c
  09-28, "25 gophers mining the operator's corpus (oral history, X-kg, session
  logs, estate architecture, research frontier, driving ladder, behavior
  cards)") plus ladder-02 (flash50/ladder-02.md:73: "designed and launched
  Sovereign Mirror Mine, 25 gophers, announced 19:27:17") plus the session-tape
  instrument work in ladder-02 ("mined from harness session store db.sqlite
  message+part join"). Per-tape gophers mining sessions into decision-pattern
  tables is proven working at 25-wide.
- One-sitting build spec: rewrite the card around the proven shape. Items =
  session tapes (one gopher per tape, named agent per item); per-item output =
  a corpus-grade table (the old card's 600-byte + Result-section substance
  floor survives); destination = training/ beside the live events.jsonl
  firehose (VC1 census: training/events.jsonl 197MB live at 09-16) instead of
  the dead memory/train_data/; laws preamble copied verbatim from
  mirror-mine.dwf.ts (every quote cites file and line, OWED if unread, no
  em-dashes). Land as: SKILL.md + saved workflow draft in one sitting; the
  mirror-mine script is the template with ITEMS swapped to tape paths.
- Falsifier for the rebuild: if two consecutive weekly runs bank fewer than 10
  corpus-grade tables, the function does not survive contact and the card dies
  for good.

### 2.2 elder-lens (KILL the card now, salvage window open)

- Wave proof: the 48h-synthesis gala (6/6 lanes division B, GATE PASS, 20 byte
  checks cited; 48h-synthesis_RECEIPT.md, moment 2026-09-30T22:48:05Z) ran
  exactly the elder-lens procedure as lanes: read the day's banked artifacts,
  find the one emergent pattern, name real anchors only, end with the question
  the fleet is not asking (STORY.md / laws.md / measure.md / lattice.md,
  commit 600b09c4b). The function is proven; the card's own delivery organ
  (queue/lanes/elder/) is dark.
- One-sitting build spec: resurrect by its own falsifier - bank ONE lens into
  queue/lanes/elder/inbox.jsonl distilled from 48h-synthesis/STORY.md (the
  synthesis already found the pattern; the lens is a 20-minute write), then
  rewrite the card's intake line to accept gala synthesis outputs as lens
  input. If no lens lands by the falsifier clock (~10-02), the kill stands and
  the card comes off the shelf.

### 2.3 salon Door B (DEMOTE the card, the door is the dead part)

- Wave proof: ractor_panel_20260926.dwf.ts ran the 7-shape persona panel as a
  saved workflow (the shape-train salon protocol, workflow-native), and the
  gate's scenario suite now re-proves such shapes against registry FAIL rows.
  Door B (write one JSON to watch/salon_inbox/) has fired once ever.
- One-sitting build spec: delete Door B from the card and replace with one
  line pointing at the saved workflow launcher; OR wire a daily runner that
  drains watch/salon_inbox/ the way the burn crons drain their queues. Pick
  one; the current state (door nobody reads + runner host-side) is the
  write-only pattern the Mickey17 09-29 wave named as the estate's disease.

## 3. The wave-invented protocols that worked: one-sitting card specs

Five protocols, each byte-proven by a workflow draft on disk plus a receipt or
commit. Each gets a one-sitting card spec. Two more (frontier-mine,
ractor-essay) already landed as cards on 09-29 and are cited as the proof the
conversion path works.

### 3.1 Gala divisions (the protocol this lane is running right now)

- Proof: Ractor-50-wave-retro.dwf.ts (divisions A/B/C on one ballroom; typed
  GalaLaneOut at line 46; lane JSON + check.txt per lane, incremental writes,
  division B deadline-first, lines 93-178). Receipts: AFTERPARTY_CLOSE_20260926.md
  ("GALA: 36/36 lanes danced, 36 LINKS rows, ~38M witnessed agent tokens,
  widths 3-6-12 clean" and "AFTERPARTY: 94 lane JSONs banked"); 48h-synthesis
  rerun 09-30: "lanes_parsed_ok: 6/6", "all six lanes division B", 20 byte
  checks cited.
- One-sitting card spec ("gala-lanes"): WHEN an operator order needs many
  independent verdicts on one estate question. SHAPE: one slug, one lanes/
  dir, per-lane ask carrying the lane head (lane id, division, archive path,
  finish line, decision ledger); division A mines rows, division B byte-checks,
  C builds. LAWS carried in every ask: write the lane JSON incrementally
  (Write tool, not heredocs), the verdict is the exit code not your opinion,
  no fabrication, no em-dashes. FOLD: parse all lane JSONs, gate on
  parsed-ok/all-expected, publish one receipt + per-lane rows. Cost note:
  36 lanes ~38M witnessed tokens is the measured amplitude (widths 3-6-12
  clean, envelope per AFTERPARTY B2-476).

### 3.2 Mickey17 partition (per-item named expendable gophers)

- Proof: mickey17-wave3.dwf.ts system line (verbatim): "You are EXPENDABLE but
  your work product is NOT. Execute your item with full effort, bank it,
  commit it, and die." Lineage: mickey17-v2 gate-fixed 7/7 (3752abae2,
  09-25) -> wave3 at full width with flash50+wide37 (1c19f26f4, 09-28) ->
  24-wide edge-mining wave, 20 returns at synthesis (bd41b4062, 09-29) ->
  wave complete 25/26 returns with the critical find (default pytest
  entrypoint broken, db6f2b5f6, 09-29). Codified as gate G1
  (tools/workflow_gate.py:46-48).
- One-sitting card spec ("gopher-partition"): WHEN one ask decomposes into N
  independent items each writable in one sitting. SHAPE: agent("x-" + item.id)
  per item; system preamble carries the expendable line + git hygiene (git add
  only your files, commit with your item id prefix); every item banks a file
  and a report() row so a dead run keeps its banked items (gate G4). FOLD:
  ledger of ok/stuck + chars, refire stragglers once, then fold again. The
  25/26-returns return rate is the measured expectation.

### 3.3 Firehose census (30 census gophers, the item bank)

- Proof: firehose.dwf.ts ITEMS f-01..f-30 (f-02 and f-21 are the skill
  censuses this very lane starts from; their outputs
  flash50/skill-liveness.md + flash50/skill-census.md are byte-present; the
  census scripts landed in bulk commit 58c1b0755 (git show file list run this
  session) and sibling bulk commit 74a4d9cd2 landed the f-06 outputs
  byte-identical, message "flash50+wide37+firehose+deep-mining+mickey17: bulk
  commit all concurrent gopher outputs", quoted from f-06.md line 67). Launch
  receipt: 671ed733c "firehose 30 census live, firehose2 24 census live". Follow-on value proven: f-06
  found 2 FALSE count>100 invariants and 3 split/stale ones.
- One-sitting card spec ("estate-firehose"): extract the ITEMS array (30
  census asks) from the draft into configs/firehose_items.json; the card
  points at it and carries the census discipline (read the actual files, count
  the real things, produce real numbers; bank a dated .md per item; name
  instrument + moment + delta on every count). Refresh law: each item's banked
  file carries its census date so the next firehose diffs drift, the same
  carrier law AGENTS.md enforces on the test census bullet.

### 3.4 Mirror mine (25-gopher self-steal over the operator's corpus)

- Proof: mirror-mine.dwf.ts (LAWS preamble verbatim: "Every quote must cite
  file and line. If you couldn't read the source, say OWED."; items span oral
  history transcripts, X-kg, state/CURRENT.md, AGENTS.md law-lineage, rib
  cards). Launch: 671ed733c. Its OWN audit closed the loop on governance:
  ladder-02.md:73 documents the FUNDING-STATEMENT violation (the 100M pack
  spend never updated the driving ladder) - the mine audited the estate's
  spend epistemics and produced a law (spend must re-anchor the ladder the
  same hour).
- One-sitting card spec ("mirror-mine"): per-source asks over the operator
  corpus with the mirror-mine LAWS preamble verbatim; output = decision-pattern
  tables + law-lineage tables; the card carries the audit law the run itself
  produced (any spend the run makes updates RIB_DRIVING_LADDER the same hour,
  else the run is OWED a funding statement). Template = mirror-mine.dwf.ts
  with ITEMS swapped per mine target.

### 3.5 Stealth-wide fetch-verify (free-lane wide fetch, funded verify)

- Proof: stealth-wide.dwf.ts (16 topics in 4 batches of 4; per-gopher pattern:
  "use the existing tools/stealth_fanout.py free-lane dispatch pattern";
  tools/stealth_fanout.py exists, byte-checked). First-contact rates measured:
  commit 1ea76d869 (09-27) "12 mining items x 10 steal-model lanes concurrent
  (Mickey17); 2/12 ok on first contact (muse-glimmer-30b + ling-flash-vl
  delivered real content...); SSRF boundary enforced in fanout (allowlist +
  public-IP)". The verify half is the standing law: AGENTS.md driving ladder,
  "Free stealth lanes are a SENSING surface only - their outputs are banked as
  findings, never as done/trusted work; verification climbs to the funded
  tier."
- One-sitting card spec ("stealth-fetch-verify"): batches of 4 concurrent
  free-lane fetches; per-result accounting is mandatory (id, ok, chars -
  delivery rate is the measured number, expect ~2/12 on first contact,
  spaced retries per the pool law); SSRF allowlist + public-IP boundary
  carried in every gopher preamble; fold publishes a ledger marking every row
  finding-not-done-work and names which rows climbed to the funded tier for
  verification. The card's falsifier: if funded-tier verification ever
  confirms less than half of what free lanes deliver as "real content", the
  sensing-only law gets teeth or the lane gets cut.

## 4. The conversion path, already proven twice

- frontier-mine (6a1c70ec9, 09-29): engine saved as named workflow olm-mine
  (gated, PASS digest), daily cron automation-cac38363 10:00, SKILL.md carries
  the ritual (fire/fold/bank), the failure law (amend-don't-rewrite), and the
  cadence law ("research intake without cadence dies silently"). The template
  every section-3 spec should copy: workflow + cron + card + failure law, one
  sitting.
- ractor-essay (f02fc2c33, 09-29): "ractor-essay skill formalized from
  Q-operation run" - a pipeline that ran once as an ask got formalized into a
  card the same day it worked.
- Plus the B1 skills.yaml registration (19 repo skills now loadable through
  the mag skill system): the loader surface moved toward the cards, not just
  the cards toward the waves.

## 5. Decision ledger

This dance closes the skills question the f-02/f-21 census left open: the
census said 1 of 18 ACTIVE and asked for triage; this lane converts that into
per-skill verdicts (5 promote / 10 demote / 3 kill), names the wave-to-card
path as the proven revival mechanism (2 conversions landed 09-29), and hands
the operator three concrete one-sitting builds (code-agent-data rebuild,
elder-lens salvage lens, estate-firehose item bank) plus two already-specd
protocols to cardify next (gala-lanes, gopher-partition). Decision changed:
the default treatment of the skills layer flips from "dormant doctrine,
ignore" to "waves are the fuzzer; cards are the commits" - promote by
conversion, not by invocation counts alone.

## 6. Instrument receipt (commands run this session, 2026-09-30)

- ls .agents/skills/ (20 dirs); wc -c over the 20 SKILL.md = 65,826 total.
- Read (full): watch/inbox/burn_reset_20260927/flash50/skill-census.md (f-21
  mirror) and skill-liveness.md (f-02 mirror).
- Searches: grep -ril mickey17 / firehose / mirror mine / stealth-wide /
  fetch-verify across watch/inbox and corpus/steal; git log --all
  --format="%h %ad %s" --date=short --grep="mickey" -i (8 rows); git log
  --diff-filter=A per new skill; git cat-file -t 328896fcb (invalid object:
  the hash AGENTS.md cites for MICKEY17 is not resolvable in this repo's
  object store; the wave lineage above uses the commits that DO resolve).
- git show 74a4d9cd2 --stat (message line only; outputs via f-06 addendum);
  git show 58c1b0755 --name-only (census scripts listed); git log -1
  --format=%B 671ed733c; git show --stat=150 328896fcb (empty, invalid).
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
