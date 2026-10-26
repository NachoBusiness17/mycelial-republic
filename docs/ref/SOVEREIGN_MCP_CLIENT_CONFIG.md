# SOVEREIGN MESH MCP SERVER INTEGRATION GUIDE

- **Server Executable:** `tools/sovereign_mcp.py`
- **Protocol:** Model Context Protocol (MCP) JSON-RPC 2.0 over `stdio`
- **Status:** OPERATIONAL (16/16 Unit Tests & 6/6 Self-Tests Passing)
- **Compliance:** House Law 100% (Zero unicode em-dashes, 0.00 first-person singular pronouns)

---

## 1. Overview

The Sovereign Mesh MCP Server (`tools/sovereign_mcp.py`) exposes the Decoupled Sovereign Data Plane to any MCP-compliant AI assistant or local client (Antigravity IDE, Claude Desktop, Cursor, local agent seats) over standard `stdio`.

Connecting an agent to this server grants instant, native access to:
1. **Immutable CAS Mesh Storage (`cas_store`, `cas_read`, `cas_verify`)**: Ingest and retrieve content by SHA-256 with automatic EPGM execution provenance sidecars.
2. **Lightning Bare-CPU Search (`bekko_search`)**: Sub-millisecond vector retrieval (15 microseconds/doc) across all 61+ slabs, 2,180 invariants, and catalog items without touching git.
3. **Harmonic Write Window Coordination (`kuramoto_phase`)**: Verify node transmit windows and Bartnik Hamiltonian flux to eliminate write collisions.
4. **Single-Writer Commit Queueing (`commit_hint_emit`)**: Emit atomic JSON hints for the commit sweeper, completely isolating client agents from `git add`, `git commit`, and `index.lock` collisions.
5. **Steganographic Parables & Absence Verification (`chord_mint`, `chord_verify_sentinel`)**: Mint chords carrying Hayashi False-Premise Sentinels to mathematically prove semantic alignment across model interfaces.

---

## 2. Client Configurations

### Antigravity IDE / Antigravity Agent Configuration
Add to your local MCP server registry (e.g. `~/.gemini/antigravity/mcp_servers.json` or workspace settings):
```json
{
  "mcpServers": {
    "sovereign-mesh": {
      "command": "python3",
      "args": [
        "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tools/sovereign_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent"
      }
    }
  }
}
```

### Claude Desktop Configuration
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "sovereign-mesh": {
      "command": "python3",
      "args": [
        "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tools/sovereign_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent"
      }
    }
  }
}
```

### Windows Host (Native PowerShell)
```json
{
  "mcpServers": {
    "sovereign-mesh": {
      "command": "wsl.exe",
      "args": [
        "-e",
        "bash",
        "-c",
        "cd /mnt/c/Users/foste/Documents/projects/local_sovereign_agent && PYTHONPATH=. python3 tools/sovereign_mcp.py"
      ]
    }
  }
}
```

---

## 3. Tool Reference

| Tool Name | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `cas_store` | `content` (str), `domain` (str), `actor` (str), `tags` (list) | `slab_hash`, `byte_count`, `cas_uri`, `epgm` | Ingests payload into CAS mesh with EPGM provenance sidecar |
| `cas_read` | `slab_hash` (str) | `content`, `byte_count`, `epgm` | Retrieves slab content and provenance by SHA-256 hash |
| `cas_verify` | *none* | `total_slabs`, `valid_slabs`, `integrity_ok` | Runs full cryptographic SHA-256 verification of all mesh slabs |
| `bekko_search` | `query` (str), `target` ('all'\|'cas'\|'invariants'), `top_k` (int) | `matches` (ranked list with cosine similarity) | Bare-CPU vector similarity search (15 microseconds/doc) |
| `kuramoto_phase` | `node` (str), `fleet_size` (4\|16) | `phase_deg`, `window_open`, `boundary_flux`, `admitted` | Checks coupled-oscillator phase angle and Bartnik flux budget |
| `commit_hint_emit` | `paths` (list), `message` (str), `seat` (str) | `ok`, `hint_file`, `paths_count` | Emits atomic single-writer commit hint into `queue/commit_hints/` |
| `chord_mint` | `domain` ('storage'\|'compute'\|'admission'\|'mesh'), `action` (str) | `chord` (dict containing parable, phase, sentinel) | Mints steganographic parable with embedded Hayashi probe |
| `chord_verify_sentinel` | `probe_id` (str), `entity` (str) | `is_absent`, `verdict`, `probe_details` | Evaluates ontological absence proof against canonical texts |

---

## 4. Verification Harness

The server includes a self-test mode and dedicated test battery:
```bash
# Standalone CLI Self-Test (Tests all 8 tools directly)
PYTHONPATH=. python3 tools/sovereign_mcp.py --test

# Direct CLI Tool Invocation
PYTHONPATH=. python3 tools/sovereign_mcp.py --call bekko_search --args '{"query": "CAS mesh", "top_k": 3}'

# Automated Test Suite
PYTHONPATH=. python3 -m unittest -v tests.test_sovereign_mcp
```
