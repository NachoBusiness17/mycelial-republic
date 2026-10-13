# trail_core_1 — vast-templates-redo

- **n:** 1
- **job_id:** vast-templates-redo
- **completed:** template registry + buyer pick() behind existing gates. No instances. No covenant edits. buyer_enabled remains false.
- **artifacts:**
  - state/vast/blade_templates.json (7 templates)
  - state/vast/blade_buyer.py (load_templates / pick_template / create_instance uses tpl)
  - tests/test_blade_templates.py
- **failures:** none on acceptance. Library docker/onstart Unresolved (Vast template API dump did not return those hash bodies). Library vram: PRO 6000 S = 97887 MB from live bundles; H200/B300 GB Unproven (0).
- **budget_used_pct:** 0 (files+code; GET /template/ and /bundles/ reads only)
- **next_action_one_line:** operator GO to flip buyer_enabled after reading registry; do not auto-arm.

## Handoff
- **done:** registry + selection code + tests green
- **untested:** live create_instance with a non-default template (forbidden this job)
- **blocked:** library one-click image/onstart not in templates API dump
- **resume_command:** grok: read jobs/vast-templates-redo/seat_contract.json + latest trail_core, do next_action, verify acceptance_commands, write trail_core_N
