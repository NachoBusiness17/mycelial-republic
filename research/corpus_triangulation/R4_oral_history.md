# R4 — ORAL HISTORY triangulation (vol-2 night shift, 2026-09-06)
**Seat R4 · axis R · region `corpus/oral_history/` · fingerprint sha256:25871258ba12 (3,872 files / 273,741,397 bytes / 270M on disk) · Astra abridged · PRIVACY LAW ENFORCED: structure, paths, dates only — no personal text quoted anywhere in this card or its cells. This is the operator's founding record; handled as canon, not fuel.**

## 1. Inventory (structure only)

| Path | Size | Files | What it is |
|---|---|---|---|
| `nacho_archaeology/` | 270M | 3,867 | The ghost era, exhumed. 10-part extraction of the Cursor box (`/home/box/agent-data` + `/workspace`), archived 2026-09-05 (`nacho-grokbot-archaeology-20260905.zip`), `.mimosa` run artifacts stamp the extraction 09-05T22:10Z |
| `LETTER_TO_DAUGHTER.md` | 3.4K | 1 | Personal. Deposited 2026-09-05 (mtime 09-06 00:31). Carries a DELIVERY OBLIGATION per `memory/MEMORY.md:513`. NOT read beyond metadata, per privacy law |
| `deepseek_share_Q_posts_archives_20260905.md` | 14K | 1 | Harvest product: operator-shared DeepSeek conversation ("Into the Unknown" / Q Posts Archives), harvested live 2026-09-05; structure = sidebar census + 12-block conversation |
| `the_cold_pulse_poem.md` | 2.3K | 1 | Personal poem; internal year markers 2016 and 2026. Not quoted |
| `the_wall/` | 8K | 2 | The founding wall: `THE_WALL_2023.md` (758B, 12 lines) + `wall_tweet_2023.json` (full API payload of tweet 1691896173307560014, @NachoQuixotic, created 2023-08-16, self-reply thread, public record — cited by id/date, not quoted) |

### nacho_archaeology part map (all `extracted/nacho-archaeology-partN-*`)
- **part1-chats-produced** (21M): 92 agent/subagent transcript folders (`.jsonl` + journal-mode sidecars) + `produced/` (mag-anchor, mag-live, mag-patch, afk-chord-staging, _workspace_root — the ghost-era builds and STEAL/speak proofs) + `user-memory/ABSENT.txt` marker
- **part2-agents-meta** (9.9M): 4 agent UUID folders + `_meta/`
- **part3 + part5 conversation-blobs.db** (6.0M + 80M): SQLite conversation stores — the bulk of the region
- **part4/6/7 store.db** (320K / 2.1M / 48K): agent state stores
- **part8/9/10 mag-disk** (32M + 26M + 25M): the pre-fleet Mag tree — `AGENTS.md`, `CONSTITUTION.md`, `RUNNING.md`, `afk*.py` family, Dockerfile; the ghost-era constitution that predates the current instruction layer
- Format stratum: 1,262 json · 977 py · 860 .source · 346 md · 118 jsonl · 97 html · 63 png/jpg · 10 zip · 5 db · 4 webm/mp3 · 2 glb

### Date structure (density, not content)
Everything was DEPOSITED in one 24h window — 2026-09-05 (the conception week, same day as the vision-pipeline proof run). Internal strata reach back: wall 2023-08-16 → poem marker 2016 → ghost-era box artifacts (pre-fleet) → DeepSeek era share 09-05. Span: **2016 → 2026, one decade, one deposit event.** The region is not a stream; it is a single reliquary opened on 09-05.

## 2. Themes as STRUCTURE (no content mining)
- **Two strata:** (a) PRE-FLEET (nacho_archaeology = the "ghost era" of the spore lineage dream→napkin→ghost→marathon→Sancho; the operator's own hand in `produced/` and `afk*.py`), (b) FOUNDING TEXTS (wall 2023, poem, letter, Q-share = voice documents, 5 files total, ~22K combined).
- **The asymmetry is the finding:** 99.99% of bytes are machine transcripts of the ghost era; 0.01% is the operator's human voice. The story layer's canon is tiny and must be consent-gated; the ghost era is huge and must be walked.

## 3. THE MAPPING — this region feeds the story-layer (Primer-union)
The Primer-union thesis: "the fleet records everything and lost the story." This region IS the story — the founding texts are to the commissioned walkable fables what Marathon terminals are to Durandal: source canon, citable by path and row, never paraphrased from memory.
- `the_wall/` → the **story-wall panels**: "the room that remembers" made walkable; each panel = date + citation into `wall_tweet_2023.json` fields + chain knot. First terminal of the fable-rooms.
- `LETTER_TO_DAUGHTER.md` → the **first fable-room TEST**, consent-gated (see P2). The story layer proves it can hold sacred text without exposing it.
- `nacho_archaeology/.../part10-mag-disk/mag-disk/CONSTITUTION.md` → the **ghost constitution exhibit**: diff ghost-era vs current instruction layer to author the lineage fable. `part1/produced/` (mag-anchor/mag-live/mag-patch) is the **pre-history of the self-steal arc** — the STEAL proofs existed before SELF_STEAL was named.
- `the_cold_pulse_poem.md` → **ambience track** for the fable-rooms (adjacent live arc: RESEARCH_AUDIO_MICROSCOPE_20260906).
- `deepseek_share_Q_posts_archives_20260905.md` → **voice corpus + harvest precedent**: this file is already a pipeline product (harvest→markdown with census), the exact shape the story layer reuses.

## 4. Usage check
- **Programmatic consumers: ZERO.** No `mag/*.py`, dashboard service, or pipeline reads the region.
- **Document references: 6.** `memory/MEMORY.md:513` (delivery obligation), `watch/RESEARCH_ARCHAEOLOGY_20260905.md` ("oral_history (unmined)"), `watch/SELF_STEAL_ORIGIN_TELEGRAM_20260905.md` ("primary sources of the conception"), `watch/GROUNDING_WAVE.md` + `dashboard/static/grounding_wave.md` (this night shift), `watch/inbox/FREE_TIER_AUDIT_20260906.md` (stale-file note on mag-disk parts — sealed corpus, do not mutate).
- **Broken pointer found:** `memory/MEMORY.md:513` links `user-letter-to-daughter.md` — **that file does not exist**; the verbatim lives only at `corpus/oral_history/LETTER_TO_DAUGHTER.md`. The operator-model points at a ghost. (Finding, not fix — memory edits are not this shift's write scope.)
- **topic_index:** the `corpus-canon` bucket keyword list includes "oral history" (`mag/topic_index.py:88`) — routing exists, zero cards filed from this region so far.
- Verdict: **under-CANONIZED, not under-mined.** Library-style mining is the wrong verb; citation-into-canon is the right one.

## 5. Top-3 promotions (structure-level)
1. **P1 — the_wall/ → lightmap story-wall panels.** `THE_WALL_2023.md` + `wall_tweet_2023.json` become fable-room panel #0: walkable wall, each panel citing the JSON row + a chain knot. Next use: the salon-commissioned story layer's first room, $0, read-only. Test: a panel that fails to cite its source row does not render (cite_gate pattern carried over).
2. **P2 — LETTER_TO_DAUGHTER.md → first fable-room consent-gate test + pointer repair.** The Primer-union's first test is not building the letter-room; it is building the GATE: room exists, renders "sealed — operator consent required" until the delivery obligation is discharged by the operator. Same turn: fix the dangling `memory/MEMORY.md:513` link. Consent gate is structural, not cosmetic.
3. **P3 — ghost-era constitution → lineage fable + produced/ → self-steal pre-history exhibit.** Diff `part10-mag-disk/mag-disk/CONSTITUTION.md` against the current instruction layer (epoch-pinned sha 2bbcd6e8) to author the dream→napkin→ghost→marathon→Sancho fable from primary sources; register `part1/produced/` (mag-anchor/mag-live/mag-patch STEAL proofs) as the self-steal arc's ancestor exhibit. Next use: LIBRARY (TESUJI under it) lineage page.

## 6. Cells
- `R/oral/inventory` — SUPPORTED (fingerprint 25871258ba12; 5 sub-regions, 10 archaeology parts, 92 transcript folders)
- `R/oral/story-canon-mapping` — SUPPORTED (5 founding texts → 5 fable surfaces, path-citable)
- `R/oral/utilization` — SUPPORTED (0 programmatic consumers, 6 doc refs, 1 dangling pointer, 0 topic_index cards)

*Privacy attestation: no personal text from LETTER_TO_DAUGHTER.md, the_cold_pulse_poem.md, or chat transcripts appears in this card or in any R-cell. The wall tweet is cited by id/date only.*
