# B2-203 LEDGER one_line freshness convention (SW-07, 2026-09-26)

## Verdict

LANDED. Spec-first: the one_line freshness convention is written into memory/burns/MANIFEST.json protocol (ledger_one_line_freshness). Enforcement tool landed: tools/ledger_close_check.py re-checks every missing/owed assertion in a draft close line against disk bytes at write time (exit 1 = stale assertion). The tool catches the exact disease: run against LEDGER row 110 it exits 1 naming both stale receipt globs. The correction-row convention is landed with a real CORRECTION row appended for the B2-156 stale assertion; row 110 stays byte-untouched per the append-only law.

## Evidence file:line quotes

- The disease, memory/burns/LEDGER.jsonl:110: `"ts": "2026-09-26T13:41:16Z", "slug": "B2-156-living-hash-law", ... "owed: missing B2-41 receipt filed as B2-198."` -- written 11m23s after watch/inbox/index_events.jsonl:3089 (seq 1789823567015749402, 13:29:52.864Z) registered watch/inbox/burn_wave_20260926/B2_41_hash_freshness_20260926.md; the phantom spun lane B2-198 (watch/inbox/burn_wave_20260926/B2_198_owed_receipt_20260926.md Verdict: "DISCHARGED. The pointer was honest; nothing was fabricated-by-pointer").
- MANIFEST spec now carries: "ledger_one_line_freshness": "B2-203 2026-09-26: before appending a close row whose one_line asserts a path missing/owed, re-check existence on disk at write time via tools/ledger_close_check.py ... if a landed row is later proven stale, do NOT mutate it (append-only), append a CORRECTION row with verdict CORRECTION, slug '<original-slug>-correction', ...".
- Live probe of the checker on row 110: `"ok": false` with stale_assertions naming watch/inbox/burn_wave_20260926/B2_41_hash_freshness_20260926.md exists_on_disk true and watch/inbox/burn_wave_20260926/B2_198_owed_receipt_20260926.md exists_on_disk true, exit 1.
- Negative control (`--one-line "owed: missing B2-99999 receipt, no receipt on disk"`): ok true, exit 0 -- a genuinely missing receipt still closes green.

## Work done

- memory/burns/MANIFEST.json: protocol.ledger_one_line_freshness spec added (pre-close re-check rule + CORRECTION row shape + never-mutate rule).
- tools/ledger_close_check.py: path-token extractor (repo-relative paths), brief-id extractor (B2-<n> resolved through the watch/inbox receipt glob convention), missing/owed clause detector, stale-assertion verdict, --row/--line mode for auditing already-landed rows.
- Landing the convention with a real row: appended the first CORRECTION row (slug B2-156-living-hash-law-correction) naming the stale assertion, the discharge evidence (seq ...402), and the B2-198 receipt; row 110 untouched.

## Falsifier

Reopen if any of: (a) tools/ledger_close_check.py --row memory/burns/LEDGER.jsonl --line 110 exits 0 (the check stopped catching the disease it was built on); (b) a new LEDGER close asserts a missing/owed path that exists on disk and no CORRECTION row follows within the session; (c) the CORRECTION row appended here is found mutated instead of superseded. Residual limit named: the checker's clause splitter works on [;.]; a missing-assertion phrased inside a parenthetical that also carries no [;.], boundary may go unseen, the --row audit mode is the backstop.

## Bibliography closed

Read: memory/burns/LEDGER.jsonl (row 110 + tail), watch/inbox/burn_wave_20260926/B2_198_owed_receipt_20260926.md (full), memory/burns/MANIFEST.json (protocol block), watch/inbox/index_events.jsonl:3089 (quoted via B2-198 receipt), docs/DRIFT_BOARD_SPEC.md:34 (LEDGER key note). No external sources.
