# f-20 - git branch census (burn_reset_20260927 flash50)

Date: 2026-09-28. Scope: every ref listed by `git branch -a` in this repo,
local branches (refs/heads) plus remote-tracking branches under refs/remotes/local.

## Method (commands run for this census)

- `git branch -a` - the enumeration named by the ask.
- `git remote -v` - remote identity.
- `git worktree list` - explains the `+` worktree marker.
- `git for-each-ref refs/heads --sort=-committerdate --format=...` - last commit per local branch.
- `git for-each-ref refs/remotes/local --format=...` - last commit per remote branch.
- `git rev-list --left-right --count main...<ref>` per ref - ahead/behind vs main
  (first number = commits only in main, second = commits only in the branch).
- `git merge-base --is-ancestor <ref> main` per ref - merged verdict (rc 0 = merged).
- `git branch --merged main` / `git branch --no-merged main` - cross-check of the merge column.
- Stale = last commit older than 7 days (repo 7-day freshness convention, BOOT_4_7).
- Ages computed at run time against UTC now; the run moment is in the table rows' age column.

## Headline

- Local branches: 37. Remote-tracking branches (remotes/local/*, HEAD excluded): 39.
- The single git remote is `local` -> `C:\Users\foste\Documents\projects\Mag-backup.git` (filesystem backup, no network origin). `remotes/local/HEAD -> local/master`.
- `main` itself is stale: parked at 5d20144e1 2026-08-04 (age 55 days at run time).
- `master` (a4733004a 2026-08-06) is 101 commits ahead of `main` and 0 behind; the branch landscape's real fork point is master, not main.
- Merged into main: 2 of 37 local branches (one real branch, cursor/conductor-loop-epic-split, which is tip-identical to main; the other is main itself).
- Current branch mag/run-beta1-factory-build-audi-20260806T231709Z is 678 ahead / 0 behind main and holds all recent work (tip 862620665 at the run moment).
- main is an ancestor of the current branch: True.
- Remote-only branches (no local twin): run-beta1-factory-audit-20260914, wave-20260916-checkpoint3.
- Local-only branches (no remote twin): none.
- Local/remote twin refs pointing at identical shas: 36 of 37 twins; diverged twins: mag/run-beta1-factory-build-audi-20260806T231709Z.
- Worktrees: 1 main checkout (this branch) + 5 detached codex worktrees at a4733004a (master tip) + 1 salon-arena-mvp worktree on codex/salon-arena-mvp (`+` marker).
- Snapshot note: the current branch tip is LIVE - concurrent flash50 lanes commit onto it while this census runs (during this census the ahead-of-main count moved 673 -> 674 between two script runs). All numbers here are the state at this script's run moment (tip 862620665, UTC 2026-09-28T22:18:27Z); per the census denominator law they are one tree at one moment, not constants.

## Table A: local branches (37), newest first

| branch | tip | last commit | age days | ahead main | behind main | merged into main | stale (>7d) |
|---|---|---|---|---|---|---|---|
| mag/run-beta1-factory-build-audi-20260806T231709Z | 862620665 | 2026-09-28T18:16:27-04:00 | 0 | 678 | 0 | no | fresh |
| sweep/kill-list-stage1 | 6f6998c33 | 2026-09-16T18:12:14-04:00 | 12 | 199 | 0 | no | STALE |
| archive/swarm-meta-2026-08-07 | 53ce03321 | 2026-08-07T15:00:10-04:00 | 52 | 104 | 0 | no | STALE |
| mag/roadmap-v5-vast-train-dry-v5-vast_train_dry-20260806T172129Z | a4733004a | 2026-08-06T18:29:43-04:00 | 52 | 101 | 0 | no | STALE |
| master | a4733004a | 2026-08-06T18:29:43-04:00 | 52 | 101 | 0 | no | STALE |
| cursor/unify-mag-home-e2ce | 7f15f27b5 | 2026-08-06T18:29:33-04:00 | 52 | 113 | 0 | no | STALE |
| unify-mag-home | 7f15f27b5 | 2026-08-06T18:29:33-04:00 | 52 | 113 | 0 | no | STALE |
| codex/salon-arena-mvp | 1e92a7012 | 2026-08-06T13:30:45-04:00 | 53 | 85 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-v5-gstd_t0_probe-20260806T170900Z | 9c8fc49e8 | 2026-08-06T13:20:42-04:00 | 53 | 84 | 0 | no | STALE |
| mag/integration-cheap-handoff-20260806 | 343781ff7 | 2026-08-06T13:08:23-04:00 | 53 | 83 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-v5-gstd_t0_probe-20260806T164134Z | 7654afe52 | 2026-08-06T12:37:24-04:00 | 53 | 82 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-v5-gstd_t0_probe-20260806T164200Z | 7654afe52 | 2026-08-06T12:37:24-04:00 | 53 | 82 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-roadmap-v5-gstd-t0-probe-20260806T162504Z | c10559c6e | 2026-08-06T12:20:46-04:00 | 53 | 81 | 0 | no | STALE |
| cursor/dashboard-v3-base-e2ce | 91ed8ffff | 2026-08-05T13:38:56Z | 54 | 84 | 0 | no | STALE |
| cursor/canvas-platform-e2ce | 33153da81 | 2026-08-05T13:32:54Z | 54 | 82 | 0 | no | STALE |
| cursor/mesh-comm-research-e2ce | ab7da8734 | 2026-08-05T13:07:24Z | 54 | 79 | 0 | no | STALE |
| mag/run-beta1-factory-build-audi-20260806T004024Z | ab7da8734 | 2026-08-05T13:07:24Z | 54 | 79 | 0 | no | STALE |
| mag/run-beta1-factory-build-audi-20260806T004214Z | ab7da8734 | 2026-08-05T13:07:24Z | 54 | 79 | 0 | no | STALE |
| cursor/v3-deepseek-run-e2ce | 15836a058 | 2026-08-05T12:47:49Z | 54 | 69 | 0 | no | STALE |
| cursor/improve-stack-integration-468b | 28377e610 | 2026-08-05T12:11:43Z | 54 | 2 | 0 | no | STALE |
| cursor/v3-v4-research-brief-e2ce | 431144513 | 2026-08-05T11:21:20Z | 54 | 57 | 0 | no | STALE |
| cursor/v3-swarm-vision-e2ce | 8025a2062 | 2026-08-05T03:49:25Z | 54 | 55 | 0 | no | STALE |
| cursor/virtual-desk-deepseek-loop-e2ce | 622d3aa4c | 2026-08-05T02:01:03Z | 54 | 26 | 0 | no | STALE |
| cursor/mag-v2-plan-e2ce | e8d75c33c | 2026-08-05T01:10:17Z | 54 | 15 | 0 | no | STALE |
| cursor/mag-autorun-v1-e2ce | b5601f4b0 | 2026-08-05T00:32:01Z | 54 | 8 | 0 | no | STALE |
| cursor/failure-kb-e2ce | f462b3986 | 2026-08-05T00:09:08Z | 54 | 5 | 0 | no | STALE |
| cursor/unified-router-e2ce | 56d7591a8 | 2026-08-05T00:05:13Z | 54 | 4 | 0 | no | STALE |
| cursor/breadcrumbs-ui-simplify-e2ce | 4cdb2955f | 2026-08-04T23:45:43Z | 54 | 17 | 0 | no | STALE |
| cursor/intelligent-governor-autorun-e2ce | 4d4e36ce0 | 2026-08-04T23:36:50Z | 54 | 16 | 0 | no | STALE |
| cursor/deepseek-prefix-cache-e2ce | 3ecd6ce17 | 2026-08-04T22:38:21Z | 54 | 10 | 0 | no | STALE |
| cursor/setup-dev-environment-6b0b | 5dd77ea87 | 2026-08-04T21:59:19Z | 55 | 2 | 0 | no | STALE |
| cursor/distributed-surface-glue-e2ce | 63ba6f15f | 2026-08-04T21:37:36Z | 55 | 7 | 0 | no | STALE |
| cursor/resume-contract-wire-e2ce | a14dbb93f | 2026-08-04T20:10:46Z | 55 | 1 | 0 | no | STALE |
| cursor/queue-lanes-behavioral-logging | c21804ec2 | 2026-08-04T19:02:00-04:00 | 54 | 1 | 0 | no | STALE |
| cursor/conductor-loop-epic-split | 5d20144e1 | 2026-08-04T15:33:07-04:00 | 55 | 0 | 0 | YES | STALE |
| main | 5d20144e1 | 2026-08-04T15:33:07-04:00 | 55 | 0 | 0 | YES | STALE |
| env-test | 3a0059e12 | 2026-08-04T11:05:53-04:00 | 55 | 2 | 5 | no | STALE |

Merged count Table A: 2 / 37. Stale count Table A: 36 / 37.

## Table B: remote-tracking branches under remotes/local (39), newest first

| branch | tip | last commit | age days | ahead main | behind main | merged into main | stale (>7d) |
|---|---|---|---|---|---|---|---|
| run-beta1-factory-audit-20260914 | 92ff2565d | 2026-09-28T08:24:24-04:00 | 0 | 607 | 0 | no | fresh |
| mag/run-beta1-factory-build-audi-20260806T231709Z | 4c28af571 | 2026-09-19T21:53:04-04:00 | 8 | 451 | 0 | no | STALE |
| sweep/kill-list-stage1 | 6f6998c33 | 2026-09-16T18:12:14-04:00 | 12 | 199 | 0 | no | STALE |
| wave-20260916-checkpoint3 | 75c030d29 | 2026-09-16T17:57:30-04:00 | 12 | 198 | 0 | no | STALE |
| archive/swarm-meta-2026-08-07 | 53ce03321 | 2026-08-07T15:00:10-04:00 | 52 | 104 | 0 | no | STALE |
| mag/roadmap-v5-vast-train-dry-v5-vast_train_dry-20260806T172129Z | a4733004a | 2026-08-06T18:29:43-04:00 | 52 | 101 | 0 | no | STALE |
| master | a4733004a | 2026-08-06T18:29:43-04:00 | 52 | 101 | 0 | no | STALE |
| cursor/unify-mag-home-e2ce | 7f15f27b5 | 2026-08-06T18:29:33-04:00 | 52 | 113 | 0 | no | STALE |
| unify-mag-home | 7f15f27b5 | 2026-08-06T18:29:33-04:00 | 52 | 113 | 0 | no | STALE |
| codex/salon-arena-mvp | 1e92a7012 | 2026-08-06T13:30:45-04:00 | 53 | 85 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-v5-gstd_t0_probe-20260806T170900Z | 9c8fc49e8 | 2026-08-06T13:20:42-04:00 | 53 | 84 | 0 | no | STALE |
| mag/integration-cheap-handoff-20260806 | 343781ff7 | 2026-08-06T13:08:23-04:00 | 53 | 83 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-v5-gstd_t0_probe-20260806T164134Z | 7654afe52 | 2026-08-06T12:37:24-04:00 | 53 | 82 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-v5-gstd_t0_probe-20260806T164200Z | 7654afe52 | 2026-08-06T12:37:24-04:00 | 53 | 82 | 0 | no | STALE |
| mag/roadmap-v5-gstd-t0-probe-roadmap-v5-gstd-t0-probe-20260806T162504Z | c10559c6e | 2026-08-06T12:20:46-04:00 | 53 | 81 | 0 | no | STALE |
| cursor/dashboard-v3-base-e2ce | 91ed8ffff | 2026-08-05T13:38:56Z | 54 | 84 | 0 | no | STALE |
| cursor/canvas-platform-e2ce | 33153da81 | 2026-08-05T13:32:54Z | 54 | 82 | 0 | no | STALE |
| cursor/mesh-comm-research-e2ce | ab7da8734 | 2026-08-05T13:07:24Z | 54 | 79 | 0 | no | STALE |
| mag/run-beta1-factory-build-audi-20260806T004024Z | ab7da8734 | 2026-08-05T13:07:24Z | 54 | 79 | 0 | no | STALE |
| mag/run-beta1-factory-build-audi-20260806T004214Z | ab7da8734 | 2026-08-05T13:07:24Z | 54 | 79 | 0 | no | STALE |
| cursor/v3-deepseek-run-e2ce | 15836a058 | 2026-08-05T12:47:49Z | 54 | 69 | 0 | no | STALE |
| cursor/improve-stack-integration-468b | 28377e610 | 2026-08-05T12:11:43Z | 54 | 2 | 0 | no | STALE |
| cursor/v3-v4-research-brief-e2ce | 431144513 | 2026-08-05T11:21:20Z | 54 | 57 | 0 | no | STALE |
| cursor/v3-swarm-vision-e2ce | 8025a2062 | 2026-08-05T03:49:25Z | 54 | 55 | 0 | no | STALE |
| cursor/virtual-desk-deepseek-loop-e2ce | 622d3aa4c | 2026-08-05T02:01:03Z | 54 | 26 | 0 | no | STALE |
| cursor/mag-v2-plan-e2ce | e8d75c33c | 2026-08-05T01:10:17Z | 54 | 15 | 0 | no | STALE |
| cursor/mag-autorun-v1-e2ce | b5601f4b0 | 2026-08-05T00:32:01Z | 54 | 8 | 0 | no | STALE |
| cursor/failure-kb-e2ce | f462b3986 | 2026-08-05T00:09:08Z | 54 | 5 | 0 | no | STALE |
| cursor/unified-router-e2ce | 56d7591a8 | 2026-08-05T00:05:13Z | 54 | 4 | 0 | no | STALE |
| cursor/breadcrumbs-ui-simplify-e2ce | 4cdb2955f | 2026-08-04T23:45:43Z | 54 | 17 | 0 | no | STALE |
| cursor/intelligent-governor-autorun-e2ce | 4d4e36ce0 | 2026-08-04T23:36:50Z | 54 | 16 | 0 | no | STALE |
| cursor/deepseek-prefix-cache-e2ce | 3ecd6ce17 | 2026-08-04T22:38:21Z | 54 | 10 | 0 | no | STALE |
| cursor/setup-dev-environment-6b0b | 5dd77ea87 | 2026-08-04T21:59:19Z | 55 | 2 | 0 | no | STALE |
| cursor/distributed-surface-glue-e2ce | 63ba6f15f | 2026-08-04T21:37:36Z | 55 | 7 | 0 | no | STALE |
| cursor/resume-contract-wire-e2ce | a14dbb93f | 2026-08-04T20:10:46Z | 55 | 1 | 0 | no | STALE |
| cursor/queue-lanes-behavioral-logging | c21804ec2 | 2026-08-04T19:02:00-04:00 | 54 | 1 | 0 | no | STALE |
| cursor/conductor-loop-epic-split | 5d20144e1 | 2026-08-04T15:33:07-04:00 | 55 | 0 | 0 | YES | STALE |
| main | 5d20144e1 | 2026-08-04T15:33:07-04:00 | 55 | 0 | 0 | YES | STALE |
| env-test | 3a0059e12 | 2026-08-04T11:05:53-04:00 | 55 | 2 | 5 | no | STALE |

Merged count Table B: 2 / 39. Stale count Table B: 38 / 39.

## Findings

1. Stale landscape: 36 of 37 local branches and 38 of 39 remote branches are older than 7 days. The only fresh local ref is the checked-out flash50 bulk branch itself.
2. main is not the trunk: it holds 0 commits that master lacks while master is 101 ahead of it, and main never moved after 2026-08-04. The active lane mag/run-beta1-factory-build-audi-20260806T231709Z is 678 commits ahead of main with main fully contained (main is an ancestor of it: True); recent work lands there, main never moves.
3. Only cursor/conductor-loop-epic-split is merged (tip-identical to main at 5d20144e1). Every other branch, including master, is unmerged into main.
4. The remote is a local-path backup mirror: every one of the 37 local branches has a remote twin, and 36 twins are sha-identical; diverged twins: mag/run-beta1-factory-build-audi-20260806T231709Z. The backup's twin of the current branch (4c28af571) is 227 commits behind / 0 ahead of the local tip 862620665 - the backup lags today's work.
5. Two branches exist only in the backup: run-beta1-factory-audit-20260914 and wave-20260916-checkpoint3 - local work not present as local refs here. run-beta1-factory-audit-20260914 is not dormant: its tip 92ff2565d is dated 2026-09-28T08:24:24-04:00 (age 0 at run moment, the only fresh remote row) and sits 607 commits ahead of main / 0 behind; the backup is still receiving pushes today while this checkout has no local ref for it.
6. Sibling-branch duplicates: the three mag/run-beta1-factory-build-audi-* branches and unify-mag-home vs cursor/unify-mag-home-e2ce share tips (see tables), i.e. duplicate pointers, not divergent work.

