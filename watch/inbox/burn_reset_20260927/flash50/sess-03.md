# sess-03: AGENTS.md law-lineage census (2026-09-28)

Item: read AGENTS.md fully; for each standing law: when minted, what incident created it,
is it still accurate, has it been superseded. Method: Read AGENTS.md (119 lines, working
tree state read 2026-09-28); git blame per line range; git log --follow on AGENTS.md; read
every receipt the file cites; ran the gates the laws name where cheap and read-only.
Branch at read time: mag/run-beta1-factory-build-audi-20260806T231709Z, HEAD 99281683e.

Law text dates come from git blame on AGENTS.md (author dates, all -0400 unless noted).
One uncommitted edit exists in the working tree: AGENTS.md:79 FW-11 fence-owner marker
(blame "Not Committed Yet 2026-09-28", diff shows only that one added line; another lane's
in-flight work, left untouched by this read-only census).

## Law-lineage table

| # | Law (AGENTS.md line) | Minted | Incident that created it | Still accurate today (evidence, this session) | Superseded by |
|---|---|---|---|---|---|
| 1 | Warm boot at session start (5) | 2026-09-25, blame ea04ebc15 (ratchet wave 2) | Spore/session-continuity work; hermes_warm_boot wired as boot step | mag/hermes_warm_boot.py exists; memory/warm_state.json mtime 2026-09-28 19:07:31 (used today). Same line's "$220 armed" is a 2026-09-14 audit datum; row 11 below states $180 as the newer funding truth, so the dollar figure is aged | No; funding datum aged by row 11 |
| 2 | Zeitgeist pointer with never-existed caveat (8) | 2026-09-14, blame 9669eec5b (self-steal round-2: fix what the audit missed and broke) | Fossil-citation disease: the docs/ZEITGEIST.md path cited before 2026-09-14 never existed; line rewritten to docs/archive/ZEITGEIST.md with the confession inline | docs/ZEITGEIST.md MISSING (existence check run); docs/archive/ZEITGEIST.md exists, head reads "era 003: THE POUR (iterated 2026-09-05)" | No |
| 3 | Shared artifact boundary, inbox as durable write root (10-20) | 2026-09-14, blame d575bc168 (checkpoint: Zenodo 17811909 capstone mined + forge-window recovery receipt) | Forge-window recovery: session directories proved to be cache, cross-surface work was being lost outside watch/inbox | watch/inbox/SHARED_SURFACE_CONTRACT.json and INDEX.json exist; `.venv\Scripts\python.exe -m mag.shared_surface validate` ran: 18 open / 0 unverified / 0 downgraded, 5 errors all other lanes' bytes (4 hash mismatches on 2026-08/09 salon receipts + 1 NEW event-kind row in LINKS.jsonl line 377, known debt) plus a large unindexed-inbox warning listing live 09-27/28 burn files; mechanism works and catches drift | No |
| 4 | New-window frozen spec (26) | 2026-08-08, blame 60e18c524 (sovereign architecture commit) | Clippy cited /memories/session/next-window-handoff.md before it existed; spec's own head: "This file did not exist until 2026-09-15 (Clippy cited a fossil). This IS the spec now." | memories/session/next-window-handoff.md exists (466 lines) with procedure + standing laws; the fossil was healed retroactively | No |
| 5 | Tests census + census denominator law B2-216 + tripwire B2-215 + deep check B2-244 + carrier shape B2-249 + scheduled deep check B2-246 (27) | Sub-laws minted 2026-09-26 (B2-69/215/216/244/246/249); carried as uncommitted law text, landed 2026-09-27 with e73b60c54 (verkle99: "carrier line also carries the 09-26 lane's uncommitted B2-215/216/249 law text"); carrier refreshed to 2,303/352 same commit | "1,341 tests" headline born 2026-09-14 hand-copied from a trio that sums 1,348 (memory/trajectory/steps.jsonl:4729 per B2_69 receipt), rode 12 days stale while tests/ grew 31 files with no gate noticing; 09-26 collected-vs-executed gaps (1,837 vs 1,776/1,782) attributed to 64 mid-wave landings (B2_216) | Ran `.venv\Scripts\python.exe tools\census_drift_patrol.py`: "ok - census 2026-09-27 (2303 collected / 352 files)", 1d old of 7d bar, 5 files grew 09-28 inside window, exit 0. MagCensusPatrolDaily Ready, next 09-29 8:30; logs/census_patrol.log shows today 17:20:35 deep check (--collect) + growth alert appended to memory/attention.md. Carrier in sync now; drifts by design as tests land | No; self-refreshing via B2-246 |
| 6 | Deliberate-ask (28) | 2026-08-08, blame 60e18c524 | Context-tax economics doctrine; parent DELIBERATE-ASK PROTOCOL standing rule + research pack logged 2026-08-07 (memory/research_packs/20260807T205500Z_context-tax-deliberate-ask-research-project.md) | Doctrine intact; no superseding law found in AGENTS.md or memory/rib listing | No |
| 7 | Thinking-mode is the axis (29) | 2026-08-08, blame 60e18c524 | Tier-probe measurement 2026-08-07: design_vague flash-on scored 0.70 vs flash-off 1.00 (pro-off 1.00), n=1 (memory/runs/tier_probe/20260807T215905Z/REPORT.md:11-13) - thinking mode moved the pass rate, model tier did not | Receipt bytes verified this session; law matches its evidence (n=1 probe, never re-run at scale: stated, not re-verified here) | No |
| 8 | Pile habit (30) | 2026-08-08, blame 60e18c524 | Pile doctrine: state summaries must be contributed before seat exit; overnight pile-classify | Commands verified: main.py:1236 "pile-classify" + :4645 dispatch; mag/state_snapshot.py:75 def capture_summary; memory/pile/ holds classified.jsonl, state_summaries.jsonl etc | No |
| 9 | Tier ladder ollama->free->deepseek->pro (31) | 2026-08-08, blame 60e18c524 | Early routing economics (free tiers first, judgment climbs) | Text still physically present | YES: explicitly superseded in place by row 11 (line 32 text: "supersedes the tier-ladder line above") |
| 10 | Clippy invocable (35) | 2026-08-08, blame 60e18c524 | Standing-reminder rope verkle-committed | main.py:1254 "clippy" + :4653 dispatch verified | No |
| 11 | DRIVING LADDER (32) | Minted night 2026-09-27/28: commit 709e2928a author/commit 2026-09-27 21:09:08 -0400 (= 2026-09-28 01:09 UTC, matches the 20260928 stamp and receipt name); law text self-dates 2026-09-28 operator code-as-law | Three operator corrections in a row (RIB_DRIVING_LADDER_20260928.md:3-5): "those aren't funded only hermes" / "stop running shit and start remembering" / "what are warmed ribs for if you won't use them"; a fresh seat re-derived what a rib held and had to be corrected three times | Receipt exists (37 lines) and updates RIB_FREE_USAGE_POLICY_20260823 funded rung (DeepSeek era -> Nous credits era) per its lineage section; $180 Nous credits, Anthropic keys unfunded | Current apex routing/funding law; supersedes row 9 |
| 12 | Fan-out width law (33) | Incident 2026-09-25 (TETHERED_LINK_STEAL_20260925.md); law text landed in AGENTS.md 2026-09-27, blame e73b60c54 | Tree Doctrine 50-wide dig dwfrun-15738edf 429-stormed z.ai (1,838 rate-limit log lines that day); workflow children maxAttempts 0 die on first 429; the operator's "subscription errors" were 1302 rate-limits rendered by the client, no 1309 in the log | Receipts all exist and were read: TETHERED_LINK_STEAL (width <=3 law, off-peak, owner, tether, retry laws), B2_25 re-measure (Task agents 10/10 clean at width 10, 109.4M tok/h, clean ladder 3-6-10-12, 15-16 untested), B2_443 (896 invisible model.network.failed on sess_dwf-* across 27 runs, 817 carrying the 1302 message), AFTERPARTY B2-476 amendment | Partially: its own <=3 workflow cap is expressly overridden for the measured gated shape by row 13 |
| 13 | Max-concurrency standing law (34) | 2026-09-26 operator ruling; text landed 2026-09-27, same commit e73b60c54 as row 12 | ENVELOPE_50W_HIT_20260926.md: first 429/1302 contact at 5 workflows x max_concurrency 10 (50 children) + hourly burn cron + offpeak tasks; operator ruled the contact a HOLD (children retry internally), width held at 50 | Receipt exists and was read (9 lines, decision recorded: "width HELD at 50"); law explicitly says "the measured envelope supersedes the 3-cap conservatism" | Current; supersedes row 12's cap for gated workflows at the measured shape |
| 14 | Load order + state pointers (37-52) | Table minted 2026-08-05/06 (blame c947407773 Cursor Agent + 1c156e2fa Codex); FROZEN-brief clause on line 52 minted 2026-09-27, blame e73b60c54 | Brief tooling regenerated August content under a today face; latest.md frozen by operator GO 2026-09-26 (banner in memory/briefs/latest.md: writers sealed mag/brief_local.py + mag/session_state_brief.py, OS +R, unfreeze via attrib -R) | All 8 load-order files + configs/version_roadmap.yaml + docs/ref/releases/VERSION_REGISTRY.md + state/CURRENT.md + queue/todo.md + HANDOFF_MAG_AGENT_TODOS.md exist (existence check run); latest.md banner verified verbatim | No |
| 15 | Specialist-seat rules: prefer briefs, [priority]/[L2], brief-not-chat, no R0 claim (54-59) | 2026-08-04, blame eb07ad62e (clean publish baseline, repo birth) | Original specialist-era routing rules | configs/lanes.yaml:19-22 + :73-77 verified (require_priority: true, priority_markers: "[priority]"); CONFLICT FOUND: line 56 still says "Prefer memory/briefs/latest.md" while line 52 (2026-09-27) froze that file and forbids consuming it as live; the 08-04 line predates the freeze and was never amended | Partially contradicted in place by row 14's FROZEN clause; operator edit owed |
| 16 | Python env: never bare python on PATH (61-74) | 2026-08-04, blame eb07ad62e | Default shell python resolves to Hermes venv (hermes-agent\venv), no Mag deps, "No module named 'langgraph'" | scripts/ensure_venv.ps1 exists; this session's own runs used .venv\Scripts\python.exe throughout and worked; the bare-python failure itself not reproduced (not run) | No |
| 17 | Commands card (76-99) | Base 2026-08-04/05 (blame eb07ad62e + c947407773); FW-11 fence-owner marker added 2026-09-28, uncommitted (concurrent lane) | FW-11: 30 launcher-shaped fences needed owner or SUPERSEDED disposition (watch/inbox/fifty_wide_20260917/FW11_fence_owners.md read: AGENTS.md#fence2 = harness command card, OWNER; detector upgraded with _FENCE_OWNER_RE, flagged 30 -> 0) | MagImproveDaily task Ready next 09-29 8:00 (schtasks via cmd); the card's fence marker is the one uncommitted AGENTS.md edit in the tree | No |
| 18 | Constitution pointer (116-118) | 2026-08-04, blame eb07ad62e | Governance anchor at repo birth | CONSTITUTION.md exists at root and points to ../mycelial-republic/docs/CONSTITUTION.md, which exists on disk (checked) | No |
| 19 | Spec before behavior change (105) | 2026-09-25, blame ea04ebc15 ("AGENTS.md build-discipline laws from ZCode source") | ZCode's own machine-enforced maker laws, recreated in Mag per the steal receipts | Doctrine, no counter-law found | No |
| 20 | No timeouts papering over sync problems; no fallback-branch creep (106) | 2026-09-25, blame ea04ebc15 | Same ZCode source wave | Doctrine, no counter-law found | No |
| 21 | Fix comments carry the receipt (107) | 2026-09-25, blame ea04ebc15 | Same ZCode source wave (FW-11 receipt demonstrates the practice: fix comment cites the receipt) | Doctrine, no counter-law found | No |
| 22 | Ratchet gate at pre-push (108) | Tool minted 2026-09-24 (ZCODE_RATCHET_LANDED_20260924.md read: virgin check FAIL 192 NEW -> baseline-update ADDED=192 -> PASS); hook wired 2026-09-25, blame ea04ebc15 ("pre-push gate wired (githooks/, core.hooksPath)") | Registered-debt ratchet stolen from ZCode's architecture gate so NEW violations block and old debt must be accepted by name | tools/violation_ratchet.py (last commit 383fed94f 2026-09-27), githooks/pre-push, configs/violation_baseline.json all exist; ratchet check itself NOT run in this ask (reported as not run) | No |
| 23 | Scenario-suite gate at pre-push (109) | B2-164, 2026-09-26; landed in AGENTS.md text 2026-09-27, blame e73b60c54 | LAW-12 genesis clause (watch/inbox/BURN_rsi-harness_20260926.md:25, read): every gate is born before its gate exists, so generation zero is structurally ungated; pre-registered 14-day clause required one scenario card per G1-G7 minted from real REGISTRY FAIL rows | configs/workflow_gate_scenarios exists; `tools/workflow_gate.py check --scenarios` NOT run in this ask (reported as not run) | No |
| 24 | Workflow gate at submit (110) | LAW-12 lineage, 2026-09-26 genesis (BURN_rsi-harness_20260926.md:14-29); gate tool last commit 383fed94f 2026-09-27 | Ungated CreateWorkflow risk; gate enforces dogfood axes and self-steals the ratchet pattern (exit-2 blocks, amend-not-rewrite, REGISTRY.jsonl ledger) | This session is itself a gated workflow child running under that gate; memory/workflows/REGISTRY.jsonl is the ledger; gate check NOT re-run in this ask | No |
| 25 | Boot freshness (111) | 2026-09-25, blame ea04ebc15; commit message records the incident: BOOT_4_7.md 11.1d + HANDOFF.md 25.3d STALE, honest FAIL left open | Stale-trap disease: boot docs rot while the repo has a heartbeat | Ran `.venv\Scripts\python.exe tools\freshness_check.py`: "FRESHNESS: PASS - boot docs inside the bar" (heartbeat 0.0d; BOOT_4_7.md 2.8d frozen-ok; HANDOFF 2.4d frozen-ok) | No |
| 26 | Corpus FTS index daily, B2-465 (112) | 2026-09-26; landed in AGENTS.md text 2026-09-27, blame e73b60c54 | The B2-102-era freshness gate only detects decay, never heals (B2-102 = 5 LEDGER.jsonl rows counted, b2-22-corpus-fts5-spike lineage); catalog drifts past the FTS5 index into scan fallback | MagFtsIndexDaily Ready next 09-29 9:00; logs/fts_index.log tail: 2026-09-28 09:00:09 POST exit=0, END exit=0, deep "match" - alive and green today | No; heals the gap row 22/23 style gates left |
| 27 | Operating-playbook pointer (113-114) | Receipts 2026-09-24 (ZCODE_RATCHET_LANDED), playbook wired 2026-09-25, blame b1d714b02 ("spore alive ... ZCode operating playbook (13 verified laws) wired into AGENTS.md") | Harness self-knowledge: cache, compaction and hook-contract laws verified against the harness's own source before running workflows on it | corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md exists | No |

Row count: 27 law rows. The Clippy block (lines 26-35) contributes rows 4-13; the header/env
sections rows 1-3 and 14-18; build discipline rows 19-27.

## Cross-law findings

1. Fossil-citation is a recurring birth defect, healed twice the same way: the new-window
   spec (row 4) and the Zeitgeist path (row 2) were both cited before their targets existed,
   both confessed inline later (line 8 and the spec's own header). The 1,341 census headline
   (row 5) is the same disease one level up: a number cited with no bytes behind it.
2. One live contradiction found: AGENTS.md:56 (2026-08-04) "Prefer memory/briefs/latest.md"
   vs AGENTS.md:52 (2026-09-27) "FROZEN 2026-09-26 and must not be consumed as live". The
   specialist-seat section was never amended when the brief froze. Fix owed to the operator;
   not applied by this read-only item.
3. Aged datum inside row 1: line 5's "$220 armed - audit 2026-09-14" predates the driving
   ladder's "$180 Nous credits" (line 32). Funding truth lives in row 11 now; the header
   number should be read as historical.
4. Width-law evolution is a chain, not a replacement: 2026-09-25 cap <=3 after the tether
   429 storm -> 2026-09-26 re-measure (Task agents clean at 10-12, B2_25) -> 2026-09-26
   first contact at 50 children ruled HOLD (ENVELOPE_50W_HIT) -> rows 12/13 landed together
   2026-09-27 with line 34 expressly claiming supremacy over the 3-cap for the measured
   gated shape. Row 12's own text still carries the <=3 default for ordinary workflow digs.
5. Law-text landing lags law minting: rows 5/12/13/23/26 were minted 2026-09-26 (or earlier)
   but their AGENTS.md text landed 2026-09-27 in e73b60c54, which the verkle99 commit message
   admits carried "the 09-26 lane's uncommitted B2-215/216/249 law text". Blame dates name
   the landing, not always the minting; receipt dates name the minting.
6. Machine-enforcement creep is the pattern that keeps laws alive: rows 5, 22, 23, 24, 25, 26
   all grew a tool or scheduled task after their prose law; row 10's rope line ("You do not
   have a choice. The rope is verkle-committed.") is the doctrine made literal.

## Checks run this session (exact commands, outputs summarized above)

- git log --follow --format="%h %ad %s" --date=short -- AGENTS.md (14 commits, 2026-08-04 base to 2026-09-27 tip)
- git blame -L per range on AGENTS.md lines 1-119 (all law lines dated)
- git show -s author+commit dates for 8 commits touching AGENTS.md
- Existence check over 61 paths AGENTS.md cites: 60 exist, 1 missing (docs/ZEITGEIST.md, which row 2's law itself asserts never existed)
- .venv\Scripts\python.exe tools\census_drift_patrol.py -> ok, exit 0 (census in sync, 1d of 7d bar)
- .venv\Scripts\python.exe tools\freshness_check.py -> PASS
- .venv\Scripts\python.exe -m mag.shared_surface validate -> ran; 5 errors, all other lanes' bytes or known LINKS.jsonl debt; large unindexed-inbox warning (live 09-27/28 burn files)
- cmd //c "schtasks /Query /TN <task>" for MagCensusPatrolDaily / MagFtsIndexDaily / MagImproveDaily -> all Ready
- tail logs/census_patrol.log and logs/fts_index.log -> both show 2026-09-28 activity (17:20 deep check; 09:00 exit 0)
- Receipts read whole or head: RIB_DRIVING_LADDER_20260928.md, RIB_FREE_USAGE_POLICY_20260823.md, ENVELOPE_50W_HIT_20260926.md, B2_69_test_census_20260926.md, B2_216_collect_delta_20260926.md, TETHERED_LINK_STEAL_20260925.md (60 of 105 lines), FW11_fence_owners.md, ZCODE_RATCHET_LANDED_20260924.md (40 of 76), ZEITGEIST.md head, next-window-handoff.md head, memories of briefs/latest.md head, B2_25_envelope_remeasure head, B2_443_dwf_error_census head, BURN_rsi-harness grep (LAW-12 genesis lines), AFTERPARTY grep (B2-476), CONSTITUTION.md head, deliberate-ask research pack head
- Grep verifications: capture_summary (mag/state_snapshot.py:75), pile-classify (main.py:1236,4645), clippy (main.py:1254,4653), lanes.yaml priority markers, design_vague (tier_probe REPORT:11-13), B2-102 count in memory/burns/LEDGER.jsonl (5)

## Not run / not verified (stated, not guessed)

- pytest --collect-only -q was not re-run by me; the carrier's 2,303/352 stands on the patrol's
  own ok verdict plus this morning's scheduled deep check in the log, not on a fresh count here.
- Ratchet check, workflow-gate scenario suite, and the bare-python failure were not executed
  in this ask (rows 16, 22, 23, 24).
- design_vague probe was n=1 on 2026-08-07 and was not re-run; the law rests on that single
  measurement plus operator doctrine.
- R0/T0/T1 semantics (line 59) verified only as text; no runtime instrument for them was found
  or run.
