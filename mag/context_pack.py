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
                       total_chars: int, shed_sections: list[str], stage: int,
                       stubs: list[dict[str, Any]] | None = None) -> None:
    """Emit one JSONL offload row naming the shed sections when the pack overflows max_chars.

    ReFold port (port-order lane P5, 2026-10-07): rows are no longer write-only
    telemetry. Each row now carries the reversible stubs created at that stage
    (section, source path, content sha256, chars) as an additive "stubs" field,
    so watch/inbox/PACK_OFFLOAD.jsonl doubles as the restore index. The schema
    string stays pack_offload.v1 (additive-field extension; pre-existing readers
    and the v1 schema pin in tests pin the string); read_pack_offload keys on
    field presence, not the schema string.
    """
    row = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "schema": "pack_offload.v1",
        "mode": mode,
        "max_chars": max_chars,
        "total_chars": total_chars,
        "shed_sections": shed_sections,
        "stage": stage,
        "stubs": stubs or [],
        "root_short": (pack.get("tip") or {}).get("root_short", ""),
    }
    PACK_OFFLOAD_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PACK_OFFLOAD_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _content_sha(text: str) -> str:
    """sha256 hex over the utf-8 bytes of a shed section's rendered content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _shed_fold_marker(count: int) -> str:
    """The one render line a fold leaves behind, naming the restore door.

    Per-section reversible pointers (section name + source organ + content
    sha256) ride the offload ROWS, not the render: measured on the live tree
    (port-order P5, 2026-10-07), route's whole sheddable tier was ~775 bytes
    while 7 render stubs cost ~1100, so in-render stubs are net-negative on
    the tight per-mode budgets and tip the ladder's own floor over budget.
    The row (read_pack_offload / list_shed_stubs) is the restore index; this
    marker keeps the fold visible in the render instead of silent.
    """
    return (f"[SHED this fold: {count} sections | "
            "restore: python -m mag.context_pack sheds]")


# ReFold stub registry: shed section name -> the organ path its content was
# rendered from. The sha256 in the stub is over the exact rendered lines that
# were removed; restore re-renders from the named organ (via
# _shed_recipe_render) and refuses on sha drift, so a drifted organ can never
# masquerade as the shed bytes.
SHED_SOURCES: dict[str, str] = {
    "L4 Heat (live_tail, attention)": "memory/live_from_grok.md + memory/attention.md",
    "L3 Task (compacted)": "memory/briefs + queue/todo.md",
    "L0f full mounted subchain + world state": "memory/runs/party_subchain/chain.jsonl",
    "L0d proven moves": "memory/improve/skill_ledger.jsonl",
    "L0d solved history": "memory/improve/pro_library.json",
    "L0d zeitgeist": "docs/archive/ZEITGEIST.md",
    "L0b agent state": "memory/agent_state/LATEST.md",
    "L0-continuity": "memory/working/OPERATOR_CONTINUITY.md",
    "L0 behavioral + tesuji tips": "memory/improve/daily/",
    "L0 coordination": "state/shared_activity.jsonl",
    "L0e resonance": "memory/resonance/findings.jsonl",
    "L1b/L1c skills + ijl + mirror/clue": "configs/skills.yaml",
    "L2 trail": "memory/runs (run trail cores)",
    "L1 bonds": "memory/bonds_active.md",
    "L0d rib vault amendments": "memory/rib_boot.json",
}


def _shed_recipe_render(name: str, pack: dict[str, Any], mode: str) -> list[str] | None:
    """Re-render a shed section's exact lines from a pack dict.

    The wrappers mirror the section builders in format_context_pack_text byte
    for byte. Divergence is detectable, never silent: restore_sha() compares
    the rebuilt content against the stub's recorded sha256 and a mismatch
    refuses the restore. Returns None when no recipe exists for the name.
    """
    p = pack
    cfg = MODE_CONFIG[mode]
    if name == "L0f full mounted subchain + world state":
        return [
            "",
            "### L0f Full mounted subchain (reasoning surface; chain is still the record)",
            p.get("subchain_full") or "(empty)",
            "",
            "### L0f World state",
            str(p.get("world_state") or "(none)"),
            "",
        ]
    if name == "L0d proven moves":
        return ["", "### L0d Proven moves (verified case law — trust these)", p.get("proven_moves"), ""]
    if name == "L0d solved history":
        return ["", "### L0d Solved history (what the system already holds — don't redo)", p.get("solved_excerpt"), ""]
    if name == "L0d zeitgeist":
        return ["", "### L0d Zeitgeist (project epoch + signal)", p.get("zeitgeist_excerpt")]
    if name == "L0b agent state":
        return ["", "### L0b Agent state (versioned self — Verkle agent tip)", p.get("agent_state") or "(none)"]
    if name == "L0-continuity":
        return [
            "",
            "### L0-continuity (goals · gaps · eject · smokes — cold Grok must use this)",
            "path: memory/working/OPERATOR_CONTINUITY.md",
            p.get("continuity"),
        ]
    if name == "L0 behavioral + tesuji tips":
        return ["", p.get("behavioral_excerpt")]
    if name == "L0 coordination":
        return ["", p.get("coordination_excerpt")]
    if name == "L0e resonance":
        return ["", p.get("resonance_l0e")]
    if name == "L0d rib vault amendments":
        return [
            "",
            "### L0d RIB vault amendments (POST-DATUM law deltas - mounted from memory/rib_boot.json)",
            (p.get("rib_vault") or {}).get("body"),
        ]
    if name == "L1b/L1c skills + ijl + mirror/clue":
        if not (cfg.get("include_skills") and p.get("skills_excerpt")):
            return []
        lines = [
            "",
            "## L1b Skills (progressive — not MCP flood)",
            p.get("skills_excerpt") or "(none — configs/skills.yaml)",
        ]
        if cfg.get("include_ijl") and p.get("ijl_skills"):
            lines.extend([
                "",
                "### L1b IJL skill beads (episode distill)",
                p.get("ijl_skills") or "(none yet)",
            ])
        if p.get("mirror_voice_excerpt"):
            lines.extend(["", "### L1c Mirror voice (operator corpus)", p.get("mirror_voice_excerpt")])
        if p.get("clue_chain_excerpt"):
            lines.extend(["", "### L1c Clue chain", p.get("clue_chain_excerpt")])
        return lines
    if name == "L2 trail":
        if not cfg.get("include_trail"):
            return []
        return [
            "",
            "## L2 Trail cores (mid-run continuity — re-inject)",
            (p.get("run_trail") or {}).get("text")
            or "(no open run — python main.py trail start \"goal\")",
        ]
    if name == "L1 bonds":
        if not (mode != "janitor" or (p.get("bonds") and "(no bonds" not in str(p.get("bonds")))):
            return []
        return [
            "",
            "## L1 Bonds (next-session / residual edges)",
            (p.get("bonds") or "(none — run: python main.py bonds)")[:800 if mode == "janitor" else 5000],
        ]
    if name == "L4 Heat (live_tail, attention)":
        if not cfg.get("include_heat"):
            return []
        return [
            "",
            "## L4 Heat (drop first under compaction)",
            "### Live tail",
            p.get("live_tail") or "",
            "",
            "### Attention",
            p.get("attention_tail") or "",
            "",
            "_Grok: answer from this. Re-inject trail cores if run active._",
        ]
    if name == "L3 Task (compacted)":
        task = [
            "",
            "## L3 Task (brief + loops + todo)",
            "### Brief",
            (p.get("brief") or "")[:400 if mode == "janitor" else 5000],
            "",
            "### Open loops",
            "\n".join(p.get("open_loops") or ["(none extracted)"])[:400 if mode == "janitor" else 2000],
        ]
        if mode != "janitor":
            task.extend([
                "",
                "### Todo open",
                "\n".join(p.get("todo_open") or ["(none)"]),
            ])
        return task
    return None


def restore_shed_section(
    section: str,
    *,
    mode: str | None = None,
    pack: dict[str, Any] | None = None,
    sha: str | None = None,
) -> dict[str, Any]:
    """ReFold restore: re-render a shed section from its stub pointer, sha-verified.

    With ``pack`` (in-process round trip): rebuilds from the same pack dict the
    shed came from. Without: rebuilds a fresh fast pack for ``mode`` from the
    current organ state named in the stub (SHED_SOURCES), so byte-identity
    holds exactly when the organs have not drifted; the sha check turns drift
    into a refused restore instead of silent corruption. ``sha`` is the stub's
    recorded content sha256; omitting it skips the verdict but still reports.
    """
    if pack is None:
        m = _normalize_mode(mode)
        pack = build_context_pack(mode=m, fast=True, refresh_bonds=False)
        mode = m
    else:
        mode = _normalize_mode(mode or str(pack.get("mode") or ""))
    lines = _shed_recipe_render(section, pack, mode)
    if lines is None:
        return {"ok": False, "section": section, "mode": mode,
                "reason": "no recipe for section (see SHED_SOURCES)"}
    content = "\n".join(lines)
    got = _content_sha(content)
    ok = bool(sha is None or got == sha)
    return {
        "ok": ok,
        "section": section,
        "mode": mode,
        "sha256": got,
        "expected_sha256": sha,
        "chars": len(content),
        "content": content,
        "reason": None if ok else "sha mismatch: organ drifted since the shed; restore refused",
    }


def read_pack_offload(
    *,
    tail: int | None = None,
    path: str | Path | None = None,
    annotate_stale: bool = True,
) -> dict[str, Any]:
    """Tolerant ledger reader: the first consumer of watch/inbox/PACK_OFFLOAD.jsonl.

    Byte-level line split, per-line decode: a torn non-UTF8 partial write is
    skipped with a note, never a crash (the live ledger holds one such row,
    bytes 80 a6 + CR). With annotate_stale, rows whose (mode, max_chars) does
    not match the current MODE_CONFIG budget are flagged "stale_code" with the
    expected budget, so a stale renderer process holding pre-raise code is
    visible from the ledger instead of needing a hand recount.
    """
    f = Path(path) if path else PACK_OFFLOAD_FILE
    out: dict[str, Any] = {
        "path": str(f),
        "rows": [],
        "torn_rows": 0,
        "torn_notes": [],
        "raw_lines": 0,
    }
    if not f.is_file():
        out["missing"] = True
        return out
    data = f.read_bytes()
    lines = data.split(b"\n")
    if tail is not None:
        lines = lines[-int(tail):]
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        out["raw_lines"] += 1
        try:
            text = ln.decode("utf-8")
        except UnicodeDecodeError:
            out["torn_rows"] += 1
            out["torn_notes"].append(f"line {i}: non-UTF8 bytes ({ln[:12]!r}) skipped")
            continue
        try:
            row = json.loads(text)
        except ValueError as exc:
            out["torn_rows"] += 1
            out["torn_notes"].append(f"line {i}: unparseable JSON ({exc}) skipped")
            continue
        if annotate_stale:
            budget = (MODE_CONFIG.get(str(row.get("mode"))) or {}).get("max_chars")
            if budget is not None and row.get("max_chars") != budget:
                row["stale_code"] = {
                    "emitted_max_chars": row.get("max_chars"),
                    "current_max_chars": budget,
                    "note": "row budget does not match the current MODE_CONFIG entry "
                            "(stale renderer process, dead constant, or an explicit "
                            "max_chars override render)",
                }
        out["rows"].append(row)
    return out


def list_shed_stubs(*, tail: int | None = 2000) -> dict[str, Any]:
    """List shed stubs from the ledger (v2 rows), newest last, plus a summary."""
    led = read_pack_offload(tail=tail)
    stubs: list[dict[str, Any]] = []
    stale = 0
    for row in led["rows"]:
        if row.get("stale_code"):
            stale += 1
        for st in row.get("stubs") or []:
            stubs.append({
                "ts": row.get("ts"),
                "mode": row.get("mode"),
                "stage": row.get("stage"),
                **st,
            })
    led["stubs"] = stubs
    led["stale_rows"] = stale
    return led


def _main(argv: list[str] | None = None) -> int:
    """CLI: `python -m mag.context_pack sheds [--tail N]` lists the shed ledger;
    `restore --section NAME [--mode M] [--sha HEX]` re-renders one shed section,
    sha-verified against its stub."""
    import argparse

    ap = argparse.ArgumentParser(
        prog="mag.context_pack",
        description="ReFold shed ledger: list reversible stubs, restore a shed section",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_sheds = sub.add_parser("sheds", help="list shed stubs + ledger health")
    p_sheds.add_argument("--tail", type=int, default=2000)
    p_res = sub.add_parser("restore", help="re-render one shed section from its stub pointer")
    p_res.add_argument("--section", required=True)
    p_res.add_argument("--mode", default=None)
    p_res.add_argument("--sha", default=None)
    args = ap.parse_args(argv)
    if args.cmd == "sheds":
        led = list_shed_stubs(tail=args.tail)
        print(f"ledger: {led['path']}")
        print(f"raw_lines={led['raw_lines']} parsed={len(led['rows'])} "
              f"torn={led['torn_rows']} stale_code_rows={led.get('stale_rows', 0)} "
              f"stubs={len(led.get('stubs') or [])}")
        for note in led["torn_notes"]:
            print(f"torn: {note}")
        for st in (led.get("stubs") or [])[-25:]:
            print(f"- {st.get('ts', '')[:19]}Z [{st.get('mode')}] stage {st.get('stage')} "
                  f"{st.get('section')} sha256={str(st.get('sha256'))[:12]} chars={st.get('chars')}")
        return 0
    res = restore_shed_section(args.section, mode=args.mode, sha=args.sha)
    if res.get("reason") and not res.get("ok"):
        print(f"restore FAILED: {res['reason']}")
        return 1
    print(f"restore {'OK (sha verified)' if res['ok'] else 'UNVERIFIED (no --sha given)'}: "
          f"{res['section']} mode={res['mode']} sha256={res['sha256']} chars={res['chars']}")
    print(res["content"])
    return 0

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
        # pheromone-swarm p1a-L0d-fix (2026-10-07): the old 7200 forced the
        # L0d rib-vault carrier to shed at stage 3 (d01 dogfood2 evidence:
        # total_chars 9471 > 7200, PACK_OFFLOAD.jsonl), so POST-DATUM law
        # never reached fresh seats. Full is the whole-surface mode (escape
        # hatch family, MAG_FULL_CONTEXT default 48000); the live uncapped
        # assembly measured 25784 chars, so the default budget now covers the
        # assembly with headroom. The shed ladder + reprioritized vault order
        # stay as the net for other modes and future growth.
        "max_chars": 26000,
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


def _latest_scope_card(*, slug: str = "") -> str:
    scope_dir = ROOT / "memory" / "steward" / "scope_cards"
    if not scope_dir.is_dir():
        return ""
    if slug:
        p = scope_dir / f"{slug}.md"
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace")[:2500]
    cards = sorted(scope_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not cards:
        return ""
    return cards[0].read_text(encoding="utf-8", errors="replace")[:2500]


def _env_on(name: str, *, default: bool = False) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def _republic_root() -> Path:
    env = os.environ.get("MAG_REPUBLIC_ROOT", "").strip()
    if env:
        return Path(env)
    return ROOT.parent / "mycelial-republic"


def _mirror_voice_excerpt(goal: str, *, max_chars: int = 600) -> str:
    """Compact mirror voice rows from republic mirror_train.jsonl."""
    if not _env_on("MAG_INJECT_MIRROR_VOICE", default=False):
        return ""
    path = _republic_root() / "data" / "annotated" / "mirror_train.jsonl"
    if not path.is_file():
        return ""
    goal_tokens = {t for t in re.findall(r"[a-z0-9]+", goal.lower()) if len(t) > 2}
    priority_tags = {"sovereign_mirror", "refusal", "rope", "chord", "meta", "mycelial"}
    rows: list[tuple[int, dict[str, Any]]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        body = str(row.get("text") or row.get("response") or "").strip()
        if not body:
            continue
        tags = set(row.get("knot_tags") or row.get("tags") or [])
        signal = str(row.get("signal") or "").lower()
        product = str(row.get("product_dna") or "").lower()
        score = 0
        if signal == "high":
            score += 4
        elif signal == "medium":
            score += 2
        if tags & priority_tags:
            score += 3
        if "sovereign_mirror" in product or "verkle" in product:
            score += 2
        if goal_tokens:
            score += len(goal_tokens & set(re.findall(r"[a-z0-9]+", body.lower())))
        if score > 0:
            rows.append((score, row))
    if not rows:
        return ""
    rows.sort(key=lambda x: x[0], reverse=True)
    lines = ["[MIRROR VOICE — operator corpus excerpt (presented, not interpreted)]"]
    used = 0
    for _, row in rows[:3]:
        rid = row.get("id") or "?"
        body = str(row.get("text") or row.get("response") or "").strip()
        snippet = body[:220] + ("…" if len(body) > 220 else "")
        block = f"- {rid}: {snippet}"
        if used + len(block) + 1 > max_chars:
            break
        lines.append(block)
        used += len(block) + 1
    return "\n".join(lines)[:max_chars]


def _clue_chain_excerpt(*, max_chars: int = 500) -> str:
    """Latest decoded clue bead from memory/improve/pins/clues/."""
    if not _env_on("MAG_INJECT_CLUE_CHAIN", default=False):
        return ""
    clues_dir = ROOT / "memory" / "improve" / "pins" / "clues"
    if not clues_dir.is_dir():
        return ""
    beads = sorted(clues_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not beads:
        return ""
    body = beads[0].read_text(encoding="utf-8", errors="replace").strip()
    if not body:
        return ""
    header = f"[CLUE CHAIN — latest bead: {beads[0].name}]"
    return f"{header}\n{body[: max_chars - len(header) - 2]}"


def _zeitgeist_excerpt(*, max_chars: int = 800) -> str:
    """Optional project zeitgeist excerpt from docs/ZEITGEIST.md."""
    candidates = [
        ROOT / "docs" / "archive" / "ZEITGEIST.md",
        ROOT / "docs" / "ZEITGEIST.md",
    ]
    for p in candidates:
        if p.is_file():
            body = p.read_text(encoding="utf-8", errors="replace").strip()
            if not body:
                return ""
            header = "[ZEITGEIST — era signal + project frame]"
            return f"{header}\n{body[: max_chars - len(header) - 2]}"
    return ""


def _clip(path: Path, n: int) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:n]


def _full_context_limit() -> int:
    """Hard ceiling for the explicit full-context escape hatch.

    Full mode is an operator choice, not permission to submit an unbounded
    transcript.  Keep the escape hatch useful while ensuring one oversized
    board cannot consume the entire model window.
    """
    try:
        value = int(os.environ.get("MAG_FULL_CONTEXT_MAX_CHARS", "48000"))
    except (TypeError, ValueError):
        value = 48000
    return min(200000, max(8000, value))


def _head_tail(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    head = max(1, int(limit * 0.72))
    tail = max(1, limit - head - 40)
    return text[:head] + "\n…(full-context ceiling; middle omitted)…\n" + text[-tail:]


def _rib_law_spine(max_chars: int = 600) -> str:
    """POST-DATUM law spine: the pinned amendment law sentences, one line each.

    L0d shedding cure (2026-10-07, pheromone-swarm run, lane p1b): the
    POST-DATUM law deltas rode ONLY the sheddable "L0d rib vault amendments"
    context block, so every real overflow render amputated the law exactly
    when the pack was tightest -- live watch/inbox/PACK_OFFLOAD.jsonl rows
    2026-10-07T18:05Z show stage-3 sheds plus the stage-4 hard clip in full
    mode, and all six modes rendered ZERO copies of the D4 law marker
    ("MEASURED ON", measured this sitting). The cure mounts the pinned law
    sentences at the HEAD of the core L0d doctrine block, inside the existing
    max_doctrine cap: zero net additive core (R4-L2's budget law -- every
    mode's cap sits below the 5.1k doctrine census, so the capped render
    length is unchanged and the spine displaces the least-load-bearing
    census tail lines), and the law survives every shed rung. The pinned
    sentences are the amendments' own "THE LAW IS NOW:" convention,
    byte-derived from memory/rib/*.md, never hand-copied. Line-based
    extraction on purpose: amendment headers hard-wrap and their
    continuation lines start with "## " themselves
    (RIB_INFERENCE_BUDGET_20261001.md:120), so section parsing breaks.
    """
    rib_dir = ROOT / "memory" / "rib"
    if not rib_dir.is_dir():
        return ""
    out: list[str] = []
    total = 0
    for f in sorted(rib_dir.glob("*.md")):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lm in re.finditer(r"THE LAW IS NOW:\s*([^\n]+)", text):
            law = lm.group(1).strip()
            if not law:
                continue
            entry = f"- AMEND {f.stem}: THE LAW IS NOW: {law}"[:220]
            if total + len(entry) + 1 > max_chars:
                return "\n".join(out)
            out.append(entry)
            total += len(entry) + 1
    return "\n".join(out)


def _rib_doctrine(max_chars: int = 2800) -> str:
    """Load the RIB doctrine (the system's understanding) into stateless-agent context.

    Reads memory/rib/*.md — the memweave/doctrine layer the stateless agent never
    sees otherwise (human-read-only). Emits title + goal line per doc, capped.
    Deterministic, $0 — the "understanding" seam for a stateless boot.
    """
    rib_dir = ROOT / "memory" / "rib"
    if not rib_dir.is_dir():
        return ""
    files = sorted(rib_dir.glob("*.md"))
    if not files:
        return ""
    out: list[str] = []
    total = 0
    # L0d shedding cure: the pinned POST-DATUM law deltas ride at the HEAD of
    # the core doctrine block so the render cap (max_doctrine) can never clip
    # them ahead of the 54-line rib census, and no shed rung ever touches the
    # core. Cause + evidence: live PACK_OFFLOAD.jsonl 2026-10-07T18:05Z
    # stage-3/4 sheds amputated the vault block carrying the D4 law in every
    # overflow render; 0/6 modes reached the model with the marker.
    _spine = _rib_law_spine()
    if _spine:
        out.append("[POST-DATUM law spine (amendment deltas the 1200-char heads "
                   "once cut off; rides every shed rung)]")
        for _ln in _spine.splitlines():
            out.append(_ln)
            total += len(_ln) + 1
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        title = ""
        goal = ""
        for line in text.splitlines():
            s = line.strip()
            if not title and (s.startswith("# ") or s.startswith("**Schema:**")):
                title = s.lstrip("# ").strip()[:100]
            if not goal and ("**RIB goal:**" in s or "**Goal:" in s or s.startswith("**Operator")):
                goal = s[:160]
            if title and goal:
                break
        entry = f"- {title or f.name}" + (f" — {goal}" if goal else "")
        if len(entry) > total + max_chars:
            break
        out.append(entry)
        total += len(entry)
    return "\n".join(out)


def _rib_vault_law() -> dict[str, Any]:
    """The rib_boot vault block -- its first code consumer (R4-L2, 2026-10-05).

    memory/rib_boot.json was a 25KB write-only orphan: regenerated by siblings,
    read by zero code. This seam mounts its --json vault block into every pack
    (pack["rib_vault"]) and renders it as ONE sheddable context block: a digest
    line (law state + freshness + demotion-register pointer) riding on top of
    the POST-DATUM amendment bodies. Zero CORE footprint on purpose: tonight's
    live content already pins build/full at their budgets (pre-existing hard
    clips, measured this sitting), so any additive core line would tip plan
    over too and cannibalize janitor bonds under the ladder. The block sheds
    after L1 bonds (last before the hard clip; p1a-L0d-fix 2026-10-07: the
    old ahead-of-bonds placement let the carrier die at stage 3 ahead of
    skills/trail and POST-DATUM law never reached fresh seats), the shed
    lands in PACK_OFFLOAD.jsonl (never
    silent), and staleness uses the ONE decay bar (PACK_STALE_DAYS): a
    rib_boot.json older than the bar renders as a debt pointer, not law.
    """
    path = ROOT / "memory" / "rib_boot.json"
    if not path.is_file():
        debt = ("(rib vault: memory/rib_boot.json missing -- regen owed: "
                ".venv/Scripts/python.exe -m mag.rib_boot)")
        return {"digest": debt, "body": debt}
    try:
        j = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        debt = ("(rib vault: rib_boot.json unreadable -- regen owed: "
                ".venv/Scripts/python.exe -m mag.rib_boot)")
        return {"digest": debt, "body": debt}
    ts = str(j.get("ts") or "")
    try:
        from datetime import datetime as _dt
        age_d = (_dt.now().astimezone()
                 - _dt.fromisoformat(ts.replace("Z", "+00:00"))
                 ).total_seconds() / 86400.0
    except ValueError:
        age_d = 99.0
    vault = j.get("vault") or {}
    ribs = vault.get("law_ribs") or []
    mounted = sum(1 for r in ribs if r.get("mounted"))
    n_amend = sum(int(r.get("amendment_count") or 0) for r in ribs)
    if not ts or age_d > PACK_STALE_DAYS:
        debt = (f"(rib vault STALE {age_d:.0f}d -- regen owed: "
                ".venv/Scripts/python.exe -m mag.rib_boot; law hidden until fresh)")
        return {"digest": debt, "body": debt}
    digest = (f"[rib vault: {vault.get('md_count')} ribs censused, {mounted} law ribs "
              f"mounted, {n_amend} amendments ride the heads; boot {ts[:19]}Z; "
              f"demotion register: memory/fold_history/SUPERSEDED.md]")
    lines: list[str] = [digest,
                        "[vault amendments: POST-DATUM law deltas the 1200-char "
                        "heads once cut off -- amend-never-rewrite bytes]"]
    for r in ribs:
        amends = r.get("law_amendments") or []
        if not amends:
            continue
        lines.append(f"- {r.get('file')} ({len(amends)} amendment(s)):")
        for a in amends:
            lines.append(f"  AMEND: {str(a)[:1100]}")
    body = "\n".join(lines)[:4200]
    return {"digest": digest, "body": body}


def _quantized_laws(max_chars: int = 1800) -> str:
    """The thought-quantizer flash pack — compiled fleet law for every seat.

    The delivery vehicle the v0.2 night never wired (QUANTIZER_V03_20260927):
    the packs existed but nothing consumed them. This seam rides the boot
    pack every seat loads (load-first rule), so compiled law reaches janitors
    and specialists alike. Flash tier only (<=220-char imperatives — the
    boot-context dose; frontier nuance is for deliberate asks). Staleness is
    VISIBLE, never silent: packs older than the ONE decay bar
    (PACK_STALE_DAYS, mag/constants.py - the same constant the quantizer's
    fossil arm and the boot meter read; L3 unification, ball-20260929)
    render as a one-line debt pointer instead of law (the fossil-in-feed
    law's read-side twin).
    """
    import json as _json
    qt_dir = ROOT / "memory" / "corpus" / "quantized_thought"
    flash = qt_dir / "instructions_flash.jsonl"
    report = qt_dir / "compile_report.json"
    if not flash.is_file() or not report.is_file():
        return ""
    try:
        rep = _json.loads(report.read_text(encoding="utf-8"))
        compiled_ts = rep.get("compiled", "")
        rows = [_json.loads(x) for x in
                flash.read_text(encoding="utf-8").splitlines() if x.strip()]
    except (OSError, ValueError):
        return ""
    if not rows or not compiled_ts:
        return ""
    try:
        from datetime import datetime as _dt
        age_d = (_dt.now().astimezone()
                 - _dt.fromisoformat(compiled_ts.replace("Z", "+00:00"))
                 ).total_seconds() / 86400.0
    except ValueError:
        age_d = 99.0
    if age_d > PACK_STALE_DAYS:
        return (f"(quantizer packs STALE {age_d:.0f}d — recompile owed: "
                "tools/thought_quantizer.py compile; law hidden until fresh)")
    out = [f"[compile v{rep.get('v', '?')} {compiled_ts[:10]}, "
           f"weight=recency x shape, counts are provenance only]"]
    total = len(out[0])
    for r in rows:
        law = str(r.get("flash") or r.get("frontier") or "").strip()
        if not law:
            continue
        entry = f"- {law}"
        if total + len(entry) > max_chars:
            break
        out.append(entry)
        total += len(entry)
    return "\n".join(out)


def _proven_moves_excerpt(limit: int = 8) -> str:
    """Proven case-law moves from skill_ledger — the moves the agent can trust."""
    try:
        from mag.skill_ledger import proven_moves
        moves = proven_moves(limit=limit)
        if not moves:
            return ""
        return "\n".join(
            f"- {m['move'][:90]} (n={m['count']}, ok={m['ok_rate']})"
            for m in moves
        )
    except Exception:
        return ""


def _solved_excerpt(limit: int = 10) -> str:
    """Solved history (case law + RIB + verkle tip) — what the system already holds."""
    try:
        from mag.solved_surface import solved
        s = solved()
        rows = (s.get("case_law") or []) + (s.get("rib") or [])
        if not rows:
            return ""
        lines = []
        for r in rows[:limit]:
            title = r.get("move") or r.get("title") or r.get("id")
            if title:
                lines.append(f"- {str(title)[:90]}")
        tip = s.get("verkle_tip") or {}
        if tip.get("n_leaves"):
            lines.append(f"- ({tip.get('n_leaves')} verkle leaves · {tip.get('root')}…)")
        return "\n".join(lines)
    except Exception:
        return ""


# --- A2: session-frozen system prompt --------------------------------------
#
# Law (Mag Estate ask A2): the system prompt + tool schemas are the stable
# prefix of every provider call in a session. They must be BYTE-IDENTICAL for
# the whole session — provider prompt caches key on exact prefix bytes, so a
# system prompt that re-renders per repack re-prices the entire context every
# time. Live values (pack text, residual crumbs, goal, health/timestamps)
# belong in the small evolving tail that rides AFTER the frozen prefix, never
# inside it.
#
# Schema-placement law (Slow Vale port, run port-debt-20261011): only
# SESSION-STABLE tool schemas may enter the frozen block. A dynamic
# (MCP-style) schema that changes mid-session would flip the prefix hash and
# re-price the whole context after it ("changing the schema prevented the
# otherwise stable context after it from hitting the cache"). A schema is
# declared dynamic by registration (register_dynamic_tool_schemas); the freeze
# drops registered-dynamic schemas from the frozen block AND the hash, and
# they render in the evolving tail as plain-text JSON contracts with backend
# validation (dynamic_tool_contracts), the lane that resolved 99.9% of
# malformed outputs at ~0.9% call-count overhead.
# Source: watch/inbox/frontier_olm_adhoc/steal/kv-cache-context-engineering.md

EVOLVING_TAIL_MARKER = "[EVOLVING TAIL"

_FROZEN_PROMPTS: dict[str, dict[str, Any]] = {}

# Names registered as dynamic tool schemas (schema-placement law). Registration
# is the explicit declaration that a tool's schema may churn mid-session.
DYNAMIC_TOOL_SCHEMA_NAMES: set[str] = set()


def register_dynamic_tool_schemas(*names: str) -> None:
    """Declare tool schemas DYNAMIC (schema-placement law).

    Registered names are excluded from the frozen block and the prefix hash by
    freeze_system_prompt, and must render per-call in the evolving tail via
    evolving_tail(dynamic_tool_schemas=...). Un-register by discarding from
    DYNAMIC_TOOL_SCHEMA_NAMES directly.
    """
    DYNAMIC_TOOL_SCHEMA_NAMES.update(n for n in names if n)


def _tool_schema_name(schema: dict[str, Any]) -> str:
    """Tool name from an OpenAI-style schema dict (function-wrapped or flat)."""
    fn = schema.get("function")
    if isinstance(fn, dict):
        return str(fn.get("name") or "")
    return str(schema.get("name") or "")


def is_dynamic_tool_schema(schema: Any) -> bool:
    """True when this schema dict names a registered-dynamic tool."""
    if not isinstance(schema, dict):
        return False
    return _tool_schema_name(schema) in DYNAMIC_TOOL_SCHEMA_NAMES


def split_tool_schemas(tool_schemas: Any) -> tuple[Any, list[dict[str, Any]]]:
    """Split tool schemas into (session-stable, dynamic) halves.

    The stable half is the only half the freeze may pin and hash; the dynamic
    half belongs to the evolving tail. Input that is not a list is returned
    wholesale as stable (the canonical serializer handles it exactly as
    before), and dict entries whose name is not registered stay stable, so an
    unregistered call site behaves byte-identically to the pre-law freeze.
    """
    if not isinstance(tool_schemas, list):
        return tool_schemas, []
    stable: list[dict[str, Any]] = []
    dynamic: list[dict[str, Any]] = []
    for s in tool_schemas:
        if isinstance(s, dict) and is_dynamic_tool_schema(s):
            dynamic.append(s)
        else:
            stable.append(s)
    return stable, dynamic


def dynamic_tool_contracts(tool_schemas: Any, *, max_chars: int = 2400) -> str:
    """Render dynamic tool schemas as PLAIN-TEXT contracts (schema-placement law).

    Slow Vale lane: a mid-session-changing tool schema never rides the frozen
    prefix; it renders here as plain text (name + description + canonical
    parameter JSON) and the backend validates the model's emitted arguments at
    call time. Deterministic per schema bytes; capped like the tail.
    """
    if tool_schemas is None:
        return ""
    items = tool_schemas if isinstance(tool_schemas, list) else [tool_schemas]
    lines: list[str] = []
    for s in items:
        if isinstance(s, dict):
            fn = s.get("function") if isinstance(s.get("function"), dict) else s
            name = _tool_schema_name(s) or "(unnamed)"
            desc = str(fn.get("description") or "").strip()
            params = fn.get("parameters")
            body = json.dumps(
                {"parameters": params}, sort_keys=True, ensure_ascii=False, default=str
            )
            lines.append(f"- {name}: {body}" + (f" :: {desc}" if desc else ""))
        else:
            lines.append(f"- (raw): {json.dumps(s, sort_keys=True, ensure_ascii=False, default=str)}")
    text = "\n".join(lines)
    if max_chars is not None and len(text) > max_chars:
        text = text[: max_chars - 20] + "\n…(contracts clipped)"
    return text


def _canonical_schemas_text(tool_schemas: Any) -> str:
    """Deterministic serialization for tool schemas (sorted keys → no byte drift)."""
    if tool_schemas is None:
        return ""
    return json.dumps(tool_schemas, sort_keys=True, ensure_ascii=False, default=str)


def freeze_system_prompt(
    prefix_text: str,
    *,
    tool_schemas: Any | None = None,
    session_id: str = "default",
    refreeze: bool = False,
) -> dict[str, Any]:
    """Freeze (system prompt + SESSION-STABLE tool schemas) as a byte-identical session prefix.

    First call for a session captures the bytes; later calls with the same
    session_id return the SAME bytes even if the inputs drifted — that drift
    belongs in the evolving tail (evolving_tail), not the prefix. Pass
    refreeze=True to deliberately start a new prefix (new session, operator
    /pack refresh). Hash is sha256 over prefix bytes + a NUL seam + the
    canonical tool-schema bytes, so either half changing flips the hash.

    Schema-placement law: the hash covers only SESSION-STABLE schemas. Schemas
    registered dynamic (register_dynamic_tool_schemas) are dropped from the
    frozen block and the hash entirely; their names are recorded in
    dynamic_schema_names for audit and their bytes must render per-call in the
    evolving tail via evolving_tail(dynamic_tool_schemas=...). A mid-session
    dynamic-schema change therefore never flips this hash and never refreezes.
    """
    key = str(session_id or "default")
    if not refreeze:
        frozen = _FROZEN_PROMPTS.get(key)
        if frozen is not None:
            return frozen
    text = str(prefix_text or "")
    stable_schemas, dynamic_schemas = split_tool_schemas(tool_schemas)
    schemas_text = _canonical_schemas_text(stable_schemas)
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    h.update(b"\x00--tool-schemas--\x00")
    h.update(schemas_text.encode("utf-8"))
    frozen = {
        "schema": "mag_context_freeze.v1",
        "session_id": key,
        "prefix_text": text,
        "tool_schemas_text": schemas_text,
        "dynamic_schema_names": [_tool_schema_name(s) for s in dynamic_schemas],
        "prefix_hash": h.hexdigest(),
        "prefix_chars": len(text),
        "frozen": True,
    }
    _FROZEN_PROMPTS[key] = frozen
    return frozen


def evolving_tail(
    *,
    goal: str = "",
    pack_text: str = "",
    residual: str = "",
    repacked: bool = False,
    dynamic_tool_schemas: Any | None = None,
    max_chars: int = 5200,
) -> str:
    """Small per-call tail carrying the LIVE values (never part of the prefix hash).

    Everything here may change between rounds/repacks; the frozen prefix above
    it must not. Capped so the tail stays small even when the pack is fat.

    dynamic_tool_schemas: dynamic (mid-session-churning) tool schemas render
    here as plain-text contracts (dynamic_tool_contracts), never inside the
    frozen prefix (schema-placement law). The backend validates the model's
    plain JSON arguments against the live schema at call time, so the schema
    may flip between calls without touching the prefix bytes.
    """
    parts: list[str] = [
        f"{EVOLVING_TAIL_MARKER} — live values; the frozen prefix above is "
        "byte-identical for this session — do not expect it to restate them]"
    ]
    if repacked:
        parts.append(
            "## Auto-repack\n"
            "History was compacted to fit this provider's context window "
            "(pack-first). Residual below holds the goal "
            "and tools already run. Continue the job; do not re-discover from zero."
        )
    if dynamic_tool_schemas:
        parts.append(
            "## Dynamic tool contracts\n"
            "Tool schemas below are DYNAMIC: they may change mid-session and are "
            "deliberately kept OUT of the frozen prefix. Call them by emitting "
            "plain JSON arguments matching the contract; the backend validates "
            "and rejects malformed calls.\n" + dynamic_tool_contracts(dynamic_tool_schemas)
        )
    if goal:
        parts.append(f"## Goal still in force\n{str(goal).strip()[:400]}")
    if pack_text:
        parts.append(f"## Context pack (live)\n{pack_text}")
    if residual:
        parts.append(f"## Residual\n{residual}")
    text = "\n\n".join(parts)
    if max_chars is not None and len(text) > max_chars:
        text = text[: max_chars - 20] + "\n…(tail clipped)"
    return text


_RESIDUAL_CENSUS_TTL_S = 3600


def _residual_census(res_dir: Path) -> int:
    """dig_edges count over memory/biography/residual, cached hourly.

    The census reads every residual JSON and runs on EVERY agent boot; once the
    dir reached ~3.7k files (2026-09-22) each boot wedged past its task timeout
    on the container bind mount (1s on NTFS, 300s+ through the mount). The
    cached number lives in memory/working/residual_census.json so a boot pays
    one small read instead of the full scan.
    """
    cache = ROOT / "memory" / "working" / "residual_census.json"
    now = time.time()
    try:
        cached = json.loads(cache.read_text(encoding="utf-8"))
        if now - float(cached.get("ts", 0)) < _RESIDUAL_CENSUS_TTL_S:
            return int(cached.get("dig_edges_n", 0))
    except Exception:
        pass
    n = 0
    for p in res_dir.glob("*.json"):
        try:
            o = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        kind = str(o.get("kind") or "").lower()
        edges = o.get("edges") if isinstance(o.get("edges"), dict) else {}
        if kind in ("dig_leaf", "dig", "corpus_leaf") or edges.get("dig_leaf") or edges.get(
            "dig_edges"
        ):
            n += 1
        digs = edges.get("dig_leaves") or edges.get("related_digs") or []
        if isinstance(digs, list) and digs:
            n += len(digs)
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({"ts": now, "dig_edges_n": n}), encoding="utf-8")
    except Exception:
        pass
    return n


def _verify_tip_chain(timeout_s: float = 2.0) -> tuple[bool, str]:
    """AG5 (audit finding #3, 2026-09-30): prove the verkle chain at launch.

    Every launch path rendered the tip as a display badge read raw — nothing
    verified the chain behind it. This is the cheap verify: run
    mag.verkle_knot._verify_chain_consistent on a daemon thread and NEVER
    block boot — a raise or a >timeout_s hang degrades to (False, reason)
    exactly like a tamper does, so the badge can render UNVERIFIED either way.
    """
    import threading

    outcome: dict[str, Any] = {}

    def _run() -> None:
        try:
            from mag.verkle_knot import _verify_chain_consistent

            outcome["verdict"] = _verify_chain_consistent()
        except Exception as e:  # the check must never take boot down with it
            outcome["verdict"] = (False, f"verify raised: {type(e).__name__}: {e}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout_s)
    if t.is_alive():
        return False, f"verify timeout >{timeout_s:.0f}s"
    ok, why = outcome.get("verdict", (False, "verify produced no result"))
    return bool(ok), str(why)


def build_context_pack(
    *,
    mode: str = "full",
    job: str | None = None,
    build_path: str | Path | None = None,
    scope_slug: str = "",
    goal: str = "",
    max_brief: int | None = None,
    max_live: int | None = None,
    max_bonds: int | None = None,
    refresh_bonds: bool = False,
    fast: bool = False,
    seat: str | None = None,
    checkpoint_session_id: str | None = None,
) -> dict[str, Any]:
    cfg = MODE_CONFIG[_normalize_mode(mode)]
    mode = _normalize_mode(mode)
    job = (job or cfg.get("default_job") or "default").strip()
    max_brief = max_brief if max_brief is not None else int(cfg["max_brief"])
    max_live = max_live if max_live is not None else int(cfg["max_live"])
    max_bonds = max_bonds if max_bonds is not None else int(cfg["max_bonds"])
    from mag.lanes import latest_brief_text
    from models.multi_smoke import last_smoke
    from models.registry import inventory

    # Queue admission must not refresh the live health surface.  A full pack
    # can still request a fresh sanity probe, but a fast pack is used by the
    # control plane before enqueue and therefore reads only the last durable
    # nervous receipt (or its minimal stale fallback).
    cached_glance: dict[str, Any] | None = None
    if fast:
        try:
            from mag.nervous_system import glance_cached

            cached_glance = glance_cached(max_age_s=30.0, refresh=False)
            body = cached_glance.get("body") or {}
            s = {
                "status": "up" if cached_glance.get("integral_ok") else "unknown",
                "recording": {"live_stale": None},
                "integral": {"port_8765": body.get("dashboard_8765")},
            }
        except Exception:
            s = {"status": "unknown", "recording": {}, "integral": {}}
    else:
        from mag.health import sanity

        s = sanity()
    brief = latest_brief_text()[:max_brief]
    live = _clip(ROOT / "memory" / "live_from_grok.md", max_live)
    att = _clip(ROOT / "memory" / "attention.md", 600)
    directives = _clip(ROOT / "memory" / "operator_directives.md", 2800)
    todo = _clip(ROOT / "queue" / "todo.md", 500)
    smoke = last_smoke() or {}
    inv = inventory()
    roles = {r["role"]: r["model"] for r in (inv.get("roles") or []) if r.get("present")}

    # Residual bonds: first-class next-session inputs
    bonds_text = ""
    bonds_meta: dict[str, Any] = {}
    bj: dict[str, Any] = {}
    try:
        from mag.bonds import BONDS_MD, ingest_bonds, load_bonds_json, load_bonds_text

        if refresh_bonds or not BONDS_MD.is_file():
            ingest_bonds(write=True)
        bonds_text = load_bonds_text(max_chars=max_bonds)
        bj = load_bonds_json() or {}
        bj["related_runs"] = [r for r in (bj.get("related_runs") or []) if not seat or r.get("seat") == seat]
        bonds_meta = {
            "session_id": bj.get("session_id"),
            "n_loops": len(bj.get("open_loops") or []),
            "n_bonds": len(bj.get("residual_bonds") or []),
            "related_by_seat": {k: sum(1 for r in bj["related_runs"] if str(r.get("seat")) == k) for k in sorted({str(r.get("seat")) for r in bj["related_runs"]})},
            "path": str(BONDS_MD),
        }
    except Exception as e:
        bonds_meta = {"error": str(e)}

    resonance_cards: list[dict[str, Any]] = []
    resonance_l0e = ""
    if cfg.get("include_resonance", True):
        try:
            from mag.resonance import format_l0e, top_cards

            goal_hint = (brief or "")[:200] + " " + " ".join(
                ln for ln in todo.splitlines() if ln.strip().startswith("- [ ]")
            )[:200]
            if goal:
                goal_hint = f"{goal[:200]} {goal_hint}"[:400]
            resonance_cards = top_cards(goal_hint, n=3)
            resonance_l0e = format_l0e(resonance_cards)
        except Exception:
            pass

    # open loops: prefer bonds, else crude from brief
    loops = list(bj.get("open_loops") or [])[:8]
    if not loops:
        for line in brief.splitlines():
            if line.strip().startswith("- ") and any(
                k in line.lower() for k in ("open", "next", "loop", "re-read", "check")
            ):
                loops.append(line.strip()[:160])
        loops = loops[:8]

    trail_excerpt: dict[str, Any] = {"active": False}
    if cfg.get("include_trail", True):
        try:
            from mag.run_trail import trail_pack_excerpt

            trail_excerpt = trail_pack_excerpt(max_events=12, max_chars=1600)
        except Exception as e:
            trail_excerpt = {"active": False, "error": str(e)}

    skills_excerpt = ""
    if cfg.get("include_skills", True):
        try:
            from mag.skills_pack import skills_for_job

            skills_excerpt = skills_for_job(job, max_chars=600)
        except Exception:
            skills_excerpt = ""

    ijl_skills = ""
    if cfg.get("include_ijl", True):
        try:
            from ijl_core import skill_excerpt_for_goal

            soft_goal = " ".join(
                [
                    goal[:200] if goal else "",
                    " ".join(loops[:3]) if loops else "",
                    (brief or "")[:200],
                ]
            ).strip() or "general harness dig"
            ijl_skills = skill_excerpt_for_goal(soft_goal, max_chars=500)
        except Exception as e:
            ijl_skills = f"(ijl skills: {e})"

    # Verkle tip badge — prove chain is live (LOAD continuity)
    tip_badge: dict[str, Any] = {"ok": False}
    dig_edges_n = 0
    try:
        tip_path = ROOT / "memory" / "biography" / "verkle_tip.json"
        if tip_path.is_file():
            tip = json.loads(tip_path.read_text(encoding="utf-8"))
            root = str(tip.get("root") or "")
            tip_badge = {
                "ok": True,
                "root_short": (root[:12] + "…") if len(root) > 12 else root,
                "n_leaves": tip.get("n_leaves"),
                "last_filename": tip.get("last_filename"),
                "last_session_id": tip.get("last_session_id"),
                "updated_minute": tip.get("updated_minute"),
            }
        res_dir = ROOT / "memory" / "biography" / "residual"
        if res_dir.is_dir() and not fast:
            dig_edges_n = _residual_census(res_dir)
        tip_badge["dig_edges_n"] = dig_edges_n
    except Exception as e:
        tip_badge = {"ok": False, "error": str(e)}
    # AG5: the badge is a VERDICT now, not a raw read — the chain verify rides
    # every launch (bounded 2s, never blocks boot; failure reason is rendered).
    v_ok, v_why = _verify_tip_chain()
    tip_badge["verified"] = v_ok
    tip_badge["verify_reason"] = v_why

    # Checkpoint restore — consume prior context via context_checkpoint
    checkpoint_restore: str = ""
    if checkpoint_session_id:
        try:
            from mag.context_checkpoint import restore_pointer

            checkpoint_restore = restore_pointer(checkpoint_session_id)
        except Exception as e:
            checkpoint_restore = f"(checkpoint restore error: {e})"

    # Agent state (versioned Grok/Mag recall — not session tip)
    agent_state_excerpt = ""
    agent_state_meta: dict[str, Any] = {}
    try:
        from mag.agent_state import load_latest, pack_excerpt

        agent_state_excerpt = pack_excerpt(max_chars=900)
        lat = load_latest()
        if lat:
            agent_state_meta = {
                "label": lat.get("label"),
                "content_commit": ((lat.get("content_commit") or {}).get("hex") or "")[:16],
                "n_versions": (lat.get("tip") or {}).get("n_versions"),
                "path": "memory/agent_state/LATEST.md",
            }
    except Exception as e:
        agent_state_excerpt = f"(agent_state: {e})"
        agent_state_meta = {"error": str(e)}

    continuity_excerpt = ""
    try:
        cont = ROOT / "memory" / "working" / "OPERATOR_CONTINUITY.md"
        if cont.is_file():
            continuity_excerpt = cont.read_text(encoding="utf-8", errors="replace")[:2200]
    except Exception as e:
        continuity_excerpt = f"(continuity: {e})"

    nervous: dict[str, Any] = {}
    try:
        from mag.nervous_system import pack_excerpt

        nervous = pack_excerpt(cached_glance) if fast else pack_excerpt()
    except Exception as e:
        nervous = {"schema": "nervous_system.v1", "error": str(e)}

    # Behavioral loop + compass (teach tools — avoid re-approving the same mistakes)
    behavioral_excerpt = ""
    compass_framework = ""
    try:
        from mag.preferences import inject_behavioral_pack
        if inject_behavioral_pack():
            from mag.governance import _latest_behavioral_leaf
            from mag.compass import FRAMEWORK_BLOCK

            leaf = _latest_behavioral_leaf()
            if leaf.get("themes"):
                lines = ["[BEHAVIORAL — recurring errors to avoid (file-backed)]"]
                for t in leaf["themes"][:5]:
                    lines.append(f"- {t['id']}: {t['title']}")
                    if t.get("avoid"):
                        lines.append(f"  avoid: {t['avoid'][:160]}")
                lines.append(f"source: {leaf.get('path', 'memory/improve/daily/')}")
                behavioral_excerpt = "\n".join(lines)[:1200]
            compass_framework = FRAMEWORK_BLOCK[:900]
    except Exception:
        pass

    tesuji_excerpt = ""
    try:
        from mag.preferences import inject_behavioral_pack
        if inject_behavioral_pack():
            from mag.tesuji_shell import latest_leaf_excerpt

            leaf = latest_leaf_excerpt(max_wins=3)
            if leaf.get("wins"):
                lines = ["[TESUJI SHELLS — emergent wins to repeat (file-backed)]"]
                for w in leaf["wins"]:
                    lines.append(f"- {w['id']}: {w['title']}")
                    if w.get("surprise"):
                        lines.append(f"  surprise: {w['surprise'][:140]}")
                    if w.get("maps_to") and w["maps_to"] != "unmapped":
                        lines.append(f"  maps_to: {w['maps_to']}")
                lines.append(f"source: {leaf.get('path', 'memory/improve/daily/')}")
                tesuji_excerpt = "\n".join(lines)[:900]
    except Exception:
        pass

    coordination_excerpt = ""
    if cfg.get("include_coordination", True):
        try:
            from mag.coordination import format_activity_excerpt

            coordination_excerpt = format_activity_excerpt(limit=6, max_chars=900)
        except Exception:
            coordination_excerpt = ""
        try:
            from mag.tripartite_boot import format_tripartite_excerpt

            trip = format_tripartite_excerpt(max_chars=700)
            if trip:
                coordination_excerpt = (coordination_excerpt + "\n\n" + trip).strip()
        except Exception:
            pass
        try:
            from mag.peer_handoff import format_latest_brief

            peer = format_latest_brief()
            if peer and peer not in coordination_excerpt:
                coordination_excerpt = (coordination_excerpt + "\n\n" + peer).strip()[:1600]
        except Exception:
            pass

    soft_goal = " ".join(
        [
            goal[:200] if goal else "",
            " ".join(loops[:3]) if loops else "",
            (brief or "")[:200],
        ]
    ).strip() or "general harness dig"
    try:
        from mag.preferences import inject_behavioral_pack
        if inject_behavioral_pack():
            from mag.decision_framework import format_tips_block, surface_tips

            tips_block = format_tips_block(surface_tips(goal=soft_goal))
            if tips_block:
                behavioral_excerpt = (behavioral_excerpt + "\n\n" + tips_block).strip()[:1400]
    except Exception:
        pass
    if tesuji_excerpt:
        behavioral_excerpt = (behavioral_excerpt + "\n\n" + tesuji_excerpt).strip()[:1800]
    mirror_voice_excerpt = ""
    clue_chain_excerpt = ""
    zeitgeist_excerpt = ""
    if cfg.get("include_mirror_clue", True):
        mirror_voice_excerpt = _mirror_voice_excerpt(soft_goal, max_chars=600)
        clue_chain_excerpt = _clue_chain_excerpt(max_chars=500)
    zeitgeist_excerpt = _zeitgeist_excerpt(max_chars=800) if mode not in ("janitor",) else ""

    build_excerpt = ""
    if cfg.get("include_build"):
        build_excerpt = _read_build_excerpt(build_path, max_chars=4000)
        if not build_excerpt and scope_slug:
            slug = scope_slug
            for p in (ROOT / "docs" / "ref").glob(f"BUILD-{slug}.md"):
                build_excerpt = _read_build_excerpt(p, max_chars=4000)
                break

    scope_excerpt = ""
    if cfg.get("include_scope"):
        scope_excerpt = _latest_scope_card(slug=scope_slug)

    pack = {
        "schema": "mag_context_pack.v1",
        "mode": mode,
        "job": job,
        "pack_max_chars": cfg.get("max_chars"),
        "ts": datetime.now(timezone.utc).isoformat(),
        "for": "grok_tui_router",
        "token_note": "Use this instead of chat_history. Escalate only hard work.",
        "operator_path": "FIND → FILE → LOAD (docs/ref/OPERATOR_CARD.md)",
        "layers": ["L0_nervous", "L0_policy", "L0e_resonance", "L0c_directives", "L1_bonds", "L2_trail", "L3_task", "L4_heat"],
        "nervous_system": nervous,
        "tip": tip_badge,
        "agent_state": agent_state_excerpt,
        "agent_state_meta": agent_state_meta,
        "continuity": continuity_excerpt,
        "health": {
            "status": s.get("status"),
            "live_stale": (s.get("recording") or {}).get("live_stale"),
            "port_8765": (s.get("integral") or {}).get("port_8765"),
        },
        "models": {
            "clerk": roles.get("clerk") or roles.get("router"),
            "worker": roles.get("worker"),
            "multi_smoke_ok": smoke.get("ok"),
            "multi_smoke_models": smoke.get("models_seen"),
        },
        "brief": brief or "(no brief — run: mag.cmd brief)",
        "bonds": bonds_text or "(no bonds — run: mag.cmd bonds)",
        "bonds_meta": bonds_meta,
        "open_loops": loops,
        "run_trail": trail_excerpt,
        "skills_excerpt": skills_excerpt,
        "proven_moves": _proven_moves_excerpt(),
        "quantized_laws": _quantized_laws(),
        "rib_vault": _rib_vault_law(),
        "solved_excerpt": _solved_excerpt(),
        "ijl_skills": ijl_skills,
        "mirror_voice_excerpt": mirror_voice_excerpt,
        "clue_chain_excerpt": clue_chain_excerpt,
        "build_excerpt": build_excerpt,
        "scope_excerpt": scope_excerpt,
        "behavioral_excerpt": behavioral_excerpt,
        "compass_framework": compass_framework,
        "checkpoint_restore": checkpoint_restore,
        "coordination_excerpt": coordination_excerpt,
        "zeitgeist_excerpt": zeitgeist_excerpt,
        "resonance_cards": resonance_cards,
        "resonance_l0e": resonance_l0e,
        "dirac_loops": _dirac_loop_count(),
        "live_tail": live or "(no live board)",
        "attention_tail": att[:400] if att else "",
        "directives": directives or "",
        "doctrine": _rib_doctrine(),
        "subchain_full": "",
        "world_state": "",
        "full_context": False,
        "todo_open": [
            ln.strip()
            for ln in todo.splitlines()
            if ln.strip().startswith("- [ ]")
        ][:12],
        "commands": {
            "load": "mag.cmd context-pack",
            "ask": 'mag.cmd ask "…"',
            "bonds": "mag.cmd bonds",
            "trail": 'mag.cmd trail start "goal" --seat local --proactivity narrow',
            "route": 'mag.cmd route "…"',
            "lab": "mag.cmd lab",
            "smoke": "mag.cmd multi-smoke",
        },
    }
    if _env_on("MAG_FULL_CONTEXT") and mode == "full":
        full_limit = _full_context_limit()
        pack["full_context"] = True
        pack["pack_max_chars"] = full_limit
        try:
            from mag.party_subchain import mount as _ps_mount
            _m = _ps_mount(full=True)
            pack["subchain_full"] = _head_tail(str(_m.get("transcript") or ""), full_limit)
            pack["subchain_n"] = _m.get("n")
            pack["subchain_full_flag"] = bool(_m.get("full"))
        except Exception as exc:
            pack["subchain_full"] = f"(mount failed: {exc})"
        pack["doctrine"] = _rib_doctrine(max_chars=min(12000, full_limit // 3))
        try:
            from mag import game_world as _gw
            st = getattr(_gw, "status", None) or getattr(_gw, "world_status", None)
            pack["world_state"] = st() if callable(st) else str(st or "")
        except Exception:
            pack["world_state"] = ""
    return pack


def infer_pack_mode(goal: str = "", *, depth: str = "") -> str:
    """Pick pack mode from goal tags and route depth."""
    g = (goal or "").lower()
    d = (depth or "").lower()
    if g.startswith("[steward]") or d == "scut":
        return "janitor"
    if "[build]" in g or d in ("heavy_code", "simple_code"):
        return "build"
    if "audit" in g or d == "audit":
        return "audit"
    if "[priority]" in g or d == "plan":
        return "plan"
    if d in ("overview", "route"):
        return "route"
    return "full"


def format_context_pack_text(
    pack: dict[str, Any] | None = None,
    *,
    mode: str | None = None,
    max_chars: int | None = None,
) -> str:
    """Layered pack: policy core (objective/laws/directives/doctrine) → context → task.

    Shed ladder: 1 drop heat, 2 compact task, 3 shed context blocks one at a
    time (core + worker contract + task never shed), 4 hard clip last resort.
    ReFold (port-order lane P5, 2026-10-07): rungs 1-3 file a reversible stub
    (section name + source organ + content sha256 + chars) into the offload
    row, so a shed is a restorable pointer, never silent telemetry; stage 3
    also leaves one fold-marker line in the render naming the restore door.
    Restore re-renders the section from the stub's named source, sha-verified
    (restore_shed_section). Stubs are pure functions of the shed content, so
    consecutive renders between fold advances stay byte-identical.
    """
    p = pack or build_context_pack()
    mode = _normalize_mode(mode or p.get("mode"))
    cfg = MODE_CONFIG[mode]
    # Escape hatch: MAG_FULL_CONTEXT lifts the per-mode core caps too — the
    # operator asked for the whole surface, not a capped one.
    esc = _env_on("MAG_FULL_CONTEXT") and mode == "full"

    def _core_cap(key: str) -> int:
        if esc:
            return 1 << 30
        return int(cfg.get(key) or 0)

    if esc:
        max_chars = _full_context_limit()
    elif max_chars is None:
        max_chars = int(cfg.get("max_chars") or 4500)
    compact_ns = bool(cfg.get("compact_nervous"))
    tip = p.get("tip") or {}
    if tip.get("ok"):
        tip_line = (
            f"- tip: {tip.get('root_short')} · leaves={tip.get('n_leaves')} · "
            f"last={tip.get('last_filename')} · dig_edges={tip.get('dig_edges_n', 0)}"
        )
        # AG5: a failed (or timed-out) chain verify demotes the badge to
        # UNVERIFIED with the reason — never a confident raw read again.
        if tip.get("verified") is False:
            tip_line = f"- tip: UNVERIFIED ({tip.get('verify_reason') or 'reason unknown'})"
    else:
        tip_line = f"- tip: (unavailable) {tip.get('error') or ''}"
    as_meta = p.get("agent_state_meta") or {}
    as_line = (
        f"- agent_state: label={as_meta.get('label')} commit={as_meta.get('content_commit')} "
        f"n={as_meta.get('n_versions')} · LOAD before redesign"
        if as_meta.get("label")
        else "- agent_state: (none — main.py agent-state --commit)"
    )
    ns = p.get("nervous_system") or {}
    body = ns.get("body") or {}
    keys_line = ns.get("keys_line") or ""
    if not keys_line:
        key_bits = []
        for row in ns.get("keys") or []:
            if isinstance(row, dict):
                key_bits.append(f"{row.get('id')}={row.get('status') or '—'}")
        keys_line = ", ".join(key_bits)
    ns_lines = [
        "### L0a Nervous system (agent ops subsystem — default LOAD)",
        f"- body_ok={ns.get('ok')} integral_ok={ns.get('integral_ok')}",
        f"- dash:8765={'UP' if body.get('dashboard_8765') else 'DOWN'} · "
        f"ollama={'UP' if body.get('ollama_11434') else 'DOWN'} · "
        f"smoke={'PASS' if body.get('multi_smoke_ok') else 'FAIL'}",
    ]
    if not compact_ns:
        ns_lines.extend([
            f"- session tip: {(ns.get('session_tip') or {}).get('root_short')}… "
            f"leaves={(ns.get('session_tip') or {}).get('n_leaves')}",
            f"- agent tip: {(ns.get('agent_tip') or {}).get('root_short')}… "
            f"commit={(ns.get('agent_tip') or {}).get('commit8')}",
            f"- keys: {keys_line or '(none)'}",
            f"- note: {ns.get('note') or 'probe before claim seats'}",
            f"- face: {ns.get('path') or 'memory/nervous_system.md'} · CLI: main.py nervous",
        ])
    ns_lines.append("")
    policy = [
        f"# Mag context pack · mode={mode} ({p.get('ts', '')[:19]})",
        "",
        "## L0 Policy (stable — pack-first, residual DNA, seat purity)",
        f"- path: {p.get('operator_path') or 'FIND → FILE → LOAD'}",
        "- Use this pack only; do not reload full chat.",
        "- Remotes: pack+goal only. T0/T1 never remote.",
        tip_line,
        (lambda d: f"- dirac loops: closed={d.get('closed', 0)} / total={d.get('total', 0)}")(p.get("dirac_loops") or {}),
        f"- health: {p.get('health')}",
        "",
    ]
    # R4-L1 component-age stamp: the boot-surface organs' ages ride the pack
    # header so a seat can SEE which organs are fresh without trusting a
    # sibling to have regenerated them (the disease the R4 synthesis named).
    # The key is set ONLY by the context-pack CLI's fired chain report
    # (main.py: run_boot_regen) - in-process builds stay byte-stable so the
    # calibrated pack-budget gates (test_context_pack_delivery) are not
    # tipped by a live-mtime line.
    _br = p.get("boot_regen") or {}
    if _br.get("ages"):
        _bits = []
        for _k, _a in (_br.get("ages") or {}).items():
            if not _a.get("exists"):
                _bits.append(f"{_k}=MISSING")
            elif _a.get("age_d") is None:
                _bits.append(f"{_k}=unreadable")
            else:
                _bits.append(f"{_k}={_a.get('age_d')}d")
        _bv = str(_br.get("verdict") or ("not-run" if not _br.get("fired") else "?"))
        policy.insert(len(policy) - 1,
                      f"- boot_regen: {_bv} · " + " · ".join(_bits)
                      + f" (bar {PACK_STALE_DAYS:g}d, mag/boot_regen.py)")
    # CODE-AS-LAW (rib_grammar action=guard): the standing objective ships in
    # every pack, first layer, by architecture. Reading it is not optional —
    # and it is BOUNDED: the old read was uncapped and had no errors="replace",
    # so the 2.2k objective alone overflowed the janitor/route budgets and one
    # non-UTF8 byte in the file would crash every render for every caller
    # (wave5 render-pipe repair, 2026-09-29).
    _objective_path = Path(__file__).resolve().parents[1] / "memory" / "boot" / "CURRENT_OBJECTIVE.md"
    if _objective_path.is_file():
        try:
            _objective_text = _objective_path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            _objective_text = ""
        if _objective_text:
            _obj_cap = _core_cap("max_objective")
            _shown = _objective_text[:_obj_cap]
            if len(_objective_text) > len(_shown):
                _shown += (f"\n…(objective clipped at {_obj_cap} chars — "
                           "full text: memory/boot/CURRENT_OBJECTIVE.md)")
            policy.append("### L0b Current objective (the standing thesis — carry it into every reply)")
            policy.append(_shown)
            policy.append("")
    # The mandated core rides in `policy` PROPER — objective, compiled laws,
    # operator directives, RIB doctrine — so no shed rung can drop it. The old
    # layout kept directives in the sheddable ctx tier, so the bare-policy
    # ladder rung dropped them in every overflow render (0/6 live renders
    # measured, arch-01) while its own comment claimed the directive tier
    # survived; doctrine was gated plan/full/build/audit and then rung-3 shed
    # it everywhere (0/6). Cause+receipt: quantizer landing 3eb6dc251
    # (2026-09-27) + wave5 render-pipe repair (2026-09-29).
    if p.get("quantized_laws"):
        policy.extend([
            "### L0b Compiled laws (thought quantizer, flash tier — obey)",
            str(p.get("quantized_laws"))[:_core_cap("max_laws")],
            "",
        ])
    if p.get("directives"):
        policy.extend([
            "### L0c Operator directives (autonomy contract — operator-set, stable)",
            str(p.get("directives"))[:_core_cap("max_directives")],
            "",
        ])
    if p.get("doctrine"):
        policy.extend([
            "### L0d RIB Doctrine (the system's understanding — memweave)",
            str(p.get("doctrine"))[:_core_cap("max_doctrine")],
            "",
        ])
    # R4-L2 (2026-10-05): the rib_boot vault block renders as ONE sheddable
    # context block ("L0d rib vault amendments", built below) with ZERO core
    # footprint -- tonight's live content already pins build/full at their
    # budgets, and an additive core line would tip plan over and cannibalize
    # janitor bonds under the ladder. The block sheds after L1 bonds (last
    # before the hard clip; p1a-L0d-fix 2026-10-07 reprioritized it ahead of
    # skills/trail per the operator ask after d01 measured the carrier dying
    # at stage 3) and every shed is offloaded, never silent.
    _rv = p.get("rib_vault") or {}
    # Contextual-history tier (sheddable one block at a time under the clip
    # ladder, never ahead of the worker contract): the L0d/L0f context blocks
    # sit here, not in `policy`. Cause+receipt: quantizer landing 3eb6dc251
    # (2026-09-27) moved laws ahead of the shed tier; wave5 (2026-09-29)
    # moved directives+doctrine into the core too and made the ladder shed
    # per block instead of all-or-nothing.
    policy_ctx_a: list[tuple[str, list[str]]] = []
    if p.get("full_context") and mode == "full":
        policy_ctx_a.append(("L0f full mounted subchain + world state", [
            "",
            "### L0f Full mounted subchain (reasoning surface; chain is still the record)",
            p.get("subchain_full") or "(empty)",
            "",
            "### L0f World state",
            str(p.get("world_state") or "(none)"),
            "",
        ]))
    if p.get("proven_moves") and mode in ("plan", "full", "build", "audit"):
        policy_ctx_a.append(("L0d proven moves", [
            "",
            "### L0d Proven moves (verified case law — trust these)",
            p.get("proven_moves"),
            "",
        ]))
    if p.get("solved_excerpt") and mode in ("plan", "full", "build", "audit"):
        policy_ctx_a.append(("L0d solved history", [
            "",
            "### L0d Solved history (what the system already holds — don't redo)",
            p.get("solved_excerpt"),
            "",
        ]))
    policy_mid = list(ns_lines)
    if mode != "janitor":
        policy_mid.extend([
            as_line,
            f"- models: {p.get('models')}",
            f"- bonds_meta: {p.get('bonds_meta')}",
        ])
    policy_ctx_b: list[tuple[str, list[str]]] = []
    if p.get("zeitgeist_excerpt"):
        policy_ctx_b.append(("L0d zeitgeist", [
            "",
            "### L0d Zeitgeist (project epoch + signal)",
            p.get("zeitgeist_excerpt"),
        ]))
    if mode not in ("janitor", "route"):
        policy_ctx_b.append(("L0b agent state", [
            "",
            "### L0b Agent state (versioned self — Verkle agent tip)",
            p.get("agent_state") or "(none)",
        ]))
        if p.get("continuity"):
            policy_ctx_b.append(("L0-continuity", [
                "",
                "### L0-continuity (goals · gaps · eject · smokes — cold Grok must use this)",
                "path: memory/working/OPERATOR_CONTINUITY.md",
                p.get("continuity"),
            ]))
    if p.get("behavioral_excerpt") and mode not in ("janitor",):
        policy_ctx_b.append(("L0 behavioral + tesuji tips", ["", p.get("behavioral_excerpt")]))
    if p.get("coordination_excerpt") and mode in ("route", "build", "audit", "plan", "full"):
        policy_ctx_b.append(("L0 coordination", ["", p.get("coordination_excerpt")]))
    if p.get("resonance_l0e") and cfg.get("include_resonance"):
        policy_ctx_b.append(("L0e resonance", ["", p.get("resonance_l0e")]))
    # p1a-L0d-fix (2026-10-07): the vault amendment bodies + digest -- one
    # sheddable block that sheds only AFTER skills/trail/L1 bonds (last
    # before the hard clip), so convenience context goes first and fat modes
    # carry the mounted law.
    if _rv.get("body"):
        policy_ctx_b.append(("L0d rib vault amendments", [
            "",
            "### L0d RIB vault amendments (POST-DATUM law deltas - mounted from memory/rib_boot.json)",
            _rv["body"],
        ]))
    policy_full = (
        policy
        + [line for _, lines in policy_ctx_a for line in lines]
        + policy_mid
        + [line for _, lines in policy_ctx_b for line in lines]
    )
    bonds = []
    if mode != "janitor" or (p.get("bonds") and "(no bonds" not in str(p.get("bonds"))):
        bonds = [
            "",
            "## L1 Bonds (next-session / residual edges)",
            (p.get("bonds") or "(none — run: python main.py bonds)")[:800 if mode == "janitor" else 5000],
        ]
    skills = []
    if cfg.get("include_skills") and p.get("skills_excerpt"):
        skills = [
            "",
            "## L1b Skills (progressive — not MCP flood)",
            p.get("skills_excerpt") or "(none — configs/skills.yaml)",
        ]
        if cfg.get("include_ijl") and p.get("ijl_skills"):
            skills.extend([
                "",
                "### L1b IJL skill beads (episode distill)",
                p.get("ijl_skills") or "(none yet)",
            ])
    if p.get("mirror_voice_excerpt"):
        skills.extend(["", "### L1c Mirror voice (operator corpus)", p.get("mirror_voice_excerpt")])
    if p.get("clue_chain_excerpt"):
        skills.extend(["", "### L1c Clue chain", p.get("clue_chain_excerpt")])

    build_block = []
    if p.get("build_excerpt"):
        build_block = [
            "",
            "## L2b Frozen BUILD (builder seat — do not mutate spec)",
            p.get("build_excerpt") or "",
        ]
    scope_block = []
    if p.get("scope_excerpt"):
        scope_block = [
            "",
            "## L2c Scope card (steward — dumb-agent brief)",
            p.get("scope_excerpt") or "",
        ]

    trail = []
    if cfg.get("include_trail"):
        trail = [
            "",
            "## L2 Trail cores (mid-run continuity — re-inject)",
            (p.get("run_trail") or {}).get("text")
            or "(no open run — python main.py trail start \"goal\")",
        ]
    task = [
        "",
        "## L3 Task (brief + loops + todo)",
        "### Brief",
        (p.get("brief") or "")[:400 if mode == "janitor" else 5000],
        "",
        "### Open loops",
        "\n".join(p.get("open_loops") or ["(none extracted)"])[:400 if mode == "janitor" else 2000],
    ]
    if mode not in ("janitor",):
        task.extend([
            "",
            "### Todo open",
            "\n".join(p.get("todo_open") or ["(none)"]),
        ])
    heat = []
    if cfg.get("include_heat"):
        heat = [
            "",
            "## L4 Heat (drop first under compaction)",
            "### Live tail",
            p.get("live_tail") or "",
            "",
            "### Attention",
            p.get("attention_tail") or "",
            "",
            "_Grok: answer from this. Re-inject trail cores if run active._",
        ]
    parts = [policy_full, bonds, skills, build_block, scope_block, trail, task, heat]
    text = "\n".join("\n".join(x) for x in parts)
    task_small = task
    shed_stubs: list[dict[str, Any]] = []
    if max_chars is not None and len(text) > max_chars:
        # The frozen BUILD and scope are the worker's actual contract; never
        # discard them while retaining contextual history. ReFold (P5
        # 2026-10-07): the dropped heat files a reversible stub (section +
        # source organ + content sha256) into the offload row instead of
        # staying silent; restore re-renders it sha-verified.
        _heat_content = "\n".join(heat)
        _heat_stub = {
            "section": "L4 Heat (live_tail, attention)",
            "source": SHED_SOURCES["L4 Heat (live_tail, attention)"],
            "sha256": _content_sha(_heat_content),
            "chars": len(_heat_content),
        }
        shed_stubs.append(_heat_stub)
        parts = [policy_full, build_block, scope_block, bonds, skills, trail, task]  # drop L4 heat
        _emit_pack_offload(p, mode, max_chars, len(text),
                           ["L4 Heat (live_tail, attention)"], 1, stubs=[_heat_stub])
        text = "\n".join("\n".join(x) for x in parts)
    if max_chars is not None and len(text) > max_chars:
        _task_content = "\n".join(task)
        _task_stub = {
            "section": "L3 Task (compacted)",
            "source": SHED_SOURCES["L3 Task (compacted)"],
            "sha256": _content_sha(_task_content),
            "chars": len(_task_content),
        }
        shed_stubs.append(_task_stub)
        brief = (p.get("brief") or "")[:800]
        task_small = [
            "",
            "## L3 Task (compacted)",
            "### Brief",
            brief + ("…" if len(p.get("brief") or "") > 800 else ""),
            "",
            "### Open loops",
            "\n".join((p.get("open_loops") or [])[:5] or ["(none)"]),
        ]
        _emit_pack_offload(p, mode, max_chars, len(text),
                           ["L3 Task (compacted)"], 2, stubs=[_task_stub])
        text = "\n".join(
            "\n".join(x) for x in [policy_full, build_block, scope_block, bonds, skills, trail, task_small]
        )
    if max_chars is not None and len(text) > max_chars:
        # Rung 3: shed context ONE BLOCK AT A TIME, least load-bearing first,
        # instead of the old all-or-nothing ctx drop. The mandated core
        # (objective/laws/directives/doctrine — inside `policy`), the frozen
        # worker contract, and the task NEVER shed here. The old bare-policy
        # rung rebuilt the pack without policy_ctx_b, so operator directives
        # silently vanished in every overflow render (0/6 live renders,
        # arch-01) even though this comment claimed the directive tier
        # survived; and the parts order put task last, so the final hard
        # clip amputated the job in 5/6 renders. Under pressure the layout
        # becomes the protection order: contract -> task -> everything else.
        policy_bare = policy + policy_mid
        sheddable: list[tuple[str, list[str]]] = (
            list(policy_ctx_a)
            + list(policy_ctx_b)
            + ([("L1b/L1c skills + ijl + mirror/clue", skills)] if skills else [])
            + ([("L2 trail", trail)] if trail else [])
            + ([("L1 bonds", bonds)] if bonds else [])
        )
        shed_order = [
            "L0f full mounted subchain + world state",
            "L0e resonance",
            "L0 coordination",
            "L0 behavioral + tesuji tips",
            "L0d zeitgeist",
            "L0-continuity",
            "L0b agent state",
            "L0d proven moves",
            "L0d solved history",
            "L1b/L1c skills + ijl + mirror/clue",
            "L2 trail",
            "L1 bonds",
            # p1a-L0d-fix (2026-10-07, supersedes the R4-L2 placement): mounted
            # vault law sheds LAST, after skills, trail and bonds -- the d01
            # dogfood2 evidence measured the carrier dying at stage 3 (9471 >
            # 7200) ahead of skills/trail, so POST-DATUM law never reached
            # fresh seats. Law outlives convenience context, not the reverse.
            # The shed is offloaded, never silent.
            "L0d rib vault amendments",
        ]
        alive = list(sheddable)
        fold_note = 0
        for _shed_name in shed_order:
            if len(text) <= max_chars:
                break
            if _shed_name not in {n for n, _ in alive}:
                continue
            # ReFold (P5 2026-10-07): the shed block files a reversible stub
            # (section + source organ + content sha256 + chars) into the
            # offload row, and one fold marker line in the render names the
            # restore door. Per-section pointer bytes stay out of the render
            # on purpose: measured on the live tree they are net-negative on
            # the tight mode budgets (route sheddable ~775 bytes vs ~1100 of
            # stubs); see _shed_fold_marker.
            _shed_block = next(ls for n, ls in alive if n == _shed_name)
            _content = "\n".join(_shed_block)
            _stub = {
                "section": _shed_name,
                "source": SHED_SOURCES.get(_shed_name, "pack (unmapped organ)"),
                "sha256": _content_sha(_content),
                "chars": len(_content),
            }
            shed_stubs.append(_stub)
            fold_note += 1
            alive = [b for b in alive if b[0] != _shed_name]
            _seqs = ([policy_bare, build_block, scope_block, task_small]
                     + [ls for _, ls in alive]
                     + [[_shed_fold_marker(fold_note)]])
            text = "\n".join("\n".join(x) for x in _seqs)
            _emit_pack_offload(p, mode, max_chars, len(text), [_shed_name], 3,
                               stubs=[_stub])
    if max_chars is not None and len(text) > max_chars:
        _emit_pack_offload(pack, mode, max_chars, len(text), ["hard clip"], 4)
        text = text[: max_chars - 20] + "\n…(pack clipped)"
    return text


def format_agent_preamble(
    pack: dict[str, Any] | None = None,
    *,
    goal: str = "",
    max_chars: int = 2200,
) -> str:
    """Blind-men coarse elephant for subagents/workflow workers.

    Nervous + tip + open loops + trail cores + optional goal.
    No L4 heat, no full bonds dump, no residual DNA.
    Law: docs/ref/COORDINATION_ELIAS_ROPE.md
    """
    p = pack or build_context_pack()
    tip = p.get("tip") or {}
    if tip.get("ok"):
        tip_line = (
            f"tip={tip.get('root_short')} leaves={tip.get('n_leaves')} "
            f"last={tip.get('last_filename')}"
        )
        # AG5: preamble rides the same verify verdict as the pack render.
        if tip.get("verified") is False:
            tip_line = f"tip=UNVERIFIED ({tip.get('verify_reason') or 'reason unknown'})"
    else:
        tip_line = f"tip=unavailable {tip.get('error') or ''}"
    ns = p.get("nervous_system") or {}
    body = ns.get("body") or {}
    keys_line = ns.get("keys_line") or ""
    if not keys_line:
        key_bits = []
        for row in ns.get("keys") or []:
            if isinstance(row, dict):
                key_bits.append(f"{row.get('id')}={row.get('status') or '—'}")
        keys_line = ", ".join(key_bits)
    loops = p.get("open_loops") or []
    loops_txt = "\n".join(f"- {x}" for x in loops[:6]) if loops else "- (none)"
    trail = p.get("run_trail") or {}
    trail_txt = trail.get("text") or "(no open run)"
    if len(trail_txt) > 700:
        trail_txt = trail_txt[:700] + "…"
    base_id = trail.get("base_id") or (trail.get("base") or {}).get("base_id") or ""
    base_tip = (trail.get("base") or {}).get("tip_root_short") or ""
    base_git = (trail.get("base") or {}).get("git_sha") or ""
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


if __name__ == "__main__":
    raise SystemExit(_main())
