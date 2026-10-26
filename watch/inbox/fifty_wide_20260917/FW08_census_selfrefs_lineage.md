# FW-08 lineage note — the old PROSE_CENSUS files' dead `docs/*` paths (2026-09-28)

One note, cited by each census file `watch/PROSE_CENSUS_20260904.md` → `watch/PROSE_CENSUS_20260916.md`
(appended citation line landed in all 13 by this item).

## Why the census files carry ghosts at all

Each census quotes the dead-path lists it found (top-ghost section). Those quoted strings are
repo-path-shaped text inside a `.md` file, so every LATER census scan re-counts them as refs of
the census file itself. The ghosts are the census quoting its own findings — a self-referential
echo, not fresh breakage. Verified 2026-09-28: e.g. `watch/PROSE_CENSUS_20260905.md:37` quotes
`watch/PROSE_CENSUS_20260904.md — 32 dead: docs/UNIFIED_TRACING.md, ...`.

## Lineage of the docs/* paths in that echo (verified against the current tree)

| Path (as quoted) | Fate (checked 2026-09-28) |
|---|---|
| `docs/CONSTITUTION.md` | MOVED → repo-root `CONSTITUTION.md` (exists) |
| `docs/AGENT_ROADMAP.md` | MOVED → `memory/ingest/local/docs/AGENT_ROADMAP.md` (exists) |
| `docs/UNIFIED_TRACING.md` | DELETED — no live copy in tree, `attic/`, or `_archaeology_out/` |
| `docs/AGENCY_SHAPE.md` | DELETED — same |
| `docs/INTERCONNECT_v0.md` | DELETED — same |
| `docs/MILESTONES.md` | DELETED — same |
| `docs/ledger_update_proposal.md` | DELETED — same |
| `docs/benchmarks.html` / `.md` / `-1106.html` / `-speed-1106.md` | THIRD-PARTY docs paths (OpenAI-help-docs shape), never files of this repo's current tree; live only inside mined third-party trees under `mine/raw/` — quoted into the echo, not broken repo links |
| `docs/about/contributing.md` | same class (third-party; live copies exist only in `mine/raw/agent_bleeding_edge/AgentOps-AI/...` and `mine/raw/agent_platform/jj-vcs/...`) |
| `docs/config/adv-model-settings.html` / `.md` | same class (third-party; live in `mine/raw/agent_platform/Aider-AI/aider/website/docs/config/adv-model-settings.md`) |
| `docs/ref/releases/RELEASE_NOTES_vN.md` | PLANNED PLACEHOLDER — `vN` is a literal version placeholder; `docs/ref/releases/VERSION_REGISTRY.md:66` lists it TBD and `docs/ref/MAG_BEHAVIORAL_COMPOUNDING.md:124` assigns it as future deliverable. Not-yet-created, not lost |
| `docs/specification/2026-07-28/*.md` (the `09-08`→`09-16` files) | FW-07 TRUNCATION NOISE — these are `index.mdx`-style MCP mirror refs quoted from `docs/mirrors/mcp/INDEX.md`; the census regex truncated `.mdx`→`.md` (fixed 2026-09-28, `mag/prose_census.py` `_REF_RE`) |

## Disposition

Census files are dated instrument snapshots; per the never-rewrite law for receipts, the files
keep their quoted text. The echo dies on its own: with the 2026-09-28 `_REF_RE` fixes
(mdx/jsonl ordering, URL strip) plus this note being the cited explanation, fresh censuses no
longer regenerate the spec-truncation half, and the remainder is explained data, not open debt.
No census file was rewritten; each carries one appended citation line pointing here.
