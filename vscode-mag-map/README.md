# MAG Framework Map — VS Code extension

A custom **framework-map pane** for `local_sovereign_agent`. A button in the VS Code
activity bar opens a searchable map of every command in the framework — CLI subcommands,
mag modules, tools, launchers, dashboard REST routes, and providers — and lets you run
them directly from a terminal, or open the backing source file.

## What it does

- **Activity-bar button** (magatama icon, "MAG Map") → opens the Framework Map pane.
- **Scans the real framework** (mirrors `tools/capability_manifest.py`) so it never goes
  stale: `main.py` subcommands, `mag/*.py` + `tools/*.py` modules (docstring purposes),
  root `.cmd` launchers, `dashboard/rest.py` REST routes, `configs/providers.yaml` providers.
- **Search + kind filter** — filter by name/help/file, or by kind (cli / mag / tool /
  launcher / route / provider), each with live counts.
- **Run or open** — click ▶ to run a command in a `MAG` terminal (uses `.venv` python,
  cd'd to the project root); click ⧉ to open the source file; double-click a card to run.

## How to run it

1. **F5 (Extension Development Host)** — the `.vscode/launch.json` config
   `"MAG Map (extension host)"` launches the extension against this workspace.
2. **Or** `F1` → `MAG: Open Framework Map` (also available in the command palette).
3. In the pane: type in the filter box, pick a kind from the dropdown, then **▶ run** /
   **⧉ open** / double-click to run.

## How the scan works

`extension.js` re-parses the live codebase at pane-open (and on the footer "⟳ rescan"
button) using the same regexes as `tools/capability_manifest.py`:

| Source | Regex |
|---|---|
| `main.py` | `add_parser("name", help="...")` |
| `mag/*.py`, `tools/*.py` | first docstring line |
| root `*.cmd` | `REM <purpose>` header |
| `dashboard/rest.py` | ROUTES table `("GET", "/api/...")` |
| `configs/providers.yaml` | `providers:` block names |

## Files

```
vscode-mag-map/
  package.json    # view container + commands + settings
  extension.js    # scanner + WebviewView provider + terminal runner
  media/
    mag.svg       # activity bar icon
    map.css       # pane styling (VS Code theme-aware)
    map.js        # webview client (search/filter/render/message)
```

## Notes

- Uses the project's `.venv\Scripts\python.exe` for `main.py` / `tools/*.py` runs.
- Pure surface — does NOT modify `mag/`, `main.py`, or any framework code.
- `node --check` is clean on both `extension.js` and `media/map.js`; the `vscode` module
  resolves inside the Extension Host (not under bare node).
