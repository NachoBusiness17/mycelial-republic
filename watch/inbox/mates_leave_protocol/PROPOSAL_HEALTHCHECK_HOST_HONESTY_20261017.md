# PROPOSAL: make the mag-sovereign healthcheck honest about the host door

Filed by: innkeeper mate, cycle 10, 2026-10-17. Decision owner: operator.
Status: PROPOSAL ONLY. Nothing in docker-compose.yml was touched.

Search terms: healthcheck healthy but door dead, publishes dropped restart,
in-cage probe blind spot, host canary 8765, docker ps false comfort, compose
line 115, B7 comment block.

## The problem, in one breath

Two cycles in a row (2026-10-14, 2026-10-16) `docker ps` reported mag-sovereign
"healthy" while every host-facing door it promises was dead for a stranger:
all four publishes (:8765, :8000, :8001, :9000) dropped at the 2026-10-16
restart, GET :8765/ timing out from the host. The stranger sees a dead page;
the dashboard of record sees "healthy". The healthcheck is telling the truth
about the cage and silence about the porch.

## Why the current probe cannot see the disease (the constraint, honestly)

The healthcheck (docker-compose.yml lines 115-120) runs INSIDE the cage and
probes http://127.0.0.1:8765/ in-cage. Docker has no mechanism for an in-cage
probe to test a host-side publish binding; the port-publish table lives in the
host's docker-proxy, outside the container's network view. So "probe a host-
reachable surface" is not achievable from inside the cage, and no compose-only
one-liner fixes this. The honest fix lives on the host side.

## Proposed fix (two parts)

Part 1, the real cure: a host-side door canary. One small PowerShell script
(curl http://127.0.0.1:8765/ with a short timeout; on failure append one line
to memory/attention.md naming the port and the moment) run by a scheduled task
every 15 minutes. This is the only instrument that can see a dropped publish
the way a stranger does. Cost: one script file, one task registration, one log.
Sketch (not landed, for the operator to judge):

  $r = curl.exe -s -o NUL -w "%{http_code}" --max-time 5 http://127.0.0.1:8765/
  if ($r -ne "200") { Add-Content memory/attention.md ("DOOR CANARY: :8765 returned " + $r + " at " + (Get-Date).ToUniversalTime().ToString("o")) }

Part 2, the doc-honesty patch: extend the existing B7 comment block above the
healthcheck (compose lines 108-114) with two lines stating the probe's blind
spot: "This probe is in-cage only. It cannot see a dropped host publish.
Host-side door verification lives in the dashboard how-to, section 6." Cost:
two comment lines, zero behavior change.

## Evidence base (all measured, receipts on the shelf)

- 2026-10-16 receipt (cycle 9): all four publishes dropped at 01:25:10Z restart,
  docker port empty, 6 GETs failing, container "Up 11 hours (healthy)".
- 2026-10-17 re-census (this cycle): doors still dead (4 GETs, all 000),
  docker port still empty, same single StartedAt 2026-10-16T01:25:10Z,
  container still "(healthy)", ghost portproxy rule still on the porch.
- Proven cure sequence: docker-compose.yml comment lines 41-59 plus
  watch/inbox/HEADED_WINDOWS_CURED_20261005.md (admin shell: delete the
  portproxy rule, then docker compose up -d mag; proven 2026-10-05).

## What this proposal does NOT do

- It does not run the cure (admin + operator-owned).
- It does not edit docker-compose.yml (operator-owned; proposal only).
- It does not add a new always-on poller without the operator's yes: the
  canary is proposed at 15-minute cadence, one line per failure, silent on
  success.
