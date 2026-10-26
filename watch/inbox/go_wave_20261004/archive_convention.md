# ARCHIVE CONVENTION - a07 operator-owed item made mechanical (lane C, 2026-10-04)

Parked item (watch/inbox/go_wave_20261004/fifty_wide_guard.md section 7):
fifty-wide Task-agent waves produced no durable per-agent artifacts; the
dispatch was ad hoc, outputs lived only in session transcripts, and the
burn_claims_50wide wave lost 10 units with no replay path. Per-agent archive
retention was filed as operator behavior. Operator said stop parking. This
lane makes it mechanical.

## 1. The tool (tools/fifty_wide_archive.py, new, 280 lines)

The coordinator runs it ONCE POST-WAVE:

    .venv\Scripts\python.exe tools\fifty_wide_archive.py --wave <slug> \
        [--input <file, or stdin when omitted or ->] \
        [--format auto|blocks|jsonl] [--dir memory/runs/fifty_wide]

- Input shapes (auto-detected): labeled blocks (a report starts at a
  '=== <lane> ===' header line and runs to the next header) or JSONL (one
  {"lane": ..., "report": ...} object per line).
- Writes each report to
  memory/runs/fifty_wide/<wave>/agents/<lane>.md and appends one manifest row
  {wave, lane, file, sha256, ts} to that wave's manifest.jsonl. The manifest
  is append-only history: changed bytes for a lane rewrite the file and bank
  a fresh row.
- Idempotency law: re-archiving bytes whose sha256 equals the lane's last
  manifest row is a full no-op (no rewrite, no row), reported as
  "unchanged (sha match)". Prints "ARCHIVED n/lane-count" on success.
- Fail-loud: empty input, content before any header, empty report bodies, and
  duplicate lane labels are exit 1. Missing/unreadable input, a corrupt
  manifest row, and failed writes are exit 2 (cannot verify); idempotency is
  never decided against a manifest that does not parse. Wave slugs and lane
  labels sanitize to safe single path components; sanitizer collisions fail
  rather than silently overwrite.
- Replay pair: the guard's dispatch_log.jsonl row (pre-flight,
  tools/fifty_wide_guard.py) plus this agents dir (post-wave). Either half
  alone cannot explain a count gap.

## 2. The convention (playbook law 14, appended)

corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md gained one dated appended
section (13 lines incl. separator, under the 15-line cap; bytes above the
append point untouched): every Task wave of width >= 5 ends with one
fifty_wide_archive run post-wave; the guard's dispatch log row plus the
agents dir are the replay pair. Append-only honored.

## 3. Tests (tests/test_fifty_wide_archive.py, new, 203 lines)

Instrument: .venv\Scripts\python.exe -m pytest tests/test_fifty_wide_archive.py -q
Final run this ask: **12 passed, 0 failed, 0 skipped in 7.89s** (first run,
2026-10-04, green on first full pass).

Pinned bands: block and JSONL inputs both archive with exact manifest-row
shape {wave, lane, file, sha256, ts} and sha256 matching on-disk bytes;
archive-then-rearchive is a full no-op (ARCHIVED 0/2, file mtime_ns
unchanged, manifest rows byte-identical); changed bytes rewrite the file and
append a third row (append-only history); empty input exits 1 with nothing
written; headerless content, empty bodies, and duplicate lanes exit 1; a
missing input file exits 2; a corrupt manifest exits 2 and adds no row past
the corruption; slug/lane sanitization lands the file at the safe path; and
CLI exit codes (0, 0-via-stdin, 1, 2) are pinned through a real subprocess.

Sibling check: tests/test_fifty_wide_guard.py still green alongside (22
passed total for both files, 16.13s).

## 4. Live demonstration against the real estate

A smoke wave was archived through the real CLI (stdin feed) at
memory/runs/fifty_wide/smoke_20261004_archive_convention/ (kept as the
living example):

- Run 1: "ARCHIVED 3/3" (lane-alpha, lane-beta, lane-gamma).
- Run 2, identical bytes: "ARCHIVED 0/3" plus three "unchanged (sha match)"
  lines; no new manifest rows.
- Disk truth (re-hashed after the run): lane-alpha c1ada62fee180df9 (66
  bytes), lane-beta f27551af88ad971b (22 bytes), lane-gamma bb196a9cbfb04bcc
  (23 bytes) - each equals the sha256 banked in manifest.jsonl (ts
  2026-10-04T10:03:32Z). Trust bytes, not reports: verified on disk.

## 5. Clean-file proof

- violation_ratchet.violations_in: tools/fifty_wide_archive.py CLEAN (0),
  tests/test_fifty_wide_archive.py CLEAN (0).
- Em-dash/en-dash byte count: 0 in every file this lane wrote (tool, tests,
  playbook section, this receipt).
- Line counts: 280 (tool) and 203 (tests), both under the 400-line bar.

## 6. Files touched (disjoint ownership held)

- tools/fifty_wide_archive.py (new; the post-wave archive)
- tests/test_fifty_wide_archive.py (new; 12 tests)
- corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md (ONE dated appended
  section, law 14; append-only)
- memory/runs/fifty_wide/smoke_20261004_archive_convention/ (live-demo
  artifact, deliberately kept)
- watch/inbox/go_wave_20261004/archive_convention.md (this receipt)

tools/fifty_wide_guard.py untouched. No git commit made (coordinator
commits). Filed by the archive-convention lane, 2026-10-04.
