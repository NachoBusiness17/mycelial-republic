# FW-08 — census self-refs: one lineage note, cited by all 13 old censuses (2026-09-28)

- Ask: the old PROSE_CENSUS 09-04→09-16 files' 13 dead docs/* paths → one lineage note cited
  by each.
- Mechanism verified first: `watch/PROSE_CENSUS_20260905.md:37` quotes
  `watch/PROSE_CENSUS_20260904.md — 32 dead: docs/UNIFIED_TRACING.md, ...` — each census
  quotes the previous censuses' dead lists, and those quoted strings re-trigger the scanner.
  The ghosts are the census reading its own output.
- Per-file dead docs/* sets recomputed this session with the FIXED instrument for all 13 files
  (20260904: 22 docs-dead incl. 8 spec-truncations; 20260905–07: 14; 20260908–13: 19 incl.
  8 spec-truncations; 20260914–15: 18; 20260916: 16 incl. 8 spec-truncations). The stable core
  across 09-05→09-15: CONSTITUTION, UNIFIED_TRACING, AGENCY_SHAPE, AGENT_ROADMAP,
  INTERCONNECT_v0, MILESTONES, ledger_update_proposal, about/contributing,
  benchmarks{.html,.md,-1106.html,-speed-1106.md}, config/adv-model-settings{.html,.md},
  ref/releases/RELEASE_NOTES_vN.md.
- Landed:
  1. `watch/inbox/fifty_wide_20260917/FW08_census_selfrefs_lineage.md` — the ONE lineage note:
     moved (CONSTITUTION → repo root; AGENT_ROADMAP → memory/ingest/local/docs/), deleted
     (UNIFIED_TRACING, AGENCY_SHAPE, INTERCONNECT_v0, MILESTONES, ledger_update_proposal —
     no copy in tree/attic/_archaeology_out), third-party (benchmarks*/adv-model-settings/
     contributing — OpenAI-docs-shape paths live only in mined `mine/raw/` trees),
     planned-placeholder (RELEASE_NOTES_vN — VERSION_REGISTRY.md:66 TBD row), truncation-noise
     (the docs/specification/* subset — FW-07).
  2. One appended `> FW-08 citation (2026-09-28): …` line in EACH of the 13 census files
     (20260904→20260916), pointing at the note; script printed "cited" 13/13. Append-only —
     no census file rewritten.
- Checks run: per-file recomputation (python, quoted in session), grep of the citation source
  lines, existence checks for every lineage claim (CONSTITUTION.md, AGENT_ROADMAP.md, attic,
  _archaeology_out, mine/raw hits, VERSION_REGISTRY.md:66, MAG_BEHAVIORAL_COMPOUNDING.md:124).
