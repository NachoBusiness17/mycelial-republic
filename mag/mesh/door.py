"""mesh.door - the MCP door over the mesh (architecture v2, three tools + chain eye).

Salon verdict: the door is exactly search / get_by_hash / propose_write plus
verify_chain from day one; read tools stay lean (a read returning megabytes is a
competence negative); every response carries the freshness header
{corpus_tip_hash, last_growth_ts, frozen} so a caller always knows whether it is
reasoning over a live or frozen corpus (the cheapest anti-fabulation device).
The stdio JSON-RPC loop is the gps_mcp pattern (stdlib only, no SDK dependency).

Search honesty law: substring over the derived index; the recall floor is NAMED
in every response (unindexed content is invisible to search, and it says so).

Schema: mesh.door.v1 · stdio JSON-RPC {id, method: tools/list|tools/call, params}
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import mag.mesh.broker as broker
import mag.mesh.feeds as feeds
import mag.mesh.knot as knot

SCHEMA = "mesh.door.v1"
FREEZE_AFTER_DAYS = 30.0
TOOLS = [
    {"name": "search", "description": "substring search over the derived blob index; "
     "recall floor is named in every response",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}},
                     "required": ["query"]}},
    {"name": "get_by_hash", "description": "fetch one library blob by sha256",
     "inputSchema": {"type": "object", "properties": {"hash": {"type": "string"}},
                     "required": ["hash"]}},
    {"name": "propose_write", "description": "file a proposal (never commits; the broker "
     "adjudicates with provenance checks)",
     "inputSchema": {"type": "object",
                     "properties": {"writer": {"type": "string"}, "kind": {"type": "string"},
                                    "body": {"type": "object"},
                                    "source_hashes": {"type": "array"},
                                    "supersedes": {"type": "array"}},
                     "required": ["writer", "kind", "body"]}},
    {"name": "verify_chain", "description": "recompute knots, name unsealed leaves",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "tail_room", "description": "merged signed room view, last n rows",
     "inputSchema": {"type": "object", "properties": {"n": {"type": "integer"}}}},
]


def freshness(root: Path) -> dict:
    """{corpus_tip_hash, last_growth_ts, frozen}: the anti-fabulation header."""
    root = Path(root)
    v = knot.verify_chain(root)
    last = 0.0
    room = feeds.room_view(root, verify=False)["rows"]
    if room:
        try:
            last = max(float(r.get("ts", 0)) for r in room)
        except (TypeError, ValueError):
            last = 0.0
    blobdir = root / "library" / "blobs"
    if blobdir.is_dir():
        last = max([last] + [p.stat().st_mtime for p in blobdir.glob("*")])
    frozen = (time.time() - last) > FREEZE_AFTER_DAYS * 86400
    return {"corpus_tip_hash": v.get("tip"), "last_growth_ts": round(last, 3),
            "frozen": frozen, "unsealed_leaves": v.get("unsealed_leaves", 0),
            "schema": SCHEMA}


def call(root: Path, name: str, args: dict) -> dict:
    """In-process tool dispatch (tests call this; the stdio loop wraps it)."""
    root = Path(root)
    hdr = freshness(root)
    if name == "search":
        idx = root / "library" / "index.jsonl"
        rows = [json.loads(x) for x in idx.read_text().splitlines() if x.strip()] \
            if idx.exists() else broker.rebuild_index(root)["rows"]
        q = (args.get("query") or "").lower()
        hits = [r for r in rows if q in (r.get("note", "") + r["hash"]).lower()]
        return {"ok": True, "freshness": hdr, "hits": hits[:20],
                "recall_floor": f"substring over {len(rows)} indexed blobs; "
                                "unindexed content is invisible to this search"}
    if name == "get_by_hash":
        h = args.get("hash", "")
        f = root / "library" / "blobs" / h
        if not f.is_file():
            return {"ok": False, "error": f"blob {h[:12]} not found", "freshness": hdr}
        data = f.read_bytes()[:200_000]  # read-tool size bound (competence law)
        return {"ok": True, "hash": h, "bytes": f.stat().st_size, "data": data.decode(
            "utf-8", "replace"), "truncated": f.stat().st_size > 200_000, "freshness": hdr}
    if name == "propose_write":
        out = broker.propose(root, args.get("writer", "anon"), args.get("kind", "note"),
                             args.get("body", {}), args.get("source_hashes"),
                             args.get("supersedes"))
        return {**out, "freshness": hdr}
    if name == "verify_chain":
        return {**knot.verify_chain(root), "freshness": hdr}
    if name == "tail_room":
        n = int(args.get("n", 20))
        return {"ok": True, "freshness": hdr,
                "rows": feeds.room_view(root)["rows"][-n:]}
    return {"ok": False, "error": f"unknown tool {name}", "freshness": hdr}


def stdio_loop(root: Path) -> None:
    """gps_mcp-pattern stdlib JSON-RPC over stdin/stdout (no SDK dependency)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps({"id": None, "error": "bad json"}), flush=True)
            continue
        method, rid = req.get("method", ""), req.get("id")
        if method == "tools/list":
            out = {"id": rid, "result": {"tools": TOOLS}}
        elif method == "tools/call":
            p = req.get("params", {})
            out = {"id": rid, "result": call(root, p.get("name", ""), p.get("arguments", {}))}
        else:
            out = {"id": rid, "error": f"unknown method {method}"}
        print(json.dumps(out, default=str), flush=True)


if __name__ == "__main__":
    stdio_loop(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mesh_root"))
