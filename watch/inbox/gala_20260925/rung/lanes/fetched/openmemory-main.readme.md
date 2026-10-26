<p align="center">
  <img src="assets/openmemory-banner.png" alt="openmemory banner" width="100%" />
</p>

<h2 align="center" style="border-bottom: none;"><strong style="color:#5ce1b1;">Sync</strong> <strong style="color:#a587f5;">Your Sessions Across Any Coding Harness</strong></h2>

<img src="assets/starlight.svg" alt="" width="100%" />

<p align="center">
  <img src="assets/welcome-screen.png" alt="openmemory welcome screen" width="90%" />
</p>
<p align="center"><em>Beta: Claude Code, Codex, OpenCode available now. More coming soon.</em></p>

**Available via TUI Wizard or CLI**  
Effortlessly import and export sessions between harnesses.  
Pick up right where you left off, across all your coding harnesses.

<p align="center">
    <img src="assets/select-screen.png" alt="openmemory select screen" width="90%" />
</p>

## Why OpenMemory

It is the age of coding harnesses, and new harnesses are released every day. Developers feel locked in to their primary harness, unable to try new ones without losing all their context from previous sessions. OpenMemory brings that context to any harness so you can pick up where you left off.

- **Codex's "Import from Claude Code"** is uni-directional, supports only one source harness, and only does a bulk "import all conversations."
- **OpenCode's import is manual** — you point `opencode import` at a JSON file you've assembled by hand, with no discovery, preview, or way to pick which conversations come over.

OpenMemory is omni-directional, shows you a preview of the sessions on your machine, and lets you choose which to import so you know exactly what you're taking with you.

Switching between different harnesses? Autosync keeps them all in sync, all the time (coming soon).

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/mem0ai/openmemory/main/scripts/install.sh | bash
```

## Usage

Interactive wizard (recommended):
```bash
openmemory tui
```

## CLI
Should you wish to run openmemory as a cli instead of the wizard:
```bash
openmemory port --from <src> --to <dest> --all
```

`port` takes `--from`/`--to` plus either `--all` or one or more `--id <session-id>`; add `--force` to re-export and `--json` for machine-readable output.

## Roadmap

- [ ] Port `Skills`, `MCPs`, `Plugins`, and `CLAUDE.md` / `AGENTS.md`
- [ ] Realtime `autosync` of conversation sessions across harnesses
- [ ] Support for `OpenClaw`,  `Hermes`


## Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) to get started.

- 💡 **[Contributing Guide](CONTRIBUTING.md)**: Learn about our contribution process and coding standards.
- 🐛 **[Report an Issue](https://github.com/mem0ai/openmemory/issues)**: Found a bug? Let us know!