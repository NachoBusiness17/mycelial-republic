# hermes docs b2 wing 03 (docs/cron-doctor-spec.md)

via seat-b1 beat ext-4acb567c10 folded=True

The file is a requirements specification, not code — it contains no implementation, so (1) and (2) cannot be answered from code.

1. WHAT IT DOES
The document specifies a new read-only subcommand, `hermes cron doctor`, that summarizes cron job health by checking active jobs for six named conditions: last run failure, last delivery failure, missing `next_run_at`, `no_agent` enabled without a script, script path missing or outside `HERMES_HOME/scripts`, and configured workdir missing. It must exit 0 when healthy and 1 when issues exist, and requires parser, dispatch, and test coverage.

2. DESIGN PATTERNS
None can be named from code — no code exists in this file. The only structural conventions visible are spec-level: an acceptance-criteria list driving exit codes, and an explicit non-goals section.

3. RISKS
Single point of failure: none identified; the doc is descriptive. Hidden mutation of shared state: none — the spec explicitly forbids mutating jobs, auto-repair, and gateway start/stop, and forbids inspecting or printing secrets. Duplicate scheduler: none; the command is diagnostic only and introduces no scheduling of its own. The stated exit-code contract (0 healthy / 1 issues) is the only observable behavior this file commits any implementation to.
