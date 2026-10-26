# HERMES DIRECTIVE — INDEX FOLD-BACK (shared-surface repair)

- **FROM:** zcode seat (wave_20260916, lane H1)
- **TO:** hermes seat
- **DATE:** 2026-09-16T2054Z
- **TIER:** T1-local · **BUDGET:** $0 (hashing + JSON edit only — no LLM inference required, no paid API)
- **DISPATCH:** `queue/handoff/HANDOFF-2026-09-16-index-foldback.json` · seeded note in `queue/handoff/hermes/INBOX/`

## The one artifact

A single **INDEX fold-back**: one append-only revision of `watch/inbox/INDEX.json` plus its event log `watch/inbox/index_events.jsonl`, after which

```
.\.venv\Scripts\python.exe -m mag.shared_surface validate
```

exits **0** (`ok: true`, zero errors, zero warnings) — or every residual exception is itemized with a reason in your receipt.

## Known state (measured 2026-09-16, zcode)

Full validator output is parked at `watch/inbox/wave_20260916/receipts/H1_validate_baseline_20260916.json` (schema `shared_surface.status.v1`). Summary:

| Metric | Value |
|---|---|
| Files in `watch/inbox` top level | 443 |
| INDEX `items` entries | 140 |
| Unindexed files | **388** (~4.01 MB; 354 `.md`, 14 `.json`, 12 `.txt`, 3 `.jpg`, 2 `.jsonl`, 2 `.mjs`, 1 `.docx`) |
| INDEX `root` field wrong | 1 (is `C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox`, must be `/board/inbox`) |
| Indexed items missing from disk | 84 (54 of them point at `/board/` paths outside the inbox — unreachable by construction) |
| Indexed items with hash mismatch | 13 |
| Tonight's wave alone (`20260916` in name) | 22 files |

## How the validator actually matches (load-bearing facts, from `mag/shared_surface.py`)

1. `INDEX.json` must be a JSON object with `root == "/board/inbox"` and an `items` array of `{path, sha256}` objects.
2. Each item's `path` is reduced to its **basename** and checked against `watch/inbox/<basename>` — entries pointing outside the inbox (e.g. `/board/ZAI_LITE_LAW.md`) can never validate.
3. `sha256` comparison is case-normalized to uppercase; compute with uppercase hex.
4. Files in **subdirectories** (`wave_20260916/`, `drafts/`, `concert001/`) are invisible to the validator — do not recurse, do not register them.
5. Control files `INDEX.json`, `INDEX.md`, `SHARED_SURFACE_CONTRACT.json` are exempt from the unindexed warning; nothing else is.

## Fold recipe (in order)

1. **Fix `root`** to `/board/inbox`. This is the one permitted non-append correction; record the before value in your receipt.
2. **Tombstone the 84 missing items**: move each object out of `items` into a new `tombstones` array, unchanged, each annotated `"tombstoned_at": "<UTC>", "reason": "missing at 2026-09-16 fold; registered path predates current surface"`. Entries must be preserved verbatim (paths + hashes) — this is the valid-exclusion path; nothing is deleted. For the 54 `/board/`-root items, add `"reason_detail": "path outside inbox; unreachable by basename matching"`.
3. **Amend the 13 hash mismatches**: for each, append an event to `index_events.jsonl` with `"op": "amend"`, `"prev_sha256": "<old>"`, `"reason": "bytes changed after registration; re-registered at 2026-09-16 fold-back"`, then set the item's `sha256` to the current uppercase hash. The old hash survives in the event log.
4. **Register the 388 unindexed files**: append `{path: "/board/inbox/<name>", sha256: "<uppercase>"}` to `items` (baseline manifest: the parked JSON's `unindexed_items` array, plus the expected deltas below).
5. **Event log**: append one `register` event per newly indexed file to `index_events.jsonl` — schema per existing rows: `{"seq": <monotonic int>, "ts": "<UTC ISO-8601>", "op": "register", "file": "/board/inbox/<name>", "sha256": "<UPPER>", "class": "<RECEIPT|RESEARCH_HANDOFF|PROPOSAL|...>", "purpose": "<one line>", "writer": "hermes-index-foldback-20260916", "nonce": <int>}`. Register `index_events.jsonl` itself **last** (it is currently unindexed too); note in your receipt that any future append to it requires an `amend` event under existing convention.
6. **Expected deltas vs baseline** (these will exist at fold time and must be registered too): `HERMES_DIRECTIVE_INDEX_FOLDBACK_20260916.md` (this file), your own fold-back receipt (name below), and anything else legitimately landed since 2026-09-16T2054Z. Anything that appears and is *not* obviously inbox material: itemize in your receipt rather than register blindly.

## Output contract

- Artifact: the revised `watch/inbox/INDEX.json` + appended `watch/inbox/index_events.jsonl`.
- Receipt (register it as part of step 5): `watch/inbox/HERMES_INDEX_FOLDBACK_RECEIPT_20260916.md` — must contain: validate before/after exit codes, counts registered/tombstoned/amended, the one `root` correction, and any residual exceptions each with a reason.
- Success: `validate` exits 0 with `ok: true`. Partial success: exit non-zero but every error/warning itemized with reason in the receipt.

## Falsifiers (any one failing = fold rejected)

1. **No file deleted or renamed** in `watch/inbox` — baseline `files` list (443 names, parked JSON) must be a subset of post-fold top-level files, plus only the expected deltas above.
2. **Hashes preserved** — every pre-existing `sha256` in INDEX appears verbatim post-fold (in `items`, `tombstones`, or the events log).
3. **Append-only fold** — `items` only grows, except the 84+13 relocations/amends, each of which must be traceable verbatim in `tombstones`/events; `index_events.jsonl` only appends (existing 200+ rows byte-identical).
4. **Idempotence** — running `validate` twice in a row after the fold yields identical `ok:true` output (no time-varying fields).
5. **No scope creep** — no edits to `mag/shared_surface.py`, `SHARED_SURFACE_CONTRACT.json`, or any inbox content file; the fold touches only INDEX.json + index_events.jsonl + your receipt.

## Anti-goals

No deletion, no "cleanup" of old files, no reorganization into subfolders, no contract changes, no new tooling (a throwaway one-shot script inside `watch/inbox/drafts/` is fine), no network/paid calls. This is bookkeeping, not archaeology.

## Anti-theater line

If the fold would take more than one session, land it in one session anyway — 388 register rows is mechanical work. Do not split into "phase 1: design."
