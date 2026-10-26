# OPERATOR WORKFLOW DIVE 2026-10-03 (self-steal on how Nacho works, not on code)

Read-only dive by Grok Bot at Sat 10/3 ~19:00 ET. Only this file was written.
Method: ZCode sessions db opened read-only (`C:\Users\foste\.zcode\cli\db\db.sqlite`, mode=ro), plus git, ledgers, inbox, residuals, scheduled tasks, ZCode MEMORY.
Scope: 152 top-level sessions since 9/1, of which 90 have >=5 messages. "Human prompts" means user text with templated cron prompts removed (same 40-char prefix seen >=8 times and longer than 150 chars). That leaves 4,727 human prompts.
Caveats up front: laptop (bob), phone, and Grok-app activity are not in this db. Inbox "Read" counts only include the ZCode Read tool (cat/rg reads are invisible). Git history visible since 9/1 starts on 9/8, after the 9/30 rewrite.

## Headline numbers

| Meter | Value | Receipt |
|---|---|---|
| Human prompts, 9/1 to 10/3 | 4,727 across 90 sessions | db.sqlite message+part, role=user |
| Human prompts per week | 1,523 / 1,053 / 851 / 840 / 460 (W1..W5) | same |
| Delegated child sessions per human prompt | 0.32 (W1) to 3.75 (W5) | session.task_type subagent_child+workflow_child by day |
| Prompts containing "self steal" | 469 (9.9%), on 32 of 32 days, 70 sessions | same |
| "self steal" rate per 1000 prompts | 91 / 92 / 130 / 89 / 102: not falling | same |
| "Forgot / we already have / remember" prompts | 219, on 32 of 32 days | same |
| Sessions that open with boot / recap / catch-up | 34 of 90 (38%) | first human prompt per session |
| ZCode sessions with a residual dossier | 0 of 152 | memory/biography/residual/*.json (4,020 files; sources mag_agent 3,027, grok 963) |
| Distinct open_loops strings in 4,020 dossiers | 5 (boilerplate) | same |
| Inbox entries since 9/1 later re-Read by an interactive seat | 20 of 1,461 (1.4%) | watch/inbox mtimes vs db Read tool calls |
| Scheduled tasks red right now | 8 | Get-ScheduledTask LastTaskResult, 10/3 19:05 ET |
| attention.md lines that are doubled_key alarms | 888 of 1,150 (77%) | memory/attention.md |
| Hermes paid spend | $37.76 (10/1), $1.17 (10/2), $25.62 (10/3) | memory/runs/hermes_burn/usage.jsonl, 1,275 rows |
| Re-fire excess share | 67.6% (10/1), 34.8% (10/2), 58.5% (10/3) | same, duplicate non-zero (id,turn) after first |
| Excess on 10/3 from TAVERN/DND key collisions | $15.00 of $15.00 | same, by id prefix |
| dwf workflow runs failed or cancelled | 54 of 134 (40%) | db.sqlite dwf_run |

## 1) Where his time goes

- **Hours.** Human prompts by ET hour peak at 18:00 to 21:00 (297, 305, 313, 285) and 08:00 to 09:00 (273, 275). 00:00 to 05:00 holds 6.8% (322 prompts). Source: db.sqlite, 4,727 human prompts.
- **Span.** The median day has prompts in 18 distinct hours. 10/2 (9) and 10/3 (12, still running) are the only days under 13.
- **Rest window.** The median longest prompt-free gap per night is 5.5h. 15 of 32 nights were under 5h, and 5 were 7h or more (9/7, 9/10, 9/28, 9/30, 10/2). These are desktop-ZCode prompts only, so this is an upper bound on how busy he was.
- **In his words (tentative, material only because it ties to the context-loss loop):** "i sleep like 3 hours a night because i'm so excited" (9/5 16:41). "tired" or "exhaust" shows up in 34 prompts over 20 days, and the costly ones are about re-explaining: "i'm so tired of evertyhing forgetting all the time" (9/17 12:09) and "its exhausting that you forget all this shit we had a mud surface" (9/23 04:04). He has also said "stop telling me to sleep" 4 times on 3 days. So the fix is to make the estate need less of him, not to nag him.
- **Session shape.** The 90 sessions are long-lived: median wall span 13.8h, p90 180h, median 324 messages and 30 human prompts. Interactive sessions per day fell from 60 (9/3) to about 1 to 2 by late September. He now runs one long seat per day and fans out from it.
- **Burst vs steady.** Commits are bursty: 143 on 9/28 and 2 to 3 a day on 9/20 to 9/23 (git log, 647 commits since 9/1). Prompting is steady but shrinking. Delegation is the steady load: 200 to 400 child sessions most days since 9/25.
- **Drops.** 731 human prompts (15.5%) carry an x.com link, falling from 169 to 70 per 1000 prompts between W1 and W5. That is a big intake stream, and it interrupts the build seat.
- **Short orders.** 649 prompts (13.7%) are 20 characters or fewer: "next" 55, "self steal" 34, "go" 31, "continue" 16, "now what" 12.

## 2) Repeat loops (top 10, counted from human prompts)

| # | Loop | Count | Days | Trend per 1000 (W1 to W5) |
|---|---|---|---|---|
| 1 | Has to say "self steal" | 469 | 32 | 91 to 102 (flat) |
| 2 | "You forgot / we already have it / remember" | 219 | 32 | flat |
| 3 | Keep going / why stop / go wide / N wide | 161 | 29 | 3.9 to 76.1 (rising) |
| 4 | Bare "next / go / continue / now what / resume" | 146 | 29 | 20 to 30 |
| 5 | Boot / recap / catch-up / where are we | 90 (34 session openers) | 21+ | 18 to 20 (U-shape, back up in W5) |
| 6 | Wire don't build / bloat / lessig / ponytail | 85 | 23 | 32.8 to 6.5 (falling) |
| 7 | English / ELI5 / I don't understand | 65 | 23 | 23.5 (W3) to 2.2 (falling) |
| 8 | Don't believe / prove it / fabricated | 49 | 25 | 11 to 15 |
| 9 | Headless / windows popping | 28 | 14 | 0 in W2-W3, then 17.9 and 13.0 (relapse) |
| 10 | Em-dash / AI slop | 10 | 8 | 0 in W5 (gate works) |

**Laws hit most, inferred from the loops:** law 1 CONSULT FIRST / self-steal (loops 1, 2, 6), keep-the-machine-fed and width discipline (loops 3, 4), the headless-only law (loop 9, back in W4), and NEVER CLAIM FIRST (loop 8).
**Gap:** violations are not metered. tools/seat_law_gate.py writes no block log (rg found no log, jsonl, or append path). .agents/skills/operator-corrections/SKILL.md holds 20 laws, the last dated 9/11, and the file was last written 9/29 11:51. Meanwhile ZCode MEMORY.md (636 lines, 201,581 bytes) uses the word "law" 237 times and records "38 law rows" on 10/2. Most newer laws never made it into the compiled skill that cheap seats load.
**Commit message vs content:** add33ba72 (10/3 16:42) is titled "DD-SELFSTEAL BIG ONE" but deletes memory/tls/lan.key and adds 22 .gitignore lines, neither of which the message mentions. 2678d88ee ("Identity hygiene", 9/30) deletes watch/inbox/INDEX.json and index_events.jsonl. a331069c7 ("AG-wave close-out", 9/30) deletes the memory/seals/2026-08-24..09-06 snapshot trees. Separately, fix-class commit share went 23% (W3), 32% (W4), 35% (W5), with 193 of 647 commits matching fix|errata|revert|correct|repair|amend.

## 3) Open-loop debt

- **Red patrols (no action logged):**
  - MagTipWitnessDaily: exit 2 on 4 of 4 runs since 9/30 19:19. The cause is a token missing gist scope (logs/tip_witness.log), so the fix is operator-gated.
  - MagXRadarDaily: exit 2 on 4 of 4 runs since 9/30 08:00. The log says "missing grok CLI at C:\Users\foste\.grok\bin\grok" (logs/x_radar.log).
  - MagCensusPatrolDaily: exit 1 on 7 of 9 runs since 9/26 (logs/census_patrol.log).
  - MagGapSentinelDaily: exit 1 on 3 of 5 runs. On 10/3 08:15 it reported local_sovereign_agent growing 29.52 GiB/day, plus x_radar.json dark for 2.7 days (logs/gap_sentinel.log).
  - Also red today: Estate KeyAudit 0x1, Estate Ratchet 0x1 (seal=1 on 5 of 6 days, logs/ratchet_daily.log), MagLeaveProtocolDaily 0x1, Estate Spine Index 0xC000013A (killed).
  - The alarm channel is drowned: 888 of 1,150 attention.md lines are doubled_key.
- **Owed items:**
  - queue/todo.md was last written 9/29 06:53. It has 11 open boxes and does not hold this week's owed list.
  - The real owed list lives in day-plan-hermes-burn-20261003.md "STILL OWED": morning three, the $50 matrix before the 10-05 wall, vast.ai, book bytes from bob, CATHEDRAL smoke 10-04, and the WBN hunt.
  - Ages (by mtime of the memory files that mention them): CATHEDRAL appears in 14 memory files dated 9/18 to 10/3. "same-disk backup" and "second machine join" first show up in the 9/27 preparedness audit and are still carried in files dated 10/3, so 6+ days. vast.ai appears in 8 files dated 9/26 to 10/3.
- **Receipts not re-read:** 1,461 inbox entries were modified since 9/1. 65% got at least one Read from any agent, and those are mostly the writer re-reading or a fold lane. Only 101 (6.9%) were ever Read by an interactive seat, and 20 (1.4%) on a later day. Of the 601 entries since 9/26, 480 were never Read on a later day. "Referenced" is not a useful meter: 1,353 of 1,363 top-level files are cited somewhere outside the inbox, mostly by indexes and ledgers.
- **Index rot:** MEMORY.md has 589 links but 562 unique (27 duplicates), and 97 of 658 memory files are not indexed.

## 4) Spend efficiency

- The A1 re-fire class (a seat re-burning the same ask) is closed. On 10/3, every id class except TAVERN and DND shows $0.00 excess.
- 10/3 still shows 58.5% "excess" ($15.00 of $25.62). All of it is TAVERN ($14.33) and DND ($0.67) ids. Per watch/inbox/ractor_engine/2026-10-03-surface-migration/break-economics.md:103, tools/tavern.py:157 builds `TAVERN_r<rnd>_<actor>` with no run stamp, so every new brawl collides with older keys. It is real play spend that the ledger can't tell apart from waste. It also fires the doubled_key alarm on 687 paid rows ($15.34), which floods attention.md.
- Play share: TAVERN was $16.20 of the $25.62 spent on 10/3 (63%).
- Cost per landed outcome is not measurable cleanly, because the ledger has no "landed" field. The proxy is $ per unique paid key: $0.55 (10/1) and $0.20 (10/3). 10/3 had 233 failed rows out of 1,034.
- Workflow waste: dwf_run since 9/1 shows week 38 at 35 of 75 failed or cancelled (459M tokens) and week 39 at 19 of 58 so far (594M tokens). Failure codes: DriverError 25, DuplicateActorName 6, ReportCapExceeded 2, ArtifactUndeclared 1, InputHashMismatch 1.

## 5) Context loss

- 0 of 152 ZCode top-level sessions have a dossier in memory/biography/residual/. That is where 4,727 of his prompts live.
- After 9/11, grok-source dossiers drop to 1 a day through 9/21, and those are cron prompts. The top tldrs are "Use x_keyword_search ONCE" (591) and "run republic_os round" (363).
- open_loops holds 5 distinct strings across all 4,020 dossiers. That confirms today's verkle finding: the biography is knotting cron noise, not his work.
- 34 of 90 sessions open with a boot or recap ask. The self-steal and "you forgot" loops (469 + 219) are the cost of that cold start, paid in his prompts every day. Examples: "i let you go and fresh booted ... you started launching old shit we literally retired self steal" (9/22 08:23), and "discovered k8s twice, neither remembered" (MEMORY.md, mesh-intelligence entry, 10/2).
- The ZCode `todo` table already stores per-session open loops, and the residual knotter ignores it.

## 6) What already works (keep it)

- **Leverage up.** Human prompts per week fell 1,523 to 460 while child sessions per prompt rose 0.32 to 3.75. He is steering more and typing less.
- **Corrections that became carriers stuck.** Em-dash complaints went to 0 in W5 after seat_law_gate. ELI5 corrections fell 23.5 to 2.2 per 1000, and wire-don't-build corrections fell 32.8 to 6.5.
- **Money guards hold.** The A1 re-fire class went to $0.00 outside play after the 10/2 guard. The arena cap held at $25.35 of $25 (day-plan memory).
- **Falsifier culture catches real lies.** The 50-wide claim wave found 3 FALSE out of 50, including a planted forged ledger row (watch/inbox/burn_claims_50wide_20261003.md, per day-plan memory).
- **Night shift.** Night-shift and cron lanes do work while he is away (MEMORY night-shift entry, 10/2). 10/2 had his longest prompt-free gap (13.7h) and still logged 208 child sessions.

## THE TOP 7 CHANGES (ranked by measured impact)

### 1. `zknot`: knot real ZCode sessions and boot from them (boot-lane step)
- **Evidence:** 0 of 152 ZCode sessions knotted. open_loops has 5 boilerplate strings. "self steal" appears in 469 prompts plus 219 "you forgot" prompts on 32 of 32 days, and the rate is not falling. 34 of 90 sessions open cold.
- **Change:** a small read-only tool, tools/zknot.py (DFHack-style verb `knot`). It opens db.sqlite with mode=ro and, for each ended or idle interactive session, writes a residual dossier with:
  - his actual prompts (templated cron removed, as in this dive),
  - the `todo` table rows still pending (real open loops),
  - commits in the session window,
  - the inbox files the session wrote.
  Then add one boot-lane step: print the last 3 dossiers' open loops, plus the self-steal hits for the first prompt's nouns (rg over memory/ and watch/), before the seat answers.
- **Meter:** (a) ZCode dossiers > 0 within a day. (b) "self steal" + "forgot" prompts per 1000, baseline about 148 (102 + 46); target under 75 in 14 days. (c) Cold-open share, baseline 38%.
- **Effort:** half a day. Wire, don't build: the residual schema and the verkle backfill already exist.

### 2. `nextball`: no turn ends without a staged next ball (Stop hook)
- **Evidence:** 146 bare "next/go/now what" prompts plus 161 "keep going / why stop / wide" prompts. The second loop rose from 3.9 to 76.1 per 1000. MEMORY already holds "keep the machine fed" (9/29) and "width discipline x5" (9/30) as laws. They live in prose, not in a carrier.
- **Change:** a Stop/PostTurn hook beside seat_law_gate. If the turn did not fire a lane or write a named ball to a queue file (memory/plans/hermes_burn_* or the dwf queue), it blocks the stop once and prints the top staged ball.
- **Meter:** bare-next + keep-going per 1000, baseline 106 in W5; target under 40.
- **Effort:** 2 to 3 hours.

### 3. `lawlog`: give the gate a memory, and compile the new laws
- **Evidence:** seat_law_gate has no block log. SKILL.md stops at law 20 (9/11), while MEMORY records 38 law rows (10/2). The headless relapse is back at 17.9 per 1000 in W4. Commit messages hide deletions (add33ba72 drops memory/tls/lan.key).
- **Change:**
  - (a) The gate appends one jsonl row per block (law id, tool, path).
  - (b) A weekly compile step pulls law rows from MEMORY into SKILL.md as #21+.
  - (c) A commit-msg trailer adds "DELETES:" with the deleted paths automatically.
- **Meter:** blocks per law per week (a baseline exists after week 1); operator law corrections per 1000; commits with unlisted deletions = 0.
- **Effort:** 2 hours.

### 4. `redboard`: one screen of red patrols with days-red and owner (boot-lane step)
- **Evidence:** 8 tasks red right now. Tip witness and X radar have been red 4 of 4 days since 9/30, census patrol 7 of 9 since 9/26, and gap sentinel reports 29.52 GiB/day of repo growth. 888 of 1,150 attention lines are one alarm class.
- **Change:**
  - The boot lane prints each red task, its first red date (from logs/*.log END exit lines), the one-line cause, and the owner (seat-fixable vs operator-gated).
  - attention.md collapses a repeated alarm into one counted line.
  - Operator-gated items become a 3-row tap list.
- **Meter:** red task count (8) and max days red (7); alarm duplicate share (77%). Target: no seat-fixable task red more than 2 days.
- **Effort:** 1 to 2 hours.

### 5. Run-stamp play keys and add a `landed` field (ledger fix)
- **Evidence:** 10/3 excess is $15.00 of $25.62, all TAVERN/DND collisions (tavern.py:157). The doubled_key alarm fired on 687 paid rows. There is no landed field, so cost per outcome is unknowable.
- **Change:**
  - ids become `TAVERN_<runstamp>_r<rnd>_<actor>`;
  - hermes_burn _bank records `landed: true/false` (receipt written and verdict not void);
  - a daily line reports $ per landed receipt by lane.
- **Meter:** excess share on true duplicates under 5%; doubled_key alarms per day near 0; $ per landed receipt, with a baseline taken on day 1.
- **Effort:** 1 hour.

### 6. `dwflint`: pre-flight a workflow before it burns
- **Evidence:** 54 of 134 dwf runs failed or cancelled (40%), roughly 1.05B tokens. 9 of the failures are deterministic shapes: DuplicateActorName 6, ReportCapExceeded 2, ArtifactUndeclared 1. The 10/3 memory also logs the "args belongs to the path source" call-shape failure. DriverError (25) needs its own look.
- **Change:** a lint step before any workflow fire checks unique actor names, report() tags vs declared artifacts, the report cap, path+args shape, and fixed-order reporting (the 9/29 journal law).
- **Meter:** failed+cancelled share, baseline 40% (33% in week 39); target under 15%.
- **Effort:** 2 to 3 hours.

### 7. `owed`: one dated owed board, plus a 5-line unread digest
- **Evidence:** queue/todo.md has been stale since 9/29 06:53. Owed items live in prose in day plans, with items 6+ days old (same-disk backup, second-machine join). 480 of 601 inbox entries since 9/26 were never re-read on a later day. On 10/2 17:05 he said "i feel like i just ran a marathon with you i barely understand where w are".
- **Change:**
  - A tool greps "OWED / STILL OWED / operator-gated" lines from MEMORY and day plans into one board with a first-seen date.
  - The boot lane prints the 5 oldest items, plus the 5 newest unread receipts as one ELI5 line each.
- **Meter:** median owed age; count of items older than 7 days; the interactive later-day re-read share of receipts, baseline 1.4%.
- **Effort:** 2 hours.

## Grok Bot could take over (max 2)

1. **Morning "where are we" brief.** Each morning, Grok Bot reads redboard, owed, git log, and the spend ledger on this PC and writes one ELI5 page to Notion (or a Drive doc), with mermaid where useful. That replaces the 90 boot/recap asks and the 34 cold session openers. Meter: cold-open share and catch-up prompts per week.
2. **X intake desk plus the dead radar.** He drops x.com links in 15.5% of prompts (731) straight into the build seat, and MagXRadarDaily has been dead 4 days for want of the grok CLI. Grok Bot can take the drops, run the law-18 primary-source sweep, and file one receipt per drop to watch/inbox, so the build seat only sees the mechanism line. Meter: x.com links pasted into ZCode per 1000 prompts; x_radar.json freshness under 1 day.

## Not raised, by rule
The 9/30 key purge, the 191.8M figure, gap-register rows, and the instance guard are closed and were not re-raised. The memory/tls/lan.key deletion is mentioned only as a commit-message mismatch. Key contents were not read.
