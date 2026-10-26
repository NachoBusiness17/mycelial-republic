# ARENA BACKFILL ATTRIBUTION - UNPROVEN, NOT ASSUMED (2026-10-04)

Filed by lane 6 (arena-cadence) per corpus/steal/MASTER_MICKEY17_V2.md section 9
GO item 6, lane citation a01#5. This receipt states what the bytes prove, names the
candidate runner, and explicitly does NOT credit it, because no receipt names the
runner. The moment-dependence law applies: the banking answer is a function of the
read moment; the tree moved under the a01 audit while it audited.

## What the bytes prove

1. The a01 audit read the tree at 03:04Z 2026-10-04 with 17 dirs unbanked (ledger
   hour buckets 16/20/21/22/23 of 2026-10-03 empty; lane file
   memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json rows 5-6).
2. The same audit's final ledger read at 03:26:51Z shows the drain complete:
   last row ts_utc byte-read as `"ts_utc":"2026-10-04T03:26:51Z"`, 53 session dirs /
   53 GWAP_BANKED / 53 ledger-covered / 0 unmatched either direction; the hour-03
   (2026-10-04) bucket holds 88 rows (recounted 2026-10-04T08:48:53Z, unchanged).
3. So between 03:04Z and 03:26:51Z an out-of-band run banked the whole backlog.
   The hourly fire's own prompt step cannot do this: its catch-up rule is "the two
   newest run dirs lacking GWAP_BANKED" per fire, which structurally starves a
   backlog (a01#3).

## The candidate runner (named, NOT credited)

`tools/arena_gwap.py --backfill` is the only code path whose shape matches the
drain: it walks ALL playground dirs with a transcript and banks every unbanked one
oldest-first (tools/arena_gwap.py main(), --backfill branch). But:

- Grep over watch/inbox top-level receipts for `--backfill` / `arena_gwap.py
  --backfill` (2026-10-04T08:4xZ): zero hits outside the parable and the ARENA_V2
  design doc. No receipt names a runner or a run.
- Counter-possibility left open: the 03:00Z fire was still live inside the drain
  window. automation_runs (read 2026-10-04T08:4xZ) shows the 03:00Z fire row with
  outcome `succeeded` and updated_at 2026-10-04T03:19:41.390Z - its seat could have
  run an out-of-band backfill by hand; equally, a human or another seat could have.
- The 02:21-02:28Z pair of day 03 already proved seats bank outside fire windows
  (02:00Z fire closed well before; a01#7), so out-of-fire manual banking is an
  observed behavior, not a hypothetical.

## Verdict

The 53/53 drain by 03:26:51Z is BYTE-PROVEN. WHO ran it is UNPROVEN. This receipt
deliberately credits no one. If the runner's seat exists, it should leave a one-line
claim with the command it ran; until then any fold or law citing "the backfill" must
cite it as attributed-to-no-one (candidate: tools/arena_gwap.py --backfill).

Systemic fix landed this wave (GO item 6): the bank now runs inside the fire (the
tavern and dungeon carriers invoke the arena_gwap bank on their own run dir at
exit, same process, same second as DONE), and the dawn report carries a banked_at
moment column, so the next drain needs neither a mystery runner nor a moment-less
audit verdict.
