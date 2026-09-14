# RECEIPT: theme lexicon folded into the birth canvas data (2026-09-11)

*Slot 5 of 6, wave standing cycle. Source card: `watch/inbox/THEME_LEXICON_20260911.md`.
Target: `dashboard/static/index_data/verkle_birth.json`. The file lives ONLY there —
one copy, edited in place, constant name kept, so the birth canvas page
(`dashboard/static/verkle_construction.html`, which fetches `./index_data/verkle_birth.json`
with `cache: "no-store"`) needed no repointing.*

## What was added

One new top-level key, `theme_lexicon`, inserted directly after the existing chain-side
`themes` block. Everything else in the file is untouched (verified by spot-check after
reload: `days` cum 7,377, `facts.rows` 7,377, chain `themes` still 33 keys). The section holds:

1. **The full 63-value vocabulary with counts** — all 62 non-null themes + NULL from the
   lexicon card's full census, in first-appearance order, each with leaf count, first/last
   filename dates, and an `in_chain` boolean. NULL (12,147 leaves, 57.7%) carried with its
   gloss (the husks + uninterpreted commits).
2. **Sum-check guard, asserted at fold time**: 8,905 named-theme leaves + 12,147 NULL =
   21,052 leaves, 0 parse failures. The fold script refused to write on a bad sum (it didn't).
3. **The chain-vs-files delta** — 31 files-only themes (named in full), 1 chain-only theme
   (`mem_invariant_map`, with the rib_mem-invariant-map same-event note), the chain full
   vocabulary statement (32 + NULL full, 9 + NULL recurring), and the never-canonicalized
   warning (`rib_grokbot` vs `rib_grok-bot` — dedupe on normalized slugs or double-count).
4. **The 3 silence-only themes** (window 08-17 → 08-30): `rib_shader` (42),
   `backfill-explore-the-python-codebase-at-c-users` (1), `backfill-integrating-model-into-glm-4-6` (1),
   each with its note (chained ts 09-06 for the two backfills).
5. **The vector-length law** — `theme_vector_raw` length == `len(theme_basis)` of the SAME
   leaf, never a global axis: 8 (canonical basis, 19,586 leaves) and 4 (nine channel-specific
   bases, 1,463 leaves), ten bases total, all nine channel bases listed by name; the
   canonical-8 trap noted (it contains `dashboard` but NOT `autonomous_janitor`/`wow_manifest`);
   consequence spelled out: consumers key on `theme_basis`, never index.

Also inside the section: a `denominator_note` warning that the sibling chain-side `themes`
block counts CHAIN ROWS while `theme_lexicon` counts FILE LEAVES — different denominators,
never mix them — plus the 3 bare leaves (no theme machinery at all) and the population block.

## Sizes

| | bytes |
|---|---|
| Before | 14,475 |
| After | 25,760 |
| Grew | +11,285 |

## Validity check

`python json.load` on the written file: **PASS** (`JSON_VALID True`). Reload round-trip
confirms 14 top-level keys, 63 lexicon values, population 21,052, and the pre-existing
blocks (`days`, `families`, `themes`, `hours`, `facts`, `castle`, `eras`) intact.
The page's fetch path and filename are unchanged; the new key is purely additive and the
page ignores unknown keys. Pre-fold backup kept at
`dashboard/static/index_data/verkle_birth.json.pre_theme_lexicon.bak` (retire on next regen).

## Absorbed

- `watch/inbox/THEME_LEXICON_20260911.md` — the entire census (counts, delta, silence-only,
  vector law) now rides in the estate data, not just the card.
- No other copies of `verkle_birth.json` exist in the workspace (searched) — nothing to re-sync.

CYCLE GENETICS: the lexicon crossed from prose card to machine-readable estate in one slot,
sum-asserted before landing (8,905 + 12,147 = 21,052 or no write) — the next slot inherits a
validated 63-value vocabulary keyed on theme_basis-never-index, and one standing debt: any
theme visualization must slug-dedupe rib_grokbot/rib_grok-bot before it draws.
