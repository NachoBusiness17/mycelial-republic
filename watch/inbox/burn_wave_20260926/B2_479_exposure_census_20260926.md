# B2-479 receipt: reset-day exposure census for the modified files (2026-09-26)

## Verdict

LANDED as census + scoped commit + named exposure. Census at ~21:4xZ: 1,134 uncommitted paths (207 tracked M, 925 untracked ??, 1 D, 1 RM; the 143 at 19:02Z grew through the afternoon lanes). The landed-not-committed criticals are now HELD BY A REF: scoped commit 6d417abd5 on branch mag/run-beta1-factory-build-audi-20260806T231709Z carries 18 files (durable ledgers + this lane's landed code), pre-commit sha table filed at B2_479_exposure_shas_20260926.txt. models/providers.py (B2-445 spec block) could NOT be committed because models/ is .gitignore'd (line 26) - registered as exposure-by-name. The remaining ~1,111 paths are registered by class, not committed: concurrent lanes' hot files, and the bulk-untracked receipts/static/runs debris that survive checkout and die only under clean -fd.

## Evidence file:line quotes

- Census (git status --porcelain, this lane): 1,134 paths = 925 ?? + 207 M + 1 D + 1 RM; branch mag/run-beta1-factory-build-audi-20260806T231709Z.
- watch/inbox/burn_wave_20260926/B2_479_exposure_shas_20260926.txt: 17 sha256-head + path rows taken BEFORE the commit (byte-verification table per the brief).
- Commit 6d417abd5 stat: "18 files changed, 3644 insertions(+), 151 deletions(-)" including memory/burns/LEDGER.jsonl, watch/inbox/index_events.jsonl, memory/trajectory/steps.jsonl, configs/violation_baseline.json, githooks/pre-push, mag/{health,improve,lifecycle,window_audit}.py, mag/win_powershell.py, tools/{drift,cascade_falsifier_run,census_collect,census_drift_patrol,checkbox_receipt_gate,seed_rib}.py.
- .gitignore:26: "models/" (why models/providers.py is exposure-by-name).
- Receipt pointer: watch/inbox/burn_wave_20260926/QUEUE.md restore-guard law (whole-file restores are the write class that skips claim detection; commit 6d417abd5 is the counter-measure for the reset-day checkout class).

## Work done

1. Census: full porcelain class count plus targeted status for the landed-work candidates (ledgers, mag code, tools, configs, hook).
2. Recorded pre-commit sha256 heads for all 17 commit candidates (B2_479_exposure_shas_20260926.txt).
3. Scoped commit 6d417abd5: durable append-only ledgers (LEDGER, index_events, trajectory steps) + violation_baseline + the burn lanes' landed code files, message naming every brief id covered. Post-commit verified via git show --stat.
4. Exposure-by-name registrations: models/providers.py (B2-445 policy block; gitignored path, add -f deliberately not used to respect the ignore law - a models/ ignore policy change is its own decision); concurrent-hot files left to their lanes (mag/shared_surface.py mid-edit above the ratchet cap; configs/lanes.yaml + configs/.config_seal.json + configs/keys.json carry other lanes' uncommitted edits; tools/openrouter_free_gate.py, tools/transport_precheck.py, tools/queue_dupes_check.py carry NEW ratchet debt from in-flight lanes); class-level: ~900 untracked paths are dashboard static output, .mimosa machinery, runs/agent_state debris, and the burn receipts themselves (untracked receipt files survive a checkout; their mass backup is the ESSENTIALS pack per watch/inbox/ESSENTIALS_RESTORE.md, not git).
5. Operational note: found and removed a stale zero-byte .git/index.lock (48 min old, no git process) before committing; a live concurrent git.exe appeared during the commit window and the commit was retried after its lock released (interleave-safe: lock-wait loop).

## Falsifier

The census dies if: (a) a reset-day `git checkout -- .`/`git reset --hard` after this commit loses bytes any receipt claims landed - impossible for the 18 committed files (ref-held at 6d417abd5, sha table pre-committed) but still possible for the exposure-by-name set, which is exactly why they are named here rather than silently left; (b) the sha table disagrees with the committed blobs (git show 6d417abd5:<path> must hash to the table's head); (c) models/providers.py is lost to a clean -f'd models/ removal (the ignore is the exposure; a future lane should either move the spec block into a tracked file or revisit the ignore).

## Bibliography closed

All read this lane: git status/branch/show/log (censuses), .gitignore (line 26), watch/inbox/burn_wave_20260926/B2_479_exposure_shas_20260926.txt (written this lane), watch/inbox/ESSENTIALS_RESTORE.md (mass backup surface), QUEUE.md B2-479 row + restore-guard law text, tools/restore_guard.py (audit arm), watch/inbox/burn_wave_20260926/B2_108_commit_gate_20260926.md (pointer).
