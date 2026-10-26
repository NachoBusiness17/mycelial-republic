# B9 doors + tier (build-it-all wave, 2026-10-05)

Lane B9: two small ports from the day-4 mine cards. Files touched by this lane:
`.agents/skills/frontier-mine/SKILL.md` (append-only), `mag/gguf_cartography.py`,
`tests/test_gguf_cartography_backend_tier.py` (new), this receipt.

## Port 1: fetch-before-bank X-door recipe

- Landed as a dated section `## X-door recipe (2026-10-04 port: fetch-before-bank)`
  appended to `.agents/skills/frontier-mine/SKILL.md`. The skill dir carries no
  lens/doors.md (ls confirmed SKILL.md is its only file), so SKILL.md is the
  doors surface. 17 lines appended, append-only, no em/en dashes (grep-verified).
- Recipe banked from the steal card
  `watch/inbox/frontier_olm_2026-10-04/steal/open-and-local-language-models via x.md`,
  instrument lines at
  `watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md:15-35`:
  quoted-"x.com" phrasing (6 status IDs vs 0 from the dead site:x.com filter),
  2-3 queries per batch (4-wide hit two 1302 storms), snowflake dating
  ts_ms = (id >> 22) + 1288834974657, fxtwitter resolution (3/3), profile-level
  hits stay snippet-grade, and KILLs bank as first-class finds.

## Port 2: backend-tier census field

- `mag/gguf_cartography.py`: new `BACKEND_TIER = "GGUF"` constant (its comment
  carries the two-clause method-tier rule) plus a `backend_tier` field in the
  scan() out_doc, placed directly under `quant_file_type` so the tier rides
  next to the quant level. Mine card clause:
  `watch/inbox/frontier_olm_2026-10-04/steal/quantization-and-compression via arxiv.md`
  estate map step 2: one field recording backend tier (GGUF vs non-GGUF) makes
  clause 2 machine-checkable at census time instead of memory-resident.
- Test: `tests/test_gguf_cartography_backend_tier.py`, one test
  (`test_backend_tier_field_lands_on_census_row`) building a minimal synthetic
  GGUF v3 (Q4_K_M file_type metadata, one F16 tensor) proving `backend_tier`
  lands on the returned census doc AND the persisted census JSON, next to
  `quant_file_type = Q4_K_M`.

## OWED (held, not this lane's to write)

- Percolator candidate row carrying the two-clause rule: HELD. Another live
  workflow owns `memory/percolator/candidates.jsonl` writes this window (the
  mine card filed it the way rows 15/16 were filed; the promote gate owns that
  path per mag/percolator.py:23-27). Owed to that owner or the next window.
- The mine card's falsifiable probe (Q4_K_M vs q8_0 arm battery, 20 code
  prompts) was not fired by this lane.

## Gate numbers

- pytest: `./.venv/Scripts/python.exe -m pytest
  tests/test_gguf_cartography_backend_tier.py -q` -> 1 passed in 0.66s
  (2026-10-05, repo venv).
- Ratchet: `./.venv/Scripts/python.exe tools/violation_ratchet.py check
  --changed` -> PASS, scope=15 changed files, hits=10, registered=10, NEW=0,
  expired-exceptions=0. Pre-change baseline this session: scope=8, hits=2,
  registered=2, NEW=0; the scope growth is sibling wave landings on the moving
  tree, not this lane's edit (my files contributed zero new hits).
- No git commit (lane law). No em/en dashes in any file this lane wrote.

No em-dashes anywhere in this file.
