# BLOB BRIDGE READY — 2026-09-01

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: blob_bridge.mjs bridges ollama model blobs into LM Studio as .gguf files via manifest layer parsing — SUPPORTED (usage/paths documented, decision line still says retest) · falsifier: cage-side retest finds no bridge output loadable in LM Studio, or manifest parse skips the model layer

`/root/.openclaw/workspace/blob_bridge.mjs` — ollama blob → GGUF bridge.

**What it does:** Reads each ollama manifest layer, finds the layer whose
`mediaType` contains `model` (the GGUF payload), and copies the matching
`blobs/sha256-<hex>` blob into LM Studio's models dir as `<model>.gguf`.

**Usage (Windows host, node only, zero deps):**
```
node blob_bridge.mjs --test          # fixture parse check (local sanity)
node blob_bridge.mjs llama3.2        # bridge one model
node blob_bridge.mjs meta/llama3.2   # namespace ignored, leaf name used
node blob_bridge.mjs --all           # bridge every manifest
```

**Paths (Windows):**
- IN  manifests: `C:/Users/foste/.ollama/models/manifests/registry.ollama.ai/library/<model>/latest`
- IN  blobs:     `C:/Users/foste/.ollama/models/blobs/sha256-<digest>`
- OUT models:    `C:/Users/foste/.lmstudio/models/bridged/<model>/<model>.gguf`

**Output:** per-bridge line (model, digest, bytes, dest) + a MAPPING table.
Missing manifest → error; no model layer → `SKIP`. Dirs auto-created.

Decision: retest — verify blob->GGUF bridge exists cage-side; fold pointer into MODEL_VAULT_MANIFEST, else archive (ZERO_BACKREF_TRIAGE_20260905)
