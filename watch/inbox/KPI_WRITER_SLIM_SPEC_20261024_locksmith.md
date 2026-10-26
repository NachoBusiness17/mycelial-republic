# KPI WRITER SLIM SPEC (locksmith, 2026-10-24): bound the incomplete_ids embed so logs/kpi.jsonl stops refattening after rotation

## The door

mag/records.py write_kpi (:138-168) appends one KPI row to logs/kpi.jsonl per
call and embeds the FULL incomplete-session backlog as a list of session ids
(:157-159, "incomplete_ids"). Measured cost: rows fattened from 17,653.1
bytes/row (10-10) to 95,044.5 bytes/row (10-17) as the backlog grew to
2,199-2,992 ids; the file crossed the CADENCE spec's own 790,000,000-byte
crisis line on 10-16 and reads 3,120,765,053 bytes today (3.95x the line).
tools/rotate_kpi.py --apply cures the file (dry run this cycle: 33,380 of
34,380 rows archivable, live drops to 33,026,341 bytes) but the writer
re-silts the file with every fat row. Rotation cures the symptom; this spec
cures the writer.

## Consumers (Anti-Cow: who reads the field)

- mag/operator_os.py:238 reads kpi.get("incomplete_ids") or [] into the dna
  block of the operator OS pack. It needs a list, not a complete list; the
  authoritative count already rides n_incomplete (:237). A bounded sample
  keeps this consumer working unchanged.
- tools/rotate_kpi.py archives rows whole (field-agnostic; size is the only
  thing it measures).
- tools/gap_gauges.py reads bytes, mtime age, last-row ts only.
- tools/gap_sentinel.py cites kpi.jsonl as the zero-reader class; no reader
  consumes the id list today.
- tests/: zero existing coverage of write_kpi output (rg write_kpi and
  incomplete_ids over tests/: 0 files, checked 2026-10-24).

## Change (mag/records.py, write_kpi)

1. Module constant KPI_SAMPLE_CAP = 50.
2. write_kpi builds all_ids once, then embeds:
   - "incomplete_ids": all_ids[:KPI_SAMPLE_CAP]
   - "incomplete_ids_total": len(all_ids)
   - "incomplete_ids_truncated": len(all_ids) > KPI_SAMPLE_CAP
3. n_incomplete stays the full-precision count (unchanged).
4. Comment on the change names the cause and this spec path (fix-comment
   law). No reader file changes required.

## Behavior after

Row size is bounded near ~2 KB regardless of backlog size; kpi.jsonl growth
becomes row-count-driven, not backlog-driven. The existing 3.12 GB still
needs the operator's rotation line (--apply or the drafted
MagCadenceOrgansDaily mount, rows 3/5 of the promise pile); this change
stops the refattening after that cut.

## Verifier

New tests/test_kpi_writer_slim_20261024.py (Anti-Cow: consumer named in
docstring, verifier is the file itself):
- fat backlog (120 ids): embedded list capped at KPI_SAMPLE_CAP, total 120,
  truncated True, n_incomplete still 120, jsonl row carries the same shape.
- small backlog (3 ids): list intact, total 3, truncated False.
- both run with BIO/KPI_PATH/KPI_LOG and pack_report monkeypatched to
  tmp_path (no real-file contact).

## Effect gate

No scheduled task, no host-side machinery, no spend. Ordinary code change on
the mag/ path; the ratchet and citation lint still run at pre-push. The
rotation itself stays operator-gated per tools/rotate_kpi.py's own docstring
(default dry run), unchanged by this spec.
