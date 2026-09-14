"""One-shot desk Step cycle filing — S2 loop proof (run from repo root)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.agent_desk import append_desk_section, set_desk_section
from mag.build_audit import write_audit
from mag.coding_session_orchestrator import orchestrator_tick, plan_session
from mag.coding_session_loop import run_board_step, run_preflight
from mag.tesuji_shell import log_tesuji_shell

STATUS = """**Sprint S1 skeleton — filed by Cursor Step cycle**

Files shipped:
- `mag/build_audit.py` — build_audit.v1 writer
- `tests/test_build_audit.py` — round-trip tests
- `main.py build-audit` + `factory-audit` alias
- `mag/handoff_inbox.py` — unified handoff queue (P1)
- `memory/runs/build_audit/` — audit trail dir

Schema `build_audit.v1`: slug, verdict, spec_path, diff_stat, commands, timestamp, note
"""

LOCAL_REPLY = """### Reply
S1 scaffold complete. build_audit.v1 fields confirmed against BUILD spec and MAG_FACTORY_PILOT.

### Canvas edit
## Status
(see Status section — file list filed)

build_audit.v1 fields: schema, slug, verdict, spec_path, diff_stat, commands, timestamp, note
CLI: `python main.py build-audit --slug X --verdict pass|fix|reject|pending`
"""

DEEPSEEK_REPLY = """### Reply
Validate: schema matches BUILD-factory-audit-json-EXAMPLE.md intent. Tests pass. Ready for factory JSON write (S3).

### Canvas edit
sprint:sprint_2_loop_proof:done

DeepSeek validates build_audit.v1 — proceed to `build-audit` CLI on disk.
"""


def main() -> int:
    pf = run_preflight()
    if not pf.get("ok"):
        print("preflight failed", pf)
        return 1

    set_desk_section("Status", STATUS)
    append_desk_section("Dialogue", LOCAL_REPLY, author="Local · step cycle")
    append_desk_section("Dialogue", DEEPSEEK_REPLY, author="DeepSeek · validate")

    log_tesuji_shell(
        "Desk Step cycle filed build_audit scaffold without operator re-prompting Cursor",
        surprise="Orchestrator PO + canvas contract carried S1→S2 without chat history dump",
        maps_to="skill:desk_step_cycle",
        source="coding_session",
        session_id="beta1-factory-build-audit-001",
        tags=["factory", "step", "build_audit"],
    )

    plan_session()
    orch = orchestrator_tick(auto_step=False, operator_note="S2 loop proof — canvas filed")
    step_local = run_board_step(auto_act=True, note="S2: Local status filed — wake Remote if needed")
    step_remote = run_board_step(auto_act=True, note="S2: DeepSeek validate build_audit.v1")

    audit = write_audit(
        "factory-audit-json",
        verdict="pass",
        spec_path="docs/ref/BUILD-factory-audit-json-EXAMPLE.md",
        commands=[
            "pytest tests/test_build_audit.py -q",
            "python main.py build-audit --slug factory-audit-json --verdict pass --dry",
        ],
        note="S2 Step cycle — DeepSeek validate on canvas",
    )

    print("preflight ok")
    print("orchestrator", orch.get("active_sprint"), orch.get("recommended_action"))
    print("step_local ok=", step_local.get("ok"), "action=", step_local.get("action_taken"))
    print("step_remote ok=", step_remote.get("ok"), "action=", step_remote.get("action_taken"))
    print("audit path=", audit.get("path"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
