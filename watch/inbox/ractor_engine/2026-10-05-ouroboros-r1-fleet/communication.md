# COMMUNICATION LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

Relay audit of the standing fleet: what actually reached the operator versus what the
receipts claim was communicated. The relay chain I audited, end to end, this session:
lane/checks JSONs (content, alive) -> scripted FOLD_SECTIONS.md (census, blind) -> prose
master fold (content, hand-carried by a per-run seat) -> md-record-seal/autoseal into
watch/inbox/index_events.jsonl (minute-fresh) -> INDEX.json derivation (20h stale) ->
operator boot surfaces (state/CURRENT.md, 2 results behind). Every link but two is
healthy; the two dead links are where the operator actually reads.

## F1 (rank 1, CONVERGENT x3). The scripted fold relays verification as a KEY CENSUS; verdict CONTENT is computed by nothing in the script layer, and PRISMA prints "excluded: 0" while unconfirmed verdicts ride included

Evidence I checked this session: `tools/mickey17_v2_fold.py:157-160` counts list LENGTHS
per key name (`for k, v in c.items(): if isinstance(v, list): vc[k] += len(v)`) - byte
read this sitting; `deep_tier2` appears 0 times in the fold script while the runner
persists exactly that key; the exclusion wiring at `:181-190` reads a top-level
`unconfirmed` key and matches `claim[:80]`, shapes the persisted entries (`row_key`,
`verdict`, `evidence`) can never meet. Both archived folds read: run-0
`FOLD_SECTIONS.md` prints "verdicts: checks 15, deep_tier2 16, rows 10, supports 50";
read-the-estate prints "verdicts: checks 10, deep_tier2 12, entries 5, supports 45" and
"- excluded: 0" - while the true content (63 no / 12 yes tier-1, 15 verified / 1
unconfirmed in run-0; 48 no / 12 yes, 7 verified / 5 unconfirmed in read-estate, the 5
all carrying measured corrections: 910 not 917, 28 not 30, 250 not 160, 86.0 not 89.4)
exists only in the prose masters (`corpus/steal/MASTER_MICKEY17_V2.md` section 4
"carried reconciliation"; `MASTER_READ_ESTATE.md` "12 yes / 48 no" / "7 verified / 5
unconfirmed"). The fold actively mis-states the run's verification state to any reader
who trusts the script layer; one per-run prose seat is the single hand-carried link.
CONVERGENT: run-0 addendum E5+E20, read-estate addendum E5+E20 (5x re-bite), operations
lens F1 (gate byte-frozen). Falsifier: execute the fold over the read-estate archive
and observe any printed number respond to the 5 persisted unconfirmed verdicts - none
does (the read-estate run IS that execution; I did not re-execute the script, per the
addenda's own no-mutate discipline). Move (~35 min): the fold script walks every
list-valued key in the checks files, reads `verdict` VALUES (tier-1 yes/no; deep_tier2
verified/unconfirmed/crashed), prints the splits in the VERIFIER TABLE, and counts
unconfirmed/crashed into PRISMA excluded under codes 9/12. OWNERSHIP COLLISION:
`tools/mickey17_v2_fold.py` is owned by the in-flight executor dwfrun-e9656e14
(`state/NIGHT_LOOP_20261005.md:33-38`) - file this amendment OWED with that run id or
land after executor completion.

## F2 (rank 2, CONVERGENT with run-0 a13#0 / GO item 5). The operator's boot relay surfaces lag the fleet by ~20h while the seal layer is minute-fresh: receipts claim communication, the surfaces the operator reads at logon carry none of it

Evidence: `watch/inbox/INDEX.json` derivations block reads `derived_at:
2026-10-04T12:09:10.239Z, event_count: 10186` while the source log
`watch/inbox/index_events.jsonl` now holds 10,650 lines - 464 events unfolded. My
needle greps: INDEX.json carries 0 hits for MASTER_READ_ESTATE,
READ_ESTATE_RUN_SPEC_ADDENDUM, NIGHT_SHIFT_20261005, and the ouroboros lens dir; the
event log registers all of them, timestamped: MASTER_READ_ESTATE autoseal
2026-10-05T00:45:14Z, READ_ESTATE addendum 01:38:20Z, NIGHT_SHIFT_20261005_OPEN
07:59:33Z, tonight's lens files 08:04-08:10Z. `state/CURRENT.md:8` says updated
2026-10-04T09:30:00Z and its Last result names NIGHT_SHIFT_20261004_CLOSE.md - two
mega-burn results behind (read-the-estate folded 10-04 21:12 EDT; executor in flight).
No scheduler heals it: my schtasks census via python subprocess (CREATE_NO_WINDOW,
342 tasks) finds only Estate Spine Index and MagFtsIndexDaily - the inbox INDEX refold
(`scripts/index_fold_host.mjs`) is hand-run and its GO item (run-0 GO 5, "747 events
stale") never fired; the disease recurred at 5x scale. CURRENT.md additionally carries
a known overwrite hazard (its own Critique: mirrored by mag/agent_cli.py:2251).
Falsifier: if a watcher re-derived INDEX.json on append, derived_at would track the log
tail; it is 20h behind, checked this session (if such a watcher exists, it is broken,
which is the same finding). Move (~30 min): (a) register MagInboxIndexDaily (09:10,
absolute-path schtasks pattern per MagFtsIndexDaily) running scripts/index_fold_host.mjs;
(b) each night-loop round appends one Last-result line to state/CURRENT.md (bak-pattern
hand edit, agent_cli mirror respected).

## F3 (rank 3). The steering decision and the run's input contract die in the workflow report: zero review files, zero manifests, across every run the engine has ever archived

Evidence: `.zcode/workflows/mickey17-v2.dwf.ts:336` (`if (review.decision === "REVISE")`)
and `:367`/`:374` hold the ACCEPT/REVISE verdict in report lines only;
`.zcode/workflow-drafts/execute-register.dwf.ts:319-325,345,352` copies the same pattern
(third generation), while its report contract otherwise IMPROVED - `:339-346` filters
`verdict !== "verified"` and returns unconfirmed rows as findings, content not census;
the estate copy of that improvement never happens. My unbounded os.walk census of
memory/runs/mickey17_v2 (all six run dirs): files matching manifest = 0, review = 0.
Consequences banked by both addenda: E30 (the operator-proxy steering act is unauditable
from estate bytes) and E22 (the run interface {topic, targets, width} is
unreconstructible; read-the-estate's "fired: 12" decoded as `String(TARGETS.length)` = 0,
self-referential through `tools/mickey17_v2_fold.py:120` `fired = a.fired or n_files`).
Falsifier: any file under memory/runs/mickey17_v2 naming the review decision or the run's
targets for one run - none exists (instrument named above). Move (~20 min, landable NOW:
.dwf.ts files are disjoint from executor ownership): in the persist phase of
mickey17-v2.dwf.ts and the execute-register draft, write RUN_MANIFEST.json {topic,
targets, width, runslug, gate_digest} and REVIEW.md {decision, bullets} into the run dir
before report(); the fold later reads the manifest for --fired, killing the E22
circularity outright.

## F4 (rank 4). The gate registry relays script SHAPE, not run identity - and its G6 receipt check has gone soft-permanent on the two newest burns

Evidence: `memory/workflows/REGISTRY.jsonl` row 85 (read-the-estate.dwf.ts,
2026-10-04T21:15:36Z) and row 86 (execute-register.dwf.ts, 2026-10-05T04:39:04Z) both
carry G6 ok:false soft "receipt mention lacks a dated stamp" - the newest fleet members
soft-fail the receipt convention at birth and nothing acts on it; rows 59-60 double-register
digest 90b1990da9ae one second apart (absolute + relative path); the 2026-10-04T02:33:47-
02:34:06Z batch re-gated 12 workflows in 19 seconds (a fleet sweep, not run gating); no
row in all 89 names dwfrun-a6bacf9c, dwfrun-e9656e14, or dwfrun-270df86a - a PASS row
cannot say WHICH run it blessed, which is exactly the addendum E22 line "no per-run gate
row exists for this run". Falsifier: a registry row carrying a run id or slug - none in
the 89 rows read. Move (~25 min): tools/workflow_gate.py gains `--run <slug>` recorded
into the registry row (OWNERSHIP COLLISION: executor dwfrun-e9656e14 owns workflow_gate.py
- file OWED or land post-completion); the runners pass RUNSLUG (already computed at
mickey17-v2.dwf.ts:88) and stamp the dated label into their receipt-path constant so G6
clears.

## F5 (rank 5). Fold messages carry no send-moment and the master's landing name drifts per skeleton copy: three names, one convention, zero parameterization

Evidence: FOLD_SECTIONS.md in both archives read this session - the only date strings
are archive paths in the header, no folded-at line (E7, both addenda), while run-0's
archive provably moved 75 -> 94 rows between two folds at the SAME path; the runner
hardcodes MASTER_MICKEY17_V2.md (8 occurrences, counted this session) while read-estate
filed MASTER_READ_ESTATE.md and the execute-register draft hardcodes
MASTER_EXECUTE_REGISTER.md (21 MASTER_ hits) with a dual-copy estate+workspace convention
at draft `:303-304` - an operator cannot predict where the message lands without reading
the specific copy's source (E33). Falsifier: a folded_at or timestamp field inside any
archived FOLD_SECTIONS.md - grep found none. Move (~15 min): the fold script emits a
first line "folded: <UTC ISO> <runslug>" (executor-owned, OWED); the runner takes
MASTER_NAME from args and records it in the F3 manifest (landable now).

## RANKED AMENDMENT TABLE (executable; ownership-respecting)

| # | File | Exact edit | Defect prevented | Evidence row |
|---|------|-----------|------------------|--------------|
| 1 | .zcode/workflows/mickey17-v2.dwf.ts | persist phase: write RUN_MANIFEST.json {topic,targets,width,runslug,gate_digest} + REVIEW.md {decision,bullets} into run dir before report(); MASTER_NAME := args parameter | E30+E22: steering verdict and run interface lost with the report; E33 name drift | REGISTRY 89-row read; runs-tree census manifest=0 review=0; runner :336/:367/:374 |
| 2 | .zcode/workflow-drafts/execute-register.dwf.ts | same three edits as row 1 (it already relays verdict content in its report at :339-346; give that content an estate address) | third-generation copy of E30/E33 | draft read :295-359; MASTER_ 21x, review.decision 3x, manifest 0x |
| 3 | scripts/index_fold_host.mjs + new schtasks MagInboxIndexDaily (09:10, absolute path) | schedule the refold; loop rounds append one Last-result line to state/CURRENT.md | operator boot surfaces 20h/464-events stale vs minute-fresh seals | INDEX.json derived_at vs log line count; schtasks census 342 tasks, no inbox task |
| 4 | tools/mickey17_v2_fold.py - OWED to dwfrun-e9656e14 | decode verdict VALUES from all list-valued keys incl. deep_tier2[].verdict; print yes/no + verified/unconfirmed splits; unconfirmed/crashed into PRISMA excluded; first line "folded: <ISO> <runslug>" | F1: excluded:0 lie; verifier census; E7 no moment | fold.py :157-160/:181-190 byte-read; deep_tier2 count 0; both FOLD verdict lines |
| 5 | tools/workflow_gate.py - OWED to dwfrun-e9656e14 | accept --run <slug>, record in registry row; runners pass RUNSLUG + dated receipt stamp | registry cannot say which run a PASS blessed; G6 soft-fail permanent | REGISTRY rows 85-86, 59-60, the 19-second 12-workflow batch |

Skeleton consolidation (CONVERGENT with operations lens F2, from the relay side): the
thrice-copied mickey17 skeleton should become ONE parameterized saved workflow whose
parameters ARE the report contract (master name, receipt stamp, review persistence,
manifest); the read-the-estate draft should be retired INTO that form, not fired again
as a copy. No workflow deserves death on my evidence; the-50 and the-gala show only
clean PASS history in the registry.

## Checks run this sitting (exact instruments)

1. Full reads: REGISTRY.jsonl (all 89 rows), both spec addenda, MASTER_MICKEY17_V2.md,
   state/CURRENT.md, state/NIGHT_LOOP_20261005.md, execute-register draft :295-359.
2. Byte-verifications via .venv python line reads: fold script :120,:125,:157-160,:181,
   :183,:190,:197,:204,:207,:225; deep_tier2 count 0; url_checked_at count 1 (print
   clause only); mickey17 runner MASTER_ count 8, :88/:300/:336/:367/:374.
3. INDEX.json vs index_events.jsonl: derived_at/event_count vs live line count; needle
   greps both sides with timestamps (00:45Z, 01:38Z, 07:59Z, 08:04-08:10Z).
4. Runs-tree census: os.walk memory/runs/mickey17_v2, filename filters manifest/review.
5. schtasks census via python subprocess with CREATE_NO_WINDOW (342 tasks).
6. FOLD_SECTIONS.md reads in run-0 and 2026-10-04-0 (verdict lines, excluded line,
   timestamp absence).
7. ListWorkflowRuns attempted - refused (capability gap, named below).

## Blind spots (honest)

- The live run board was unreachable from this seat (ListWorkflowRuns returned
  workflow_introspection_unavailable); dwfrun-e9656e14's live progress and token spend
  are OWED - I verified only its estate footprint (2026-10-05-exec lane files e01-e04
  present at walk moment, registry row 86).
- I did not re-verify the read-estate 5 unconfirmed corrections' underlying measurements
  (910/917, 28/30, 250/160, 86.0/89.4) - trust-lens territory; I verified the relay
  blindness, not the re-measurements.
- Sibling lens bodies (operations.md, economics.md) were skimmed at header level only;
  CONVERGENT flags rest on their headers plus my own bytes.
- The INDEX fold_warnings (dozens of writer nonce gaps) were not examined - trust lens.
- Two earlier schtasks attempts failed on shell quoting before the clean subprocess
  census; the 342-task census is the only instrument cited.
- attention.md (70,430 bytes) was sampled at head only; it is a scheduled-task alert
  surface and carries no mega-burn relay, but I did not read all of it.

Filed by the communication lens (lens-communication), OUROBOROS R1 fleet round,
dwfrun-270df86a, 2026-10-05. No em-dashes in this file.
