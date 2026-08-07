# Lifecycle REST (passive efficiency) — 2026-08-06

GET  /api/v1/lifecycle
POST /api/v1/lifecycle/reconcile  {\"dry_run\": true|false}
Alias: GET /api/v1/power/lifecycle
Also nested under GET /api/v1/power → lifecycle glance

Rule: core local always when stack on; remotes/drainer/improve off unless work.
