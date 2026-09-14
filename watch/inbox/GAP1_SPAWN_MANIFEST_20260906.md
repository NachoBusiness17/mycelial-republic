# GAP-1 CLOSURE — spawn manifest + pointer repair (2026-09-06, builder spawnman)

Astra's chain, gap 1: **"the archive cannot reliably supply its own precedents."**
Smallest build per the verdict: repair pointers + enforce a spawn manifest recording
consumed sources. Both organs landed. $0, no network, no daemons, additive only —
`memory/MEMORY.md` is SEALED and byte-untouched (sha `bd118c63…` before == after).

## Organ 1 — `mag/spawn_manifest.py` (the consumed-sources law)

```bash
python -m mag.spawn_manifest record --sources file1,file2 --session <id> [--note text]
# appends {ts, session, sources[], note} to memory/runs/spawn_manifest.jsonl (append-only)

python -m mag.spawn_manifest check --brief <path>
# anti-phantom check: extracts every file ref (slash paths + bare known-ext filenames),
# resolves literal-root → literal-briefdir → literal-memory → basename walk (memory/ first,
# then repo; .git/mine/seals + per-session state dumps pruned from basename walk only),
# prints resolved + PHANTOMS list. Exit 0 all-resolve, exit 1 phantoms.

python -m mag.spawn_manifest resolve
# regenerates memory/MEMORY_resolved.md deterministically (organ 2 below)
```

**Falsifier this makes testable** ("fresh seat misses the August brief"): a fresh seat's
manifest either CONTAINS the brief or PROVABLY never saw it. Ledger row #1 is this
build's own dogfood: session `spawnman-gap1-20260906`, 5 sources (astra ANSWER.md,
memory_orphans.md, sealed MEMORY.md, the 08-08 brief, SELF_STEAL_ORPHANS).

## The demo receipt — the 08-08 brief checked by the organ it predicted

`check --brief memory/research_packs/20260808T153000Z_session-maze-handoff-fresh-agent-research-project.md`
→ **13 file refs, 11 resolve, 2 PHANTOMS**: `tools/maze_probe.py` + `memory/runs/maze_probe/*`
— the founding experiment's probe, spec'd in the brief, never built. **Orphan #2
("maze_probe never created, RQ1–RQ5 never measured") is now machine-confirmed by an
organ, not a reading.** The brief's resolvable spine (state/CURRENT.md,
agent_state/LATEST.json, tools/tier_probe.py, dashboard/rest.py, both companion packs)
resolves clean; `memory/graph/nodes.jsonl` resolves only via basename to
`memory/ideas/nodes.jsonl` (another moved-without-repointing).

## Organ 2 — `memory/MEMORY_resolved.md` (pointer repair, additive)

Generated resolved index of the sealed `memory/MEMORY.md` (never edited; generator =
`resolve` subcommand, deterministic, re-runnable):

- **RESOLVED: 31 of 467 link rows (31 unique targets)** — all via codex_seat fold
  basenames, matching memreg's independent 30-of-396 measurement.
- **PHANTOMS: 436 rows / 416 unique targets (92.7%)** — cross-validates memreg's
  92% headline with a second method. Footer keeps them as forensic evidence
  ("rooms never built, or moved without re-pointing"), not garbage.

Known payload remap (NOT fixed here — needs the sealed-file decision, operator-gated):
`user-letter-to-daughter.md` (MEMORY.md:L570/L573, 2 phantom rows) has its payload safe
at `corpus/oral_history/LETTER_TO_DAUGHTER.md` under a different basename — basename
resolution cannot and should not guess that jump.

## Verify receipts

- `python -m py_compile mag/spawn_manifest.py` → clean.
- check demo above → 11/13, phantoms listed, exit 1 (honest fail-safe).
- `resolve` → 31/467 resolved, 436 phantom (counts in file header).
- `python -m mag.tesuji_map verify` → **PASS 298 cells**, tip `d514226143a2`;
  cells `R/gap1/spawn-manifest` + `R/gap1/pointer-repair`, verdicts SUPPORTED, seat `spawnman`.

## Residuals (tri-state)

- SUPPORTED: manifest law works; phantom check is deterministic ($0, ~14s run).
- UNPROVEN: adoption — the organ gates nothing yet; it becomes law when spawn
  prompts/dispatch templates require a `record` row (next smallest build).
- OPEN: the 416 phantom targets await the memreg promotion path (index-only rows →
  materialize or formally retire); that is an operator-classification pass, not a build.

---

One builds, one verifies: Astra's chain named the gap, memreg measured it, this seat
built the two organs and verified on the brief that started it. Re-run anything:
`python -m mag.spawn_manifest --help`.
