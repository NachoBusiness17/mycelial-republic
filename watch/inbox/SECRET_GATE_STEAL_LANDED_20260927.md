# SECRET GATE STEAL LANDED 2026-09-27: five industry amendments, parity-proven

Class: RECEIPT · Writer: zcode seat · Operator order: "grind it out" · Executes
card watch/inbox/SECRET_GATE_INDUSTRY_STEAL_20260927.md against the live gate
(tools/secret_gate.py, pre-push gate 10).

## Verdict

All five amendments LANDED and proven. The prefilter is parity-IDENTICAL on a
real corpus (1,860 rule hits + 40,253 entropy findings, byte-equal counts on
vs off, 20 percent faster at 96.3s vs 120.0s on the watch/inbox+tools scope).
One real bug was caught by the parity gate itself before it could ship: the
first fast-pass charset dropped the hyphen (kebab-case tokens like
BURN_judge-lane-spec are legal entropy hits) and missed one finding plus a
fleet of entropy rows; fixed by including "-" and the eyJ literal, then
re-proven identical. The parity gate is the reason this landed clean.

## Evidence

1. gitleaks:allow inline marker (steal 1): synthetic sk-ant fixture with the
   marker on the same line scans clean (exit 0); without it, blocks (exit 1).
2. Path-scoped baseline (steal 2): configs/secret_gate_baseline.json migrated
   to {"paths":[...]} shape, CDX digest acceptance now keyed by rule+path
   regex with by+reason (loader REJECTS reasonless entries, exit 2);
   cdx_rar.json scans clean through the path entry.
3. Fast-pass prefilter (steal 3): PARITY IDENTICAL run (see Verdict); parity
   gate SG_NO_PREFILTER=1 stays in the tool as the standing A/B switch.
   First-pass DRIFT (GENERIC-KEYASSIGN 1 vs 2, entropy rows missed) is the
   receipt's own falsifier firing: charset fixed, second run identical.
4. --history mode (steal 4): landed, dedupes (rule, path, line fp) across
   git log -p --all, entropy skipped by design, path labels traversal-guarded
   (Mimosa catch honored: dropped ../-carrying and NUL paths), outputs the
   purge-target list. RUN IN PROGRESS at filing; results land in
   watch/inbox/secret_gate_results/history_*.json.
5. Push-protection UX (steal 5): blocking output now names the exact operator
   response (excise/rotate or accept by name, never loosen the hook).

Acceptance battery post-amendment: planted blocks exit 1; gitleaks:allow
suppresses exit 0; masked+clean exit 0; lan.key PRIVATE-KEY-BLOCK critical
exit 1 with the UX line; CDX path-accepted exit 0.

## Side landings from the same grind

- Fleet task doctor has a STANDING home: census_patrol_daily.ps1 now runs a
  Mag* task-health pass every morning (WARN-only, self-catching, Disabled
  tasks skipped), alerting memory/attention.md. Dry-run proof fired on live
  state and named: MagArmC200 dead (0xC000013A, console Ctrl-C when its
  headed window was closed; output file had only a 127-byte header),
  MagCorpusRescanDaily FAILED exit 1 on its first-ever fire (3:30 AM tonight,
  autopsy OWED), MagImproveDaily exit 1 (autopsy below).
- MagArmC200 relaunched headless (pythonw per tonight's conversion) and
  confirmed Running; the 200-leg lives again and can no longer be killed by
  closing a window it no longer has.
- MagImproveDaily autopsy: the 09-26 08:00 run COMPLETED its work (field
  brief, latest report, candidates all on disk, llm_used false local run)
  and exited 1 anyway; the exit contract lies. Root return-1 line in
  main.py's improve path OWED to a fresh lane.

## Owed

- history_*.json purge list lands when the background run finishes; feed it
  straight into the operator-gated filter-repo step.
- MagCorpusRescanDaily exit-1 autopsy (first fire failed).
- improve --once exit-contract root line.
- Ratchet: tools/secret_gate.py carries one NEW file-too-long debt (749
  lines) awaiting named acceptance or a split; not silently accepted here.

## Falsifier

Prefilter parity re-run must stay IDENTICAL after any future rule-table
change: a new rule without a derivable fast-pass condition breaks the
necessary-condition invariant and must either add a literal branch or set
NO_PREFILTER semantics aside for itself. The parity A/B run is the check.
