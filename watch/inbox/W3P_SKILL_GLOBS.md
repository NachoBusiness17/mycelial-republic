# W3P — skill permission globs (advisory v0) — 2026-09-29

Mickey17 wave-3 lane (agent cd1474bb). Seed: S12 Kilo steal (MICKEY17_WAVE_LEDGER_20260929.md, agent ca7ff8d5) — modes carry ORDERED glob permission lists, LAST-match-wins (`deny-* allow-*.md`). Kilo's visibility axis (primary/subagent) intentionally NOT v0: this registry has no invoker concept yet.

## Landed (3 files, all additive)

- `mag/skills_pack.py` — `check(skill_id, path, mode) -> bool` + `DENY_PREFIX` + `_norm_perm_path`. Semantics: rules = ordered repo-relative globs under `permissions.<mode>`; a `deny-` prefix flips a glob to a deny; the LAST matching rule decides; no matching rule => REJECT. Matching is `fnmatch.fnmatchcase`: `*` crosses `/` at v0 (so `**` and bare `*` both span directories — documented, not gitignore semantics). Paths normalize: backslashes, leading `./`, ROOT-absolute -> repo-relative.
- `configs/skills.yaml` — optional `permissions` field documented in header (schema stays mag_skills.v1, additive), version bumped 2026-07-27 -> 2026-09-29. Five pilots: ractor-essay (read `["*"]`, write `["watch/inbox/**"]`), corpus-harvest (read `["corpus/**"]`, write `["watch/inbox/**"]`), show-me (read `["*"]`, write `["watch/inbox/**"]`), elder-lens (read `["watch/inbox/**","memory/**"]`), code-agent-data (read `["memory/**","watch/inbox/**"]`). Parse verified live: 34 skills, exactly 5 carry permissions.
- `tests/test_skill_permissions.py` — 8 tests: allow, deny, last-match-wins (both directions: allow-then-deny carves out, deny-then-allow reopens), fail-closed default (unknown skill / no permissions field / missing mode / empty-or-blank rules / no match), path normalization, real-config pilot behavior, and pilot field does not break `skills_for_job`.

## NOT ENFORCED anywhere — adoption is a separate law change

`check()` is a standalone helper. `skills_for_job` still packs excerpts without asking permissions; no effect broker, gate, or hook consults it. Wiring enforcement into any path is its own law change with its own receipt; until then these globs are declared intent + a proven contract, not a constraint.

## Tests (real counts, instrument + moment named)

- Own file: `pytest tests/test_skill_permissions.py -q` -> 8 passed (2026-09-29 ~23:00 EDT).
- With sibling: `tests/test_skill_fired.py` + own -> 11 passed.
- Full tree `pytest -q`, started ~23:04 EDT, finished 36:54 later: 2876 passed, 4 failed, 12 skipped, 3 errors (executed outcomes, not collected). The 4+3 are pre-existing on surfaces this lane does not own: test_healthz_status (server module has no `app` attr, sibling lane shape drift), test_census_drift_patrol (names sibling file tests/script_self_test.py as zero-collect), test_headless_law (bare-spawn baseline 22 -> 33, offender list contains none of this lane's files), test_invariant (memory preamble delimiter), test_stealth_driver_v2 (stealth ledger row state).

## Provenance note

This lane did NOT git commit (per lane order). The wave coordinator's day-close commit 0a15cd81d (2026-09-29 23:06:51 -0400, "Codex") swept this lane's working-tree files into HEAD while the full pytest run was still executing; working tree matches HEAD byte-for-byte on all three files. This receipt lands after that commit and is untracked working-tree truth.
