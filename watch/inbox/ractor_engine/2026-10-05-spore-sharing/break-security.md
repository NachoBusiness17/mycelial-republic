# SPORE SHARING - BREAK-SECURITY PASS (2026-10-05, hostile second pass on lens-security)

Target: `watch/inbox/ractor_engine/2026-10-05-spore-sharing/security.md` (5 findings).
Method: every evidence cite re-executed this sitting; falsifiers attacked head-on
where they were executable; the ask's truncated JSON recovered from the lens file on
disk (security.md is the authoritative text). No secret bodies printed anywhere.

## VERDICTS

| Finding | Verdict | One-line reason |
|---|---|---|
| F1 push publishes the private layer | CONFIRMED (strengthened) | All headline cites byte-exact; the lens UNDERCOUNTED the dirt (17 tracked tars / 2.85 GiB, not 7 / ~562 MB) and missed that three blobs bust GitHub's 100MB cap |
| F2 three permissive gate layers | CONFIRMED (strengthened) | Receipt fields byte-exact; all six fingerprints recur in a fresh dry-run (now 16 findings / 13 unique fps / 0 accepted); a FOURTH scheduled layer exists and is equally blind |
| F3 PR-writable boot law, no integrity check | CONFIRMED | Falsifier executed as the full read the lens owed: mag/rib_bus.py (274 lines) has zero verification on the load path and FAILS OPEN on corrupt gene files; sharpened by a lens miss: state/GENOME.md itself is untracked |
| F4 crons armed by documentation | CONFIRMED (strengthened) | Cites byte-exact; the falsifier's extension (read all 13 registrars) was executed here: 0 consent/funding guards in any of them; live schtasks shows the tasks Ready on this seat |
| F5 .env clean, banked content dirty | CONFIRMED (discrepancy resolved) | Census re-run byte-exact (7 rows, all .example); the lens's steps.jsonl discrepancy RESOLVED: the 4 LANE4C commits are reflog/dangling objects (d575bc1686b4's tree carries the file; zero refs do), so the push-irrelevance conclusion holds |

## F1 byte-check detail (CONFIRMED)

- `git remote -v`: `github https://github.com/NachoBusiness17/mycelial-republic.git`
  (fetch+push) plus sibling `local .../Mag-backup.git`. CONFIRMED (security.md:25-26).
- `git ls-tree -l HEAD attic/20260923_biography_rotation/biography_backup_20260825.tar`
  -> blob `6fb541750f9fa9f476a2e95d31c0987a31504c52`, size `189808640`. Byte-exact.
- LANE4C cites: line 5 (2 history-only XAI-KEY HIGH, 19 commits, 2026-08-01..09-14) ✓;
  line 42 ("the same live-shaped key is still inside a tracked tar in the current
  tree") ✓; line 49 (lan.key critical, 318 commit trees, HEAD included at audit time) ✓.
  DRIFT: "Nothing was fixed, rotated, purged, or rewritten" is LANE4C:7, not :6 as the
  lens's F1 evidence block cites (the ask's compressed JSON lumps it under 5,42,49).
- `git merge-base --is-ancestor 799ddb6feaad HEAD` -> rc=0. CONFIRMED.
- `git ls-files memory/zknot` -> 19 dated knots + LATEST.md = 20 files. Byte-exact.
  AGENTS.md:5 carries "his prompts" verbatim. CONFIRMED; memory/zknot/LATEST.md head
  shows prompt first-lines ("55 distinct first lines", session ids), so "prompt
  history" is accurate at the summary level, not full transcripts.
- `git push --dry-run github HEAD:master` re-run this sitting (rc=1):
  `! [rejected] HEAD -> master (non-fast-forward)`. CONFIRMED.
- `git merge-base HEAD github/master` rc=1; `git rev-parse --short github/master` ->
  `dc6649943`. CONFIRMED.
- `git ls-tree -r --name-only github/master | grep -icE "\.env$|\.key$|xai-|credential|secret"`
  -> 0. CONFIRMED (nothing leaked YET, on the local tracking ref's snapshot).

Corrections that STRENGTHEN F1:
1. "Seven tracked tars" is directory-scoped truth. Full census: `git ls-files | grep
   -c "\.tar$"` -> 17 tracked tar blobs, total 3,064,168,947 bytes (~2.85 GiB),
   including `attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar` blob
   `96bbe2b3` at 2,318,299,059 bytes (2.16 GiB) and
   `attic/20260923_ghost_rotation/leak_reports_pre_2026-09-16.tar` blob `caa14f9b` at
   156,631,040 bytes. The lens inventoried neither.
2. lan.key CLASS SHIFT the lens missed: `git diff-tree --name-status -r add33ba72` ->
   `D memory/tls/lan.key`; add33ba72 (2026-10-03) is ancestor of HEAD (rc=0). The key
   is NO LONGER tree-tracked (LANE4C:51's "still tracked in HEAD" was true 2026-09-26,
   stale today); `git ls-files memory/tls/` -> lan.crt only; the working-tree copy
   (1675 bytes, mtime Aug 14) is untracked. Net: a git-push spore carries lan.key via
   history only; a directory-copy spore carries it live. The lens's "reachable from
   HEAD's history" phrasing was exactly right and survives.
3. The lens's "~562MB on disk" for the 7 biography tars measures 573,194,240 bytes
   (`du -sb`) = 573.2 MB / 546.7 MiB; neither convention reads 562. Immaterial.

## F2 byte-check detail (CONFIRMED, strengthened)

- `watch/inbox/secret_gate_results/changed_20261005T075617Z.json`: mode "changed",
  scope_basis "worktree+untracked (no upstream configured)", census 18/13/5
  large_skipped, max_file_bytes 10485760, rule_counts {}, blocking_count 0. ALL
  BYTE-EXACT against the receipt.
- `tools/secret_gate.py:119-122`: `--history` defined, help "Slow; manual; never in
  the hook." CONFIRMED. Also :117-118 `--full` = "whole-tree scan (offline /
  scheduled)" and :182-183 the rotate-before-strip operator line. CONFIRMED.
- Scheduled-path check (the falsifier): `Get-ScheduledTask` action map shows the only
  secret-scanning scheduled task is `MagSecretScanWeekly` ->
  `scripts/secret_scan_weekly.py`, which runs `watch/inbox/burn_wave_20260926/
  B2_73_secret_scan.py`: scope `corpus/` + `watch/inbox/`, text files only,
  MAX_FILE_BYTES 10MB (B2_73_secret_scan.py:5-8,22). NO scheduled path runs
  secret_gate --history or --full. Lens claim CONFIRMED, with a fourth layer added
  (see A4).
- History mode RAN ONCE manually: `history_20260927T104430Z.json` -> mode "history",
  runtime_sec 3769.6, unique_findings 7079, blocking_count 21. The lens marked the
  history census OWED without noticing this receipt exists (8 days stale). Its
  runtime (~63 min) triples the lens's "minutes to ~20 min" move estimate.
- Push layer re-run this sitting (fresh `git push --dry-run`, output in session temp):
  CRED-SHAPE WARN "scanned 55 changed file(s), 16 finding(s) (0 accepted by name)";
  the fp block contains ALL SIX lens fingerprints (d2c6c6159157b588, 40e65f6f759579a0,
  d490fb12f0b36db9, c990171ad3a64390, 782dd42793948b98, aaf6377cce055a1a) plus 7 more
  unique (13 unique / 16 printed); verbatim "the push is NOT blocked (WARN-ONLY)";
  `! [rejected] HEAD -> master (non-fast-forward)`. STRENGTHENED: 6 -> 13 unique
  unaccepted fingerprints in one day.
- Per-path attribution (the lens's OWED item) now exists from the same output: the 16
  findings are 6x BEARER-TOKEN (dashboard/static/lanes/elder.md:345,
  dashboard/static/trails/elder.jsonl:38, queue/lanes/elder/surface.md:345,
  queue/lanes/elder/trail.jsonl:38, len-24 bearer shapes) + 10x OPERATOR-HOME-PATH
  (queue/lanes/research/trail.jsonl:4 and ten rows inside
  watch/inbox/ractor_engine/2026-10-05-spore-sharing/*.md). CLASS PRECISION: the push
  WARN channel is currently bearer-shaped strings and operator identity paths, NOT
  provider keys. The fp-to-path 1:1 binding was not extracted (tool JSON mode not
  run; findings list and fp block are both printed, order-preservation unverified).
- `configs/prepush_credential_baseline.json` absent (`ls` rc=2 here vs the lens's
  rc=1; same conclusion: zero accepted). `tools/prepush_credential_shape.py`
  docstring CONFIRMED: changed/staged-only scope ("a full-tree scan in pre-push is a
  gate nobody keeps") and "WARN-ONLY first landing ... flip to enforce is an operator
  call". `githooks/pre-push` credential block read: "this block NEVER exits nonzero
  (the tool may exit 1 on findings; the hook's capture never propagates it)".
  CONFIRMED at the source, not just the output.

## F3 byte-check detail (CONFIRMED, falsifier executed and did not fire)

- state/GENOME.md:10-14 (rib_bus genes, mount/inject_for), :72-73 (boot step 5, Delta
  Register), :73-75 (step 6 "fire the crons") all byte-exact.
- `git ls-files memory/rib_bus | wc -l` -> 51, incl doctrine.json +
  standing-wave.json. Byte-exact.
- THE FULL READ THE LENS OWED (mag/rib_bus.py, all 274 lines): `mount()` (:185-190)
  is a bare `_load_store` -> `json.loads` with no hash, signature, or manifest check;
  the only hashlib use is `_rib_key` at :64 (dedupe key, not integrity); `inject_for`
  (:193-214) delegates to steer_engine.compile_steer with a mount()-based fallback,
  none verifying. WORSE THAN THE LENS CLAIMED: `_load_store` :74-75 FAILS OPEN, a
  corrupt gene file returns an empty store silently, so tamper either injects (valid
  JSON) or silently drops the law (invalid JSON), never blocks. Cross-check on the
  primary path: mag/steer_engine.py `compile_steer` at :92; the +25-line window has
  zero verification terms; the file's single hash-class hit is the word "verify"
  inside a default acceptance string. Falsifier did not fire.
- `git ls-files watch/inbox/frontier_delta_register_20261003.json` -> tracked.
  CONFIRMED. X_INTEL count 16. Byte-exact.
- LENS MISS that sharpens F3: `git check-ignore -v state/GENOME.md` ->
  `.gitignore:40: state/`; `git ls-files state/` -> only
  state/NIGHT_LOOP_20261005.md. The genome itself (boot step 1, "the inheritable
  artifact") is UNTRACKED. The PR-writable law channel is precisely
  memory/rib_bus/*.json (51 files) + queue/STANDING_RAILS.md; the genome is on NO
  shared surface (see A1).

## F4 byte-check detail (CONFIRMED, falsifier extension executed)

- `ls scripts/register_*.ps1 | wc -l` -> 13; name list matches the lens exactly.
- `scripts/register_x_radar_task.ps1:8` -> `$Root = Split-Path $PSScriptRoot -Parent`;
  :17-24 -> `schtasks /Delete /TN $TaskName /F` then `schtasks.exe /Create /TN
  $TaskName /TR $Tr /SC DAILY /ST 08:00 /RL LIMITED /F`, unconditional. Byte-exact.
- `scripts/x_radar_daily.ps1:20` -> "COST LAW: the grok CLI rides a Grok Build usage
  balance. A 402 in" byte-exact.
- FALSIFIER EXTENSION (the lens's own 15-minute offer, executed here): grep
  `Confirm|WhatIf|ESTATE_FUNDED|Read-Host|\$env:` over ALL 13 registrars -> 0 hits in
  every file. No registrar fails closed; the single-file claim is now an all-13 claim.
- Live schtasks query (the lens's blind spot, partially cured): MagXRadarDaily,
  MagCensusPatrolDaily, MagFtsIndexDaily, MagGateCanaryDaily, MagSecretScanWeekly et
  al. exist with State Ready/Running (Estate LaneSupervisor, MagLabKit8765,
  MagPrivateOffice8765 Disabled). The crons are live on this seat, not hypothetical.

## F5 byte-check detail (CONFIRMED, discrepancy resolved)

- `git log --all --pretty=format: --name-only | grep -i "\.env" | sort | uniq -c` ->
  exactly 7 rows, all `.example` variants (4 .env.example, starter-kit, OnionClaw,
  configs/cloud_steering.env.example). BYTE-EXACT re-run.
- `.gitignore:19-24` (.env/.env.local/.env.*/!.env.example + providers.yaml) ✓;
  deploy/k8s/mag-secret.yaml is at .gitignore:25, not inside 19-24 (one-line drift,
  wall exists). `.gitignore:30-34` ("7 live .env values were committed in it (audit
  2026-09-30 finding #1). Untracked 2026-09-30; history left intact per operator
  (no rewrite)." + memory/trajectory/steps.jsonl) byte-exact.
- `git grep -nIE "xai-[A-Za-z0-9]{30,}" HEAD` -> exactly 2 paths:
  tests/test_gate_blocking_paths.py + watch/inbox/audit_20260926/
  GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md (paths/lines only printed; no token
  bodies). Byte-exact. `configs/secret_gate_baseline.json:39-45` acceptance
  ("fabricated documentation payload (len 59 ...)") byte-exact.
- DISCREPANCY RESOLVED (the lens's OWED item): `git log --all --oneline --
  memory/trajectory/steps.jsonl` -> zero commits in any ref (reproduced); census of
  `^memory/trajectory/` across all refs -> 0 rows. BUT `git cat-file -e d575bc1686b4`
  exists and NO ref contains it (`git for-each-ref --contains d575bc1686b4` -> empty),
  and `git ls-tree d575bc1686b4 -- memory/trajectory/steps.jsonl` -> blob
  `fe65a8659374`. So LANE4C's "4 commit(s) contain it, first d575bc1686b4" walked a
  commit set that includes reflog/dangling objects; the file IS in a real local tree,
  just not a ref-reachable one. The lens's conclusion (a git push does not carry it; a
  directory-copy spore would) HOLDS and is now object-level grounded. The bare repo
  Mag-backup.git path-log for steps.jsonl is also empty (probed via
  `git --git-dir=.../Mag-backup.git log -- path`).
- Worktree file now 57,034,311 bytes (lens read 56,695,409; live append-only ledger,
  moment drift per the B2-216 census law; not a contradiction).
- `.env` present, untracked, 6546 bytes. CONFIRMED.

## ADDITIONS (what the lens missed)

A1. THE SEED LAYER IS GIT-INVISIBLE IN BOTH DIRECTIONS. `.gitignore:40` is `state/`;
    `git ls-files state/` -> only state/NIGHT_LOOP_20261005.md. state/GENOME.md and
    state/CURRENT.md are untracked. A git push of this clone cannot leak the genome,
    and a git clone cannot regrow the boot chain: boot step 1 points at a file the
    pack does not contain. The spore recipe must therefore have TWO lists, not one: a
    dirt denylist (F1's move) AND a seed whitelist copied from the WORKTREE
    (state/GENOME.md, state/CURRENT.md), with a pre-export tripwire asserting the
    seed PRESENT and the dirt ABSENT. The failure modes are asymmetric: over-strip
    loses the genome silently; under-strip leaks keys loudly. Evidence: this file's
    F3 section. Falsifier: state/GENOME.md appearing in any ref, or a recipe
    extracting it from git history. Move: 20 min to write the two-list manifest.
A2. THREE BLOBS BUST GITHUB'S 100MB CAP, so the "which artifact trips it first" blind
    spot has a deterministic answer: hook-state_stale_baselines.tar (2.16 GiB, blob
    96bbe2b3) then biography_backup_20260825.tar (181 MiB, 6fb541750f) then
    leak_reports_pre_2026-09-16.tar (149 MiB, caa14f9b), all in HEAD's tree (`git
    ls-tree -l HEAD` this sitting). Any pack containing HEAD's tree is rejected on
    size alone, with or without --force, before any secret detection matters. That
    rejection is currently the ONLY thing standing between the estate and publication
    besides the unrelated-history non-fast-forward (F1), and it fails SAFE, not
    PRIVATE: a history-rewrite that drops only the tar paths but keeps the pack
    recipe would still be needed. Falsifier: GitHub accepting a >100MB blob, or all
    three blobs absent from the pushed refs. Move: 5 min, add a >100MB blob tripwire
    to the export gate.
A3. THE HISTORY CENSUS THE LENS OWED ALREADY EXISTS, STALE: history_20260927T104430Z.json
    (mode history, runtime_sec 3769.6, unique_findings 7079, blocking_count 21, one
    manual run 2026-09-27). The F2 move is a refresh-and-diff against this baseline,
    not a first census, and the honest runtime estimate is ~63 minutes (the receipt's
    own runtime), not "minutes to ~20 min per LANE4C:102" (LANE4C:102's 23 min was a
    DIFFERENT scanner). Falsifier: a fresh history run reporting blocking_count 0.
    Move: unchanged in kind, re-costed ~65 min.
A4. A FOURTH PERMISSIVE LAYER, ALIVE AND ADVISORY-ONLY: scheduled task
    MagSecretScanWeekly (action verified via Get-ScheduledTask) runs
    scripts/secret_scan_weekly.py -> B2_73_secret_scan.py, scope corpus/ +
    watch/inbox/, text files only, 10MB cap; it appends a beat row and prepends an
    attention alert, and blocks nothing. Beat rows: 2026-09-26, 2026-09-28,
    2026-10-05T12:08:13Z (Mondays; today critical=1 high=52246, the standing noise
    floor). Every layer in the stack is now shown to be changed-scoped, cap-limited,
    or advisory. Falsifier: B2_73 flagging a tracked tar credential (it cannot: text
    sniff + cap + scope). Move: 10 min, feed the beat row's rule_counts into the
    spore pre-export tripwire inputs.
A5. THE REF SURFACE IS WIDER THAN HEAD: `git for-each-ref --contains cd2f8e6a520d`
    -> refs/heads/env-test AND refs/purged/env-test. A namespace literally named
    "purged" carries the history-only xai credential's introduction commit, in
    addition to HEAD's ancestry. Any `git push --mirror`, or a collaborator fetching
    all refs, publishes it even after HEAD is cleaned. F1's "reachable from HEAD's
    history" is true but understated: the credential is multi-ref. Falsifier:
    refs/purged/env-test absent at push time or not containing the blob. Move:
    15 min, enumerate the full ref set in the spore recipe and mandate single-ref
    push of the fresh root, never mirror.
A6. THE RECEIPT LAYER IS SELF-LEAKING FOR A DIRECTORY-COPY SPORE: today's push WARN
    names 10 OPERATOR-HOME-PATH rows inside this very thread's receipts
    (watch/inbox/ractor_engine/2026-10-05-spore-sharing/accuracy.md:28,299;
    communication.md:15; dogfood.md:91; economics.md:11; lineage.md:67; logic.md:136;
    moonshot-2.md:47,51,169). The audit trail of the spore question embeds the
    operator's home path. Falsifier: those lines lacking C:/Users paths at read time.
    Move: 5 min, add watch/inbox/ractor_engine/ to the directory-class denylist or
    scrub at export.
A7. DATE-STAMP THE lan.key CLASSES (no verdict change): deleted from the tree by
    add33ba72 (2026-10-03, ancestor rc=0, diff-tree D), working-tree copy untracked.
    LANE4C:51 "still tracked in HEAD" is stale by 9 days as of this pass; the lens's
    "reachable from HEAD's history" is the correct present-tense phrasing. Push spore:
    history-only exposure. Directory-copy spore: live file. Falsifier: a filter-repo
    purge of the 799ddb6fe blob or re-tracking. Move: absorbed by F1's fresh-root
    export.

## Checks run this sitting (inventory)

git remote -v; git ls-tree -l HEAD (three tars); git ls-files tar census + per-blob
sizes via ls-tree loop (17 tars, 3,064,168,947 total); du -sb of
attic/20260923_biography_rotation (573,194,240); git ls-files memory/zknot (20);
git merge-base --is-ancestor 799ddb6feaad HEAD (rc=0) and add33ba72 HEAD (rc=0);
git diff-tree --name-status add33ba72 (D memory/tls/lan.key); git log --all --oneline
-- memory/tls/lan.key; git merge-base HEAD github/master (rc=1); git rev-parse --short
github/master (dc6649943); git ls-files memory/tls (lan.crt only); X_INTEL count (16);
git log --all --pretty=format: --name-only .env census (7 rows) and
^memory/trajectory/ census (0 rows); git grep -nIE xai shape HEAD (2 paths,
paths-only); git log --all --oneline -- memory/trajectory/steps.jsonl (empty);
git cat-file -e d575bc1686b4 (exists); git for-each-ref --contains d575bc1686b4
(empty) and --contains cd2f8e6a520d (env-test + purged/env-test);
git --git-dir=Mag-backup.git log -- steps.jsonl (empty); git ls-tree d575bc1686b4 --
steps.jsonl (blob fe65a8659374); TWO git push --dry-run github HEAD:master runs
(both rc=1 non-fast-forward; hook receipts changed_20261005T115947Z.json and
changed_20261005T120522Z.json created as a side effect of running them); fingerprint
block extraction from the dry-run output (token bodies masked before display);
git ls-tree -r github/master secret-name grep (0); git count-objects -vH (size-pack
14.37 GiB; 4 tmp_pack garbage warnings); git rev-list --count HEAD (880, vs the
lens's 878 at its earlier moment: census law, not differenced further); reads of
state/GENOME.md, tools/secret_gate.py:100-199, tools/prepush_credential_shape.py
(docstring), githooks/pre-push credential block, mag/rib_bus.py (ALL 274 lines),
mag/steer_engine.py compile_steer window, scripts/secret_scan_weekly.py,
B2_73_secret_scan.py head, scripts/secrets_hygiene_check.py head (scans .env files,
live-hygiene class), scripts/register_x_radar_task.ps1, scripts/x_radar_daily.ps1:20,
.gitignore, configs/secret_gate_baseline.json:39-45,
changed_20261005T075617Z.json, history_20260927T104430Z.json summary fields,
SECRET_SCAN_BEAT.jsonl (3 rows, via .venv python); registrar guard grep (13 files,
0 hits); Get-ScheduledTask inventory + action map (MagSecretScanWeekly etc.);
git check-ignore -v state/GENOME.md (.gitignore:40); head of memory/zknot/LATEST.md.
Note: a bare-`python` invocation was blocked by the seat-law hook; re-ran with
.venv/Scripts/python.exe.

## OWED / not run (carried honestly)

- tools/secret_gate.py --history fresh run: NOT executed (est ~63 min per the Sep 27
  receipt's own runtime_sec 3769.6). The Sep 27 census (7079 findings / 21 blocking)
  stands as the latest history inventory; it is 8 days stale and predates the
  lan.key deletion.
- Tar member re-extraction: NOT performed (LANE4C:108 no-secret-bodies policy). The
  tar credential claim rests on LANE4C's extraction, as it did for the lens.
- GitHub-side live state beyond the local tracking ref (dc6649943): NOT re-fetched
  this sitting; the "clean today" verdict inherits the lens's staleness risk.
- Fingerprint-to-path 1:1 binding via the tool's JSON output: NOT run; the output
  prints path-attributed findings and the fp block separately.
- Scheduler next-fire behavior for MagSecretScanWeekly: task action + beat rows
  verified; live firing not observed beyond today's 12:08:13Z row.
