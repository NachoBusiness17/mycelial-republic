# D20 — /bones Discord adapter (thin, Sep-20 critical path)

- **Lane:** D20 · wave_20260916 · 2026-09-16
- **Repo:** `C:\Users\foste\Documents\projects\local_sovereign_agent`
- **Interpreter:** `.venv\Scripts\python.exe` only (never bare `python` — Hermes venv on PATH)

## Mission

Wire the /bones Discord surface onto the kernel `mag/wow_bones_session.py` (BonesSession
class; receipts wow_session.v1 byte-stable). Slash commands: `/bones start` (seed
optional, world-boss flag), `/bones move <verb>`, `/bones status`, `/bones receipt`,
`/bones verbs` — each maps to the BonesSession API **in-process**.

## Laws acknowledged

1. **Adapter formats text ONLY — zero game logic.** Every game fact (legality, state,
   draws, verdict) comes from BonesSession / the kernel CLI's own output envelopes.
   The adapter builds the same JSON envelopes the kernel CLI emits and formats them.
2. **Token at runtime only.** Read from `%LOCALAPPDATA%\hermes\.env`, var
   `DISCORD_BOT_TOKEN` (verified present at line 530 by redacted grep — value never
   printed, never copied into any file). Adapter reads env at process start.
3. No git commands. No paid APIs. Write/Edit for source. Receipt appended as I go.

## Pinned surfaces

- Guild **NT-ACv2** `799817554549800982`, channel **#game-c-overview**
  `1050760558883913780` (constant block cites `watch/inbox/HERMES_DISCORD_SETUP_20260915.md`).
- discord 2.7.1 installed in repo venv (verified via `import discord; __version__`).

## Plan

1. [x] Survey kernel API + env var name + venv versions
2. [ ] `mag/bones_adapter.py` (slash group, channel gate, `--check` dry-run)
3. [ ] `tests/test_bones_adapter.py` (formatting + wiring, bot connect mocked, no network)
4. [ ] Run tests + `--check` verbatim below
5. [ ] Launch command + OPERATOR GATES

## Results

### Files

| File | Role |
|---|---|
| `mag/bones_adapter.py` | The thin /bones Discord adapter — formatting only; zero game logic (enforced by `test_adapter_source_contains_no_game_logic`) |
| `tests/test_bones_adapter.py` | 17 offline tests — formatting, wiring, channel gate, runtime token, `--check` dry-run; bot connect mocked (`discord.Client.run` raises if called) |
| `watch/inbox/wave_20260916/receipts/D20_BONES_ADAPTER.md` | This receipt |

### Design notes (the laws, made concrete)

- Every command builds the **same JSON envelope the kernel CLI emits**
  (`mag/wow_bones_session.main`: start/turn/status/receipt/verbs) from BonesSession
  return values, then formats it (fenced `key: value` block, canonical inline JSON for
  list items, 1900-char cap). The adapter decides nothing about legality, state,
  draws, or verdicts; it also reuses the kernel's own fixture gate (`_fixture_or_none`)
  and legality listing rather than re-implementing either.
- Sessions live only in the kernel store (`memory/runs/wow_bones/sessions`) via
  `BonesSession.save/load`; the adapter holds a per-channel pointer (id parsed from the
  kernel envelope text), plus an optional explicit `session` parameter on every command.
- Channel gate: all five subcommands answer **only** in
  <#1050760558883913780>; elsewhere → ephemeral pointer, kernel untouched.
- Guild-scoped sync to NT-ACv2 (`799817554549800982`) in `setup_hook`; nothing global.
- Token: `load_token()` reads `DISCORD_BOT_TOKEN` from
  `%LOCALAPPDATA%\hermes\.env` **at process start**, value goes only to
  `client.run()`; error paths name file + variable, never the value. `--check`
  never reads the token at all.

### Test results — verbatim

```
$ ./.venv/Scripts/python.exe -m pytest tests/test_bones_adapter.py -v
rootdir: C:\Users\foste\Documents\projects\local_sovereign_agent
configfile: pytest.ini
plugins: anyio-4.14.2, langsmith-0.10.14, timeout-2.4.0
collecting ... collected 17 items

tests/test_bones_adapter.py::test_fmt_any_scalars_nesting_and_lists PASSED [  5%]
tests/test_bones_adapter.py::test_fmt_block_fences_and_truncates PASSED [ 11%]
tests/test_bones_adapter.py::test_adapter_source_contains_no_game_logic PASSED [ 17%]
tests/test_bones_adapter.py::test_start_envelope_and_hub_pointer PASSED [ 23%]
tests/test_bones_adapter.py::test_start_world_boss_flag_reaches_kernel PASSED [ 29%]
tests/test_bones_adapter.py::test_wrong_channel_is_refused_ephemeral PASSED [ 35%]
tests/test_bones_adapter.py::test_move_legal_verb_promotes_and_persists PASSED [ 41%]
tests/test_bones_adapter.py::test_move_unknown_verb_formats_kernel_refusal PASSED [ 47%]
tests/test_bones_adapter.py::test_move_without_session_answers_no_session PASSED [ 52%]
tests/test_bones_adapter.py::test_move_explicit_session_overrides_hub PASSED [ 58%]
tests/test_bones_adapter.py::test_status_envelope PASSED                 [ 64%]
tests/test_bones_adapter.py::test_receipt_writes_kernel_file_and_shows_sha PASSED [ 70%]
tests/test_bones_adapter.py::test_verbs_lists_kernel_legality PASSED     [ 76%]
tests/test_bones_adapter.py::test_group_registers_five_guild_scoped_subcommands PASSED [ 82%]
tests/test_bones_adapter.py::test_load_token_reads_runtime_var PASSED    [ 88%]
tests/test_bones_adapter.py::test_load_token_missing_var_and_missing_file_never_leak PASSED [ 94%]
tests/test_bones_adapter.py::test_check_mode_lists_commands_and_never_connects PASSED [100%]

======================== 17 passed, 1 warning in 0.73s ========================
```

(1 warning = discord's own `audioop` deprecation notice under Python 3.13; not ours.
No network, no token, repo kernel store untouched — tests point the kernel's
session/receipt dirs at tmp_path.)

### `--check` dry-run — verbatim

```
$ ./.venv/Scripts/python.exe -m mag.bones_adapter --check
[bones-adapter] --check: dry-run (no token read, no connect)
[bones-adapter] guild 799817554549800982 (NT-ACv2), channel 1050760558883913780 (#game-c-overview)
  /bones start  [seed (opt), world_boss (opt)]  Start a bones session
  /bones move  [verb, session (opt)]  One bones turn: a verb through the referee
  /bones status  [session (opt)]  Bones session status
  /bones receipt  [session (opt)]  wow_session.v1 receipt for a bones session
  /bones verbs  [session (opt), limit (opt)]  Legal verbs for the session's current status
[bones-adapter] 5 subcommands registered; connect skipped (--check)
EXIT=0
```

### Exact launch commands

```text
:: dry-run (safe now, no token needed)
.venv\Scripts\python.exe -m mag.bones_adapter --check

:: live boot (ONLY after both OPERATOR GATES below clear)
.venv\Scripts\python.exe -m mag.bones_adapter
```

Live boot reads `DISCORD_BOT_TOKEN` from `%LOCALAPPDATA%\hermes\.env` at process
start, syncs the five subcommands to guild 799817554549800982, and answers only in
#game-c-overview (1050760558883913780).

## OPERATOR GATES

- [ ] **Token rotation pending** — the `DISCORD_BOT_TOKEN` currently in
  `%LOCALAPPDATA%\hermes\.env` predates the setup note; rotate before live boot.
- [ ] **#game-c-overview 403 permission click pending** — bot needs the channel
  permission grant in NT-ACv2 before it can respond in-channel.

The adapter does **not** go live until both gates clear. That is expected and correct.
