# f-05: EVENTS.jsonl event taxonomy (census, 2026-09-28)

Item: f-05. Subject: `watch/inbox/EVENTS.jsonl`. Instrument: venv python parses of the
file bytes plus git grep over tracked sources. Every number below comes from a command
run in this session (commands listed at the end). Byte truth at census moment: 43,737
bytes, 58 rows, 0 unparseable lines, sha256
`ae77c7910fb5c397e7c0103aae195d69a3ffbfe194264a5ff592f6ad457ef287`
(`Get-Item` size + `wc -l`-equivalent line count + `sha256sum`, all run 2026-09-28).

## 1. What this file is

The fleet event ledger minted by the B2-28 schema split (2026-09-26): LINKS.jsonl
became link rows only; the 51 event rows that used to cohabit it were mirrored here,
each self-describing with `"schema": "event.v1"` and an `"origin": {"file","line"}`
block naming the LINKS.jsonl line it was copied from. Contract owner:
`mag/link_library.py` (constant `EVENTS` at mag/link_library.py:89; the strict parse
path `load_events()` at mag/link_library.py:180-201 refuses any row without
schema=event.v1 plus an origin dict). The B2-168 split gate
(`mag/links_split_gate.py`) blocks NEW kind rows from entering LINKS.jsonl and
registers its 2 pre-gate stragglers in `configs/links_kind_baseline.json`; that gate
reads LINKS.jsonl only (its `open()` calls at mag/links_split_gate.py:40,94,124 never
open EVENTS.jsonl), so nothing code-side guards the shape of EVENTS.jsonl appends.

Provenance verified from bytes: all 53 schema-bearing rows carry
origin.file = `watch/inbox/LINKS.jsonl`, origin lines 275..334 (51 rows from 275-331
per B2-146, plus the 2 pre-gate rows from 333-334 per B2-168: line 52
ALERT-ORACLE-CUT origin.line=333, line 53 SCOUT-QUIET-LANES origin.line=334).
Cross-check: the B2-28 burn-ledger verdict (memory/burns/LEDGER.jsonl:78) records the
51-row mint with kinds ALERT x8, alert x1, finding x37, correction x1, operator-post
x1, receipt x1, verdict x2; adding the B2-168 pair (1 ALERT + 1 finding) reproduces
this census's schema-bearing counts exactly (ALERT 9, alert 1, finding 38,
correction 1, operator-post 1, receipt 1, verdict 2).

## 2. Kind taxonomy (the event classes)

7 distinct `kind` values across 58 rows:

| kind | rows | share | writers | notes |
|---|---|---|---|---|
| finding | 42 | 72.4% | free-resource-scout 22, x-intel-dig 10, endpoint-news 6, b2-142-cerebras-dig 4 | the workhorse class |
| ALERT | 9 | 15.5% | free-resource-scout 5, endpoint-news 3, x-intel-dig 1 | all 9 carry `severity` |
| correction | 2 | 3.4% | zcode-seat 1, unattributed 1 | line 58 has a different key shape (corrects/correct_state/error/src/note), no writer, no schema |
| verdict | 2 | 3.4% | zcode-seat 2 | GLM rerun day-2 verdicts |
| alert | 1 | 1.7% | zcode-seat 1 | lowercase case-drift twin of ALERT; no severity field |
| operator-post | 1 | 1.7% | zcode-seat 1 | OP-BOOKS-DISAGREEMENT-PUBLIC |
| receipt | 1 | 1.7% | zcode-seat 1 | THE50-REVIEW-FOLD |

Field vocabulary on top of kinds:

- `flag`: 28 distinct values incl. absent (6 rows). Top: verified-live 10, status 7,
  capability-expansion 3; 16 values appear exactly once. Free-text-tag disease: the
  flag namespace is unbounded and ungated.
- `severity`: 7 distinct values incl. absent (49 rows). Present ONLY on the 9 ALERT
  rows: lane-breaking 3, process-debt 2, watch 1, "watch (lanes healthy)" 1
  (a prose value inside a typed field), operator-decision 1, free-compute-loss 1.
- `detail`: present and non-empty on 56/58 rows (mean 277.9 chars). Missing on line 54
  (B2-142-HN-QWEN38-DIG) and line 58 (LINKS-329-CORRECTION).
- `sources`: present on 25 rows (scout/endpoint/x-intel dig rows that cite URLs).

Temporal shape: 2026-09-20 x21, 09-21 x7, 09-22 x5, then silence 09-23/24/25, 09-26
x24 (the burn-wave burst), 09-27 x1 (line 58, 11:27:43Z). Last row predates this
census by ~1 day; the scout charter cadence is 09:00 daily, so 09-28 produced nothing
on file at census time.

## 3. Writers

5 writer ids plus 1 unattributed row. NO CODE WRITES THIS FILE. Verified: the only
module defining the path (`mag/link_library.py:89`) only ever reads it; the
similarly-named writers in `mag/` (`EVENTS_PATH` in mag/memory_events.py:16,
mag/behavioral_synth.py:17, mag/operator_inbox.py:30, mag/vscode_feed.py:35,
mag/board_tailer.py:38) point at OTHER ledgers (logs/memory_events.jsonl,
logs/behavioral_events.jsonl, state/events.jsonl) and must not be confused with this
file. `scripts/endpoint_news.py` writes
`watch/inbox/endpoint_news/endpoint_news.jsonl` (scripts/endpoint_news.py:27-28), not
this ledger; the endpoint-news rows here were appended by the lane, not the script.

| writer | rows | armed by |
|---|---|---|
| free-resource-scout | 27 | watch/inbox/SCOUT_CHARTER_20260926.md (charter v0; event.v1 findings door, kinds finding/ALERT/verdict) |
| x-intel-dig | 11 | watch/inbox/burn_wave_20260926/B2_15_xintel_dig_20260926.md |
| endpoint-news | 9 | EPNEWS receipts (watch/inbox/burn_wave_20260926/B2_35_groq_surgery_20260926.md, B2_114_groq_third_lane_20260926.md, BURN_free-resource-landscape_20260926_h.md and 09-27 siblings) |
| zcode-seat | 6 | workflow seats (THE50 review fold, GLM rerun verdicts, mobile run-card alert, books-disagreement post, one correction) |
| b2-142-cerebras-dig | 4 | watch/inbox/burn_wave_20260926/B2_142_cerebras_dig_20260926.md |
| (none) | 1 | line 58 LINKS-329-CORRECTION carries no writer key |

Per the drift law (watch/inbox/EVENTS_DRIFT_LAW_20260926.md, rule 2) every append
owes a same-critical-section re-register in watch/inbox/index_events.jsonl. Register
state: 3 register rows name EVENTS.jsonl (seq 1789823567015749390 13:15:57Z sha
91D40DDA..., seq 1789823567015749413 13:53:59Z sha 91D40DDA... living-seal, seq
1790458967636140170 2026-09-27T11:38:21Z sha AE77C7910F... writer exp002a purpose
"stale-register heal"). Newest-register sha equals current bytes sha (verified this
session), so rule 1 (newest register is truth) is currently satisfied; the heal
registration is what covers the lines-54-58 appends, not any writer's own
re-register.

## 4. Consumers

Exactly 3 code paths read this file, plus 1 protocol surface and 1 test:

1. `mag/link_library.py:180-201` `load_events()` - THE strict parse path. RUN THIS
   SESSION against the live file: it RAISED
   `ValueError: EVENTS.jsonl row missing schema=event.v1 or origin block:
   B2-142-HN-QWEN38-DIG`. The door is fail-closed on the whole file: one bad row
   makes all 58 rows unreachable through the sanctioned path, not just the 5 bad
   ones.
2. `tools/research.py:28` + search block at tools/research.py:80-96 - the `events`
   source of the research corpus search. Tolerant parser (skips JSONDecodeError),
   kind-blind, emits `watch/inbox/EVENTS.jsonl#<id>` pointers (B2-169 fix).
3. `tools/visor.py:235` - `tail_jsonl("fleet events", watch/inbox/EVENTS.jsonl, 3)`
   on the operator status surface. Prints the last 3 raw lines; right now those are
   lines 56-58, i.e. the status surface is currently showing only schema-less rows.
4. Index register protocol (watch/inbox/index_events.jsonl) - readers per drift-law
   rule 1 compare bytes sha to the newest register row (see section 3).
5. `tests/test_link_library.py:138-155` - exercises `load_events()` against tmp_path
   fixtures only, never the live file, so the live-file rot is invisible to the
   suite (the cataloged `agents/pytest-tmp-*/test_load_events_reads_schema_0/`
   droppings are this test's fixtures).

## 5. Orphan events (the ask's deliverable)

- **Strict-door orphans (5 rows, lines 54-58):** B2-142-HN-QWEN38-DIG,
  B2-142-HN-CODEPLAN-DIG, B2-142-TRIAL-SHAPES-LIVE, B2-142-REDDIT-TRIAL-DECAY
  (writer b2-142-cerebras-dig, no schema/origin/detail on the first), and
  LINKS-329-CORRECTION (no writer, no schema, alien key shape). They violate the
  only strict contract and, because that contract fails closed, they orphan the
  ENTIRE ledger through `load_events()` - proven by running it this session. No
  gate guards future appends (the B2-168 gate reads LINKS.jsonl only), so the next
  schema-less append lands silently the same way.
- **Kind-level orphans (all 7 kinds):** no code anywhere dispatches on `kind` or
  `severity` for this file. Verified by git grep: the only readers are
  load_events/research/visor, and none of them reads those fields. Every kind's
  semantics live purely in prose (SCOUT_CHARTER_20260926.md, B2-28 ledger entry).
  The `severity` field is write-only: 9/9 ALERT rows carry it, 0 readers consume
  it - the same write-only-alert-channel disease the theater audit (F7) found for
  memory/attention.md alert appends.
- **Outside-charter kinds (5 rows, 8.6%):** the scout charter names the vocabulary
  as `finding`, `ALERT`, `verdict` (SCOUT_CHARTER_20260926.md lines 20-21). Rows
  filed outside it: operator-post x1 (line 8), correction x2 (lines 9, 58), alert
  x1 (line 11, the lowercase twin that also drops severity), receipt x1 (line 13).
  No schema doc owns these kinds; they exist only by precedent.
- **Case drift:** ALERT (9 rows, upper) vs alert (1 row, lower) are the same intent
  with different bytes; any future kind-dispatching consumer that matches exactly
  one casing silently drops the other.
- **Flag namespace:** 28 distinct values and climbing, 16 of them singletons, no
  enum anywhere - an ungated vocabulary, orphan by construction since no reader
  interprets any flag value.

## 6. Falsifiers / caveats

- This is a snapshot of one tree at one moment (census denominator law): 58 rows /
  43,737 bytes / sha AE77C791... at 2026-09-28. Armed writers can append at any
  time; per the drift law the newest index register, not this census, is truth.
- I did not fix anything: the 5 schema-less rows stay untouched per the no-erase
  law; repair belongs to the owning lanes (b2-142-cerebras-dig for lines 54-57;
  the line-58 correction's filing lane) as receipted backfills with origin blocks,
  followed by the drift-law re-register. Nothing outside this census was modified.
- The background repo-wide grep was killed after git grep + targeted greps already
  covered tracked sources; any consumer living ONLY in untracked scratch files
  would be missed by both and is not claimed either way.

## 7. Commands run this session (evidence)

- `powershell -NoProfile -Command "(Get-Item 'watch\inbox\EVENTS.jsonl').Length; ...Lines"` -> 43737 bytes, 58 lines
- venv python jsonl parse -> 58 parsed, 0 bad, 7 kinds, writer x kind cross-tab, keysets per kind, id lists per kind
- venv python stats script -> kind/writer/flag/severity/date/distinct counts as cited (flag sum 58, severity sum 58)
- `.venv/Scripts/python.exe -c "from mag.link_library import load_events; ..."` -> ValueError naming B2-142-HN-QWEN38-DIG
- `sha256sum watch/inbox/EVENTS.jsonl` -> ae77c7910fb5... (matches newest register seq 1790458967636140170)
- tolerant index_events.jsonl register listing -> 3 register rows for EVENTS.jsonl
- `git grep -n "EVENTS.jsonl"`, `git grep -n "EVENTS"`, `git grep -n "event.v1"` over code -> consumer/writer map; targeted greps of endpoint_news.py, links_split_gate.py, visor.py, research.py, test_link_library.py
- `sed -n '275p;331p'` + `tail -1` of LINKS.jsonl -> origin projection endpoints confirmed
- Reads: watch/inbox/EVENTS_DRIFT_LAW_20260926.md, watch/inbox/burn_wave_20260926/B2_161_events_drift_policy_20260926.md, watch/inbox/SCOUT_CHARTER_20260926.md, memory/burns/LEDGER.jsonl rows 78/98/125/181/270/275/276/311
