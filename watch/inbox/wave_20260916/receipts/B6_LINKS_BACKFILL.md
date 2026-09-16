# B6 — INTAKE links backfill into canonical ledger

- date: 2026-09-16
- lane: B6_LINKS_BACKFILL
- operator drop: verified-pending, 2026-09-14
- tool: `mag.link_library.add_urls` (no hand edits to LINKS.jsonl)
- script: `artifacts/backfill_links_20260916.py` (stdlib only, fixed paths)
- runner: `.venv\Scripts\python.exe`
- glob: `watch/inbox/INTAKE_*.md` (strict prefix `INTAKE_`; sibling intake-named files like `FIVE_LINK_INTAKE_*` are outside the given pattern)

## Status: COMPLETE

## Before

- `wc -l watch/inbox/LINKS.jsonl` = 136

## Plan

1. enumerate `watch/inbox/INTAKE_*.md`
2. extract URLs per file (`https?://\S+`, trailing markdown punctuation trimmed)
3. per URL: `add_urls([url], note=f"backfill from {filename}", writer="backfill-20260916")`
   - DUPLICATE flag = canonical already known (expected, that is success)
   - ValueError from `validate_host_safety` (localhost/private) = refused, counted
4. re-count ledger lines

## Results

- files scanned: 18 (`INTAKE_*.md` glob, strict prefix)
- URLs found: 6
- registered (new canonical): 6
- duplicate (canonical already known): 0
- refused (validate_host_safety / localhost-private): 0
- `wc -l watch/inbox/LINKS.jsonl` before = 136, after = 142 (+6, all `writer: backfill-20260916`)

Registered URLs (via `mag.link_library.add_urls` only):

| canonical | source file |
|---|---|
| https://suno.com/s/zJbxdyVGZsVvUPlF | INTAKE_DISSOLVE_20260907.md |
| https://arxiv.org/abs/2405.02421 | INTAKE_HAUL11_20260907.md |
| https://openreview.net/forum?id=2HJRwwbV3G | INTAKE_HAUL11_20260907.md |
| https://arxiv.org/html/2605.11496v1 | INTAKE_HAUL11_20260907.md |
| https://www.anthropic.com/research/global-workspace | INTAKE_HAUL11_20260907.md |
| https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/69ef71d84c7cac3b9be8dd42_260401_UK_AISI_Research_Sabotage_Report.pdf | INTAKE_HAUL11_20260907.md |

Per-file breakdown: 16 of 18 files contain **zero** raw URLs (prose-only intake notes citing titles/sources in words). Only INTAKE_DISSOLVE (1 URL) and INTAKE_HAUL11 (5 URLs) carried links.

## Notes

- The mission anticipated "many DUPLICATE flags"; the honest result is **0 duplicates** — none of the 6 URLs in the strict `INTAKE_*.md` set were already canonical in the 136-line ledger. The pre-existing ledger entries came from other writers (sibling intake-named files like `FIVE_LINK_INTAKE_*` sit outside the given glob and were not scanned).
- Writes went exclusively through `mag.link_library.add_urls`; LINKS.jsonl never touched by hand. Verified post-run: exactly 6 lines carry `writer: backfill-20260916`.
- Script: `artifacts/backfill_links_20260916.py` (stdlib only, fixed paths, venv run). Trailing markdown punctuation trimmed after the `https?://\S+` match; within-file repeats deduped before submission.
- No git commands, no paid APIs.
