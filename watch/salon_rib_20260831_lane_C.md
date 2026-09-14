# Lane C – Build Program for RenderMan Compaction Lens

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: three $0 JSON patches (trajectory metadata injection, read_archive helper, append-only summary spine) plus a deterministic riddler sanitizer protocol are the smallest buildable compaction-lens steps — UNPROVEN (proposal only; no applied-patch receipts, and the file is truncated mid-spec) · falsifier: patches applied and their own validation assertions fail (entries missing metadata, spine rewritten instead of appended), or the sanitizer's regex strip corrupts public rows

## 1. Smallest Buildable Patches (3 × $0)

| # | Patch file | Target surface | Patch shape | $0 validation (free lane) |
|---|------------|----------------|------------|---------------------------|
| A | `/patches/add_metadata_to_traj.json` | `/board/openclaw_traj.jsonl` (compact‑after tape) | JSON‑patch that **replaces** the terminating `}` of each entry with `, "metadata": {"spanId":"<uuid>","byteRange":[<start>,<end>],"hash":"<sha256>","pathsTouched":["/mag/..."],"tokenCount":<int>} }`.  The patch uses a single‑line regex search for `"\}$"` and a replace that injects the metadata block. | Run a free Cerebras lane script (`python - <<'PY'
import json, pathlib, uuid, hashlib
p=pathlib.Path('board/openclaw_traj.jsonl')
for line in p.read_text().splitlines():
  e=json.loads(line)
  assert 'metadata' in e, f"missing on {e.get('id')}"
print('All entries contain metadata')
PY`)`. Success = no assertion.
| B | `/patches/implement_read_archive_convention.json` | New file `/mag/tools/read_archive.py` (added via ``"content"`` field) | Creates a tiny helper:
```python
import json, pathlib

def read_archive(span_id: str):
    idx = int(span_id.split('-')[-1])
    path = pathlib.Path('board/openclaw_traj.jsonl')
    for i,line in enumerate(path.read_text().splitlines()):
        if i==idx:
            return json.loads(line)
    raise KeyError('span not found')
```
Also adds a one‑line ``"search"/"replace"`` entry that injects a reference field `"archiveSpan":"<spanId>"` into each compaction item. | Free lane test: invoke the function on a known span (e.g. first line) and verify that the returned dict matches the original entry.
| C | `/patches/append_summary_spine.json` | New file `/mag/session_summary_spine.jsonl` (created via ``"content"``) | The patch adds an ``"on_compact"`` hook (via a tiny JSON specification) that **appends** a JSON line containing the new summary segment to the spine file rather than rewriting the existing summary. The hook is a pure‑data directive; the runtime reads it and performs the append.
| | | | Validation: run a free lane script that triggers two successive compactions (simulated by appending two dummy summary lines) and asserts that the spine file line count increased by 2. |

## 2. Riddler Shared Session Column – Minimal Protocol

* **Write side (seat)** – Each seat writes its private detailed transcript to a JSONL file under `/mag/memory/runs/riddler/private_<session>.jsonl`. A **sanitizer** (run on the same cage, no extra jobs) reads the private file, strips any fields matching the regex patterns `"geography":.*`, `"Heart":.*`, and any keys listed in `/board/PACK_PHYSICS.md` under *Sensitive*. The sanitized output is written to `/board/riddler_shared.jsonl` as a **public** JSONL pair.
* **Read side (seat & OpenClaw sessions)** – All agents read `/board/riddler_shared.jsonl` for the shared context. The file is append‑only; newer public entries are simply appended, preserving the order of sanitized history.
* **Sanitizer rule** – Deterministic, rule‑based removal; no AI‑based inference. It guarantees that the public column contains only **physics‑relevant** fields (`"entityId"`, `"position"`, `"velocity"`, `"action"`) and the deterministic metadata added by Patch A.
* **Filesystem bus** – Both the seat’s virtual environment and the OpenClaw cage share the same host filesystem; the public file lives under `/board`, which is writable by the cage, satisfying the “no new cages” constraint.
* **No Heart mining** – The sanitizer never reads or copies any `