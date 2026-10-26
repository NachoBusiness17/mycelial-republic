# W2 SCARLESS PREFLIGHT — Mickey17 Wave 2 (2026-09-29)

**Lane:** scarless-clone improvement from ledger return 25 (configs agent): "move endemic rules for files born after a cutoff into preflight rails; heredity becomes impossible; the baseline shrinks monotonically."

## What was built

A date-conditioned content rail that blocks NEW except-pass scars at the preflight door (agent_cli.py:717 -> mag/rails.py check_write_file), with everything existing grandfathered by git birth date.

**Files:**

- `configs/constitutional_rails.json` — new rule `no_new_except_pass` in `write_file_content`, following the exact existing schema (id/desc/regex/severity) plus one additive field `git_first_commit_after: "2026-09-29"`. Regex scope is deliberately the two named shapes only: bare `except: pass` and `except Exception[: as e]: pass`, multiline included; typed tuple excepts stay the pre-push ratchet's domain.
- `mag/rails.py` — minimal additive engine extension (existing rules byte-unaffected, proven by test): in `check_content`, a rule carrying `git_first_commit_after` is skipped when `_grandfathered(path, cutoff)` says so. `_git_first_commit` (lru_cached, lazy: git is probed only after the regex already matched, so clean writes pay zero subprocess cost) returns the ISO date the path first appeared in history (`git log --reverse --format=%as --`), `''` for untracked (a file being born now: fully subject), `?` for probe failure (fail OPEN, the engine's existing never-crash law; pre-push ratchet remains the backstop for undatable files). Grandfather comparison is inclusive: born ON the cutoff = existing estate.
- `tests/test_scarless_preflight.py` — new, 10 tests against the REAL frozen contract, not a synthetic copy.

## Design decision (documented)

The rails engine had no date awareness, so the choice was engine extension vs wrapper check. Chose the in-engine extension: one optional field, ~55 lines, keeps a single enforcement loop and keeps the law itself in the editable JSON where the file header says it belongs ("rails file is the single editable source for new rules"). A wrapper would have forked the preflight door agent_cli already calls.

## THE key finding — heredity count

Ran the real rail over the whole tree with the grandfather disabled (every file treated as born-now):

- **mag/ + tools/: 1,247 files scanned; 513 files (41.1%) would have been BLOCKED without the grandfather.**
- AST cross-check (ratchet scanner): 655 files (52.5%) carry except-pass/bare-except, 1,687 raw hits, collapsing to 655 claims — exactly the 654 except-pass + 1 bare-except registered in `configs/violation_baseline.json`, i.e. the 69%-of-945-claims heredity return 25 named.
- The 142-file gap between 513 (rail) and 655 (AST) is the typed/tuple except-pass shapes outside the rail's named scope.

So: 4 in 10 files in the enforced roots carry the scar today, and every one of them got there through a write the new rail would have refused. From the cutoff forward, heredity for the two named shapes is structurally impossible at the write door.

## Verification

- `pytest tests/test_scarless_preflight.py -q` — **10 passed** (grandfathered old file passes; born-on-cutoff passes; born-after-cutoff blocked; untracked+except-pass blocked; untracked+bare-except blocked; untracked+proper handling passes; probe-failure fail-open; secret rail unaffected on grandfathered path; check_write_file door blocks).
- Adjacent suites (test_agent_desk, test_bard, test_lane_runner_cluster, test_seed_mcp) — **73 passed**.
- Live end-to-end probe, no monkeypatch: untracked path + scar -> BLOCKED naming `rail[no_new_except_pass]`; `mag/rails.py` (git-born 2026-08-04) + scar text -> PASSES (grandfathered); untracked + handled -> passes.
- Ratchet `check --changed`: my files (`mag/rails.py`, `tests/test_scarless_preflight.py`) scan CLEAN; the two NEW file-too-long rows in the same run belong to sibling wave lanes (`mag/physical_compute_acquire.py`, `tools/regen_front_door.py`), untouched by this lane.

## Limitations (honest)

- Regex, not AST: a docstring in a new file quoting `except: pass` literally will be blocked; the remedy is rewording the docstring, not a handling change. Accepted cost of a no-LLM, no-parse preflight.
- Untracked-but-pre-existing files (written before the cutoff, never committed) are treated as born-now; correct under "grandfather everything existing IN GIT", and the write that would have created them was refused anyway going forward.
- A file renamed into place reads its rename date as birth (no `--follow`); conservative in the enforce direction, documented here.
