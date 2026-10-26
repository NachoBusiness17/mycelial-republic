# SKILLS REDUNDANCY CENSUS (2026-09-29)

Question: "how many of them are the same thing in different jackets?" Method: pairwise Jaccard over name+description+body sample for all 205 installed SKILL.md files, plus name-dedupe and functional-family rollup. Instrument: inline venv python, one pass, reproducible.

## The funnel

- **205 installed slots** (19 house-repo, 14 house-user, ~14 zcode-user, ~158 vendor plugin cache)
- **148 distinct names** (57 slots are straight copies)
  - 15 names installed in more than one root (13 exact house-user <-> zcode-user duplicates: the whole cloudflare/workers pack, agents-sdk, sandbox-*, turnstile-spin, web-perf, wrangler; plus vendor version-stacked copies)
  - ~42 more slots are old plugin versions stacked in the cache (control-browser, web-gui-tester, docx/pdf/pptx/xlsx each shipped in 2-4 plugin versions)
- **71 of the 148 distinct names belong to 8 vendor functional families**:
  mapbox x18, togetherai x13, cloudflare/workers x13, github x10, zcode-guide x6, video-agent x5, office-docs (pdf/docx/pptx/xlsx) x4, browser-use x2
  (and within families the variants overlap heavily: auth-nodejs/auth-tool/auth-web/auth-wechat are four jackets for auth; control-browser vs web-gui-tester near-same)
- **77 true one-offs**, of which ~33 are house skills (19 repo + ~14 user-level)

## House semantic near-dupes (same function, different jackets)

1. **salon vs ractor-essay** — two multi-lens research pipelines born a week apart, same skeleton (fan perspectives -> grade -> fold -> file). Merge candidate: salon's 7 shapes become a lens-pack inside ractor-essay. This is the estate reinventing its own pattern, which is exactly what the ractor-essay self-feed exists to stop.
2. **memweave / mesh-comms / memlance / retrocausal-steering** — four jackets for context-steering (weave structures, aimed injection, seat-to-seat relay, future-seeding). Related but distinct enough to keep; document as one family.
3. **corpus-harvest vs code-agent-data** — both mining organs (corpus vs session-tapes). Keep; document as one family.
4. **sandbox-next vs sandbox-stable** — intentional two-lane variant (jaccard 0.54), like the estate's own lane discipline. Keep.

## Actions owed (cheap)

1. Pick one root for the 13 duplicated packs (migrate house-user -> repo .agents/skills for versioning, or delete from house-user).
2. Prune stale plugin versions from the cache (~40 slots of dead weight the harness still indexes).
3. Decide the salon/ractor-essay merge.
4. Fill /corpus-harvest's missing description.

Em-dash count: 0.
