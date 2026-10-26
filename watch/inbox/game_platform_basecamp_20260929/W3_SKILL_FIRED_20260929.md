# W3: skill_fired.v1 receipts at the skills_for_job chokepoint (2026-09-29)

Lane: Mickey17 Wave 3 (replacement lane; the prior lane died to a rate limit pre-write).
Spec: `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md` return 16 (skills organ):
the ledger held routing decisions, never fires; progressive disclosure was wired but
unmeasured, and the excerpt line filter was a no-op.

## What landed

Files (no commit; additive only; `mag/context_pack.py` untouched per fence):

- `mag/skills_pack.py`
  - `skills_for_job` now appends one `skill_fired.v1` receipt row per skill
    actually returned, to `memory/improve/skill_ledger.jsonl` (shared file; the
    schema tag separates these from the existing `skill_ledger.decision.v1`
    rows, and `fired()` counts only `skill_fired.v1`).
    Row: `{schema, skill_id, job, pack_mode, chars_injected, ts}`.
    `pack_mode`: `excerpt` (body clipped into the pack, chars = chunk length)
    or `missing` (path unresolved, chars 0). Skills skipped by
    `pack_excerpt: false` or by budget exhaustion are NOT returned and never
    fire. Ledger write failure swallows OSError only: telemetry must not break
    pack building.
  - Fixed the no-op line filter (was `... or ln.strip()`, truthy for every
    non-blank line, so the `#`/`**` checks filtered nothing). Dated fix comment
    carries cause + evidence per build discipline. The filter now keeps only
    skeleton lines: headings (`#`), bold-led (`**`), list items (`- `).
  - New `fired(skill_id=None, *, path=None)`: per-skill_id fire counts from the
    ledger; `int` for a single id, full `dict` otherwise.
- `tests/test_skill_fired.py` (new): filter actually filters (fixture with
  prose lines that must drop); N skills returned -> N fired rows (3 returned of
  4 configured: muted `pack_excerpt: false` never fires, ghost fires
  `missing/0`); `fired()` counts per id, stays 0 for never-fired, and ignores
  interleaved `decision.v1` + malformed rows.

## Real runs (instruments named)

- `pytest tests/test_skill_fired.py -q` -> `3 passed in 0.60s`.
- `pytest tests/test_skill_drop.py tests/test_skill_lifecycle.py tests/test_skill_seat.py tests/test_skill_fired.py -q`
  -> `28 passed, 4 warnings in 122.18s` (no sibling regressions).
- One real `skills_for_job('research')` (default 800 chars): pack built, 6
  receipts appended to `memory/improve/skill_ledger.jsonl`:

  | skill_id | pack_mode | chars_injected |
  |---|---|---|
  | feature-compose | excerpt | 134 |
  | memory-verkle | excerpt | 116 |
  | skill-ecosystem | excerpt | 104 |
  | salon | excerpt | 90 |
  | ractor-essay | excerpt | 97 |
  | corpus-harvest | excerpt | 99 |

  `frontier-hr` is routed under job `research` in `configs/skills.yaml` but has
  `pack_excerpt: false`, so it did not fire (0) - now a countable fact instead
  of ledger-return-16 folklore.

## Organs that close their loop

- Catalog (`docs/SKILLS_CATALOG.md`): gains a fired column from `fired()`.
- right_size: `missing`-mode rows and zero-fire ids are demotion grounds.
- Bare verbs (fold, flex): zero-fire skill ids become skill candidates.

Laws held: em-dash 0 in both landed files (grepped), counts above are the real
instrument outputs, no commit made.
