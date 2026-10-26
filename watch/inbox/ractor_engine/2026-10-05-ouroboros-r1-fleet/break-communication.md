# break-communication: hostile second pass on communication.md (OUROBOROS R1, fleet)

Seat: break-communication subagent, 2026-10-05. Instrument: direct file reads,
grep/findstr, venv python censuses (`./.venv/Scripts/python.exe`, one-liners, no
child subprocesses spawned), schtasks //Query //FO CSV (343 CSV rows = 342 tasks
+ header, matching the lens's 342), ListWorkflowRuns attempt from this seat.
Nothing edited outside this file. The ask's finding 4 arrived TRUNCATED
mid-evidence (JSON cut in the ask payload); verdict below covers the visible
evidence and names the truncation.

## F1: fold relays verification as a key-name census; excluded: 0 while unconfirmed ride included

VERDICT: CONFIRMED (one scoping correction).

Byte checks, all run this sitting:
- tools/mickey17_v2_fold.py:157-160: `for k, v in c.items(): if
  isinstance(v, list): vc[k] += len(v)` is list-length sums per key name.
  `grep -n deep_tier2 tools/mickey17_v2_fold.py` returns rc=1 (zero
  occurrences).
- Exclusion wiring tools/mickey17_v2_fold.py:179-193: reads top-level
  `c.get("unconfirmed")`, collects `norm(x.get("claim",""))[:80]` from dict
  entries, matches rows by `norm(r.get("claim"))[:80]` at :190. Persisted shape
  is `{evidence, row_key, verdict}` (verified: r04-estate-index-anatomy
  .checks.json deep_tier2[1] keys exactly those three) and ZERO of 12 (read-
  estate) / 15 (run-0) / 8 (2026-10-05-exec) checks files carry a top-level
  `unconfirmed` key (censused per file this sitting).
- FOLD_SECTIONS quotes byte-exact: runs/run-0/FOLD_SECTIONS.md:27 `verdicts:
  checks 15, deep_tier2 16, rows 10, supports 50`; runs/2026-10-04-0/
  FOLD_SECTIONS.md:27 `verdicts: checks 10, deep_tier2 12, entries 5, supports
  45` and :40 `excluded: 0`.
- True counts recomputed from persisted bytes (my instrument, sums over
  `counts.yes/no` and `deep_tier2[].verdict`): 2026-10-04-0 (read-the-estate)
  = 12 yes / 48 no, 7 verified / 5 unconfirmed; run-0 = 12 yes / 63 no,
  15 verified / 1 unconfirmed. Both match the prose masters byte-for-byte
  (corpus/steal/MASTER_READ_ESTATE.md:8-9 "12 yes / 48 no", "7 verified / 5
  unconfirmed"; corpus/steal/MASTER_MICKEY17_V2.md:54 "75 tier-1 supports =
  12 yes / 63 no" plus "16 deep_tier2 verdicts = 15 verified / 1
  unconfirmed").
- Falsifier executed by the run itself: the read-estate FOLD_SECTIONS.md (the
  fold's own output over that archive) prints `excluded: 0` while the archive
  persists 5 `unconfirmed` verdict values. I did not re-run the fold (it writes
  its fixed output path; the run artifact already is the execution).
- Scoping correction (does not weaken the finding): "the true counts exist only
  in the prose masters" is slightly overdrawn. They are also derivable from the
  persisted `counts` keys and `deep_tier2[].verdict` values (I derived them
  above). The accurate statement: no SCRIPTED surface computes them;
  FOLD_SECTIONS.md is the surface that mis-states them, and it is the one the
  fold header calls "computed by this script" (FOLD_SECTIONS.md:3).
- Note for the fix: tier-1 `checks` entries carry NO verdict field in these
  runs (key shapes censused: `{claim,quote,reason,row,supports}` etc.; the
  yes/no lives in `counts` and in per-entry `supports`). The amendment must
  read two vocabularies: tier-1 from `counts`/`supports`, tier-2 from
  `verdict`. Still one sitting.
- Ownership respected: state/NIGHT_LOOP_20261005.md:33-38 lists
  mickey17_v2_fold.py under executor dwfrun-e9656e14, so the lens's OWED filing
  is correct; this pass touched nothing.

## F2: boot relay surfaces (INDEX.json, state/CURRENT.md) ~20h stale while the seal log is minute-fresh

VERDICT: CONFIRMED.

- watch/inbox/INDEX.json derivations block read byte-exact: derived_at
  2026-10-04T12:09:10.239Z, event_count 10186. Live log now 10,684 lines (wc
  -l; the lens read 10,650; the tree moved +34 under both of us, gap now 498).
- Needles this sitting: INDEX.json hits = 0 for MASTER_READ_ESTATE, for
  READ_ESTATE_RUN_SPEC_ADDENDUM, for NIGHT_SHIFT_20261005, for ouroboros-in-
  new-context, and strongest: `grep -c "2026-10-05" INDEX.json` = 0. Nothing
  dated today exists in the boot surface at all, vs log hits 2 / 2 / 6 / 197 /
  183.
- Log tail is minute-fresh: last line ts 2026-10-05T08:50:52Z, an autoseal of
  this round's own break-operations.md (sibling pass banking in real time).
- state/CURRENT.md:8 `updated: 2026-10-04T09:30:00Z`, :105 Last result =
  NIGHT_SHIFT_20261004_CLOSE.md. Both byte-verified.
- Scheduled-task census re-run: `schtasks //Query //FO CSV` = 343 rows (342
  tasks + header, matches the lens count). Keyword filter over all names:
  Estate Spine Index and MagFtsIndexDaily exist; NO task matches inbox, fold,
  or refold (nothing like MagInboxIndexDaily).
- scripts/index_fold_host.mjs exists (40,108 bytes, mtime Sep 30 08:11); no
  registration script beside it (scripts/register_fts_index_task.ps1 pattern
  has no index_fold sibling).
- Blind-spot probes do not rescue the surface: INDEX.json fold_warnings = 168
  entries, ALL writer nonce gaps, zero staleness signal; memory/attention.md
  head shows session records and provider alarms, no INDEX staleness alert.
- SHARPENING the lens missed (see Additions A1): the 12:09:10Z derivation is
  itself proof a manual cure already fired once and decayed again. run-0's a13
  census read "747 events stale" (MASTER_MICKEY17_V2.md:206, :221 GO item 5);
  someone hand-ran the refold at 2026-10-04T12:09:10Z (event_count 10186);
  the surface then froze and is 498 behind again. Drift sequence on the
  estate's own bytes: 521 -> 747 -> cured once by hand -> 498. A one-time
  manual refold is proven insufficient by the estate's own history; the
  schtasks move is the only shape the bytes support.

## F3: review decision and input contract ({topic,targets,width}) live only in the ephemeral report

VERDICT: CONFIRMED on the core; WEAKENED on the fired-decoding detail.

- Line cites exact: .zcode/workflows/mickey17-v2.dwf.ts:336
  (`if (review.decision === "REVISE")`), :367 and :374 (review.decision into
  ephemeral conclusion/verified lines only).
  .zcode/workflow-drafts/execute-register.dwf.ts:319/:345/:352 same pattern;
  its improved report contract verified at :339-352 (filters `verdict !==
  "verified" && verdict !== "same-chain-verified"`, returns unconfirmed rows
  as findings), third-generation copy confirmed.
- Universal re-censused harsher than the lens's instrument (quantifier law):
  the lens used os.walk filename filters for manifest/review. I walked all 278
  files under memory/runs/mickey17_v2 checking BOTH filenames AND contents
  (regex ACCEPT|REVISE; "targets" with "topic"). Result: zero files named
  manifest*/review*; 5 content hits, all lane-row prose about other subjects
  (e.g. a08-48h-synth.checks.json mentions a "CHECK 7 REVISE correction" in
  mined text; a13-cadence.json matches generic "targets" in row schema). The
  universal SURVIVES the stronger census.
- gauntlet_w4/verdict.json exists under runs/ but is a 2026-09-01 gauntlet
  falsifier verdict (filed 2026-09-25, schema falsifier.verdict.v1), NOT a
  mickey17_v2 review decision, so it does not break the universal, but see A3.
- KILLED SUB-CLAIM: "read-the-estate's 'fired: 12' decoded as
  String(TARGETS.length)=0, self-referential". False on the bytes:
  read-the-estate.dwf.ts:101 WIDTH defaults to 12, ALL is a STATIC 12-entry
  list (r01-r12, verified by reading the array), TARGETS = ALL.slice(0,WIDTH)
  = 12, so the fold receives the true count 12. And mickey17-v2.dwf.ts:107-109
  THROWS "no targets passed" on an empty list, so a 0 can never reach the fold
  through either engine. fired:12 == n_files:12 is coincidence (12 static
  targets, 12 landed files), not evidence of vacuity. The E22 circularity
  clause should be struck from this finding; the manifest/review core stands
  without it. What the lens probably conflated: the RUNSLUG dir-name suffix
  (A2 below) does encode args.targets length 0. The 0 lives in the directory
  name, not in --fired.

## F4 (truncated in the ask): registry G6 soft-fails + double-registration

VERDICT: evidence CONFIRMED as far as it arrived; the finding's own statement
and move were cut off mid-JSON in the ask payload, so no verdict on the
unstated claim.

- memory/workflows/REGISTRY.jsonl (88 rows total): row 85 ts
  2026-10-04T21:15:36Z script .zcode/workflow-drafts/read-the-estate.dwf.ts,
  row 86 ts 2026-10-05T04:39:04Z script execute-register.dwf.ts, both carry
  G6-receipts ok:false soft:true "receipt mention lacks a dated stamp (label +
  YYYY-MM-DD, t62 prefilter family)". Byte-exact vs the lens.
- Rows 59-60: ts 2026-10-02T16:13:42Z / :43Z (one second apart), SAME digest
  90b1990da9ae, scripts `C:/Users/foste/.../.zcode/...` (absolute) vs
  `.zcode/workflows/ractor-engine.dwf.ts` (relative), a double registration
  of one gate run under two path spellings. Byte-exact vs the lens fragment.
- See A5: the dedup-key defect and its ownership constraint
  (workflow_gate.py is executor-owned per NIGHT_LOOP:36).

## What the lens missed (additions)

- A1 (sharpens F2, ~0 min, evidence only): the refold WAS manually cured once
  (derived_at 2026-10-04T12:09:10.239Z, event_count 10186) after run-0's a13
  flagged 747-stale (MASTER_MICKEY17_V2.md:206 GO table, :221 GO item 5), and
  the surface decayed to 498-behind again. The defect is not "nobody ran it";
  it is "running it by hand provably rots within a day". Cite in the amendment
  table row for the schtasks fix.
- A2 (corrects + strengthens F3, ~5 min): the run-dir name is a manifest
  fingerprint that already persists the WRONG number: read-the-estate.dwf.ts:87
  builds RUNSLUG as topic + "-" + String(args.targets?.length || 0), producing
  "2026-10-04-0" and "run-0" on disk while 12/15 STATIC targets actually
  fired. The F3 fix should write RUN_MANIFEST.json at this existing site
  (RUNSLUG construction, before the lane sweep) rather than inventing a new
  location, and stop encoding args-targets-length into the slug.
- A3 (census hazard, ~5 min): runs/gauntlet_w4/ holds verdict.json, a foreign
  falsifier artifact (2026-09-01 wave) inside the mickey17_v2 run archive. Any
  census over runs/* silently mixes non-engine content; the fold's load_lanes
  ignores it (no lanes/ dir), but every "all runs" claim (including F3's) must
  scope to runs with lanes/ or name the exception.
- A4 (CONVERGENT with F1 from the engine side, ~5 min inside F1's fix):
  mickey17-v2.dwf.ts:373 verified[] bullet asserts, in substance, that tier-2
  verdicts are appended to <id>.checks.json as deep_tier2 arrays and that the
  fold recount counting every list-valued key means they exist for the
  recount. The workflow's own self-description encodes the key-name-census
  belief. Fixing only the fold leaves the engine asserting a false contract;
  the amendment must touch both the fold and this bullet
  (execute-register.dwf.ts:349 carries the same wording minus the claim).
- A5 (new defect, owed not editable, ~10 min): REGISTRY rows 59-60 show the
  gate double-registers one run when the script path spelling differs
  (absolute vs relative, same digest one second apart); the registry dedup
  does not normalize paths, so registry-based censuses (the ouroboros rounds
  themselves) can double-count. Fix belongs in workflow_gate.py's row
  identity, which is EXECUTOR-OWNED (state/NIGHT_LOOP_20261005.md:36): file
  owed with dwfrun-e9656e14, do not edit from this round.
- A6 (inside F1's fix, ~2 min): the PRISMA invariant line
  (tools/mickey17_v2_fold.py:200-202, "identified == included + excluded
  HOLDS") is tautological: excluded and included are computed in the same
  partitioning loop over all_rows, so the assert can never fire. It is a gate
  that cannot fail, the estate's own assurance-theater class. Any F1 fix that
  leaves this line in place launders the same defect with a green checkmark;
  delete it or re-base it on an independently derived total.

## Not run / OWED (honesty ledger)

- Live run board: ListWorkflowRuns from this seat returns
  workflow_introspection_unavailable, so the lens's blind spot REPRODUCED
  exactly; dwfrun-e9656e14 live progress and token spend remain OWED.
- The underlying re-measurements behind the 5 unconfirmed corrections (910 vs
  917, 28 vs 30, 250 vs 160, 86.0 vs 89.4) were NOT re-verified (trust-lens
  territory; same boundary the lens drew).
- I did not execute the fold script (its output path is the run's own
  FOLD_SECTIONS.md; the archived artifact already is the execution the
  falsifier names).
- run-0 GO item 5 provenance verified upstream (MASTER_MICKEY17_V2.md:221);
  the a13#0 747-stale row is the lens's cite, confirmed at :206.
