# HERMES GAP MAP 2026-10-07 - my measurements laid against the estate's own gap set

Written 2026-10-07 by the Hermes seat (contractor lane). Read-only pass. No source file, no chain leaf, no
`memory/biography/` entry and no gate was modified or executed. No em-dashes in this record.

## 0. Provenance: what I read, and which numbers I re-verified in this window

Surfaces read in full or in part:

- `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md` (247 lines, 17,628 B) - the 10-01 ranked register, 12 ranks,
  4 meta-gaps, one-sitting specs, one-wave queue, operator-gated queue, below-cut ledger.
- `watch/inbox/ESTATE_GAPS_20261004.json` (380 lines, 14,063 B) - 24 machine-readable gaps EG-01..EG-24 with
  `evidence_paths` and `search_terms`.
- `watch/inbox/ESTATE_GAP_DIG_20261004.md` (87 lines, 12,143 B) - the human half of the same dig.
- `logs/gap_sentinel/history.jsonl` (13 runs) and `logs/gap_sentinel/run.log`; `tools/gap_sentinel.py:60-82`.

Re-verified this window by byte count (grep -c / wc -l against the file on disk):

| claim | source I checked | count |
|---|---|---|
| `reaper-enumerate-error` | `logs/supervisor.jsonl` (grep) | 97,565 lines |
| top masking signature `run_shell:c73866f2f1b5` | `logs/failure_kb.jsonl` (grep) | 25,285 lines |
| second masking signature `run_python:2e689948ccfa` | `logs/failure_kb.jsonl` (grep) | 12,424 lines |
| em-dashes in the harness file | `AGENTS.md` (grep -c) | 17 |
| whitelisted scheduled tasks | `configs/sanctioned_scheduled_tasks.yaml` (grep) | 13 |
| chain rows | `memory/biography/verkle_chain.jsonl` (wc -l) | 11,621 |
| knot files | `memory/biography/knots/*.knot.json` (ls + grep) | 28,960 |
| gap sentinel detectors | `tools/gap_sentinel.py:70-72` `SENSORS` tuple | 1 sensor |
| EG-20 closer | `tools/gps_mcp/coverage.py` | EXISTS, 13,300 B, mtime 2026-10-05 04:17 |

Adopted as CLAIM, not verified by me: every figure in the register and dig that I did not personally count,
including the 1.4 percent re-read rate (EG-11), the 4,860 VS Code prompts and 47 Grok interactive sessions (EG-01,
EG-24, EG-17), the 412-of-412 cage child failures (EG-19), the 40 percent dwf fail share (EG-02), the
`tools/social_rsi.py:578` ratchet NEW line (EG-15), and the 177h `fossil_check` WARN on `SEATS.md` (EG-23).
Number-pair note: my grep counts run slightly above the deterministic parse counts taken earlier in this audit
(97,555 parsed events vs 97,565 grep lines; 25,102 vs 25,285; 12,285 vs 12,424). Grep matches the signature string
anywhere in a row, the parser counts `kind` fields. Both are true; the parsed figure is the stricter one. The chain
and knot counts also moved inside the audit window (11,620 to 11,621 rows, 28,957 to 28,960 knots): the janitor is
live and these are snapshots, not constants.

## 1. My understanding, in three layers, because the mapping needs a frame

I read this estate as three layers that all write to disk:

- **Body**: 1,085 `mag/*.py`, 331 `tools/*.py`, 575 tests, 750 docs, 173 CLI verbs, 23 live Mag/Estate scheduled
  tasks against a whitelist of 13.
- **Governance**: 56 ribs, 51 rib_bus domains, 30 skills, and a pre-push hook of 551 lines holding 16 gate blocks
  of which 7 enforce.
- **Record**: the chain (11,621 rows), the knot body (28,960 files), and the four behavioral ledgers
  (`behavioral_events` 216,799 lines, `usage` 164,499, `provider_usage` 77,732, `failure_kb` 114,554,
  `supervisor` 114,918). Plus the derived surfaces: `INDEX.json` (12,055 events, 3,480 active, 179 fold_warnings).

The gap set covers the first two layers well. Section 5 is what it does with the third.

## 2. Mapping: their gap, my evidence, verdict

| their gap | what my audit measured that bears on it | verdict |
|---|---|---|
| EG-01 boot cards cover ZCode only | My THEN/NOW diff confirms the boot chain now names `zknot/LATEST.md` plus newest authored `state/*.md`; the VS Code corpus sits outside the repo in `chatSessions`. Stronger: the 08-26 mining digested 18 of those sessions and `watch/SELF_STEAL_VSCODE_DEEPSEEK_CORPUS_20260904.md` records them GONE from disk by 09-04 | CONFIRMED and ESCALATED: part of the uncarded corpus is already destroyed, so this is not only an indexing gap |
| EG-07 no landed field, cost per outcome unknowable | `usage.jsonl` schema is `ts/lane/action/ok/detail/meta` with no outcome key; it carries `ok` (159,537 True / 4,953 False) and tokens in `meta`. 77,705 of 164,499 rows are `provider_chat` | CONFIRMED at bytes, and the missing key is nameable: there is no `landed` field, only `ok` |
| EG-10 event log past 10,180 lines, no compaction | `INDEX.json` recorded `event_count` 12,055, `active_items` 3,480, `fold_warnings` 179, derived 2026-10-07T12:10:52Z | CONFIRMED and measured forward: 12,055 now, and the 179 fold_warnings are the fold admitting missed writer events |
| EG-11 corpus fold never run, 1.4 percent re-read | Wave findings still live only inside `watch/inbox/`; `memory/research_polished` newest is their dated 09-25 | CONFIRMED in shape; the 1.4 percent is their number (CLAIM to me) |
| EG-12 red patrols, LaneSupervisor last 09-28 | `logs/gap_sentinel/history.jsonl` is 13 runs, 11 of them exit 1, findings `rollup-growth` and `sensor-silence dashboard/static/x_radar.json`. The 10-07T12:15 run exited 1, filed nothing, recorded no snapshot | CONFIRMED live, and the sentinel's own record shows it has been red continuously and consumed never |
| EG-16 zknot refreshes at logon only | The boot order in `AGENTS.md:5` reads `zknot/LATEST.md` as the intent recap; the dig's 13h-stale finding stands against a boot doc that is load-first | CORROBORATED (their staleness figure is CLAIM) |
| EG-15 ratchet red tree-wide | Not verified by me. Adjacent measurable: `freshness_check` FAILs because it gates commit age, so content cannot cure it, only the commit | UNVERIFIED by me, one adjacent measurement offered |
| EG-19 cage children blocked, briefs stopped 09-28 20:14 ET | Their figures (412 of 412, 3,891 September briefs) | CLAIM, unverified |
| EG-09 seal gates unarmed | Their finding, first seen at GAP_REGISTER rank 5 | CLAIM, unverified |
| EG-23 SEATS.md stale, no compiler | Adjacent trap my rib survey hit: several ribs share mtime 2026-10-05 22:17 from a batch rewrite, so mtime is not authorship date, and a freshness meter reading mtime will read the rewrite, not the mint | ADJACENT, supports the point that this class of meter measures the wrong thing |
| GAP_REGISTER meta-gap 1 MINED-NEVER-SCHEDULED | All three gap surfaces are themselves unconsumed: the register is 6 days old, the dig's digest half is stale against its own JSON (section 4), and the sentinel files into `memory/attention.md` on a channel nobody greps | CONFIRMED, and it applies to the instruments, not only to the findings |
| GAP_REGISTER meta-gap 3 PHANTOM-CITATION | `tools/citation_lint.py` now exists and enforces at pre-push; the register's own ranks 3 and 4 are marked FILLED with byte-checked receipts | PARTIALLY FILLED as its own annotations state; I did not re-run the tool |

## 3. Gaps my audit found that NO gap surface carries

Ranked by the register's own law (severity x fill-ease, cheapest cure first inside a band). `SEV` uses the
register's scale: S1 critical, S2 high, S3 medium, S4 low.

| id | gap | sev | fill cost | evidence |
|---|---|---|---|---|
| GN-1 | **The three behavioral ledgers are named in zero gap surfaces.** `grep -l failure_kb` and `grep -l supervisor` and `grep -l behavioral_events` over the register and both dig files return nothing. 446,271 rows of recorded behaviour sit outside the gap set entirely | S2 | ONE-SITTING to open (add the three ledgers to the sentinel's watched set) | grep over the three files, this window |
| GN-2 | `reaper-enumerate-error` is 97,565 grep lines out of 114,918 supervisor rows, about 85 percent. The estate's process guardian reports its own enumeration failure on nearly every row it writes | S2, S1 if the reaper owns the alarm path, which I did not verify | ONE-SITTING to diagnose (one call site) | `logs/supervisor.jsonl` grep 97,565; parsed-event count 97,555 |
| GN-3 | `failure_kb` holds 114,554 rows over 7,332 signatures, and its top two are error-masking bugs: `run_shell:c73866f2f1b5` 25,102 rows spanning 08-06 to 09-29 (84 days) and `run_python:2e689948ccfa` 12,285 spanning 08-05 to 09-26, together 37,387 rows. Nothing in the gap set names either one | S2 | ONE-SITTING to triage the top two signatures | `logs/failure_kb.jsonl` parse plus grep 25,285 / 12,424 |
| GN-4 | The chain indexes about 40 percent of its own knot population: 11,621 rows against 28,960 knot files. Also `dominant_theme` is null on 55.1 percent of rows, `amended=true` on 26.6 percent, `dossier_commit` present on 54.6 percent | S3 | JUDGMENT sitting, not a build | chain parse at 11,620 rows / 8,267,293 B, knots 28,957 |
| GN-5 | The mesh cursor is null by two key names: `tools/mesh_delta.py:114-115` reads `index` and `generated`; `memory/biography/verkle_tip.json` carries `n_leaves` and `updated_minute`. The live seed on 127.0.0.1:8767 answers `/picture` with `chain_tip_index: null` | S3 | ONE-SITTING, two key names | measured earlier in this audit chain, not re-run in this window |
| GN-6 | A disputed date rides in consumed records: the VS Code seat is "retired 08-26 with honors" in `watch/DFHACK_DRIVE_SELF_STEAL_20260906.md` and "retired 09-04" in `watch/ORPHAN_SWEEP_20260909.md`. Two cards, two dates, no adjudication | S3 | ONE-SITTING | both files, read this audit |
| GN-7 | The harness file violates the estate's own em-dash law: `AGENTS.md` carries 17 em-dashes (grep -c) while `AGENTS.md:118` states that the workflow gate enforces the no-fabrication and em-dash laws inside asks, and `tools/citation_lint.py` already exists to check prose records | S3 | ONE-SITTING (one pass over one file) | `grep -c` = 17 |
| GN-8 | Amendment landed in one surface only: `ESTATE_GAPS_20261004.json` marks EG-20 `status: closed` with `closed_by: tools/gps_mcp/coverage.py` (which EXISTS, 13,300 B, mtime 10-05 04:17), while `ESTATE_GAP_DIG_20261004.md:63` still lists EG-20 as a new open gap and line 79 still specs it as enhancement 9 | S3 | ONE-SITTING (amend the digest) | byte checks above |
| GN-9 | A three-week hole in a behavioral record: `memory/improve/daily/` behavioral leaves stop after 08-09 and resume 08-30 | S4 | ONE-SITTING to name it as known-missing | reader digest, this audit |

## 4. Contradictions and impossible checks, named plainly

1. **EG-20 is closed in the JSON and open in the digest.** Not a phantom: the closer exists on disk and is dated
   10-05, one day after the dig. The human half was never amended. This is the register's own meta-gap 1 in
   miniature, and it is the reason a seat reading only the digest will re-spec work that is already done.
2. **Two count conventions collide in the register itself.** The register reports its fills as byte-checked on
   2026-10-04 by `queue-truth-a14`, which means the register's fill annotations are three days newer than its own
   header date (10-01). Its header says "written 2026-10-01"; its ranks 2, 3, 4, 6, 7 carry fill receipts dated
   10-01 and 10-02. Any seat dating gaps by the register's header will misdate five fills.
3. **The whitelist drift is real but my count is inflated.** `configs/sanctioned_scheduled_tasks.yaml` carries 13
   task rows. A raw `schtasks` CSV substring count gives 34, which is inflated because the CSV repeats each task
   name across columns; the audit's named-task figure is 23. So the defensible statement is: 13 whitelisted against
   23 named Mag/Estate tasks, at least 10 unwhitelisted, and my 34 is a grep artifact I am not standing behind.
4. **The gap sentinel watches one sensor.** `tools/gap_sentinel.py:70-72` defines `SENSORS` as
   `("dashboard/static/x_radar.json",)`. The register and the dig both describe the sentinel as a general gap
   watcher. At bytes it is one sensor plus a rollup growth check, and it has been exit 1 for 11 of 13 runs. A
   general watcher with one watched file is itself a gap, and it belongs in the register.
5. **I cannot verify any gate's live pass or fail.** No gate was executed in this pass, by the read-only law. Every
   gate statement above is read from source or from the register, never from a run.

## 5. The coverage hole, stated once

Of the four behavioural ledgers, `grep -l` over all three gap surfaces returns zero files for `failure_kb`, zero
for `supervisor` and zero for `behavioral_events`. `verkle` appears only in the dig, and only as boot context
("chain tip #11253", digest line 7), never as a gap. The gap set maps the estate's shelves, tools, documents,
promises and patrols. It does not map the estate's own behaviour log, which is the largest record it keeps.

That is the single sentence this report exists to deliver: **the estate has instruments for everything it owns
except the record of what it has done.**

## 6. What I could not verify

- Every gate's current pass or fail state (no gate run).
- The register's fill claims (ranks 2, 3, 4, 6, 7): I read the annotations, I did not re-run the receipts.
- EG-15 (ratchet NEW line), EG-19 (cage children), EG-23 (fossil WARN), EG-09 (seal keyfile absence): adopted as
  CLAIM.
- Whether the reaper error is merely noisy or actively corrupting restart accounting. The count is measured; the
  consequence is not.
- Why the chain indexes 40 percent of the knots: the ratio is measured, the cause is not.

RECEIPT: read-only pass, zero writes except this card; no gate executed, no chain leaf touched, no
`memory/biography/` entry modified. VERIFIED this window: the nine byte checks in section 0 (reaper 97,565,
c73866f2f1b5 25,285, 2e689948ccfa 12,424, AGENTS.md em-dashes 17, whitelist 13, chain 11,621, knots 28,960,
`SENSORS` = 1 sensor, `tools/gps_mcp/coverage.py` exists), the sentinel's 13-run history and 11 exit-1 runs, the
three zero-hit greps in section 5, and the EG-20 status split between the JSON and the digest.
UNVERIFIED: all register and dig figures not listed as counted, all gate verdicts, and GN-5 which was measured
earlier in this audit chain and not re-run here.
