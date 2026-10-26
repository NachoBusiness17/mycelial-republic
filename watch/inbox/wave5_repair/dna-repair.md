# dna-repair receipt (gala wave5, division B)

Date: 2026-09-29. Lane: dna-repair. Ownership honored: only `docs/DNA.md` edited (plus this receipt and the lane/check artifacts under `watch/inbox/gala_20260925/wave5-repair/lanes/`).

## Owed work (from the ask + start-from files corpus-01.md / s2-13.md)

1. Complete the truncated last line (ended mid-word: "Skip forever-keeping every P").
2. Correct the `session_end_hook` claim to the real close path with file:line.
3. Pointer the two orphaned commitment ids to their stores or mark them retired.

All three done. Finish line met: the doc reads clean end to end (byte-checked tail), all 32 path claims resolve on disk, and the git diff shows content edits only with history untouched.

## Premise audit (one nuance found, recorded not papered over)

The ask said `session_end_hook` "does not exist anywhere in live code". Half true:

- The endpoint file `watch/session_end_hook.py` EXISTS and is git-tracked. It is the old Grok SessionEnd hook, importing `summarize_session` at watch/session_end_hook.py:17. The start-from fact-checks missed it because their greps scoped to mag/ dashboard/ configs/ scripts/ and skipped watch/.
- Nothing wires it: harness config `C:/Users/foste/.zcode/cli/config.json` wires PreToolUse (1) + PostToolUse (2) and `SessionEnd wired: False`; `.claude/settings.json` carries only `env`; no tracked config-type file (json/toml/yaml/cmd/ps1/bat/cfg/ini) wires it, and `watch/grok_hook.py:127` references it only in a comment.
- The real close path verified first-hand: `mag/daemon.py:87` `run_cycle()` calls `_maybe_summarize_ended_sessions()` (def mag/daemon.py:27); on session switch it calls `summarize_session(prev, use_llm=True, force=False, amend=True)` at `mag/daemon.py:44`, logged as phase `session_end_summary_fallback`. `mag/daemon.py` is clean vs HEAD; line 44 re-verified twice. Manual CLI: `summarize-session` registered main.py:238, dispatched main.py:2287.

So the correction follows the ask (daemon poll is the live close path) and the trigger note in the doc records the endpoint's unwired survival.

## Orphaned commitments

Store sweep (venv python, byte-level, recursive over all of `memory/biography/`, run twice, 46,519 then 46,531 files as the live estate wrote): `dna-residual-003` hits 0, `coldest-vertex-001` hits 0. Neither id is bound by residual, registry, knots, chain, or kpi.

- `dna-residual-003`: no store binds it anywhere -> marked RETIRED in the doc header with the reason (per the ask's "or mark them retired").
- `coldest-vertex-001`: one live anchor outside the doc, verified verbatim at `docs/archive/README.md:5` ("Moved here under `coldest-vertex-001` so Mag hangs on residual+card+tip only.") -> pointed to it.

## Edits to docs/DNA.md (13 content edits, one coherent repair set)

1. Line 3: `dna-residual-003` marked retired 2026-09-29 with reason.
2. Line 3: `coldest-vertex-001` given anchor `docs/archive/README.md:5`.
3. Line 42 (Cold row): "SessionEnd must write" -> "Session close must write (daemon poll, `mag/daemon.py:44`)".
4. Line 60 (Set and forget row): "SessionEnd architecture" -> "Daemon-poll close files DNA".
5. Line 73: heading "Required (SessionEnd)" -> "Required (session close)".
6. Line 76: pipeline first line `hooks -> session_end_hook -> summarize_session` -> `daemon poll -> summarize_session (mag/daemon.py:44; def in mag/biography.py)`.
7. Lines 84-86: trigger note added (old trigger retired; endpoint survives unwired; config checked 2026-09-29: PreToolUse and PostToolUse only; manual fallback `python main.py summarize-session`) + heading "Optional derived (export layer; outside the close write)".
8. Line 131 (Architecture row): "SessionEnd files DNA" -> "Daemon close files DNA".
9-11. Lines 145-147: bare backup names prefixed with `memory/biography/` so every path claim resolves at repo root (finish-line requirement; the bare forms were root-MISSING per f-23).
12. Line 149: truncation completed from the doc's own context (sticker rule line 44, data-first line 62, export route rest.py:5291, derived/ dir verified 4,926 entries): "Skip forever-keeping every PDF or visual; `derived/` regenerates on demand (`POST /api/v1/export`)."
13. Line 76 follow-up: def citation "mag/biography.py:347" -> name-only "mag/biography.py" (see drift incident).

## Concurrent-drift incident (caught, resolved)

`mag/biography.py` was modified by another actor mid-run (uncommitted, +57/-17 vs HEAD): `def summarize_session` moved from line 347 (my first git grep) to line 395 (re-grep minutes later). My first edit had cited :347; corrected to name-only so the doc does not bank a line number that rotted the same hour. `mag/daemon.py` was verified clean vs HEAD and stable. Raw probes in the check file, section "mid-run drift catch + resolution".

## Checks run (all this ask; raw output banked)

Evidence file: `watch/inbox/gala_20260925/wave5-repair/lanes/dna-repair.check.txt`, instrument: `_dna_repair_check.py` (kept as evidence).

- Finish-line instrument, final run exit 0: CRLF-consistent endings (149 CRLF, 0 lone LF), byte tail is a complete sentence ending in a period, 32/32 path claims resolve, zero em/en dashes on authored lines (10 pre-existing em-dash lines untouched: 1, 8, 9, 10, 11, 14, 23, 25, 46, 88).
- Instrument honesty note: run 1 reported a false [2] FAIL from a wrong assertion in my own script (`endswith(")")` vs the sentence's final `.`); corrected and both runs kept in the check file.
- git: `git diff -- docs/DNA.md` shows the 13 content hunks only; `git log --oneline -- docs/DNA.md` unchanged (c5031bf45, eb07ad62e); `git rev-parse HEAD` 6a6e35b59 with no commits created by this lane (working-tree edit; no history rewrite).
- Store sweep, harness/claude config parse, daemon/biography/README/main.py/rest.py greps: probes P1-P9 in the check file.

## Not run / out of scope (stated, not filled)

- `tools/violation_ratchet.py check --changed` NOT run: this lane touched no code under mag/ or tools/ (docs/DNA.md and watch/inbox receipts only), so the ask's step 3 condition does not fire.
- pytest suite not run (doc-only repair, matching corpus-01's own scope note).
- Observed but not mine, left untouched: residual `edges.pins` has no writer/reader (s2-13 soft defect, DNA.md line 26 region) and the AGENTS.md DNA one-liner alignment flagged by corpus-01; both named here for the next owner.

## Decision ledger

Closes the burn-reset flash50 DNA.md repair item and changes close-path doctrine: the residual constitution now teaches the daemon poll (`mag/daemon.py:44` -> `summarize_session`) as the live close path, not the unwired `session_end_hook`; `dna-residual-003` is formally retired; `coldest-vertex-001` is bound to `docs/archive/README.md:5`.
