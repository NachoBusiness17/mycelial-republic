# RUN RECEIPT: ball-20260929 (gala_20260925)

- Written: 2026-09-29, by the herald receipt writer
- Slug: ball-20260929
- Gala: gala_20260925 (`watch/inbox/gala_20260925/`)
- Lanes: 9 lane JSONs (expected 9)
- Parsed ok: 5/9 (gate parse pass)
- Divisions: B=7, C=1, A=1
- Gate: GATE PASS
- Ballroom: 8 danced / 0 refired / 1 buried
- Review: REVISE (one claim in heads-abliteratus to correct before banking)
- Filing: FILED (8 GALA LINKS rows + one handoff STATE entry)
- Receipt path: `watch/inbox/gala_20260925/ball-20260929_RECEIPT.md`

Source of record: the run's script-written sections (authoritative per the filing ask), plus the run's fold, review and filing records carried in the same ask. Em-dashes, en-dashes and arrows are normalized to ASCII per house law; numbers are transcribed verbatim and never re-derived. Items marked "herald" were run by this receipt writer in this session; everything else is transcribed from the run's own records and is not re-run here.

## 1. Scoreboard (script-written sections, authoritative)

- lanes_json_count: 9 (expected 9)
- lanes_parsed_ok: 5/9
- by_division: {"B": 7, "C": 1, "A": 1}
- byte_checks_cited: 46
- mined_rows: 29
- decisions_changed: 7
- ballroom_count (danced/refired/buried): 8/0/1
- GATE PASS

Stuck (1):

- abliterate-p1.json (no ok, rows=0, checks=0 - the empty-on-refire buried shape)

Banked (3):

- bare-spawn-descent.json (ok absent/false, evidence-banked: 5 checks, 0 rows)
- driver-v2.json (ok absent/false, evidence-banked: 7 checks, 0 rows)
- grave-supersede.json (ok absent/false, evidence-banked: 6 checks, 19 rows)

Gate decision_changed lines (7, as written in the sections; each line is truncated at source, full statements in section 2):

- abliterate-p1.json: Closes: ABLITERATUS probe P1 baseline (owed from the drop). Changes: the P2 decision input - gemma:2 [truncated at source]
- attention-ledger.json: Attention-market wiring decision: the trade ledger (memory/attention_feedback.jsonl) went from ABSEN [truncated at source]
- driver-v2.json: sensed-never-done is closed: the work queue now drains through funded verification (lib-belady-1966 [truncated at source]
- fold-gate.json: gala fold arithmetic is now script-written end to end: fold_gate.sh prints the ballroom danced/refir [truncated at source]
- heads-abliteratus.json: Janitor-ladder probe order: try P3 (reversible inference-time steering vectors, no weight mutation, [truncated at source]
- mcp-bridge-r1.json: mcp-bridge R1 closed: estate compute moved from zero tools on the live MCP surface to five verbs / s [truncated at source]
- quantizer-hygiene.json: The compiled-law decay relation is now ONE named constant (PACK_STALE_DAYS=7, mag/constants.py) impo [truncated at source]

### Fold scoreboard narrative (fold field, content verbatim, dashes normalized)

GATE PASS (ask's scripted sections, authoritative). Ballroom 8 danced / 0 refired / 1 buried; by_division B7 C1 A1; 9 lane JSONs as expected (I listed the lanes dir - exactly the 9 lane files present); 5/9 parsed-ok; 46 byte checks cited; 29 mined rows (carried verification from the files: 5 mcp-bridge-r1 + 5 heads-abliteratus + 19 grave-supersede = 29, agrees). DIVISION B - 6/7 danced, 1 buried. Standouts: fold-gate (fold arithmetic script-written end to end; 7 probes incl. both negatives failing loud rc 2 and the wrong-bash 127 byte-reproduced); driver-v2 (funded DONE gate flipped lib-belady-1966 done_ts 2026-09-29T15:18:30Z on a real OWED->DONE pair; 30 driver tests green; GHOST filed for the out-of-repo actor killing driver instances every ~10 min); mcp-bridge-r1 (five verbs / six tools live over stdio, 13/13 probe PASS + 262 consumer tests, repair/bank/control-words/keys never exposed); attention-ledger (ledger ABSENT -> proven rails with the market's first two settled trades, retry idempotent, ranker consumed them 84->88 and 71->75); quantizer-hygiene (PACK_STALE_DAYS=7 one constant at 3 import sites, kept==packed 374, kept-but-unpacked now a compile-time linker error); bare-spawn-descent (tests/ bare spawns 21->0, accepted register 41->22, headless-law test red->green). Buried: abliterate-p1 (the gate read no ok / rows=0 / checks=0 - the empty-on-refire buried shape; the file carries its battery results and decision under other key names instead; carried note: run metadata marks it ok:true rows:3 - gate sections authoritative, contradiction not averaged). DIVISION A - 1/1 danced: heads-abliteratus (5 laws mined with quotes byte-verified as exact substrings, 3 LINKS rows appended through the line-355 precedent shape, mcp_pin self-test 9/0, decision changed). DIVISION C - 1/1 danced: grave-supersede (19 of 38 queue/handoff JSONs graved receipt-only with disk-verified successors, 23 index_events rows appended, decision 'no'). Totals: 9 lanes, 7 decisions changed, parade = false.

## 2. Decision ledger (fold; parade: false, so NOT a parade)

Seven decisions changed - NOT a parade, plainly. (1) abliterate-p1.json (lane file decision_ledger field): gemma:2b friction on fleet scut shapes is capability-shaped, not safety-refusal-shaped (0/60 safety refusals, 11/60 file-reference declinations), so the $0 counter-move (attach cited-file content to scut prompts or tool-wire the janitor) is registered as first remediation before any weight change; the P2 gate reads the capability/safety split from this exact battery unchanged. (2) attention-ledger.json: the trade ledger (memory/attention_feedback.jsonl) went from ABSENT/zero-trades-uninformative (w4-03, w4-37 T2: apathy indistinguishable from broken rails) to proven rails with the market's first two settled trades; POST casts settle once in the five-signal vocabulary and the next ranking pass provably consumes them, so future zero-trade readings are honest demand signals. (3) driver-v2.json: sensed-never-done is closed - the work queue drains through funded verification (lib-belady-1966 flipped done_ts 2026-09-29T15:18:30Z after a real OWED->DONE verify pair), and the selffeed never-drains-it-grows doctrine is replaced by the bounded loop (trigger gate, hourly spacing, cap 20, depth 2, dedupe, m%03d ids, 24h ttl, breaker). (4) fold-gate.json: gala fold arithmetic is now script-written end to end - fold_gate.sh prints the ballroom danced/refired/buried count (was hand-computed by the filer) and counts decisions under all three observed key names (10->12, matching the filer's verified hand count); wrong-bash invocations fail loud rc 2 instead of the silent 127. (5) heads-abliteratus.json: janitor-ladder probe order is P3 (reversible inference-time steering vectors, no weight mutation, hot-swappable) before P2 (permanent weight projection), both gated on the P1 refusal-census baseline and the named capability battery, and the verification stage is adopted regardless of whether the ablation itself is; second-order change: violation classes excised by the ratchet keep their downstream detectors enabled instead of closing the watch. (6) mcp-bridge-r1.json: mcp-bridge R1 closed - estate compute moved from zero tools on the live MCP surface to five verbs / six tools any MCP client can call over stdio, with the standing decision that chain repair, dirac bank, driver control words and provider keys are never exposed (R2-R5 unstarted per the rollout order). (7) quantizer-hygiene.json: the compiled-law decay relation is now ONE named constant (PACK_STALE_DAYS=7, mag/constants.py) imported by producer, consumer and boot meter, closing the w4-27 L3 subsumption gap in code, and kept-but-unpacked law is a loud compile-time linker error instead of a silent 283-law census finding. Not changed: bare-spawn-descent.json (banked; no decision key in the file - it updated the headless register 41->22 instead) and grave-supersede.json (decision_changed: 'no').

### Top laws (fold)

1. verify-after-modify with a named battery (heads-abliteratus.json row 1, byte-verified quote from watch/inbox/ABLITERATUS_DROP_20260929.md). Why: it is the law that already bent this gala's biggest decision - the P3-before-P2 janitor-ladder order gates both rungs on the P1 battery and adopts the verification stage even if the ablation itself is rejected - and it generalizes the estate's own gate discipline proven in someone else's forge: nothing is done until a named capability battery reruns green; falsified when a modified model or mechanism is claimed done with the battery skipped, run after the claim, or swapped for an unnamed ad hoc check.
2. isError in-band, never protocol-level (mined twice: mcp-bridge-r1.json row 1 and heads-abliteratus.json row 3, from two different drops). Why: two lanes independently mined the same law from two different banks - the estate's twice-learned promotion trigger - and it landed in code this gala (mag/estate_bridge.py wraps caller-fixable failures as isError, 1 [text truncated at source; not completed by the receipt writer]

### Run metadata lane records (9, from the run metadata danced array; each carries ok:true in the metadata)

| lane | division | ok | rows |
|---|---|---|---|
| fold-gate | B | true | 0 |
| driver-v2 | B | true | 0 |
| quantizer-hygiene | B | true | 0 |
| abliterate-p1 | B | true | 3 |
| mcp-bridge-r1 | B | true | 5 |
| bare-spawn-descent | B | true | 0 |
| attention-ledger | B | true | 0 |
| heads-abliteratus | A | true | 5 |
| grave-supersede | C | true | 0 |

Note: the gate's ballroom arithmetic is 8 danced / 1 buried (abliterate-p1); the metadata's danced array lists all 9 lanes with ok:true. The fold rules the gate sections authoritative and the contradiction is recorded, not averaged.

Run metadata decision fields (verbatim, dashes normalized):

- fold-gate: gala fold arithmetic is now script-written end to end: fold_gate.sh prints the ballroom danced/refired/buried count (was hand-computed by the filer per the wave5 completion finding) and counts decisions under all three observed key names (10 -> 12, matching the filer's verified hand count); wrong-bash invocations fail loud rc 2 instead of the silent 127.
- driver-v2: sensed-never-done is closed: the work queue now drains through funded verification (lib-belady-1966 flipped done_ts 2026-09-29T15:18:30Z after a real OWED-then-DONE verify pair), and the selffeed never-drains-it-grows doctrine is replaced by the bounded loop (trigger gate, hourly spacing, cap 20, depth 2, dedupe, m%03d ids, 24h ttl, breaker)
- quantizer-hygiene: The compiled-law decay relation is now ONE named constant (PACK_STALE_DAYS=7 in mag/constants.py) imported by producer, consumer and boot meter, closing the w4-27 L3 subsumption gap in code, and kept-but-unpacked law is now a loud compile-time linker error instead of a silent 283-law census finding
- abliterate-p1: ABLITERATUS P2 decision input changed: the measured gemma:2b baseline friction on fleet scut shapes is capability-shaped (0/60 safety refusals), so the $0 counter-move (attach cited-file content to scut prompts or tool-wire the janitor) is registered as first remediation before any ablation, and the P2 gate reads the capability/safety split from this exact battery unchanged.
- mcp-bridge-r1: mcp-bridge R1 closed: estate compute moved from zero tools on the live MCP surface to five verbs / six tools any MCP client can call over stdio, with the standing decision now in force that chain repair, dirac bank, driver control words and provider keys are never exposed (R2-R5 unstarted per the design's rollout order).
- bare-spawn-descent: bare-spawn debt under the headless law: tests/ descended to zero bare spawn sites and the accepted register lowered 41 -> 22 (live 43 at lane start), so any new tests/ spawn without creationflags now goes red with zero tests/ headroom; runtime half was already sealed by the conftest default, this closed the static half
- attention-ledger: Attention-market wiring: the trade ledger went from ABSENT with zero trades ever (w4-03; w4-37 T2: absence of trades was uninformative, apathy indistinguishable from broken rails) to proven rails with the market's first two settled trades; POST casts now settle once in the five-signal vocabulary and the next ranking pass provably consumes them, so future zero-trade readings are honest demand signals.
- heads-abliteratus: Janitor-ladder probe order: try P3 (reversible inference-time steering vectors, no weight mutation, hot-swappable) before P2 (permanent weight projection) for the local-janitor refusal-friction fix, both gated on the P1 refusal-census baseline and the named capability battery from row 1, and adopt the verification stage regardless of whether the ablation itself is adopted; second-order change from row 2: violation classes excised by the ratchet keep their downstream detectors enabled instead of closing the watch when the fix lands.
- grave-supersede: no

## 3. Refired and buried

- Refired: none (0). Run metadata refired list is empty; gate ballroom refired count is 0.
- Buried: 1 per the gate sections - abliterate-p1.json, the empty-on-refire shape (no ok, rows=0, checks=0). The run metadata buried list is empty and its lane record marks abliterate-p1 danced ok:true rows:3 (the file carries its battery results and decision under other key names). Gate sections authoritative; contradiction recorded, not averaged (fold's own ruling).
- Banked (evidence-banked, no dance): bare-spawn-descent.json (5 checks, 0 rows), driver-v2.json (7 checks, 0 rows), grave-supersede.json (6 checks, 19 rows).

## 4. Review verdict: REVISE

DECISION: REVISE - the fold's arithmetic, both archives, and 8 of 9 lanes verify cleanly against bytes, but a knowingly self-contradictory verification record (exit 0 on a check that errors) in heads-abliteratus violates the no-fabrication standard the fold itself enforces; correct that one claim before banking.

What passed (review's own runs, transcribed):

- QUOTES PASS (ran all 10, not just 3): python byte-substring check of every quote in heads-abliteratus.json and mcp-bridge-r1.json against its cited source -> heads-abliteratus 5/5 EXACT-BYTES (rows 0-1 vs watch/inbox/ABLITERATUS_DROP_20260929.md; rows 2-4 vs mcp-composition.md / mcp-bridge.md); mcp-bridge-r1 2/5 byte-exact ('estate_ prefix' vs mcp-bridge.md; 'sill=int(n.get("sill", 0))' vs mag/water_graph.py) and 3/5 are faithful wrap-joined reflows - word-identical at mcp-composition.md:45-47 and mcp-bridge.md:135-136/163-164 - with no byte-check claimed for those, so no false claim.
- CHECK FILES 9/9 ON DISK: 8 lanes/*.check.txt plus ball2/graves/grave-supersede.check.txt (named at GALA_GRAVE_grave-supersede.md:7); spot-read contents substantiate the JSONs (attention 18 passed, heads ALL_QUOTES_OK, mcp-bridge PROBE-SUMMARY: 0 failures, bare-spawn CHECK 5 = 47+10+47+16 = 120 passed, driver 30 passed, quantizer kept==packed True). One pointer rot: bare-spawn-descent.json and its check.txt cite lanes/census_before.json / census_after.json but the files actually live in lanes/_qc/ (both exist, contents match 43/22 claims).
- DECISION LEDGERS HONEST + NO CROSS-LANE THEFT: every decision_changed names verifiable disk state - memory/attention_feedback.jsonl has exactly 2 rows both signal 'useful' with 2 distinct cast_ids; state/fuel/stealth_work_queue.jsonl row 1 byte-matches driver-v2's claim (lib-belady-1966, done_ts 2026-09-29T15:18:30.887738+00:00, verdict DONE); mag/constants.py has 'PACK_STALE_DAYS = 7' imported at exactly the 3 claimed sites (thought_quantizer.py:55, context_pack.py:14, freshness_check.py:39); state/fuel/headless_census.json reads bare_spawn_total 22 accepted by the bare-spawn lane; tools/abliterate_p1_probe.py is 348 lines with a banked 60-run battery; ABLITERATUS_DROP names P2/P3 (lines 65/70) as heads' decision requires; grave-supersede honestly says decision_changed 'no'. Ratchet debt attributions verified: commit dbe5f682c exists and its message registers exactly the '2 sibling corpus_acquire.py debts at fold (owner lane owes fix)'; heads' LINKS claim exact (387 total rows, 3 by writer gala-ball-20260929-heads-abliteratus, the only ball-lane writer); the 5 pre-existing x-drop LINKS rows (380-384) belong to free-resource-scout, claimed by no ball lane.
- B-DIVISION FINISH LINES REPRODUCED LIVE (reviewer's own runs): bash fold_gate.sh wave5-repair/lanes 12 -> 12/0/0 GATE PASS exit 0 with decisions_changed 12 (matches the '10 -> 12' claim); bash fold_gate.sh synth_lanes 12 -> 11/0/1 exit 0 with the synth-stuck buried line; bash fold_gate.sh wave5-repair/lanes 11 (negative) -> exit 2, unweakened; _census_bare_spawns.py rerun -> SUMMARY total=22 tests=0 tools=22; tools/thought_quantizer.py --check -> fresh 0.1d exit 0; pytest reruns: tests/test_headless_law.py 2 passed, attention trio 18 passed, tests/test_mcp_bridge_r1.py 22 passed.

The strike:

- STRIKE -> REVISE: heads-abliteratus's CHECK 7 claim 'shared_surface validate exit 0 with pre-existing hash mismatches confined to other lanes' files' is byte-impossible. Reviewer rerun `.venv/Scripts/python.exe -m mag.shared_surface validate` exits 1 (ok:false) with 10 errors: 5 hash mismatches + 5 NEW event-kind LINKS rows. Hash mismatch is an error (mag/shared_surface.py:346) and validate exits 0 iff ok (mag/shared_surface.py:443); the validator is unmodified since commit dbe5f682c (10:19 local, before heads' ~10:47 run); INDEX.json was last stamped 08:27 while the mismatched files changed 08:58/08:59/09:50, so at least 3 hash mismatches predate the lane's run and its recorded 'exit 0' could not have occurred. The confinement half is true (none of the 5 mismatched files are heads-owned), and the lane's actual deliverable (5 byte-verified quotes, 3 LINKS rows) fully verifies - the fix is narrow: re-run validate, record the true exit code and the provenance of the 8 pre-existing errors, or have the fold annotate heads' check as misrecorded.

## 5. Filing verdict: FILED

- memory/corpus/LINKS.jsonl: 8 GALA rows appended (GALA-ball-20260929-fold-gate, -driver-v2, -quantizer-hygiene, -abliterate-p1, -mcp-bridge-r1, -bare-spawn-descent, -attention-ledger, -heads-abliteratus), kind gala, src watch/inbox/gala_20260925/ball-20260929/lanes/<id>.json, lane tag gala-20260925/ball-20260929/<div>, title = the lane's top law where one exists (abliterate-p1: gemma-2b-friction-is-capability-shaped; mcp-bridge-r1: isError in-band, never protocol-level; heads-abliteratus: verify-after-modify with a named battery) else the changed decision, decision_changed verbatim from the lane JSON (bare-spawn-descent's from the ask's summary, corroborated by its baseline_update/conversions since the lane JSON carries no decision key). Dedupe by src ran first: grep over the 190-row ledger showed 0 prior ball-20260929 rows and the writer script re-checked src+id sets before each append (skipped_dupe 0); ledger 190 -> 198, whole-ledger json re-parse OK, em/en-dash scan on the 8 new lines = 0. grave-supersede (division C) got NO LINKS row: its JSON records decision_changed "no" and its 19 rows are grave-register machine rows, not mined law rows.
- ONE STATE entry appended to memories/session/next-window-handoff.md (final line, em-dash scan 0): slug ball-20260929; danced count from the script-written gate (ran: bash watch/inbox/gala_20260925/fold_gate.sh watch/inbox/gala_20260925/ball-20260929/lanes 9 -> GATE PASS rc 0, ballroom_count 8/0/1, by_division B7/A1/C1, byte_checks_cited 46, mined_rows 29); decisions changed 8 by lane content (the gate's key-name map counts 7; named discrepancy: bare-spawn-descent has no decision_changed/decision/decision_ledger key, verified by grep, so the gate cannot see it); B-division finish 7/7 per lane JSON (fold-gate ok, driver-v2 done, quantizer-hygiene ok, abliterate-p1 done, mcp-bridge-r1 ok, bare-spawn-descent done, attention-ledger ok) plus division A heads-abliteratus ok; graves filed 19 (grave-supersede: 19 receipts verified on disk in watch/inbox/ball2/graves/, 23 index_events.jsonl rows under writer gala-grave-supersede-20260929 verified by grep, queue/handoff untouched).
- Two discrepancies flagged in the STATE entry rather than hand-smoothed: the gate's buried branch counts abliterate-p1.json (evidence lives under battery/results/ratchet keys, not ok/checks/rows) and the 7-vs-8 decision count.
- Not run (per the filing record): pytest suite and mag.shared_surface validate were not named by the ask; the 57 em-dash-bearing lines already in the handoff file are pre-existing house prose, untouched.
- Outstanding from the review: the REVISE condition (correct heads-abliteratus's CHECK 7 exit-0 claim - re-run validate and record the true exit code and the provenance of the 8 pre-existing errors, or have the fold annotate heads' check as misrecorded) is not recorded as applied anywhere in this run record; this receipt carries the verdict as given.

## 6. Herald notes for this receipt

- Receipt written by the herald at the ask's exact output path, composed from the ask's script-written sections (authoritative) plus the run's fold/review/filing records carried in the same ask.
- Herald checks run this session (grounding for this receipt only; the run's own checks are transcribed above, not rerun):
  - `ls watch/inbox/gala_20260925/` and `ls watch/inbox/gala_20260925/ball-20260929/lanes/` -> gala dir holds fold_gate.sh and ball-20260929/; lanes dir holds exactly 9 .json lane files (abliterate-p1, attention-ledger, bare-spawn-descent, driver-v2, fold-gate, grave-supersede, heads-abliteratus, mcp-bridge-r1, quantizer-hygiene), 8 .check.txt files (grave-supersede's check.txt lives in ball2/graves/ per the review), census_before.summary.txt / census_after.summary.txt at lanes root and a lanes/_qc/ dir (consistent with the review's pointer-rot note that the lane's JSON cites census_before.json / census_after.json).
  - `ls watch/inbox/gala_20260925/ball-20260929/lanes/*.json | wc -l` -> 9 (matches lanes_json_count 9).
  - Dash/arrow scan on this receipt (U+2014 em / U+2013 en / U+2192 arrow counts): 0 / 0 / 0 (herald, post-write, 22230 bytes)
- Not rerun by the herald (inherited from the run's records, cited above with their original commands): fold_gate.sh runs, pytest reruns, shared_surface validate rerun, byte-substring quote checks, LINKS dedupe grep and re-parse, handoff grep, graves disk verification.
