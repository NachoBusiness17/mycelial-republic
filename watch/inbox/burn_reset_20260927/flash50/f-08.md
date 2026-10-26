# f-08 ledger-truth audit: memory/burns/LEDGER.jsonl

Instrument: full read of all 693 ledger rows (0 unparseable), plus a filesystem
existence check of every `landing` path and a ledger-derived supersession pass.
Generator (banked beside this file): `_f08_ledger_audit.py`; every number below is
computed from the bytes by that script run on 2026-09-28, not hand-copied.

Commands run this ask:
```
.venv/Scripts/python.exe -c "<json key/verdict tally over all 693 lines>"   # 693/693 parse, 0 bad lines
.venv/Scripts/python.exe -c "<per-row landing isfile check>"               # 690 OK / 1 compound-OK / 2 MISSING
.venv/Scripts/python.exe -c "<slug repeat + correction-slug pass>"          # 470 unique slugs, 21 multi-row
.venv/Scripts/python.exe -c "<erratum/correction row extraction>"          # 40 rows flagged
find watch -iname "*B2_523*" ; find watch -iname "*ORGAN_CENSUS*"          # both rc=1, zero hits
.venv/Scripts/python.exe _f08_ledger_audit.py                               # generated this file
```

## Headline

- Rows: **693** (lines 1-693, first ts 2026-09-25T10:05:50Z, last ts 2026-09-28T13:45:00Z).
- Unique slugs: 470. Slugs burned more than once: 21 (244 rows live in multi-row slugs).
- Receipt on disk: **691/693** rows (690 plain + 1 compound landing whose primary file exists).
- Rows with NO receipt file on disk: **2** (line 434 and line 554, detailed below).
- Rows whose row-verdict was later corrected/eratized by an appended row: **30** targets of 31 correction rows.
- Rows re-burned later under the same slug (topic re-fired; earlier row historical): **223**.
- Rows with the single status `current` (no correction flag, no re-burn flag): **418**.
- Status cross-tab (flag combinations, computed with the same code that renders the table):

  - 418 x `current`
  - 34 x `re-burned later (latest line 692)`
  - 29 x `re-burned later (latest line 684)`
  - 25 x `re-burned later (latest line 693)`
  - 18 x `re-burned later (latest line 662)`
  - 18 x `re-burned later (latest line 650)`
  - 16 x `re-burned later (latest line 627)`
  - 14 x `re-burned later (latest line 640)`
  - 11 x `re-burned later (latest line 616)`
  - 10 x `re-burned later (latest line 604)`
  - 10 x `re-burned later (latest line 595)`
  - 9 x `re-burned later (latest line 614)`
  - 8 x `re-burned later (latest line 594)`
  - 7 x `re-burned later (latest line 568)`
  - 3 x `re-burned later (latest line 565)`
  - 2 x `re-burned later (latest line 575)`
  - 1 x `corrected by 79; re-burned later (latest line 79)`
  - 1 x `corrects 77`
  - 1 x `corrected by 90`
  - 1 x `corrects 86`
  - 1 x `corrected by 92`
  - 1 x `corrects 91`
  - 1 x `corrected by 108; re-burned later (latest line 108)`
  - 1 x `re-burned later (latest line 107)`
  - 1 x `corrects 105`
  - 1 x `corrected by 296`
  - 1 x `corrected by 122`
  - 1 x `corrects 120`
  - 1 x `corrected by 124`
  - 1 x `corrects 123`
  - 1 x `corrected by 149`
  - 1 x `corrects 148`
  - 1 x `corrected by 161`
  - 1 x `corrects 158`
  - 1 x `corrected by 165`
  - 1 x `corrects 162`
  - 1 x `corrected by 177`
  - 1 x `corrected by 176`
  - 1 x `corrects 175`
  - 1 x `corrects 171`
  - 1 x `corrected by 201; re-burned later (latest line 204)`
  - 1 x `corrected by 205`
  - 1 x `corrected by 204; corrects 198; re-burned later (latest line 204)`
  - 1 x `corrects 201`
  - 1 x `corrects 200`
  - 1 x `corrected by 208,212`
  - 1 x `corrected by 209; corrects 207`
  - 1 x `corrects 208`
  - 1 x `corrected by 214`
  - 1 x `corrects 207`
  - 1 x `corrects 211`
  - 1 x `corrected by 220`
  - 1 x `corrects 218`
  - 1 x `corrected by 223`
  - 1 x `corrects 222`
  - 1 x `corrected by 235`
  - 1 x `corrected by 234`
  - 1 x `corrected by 236`
  - 1 x `corrects 232`
  - 1 x `corrects 230`
  - 1 x `corrects 233`
  - 1 x `corrected by 240`
  - 1 x `corrected by 242; corrects 238`
  - 1 x `corrects 240`
  - 1 x `corrects 110`
  - 1 x `re-burned later (latest line 372)`
  - 1 x `re-burned later (latest line 422)`
  - 1 x `corrected by 530`
  - 1 x `corrects 528`
  - 1 x `corrected by 541`
  - 1 x `corrected by 540`
  - 1 x `corrects 539`
  - 1 x `corrects 536`
  - 1 x `corrected by 606; re-burned later (latest line 594)`
  - 1 x `corrected by 607; re-burned later (latest line 614)`
  - 1 x `corrects 576`
  - 1 x `corrects 579`

- fresh_failure_mode true: 110 rows. lane field: 88 rows. failure_class: 1 row (dict). restore: 2 rows (dicts).
- Ledger contains 0 em-dashes and 0 en-dashes (verified by byte scan of the parsed JSON).

Supersession is judged FROM THE LEDGER, per the burn protocol in
`memory/burns/MANIFEST.json` ("receipt_ledger: memory/burns/LEDGER.jsonl via python
json.dumps"; "do NOT mutate it (append-only), append a CORRECTION row"):

1. **corrected** - a later row names this row/receipt as stale or supersedes its sha
   (erratum/correction chains; the receipt file itself is usually shared and stays on disk).
2. **re-burned** - a later row carries the same slug (round-robin re-fire of the topic;
   the latest row is the live verdict for that item, earlier rows are that fire's record).
3. **current** - neither; nothing later in the ledger touches it.

File-level caveat: receipt CONTENT was not diffed against git history; a receipt that
was silently edited without any ledger row would not be caught by this pass. The
ledger's own protocol says receipts are append-only, and the correction chains do
re-register the original receipt path rather than replacing it (35 receipts are shared
by 74 rows, exactly the chains).

## Receipt gaps (the two rows with no file)

- **Line 434** ts 2026-09-26T21:04:49Z slug `SW-03-board-repair-note` verdict `BOARDFIX`:
  landing names `watch/inbox/burn_wave_20260926/B2_523 (repair row; SW-03 slice receipts all on disk)` - no such file, and no matching
  `B2_523*` / `ORGAN_CENSUS*` filename anywhere under watch/ (find rc=1 both).
- **Line 554** ts 2026-09-27T01:45:55Z slug `b2-wave-fold` verdict `steal`:
  landing names `watch/inbox/ORGAN_CENSUS_20260927.md` - no such file, and no matching
  `B2_523*` / `ORGAN_CENSUS*` filename anywhere under watch/ (find rc=1 both).

Compound landing verified present:
- Line 110 `B2-156-living-hash-law`: landing is a multi-path string; primary file
  `watch/inbox/LIVING_HASH_LAW_20260926.md` exists (6293 bytes), as do the other named files.

## Schema anomalies found

- Line 265 (`B2-... doctor locality seam`): `one_line` is a JSON **list**, not a string - the only
  row in the file whose one_line breaks the string contract. Every consumer that calls
  `.lower()` on it would crash; readers must join it.
- Line 110: `landing` is a prose multi-path string (`file + file + tests ...`) instead of one
  path. Its primary receipt exists, but the shape is off-contract.
- Line 434: landing points at `B2_523` with no extension and no such file - a dangling pointer
  in a BOARDFIX row.

## Verdict families (exact-string tally on top, prefix rules below)

- landed-family: 362
- steal: 200
- free-text: 63
- erratum/correction: 36
- green: 21
- owed: 11

Most common exact verdict strings: `LANDED` x310, `steal` x200, `landed` x19, `green` x21,
`built` x8, `vacuous` x7, `ERRATUM` x7, `CORRECTION` x5, `erratum` x3, `done` x3, `OWED` x3,
`OWED-DORMANT` x3, rest are one-off free-text verdicts (the long landed/steal narratives).

## Rows per day

- 2026-09-25: 23
- 2026-09-26: 517
- 2026-09-27: 108
- 2026-09-28: 45

## Correction chains (row corrected -> correcting rows)

- line 77 (`b2-35-groq-lane-config-surgery`) corrected by lines [79]
- line 86 (`b2-53-grok-lane-packet-fire-card`) corrected by lines [90]
- line 91 (`B2-50-missing-triage`) corrected by lines [92]
- line 105 (`B2-61-roster-purge`) corrected by lines [108]
- line 110 (`B2-156-living-hash-law`) corrected by lines [296]
- line 120 (`B2-70-referee-meter-refresh`) corrected by lines [122]
- line 123 (`B2-72-curvature-order-sensitivity`) corrected by lines [124]
- line 148 (`B2-256-caption-b243-class-pin`) corrected by lines [149]
- line 158 (`B2-246-collect-deep-check-scheduled`) corrected by lines [161]
- line 162 (`B2-247-collect-gap-reconciled`) corrected by lines [165]
- line 171 (`B2-279-fold-sort-totality`) corrected by lines [177]
- line 175 (`B2-79-gap-log-pollution-fix`) corrected by lines [176]
- line 198 (`B2-352-stragglers`) corrected by lines [201]
- line 200 (`B2-353-shell-pin`) corrected by lines [205]
- line 201 (`B2-352-stragglers`) corrected by lines [204]
- line 207 (`B2-88-metadata-fetch`) corrected by lines [208, 212]
- line 208 (`B2-88-metadata-fetch-erratum`) corrected by lines [209]
- line 211 (`B2-93-stego-erratum-20260926`) corrected by lines [214]
- line 218 (`B2-383-chain-quote-pin`) corrected by lines [220]
- line 222 (`B2-374-behavioral-scout-pin`) corrected by lines [223]
- line 230 (`B2-97-width15-probe-no-go`) corrected by lines [235]
- line 232 (`B2-96-scripts-mimosa-triage`) corrected by lines [234]
- line 233 (`B2-95-ratchet-prune-gap`) corrected by lines [236]
- line 238 (`B2-94-mimosa-live-tail-triage`) corrected by lines [240]
- line 240 (`B2-94-self-feed-numbering-erratum`) corrected by lines [242]
- line 528 (`B2-138-pack-retention-law`) corrected by lines [530]
- line 536 (`b2-139-ask3-source-repair`) corrected by lines [541]
- line 539 (`b2-181-seed-mcp-server`) corrected by lines [540]
- line 576 (`judge-lane-spec`) corrected by lines [606]
- line 579 (`b2-wave-fold`) corrected by lines [607]

Erratum-work rows that landed errata into artifacts rather than correcting a ledger row:
lines 56, 65, 68, 78, 211, 288, 308, 347, 384, 413 (413 is a NO_ERRATUM: erratum declined on bytes).

## Per-entry table (all 693 rows)

Columns: ledger line, ts, slug, verdict family, verdict (trimmed 90), item one_line
(trimmed 110, line 265 joined from its list), receipt status with bytes, supersession.

| # | ts | slug | fam | verdict | item (one_line) | receipt | superseded? |
|---|----|------|-----|---------|-----------------|---------|-------------|
| 1 | 2026-09-25T10:05:50Z | free-resource-landscape | steal | steal | Groq free plan now 1K req/day + 200K tok/day (filed 14.4K stale); all 3 fleet groq lanes live 30 RPM; cached ... | OK 2855B | re-burned later (latest line 692) |
| 2 | 2026-09-25T10:05:50Z | judge-lane-spec | steal | steal | both abstracts confirm spec; adds escalate-rate as calibration-drift alarm, judge-must-not-move-its-own-gate ... | OK 3722B | re-burned later (latest line 594) |
| 3 | 2026-09-25T10:05:50Z | prompt-uplift-lane | steal | steal | 5 laws survive VQQA anchor rule except: bibliography laundering under optimizer rewrite (FAIL(BIB_LAUNDER) pa... | OK 3083B | re-burned later (latest line 568) |
| 4 | 2026-09-25T10:17:30Z | judge-lane-spec | steal | steal | build order filed: 3-axis JSON verdict contract w/ confidence + escalation rule (conf<0.7, confident-failure,... | OK 8666B | re-burned later (latest line 594) |
| 5 | 2026-09-25T12:06:25Z | rsi-harness | steal | steal | muratcan beats registry on amendment acceptance (scenario cards from real traces, dual-runtime, incumbent-sta... | OK 3478B | re-burned later (latest line 616) |
| 6 | 2026-09-25T12:06:25Z | adversarial-self-probes | steal | steal | PAT 3-key re-rank survives arXiv 2609.19101 (Sept 2026); steals: detector-miss induction = only sanctioned ta... | OK 3171B | re-burned later (latest line 640) |
| 7 | 2026-09-25T12:06:25Z | queue-field | steal | steal | backlog-as-vector-space vacuous at fleet scale (43 open items, no embedding substrate) but steal real: parse ... | OK 3675B | re-burned later (latest line 604) |
| 8 | 2026-09-25T14:06:12Z | world-models-multi-agent | steal | steal | Agora-2 confirms NPC=SEAT at product grade: entity state in shared server independent of participant view (sw... | OK 3480B | re-burned later (latest line 662) |
| 9 | 2026-09-25T14:06:12Z | roblox-durable-lane | green | green | no Roblox Halloween 2026 platform event announced, Oct 23 dev-run slot + horror-maze durable thesis both hold... | OK 2912B | current |
| 10 | 2026-09-25T14:06:12Z | stego-canon-pipeline | steal | steal | lookup-before-cold-read law paying out (FoJAk3 index, BG census, LSB stego pass, vision triage 100% of 1980);... | OK 3309B | re-burned later (latest line 650) |
| 11 | 2026-09-25T19:09:30Z | steering-theory | steal | steal | gps_50 mapping validated by arXiv 2607.11871 (linear read of internal state predicts judge failure, AUC 0.82 ... | OK 3241B | re-burned later (latest line 595) |
| 12 | 2026-09-25T19:09:30Z | free-resource-landscape | steal | steal | Groq cached-token bypass confirmed official on-doc; NVIDIA post-purge first roster signal (Kimi + DeepSeek + ... | OK 3068B | re-burned later (latest line 692) |
| 13 | 2026-09-25T19:09:30Z | prompt-uplift-lane | steal | steal | VQQA Global Selection confirmed from full text arXiv 2603.12310v1 sec 3.2.2 (rater assesses each candidate ag... | OK 3210B | re-burned later (latest line 568) |
| 14 | 2026-09-25T19:19:25Z | rsi-harness | steal | steal | gateless CONFIRMED from RRSI full text arXiv 2609.24972 (only algorithmic gates: noise floor + cost cap + lea... | OK 3363B | re-burned later (latest line 616) |
| 15 | 2026-09-25T19:19:25Z | adversarial-self-probes | steal | steal | Detector-Miss Induction Protocol drafted: rotated real-receipt probe briefs w/ one measured wild slice, janit... | OK 3720B | re-burned later (latest line 640) |
| 16 | 2026-09-25T19:19:25Z | queue-field | steal | steal | BUILD LANDED: queue/queue_index.jsonl 50 rows (Q-001..Q-050, fields id/ts/source/title/pointer/seat_hint/stat... | OK 3429B | re-burned later (latest line 604) |
| 17 | 2026-09-25T20:11:46Z | world-models-multi-agent | steal | steal | Agora-2 tech report REACHED (agora-2.odyssey.systems/agora-2.pdf, 23pp read): vendor concedes long-horizon un... | OK 3832B | re-burned later (latest line 662) |
| 18 | 2026-09-25T20:11:46Z | stego-canon-pipeline | steal | steal | delta harvest landed: @official_mrpool advanced to post 3823 (posts 3814-3823, self-dated Sept 21-25, 3 new d... | OK 3331B | re-burned later (latest line 650) |
| 19 | 2026-09-25T20:11:46Z | steering-theory | steal | steal | two registry-ready drift_check pair drafts: A conf-margin vs correct/20 on version-hashed 20-task probe (corr... | OK 3621B | re-burned later (latest line 595) |
| 20 | 2026-09-25T22:06:55Z | judge-lane-spec | steal | steal | build advanced to executable drafts off real code: GATE_VERDICT_V2 trail row (nested verdict key, _trail deta... | OK 3940B | re-burned later (latest line 594) |
| 21 | 2026-09-25T22:06:55Z | free-resource-landscape | steal | steal | Groq cache bypass quantified (auto-on, exact prefix match, 128-1024 token minimum, 2h TTL, 50% discount, no t... | OK 3572B | re-burned later (latest line 692) |
| 22 | 2026-09-25T22:06:55Z | prompt-uplift-lane | steal | steal | GEPA primary text (arXiv 2507.19457v2, Observation 4, triple-verified arxiv HTML + ar5iv) INVERTS the pass-b ... | OK 3742B | re-burned later (latest line 568) |
| 23 | 2026-09-25T23:59:00Z | adversarial-self-probes | steal | steal | PAT falsifier MEASURED: 22 ledger rows, 1 identifiable offpeak deep dive excluded (judge build order 10:17:30... | OK 3334B | re-burned later (latest line 640) |
| 24 | 2026-09-26T00:06:31Z | rsi-harness | steal | steal | LAW-12 amendment_gate checklist drafted (LAW-11 slot collision caught: credits_over_failure registered same d... | OK 3918B | re-burned later (latest line 616) |
| 25 | 2026-09-26T00:06:31Z | queue-field | steal | steal | first janitor roam landed: all 9 open janitor rows in queue/queue_index.jsonl roamed and stamped (roamed + ro... | OK 3577B | re-burned later (latest line 604) |
| 26 | 2026-09-26T01:49:50Z | doctrine-owed-chase | steal | steal | 3 of 3 owed targets RESOLVED: (a) Kol HaTor end of ch.4 retrieved verbatim (Yedid Nefesh trans): the end-calc... | OK 3411B | re-burned later (latest line 693) |
| 27 | 2026-09-26T01:49:50Z | third-way-game | steal | steal | playtest addendum drafted keyed to real PLAYTEST.md pattern: 20-min beats (war entry -> loop -> Wall -> 42 Do... | OK 3845B | re-burned later (latest line 627) |
| 28 | 2026-09-26T01:49:50Z | middle-path-doctrine | steal | steal | C9 SHARING PROTOCOL drafted at both layers: fleet (gated canon drops priced by a pre-registered falsifier; se... | OK 3547B | re-burned later (latest line 684) |
| 29 | 2026-09-26T01:54:04Z | middle-path-doctrine | steal | steal | C8 SCOPED: the crime is end-computation divorced from deeds (Kol HaTor ch.4 verbatim: curse narrowed to compu... | OK 7503B | re-burned later (latest line 684) |
| 30 | 2026-09-26T02:12:04Z | steering-theory | steal | steal | drift.py has NO registry (stateless drift_check(metric, referent, window, label) is the whole contract): pair... | OK 4554B | re-burned later (latest line 595) |
| 31 | 2026-09-26T02:12:04Z | stego-canon-pipeline | steal | steal | 3 dictionary entries landed via lookup-before-cold-read: TEN DAYS OF DARKNESS = Q drop 88 EBS prophecy w/ pri... | OK 3811B | re-burned later (latest line 650) |
| 32 | 2026-09-26T02:12:04Z | world-models-multi-agent | steal | steal | MSEAT-DRIFT probe SPEC landed for Mirror Sea MUD: per-seat entity-state accuracy vs memory/game/world/world_s... | OK 3905B | re-burned later (latest line 662) |
| 33 | 2026-09-26T04:11:39Z | free-resource-landscape | steal | steal | NVIDIA roster advanced to primary: featured 4 confirmed (Kimi, DeepSeek, Nemotron x2, no Llama), unauthentica... | OK 4098B | re-burned later (latest line 692) |
| 34 | 2026-09-26T04:11:39Z | judge-lane-spec | steal | steal | 50-wide falsifier baseline MEASURED: infra share 39/41 = 95.1%, but the taxonomy census table sums to 42 vs i... | OK 3706B | re-burned later (latest line 594) |
| 35 | 2026-09-26T04:11:39Z | prompt-uplift-lane | steal | steal | FAIL(BIB_LAUNDER) patched from name to shippable draft: one invariant-section line per prompt file (FACTS/SOU... | OK 3813B | re-burned later (latest line 568) |
| 36 | 2026-09-26T04:20:26Z | gala-36-lane-self-steal | steal | steal | 36/36 lanes: last-24h systems self-stolen, owed waltz danced, fossils buried, envelope measured 3-6-12 clean,... | OK 5229B | current |
| 37 | 2026-09-26T06:11:38Z | doctrine-owed-chase | steal | steal | 3 of 3 resolved AGAIN: Porete annihilated-soul passages fetched (Babinsky trans, archive.org OCR of 1993 Paul... | OK 3484B | re-burned later (latest line 693) |
| 38 | 2026-09-26T06:11:38Z | third-way-game | steal | steal | build advanced paper -> data shape: THIRD_WAY_BOONS_STUB.json (all 12 MUD boons with Third Way fields: god_fa... | OK 4136B | re-burned later (latest line 627) |
| 39 | 2026-09-26T06:11:38Z | middle-path-doctrine | steal | steal | C8 falsifier MEASURABLE: 19 receipts-attached vs 17 bare LEDGER rows (28 vs 68 combined w/ LINKS tail), both ... | OK 3499B | re-burned later (latest line 684) |
| 40 | 2026-09-26T08:06:35Z | adversarial-self-probes | steal | steal | first DMIP probe queue filed (selection only, no attack executed): 3 receipts seeded one per PAT key (judge-l... | OK 3598B | re-burned later (latest line 640) |
| 41 | 2026-09-26T08:06:35Z | queue-field | steal | steal | builder-seat roam: 5 priority open rows (Q-009, Q-010, Q-030, Q-041, Q-042) stamped in place, 14 total roamed... | OK 2879B | re-burned later (latest line 604) |
| 42 | 2026-09-26T08:06:35Z | rsi-harness | steal | steal | LIVE AMENDMENT DRILL: LAW-12 checklist run retroactively against the real workflow-gate amendment (tools/work... | OK 3420B | re-burned later (latest line 616) |
| 43 | 2026-09-26T10:12:00Z | steering-theory | steal | steal | runner EXECUTED: tools/probe20_run.py live-verified importing tools/drift.py, seed PROBE20_steering_v1.jsonl ... | OK 3541B | re-burned later (latest line 595) |
| 44 | 2026-09-26T10:12:00Z | stego-canon-pipeline | steal | steal | dual-numbering RESOLVED and worse than drift: the harvest ledger (watch/inbox/mrpool_export/ledger_full.jsonl... | OK 3710B | re-burned later (latest line 650) |
| 45 | 2026-09-26T10:12:00Z | world-models-multi-agent | steal | steal | MSEAT-DRIFT executable: MSEAT_DRIFT_FIXTURE_v1.json built (139-key authoritative census from world_state.json... | OK 3458B | re-burned later (latest line 662) |
| 46 | 2026-09-26T10:54:38Z | afterparty-94-lane-churn | steal | steal | 94 afterparty lanes banked, battery 12/12 twice + harness graduation, seals+registry green, window closed by ... | OK 6407B | current |
| 47 | 2026-09-26T11:45:00Z | link-dupes-triage | green | green | link ledger triaged append-only: 9 clusters over 305 rows; 3 already flagged true dupes, 5 silent dupes (arxi... | OK 4387B | current |
| 48 | 2026-09-26T11:34:25Z | b2-10-playtest-prereg | free-text | prereg gated; one red finding: shipped rbxlx stale, missing t74 UpdateAsync + t67 join + ... | Sep-29 playtest prereg P0-P7 built with pass/fail + falsifier per item; P0 = mountain_check rebuild then grep... | OK 4357B | current |
| 49 | 2026-09-26T12:00:00Z | judge-lane-spec-deep-dive | steal | steal | Judge-lane spec v2 from full-text reads of arxiv 2609.26550 (JEV cascade) + 2604.24842 (Co-Director factored ... | OK 4526B | current |
| 50 | 2026-09-26T11:37:50Z | endpoint-news-pass2 | steal | steal | pass 2 verified all 7 free lanes from official docs + 3 read-only live probes: Groq 1K RPD / 200K TPD confirm... | OK 4210B | current |
| 51 | 2026-09-26T12:25:00Z | b2-02-writer-debt-backfill | landed-family | landed: 235 register events appended (writer b2-02-writer-debt-20260926, nonces 1-235, 8 ... | 229+3+1 fold-left-unregistered inbox files registered via index_fold_host.mjs pattern from cwd watch/inbox wi... | OK 3944B | current |
| 52 | 2026-09-26T11:39:24Z | provider-health-free-lane-probe | steal | steal | 8 of 16 keyed free lane-keys answered live (groq, openrouter x2, nous, together, cohere, zai Pro/Lite); 6,890... | OK 6229B | current |
| 53 | 2026-09-26T11:45:00Z | b2-07-grounding-chain-resync | landed-family | landed: grounding_chain f0e992d3e run live 3 cycles; research+build fired x3, tender_sign... | stale locks 2 found 2 cleared (Sep-18 run.lock age 710394s self-cleared by driver; 2026-09-26 stranded lock f... | OK 3788B | current |
| 54 | 2026-09-26T12:00:00Z | prompt-uplift-lane | steal | steal | third pass resolves all three OWED items full-text: VQQA 2603.12310 re-verified first-hand (judge anchored to... | OK 4400B | re-burned later (latest line 568) |
| 55 | 2026-09-26T11:39:59Z | teleo-drift-pairs-t4-t6 | steal | steal | T4-T6 teleological drift pairs landed in tools/drift_pairs_stamp.py and stamped W39: T4 lane_grind_vs_release... | OK 4478B | current |
| 56 | 2026-09-26T11:44:06Z | b2-01-the50-punch | erratum/correction | landed: wave-2 audit FIX-1 (T42 endpoint-news receipt churn inverted vs ledger) fixed fro... | T42 receipt churn sentence + one_line_proof rewritten from endpoint_news.jsonl:499-502 (added perceptron/perc... | OK 4327B | current |
| 57 | 2026-09-26T11:53:23Z | b2-17-adventure2d6-settlement-verify | free-text | confirmed: all six region cosines (incl. adventure_2d6 0.483) reproduce from raw normals ... | B2-17 referee settlement re-derived from bytes: watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260921.json:33 cos 0.4... | OK 4358B | current |
| 58 | 2026-09-26T13:05:00Z | b2-16-uf-sweep | landed-family | swept: UF-127 landed (honest self-flagged cache matrix), UF-128 landed with defect (junct... | all 27 raw.jsonl rows for UF-124..131 read and error bodies extracted from state.json:132-136 + queue.jsonl:1... | OK 4216B | current |
| 59 | 2026-09-26T11:54:42Z | B2-15-xintel-dig-20260926 | free-text | 56pct figure confirmed in RESEARCH_GAP_ANALYSIS_20260918.md; two thinnest families (windo... | Thin x-intel families (swarm economics, windows reparse law) got their prior-art floor: jitter+retry-budget+c... | OK 4201B | current |
| 60 | 2026-09-26T11:55:38Z | b2-20-loop-gaps-drain | landed-family | landed | loop_gaps.jsonl triaged 304/304 rows read: 293 infra (96.4 pct lifecycle_gap 175 + lifecycle_waste 102 + miss... | OK 4003B | current |
| 61 | 2026-09-26T11:58:04Z | b2-18-stone2b-7fix-recheck | free-text | 7/7 fixes hold at HEAD 77b887483, zero regressions; adjacent drift named: verkle tip stal... | stone2b 7 fixes re-verified against current bytes: pile write-back code+tests live, both chain flags present ... | OK 4892B | current |
| 62 | 2026-09-26T12:10:00Z | B2-19-improve-backlog-20260926 | free-text | 69 pending candidates triaged: 3 real (promote c-5074b7228c67 write_file FKB, c-b341f669f... | Improve backlog is a stale telemetry mirror: scout dead since 2026-08-31, FKB signatures index reset 2026-09-... | OK 4689B | current |
| 63 | 2026-09-26T12:05:00Z | B2-14-qdrop874-gap-20260926 | free-text | gap DISSOLVES, nothing owed: canonical drop #874 = Snowden HK post (8ch post 580331, 2018... | qdrop 874 sourcing pass over qalerts + qagg + wayback + local bytes: the one true gap was a numbering misiden... | OK 4622B | current |
| 64 | 2026-09-26T12:01:03Z | b2-12-caption-ledger | landed-family | landed: CAPTION_LEDGER_20260926.jsonl 2726 rows (one per media id, cite @MrPool_Q#N dual-... | caption ledger built from existing metadata only, zero model calls zero media reads: watch/inbox/CAPTION_LEDG... | OK 4920B | current |
| 65 | 2026-09-26T13:05:00Z | B2-11-mimosa-close-20260926 | erratum/correction | close landed with count correction: brief said 33 SSRF/path in archived 09-16 scripts, se... | mimosa L3 close on bytes not the brief: 30 not 33 findings, all dead watch/inbox one-shots, accepted by name ... | OK 4817B | current |
| 66 | 2026-09-26T12:03:52Z | b2-13-workflow-gate-scenario-cards | landed-family | landed | LAW-12 genesis clause executed inside window: 7 scenario cards (G1-G7) minted under configs/workflow_gate_sce... | OK 3864B | current |
| 67 | 2026-09-26T12:09:06Z | b2-25-envelope-remeasure | steal | steal | width-10 rung MEASURED CLEAN from this burn own lane data: wave 1 (B2-01..10, all fired 11:24:57Z) 10/10 comp... | OK 4148B | current |
| 68 | 2026-09-26T12:10:07Z | b2-23-seed-drive-flip-card | erratum/correction | landed: flip card + checklist for the seed-3.2.0 Drive link flip (card only, nothing re-z... | operator card: hash gate e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e -> browser upload t... | OK 4249B | current |
| 69 | 2026-09-26T12:14:31Z | free-resource-landscape | steal | steal | Cerebras slot CLOSED as corrected at primary: inference-docs.cerebras.ai/support/rate-limits renders and CONF... | OK 3166B | re-burned later (latest line 692) |
| 70 | 2026-09-26T12:14:31Z | judge-lane-spec | steal | steal | second C8 check ran at LEDGER row 65 (doubled since _d): failure_class adopted by ZERO writers (0 rows); clas... | OK 3509B | re-burned later (latest line 594) |
| 71 | 2026-09-26T12:14:31Z | doctrine-owed-chase | steal | steal | 2 of 3 resolved: (a) Kol HaTor literal mitzvah wording = DECISIVE NEGATIVE: Sefaria hard-errors (Kol HaTor en... | OK 3738B | re-burned later (latest line 693) |
| 72 | 2026-09-26T12:17:23Z | b2-22-corpus-fts5-spike | landed-family | landed, target beaten: external-content FTS5 index built over catalog/catalog.jsonl (757,... | UF-120 spike executed on real bytes: watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py built catalog/catalog... | OK 3886B | current |
| 73 | 2026-09-26T12:25:07Z | b2-21-doctor-probe-wiring | landed-family | landed: mag/doctor.py check_provider_endpoints() extended with the B2-04 deep remote prob... | doctor deep probe wired to the B2-04 measured classes: default path still sends zero bytes, opt-in ping costs... | OK 4540B | current |
| 74 | 2026-09-26T12:40:00Z | b2-24-carrier-ledger-activation-scan | free-text | 0/7 signals fired post-ledger (2026-09-19T04:50Z to 2026-09-26T12:30Z): 1 ambiguous (FoJA... | carrier ledger v1 activation audit over 156 post-ledger LINKS rows plus settlement/gstdbot audits, fojak_boom... | OK 4906B | current |
| 75 | 2026-09-26T12:29:43Z | b2-29-rbxlx-rebuild-verify | landed-family | landed: bash tools/mountain_check GATE PASS (0 parse failures, 9 unique findings all acce... | P0 rebuild gate executed per B2-10 prereg: rbxlx rebuilt from 790145ab1 src, t74 UpdateAsync + t72 annotation... | OK 3095B | current |
| 76 | 2026-09-26T12:32:12Z | b2-32-gate-verdict-v2-cascade-wire | landed-family | landed: gate_verdict_v2 block appended to configs/lanes.yaml (lines 110-145), config regi... | GATE_VERDICT_V2 two-band cascade frozen at registration in configs/lanes.yaml per the B2_08 owning spec (rout... | OK 4314B | current |
| 77 | 2026-09-26T12:35:12Z | b2-35-groq-lane-config-surgery | landed-family | landed: providers.yaml groq models now [openai/gpt-oss-120b, qwen/qwen3.8-27b]; qwen/qwen... | groq lane surgery per LINKS ALERT-GROQ-FLEET-IDS-GONE: live-confirmed qwen3.8-27b as the only qwen and no com... | OK 4045B | corrected by 79; re-burned later (latest line 79) |
| 78 | 2026-09-26T12:35:16Z | b2-28-ledger-schema-split | erratum/correction | landed: watch/inbox/EVENTS.jsonl minted as the canonical event ledger (schema event.v1), ... | schema split executed append-only: 51 event rows (not 31, endpoint-news grew it) duplicated into watch/inbox/... | OK 4091B | current |
| 79 | 2026-09-26T12:36:21Z | b2-35-groq-lane-config-surgery | erratum/correction | correction to the row above: the self-feed numbers B2-111/112/113 claimed there were take... | queue-number correction only: B2-35 self-feed renumbered to B2-114/115/116 after concurrent-lane collision on... | OK 4045B | corrects 77 |
| 80 | 2026-09-26T12:37:32Z | b2-33-rejection-recount | landed-family | landed | denominator FROZEN at 41 from the write-time committed snapshot (git 3d12289f9, 71 rows, 41 verdict FAIL): he... | OK 4374B | current |
| 81 | 2026-09-26T12:40:09Z | b2-31-poll-tripwire | landed-family | landed: two advisory disease checks added to tools/luau_lint.py per spec filed FIRST in r... | poll+RMW disease tripwire landed in luau_lint.py (advisory, prints at mountain_check step 1), spec-first in P... | OK 4088B | current |
| 82 | 2026-09-26T12:43:58Z | B2-27-scout-checkgate-20260926 | landed-family | landed: python -m mag.link_library check wired into the free-resource-scout filing path a... | The scout (an agent writer with no script, proven by repo + schtasks census) lost its bypass: all 21 scout li... | OK 3802B | current |
| 83 | 2026-09-26T12:45:00Z | b2-26-links-sha-backfill | landed-family | landed: all 110 PENDING-URL rows in watch/inbox/LINKS.jsonl backfilled field-only via mag... | 110 PENDING-URL shas recomputed field-only, 8 single-canonical collision groups reported, L265 silent dupe an... | OK 4747B | current |
| 84 | 2026-09-26T12:50:22Z | b2-30-shadowledger-sim-20260926 | landed-family | simulation landed, live proof still owed: real HEAD + real pre-t74 (5e291421a) ShadowLedg... | Studio automation unavailable so the static equivalent ran the REAL luau bytes under the repo luau.exe: t74 U... | OK 3915B | current |
| 85 | 2026-09-26T12:51:08Z | B2-52-off-machine-bridge-card | landed-family | landed: HARD FINDING proven from host bytes on all three axes (fsutil reparsepoint query ... | the 09-19 sync protocol was never executed here (proven byte-level) and the exact 7-step operator-GO card now... | OK 4076B | current |
| 86 | 2026-09-26T12:52:56Z | b2-53-grok-lane-packet-fire-card | landed-family | fire-ready with three amendments: scope GO to asks 2-4 only (Ask 1 already landed UNSOUND... | fire card for the unfired Grok 4.7 seat packet: Ask 1 already fired via harness/grok_cli.py (VERDICT UNSOUND ... | OK 5006B | corrected by 90 |
| 87 | 2026-09-26T08:52:00Z | B2-37-provider-health-close-20260926 | landed-family | closed, no rebuild: watch/inbox/PROVIDER_HEALTH_20260926.md exists (landed by B2-04, 6140... | Receipt verified against probe bytes claim by claim: totals and dead-lane statuses all match, one scoreboard ... | OK 4162B | current |
| 88 | 2026-09-26T12:55:12Z | B2-36-cerebras-reclassify | landed-family | LANDED | Cerebras moved off the standing free-lane ladder to card-gated 30-day trial: providers.yaml prefer_order + al... | OK 4416B | current |
| 89 | 2026-09-26T12:56:57Z | b2-54-cron-arm-card-20260926 | landed-family | card landed, nothing armed (card only per order; lane holds no automation seat and FLEET_... | arm card for the Sunday 06:30 essentials pack refresh: the creation recipe is not in ESSENTIALS_RESTORE.md (r... | OK 4977B | current |
| 90 | 2026-09-26T13:00:01Z | b2-53-queue-number-correction | erratum/correction | correction to the b2-53 row above: self-feeds first claimed B2-125/126/127 against a stal... | queue repair: 4 of 6 accidentally deleted concurrent-lane briefs restored verbatim from owning scripts, 2 fil... | OK 4672B | corrects 86 |
| 91 | 2026-09-26T13:02:19Z | B2-50-missing-triage | landed-family | LANDED | missing-triage sweep closed: INDEX vs index_events fold-exact diff found 3 files with broken triage; FRONTDOO... | OK 3927B | corrected by 92 |
| 92 | 2026-09-26T13:03:17Z | B2-50-missing-triage-renumber | erratum/correction | correction | self-feed briefs from the B2-50 row above were first filed as B2-142/143 and collided with concurrent lanes c... | OK 3927B | corrects 91 |
| 93 | 2026-09-26T13:12:32Z | B2-51-autorun-autopsy | landed-family | LANDED | governor_autorun autopsy (owed 9/19) run from bytes: the 9/19 17:31Z loop was a false crash-loop, DOCKER_ONLY... | OK 4778B | current |
| 94 | 2026-09-26T13:14:01Z | B2-58-prompt-amendments-20260926 | landed-family | LANDED | prompt-law v2 amendments landed in roblox/prompts/README.md (74 insertions, 0 deletions, no code): law 1 spli... | OK 5098B | current |
| 95 | 2026-09-26T13:14:47Z | B2-145-phantom-paths | landed-family | LANDED | absolute-path phantom sweep closed: INDEX.json carried 5 items registered under the absolute host root C:/Use... | OK 4175B | current |
| 96 | 2026-09-26T13:20:00Z | B2-56-returncode-law | landed-family | LANDED | returncode law landed: grounding_chain.py now appends its row after the fires and records child exit_code (or... | OK 4257B | current |
| 97 | 2026-09-26T14:55:00Z | b2-57-uf119-uf122-promotion-check | landed-family | landed: UF-119 answer 3 of 8 attacks survive byte-check (5 tail undercount with corrected... | promotion check via live probes through the real corpus tools: 2 attacks promoted, 4 refuted, spec scaffold p... | OK 4134B | current |
| 98 | 2026-09-26T13:18:21Z | unregistered-files | steal | steal | 5 unregistered inbox files registered via index_fold_host.mjs add (EVENTS.jsonl DATA, vault pack artifact, 3 ... | OK 4355B | current |
| 99 | 2026-09-26T13:21:48.942927Z | B2-55-buildlane-flip | landed-family | LANDED | build lane model flip: stealth/union-alpha provider-dead (12 HTTP 404 rows 2026-09-26, proposals.jsonl:100-11... | OK 4254B | current |
| 100 | 2026-09-26T13:22:15Z | b2-34-cluster-organ-detectors | landed-family | landed: CLUSTER_REPORT cluster organ + the two B2-34 detectors wired into mag/lane_runner... | cluster-organ detectors landed spec-first in the lane runner: fos + caw detectors, min-events rate law, pipe_... | OK 4603B | current |
| 101 | 2026-09-26T13:22:43Z | B2-42-events-hygiene | landed-family | LANDED | events-log hygiene closed: lines 94-96 of index_events.jsonl confirmed the only malformed lines in the log (p... | OK 4744B | current |
| 102 | 2026-09-26T13:29:33Z | B2-63-gemini-auth-shape | landed-family | LANDED | gemini auth shape identified byte-level: the AQ.Ab8... key is a Vertex express-mode key, permanently 401 on g... | OK 4821B | current |
| 103 | 2026-09-26T13:40:00Z | B2-41-hash-freshness | landed-family | LANDED | hash-freshness sweep closed: of the 27 stale rows the brief named, 23 were refreshed by drift-patrol-cron 12:... | OK 4342B | current |
| 104 | 2026-09-26T13:34:37Z | B2-59-miprov2-dig | free-text | hold: amendments neither stolen nor vacuous; F1 not triggered | MIPROv2 full-text dig live (arXiv 2406.11695 v2 HTML 572297 bytes, EMNLP 2024, paper names it MIPRO, string M... | OK 4586B | current |
| 105 | 2026-09-26T13:35:26Z | B2-61-roster-purge | landed-family | LANDED | providers.yaml roster purge landed config-only on live 2026-09-26 bytes, one verification call per change bef... | OK 4646B | corrected by 108; re-burned later (latest line 108) |
| 106 | 2026-09-26T13:35:30Z | B2-60-judge-independence | landed-family | LANDED | judge-independence sweep under the VisualPrompter Appendix L same-VLM lens: REGISTRY.jsonl clean (19 rows, al... | OK 4681B | re-burned later (latest line 107) |
| 107 | 2026-09-26T13:36:24Z | B2-60-judge-independence | landed-family | LANDED | judge-independence sweep under the VisualPrompter Appendix L same-VLM lens: REGISTRY.jsonl clean (19 rows, al... | OK 4681B | current |
| 108 | 2026-09-26T13:37:10Z | B2-61-roster-purge | landed-family | LANDED | CORRECTION of the prior B2-61 row (last-wins), one field only: the self-feed briefs landed as B2-202/203/204 ... | OK 4646B | corrects 105 |
| 109 | 2026-09-26T13:37:38Z | B2-65-registry-revival | landed-family | LANDED | VERSION_REGISTRY release trail revival: death diagnosed (writers were mag/roadmap_runner.py:278 roadmap passe... | OK 4030B | current |
| 110 | 2026-09-26T13:41:16Z | B2-156-living-hash-law | landed-family | LANDED | Living-file hash law: sealed living (add --living, sha256+size prefix seal) and open living (add --living-ope... | OK-compound 6293B | corrected by 296 |
| 111 | 2026-09-26T13:43:42Z | B2-157-composed-prefix-case | landed-family | LANDED | Composed-prefix normalization (closes B2-149 + B2-157): normInboxFile strips the board/app/inbox prefix AND t... | OK 4225B | current |
| 112 | 2026-09-26T13:45:32Z | B2-40-fold-poison-guard | landed-family | LANDED | fold poison guard landed: OUTSIDE_RE register drops now surface as fold_warnings on the WARN+exit-2 channel (... | OK 4669B | current |
| 113 | 2026-09-26T13:47:41Z | B2-40-fold-poison-guard-addendum | landed-family | LANDED | addendum to the B2-40 row (all prior facts stand as of their ts): while B2-40 was closing, lane B2-157 sharpe... | OK 4669B | current |
| 114 | 2026-09-26T14:05:00Z | B2-198-owed-b2-41-receipt | free-text | DISCHARGED | owed B2-41 receipt discharged: the receipt the brief called missing exists (watch/inbox/burn_wave_20260926/B2... | OK 4222B | current |
| 115 | 2026-09-26T13:48:49.896429Z | B2-62-zai-backoff-floor | landed-family | LANDED | z_ai lane client 1305 adaptive backoff + reasoning budget floor landed (closes the B2-04 measured scars): spe... | OK 4608B | current |
| 116 | 2026-09-26T13:49:31Z | B2-66-referent-aging-guard | landed-family | LANDED | referent-age guard landed spec-first in tools/drift_pairs_stamp.py: every stamp row now carries referent_age_... | OK 4818B | current |
| 117 | 2026-09-26T13:51:52Z | B2-69-test-census-recount | landed-family | landed | Recount pytest --collect-only -q: 1,837 tests collected / 301 files, exit 0; 1,341 headline retired as hand-c... | OK 4449B | current |
| 118 | 2026-09-26T13:52:42Z | B2-68-caption-fraction-guard | landed-family | LANDED | proportion guard landed spec-first in scripts/the50_t21_q_caption_ledger.py: proper fraction (numerator<denom... | OK 4112B | current |
| 119 | 2026-09-26T14:58:00Z | B2-199-patrol-living | landed-family | LANDED | drift-patrol-cron living-law adoption: the patrol is ZCode automation automation-a7c71ad1-f43f-403d-8677-105f... | OK 4464B | current |
| 120 | 2026-09-26T13:54:08Z | B2-70-referee-meter-refresh | landed-family | LANDED | referee brief meter refreshed append-only: dated ADDENDUM appended to watch/inbox/REFEREE_VERDICT_20260926.md... | OK 3832B | corrected by 122 |
| 121 | 2026-09-26T13:54:54Z | B2-64-drift-dashboard | landed-family | LANDED | Drift board T1-T6: spec filed first (docs/DRIFT_BOARD_SPEC.md) then tools/drift_dashboard.py renders dashboar... | OK 4185B | current |
| 122 | 2026-09-26T13:55:55Z | B2-70-referee-meter-refresh-correction | erratum/correction | CORRECTION | corrects the B2-70-referee-meter-refresh row filed minutes earlier: its closing clause named self-feeds B2-21... | OK 3832B | corrects 120 |
| 123 | 2026-09-26T13:56:11Z | B2-72-curvature-order-sensitivity | landed-family | LANDED | keyword-order sensitivity measured, settlement NOT order-robust: probe reproduces all 6 filed cosines bit-for... | OK 4348B | corrected by 124 |
| 124 | 2026-09-26T13:57:51Z | B2-72-self-feed-renumber | erratum/correction | ERRATUM | the B2-72 ledger row said self-feeds B2-224, B2-225, B2-226; a live queue race claimed B2-224 through B2-228 ... | OK 4348B | corrects 123 |
| 125 | 2026-09-26T13:58:13Z | living-census | landed-family | LANDED with one owed alarm | Living-law census: 3 static append-only originals reclassified sealed living (EVENTS.jsonl, verb_trace.jsonl,... | OK 4642B | current |
| 126 | 2026-09-26T13:59:19Z | B2-67-qvision-b1-audit-fixes | landed-family | LANDED | wave-2 audit batch 1.2 defects 1-3 fixed in Q_VISION_TRIAGE_B1.json from bytes: findings[1] numerator reconci... | OK 4278B | current |
| 127 | 2026-09-26T14:07:46Z | B2-223-mimo-living | free-text | CONFIRMED on bytes, left static by design | mimo_watch.jsonl byte-proven append-only: 09-22 10:29:36Z register sha 45CB3100 equals sha256 of newline-alig... | OK 6350B | current |
| 128 | 2026-09-26T14:08:23Z | third-way-game | steal | steal | GRACE schema debt CLOSED: THIRD_WAY_GRACE_SCHEMA.json (draft 2020-12, additionalProperties false, 9 required ... | OK 3166B | re-burned later (latest line 627) |
| 129 | 2026-09-26T14:08:23Z | middle-path-doctrine | steal | steal | C8 citation correction LANDED: deeds/computation distinction stays verbatim now cited as Kol HaTor per the Ye... | OK 4103B | re-burned later (latest line 684) |
| 130 | 2026-09-26T14:08:23Z | adversarial-self-probes | steal | steal | PROBE-A tabletop EXECUTED paper-only: forged the judge-lane-spec fee-fold false-success (verbatim 0.36% swapp... | OK 3748B | re-burned later (latest line 640) |
| 131 | 2026-09-26T14:10:53Z | B2-220-caption-ledger-dotted-guards | landed-family | LANDED | DOT_NOY sibling guards landed in scripts/the50_t21_q_caption_ledger.py: QUANTITY now covers yr/yrs units (id ... | OK 7378B | current |
| 132 | 2026-09-26T14:10:55Z | B2-71-adventure2d6-hill-build | landed-family | LANDED | adventure_2d6 builder agreement raised across the 0.5 HILL bar honestly: two live builder seats (groq gpt-oss... | OK 4586B | current |
| 133 | 2026-09-26T14:14:07Z | hot-living-build-lane | steal | steal | B2-222 LANDED: both hot unregistered build-lane originals registered sealed living (add --living, writer zcod... | OK 7014B | current |
| 134 | 2026-09-26T14:14:37Z | B2-216-collected-executed-delta | landed-family | LANDED | collected-vs-executed delta attributed from bytes: census 1,837/301 (B2-69, ~09:49 EDT, exit 0) vs executed s... | OK 7044B | current |
| 135 | 2026-09-26T14:15:40Z | B2-219-caption-ledger-misdate-classes | landed-family | LANDED | caption ledger dash-pair unit/tally/reference guards landed: byte audit of the 31 residual 0.65 rows split 15... | OK 6475B | current |
| 136 | 2026-09-26T14:16:22Z | B2-215-census-freshness-tripwire | landed-family | LANDED | census-carrier tripwire landed: tools/census_drift_patrol.py flags the AGENTS.md Tests bullet STALE when its ... | OK 5987B | current |
| 137 | 2026-09-26T14:33:35Z | B2-245-census-parser-order-fragility | landed-family | LANDED | census carrier parser order-fragility closed: parse_carrier reads ONLY the parenthesized census clause (new C... | OK 6603B | current |
| 138 | 2026-09-26T14:33:45Z | B2-244-collect-deep-check | landed-family | LANDED | collected-count deep check landed as opt-in --collect on tools/census_drift_patrol.py: runs pytest --collect-... | OK 8034B | current |
| 139 | 2026-09-26T14:38:02Z | B2-236-mimo-retest-403 | landed-family | LANDED | mimo 403 retest under the UA fix: B2-235 sequence landed first (add --living sealed the prior 492 bytes, even... | OK 9311B | current |
| 140 | 2026-09-26T14:38:47Z | B2-238-self-feed-checkbox-law | landed-family | LANDED | self-feed checkbox law codified in QUEUE.md header: dispatcher outstanding defined as unchecked Open rows wit... | OK 5681B | current |
| 141 | 2026-09-26T14:40:53Z | B2-243-caption-bucket-audit-05-075 | landed-family | LANDED | caption ledger residual buckets audited against qdrops.jsonl bytes: 0.5 bucket 15/15 keepers (all genuine Q c... | OK 13723B | current |
| 142 | 2026-09-26T14:41:10Z | B2-244-guard-class-regression-pin | landed-family | LANDED | guard-class regression pin landed: verifier check7 in scripts/the50_t21_q_caption_ledger_verify.py pins the B... | OK 9135B | current |
| 143 | 2026-09-26T14:41:30Z | B2-235-mimo-revival | landed-family | LANDED | mimo watch revival papering order confirmed on bytes: the add --living re-registration (event 178982356701574... | OK 10630B | current |
| 144 | 2026-09-26T14:47:01Z | B2-242-quantity-word-bounds | landed-family | LANDED | caption ledger QUANTITY word bounds landed: every letter-led unit alternative boundary-bounded so the guard c... | OK 9859B | current |
| 145 | 2026-09-26T14:38:00Z | B2-221-prefix-editor | free-text | ATTRIBUTED to mechanism, writer named by exclusion | LINKS.jsonl sealed-prefix alarm resolved: the 13:53:18.678Z unowned write was a whole-file atomic rewrite (ct... | OK 8741B | current |
| 146 | 2026-09-26T15:21:00Z | B2-237-touch-law | landed-family | LANDED | 13:53:18Z no-row touch attributed to mechanism: one repo-wide alphabetical rewrite sweep 13:53:12.259-18.695Z... | OK 7546B | current |
| 147 | 2026-09-26T15:15:43Z | B2-253-transport-decision | landed-family | WIRED: serve-mode probe landed in tools/mimo_watch.py; raw-HTTP lane RETIRED BY DESIGN; b... | Transport decision before window close: triple FreeTierError battery (B2-236) + 09-22 records retired the zen... | OK 8898B | current |
| 148 | 2026-09-26T15:15:52Z | B2-256-caption-b243-class-pin | landed-family | LANDED | caption ledger check7 extended to pin the B2-243 classes: 11 canonical-month-word and sentence-year misdate p... | OK 11292B | corrected by 149 |
| 149 | 2026-09-26T15:17:56Z | B2-256-erratum-self-feed-renumber | erratum/correction | ERRATUM for B2-256-caption-b243-class-pin | the B2-256 row above names self-feeds B2-267/B2-268, but both numbers were taken by concurrent lanes between ... | OK 11292B | corrects 148 |
| 150 | 2026-09-26T15:19:40Z | B2-252-mimo-error-type-capture | landed-family | LANDED, target migrated mid-lane to the B2-253 serve transport, contract holds on the rep... | mimo_watch error rows now name their own cause: the gateway _probe str(e)[:160] defect (rows 2-5 all HTTP Err... | OK 9070B | current |
| 151 | 2026-09-26T15:19:56Z | B2-248-census-patrol-module-split | landed-family | LANDED | census_drift_patrol module split landed on bytes: self_test moved whole to tools/census_patrol_selftest.py (1... | OK 8153B | current |
| 152 | 2026-09-26T15:22:09Z | B2-259-caption-ledger-guard-pin-maintenance-law | landed-family | LANDED | pin maintenance law filed at its operative site, the verifier check7 constants block: a check7 FAIL the momen... | OK 8460B | current |
| 153 | 2026-09-26T15:26:39Z | B2-249-carrier-shape-law | landed-family | LANDED | carrier shape law landed on the carrier itself: one sentence appended to the AGENTS.md:27 Tests bullet statin... | OK 5804B | current |
| 154 | 2026-09-26T15:27:38Z | B2-260-verifier-prepush-gate | landed-family | LANDED | caption ledger verifier wired into a pre-push conditional gate: githooks/pre-push block (WARN-ONLY first land... | OK 9540B | current |
| 155 | 2026-09-26T15:30:57Z | B2-258-yearfirst-extraction | landed-family | LANDED | Year-first month-day rule landed at 0.90 in scripts/the50_t21_q_caption_ledger.py: standalone 19xx/20xx year ... | OK 11153B | current |
| 156 | 2026-09-26T15:35:41Z | B2-250-shared-file-claim-law | landed-family | LANDED | B2-167 claim-row convention extended to shared uncommitted files and codified in the QUEUE.md header as the S... | OK 7075B | current |
| 157 | 2026-09-26T15:45:00Z | B2-254-living-regression | landed-family | LANDED | Living re-classification regression root caused and pinned: the refresh writer is drift-patrol-cron (automati... | OK 14921B | current |
| 158 | 2026-09-26T15:39:20Z | B2-246-collect-deep-check-scheduled | landed-family | LANDED | the --collect deep check left hand-catch: MagCensusPatrolDaily registered daily 08:30 (scripts/census_patrol_... | OK 9873B | corrected by 161 |
| 159 | 2026-09-26T15:39:44Z | B2-257-year-inference-ladder | landed-family | LANDED | B2-257 year ladder landed on the 0.75 month-name no-year path (clause 1 explicit sentence year, clause 2 sing... | OK 10636B | current |
| 160 | 2026-09-26T15:44:15Z | B2-255-queue-double-spend-sweep | landed-family | LANDED | B2-255 sweep renumbered 24 later claimants B2-285..B2-308 in QUEUE.md per the B2-167 law (the 20 brief-census... | OK 29286B | current |
| 161 | 2026-09-26T15:44:31Z | B2-246-erratum-self-feed-renumber | erratum/correction | ERRATUM for B2-246-collect-deep-check-scheduled | the B2-246 row above names self-feeds B2-285/B2-286, but both draft numbers were taken by concurrent lanes be... | OK 9873B | corrects 158 |
| 162 | 2026-09-26T15:56:20Z | B2-247-collect-gap-reconciled | landed-family | LANDED | B2-247 gap reconciliation landed on bytes: the 2 zero-collect candidates are named (tests/ack_reaper_test.py,... | OK 11078B | corrected by 165 |
| 163 | 2026-09-26T16:01:16Z | B2-77-driver-v2-resilience-spec | landed-family | LANDED | B2-77 driver v2 resilience spec landed as receipt (5 sections): five XIDIG-SWARM LINKS rows mapped onto scrip... | OK 9975B | current |
| 164 | 2026-09-26T16:02:24Z | B2-251-open-checkbox-truth-audit | landed-family | LANDED | swept every checked Open row for a resolvable landing receipt: 16 unearned rows flipped to [ ] with dated no-... | OK 9865B | current |
| 165 | 2026-09-26T16:04:00Z | B2-247-queue-flip-disclosure | erratum/correction | ERRATUM for B2-247-collect-gap-reconciled | close pass on the landed B2-247: the receipt (registered sha 8CFFAC2468E3A7089DF7C09E8EF83675B915D65E4EA86A97... | OK 11078B | corrects 162 |
| 166 | 2026-09-26T16:20:00Z | B2-74-qlora-recipe-real-sources | landed-family | LANDED | UF-130 dead redo delivered a 9-part QLoRA recipe for ~10K reasoning parts on 12-24GB (QLoRA 4-bit over SFT, l... | OK 8679B | current |
| 167 | 2026-09-26T16:05:57Z | B2-214-dungeon-lore-census-fossil | landed-family | LANDED | B2-214 dungeon lore census fossil landed: audit_dungeon.v1.json:147 librarian line now carries the dated 2026... | OK 5627B | current |
| 168 | 2026-09-26T16:13:06Z | queue-field | steal | steal | scout roam under pinned tie-break: exactly 5 open scout rows stamped (Q-024 real X-radar steals bundle, Q-034... | OK 2583B | re-burned later (latest line 604) |
| 169 | 2026-09-26T16:13:06Z | rsi-harness | steal | steal | GENESIS CLAUSE DISCHARGES: all 7 G1-G7 scenario cards landed day 0 (configs/workflow_gate_scenarios/), 6 of 7... | OK 3621B | re-burned later (latest line 616) |
| 170 | 2026-09-26T16:13:06Z | steering-theory | steal | steal | live client SPECCED: local llama-server logprob client (ollama docs fetched today list Logprobs UNSUPPORTED o... | OK 3926B | re-burned later (latest line 595) |
| 171 | 2026-09-26T16:19:48Z | B2-279-fold-sort-totality | landed-family | LANDED | B2-279 gave every fold event a total-order key in scripts/index_fold_host.mjs (null-seq tier keyed (ts, file ... | OK 14406B | corrected by 177 |
| 172 | 2026-09-26T16:23:16Z | B2-75-gardenfors-bytes-fetch | landed-family | LANDED | B2-75 landed the UF-131 redo on three of four deliverables with the fourth filed as owed with exact block evi... | OK 17164B | current |
| 173 | 2026-09-26T16:28:52Z | B2-76-catalog-junction-policy | landed-family | LANDED | junction prune codified as scanner policy: mag/catalog_scan.py v2->v3 spec P1-P5 from LINKS XIDIG-WIN-* 2026-... | OK 8465B | current |
| 174 | 2026-09-26T16:31:17Z | B2-280-seq-band-retired | landed-family | LANDED | B2-280 2^53 inexact seq band retired: census 561 numeric seqs failing Number.isSafeInteger all parsing to dou... | OK 11564B | current |
| 175 | 2026-09-26T16:34:34Z | B2-79-gap-log-pollution-fix | landed-family | LANDED | B2-79 decoupled the gap-log writer from the production path: _gaps_log() in mag/temperature_stack.py:37 honor... | OK 5217B | corrected by 176 |
| 176 | 2026-09-26T16:37:25Z | B2-79-gap-log-pollution-fix-correction | erratum/correction | CORRECTION | Close-pass byte check on B2-79: an 18th test_gap_unique_xyz row (ts 2026-09-26T16:32:38Z) landed after the 17... | OK 5217B | corrects 175 |
| 177 | 2026-09-26T16:40:59Z | B2-279-fold-sort-totality-erratum-shared-file-c... | erratum/correction | ERRATUM for B2-279-fold-sort-totality | during the B2-279 receipt registration at 16:35:30Z the fold printed a transient wrong census (2087 events ac... | OK 14406B | corrects 171 |
| 178 | 2026-09-26T16:42:24Z | B2-329-events-dump-strip | landed-family | LANDED | B2-329 landed the events-dump purity fix: the events command of scripts/index_fold_host.mjs strips every unde... | OK 10714B | current |
| 179 | 2026-09-26T16:44:00Z | B2-82-verkle-tip-re-anchor | free-text | LANDING for B2-82-verkle-tip-re-anchor | chain_guard state=tip_stale (tip root 5aa0f154e517ce59 frozen at the 06:12Z write vs recomputed e26157d613efd... | OK 6315B | current |
| 180 | 2026-09-26T16:44:56Z | B2-328-refold-gate | landed-family | LANDED | B2-328 wired the refold-stability falsifier into a conditional pre-push gate: githooks/pre-push now carries a... | OK 10116B | current |
| 181 | 2026-09-26T16:47:55Z | b2-wave-fold | steal | steal | B2-wave inventory: 114 rows (103 landed, 5 corrections, 5 erratums, 1 hold); 3 load-bearing builds verified L... | OK 3257B | re-burned later (latest line 614) |
| 182 | 2026-09-26T16:48:22Z | B2-78-gap-denominator-refresh | landed-family | LANDED | B2-78 gap-analysis denominator refresh: all 8 gap rows of RESEARCH_GAP_ANALYSIS_20260918.md re-derived from l... | OK 13648B | current |
| 183 | 2026-09-26T16:48:31Z | B2-80-lifecycle-reason-carry | landed-family | LANDED | B2-80 mag_loop_gap.v1 lifecycle rows now carry the audit context: spec landed first in the mag/temperature_st... | OK 5246B | current |
| 184 | 2026-09-26T16:49:11Z | B2-83-row-6868-flag-restore | landed-family | LANDED | B2-83 restored the two flag metadata fields the 04:17Z re-fold dropped from verkle_chain.jsonl row 6868 (evid... | OK 7653B | current |
| 185 | 2026-09-26T16:51:01Z | B2-84-pile-tail-drain | landed-family | LANDED | B2-84 drained the pile tail: the brief said 2 unclassified of 140 but bytes at execution showed 4 of 142 (st-... | OK 4666B | current |
| 186 | 2026-09-26T16:52:57Z | B2-73-secret-scan-estate-pass | landed-family | LANDED | B2-73 UF-129 dead redo landed local-only: 31-rule gitleaks-pattern scanner + 4.3-bit entropy pass over corpus... | OK 7063B | current |
| 187 | 2026-09-26T17:01:23Z | B2-85-bare-powershell-path-fix | landed-family | LANDED | B2-85 bare-powershell PATH fix landed: 10 sites fixed across 9 files with the process_reaper pattern (shutil.... | OK 7283B | current |
| 188 | 2026-09-26T17:05:35Z | B2-337-ghost-resolve | landed-family | LANDED | B2-337 resolved the B2-279 receipt ghost by verification, neither reconstruction nor retirement: B2_279_sort_... | OK 11657B | current |
| 189 | 2026-09-26T17:16:30Z | B2-86-writer-test-isolation | landed-family | LANDED | B2-86 writer test isolation landed: both brief sinks inject at the writer, tests/test_seat_crash_guard.py red... | OK 7037B | current |
| 190 | 2026-09-26T17:14:32Z | build-fold-verify | steal | steal | first build-fold-verify: 3 of 4 landed builds verify byte-for-byte vs owning specs (b2-32 gate_verdict_v2 dor... | OK 3610B | re-burned later (latest line 575) |
| 191 | 2026-09-26T17:14:32Z | stego-canon-pipeline | steal | steal | watch-surface decision LANDED: both Mr. Pool surfaces alive, @Official_MrPool leads content flow (first emitt... | OK 3206B | re-burned later (latest line 650) |
| 192 | 2026-09-26T17:14:32Z | world-models-multi-agent | steal | steal | MSEAT-DRIFT grader BUILT + VALIDATED: watch/inbox/mseat_drift_grade.py (stdlib) reproduces all 3 fixture verd... | OK 3480B | re-burned later (latest line 662) |
| 193 | 2026-09-26T17:15:39Z | B2-87-fkb-continuity-repair | landed-family | LANDED | B2-87 FKB continuity repair landed: 2026-09-22T14:54Z index reset confirmed digit-exact on bytes (run_shell:c... | OK 11203B | current |
| 194 | 2026-09-26T17:16:17Z | B2-338-census-ok-line-case | landed-family | LANDED | B2-338 fixed the census patrol ok-line case crying wolf: the pre-push census block case-matches output START ... | OK 8313B | current |
| 195 | 2026-09-26T17:17:04Z | B2-92-qagg-card-completeness-sweep | landed-family | LANDED | B2-92 qagg card completeness sweep: all 45 ok:false rows in watch/inbox/qdrop_export/media_register_qagg.json... | OK 8408B | current |
| 196 | 2026-09-26T17:17:21Z | B2-81-ollama-truth | landed-family | LANDED | B2-81 verdict DETECTION not absence: 89 lifecycle_gap:ollama rows re-counted on bytes (89/313, 28.4 pct; brie... | OK 6501B | current |
| 197 | 2026-09-26T17:24:31Z | B2-343-restore-guard | landed-family | LANDED | B2-343 stale-base restore guard landed: tools/restore_guard.py new (pre-write check arm names a restore whose... | OK 10915B | current |
| 198 | 2026-09-26T17:35:34Z | B2-352-stragglers | landed-family | LANDED | B2-352 verdict LANDED: all 4 briefed straggler bare-powershell sites fixed with the process_reaper resolution... | OK 9472B | corrected by 201; re-burned later (latest line 204) |
| 199 | 2026-09-26T17:39:14.000Z | B2-357-scout-pin | landed-family | LANDED | B2-357 crash scout counting contract pinned at ENTRY level: mag/improve.py crash_log_census splits logs/seat_... | OK 7394B | current |
| 200 | 2026-09-26T17:44:00Z | B2-353-shell-pin | landed-family | LANDED | B2-353 run_shell powershell resolution pinned: tests/test_shell_powershell_resolution.py new, 3 pins 3 passed... | OK 7356B | corrected by 205 |
| 201 | 2026-09-26T17:40:00Z | B2-352-stragglers | erratum/correction | LANDED-CORRECTION | self-feed number correction for the B2-352 landing: briefs drafted as B2-372/373/374 renumbered to B2-375/376... | OK 9472B | corrected by 204; corrects 198; re-burned later (latest line 204) |
| 202 | 2026-09-26T17:40:02Z | B2-354-icon-drop-honesty | landed-family | LANDED | B2-354 icon_drop honesty landed: drop_shortcut captures stderr and requires BOTH powershell exit 0 and the .l... | OK 6435B | current |
| 203 | 2026-09-26T17:41:47Z | B2-342-schema-registry | landed-family | LANDED | B2-342 events key schema registry landed: configs/events_key_schema.json (events_key_schema.v1, 30 writer key... | OK 8291B | current |
| 204 | 2026-09-26T17:42:33Z | B2-352-stragglers | landed-family | LANDED-FINAL | final receipt state for the B2-352 landing: second concurrent-writer event named in the receipt Work done (a ... | OK 9472B | corrects 201 |
| 205 | 2026-09-26T17:52:00Z | B2-353-shell-pin-renum | erratum/correction | ERRATUM | Erratum to the B2-353-shell-pin row 17:44:00Z: its one_line said self-fed B2-375 B2-376, but the concurrent B... | OK 7356B | corrects 200 |
| 206 | 2026-09-26T17:45:45Z | B2-358-env-tripwire | landed-family | LANDED | B2-358 env-injection tripwire landed: new mag/env_redirect.py (REDIRECT_VARS over MAG_SEAT_CRASH_LOG and MAG_... | OK 8618B | current |
| 207 | 2026-09-26T17:50:22Z | B2-88-metadata-fetch | landed-family | LANDED | B2-88 metadata-only mrpool photos landed: all 314 CAPTION_LEDGER_20260926.jsonl metadata-only .jpg rows (Mess... | OK 7409B | corrected by 208,212 |
| 208 | 2026-09-26T17:50:48Z | B2-88-metadata-fetch-erratum | erratum/correction | ERRATUM | Erratum to the B2-88-metadata-fetch row 17:50:22Z: its one_line quoted receipt sha256 3f14a68ba0da2c86b9b53db... | OK 7409B | corrected by 209; corrects 207 |
| 209 | 2026-09-26T17:51:08Z | B2-88-metadata-fetch-erratum-2 | erratum/correction | ERRATUM | Erratum to erratum 17:50:48Z: it said the landed receipt is 8,377 bytes, another unverified number; os.path.g... | OK 7409B | corrects 208 |
| 210 | 2026-09-26T17:52:00Z | B2-372-chain-census | landed-family | LANDED | B2-372 chain naming landed fixture-first: mag/improve.py crash_log_census gained chains=N, the count of the t... | OK 7271B | current |
| 211 | 2026-09-26T17:44:00Z | B2-93-stego-erratum-20260926 | erratum/correction | erratum propagation LANDED: wrong mapping (qagg gap = drop #874 the central-algorithm pos... | stego 874-to-1104 erratum sweep: 3 living carriers anchored with errata, 4 correcting artifacts verified, 5 f... | OK 9352B | corrected by 214 |
| 212 | 2026-09-26T17:54:14Z | B2-88-metadata-fetch-erratum-3 | erratum/correction | ERRATUM | Erratum closing B2-88: (1) the drafted self-feed B2-384 was taken mid-lane by the concurrent B2-372 self-feed... | OK 7409B | corrects 207 |
| 213 | 2026-09-26T17:58:40Z | B2-359-writer-census | landed-family | LANDED | B2-359 writer census: 306 test files static-swept, 40 dynamic-probed with byte-still snapshots plus a 30s no-... | OK 10856B | current |
| 214 | 2026-09-26T17:52:00Z | B2-93-stego-erratum-20260926-erratum | erratum/correction | self-feed numbering erratum on the previous B2-93 row: briefs were drafted as B2-375 to B... | B2-93 self-feed numbers corrected 375-377 to 404-406, nothing else in the prior row changes | OK 9352B | corrects 211 |
| 215 | 2026-09-26T18:02:01.000Z | B2-373-stanza-pin | landed-family | LANDED | B2-373 crash-stanza writer shape pinned at the writer: tests/test_seat_crash_guard.py gained _assert_stanza_s... | OK 8936B | current |
| 216 | 2026-09-26T18:04:32Z | B2-89-hash-backfill-20260926 | landed-family | LANDED | B2-89 hash backfill media_full: all 2375 media_full files sha256-hashed from disk bytes (3,637,862,462 bytes ... | OK 7074B | current |
| 217 | 2026-09-26T18:07:13Z | B2-378-fold-outcome | landed-family | LANDED | B2-378 fold outcome honesty landed: mag/icon_drop.py _fold_training now passes the row status through to skil... | OK 8588B | current |
| 218 | 2026-09-26T18:12:44Z | B2-383-chain-quote-pin | landed-family | LANDED | B2-383 chains versus quoted chain-marker sentences: crash_log_census chains counting hardened from the B2-372... | OK 7854B | corrected by 220 |
| 219 | 2026-09-26T18:13:12Z | B2-377-icon-drop-unescape | landed-family | LANDED | B2-377 unescape landed: every drop_shortcut PS literal (lnk, target_path, args, WorkingDirectory, IconLocatio... | OK 9454B | current |
| 220 | 2026-09-26T18:14:49Z | B2-383-chain-quote-pin-erratum | erratum/correction | ERRATUM | Erratum to the B2-383-chain-quote-pin row same lane: its one_line pre-announced self-fed B2-410 and B2-411, b... | OK 7854B | corrects 218 |
| 221 | 2026-09-26T18:15:00Z | B2-384-real-chains-census | landed-family | LANDED | B2-384 real-chains census landed: crash_log_census on the real logs/seat_crashes.log reads blocks=424 entries... | OK 9486B | current |
| 222 | 2026-09-26T18:16:30Z | B2-374-behavioral-scout-pin | landed-family | LANDED | B2-374 behavioral-events scout counting contract pin: mag/improve.py gained behavioral_events_census plus nam... | OK 11909B | corrected by 223 |
| 223 | 2026-09-26T18:20:10Z | B2-374-self-feed-numbering-erratum | erratum/correction | self-feed numbering erratum on the previous B2-374 row: the two briefs were first appende... | B2-374 self-feed numbers corrected 417-418 to 419-420, nothing else in the prior row changes | OK 11909B | corrects 222 |
| 224 | 2026-09-26T18:20:48Z | B2-90-album-captions-v2 | landed-family | landed | All 9 unresolved grouped mrpool album captions resolved from local bytes by widening the caption carrier sear... | OK 6512B | current |
| 225 | 2026-09-26T18:29:30Z | B2-163-law12-registration | landed-family | landed | LAW-12 amendment_gate (T0) registered in memory/law/registry.json between LAW-11 and LAW-13 from bytes: BURN_... | OK 8596B | current |
| 226 | 2026-09-26T18:32:17Z | prompt-uplift-lane | steal | steal | FAIL(BIB_LAUNDER) checker EXECUTED as tabletop: bib_launder_check.py built (marker-span extraction learned fr... | OK 3503B | re-burned later (latest line 568) |
| 227 | 2026-09-26T18:32:17Z | doctrine-owed-chase | steal | steal | 3 of 3 at PRIMARY strength: (a) Sefer Raziel 1701 title page fetched via HebrewBooks downloadhandler route (5... | OK 3693B | re-burned later (latest line 693) |
| 228 | 2026-09-26T18:32:17Z | free-resource-landscape | steal | steal | Groq bypass live-measurement protocol PRE-REGISTERED (spec only, no call executed, GROQ_API_KEY = open depend... | OK 4012B | re-burned later (latest line 692) |
| 229 | 2026-09-26T18:33:00Z | B2-162-g1-retro-citation | landed-family | landed | G1 card retro-citation tripwire fired the day it was filed: the first genuine fleet G1 FAIL is REGISTRY.jsonl... | OK 7337B | current |
| 230 | 2026-09-26T18:34:19Z | B2-97-width15-probe-no-go | landed-family | landed | Width-15 ceiling probe precondition check: NO explicit operator GO for width 15 on QUEUE.md or any 2026-09-26... | OK 9415B | corrected by 235 |
| 231 | 2026-09-26T18:36:30Z | b2-99-fanout-reconcile | landed-family | landed | AGENTS.md fan-out bullet reconciled to the dispatch-shape law: workflow children maxAttempts 0 keep the max_c... | OK 6186B | current |
| 232 | 2026-09-26T18:39:30Z | B2-96-scripts-mimosa-triage | landed-family | LANDED | B2-96 scripts/ mimosa ssrf/path triage: sealed scan 04-10-04Z holds exactly 43 ssrf/path occurrences in 21 fi... | OK 9521B | corrected by 234 |
| 233 | 2026-09-26T18:37:13Z | B2-95-ratchet-prune-gap | landed-family | landed | Ratchet prune reaping gap closed: prune now reaps only scanner-domain claims (SCANNER_RULES + scanner_domain;... | OK 8228B | corrected by 236 |
| 234 | 2026-09-26T18:43:10Z | B2-96-self-feed-numbering-erratum | erratum/correction | self-feed numbering erratum on the previous B2-96 row: the three briefs landed as B2-438,... | B2-96 self-feed numbers corrected 429-431 to 438-440, nothing else in the prior row changes | OK 9521B | corrects 232 |
| 235 | 2026-09-26T18:39:45Z | B2-97-index-insert-erratum | erratum/correction | erratum | B2-97 INDEX registration erratum: the receipt item inserted at 18:34:19Z was erased by a concurrent whole-fil... | OK 9415B | corrects 230 |
| 236 | 2026-09-26T18:39:53Z | B2-95-prune-gap-rebase-erratum | erratum/correction | erratum on the prior B2-95 row, nothing else in it changes | Concurrent B2-94 and B2-96 landings grew the mimosa family 25 to 57 (register 900 to 932) mid-close, breaking... | OK 8228B | corrects 233 |
| 237 | 2026-09-26T18:40:51Z | B2-100-flip-receipt-template-20260926 | free-text | TEMPLATE LANDING ONLY, flip NOT executed, operator GO pending per the B2-23 card: receipt... | Flip receipt prepared before GO: every field the post-flip proof needs is pre-named with its exact command, n... | OK 9090B | current |
| 238 | 2026-09-26T18:41:10Z | B2-94-mimosa-live-tail-triage | landed-family | LANDED | B2-94 mimosa live tail: brief said 14 (tools/ 9 in 8 files + models/ 5), seal bytes hold 19 occurrences / 13 ... | OK 12233B | corrected by 240 |
| 239 | 2026-09-26T18:44:00Z | B2-98-provider-error-visibility | landed-family | landed | Provider-error counter landed: tools/provider_error_tally.py plus tests/test_provider_error_tally.py (3 pins)... | OK 7052B | current |
| 240 | 2026-09-26T18:42:50Z | B2-94-self-feed-numbering-erratum | erratum/correction | self-feed numbering erratum on the previous B2-94 row: the three briefs were first append... | B2-94 self-feed numbers corrected 441-443 to 444-446, CLAIMED flips re-applied after concurrent erase, nothin... | OK 12233B | corrected by 242; corrects 238 |
| 241 | 2026-09-26T18:43:01Z | B2-101-seed330-papers-20260926 | landed-family | landed: seed-3.3.0.zip papers filed from bytes, no re-zip needed; hash gate 015acfa0... (... | The 3-pyc author-path leak lived only in the superseded 96950daa Desktop export (59 rows); the shipped 015acf... | OK 7874B | current |
| 242 | 2026-09-26T18:44:33Z | B2-94-erratum-correction | erratum/correction | correction to the 18:42:50Z B2-94 erratum row: that row attributed the unflipped CLAIM to... | B2-94 erratum correction: CLAIMED miss was own close-script bug not a concurrent clobber, token fixed 18:44Z,... | OK 12233B | corrects 240 |
| 243 | 2026-09-26T18:45:28Z | B2-164-scenarios-gate | landed-family | LANDED | B2-164 scenario suite at pre-push: githooks/pre-push gained a conditional ENFORCING workflow_gate_scenarios b... | OK 11040B | current |
| 244 | 2026-09-26T18:50:31Z | B2-179-dogflood-meters-20260926 | landed-family | LANDED | dogfood meter window truth filed: reading 1 operator screenshot ~13:0xZ (5h window 80 pct used reset 10:06 ou... | OK 8243B | current |
| 245 | 2026-09-26T18:50:46Z | B2-105-mistral-surgery | landed-family | landed | Mistral lane surgery verified landed and closed: both brief arms already on disk (repoint arm B2-61 configs/p... | OK 4986B | current |
| 246 | 2026-09-26T19:00:25Z | B2-165-asekin-grading-ledger-20260926 | landed-family | LANDED | asekin113 grading ledger built (the owed file B2-24 named): watch/inbox/asekin113/GRADING_LEDGER.jsonl sha256... | OK 7236B | current |
| 247 | 2026-09-26T19:03:30Z | B2-166-rubric-scoring | landed-family | LANDED | window 21/22 rubric scoring run, owed since the 2026-09-23 06:00Z clock: MISS on receipts on file, data point... | OK 10047B | current |
| 248 | 2026-09-26T19:02:24Z | B2-102-corpus-fts5-wiring | landed-family | LANDED | B2-102 FTS5 wired into corpus_search: index-preferred path answers engine=fts5 on a fresh catalog/catalog_fts... | OK 9418B | current |
| 249 | 2026-09-26T19:06:03Z | B2-178-freelane-runner | landed-family | LANDED | B2-178 free-lane tandem burn runner LANDED AND RUNNING: 8 alive B2-04 lanes (groq gpt-oss-120b, openrouter k1... | OK 6421B | current |
| 250 | 2026-09-26T19:09:53Z | B2-103-catalog-path-census-rebuild | landed-family | LANDED | catalog path-anchoring census + salon Appendix A module landed: census of the Sep-18 map (757,667 rows) found... | OK 11742B | current |
| 251 | 2026-09-26T19:10:53Z | B2-107-ollama-locality-trap | landed-family | LANDED | OLLAMA_HOST locality trap closed with the host-reachable law, doctor-enforced: a local-declared lane (id olla... | OK 8355B | current |
| 252 | 2026-09-26T19:11:30Z | B2-108-rbxlx-commit-gate-20260926 | landed-family | LANDED | B2-108 Sep-29 commit gate landed: the rebuilt GATE PASS the_mountain.rbxlx (B2-29, UpdateAsync 2 / GetAsync(k... | OK 4024B | current |
| 253 | 2026-09-26T19:13:51Z | B2-167-queue-dedupe | landed-family | LANDED | Queue-number dedupe final census zero double-claimed ids (462 row-start rows, 462 distinct ids, post sha cbac... | OK 8191B | current |
| 254 | 2026-09-26T19:15:23Z | B2-106-provider-probe-cadence | landed-family | landed | Provider-health cadence landed: the first non-dry improve scout that finds last_provider_probe stale vs confi... | OK 7132B | current |
| 255 | 2026-09-26T19:15:40Z | judge-lane-spec | steal | steal | cluster organ verified against ALL 249 burn-ledger rows w/ unmodified organ code: alarm correctly silent (per... | OK 3689B | re-burned later (latest line 594) |
| 256 | 2026-09-26T19:15:40Z | third-way-game | steal | steal | ACT content stubs LANDED: THIRD_WAY_ACT1_WALL_STUB.json (Wall stone ASCEND NOT AS A WALL + two-sided fence li... | OK 3612B | re-burned later (latest line 627) |
| 257 | 2026-09-26T19:15:40Z | middle-path-doctrine | steal | steal | third C8 reading pinned at LEDGER row 252: classes hold over min-10 (attached 179 vs bare 73 lifetime), 8 NEW... | OK 3294B | re-burned later (latest line 684) |
| 258 | 2026-09-26T19:24:30Z | b2-464-corpus-search-caller-census | steal | steal | corpus_search caller census after the B2-102 FTS5 wiring: 16 caller classes adjudicated across mag/ tools/ da... | OK 12376B | current |
| 259 | 2026-09-26T19:34:18Z | B2-490-baseurl-locality-sweep | landed-family | LANDED | base_url_env locality sweep beyond ollama landed comment-only: every env-set base URL classified seat-scope (... | OK 10555B | current |
| 260 | 2026-09-26T19:34:28Z | B2-104-corpus-freshness-policy | landed-family | LANDED | C6 freshness policy landed as three arms, one module per arm: mag/catalog_rescan.py (incremental append-upser... | OK 7528B | current |
| 261 | 2026-09-26T19:35:59Z | B2-469-dated-meters | landed-family | LANDED | B2-469 dated meters landed: new $0 organ tools/meter_patrol.py (314 lines, schema dated_meter_v1, under the 4... | OK 9307B | current |
| 262 | 2026-09-26T19:37:37Z | B2-112-v1-v2-escalation-reconcile | landed-family | LANDED | V1 escalation triggers (conf<0.7; score<0.5 AND conf>0.7) resolved SUPERSEDED not pre-filter: governor write ... | OK 3850B | current |
| 263 | 2026-09-26T19:44:30Z | b2-467-pool-repull | steal | steal | Mr Pool re-pull before further scoring: Telethon resume BLOCKED exactly (connect OK, harvest.session 256-byte... | OK 13107B | current |
| 264 | 2026-09-26T19:40:00Z | B2-109-rbxlx-line-ending-armor | landed-family | LANDED | .gitattributes created with *.rbxlx binary + *.rbxm binary (repo had none, core.autocrlf=true); live damage m... | OK 5382B | current |
| 265 | 2026-09-26T19:40:08Z | b2-489-resolver-bound | landed-family | LANDED | landed: doctor locality seam _host_resolves got the registry treatment (one getaddrinfo on a daemon thread jo... | OK 9294B | current |
| 266 | 2026-09-26T19:40:14Z | B2-491-pointer-anchor-law | landed-family | LANDED | B2-491 pointer-anchor law landed: QUEUE header gains the law (every NEW file:line pointer in a brief row carr... | OK 7799B | current |
| 267 | 2026-09-26T19:41:13Z | B2-122-canonical-first-filing | landed-family | LANDED | known_canonicals fixed from last-writer-wins dict comprehension to first-occurrence-wins so check_url.first_e... | OK 3295B | current |
| 268 | 2026-09-26T19:41:31Z | B2-468-oct3-check | landed-family | LANDED | pre-registered OCT 3 check run receipts-only on the re-pulled Pool surface: NOT FIRED through data horizon 20... | OK 12021B | current |
| 269 | 2026-09-26T19:41:44Z | B2-115-probe-chain-freeze | landed-family | LANDED | groq model_chain at B2_04_probe.py:219 annotated dated-frozen as a period artifact (brief arm 1): comment abo... | OK 2629B | current |
| 270 | 2026-09-26T19:42:28Z | B2-169-research-event-pointers | landed-family | LANDED | tools/research.py links search skips empty-canonical event rows (54/338) and EVENTS.jsonl is searchable as it... | OK 2467B | current |
| 271 | 2026-09-26T19:43:32Z | B2-116-groq-nonchat-classification | landed-family | LANDED | groq live-11 classification landed: out_of_routing_scope register (9 ids, per-class comments) added to the pr... | OK 3781B | current |
| 272 | 2026-09-26T19:44:54Z | B2-175-shadowledger-datastore-leg | owed | OWED scheduled Sep-29 | live DataStore leg confirmed future-dated by its own gate chain (B2-10 prereg Sep-29 P0 first, B2-108 names B... | OK 4131B | current |
| 273 | 2026-09-26T19:44:59Z | B2-171-xpost-source-convention | landed-family | LANDED | x-post-source convention (canonical=resource, url=X post, 33 rows) written into mag/link_library.py spec; new... | OK 2552B | current |
| 274 | 2026-09-26T19:45:04Z | b2-113-cascade-falsifier-run | free-text | UNDECIDABLE-OWED | B2-113 cascade falsifier run owned: tools/cascade_falsifier_run.py built (~150 lines, registered vocabulary, ... | OK 5264B | current |
| 275 | 2026-09-26T19:46:29Z | B2-161-events-drift-policy | landed-family | LANDED | EVENTS.jsonl drift decision landed as LAW note watch/inbox/EVENTS_DRIFT_LAW_20260926.md: refresh-owner re-reg... | OK 2807B | current |
| 276 | 2026-09-26T19:46:36Z | b2-123-scout-charter | landed-family | LANDED | Scout charter landed at watch/inbox/SCOUT_CHARTER_20260926.md: one page, three laws naming writers (free-reso... | OK 3095B | current |
| 277 | 2026-09-26T19:46:41Z | B2-174-p3-falsifier-sharpen | landed-family | LANDED | same-uid same-UTC-day cross-server double-write probe landed in PLAYTEST.md as a checked section above Score ... | OK 3633B | current |
| 278 | 2026-09-26T19:55:00Z | B2-170-imprint-deck-denominator | landed-family | LANDED | B2-170 links/events denominators landed: build_fleet_imprint.py json_row_kind() splits LINKS.jsonl into 284 l... | OK 3828B | current |
| 279 | 2026-09-26T19:47:39Z | B2-110-mudbasecamp-wisp | landed-family | LANDED | wisp chase hum declaration narrowed FindFirstChild Instance? to BasePart? (file cast pattern) killing the rea... | OK 4209B | current |
| 280 | 2026-09-26T19:48:16Z | B2-466-catalog-v4-rescan-decision | landed-family | LANDED-SUPERSEDED-EXECUTED | GO on v4 rescan plus index refresh, already executed by concurrent lanes (map replaced 19:01:27Z, B2-104 incr... | OK 6191B | current |
| 281 | 2026-09-26T19:48:51Z | b2-129-gemini-bearer-401 | landed-family | LANDED | gemini Bearer 401 captured same day not next run: B2_129_gemini_bearer_retry.py fires generateContent twice p... | OK 3857B | current |
| 282 | 2026-09-26T19:49:15Z | B2-111-gate-verdict-v2-wiring | landed-family | LANDED | gate_verdict_v2 wired into mag/lane_runner.py: load_gate_block reads the frozen B2-32 yaml block per call (no... | OK 5212B | current |
| 283 | 2026-09-26T19:49:28Z | B2-160-ledger-c8-check | landed-family | LANDED | overdue C8 check ran marker-strict over 277 LEDGER rows: 156 attached vs 121 bare (tolerance 188 vs 89 with t... | OK 4131B | current |
| 284 | 2026-09-26T19:50:38Z | B2-120-playtest-lint-headline-refresh | landed-family | LANDED | PLAYTEST.md header refreshed from 21-files-clean fossil to live 2026-09-26 luau_lint bytes (checked 43 files,... | OK 3098B | current |
| 285 | 2026-09-26T19:51:19Z | B2-134-key-inventory-truth-sweep | landed-family | LANDED | Five key-inventory lies fixed in bytes (cerebras_2 active, cerebras_1 silence, together verify-auth stale, nv... | OK 4385B | current |
| 286 | 2026-09-26T19:51:55Z | b2-218-fragile-aligned-vocabulary | landed-family | LANDED | FRAGILE-ALIGNED vocabulary sweep landed: tools/drift.py docstring now enumerates the fifth verdict as ALIGNED... | OK 4591B | current |
| 287 | 2026-09-26T19:52:18Z | B2-224-w40-stamp-board | owed | OWED scheduled W40 flip | W40 stamp confirmed unrunnable today (ISO week 39; stamp tool refuses wall-clock ahead of run date) but decis... | OK 3814B | current |
| 288 | 2026-09-26T19:52:00Z | B2-118-taxonomy-first-pass-recount | erratum/correction | ERRATUM FILED | 52 percent first-pass line recounted at frozen cutoff 3d12289f9: numerator 17 promoted is a stale mid-day tal... | OK 4576B | current |
| 289 | 2026-09-26T19:58:00Z | B2-172-image-drop-schema | landed-family | LANDED | B2-172 image-drop third schema landed per the B2-28 split shape: own register watch/inbox/IMAGE_DROPS.jsonl (... | OK 4735B | current |
| 290 | 2026-09-26T19:53:58Z | b2-240-b2-219-reconcile | landed-family | LANDED | B2-240 reconciliation landed: the demanded B2-219 receipt now exists on disk (B2_219_misdate_classes_20260926... | OK 4929B | current |
| 291 | 2026-09-26T19:54:28Z | B2-119-ifexpr-balance | landed-family | LANDED | three permanent balance advisories triaged to a new false-positive class, Luau if-expressions counted as if-s... | OK 5115B | current |
| 292 | 2026-09-26T19:54:39Z | B2-132-steering-fold-delta | landed-family | LANDED | fold filed as corpus/steal/STEERING_FOLD_DELTA_20260926.md: 3 practice-has-theory matches (probe20 runner IS ... | OK 4146B | current |
| 293 | 2026-09-26T19:54:58Z | B2-465-rebuild-schedule-daily | landed-family | LANDED | B2-465 daily FTS rebuild + deep audit LANDED: MagFtsIndexDaily task daily 09:00 (scripts/fts_index_daily.ps1,... | OK 15218B | current |
| 294 | 2026-09-26T19:55:01Z | B2-341-secret-scan-papers | landed-family | LANDED | secret-scan papers filed from bytes with a correction: the current results file (regenerated 16:39:42Z) is NO... | OK 5973B | current |
| 295 | 2026-09-26T19:56:01Z | B2-117-error-class-census | landed-family | LANDED | Class mapping landed in scripts/build_lane_game.py as constants plus _error_class plus a read-only --census s... | OK 5972B | current |
| 296 | 2026-09-26T19:56:10Z | B2-156-living-hash-law-correction | erratum/correction | CORRECTION | correction row per MANIFEST ledger_one_line_freshness: LEDGER row 110 one_line assertion owed-missing-B2-41-r... | OK 3569B | corrects 110 |
| 297 | 2026-09-26T19:56:15Z | B2-201-dspy-optimizer-protected-field-sweep | landed-family | LANDED | F1 does not fire: all five B2-59-owed dspy files fetched live from stanfordnlp main (sha256 pinned, archived ... | OK 4382B | current |
| 298 | 2026-09-26T19:56:41Z | B2-203-ledger-one-line-freshness | landed-family | LANDED | MANIFEST ledger_one_line_freshness spec + tools/ledger_close_check.py (row 110 exits 1 naming both stale rece... | OK 3569B | current |
| 299 | 2026-09-26T20:04:00Z | B2-137-vault-pack-register | landed-family | LANDED | B2-137 closed byte-verified: full sha256 recomputed from ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc bytes = AD... | OK 3357B | current |
| 300 | 2026-09-26T19:58:00Z | B2-176-disposition-durability | free-text | DECIDED | disposition() stays session-scoped, decided spec-first in roblox/README.md (Disposition read law paragraph): ... | OK 4535B | current |
| 301 | 2026-09-26T19:58:36Z | B2-421-caption-via-pin | landed-family | LANDED | caption_via invariant pin landed two classes deep: B2_421_caption_via_verify.py checks carrier validity (grou... | OK 4229B | current |
| 302 | 2026-09-26T19:58:54Z | B2-261-mimo-watch-armed | landed-family | LANDED | MagMimoWatchHourly armed (live fire appended an honest serve-down row); forever-append tail bounded by paired... | OK 3838B | current |
| 303 | 2026-09-26T19:59:43Z | b2-365-census-patrol-split | landed-family | LANDED | B2-365 split landed: --collect collectors (COLLECT_TAIL_RE, parse_collect_tail, parse_collect_files, collect_... | OK 5283B | current |
| 304 | 2026-09-26T20:00:12Z | B2-234-wave2-batch1-reaudit | landed-family | LANDED | other 5 batch-1 artifacts carry no naive-index or unstated-ruler approvals: all load-bearing counts recompute... | OK 5046B | current |
| 305 | 2026-09-26T20:00:14Z | B2-131-steering-failures | landed-family | LANDED | mined 19,185 user text parts since 9/19 (zcode db part table, the real transcript surface; sessions/tasks dir... | OK 7211B | current |
| 306 | 2026-09-26T20:02:00Z | B2-130-steering-self-steal-pass-1 | landed-family | LANDED | steering self-steal pass 1 mined 1,391 promoted operator inputs since 09-19 from the CLI sqlite store (sessio... | OK 6971B | current |
| 307 | 2026-09-26T20:01:06Z | B2-144-free-cache-model-map | landed-family | LANDED bounded | free-cache map landed bounded: DeepSeek and z.ai rows verified from official docs fetched today (deepseek-fla... | OK 5578B | current |
| 308 | 2026-09-26T20:01:17Z | b2-177-nous-cell-erratum | landed-family | LANDED | nous cell erratum landed: PROVIDER_HEALTH_20260926.md:17 now cites the measured x-ratelimit set (50 req/min, ... | OK 2421B | current |
| 309 | 2026-09-26T20:02:39Z | B2-288-test-debt-cure | landed-family | LANDED | all three surfaces cured: (a) zai_burst+loop_death_guards order interaction root-caused to from-import parent... | OK 7104B | current |
| 310 | 2026-09-26T20:16:00Z | B2-286-null-model-refuse | landed-family | LANDED | B2-286 landed refuse arm: chat_provider AND chat_messages return named null_model_refused error when resolved... | OK 3450B | current |
| 311 | 2026-09-26T20:02:47Z | B2-168-event-split-gate | free-text | HOLDS | LINKS event-split validate gate: mag/links_split_gate.py + 2-line wiring in shared_surface (file held at 400 ... | OK 6896B | current |
| 312 | 2026-09-26T20:03:15Z | B2-385-caption-sha-promotion-v2 | landed-family | LANDED | 314 CAPTION_LEDGER rows patched in place from the recovered register (fail-closed disk-sha gate), INDEX re-se... | OK 4778B | current |
| 313 | 2026-09-26T20:04:51Z | B2-182-free-tier-power-users | landed-family | LANDED bounded | power-user patterns dig landed bounded by 429-stormed search: TRC fetched (1,000+ TPU pool, obligation = publ... | OK 5765B | current |
| 314 | 2026-09-26T20:04:54Z | b2-180-seed-rib-v0 | landed-family | LANDED | SEED-RIB v0 landed: spec at watch/inbox/SEED_RIB_FORMAT_v0_20260926.md (seed_rib.v0 schema, roles, sha256 sea... | OK 4266B | current |
| 315 | 2026-09-26T20:05:39Z | B2-200-lawd-fold-check | landed-family | LANDED | law D upgraded from single seed-paired delta to beats-seed AND gain-holds-across-folds per the B2-59 pre-auth... | OK 5863B | current |
| 316 | 2026-09-26T20:05:47Z | B2-190-past-2p53-seq-forms | landed-family | LANDED | Audit: 561 raw number-literal seqs past 2^53 (latest line 3084 the B2-42 note raw 1789823567015749478) vs 491... | OK 5634B | current |
| 317 | 2026-09-26T20:06:02Z | B2-363-pre-push-prefix-pairing-pins | landed-family | LANDED | B2-338 sh-replay pattern factored into tests/hook_pairing.py and extended to every pre-push ok arm: freshness... | OK 4502B | current |
| 318 | 2026-09-26T20:07:18Z | B2-126-laptop-bootstrap-receipt | owed | OWED-DORMANT | condition unmet: zero laptop rows in LEDGER, no landing receipt in watch/inbox, wave bridge receipt names no ... | OK 2734B | current |
| 319 | 2026-09-26T20:14:00Z | B2-191-queue-registered-hash-drift-flap | landed-family | LANDED | QUEUE.md drift flap resolved by registering the board living-open (B2-156 edit-shaped vocabulary, seq 1790452... | OK 5761B | current |
| 320 | 2026-09-26T20:07:52Z | B2-340-prompt-cache-matrix | landed-family | LANDED | four verified LINKS.jsonl rows landed (writer zcode-sw-10-b2-340) with same-day fetched quotes: anthropic 1.2... | OK 4835B | current |
| 321 | 2026-09-26T20:08:00Z | B2-189-retirement-body-parser | landed-family | LANDED | retirement-body handler landed in scripts/build_lane_game.py: _call's 404 arm now parses the full body for 'U... | OK 4039B | current |
| 322 | 2026-09-26T20:22:00Z | B2-226-aging-guard-board-test | landed-family | LANDED | 3 pins appended to tests/test_drift_dashboard.py pushing a synthetic W40 FRAGILE-ALIGNED v2 row through histo... | OK 3910B | current |
| 323 | 2026-09-26T20:10:45Z | B2-225-drift-alarm-tripwire | landed-family | LANDED | --alarm landed in tools/drift_dashboard.py spec-first (DRIFT_BOARD_SPEC.md 4b): fires on DRIFTING streak >= 1... | OK 4818B | current |
| 324 | 2026-09-26T20:10:53Z | B2-152-ractor-panel-spec | landed-family | LANDED | Ractor panel spec filed (4 faces, subsystem-wide mapping, instrument-bound dogfood loop, steal dig, run-book)... | OK 3169B | current |
| 325 | 2026-09-26T20:11:02Z | adversarial-self-probes | steal | steal | PROBE-B executed paper-only: forged all-5-real roam receipt CAUGHT by the DMIP verdict-content cross-check vs... | OK 3426B | re-burned later (latest line 640) |
| 326 | 2026-09-26T20:11:02Z | queue-field | steal | steal | judge-seat roam: 5 of 7 open unroamed judge rows stamped (Q-050, Q-011, Q-033, Q-036, Q-020 by effort then ol... | OK 3177B | re-burned later (latest line 604) |
| 327 | 2026-09-26T20:11:02Z | rsi-harness | steal | steal | LAW-12 REGISTERED by another window (memory/law/registry.json 2026-09-26T18:26:53Z, B2-163, genesis falsifier... | OK 3841B | re-burned later (latest line 616) |
| 328 | 2026-09-26T20:12:47Z | B2-150-232-vs-84-blocked-line-delta | free-text | PARTIAL-UNKNOWN-FILED | 84 byte-confirmed as unique supervisor spawns (started 9+45+30; auto_restarted rows are same-ts-same-pid dupl... | OK 4880B | current |
| 329 | 2026-09-26T20:34:00Z | B2-318-pytest-port-batteries | landed-family | LANDED | B2-318 landed port arm: ack_reaper_test (21 checks) + lesson_gate_test (22 checks) refactored to single colle... | OK 3369B | current |
| 330 | 2026-09-26T20:13:15Z | B2-290-live-dead-child-proof | landed-family | LANDED | grounding_chain.py BASE/CHAIN_LOG injectable via --base/--log + env; new end-to-end test runs a real exit-3 s... | OK 3360B | current |
| 331 | 2026-09-26T20:13:59Z | B2-387-canary-marker-root-law | landed-family | LANDED | repair_root pinned informational-only in mag/chain_guard.py check() with a counted marker_root_drift field (r... | OK 5232B | current |
| 332 | 2026-09-26T20:47:00Z | B2-386-refetch-probe | landed-family | LANDED | B2-386 probed all surfaces, honest-limit STANDS: register source_url refetch, fresh t.me embed page URLs, and... | OK 3568B | current |
| 333 | 2026-09-26T20:16:15Z | B2-184-corpus-path-seam | landed-family | LANDED | _confine strips the scanner's local_sovereign_agent/ prefix (literal, confinement unchanged) so corpus_get/ta... | OK 3719B | current |
| 334 | 2026-09-26T20:16:48Z | B2-205-quorum-p4-selfvote-exclusion | landed-family | LANDED | p4 self-vote exclusion landed in mag/quorum_window.py: addition authors parsed from fold headers (**A1** [TAG... | OK 4235B | current |
| 335 | 2026-09-26T20:17:06Z | B2-416-stanza-census | landed-family | LANDED | watch/inbox sweep: 7 files / 16 traceback headers, 1 file / 6 headers stanza-owned, 6 files / 10 headers stan... | OK 4837B | current |
| 336 | 2026-09-26T20:17:26Z | B2-195-express-quota-lane-block | owed | OWED-DORMANT | condition unmet: probe bytes still 403 PERMISSION_DISABLED on both auth shapes, no 200 anywhere, no first-200... | OK 3711B | current |
| 337 | 2026-09-26T20:18:47Z | B2-422-declared-unresolvable-class | landed-family | LANDED | Declared-unresolvable class registered (option b) in a dated addendum to B2_12_caption_ledger_20260926.md: em... | OK 5699B | current |
| 338 | 2026-09-26T20:18:58Z | B2-227-walk-compare-rescan | landed-family | LANDED | walk-voice date gap closed by running the LAW-13 minimal experiment instead of choosing owed-vs-stands: tools... | OK 4172B | current |
| 339 | 2026-09-26T20:19:34Z | B2-294-register-sha-fix | landed-family | LANDED | md_record_seal register events now hash real bytes (streaming, 8MB cap) or emit the B2-156 living-style 256KB... | OK 3409B | current |
| 340 | 2026-09-26T20:55:00Z | B2-141-grok-ask4-scope-freeze | landed-family | LANDED | B2-141 Ask 4 scope freeze landed: audit bound to the 39 BURN_*/SEED_SALON_* files dated 20260925 (byte-census... | OK 5872B | current |
| 341 | 2026-09-26T20:19:48Z | B2-143-card-trial-sweep | free-text | PARTIAL | card-trial census split honest against a 1302-throttled search window: VERIFIED LIVE google cloud $300 new-cu... | OK 6084B | current |
| 342 | 2026-09-26T20:20:27Z | B2-209-regime-gate-display-split | landed-family | LANDED | regime rows excluded from _gates_passed_for (closes the B2-65 falsifier), _regime_passed_for mirror added, st... | OK 4069B | current |
| 343 | 2026-09-26T20:21:11Z | b2-186-uf122-eval | landed-family | LANDED | UF-122 eval re-anchored and executed at tool level: 11 dead anchor paths replaced by real catalog lookups (pa... | OK 5407B | current |
| 344 | 2026-09-26T20:21:28Z | B2-213-fullscan-report-resync | landed-family | LANDED | Drift cause named: Estate FullScan schtask rewrites FULL_SCAN_REPORT whole-file per run (full_scan.py:229, 13... | OK 3454B | current |
| 345 | 2026-09-26T20:40:00Z | B2-388-stale-tip-writer-hunt | landed-family | LANDED WITH INCIDENT (disclosed) | hunt found the stale-tip path: usage_digest commit_day amend arm never bound root, raising UnboundLocalError ... | OK 6719B | current |
| 346 | 2026-09-26T21:05:00Z | B2-153-seedrib-steal-dig | landed-family | LANDED | B2-153 external steal dig landed: 9 idea classes surveyed (reproducible-build manifests, Nix derivations/clos... | OK 4986B | current |
| 347 | 2026-09-26T20:23:04Z | B2-231-deepseek-truncation-erratum | landed-family | LANDED | truncation byte-confirmed (27594 bytes, 515 lines, no trailing newline, cut mid-sentence in Level 3 The Wall)... | OK 3662B | current |
| 348 | 2026-09-26T20:23:10Z | B2-302-builder-truncation-guard | landed-family | LANDED | chat() in B2_71_hill_build.py detects finish_reason=length and refires once at x3 budget (cap 16000), discard... | OK 3395B | current |
| 349 | 2026-09-26T20:23:19Z | B2-233-qnum-dropno-map | landed-family | LANDED | qnum_dropno_map.jsonl landed: min-cost alignment of 6242 qdrops rows to dense q_num 1..4966 anchored on 16 pa... | OK 6546B | current |
| 350 | 2026-09-26T20:23:31Z | b2-292-drift-patrol-living | free-text | PARTIAL-OWED | Drift-patrol living adoption PARTIAL: disease quantified on bytes (drift-patrol-cron whole-file refreshed LIN... | OK 4831B | current |
| 351 | 2026-09-26T20:24:09Z | B2-147-writer-poison-guard | landed-family | LANDED | Writer-side poison guard landed in scripts/index_fold_host.mjs: normInboxFile/OUTSIDE_RE/isUnresolved hoisted... | OK 5879B | current |
| 352 | 2026-09-26T20:52:00Z | B2-423-carrier-position-honesty | landed-family | LANDED | carrier-position distribution byte-verified (6 B2-90 v2 albums: carrier on first member in 5, last member in ... | OK 3707B | current |
| 353 | 2026-09-26T20:24:20Z | B2-271-qcaption-verify-beat | landed-family | LANDED | Daily MagQCaptionVerifyDaily schtask (07:30) runs the 7-check verifier and lands RESULT+row count in QCAPTION... | OK 2902B | current |
| 354 | 2026-09-26T20:25:35Z | B2-263-dash-noun-audit | landed-family | LANDED | dash-pair noun-class audit closed with per-noun proven as ceiling: full 6,242-drop sweep found 39 distinct fo... | OK 5360B | current |
| 355 | 2026-09-26T20:26:24Z | B2-267-touch-law-patrol-prompt | landed-family | LANDED | all three B2-237 touch-law clauses appended to the live drift-patrol DB prompt (readback 4438 chars, block x1... | OK 4290B | current |
| 356 | 2026-09-26T20:27:24Z | B2-155-seed-paired-harness | landed-family | LANDED | law-D TARA gate executor landed: tools/seed_paired_uplift.py (gate + F2 flag-only compare + offline --demo re... | OK 4868B | current |
| 357 | 2026-09-26T20:27:26Z | B2-344-dangling-disposition | free-text | FILED | disposition filed and the brief falsifier FIRED: chain shrank 9873 to 7758 rows post-B2-83-pin erasing restor... | OK 5834B | current |
| 358 | 2026-09-26T20:27:32Z | B2-281-yearfirst-keeper-pin | landed-family | LANDED | check7 now pins the 0.90 year-first keeper row byte-equal (77/77 green on live ledger); scratch demo proves t... | OK 3080B | current |
| 359 | 2026-09-26T20:28:20Z | B2-307-mimo-failure-classes | landed-family | LANDED | mimo_watch non-HTTP failure classes landed: _nonhttp_error_row parses refused/timeout/dns from the URLError r... | OK 3237B | current |
| 360 | 2026-09-26T20:29:01Z | B2-183-cool-shit-people | landed-family | LANDED | Top 10 free-compute/agent-fleet builders filed to fleet canon watch/inbox/FLEET_CANON_COOL_SHIT_20260926.md (... | OK 4711B | current |
| 361 | 2026-09-26T20:29:10Z | B2-125-bridge-go-blocked | free-text | BLOCKED | bridge GO card BLOCKED AS OWED on current bytes: Drive client absent (both install paths), repo not a junctio... | OK 4450B | current |
| 362 | 2026-09-26T21:02:00Z | B2-148-seal-hook-adopts-seq-scheme | landed-family | LANDED | md_record_seal register events now carry a BigInt-exact seq per the B2-40 scheme (fold-exact seqOf/nextSeq po... | OK 4146B | current |
| 363 | 2026-09-26T20:30:13Z | B2-275-pin-law-check7-fail-output | landed-family | LANDED | check7 FAIL branch now prints the B2-259 law's four required steps verbatim under the FAIL detail (spec first... | OK 3848B | current |
| 364 | 2026-09-26T20:30:41Z | B2-192-verdict-store-amend | landed-family | LANDED | Owning doc amended (option b): BURN_JUDGE_LANE_BUILD_20260925.md section 2 now names queue/lanes/<lane>/trail... | OK 4732B | current |
| 365 | 2026-09-26T20:30:43Z | B2-149-norminbox-root-strip | landed-family | LANDED | verification-landing per B2-238: normInboxFile absolute-host-root strip already in bytes under the B2-149+B2-... | OK 5014B | current |
| 366 | 2026-09-26T20:30:48Z | B2-309-queue-registration-reseal | landed-family | LANDED | QUEUE.md registration re-seal landed: chain proven unbroken across the B2-255 sweep (pre-sweep seal 392929B8 ... | OK 4340B | current |
| 367 | 2026-09-26T20:31:37Z | B2-389-selftests-namespace | landed-family | LANDED | Both *_test.py batteries moved to tests/selftests/*_selftest.py with wrappers repointed and roots fixed; patr... | OK 3429B | current |
| 368 | 2026-09-26T21:12:00Z | B2-158-games-history-fresh-eyes | landed-family | LANDED | games history dig (tabletop/MMO/on-chain) against our estate (Mountain, Ossuary, Virtue Marks): 5 steals with... | OK 6922B | re-burned later (latest line 372) |
| 369 | 2026-09-26T20:32:55Z | B2-314-census-patrol-liveness-tripwire | landed-family | LANDED | mag.cmd context-pack now reads the last bracketed START stamp from logs/census_patrol.log and names darkness ... | OK 3993B | current |
| 370 | 2026-09-26T20:33:05Z | B2-188-transport-tripwire | landed-family | LANDED | across-runs transport tripwire landed in scripts/build_lane_game.py: run-end scan counts the consecutive HTTP... | OK 4819B | current |
| 371 | 2026-09-26T20:33:47Z | B2-325-thoughtbank-preflight | landed-family | LANDED | thought-bank preflight falsifies the recipe's own assumption: exportable bank = 1,841 unique reasoning parts ... | OK 4266B | current |
| 372 | 2026-09-26T20:34:00Z | B2-158-games-history-fresh-eyes | landed-family | LANDED | games history dig (tabletop/MMO/on-chain) against our estate (Mountain, Ossuary, Virtue Marks): 5 steals with... | OK 6922B | current |
| 373 | 2026-09-26T20:34:09Z | B2-159-physcomp-gstd-fresheyes | landed-family | LANDED | fresh-eyes research receipt: gstd front door still 404-dark tonight but upstream repo alive again (pushed 202... | OK 7527B | current |
| 374 | 2026-09-26T20:34:24Z | B2-324-sibling-module-retired-headline-sweep | landed-family | LANDED | sweep clean: zero retired-headline hits in the 7 sibling modules (only audit_dungeon hits are the B2-214-fixe... | OK 3897B | current |
| 375 | 2026-09-26T20:34:53Z | B2-204-dormant-skip | landed-family | LANDED | dormant skip landed at the pick_provider candidate seam (models/quota.py): p.get('dormant') now skips before ... | OK 3609B | current |
| 376 | 2026-09-26T20:36:20Z | B2-336-conftest-gap-gate | landed-family | LANDED | suite-wide gap-log pollution gate landed: tests/conftest.py created (did not exist) with autouse fixture sett... | OK 3458B | current |
| 377 | 2026-09-26T20:36:46Z | b2-211-patrol-cron-charter | owed | OWED-CHARTERED | drift-patrol-cron writer charter landed at watch/inbox/DRIFT_PATROL_CRON_CHARTER_20260926.md with absence fil... | OK 4644B | current |
| 378 | 2026-09-26T20:45:00Z | B2-193-caw-f2-spotcheck-protocol | landed-family | LANDED | F2 spot-check protocol pinned in SPOTCHECK_PROTOCOL_20260926.md: denominator = verdicts with max axis confide... | OK 4324B | current |
| 379 | 2026-09-26T20:37:40Z | B2-299-fold-verify-cwd | landed-family | LANDED | fold verify cwd trap closed: index_fold_host.mjs verify now joins inbox-relative item paths against INBOX_DIR... | OK 3515B | current |
| 380 | 2026-09-26T20:38:21Z | B2-206-judge-independence | landed-family | LANDED | Mechanism correction landed: the dwf facade has no per-subagent model (skill bytes: session model only), so j... | OK 6553B | current |
| 381 | 2026-09-26T20:38:44Z | B2-360-fkb-process-lock | landed-family | LANDED | FKB cross-process lock landed: signatures.json.lock sidecar (msvcrt.locking, fcntl fallback, fail-closed 15s ... | OK 4107B | current |
| 382 | 2026-09-26T20:39:30Z | B2-393-chain-byte-exact-io | landed-family | LANDED | all four chain write sites byte-exact (verkle_knot _rewrite_chain write_bytes, append newline='', both flag s... | OK 4103B | current |
| 383 | 2026-09-26T20:39:32Z | b2-300-handoff-kernel-map | landed-family | LANDED | Seed-from-handoffs kernel map landed: watch/inbox/SEED_RIB_HANDOFF_KERNEL_20260926.md with 8-surface byte cen... | OK 4086B | current |
| 384 | 2026-09-26T20:39:58Z | B2-228-margin-erratum | landed-family | LANDED | Brief's reading confirmed on bytes and erratum appended to B2_17 receipt (append-only): 'stale by 0.006' name... | OK 4248B | current |
| 385 | 2026-09-26T21:40:00Z | B2-291-estate-mcp-docker | landed-family | LANDED | B2-291 landed and running: compose mcp service (mag-mcp, healthy, restart unless-stopped) serves the estate T... | OK 4778B | current |
| 386 | 2026-09-26T20:41:34Z | b2-269-serve-decline | free-text | DECLINED | opencode serve DECLINED on the record: free lane client-locked 403 either way (B2-261 own finding) so serve=u... | OK 3832B | current |
| 387 | 2026-09-26T20:41:39Z | B2-367-media-register-scope-headers | landed-family | LANDED | _scope_header rows prepended to both registers (qagg cards 5012 lines keyed q_num vs original media 1893 line... | OK 3929B | current |
| 388 | 2026-09-26T21:05:00Z | B2-207-constitutional-filter-producer-record | landed-family | LANDED | producer_model + same_family_refused threaded into CritiqueResult (fields + to_dict) and filter_response (fam... | OK 4272B | current |
| 389 | 2026-09-26T20:42:55Z | B2-399-shared-surface-split | landed-family | LANDED | shared_surface split landed: scan_events_log moved byte-for-byte to new sibling mag/events_scan.py (B2-248 pr... | OK 4736B | current |
| 390 | 2026-09-26T20:43:10Z | B2-262-quantity-adjacency-probe | free-text | NOT_CLEAN_NO_EDIT | adjacency-vs-window probe over all 6,242 drops and 273 candidate sites, three adjacency variants: strict matc... | OK 5569B | current |
| 391 | 2026-09-26T20:44:07Z | B2-194-gemini-native-kind | landed-family | LANDED | kind gemini_native staged fixture-first: chat_provider dispatch + _chat_gemini_native (generateContent, x-goo... | OK 6195B | current |
| 392 | 2026-09-26T20:44:42Z | b2-277-blind-exit-split | landed-family | LANDED | Pre-push census exit-class split landed: exit 1 STALE stays WARN-ONLY (t40, TODO-FLIP note rescoped to exit-1... | OK 4962B | current |
| 393 | 2026-09-26T20:45:27Z | B2-410-outcome-vocabulary | landed-family | LANDED | outcome vocabulary registry landed in mag/skill_ledger.py: OUTCOME_WIN + OUTCOME_REGISTRY (6 values with mean... | OK 3850B | current |
| 394 | 2026-09-26T21:20:00Z | B2-229-audit-seed-adventure-learn | landed-family | LANDED | audit seed materialized at AUDIT_SEED_ADVENTURE_LEARN_20260926.md (6,827 B, SEED-RIB order): laws first (13-l... | OK 4141B | current |
| 395 | 2026-09-26T21:52:00Z | B2-295-openrouter-free-rotation | landed-family | LANDED | B2-295 verify-then-add rotation landed: tools/openrouter_free_gate.py gates each :free candidate with one liv... | OK 3468B | current |
| 396 | 2026-09-26T20:46:44Z | B2-264-links-seal-recovery | owed | OWED-PARTIAL | Seal-byte recovery blocked where the brief predicted (USN and VSS both access-denied, not admin); transcript ... | OK 6027B | current |
| 397 | 2026-09-26T20:46:44Z | B2-306-cipher-pin | landed-family | LANDED | 0.5 dotted cipher bucket pinned in check7: all 16 live 0.5 rows extracted verbatim into B2_306_CIPHER_KEEPER_... | OK 4449B | current |
| 398 | 2026-09-26T20:47:36Z | B2-425-operator-go-surface | landed-family | LANDED | canonical operator-GO surface landed: watch/inbox/OPERATOR_GO.jsonl (operator_go.v1: ts, gate, order, source_... | OK 3756B | current |
| 399 | 2026-09-26T20:48:01Z | B2-506-census-prose-fossils | landed-family | LANDED | catalog_rescan C6 story states the engine split (757667 = pre-wiring semantics only) and mcp_server posture n... | OK 3150B | current |
| 400 | 2026-09-26T20:48:13Z | B2-404-qdrop-canonical-numbering-guard | landed-family | LANDED | qdrop_canonical.py: resolver takes id+ts only, refuses positions, canonical numbers only from receipt-anchore... | OK 5301B | current |
| 401 | 2026-09-26T21:32:00Z | B2-265-seat-links-row-refile | landed-family | LANDED | zcode-seat-20260926 LINKS.jsonl:335 row repaired via the B2-26 field-only backfill: op dropped, canonical_sha... | OK 4804B | current |
| 402 | 2026-09-26T20:49:30Z | B2-208-staleness-tripwire | landed-family | LANDED | staleness_tripwire landed in drift_pairs_stamp: alarms when no regime_*/graduation gate in 14 days while trai... | OK 5575B | current |
| 403 | 2026-09-26T20:50:20Z | B2-332-catalog-refresh-decision | landed-family | LANDED | Refresh flow decided: v3 module atomic replace (mag/catalog_rebuild.py via B2-103); map now 489,548 rows, tag... | OK 4010B | current |
| 404 | 2026-09-26T20:50:37Z | b2-316-checkbox-receipt-gate | landed-family | LANDED | Checkbox-receipt gate landed standing: tools/checkbox_receipt_gate.py (Open-section boundary fix, 71-row B2-2... | OK 4807B | current |
| 405 | 2026-09-26T20:50:54Z | B2-481-derived-pair-refresh | landed-family | LANDED | FTS rebuilt from the 489,548-row map via redirected B2_481_fts_build.py (B2_22 artifact untouched); joins gre... | OK 3958B | current |
| 406 | 2026-09-26T20:51:05Z | B2-284-claim-tests-extension | landed-family | LANDED | claim law extended to shared test surfaces: QUEUE.md header paragraph now accepts a tests/ path claim (or mod... | OK 4517B | current |
| 407 | 2026-09-26T20:51:10Z | B2-308-mimo-error-headers | landed-family | LANDED | _http_error_row captures Server/Content-Type as resp_server/resp_content_type so opaque or binary bodies are ... | OK 5365B | current |
| 408 | 2026-09-26T20:51:20Z | B2-230-assignment-law | landed-family | LANDED | assignment law written as build_sections docstring before B2-71 bar-raise: single-label first-match declared,... | OK 4488B | current |
| 409 | 2026-09-26T20:51:58Z | B2-439-wave-driver-scheduling-truth | landed-family | LANDED | wave_driver scheduling truth registered: fresh schtasks census (240 tasks) confirms zero wave_driver/m12_pair... | OK 5006B | current |
| 410 | 2026-09-26T20:51:59Z | B2-414-icon-drop-icon-thread | landed-family | LANDED | dead ico_line removed from drop()'s .cmd (spec first in docstring: icons belong on .lnk via IconLocation); ic... | OK 4124B | current |
| 411 | 2026-09-26T22:02:00Z | B2-297-living-downgrade-detector | landed-family | LANDED | B2-297 landed: KNOWN_LIVING_PATHS watchlist in mag/shared_surface.py validate warns living-downgrade when LIN... | OK 3582B | current |
| 412 | 2026-09-26T20:52:34Z | B2-458-builder-pyc-audit | free-text | CONFIRMED | Audit confirms both build-book specs wired in seed_v2.py: purge+exclude arms keep .pyc out of MANIFEST and zi... | OK 3940B | current |
| 413 | 2026-09-26T20:52:53Z | B2-266-no-erratum | erratum/correction | NO_ERRATUM | erratum declined on bytes: a genuine B2-172 receipt EXISTS (all five sections, LEDGER row, INDEX registration... | OK 4954B | current |
| 414 | 2026-09-26T21:45:00Z | B2-273-ratchet-growth-law | landed-family | LANDED | growth law landed (refresh-size-over-expiry): baseline-update stamps accepted_lines into file-too-long claims... | OK 4351B | current |
| 415 | 2026-09-26T20:53:15Z | b2-330-junction-diff | free-text | PROVEN | Junction falsifier PROVEN by bytes: repo/training -> memory/training junction walked both views, 24/24 files ... | OK 3991B | current |
| 416 | 2026-09-26T20:53:47Z | B2-322-gap-denominator-refresh | landed-family | LANDED | union-driver cell refreshed from raw.jsonl bytes (184 attempts, 156 ok = 84.78 pct, 128 unique completed of 1... | OK 3599B | current |
| 417 | 2026-09-26T20:54:16Z | b2-349-rotation-owed | owed | OWED-OPERATOR-GATED | Credential rotation OWED operator-gated: console revocation is a human action; re-verified exposure on bytes ... | OK 4045B | current |
| 418 | 2026-09-26T20:55:55Z | B2-310-attribution-audit | landed-family | LANDED | 24 moved ids swept across QUEUE rows, receipts, and LEDGER (zero ledger rows named a moved id as landing slug... | OK 5502B | current |
| 419 | 2026-09-26T22:00:00Z | B2-311-whole-drop-year-context-clause | landed-family | PROBE LANDED, CLAUSE REJECTED (falsifier branch) | clause 2b (whole-drop single distinct year) probed over all 6,242 drops before any edit: multiset guard EQUAL... | OK 5165B | re-burned later (latest line 422) |
| 420 | 2026-09-26T20:56:12Z | B2-429-law-registry-index-registration | landed-family | LANDED-ALTERNATE-ROUTE | direct add of memory/law/registry.json blocked by the B2-147 writer guard (two live refusals; file is owned b... | OK 5493B | current |
| 421 | 2026-09-26T20:56:16Z | B2-335-testborn-candidate | landed-family | LANDED | test-born candidate gap-c4f076b1e0205c27 (candidates.jsonl:95) flipped new -> rejected via the repo's own upd... | OK 4471B | current |
| 422 | 2026-09-26T22:00:00Z | B2-311-whole-drop-year-context-clause | landed-family | PROBE LANDED, CLAUSE REJECTED (falsifier branch) | clause 2b (whole-drop single distinct year) probed over all 6,242 drops before any edit: multiset guard EQUAL... | OK 5165B | current |
| 423 | 2026-09-26T20:57:19Z | B2-396-mag-tasks-whitelist | landed-family | LANDED | Sanctioned-task set spec-first in configs/sanctioned_scheduled_tasks.yaml (13 rows with sources); lattice whi... | OK 3653B | current |
| 424 | 2026-09-26T20:58:11Z | B2-326-qlora-smoke | owed | OWED | Run blocked on hardware bytes, filed owed not faked: this box has one AMD Radeon RX 5600 XT (4GB WMI cap), no... | OK 4308B | current |
| 425 | 2026-09-26T20:58:43Z | B2-451-scenarios-hook-pins | landed-family | LANDED | scenario-gate hook pairing pins landed: tests/test_scenarios_gate_hook_pin.py (4 green) reads the B2-164 bloc... | OK 4634B | current |
| 426 | 2026-09-26T22:10:00Z | B2-327-research-transport-precheck | landed-family | LANDED | transport precheck gate landed: tools/transport_precheck.py (HEAD-first with range-GET fallback; wall classif... | OK 4474B | current |
| 427 | 2026-09-26T21:00:30Z | B2-274-carrier-ownership-law | landed-family | LANDED | ownership law landed at the grammar (CENSUS_CLAIM_RE comment block): parser owned by regex+comment, frozen ve... | OK 6359B | current |
| 428 | 2026-09-26T21:00:31Z | B2-443-dwf-error-census | landed-family | LANDED-CENSUS-AS-RECORD | 896 model.network.failed across 375 dwf actor sessions in 27 runs (09-20..09-26 logs), invisible to _belongs ... | OK 4899B | current |
| 429 | 2026-09-26T22:20:00Z | B2-459-seed330-reply-draft | landed-family | LANDED | B2-459 landed: 3.3.0 X reply draft parked at SEED_PUBLIC_PACK_20260925.md bottom as append-only addendum; num... | OK 2463B | current |
| 430 | 2026-09-26T21:01:26Z | B2-449-flip-go-transcription | owed | OWED-DORMANT | condition unmet: OPERATOR_GO.jsonl exists (B2-425 landed it) but holds only the burn-wave gate row; the B2-10... | OK 3177B | current |
| 431 | 2026-09-26T21:01:42Z | B2-394-lifecycle-writer-identity | landed-family | LANDED | writer chain named from bytes: track_lifecycle_into_improve (hardcoded where='GET /api/v1/lifecycle') called ... | OK 4705B | current |
| 432 | 2026-09-26T21:02:48Z | B2-477-sep29-p0-reverify-checkout | landed-family | LANDED | all three pre-Studio checks green on this checkout 2026-09-26: HEAD rbxlx commit is 027baff4c (the B2-108 gat... | OK 3687B | current |
| 433 | 2026-09-26T21:03:56Z | B2-345-lifecycle-reason-carry | landed-family | LANDED | Lifecycle carry (B2-80 should/should_reason/signals) now flows into both track_loop_gap sinks: training emit ... | OK 5345B | current |
| 434 | 2026-09-26T21:04:49Z | SW-03-board-repair-note | free-text | BOARDFIX | concurrent whole-file board write reverted QUEUE.md to a stale generation erasing 11 SW-03 flips and the enti... | MISSING | current |
| 435 | 2026-09-26T22:26:00Z | B2-436-width15-validation-arm | landed-family | LANDED | B2-436 landed: B2-98 counter confirmed LIVE (tools/provider_error_tally.py + tests + LEDGER 18:44:00Z, baseli... | OK 3440B | current |
| 436 | 2026-09-26T22:20:00Z | B2-346-verdict-flip-row-link | landed-family | LANDED | per-piece flip link landed: lifecycle rows carry piece (name minus lifecycle_gap:/lifecycle_waste: prefix), p... | OK 4220B | current |
| 437 | 2026-09-26T21:06:31Z | B2-492-snapshot-differ | landed-family | LANDED | provider-probe snapshot differ landed: tools/provider_snapshot_differ.py diffs the two newest memory/improve/... | OK 3449B | current |
| 438 | 2026-09-26T21:06:31Z | B2-463-window-convention | landed-family | LANDED | asekin window convention filed at the ledger site before row 2 (watch/inbox/asekin113/WINDOW_CONVENTION_20260... | OK 4221B | current |
| 439 | 2026-09-26T22:48:00Z | B2-482-matched-copy-audit | landed-family | LANDED | B2-482 landed: 64 files hashed, 0/32 dual-copy pairs byte-identical while 32/32 agree in byte length; matched... | OK 3764B | current |
| 440 | 2026-09-26T21:09:01Z | B2-382-shell-resolution-pins | landed-family | LANDED | 4 pytest pins landed for the B2-85 mag-side resolutions (legacy_audit._enum_procs, platform_kill._enum_host_p... | OK 3774B | current |
| 441 | 2026-09-26T21:09:15Z | B2-312-post-drop-ts-rejected | free-text | REJECTED | post-drop-ts ineligibility clause REJECTED BY FALSIFIER: full 6242-drop sweep through the real module confirm... | OK 5119B | current |
| 442 | 2026-09-26T21:09:52Z | B2-476-envelope-source-cited-contract | landed-family | LANDED | proven-width table (7 receipt-cited rows incl. the 50-wide workflow-children storm as counterexample, the 3/6... | OK 4976B | current |
| 443 | 2026-09-26T22:30:00Z | B2-362-fkb-singleton-log-search | landed-family | LANDED | log-tail search landed: failure_kb search_log + reverse-chunk _tail_lines (bounded, never loads the 39MB log ... | OK 3725B | current |
| 444 | 2026-09-26T21:10:48Z | steering-theory | steal | steal | end-to-end gap FOUND: B2-64 dashboard live + verified (renders T1-T6 from teleo_drift_stamps.jsonl, 4/6 pairs... | OK 4075B | re-burned later (latest line 595) |
| 445 | 2026-09-26T21:10:48Z | stego-canon-pipeline | steal | steal | MRPOOL_SYMBOL_DICT_v1.json LANDED (4 entries, JSON-validated): the 3 pass-_c prose entries upgraded to the mi... | OK 3260B | re-burned later (latest line 650) |
| 446 | 2026-09-26T21:10:48Z | world-models-multi-agent | steal | steal | ARM-0 lookup test EXECUTED through the real grader: receipt with asserted values copied verbatim from fixture... | OK 3224B | re-burned later (latest line 662) |
| 447 | 2026-09-26T21:11:14Z | B2-361-fkb-verify-tripwire | landed-family | LANDED | python -m mag.failure_kb verify landed: read-only recount of the log by sig (rebuild_index oracle) naming ind... | OK 5371B | current |
| 448 | 2026-09-26T21:12:05Z | B2-323-dated-numbers | landed-family | LANDED | dated-number rule + tripwire tools/game_module_dated_numbers.py: real-estate-shaped numbers in game-module lo... | OK 4962B | current |
| 449 | 2026-09-26T21:12:40Z | b2-406-bridge-decouple | landed-family | LANDED | Bridge-symbol linkage DECOUPLED and landed: bridge family is channel art not drop-linked - census scales with... | OK 4674B | current |
| 450 | 2026-09-26T21:13:05Z | B2-409-caption-sha-pin | landed-family | LANDED | have-row sha invariant pinned: tools/caption_ledger_sha_check.py recomputes all 2689 have-row shas from disk ... | OK 3848B | current |
| 451 | 2026-09-26T22:58:00Z | B2-486-queue-dupes-gate | landed-family | LANDED | B2-486 landed: B2_167_census.py promoted to tools/queue_dupes_check.py (strict+tolerant row-start ids, exit 1... | OK 3765B | current |
| 452 | 2026-09-26T21:15:22Z | B2-424-envelope-harvest | landed-family | LANDED | one-command envelope harvest landed: tools/envelope_harvest.py clusters 191 metadata.json of sess_fd5ec147 in... | OK 3428B | current |
| 453 | 2026-09-26T22:40:00Z | B2-402-improve-loop-test-isolation | landed-family | LANDED | both test files isolated via module-constant monkeypatch: improve_loop (HANDOFF_DIR/TRAIL/EVENTS_PATH to tmp;... | OK 4602B | current |
| 454 | 2026-09-26T21:17:26Z | middle-path-doctrine | steal | steal | State XI adoption patch DRAFTED (byte-minimal, nothing self-applied, operator gate): 3 one-line diffs to MANI... | OK 3249B | re-burned later (latest line 684) |
| 455 | 2026-09-26T23:06:00Z | B2-272-prepush-paths-helper | landed-family | LANDED | B2-272 landed: changed-path decision extracted to tools/prepush_paths_changed.py (five cases: dirty-vs-HEAD, ... | OK 3357B | current |
| 456 | 2026-09-26T22:50:00Z | B2-412-icon-drop-fold-repo-pin | landed-family | LANDED | icon_drop fold-outcome arms pinned in tests/test_icon_drop_fold.py (probe sandbox pattern: tmp_path + monkeyp... | OK 3179B | current |
| 457 | 2026-09-26T21:19:07Z | third-way-game | steal | steal | SIX_CHAIR_TELLINGS.json LANDED (6 chairs x 3 beats, JSON-validated, ractor contract holds: one shared_facts b... | OK 2644B | re-burned later (latest line 627) |
| 458 | 2026-09-26T21:19:32Z | build-fold-verify-b | steal | steal | owed t67/t63 grep pair run on shipped rbxlx bytes (383,204b, mtime 15:38): t67 derived join CLOSED (ZONE_REGI... | OK 3410B | current |
| 459 | 2026-09-26T21:20:22Z | B2-392-hot-writer-attributed | landed-family | LANDED | hot re-fold writer ATTRIBUTED: append_verkle_knot amend path _rewrite_chain (whole-file rewrite re-anchoring ... | OK 6573B | current |
| 460 | 2026-09-26T21:20:39Z | B2-401-trail-env-seams | landed-family | LANDED | Env seams landed in the B2-86 shape: seat_registry _trail_path honors MAG_SEAT_REGISTRY_TRAIL, orchestrator _... | OK 6613B | current |
| 461 | 2026-09-26T21:20:46Z | b2-wave-fold | steal | steal | all 5 act items chased to actionable states, nothing fired/armed/edited: b2-53 Grok packet card fire-ready bu... | OK 3783B | re-burned later (latest line 614) |
| 462 | 2026-09-26T23:00:00Z | B2-484-law12-clause-verdict | free-text | PASS (filed 14 days early) | LAW-12 clause verdict PASS, filed 2026-09-26 (deadline 2026-10-10): scenario suite exit 0 (7 cards read-only)... | OK 3988B | current |
| 463 | 2026-09-26T23:18:00Z | B2-282-yearmonth-sweep | landed-family | LANDED | B2-282 landed non-rule arm: full-corpus sweep of 6242 drops with the year-MONTH pattern (+dash variant) found... | OK 3439B | current |
| 464 | 2026-09-26T23:10:00Z | B2-441-provider-tally-envelope-law | landed-family | LANDED | envelope law landed: any wave receipt claiming a 1302 count is invalid without a provider_errors.json (or per... | OK 853B | current |
| 465 | 2026-09-26T21:22:18Z | B2-366-register-overrun | landed-family | LANDED | all 45 ok:false rows of media_register_qagg.jsonl annotated additive in place: 44 tail rows gap_class registe... | OK 3860B | current |
| 466 | 2026-09-26T21:22:59Z | B2-411-fold-training-surface | landed-family | LANDED | _fold_training no longer silent: returns a bounded fold_status dict {ok, outcome/error} that all three caller... | OK 4272B | current |
| 467 | 2026-09-26T23:15:00Z | B2-447-execute-flip-receipt | free-text | EXECUTION OPENED, BLOCKED ON OPERATOR BROWSER STEP (no fabrication) | E0 hash gate re-run and matched (e9f4603a... equals the shipped seal); operator_go resolved honestly: burn-wa... | OK 9090B | current |
| 468 | 2026-09-26T23:25:00Z | B2-471-b2-178-caption-census | landed-family | LANDED | caption census filed at B2_178_caption_census.md: 1234 enrich rows join to 1195 verdict rows (39 unparseable ... | OK 3432B | current |
| 469 | 2026-09-26T21:25:33Z | B2-438-scripts-path-pins | landed-family | LANDED | four runner-driven scripts pinned: scripts/path_pin.py (repo-root pin, SystemExit 2 named refusal, MAG_ALLOW_... | OK 5201B | current |
| 470 | 2026-09-26T23:30:00Z | B2-303-one-error-named | landed-family | LANDED | B2-303 landed: the standing 1 error is tests/test_spore_seed.py (fixture mocker not found, pytest-mock absent... | OK 4047B | current |
| 471 | 2026-09-26T21:26:40Z | B2-426-decay-window | landed-family | LANDED-PARTIAL-FIT | One measured hold from the afterparty mtime timeline: 12-wide burst t78-t83 banked 05:29:14-05:36:30Z then 8m... | OK 5738B | current |
| 472 | 2026-09-26T21:27:08Z | B2-413-icon-drop-pins | landed-family | LANDED | tests/test_icon_drop_escape.py NEW 5 pins gating the B2-377 surface that was probe-only: ps_quote doubling, e... | OK 4810B | current |
| 473 | 2026-09-26T21:27:31Z | b2-375-powershell-tokens | landed-family | LANDED | Powershell token forms landed: new mag/win_powershell.py resolver (which first, System32 + Sysnative candidat... | OK 4755B | current |
| 474 | 2026-09-26T23:35:00Z | B2-494-probe-alarm-surface | landed-family | LANDED | probe alarm surface landed (one mouth): alarm-class runs append exactly one [priority][probe-alarm] line to m... | OK 3488B | current |
| 475 | 2026-09-26T23:38:00Z | B2-457-doctor-403-arm | landed-family | LANDED | B2-457 landed: _classify_chat_failure arms 403 tier_not_allowed as AUTH-DEAD per-key tier fact (defining byte... | OK 3114B | current |
| 476 | 2026-09-26T21:29:59Z | B2-462-asekin-carrier-scan | landed-family | LANDED | asekin carrier status line updated from bytes: grading ledger now exists (B2-463 landed it mid-wave), holds 1... | OK 3763B | current |
| 477 | 2026-09-26T21:30:01Z | doctrine-owed-chase | steal | steal | Picasso owed chase: 1.5 of 3: (b) Splunk tutorial FOUND + fetched w/ verbatim quotes (P. Bhavsar, Sep 21 2026... | OK 3581B | re-burned later (latest line 693) |
| 478 | 2026-09-26T21:30:50Z | free-resource-landscape | steal | steal | Groq bypass MEASURED LIVE on openai/gpt-oss-120b (raw per-call bodies+headers: logs/groq_cache_bypass_2026092... | OK 3434B | re-burned later (latest line 692) |
| 479 | 2026-09-26T23:44:00Z | B2-320-driver-v2-s1-s3 | landed-family | LANDED | B2-320 landed: driver v2 S1-S3 in scripts/union_fullsend_day.py (S1 jitter uniform(0,min(60,2*2^n)) before re... | OK 4013B | current |
| 480 | 2026-09-26T21:32:41Z | B2-408-crash-write-surface | landed-family | LANDED | _log_seat_crash failure path now records a loud console line + importable CRASH_LOG_FAILURES counter (count/l... | OK 3100B | current |
| 481 | 2026-09-26T21:33:24Z | b2-418-chain-marker-pin | landed-family | LANDED | Chain-marker between-headers placement pinned fixture-first: new falsifier test (2-header genuine chain whose... | OK 4549B | current |
| 482 | 2026-09-26T23:52:00Z | B2-333-index-selfseal-decision | landed-family | LANDED | B2-333 landed arm (a): INDEX.json self-item invalidated unsealable-by-design via an exact-string-seq invalida... | OK 3472B | current |
| 483 | 2026-09-27T00:00:00Z | B2-355-checkbox-reaudit | landed-family | LANDED | B2-355 second-pass re-audit landed CLEAN: all 169 checked Open rows carry resolvable receipt pointers on disk... | OK 3364B | current |
| 484 | 2026-09-26T21:35:52Z | b2-433-mimosa-sweep | landed-family | LANDED | Mimosa tail B2-238 sweep resolved as the find-and-pointer arm: both landings verified on bytes (B2_94 receipt... | OK 4458B | current |
| 485 | 2026-09-26T21:35:55Z | B2-420-census-seat-errors-relabel | landed-family | LANDED | Behavioral row seat-errors number now counts only error-kind rows (error/fail/crash/exception markers); lifec... | OK 3537B | current |
| 486 | 2026-09-26T21:36:04Z | B2-440-hunger-ledger-pin | landed-family | LANDED | Drift pin landed: tests/test_hunger_ledger_parity.py 3/3 (end-to-end subprocess parity of both hunger_ledger ... | OK 5424B | current |
| 487 | 2026-09-26T21:36:56Z | b2-445-base-url-spec | landed-family | LANDED | Providers base_url surface spec pinned: doc block above provider_base_url in models/providers.py naming the e... | OK 4306B | current |
| 488 | 2026-09-26T21:37:13Z | B2-488-queue-row-normalizer | landed-family | LANDED | shared tolerant row surface + tripwire + normalizer landed: tools/queue_row_census.py (check names malformed-... | OK 3979B | current |
| 489 | 2026-09-26T21:37:59Z | B2-435-width3-folklore-sweep | landed-family | LANDED | Estate sweep: one live folklore carrier (TETHERED_LINK_STEAL generic Width law) amended with dated frozen reg... | OK 3764B | current |
| 490 | 2026-09-26T21:38:11Z | B2-452-scenario-citation-patrol | landed-family | LANDED | Scenario-card citation liveness wired into every improve --status read (workflow_scenarios block via _scenari... | OK 4571B | current |
| 491 | 2026-09-26T21:38:43Z | B2-403-test-sinks | landed-family | LANDED | decisions sink redirectable via MAG_DECISIONS_LOG (compass decisions_log_path); t1_steering+repack autouse fi... | OK 6021B | current |
| 492 | 2026-09-26T21:38:57Z | BOARD-REPAIR-QUEUE-TRUNCATION | free-text | RECOVERED | SW-07 diagnostic open(w) truncated QUEUE.md at ~20:57Z; board rebuilt to 446 row keys from git 10:45 blob + l... | OK 5309B | current |
| 493 | 2026-09-27T00:08:00Z | B2-380-minter-key-pins | landed-family | LANDED | B2-380 landed: two pins in tests/test_index_fold_host.py run the real add/invalidate minters through _run and... | OK 2968B | current |
| 494 | 2026-09-26T21:40:07Z | b2-454-cache-rate-audit | free-text | BLOCKED-AT-SOURCE | Cache-rate byte audit BLOCKED AT SOURCE - the real finding: zcode-2026-09-26.jsonl (233MB, 264,059 lines) car... | OK 5069B | current |
| 495 | 2026-09-26T21:40:18Z | B2-485-scenarios-verify | landed-family | LANDED | B2-164 landing VERIFIED on bytes: pre-push:280-306 carries the wired conditional invocation, suite green in h... | OK 4169B | current |
| 496 | 2026-09-26T21:42:23Z | B2-456-line-pointer-sweep | landed-family | LANDED | All Open line-number citations into burn-hot files anchor-verified: 2 drift classes re-pointed with dated ann... | OK 4003B | current |
| 497 | 2026-09-26T21:42:37Z | B2-470-links-dedupe-merge | owed | OWED | Merge filed OWED on an impossibility proof: the 27 verdicts exist (20 same=true / 7 false, one lane verdict p... | OK 5749B | current |
| 498 | 2026-09-26T21:42:40Z | B2-442-waves-mode | landed-family | LANDED | --waves mode landed in provider_error_tally: createdAt-gap clustering (default 10min) emits per-wave totals b... | OK 4352B | current |
| 499 | 2026-09-27T00:14:00Z | B2-427-registry-append-only | landed-family | LANDED | B2-427 landed: configs/workflow_registry_baseline.json pins per-line sha256 of all 25 REGISTRY.jsonl rows plu... | OK 3280B | current |
| 500 | 2026-09-26T21:42:49Z | B2-450-scenarios-commit-block | free-text | PARTIAL_BLOCKED | commit arm blocked by shared state: .git/index.lock held since 16:54 local by four hung git PIDs (11672/29748... | OK 5034B | current |
| 501 | 2026-09-26T21:42:53Z | B2-351-secret-scan-schedule | landed-family | LANDED | MagSecretScanWeekly schtask (Mon 06:40) + SECRET_SCAN_BEAT.jsonl + attention.md alert gate; live beat green (... | OK 3458B | current |
| 502 | 2026-09-26T21:43:41Z | B2-493-provider-probe-block | landed-family | LANDED | status_summary now carries a labeled provider_probe block {last, cadence_days 7.0, due from provider_probe_du... | OK 4420B | current |
| 503 | 2026-09-26T21:44:03Z | B2-140-armc-closeout-owed | owed | OWED | Arm C 200-leg did not land: full attempt killed at 66min/1-of-30 (partials preserved byte-verbatim); honest s... | OK 3304B | current |
| 504 | 2026-09-26T21:44:42Z | B2-448-post-link-recheck | landed-family | LANDED | post-posting re-check landed as flip-card step 5.5 (E5.5a anonymous curl after share change, E5.5b sha must e... | OK 4197B | current |
| 505 | 2026-09-26T21:45:09Z | b2-479-exposure-census | landed-family | LANDED | Reset-day exposure census landed: 1,134 uncommitted paths classified; scoped commit 6d417abd5 holds the 18 la... | OK 4555B | current |
| 506 | 2026-09-26T21:49:41Z | B2-472-corpus-prune-report | landed-family | LANDED | corpus prune report landed (json data + md card): 1390/1394 class rows joined to real paths via the runner de... | OK 4767B | current |
| 507 | 2026-09-26T21:51:11Z | rsi-harness | steal | steal | LAW-12 provenance patch FILED as paste-ready amendment (registry untouched, B2-163 lane owns): byte-exact old... | OK 3014B | re-burned later (latest line 616) |
| 508 | 2026-09-26T21:51:25Z | middle-path-doctrine | steal | steal | receipt-contract States I-XI DRAFTED w/ ablation rows from measured usage (505 ledger one_lines are fresh com... | OK 3140B | re-burned later (latest line 684) |
| 509 | 2026-09-26T21:51:25Z | b2-wave-fold | free-text | resolved | B2-59 MIPROv2 hold RESOLVED on act-item (e) condition 1: all 5 owed dspy teleprompt files read in full from t... | OK 3168B | re-burned later (latest line 614) |
| 510 | 2026-09-26T21:51:57Z | b2-wave-fold | free-text | FALSIFIER FIRED, LOCK OWED | b2-wave-fold falsifier counter check: next-50 window after the 16:47:55Z baseline closed FIRED (11 correction... | OK 2736B | re-burned later (latest line 614) |
| 511 | 2026-09-26T21:52:11Z | b2-504-fts5-spike-guard | landed-family | LANDED | fts5 spike re-run guard landed, both arms: baseline FORCES the scan path in-process (absent FTS_DB injection,... | OK 5174B | current |
| 512 | 2026-09-26T21:52:17Z | b2-wave-fold | steal | steal | concurrent-claim falsifier TRIGGERED in its own next-50 window (16:48-18:40Z: 11 correction/erratum/renum row... | OK 2736B | re-burned later (latest line 614) |
| 513 | 2026-09-26T21:52:48Z | judge-lane-spec | steal | steal | GATE_VERDICT_V2 emitter spec FILED (patch drafted, nothing applied): zero-emitter gap byte-true (gate_drop_v2... | OK 3858B | re-burned later (latest line 594) |
| 514 | 2026-09-26T21:53:12Z | third-way-game | steal | steal | THIRD_WAY_ACT3_STUB.json LANDED (valid JSON, per-fact source pointers, no game code) closing the prose-bound ... | OK 3103B | re-burned later (latest line 627) |
| 515 | 2026-09-26T21:53:40Z | steering-theory | steal | steal | --live flag BUILT on tools/probe20_run.py (117 insertions 0 deletions, demo/seed paths byte-untouched): 20 ur... | OK 2804B | re-burned later (latest line 595) |
| 516 | 2026-09-26T21:53:40Z | steering-theory | steal | steal | probe20 stamp bridge BUILT: tools/probe20_stamp.py (default-dry, verdict via probe20_run own evaluate(), idem... | OK 2938B | re-burned later (latest line 595) |
| 517 | 2026-09-26T21:53:52Z | queue-field | free-text | real | judge + builder roam: 6 rows stamped (Q-031, Q-047, Q-022, Q-026, Q-027, Q-029), index 30/50 roamed, nothing ... | OK 2777B | re-burned later (latest line 604) |
| 518 | 2026-09-26T21:54:51Z | B2-475-real-limits | landed-family | LANDED | zai-org/ZCode vendored at corpus/library/zcode-zai-org/repo; THE REAL LIMITS from source with file:line citat... | OK 7255B | current |
| 519 | 2026-09-26T21:59:27Z | middle-path-doctrine | steal | steal | C8 falsifier FOURTH reading, census pinned 505 rows (518 by session end, lanes live): classes hold over min-1... | OK 2612B | re-burned later (latest line 684) |
| 520 | 2026-09-26T22:08:42Z | prompt-uplift-lane | steal | steal | uplift RUNBOOK drafted (5-step wiring: PIN seed hash -> uplift a copy -> UNPIPED checker call -> reject-and-r... | OK 3650B | re-burned later (latest line 568) |
| 521 | 2026-09-26T22:08:42Z | adversarial-self-probes | steal | steal | PROBE-C MISSED (first detector-miss booked vs the 1-per-20-fires cap): forged prose-in-fresh_failure_mode row... | OK 4559B | re-burned later (latest line 640) |
| 522 | 2026-09-26T22:08:42Z | stego-canon-pipeline | steal | steal | falsifier-1 countdown CONFIRMED: 1d 16h 26m 42s remaining (deadline 09-28 14:30:19Z): no verbatim twin of Off... | OK 3348B | re-burned later (latest line 650) |
| 523 | 2026-09-26T22:56:09Z | openrouter-keymeta-persist | steal | steal | openrouter /key bodies persisted on disk (B2_128_keymeta_results.json, both keys 200: key1 usage 4.630361878,... | OK 4495B | current |
| 524 | 2026-09-26T22:58:11Z | B2-114-groq-third-lane-decision | landed-family | LANDED | groq third chat lane decision REGISTERED SKIP: fresh 2-call probe proved openai/gpt-oss-20b listed AND served... | OK 6771B | current |
| 525 | 2026-09-26T23:02:18Z | B2-124-paste-door-consolidation | landed-family | LANDED | B2-124 paste_pipeline door consolidation LANDED: _canonical_footer now routes every extracted URL through lin... | OK 5856B | current |
| 526 | 2026-09-26T23:03:50Z | B2-142-cerebras-community-dig | landed-family | LANDED | cerebras community usage dig landed: trial-era patterns are speed-run demos, coding-agent DELEGATION (docs/li... | OK 13659B | current |
| 527 | 2026-09-26T23:05:00Z | b2-476-deep-compute-b2301-full-normals | landed-family | LANDED | deep lane picked (a) B2-301 full-normals combined-world hill rebuild at V2 glossary: 24 fresh builder calls (... | OK 11525B | current |
| 528 | 2026-09-26T23:13:23Z | B2-138-pack-retention-law | landed-family | LANDED | pack retention law LANDED before pack #2 (2026-10-04 window): watch/inbox/PACK_RETENTION_LAW_20260926.md (IND... | OK 6471B | corrected by 530 |
| 529 | 2026-09-26T23:14:19Z | B2-133-cerebras-consumer-purge | landed-family | LANDED | cerebras consumer purge in mag/ LANDED: new mag/dormant.py reads the providers.yaml dormant flag (one reader,... | OK 7664B | current |
| 530 | 2026-09-26T23:16:38Z | B2-138-retention-law-erratum | erratum/correction | ERRATUM | self-feed ids corrected B2-518/519/520 to landed B2-523/524/525: first draft collided with the concurrent B2-... | OK 6471B | corrects 528 |
| 531 | 2026-09-26T23:17:14Z | b2-173-l265-flag-sha-ratchet | landed-family | LANDED | landed: brief premise erratum carried against bytes (LINKS.jsonl:308, B2-06 flag row, already names L265's se... | OK 8172B | current |
| 532 | 2026-09-26T23:21:18Z | build-fold-verify | steal | steal | all 4 charged builds reproduced expected outputs in ACTUAL runs: probe20_stamp --dry exit 0 SKIP, probe20_run... | OK 3943B | re-burned later (latest line 575) |
| 533 | 2026-09-26T23:21:18Z | world-models-multi-agent | steal | steal | grader v2 BUILT (mseat_drift_grade_v2.py, v1 untouched as contrast): enforces grounding_trace per claim, fixt... | OK 3506B | re-burned later (latest line 662) |
| 534 | 2026-09-26T23:21:18Z | doctrine-owed-chase | steal | steal | MAST CONFIRMED at primary (arXiv 2503.13657: 14 failure modes in 3 categories: system design / inter-agent mi... | OK 3591B | re-burned later (latest line 693) |
| 535 | 2026-09-26T23:36:10Z | b2-217-w40-guard-stamp | landed-family | LANDED | first guard-bearing W40 drift stamp executed and verified: 6 rows appended to memory/runs/adv_arc_50/teleo_dr... | OK 8018B | current |
| 536 | 2026-09-26T23:36:30Z | b2-139-ask3-source-repair | landed-family | landed | GROK ASK 3 SOURCE REPAIRED (both halves of the brief OR): 4 link rows mirrored into watch/inbox/LINKS.jsonl:3... | OK 7266B | corrected by 541 |
| 537 | 2026-09-26T23:37:13Z | B2-202-free-rotation | landed-family | LANDED | openrouter :free rotation second pass landed live on 2026-09-26 bytes under the lane's own CLAIM configs/prov... | OK 5698B | current |
| 538 | 2026-09-26T23:37:37Z | b2-522-cost-truth-dormant-reprice-review | steal | steal | B2-522 DECIDED: accept unpriced as the honest unknown, no frozen rate table; byte-proof the B2-133 gate moved... | OK 9400B | current |
| 539 | 2026-09-26T23:40:44Z | b2-181-seed-mcp-server | landed-family | landed | B2-181 LANDED: tools/seed_mcp.py (371 lines, seed_mcp.v0) serves the SEED-RIB over MCP stdio (3 resources: se... | OK 8718B | corrected by 540 |
| 540 | 2026-09-26T23:41:55Z | b2-181-selffeed-renumber | erratum/correction | erratum | correction to the b2-181-seed-mcp-server row filed earlier this window: its one_line named self-fed B2-528/52... | OK 8718B | corrects 539 |
| 541 | 2026-09-26T23:52:30Z | b2-139-ask3-source-repair-erratum | erratum/correction | erratum | ERRATUM to the 23:36:30Z b2-139-ask3-source-repair row: its self-feed ids B2-528/529 were taken by concurrent... | OK 7266B | corrects 536 |
| 542 | 2026-09-26T23:43:04Z | b2-521-cerebras-stragglers-dormant-gate | landed-family | landed | B2-521 LANDED: the six remaining hardcoded cerebras consumers outside the B2-133 seven now gate on mag/dorman... | OK 10479B | current |
| 543 | 2026-09-26T23:48:17Z | b2-239-line-endings | landed-family | landed | B2-239 LANDED: the B2-220 pre-regen CRLF state of q_caption_ledger.jsonl proven a content-preserving ending f... | OK 8230B | current |
| 544 | 2026-09-27T00:03:33Z | b2-151-pid-survivor | landed-family | landed | B2-151 LANDED: pid 37172 never survived as a process, the supervisor STATE ROW survived 12h33m; the fifth sto... | OK 10664B | current |
| 545 | 2026-09-27T00:08:53Z | free-resource-landscape | steal | steal | FREE LANE BOARD compiled, 8 lanes: Groq measured (async token refund, 1:1 requests, TPD unmeasured), NVIDIA l... | OK 3522B | re-burned later (latest line 692) |
| 546 | 2026-09-27T00:08:53Z | rsi-harness | steal | steal | LAW-12-AMD-1 STILL UNAPPLIED (registry byte-checks: no AMD-1 key, zero pre-existing hits, _d OLD line matches... | OK 3570B | re-burned later (latest line 616) |
| 547 | 2026-09-27T00:08:53Z | b2-wave-fold | steal | steal | LEDGER LOCK BUILT + LIVE-TESTED: tools/ledger_lock.py (O_EXCL lockfile + 600s stale-break + fsync append + st... | OK 3720B | re-burned later (latest line 614) |
| 548 | 2026-09-27T01:17:22Z | judge-lane-spec | steal | steal | all 3 pass-g blockers STILL COLD (no _emit_gate_verdict_v2 callers, cascade_exempt_seats lanes.yaml:145 read ... | OK 3518B | re-burned later (latest line 594) |
| 549 | 2026-09-27T01:17:22Z | third-way-game | steal | steal | F1-F12 CONSOLIDATED into THIRD_WAY_FALSIFIER_REGISTRY.md (11 entries after F6/F8 merge: F6 is the law, F8 its... | OK 3704B | re-burned later (latest line 627) |
| 550 | 2026-09-27T01:17:22Z | steering-theory | steal | steal | pipeline BUILT end-to-end and idle w/ zero real rows: --dry SKIPs (no series), probe20 dir empty, port 8080 C... | OK 3625B | re-burned later (latest line 595) |
| 551 | 2026-09-27T01:19:57Z | b2-296-mistral-key-name-case | landed-family | landed | B2-296 LANDED: the falsifier ran literally, pre-fix under wsl -d Ubuntu python3 the exact-case plain-dict loo... | OK 7745B | current |
| 552 | 2026-09-27T01:37:29Z | free-resource-landscape | steal | steal | ractor panel EXECUTED via free lanes (7 seats x OpenRouter ember-1 + DeepSeek rescue): 7/7 partly-sound, cons... | OK 4979B | re-burned later (latest line 692) |
| 553 | 2026-09-27T01:42:30Z | free-resource-landscape | steal | steal | WIDTH LEDGER v1 BORN (the standing concurrency instrument, census-carrier self-steal): consolidated table rec... | OK 4247B | re-burned later (latest line 692) |
| 554 | 2026-09-27T01:45:55Z | b2-wave-fold | steal | steal | organ census: 17 organs inventoried, flywheel law confirmed byte-level; leaks: no content-layer search (FTS5 ... | MISSING | re-burned later (latest line 614) |
| 555 | 2026-09-27T01:47:09Z | b2-wave-fold | steal | steal | billboard census: L0-L6 comm-theory stack confirmed (event log / snapshot / index / board / gallery / pack / ... | OK 6113B | re-burned later (latest line 614) |
| 556 | 2026-09-27T02:00:16Z | b2-wave-fold | steal | steal | Q3 DONE: visor v2 writer-liveness landed (10-surface hardcoded table, LIVE/STALE/FROZEN/DEAD/MISSING by mtime... | OK 2240B | re-burned later (latest line 614) |
| 557 | 2026-09-27T02:10:32Z | free-resource-landscape | steal | steal | gopher-director triage DONE: 146/150 ok unique (cohere 66, deepseek 49, openrouter 31; mistral 0 ok = dead la... | OK 1250B | re-burned later (latest line 692) |
| 558 | 2026-09-27T02:43:47Z | atlas-fix-queue | free-text | done | Q5 INDEX backfill banked late (cancelled by AV question): cross-window receipts folded via sanctioned scripts... | OK 466153B | re-burned later (latest line 565) |
| 559 | 2026-09-27T02:43:47Z | queue-roam | free-text | roam | operator roam over queue fields mid-fire: queue/todo.md + queue_index reviewed, no new orders beyond standing... | OK 36212B | current |
| 560 | 2026-09-27T02:43:47Z | middle-path-doctrine | free-text | pilot | State XI A/B pilot fire 1 of 2-20 complete: ablation-with-rollback beat one-way deletion on middle-path doctr... | OK 14236B | re-burned later (latest line 684) |
| 561 | 2026-09-27T02:50:00Z | adversarial-probes | free-text | adopted | append gate ADOPTED: ledger_lock.py burn-ledger appends face validate_line pre-lock, fail-closed on ImportErr... | OK 2722B | current |
| 562 | 2026-09-27T02:56:00Z | atlas-fix-queue | free-text | done | Q4 receipt-body FTS landed: tools/receipt_body_fts.py indexes 2,084 watch/inbox md/txt bodies (36.7MB db) whe... | OK 2035B | re-burned later (latest line 565) |
| 563 | 2026-09-27T03:10:00Z | atlas-fix-queue | free-text | done | Q7 draft sweep: 5 game-dig veins promoted to saved workflows (runnable by name), 5 superseded drafts retired ... | OK 1794B | re-burned later (latest line 565) |
| 564 | 2026-09-27T03:22:00Z | rsi-harness | free-text | applied | LAW-12-AMD-1 applied at last: trace_provenance axis now demands pre-existing fleet FAIL rows (fixture-minted ... | OK 9849B | re-burned later (latest line 616) |
| 565 | 2026-09-27T03:40:00Z | atlas-fix-queue | free-text | retired | Q6 librarian v1 formally retired: 189/194 arXiv backlog ids resolved to names via Semantic Scholar batch (NAM... | OK 2067B | current |
| 566 | 2026-09-27T03:52:00Z | middle-path-doctrine | free-text | amended | State XI pilot unblock: protocol.receipt_contract amended to authorize the optional Pilot annotation sixth se... | OK 14236B | re-burned later (latest line 684) |
| 567 | 2026-09-27T04:15:00Z | queue-field | steal | steal | queue-field pass b steal: janitor axis of queue_index.jsonl fully triaged (9/9 stamped) but 0 of 50 rows ever... | OK 3410B | re-burned later (latest line 604) |
| 568 | 2026-09-27T04:15:10Z | prompt-uplift-lane | green | green | prompt-uplift-lane green: roblox/prompts V2 amendment laws (ANCHOR/LOCK, judge-must-quote, seed-paired uplift... | OK 3294B | current |
| 569 | 2026-09-27T04:15:20Z | adversarial-self-probes | steal | steal | adversarial-self-probes pass b steal: arXiv 2606.09863 names our probe target (claim-vs-state mismatch, 45-48... | OK 3570B | re-burned later (latest line 640) |
| 570 | 2026-09-27T03:51:31Z | flashx-latency-probe | free-text | declined | speed tier with default thinking ON loses the first-content-token race it is sold for (flashx 5246ms vs flash... | OK 2782B | current |
| 571 | 2026-09-27T05:02:00Z | world-models-multi-agent | steal | steal | Odyssey Agora-2 (humans+agents as peers, live research preview) confirms NPC=SEAT as shipped precedent; Share... | OK 2842B | re-burned later (latest line 662) |
| 572 | 2026-09-27T05:02:10Z | stego-canon-pipeline | steal | steal | pipeline law adopted (interpretation lookup before cold read, receipt to LINKS.jsonl); dictionary seeded from... | OK 3807B | re-burned later (latest line 650) |
| 573 | 2026-09-27T05:02:20Z | doctrine-owed-chase | steal | steal | 3 fetches spent: Kol HaTor ch. 2 fetched live via Sefaria API, reveal-the-end mitzvah line absent (byte-backe... | OK 3431B | re-burned later (latest line 693) |
| 574 | 2026-09-27T04:37:37Z | B2-298-patrol-prompt-persistence | landed-family | LANDED | exposure already closed byte-side by the B2-267 lane: configs/drift_patrol_prompt.txt on disk 4438 bytes sha2... | OK 7511B | current |
| 575 | 2026-09-27T05:40:00Z | build-fold-verify | green | green | build-fold-verify green: all four claimed builds byte-verified on disk (gate_verdict_v2 lanes.yaml:120-158 + ... | OK 3633B | current |
| 576 | 2026-09-27T05:40:10Z | judge-lane-spec | steal | steal | judge-lane-spec re-burn steal: JEV (2609.26550) and Co-Director (2604.24842) abstracts byte-confirm the lande... | OK 3526B | corrected by 606; re-burned later (latest line 594) |
| 577 | 2026-09-27T05:40:20Z | steering-theory | steal | steal | drift.py verdict organ + probe20 honest-series caller adopted as canon instrument pair (typed TRUE/FALSE prob... | OK 3466B | re-burned later (latest line 595) |
| 578 | 2026-09-27T05:55:00Z | third-way-game | steal | steal | fresh species REPORT-CAP-CRASH twice-confirmed (roguelike 33,974B + co-op 40,898B items vs the 32KB report ca... | OK 2184B | re-burned later (latest line 627) |
| 579 | 2026-09-27T06:20:00Z | b2-wave-fold | green | green | pass d green: ATLAS Q1-Q7 closure byte-verified (ledger_lock O_EXCL+600s+validate_line gate, AMD-1 key at reg... | OK 3826B | corrected by 607; re-burned later (latest line 614) |
| 580 | 2026-09-27T06:20:10Z | free-resource-landscape | steal | steal | hammer DeepSeek off-peak half-price window + OpenRouter funded lanes (1000 rpd each, 18-lane math holds) + Gr... | OK 3117B | re-burned later (latest line 692) |
| 581 | 2026-09-27T06:20:20Z | rsi-harness | green | green | pass f green: LAW-12 + AMD-1 verified applied in registry bytes, scenario suite exit 0 (7 cards pass_control ... | OK 3089B | re-burned later (latest line 616) |
| 582 | 2026-09-27T06:35:00Z | third-way-game | steal | steal | co-op-social vein COMPLETE (dwfrun-77a25387, first of five veins): 30/30 findings with evidence, 8 deep-dives... | OK 88529B | re-burned later (latest line 627) |
| 583 | 2026-09-27T06:50:00Z | third-way-game | steal | steal | roguelike-runs vein COMPLETE (dwfrun-ba80ec38, second of five veins): 30/30 findings with evidence, 8 deep-di... | OK 87639B | re-burned later (latest line 627) |
| 584 | 2026-09-27T07:04:02Z | ractor-panel-20260926 | free-text | accept | prereg-attack is the night's sharpest ruling: the cost-unit law's frozen token clause (prereg:47-48) is verif... | OK 19178B | current |
| 585 | 2026-09-27T07:10:00Z | middle-path-doctrine | steal | steal | the Vow, unpeeked seed, positive-sum transmutation, and C9 gated-sharing kit re-confirmed as canon with Ellul... | OK 3108B | re-burned later (latest line 684) |
| 586 | 2026-09-27T07:10:10Z | queue-field | steal | steal | drain pass c steal: the drain is structurally absent not neglected (queue_index 42 open / 8 superseded / 0 cl... | OK 3417B | re-burned later (latest line 604) |
| 587 | 2026-09-27T07:10:20Z | adversarial-self-probes | green | green | live false-success hunt green: spot-checked B2-298-patrol-persistence LANDED row, every byte claim verified o... | OK 3435B | re-burned later (latest line 640) |
| 588 | 2026-09-27T07:25:00Z | third-way-game | steal | steal | creature-farming vein COMPLETE (dwfrun-1011ea86, third of five veins): 30/30 findings with evidence, 8 deep-d... | OK 105782B | re-burned later (latest line 627) |
| 589 | 2026-09-27T07:45:00Z | third-way-game | steal | steal | horror-maze vein COMPLETE (dwfrun-0873f855, fourth of five veins): 30/30 findings with evidence, 8 deep-dives... | OK 121819B | re-burned later (latest line 627) |
| 590 | 2026-09-27T08:05:00Z | world-models-multi-agent | green | green | pass b green: Odyssey ships the shared human+agent sim but publishes no identity-persistence answer (Agora-2 ... | OK 2895B | re-burned later (latest line 662) |
| 591 | 2026-09-27T08:05:10Z | stego-canon-pipeline | steal | steal | growth pass b steal: cold symbol ExploitGym probed live, dictionary miss (dictionary file never built, seed 0... | OK 3973B | re-burned later (latest line 650) |
| 592 | 2026-09-27T08:05:20Z | doctrine-owed-chase | steal | steal | pass b steal: 2 Sefer Raziel archive.org candidates byte-backed (identity unconfirmed, English-OCR RTF item),... | OK 2953B | re-burned later (latest line 693) |
| 593 | 2026-09-27T08:20:00Z | third-way-game | steal | steal | liveops-seasonal vein COMPLETE (dwfrun-5005fbf4, fifth and final vein): 30/30 findings with evidence, 8 deep-... | OK 86059B | re-burned later (latest line 627) |
| 594 | 2026-09-27T08:40:00Z | judge-lane-spec | green | green | pass c green: zero-emitter claim corrected one word (B2-111 landed a real V2 emitter gate_drop_v2 at lane_run... | OK 3803B | current |
| 595 | 2026-09-27T08:40:10Z | steering-theory | green | green | pass b green: drift.py + probe20 verified live on real bytes (gps_50 50 rows: DRIFTING corr 0.1807 self-test,... | OK 3156B | current |
| 596 | 2026-09-27T08:40:20Z | free-resource-landscape | steal | steal | pass c steal: Featherless /v1/models keyless HTTP 200 (22,032 models, 7MB list, per-model pricing) goes hot a... | OK 3237B | re-burned later (latest line 692) |
| 597 | 2026-09-27T09:38:00Z | queue-field | free-text | built | queue-owner close verb LANDED and falsifier PASS all three legs: tools/queue_close.py closed Q-044/Q-045/Q-02... | OK 2405B | re-burned later (latest line 604) |
| 598 | 2026-09-27T09:38:10Z | stego-canon-pipeline | free-text | built | symbol dictionary MINTED per pass-b falsifier: memory/corpus/symbol_dictionary.jsonl carries the ExploitGym e... | OK 6291B | re-burned later (latest line 650) |
| 599 | 2026-09-27T09:50:00Z | adversarial-self-probes | free-text | built | ledger spot-check patrol LANDED per pass-c falsifier: tools/ledger_spot_patrol.py samples 3 LANDED rows per U... | OK 2106B | re-burned later (latest line 640) |
| 600 | 2026-09-27T10:05:00Z | middle-path-doctrine | steal | steal | C9 weakest link sharpened from named gap to mechanism: four gates (worthiness, gift-price, inefficiency, stru... | OK 3398B | re-burned later (latest line 684) |
| 601 | 2026-09-27T10:05:10Z | doctrine-owed-chase | steal | steal | pass three: Major Trends locator majortrendsinjew00scho closed byte-backed as lending-gated (access-restricte... | OK 3038B | re-burned later (latest line 693) |
| 602 | 2026-09-27T10:05:20Z | third-way-game | steal | steal | 4 of 5 atlas game-design laws adopt into the 2d6 stub (settlement-at-death VM ledger, hard-capped Vow interes... | OK 3473B | re-burned later (latest line 627) |
| 603 | 2026-09-27T10:30:00Z | free-resource-landscape | green | green | pass d green: Chutes keyless catalog 200 with 491 chutes but /v1/models 404 and primary source confirms the 2... | OK 3211B | re-burned later (latest line 692) |
| 604 | 2026-09-27T10:30:10Z | queue-field | green | green | pass d verified the drain holds byte-stable: 3 closed / 39 open (34 todo, 5 help_wanted, 0 events) / 8 supers... | OK 2415B | current |
| 605 | 2026-09-27T10:30:20Z | stego-canon-pipeline | steal | steal | pass c steal: second growth probe on Jacob Coxon (canon 6 lines, dictionary miss, inbox-spanning lookup clean... | OK 3166B | re-burned later (latest line 650) |
| 606 | 2026-09-27T11:27:43Z | judge-lane-spec-correction | erratum/correction | CORRECTION | CORRECTION 2026-09-27: discharges the stale assertion in the 2026-09-27T05:40:10Z judge-lane-spec row that th... | OK 135432B | corrects 576 |
| 607 | 2026-09-27T11:27:43Z | b2-wave-fold-correction | erratum/correction | CORRECTION | CORRECTION 2026-09-27: discharges the stale assertion in the 2026-09-27T06:20:00Z b2-wave-fold row that the '... | OK 135432B | corrects 579 |
| 608 | 2026-09-27T11:15:00Z | rsi-harness | free-text | backfilled | cross-slug receipt-row gap repaired by retro row: the _c receipt ( amendment-convention genesis, fixed-sectio... | OK 3841B | re-burned later (latest line 616) |
| 609 | 2026-09-27T11:15:10Z | free-resource-landscape | steal | steal | pass e supplement: LLM7 HOT (unauthenticated /v1/models 200 with 64 models, free tier with anonymous limits p... | OK 2305B | re-burned later (latest line 692) |
| 610 | 2026-09-27T11:15:20Z | doctrine-owed-chase | steal | steal | librarian redo: zero-padding hypothesis CONFIRMED (2007.1558=ARXIV:2007.01558 Bernhardt h-BN 2020, 2008.0277=... | OK 3095B | re-burned later (latest line 693) |
| 611 | 2026-09-27T11:15:30Z | stego-canon-pipeline | free-text | built | dictionary v2 landed per pass-c steals: Jacob Coxon minted in the cold-read shape (canon-anchored pointer, ex... | OK 6291B | re-burned later (latest line 650) |
| 612 | 2026-09-27T11:15:40Z | third-way-game | free-text | built | redo sweep closed the stale-saved-copy regression: all five saved game-dig workflows predated the shrink cras... | OK 3095B | re-burned later (latest line 627) |
| 613 | 2026-09-27T11:50:00Z | world-models-multi-agent | steal | steal | LINKS-349 structure-stripping steal: mathematics as forgetting on purpose maps 1:1 onto the fleet (estate->ca... | OK 3061B | re-burned later (latest line 662) |
| 614 | 2026-09-27T12:00:00Z | b2-wave-fold | green | green | window closed clean: handoff re-keyed (next-window-handoff STATE 09-27 block, CURRENT.md prepended, state sna... | OK 2033B | current |
| 615 | 2026-09-27T12:30:00Z | adversarial-self-probes | steal | steal | pass d steal: patrol ran green in-distribution (11 rows 2 checks 0 warns) but the stress test caught the extr... | OK 3184B | re-burned later (latest line 640) |
| 616 | 2026-09-27T12:30:10Z | rsi-harness | green | green | pass g green: LAW-12-AMD-1 application verified complete and consistent (key exactly once, old wording 0, bot... | OK 3108B | current |
| 617 | 2026-09-27T12:30:20Z | free-resource-landscape | steal | steal | pass f steal: LLM7 freelane CONFIRMED live keyless inference (chat probe HTTP 200 content returned, no auth h... | OK 3249B | re-burned later (latest line 692) |
| 618 | 2026-09-27T13:00:00Z | stego-canon-pipeline | steal | steal | probe three permadeath = steal: second inbox-anchored mint (FLEET_IMPRINT_20260917.md:1297 interpretation pre... | OK 4161B | re-burned later (latest line 650) |
| 619 | 2026-09-27T13:00:10Z | middle-path-doctrine | steal | steal | C9 steward leg sharpens from open edge to the Abolishing Steward design: named, auditable (never seals the ch... | OK 3491B | re-burned later (latest line 684) |
| 620 | 2026-09-27T13:00:20Z | third-way-game | steal | steal | concrete stub-patch spec filed for the 4 adopted atlas laws (vm_ledger settlement, vow_interest 1-per-5 cap 5... | OK 3577B | re-burned later (latest line 627) |
| 621 | 2026-09-27T13:35:00Z | doctrine-owed-chase | steal | steal | Porete pull LANDED 2 attempts 0 failed: TheMirrorsOfSimpleSouls whole file 138,952 bytes sha1-verified, annih... | OK 3265B | re-burned later (latest line 693) |
| 622 | 2026-09-27T13:35:10Z | world-models-multi-agent | steal | steal | cold-boot falsifier grounded 3/3 in fleet machinery: trail dashboard/static/trails/<seat>.jsonl, registry que... | OK 3845B | re-burned later (latest line 662) |
| 623 | 2026-09-27T13:35:20Z | free-resource-landscape | steal | steal | LLM7 authenticity closed for the testable id: codestral-latest proven REAL backend by byte-identical keyed A/... | OK 3530B | re-burned later (latest line 692) |
| 624 | 2026-09-27T13:55:00Z | adversarial-self-probes | steal | steal | pass e measured the vacancy rate honestly: of 329 LANDED rows 73 (22.2 percent) fully token-vacuous + 98 (29.... | OK 2850B | re-burned later (latest line 640) |
| 625 | 2026-09-27T13:55:10Z | stego-canon-pipeline | free-text | built | both pass-d steals executed: permadeath minted (row 3, inbox-anchored, sense-gated canon_hits 4 canon lines, ... | OK 3545B | re-burned later (latest line 650) |
| 626 | 2026-09-27T13:55:20Z | middle-path-doctrine | steal | steal | six-lens salon: Abolishing Steward survives all six chairs (Pratchett hardest hit: the seat dissolves, the Qu... | OK 3368B | re-burned later (latest line 684) |
| 627 | 2026-09-27T14:20:00Z | third-way-game | green | green | pass d pre-build review: 4/4 patch items verified pure additions against stub bytes (vm_ledger, vow_interest,... | OK 3329B | current |
| 628 | 2026-09-27T14:20:10Z | world-models-multi-agent | steal | steal | rehydration dry-run on live seat research (2,085-row trail, manifest ARMED-PENDING, runner_state last_run tod... | OK 4216B | re-burned later (latest line 662) |
| 629 | 2026-09-27T14:20:20Z | free-resource-landscape | steal | steal | Featherless catalog probed 4 calls keyless: nightly roster-diff CONFIRMED buildable via undocumented ?sort=-c... | OK 3703B | re-burned later (latest line 692) |
| 630 | 2026-09-27T14:50:00Z | adversarial-self-probes | free-text | vacuous | grammar extension BUILT then REVERTED by its own falsifier same pass: 7 of 19 blind rows gained (bar 10) and ... | OK 3540B | re-burned later (latest line 640) |
| 631 | 2026-09-27T14:50:10Z | stego-canon-pipeline | free-text | vacuous | sibling-routing lookup test: schema law is AHEAD OF ITS MACHINERY (fresh mode): the law row names siblings as... | OK 3194B | re-burned later (latest line 650) |
| 632 | 2026-09-27T14:50:20Z | middle-path-doctrine | steal | steal | C9 v2 consolidated after three sharpenings: four gates + Abolishing Steward + green-on-six-chairs + one open ... | OK 3437B | re-burned later (latest line 684) |
| 633 | 2026-09-27T15:25:00Z | adversarial-self-probes | steal | steal | pass g bare-path matcher binds the pass-f-named extensionless gap (githooks/pre-push, 8 rows): BARE_PATH_RE d... | OK 3424B | re-burned later (latest line 640) |
| 634 | 2026-09-27T15:25:10Z | stego-canon-pipeline | steal | steal | pass-f named fix executed: permadeath siblings enumerated (only attested form: permadeath collectives; collec... | OK 3407B | re-burned later (latest line 650) |
| 635 | 2026-09-27T15:25:20Z | middle-path-doctrine | steal | steal | decay gate proposed as C9 gate five (the Pratchett open edge sharpened): twin ledger censuses (seats of recor... | OK 3431B | re-burned later (latest line 684) |
| 636 | 2026-09-27T15:40:00Z | lean-fire | free-text | hold | lean fire HOLD: seat weekly/monthly meter exhausted (limit reset 2026-09-28T03:29:00Z), all 3 topic dispatche... | OK 562938B | current |
| 637 | 2026-09-27T21:15:00Z | doctrine-owed-chase | steal | steal | Porete attribution gap closed as provenance: bytes 0-30000 of TheMirrorsOfSimpleSouls title page name transla... | OK 3408B | re-burned later (latest line 693) |
| 638 | 2026-09-27T21:15:10Z | world-models-multi-agent | steal | steal | missing-field claim half-confirmed on byte re-check: runner_state.json seatless byte-exact and pack threads z... | OK 3816B | re-burned later (latest line 662) |
| 639 | 2026-09-27T21:15:20Z | free-resource-landscape | steal | steal | Lightning gap half-closed via SDK-registry angle: PyPI lightning-sdk 2026.9.18.post1 (HTTP 200) pins the full... | OK 3504B | re-burned later (latest line 692) |
| 640 | 2026-09-27T21:45:00Z | adversarial-self-probes | green | green | first real catch hunt drew clean at 40 rows (20 checks 0 warns), and the adversarial value came from re-verif... | OK 3844B | current |
| 641 | 2026-09-27T21:45:10Z | stego-canon-pipeline | steal | steal | sense-routing third leg probed: the routing law exact-name-first leg is SENSE-BLIND at lookup (sense gate onl... | OK 3554B | re-burned later (latest line 650) |
| 642 | 2026-09-27T21:45:20Z | middle-path-doctrine | steal | steal | decay gate ruled STATABLE against the doctrine own machinery: twin census cheap on existing jsonl patrol+viso... | OK 3877B | re-burned later (latest line 684) |
| 643 | 2026-09-27T23:20:00Z | world-models-multi-agent | steal | steal | two diffs sized byte-exact: setdefault seat-lane as first body line of _save_state (mag/lane_runner.py:109, t... | OK 3851B | re-burned later (latest line 662) |
| 644 | 2026-09-27T23:20:10Z | free-resource-landscape | steal | steal | TIME-class window check: DeepSeek alive (401 governor not refused) and UTC 23 Sunday in-window under both the... | OK 3267B | re-burned later (latest line 692) |
| 645 | 2026-09-27T23:20:20Z | stego-canon-pipeline | steal | steal | both pass-h named fixes executed: permadeath homonym_note citation corrected to byte-true GAMEDIG_roguelike-r... | OK 3321B | re-burned later (latest line 650) |
| 646 | 2026-09-27T23:50:00Z | doctrine-owed-chase | steal | steal | Sefer Raziel chase byte-closed both archive.org candidates as identity mismatches (sefer-raziel = 2024 amateu... | OK 3444B | re-burned later (latest line 693) |
| 647 | 2026-09-27T23:50:10Z | middle-path-doctrine | steal | steal | death-arm denial lever CONFIRMED then closed: manufactured ungated share trips the gate and the faction then ... | OK 3403B | re-burned later (latest line 684) |
| 648 | 2026-09-27T23:50:20Z | free-resource-landscape | steal | steal | LLM7 turbo census: new top-level tier field (5 turbo / 59 pro), free-class DRIFTED 5 to 4 same-day (DeepSeek-... | OK 2715B | re-burned later (latest line 692) |
| 649 | 2026-09-28T00:00:00Z | world-models-multi-agent | free-text | built | both pass-f one-liners landed byte-exact (lane_runner.py:110 setdefault seat-lane; context_pack.py:549 seat p... | OK 3558B | re-burned later (latest line 662) |
| 650 | 2026-09-28T00:00:10Z | stego-canon-pipeline | green | green | first end-to-end routing drill green: exact-name, siblings, and sense-tag legs all fire as written against th... | OK 2719B | current |
| 651 | 2026-09-28T00:00:20Z | middle-path-doctrine | steal | steal | C9 bloat audit: five gates and two arms collapse to THREE gates (worthiness, Vow, inefficiency) plus the endg... | OK 3511B | re-burned later (latest line 684) |
| 652 | 2026-09-28T00:20:00Z | doctrine-owed-chase | steal | steal | Sefer Raziel HebrewBooks pass: candidate id 49094 byte-closed as wrong book (Chazon Yechezkel Abramsky, 27,68... | OK 3369B | re-burned later (latest line 693) |
| 653 | 2026-09-28T00:20:10Z | world-models-multi-agent | steal | steal | reader surface NAMED: the pack bonds field (context_pack.py:865, rows rendered bonds.py:438-453 with seat lab... | OK 3863B | re-burned later (latest line 662) |
| 654 | 2026-09-28T00:20:20Z | middle-path-doctrine | steal | steal | C9 v3 restated in full from the collapse (three gates, F7 endgame clause, one post-abolition death arm with t... | OK 3347B | re-burned later (latest line 684) |
| 655 | 2026-09-28T00:45:00Z | free-resource-landscape | steal | steal | two owed items landed: the world-models trace Agora-2 tech-report one-liner closed (HEAD 200 application/pdf ... | OK 3230B | re-burned later (latest line 692) |
| 656 | 2026-09-28T00:45:10Z | world-models-multi-agent | free-text | built | owed bonds_meta emitter landed as one line (context_pack.py:628 related_by_seat seat counts over the same row... | OK 3535B | re-burned later (latest line 662) |
| 657 | 2026-09-28T00:45:20Z | middle-path-doctrine | steal | steal | weak-link depth-check flipped the worry: Vow pricing MISLABELED one-deep (four instruments: salon origin, rac... | OK 3893B | re-burned later (latest line 684) |
| 658 | 2026-09-28T00:55:00Z | free-resource-landscape | steal | steal | pro-tier self-ID probe: 4 of 4 keyless POSTs on the frontier-shaped ids returned 401 missing_api_key while th... | OK 3139B | re-burned later (latest line 692) |
| 659 | 2026-09-28T00:55:10Z | world-models-multi-agent | free-text | vacuous | precondition hunt vacuous-on-replay: zero seat=research rows exist AND normalize_seat (run_trail.py:73-77) co... | OK 3792B | re-burned later (latest line 662) |
| 660 | 2026-09-28T00:55:20Z | middle-path-doctrine | steal | steal | Taanit 7a bridge second derivation SUCCEEDED via a different route than expected: digest 1.8 Abulafia/Vital p... | OK 3049B | re-burned later (latest line 684) |
| 661 | 2026-09-28T01:20:00Z | free-resource-landscape | steal | steal | churn series interval 2: 4-to-4-to-4 same ids zero drift two intervals, keyless GLM-5.3-Flash probe 200 with ... | OK 2850B | re-burned later (latest line 692) |
| 662 | 2026-09-28T01:20:10Z | world-models-multi-agent | green | green | research seat fix landed (_SEAT_MAP += research:research in run_trail.py:61, PARSE_OK, normalize_seat researc... | OK 3772B | current |
| 663 | 2026-09-28T01:20:20Z | middle-path-doctrine | steal | steal | digest survivorship audited: C9 1.7, X6 (9 carriers), and Kook dissolution multi-carrier (survive digest loss... | OK 3310B | re-burned later (latest line 684) |
| 664 | 2026-09-28T01:45:00Z | doctrine-owed-chase | steal | steal | Sefer Raziel id-pin pass: the citing encyclopedia.com source 500-closed on both transports, search-surfaced i... | OK 3806B | re-burned later (latest line 693) |
| 665 | 2026-09-28T01:45:10Z | free-resource-landscape | steal | steal | LLM7 cap table COMPLETE: enforced codestral-latest 5/5 and mistral-Nemo 5/5, violated minimax-m2.7 and GLM-5.... | OK 3493B | re-burned later (latest line 692) |
| 666 | 2026-09-28T01:45:20Z | middle-path-doctrine | steal | steal | founding-sentence restatement carrier MINTED outside the verbatim chain (FOUNDING_SENTENCE_RESTATEMENT_202609... | OK 3631B | re-burned later (latest line 684) |
| 667 | 2026-09-28T02:20:00Z | doctrine-owed-chase | steal | steal | archive.org route byte-closed empty: both Sefer-Raziel-titled items are one uploader modern tables, wrong-boo... | OK 3581B | re-burned later (latest line 693) |
| 668 | 2026-09-28T02:20:10Z | free-resource-landscape | free-text | vacuous | DeepSeek in-window debt NOT fired: the boards in-window premise was STALE at execution (07:03:52Z vs 16:30-00... | OK 2987B | re-burned later (latest line 692) |
| 669 | 2026-09-28T02:20:20Z | middle-path-doctrine | steal | steal | X6 steward leg survivorship risk retired: verbatim quote-class held at 9 files (one directory class) and a se... | OK 724B | re-burned later (latest line 684) |
| 670 | 2026-09-28T08:35:00Z | doctrine-owed-chase | steal | steal | Zeramim mine closed with the p. 44b pin DOUBLE-ATTESTED: Arnow Zeramim Vol IV Issue 3 footnote 24 fetched byt... | OK 3356B | re-burned later (latest line 693) |
| 671 | 2026-09-28T08:35:10Z | free-resource-landscape | steal | steal | DeepSeek window contest CLOSED on the official pricing page: peak = 01:00-04:00 plus 06:00-10:00 UTC Mon-Fri ... | OK 3385B | re-burned later (latest line 692) |
| 672 | 2026-09-28T08:35:20Z | middle-path-doctrine | steal | steal | Abulafia/Vital 1.8 recipient-side gate restated as THIRD carrier (ABULAFIA_VITAL_DERIVATION_20260928.md, 124 ... | OK 966B | re-burned later (latest line 684) |
| 673 | 2026-09-28T09:30:00Z | doctrine-owed-chase | steal | steal | HebrewBooks viewer route spent 3 fetches, ids 51626/22234/23156 closed as wrong books with byte-quoted title ... | OK 2883B | re-burned later (latest line 693) |
| 674 | 2026-09-28T09:30:10Z | free-resource-landscape | steal | steal | LLM7 churn interval 4 zero-drift (4 free ids byte-stable, series 4/4/4/4, total 64 to 65 paid-only) plus Feat... | OK 3615B | re-burned later (latest line 692) |
| 675 | 2026-09-28T09:30:20Z | middle-path-doctrine | steal | steal | fourth restatement carrier minted (KOOK_INQUISITOR_DISSOLUTION_20260928.md, 125 words citing digest lines 250... | OK 902B | re-burned later (latest line 684) |
| 676 | 2026-09-28T10:20:00Z | doctrine-owed-chase | steal | steal | site-search pin did not land: both search URL shapes byte-identical IIS 404, id hint 42032 falsified as Talmu... | OK 3104B | re-burned later (latest line 693) |
| 677 | 2026-09-28T10:20:10Z | free-resource-landscape | steal | steal | DeepSeek off-peak hammer FIRED 10:04Z Monday in-window: authenticated GET /models HTTP 200 with 2 models (dee... | OK 3146B | re-burned later (latest line 692) |
| 678 | 2026-09-28T10:20:20Z | middle-path-doctrine | steal | steal | game-class clause RE-ARMS as F8 (pre-registered ractor-class falsifier on the MUD stub: first faction-war sea... | OK 3314B | re-burned later (latest line 684) |
| 679 | 2026-09-28T11:30:00Z | doctrine-owed-chase | steal | steal | beta-record locator route: both search URL shapes byte-identical IIS 404, id hint 42032 falsified on BOTH dom... | OK 3239B | re-burned later (latest line 693) |
| 680 | 2026-09-28T11:30:10Z | free-resource-landscape | steal | steal | DeepSeek off-peak inference-PROVEN 11:04Z Monday in-window: first real chat call HTTP 200, usage {36 cache-mi... | OK 3506B | re-burned later (latest line 692) |
| 681 | 2026-09-28T11:30:20Z | middle-path-doctrine | steal | steal | F8 instrumentation spec landed against mud.html bytes: the stub has NO factions, NO sentiment, NO VM pool, NO... | OK 2956B | re-burned later (latest line 684) |
| 682 | 2026-09-28T11:55:00Z | doctrine-owed-chase | steal | steal | Kol HaTor ch. 2 absence upgraded single-pull to DOUBLE-ATTESTED via Hebrew Wikisource print edition: mitzvah ... | OK 3672B | re-burned later (latest line 693) |
| 683 | 2026-09-28T11:55:10Z | free-resource-landscape | steal | steal | Featherless instrument-mismatch gap CLOSED: full dump 22,054 served rows byte-backed (grew plus 10 per day) v... | OK 2881B | re-burned later (latest line 692) |
| 684 | 2026-09-28T11:55:20Z | middle-path-doctrine | green | green | X6 window audit: 7 of 7 scenario cards cite byte-verified pre-existing fleet FAIL rows per AMD-1 (G1 the only... | OK 3808B | current |
| 685 | 2026-09-28T12:15:00Z | doctrine-owed-chase | steal | steal | Sefer Raziel scan id PINNED on fetch 1: HebrewBooks req 35004 (title line razial hamalach page 7 of 124, 9MB ... | OK 2626B | re-burned later (latest line 693) |
| 686 | 2026-09-28T12:15:10Z | free-resource-landscape | free-text | vacuous | Lightning credits chase closed VACUOUS: 8 keywords 0 hits across 6,566 byte-read description chars, no pricin... | OK 3928B | re-burned later (latest line 692) |
| 687 | 2026-09-28T12:35:00Z | doctrine-owed-chase | steal | steal | Sefer Raziel primary pull LANDED with a provenance CORRECTION: HebrewBooks req 35004 byte-confirmed as a name... | OK 3586B | re-burned later (latest line 693) |
| 688 | 2026-09-28T12:35:10Z | free-resource-landscape | free-text | vacuous | Lightning pass l executed per pre-registration: both official pricing URLs are client-rendered shells with pl... | OK 3084B | re-burned later (latest line 692) |
| 689 | 2026-09-28T12:55:00Z | doctrine-owed-chase | steal | steal | Amsterdam 1701 scan FOUND-NOT-PULLED and double-pinned: archive.org FD9301B81B1F46BBA655C5756A55D35D creator ... | OK 3172B | re-burned later (latest line 693) |
| 690 | 2026-09-28T12:55:10Z | free-resource-landscape | free-text | vacuous | Lightning pass m executed: newest Wayback capture of lightning.ai/pricing (20260921224149, 21,148 bytes) is t... | OK 2560B | re-burned later (latest line 692) |
| 691 | 2026-09-28T13:20:00Z | doctrine-owed-chase | steal | steal | Amsterdam imprint BYTE-BACKED via the archive.org JPEG originals (sha1-verified against metadata): req 23968 ... | OK 3908B | re-burned later (latest line 693) |
| 692 | 2026-09-28T13:20:10Z | free-resource-landscape | green | green | board consolidation GREEN-solved pending next churn event: four probes fired and absorbed by standing laws (L... | OK 3421B | current |
| 693 | 2026-09-28T13:45:00Z | doctrine-owed-chase | green | green | topic CLOSED green-pending-chronogram: archive item verified text-derivative-free (thumb-only), the 885,009-b... | OK 2968B | current |

- f-08, 2026-09-28. Source of every number: memory/burns/LEDGER.jsonl bytes read in full
  this session plus the os.path.isfile checks above. Nothing hand-copied.
