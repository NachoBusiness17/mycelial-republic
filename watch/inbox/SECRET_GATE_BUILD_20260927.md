# SECRET GATE BUILD 20260927 (gate-builder seat, per PACK_SECRET_GATE_20260926)

**Verdict:** `tools/secret_gate.py` is built, staged, and banked per pack
section 4. All deterministic acceptance items PASS with captured output
(fail-closed exits, venv guard, clean dir, masked-token exemption, planted
token blocking, baseline mechanics, S1 copy-don't-move, hook untouched).
The whole-tree `--full` completion is OWED: attempt 1 exited 2 fail-closed
on a pre-existing tree defect (literal `nul` device-name files) which I
then fixed in-tool; attempt 2 was killed externally at ~52 min (2,732s CPU,
stable 701MB, no output). A third attempt was launched at bank time with
its outcome landing in `watch/inbox/secret_gate_results/full_run_row.json`
and `full_run_exit.txt`. No hook was wired, per instruction.

## Evidence (real captured output)

Interpreter for every run: `.venv/Scripts/python.exe`. Nothing below is
paraphrased; masked heads are the scanner's own output shape (first 6
chars + length). No secret values appear in this receipt.

1. Fail-closed CLI semantics, all captured:
   - `--help` exit 0; no mode flag exit 2; `--changed --full` exit 2;
     `--severity urgent` exit 2.
   - Foreign interpreter (venv guard, the simulated missing-venv case; if
     the venv were missing its interpreter could not run at all, so any
     foreign interpreter means unsanctioned environment):
     `python tools/secret_gate.py --full` exit 2,
     stderr: `secret_gate: not running on the repo venv
     (C:\Users\foste\AppData\Local\Programs\Python\Python312\python.exe);
     use .venv/Scripts/python.exe`
   - Missing scan path exit 2; missing baseline file exit 2 (before any
     scanning: `baseline unreadable`).
2. Clean dir (dedicated temp dir, 1 file) exit 0, machine row:
   `{"tool":"tools/secret_gate.py","schema":"secret_gate_beat.v1",...,"census":{"files_seen":1,"scanned":1,...},"severity_counts":{"critical":0,"high":0,"medium":0,"low":0},"rule_counts":{},"blocking_count":0,...,"results_file":null,"runtime_sec":0.0}`
3. Redaction exemption (B2), exit 0, zero findings. Temp file lines:
   `masked example one: xai-REDACTED...MASKED` (the pack's literal test
   token) and `masked example two: xai-REDACTEDMASKEDTOKEN12345678ab`
   (padded so the XAI-KEY regex itself matches; exempted by the borrowed
   ALLOW_RE). Row: `"rule_counts":{},"blocking_count":0`.
4. Planted high-severity provider token BLOCKS, exit 1. Synthetic token
   (not a real credential), file line:
   `planted_token = "sk-ant-[SYNTHETIC FIXTURE, MASKED 2026-09-27: the gate
   correctly flagged this receipt for quoting its own fixture verbatim]"`.
   Row: `"rule_counts":{"ANTHROPIC-KEY":1},"blocking_count":1`,
   sample `... "rule":"ANTHROPIC-KEY","severity":"high",
   "masked":"sk-ant...(len=42)"`.
5. Same plant as an UNTRACKED file at repo root on the `--changed` path
   (the realistic pre-push shape): exit 1, `blocking_count` 3, planted row
   present alongside the two real findings below. Plant deleted after the
   run (`ls` confirms gone, `git status --porcelain` empty for that path),
   nothing staged or committed by any test.
6. Baseline named acceptance (B3 shape): the planted finding accepted via
   `--baseline` exit 0, `"blocking_count":0,"accepted_count":1` (finding
   still reported in severity counts; day-one baseline is zero and none
   ships with the tool).
7. Real `--changed` run over the current tree (no plant), captured:
   `mode=changed scope=worktree+untracked (no upstream configured)
   files_scanned=2136 runtime_sec=110.6`,
   `severity: critical=1 high=14 medium=1 low=748`,
   `s3: aws_secret_entropy_filtered=189`,
   `blocking=2`:
   `cdx_rar.json:616:GOOGLE-OAUTH-AQ:high masked=AQTA2T...(len=32)` and
   `watch/inbox/audit_20260926/LANE0_PARENT_INTEGRATOR.md:21:PRIVATE-KEY-BLOCK:critical masked=-----B...(len=31)`.
   Both blocking files are untracked (`??`), caught by the untracked arm.
   High breakdown: GOOGLE-OAUTH-AQ 1 (blocks), AWS-SECRET-40 13 kept after
   entropy gating (never blocks), PRIVATE-KEY-BLOCK 1 critical (blocks).
   Results: `watch/inbox/secret_gate_results/changed_20260927T034649Z.json`
   (plant run kept at `changed_20260927T034900Z.json`).
8. Whole-tree `--full` attempts:
   - Attempt 1 (23:50): exit 2, `secret_gate: internal error: ValueError:
     path is on mount '\\.\nul', start on mount 'C:'`. Fail-closed worked;
     root cause: the tree carries literal `nul` files (Windows reserved
     device names; stray `> nul` debris) at repo root,
     `corpus/library/lmcache-src/nul`, `memory/runs/the50/nul`. Fixed by
     hardening `rel_of` (comment in-tool carries cause + evidence).
   - Attempt 2 (23:53): killed externally, wrapper exit 137. Process
     telemetry while alive: single-threaded full CPU, 2,732s CPU,
     working set stable at 701MB. No row, no results file.
   - Attempt 3 launched at bank time 00:56:21 and confirmed ALIVE at
     bank+8min (venv trampoline PID 22820 + base interpreter PID 3980,
     51s CPU, 690MB, ramping normally; the uv-managed venv always spawns
     this pair). Additional identical `tools/secret_gate.py --full --json`
     runs were started by launchers I did not start (00:57:15, PIDs
     34304/21128; 00:58:20, PIDs 7740/26896; all still alive at 01:0x);
     no action taken per stop-and-report. Duplicate runs do not collide
     on the timestamped results files; only the fixed-name row/exit files
     are last-writer-wins. Outputs land at
     `watch/inbox/secret_gate_results/full_run_row.json` and
     `full_run_exit.txt` (fixed names, last-writer-wins if both runs
     complete) plus per-run timestamped `full_<ts>.json` results files
     (unique names, authoritative). The prior corpus+watch reference run
     took 1,183.1s for 38,710 files (results file census), so expect
     ~25-35 min per whole-tree run.

## Work done

- Built `tools/secret_gate.py` (staged, `A tools/secret_gate.py`, 559+
  lines after fix). Flags exactly per pack section 4: `--changed`,
  `--full` (mutually exclusive, required), `--severity`
  {critical,high,medium,low} default high, `--baseline`, `--json`, plus
  documented optional positional paths that narrow the scan scope (needed
  to make the clean-dir and planted-token acceptance items deterministic
  without committing anything; flagged here as the one deliberate
  addition to the pack's flag list).
- S3 (fixed first): AWS-SECRET-40 is entropy-gated behind the scanner's
  own shannon floor (4.3, the ENT branch threshold). The rule TABLE stays
  byte-verbatim (no regex touched); the filter applies at match time.
  Hex SHAs (~3.9 bits/char) cannot pass; real 40-char base64 secrets do.
  Filtered-vs-kept is emitted as `s3_aws_secret_entropy_filtered`.
  Directional evidence: in the dirty-tree sample 189 filtered vs 13 kept.
- S4 (fixed second, inside my boundary): the machine row is
  `secret_gate_beat.v1`: counts + `files_with_rule_hits_count` +
  `results_file` path, never the list. Captured rows are ~0.7-3KB vs the
  old 641,924-byte beat row (verified by reading the old row: 4,812-entry
  `files_with_rule_hits` list). The weekly script's own line 45 still
  embeds the list; I did not edit it (detector-only boundary) and the
  one-line fix is owed below.
- S1 (third): B2_73 content copied into `tools/`; original
  `watch/inbox/burn_wave_20260926/B2_73_secret_scan.py` untouched (still
  9,533 bytes, mtime Sep 26 12:22). No stub left (5d: rename/move is
  operator-gated; copy-don't-move default honored).
- S2 preparation: `--changed` is upstream-aware (diff `@{upstream}..HEAD`
  plus staged, unstaged, untracked) and records its basis in every row.
  This branch has NO upstream configured (verified), so the run above
  used `worktree+untracked`. The hook itself was NOT wired, per
  instruction.
- Blocking tier per pack ruling 3: only specific provider shapes can
  block and only at/above `--severity` (default high). AWS-SECRET-40,
  GENERIC-KEYASSIGN, ENV-ASSIGN, JWT-TRIPLE, GENERIC-BEARER never block.
- Incident, reported: removed a stale 0-byte `.git/index.lock` dated
  22:12 (97 min old) after `tasklist` and a PowerShell process probe both
  showed no live git process; it was blocking `git add`. No other git
  state was touched.

## Acceptance checklist (pack section 6)

- `--full` runs to completion, exit recorded: **FAIL/OWED** (attempts and
  telemetry above; attempt 3 in flight at bank time, path named).
- Reports PRIVATE-KEY-BLOCK for `memory/tls/lan.key`: **OWED** (needs a
  completing whole-tree run; memory/ is in `--full` scope by design). Two
  related truths: the `--changed` run already produced a critical
  PRIVATE-KEY-BLOCK block on
  `watch/inbox/audit_20260926/LANE0_PARENT_INTEGRATOR.md:21`, and the
  pack's evidence table misattributes the old run's hit: the 2026-09-26
  results file records it at
  `corpus/library/openai-cookbook/examples/chatgpt/gpt_actions_library/gpt_action_box.ipynb:929`,
  not lan.key (old scope never included memory/).
- Post-S3 total under ~12,000, critical/high readable: **OWED for the
  whole tree**; directionally supported (old scope arithmetic
  60,470 - 48,427 = 12,043; changed-run sample 189 filtered vs 13 kept).
- Synthetic masked token produces no finding: **PASS** (item 3).
- `githooks/pre-push` passes its existing gates unchanged: **PASS
  structurally** (hook not wired and byte-identical: `git diff` on
  githooks/ empty, file tracked and unmodified).
- Pre-push runtime under 15.7s on `--changed`: **FAIL as measured**:
  110.6s on the current tree. Cause: no upstream + 1,681 dirty + 2,204
  untracked entries, so `--changed` degenerates to a 2,136-file scan.
  This also crosses the pack's 60s stop line: reported, not silently
  optimized. On a clean tree with an upstream the changed set collapses
  to the push range.
- Planted high-severity token blocks: **PASS** (items 4 and 5).
- Clean push does not block: **PASS at scanner level** (clean dir exit 0);
  the literal hook case is unwired by instruction.
- Simulated missing-venv returns exit 2: **PASS** (item 1).
- `git add` lands, `git status` shows it tracked: **PASS**
  (`A tools/secret_gate.py`).

## Recommendation: hook vs weekly (pack section 10)

**The pre-push hook (`--changed`) is canonical.** Reasons, from bytes:
(1) the scheduled path is the living example of this estate's root
disease, instruments built but not run: `MagSecretScanWeekly` is
Ready+Enabled with last result 267011 and has never fired, while the
hook fires exactly at the moment a secret would leave the machine;
(2) the estate's own evidence says unenforced detectors get ignored
(critical=1 high=48,544 buried the one real critical); (3) the measured
cost is acceptable when the precondition is met: wire the hook to
`--changed` on pushes from a clean tree with an upstream configured
(seconds), and treat the current 110.6s dirty-state run as the cost of
the burn-wave debris, not of the gate. Keep the weekly only as an
optional report-only `--full` archive beat (S4-compliant row), never as
the enforcement path. Do not ship both as peers: if the hook lands, the
weekly's alert-writing role should be deleted rather than duplicated.

## Owed

1. Completing whole-tree `--full` (attempt 3 in flight; else chunked
   foreground runs, each under the 10-min cap: everything except
   corpus+watch, then watch/, then corpus/ split by size, merged
   arithmetically with captured output).
2. PRIVATE-KEY-BLOCK demonstration on `memory/tls/lan.key` from that run.
3. Post-S3 whole-tree totals (and the corpus+watch subset for the
   apples-to-apples ~12,000 comparison; different scope = different
   denominator, name it per census law).
4. `scripts/secret_scan_weekly.py` line 45 still embeds
   `files_with_rule_hits` (the 641,924-byte row cause): the S4 fix there
   is a one-line operator-gated edit I did not make (detector-only
   boundary). If the hook becomes canonical per the recommendation,
   retire that script instead.
5. Operator items (5a-5c stand): plus two NEW blocking findings from the
   changed run, both untracked: `cdx_rar.json:616` GOOGLE-OAUTH-AQ high
   (validate/rotate/remove; masked head AQTA2T, len 32) and
   `watch/inbox/audit_20260926/LANE0_PARENT_INTEGRATOR.md:21`
   PRIVATE-KEY-BLOCK header inside an inbox receipt (check whether actual
   key material follows the header; I did not open either file beyond
   the scanner's own reads).
6. Three stray `nul` device-name files (repo root,
   `corpus/library/lmcache-src/`, `memory/runs/the50/`): pre-existing
   debris that breaks `os.path.relpath`; reported, not deleted.
7. Hook wiring itself: three lines, land only after operator review per
   instruction; this receipt's runtime section is the input to that call.
