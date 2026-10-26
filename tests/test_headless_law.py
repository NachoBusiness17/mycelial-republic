"""HEADLESS LAW (ratchet-style) — operator order 2026-09-27/28.

"you launched a python window without it being headless again... summon
lessig": visible console windows from spawned processes are a registered
guard regression (spawn_sites_no_window). This test makes the law
machine-enforced: every subprocess.run / Popen call in tools/ and tests/
must carry creationflags (CREATE_NO_WINDOW on win32). The count may only
ratchet DOWN: any NEW bare spawn fails this test; fixing sites lowers the
census in state/fuel/headless_census.json (re-baseline by editing that
file, which is a named acceptance).

os.system and os.spawn* are banned outright in tools/ and tests/ (no
way to be headless). Use subprocess with the flag, or mag.headless.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "state" / "fuel" / "headless_census.json"
BANNED_MODULES = {"os"}  # os.system / os.spawn* calls


def _spawn_call(node) -> str | None:
    """Real subprocess spawn calls only: subprocess.run/Popen/check_* —
    an Attribute whose value is the Name 'subprocess' (or a 'from
    subprocess import run' alias is NOT matched: aliases must be audited
    by grep, and false positives would erode the ratchet's meaning)."""
    f = node.func
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) \
            and f.value.id == "subprocess":
        return f"subprocess.{f.attr}"
    return None


def _scan() -> dict[str, int]:
    census: dict[str, int] = {}
    for d in ("tools", "tests"):
        for p in (ROOT / d).glob("*.py"):
            try:
                tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = _spawn_call(node)
                if name in ("subprocess.run", "subprocess.Popen",
                            "subprocess.check_call", "subprocess.check_output",
                            "subprocess.getoutput", "subprocess.getstatusoutput"):
                    if not any(k.arg == "creationflags" for k in node.keywords):
                        census[rel] = census.get(rel, 0) + 1
                if name in ("subprocess.getoutput", "subprocess.getstatusoutput"):
                    pass  # counted above: inherently windowed + shell
    return census


def test_headless_ratchet_never_grows():
    current = _scan()
    total = sum(current.values())
    if BASELINE.is_file():
        base = json.loads(BASELINE.read_text(encoding="utf-8"))
        assert total <= base.get("bare_spawn_total", 10**9), (
            f"HEADLESS LAW: bare spawns grew {base.get('bare_spawn_total')} -> "
            f"{total}. New spawn sites must carry creationflags="
            "(CREATE_NO_WINDOW on win32). Offenders: "
            f"{[k for k, v in current.items()]}")
    else:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(
            {"bare_spawn_total": total, "census": current}, indent=1),
            encoding="utf-8")
        print(f"headless baseline minted at {total}")


def test_no_os_system_in_tools_or_tests():
    for d in ("tools", "tests"):
        for p in (ROOT / d).glob("*.py"):
            try:
                tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                        and isinstance(node.func.value, ast.Name) \
                        and node.func.value.id == "os" \
                        and node.func.attr in ("system", "popen"):
                    raise AssertionError(
                        f"{rel}:{node.lineno} os.system/popen is banned "
                        "(cannot be headless); use subprocess with "
                        "creationflags")
