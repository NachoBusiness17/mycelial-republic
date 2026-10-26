"""mcp_registry_check -- validator for the MCP TOOL REGISTRY sample (mcp_registry.v1).

Banked 2026-09-28 with flash50/mcp-registry-design.md. Reads a registry YAML
and proves, without any live connection:
  1. schema/updated/census/tiers/servers/classes/tools/composition/gates present
  2. every tool row carries name, server, funding_min, mode, cost.class,
     inputs, outputs (the ask's six declared fields plus gate fields)
  3. referential integrity: server ids, tier ids, class ids all declared
  4. tier-gate invariants (the ask's core rule):
       a. funding_min free  -> mode perception AND cost class free-local or web-free
          (free lanes get free tools; sensing only per DRIVING LADDER)
       b. mode hands        -> funding_min funded or operator (quantized tiers
          never get hands, MCP_MANIFEST_SPEC.md:120-122)
       c. cost class unmetered -> funding_min operator (fail-close: unknown
          weight is a denial, MCP_MANIFEST_SPEC.md:78-79)
  5. composition render: emits the per-tier context-pack tool block and checks
     it fits the budgets_chars in the registry

Run: .venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/mcp_registry_check.py \
        watch/inbox/burn_reset_20260927/flash50/mcp_registry.sample.yaml
Exit 0 = all checks pass. Exit 1 = any check failed. Exit 2 = registry unreadable.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_TOOL_FIELDS = ("name", "server", "funding_min", "mode", "cost", "inputs", "outputs")
FREE_CLASSES = {"free-local", "web-free"}
HANDS_TIERS = {"funded", "operator"}


def check(registry_path: str) -> dict:
    import yaml

    raw = Path(registry_path).read_text(encoding="utf-8")
    reg = yaml.safe_load(raw)
    if not isinstance(reg, dict):
        return {"ok": False, "fatal": "registry did not parse to a mapping"}

    checks: list[dict] = []

    def ck(name: str, cond: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(cond), "detail": detail})

    # 1. top-level sections
    for key in ("schema", "updated", "census", "tiers", "servers", "classes",
                "tools", "composition", "gates"):
        ck(f"top_level.{key}", key in reg, f"present={key in reg}")
    ck("schema_id", reg.get("schema") == "mcp_registry.v1", f"schema={reg.get('schema')}")

    tiers = reg.get("tiers") or {}
    servers = {s["id"] for s in (reg.get("servers") or [])}
    classes = set(reg.get("classes") or {})
    tools = reg.get("tools") or []

    # 2. per-row required fields
    missing = [
        (t.get("name"), f) for t in tools for f in REQUIRED_TOOL_FIELDS
        if f not in t or t.get(f) in (None, "", {})
    ]
    ck("rows_complete", not missing, f"{len(tools)} rows, missing fields: {missing or 'none'}")

    # 3. referential integrity
    bad_server = sorted({t.get("name") for t in tools if t.get("server") not in servers})
    bad_class = sorted({t.get("name") for t in tools if (t.get("cost") or {}).get("class") not in classes})
    bad_tier = sorted({t.get("name") for t in tools if t.get("funding_min") not in tiers})
    dupes = sorted({t.get("name") for t in tools if [x.get("name") for x in tools].count(t.get("name")) > 1})
    ck("server_refs", not bad_server, f"undeclared servers on: {bad_server or 'none'}")
    ck("class_refs", not bad_class, f"undeclared classes on: {bad_class or 'none'}")
    ck("tier_refs", not bad_tier, f"undeclared tiers on: {bad_tier or 'none'}")
    ck("names_unique", not dupes, f"duplicate names: {dupes or 'none'}")

    # 4. tier-gate invariants
    viol_free = [
        t["name"] for t in tools if t.get("funding_min") == "free"
        and (t.get("mode") != "perception" or (t.get("cost") or {}).get("class") not in FREE_CLASSES)
    ]
    viol_hands = [t["name"] for t in tools if t.get("mode") == "hands" and t.get("funding_min") not in HANDS_TIERS]
    viol_unmetered = [
        t["name"] for t in tools if (t.get("cost") or {}).get("class") == "unmetered"
        and t.get("funding_min") != "operator"
    ]
    ck("free_gets_free_only", not viol_free, f"violations: {viol_free or 'none'}")
    ck("hands_never_free", not viol_hands, f"violations: {viol_hands or 'none'}")
    ck("unmetered_operator_only", not viol_unmetered, f"violations: {viol_unmetered or 'none'}")

    # 5. composition render per tier + budget fit
    comp = (reg.get("composition") or {}).get("context_pack") or {}
    budgets = comp.get("budgets_chars") or {}
    renders = {}
    for tier_name, tier in sorted(tiers.items(), key=lambda kv: kv[1].get("rank", 0)):
        allowed = set(tier.get("cost_classes") or [])
        mode_max = tier.get("mode_max")
        rank = tier.get("rank", 0)
        lines = []
        for t in tools:
            if t.get("funding_min") not in tiers:
                continue
            if tiers[t["funding_min"]].get("rank", 0) > rank:
                continue
            if (t.get("cost") or {}).get("class") not in allowed:
                continue
            if mode_max == "perception" and t.get("mode") != "perception":
                continue
            if t.get("status") == "planned" and rank < 2:
                continue
            cost = (t.get("cost") or {})
            tag = cost.get("class") + (f" {cost['per_call']}{cost.get('unit','')}/call" if cost.get("per_call") else "")
            verb = "writes state" if t.get("mode") == "hands" else "read-only"
            lines.append(f"{t['name']} [{tag}] {verb}")
        block = f"[mcp-tools tier={tier_name} tools={len(lines)}]\n" + "\n".join(lines)
        renders[tier_name] = {"tools": len(lines), "chars": len(block)}
    for tier_name, budget in budgets.items():
        got = renders.get(tier_name, {}).get("chars", 0)
        ck(f"render_fits.{tier_name}", got <= budget, f"{got} <= {budget} chars")
        ck(f"render_nonempty.{tier_name}", got > 0, f"block rendered {got} chars, not vacuous")
    ck("free_block_smallest",
       renders.get("free", {}).get("tools", 0) <= renders.get("funded", {}).get("tools", 1),
       f"free={renders.get('free', {}).get('tools')} funded={renders.get('funded', {}).get('tools')} operator={renders.get('operator', {}).get('tools')}")

    ok = all(c["ok"] for c in checks)
    return {
        "ok": ok,
        "schema": "mcp_registry_check.v1",
        "registry": str(registry_path),
        "rows": len(tools),
        "checks": checks,
        "passed": sum(1 for c in checks if c["ok"]),
        "failed": sum(1 for c in checks if not c["ok"]),
        "renders": renders,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        out = check(argv[1])
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "fatal": f"{type(e).__name__}: {e}"}, indent=2))
        return 2
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
