"""corpus_self_lens — run the 6 corpus lenses over MAG's OWN framework corpus, then
map the surfaced findings onto the operational surface (framework_map groups) for
future data usage.

The operator (2026-08-09): "revisit our entire corpus via our lenses as we did with
that dude's repo and lets see what we can surface and classify" + "map it all to our
operational surface artifact/via for future data usage."

Two stages, both framework-native (no ad-hoc terminal):
  STAGE A  build_manifest() + enqueue()  — walk docs/, mag/ docstrings, memory/ key
           prose into a `_manifest.json`, then spawn the 6 lenses (bard, structure,
           evolution, semantic, behavioral, safety) on the cheap tier
           (deepseek-v4-flash) via orchestrator.spawn_task -> the passive queue
           drainer eats them. Each lens writes memory/runs/corpus_self/lenses/<lens>.md
           + appends to _lens_training.jsonl.

  STAGE B  map_to_surface()  — read the landed lens training records and attach each
           finding to the matching framework_map group (steer/decide/state/learn/run/
           ops/agents/launcher/route/provider). Emits memory/graph/lens_surface.json
           (schema lens_surface.v1) so any future consumer (dashboard, context_pack,
           improve_loop) can read "what the corpus surfaces per operational group."

Usage:
  python -m tools.corpus_self_lens manifest   (build manifest + enqueue lenses)
  python -m tools.corpus_self_lens map        (map landed findings -> framework_map groups)
  python -m tools.corpus_self_lens status     (lenses enqueued + landed so far)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT = ROOT / "memory" / "runs" / "corpus_self"
MANIFEST = OUT / "_manifest.json"
LENSES = OUT / "lenses"
TRAINING = LENSES / "_lens_training.jsonl"

# Operational surface groups (must match framework_map.json ids).
SURFACE_GROUPS = [
    "steer", "decide", "state", "learn", "run",
    "ops", "agents", "launcher", "route", "provider",
]

# Keyword families used to attach a lens finding to an operational group (deterministic).
_GROUP_KEYWORDS: dict[str, list[str]] = {
    "steer":   ["ghost", "inbox", "steer", "skill", "aimbot", "deploy", "vector", "socratic"],
    "decide":  ["router", "tier", "escalat", "model_shape", "agent_state", "shape", "depth", "routing"],
    "state":   ["verkle", "ledger", "knot", "case law", "memory", "pile", "witness", "snapshot"],
    "learn":   ["fold", "tesuji", "improve", "skill_ledger", "remedy", "case_law", "retrospect"],
    "run":     ["queue", "job", "orchestrator", "drain", "spec_gate", "spawn", "task", "pipeline"],
    "ops":     ["watch", "diagnos", "graph", "monitor", "supervisor", "health", "doctor", "gap"],
    "agents":  ["agent", "gpipes", "desk", "seat", "arena", "swarm", "fan_out", "sub-agent", "flock"],
    "launcher":["launch", ".cmd", "wake", "boot", "supervisor up"],
    "route":   ["/api", "rest", "endpoint", "route"],
    "provider":["deepseek", "ollama", "grok", "xai", "provider", "model", "flash", "pro"],
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _walk_corpus_files() -> list[dict[str, Any]]:
    """Walk the framework's own prose/docs/docstring corpus into manifest entries."""
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    # Prose docs
    for sub, exts in (("docs", {".md", ".txt"}), ("memory", {".md"})):
        base = ROOT / sub
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in exts:
                continue
            if any(seg.startswith("_") or seg in (".git", "node_modules", "trash") for seg in p.parts):
                continue
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            try:
                sz = p.stat().st_size
            except OSError:
                sz = 0
            if rel in seen:
                continue
            seen.add(rel)
            entries.append({"name": p.name, "path": rel, "bytes": sz, "type": "doc"})
    # Top-level prose (README, AGENTS, CONSTITUTION, LOAD, HANDOFF)
    for name in ("README.md", "AGENTS.md", "CONSTITUTION.md", "LOAD.md", "HANDOFF_MAG_AGENT_TODOS.md"):
        p = ROOT / name
        if p.is_file():
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            if rel not in seen:
                seen.add(rel)
                entries.append({"name": p.name, "path": rel, "bytes": p.stat().st_size, "type": "doc"})
    # Module docstrings (mag/*.py first 200 chars = the "what is this" surface)
    mag = ROOT / "mag"
    if mag.is_dir():
        for p in sorted(mag.glob("*.py")):
            rel = f"mag/{p.name}"
            if rel in seen:
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            head = txt[:600]
            entries.append({"name": p.name, "path": rel, "bytes": len(head), "type": "docstring", "head": head})
    return entries


def build_manifest() -> dict[str, Any]:
    """Write _manifest.json over our own corpus. Returns summary."""
    OUT.mkdir(parents=True, exist_ok=True)
    entries = _walk_corpus_files()
    manifest = {
        "schema": "corpus_self.v1",
        "root": str(ROOT),
        "ts": _now(),
        "groups": SURFACE_GROUPS,
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return {"ok": True, "files": len(entries), "manifest": str(MANIFEST.relative_to(ROOT))}


def enqueue(provider: str = "deepseek", model: str = "deepseek-v4-flash") -> dict[str, Any]:
    """Enqueue the 6 lenses through the passive queue (cheap tier)."""
    from tools.corpus_lens import LENSES as LENS_SPECS, _write_lens_spec
    from mag.orchestrator import spawn_task

    LENSES.mkdir(parents=True, exist_ok=True)
    diff_path = LENSES / "_diff_training.jsonl"
    if not diff_path.is_file():
        diff_path.write_text("", encoding="utf-8")
    tasks = []
    for lens in LENS_SPECS:
        spec = _write_lens_spec(LENSES, lens, str(ROOT), str(MANIFEST), str(diff_path))
        goal = (
            f"Execute the lens spec at {spec}. Read the corpus manifest ({MANIFEST}), "
            f"sample up to 60 documents from {ROOT} (docs/, mag/ docstrings, memory/ prose, "
            f"README/AGENTS/CONSTITUTION). {lens['prompt']} "
            f"Deliverable: write {LENSES / lens['name']}.md and append a training record "
            f"(schema corpus_lens.v1: lens, focus, ts, summary, findings[], quotes[]) to "
            f"{TRAINING}. Be concrete, cite file names."
        )
        r = spawn_task(goal=goal, provider=provider, model=model, tag="corpus-self-lens")
        tasks.append({"lens": lens["name"], "spec": str(spec), **r})
    idx = {
        "schema": "corpus_self.v1", "ts": _now(), "stage": "enqueue",
        "corpus": str(ROOT), "tasks": tasks,
    }
    (OUT / "_lens_index.json").write_text(json.dumps(idx, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return {"ok": True, "enqueued": len(tasks), "tasks": [
        {"lens": t["lens"], "task_id": t.get("task_id"), "ok": t.get("ok")} for t in tasks]}


def _attach_group(text: str) -> str:
    """Deterministic keyword attach of a finding to one operational group."""
    t = (text or "").lower()
    best, best_hits = "learn", 0
    for gid, kws in _GROUP_KEYWORDS.items():
        hits = sum(1 for k in kws if k in t)
        if hits > best_hits:
            best, best_hits = gid, hits
    return best


def _read_training() -> list[dict[str, Any]]:
    if not TRAINING.is_file():
        return []
    rows = []
    for line in TRAINING.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def map_to_surface() -> dict[str, Any]:
    """Attach landed lens findings to framework_map groups -> lens_surface.json."""
    rows = _read_training()
    per_group: dict[str, list[dict[str, Any]]] = {g: [] for g in SURFACE_GROUPS}
    findings_total = 0
    for row in rows:
        lens = row.get("lens") or "?"
        findings = row.get("findings") or []
        if isinstance(findings, str):
            findings = [findings]
        if not findings:
            findings = [row.get("summary") or ""]
        for f in findings:
            ft = str(f)
            findings_total += 1
            g = _attach_group(ft + " " + lens)
            per_group.setdefault(g, []).append({
                "lens": lens, "finding": ft[:300],
                "source": row.get("ts", ""),
            })
    surface = {
        "schema": "lens_surface.v1",
        "ts": _now(),
        "lenses_landed": len(rows),
        "findings_total": findings_total,
        "per_group": {g: v for g, v in per_group.items() if v},
    }
    out = ROOT / "memory" / "graph" / "lens_surface.json"
    out.write_text(json.dumps(surface, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return {"ok": True, "landed": len(rows), "findings": findings_total,
            "groups_hit": sorted(per_group.keys()), "surface": str(out.relative_to(ROOT))}


def status() -> dict[str, Any]:
    idx = OUT / "_lens_index.json"
    enq = []
    if idx.is_file():
        try:
            enq = json.loads(idx.read_text(encoding="utf-8")).get("tasks", [])
        except Exception:
            pass
    rows = _read_training()
    return {
        "ok": True, "enqueued": len(enq),
        "landed": len(rows),
        "landed_lenses": sorted({r.get("lens") or "?" for r in rows}),
        "out": str(LENSES.relative_to(ROOT)),
        "training": str(TRAINING.relative_to(ROOT)),
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "status"
    if cmd == "manifest":
        bm = build_manifest()
        print(json.dumps(bm, indent=2))
        print(json.dumps(enqueue(), indent=2))
    elif cmd == "enqueue":
        print(json.dumps(enqueue(), indent=2))
    elif cmd == "map":
        print(json.dumps(map_to_surface(), indent=2))
    elif cmd == "status":
        print(json.dumps(status(), indent=2))
    else:
        print(json.dumps({"ok": False, "error": f"unknown cmd {cmd}"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
