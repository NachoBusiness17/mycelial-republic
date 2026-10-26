#!/usr/bin/env python3
"""install_into_cli - wire the starter kit seat pack into your coding-agent CLI.

Detects installed CLI agents (claude, codex, gemini, opencode, cursor) by
binary on PATH or their config dir, then wires the seat pack (the kit's
README, LAWS, BOOT and agent cards) into each found CLI's project config
convention:

  claude    ./CLAUDE.md        marked block with @path imports
  codex     ./AGENTS.md        marked block with read-order pointers
  opencode  ./AGENTS.md        same block (opencode reads AGENTS.md too)
  gemini    ./GEMINI.md        marked block with read-order pointers
  cursor    ./.cursor/rules/starter-kit.mdc   marked rule file, alwaysApply

Idempotent: every insertion sits between starter-kit begin/end markers and
a re-run that would produce identical bytes writes nothing. --dry prints
the actions without touching disk. --uninstall removes only marker-scoped
content. --cli NAME forces a single CLI. Stdlib only.

Run it from the directory the CLI opens in (usually your project root),
with the kit cloned somewhere inside that tree:

  python starter-kit/tools/install_into_cli.py            # wire all found
  python starter-kit/tools/install_into_cli.py --dry      # preview
  python starter-kit/tools/install_into_cli.py --cli claude
  python starter-kit/tools/install_into_cli.py --uninstall

No MCP config is written: this kit ships no MCP server, and registering a
server that does not exist would be fabrication.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# windows consoles default to a non-utf8 codepage; the report must not crash
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KIT_ROOT = Path(__file__).resolve().parents[1]

BEGIN = "<!-- starter-kit:seat-pack begin (kit-managed; edit outside the markers) -->"
END = "<!-- starter-kit:seat-pack end -->"

CURSOR_RULE_REL = Path(".cursor") / "rules" / "starter-kit.mdc"
CURSOR_RULE_HEADER = (
    "---\n"
    "description: Starter Kit method seat pack (laws, boot order, agent cards)\n"
    "alwaysApply: true\n"
    "---\n\n"
)

# the seat pack: what a seat loads, in order (docs first, then skill cards)
PACK_DOCS = ["README.md", "LAWS.md", "BOOT.md", "PROTOCOLS.md"]
PACK_CARDS = [
    "agent/conversation-miner.md",
    "agent/profile-grower.md",
    "agent/law-minter.md",
]

CLIS = {
    # name: (binaries to look for, config dir that also proves presence)
    "claude": (["claude"], ".claude"),
    "codex": (["codex"], ".codex"),
    "gemini": (["gemini"], ".gemini"),
    "opencode": (["opencode"], Path(".config") / "opencode"),
    "cursor": (["cursor", "cursor-agent"], ".cursor"),
}

# project config convention per CLI: relative path of the wired file and
# which renderer makes its block
CONVENTIONS = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
    "opencode": "AGENTS.md",
    "gemini": "GEMINI.md",
    "cursor": str(CURSOR_RULE_REL),
}


def detect_cli(name: str) -> str | None:
    """Return why the CLI counts as installed, or None if not found."""
    for binary in CLIS[name][0]:
        if shutil.which(binary):
            return f"binary '{binary}' on PATH"
    cfg = Path.home() / CLIS[name][1]
    if cfg.is_dir():
        return f"config dir {cfg}"
    return None


def pack_list(kit_rel: str) -> list[str]:
    return PACK_DOCS + PACK_CARDS


def render_block(cli: str, kit_rel: str) -> str:
    """The seat pack block, in the CLI's own convention."""
    files = pack_list(kit_rel)
    if cli == "claude":
        # CLAUDE.md supports @path imports (relative to this file)
        lines = ["# Starter Kit seat pack",
                 "",
                 "You are running with the Starter Kit method. Load, in order:",
                 ""]
        lines += [f"@{kit_rel}/{f}" for f in files]
        lines += ["",
                  f"Everything lives under {kit_rel}/; nothing else is imported."]
    else:
        lines = ["# Starter Kit seat pack",
                 "",
                 "You are running with the Starter Kit method. At session start,",
                 "read these files IN ORDER before acting:",
                 ""]
        lines += [f"{i}. {kit_rel}/{f}" for i, f in enumerate(files, 1)]
        lines += ["",
                  f"Everything lives under {kit_rel}/. Obey LAWS.md; the boot",
                  "order is README, then LAWS, then BOOT, then the agent cards."]
    return "\n".join(lines) + "\n"


def render_cursor_rule(kit_rel: str) -> str:
    """Cursor rule file: frontmatter + kit-marked body (the whole file is
    kit-owned, but it carries the markers so --uninstall recognizes it)."""
    body = render_block("codex", kit_rel)  # same markdown body, no imports
    return CURSOR_RULE_HEADER + BEGIN + "\n" + body + END + "\n"


def strip_block(text: str) -> tuple[str, bool]:
    """Remove marker-scoped content; return (new_text, had_markers)."""
    if BEGIN not in text:
        return text, False
    out, had, i = [], False, 0
    while True:
        b = text.find(BEGIN, i)
        if b == -1:
            out.append(text[i:])
            break
        out.append(text[i:b])
        e = text.find(END, b + len(BEGIN))
        if e == -1:
            # unterminated markers: strip to EOF, the block owns the tail
            out.append("")
            break
        out.append("")
        i = e + len(END)
        had = True
        # drop one leading newline pair left behind after the block
        while out and out[-1].endswith("\n\n"):
            out[-1] = out[-1][:-1]
    return "".join(out), had


def splice_block(text: str, block: str) -> str:
    """Replace existing marked content, or append a new marked block."""
    stripped, had = strip_block(text)
    body = BEGIN + "\n" + block + END + "\n"
    if had:
        return stripped.rstrip("\n") + "\n\n" + body if stripped.strip() else body
    return (stripped.rstrip("\n") + "\n\n" + body) if stripped.strip() else body


def relpath(target: Path) -> str:
    """Relative path from the target dir to the kit root, posix style."""
    import os
    return Path(os.path.relpath(KIT_ROOT, target)).as_posix()


def wire_file(path: Path, block: str, dry: bool) -> str:
    """Create/append/update a marked block in a markdown file. Returns verb."""
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="ignore")
        new = splice_block(text, block)
        if new == text:
            return "unchanged"
        if not dry:
            path.write_text(new, encoding="utf-8")
        return "updated"
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(BEGIN + "\n" + block + END + "\n", encoding="utf-8")
    return "created"


def unwire_file(path: Path, dry: bool, owns_file: bool = False) -> str:
    """Remove marker-scoped content; delete the file if nothing else remains.
    owns_file: the file itself is kit-named (cursor rule), so markers present
    means the whole file goes; a leftover empty rule shell would still be
    loaded by the CLI."""
    if not path.is_file():
        return "absent"
    text = path.read_text(encoding="utf-8", errors="ignore")
    new, had = strip_block(text)
    if not had:
        return "no-block"
    if owns_file:
        if not dry:
            path.unlink()
        return "removed"
    if new.strip():
        # trim only the trailing newlines our own splice added
        if not dry:
            path.write_text(new.rstrip("\n") + "\n", encoding="utf-8")
        return "stripped"
    if not dry:
        path.unlink()
    return "removed"


def wire_cli(cli: str, target: Path, dry: bool) -> tuple[str, str | None]:
    """Wire one CLI. Returns (status_line, error_or_none)."""
    why = detect_cli(cli)
    if why is None:
        return f"{cli}: not detected (skipped)", None
    conv = Path(CONVENTIONS[cli])
    path = target / conv
    kit_rel = relpath(target)
    if kit_rel.startswith(".."):
        note = (f"note: the kit sits outside {target}; some CLIs only read "
                f"files inside the project tree")
    else:
        note = None
    try:
        if cli == "cursor":
            content = render_cursor_rule(kit_rel)
            if path.is_file():
                old = path.read_text(encoding="utf-8", errors="ignore")
                if old == content:
                    verb = "unchanged"
                else:
                    verb = "updated"
                    if not dry:
                        path.write_text(content, encoding="utf-8")
            else:
                verb = "created"
                if not dry:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
        else:
            verb = wire_file(path, render_block(cli, kit_rel), dry)
    except OSError as e:
        return f"{cli}: ERROR {e}", str(e)
    tag = " [dry]" if dry else ""
    line = f"{cli}: {verb} {path}{tag}  (detected: {why})"
    if note:
        line += f"  {note}"
    return line, None


def unwire_cli(cli: str, target: Path, dry: bool) -> str:
    conv = Path(CONVENTIONS[cli])
    path = target / conv
    tag = " [dry]" if dry else ""
    try:
        verb = unwire_file(path, dry, owns_file=(cli == "cursor"))
    except OSError as e:
        return f"{cli}: ERROR {e}"
    return f"{cli}: {verb} {path}{tag}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="install_into_cli",
        description="Wire the starter kit seat pack into installed CLI agents.")
    ap.add_argument("--cli", choices=sorted(CLIS), default=None,
                    help="force one CLI instead of auto-detecting all")
    ap.add_argument("--dry", action="store_true",
                    help="print actions, write nothing")
    ap.add_argument("--uninstall", action="store_true",
                    help="remove kit-wired blocks (marker-scoped only)")
    ap.add_argument("--dir", default=".",
                    help="project directory to wire (default: current dir)")
    a = ap.parse_args(argv)
    target = Path(a.dir).resolve()
    if not target.is_dir():
        print(f"ERROR: --dir {target} is not a directory")
        return 1

    names = [a.cli] if a.cli else sorted(CLIS)
    results = []
    for name in names:
        if a.uninstall:
            results.append(unwire_cli(name, target, a.dry))
        else:
            line, _err = wire_cli(name, target, a.dry)
            results.append(line)

    print("STARTER KIT CLI INSTALLER"
          + (" (dry run)" if a.dry else "")
          + (" (uninstall)" if a.uninstall else ""))
    for r in results:
        print(f"  {r}")

    if a.uninstall:
        print("done. Kit-wired blocks removed; only marker-scoped content "
              "was touched.")
        return 0
    if a.cli:
        # forced single CLI: failing to detect is a failed ask
        if detect_cli(a.cli) is None:
            print(f"  {a.cli} is not installed on this box; nothing wired.")
            return 1
    else:
        detected = [n for n in names if detect_cli(n)]
        skipped = [n for n in names if n not in detected]
        if skipped:
            print(f"  not installed on this box, skipped: {', '.join(skipped)}")
        if not detected:
            print("  no supported CLI detected. Install one first (see "
                  "INSTALL.md step 0), then rerun.")
            return 1
    print("done. Open the project in your CLI and it now boots with the "
          "seat pack.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
