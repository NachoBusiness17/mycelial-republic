# KV slot cold store pilot (Mag Estate, lane A4)

Status: **UNBLOCKED, BINARY FOUND** (2026-10-05, lane B4): a vendored llama.cpp build
lives in-tree at `tools/llamacpp/` (`llama-server.exe`, `llama-bench.exe`, and siblings;
Vulkan AMD RX 5600 XT + CPU backends). `kv_slot_pilot.py` COMMON_PATHS now checks that
location first, so `find_llama_server()` resolves with zero install steps and the
`NOT_INSTALLED` exit 3 path is dead on this machine. The full 10-session replay remains
first-run-untested (section 10); the binary itself is verified live by the 2026-10-05
KV-type sweep, receipt `watch/inbox/build_wave_20261005/b4_kv_sweep.md`.

## 0. Current machine state (measured 2026-09-22)

| Check | Command | Result |
|---|---|---|
| PATH lookup | `where.exe llama-server` | `INFO: Could not find files for the given pattern(s).` exit 1 |
| Sibling binaries | `where.exe llama-cli llama-quantize` | both not found |
| Common paths | `Program Files\llama.cpp`, `C:\llama.cpp`, `%LOCALAPPDATA%\llama.cpp`, `%USERPROFILE%\llama.cpp`, `%USERPROFILE%\scoop\apps\llama.cpp`, `%USERPROFILE%\.cargo\bin`, `C:\tools\llama.cpp` | none exist |
| Vendored in-tree (2026-10-05, lane B4) | `tools\llamacpp\llama-server.exe` | EXISTS, with `llama-bench.exe` and siblings; now first entry in COMMON_PATHS |
| Ollama (present) | `where.exe ollama` | `C:\Users\foste\AppData\Local\Programs\Ollama\ollama.exe` |
| Winget package | `winget search --id ggml.llamacpp -e` | `llama.cpp  ggml.llamacpp  b11057  winget` |

## 1. Goal

Stop re-prefilling the same long session prefixes. llama.cpp's KV-slot cache saves the
KV cache of a prompt to disk and restores it when the same prefix comes back, turning a
multi-second prefill into a file read. Pilot: persist KV slots for the 10 longest stored
sessions and measure cold vs warm prefill.

## 2. Model source: existing .ollama blobs  -  NO re-download

Ollama stores each model as a plain GGUF blob under `C:\Users\foste\.ollama\models\blobs\`
(49 `sha256-*` files measured on this machine). The manifest maps a model tag to its GGUF
layer; llama-server can load that file directly with `-m`:

- Manifest: `C:\Users\foste\.ollama\models\manifests\registry.ollama.ai\library\qwen2.5\7b`
  → model layer `sha256:2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730`
  (4,683,073,952 bytes) → blob file
  `C:\Users\foste\.ollama\models\blobs\sha256-2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730`
- Manifest: `...\library\gemma4\latest` → model layer
  `sha256:4c27e0f5b5adf02ac956c7322bd2ee7636fe3f45a8512c9aba5385242cb6e09a`
  (9,608,338,848 bytes).

Caveat: Ollama keeps the chat template in a separate manifest layer, so llama-server does
not inherit it from `-m`. The pilot uses raw `/completion` prompts (no chat template), so
this is harmless for KV measurement; production use of these blobs through llama-server
must pass `--chat-template` explicitly.

## 3. Dedicated KV directory

Slots go to `C:\Users\foste\.llama-kv-slots\` (created on first run, nothing else writes
there) via `--slot-save-path`. The session store it replays from is
`memory/agent_sessions/*.json` (77 MB, shape `{"session_id","provider","model",
"messages":[{"role","content"},...],"last_answer","updated"}`).

## 4. Server launch line

```
llama-server -m <blob> --host 127.0.0.1 --port 8081 \
  --slot-save-path C:\Users\foste\.llama-kv-slots \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --flash-attn on \
  -c 32768 --parallel 1
```

- **q8_0 KV quant**: `--cache-type-k q8_0 --cache-type-v q8_0` halves KV memory vs f16.
  V-cache quantization requires flash attention; launch fallbacks in the script:
  (1) `--flash-attn on` (newer builds) → (2) `--flash-attn` (boolean, older) → (3) drop
  `-fa`/`-ctv` and keep K-only q8_0, logging the degradation.
- Slot save/restore API: `POST /slots/0?action=save&filename=<name>.bin` and
  `POST /slots/0?action=restore&filename=<name>.bin` (only honored when
  `--slot-save-path` is set).

## 5. Slot naming: `<model-digest>-<prompt-hash>.bin`

- `<model-digest>` = first 16 hex chars of the GGUF blob sha256 (full digest kept in the
  pilot's stdout log; truncation avoids Windows MAX_PATH issues).
- `<prompt-hash>` = first 16 hex chars of `sha256(first user message text)`.
- Example: `2bada8a745067700-9f2c1ab77e01d433.bin`.

## 6. Restore on prefix match

For a session whose first user message hashes to an existing slot file:
1. `POST /slots/0?action=restore&filename=<slot>`  -  server loads the saved KV cache;
2. send the identical prompt to `/completion`  -  the server binds the restored cache onto
   the shared prefix, so prefill only covers tokens past the match.
Cold sessions: run `/completion` first (measures cold prefill), then save the slot.

## 7. Replay protocol  -  the 10 longest sessions

1. Scan `memory/agent_sessions/*.json`; score = total characters across
   `messages[*].content`; keep top 10 with a non-empty user message
   (largest today: `orc-t31873a68f8.json`, 1,714,939 bytes).
2. Pass 1 (cold): prompt → record `timings.prompt_ms` → `save` slot.
3. Pass 2 (warm): `restore` slot → same prompt → record `timings.prompt_ms`.
4. Success per session: slot file exists on disk AND warm `prompt_ms` < cold `prompt_ms`.
5. Pilot success: ≥ 8/10 sessions show a speedup and slots materialize in the KV dir.

## 8. Install step (exact, verified in winget b11057)

```
winget install --id ggml.llamacpp -e --source winget
```

Then re-run:

```
C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe ^
  C:\Users\foste\Documents\projects\local_sovereign_agent\tools\kv_slot_pilot.py
```

Exit codes: `0` = pilot ran (summary printed); `3` = `NOT_INSTALLED` (staged); `1` = error.

## 9. Safety

The script is a loopback-only test client: every URL it builds must be http/https and must
point at the `127.0.0.1` llama-server process it spawned itself; it never fetches an
operator- or session-supplied URL, and it downloads nothing (blobs are reused in place).

## 10. Honest limits

The replay code path (slot save/restore over the 10 longest sessions) has not executed
end-to-end yet: the 2026-10-05 sweep exercised `llama-server` and `llama-bench` from the
same vendored directory but not the slot replay itself. Known limit to cure before the
full run: the longest stored sessions (section 7) exceed the pilot's fixed `-c 32768`
context, so the full replay will need either a bigger context or a prompt-size filter.
Flag spellings (`--flash-attn on` vs boolean) are guarded by launch fallbacks; the sweep
used `-fa on` successfully on this Vulkan build.
