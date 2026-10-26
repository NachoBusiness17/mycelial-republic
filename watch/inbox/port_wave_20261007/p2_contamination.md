# P2: paired seen/unseen contamination tripwire (port wave 2026-10-07)

Lane: P2 of the day-7 mine fold port wave. Steal: find 1 of the
evals-self-improvement card under
`watch/inbox/frontier_olm_2026-10-07/steal/` (the decontamination thread:
lab-side decontamination search cannot prove unseen-ness; the standing signal
is score DIVERGENCE between corpus-seen material and a post-freeze minted twin
set). Graduate mag/mirror_control.py condition C into a standing paired-score
tripwire, per the ask.

## Landed

- `mag/contamination_tripwire.py` (new, 400 lines exactly, ratchet-clean).
  New module, not a mirror_control extension: the pair shape (two eval arms +
  divergence ledger + improve-candidate landing) is not the one-shot
  instrument-control shape mirror_control owns; mirror_control is untouched.
- `mag/improve.py`: run_eval hook (standing_check call, step recording) and a
  generalized `provider_probe_due` with an optional keyword-only `key` param
  (default keeps the pinned B2-106 contract byte-identical; the tripwire
  reuses the same broken-clock cadence semantics under state key
  `last_contamination_check`).
- `configs/improve.yaml`: `contamination_tripwire` block (enabled, lane
  gemma:2b, count 12, threshold 0.15, cadence_days 1).
- `tests/test_contamination_tripwire.py`: 22 tests, all passing.

## Pair mechanics

Same generator, count, spec on both arms; only the cycle index differs.

- SEEN arm: tools/duty_fuzz.py cycle 0, the cycle-0 reference battery whose
  bytes sit in the duty_fuzz docstring and in
  `watch/inbox/duty_fuzz/cycle_000.jsonl` (filed 2026-09-18): repo-seen.
- MINTED arm: duty_fuzz cycle 9999, held-out by construction (the generator
  seeds an independent RNG per global case index, so different cycles can
  never emit the same case, and no cycle-9999 batch is filed anywhere: the
  live check is test_minted_cycle_not_filed_anywhere in the test file).
- Grader: deterministic closed-option letter match against the case's
  spec_reading; no LLM judge; a response with no A-D letter scores wrong.
- delta = seen_score - minted_score; delta at or above the threshold is the
  WARN (seen climbs while minted stays flat). The row shape is exactly
  {ts, lane, seen_score, minted_score, delta, threshold, verdict, warn,
  count, seed, seen_cycle, minted_cycle}, appended to
  `memory/improve/contamination/pairs.jsonl`.

## B2-106 landing pattern (row shape matched to mag/improve.py run_provider_probe)

On WARN: ONE candidate via mag.improve.append_candidates with schema
improve_candidate.v1, id from the same _candidate_id, kind=risk status=new,
source=mag_internal, source_urls naming the ledger, plus EXACTLY ONE
[priority] line to the B2-494 attention surface. Quiet pair: kind=runtime
status=hold (evidence, not a ticket), no attention line. The candidate row
shape test pins the key set against the provider-probe row.

## CLI

- `python -m mag.contamination_tripwire --check gemma:2b` runs the pair once
  (exit 0 clean, 1 WARN, 2 error; `--root` sandboxes ledger/candidates/state).
- `--register` writes the standing-call note into the improve playbook
  (idempotent, marker-checked). No schtask was created: MagImproveDaily
  already drives improve_once -> run_eval daily, and run_eval now calls
  standing_check, so the standing call rides the existing cadence.

## First fires (real, local ollama gemma:2b)

- Sandbox smoke at count 3: both arms 1.0, delta 0.0, OK, exit 0.
- First real pair at default width, count 12 (source row:
  `memory/improve/contamination/pairs.jsonl`): seen 0.9167 vs minted 0.8333,
  delta 0.0833 below the threshold, verdict OK, hold candidate c-464fa9e1143d.
  Both arms tracking each other falsifies the contamination worry for this
  lane at this width. The run stamped `last_contamination_check`, so the next
  eval inside the window skips (B2-106 semantics).

## Tests

tests/test_contamination_tripwire.py: 22 passed in about a second. Combined
improve-related sweep (tripwire + provider probe + loop + behavioral + crash +
off/on + status suites): 79 passed. Fixture falsifier pinned: a lane answering
seen-arm cases correctly and minted-arm cases wrongly trips (delta 1.0, risk
row, one attention line); a fair lane passes silent (hold row, no attention
line).

## Gates

- pytest: green as above.
- Ratchet (`tools/violation_ratchet.py check --changed`): zero NEW from this
  lane. Two of my findings were found and fixed during the build (file over
  the 400-line cap: trimmed to exactly 400; a silent except-pass: both
  handlers now name the skipped action on stderr). Remaining NEW findings are
  sibling working-tree debt in files this lane never opened
  (`mag/llama_cpp_bridge.py`, `tools/code_execution.py`, plus GROWTH claims on
  `tools/hermes_burn.py` and `tools/workflow_gate.py`); code_execution.py's
  violation line moved between two of my runs, so a sibling seat is actively
  editing it. Accepting that debt by name is the owner's call, not this lane's.
- Citation lint (`tools/citation_lint.py check --changed`): all blocking
  findings sit in `memory/zknot/` session records, which zknot regenerates at
  logon (generated sibling surfaces, none authored here). No finding names a
  file this lane wrote.

## Blockers / handoff

None blocking this lane. Repo-wide ratchet and citation-lint FAILs above are
pre-existing shared-tree debt owned by other lanes; flagged for the wave
close. The standing tripwire's real value accrues at cadence: watch the pairs
ledger for a lane whose seen arm climbs while its minted arm stays flat.
