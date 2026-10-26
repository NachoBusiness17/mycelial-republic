# config-hygiene receipt (gala wave5-repair, division B, 2026-09-29)

Lane file: `watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.json` (incremental).
Raw check output: `watch/inbox/gala_20260925/wave5-repair/lanes/config-hygiene.check.txt`
(instrument: `config-hygiene.check.py` + `config-hygiene.check_driver.py` in the same directory).
Started from: `watch/inbox/burn_reset_20260927/flash50/f-03.md` (finding 5, silent-soft class)
and `watch/inbox/burn_reset_20260927/flash50/s2-10.md` (seal red modified=4, F1/F3).

## What was done

### 1. models/providers.py fail loud (was the silent empty-roster swallow)

- Old code (f-03 finding 5): `load_providers()` returned
  `{"providers": {}, "defaults": {}, "routing": {}}` BOTH when
  `configs/providers.yaml` was missing AND on any yaml parse error, rc=0.
  A corrupted roster read as "zero providers configured" and every lane died
  later as "unknown provider".
- New code: `models/providers.py:73` adds `ProviderConfigError(RuntimeError)`;
  `models/providers.py:82` `load_providers()` now:
  - missing file -> raise naming the absolute path + recovery hint
    (`providers roster missing: ...` at :103; providers.yaml is gitignored,
    disk-only copy per f-03, and the `providers.yaml.bak-*` sits beside it);
  - yaml parse error -> raise `providers roster unreadable: <path>: <exc>` at
    :113, chained `from e`;
  - parses to a non-mapping -> raise `providers roster malformed` at :117;
  - success -> `setdefault` of `providers`/`defaults`/`routing` so downstream
    `.get(...)` shapes hold (strict improvement: the old success path did not
    guarantee those keys).
- Decision recorded in the code comment: NO marked empty-roster fallback is
  kept, because no default roster exists anywhere in the repo to fall back TO;
  the empty map was the failure dressed as a default. This is the ask's
  "explicit fallback only where a default roster is genuinely intended"
  clause, answered with "nowhere": stated in code and here.
- Blast radius checked, not guessed: `mag/boot.py:_quota_snapshot` wraps the
  loader in try/except; `dashboard/rest.py:1552-1560` loads inside a try
  block; `mag/doctor.py:639-641` reads through the same loader. A raise
  surfaces as a named error in those surfaces, not a crash of the host.

### 2. mag/improve.py fail loud (was silent-disable on missing config)

- Old code: `load_config()` returned `{"enabled": False, ...}` when
  `configs/improve.yaml` was missing, so the scout went dark with rc=0.
- New code: `mag/improve.py:64` raises `FileNotFoundError` naming the path
  (:76) and pointing at the sanctioned channel: deliberate disablement is the
  t73 executor `python main.py improve-off --reason ...`, which writes the
  marker `logs/magimprove_intentional.flag` (`mag/lifecycle.py:68`,
  `improve_off` at `mag/lifecycle.py:156`) and NEVER touches improve.yaml.
  So a missing file is a broken install, not an off state.
- Parse errors were already loud here (`yaml.safe_load` uncaught); the missing
  file was the only silent path, and it is closed.
- `configs/improve.yaml` exists and is git-tracked, so live behavior is
  unchanged (proved: enabled=True, 18 sources, regression guard below).

### 3. Seal debt cleared by the sanctioned re-seal (restore-bytes rejected with reasons)

Baseline verify (before any change, raw output banked):
`CONFIG-SEAL verify: sealed=56 live=56 modified=4 missing=0 unsealed=0`,
exit 1, MODIFIED exactly fossil_registry.json, improve.yaml, mirrors.json,
violation_baseline.json. No NEW modified files beyond the known 4 at lane
start.

Per-file verdict on "restore sealed bytes vs re-seal" (all four examined, not
assumed):

| file | evidence run | verdict |
|---|---|---|
| improve.yaml | `git diff configs/improve.yaml` empty; `git log -1` = caddaeb72 2026-09-28T13:21 Q-049 demote block | live bytes ARE committed truth; restoring seal bytes would time-travel the estate. re-seal |
| violation_baseline.json | `git log -1` = d90bc8607 2026-09-28T15:09 ratchet prune 943->941, post-stamp; git-clean | committed truth. re-seal |
| fossil_registry.json | `git diff` shows +3/-1: adds recompile_cmd/check_cmd to the thought-quantizer entry; uncommitted working-tree edit | restoring would destroy a concurrent lane's registry work; left uncommitted for its author. re-seal |
| mirrors.json | git-untracked, rewritten by tools/stealth_driver.py every cycle (s2-10 item 10 + F3) | it is live state, not config; restoring would corrupt driver state. re-seal + structural fix owed |

Sanctioned act, reasons named per file in the note:
`python tools/config_seal.py update --by gala-wave5-config-hygiene-lane --note "..."` exit 0,
then verify `sealed=56 live=56 modified=0 missing=0 unsealed=0` PASS exit 0.

## Finish line, byte-checked (all run this session, raw output in the check file)

1. Corrupted provider yaml fails loud with the file named:
   `config-hygiene.check.py` CHECK 1 PASS: temp providers.yaml with a yaml
   ParserError -> `ProviderConfigError: providers roster unreadable:
   C:\...\Temp\config_hygiene_jg0593k7\providers.yaml: ParserError: ...`
   (also CHECK 2 PASS: non-mapping yaml -> malformed error naming the file).
   Driver stage `pre`, exit 0.
2. Missing improve.yaml fails loud: CHECK 5 PASS: `FileNotFoundError: improve
   config missing: C:\...\improve.yaml (...)`.
3. Seal verify reports no NEW modified files beyond the known 4: baseline
   verify showed modified=4 = exactly the known 4 (nothing NEW); after the
   sanctioned re-seal, verify is modified=0 PASS exit 0. Mid-lane, a
   concurrent stealth_driver cycle rewrote mirrors.json and the first
   stage-`final` verify went red with modified=1 = mirrors.json ONLY - a
   member of the known 4, zero NEW files, the exact s2-10 F3 churn this
   receipt predicts, now with live evidence. A second named act re-sealed it
   (stage `reseal2`, note names the churn and the owed structural fix), and
   the closing stage-`final` verify reads modified=0 PASS exit 0. Full
   chronology is in the check file: pre (baseline red 4/4) -> reseal (green)
   -> final (red, mirrors.json 1/known-4) -> reseal2 (green) -> final
   (green) -> scan.
4. Regression guards: live configs/providers.yaml loads 28 providers (CHECK 4
   PASS); real configs/improve.yaml loads enabled=True with 18 sources
   (CHECK 6 PASS).
5. Ratchet (ask step 3, mag/ touched):
   `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
   exit 1. Attribution proved, not assumed: the 3 NEW hits are
   mag/corpus_gap_research.py:663 (UNTRACKED new file, `??` in git status,
   663 lines), mag/corpus_selfsteal.py:476 (working-tree +159 lines), and
   tools/fossil_check.py:73 (working-tree +48 lines) plus one GROWTH claim on
   tools/census_drift_patrol.py (+3) - all concurrent lanes' in-flight files.
   My only edits are models/providers.py (outside the mag/+tools/ ratchet
   scope) and mag/improve.py, and mag/improve.py drew ZERO hits. The exit 1
   is the shared tree's pre-existing debt, not introduced by this lane; per
   the ratchet's own rule the fix belongs to the owning lanes (accept by
   name or fix), not to a bystander lane, and I did not touch their files.

## Owed / stated plainly

- mirrors.json remains a standing churn source: a live stealth_driver state
  file inside a push-blocking configs/ seal, git-untracked (s2-10 F3). It
  will drift again on the next stealth cycle and the daily 09:45 ratchet log
  will show MODIFIED mirrors.json again. The structural fix (move it out of
  configs/ or exempt live-state files by name) is an operator decision; this
  lane re-sealed per its mandate and did NOT unilaterally restructure the
  seal.
- Seal scope gap unchanged: `tools/config_seal.py:36-43` globs top-level
  only, so subdirectory configs (incl. the 7 LAW-12 cards) stay unsealed
  (s2-10 F2). Recorded, not judged, not changed.
- fossil_registry.json's working-tree edit is sealed but still uncommitted;
  its author (or an operator) should commit it.
- I did NOT touch tools/stealth_driver.py (another lane owns it), did not
  commit anything, and did not change any other config reader's error
  handling beyond the two named sites.

## Decision ledger

Closes the wave5-repair owed work "fix the silent-soft config failure class
and the seal debt": the two named silent-soft sites are fail-loud now, and
the config-seal modified=4 red state is cleared by a named re-seal whose
note carries the per-file reasons. Decision changed: a corrupted or missing
provider roster and a missing improve.yaml now stop the seat with the file
named instead of degrading silently; the seal's "known 4" debt is retired to
modified=0 with mirrors.json churn explicitly handed to the operator as the
remaining structural item.

## Hygiene

- Scan instrument `config-hygiene.scan.py` v2 (stage `scan`, exit 0):
  - authored files (receipt, lane JSON, check py, check driver py, scan py):
    em/en dashes=0 nonascii=0 each;
  - ADDED lines only of the two edited code files (git diff -U0 vs HEAD,
    '+' lines): models/providers.py and mag/improve.py both 0 em/en dashes,
    0 nonascii;
  - config-hygiene.check.txt is EXEMPT from the 0/0 rule and reported
    (10 em/en dashes, 12 nonascii): it is a byte-faithful raw capture, and
    the dashes belong to the captured tool itself (tools/config_seal.py:70
    and :72 print em-dashes in their own FAIL/PASS lines). Scrubbing them
    would falsify raw output.
- Pre-existing em-dashes elsewhere in models/providers.py (lines 30, 362,
  414, 416, 506, 533, 539, 779+) and mag/improve.py (lines 917 through 2729)
  were in the files before this lane; none fall inside the added-line ranges.
