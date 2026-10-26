# CITATION DEBT SWEEP — 2026-10-17

- class: RECEIPT
- writer: zcode-seat (deep-work lane)
- ask: clear the 341-entry citation prose-fix debt the 10-17 patrol named
- instrument: `tools/citation_lint.py` (unchanged), battery re-run after: 10 passed, 1 skipped

## Verdict

The debt was **not 341 unpaid prose fixes**. It was 341 fingerprints with no
file, line or rule attached — a ledger that could not be worked without being
re-derived. The sweep re-derived it and split it:

| bucket | count | meaning |
|---|---|---|
| still firing, now mapped | 287 | real outstanding claims, each now carrying `record:line rule anchor` |
| inert | 54 | the fingerprint does not reproduce anywhere in the estate under the current linter |
| repaired in this pass | 7 | fixed and verified clean (below) |
| newly mapped, re-fingerprinted | 8 | the patrol's same claims, re-fingerprinted after their detail changed; accepted by name with the mapping attached |

Baseline after the sweep: **318 live / 205 retired** (was 515 accepted, none
mapped). Retired entries keep their reason plus `retired_on` / `retired_why`;
nothing was deleted. The pre-push gate on the working tree:
`CITATION-LINT: ok records=57 anchors=166 numbers-checked=104 blocking=0 warns=114`.

The honest headline: the 341 were **mostly real**. What was missing was the map.

## Repairs landed (each verified with the stock linter)

1. `AGENTS.md` — six findings cleared, file now verifies `CITATION-LINT: ok`:
   - two `tools/zknot.py` cites at lines 51-52 re-anchored to lines 14-15,
     where the child-session / under-5-prompt selection actually lives;
   - the `mag/governor_autorun.py` cite at lines 1353-1357 re-anchored to lines
     1393-1397, the live `MAG_LIVE_REPORT_EVERY` regeneration call, and the
     "read at" cite moved from 992 (`topic_every`) to 1026 (`live_report_every`);
   - the 4,188 and 4,147 census figures now name the receipt that carries them,
     `watch/inbox/census_refresh_20261002.md`. The numbers were true; the
     attribution was missing.
2. `watch/inbox/hermes_burn/H247_STUDYA_ENTROPY_SPLIT_INSTRUMENT.md`: the
   `tools/consensus_harness.py` cite moved from line 262 to line 317, where
   `"answers": col` is stored.
3. `tools/zknot.py` plus 33 existing knots: the receipts-census heading read
   `(N under watch/inbox)`, so a file count looked like a content claim. The
   numbers engine exempts census facts only when a unit noun sits next to the
   number; the heading now reads `(N files under watch/inbox)`. This stops the
   class at the generator, not only in the knots already written.
4. `watch/inbox/gap_analysis_20261010/GAP_REGISTER.md` line 342: `14069 on disk`
   became `14069 chars on disk` (the number is a character count; the unit was
   missing).

## What the sweep found about the estate (the bigger number)

The gate scans changed records only. Linting every prose record that carries
either a cite anchor or a path mention — 3,716 records, tracked and untracked —
yields **23,855 standing findings**:

| rule | count |
|---|---|
| TOKEN-MISS (warn) | 8,559 |
| PHANTOM-NUMBER | 7,836 |
| UNRESOLVED-SOURCE | 2,783 |
| SHORTHAND-UNRESOLVED (warn) | 2,588 |
| PATH-MISSING | 1,117 |
| EMPTY-SPAN | 678 |
| LINE-OOB | 294 |

The accepted ledger was never the size of the debt; it was the size of the debt
that happened to be in the push path at the moment it was banked.

## Instrument findings (owed, each with a concrete case)

1. **Shorthand resolution glob-matches the wrong file.** `resolve_path` asks the
   git index for `*attention.md`, which returns `w4-attention.md`; a burn card
   citing `attention.md` at line 519 therefore files LINE-OOB against a 76-line
   file instead of an honest SHORTHAND-UNRESOLVED. 27 of the 31 LINE-OOB
   findings in `watch/inbox/ractor_engine/ractor-topic/break-communication.md`
   are this shape. Cut: require the index hit's basename to equal the cited
   basename.
2. **Census counts fire unless the unit noun is adjacent.** `(N receipt files
   under watch/inbox)` still fired; only `(N files under ...)` is exempt. The
   generator is fixed; the cut itself is one word wide.
3. **Hex commit prefixes parse as numbers.** `669703ede` at the head of a commit
   line in `memory/zknot/2026-10-05_sess_bb3c0189-1f99-40d4-bcd2-94561ed5c911.md`
   yields PHANTOM-NUMBER 669703. Cut proposal: a digit run followed by three or
   more non-unit letters is an identifier, not a quantity.
4. **Quoted commit subjects attribute files.** A knot quoting "atomic write for
   quick_report.json" makes that filename a named source for its own numbers
   (warn tier, `UNRESOLVED-SOURCE` 85676 and 3000 on `quick_report.json`).

## Method (reproducible) and the trap it exposed

Two candidate sets, because the two finding engines read different grammars:

- **anchor pass** — records whose text matches the linter's `ANCHOR_RE`
  (3,228 records): feeds `check_anchor` and `check_phantom_numbers`.
- **delta pass** — records with a path mention but no anchor (5,829 records):
  feeds `check_phantom_numbers` only. PHANTOM/UNRESOLVED need a path, never a
  colon-digit anchor.

Join to the baseline by fingerprint `sha1(rule|record|anchor|detail[:80])`, the
linter's own key. Speed patches (index loaded once, mtime-keyed source cache,
token-set containment) live in the sweep harness, never in the tool; every
repair is re-verified by the stock engine in-file.

The trap: an anchor-only candidate set called 66 of the retired entries inert
when they were live in path-mention-only records. Both passes are required; the
single-pass split was wrong and was corrected before this receipt.

Caveat: 66 census-shaped records (more than 200 named sources in one file) were
skipped in total — the stock engine is quadratic there and pinned the pass for
minutes. Those records may hold entries not yet mapped.

## Next moves

1. Work the 287 mapped live entries in batches by record. Most are the
   "number is true, attribution missing" class fixed in `AGENTS.md` today; a
   record-level batch is one sitting each.
2. Land instrument cuts 1 and 3 with fixtures in `tests/test_citation_lint.py`.
3. Decide whether the estate-wide 23,855 gets a standing sweep lane or stays
   gate-scoped; today the gate can only see what a seat happens to touch.
