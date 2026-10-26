# SEAT CAPABILITIES — research, skills, and primary evidence sources (2026-09-18)

*The surfacing pass: what the seat can search, what it can do, and where the
primary evidence lives — wired into the tool registry so any body (MCP client,
lane, dashboard) can consume it natively. Read-only throughout; bytes stay the
retrieval target.*

## 1. THE RESEARCH SURFACE (operational — tool calls, not greps)

New read-only tools in `tools/research.py`, registered in TOOL_MAP (31 tools)
+ mcp_server (archivist / historian / scout profiles):

- `research_search(query, source=all|links|packs|canon, limit)` — AND-term
  search across the canonical link ledger, the 107-pack research index, and
  20 canon lanes (22,390 primary files). Pointers + snippets only.
- `research_sources()` — the canon lane inventory with counts + samples.
- `research_stats()` — 245 links / 107 packs / 20 lanes / 22,390 files (measured).

Verified live: `research_search "go 1908" canon` → Smith's Game of Go 1908;
`"six-witness"` links → the operator's 09-14 drop; MCP stdio round-trip green
on the scout profile; 27/27 adjacent tests pass.

## 2. THE RESEARCH LANES (what the corpus holds)

Top canon lanes by file count (`research_sources()` for the full table):
shadertoy21k (21,809 GLSL seeds) · ractors (317) · mycology_canon (52) ·
game_design_docs (38) · training_pdfs (36) · esoteric_canon (8 PD texts incl.
Smith's Go 1908, Chesterton ×2, Carroll ×2, Kafka ×2, Falkener 1892) ·
ai_canon · electronics_canon · steering_canon · moonshot_canon ·
augmentation_canon · founding_law · substrate · tide_cards · shadow · lore ·
salons · zcode_history (the shadow-steal corpus).

Plus: `memory/lenses/corpus_index.json` (107 research packs, ask+answer
shaped), `watch/inbox/LINKS.jsonl` (245 canonical links, hash-anchored),
`memory/archaeology/` (prompt-leaks findings), 150 research-pack files.

## 3. PRIMARY EVIDENCE SOURCES (cite the file, not the summary)

- **Esoteric/PD canon**: `memory/corpus/esoteric_canon/*.txt` (8 texts, sha256'd
  at fetch — receipts in F4_ESOTERIC_CANON receipt)
- **AI canon**: `memory/corpus/ai_canon/` + `memory/archaeology/prompt_findings.jsonl`
- **Games**: `memory/corpus/game_design_docs/` + Steam corpus
  (`memory/game/steam_corpus.json`) + shadertoy21k (shader-as-environment seeds)
- **Physics/steals**: research_packs (150 files, 107 indexed) + LINKS.jsonl
- **Fleet primary (parables = T1)**: THE_SCALE_FINAL, Rashomon surface,
  Looking Glass transcript (`transcripts/LOOKING_GLASS_TRANSCRIPT_20260917.txt`)
- **Mycology**: `memory/corpus/mycology_canon/` (52 files — the compass's biology map)
- **Founding law**: `memory/corpus/founding_law/` + CONSTITUTION pointers

Standing law (2026-09-16, operator): parables/primary documents carry T1
standing — equal to physics papers. Cite primaries before deriving doctrine.

## 4. SKILLS (two layers)

**Fleet skills** (`.agents/skills/`, in-repo, house doctrine):
agent-harness · chan (lane-to-lane comms via /chan 8765) · code-agent-data ·
fireball-cycle · frontier-hr · frontier-researcher · light-operator ·
operator-corrections · salon (7-shape shape-train; "salon" intake Door B) ·
show-me · verb-genomes · zai-reference.

**Seat harness skills** (invocable via the Skill tool, beyond the fleet's):
browser control + web-gui testing · document suites (docx/pdf/pptx/xlsx) ·
github suite (repo/pr/issue/commit/workflows) · mapbox geospatial suite ·
android emulator + UI automation · workers/durable-objects/cloudflare ·
web-perf · skill-creator · video-agent-kit · imagegen · agents-sdk ·
mimosa security scan · web reader/fetch.

Usage laws that bind: skills serve the task; tri-state claims; T0/T1 local;
private material never rides remote lanes; receipts for anything filed.

## 5. HOW TO OPERATE (the one-paragraph runbook)

Need prior art or a canon text → `research_search`; need the raw file →
`corpus_get` the pointer it returns; need estate-wide file discovery →
`corpus_search`; need ledgers/telemetry → `corpus_tail`; need a verdict
session → salon intake (Door B) and the shapes; anything durable → watch/inbox
+ index_events registration; anything private → local only, forever.

---
*Receipts: registry 28→31 tools; compile + dispatch selftests + MCP roundtrip
+ 27/27 tests; queries quoted above were executed this pass.*
