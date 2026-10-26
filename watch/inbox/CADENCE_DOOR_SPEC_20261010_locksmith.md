# CADENCE DOOR SPEC: five organs built for the nightly lane, zero mounted (locksmith, 2026-10-10)

Status: SPEC ONLY, awaiting operator mount decision. Nothing here runs until the
operator mounts it. This file is the law-13 design-cite pass for that mount.
Author seat: THE LOCKSMITH, mission_20261010_02 (receipt:
watch/inbox/mates_leave_protocol/receipts/receipt_20261010_locksmith.md).

## The doors (all verified this cycle, bytes not vibes)

| Organ | Promise | Verified state this cycle |
|---|---|---|
| tools/meters_nightly.py:11 | "one line in the estate's daily task (e.g. MagImproveDaily)" | mounted on 0 of 24 Mag tasks; wraps estate_smith_chart --no-plot, curvature_scan, lattice_build + autoseal register |
| tools/pricing_diff.py:13 | "cron-ready, one line in the estate's daily task (same pattern as tools/meters_nightly.py)" | ran 2x by hand (09-22, 09-27) then never; anthropic extractor silently broken 09-27..10-10 (page reshaped to a two-row header); fixed + tested this cycle, 4-provider dashboard restored (exit 0) |
| tools/memory_gauge.py:1 | "nightly memory gauge" | 4 rows ever, all 09-22/09-27; the 10-06 knowledge_graph rebuild (new module: ids, nodes 1695 -> 2938) went unread until this cycle's manual run |
| tools/provider_snapshot_differ.py:1 | reads the two newest provider_health snapshots so lane flips stop needing a human | never ran; first run this cycle banked 2 unseen flips: nous ALIVE -> QUOTA-DEAD, z_ai3 DEGRADED -> DORMANT (snapshots 2026-09-26 -> 2026-10-04) |
| tools/rotate_kpi.py:1 | keeps logs/kpi.jsonl rotated (790 MB crisis 2026-10-03) | ran 1x by hand (attic/kpi one archive, 126.8 MB, 10-04 06:56); regrew to 17,688,381 bytes / 1,002 rows by 10-10; dry run ok:true this cycle (--apply is the operator's line per its own docstring) |

Box cadence census: 24 Mag scheduled tasks exist (22 enabled); none runs any of
the five. The pattern organ the others name (meters_nightly) is itself unmounted.

## Proposed mount (operator decision)

Follow the existing registration pattern (template: scripts/register_fts_index_task.ps1,
headless via scripts/run_hidden.vbs wscript //B //Nologo), one new daily task or
append to scripts/improve_daily.ps1, after 09:15 to run after MagFtsIndexDaily:

```
.venv\Scripts\python.exe tools\meters_nightly.py
.venv\Scripts\python.exe tools\pricing_diff.py
.venv\Scripts\python.exe tools\memory_gauge.py
.venv\Scripts\python.exe tools\provider_snapshot_differ.py
.venv\Scripts\python.exe tools\rotate_kpi.py --apply
```

Each is $0 (no API calls except pricing_diff's public docs fetches), each
self-registers its output into watch/inbox/index_events.jsonl (pricing_diff and
meters_nightly do; memory_gauge appends to watch/inbox/MEMORY_GAUGE.jsonl).

## Law-13 design-cite rows (corrections-design-cite)

- docker-not-desktop: CITED-WITH-EXEMPTION. The mount extends the estate's
  existing host-process daily-task fleet (24 Mag tasks already host-process);
  containerizing meters is a different design and out of scope here. No new
  runtime class is introduced.
- headless-only (also law 48): CITED-AND-COMPLIANT. Every proposed line rides
  the existing run_hidden.vbs pattern (wscript //B //Nologo), same as
  MagFtsIndexDaily / MagCensusPatrolDaily. No new window class.
- one-supervisor (also law 11): CITED-AND-COMPLIANT. No second supervisor: the
  jobs join one existing daily script behind one existing scheduled task; no
  new supervisor process or daemon.
- Egress (Mimosa PreToolUse constraint, 2026-09-22): CITED-AND-COMPLIANT.
  pricing_diff self-enforces https-only, host allowlist, public-IP pinning,
  per-hop redirect re-validation (tools/pricing_diff.py:61-97).
- Senses topology (watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md): CITED-AND-
  COMPLIANT. All five are meters/writers, not senses; no MCP surface touched.

Uncited host-spawning designs get DISPUTED and culled at census (LAW-056 gate).
This spec is the citation; the operator's mount decision completes it.

## What this cycle already did WITHOUT mounting (safe, in-repo)

- Ran all four non-apply organs once by hand; outputs banked (receipt COUNTS).
- Fixed pricing_diff anthropic two-row header + HF prose-tolerance; 5 new tests
  tests/test_pricing_diff_anthropic.py all pass; today's CSV has 4 providers.
- rotate_kpi left at dry run; --apply stays the operator's call per its docstring.
