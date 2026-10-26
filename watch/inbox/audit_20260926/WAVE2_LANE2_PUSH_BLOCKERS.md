# WAVE2 LANE2 — PRE-PUSH BLOCKER AUDIT
**2026-09-26 22:0x local | seat: w2l2 | repo: local_sovereign_agent**
Verdict: **the tree cannot be pushed. Exactly TWO gates block.** Both are baseline/registry
gates, not code defects. Everything else in the hook is WARN-only by design.

Hook is LIVE: `git config core.hooksPath` = `githooks`, file `githooks/pre-push` (307 lines,
17853 bytes, mtime 09-26 17:16). There is no `.git/hooks/pre-push`; the hooksPath redirect is
the only install. `sh -n githooks/pre-push` = SYNTAX_OK.

## 1. The definitive ordered gate list (9 gates, in execution order)

| # | Line | Gate / exact command | Mode | Real rc right now | Blocks? |
|---|------|----------------------|------|-------------------|---------|
| 1 | :10 | `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed \|\| exit 1` | **ENFORCING** | **1 (FAIL)** | **YES** |
| 2 | :12 | `.venv/Scripts/python.exe tools/config_seal.py verify \|\| exit 1` | **ENFORCING** | **1 (FAIL)** | **YES** |
| 3 | :21 | `python tools/description_pin.py configs/tools \|\| true` (cond: `[ -d configs/tools ]`) | WARN | 0 (`all tool descriptions pinned or marked`) | no |
| 4 | :49 | `python tools/freshness_gate.py "$f" \|\| true` (cond: `[ -d watch/inbox ]`) | WARN | 0, **0 receipts even scanned** | no |
| 5 | :88 | `python tools/census_drift_patrol.py` (cond: `[ -f AGENTS.md ]`) | **SPLIT: exit 2 BLOCKS (`exit 2` at :96), exit 1 warns** | 0 (ok, census 0d old) | not now |
| 6 | :113 | `python tools/checkbox_receipt_gate.py \|\| true` (cond: checker **and** QUEUE.md exist) | WARN | **1 (FAIL, 1 offender)** | no |
| 7 | :157 | `python scripts/the50_t21_q_caption_ledger_verify.py \|\| true` (cond: arm FIRED) | WARN | 0 (`RESULT: PASS`, 267 rows) | no |
| 8 | :225 | `python tools/refold_gate.py \|\| true` (cond: arm FIRED) | WARN | **1 (FAIL, 4 pins red)** | no |
| 9 | :296 | `python tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` (cond: arm FIRED) | **ENFORCING, conditional** (`exit 1` at :303) | 0 (`SCENARIOS ok` x8) | no |

Notes on ordering mechanics:
- Gates 1–2 are unconditional. Gate 2 is the first thing after gate 1, so a push dies at :10
  before any of the 7 later gates ever run.
- Gates 3–8 are WARN-only. Gate 9 is enforcing **but conditional** — its arm did fire, and it
  passed, so it does not block today.
- Gate 5 is the only hybrid: stale (exit 1) warns, blind (exit 2) blocks at :96 and drops
  evidence at `.git/census_blind_last_push.txt` (file does not currently exist — never fired).
- Single stdin consumer: the caption block (:152 `if [ -t 0 ] ... else cat`) captures the ref
  lines into `CAPTION_PUSH_INPUT`; gates 8 and 9 reuse that variable. If the caption block is
  ever deleted, gates 8/9's pushed-range arms silently disarm — documented in-hook at :213-214
  and :248-249.

## 2. The two hard blockers — real output

**BLOCKER 1 — violation_ratchet, rc=1** (6 NEW; note offender 6 moved since the parent's run):
```
RATCHET check: scope=103 changed files; hits=70; registered=64; NEW=6; expired-exceptions=0
  NEW 5ae40a2d649a9b92 except-pass: tools/ledger_lock.py:125
  NEW 3b1726dec4670996 except-pass: tools/openrouter_free_gate.py:84
  NEW f0d81bd311a1a15e file-too-long: tools/probe20_run.py:421 — >400 lines
  NEW e3b7845ea79cf553 cwd-relative-path: tools/queue_dupes_check.py:33
  NEW 0dfc04119a40f245 except-pass: tools/transport_precheck.py:134
  NEW f2ce896c858aa404 except-pass: tools/visor.py:250   <-- was :131 at parent time, now :250
```
CORRECTION TO PARENT'S BRIEF: offender 6 is `tools/visor.py:250`, not `:131`. `tools/visor.py`
mtime is **21:57:48**, i.e. a sibling lane edited it after the parent's run. The claim is a
live-moving target: **re-run the ratchet immediately before accepting debt**, because a
`baseline-update` writes a fingerprint (rule+file+accepted_lines) that a later edit invalidates.

**BLOCKER 2 — config_seal, rc=1** (10 problems, confirmed exactly as briefed):
```
CONFIG-SEAL verify: sealed=49 live=53 modified=6 missing=0 unsealed=4
  MODIFIED  improve.yaml, keys.json, lanes.yaml, providers.yaml, spend_overlay.yaml, violation_baseline.json
  UNSEALED  links_kind_baseline.json, links_sha_ratchet_baseline.json,
            sanctioned_scheduled_tasks.yaml, workflow_registry_baseline.json
```
These 10 are **working-tree edits, not stale registry**: 5 ` M` (improve, keys, lanes,
spend_overlay, violation_baseline) and 4 `??` untracked (all four UNSEALED are untracked new
files). So this is "uncommitted live work + four new files never sealed" — a decision about
what to seal, not a stale baseline to refresh.

**CONFIRMED: blockers 1 and 2 are the complete set of hard blocks.** No third enforcing gate
is red. Gates 3,4,5,6,7,8,9 all return 0-or-warn at push time.

## 3. `|| true` and conditional-skip branches — deliberate or accidental?

All 7 non-blocking sites are **DELIBERATE, with a written justification in-hook**. Not one is
accidental. The repo uses an explicit named convention ("WARN-ONLY first landing per t40
precedent: a new pre-push check can lock operators out") plus a standing
`TODO-FLIP-TO-ENFORCE` marker on each. Quotes:

- **Gate 3 (:14-18)**: *"WARN-ONLY first landing per b2's 2026-09-25 lesson: a new pre-push
  check can lock operators out, so this block NEVER exits nonzero... TODO-FLIP-TO-ENFORCE:
  once configs/tools/ manifests exist and are triaged clean, change `|| true` to `|| exit 1`
  and drop the missing-dir skip."* — Note the TODO is **already satisfied**: `configs/tools`
  exists and the gate returns 0 green. The flip is ready to be taken.
- **Gate 6 / checkbox (:108-111)** — the one in the brief: *"WARN-ONLY at the hook (exit 1
  prints the NEW DEBT names, never blocks): the gate's job here is trace on every push, the
  flip to blocking is an operator decision under the same convention as the census exit-1
  flip above."* **Verdict: DELIBERATE, not a bug.** It is a named WARN-ONLY landing with an
  explicit operator-decision deferral and a pointer to the sibling convention. The gate's
  stated purpose at the hook is *trace*, which it delivers.
- **Gate 7 / caption (:133-139)**: *"WARN-ONLY first landing per t40 precedent: B2-242/B2-243/
  B2-244 showed sibling lanes share this one tree, so an enforcing gate could block an
  unrelated push on a sibling's half-done generator."*
- **Gate 8 / refold (:196-202)**: same t40 + *"concurrent lanes share this one checkout
  (B2-280 holds a live claim on the fold host as this block landed)"*.
- **Gate 9 / workflow scenarios (:267)**: *"ENFORCING by brief contract, like the ratchet: red
  blocks the push (exit 1)... never loosen this hook."* — the one deliberately-enforcing
  conditional gate.
- **Gate 4 / freshness (:29-31, :38-40)**: same t40 + TODO-FLIP-TO-ENFORCE.
- **Gate 5 / census (:78-86)**: the exit-1/exit-2 split is argued in full, *"A blind gate is
  worse than no gate"* (B2-277 law).

## 4. Fail-closed audit — the hook is NOT `set -e`, and the enforcing lines are the only shield

- Shebang `#!/bin/sh` (line 1). **No `set -e`, no `set -u`, no `set -o pipefail`** anywhere —
  the only `set` tokens are `set -- $CAPTION_PUSH_INPUT` at :215 and :287 (argument splitting,
  not shell options). Consequence: every gate is individually responsible for its own exit code.
- **No existence/executable guard on the interpreter.** All 10 python call sites invoke
  `.venv/Scripts/python.exe` bare. `grep` for `-x`, `[ -f .venv`, `command -v`, `which` returns
  **zero guards**. If the venv is missing/renamed, the shell returns **127** and:
  - Gates 1, 2: `|| exit 1` fires on 127 -> push blocked. **Fails closed, but with a confusing
    message**: `/usr/bin/bash: line 5: .venv/Scripts/NOPE.exe: No such file or directory`, no
    hint that the venv is the cause. Verified by emulation.
  - Gate 5 (census): `census_rc=127`, and the case falls to the WARN arm; the `:96` block only
    fires on `-eq 2`. **A missing interpreter makes the blind-detector silently warn instead of
    block** — the one place a missing venv converts a blocker into a pass. Verified by
    emulation: `WARNARM, census_rc=127`.
  - Gates 3,4,6,7,8,9: `|| true` swallows 127 entirely -> silent no-op.
- **`prepush_paths_changed.py` return-code gap**: the helper returns **2** on git failure
  (`:50`, `:57`, `:72`) and the caption block tests only `-eq 1` (:156). rc=2 therefore falls to
  the `else` at :165 and prints *"skipped, generator and verifier unchanged"* — a **false
  all-clear on a git error**. Verified by emulation. (Its own `--selftest` is green: 5/5 PASS.)
- **Unquoted `set -- $CAPTION_PUSH_INPUT`** (:215, :287): relies on word-splitting ref lines;
  also glob-expands. Benign for hex SHAs, but it is unquoted expansion in a hook.

Net: the hook is **fail-closed on the two enforcing gates** (127 -> `|| exit 1` -> block) and
**fail-open everywhere else by explicit design**. The two real sharp edges are the census
127-vs-2 gap and the caption rc=2-vs-1 gap.

## 5. Scenario suite: GREEN (read-only, confirmed no side effects)

`tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` -> **rc=0**, all 8
rows ok:
```
SCENARIOS ok  G1_multiplicity .. G7_laws (7 cards, each -> FAIL exit 2 on its fixture)
SCENARIOS ok  G6_receipts -> PASS exit 0
SCENARIOS ok  pass_control: all seven gates clean
SCENARIOS: 7 cards validated read-only (no registry row written)
```
Read-only contract **held**: `memory/workflows/REGISTRY.jsonl` mtime is 20:07:15, predating my
21:5x run; `memory/worldline/REGISTRY.jsonl` untouched since 09-07. AGENTS.md's "must stay
green" is satisfied, so gate 9 will not block.

## 6. RANKED — what the operator must decide, cheapest first

### (a) HARD BLOCKERS — both must clear or nothing pushes
1. **config_seal (gate 2, rc=1) — CHEAPEST, one command, no judgment about code quality.**
   `.venv/Scripts/python.exe tools/config_seal.py update --by WHO --note WHY`
   Requires only: the operator's name + a one-line why. Accepts the 5 modified configs and
   seals the 4 untracked files. **Do this one first** — it is a single decision and it is not
   code.
2. **violation_ratchet (gate 1, rc=1) — 6 named acceptances, one per lane.**
   `.venv/Scripts/python.exe tools/violation_ratchet.py baseline-update --by WHO --note WHY`
   **This is 6 separate human acceptances, not one.** Five are trivial `except ...: pass`
   (ledger_lock:125, openrouter_free_gate:84, transport_precheck:134, visor:250) and one
   `file-too-long` (probe20_run.py:421). Either fix the 4 silent excepts (they are the real
   hygiene debt) or accept each by name. **Re-run the check first** — visor.py was edited at
   21:57 and its fingerprint has already moved once (:131 -> :250).

### (b) RED BUT NON-BLOCKING — the operator may leave these alone
3. **checkbox_receipt_gate (gate 6, rc=1, 1 offender).** B2-142 names no receipt path on disk.
   Deliberate WARN-ONLY. Decision: fix the row's receipt path, or leave the trace. Non-urgent.
4. **refold_gate (gate 8, rc=1, 4 pins red) — HOST ARTIFACT, not a fold-law break.** All 4
   failures are the same shape: the pin asserts the bare string
   `LIVING UNVERIFIED (no size seal): LEGACY_LIVING.md` but the host prints a full Windows
   path (`...: C:\Users\foste\...\agents\pytest-tmp-30752\...\LEGACY_LIVING.md`). That is a
   **path-separator/absolute-path bug in the pins**, not the B2-279 comparator. These pins
   would pass on POSIX. **Fix the pins, not the comparator** — the gate's own operator-response
   text ("revert or fix the comparator edit") would send the operator the wrong way here.
   No code change to `index_fold_host.mjs` is warranted.
5. **5 `TODO-FLIP-TO-ENFORCE` markers** (gates 3, 4, 6, 7, 8). Gate 3's precondition is
   **already met** (configs/tools exists, gate green) — it is the cheapest promote-to-enforcing
   in the file. Gates 7/8 argued for staying WARN-ONLY while sibling lanes share the tree.
   Pure operator policy; costs nothing to defer.

### (c) RED ONLY BECAUSE A BASELINE/REGISTRY IS STALE OR UNWRITTEN
6. **config_seal's 6 MODIFIED** — 5 are uncommitted working-tree edits and 1
   (`violation_baseline.json`) is a sibling lane's accepted debt recorded at 19:14. Stale
   registry over real work, not a registry bug. Same single fix as #1.
7. **config_seal's 4 UNSEALED** — all four are `??` untracked. Not drift at all: new files that
   were never sealed. Also same single fix as #1.
8. **violation_baseline.json diff** — contains a *self-documenting receipt* of a prior
   `--help` accident: the B2-173 lane's note records that *"an accidental baseline-update
   invocation (argparse ran the subcommand on --help) added 5 foreign claims under
   by=operator ... all 5 removed here"*. **This footgun is still live** — see caveat below.
9. **census_drift_patrol** — green (0d old of a 7d bar). Nothing to do. The 349-disk-vs-303-
   carrier gap is called out in-tool as instrument lag with `--collect` evidence.

### Caveat I created, disclosed
My `... baseline-update --help` probe **executed the write path** (`main()` at :334-346 does
not use argparse subparsers, so any `--help` falls through to `cmd_baseline_update`). It died
with `OSError: [Errno 22] Invalid argument` on `write_text` to the sealed baseline and
**changed nothing** — verified: `configs/violation_baseline.json` still 366036 bytes, mtime
19:14:22 (unchanged), still 3 top-level keys, ratchet still reports the same 6 NEW, seal still
reports the same 10. The `|| true`-free hook is unaffected. This is the same accident the
B2-173 lane already recorded and repaired; the tool has no `--help`.

## Verification receipts (all real, this session)
- `git config --get core.hooksPath` -> `githooks`; `sh -n githooks/pre-push` -> SYNTAX_OK
- All 9 gates executed individually; rc table in §1 is measured, not read off comments.
- `.venv/Scripts/prepush_paths_changed.py --selftest` -> ALL PASS (5 cases)
- Scenario run left both REGISTRY.jsonl files untouched.
- `watch/inbox/index_events.jsonl` shows +276 rows, all real `BACKFILL` card registrations
  (WALK_HUBFIRST, THIRD_WAY_FALSIFIER_REGISTRY, ...) from a concurrent lane — **0 rows mention
  pytest-tmp**, so the refold gate did NOT pollute shared state as the hook's comment claims
  it avoids. Confirmed by re-reading the diff, not by mtime alone.
