# A-16: Lens-rz1 results fold-in (archeology.wave2 lane receipt)

Schema: archeology.wave2.receipt.v1 · lane A-16 · night lane 2026-10-02 ~04:1xZ
Cost: $0 (bytes only). Deliverable per memory/plans/ARCHEOLOGY_20.md row A-16:
LENS1_VERDICT.md (C1-C3 live-or-die + genealogy note). Verdict BELOW cannot
fire tonight; this receipt is the honest partial plus the falsified premise.

## Bytes checked (all 2026-10-02 ~04:10Z)

- watch/inbox/model_garden/lens1/lens1_results.json: DOES NOT EXIST (dir
  listing: only lens1_row_zero.py 22880 B and lens1_run_log.txt 15155 B).
- watch/inbox/model_garden/STOCHASTIC_LENSING.md sections 6 and 7: both read
  "PENDING RUN" (lines 208-213).
- lens1_run_log.txt tail: [load] gemma2:2b-instruct-q5_K_M 227s; [answers] 18
  greedy frame answers 710s; [samples] 60 cloud samples 2392s. Log mtime
  2026-10-02 00:09 local stamp on disk (mtime), last content phase = samples.
- memory/runs/kache/captures.jsonl: LAST rows ts 2026-10-02T01:43:44Z,
  qwen2.5:3b-instruct L9/L18/L27 P10 capture rows, schema kache.capture.v1.
  So capture appends continued ~94 min after the run log's last phase line,
  then stopped.
- No python process matching lens1/row_zero alive at 04:05Z (WMI scan).

## Verdict

C1-C3 (the lens-rz1 predictions in STOCHASTIC_LENSING.md sec 5) are
UNEVALUATED: the run died between capture-append completion (01:43:44Z) and
the analysis/results phase. The expensive legs (model loads, answers, samples,
both families' captures) are banked on disk; only the analysis and the results
json are missing. Live-or-die remains open; nothing here refutes any
prediction.

## Why it died (bounded claim)

Not established by bytes; the log shows no traceback (tail ends on the
samples-done line). Candidates in order of evidence: the seat that owned the
lane ended without the analysis leg, or the analysis phase crashed without
redirecting stderr into this log. Do not claim OOM without a receipt.

## Morning repair ticket (cheap, local, free-lane)

lens1_row_zero.py main() has a rerun guard that REFUSES a second run while
lens-rz1 rows exist in captures.jsonl (lines ~295-299, duplicate-append
protection), and NO analysis-only entry point. The repair is an amend, not a
rerun: add an --analyze-only mode that loads the banked captures.jsonl rows +
.npy sidecars under memory/runs/kache/vec/, runs the LOO/silhouette analysis
against the C1-C5 prediction block, and writes lens1_results.json + sections
6/7 of STOCHASTIC_LENSING.md. Then A-16 verdict fires for real.

## Genealogy note (the part of A-16 that IS actionable tonight)

Per the wave-1 arc (ARCHEOLOGY_WAVE1.md, now redacted-committed in 0c9d72a06)
the lens-rz1 lineage runs: the Aug-12 stillbirth doctrine -> stochastic
lensing theory -> this run. The Aug-12 sentence is the prior art; this receipt
adds only: the first execution of that doctrine banked its captures and lost
its verdict to a dead session, which is itself the stillbirth shape the
doctrine names. The fix is always the same: the analysis leg must be cheap,
resumable, and seat-independent.

Filed by night lane, 2026-10-02Z. $0. No em-dash bytes. LANE COUNT: A-16
partial (premise falsified, repair ticket filed).

## ADDENDUM 2026-10-04: verdict fired (append-only, queue-truth-a14, mickey17_v2 GO item 7)

The repair this receipt ticketed was executed ~90 minutes after filing, and
the A-16 verdict below ("C1-C3 are UNEVALUATED") is superseded by landed
bytes:

- watch/inbox/model_garden/lens1/lens1_results.json now exists (13,505 B on
  disk, internal ts "2026-10-02T05:49:57.674040Z"; this receipt's bytes-checked
  section correctly recorded its absence at ~04:10Z).
- watch/inbox/model_garden/STOCHASTIC_LENSING.md section 6 is titled "RESULTS
  (lens-rz1, landed post-run)" (run fired 04:37Z, completed 05:49:57Z) and
  section 7 records the verdict: C1 (frames separate launch positions) REFUTED
  in pre-registered form on both models at every depth; the real discovery is
  that the frame's REGISTER, not its AIM, moves the launch representation.
- The "LANE COUNT: A-16 partial" line above is closed by this addendum:
  A-16 is COMPLETE. Premise no longer falsified-as-stalled; the run's
  expensive legs were banked, the analysis leg landed, the verdict fired.
- The "do not claim OOM without a receipt" discipline stands; the death cause
  of the original attempt remains unestablished and is now moot.

The closing the night orders asked for ("then A-16's verdict fires for real")
is done; NIGHT_CLOSE_20261002.md morning-move 2 was struck 2026-10-04 with a
pointer here. Amended by queue-truth-a14, 2026-10-04. $0. No em-dash bytes.
