# MIMOSA FULL SCAN — VERDICT 20260925/26

**Verdict: FULL DEEP SCAN COMPLETED AND SEALED. The ENOBUFS compatibility-mode era is over — the scanner completed a sealed deep scan of the estate repo on attempt 2. Scan run status is honestly `inconclusive` (coverage `partial`): the repo hit Mimosa's 50,000-file source cap, and all 104 business-logic hypotheses stayed `inconclusive` candidates. No confirmed exploitable finding in estate-owned code; 5 hardcoded-credential hits are scratch/local-provider placeholders pending operator eyeball.**

Filed: 2026-09-26 ~04:15Z by the mimosa-scan-retry seat. Scope: read-only (repo untouched except this file). All numbers below come from the sealed artifacts or commands run during this ask.

---

## 1. The context being closed out

- `watch/inbox/V2.1_ITERATION_20260925.md:33` — "Mimosa full scan when the scanner's ENOBUFS clears (**two** commits landed in compatibility mode)." The brief for this ask says **three** — confirmed: the three commits at HEAD are `f846107f4` (09-25 21:11:48 -0400, THE 50 relaunch), `926b9abf1` (21:12:36, window close: salon seats), `a741defc5` (21:16:24, schtask bare-python trap). All three landed after that note; none had a full audit. 35 files changed across the three, only two of them code: `tools/duty_fuzz.py`, `tools/seed_salon.py` (`git diff --name-only a741defc5~3..a741defc5`).
- Prior audit finding preserved: `watch/inbox/SPEC_EDITS_MICKEY17_V2_20260925.md:96` — `grep -c -i ENOBUFS = 0`; "the operator-reported cause appears nowhere in the audited log." Re-verified this ask: `grep -c -i "enobufs" /c/Users/foste/.zcode/mimosa-debug.log` → **0** (log now 60,866 lines, tail 2026-09-26T03:38Z, all hook events completing `clear`/`complete`). ENOBUFS was never a confirmed cause; it was an operator-reported label. The compatibility mode that mattered was the PreToolUse hook profile (`scan-profiles.json`: `diff-only`, `maxDiffLines: 500`, `hardTimeoutMs: 1000`) — which this full scan replaces.

## 2. Scan identity and integrity

- Tool: Mimosa MCP plugin, `security_scan_start` → `security_scan_resume` → sealed result. Job `scan-job-muhucg7m-4d8d76be63673255`, depth `deep`, evidence boundary `static_only_no_runtime_execution`, verdict effect `none`.
- **Attempt 1 (03:39:34Z → 03:49:27Z, 9m53s): interrupted** — `owner_process_exited`: "background owner exited before a sealed result was recorded." No artifacts written, no stack on disk (`~/.mimosa` did not exist; plugin data dir empty; mimosa-debug.log carries only hook traffic, no deep-scan events). Not ENOBUFS — an owner-process crash, unexplained at my layer. The job's `restart-unsealed-attempt` policy allowed resume.
- **Attempt 2 (03:50:10Z → 04:10:05Z, 19m55s): completed** and passed the 10-minute mark where attempt 1 died.
- scanId: `scan-2026-09-26T04-10-04.918Z-41fc75fa84c4`
- scanDir: `C:\Users\foste\.mimosa\security-scans\project-8af8c49a6c1b0282e16b1e73\scan-2026-09-26T04-10-04.918Z-41fc75fa84c4` (outside the repo — repo stayed read-only)
- Seal digest: `sha256:6c860bebfda869ec1f71245ea10c3bc152f97c909cffe829ff3ae27b92d3232d`
- **Integrity check (run this ask, venv python `hashlib`):** all three artifact hashes in `seal.json` reproduce exactly — `scan-manifest.json` `dc6920ee…05734` ✓, `findings.json` `0a7a2b08…0f3bf` ✓, `coverage.json` `0155135c…4e70` ✓. The top-level digest is NOT sha256 of the concatenated artifact hashes (that yields `6f7e01cf…` ≠ recorded `6c860beb…`); derivation scheme unknown. Artifact-level integrity verified; digest derivation not reproduced.

## 3. Coverage — read the fine print

From the sealed `coverage.json`:

- `completeness: partial`, `runStatus: inconclusive`. **The repo hit the 50,000-file source cap: `selectedFiles: 50000, truncated: true, omittedAtLeast: 1`** — at least one file was never scanned. `readFailures: 0, parseFailures: 0`.
- Phases: threatModel partial (565 entry points, 0 principals, 670 authorization surfaces) · findingDiscovery partial (5,305 findings, 104 business-logic candidates) · validation partial (all 104 investigated, 487 queries, **all 104 returned `inconclusive`** — the openQuestions list) · pathAnalysis **completed** (36,867 functions, 59,348 call edges, 117 traces) · reporting **completed**.
- Dependencies (MCP status `dependencySummary`): 3,347 packages scanned; offline advisory DB: 41 matched packages, 121 matched advisories, 0 unknown.

## 4. Findings — the estate vs the mirrors

**5,305 total: 3,144 medium / 2,008 high / 153 low** (5,201 static-finding + 104 business-logic candidates). The bulk sits in vendored/mined third-party trees, not estate code:

- Top files: `mine/raw/agent_platform/google/adk-python/.../main-KSQARI5D.js` (481), `mine/raw/steal_protocol/robzilla1738/agentswarm/src/executor.ts` (371), `mine/raw/steal_protocol/Bradliebs/ollama-agent-harness/src/web/server.ts` (269), `mine/raw/steal_protocol/microsoft/conductor/...` (161), `reference/gstdcoin/gstdbot/...` (151). These are the clone-mined mirrors (cf. commit `a48a63d4b`, "mirror dirs gitignored … mined in place") — findings there are upstream code quality, not estate attack surface.

**Estate-owned slice (excluding `mine/`, `reference/`, `node_modules/`, `vendor/`): 219 findings — 196 high / 6 medium / 17 low.** By title: 路径穿越 (path traversal) 102 · SSRF 72 · 不安全的随机数 (insecure random) 16 · 代码注入 (code injection) 6 · 硬编码凭据 (hardcoded credentials) 5 · 疑似跨文件污点 4 · 命令注入 (command injection) 3 · XML 实体扩展 2 · 不安全反序列化 1 · 证书校验缺失 1 · plus 7 single-entry business-logic candidates (`harvest`/`post_chat`/`launch`/`destroy`/`components`/`ready` entry flags).

Top estate files: `tools/oracle_calibration.py` (7), `watch/hermes_wings/src/traj.py` (7), `scripts/wave_driver.py` (7), `watch/salon_runner.py` (6), `scripts/fetch_training_pdfs.py` (4), `models/providers.py` (4).

**The three audited commits:** `tools/duty_fuzz.py` — 1 finding (low, insecure random, line 476). `tools/seed_salon.py` — **0 findings**. The compatibility-mode backlog is clean at the code level.

**Hardcoded-credential hits (CWE-798, all high) — spot-checked this ask with literals redacted:**
- `watch/hermes_wings/src/gw_run.py:20053` → read of the line shows `"api_key": "moa-virtual-provider"` for a `moa://local` virtual provider — **placeholder, not a real secret**.
- `_alpha_multi.py:109`, `_alpha_rar_fleet.py:76`, `_cache_mine.py:52`, `_test_legibility.py:118` — root scratch files, **not spot-checked**; operator should eyeball (names suggest throwaway experiment scripts).

Sample of other estate highs (locations only, from sealed findings.json): 代码注入 at `main.py:1347`, `tools/tier_probe.py:84`, `tools/wandr_selfeval.py:2`; 命令注入 at `tools/pupeteer_gauntlet.py:558`; XML 实体扩展 at `watch/monitor_lane.py:168`, `watch/inbox/physical_computing/receipts/f6_fetch.py:133`. Spot-check of `main.py:1347`: the flagged line is an argparse `sub.add_parser("improve", help=…)` definition — no dynamic execution visible at that line; treat the CWE-95 cluster as static-heuristic until triaged.

## 5. What the operator owes next

1. **50k-file cap**: at least 1 file unscanned (likely more as the repo grows). If Mimosa exposes a source-list override, point it at the cap; otherwise accept partial as the ceiling for deep scans of this repo.
2. **Triage order**: the 5 CWE-798 hits (4 unverified scratch files) → the 3 命令注入 → the path-traversal cluster (102, mostly scripts/watch tooling). All 104 business-logic hypotheses are `inconclusive` — the proof gaps say query budget exhausted, not "secure".
3. **PreToolUse hook profile** (`diff-only`, 500-line, 1000ms) can stay as the fast gate; the deep scan is now the periodic floor, not a blocked chore. The V2.1 owed item "Mimosa full scan when ENOBUFS clears" is **discharged** — recommend marking it taken in the next LINKS/owed-register pass (this file is the receipt).
4. Attempt 1's `owner_process_exited` crash is unexplained at my layer — if it recurs on the next full scan, it's a Mimosa plugin bug to report upstream, not an estate problem.

## 6. Evidence index (commands run this ask)

- `git -C … log --oneline -8` / `log -3 --format="%h %ad %s" --date=iso` / `diff --name-only a741defc5~3..a741defc5` — commit identity + 35 changed files, 2 code.
- `grep -c -i "enobufs" /c/Users/foste/.zcode/mimosa-debug.log` → `0`; `wc -l` → 60,866.
- `security_scan_start(depth=deep, focusFiles=[tools/duty_fuzz.py, tools/seed_salon.py])` → job `scan-job-muhucg7m-4d8d76be63673255`; `security_scan_status` polls (attempt 1 interrupted `owner_process_exited`; `security_scan_resume` → attempt 2 completed, full result JSON with seal + dependencySummary).
- venv python (`.venv/Scripts/python.exe`) hashlib seal verification — 3/3 artifact hashes match; digest derivation not reproduced.
- venv python summaries of `findings.json` — severity/evidenceState/file/estate-slice/CWE-798 tables above.
- `sed -n` spot-checks of `gw_run.py:20053` and `main.py:1347` (literals redacted on output).
- Sealed artifacts: `report.md` (1.7 MB), `findings.json` (5.2 MB), `coverage.json`, `scan-manifest.json`, `seal.json` at the scanDir in §2.
