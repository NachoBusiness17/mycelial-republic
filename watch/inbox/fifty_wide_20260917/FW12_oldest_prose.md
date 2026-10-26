# FW-12 — oldest prose top-25: structure-or-tombstone decisions (2026-09-28)

Decisions per file from the 2026-09-17 census "Oldest prose (top 25)" list. Ages are as-of
09-17; classification is from today's file heads + reader grep, not vibes.

## STRUCTURE — keep as data/corpus (24 files)

### `memory/ingest/local/docs/*` (17 of the 25)

MANIFESTO.md, doc-manifesto.md, doc-zeitgeist.md, DIAGNOSTIC_ZEITGEIST.md,
extra-0094e7ed7c76.md, STEINIGER_PAPERS.md, doc-steiniger-papers-map.md, AGENT_ROADMAP.md,
SKILL.md, CONSTITUTION.md, SCRUM.md, doc-scrum.md, README.md (+ the ingest-dir census block
they anchor). **Decision: STRUCTURE (ingested corpus — data, not the machine's voice).**
These are the old mag-disk / operator-persona docs ingested from the 2026-08 archaeology
(same basenames as FW-08's dead `docs/*` paths — the live originals moved to repo root or
`attic/`; these copies ARE the ingest record). The census's own SKIP_DIRS doctrine says mined
corpora are DATA, not a workqueue; `memory/ingest` is the same class but is not yet skipped.
**Recommended structural follow-up (operator call, not done here — it changes census scope):
add `ingest` to `mag/prose_census.py` SKIP_DIRS.** No file annotations made; tombstoning
ingested source material would falsify the archive.

### `memory/briefs/019f*.md` (7 of the 25: 019f7f37, 019f4d15, 019f4df4, 019f6569, 019f7582,
019f7780, 019f77fe, 019f847b, 019f858e, 019f8684 — 10 entries in the census list)

**Decision: STRUCTURE (historical biographer dossiers).** The briefs dir holds 3,979 dated
dossiers; the live-truth surface is `memory/briefs/latest.md`, which AGENTS.md already marks
FROZEN 2026-09-26 (not to be consumed as live). Old UUID dossiers are the biographer's
corpus — same data class as the ingest docs. Not tombstoned; not deleted.

### `memory/research_packs/20260720T155500Z_...answer.local.md` (1 of the 25)

**Decision: STRUCTURE (dated research-pack artifact).** Name carries its own timestamp;
content is a frozen Q&A answer with source URLs. Data.

## TOMBSTONE — mark dead (1 of the 25)

### `state/mag_brief.md`

**Decision: TOMBSTONED (done this session).** July-era mag-cycle status brief claiming
operational truth ("The system executed a 'mag cycle'… debugging focused on goal routing") —
stale live-claiming prose sitting in `state/`, which agents read as current. Preceded with a
TOMBSTONED header pointing at `state/CURRENT.md` (live truth) and `memory/briefs/`
(dossiers). Reader grep verified nothing in `mag/`, `scripts/`, `tools/`, or `main.py`
references the file, so the header cannot break a consumer. File content otherwise untouched
(append/prepend-only).

## Net

25/25 decided: 24 structure-keep (with the ingest-skip recommendation filed as the structural
fix), 1 tombstone landed (`state/mag_brief.md`). No deletions anywhere in this item.
