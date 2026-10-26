# B2-416 receipt (2026-09-26)

## Verdict

LANDED. The sweep counted every traceback body under watch/inbox, and the decision is registered as an explicit OUT-OF-SCOPE note in the crash_log_census docstring (mag/improve.py): stanza-less bodies are not owned by this census and stay out of scope by decision, with the census numbers and the named files carried in the docstring itself. The brief's falsifier is thereby closed for every stanza-less body on disk as of today.

## Evidence file:line quotes

- Sweep method: walk of watch/inbox, files over 8MB skipped, counting literal "Traceback (most recent call last):" headers and testing each file for the "[<iso-utc>] stage=" stanza regex.
- Census (2026-09-26, this lane): 7 files / 16 headers total. WITH stanza: 1 file / 6 headers (in scope, owned by the census). WITHOUT stanza: 6 files / 10 headers, split into QUOTED (3 files / 5 headers: QUEUE.md brief rows 3, B2_373_stanza_pin_20260926.md 1, B2_86_writer_isolation_20260926.md 1) and REAL captured output from other writers (3 files / 5 headers: gala_20260925/w1/lanes/b2-stone2b.check.txt 3, gala_20260925/afterparty/lanes/t33.check.txt 1, dogfood-trajectory save.txt 1).
- watch/inbox/gala_20260925/afterparty/lanes/t39.check.txt (the brief's named exemplar) holds ZERO traceback headers: grep for "Traceback" returns nothing; it carries 4 column-0 chain-marker sentences ("During handling of the above exception" family) and PermissionError lines in pytest E-line summary shape, e.g. line 76: `E           PermissionError: [WinError 5] Access is denied: '\\\\?\\C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\agents\\pytest-tmp-11820'`. So the brief's premise (a header present but stanza-less) is corrected by the bytes: this class has no header at all, which is a strictly worse visibility gap than the one the brief named.
- mag/improve.py crash_log_census docstring, after this lane's edit, new closing block: "B2-416 OUT-OF-SCOPE NOTE (2026-09-26): crash evidence that never passed through the _log_seat_crash writer seam is out of scope by decision... If a lane later wants these classes counted, that is a NEW writer or a NEW reader contract, not an edit here; this census stays stanza-scoped".
- mag/agent_cli.py _log_seat_crash is NOT modified: the decision taken is the out-of-scope registration, not a writer seam change (capturing pytest-report crash evidence in the seat guard would change product behavior far beyond this brief).

## Work done

1. Read the crash_log_census contract and the B2-373 stanza pin receipt before deciding.
2. Swept watch/inbox (file count, header count, stanza presence) and hand-classified the 6 stanza-less files into quoted vs real captured output.
3. Checked t39.check.txt byte-level and corrected the brief's premise: no header, 4 chain-marker sentences, pytest-summary shape.
4. Landed the out-of-scope note in the docstring with the full census, so the unowned class is registered by name; py_compile clean; tests/test_improve_crash_scout.py green standalone (17 passed, run three times).

## Falsifier

The brief's falsifier: "a stanza-less real traceback on disk that no receipt names as in-scope or out-of-scope". After this landing, every stanza-less body under watch/inbox at sweep time is named in the docstring block and this receipt, so the falsifier is empty for the swept population. It re-arms tomorrow: any NEW stanza-less traceback body landing in watch/inbox after 2026-09-26 is again unowned until a future sweep or writer change covers it; the docstring states the census stays stanza-scoped, so the standing risk is honest, not hidden. The docstring edit itself falsifies if tests/test_improve_crash_scout.py regresses (it pins the reader contract); it is green post-edit.

## Bibliography closed

- mag/improve.py crash_log_census docstring (698-764 region post-edit)
- mag/agent_cli.py _log_seat_crash (read, unmodified)
- watch/inbox/gala_20260925/afterparty/lanes/t39.check.txt (lines 76, 78, 202, 204, 237, 239, 363, 365; 4 chain markers)
- watch/inbox/gala_20260925/w1/lanes/b2-stone2b.check.txt; watch/inbox/gala_20260925/afterparty/lanes/t33.check.txt; watch/inbox/dogfood-trajectory save.txt
- watch/inbox/burn_wave_20260926/B2_373_stanza_pin_20260926.md; watch/inbox/burn_wave_20260926/B2_86_writer_isolation_20260926.md; QUEUE.md brief-row quotes
- watch/inbox/burn_wave_20260926/B2_384_real_chains_20260926.md (the self-feeder's Evidence)
- Observed, not owned here: 3 fixture ERRORs in tests/test_improve_crash_scout.py appeared only when it shared a pytest process with tests/test_seat_crash_guard.py under concurrent lane disk load (runs alternating 17 passed / 17 passed 3 errors / 20 passed on immediate rerun); standalone the suite is green every time. Same tmp-dir flake family as B2-288's findings; left for its own lane.
