"""Minimum-token pack for Grok (this TUI) — never full chat."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT
from mag.constants import PACK_STALE_DAYS

VALID_PACK_MODES = frozenset({"janitor", "route", "build", "audit", "plan", "full"})
PACK_OFFLOAD_FILE = ROOT / "watch" / "inbox" / "PACK_OFFLOAD.jsonl"


def _dirac_loop_count() -> dict[str, Any]:
    """Dirac visor: closed/total independent loop count for the context pack."""
    try:
        from mag.dirac_loop import BANKED_FILE, rank

        total = int(rank().get("dirac_loops") or 0)
        if BANKED_FILE.is_file():
            closed = sum(1 for l in BANKED_FILE.read_text(encoding="utf-8").splitlines() if l.strip())
        else:
            closed = 0
        return {"closed": closed, "total": total}
    except Exception:
        return {"closed": 0, "total": 0}


def _emit_pack_offload(pack: dict[str, Any], mode: str, max_chars: int,
                       total_chars: int, shed_sections: list[str], stage: int) -> None:
    """Emit one JSONL offload row naming the shed sections when the pack overflows max_chars."""
    row = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "schema": "pack_offload.v1",
        "mode": mode,
        "max_chars": max_chars,
        "total_chars": total_chars,
        "shed_sections": shed_sections,
        "stage": stage,
        "root_short": (pack.get("tip") or {}).get("root_short", ""),
    }
    PACK_OFFLOAD_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PACK_OFFLOAD_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

# Layer budgets per mode — janitor default for ask/steward.
#
# wave5 render-pipe repair (2026-09-29): the mandated core — objective,
# compiled laws, operator directives, RIB doctrine — renders in EVERY mode
# (arch-01 measured it reaching the model 0/6 live renders). Core caps
# (max_objective / max_laws / max_directives / max_doctrine) bound the
# render per mode; max_chars is sized so the core + compacted task fit
# without the hard clip amputating the task. The old janitor/route budgets
# (1200/1800) were smaller than the uncapped objective alone (2.2k), which
# is why the core never survived the clip there.
MODE_CONFIG: dict[str, dict[str, Any]] = {
    "janitor": {
        "max_brief": 400,
        "max_bonds": 500,
        "max_live": 0,
        "max_chars": 4800,
        "max_objective": 400,
        "max_laws": 1000,
        "max_directives": 500,
        "max_doctrine": 500,
        "default_job": "ask",
        "include_resonance": False,
        "include_trail": False,
        "include_skills": False,
        "include_ijl": False,
        "include_heat": False,
        "include_coordination": False,
        "include_mirror_clue": False,
        "compact_nervous": True,
    },
    "route": {
        "max_brief": 600,
        "max_bonds": 800,
        "max_live": 200,
        "max_chars": 5800,
        "max_objective": 600,
        "max_laws": 1000,
        "max_directives": 700,
        "max_doctrine": 600,
        "default_job": "route",
        "include_resonance": True,
        "include_trail": False,
        "include_skills": True,
        "include_ijl": False,
        "include_heat": False,
        "include_coordination": True,
        "include_mirror_clue": False,
        "compact_nervous": True,
    },
    "build": {
        "max_brief": 900,
        "max_bonds": 1200,
        "max_live": 400,
        "max_chars": 7400,
        "max_objective": 800,
        "max_laws": 1200,
        "max_directives": 700,
        "max_doctrine": 1000,
        "default_job": "build",
        "include_resonance": True,
        "include_trail": True,
        "include_skills": True,
        "include_ijl": True,
        "include_heat": False,
        "include_coordination": True,
        "include_mirror_clue": False,
        "include_build": True,
        "include_scope": True,
        "compact_nervous": False,
    },
    "audit": {
        "max_brief": 600,
        "max_bonds": 600,
        "max_live": 200,
        "max_chars": 7500,
        "max_objective": 800,
        "max_laws": 1200,
        "max_directives": 900,
        "max_doctrine": 1200,
        "default_job": "audit",
        "include_resonance": False,
        "include_trail": True,
        "include_skills": True,
        "include_ijl": False,
        "include_heat": False,
        "include_coordination": True,
        "include_mirror_clue": False,
        "include_build": True,
        "compact_nervous": False,
    },
    "plan": {
        "max_brief": 1200,
        "max_bonds": 1600,
        "max_live": 600,
        "max_chars": 11000,
        "max_objective": 1200,
        "max_laws": 1800,
        "max_directives": 2800,
        "max_doctrine": 2800,
        "default_job": "plan",
        "include_resonance": True,
        "include_trail": False,
        "include_skills": True,
        "include_ijl": True,
        "include_heat": True,
        "include_coordination": True,
        "include_mirror_clue": True,
        "compact_nervous": False,
    },
    "full": {
        "max_brief": 1200,
        "max_bonds": 1600,
        "max_live": 800,
        "max_chars": 7200,
        "max_objective": 1000,
        "max_laws": 1200,
        "max_directives": 1200,
        "max_doctrine": 1200,
        "default_job": "default",
        "include_resonance": True,
        "include_trail": True,
        "include_skills": True,
        "include_ijl": True,
        "include_heat": True,
        "include_coordination": True,
        "include_mirror_clue": True,
        "compact_nervous": False,
    },
}


def _normalize_mode(mode: str | None) -> str:
    m = (mode or "full").strip().lower()
    return m if m in VALID_PACK_MODES else "full"


def _read_build_excerpt(path: str | Path | None, *, max_chars: int = 4000) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.is_file():
        p = ROOT / str(path)
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")[:max_chars]


def _latest_scope_card(*, slug: 
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 6300 + tail 2100 of 59418 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
}).get("git_sha") or ""
    goal_block = (goal or "").strip()[:500]
    lines = [
        "# Mag agent preamble (coarse elephant — not DNA)",
        f"# ts={(p.get('ts') or '')[:19]} · law=COORDINATION_ELIAS_ROPE",
        "",
        "## Contract",
        "- Trust this pack + your task boundary. Do not invent body/keys/status.",
        "- Do not load full residual or chat history. Deep probe only if task requires a path.",
        "- FILE progress as trail drift cores (base_id + locus), not peer chat.",
        "- Remotes: pack+goal only. No T0/T1 private archive paths.",
        "",
        "## Base (frozen graph — cite in every drift)",
        f"- base_id: {base_id or '(no open run — trail start first)'}",
        f"- tip: {base_tip or '—'} · git: {base_git or '—'}",
        "- Drift without this base_id is rejected by architecture.",
        "",
        "## Goal (if provided)",
        goal_block or "(orchestrator supplies goal in task prompt)",
        "",
        "## L0a Nervous",
        f"- body_ok={ns.get('ok')} integral_ok={ns.get('integral_ok')}",
        f"- dash:8765={'UP' if body.get('dashboard_8765') else 'DOWN'} · "
        f"ollama={'UP' if body.get('ollama_11434') else 'DOWN'} · "
        f"smoke={'PASS' if body.get('multi_smoke_ok') else 'FAIL'}",
        f"- session tip: {(ns.get('session_tip') or {}).get('root_short')} "
        f"leaves={(ns.get('session_tip') or {}).get('n_leaves')}",
        f"- agent tip: {(ns.get('agent_tip') or {}).get('root_short')} "
        f"commit={(ns.get('agent_tip') or {}).get('commit8')}",
        f"- keys: {keys_line or '(none)'} · probe before claim seats",
        f"- {tip_line}",
        "",
        "## Open loops (narrow)",
        loops_txt,
        "",
        "## Trail cores (mid-run — re-inject)",
        trail_txt,
        "",
        "_Worker: complete task from tools + this preamble. Empty findings only after real inspection._",
    ]
    text = "\n".join(lines)
    if max_chars is not None and len(text) > max_chars:
        text = text[: max_chars - 20] + "\n…(preamble clipped)"
    return text
