# B2-122 known_canonicals last-writer-wins -> earliest filing

## Verdict

LANDED. known_canonicals now returns the EARLIEST filed row per canonical (first occurrence in file order of the append-only ledger), so check_url.first_entry and the add_urls duplicate_of stamp point at the original filing, not the newest dupe row. Pin test written first, red with the exact disease, green after the fix; full test file 31 passed.

## Evidence file:line quotes

- mag/link_library.py:116-117 (pre-fix): "def known_canonicals() -> dict[str, dict]:" / "    return {e[\"canonical\"]: e for e in load_ledger() if e.get(\"canonical\")}" — a dict comprehension keeps the LAST row per canonical.
- mag/link_library.py:121-123 (docstring, unchanged): "Submission-time duplicate gate (B2-27, 2026-09-26). ... canonicalize and answer whether the canonical is already on the ledger, carrying the first entry when it is." The docstring promised first; the code delivered last.
- mag/link_library.py:175 (add_urls): "if canon in known:" / "    entry[\"duplicate_of\"] = known[canon].get(\"url\", canon)" — the stamp inherits the same newest-row map.
- Red run: tests/test_link_library.py::test_known_canonicals_first_filing_wins FAILED, "AssertionError: assert 'first-writer' == 'dupe-writer'" (the map returned the second filing).
- Live bytes cross-check: watch/inbox/LINKS.jsonl still holds both thundercompute rows cited by the brief (seq 1789484000012 original, seq 1790422309734386 dupe-triage), append-only, untouched.

## Work done

- Fixture-first: added tests/test_link_library.py::test_known_canonicals_first_filing_wins pinning (1) first_entry carries the earliest row's writer and note, (2) a later add_urls filing stamps duplicate_of with the FIRST filing's raw url. Red pre-fix, green post-fix.
- Fixed mag/link_library.py known_canonicals to first-occurrence-wins with the cause and evidence named in the docstring per the fix-comment law (B2-122, seq numbers, live proof date).
- No other call sites needed changes: add_urls and check_url both consume the same map and their contracts now hold; the in-memory known[canon] update inside add_urls still lets a same-call second URL dedupe against the first.
- Verification: .venv/Scripts/python.exe -m pytest tests/test_link_library.py -q, 31 passed.

## Falsifier

The brief's falsifier was the live proof (check on thundercompute returning the dupe-triage row). Discharged structurally: the same lookup now cannot return a later row because the builder skips already-seen canonicals. Re-falsifier for the future: if a writer ever sorts or rewrites LINKS.jsonl out of append order, first-in-file stops meaning earliest; the pin test guards the map, and any reorder of the ledger would need a re-examination of this contract. Run tests/test_link_library.py::test_known_canonicals_first_filing_wins; red means the gate regressed to newest-row.

## Bibliography closed

- mag/link_library.py known_canonicals/check_url/add_urls (fixed + docstring)
- tests/test_link_library.py (new pin, 31 passed)
- watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md (the gate this lookup backs)
- watch/inbox/burn_wave_20260926/B2_06_link_dupes_20260926.md (the dupe clusters that motivated the gate)
- QUEUE.md B2-122 row; memory/burns/LEDGER.jsonl
