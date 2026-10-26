# R4 LAND: AGENTS.md load-order table edit (ouroboros R4-L3, move 4)

Moment: 2026-10-06T02:02Z (2026-10-05 22:02 EDT). Seat: R4-L3 small lane.
Source ask: `watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md` memory-amendment table row 4 (boot-order verdict: NOT still right).
Laws held: no git commit; no em/en dashes in any added byte; the `**Tests:**` census bullet (AGENTS.md line 29) and its neighborhood byte-untouched.

## What changed (move map)

| Move | Verdict | Where |
|---|---|---|
| (a) newest `state/*.md` by mtime row BEFORE zknot | DONE | new table row 0a, plus the boot-recap line reordered (state canon first, zknot second) |
| (b) zknot relabeled operator-intent recap (autonomous windows invisible by design, zknot.py:51-52) | DONE | boot-recap line + new table row 0b |
| (c) rib_boot row added | DONE | new table row 0c |

## Before (exact bytes, load-order surface)

Boot-recap line:

```markdown
**Boot recap first:** read `memory/zknot/LATEST.md` (last 3 real ZCode sessions: his prompts, pending todos, commits, receipts, plus the self-steal meter; rewritten at logon by `tools/zknot.py`). Red patrols: `state/REDBOARD.md`.
```

Table: rows 1 through 8 only (`docs/FRAMEWORK_LOAD.md` ... `AGENTS.md` ... `mag.cmd context-pack`). No state row, no zknot row, no rib_boot row. The live window canon (`state/NIGHT_LOOP_20261005.md`, mtime 2026-10-05 23:29Z per synthesis) sat in no row; zknot was ordered FIRST; the order served a human-morning estate.

## After (exact bytes, load-order surface)

Boot-recap line:

```markdown
**Boot recap (Load order rows 0a-0b):** read the newest `state/*.md` by mtime FIRST (live window canon; red patrols: `state/REDBOARD.md`), then `memory/zknot/LATEST.md` as the operator-intent recap (last 3 interactive ZCode sessions: his prompts, pending todos, commits, receipts, plus the self-steal meter; rewritten at logon by `tools/zknot.py`; autonomous windows invisible by design, `tools/zknot.py:51-52` excludes child sessions and under-5-prompt mains).
```

Table rows now open with (rows 1 through 8 unchanged below them):

```markdown
| 0a | newest `state/*.md` by mtime | Live window canon, before any recap: the estate runs around the clock, so the newest truth is what the current window is doing (e.g. `state/NIGHT_LOOP_20261005.md`); newest mtime outranks any fixed name, including `state/CURRENT.md` |
| 0b | `memory/zknot/LATEST.md` | Operator-intent recap, not live truth: his prompts, pending todos, commits, receipts, self-steal meter; autonomous windows invisible by design (`tools/zknot.py:51-52`: child sessions and under-5-prompt mains excluded) |
| 0c | `memory/rib_boot.json` (regen: `.venv\Scripts\python.exe -m mag.rib_boot`) | Rib vault boot block: law-head digest of `memory/rib/` plus brief and chain stamps; load rib law before building any mechanism (DRIVING LADDER: ribs, then state, then act) |
```

Design notes: 0-numbering keeps rows 1-8 byte-stable (minimal diff, no renumber churn). Row 0a explicitly says mtime outranks fixed names including `state/CURRENT.md`, which resolves the stale "Then: state/CURRENT.md (live truth...)" line without touching it (scope law). The zknot relabel lives in BOTH the recap line and row 0b so the label survives whichever surface a seat reads first.

## Verification (this seat's own runs, post-edit)

- Census patrol: `./.venv/Scripts/python.exe tools/census_drift_patrol.py` exit 0. Verdict line: `CENSUS-PATROL: ok - census 2026-10-04 (4358 collected / 518 files)` plus the growth note (24 files since census, inside the 7d window). No claim-shape fail-close: parse_carrier found the canonical grammar untouched.
- Citation lint: `./.venv/Scripts/python.exe tools/citation_lint.py check --files AGENTS.md` reports 3 blocking PHANTOM-NUMBER findings, all on line 29 (the Tests bullet). Byte-identical finding set (same 3, same line, same numbers) on a temp copy of `git show HEAD:AGENTS.md`: pre-existing debt, zero new findings from this edit; the edit added 2 anchors (`tools/zknot.py:51-52` twice), both resolve against real non-blank lines. The 3 pre-existing findings are the census bullet's own history narration, not this lane's to touch (CRITICAL LAW).
- Dash scan of every edited line: no em/en dashes added. The dashes the scanner flags in table rows 2-4 are pre-existing estate styling in rows this lane did not touch.
- Artifacts verified before citing: `memory/rib_boot.json` on disk (regenerated this window by the dwfrun executor lane), `mag/rib_boot.py` has a `__main__` entry (so the row's regen command is real), `tools/zknot.py` lines 51-52 are `CHILD_TYPES` and `MIN_PROMPTS = 5` (the invisibility-by-design evidence).
- mtime check at landing moment: newest `state/*.md` is `state/gstd_analysis_prompt.md`, then `state/REDBOARD.md`, then `state/NIGHT_LOOP_20261005.md`; the 0a rule (newest by mtime) handles the rotation without a fixed name, which is the point of the row.

## Residue

None blocking. The "Then:" line below the table still names `state/CURRENT.md` as "live truth"; row 0a now outranks it explicitly, and rewording that line was outside this lane's scope. The 3 pre-existing lint findings on line 29 belong to the census-bullet owner.
