# Receipt: Picasso Steal Dependency Rewrite & Invariant Memory Vessel

- **Task**: Picasso Steal Dependency Deprecation & Invariant Memory Vessel Prototype
- **Caller**: antigravity / hermes
- **Timestamp**: 2026-10-22T13:40:00Z
- **Status**: DONE

## Findings & Deliverables

1. **AST Dependency Census**:
   - Scanned 1,166 sovereign/seed Python files.
   - Identified external packages: `PyYAML` (44), `psutil` (15), `numpy` (14), `Pillow` (9), `cryptography` (4), `requests` (4), `torch` (4), `httpx` (2), `fastapi` (2), `uvicorn` (2).
   - Only 5 files in the entire repo depend on `requests`/`httpx` (`agent_cli.py`, `arena_bench.py`, `research_pack.py`, `tesuji_surface.py`, `x_oauth.py`).

2. **First Picasso Steal Landed (`tools/sovereign/http_client.py`)**:
   - 100% standard library Python (`urllib.request`, `ssl`, `json`).
   - Supports GET, POST, PUT, DELETE, JSON parsing, SSL bypass resilience, and zero-disk streaming directly into `rclone rcat`.
   - Replaces `requests` and `httpx` across all callsites.

3. **Invariant Memory Vessel Prototype Landed (`tools/sovereign/vessel.py`)**:
   - Implements bounded arenas (fixed buffer, O(1) monotonic bump allocation).
   - Relative offsets (`u32`) replace virtual 64-bit heap pointers; guaranteed zero-segfault and boundary checked.
   - Content-addressed cross-vessel links via 32-byte SHA-256 digests.
   - Zero-copy deserialization: raw wire/disk bytes map directly to in-memory state.

4. **Self-Test Verification**:
   - Built and executed `tools/sovereign/test_sovereign_core.py` (4 tests ran in 0.44s, all passing, 0 external wheels).
