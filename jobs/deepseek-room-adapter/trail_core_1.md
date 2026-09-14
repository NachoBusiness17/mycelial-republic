# trail_core_1 — deepseek-room-adapter

## Discovery (read-only)

Extension on disk: `%USERPROFILE%\.vscode\extensions\vizards.deepseek-v4-for-copilot-0.8.1` (Copilot `languageModelChatProviders` vendor=`deepseek`). `debugMode` default/live = `minimal`.

| Probe | Result |
|---|---|
| `globalStorage/vizards.deepseek-v4-for-copilot/` | **absent** — no extension globalStorage dir |
| `globalStorage/.../request-dumps` | **absent** — dumps only when `debugMode=verbose`; not written |
| `%TEMP%\deepseek-request-dumps` | **absent** |
| `User/globalStorage/storage.json` | no `deepseek` / `vizards` substring |
| `User/globalStorage/state.vscdb` | not parsed (no vizards dir; dumps/chat jsonl already answered the trail) |
| OutputChannel logs | **present** — `%APPDATA%\Code\logs\*\window*\exthost\Vizards.deepseek-v4-for-copilot\DeepSeek.log` (9 files). Sparse: activation + token usage lines. |
| Copilot `workspaceStorage/*/chatSessions/*.jsonl` | **present** — newest session `f12c9a62-….jsonl` has `selectedModel.metadata.vendor = deepseek` / `modelId = deepseek/deepseek-v4-flash`. This is Copilot Chat's store, not the extension's own files. It is the verbose chat trail. |

Honest: **the extension itself has no dump/session file trail at `debugMode=minimal`.** Chat lives in VS Code Copilot chatSessions. Token/activation log is DeepSeek.log. Tailer `--source auto` prefers dumps (if they appear later), else deepseek-tagged chatSessions, else DeepSeek.log.

No writes into VS Code state or the extension dir.

## Completed

- `watch/deepseek_room.py` on the `watch/codex_room.py` pattern: run-once, offset file `watch/.deepseek_room_state.json`, ISO-ts skip, 50-line first-run cap, fail-open, exit 0 always. Posts `seat=deepseek` to `watch/room.jsonl`, no thread.

## Artifacts

- `watch/deepseek_room.py`
- `watch/.deepseek_room_state.json` (offset; Mag watch dir, not VS Code)
- `jobs/deepseek-room-adapter/trail_core_1.md`

## Acceptance

First invoke (no prior offset; Mag venv):

```text
{"posted": 34, "session": "f12c9a62-386f-428d-a38b-b58f3bf5d91d.jsonl", "source": "chat-sessions"}
```

Git bash (offset already set; exact `echo EXIT:$?`):

```text
{"posted": 0, "session": "f12c9a62-386f-428d-a38b-b58f3bf5d91d.jsonl", "source": "chat-sessions"}
EXIT:0
```

Parse check:

```text
adapter parses
```

PowerShell `echo EXIT:$?` printed `EXIT:True` (PowerShell boolean, not bash). Bash `EXIT:0` is the contract's `$?`.

## Failures

- None for acceptance. Dumps source is empty until debugMode=verbose.

## Checkpoint

- completed: true
- artifacts: `watch/deepseek_room.py`, `watch/.deepseek_room_state.json`, `jobs/deepseek-room-adapter/trail_core_1.md`
- failures: none
- budget_used_pct: not tracked (no model calls)
- next_action_one_line: stop; this cage is done

## Handoff

- done: discovery filed; adapter bound; acceptance parse + exit 0; first-run posted 34 deepseek chatSession lines then 0 on replay
- untested: `request-dumps` path (folder does not exist yet); `--source vscode-log` live cadence
- blocked: false
- resume_command: `grok#2: read jobs/deepseek-room-adapter/seat_contract.json + latest trail_core, do next_action, run acceptance, write trail_core_N`
