# U9 TASK — ractor-salon: REAL stdio MCP server (one file, dependency-free)

Write ONE complete Python file: `src/ractor_salon/mcp_server.py` for the `ractor-salon`
package (v0.1.0, Python >= 3.9, ZERO third-party dependencies — stdlib only).

It replaces a handshake-only stub. It is a REAL Model Context Protocol stdio server:
newline-delimited JSON-RPC 2.0 over stdin/stdout, implementing `initialize`,
`notifications/initialized`, `ping`, `tools/list`, `tools/call`, and proper JSON-RPC
error responses.

## Transport law

- Each stdin line = one JSON-RPC 2.0 message. Blank lines are skipped.
- Each response = exactly one line on stdout: `json.dumps(resp, ensure_ascii=False, default=str) + "\n"`, flushed immediately.
- Messages WITHOUT an `id` are notifications: never respond to them.
- A line that fails `json.loads` → one error response with `"id": null`, error code `-32700`, message `"parse error"`.
- Unknown/unsupported method WITH an id → error code `-32601`, message `f"method not found: {method}"`.

## Method contracts (exact)

1. `initialize` — params: `{"protocolVersion": "<client string>", "capabilities": {...}, "clientInfo": {...}}`.
   Result: `{"protocolVersion": <negotiated>, "capabilities": {"tools": {"listChanged": false}}, "serverInfo": {"name": "ractor-salon", "version": __version__}}`.
   Negotiation rule: let `SUPPORTED = {"2024-11-05", "2025-03-26", "2025-06-18"}` and `PROTOCOL_VERSION = "2024-11-05"`. If the client's `protocolVersion` is in SUPPORTED, echo it back; otherwise return `PROTOCOL_VERSION`.
2. `notifications/initialized` — notification, NO response.
3. `ping` — result `{}`.
4. `tools/list` — result `{"tools": [<the three descriptors below>]}`.
5. `tools/call` — params `{"name": str, "arguments": object}`.
   - OK result: `{"content": [{"type": "text", "text": <string>}], "isError": false}`.
   - Tool failure (exception or `ok: false` payload): NORMAL result with `isError: true`, text carries the error. Tool failures are NEVER JSON-RPC errors.
   - Unknown tool name: JSON-RPC error, code `-32602`, message includes the name.

## The three tools (exact names, descriptions, inputSchema)

```python
{
    "name": "salon_run",
    "description": (
        "Probe the model lanes live (a stored key is not a live key), fan ONE question "
        "across every live lane, and return the Rashomon fold — every lane's account "
        "side by side, failures preserved, never averaged. Appends to the append-only "
        "receipt tape and writes receipt.json + pack.md under salon_run/."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "minLength": 1,
                         "description": "the single question every live lane answers"},
            "lanes": {"type": "array", "items": {"type": "string"},
                      "description": "optional lane ids restricting the registry; "
                                     "unknown ids are reported back, never silently dropped"},
            "seeds": {"type": "integer", "minimum": 1,
                      "description": "optional cap on how many live lanes are seeded "
                                     "into the fan (registry order)"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}
```

`salon_run` behavior: filter `DEFAULT_LANES` by `lanes` (report unknown ids under
`"unknown_lanes"`); `env = merge_env(None)`; call
`salon.run([question], lanes=<filtered or None>, env=env, opener=<injected opener>, max_lanes=seeds)`
— the runner probes first, fans out, retries, writes the tape/receipt/pack, and returns
a summary dict that now carries `summary["probe"]` (the probe report) and `summary["fold"]`
(the pack markdown). Respond with a JSON object:
`{"ok": summary["ok"], "summary": summary, "fold": summary.get("fold", "")}` as the text
payload (`json.dumps(..., ensure_ascii=False, default=str)`); `isError` mirrors `not ok`.
After every run, remember `summary["probe"]` in a module-level `_LAST_PROBE` cache.

```python
{
    "name": "salon_lanes",
    "description": (
        "The lane registry — id, model, role, key env var, whether a key is present "
        "in the environment — plus the last live probe status from this server "
        "process, if any."
    ),
    "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
}
```

`salon_lanes` behavior: respond with JSON
`{"ok": True, "registry": [{"id","model","role","key_env","keyed"}...], "last_probe": <cached probe dict or None>, "note": "no live probe yet in this server process; salon_run probes first" when None}`.

```python
{
    "name": "salon_fold",
    "description": (
        "Re-fold an existing append-only tape (raw.jsonl) into the Rashomon pack: "
        "every account verbatim and side by side, failures preserved. Deterministic — "
        "the same tape always folds to the same markdown. Offline, no network."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {"tape_path": {"type": "string",
                                     "description": "path to a raw.jsonl tape written by salon_run or the CLI"}},
        "required": ["tape_path"],
        "additionalProperties": False,
    },
}
```

`salon_fold` behavior: `tape = receipts.Tape(tape_path)`; if the file does not exist →
`isError: true` text `f"tape not found: {tape_path}"`. Otherwise rows = tape.rows(),
fold = `fold_markdown(rows, title=f"FOLD — {Path(tape_path).name}", tape_digest=tape.digest())`,
text payload `{"ok": True, "tape": tape_path, "rows": len(rows), "digest": tape.digest(), "fold": fold}`.

## Host APIs you MUST reuse (do not reimplement any of this)

```python
from . import __version__
from .lanes import DEFAULT_LANES, Lane, merge_env        # Lane(id, base, model, key_env, role)
from . import receipts, salon
```

- `salon.run(questions: list, *, lanes: list[Lane] | None = None, env=None, out_dir="salon_run", mode="salon", workers=8, timeout=120, retries=1, opener=None, max_lanes=None) -> dict`
  — probes first (probe rows go on the tape), fans every question to every live lane,
  retries failures append-only, writes `raw.jsonl` / `receipt.json` / `pack.md`,
  returns summary with `ok`, `answered`, `failed`, `lanes_used`, `digest`, `raw`, `pack`,
  and (new in this pass) `probe` + `fold`.
- `receipts.Tape(path)` → `.rows()`, `.digest()`; `receipts.fold_markdown(rows, *, title, tape_digest="")` → markdown string.
- Keys live in the ENVIRONMENT only (`merge_env` = os.environ + optional files). NEVER read
  keys from mcp.json, never place a credential or Authorization header in any response.

## Server shape requirements

- `PROTOCOL_VERSION = "2024-11-05"`, `SUPPORTED` set as above.
- `def serve(stdin=None, stdout=None, opener=None) -> int` — defaults to `sys.stdin`/`sys.stdout`;
  `opener` is the injectable lane transport (a urllib-opener-like callable) that MUST be
  threaded into `salon.run(...)` so tests can run the whole server offline with a fake transport.
- Module-level `_LAST_PROBE: dict | None = None` cache updated by `salon_run`.
- `def main() -> int: return serve()` and `if __name__ == "__main__": raise SystemExit(main())`
  (the `ractor-salon-mcp` console script binds to `main`).
- Keep the module docstring style of the package (short, law-stating).
- `from __future__ import annotations` at top; Python 3.9-compatible runtime.
- Output ONLY the raw Python file content — no markdown fences, no commentary.
