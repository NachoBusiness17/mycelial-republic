# X6 - ORAL LAW WIRED INTO THE CONTEXT PATH (2026-09-29)

## Change
The deduped oral law (hydrology W3S, `watch/inbox/operator_model/ORAL_LAW_DEDUPED.jsonl`,
55 rows) is now a first-class skill on the research path:

1. **Registry** — `configs/skills.yaml` gains the entry:
   ```yaml
   - id: oral-law
     when: [research, always_soft]
     path: watch/inbox/operator_model/ORAL_LAW_DEDUPED.jsonl
     pack_excerpt: true
   ```
   and `job_to_skills.research` now lists `oral-law` FIRST so the laws land
   inside the 800-char pack budget before the markdown skills spend it.

2. **Loader** — `mag/skills_pack.py` `_law_tail(path, n=5)`: a `.jsonl` skill
   path excerpts as the TOP-5 laws by `birth_count` (tiebreak: file `rank`
   asc), one law per line `- <canonical> (birth_count=N)` — a 5-line tail,
   never the whole 55-row file. Rows marked `superseded` are skipped (dead
   law never ships into context; rank 26 carries a superseded note).
   Rationale: `_clip_file` keeps only `#`/`**`/`-` markdown skeleton lines
   and JSONL has none, so without this the wiring would pack an empty body.
   Malformed JSONL lines are skipped with the same tolerance `fired()` uses.

## Verification (bytes, not reports)
- Live probe: `skills_for_job('research')` (default `max_chars=800`) packs
  `### oral-law` with exactly 5 law lines — the two birth_count=3 laws
  (ranks 1-2) leading — plus feature-compose/memory-verkle behind it;
  `text.count('(birth_count=') == 5`; rank-55 tail law absent.
- `pytest tests/test_skill_fired.py -v` -> **5 passed in 0.67s**
  (3 pre-existing W3 tests + 2 new: hermetic top-5 test with SHUFFLED file
  order proving the sort, superseded birth_count=99 row excluded, exactly-5
  marker count, fired row `pack_mode=excerpt`; live wiring test on the real
  yaml + real jsonl with the ledger diverted to tmp).
- Neighbor suite unaffected: `pytest tests/test_skill_permissions.py -q` ->
  **8 passed in 0.88s**.
- Router/autorun consumers read `job_to_skills` as id strings only
  (`mag/router.py:538`, `mag/governor_autorun.py:118`) — additive-safe.
  `mag/context_pack.py:726` calls with `max_chars=600`: the tail starts at
  char ~167, so 4+ laws still fit at that budget.

## Boundary
No commit (per mission). One additive source file (`mag/skills_pack.py`) +
registry + test amendment; no behavior removed.
