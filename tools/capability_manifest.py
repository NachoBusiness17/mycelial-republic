"""Capability manifest — the present-tense shape of the framework.

The local Ollama prompt-interpreter's "permanent memory kept in the present of
its capabilities, shape, and endpoints." Regenerated from code, not docs, so it
never goes stale: main.py subcommands, dashboard REST routes, mag modules,
and live provider/model inventory.

Output: memory/capability_manifest.md (the T0/T1 recall context).

Run:
  python tools/capability_manifest.py            # write the manifest
  python tools/capability_manifest.py --print    # print, don't write
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ROOT  # noqa: E402

OUT = ROOT / "memory" / "capability_manifest.md"


def _subcommands(main_py: Path) -> list[str]:
    """main.py argparse subcommand names."""
    if not main_py.is_file():
        return []
    out: list[str] = []
    for m in re.finditer(r'add_parser\(\s*"([a-z0-9_-]+)"', main_py.read_text(encoding="utf-8", errors="replace")):
        out.append(m.group(1))
    return sorted(set(out))


def _routes(rest_py: Path) -> list[str]:
    """dashboard REST routes from the ROUTES table."""
    if not rest_py.is_file():
        return []
    txt = rest_py.read_text(encoding="utf-8", errors="replace")
    out = re.findall(r'\(\s*"(GET|POST|PUT|DELETE)",\s*"(/[^"]+)"', txt)
    return [f"{m} {p}" for m, p in out]


def _modules(mag_dir: Path) -> list[str]:
    """mag/*.py module → one-line purpose (from the docstring header)."""
    if not mag_dir.is_dir():
        return []
    out: list[str] = []
    for p in sorted(mag_dir.glob("*.py")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'"""(.*?)(?:\n\s*""")', txt, re.S)
        head = (m.group(1).split("\n")[0].strip() if m else "").split(" — ")[0]
        out.append(f"{p.stem}: {head[:100]}")
    return out


def _providers() -> list[str]:
    try:
        from models.providers import list_provider_ids
        from models.registry import ollama_tags

        return [f"{pid} (ollama tags: {', '.join(ollama_tags()[:8])})" for pid in list_provider_ids()]
    except Exception as e:  # noqa: BLE001
        return [f"provider scan error: {e}"]


def build_manifest() -> str:
    main_py = ROOT / "main.py"
    rest_py = ROOT / "dashboard" / "rest.py"
    mag_dir = ROOT / "mag"
    lines = [
        "# Capability Manifest — present-tense framework shape (auto-generated)",
        f"- regenerated: {__import__('datetime').datetime.now().isoformat()}",
        f"- source: {main_py.name}, {rest_py.name}, mag/*, providers.yaml", "",
        "## CLI (main.py subcommands)",
        "`" + "` `".join(_subcommands(main_py)) + "`", "",
        "## REST endpoints (dashboard)",
        "`" + "` `".join(_routes(rest_py)) + "`", "",
        "## mag modules",
    ]
    for m in _modules(mag_dir):
        lines.append(f"- {m}")
    lines += ["", "## Providers / local models"]
    for p in _providers():
        lines.append(f"- {p}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="capability-manifest", description="Generate the present-tense framework manifest.")
    ap.add_argument("--print", action="store_true", help="print to stdout only")
    args = ap.parse_args(argv)
    text = build_manifest()
    if args.print:
        print(text)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"[manifest] {OUT} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
