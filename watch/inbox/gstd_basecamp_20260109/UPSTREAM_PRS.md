# UPSTREAM_PRS.md - gstdbot public submission lane (2026-10-08)

Operator order: submit 3 PRs + 1 issue publicly to github.com/gstdcoin/gstdbot
from live-node dogfood evidence. Account NachoBusiness17. All four artifacts
are pushed publicly to the fork. PR and issue CREATION on the upstream repo
was attempted and is blocked by the account's fine-grained PAT (403 "Resource
not accessible by personal access token", both GraphQL and REST; account has
pull:true / push:false on gstdcoin/gstdbot, so no co-founder branch push
either). Per orders: banked, not faked. Everything a maintainer or an account
with rights needs is public and one click away (compare links below). The
submission bodies are also committed verbatim on the fork branch
`upstream-proposals` under `proposals/`.

Base for all branches: origin/main e0bbe4851b9c4ddcc0dd9956a8f258e8c1320280
(verified in sync with local main before branching).

## PR 1 - fix(router): L1 response cache collides on shared message prefixes

- Branch: fix/l1-cache-key-collision (fork commit b18df32)
- Public: https://github.com/NachoBusiness17/gstdbot/tree/fix/l1-cache-key-collision
- One-click PR: https://github.com/gstdcoin/gstdbot/compare/main...NachoBusiness17:gstdbot:fix/l1-cache-key-collision
- Body: `proposals/PR_l1_cache_key.md` on fork branch upstream-proposals (copy in /tmp/gstd_proposals on this seat)
- Files touched: src/gateway/router.ts (key on sha256(model + full normalized
  message), model resolution hoisted above the L1 lookup), new
  src/gateway/router.test.ts (6 tests)
- Evidence verified on main: makeKey at src/gateway/router.ts lines 147-150
  keyed on first 200 chars of last user message, no model dimension
- Test outcome: before fix 4 failed / 2 passed (both collision classes +
  both regression tests red); after fix 6/6 green; full suite 92 tests /
  11 files green on this branch; tsc --noEmit clean
- Hygiene grep (UQ / trycloudflare over staged diff): 0 hits

## PR 2 - fix(gateway): task sampling params dropped before inference

- Branch: fix/task-sampling-params-dropped (fork commit b3aeefc)
- Public: https://github.com/NachoBusiness17/gstdbot/tree/fix/task-sampling-params-dropped
- One-click PR: https://github.com/gstdcoin/gstdbot/compare/main...NachoBusiness17:gstdbot:fix/task-sampling-params-dropped
- Body: `proposals/PR_task_sampling_params.md` on fork branch upstream-proposals
- Files touched: src/gateway/server.ts (push handler accepts + forwards
  temperature/max_tokens, drop site was the JSON.stringify body at the
  ollama call), src/core/platform-link.ts (poll fallback path, same fix),
  src/core/platform-link.test.ts (+3 tests with global fetch stub)
- Note: the swarm path (SwarmAgent.processInference) and /v1/ollama/completions
  already forwarded these fields; only the M4 push + poll paths dropped them
- Test outcome: before fix the forwarding test failed (temperature undefined
  in backend body); after fix 8/8 green in the touched file; full suite 89
  tests green on this branch; tsc --noEmit clean. Push-handler half covered
  by curl repro in the PR body (server module not unit-bootable in isolation)
- Hygiene grep: 0 hits

## PR 3 - security(gateway): authenticate POST /api/v1/tasks/push

- Branch: security/task-push-auth (fork commit 6e940df)
- Public: https://github.com/NachoBusiness17/gstdbot/tree/security/task-push-auth
- One-click PR: https://github.com/gstdcoin/gstdbot/compare/main...NachoBusiness17:gstdbot:security/task-push-auth
- Body: `proposals/PR_task_push_auth.md` on fork branch upstream-proposals
- Files touched: new src/gateway/task-push-auth.ts (GSTD_TASK_PUSH_SECRET,
  X-GSTD-Task-Push-Secret header, sha256-then-timingSafeEqual constant-time
  compare, fail-closed on malformed headers, open + startup warn when unset),
  new src/gateway/task-push-auth.test.ts (6 tests), src/gateway/server.ts
  (guard + one-time startup warning)
- Endpoint evidence on main: src/gateway/server.ts line 4568, no auth of any
  kind; also honors caller-supplied platform_url for the completion callback
  (noted in body as follow-up hardening, not fixed here to keep the diff
  minimal)
- Test outcome: 6/6 green; full suite 92 tests / 11 files green on this
  branch; tsc --noEmit clean. Fails-before is inherent-new-module; behavioral
  curl check documented in body
- Hygiene grep: 0 hits

## ISSUE 4 - rate limiting behind tunnels/proxies

- Type: issue draft, no code
- Body: `proposals/ISSUE_rate_limit_behind_tunnels.md` on fork branch
  upstream-proposals (copy in /tmp/gstd_proposals)
- Evidence verified on main: src/gateway/server.ts lines 452-480, key is
  req.ip || req.socket.remoteAddress, RATE_LIMIT 120 / 60000ms, and express
  trust proxy is never configured anywhere in the repo (grep: zero
  app.set("trust proxy") hits), so all tunneled traffic shares one bucket
- Body includes the observed effective throughput note (~1 request per
  10-15s during scanner waves) and the proposals: opt-in TRUST_PROXY=1,
  identity-based buckets for machine endpoints, /health exemption,
  Retry-After
- Hygiene grep: 0 hits

## Submission state (banked)

- Fork created: https://github.com/NachoBusiness17/gstdbot (gh repo fork, clone=false)
- Branches pushed to fork: fix/l1-cache-key-collision,
  fix/task-sampling-params-dropped, security/task-push-auth,
  upstream-proposals (docs-only, carries the 4 bodies + index README)
- Blocked upstream-side with this PAT: gh pr create (GraphQL and REST, 403),
  gh issue create (GraphQL, same class), direct branch push to origin
  (push:false). Probe issue text never landed anywhere
- To finish with a rights-capable token: gh pr create --repo gstdcoin/gstdbot
  --head NachoBusiness17:<branch> --title <see commit subject> --body-file
  <body from proposals/>, then gh issue create --repo gstdcoin/gstdbot with
  ISSUE_rate_limit_behind_tunnels.md
- Diff hygiene across all four commits: zero UQ / trycloudflare hits; no
  wallet address, no tunnel URL, no internal estate path in any public body
  or commit; docker-compose.override.yml + .mimosa/ never staged (git status
  on main after all work shows both still untracked)
- Coordination note (PR1 + PR2): PR 2 does not change the router.route()
  signature, so no temperature/max_tokens dimension was needed in the PR 1
  cache key; the two PRs are independent and merge in either order

## Toolchain notes

- npm ci ran in the clone (655 packages) to get vitest 5.0.3; node v22.23.1
- Repo-local git identity set: NachoBusiness17 / NachoBusiness17@users.noreply.github.com
  (repo config only, not global)
