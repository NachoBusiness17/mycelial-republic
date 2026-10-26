# W2 receipt: receipt_xref_gate landed (2026-09-29)

Seat: zcode (GLM-5.3), MICKEY17 wave 2 lane, building the RETURN 14
improvement from `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md` (receipt
cross-refs ungated; skills_lint already owned the regex, pointed only at
SKILL.md). No git commit made; githooks untouched (arm proposed below).

## Files (owned by this lane, all new)

- `tools/receipt_xref_gate.py` (237 lines; the ledger guessed ~50, the real
  cost is the mask law + parse/CLI + docstring contract text)
- `tests/test_receipt_xref_gate.py` (219 lines, 16 tests)

Contract: backticked repo-relative paths (docs|watch|mag|tools|configs|
corpus|memory|state|scripts|tests|server prefix, the self-stolen
`tools/skills_lint.py:61` regex plus server/) must resolve on disk;
LINKS-N citations must name a row of `watch/inbox/LINKS.jsonl` (1-based,
trivially parseable shapes only); trailing :line[,line[-line]] anchors
resolve the base file; WARN-only default, `--strict` exit 1, exit 2
cannot-verify; `--summary` prints per-receipt dead counts; `--changed`
scans git diff vs HEAD for .md under watch/; all output passes mask()
(secret-looking runs become [REDACTED]); green first line opens
"RECEIPT-XREF: ok" (B2-338 lowercase case-arm convention).

## Real test line

`.venv/Scripts/python.exe -m pytest tests/test_receipt_xref_gate.py -q`
-> `16 passed in 3.27s` (final run, 2026-09-29).
Collect check: `pytest --collect-only -q tests/test_receipt_xref_gate.py`
-> `16 tests collected in 0.52s`. Ratchet: both new files land zero NEW
debt (`tools/violation_ratchet.py check --changed` NEW rows name other
lanes' files only: physical_compute_acquire.py, regen_front_door.py).

## Real run (the key finding)

`tools/receipt_xref_gate.py watch/inbox/game_platform_basecamp_20260929/*.md watch/inbox/MICKEY17_*`
-> `RECEIPT-XREF: DEAD-CITATIONS (WARN-ONLY) 6 dead citation(s) found`
over 24 receipts scanned (18 clean, 6 receipts carry exactly 1 dead each).

Instrument story (found by the gate's own first run): pass 1 read 21 dead;
12 were false-dead line-anchor citations (`tools/mickey17_v2_fold.py:101`
etc., base file live). Fixed at the design level (anchor-normalization
regex, pinned by `test_line_anchor_citation_resolves_base_file`), not by
papering over output. Final count 6. Triage of the 6:

| Citation | Verdict | Evidence |
|---|---|---|
| `server/protocol.json` (MICKEY17_RUN_PLAN) | TRULY DEAD | nothing on disk; RETURN 17's bones-shaped protocol table was proposed, never landed |
| `mag/wow_*` (LANES) | non-literal glob | expands to mag/wow_bones.py + 2 more, all live |
| `watch/inbox/**/*BRIEFS*.md` (W1_BRIEF_REAPER) | non-literal glob | only referent is game_platform_basecamp_20260929/FREE_LANE_BRIEFS.md at depth 2; the 10 FL briefs RETURN 15 counted are not at the cited top level |
| `memory/runs/gwap/<session_id>.jsonl` (B3_PAYLOAD_V0) | placeholder | session-template path, dead by construction |
| `server/world.py.validate` (W1_PROTOCOL_TABLE) | method-glue | base server/world.py exists |
| `corpus/library/.../RESEARCH_LOG.md:322-325` (V2_RUN_SPEC_ADDENDUM) | elided path | referent exists at corpus/library/interference-search/docs/RESEARCH_LOG.md |

Net: exactly ONE truly dead file citation in the wave's receipts
(server/protocol.json); the other 5 are citation-shape noise the literal
instrument correctly cannot resolve (and should keep flagging: a dispatch
loading the citation verbatim fails the same way the gate does).

## Proposed one-line pre-push arm (NOT landed; operator decision)

Append inside the census/freshness gate block of `githooks/pre-push`:

```sh
out=$(.venv/Scripts/python.exe tools/receipt_xref_gate.py --changed 2>&1); rc=$?; case "$out" in "RECEIPT-XREF: ok"*) : ;; *) echo "PUSH-GATE: receipt_xref (WARN-ONLY; exit 2 blocks)"; echo "$out"; [ "$rc" -eq 2 ] && exit 1 ;; esac
```

WARN-only for dead citations (t40 precedent, no lockouts without
operator); exit 2 cannot-verify blocks (B2-277 convention); flip the
dead-citation tail to `[ "$rc" -ne 0 ] && exit 1` only as an operator
call once the citation-shape noise is triaged down.

## Laws

- em-dash count 0 in all three files (`grep -c $'\u2014'` over
  tools/receipt_xref_gate.py tests/test_receipt_xref_gate.py
  watch/inbox/W2_RECEIPT_XREF_20260929.md -> 0/0/0).
- No bare-except, no except-pass, no shell-true, no env-key reads in the
  new tool (ratchet rules); repo root derived from __file__, never cwd.
- Counts above are byte-backed: test line pasted from the real run, dead
  citations from the real scan output.
