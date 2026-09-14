# ROW — verify_vast_templates

- **pointer:** /mag/jobs/vast-templates-redo/ (seat_contract.json, trail_core_1.md); artifacts: state/vast/blade_templates.json, state/vast/blade_buyer.py, tests/test_blade_templates.py
- **claim:** Replaced the single hand-rolled ollama/qwen3:8b onstart with a TEMPLATE REGISTRY so blades boot into configurable templates (7 templates + buyer pick() behind existing gates; no instances; buyer_enabled stays false).
- **type:** verify-check
- **confidence:** H (byte-level corroboration); overall PARTIAL because executable acceptance could not run on this host
- **status:** PARTIAL

## Evidence (1 line per check)

1. `/mag/jobs/vast-templates-redo/` exists and holds exactly `seat_contract.json` + `trail_core_1.md` (drive=desktop:grok1, opened 2026-08-29) — matches job dir claim.
2. trail_core_1.md claims registry + buyer pick() + 7 templates + no-instances + buyer_enabled false, and honestly flags library image/onstart as Unresolved and H200 GB as Unproven — coherent, non-overclaiming.
3. `state/vast/blade_templates.json` exists (5247 B, Aug 29 08:26): `grep -c '"name"'` = 7; every one of the 7 entries contains name/image/onstart_cmd/env/port/vram_gb — exactly the claimed "7 templates".
4. Registry content: default `qwen3-8b-ollama` (image ollama/ollama:latest, port 11434, vram 10) matches the old single onstart; 4 non-blade `vast-lib-*` entries have `blade_eligible:false` + empty image/onstart with explicit Unresolved notes — honest sourcing, no invented fields.
5. `state/vast/blade_buyer.py` exists (14833 B) and has `load_templates()`/`pick_template()` wired into create_instance via `tpl.get("image"/"env"/"onstart_cmd")` — registry drives the boot; replaces hand-rolled onstart.
6. `tests/test_blade_templates.py` exists and asserts required fields, default=qwen3-8b-ollama (port 11434), and VRAM fit — matches JSON default.
7. `mag/blade_plan.py` TEMPLATES const also points at `state/vast/blade_templates.json` — consistent wiring.
8. Acceptance-command file paths all resolve: `.venv/Scripts/python.exe`, `state/vast/blade_templates.json`, `state/vast/blade_buyer.py`, `tests/` (`-k template` matches test_blade_templates.py) — all real.
9. EXEC BLOCKER: `.venv/Scripts/python.exe` (the interpreter in all 3 acceptance commands) fails to launch on this host with `WSL UtilBindVsockAnyPort:309 socket failed 1` (>5 attempts). No system python present. Bytes verified without interpreter, but executable acceptance (ast.parse + pytest) could not be completed here.

## Notes

- No instance created, no covenant edit, buy_enabled stays false — invariant respected per bytes + trail.
- Re-run acceptance on a host that can launch `.venv/Scripts/python.exe` to close the PARTIAL gap (cmd1 TEMPLATES OK, cmd2 buyer parses, cmd3 pytest -k template).
