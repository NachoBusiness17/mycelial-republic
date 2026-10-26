"""zmirror_mcp - MCP (JSON-RPC 2.0 over stdio, stdlib-only, same shape as mag/mcp_server.py)
exposing the ZCode mirror: list_sessions, get_snapshot, pull_since. Talks to the daemon over the tailnet.
Enable (NOT auto-registered): add to your MCP client config, e.g.
  "zcode-mirror": {"command": "python", "args": ["tools/zcode_mirror/zmirror_mcp.py"], "env": {"ZMIRROR_URL": "http://100.125.103.60:8790"}}"""
import json, os, sys, urllib.request
URL = os.environ.get("ZMIRROR_URL", "http://100.125.103.60:8790").rstrip("/")
def http(path, body=None):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode() if body is not None else None, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())
TOOLS = {
 "list_sessions": ({"type": "object", "properties": {}}, lambda a: http("/sessions"), "List mirrored ZCode sessions with head seq/hash."),
 "get_snapshot": ({"type": "object", "properties": {"sessionId": {"type": "string"}, "include_blob": {"type": "boolean"}}, "required": ["sessionId"]},
   lambda a: (lambda s: s if a.get("include_blob") else {k: v for k, v in s.items() if k != "blob"})(http("/snapshot/" + a["sessionId"])) | {"trajectory": http("/trajectory/" + a["sessionId"])},
   "Snapshot metadata (+compact trajectory digest) for a session."),
 "pull_since": ({"type": "object", "properties": {"sessionId": {"type": "string"}, "haveSeq": {"type": "integer"}, "haveHash": {"type": "string"}}, "required": ["sessionId", "haveSeq", "haveHash"]},
   lambda a: http("/sync", {"sessionId": a["sessionId"], "haveSeq": a["haveSeq"], "haveHash": a["haveHash"]}), "Chunks after haveSeq (<=256KB page) or RESET+snapshot on hash mismatch."),
}
def handle(m):
    meth, mid = m.get("method"), m.get("id")
    if meth == "initialize": res = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "zcode-mirror", "version": "0.1"}}
    elif meth == "tools/list": res = {"tools": [{"name": k, "description": v[2], "inputSchema": v[0]} for k, v in TOOLS.items()]}
    elif meth == "tools/call":
        p = m.get("params") or {}
        try: res = {"content": [{"type": "text", "text": json.dumps(TOOLS[p["name"]][1](p.get("arguments") or {}))}]}
        except Exception as e: res = {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True}
    elif mid is None: return None
    else: return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "method not found"}}
    return {"jsonrpc": "2.0", "id": mid, "result": res}
for line in sys.stdin:
    if not line.strip(): continue
    r = handle(json.loads(line))
    if r is not None: sys.stdout.write(json.dumps(r) + "\n"); sys.stdout.flush()
