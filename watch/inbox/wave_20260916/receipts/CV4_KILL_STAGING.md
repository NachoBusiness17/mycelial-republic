# CV4 KILL STAGING — wave_20260916

Lane law: STAGE ONLY. Deletions commit on `sweep/kill-list-stage1` (created from current HEAD). Nothing lands on the previous/current branch tip — the merge is the human gate.

Source of kill list: `watch/inbox/TRIAGE_MEMO_20260916.md` — safest first bite = `_`-prefixed Aug-25 probe files (~22).

## Progress log

- [x] Read memo, extract safest list
- [x] Record starting branch + HEAD
- [x] Create branch `sweep/kill-list-stage1`
- [x] Zero-import verification per file (whole-repo grep); pull + record any with imports
- [x] Remove verified-zero-import files on sweep branch
- [x] Targeted regression: wow family + link_library (`pytest tests -q -x`)
- [x] Smoke: `./.venv/Scripts/python.exe -m mag.shared_surface validate || true` (result recorded either way)
- [x] Commit on sweep branch; switch back to previous branch
- [x] Final block: removed count + list, test results verbatim, branch name, accept/discard commands

---

# FINAL — CV4 KILL STAGING

## Files removed: 21 of the memo's 22 (1 pulled)

**Staged deletions committed on sweep branch (20 tracked files, `git show --stat`: `20 files changed, 1001 deletions(-)`):**

1. `mag/_bench_free_shelf.py` (59)
2. `mag/_cache_ab_probe.py` (64)
3. `mag/_comb_tokens.py` (84)
4. `mag/_compare_chain_sources.py` (31)
5. `mag/_deep_research_verkle_dedupe.py` (63)
6. `mag/_diag_cache.py` (11)
7. `mag/_gpu_probe_debug.py` (39)
8. `mag/_grok_corpus_burn.py` (103)
9. `mag/_openclaw_real.py` (19)
10. `mag/_probe_dangling.py` (29)
11. `mag/_probe_mcp.py` (36)
12. `mag/_probe_zai_balance.py` (51)
13. `mag/_relane_game_tasks.py` (44)
14. `mag/_salon_burn.py` (96)
15. `mag/_verify_concurrency_gate.py` (49)
16. `mag/_verify_queue_gate.py` (80)
17. `mag/_verify_repair_state.py` (16)
18. `mag/_verify_rung5.py` (50)
19. `mag/_verify_sharp_edge.py` (59)
20. `mag/_warm_rib.py` (18)

**Removed from working tree only (was UNTRACKED — no git record possible):**

21. `mag/_fold_vision.py` (13) — bytes quarantined FIRST at `watch/inbox/wave_20260916/cv4_quarantine/_fold_vision.py`; sha256 `2aaca5cede79dd5dd533018d692027672bd9eb085c39a9a6b096f05ce6f2f437` (verified identical to original).

**PULLED from the memo's list (still on disk, untouched): `mag/_verify_chain_now.py`** — `audit_prep/READING_PATH_1HR.md:13` documents a live run command `.\.venv\Scripts\python.exe mag\_verify_chain_now.py`; the memo's E3 sweep did not cover `audit_prep/` (its blind spot #1). Documented invocation ⇒ not trivially safe to delete. Re-triage it with that doc.

## Test results (verbatim)

Targeted regression — `./.venv/Scripts/python.exe -m pytest tests/test_wow_bones.py tests/test_wow_bones_session.py tests/test_wow_family.py tests/test_wow_manifest.py tests/test_wow_player.py tests/test_wow_world.py tests/test_link_library.py -q -x` (run on the sweep-branch working tree with deletions applied):

```
88 passed in 2.15s
PYTEST_EXIT=0
```

Smoke — `./.venv/Scripts/python.exe -m mag.shared_surface validate || true`:

```
"schema": "shared_surface.status.v1",
"ok": false,
VALIDATE_EXIT=0   (module exit masked by `|| true`; JSON verdict above)
```

`ok:false` cause (first errors, verbatim): `INDEX root is 'C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox', expected '/board/inbox'` + hundreds of `indexed item missing: /board/...20260901...` and `hash mismatch:` entries — all 2026-09-01-era INDEX drift. **Pre-existing, not caused by this lane:** the validated surface is `watch/inbox`; the removed modules live in `mag/` (outside it), and the only surface files this lane added are this receipt + the quarantine copy.

## Branch

- Sweep branch: **`sweep/kill-list-stage1`** — commit `6f6998c3353a6803a7798b9f360f3e87788ab549`, parent `75c030d296a5` (current tip of `mag/run-beta1-factory-build-audi-20260806T231709Z`).
- Current branch after work: `mag/run-beta1-factory-build-audi-20260806T231709Z` (untouched; nothing landed on it). Untracked-removed `_fold_vision.py` remains absent from the working tree even after switch — by design, see discard path.

## Operator gate — EXACT commands

ACCEPT (delete the 21 for real):

```
git merge sweep/kill-list-stage1
```

DISCARD (restore everything):

```
git branch -D sweep/kill-list-stage1
cp watch/inbox/wave_20260916/cv4_quarantine/_fold_vision.py mag/_fold_vision.py
```

(The `git branch -D` alone restores the 20 tracked files; the `cp` restores the one untracked file — that is why it was quarantined with a verified sha256 before removal.)

*Nothing was committed to `mag/run-beta1-factory-build-audi-20260806T231709Z`. All 21 removals verified zero-import by whole-repo word-boundary grep prior to staging; the only references found were catalog/estate/audit index rows, audit-snapshot copies, trajectory logs, and memo-adjacent prose. Interpreter used throughout: `.venv\Scripts\python.exe`.*

## 2026-09-16 — starting state

- Previous/current branch: `mag/run-beta1-factory-build-audi-20260806T231709Z` @ `75c030d296a5d5c3d34ad466d92d81e3f0a51b39`
- Dirty working tree: 24 entries, NONE under `mag/_*.py` (dashboard trails, memory/percolator, queue lanes, training events, watch receipts — unrelated; will not be staged)
- Memo safest list = rows 1–22 (22 files, `mag/_*.py`, mtime stratum 2026-08-10…2026-08-27). All 22 verified present on disk; `wc -l` matches memo per-file exactly (sum 1046).

## Zero-import verification (whole-repo grep, per file)

Method: `grep -rIlw "<module>" .` (word-boundary) over the entire repo excluding `.git/.venv/__pycache__/node_modules`, per each of the 22 names. All hits classified by path:

- **Index/telemetry only (PASS, all 22):** `catalog/catalog.jsonl` (corpus + dist_audit index rows), `dist_audit/nacho_business_audit_20260912T214050Z/` (shipped audit snapshots incl. full file copies), `dashboard/data/ESTATE_INDEX.jsonl`, `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`, `watch/audit/FULL_AUDIT_20260908/audit_records.json`, `memory/trajectory/steps.jsonl`, `memory/thinking/app_reasoning.jsonl`, memo probe outputs `watch/inbox/wave_20260916/d24_*.json`. These list filenames/history; none is live code.
- **Eyeballed 4 non-index hits:**
  - `_probe_mcp` → `watch/salon_ocean_20260831/row_hand.md:11`: prose stating the probe is unused, "zero MCP traffic ever". PASS.
  - `_relane_game_tasks` → `watch/inbox/FREE_TIER_AUDIT_20260906.md`: independent audit, "One-shot 08-25 patch script", no external importer (it is itself the only importer of `free_tier.status`). PASS.
  - `_verify_chain_now` → `audit_prep/READING_PATH_1HR.md:13` documents a live run command `.\.venv\Scripts\python.exe mag\_verify_chain_now.py` (also echoed in historical transcript `watch/inbox/desktop_bundle_20260901/wow.txt:3165`). **PULLED from staging list** — documented invocation path; memo's E3 sweep did not cover `audit_prep/` (memo blind spot #1). Deleting it is not trivially safe.
- **Zero hits in any live code:** no `mag/*.py` importer, `main.py`, `mag_launch.py`, `scripts/`, `tests/`, `docs/`, `configs/`, `queue/`, dashboard/backend code, root manifests. Self-hits only inside `mag/_grok_corpus_burn.py` / `mag/_salon_burn.py` themselves.

**Result: 21 of 22 cleared → staged. 1 pulled (`mag/_verify_chain_now.py`, reason above).**
