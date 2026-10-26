# W3R — ESTATE_INDEX mirror dedup (Mickey17 W3 lane, 2026-09-29/30)

**Verdict: DUPLICATION CONFIRMED, byte-for-byte. Pointer swapped. 1,945,896,422 bytes reclaimed.**

## 1. The claim, verified honestly

Telemetry claimed `dashboard/data/ESTATE_INDEX.jsonl` (1.95 GB) was duplicated byte-for-byte
at `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`. Evidence chain (instrument:
`tools/estate_index_dedup.py`, repo venv):

| Gate | Result |
|---|---|
| Sizes | both 1,945,896,570 bytes — equal |
| Head sample sha256 (4 MiB) | `712297ccde3bf5835ebc8ca7b692724591adf243e4aec067db39bdacaba96f27` — match |
| Mid sample sha256 (4 MiB) | `07accc2364c5bc763b296b3c61e595eeb6e12f33e216d978f6f5db1cfe1e8cbb` — match |
| Tail sample sha256 (4 MiB) | `bc08ccaefae97067076c029690503c01a781f1856b904233b20e8802e075f548` — match |
| **Full-file sha256 (both files, streamed)** | **`bd9d34c273b99e1fc6dbe3225946edbc86634a4789926d6de9d8a7f164d86ab1` — EQUAL** |

Not just sampled: the whole 1,945,896,570 bytes of both copies hash identically.

## 2. What was done (order matters)

1. `--check` ran FIRST on the live files: dup confirmed, nothing mutated.
2. `--apply`: sizes + samples re-verified, full sha256 of BOTH computed, **banked BEFORE
   any mutation** to `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl.dedup_shas.json`
   (both full shas, sample shas, sizes, mtimes, verdict, applied_utc 2026-09-30T02:25Z).
3. Mirror replaced (temp + os.replace) by the one-line pointer, 92 bytes:
   `superseded by dashboard/data/ESTATE_INDEX.jsonl, deduped 2026-09-30, sha head/tail recorded`
4. Untouched: `dashboard/data/ESTATE_INDEX.jsonl` (mtime still 09-29 10:23),
   `watch/ESTATE_INDEX/last_run.json`, `rollup.json`. No git commit, nothing else deleted.

**Incident (fixed in-tool):** first swap attempt hit `WinError 5` — os.replace is denied
while any handle on the target lacks FILE_SHARE_DELETE (fleet watchers hold transient
handles; shas were already banked so nothing was at risk). Fix: bounded retry, then
remove+rename fallback, both-denied surfaces as a named error. Second run swapped clean.

## 3. Future checking (`--check` mode)

`python tools/estate_index_dedup.py --check` — exit 0 = duplicate confirmed OR already
deduped (pointer present); exit 1 = DIVERGENT (mirror is not a byte copy — do not dedup);
exit 2 = missing/error. Arbitrary pairs: `--primary P --mirror M`.

## 4. Tests

`tests/test_eid_dedup.py` — **7 passed** (`pytest -q tests/test_eid_dedup.py`, repo venv,
2026-09-29). Covers: dup fixture -> pointer written + full shas banked before swap;
tail-flip divergence -> byte-still mirror, no pointer, no bank, exit 1; size mismatch ->
untouched; post-dedup check -> 'deduped'; second apply -> no-op; missing files -> error
not "divergent".

## 5. Follow-up risk (not W3's to fix)

Both files were written the same morning (mtimes 09-29 10:22/10:23) — the estate-index
producer writes BOTH the dashboard copy and the watch mirror. If its next run re-materializes
the mirror, disk usage returns and `--check` will report `dup` (or `divergent`) again. The
producer should write the watch side as a pointer/rollup only; fence owner: estate-index
producer (not owned by this lane).
