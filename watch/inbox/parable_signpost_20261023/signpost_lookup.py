#!/usr/bin/env python3
"""signpost_lookup - resolve a parable pointer ID (e.g. pd1:L03) to its quanta.
Stdlib only. Two modes:
  python signpost_lookup.py pd1:L03 [pd1:L08 ...]      -> JSON to stdout
  python signpost_lookup.py --mcp                      -> minimal stdio JSON-RPC MCP stub
     tools: parable.resolve {ids:[...], verdict:"HOLD"}
Resolution only fires when verdict == HOLD (RIB delayed-read: beacon by default,
full scene only on HOLD). PASS/BLOCK return pointers only, no scene."""
import sys, json, os
D = os.path.dirname(os.path.abspath(__file__))
Q = json.load(open(os.path.join(D, "quanta.json"), encoding="utf-8"))["quanta"]

def resolve(ids, verdict="HOLD"):
    out = []
    for i in ids:
        q = Q.get(i)
        if q is None:
            out.append({"id": i, "error": "unknown pointer"}); continue
        if verdict != "HOLD":
            out.append({"id": i, "law": q["law"], "note": "verdict %s: pointer only, scene not loaded" % verdict}); continue
        out.append(q)
    return out

def mcp():
    tool = {"name": "parable.resolve", "description": "Resolve parable pointer IDs to verbatim quanta scenes (only on HOLD).",
            "inputSchema": {"type": "object", "properties": {"ids": {"type": "array", "items": {"type": "string"}},
                            "verdict": {"type": "string", "enum": ["PASS", "BLOCK", "HOLD"]}}, "required": ["ids"]}}
    for line in sys.stdin:
        if not line.strip(): continue
        m = json.loads(line); mid = m.get("id"); meth = m.get("method"); p = m.get("params") or {}
        if meth == "initialize": r = {"protocolVersion": "2025-06-18", "serverInfo": {"name": "parable-signpost", "version": "0.1"}, "capabilities": {"tools": {}}}
        elif meth == "tools/list": r = {"tools": [tool]}
        elif meth == "tools/call":
            a = p.get("arguments") or {}
            r = {"content": [{"type": "text", "text": json.dumps(resolve(a.get("ids", []), a.get("verdict", "HOLD")), ensure_ascii=False)}]}
        elif mid is None: continue
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "no method"}}), flush=True); continue
        print(json.dumps({"jsonrpc": "2.0", "id": mid, "result": r}, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    if sys.argv[1:2] == ["--mcp"]: mcp()
    else: print(json.dumps(resolve(sys.argv[1:]), indent=1, ensure_ascii=False))
