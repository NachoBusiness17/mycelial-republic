"""Icon Drop — the human-doorway surface on the operator's Desktop.

When ghost hits an action it CANNOT automate (secret entry, extension reload,
lab restart, manual Vast launch, one-off operator decision), it must NOT nag
the operator in chat. It DROPS a clickable icon into the Desktop "Mag/Tools"
folder and the operator clicks it when ready.

This is the trained behavior (see memory/operator_directives law #8 "don't nag"):
  can't automate? -> drop an icon, one line, move on.

Surfaces:
  Desktop\Mag\Tools\<name>.cmd   — double-click launcher (operator clicks it)
  memory/icons/ledger.jsonl      — which icons are pending / clicked
  skill_ledger + training_events (operator_behavior) — folded case law

CLI:
  python -m mag.icon_drop ensure
  python -m mag.icon_drop list
  python -m mag.icon_drop drop NAME "COMMAND" --desc "what it does"
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parent.parent

ICON_FOLDER_NAME = "Mag"
ICON_SUBFOLDER = "Tools"
LEDGER = ROOT / "memory" / "icons" / "ledger.jsonl"
ROOT_CMD = ROOT / "mag_agent.ico"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def desktop_folder() -> Path:
    """Resolve the Desktop Mag/Tools folder (the icon-drop surface)."""
    import os
    try:
        import ctypes.wintypes
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0000, None, 0, buf)  # CSIDL_DESKTOPDIRECTORY
        desktop = Path(buf.value)
    except Exception:
        desktop = Path.home() / "Desktop"
    if not desktop.is_dir():
        desktop = Path.home()
    folder = desktop / ICON_FOLDER_NAME / ICON_SUBFOLDER
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _append_ledger(row: dict[str, Any]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def drop(name: str, command: str, *, desc: str = "", icon: str | None = None) -> dict[str, Any]:
    """Write a double-clickable .cmd launcher into Desktop\Mag\Tools.

    The operator clicks it deliberately — this is the HUMAN-doorway surface,
    so a visible console window on click is correct and intended.
    """
    safe = "".join(c for c in name if c.isalnum() or c in " _-")
    folder = desktop_folder()
    target = folder / f"{safe}.cmd"

    ico_line = ""
    if icon and Path(icon).is_file():
        ico_line = f'start "" /D "%CD%" /B >nul 2>&1\n'
    cmd_text = (
        "@echo off\r\n"
        "title Mag Action — {name}\r\n"
        "cd /d \"{root}\"\r\n"
        "{ico}"
        "echo.\r\n"
        "echo  M A G   A C T I O N\r\n"
        "echo  {name}\r\n"
        "{desc_line}"
        "echo.\r\n"
        "echo  Running: {command}\r\n"
        "echo.\r\n"
        "{command}\r\n"
        "echo.\r\n"
        "echo  Done. Window will close in 8s...\r\n"
        "timeout /t 8 /nobreak >nul\r\n"
    ).format(
        name=safe,
        root=ROOT,
        ico=ico_line,
        desc_line=(f"echo  {desc}\r\n" if desc else ""),
        command=command,
    )
    target.write_text(cmd_text, encoding="utf-8")

    row = {
        "schema": "icon_drop.v1",
        "ts": _now(),
        "name": safe,
        "path": str(target),
        "command": command[:300],
        "desc": desc,
        "status": "dropped",
    }
    _append_ledger(row)
    _fold_training(row)
    return row


def drop_shortcut(name: str, target_path: str, args: str = "", *, icon: str | None = None, desc: str = "") -> dict[str, Any]:
    """Create a real .lnk shortcut (for launching .cmd / .exe with an icon)."""
    import subprocess
    folder = desktop_folder()
    lnk = folder / f"{name}.lnk"
    ps = (
        "$s=(New-Object -ComObject WScript.Shell).CreateShortcut"
        f"('{lnk}');$s.TargetPath='{target_path}';"
        f"$s.Arguments='{args}';$s.WorkingDirectory='{ROOT}';"
        + (f"$s.IconLocation='{icon}';" if icon else "")
        + f"$s.Description='{desc}';$s.Save()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False,
                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0)
    row = {
        "schema": "icon_drop.lnk.v1",
        "ts": _now(),
        "name": name,
        "path": str(lnk),
        "target": target_path,
        "desc": desc,
        "status": "dropped",
    }
    _append_ledger(row)
    _fold_training(row)
    return row


def _fold_training(row: dict[str, Any]) -> None:
    """Surface the lesson: operator-only action -> icon dropped, not a chat nag."""
    try:
        from mag import skill_ledger, training_events
        skill_ledger.record_decision(
            goal="human-only action routing",
            task_shape="operator_action",
            provider="local",
            model="icon_drop",
            reasoning_level="none",
            source="icon_drop",
            outcome="ok",
            detail=f"dropped icon {row.get('name')} for operator click (no chat nag)",
        )
        training_events.emit(
            "operator_behavior",
            action={"kind": "icon_drop", "name": row.get("name")},
            outcome={"status": row.get("status"), "path": row.get("path")},
            pattern_tags=["desktop_icons", "donot_nag", "human_doorway"],
            tier_max="T1",
            exportable=False,
        )
    except Exception:
        pass


# Keyword -> (icon name, command, desc) for KNOWN operator-only actions that
# cannot be automated. When ghost hits one of these, it drops the icon and moves
# on (never nags in chat).
_KNOWN: dict[str, tuple[str, str, str]] = {
    "reload": ("Reload VS Code", "code --reuse-window .", "Reload/reopen the VS Code window (extension + agent reload)"),
    "restart lab": ("Lab Restart", "python -m mag.lifecycle restart_lab --port 8765", "Restart the dashboard lab on 8765"),
    "restart_lab": ("Lab Restart", "python -m mag.lifecycle restart_lab --port 8765", "Restart the dashboard lab on 8765"),
    "vast": ("Launch Vast Training", "python -m mag.vast_launcher launch_training", "Launch the Vast training run (needs VAST_API_KEY set)"),
    "secret": ("Set Secret (operator)", "notepad %USERPROFILE%\.env", "Set a secret/env value by hand (operator-only)"),
    "container": ("Mag Container", "launch_mag_container.cmd", "Bring up the Mag container (docker)"),
}


def auto(prompt: str) -> dict[str, Any]:
    """Route a human-only action to an icon drop. Returns the plan + dropped icon.

    If no known action matches, return a dry plan (no drop) so the caller can
    decide — we never guess-drop into the operator's Desktop folder.
    """
    t = (prompt or "").lower()
    for key, (name, cmd, desc) in _KNOWN.items():
        if key in t:
            row = drop(name, cmd, desc=desc, icon=str(ROOT_CMD) if ROOT_CMD.is_file() else None)
            return {"schema": "icon_drop.auto.v1", "ts": _now(), "ok": True,
                    "matched": key, "dropped": row}
    return {"schema": "icon_drop.auto.v1", "ts": _now(), "ok": True,
            "matched": None, "note": "no known human-only action matched; nothing dropped"}


def list_icons() -> list[dict[str, Any]]:
    folder = desktop_folder()
    icons = []
    for f in sorted(folder.glob("*.cmd")) + sorted(folder.glob("*.lnk")):
        icons.append({"name": f.stem, "path": str(f)})
    return icons


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="mag.icon_drop")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ensure = sub.add_parser("ensure")
    p_ensure.set_defaults(fn=lambda a: print(desktop_folder()))

    p_list = sub.add_parser("list")
    p_list.set_defaults(fn=lambda a: print(json.dumps(list_icons(), indent=2)))

    p_drop = sub.add_parser("drop")
    p_drop.add_argument("name")
    p_drop.add_argument("command")
    p_drop.add_argument("--desc", default="")
    p_drop.add_argument("--icon", default=None)
    p_drop.set_defaults(fn=lambda a: print(json.dumps(drop(a.name, a.command, desc=a.desc, icon=a.icon), indent=2)))

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
