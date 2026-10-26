# accuracy.md - ractor lens: accuracy (2026-10-03 grokbot-estate run)

Lens: accuracy (falsifier-hunter; jacket: the verdict consumed without its
conditions). Subject: Grok Bot's 10/3 ET findings and plans. Method self-stolen
from watch/inbox/ractor_engine/2026-10-02-dogfood-48h/ (SYNTHESIS.md,
security.md, break-security.md) and .zcode/workflows/ractor-engine.dwf.ts:88-129
(lens library, QUANTIFIER LAW). Every check below was run this sitting
(18:35-18:50 ET) on host 5c18da76 unless marked OWED. Verdicts on Grok Bot's
claims: TRUE / FALSE / THEATER / UNVERIFIED (STALE = was true, tree moved).

## Findings

A1. Import crash at mag/health.py:26 via powershell_exe() in the Linux cage. TRUE.
mag/health.py:14 imports mag.win_powershell at module top; :25-27 evaluates
CAGE_DOCTOR = powershell_exe() at import; mag/win_powershell.py:30-43 raises
FileNotFoundError when shutil.which and both C:\Windows candidates miss.
git blame -L 25,27 mag/health.py = 48f7f5ace, 2026-09-26 17:43:49 -0400.

A2. "Every janitor run since 9/26 crashes." TRUE (scoped). Instrument: parse of
memory/runs/orchestrator/tasks/*.json (6,457 files), created_at >=
2026-09-26T21:23Z, tag copilot-auto-fkb*: 375 receipts, 375 failed. Log
signature census over logs/orchestrator/<task_id>.out.log: 374 "powershell.exe
not resolvable", 1 the earlier win_powershell import form. Last container
"done" receipt: 2026-09-26T09:01:12Z (05:01 ET). Plan's "373" is STALE by tree
churn (two more janitor spawns since).

A3. read_only=True default (3752abae2) strips writes. TRUE, secondary.
mag/orchestrator.py:640; mag/ghost.py:1124-1128 calls spawn_task with no
read_only; 3752abae2 = 2026-09-25 23:42:10 -0400.

A4. "Knots every run at ghost.py:1506." TRUE, and worse than stated. The fold
runs immediately after exec_copilot returns (ghost.py:1472), when outcome is
"spawned", before the child has run; then a bus event typed
"autonomous_task_completed" is published (ghost.py:1515-1521). Whole chain:
819 rows with session_id prefix autonomous- (python census of
memory/biography/verkle_chain.jsonl). verkle_tip.json now names
autonomous-auto-fkb-632d09, the knot of failed task t57a5a3a9e1.

A5. Plan fix (a) "gate the fold on outcome done plus output file existing".
FALSE as written. At ghost.py:1483-1506 the only outcomes are spawned /
spawn_failed (ghost.py:1129); "done" is not knowable at that site. The gate
must move to task completion (orchestrator task end), or the fold never fires.

A6. Backfill 2,154 knots = 2,108 dwf + 45 real. TRUE within 3 rows. Rows
appended since the first 10/3 backup (bak-orphanlane-20261003T205738Z, 9,046
rows) to now (11,203): 2,157 = dwf- 2,109 (includes the 18:16 ET boot-lane
test knot), other 45, autonomous- 3.

A7. Filter bug cause. TRUE. git diff mag/knot_at_close.py: --skip-subagents
drops only task_type == "subagent_child"; scripts/verkle_boot_view.py:41
records dwf- actors as task_type=workflow_child, which the filter keeps.

A8. knot_at_close.py +28/-2 with backup .bak-20261003. TRUE. git diff --stat
= 28 insertions, 2 deletions; git hash-object of the .bak = 36ce22a55 = HEAD
blob. (Its 09/07 mtime is copy2 metadata, not a defect.)

A9. "About 17 orphanlane .bak copies." FALSE (count). Get-ChildItem
memory/biography -Filter verkle_chain.jsonl.bak-orphanlane-*: 25 total
(165,800,928 B), 18 created 10/3 (129,621,240 B). All gitignored
(.gitignore:63 memory/biography/**).

A10. verify_verkle_full.py "0 mismatches, 53 dangling". TRUE, reproduced
live: rows 11,203, leaf mismatch 0, dangling 53, prefix root/parent/n_leaves
mm 0, linkage break 0, tip ok, exit 0, 7.0 s (script is read-only without
--json, scripts/verify_verkle_full.py:4-5).

A11. memory/tls/lan.key "untracked (staged)". FALSE / STALE. Not staged:
git diff --cached is empty. It was COMMITTED in add33ba72 (author Codex,
2026-10-03 16:42:35 -0400) together with the 22-line .gitignore block
(+# grok-bot estate audit 2026-10-03), under a commit message about D&D
self-steal that names neither. git ls-files memory/tls = lan.crt only;
git check-ignore = .gitignore:278 memory/tls/*.key.

A12. "59-char xai- token" as a leak. THEATER. tests/test_gate_blocking_paths.py
:212-219 is the _SYNTHETIC fixture dict; :215 reads "Values are fabricated;
entropy is real. Never place a real key here." Length 59, same sha256 prefix
131CC67D0D10 in watch/inbox/audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md:20
(a worked example). Realness cannot be proven without an authenticated call
(not made: no paid/auth calls), so "real" stays UNVERIFIED, but the bytes
declare it synthetic. Value never printed.

A13. Port 8765 rebound to 127.0.0.1. TRUE and already live. git diff
docker-compose.yml (one line, ports block); Get-NetTCPConnection: 127.0.0.1:8765
and :8001 pid 26172; docker inspect mag-sovereign created
2026-10-03T20:40:52Z (16:40 ET), restarts=0: the container was recreated
today. Who ran the recreate: UNVERIFIED.

A14. CURRENT.md stale. TRUE. state/CURRENT.md mtime 2026-10-02 08:51 ET.

A15. kpi.jsonl 790 MB unrotated. TRUE. 790,310,798 B at 18:39 ET; Get-ChildItem
logs -Filter kpi* lists only kpi.jsonl (scope: logs/ only).

Tally (this lens): TRUE 11, FALSE 3 (A5, A9, A11), THEATER 1 (A12), UNVERIFIED 0.

## Quantifier lint (engine fix 2) applied

"Every run" (A2) is scoped to orchestrator receipts on disk; "0 mismatches"
(A10) is scoped to verify_verkle_full's rule set; "no rotation sibling" (A15)
to logs/; A3 "never passes read_only" is scoped to ghost.py:1124 only (other
exec sites in ghost.py not read).

No em-dash bytes. Filed by the accuracy lens.
