# RECEIPT: theme lexicon slug dedupe — standing debt cleared (2026-09-11)

Night rotation, slot after `watch/inbox/THEME_LEXICON_FOLDED_20260911.md`. The card's
standing debt — "any theme visualization must slug-dedupe rib_grokbot/rib_grok-bot before
it draws" — is now paid at the data layer, not left to every future consumer.

Target: `dashboard/static/index_data/verkle_birth.json`, `theme_lexicon` section only.
Backup kept at `dashboard/static/index_data/verkle_birth.json.pre_dedupe.bak`
(byte-identical to pre-edit state, verified with `cmp`).

## The merge

- `rib_grok-bot` (1 leaf, 2026-08-12, never chained) folded into canonical **`rib_grokbot`**
  → now **34 leaves**, first 2026-08-12, last 2026-09-02, `in_chain: true`, with an
  on-record `note` naming the dedupe, the source card, and the count arithmetic.
- `population`: `values_total` 63 → **62**, `non_null_values` 62 → **61**;
  sum-check re-asserted at write time: 8,905 named leaves + 12,147 NULL = 21,052 (totals
  unchanged — a merge moves counts between values, never out of the population).
- `delta`: `rib_grok-bot` removed from `files_only_themes`, `files_only_count` 31 → **30**;
  the `never_canonicalized` field now records the resolution (key kept, value rewritten to
  state canonical = rib_grokbot, 34 file leaves + 1 chain row, and that consumers should
  still dedupe on normalized slugs as defense-in-depth). Key rename considered; dropped —
  zero consumers read this section (verified: `verkle_construction.html` never references
  `theme_lexicon` at all; the only other workspace hit, `self_hologram_data.json`, already
  uses the canonical `rib_grokbot` spelling and has no `rib_grok-bot`).

## Separator-variant scan (the full-vocabulary sweep)

Two normalizations over all 63 pre-merge values, plus a cross-check against the chain-side
`themes` block:

1. **Unify separators** (`-` and `_` → same char): **zero** colliding pairs. No other slug
   in the lexicon differs from another purely by hyphen-vs-underscore choice.
2. **Strip separators** (separator deleted): exactly **one** group — the known
   `rib_grok-bot`/`rib_grokbot` pair. Nothing else.

**Flagged, not merged:** `mem_invariant_map` (chain-only) vs `rib_mem-invariant-map`
(files-only). Same event family per the lexicon's own `chain_only_note`, but they differ
by the `rib_` prefix, not a separator, and they live in different denominator blocks
(chain rows vs file leaves) — merging across blocks would violate the denominator law.
Relationship stays documented; both values stay.

## Validity check

- `python json.load` on the written file: **PASS**.
- 14 top-level keys, 62 lexicon values, no duplicate theme strings.
- Pre-existing blocks untouched: chain `themes` still 33 keys, `days` cum 7,377,
  `facts.rows` 7,377. Structural diff vs backup: **only `theme_lexicon` differs** (PASS).
- Size: 25,760 → 26,120 bytes (+360; the merge note and resolution text outweigh the
  removed entry).
- Prior backup `verkle_birth.json.pre_theme_lexicon.bak` still in place per its own
  receipt's retire-on-next-regen note; the new `.pre_dedupe.bak` retires on the next
  regen from source.

CYCLE GENETICS: the debt was "every visualizer must dedupe before drawing"; paid once in
the data, the debt is now inherited by nobody — the vocabulary ships pre-deduped, with the
scan method (unify-then-strip normalization) on record so the next lexicon fold runs it
before landing, not after.
