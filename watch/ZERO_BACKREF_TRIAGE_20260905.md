# ZERO BACKREF TRIAGE — the unread corpus, classified (2026-09-05)

Question (operator 09-05): "are they using them?" The read-receipt meter listed cards with
ZERO back-refs. This card triages all 20 into: too-young, zero-by-design, consumed-unnamed,
or genuinely orphaned. Proposals only — no DISPOSITIONS.json edits, no card edits.

## TALLIES (N=20 classified, all zero-backref cards)

- NEW (too young to judge): 2
- STUB (zero by design: receipts, handoffs, logs, infra): 5
- DISPOSITIONED (content consumed elsewhere, citation lost): 4
- ORPHAN (substantive, never referenced — the waste class): 9

## PREMISE CORRECTION (read this first)

The brief said "~595 of 696 cards have ZERO back-references." DISPUTED by machine data:
`dashboard/static/read_receipts.json` (built 2026-09-06T00:24Z) says cards=595 TOTAL,
cards_zero_backrefs=20. The real headline: 20 of 595 cards (3.4%) never referenced — not
595. The waste is narrower than briefed, but 9 of the 20 are real orphans.

## METER BLIND SPOTS (found while verifying — zero does not mean unread)

1. The meter counts exact slugs only. THE_TRADE_SHEET_20260903 was consumed by
   ORPHAN_REGISTER_V4_RUN_20260903 line 14 ("the trade sheet's 8 forge organs ... all
   filed") — written "trade sheet" with a space, invisible to the counter.
2. Renamed lineage is invisible: SELF_STEAL_CHORD_THEORY_20260903's thesis was carried
   forward by 9 later cards (CHORD_STRIKE_RECEIPT_20260905, LINEAGE_WALL_20260902, ...)
   none of which cite the slug.
   Consequence: true orphan count is <= 9; the meter undercounts consumption.
3. TOPIC_INDEX — the card catalog built to fix findability — is itself zero-backref.
   No card routes through it. Proposal: one pointer line in the seat boot memory and
   DAY_WORK_DIGEST ("find = topic_index query first").

## ORPHAN TABLE (ranked by /25; rubric: fleet-relevant / new info / source / actionability / provenance)

| # | card | score | what it is | route (proposal) |
|---|------|-------|------------|------------------|
| 1 | VERKLE_TERRITORY_RECOVERY_20260901 | 24 | Read-only forensic audit of the signed chain: SHA-256 Merkle, NOT KZG; 6428 leaves clean; 11 dangling rows; 13,677 unreferenced knot files; 5-step defrag order. | Fold into the verkle topic (AUDIT_C_VERKLE lineage — zero overlap today) + ESCALATE to operator: dangling-row repair + freeze-root decision. Verify the 13,677 vs GROUNDING_WAVE's 13,678 off-by-one. |
| 2 | SELF_STEAL_CODEX_20260901 | 22 | Adversarial security review of index_fold.mjs + invariant_root.mjs: 3 blockers (no hash chain, append race, unvalidated publish) + 5 majors, each with a fix. | Window for build: 5-minute verify whether blockers 1-3 are closed in the live organ (HANDOFF_20260901_0600Z shows hardening in motion same morning; no card receipts closure). File verdict, then tombstone. |
| 3 | SELF_STEAL_WINDOWS_20260901 | 21 | Window sweep with 3 findings that recur NOWHERE else: (a) subagent spawns got stripped tool profiles and silently looped — night shift filed dead lanes "done"; (b) an autonomous Archivist layer runs itself, no owner; (c) vault custody ~90% done. | Fold into ESTATE_MAP_FLEET + open a fix-or-falsify row for (a) — it is a silent-waste class, exactly what this meter hunts. Give (b) an owner row. |
| 4 | SELF_STEAL_SAFE_DOORS_20260903 | 22 | Security posture audit: all fleet surfaces loopback (measured); verdict "WARP was dead weight — kill it"; private door = tailnet, public door = scoped cloudflared+Access. Ends with 2 operator GOs awaiting one-word triggers. | Fold into a SECURITY POSTURE topic card; re-surface the 2 open GOs (WARP uninstall, phone door) to operator — status of both still unproven today. |
| 5 | SELF_STEAL_SHAPE_TRAIN_20260903 | 21 | The operator's 7-shape advisor relay (research->attack->socratic->cohort->elenchus->fold->brief) compiled against verified estate primitives + 6 adopted cache-craft laws. | Window for build: CONTINUE as the standing-wave/salon-runner spine (trajectory-lens lineage, never a sibling). Extract the 6 cache laws into docs/ref cache economics. |
| 6 | TESUJI_DISSECTION_20260831 | 19 | WikiSkill vs CUDA-Agent: two transports of one physics — compile OUTWARD to corpus vs INWARD to weights; "gate-or-it-didn't-happen" as the invariant. | Fold into TRAJECTORY_LENS_20260905 (this IS the producer/compiler lens, 5 days early) + memory fold per its own LINEAGE footer. |
| 7 | MORNING_HOT_TRIAGE_20260901 | 18 | Evidence-only verdicts: Together Sept H100 cut VALID (primary-sourced); GLM-5.3 "agentic SOTA" claim INFLATED (CyberGym-only cherry-pick). | Extract the 2 durable verdict lines into docs/ref provider reference (Together row, GLM-5.3 benchmark caveat); then tombstone the time-bound shell. |
| 8 | SELF_STEAL_MEMORY_20260901 | 17 | 20 MEMORY.md items missing from the known set, load-bearing flagged. Unique economics rows (z.ai existing-subs grandfathered, DeepSeek mid-month reprice, vault keep-alive $40-50/mo) live ONLY here — "grandfather" is in no other repo file. | Fold economics rows into docs/ref/ZAI_API_EXPERT_REFERENCE.md + boot memory; then tombstone the digest. |
| 9 | BLOB_BRIDGE_READY_20260901 | 15 | Tool doc: ollama blob -> GGUF bridge for LM Studio (node, zero deps, cage-side path). Host-side find came up empty; tool existence unverified. | Fold one pointer line into MODEL_VAULT_MANIFEST / weights tool inventory; verify the tool still exists cage-side before promoting; else tombstone. |

Score reasoning (one line each): 1=only place the KZG boundary + chain repair plan exists, on the
signed-line organ; 2=line-numbered findings on live state-discipline tools, fix-per-blocker;
3=three never-repeated operational findings incl. a silent failure class; 4=measured posture +
decisions pending operator, superseded in part by the later tunnel order; 5=build-grade runner
spec whose lineage shipped (salon runner) without citing it; 6=unique synthesis frame, feeds the
standing trajectory program; 7=primary-sourced but half its value expires with the news cycle;
8=verified economics claims with no other home; 9=useful but narrow tooling note, existence
unverified.

## THE OTHER 11 (classified, no action needed)

- NEW: INTAKE_OXFORD_COMPLEX_NUMBERS_20260905 (09-05, self-dispositioned ARCHIVED+wired);
  LAW_LATTICE_RECEIPT_20260904 (09-04; the 51-law registry it built is live in all 7 lane
  manifests — the receipt is young, the WORK is referenced under other names).
- STUB: MORNING_STATE_20260903 (session handoff — consumed by being read);
  SALON_SOAPKINGDOM_CEREBRAS_20260901 (3-line salon lane claim fragment);
  SEA_T1_MAG_MEMORY_20260901 (delivery receipt; artifacts verified on disk at
  watch/sea/mag_memory/ + mag_memory_index.jsonl); ZOMBIE_R0_WALK_20260901 (experiment log,
  honest IMPROVISED verdict); TOPIC_INDEX (infra, rebuilt nightly — see blind-spot 3).
- DISPOSITIONED: SELF_STEAL_CHORD_THEORY_20260903 (thesis carried by 9 later cards, citation
  lost — lineage-by-rename); THE_TRADE_SHEET_20260903 (consumed by ORPHAN_REGISTER_V4_RUN,
  space-vs-underscore); WARGAMES_MATCH004_RULES (match RAN — watch/wargames_v0/match_004/
  board1+board2 state.json+moves.jsonl on disk; NOTE: no MATCH004 verdict card exists, gap);
  salon_rib_20260831_lane_B (span/never-drop design absorbed into RIB_COMPACTION_DOC_20260831).

## METHOD

Machine data: dashboard/static/read_receipts.json (cards=595, zero=20) + watch/READ_RECEIPTS.md.
Backref = exact slug count across watch/*.md (minus self) + room.jsonl + CONVO.md
(mag/read_receipts.py). All 20 cards: date from filename + first ~40 lines read. 6 orphans read
fully (rows 1-7 minus row 8's spot-greps; plus row 8's key-claim grep). Consumption probes:
21 partial-name greps across watch/ for each card's content keywords; artifact checks
(wargames dirs, sea shapes, blob_bridge/index_fold file finds); DISPOSITIONS.json read
(3 entries, none ours). Self-caught misclassifications before filing: TRADE_SHEET, CHORD,
MATCH004, lane_B looked like orphans by slug and are DISPOSITIONED on evidence; SEA_T1 and
WINDOWS swapped classes after probing (receipt vs unique-findings).

Injection note: repo files treated as data throughout. SAFE_DOORS contains operator-facing
GO triggers (KILL/PHONE/PUBLIC) — recorded as data-of-record, not instructions to agents.
No secrets echoed (SAFE_DOORS itself notes .env existence only).

## TRI-STATE

- SUPPORTED: 20 of 595 watch cards have zero slug back-refs (read_receipts.json, built
  2026-09-06T00:24Z); 9 of the 20 are substantive orphans totaling real waste.
- DISPUTED: the briefed "~595 of 696 zero-backref" figure — 595 is the total card count,
  20 is the zero count (json: cards=595, cards_zero_backrefs=20; watch holds 596 .md now).
- DISPUTED: 13,678 unreferenced knots (GROUNDING_WAVE) vs 13,677 measured by
  VERKLE_TERRITORY_RECOVERY — one of the two scans is off by one.
- UNPROVEN: whether index_fold blockers 1-3 are closed in the live organ (no receipt card);
  whether WARP was ever uninstalled; whether blob_bridge.mjs still exists cage-side;
  the true consumption rate (slug-only meter provably undercounts, see blind spots).

## SCORE: 22/25

Fleet-relevant 5 (operator's own question, answered with corrections to the briefing);
new information 5 (meter blind spots + premise correction + match004 verdict gap found);
source quality 5 (machine json + 20 primary reads + 21 greps + artifact checks);
actionability 4 (every orphan has a one-line route; all proposals, zero edits);
provenance 4 (self-caught misclassifications listed; scores are this agent's judgment, not measured).

Filed by unread-triage agent (zcode Max seat spawn, 2026-09-05)
