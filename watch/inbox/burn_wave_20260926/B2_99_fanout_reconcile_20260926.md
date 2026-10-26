# B2-99 FAN-OUT RECONCILE 20260926

## Verdict

The AGENTS.md fan-out bullet is reconciled with the dispatch-shape law and no longer carries the
falsified width-only folklore. The old bullet told every reader to cap dispatch at
`max_concurrency` 3 "citing z.ai 1302" as the plan's concurrency cap; the gala bytes show that cap
was scoped to the wrong shape: workflow children get `maxAttempts 0` and die on the first 429/1302,
while Task agents ride the main-session retry path (`maxAttempts 11` + driver backoff) and measured
clean at widths 3, 6, 10 and 12, with the 20260926 re-measure banking 109.4M tok/h at width 10 and
zero surfaced 1302s. The bullet now names the shape distinction, keeps the workflow-children cap at
3 or less, records the Task-agent ladder, keeps the honestly untested 15-16 rung and the post-burst
penalty, and cites all three receipts (the original storm receipt plus the two the brief named).
Spec-before-behavior honored: the owning doc moved before any code that would rely on the new law.
The pre-checked B2-99 row's check is now earned by this receipt.

## Evidence

Old bullet (AGENTS.md:32, read on bytes 2026-09-26T18:32Z before the claim-plus-edit):
"**Fan-out width law:** on `account:zai-individual-coding-plan`, dispatch workflows at
`max_concurrency` 3 or less (z.ai 1302 = the plan's concurrency cap; Lite is rated ONE project at a
time; off-peak earns more). A 50-wide dig on this account 429-storms the account and crashes
tethered sessions with fake "subscription" errors. Receipt: `corpus/steal/TETHERED_LINK_STEAL_20260925.md`."

Receipt 1, watch/inbox/GALA_20260925.md: envelope table line 26 "workflow children 50-wide ... 1302
storm, children maxAttempts 0"; lines 27-29 Task agents clean at width 3, 6 and 12; named law lines
33-38: "DISPATCH SHAPE IS THE RETRY STRATEGY. Workflow children get zero adapter attempts and die
on first 429; Task agents ride the main-session retry path (maxAttempts 11 + driver backoff) and
climbed 3-6-12 clean. The old width-3 folklore was scoped to the wrong shape."

Receipt 2, watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md: verdict lines 5,
25-27: wave 1 ran 10 Task agents concurrently, 10/10 completed, zero 1302 in the session's 25 agent
output files, 37,386,533 witnessed tokens in 0.34165 h = 109.4M tok/h; clean ladder reads 3-6-10-12;
the 15-16 ceiling rung untested; falsifier 1 names the blind spot that zero 1302 recorded means
zero surfaced (main-session retry absorbs silently, TETHERED_LINK_STEAL_20260925.md:17).

Supporting: memory/burns/LEDGER.jsonl row 46 "1302 ceiling found at width 15-16 then 12-post-burst:
limit is rolling throughput, not width-only"; AFTERPARTY_CLOSE_20260926.md:8-9 "Task agents clean
at 3/6/12; ceiling between 12 and 16; after a burst even 12 gets 1302s until the window decays."

New bullet (AGENTS.md:32, on bytes after this landing): names the shape distinction, keeps workflow
`max_concurrency` at 3 or less, records the Task-agent retry path and the 3-6-10-12 clean ladder
with 109.4M tok/h at width 10, keeps the 15-16 rung untested and the post-burst penalty, and cites
`corpus/steal/TETHERED_LINK_STEAL_20260925.md`, `watch/inbox/GALA_20260925.md`,
`watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md`. Every factual token in the
new bullet traces to one of the bytes above; the dropped claims ("z.ai 1302 = the plan's concurrency
cap", "Lite is rated ONE project at a time", "off-peak earns more") were the folklore the gala
envelope table measured against and found shape-scoped wrong.

## Work done

Appended two CLAIM lines to QUEUE.md (AGENTS.md and own board) at 18:33:00Z per the shared-file
claim law before touching either file's bytes; re-read AGENTS.md fresh post-claim and replaced only
the line-32 bullet (no other byte of the file touched); re-read QUEUE.md tail fresh and rebased on
the live concurrent B2-162/B2-163 claim lines (theirs untouched, appended after them); filed this
receipt; appended the LEDGER row via .venv/Scripts/python.exe json.dumps; retired both of my claim
lines (CLAIM to CLAIMED with receipt pointer); appended the landing note to the pre-checked B2-99
row earning its check; self-fed B2-429 to B2-431 UNCHECKED under Open (highest brief row on the
board was B2-428 at apply time). Em-dash count on every byte this lane wrote: 0.

## Falsifier

1. A receipt this lane did not read (a 09-26 re-measure other than B2-25, or a memory/briefs entry)
   could carry a newer ladder; the bullet cites exactly the two receipts the brief named plus the
   original storm receipt, and names the 15-16 rung untested so a newer rung would amend, not
   contradict, the landed text.
2. The width-10 clean read cannot prove zero 1302s occurred, only zero surfaced (B2-25 falsifier 1,
   the retry blind spot); the bullet words it as "zero surfaced 1302s" on purpose, and B2-98's
   provider-error counter is the instrument that would close the gap.
3. The 15-16 ceiling rung is untested; a clean width-15 Task wave extends the ladder and a 1302
   there confirms the rung (the armed B2-97 card owns that fire on an operator GO), so the landed
   bullet is deliberately provisional at the top of the ladder.
4. Dropping "Lite is rated ONE project at a time" could overstate freedom if the published rating
   is enforced at a layer the gala never touched (a multi-project parallel run, not a width rung);
   the gala only proves Task-agent waves within one session are clean, and the bullet keeps the
   workflow cap for exactly that reason.

## Bibliography closed

Read: watch/inbox/burn_wave_20260926/QUEUE.md (header law block, B2-99 row line 234, B2-97/B2-98
rows, active claim tail); watch/inbox/GALA_20260925.md (whole); watch/inbox/burn_wave_20260926/
B2_25_envelope_remeasure_20260926.md (whole); watch/inbox/burn_wave_20260926/
B2_97_width15_probe_20260926.md (whole, for the untested-rung and GO-gate wording);
memory/burns/LEDGER.jsonl (tail row shape plus the row-46 quote as cited by B2-25); AGENTS.md
lines 20-64 on bytes before and after the edit. No web sources. Every claim in this receipt was
read from file bytes this session; nothing synthesized; em-dash count 0.
