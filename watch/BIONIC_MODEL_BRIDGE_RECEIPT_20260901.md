# Bionic model bridge receipt — 2026-09-01

Status: PASS — host model inventory repaired and chat seat verified.

## Finding

Bionic is LM Studio rebranded (`Bionic 1.1.1+5`). Its configured model root is:

`C:\Users\foste\.lmstudio\models`

Its local server is bound to `127.0.0.1:1234`, with just-in-time loading enabled.
At the start of this run, that directory was empty and `lms ls` showed only the
bundled 84.11 MB Nomic embedding model. The Ollama store was healthy, but its
model payloads were content-addressed files named `sha256-<digest>` without a
`.gguf` suffix. LM Studio correctly rejected those names as non-model files.

## Repair

The existing Ollama payloads were copied, never moved or deleted, and imported
through the native `lms import --copy` path. Seven unique non-embedding models
are now present in Bionic's inventory:

| Ollama tag | Bionic model id | State |
|---|---|---|
| `deepseek-r1:1.5b` | `deepseek-r1-distill-qwen-1.5b` | present, not loaded |
| `gemma:2b` | `gemma-2b` | present, not loaded |
| `gemma4:latest` plus aliases | `gemma4-desk-latest` | present, not loaded |
| `qwen2.5:32b` | `qwen2.5-32b-instruct` | present, not loaded |
| `qwen2.5:3b-instruct` plus `qwen-desk:latest` | `qwen2.5-3b-instruct` | loaded and verified |
| `qwen2.5-coder:7b` | `qwen2.5-coder-7b-instruct` | loaded and verified |
| `qwen2.5vl:3b` | `qwen2.5-vl-3b-instruct` | present, not loaded |

The two Qwen 3B/7B seats are loaded simultaneously. Real local API probes
returned exactly `READY` and `CODER_READY` from the corresponding models on
`http://127.0.0.1:1234/v1/chat/completions`.

After the bridge completed, a second Coder probe returned `CODER_READY_2`.
Mag's `lm_studio status` reached the same endpoint and listed all eight visible
models, and the focused `tests/test_lm_studio.py` suite passed 3/3.

The 32B model is catalogued and visible but deliberately not loaded on this
host's 6 GB Vulkan GPU. Visibility is not being confused with loadability.

## Docker integration

Compose now supplies both `mag` and `worker` with:

`BIONIC_BASE_URL=http://host.docker.internal:1234/v1`

Both containers were recreated and became healthy. From inside the `mag`
container, Mag enumerated all eight Bionic-visible models and returned the
bounded completion `DOCKER_BIONIC_READY` through its local Bionic lane.

## Shared artifacts

- Bridge: `tools/ollama_to_lmstudio.mjs`
- Canonical registry: `watch/MODEL_REGISTRY.json`
- Source store: `C:\Users\foste\.ollama\models`
- Bionic store: `C:\Users\foste\.lmstudio\models`

The bridge is idempotent, groups duplicate Ollama aliases by payload digest,
keeps the Ollama store intact, uses the native importer, and refreshes the
registry with source paths, content digests, Bionic paths, API visibility, and
actual loaded-state evidence.

## Boundary retained

Bionic remains bound to loopback on the Windows host. Docker Desktop's
`host.docker.internal` path reaches it without widening the service to the LAN.
No firewall rule, public bind, credential, or external network exposure was
added.
