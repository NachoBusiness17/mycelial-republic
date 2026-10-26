# PERSONAL SORT 2026-10-26 - the device transfer is sorted, chaff staged for review

Operator: the huge all-devices personal transfer landed at
`C:\Users\foste\PERSONAL_ARCHIVE_20261025\` (Bob 8,526 / Moto 6,438 / Pixel
503 / T90 252 files, sha256 manifests for Pixel+T90, device-shaped trees).
Sorted per `watch/inbox/DEVICE_DOWNLOADS_PLAN_20261025.csv` (8,245-row
census, per-row action + suggested name).

## Executed (scripts/sort_personal_archive_20261026.py, ledger-replayable)

`C:\Users\foste\PERSONAL_SORTED_20261026\` - 7,467 moves, ~27.0 GB, every
move one row in move_ledger.jsonl (7,471 rows incl. 4 preflight recon):
- photos/ 10.9 GB - 1,213 camera/media keepers by device (moto/pc/t90)
- memes/ 5.6 GB - 1,940 saved/received media
- uncertain/ 3.7 GB - 869 origin-unclear images, staged for review
- chaff/ 5.6 GB - 3,383 remove-candidates + 66 dedupes, quarantined
  for THE OPERATOR'S WEEKLY CHAFF TRIAGE (nothing deleted)
- keep: 394 rows stayed in the archive by plan

## Known gaps (honest)

- Bob + Moto pulls were rc=1 TRUNCATED TARS (_logs/phones_pull.log):
  27 personal_archive rows + 379 total rows missing on disk (mostly
  .thumbnails never transferred + the truncated tails). Re-pull of the
  missing tails owed over the mesh; Moto missing count includes
  Movies/Telegram truncation.
- Bob+Moto lack sha256 manifests (Pixel/T90 have them); verify pass owed
  on the re-pull.

## Next for the operator

1. Sort `PERSONAL_SORTED_20261026\chaff\` (the week's chaff - 3,449 files,
   5.6 GB; thumbnails/caches/dupes; delete-at-will, it is quarantine not
   record) and glance `uncertain\` (869).
2. Say GO on the re-pull for the Bob/Moto truncated tails.
