# GAP_REGISTER R4 FILL - arena banked_at moment column + backfill credit (2026-10-10)

Filed by GALA lane a01-arena-cadence-r4 (division B, the owed waltz), closing
GAP_REGISTER row R4 [high] a01-arena-cadence (new),
watch/inbox/gap_analysis_20261010/GAP_REGISTER.md:21-24. Raw verification
output for every number below lives in the check file
watch/inbox/gala_20260925/rung/lanes/a01-arena-cadence-r4.check.txt
(this sitting's own runs).

## What R4 demands

FILL verbatim (register line 23): "add a banked_at moment column to the dawn
report's gwap line (rows, sessions, AS-OF timestamp) and a receipts note
crediting the backfill run (tools/arena_gwap.py --backfill is the only flag
that matches the 88-row hour-03 drain, but no receipt names it - attribution
is unproven), landing in watch/inbox/."

## Finding: both halves landed 2026-10-04 (GO item 6), BEFORE the register
mint. This sitting re-proved every byte and stamped a fresh AS-OF.

The register was minted 2026-10-10 from the ORIGINAL run's lane rows
(memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json row 6 is
R4's source row), which predate the same-day cure. Nothing was redone;
everything was verified.

### Half 1: the banked_at moment column (code + rendered artifact)

- tools/arena_gwap.py:261-304 is status(), docstring line 262: "The dawn
  report's gwap line with the banked_at moment column." Its output shape
  carries exactly the FILL's triple: "GWAP LEDGER AS-OF <timestamp>",
  "ledger rows=<N> distinct_scenes=<M> dirs=<D> banked=<B> unbanked=<U>",
  then one banked_at line per session dir (rows, sessions, AS-OF).
- tools/cycle_brief.py:122-143 (section_arena_gwap) renders that instrument
  into the dawn/cycle brief under the header "ARENA GWAP (banked_at moments
  - the moving-tree law: no count without its AS-OF)".
- Rendered on disk: watch/inbox/CYCLE_BRIEF_20261004.md:52-55, AS-OF
  2026-10-04T08:43:45Z, ledger rows=476 distinct_scenes=343 dirs=73
  banked=67 unbanked=6.
- Re-run by this sitting (check file, first command, exit 0). Verbatim head
  of that captured run, grep-able:

```
GWAP LEDGER AS-OF 2026-10-10T13:12:39Z
ledger rows=730 distinct_scenes=597 dirs=110 banked=110 unbanked=0
```

  The instrument is live, not vestigial. (An earlier interactive run of the
  same command this sitting stamped 13:10:37Z with identical counts; the
  check file's captured 13:12:39Z run is the canonical one quoted here.)

The moment-dependence law is demonstrated by the stamps themselves: the same
line read 414 rows at the register's 03:3xZ moment, 476 at the 08:43Z brief
render, 730 at today's read. No count without its AS-OF, three times over.

### Half 2: the receipts note crediting the backfill run

- watch/inbox/ARENA_BACKFILL_ATTRIBUTION_20261004.md is that note, in
  watch/inbox/ as the FILL names. It byte-proves the drain (53 session dirs
  / 53 GWAP_BANKED / 53 ledger-covered / 0 unmatched either direction by
  03:26:51Z, 88 rows in the 2026-10-04 hour-03 bucket), names
  tools/arena_gwap.py --backfill as the only code path whose shape matches
  (it walks ALL playground dirs with transcript + DONE oldest-first,
  tools/arena_gwap.py:329-332), and deliberately credits no runner because
  no receipt names one.
- This fill receipt endorses that stance and restates it as the credit: the
  RUN is credited (the drain happened, bytes prove it); the RUNNER stays
  unattributed (candidate: tools/arena_gwap.py --backfill, attribution
  unproven). Any fold citing "the backfill" cites it this way.

### SOURCE re-proof at this sitting (all numbers byte-matched)

Run against memory/runs/gwap/arena-capability.jsonl at 2026-10-10 (check
file, third command): rows with ts_utc before 2026-10-04T04:00Z = 414
(register: 414); last ts in that slice = 2026-10-04T03:26:51Z (register:
same); hour buckets 13h=121, 14h=145, 15h=12, 17h=12, 18h=12, 19h=12,
02h(10-04)=12, 03h(10-04)=88 (register: identical, including the zero-row
hours 16/20/21/22/23 implied by absence). Honest partials confirmed:
dnd0_20261003T225014Z and dnd0_20261003T225040Z banked 2 rows each at
2026-10-04T03:16:51Z; the mid-flight 03:03Z trio dnd0_20261004T030348Z /
  030349Z / 030426Z banked 3 rows each at 03:16:52-53Z; the final 03:26:51Z
row belongs to dnd0_20261004T032151Z (3 rows). Marker census (check file,
second command): 46 dirs of 2026-10-03 + 7 dirs of 2026-10-04 hour<=03 =
53, every one carrying GWAP_BANKED at this read (110 dirs total, 110
banked, 0 unbanked anywhere on the tree today).

## Verdict

R4 CLOSED as verify-and-bank. The fill's named landing spots are on disk
(the receipts note above; the banked_at column live in code and rendered in
the 2026-10-04 brief), and this sitting's fresh AS-OF stamp re-arms the
moment law for the next reader.

## Addendum (2026-10-10T13:33Z): the code moved under this lane too

While this receipt was being written, a sibling seat grew
tools/arena_gwap.py from the 357-line bytes this sitting verified (status()
at lines 261-304) to 426 lines: mtime 13:13Z, one minute after the captured
13:12:39Z run; status() now sits at line 325 with its docstring line 326
unchanged; +69 lines vs HEAD per git diff --stat. The fill was re-verified
against the CURRENT bytes: a fresh --status run stamps AS-OF
2026-10-10T13:32:48Z with identical counts (rows=730 distinct_scenes=597
dirs=110 banked=110 unbanked=0). The violation ratchet, run read-only as
tree evidence, exits 1 with one NEW finding (file-too-long:
tools/arena_gwap.py:426) plus three GROWTH claims, all sibling-seat
in-flight state: this lane authored nothing under mag/ or tools/ (its only
writes are this receipt, its check file, and its lane JSON, all new files
under watch/inbox/). The moment law this fill banks applies to code bytes
too.
