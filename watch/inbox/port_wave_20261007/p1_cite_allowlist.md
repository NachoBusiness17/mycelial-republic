# P1 CITE-ALLOWLIST: input-allowlist cite gate, landed (port wave 2026-10-07)

Lane P1 of the day-7 mine fold. Spec: watch/inbox/frontier_olm_2026-10-07/steal/evals-self-improvement via reddit.md, find 2 (r/LocalLLaMA thread on grounded generation: "any citation in the output that isn't in the input list fails the run"). The gap: tools/citation_lint.py and mag/cite_gate.py both verify cites against the whole repo, so a seat citing a sibling lane's file it never read passes both. This lane adds the missing input scope.

## Landed

- tools/cite_allowlist.py: the gate. `check_doc(doc, allowlist)` extracts directory-anchored path cites from a produced document and classifies each against the allowlist of source paths the producing seat was GIVEN: CITE-OUTSIDE-ALLOWLIST (resolves on disk, not in the allowlist; the sibling-file-it-never-read class, with a nearest-neighbor named for remediation) or PATH-MISSING (resolves nowhere). Exit contract 0/1/2; first-line law shape CITE-ALLOWLIST: ok / FAIL / ERROR. Allowlist format: one repo path per line, #comments allowed, a trailing slash or on-disk directory entry is a directory prefix; comparison is separator-, ROOT/-prefix-, and case-normalized. Cite grammar mirrors tools/citation_lint_io.py so both gates parse cites identically. Bare filenames stay mentions (cite_gate stance); URLs out of scope for this lane. Tightens, never replaces, the two existing gates.
- Integration point (one line, documented in the module docstring, no other lanes' files touched):
  `from tools.cite_allowlist import check_doc` then `ok = check_doc(doc_path, allowlist_path)["ok"]`
- CLI: `.venv\Scripts\python.exe tools\cite_allowlist.py check --doc <file> --allowlist <file> [--json]`
- tests/test_cite_allowlist.py: 13 tests, hermetic (ESTATE_ROOT monkeypatched to tmp_path). The three founding scenarios per the lane spec: allowlisted cites pass exit 0; a sibling file that exists on disk but is outside the allowlist trips CITE-OUTSIDE-ALLOWLIST; a nonexistent path trips PATH-MISSING. Extras: directory-prefix entries, on-disk dir expansion, line-anchor and prose-tail parsing, bare-filename mention stance, win32/case/ROOT/ normalization, nearest-neighbor naming, mixed-doc dedupe with per-class verdicts, CLI json + exit codes, empty-allowlist semantics.

## Gates (run this session, real numbers)

- pytest: tests/test_cite_allowlist.py reads 13 passed, zero failed (.venv\Scripts\python.exe -m pytest tests/test_cite_allowlist.py -q).
- Census instrument unchanged: pytest --collect-only -q with the pytest.ini default testpaths reads 4,924 tests collected in 13.9s, zero collection errors.
- Ratchet: direct scanner over tools/cite_allowlist.py reads zero violations; the full check --changed shows 4 NEW hits, all in sibling lanes' files (mag/contamination_tripwire.py and tools/code_execution.py, file-too-long and except-pass), none in this lane's files.
- Citation lint on this receipt: clean (run via check --files after filing).

## Falsifier and probe note

The steal card's falsifiable probe (banked, not run here): extract every cite from the banked steal cards, test membership in each card's own input material, count input-escapes that resolve repo-wide. This lane ships the instrument that probe needs; running the probe over the corpus is the next lane's move.

## Files

- tools/cite_allowlist.py (new)
- tests/test_cite_allowlist.py (new)
- watch/inbox/port_wave_20261007/p1_cite_allowlist.md (this receipt)

No git commit, per lane law. No em/en dashes in landed files.
