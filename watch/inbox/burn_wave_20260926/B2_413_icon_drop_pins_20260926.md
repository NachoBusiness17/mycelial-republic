# B2-413 Pytest pins for the icon_drop escaping helpers (2026-09-26)

## Verdict

LANDED. tests/test_icon_drop_escape.py (NEW, 5 pins) gates the B2-377 escaping surface that was probe-verified only: (1) _ps_quote doubles embedded single quotes including the already-doubled case and the O'Brien's compound; (2) _cmd_echo_safe caret-prefixes ^ & | < > and doubles %; (3) _cmd_echo_safe collapses CR, LF, and CRLF to space-only output (no injected batch line); (4) _cmd_single_line collapses CR/LF while leaving % live (no %% doubling, so %VAR% still expands at click time); (5) the B2-354 silent-drop class end to end: drop_shortcut with a real target file whose PATH contains a single quote, quote-carrying args and desc, lands status "dropped" with the .lnk on disk and target/args/desc read back byte-equal through a real WScript.Shell. All 5 pass live (powershell present); the icon-drop suites stay green (14 passed across escape+fold+icon_thread). The helpers and drop_shortcut bytes are UNTOUCHED: this lane pins the fixed behavior, it does not change it. Two probe-harness corrections are disclosed in Work done: the CRLF pins assert the no-control-char invariant (the helper emits two spaces for a bare \r\n, so exact-spacing expectations were wrong pins, not a helper bug), and the round-trip pin must create the sandbox desktop dir (drop_shortcut does not mkdir; the fold suite's sandbox has the same shape).

## Evidence

- tests/test_icon_drop_escape.py (NEW): 5 tests as listed; sandbox pattern matches tests/test_icon_drop_fold.py (LEDGER, desktop_folder, skill_ledger.DECISIONS_PATH, training_events.EVENTS_PATH all monkeypatched to tmp_path)
- Run: pytest tests/test_icon_drop_escape.py -q => "5 passed"; regression pytest tests/test_icon_drop_escape.py tests/test_icon_drop_fold.py tests/test_icon_drop_icon_thread.py -q => "14 passed"
- mag/icon_drop.py:77-99 _ps_quote / _cmd_echo_safe / _cmd_single_line (read, unchanged; the comment blocks name the B2-377 cause and the B2-354 probe arms); :174-201 drop_shortcut assembly (read, unchanged; every literal via _ps_quote)
- watch/inbox/burn_wave_20260926/B2_377_unescape_probe.py:1-25 (the probe this lane converted to pins; arms A/B/C mapped to tests 5/2-4/1)
- The pre-pin gap, verified: tests/ carried no icon_drop escape module before this lane (the brief's 2026-09-26 grep; confirmed by ls tests/ | grep icon showing only fold and icon_thread)

## Work done

Mapped the three helpers and the drop_shortcut assembly, then wrote the five pins fixture-first against the CURRENT fixed behavior (the pins are the gate, not a behavior change: the helpers were already correct per B2-377). Iterated the pins to green with two self-caught corrections: (1) my first CRLF expectations asserted single-space collapsing, but the helper's real contract is CR/LF removal with space substitution per character - the invariant worth pinning is "no CR/LF survives", which is what a refactor could actually break; (2) the round-trip pin needed the sandbox desktop directory pre-created (drop_shortcut assumes the folder exists, as does the production desktop_folder path once Windows created it once). The WScript.Shell read-back runs a real powershell subprocess exactly like the B2-377 probe's arm A, with the same no-real-Desktop/no-real-ledger sandbox disclosures. An intermediate heredoc-escape mistake of mine produced control characters in the test file; the file was deleted and rewritten cleanly rather than patched in place (disclosed, no residue).

## Falsifier

The brief's own: revert drop_shortcut's assembly to raw interpolation f"('{target_path}')" (or delete the _ps_quote doubling) and `pytest tests/test_icon_drop_escape.py -q` must FAIL on test_ps_quote_doubles_embedded_single_quotes and test_drop_shortcut_quote_carrying_fields_round_trip; revert _cmd_echo_safe's caret/% handling and pins 2-3 fail; make _cmd_single_line double the % and pin 4 fails. If any of those refactors lands with the suite still green, the pins are vacuous and must be strengthened. The round-trip pin skips on hosts without powershell: on a no-powershell host the suite passing proves nothing about the wire, which the skip names.

## Bibliography closed

mag/icon_drop.py (read 77-215, unchanged); tests/test_icon_drop_escape.py (NEW); tests/test_icon_drop_fold.py (sandbox pattern source, read; run, unchanged); tests/test_icon_drop_icon_thread.py (run, unchanged); watch/inbox/burn_wave_20260926/B2_377_unescape_probe.py + B2_377_unescape_20260926.md + B2_354_falsifier_probe_results.json (named by the brief; probe read in full); watch/inbox/burn_wave_20260926/B2_353_shell_pin_20260926.md (the pattern; cited); QUEUE.md (row note); memory/burns/LEDGER.jsonl (appended); watch/inbox/burn_wave_20260926/B2_413_icon_drop_pins_20260926.md (this receipt).
