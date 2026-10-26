# B2-123 receipt: scout charter (2026-09-26)

## Verdict

LANDED. The free-resource scout now has a written spec on disk: watch/inbox/SCOUT_CHARTER_20260926.md, one page, three laws (writers, filing doors, dedupe law). The next patrol audits the scout against named doors instead of observed work. The charter registers only what bytes already prove: the add/check doors (mag/link_library.py), the event.v1 split (B2-28), and the duplicate_of law (B2-06/B2-27).

## Evidence file:line quotes

- watch/inbox/DIRECTIVE_WATCHERS_20260926.md:14: "| Free-resource scout cron (09:00) | 8 runs, last 9/25 09:00 |" the LEAD-watcher classification with no spec behind it.
- watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md:5: "`add` is the only sanctioned filing door, `check` the read-only pre-flight."
- watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md:13: "Scout has no driver: repo-wide grep for free-resource-scout in scripts/tools/mag/configs returns nothing ... DIRECTIVE_WATCHERS_20260926.md:14 classified it 'by observed work'."
- mag/link_library.py:21: "append-only law and are mirrored with provenance into watch/inbox/EVENTS.jsonl"; mag/link_library.py:147 `def check_url`, mag/link_library.py:245 `def add_urls` the two real door signatures.
- watch/inbox/burn_wave_20260926/QUEUE.md:190 (B2-28 row): "31 event rows ... cohabit watch/inbox/LINKS.jsonl with link rows; move them to their own event jsonl or add a schema field" landed, hence event.v1 rows live in EVENTS.jsonl.

## Work done

1. Wrote watch/inbox/SCOUT_CHARTER_20260926.md naming: writers (writer id free-resource-scout for link rows in LINKS.jsonl; event.v1 findings in EVENTS.jsonl per B2-28), filing doors (python -m mag.link_library add / add_urls for links, check_url pre-flight, EVENTS.jsonl event.v1 for findings), and the dedupe law (known canonical never re-filed with empty duplicate_of; re-confirmations are event rows, not link rows).
2. Every citation in the charter was verified against the current file bytes this lane (directives table line 14, B2-27 receipt lines 5/13, link_library module lines and function defs, B2-28 queue row).
3. No code touched: the charter is the spec the B2-27 gate already enforces; behavior owned by existing modules.

## Falsifier

The charter dies if: (a) the next scout fire files a link row through any path other than the add door (LINKS.jsonl grows a free-resource-scout row whose provenance is not mag.link_library), or (b) a known canonical gets re-filed with duplicate_of empty (B2-27's own falsifier (a)), or (c) a scout finding lands in LINKS.jsonl as an event row re-cohabiting the ledgers (the B2-28 disease returning). Audit is one grep of new LINKS rows per patrol.

## Bibliography closed

All read this lane: watch/inbox/DIRECTIVE_WATCHERS_20260926.md (line 14 table), watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md (full), watch/inbox/burn_wave_20260926/QUEUE.md rows B2-27/B2-28, mag/link_library.py (docstring law, EVENTS constant, check_url, add_urls), B2_06_link_dupes_20260926.md (cited via B2-27 line 11).
