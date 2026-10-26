# FW-14 — ghost-ref noise audit: 50 DISPUTED hits eyeballed (2026-09-28)

## Instrument (exact, run this session)

- Census re-run first: `./.venv/Scripts/python.exe -m mag.prose_census` → `files=23663
  ghost_refs=2222 launchers=293` (was 3,269 on 09-17; delta = two weeks of churn + the
  FW-07/FW-10 `_REF_RE` fixes: mdx + jsonl alternation order, URL strip).
- Sampler: `watch/inbox/fifty_wide_20260917/FW14_sample50.py` — recomputes the census set
  with the fixed instrument, dedupes to (file, line, ref) hits = **6,812 across 1,192 files**,
  then takes a deterministic systematic sample: every 136th hit → **exactly 50**, each printed
  with its referencing line. Every one of the 50 read and classified by hand this session;
  twin checks run for the moved-pointer candidates (`ls`/`find` results quoted in the table).

## Verdict: regex-noise rate 45/50 = 90%

Only **5 of 50** sampled hits are genuine dead-path claims a reader could trip on.
**45/50 (90%)** are instrument artifacts of four kinds:

| Class | Hits | Share |
|---|---|---|
| ECHO — census files quoting their own/eacother's findings (the FW-08 self-reference loop) | 29 | 58% |
| CROSS-REPO — regex tails of paths in OTHER repos (hermes-agent, forge-memory), checked against this tree | 4 | 8% |
| HYPOTHETICAL/PROPOSAL — "create X", design specs, vision docs, negations ("did not write X") | 9 | 18% |
| NEGATION — explicit "never existed" / "did not write" disclaimers | 2 | 4% |
| TRANSIENT — points at a receipt this very wave lands (self-resolving) | 1 | 2% |
| EXPLAINED — genuine ghost inside a doc dispositioned this wave (FW-06 SUPERSEDED boards) | 2 (counted in the 45) | 4% |
| **TRUE-GHOST** — genuine stale pointers | **5** | **10%** |

## The 5 genuine ghosts (the real residue)

1. `watch/PARTICLE_FLUENCY_20260907.md:42` → `mag/salon_runner.py` — claims "already built";
   gone from `mag/` and `attic/` (checked). Stale.
2. `watch/octant_20260831/moiche.md:38` → `/mag/memory/runs/seat_corpus/latest.json` — live
   twin exists at `memory/runs/seat_corpus/latest.json` (old mag/ working-dir prefix).
3. `queue/handoff/openclaw/OUTBOX/ext-81e1903983.md:8` → `/mag/watch/hermes_wings/b1_docs/
   b1doc_14.md` — live twin at `watch/hermes_wings/b1_docs/b1doc_14.md` (same prefix strip).
4. `memory/runs/batch5_20260906/ARTIFACT_INTROSPECT_E.md:40` →
   `mag/watch/SESSION_SELF_STEAL_PLACEHOLDER.md` — no twin in `mag/`, `watch/`, or `attic/`.
5. `memory/runs/matthew480_20260913/hermes_out/lens_doc__attack_deepseek__deepseek-chat.md:22`
   → `memory/runs/hermes_jobs/reboot_test.json` — no such file (no hermes_jobs dir hit).

2 of the 5 are just the mag/-prefix strip (fixed map: FW09_mag_moves.md); the other 3 are
stale/never-landed pointers inside dated run artifacts — history, cheap to leave.

## Sample detail (50 rows, in draw order)

1. AGENTS.md:8 `docs/ZEITGEIST.md` — NEGATION (line itself says the path "never existed")
2. PARTICLE_FLUENCY:42 `mag/salon_runner.py` — TRUE-GHOST
3–31. PROSE_CENSUS_20260904..0928 (29 hits) — ECHO (FW-08 dispositioned)
32. TOPIC_INDEX_20260905:813 `docs/streaming-tts.md` — CROSS-REPO (hermes-agent doc)
33. _ALL_WINGS:705 `memory/honcho/client.py` — CROSS-REPO (tail of hermes-agent/plugins/…)
34. FIFTY_WIDE_BOARD_20260915:63 `memory/runs/fifty_wide/link_integrate.md` — EXPLAINED (FW-06)
35. SELF_STEAL_REBUILD_SALON:514 `…/FW11_fence_owners.md` — TRANSIENT (receipt landed this wave)
36. B2_186_uf122_eval:17 `dashboard/widget_config.yaml` — CROSS-REPO (hermes spec-path quote)
37. AFTERPARTY_QUEUE:26 `mag/ollama_maze.py` — HYPOTHETICAL ("worth building now?")
38. octant/moiche:38 `mag/memory/runs/seat_corpus/latest.json` — TRUE-GHOST (twin live)
39. LAYMAN_OFFICE_VISION:93 `memory/operator/dashboard_layout.json` — HYPOTHETICAL (vision doc)
40. ext-81e1903983:8 `mag/watch/hermes_wings/b1_docs/b1doc_14.md` — TRUE-GHOST (twin live)
41. alternative-hooks:23 `memory/cursor_preamble_latest.md` — HYPOTHETICAL ("Add a branch: write…")
42. STEAL_20260809T215934Z:46 `memory/patterns.md` — CROSS-REPO (tail of `forge-memory/patterns.md`)
43. plans/fifty_wide_20260915:74 `memory/runs/fifty_wide/maxdistill.md` — EXPLAINED (FW-06)
44. ARTIFACT_INTROSPECT_E:40 `mag/watch/SESSION_SELF_STEAL_PLACEHOLDER.md` — TRUE-GHOST
45. canon_configs__verifyb:24 `configs/canon_enforcement_map.yaml` — HYPOTHETICAL ("Create a new file")
46. lens_doc__attack_deepseek:22 `memory/runs/hermes_jobs/reboot_test.json` — TRUE-GHOST
47. smoke_harness__attacka:21 `mag/headless_render_fidelity.py` — HYPOTHETICAL ("Create … (new)")
48. M06_veto_clock:16 `mag/veto_clock.py` — HYPOTHETICAL (missing-organs design spec)
49. ASTRA_DESIGN_RAW:5703 `mag/ollama_maze.py` — HYPOTHETICAL (design paths list)
50. STEAL_EMERGENT_FIELD:5 `mag/game_recall.py` — NEGATION ("Did not write …")

## Caveats (named per the denominator law)

- Population instrument = per-(file,line) hits (6,812); the census headline (2,222) counts
  unique refs per file — different denominators, same scanner. Sample is systematic (step
  136) over the line-level population, not random.
- The 09-17 "3,269" and today's numbers are different moments AND different instruments (the
  regex was fixed in between); they are not differable, only trendable.
- 29/50 echo share is inflated BY the sampler's population containing 25 census files × their
  quoted lists; it measures the echo loop, not repo-wide path health. The 10% true-ghost rate
  on this sample says the DISPUTED queue is mostly self-measurement noise — consistent with
  the census's own "DISPUTED — regex noise possible" header.
