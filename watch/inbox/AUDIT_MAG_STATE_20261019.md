# AUDIT_MAG_STATE_20261019

- class: RECEIPT
- writer: grok-bot executor (read-only audit)
- audited_at: 2026-10-19T11:36-15:00 America/New_York (UTC-4)
- HEAD: f77a55470ca2ccb3b74e7b48e0728b48ed676904
- repo: C:\Users\foste\Documents\projects\local_sovereign_agent
- machineId: 5c18da76-268a-457c-9ed3-4c3a990b9d6c
- rules: no writes to repo except this receipt; no .env/secret contents read; no recursive Get-ChildItem over repo; no process kill/suspend/resume; no chain_repair; no verkle_lock taken by this audit
- box scratch: /workspace/mag-audit-20261019/

## Summary (top findings)

1. **Signed prefix is NOT byte-identical.** Live chain first 8,619,201 bytes do not match sealed candidate sha256 `0da8026d...` (root `ab595c33...`). Live prefix has 12,009 of 12,016 rows changed: 24 leaf rewrites (all `amended=True`, mostly on 2026-10-17) plus 11,985 root-only rewrites cascading from those. Live tip root is `eb336df9...`, n=13,135. Full verifier still reports OK=True (internal consistency only; it does not check the sealed restore prefix).
2. **Suspend/pause posture is gone.** All 28 recorded Windows lab PIDs are dead (host reboot 2026-10-19 00:14 ET). Container `mag-sovereign` was restarted multiple times; current lab is container PID 13, state **R** (running), not STOP. Mag launch log shows lab respawns on 10-17 14:15 ET, 10-18 02:29 ET, 10-19 00:16 ET, 10-19 07:54 ET.
3. **~1,119 appends after the 12,016 prefix** (live 13,135). Dominant writers: mag-agent-orc re-knots (854, of which 830 reuse prefix session_ids; 649 filenames dated 2026-08), law empty rows (135), autonomous-janitor/fkb (93, stopped after 10-17 17:40Z after ghost Linux fkb guard), memlang (22), uuid-session (8). Empty/null-theme rows: 463/1119. After `chain_mode: v2` (configs/mag.yaml, 2026-10-17 15:17 ET) new re-saves append `.sN.knot.json` instead of rewriting leaves (matches 10-18/19 wave).
4. **CURRENT.md claims mostly hold on unit tests, but surface/seal drifted.** Named pour tests: claim_drift 48 pass + 1 skip (matches 48/49), canon_boot 51/51, desktop_mode 28/28, archive_guard 10/10, systems-check suite 38+4+2+10=54/54. CONFIG-SEAL now FAIL: mirrors.json modified (1 of 72). shared_surface dry rebuild: 1,668 top-level files, 3 stale (claimed 1,641 / 0 stale). Skills dir has 45 entries; the archival/roster batch of 12 exists.
5. **Cookie-pull artifacts on disk (gitignored).** `tools/chrome_cookie_pull.py` tracked (commit e9a3b72a4); untracked `tools/chrome_cookie_pull.ps1`; output `memory/runs/x_church_campaign/x_cookies.json` (4,268 B) plus four `ck_Profile_*.db` copies and ~1.8 GB of chrome profile clone dirs. Names/sizes only; contents not opened. Tip witness daily still exit 2 (gist scope).

## Full verify result

Command (live estate, no `--json`, no lock): `.venv\Scripts\python.exe scripts/verify_verkle_full.py`

```
rows=13135 checked=13135 no_leaf_hash=0 leaves=13135 bad_json=0
leaf_hash: ok=13125 mismatch=0 dangling=10 unreadable=0 (file!=row 0; attic=0 diary_nodes=0)
prefix: root ok=13135 mm=0 | parent ok=13135 mm=0 | n_leaves ok=13135 mm=0 | naive xcheck bad=[]
linkage: ok=13135 break=0
tip: tip_root eb336df92b30b21e ... tip_n_leaves 13135 ... ok True
OK=True runtime=11.73s
```

`mag/_verify_chain_now.py`: chain_rows=13135, dangling=10, evidence_lost_flags=618 (inherited), tip_root=eb336df92b30b21e, tip_leaves=13135, last_row_ts=2026-10-19T12:12:12.226958Z. Chain sha256 before/after verify unchanged: `d887ccc223c97b311da2c91a4f08ad0252a754ebed0daddd605e665654f522b3`.

Prefix seal check (box copy of live vs `/workspace/mag-archaeology-oct/restore/candidate_verkle_chain.jsonl` and `%TEMP%\magrestore\candidate\...`, both sha256 `0da8026d...`): first 8,619,201 bytes DIFFER (byte 5185 / line 8). Live root at index 12015 = `7fe9285a...`, sealed root = `ab595c33...`. Seal companion `CHAIN_RESTORE_20261015.chain.json` / `.seal` key_id `de5fc05e962c43ab` still present; they certify the fixed restore file, not the moving live tip.

## Writer breakdown (rows index >= 12016; n=1119)

| Date (UTC) | Count | Notes |
|---|---|---|
| 2026-10-16 | 46 | memlang first append 15:59Z; janitor + law |
| 2026-10-17 | 117 | janitor continues to 17:40Z; 1 amended append (uuid mag .knot) |
| 2026-10-18 | 839 | mag-agent-orc 747 (re-knot wave after lab up at 06:29Z) + law 80 |
| 2026-10-19 | 117 | mag-agent-orc 107 + mag-other 7 + uuid 3; tip theme mag_hands |

| Writer class | n | empty (theme null) | also in prefix sessions | Window |
|---|---|---|---|---|
| mag-agent-orc | 854 | 300 | 830 | 10-18 06:29Z to 10-19 12:05Z |
| law | 135 | 135 | 0 | 10-16 to 10-18 15:55Z (`mag/law.py`) |
| autonomous (fkb janitor) | 93 | 0 | 0 | 10-16 16:13Z to 10-17 17:40Z (`mag/ghost.py` auto-fkb) |
| memlang | 22 | 22 | 0 | 10-16 to 10-18 (`mag/memlang.py`) |
| mag-other | 7 | 3 | 7 | 10-19 04:16Z |
| uuid-session | 8 | 3 | 0 | 10-17 to 10-19 |

Themes on appends: None 463, biography 349, mag_hands 152, autonomous_janitor 93, constitution 28, mirror_meta 12, ... Duplicate session_ids among appends: 32 sessions. amended=True among appends: 1 (row 12132). index contiguous True; n_leaves ok.

Process / job context (read-only):
- Suspended list `%TEMP%\magarch\suspended_lab_pids_20261016.txt`: 27/28 gone; PID 21456 alive but is Discord.exe (PID reuse after reboot), not lab.
- No host `main.py lab` currently running. Stealth driver IS running (PIDs 4976/17236, `scripts\run_stealth_driver.py` since 00:23 ET) and is the known dry chain_repair lock taker.
- mag-sovereign lab PID 13: State R. Ghost PID 12 State S (with uncommitted Linux fkb guard in `mag/ghost.py`).
- Scheduled: MagChainBackupDaily last 03:15 ET ok; MagTipWitnessDaily last exit 2; mag-docker-watchdog only relaunches Docker Desktop, not containers; MagLawPackDaily last 09:36 ET.

## CURRENT.md spot-check (claim vs measured)

| Claim | Measured | Match? |
|---|---|---|
| Pour2 claim_drift 48/49 | pytest tests/test_claim_drift_patrol.py: 48 passed, 1 skipped | YES |
| Pour3 canon 51/51 | test_canon_boot.py: 51 passed | YES |
| Pour4 desktop 28/28 | test_desktop_mode.py: 28 passed | YES |
| archive_guard 10/10 | test_archive_guard.py: 10 passed | YES |
| 54/54 unit tests (systems check suite) | shared_surface 38 + contract_widening 4 + root_temp 2 + archive_guard 10 = 54 passed | YES |
| CONFIG-SEAL sealed=72 | verify: sealed=72 live=72 **modified=1** (mirrors.json) missing=0 unsealed=0 FAIL | NO (drift since seal) |
| 0 root orphans / surface | dry rebuild: invisible=[], missing=[], **stale=3**, top_level_files=**1668** (claim 1641 / 0 stale) | PARTIAL |
| 12 skills in .agents/skills/ | archival/roster batch of 12 present; total skill dirs = **45** | PARTIAL (batch exists; total higher) |
| SHARED_SURFACE_CONTRACT / PROMOTION_LEDGER at repo root | live under `watch/inbox/`; schema shared_surface.v2; ledger 11 rows | path claim imprecise |
| git status ~1787 | porcelain 1787 = ??1522 + M245 + D20 | YES |

pytest run used conftest live-estate write fence + PYTHONDONTWRITEBYTECODE=1 + `-p no:cacheprovider`; git status hash before/after identical (`7E0118E20ABC0688`).

## Uncommitted changes (porcelain 1787)

| Top-level | total | ?? | M | D |
|---|---|---|---|---|
| watch/ | 1246 | 1201 | 37 | 8 |
| memory/ | 136 | 81 | 55 | 0 |
| queue/ | 70 | 48 | 22 | 0 |
| (root) | 52 | 36 | 6 | 10 |
| tools/ | 51 | 21 | 30 | 0 |
| tests/ | 48 | 36 | 12 | 0 |
| scripts/ | 41 | 37 | 4 | 0 |
| mag/ | 39 | 18 | 21 | 0 |
| dashboard/ | 30 | 3 | 27 | 0 |
| other | ~74 | | | |

Risky / notable (names only):
- Secrets-looking: `tools/chrome_cookie_pull.ps1` (untracked); several `*secret*` / `*token*` receipt names under watch/inbox (scan results / cards, not opened).
- Large untracked: `dashboard/static/index_data/ESTATE_INDEX.jsonl` (~506 MB), `memory/biography_v2/chain_v2.jsonl` (~22 MB), `memory/mesh/index_history/...` (~118 MB), PDFs under canon/, Spell.dbc ~28 MB.
- Deleted tracked: 8 gala_20260925 grokbot lane JSONs under watch/inbox; plus path-corrupted Temp/UsersfosteAppDataLocalTemp* entries (look like accidental absolute-path commits).
- Core modified (not deleted): mag/verkle_knot.py (+29 net with ignore-space; append-leaves AH19), mag/ghost.py (fkb Linux guard), configs/mirrors.json (breaks seal), state/CURRENT.md, tests/conftest.py.

Note: `git ls-files --others --exclude-standard` expands to ~18,140 paths (gitignore does not hide everything porcelain collapses); porcelain entry count remains 1,787.

## Security note (factual)

| Path | Size | mtime (ET) | Status |
|---|---|---|---|
| tools/chrome_cookie_pull.py | 4,191 | 2026-10-18 12:43 | tracked in e9a3b72a4 |
| tools/chrome_cookie_pull.ps1 | 5,707 | 2026-10-18 12:38 | untracked |
| tools/cdp_eval.js | 2,289 | 2026-10-18 12:25 | tracked |
| memory/runs/x_church_campaign/x_cookies.json | 4,268 | 2026-10-18 12:44 | present; gitignored (`memory/runs/**`) |
| memory/runs/x_church_campaign/ck_Profile_1.db .. _4.db | 1.8M / 2.8M / 950K / 41K | 2026-10-18 12:41 | present; gitignored |
| chrome_clone / chrome_clone_p1 / clone_team_0 / clone_team_1 | ~1.86 GB combined, thousands of files | 2026-10-18 | present under same runs dir |

Contents of cookie JSON/DBs and profile clones were **not** opened. Risk: DPAPI-decryptable cookie material and full profile clones sit on disk under the estate tree (ignored by git, still local-disk exposure).

## Today's receipts vs measured

| Receipt | Claim / risk | Measured |
|---|---|---|
| DRIFT_PATROL_20261019.md | fleet healthy; mag-browser new; Church campaign 30s login; geometric_probe env-key debt; no chain mention | mag-browser Up confirmed; **silent on** lab STOP loss, prefix rewrite, cookie dumps on disk |
| STEALTH_SWEEP_LATEST.md | 1 free wall fire ok | no contradiction; shared_surface marks this file **stale** vs INDEX hash |
| THE_ONE_MAP_20261019.md | "all containers (auto-restore from any reboot)"; Org System V2 "192 tests, receipts filed"; X login as decision item | auto-restore **contradicts** the 10-16 "writers stay paused" posture (lab came back running after reboot); Org System V2 named suites total 67+ for pours, not 192 (map may count broader); X login note is operational fact, not content critique |
| CURRENT.md (10-18) | CONFIG-SEAL PASS; surface 1641/0 stale | **FAIL** mirrors.json; surface 1668 / 3 stale |

## Findings table

| # | Finding | Evidence | NEW/KNOWN | Severity | Staleness | Suggested next step |
|---|---|---|---|---|---|---|
| 1 | Sealed 12,016-row prefix no longer byte-identical; 24 leaf rewrites + cascade of 11,985 root rewrites; live root at 12015 is 7fe9285a not ab595c33 | cmp live vs candidate; analyze1/2.py; CHAIN_RESTORE_20261015.md certifies 0da8026d / ab595c33; daily bk_20261018 already matches live prefix (rewrites done by 10-18 03:14Z backup) | NEW vs sealed 10-16 tip; KNOWN class of in-place amend (CHAIN_RESTORE step 9 / Oct 16 pause reason) | high | sealed state source 2026-10-16; verified-at-HEAD 2026-10-19: **broken** | Decide: re-seal a new certified tip, or restore candidate again under lock after stopping writers; keep amends on v2 append-leaves only |
| 2 | Suspended Windows labs gone; container lab PID 13 running (R), not STOP; host reboot 2026-10-19 00:14 ET | suspended_lab_pids check; docker top + /proc State; mag_launch.log spawn lines; Win32 LastBootUpTime | NEW (posture lost) | high | CHAIN_RESTORE "writers stay stopped" 2026-10-16; verified-at-HEAD: **not held** | Re-STOP lab (or remove lab from mag_launch spawn list) until operator accepts running appends; document reboot as suspend-killer |
| 3 | ~1,119 post-prefix appends; 854 are mag-agent-orc re-knots of old sessions (830 also in prefix); 463 empty/null-theme | analyze3/4/5.py on live chain copy | KNOWN unidentified appenders (janitor/law/memlang) STILL-OPEN; NEW volume/shape for orc re-knot wave after chain_mode v2 | medium | janitor noted CHAIN_RESTORE 2026-10-16; verified: janitor last row 10-17 17:40Z then stopped (ghost fkb Linux guard in uncommitted mag/ghost.py) | Confirm v2 is intended for orc re-knots; optionally filter empty law/memlang from knot_at_close; commit ghost fkb guard |
| 4 | chain_mode v2 set 2026-10-17 15:17 ET; leaf rewrites on 10-17 were before that flip; after flip appends use .sN.knot | configs/mag.yaml line; leaf rewrite timestamps 12:06-18:42Z 10-17; tip last_filename ...e77af8c5.s3.knot.json | NEW (migration landed) | medium | AH19_AMEND_PERF.md prior; verified-at-HEAD: live mode v2 | Keep v2; ensure all writers load policy the same way; commit pending mag/verkle_knot.py AH19 hunk |
| 5 | Full chain verifies OK=True (internal) but that does not prove sealed-prefix integrity | scripts/verify_verkle_full.py output | KNOWN verifier behavior; NEW observation that OK=True coexists with broken seal prefix | medium | restore verify 2026-10-16 OK=True on sealed file; verified-at-HEAD: live OK=True, prefix mismatch | Extend verifier with optional `--expect-prefix-sha256 0da8026d...` or compare to seal companion |
| 6 | CONFIG-SEAL FAIL: mirrors.json modified | tools/config_seal.py verify | NEW drift today (mtime 11:45 ET; seal file mtime 08:04 ET) | medium | CURRENT.md claim PASS 2026-10-18; verified-at-HEAD: FAIL | Re-seal with named update after reviewing mirrors.json diff, or revert mirrors.json |
| 7 | shared_surface: 1668 top-level, 3 stale (ORPHAN_CENSUS, STEALTH_SWEEP_LATEST, STEALTH_MINED_FINDINGS); validate errors on new event keys | mag.shared_surface rebuild --dry / validate | NEW vs CURRENT 1641/0 stale | low | CURRENT 2026-10-18; verified-at-HEAD: drifted | Dry-known: run rebuild (non-dry) when approved; register new event keys |
| 8 | Cookie pull tool + dumps + ~1.8GB profile clones on disk under memory/runs/x_church_campaign/ | paths/sizes listed above; .gitignore memory/runs/**; commit e9a3b72a4 | NEW on-disk persistence (tool existence known from commit message) | high (local secret exposure) | commit 2026-10-18; verified-at-HEAD: files still present | Operator: delete or vault-encrypt x_cookies.json + ck_Profile_*.db + clone dirs if no longer needed; treat chrome_cookie_pull as seat-key tool |
| 9 | MagTipWitnessDaily exit 2 (gist scope) since at least 10-18 | logs/tip_witness.log | KNOWN/STILL-OPEN | low | tip_witness log 2026-10-18/19; verified still exit 2 | Fix PAT gist scope or disable task until credential fixed |
| 10 | Stealth driver running; known to take verkle_lock via chain_repair --dry | process list; CHAIN_RESTORE 2026-10-16 note | KNOWN/STILL-OPEN | medium | 2026-10-16; verified-at-HEAD: driver alive | Make chain_repair --dry lock-free, or exclude from stealth while chain is under audit |
| 11 | ~1787 uncommitted; watch/ dominates; large binaries; corrupted Temp path deletions | git status --porcelain summary | KNOWN backlog shape; NEW count snapshot | medium | context said ~1787; verified 1787 | Fold/commit receipts separately from large binaries; scrub accidental Temp path deletes |
| 12 | DRIFT_PATROL_20261019 / THE_ONE_MAP omit chain posture and cookie-disk risk; map claims containers auto-restore (conflicts with pause intent) | receipt text vs measurements above | NEW contradiction | medium | receipts dated 2026-10-19; verified same day | Next drift patrol: add chain prefix-seal check + lab STOP check; map section 1 should not imply pause-bypass is desired without a decision |

## Explicitly not re-raised (closed / out of scope)

- 9/30 key purge, 191.8M figure, closed GAP_REGISTER rows, instance guard: not revisited.
- Strike the Chord / Church campaign **content**: not critiqued. Only operational/security facts (cookie tool, dumps, 30s login window as stated in existing receipts).
- Dangling=10 and evidence_lost_flags=618: inherited from restore; still present; not new.

## Methods note

- Live chain copied to box for offline analysis; PC live sha256 rechecked after verifiers.
- No `.env`, no key files, no cookie JSON/DB contents, no profile clone file contents read.
- No recursive repo Get-ChildItem; used rg and targeted paths.
- No chain_repair; no verkle_lock acquisition; no process state changes.
