# SKILL REFORM: operator-corrections -> winning card shape - 2026-10-04 (night shift, free lane)

Task: reformat the estate skill `.agents/skills/operator-corrections/SKILL.md`
(403 lines, the census's top offender) into the winning skill-card shape stolen
from image-blast (receipt `watch/inbox/IMAGE_BLASTER_GO_20261003.md`). $0 spent,
no paid APIs, plain hyphens, nothing committed.

## Before

- `operator-corrections/SKILL.md`: 403 lines / 3,973 words / 29,263 bytes, one
  card carrying ~8 distinct verbs, zero argument-hints, zero runnable command
  blocks, zero run gates, zero "Final response:" lines, 37 em-dashes.
- Laws 21-66 (1,892 words) duplicated the shared file `LAWS_COMPILED_20261003.md`
  byte-for-byte in substance (the compiled file pre-dates this reform and holds
  every row with dates, restatements, and source paths).

## After - one main card + 8 sibling verb cards (single-SKILL.md-per-dir kept)

| Card (all under .agents/skills/) | Verb | Laws | Lines | Words |
|---|---|---|---|---|
| operator-corrections/SKILL.md | LOAD | 1-12 + map + distilled policy | 100 | 877 |
| corrections-design-cite/SKILL.md | CITE | 13 | 37 | 262 |
| corrections-handshake/SKILL.md | LOG + DRIVE | 14 | 39 | 291 |
| corrections-reserves/SKILL.md | VET | 15 | 41 | 315 |
| corrections-spawn-gate/SKILL.md | CHECK | 16+28+30 | 43 | 359 |
| corrections-charged/SKILL.md | HANDLE | 17 | 48 | 364 |
| corrections-research/SKILL.md | SWEEP | 18 | 38 | 282 |
| corrections-playbook/SKILL.md | MATCH | 19 | 42 | 292 |
| corrections-infinity/SKILL.md | MARK | 20 | 63 | 519 |

Family total: 451 lines / 3,561 words across 9 cards, every card under the
~100-line cap (max: main card at 100).

## What moved where (nothing binned)

- Laws 1-12 (core conduct) stay verbatim-substance in the main card - BOOT_4_7.md
  ("the 12 laws") and .github/copilot-instructions.md load this path and keep
  working; configs/skills.yaml id operator-corrections path unchanged.
- Laws 13-20 moved whole into the sibling cards, one verb each, law numbers kept
  in the H1 so external number citations still resolve (e.g.
  configs/riddler_charged_graphs.yaml cites "operator-corrections law 17").
  Law 16 shares corrections-spawn-gate with laws 28 + 30 because all three
  govern the same verb (spawn / never cancel / width posture).
- Laws 21-66 (1,892 words) were deduplicated OUT of the card family into the ONE
  shared file `LAWS_COMPILED_20261003.md` (128 lines / 3,079 words after a
  +10-line split amendment) - the hoist the winning shape requires. Verified:
  all 46 titles and full text pre-existed there before this change, so zero
  doctrine lost; the main card's map points to it instead of duplicating.
- Distilled identification policy + why-these-exist: main card tail (condensed,
  substance intact).
- Original 403-line bytes preserved at
  `operator-corrections/SKILL.md.bak-20261004a` (house .bak convention, cf.
  image-blast's .bak-20261003w).

## Rule compliance (the five stolen rules, verified by instrument)

- Argument surface: every card carries `argument-hint:` plus "if $0 missing, ask
  for X" text (main card defaults to load-all + lookup-from-file instead).
- One verb = one card = exactly one runnable bash block each (grep-counted 1 per
  card; commands verified against disk: `python -m mag.burn_steer` and
  `python -m mag.lane_runner --lane day_work --once` exist and run $0;
  `mag.riddler` compiles locally; `tools/hermes_burn.py`, handshakes.jsonl
  schema, SUBVERSION_CORPUS, FILTER_1301_SHADOW, BIBLIOGRAPHY_MAP,
  SELF_STEAL_MCP_TOPOLOGY receipt all exist).
- Explicit gates: design-cite (LAW-056 DISPUTED-at-census), handshake (minimal
  receipted drive), reserves (refill < 24h = WAIT), spawn-gate (>1 warm session
  = spawn nothing; TaskStop only after deadline), charged (1301 = fork never
  retry; riddler_transport SENDS = operator gate), research (pad-out cheap lane
  only), infinity (publish is one-way, markers BEFORE it leaves).
- "Final response:" line present on all 9 cards (grep-counted).
- Cap + hoist: all cards <= 100 lines; shared law hoisted to LAWS_COMPILED.
- Frontmatter name matches dir on all 9; descriptions rewritten to point at the
  new split; em-dash count across the family: 0 (old card had 37).

## Word-count honesty (the accounting)

Old card 3,973 words = laws 1-20 + distilled + why + the 1,892-word 21-66
duplication. New family 3,561 words = laws 1-12 + 13-20 + distilled + why +
card-map index + new gates/commands/Final-response contracts. Net -412 words on
the card family while ADDING structure, because the 1,892-word duplication moved
to the single shared home that already held it. Total doctrine on disk across
family + shared file: 3,561 + 3,079 = 6,640 words vs 3,973 + 2,997 (compiled
before amendment) = 6,970 before - the -330 delta is the removed duplication
minus the amendment and new card framing. No law lost; every one of the 66 has a
verified home (title-grep proof run this shift).

## Notes for the operator

- New sibling cards are NOT registered in configs/skills.yaml - image-blast
  precedent (the winning card itself is unregistered); harness discovery is the
  .agents/skills scan. Register them only if the brief pack should carry them.
- Pre-existing drift noticed, not touched: .github/copilot-instructions.md says
  "the operator's ten laws" (card has held 12+ since 2026-08-28).
- Side effect this shift: `python -m mag.riddler` with no args fired one local $0
  surrogate compile to stdout (verified the command; it takes no --help).

Final response: 9 cards on disk (1 reformed + 8 new siblings), shared file
amended, backup + this receipt filed; every card argument-hinted, one-verb,
gated where paid/irreversible, Final-response-lined, under cap; all 66 laws'
homes grep-verified; nothing committed.
