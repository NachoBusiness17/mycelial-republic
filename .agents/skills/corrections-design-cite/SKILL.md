---
name: corrections-design-cite
description: CITE the standing laws a host-side runtime design touches BEFORE it runs (law 13). Use when building anything that spawns processes, installs hooks, registers scheduled tasks, or adds per-session machinery on the operator's machine.
when_to_use: Before any host-spawning design leaves the whiteboard.
argument-hint: <design-doc-or-idea> [spawns|hooks|tasks|processes]
---

# CITE - design-time law check for host-side runtimes (law 13, 2026-09-05)

Window-swarm catch: twice in one week the standing laws existed on record and
were not consulted (the lane runtime, then the default MCP battery + steer_47
hook). Before building ANY host-side runtime, name the standing laws it
touches and either comply or write the exemption down BEFORE it runs. If
`$0` (the design) is missing, ask for the design doc or idea before citing.

Standing host laws to cite by name:

- `docker-not-desktop` - containers over host processes.
- `headless-only` - CREATE_NO_WINDOW on every spawn (also law 48).
- `one-supervisor` - never a second supervisor on the host (also law 11).

GATE (LAW-056 teeth, hard): any host-spawning design that cannot cite its
law-or-exemption is DISPUTED by default and gets culled at the next census.
No default senses; senses live in the cage; one sense, one instance
(watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md).

## Command

```bash
# pull the standing rows the design must answer to before it runs
grep -in "docker\|headless\|supervisor\|spawn" memory/law/registry.json | head -20
grep -in "one sense\|cage\|default senses" watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md | head -10
```

Final response: for the design in `$0`, one row per standing law touched -
cited-and-compliant, cited-with-exemption (exemption text included), or
DISPUTED - plus the census fate if it runs uncited.
