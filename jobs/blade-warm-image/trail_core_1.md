# trail_core_1 — blade-warm-image

Memlang token resolved to this contract (`action=route`, spec job_id blade-warm-image).

- **completed:** Dockerfile.blade + warm_preload.sh + WARM_BLADE_RUNBOOK.md. Registry `models` on the three ollama plants so preload can loop pulls at runtime. No docker commands, no snapshot, no instances, no covenant edits.
- **artifacts:**
  - docker/Dockerfile.blade
  - docker/warm_preload.sh
  - docs/WARM_BLADE_RUNBOOK.md
  - state/vast/blade_templates.json (models arrays)
- **failures:** none on acceptance
- **budget_used_pct:** 0
- **next_action_one_line:** OPERATOR-GO to build/snapshot; then fill `warm_image` on eligible templates

## Handoff
- **done:** files+docs; preload reads registry at runtime; status.json boot/pull/READY for boot_watcher
- **untested:** docker build, vast snapshot, live boot from warm image
- **blocked:** snapshot spends — operator GO
- **resume_command:** grok#1: read jobs/blade-warm-image/seat_contract.json + latest trail_core, do next_action, run acceptance, write trail_core_N
