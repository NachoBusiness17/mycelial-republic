#!/usr/bin/env python3
"""seed_mcp.py - MCP server that serves the SEED-RIB (B2-181, 2026-09-26).

Any MCP-capable cold agent spawns this server and gets the kilobyte seed:
  resources: seed://current (the seed JSON), seed://law-registry (the live
             law registry bytes), seed://brief-pointers (sealed brief list)
  tools:     rebuild_subtree, verify_hash, fetch_bounded_pointer,
             join_protocol (how a cold agent boots into the fleet)

Format: seed_rib.v0 (B2-180, watch/inbox/SEED_RIB_FORMAT_v0_20260926.md),
built by tools/seed_rib.py. Laws carried over unchanged: the server never
invents pointer bytes. fetch_bounded_pointer serves live estate bytes only
after the sha256 seal matches, capped at --max-fetch, else it serves the
bounded record only and the pointer stays a named stub.

Default seed: watch/inbox/SEED_RIB_CURRENT (a JSON pointer doc) resolved via
seed_rib.resolve_current, so the MCP surface and the named-current seed cannot
split-brain (wave5 seed-kernel repair, 2026-09-29); --seed still overrides.

Transport: JSON-RPC 2.0 over stdio, same stdlib-only convention as
mag/mcp_server.py (the venv has no mcp package and that is the law).

Usage:
  .venv/Scripts/python.exe tools/seed_mcp.py                 # serve stdio
  .venv/Scripts/python.exe tools/seed_mcp.py --seed <path> --source .
  .venv/Scripts/python.exe tools/seed_mcp.py --list          # manifest
  .venv/Scripts/python.exe tools/seed_mcp.py --seed-sha      # seed seal
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

try:
    from tools.seed_rib import SCHEMA as SEED_SCHEMA, resolve_current
except ImportError:  # running as a plain script from tools/
    from seed_rib import SCHEMA as SEED_SCHEMA, resolve_current  # type: ignore

SCHEMA = "seed_mcp.v0"
JOIN_SCHEMA = "seed_join.v0"
BRIEF_SCHEMA = "seed_brief_pointers.v0"
PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "seed-rib", "version": "0.1.0"}
DEFAULT_FETCH_CAP = 262144
STUB_FMT = "seed_rib.v0 pointer sha256={sha} bytes={n}\n"


def is_void(rel: str) -> bool:
    return rel.startswith("/") or rel.startswith("\\") or ".." in rel.replace("\\", "/").split("/")


class SeedServer:
    def __init__(self, seed_path: Path, source_root: Path, fetch_cap: int = DEFAULT_FETCH_CAP):
        self.seed_path = seed_path
        self.source_root = source_root.resolve()
        self.fetch_cap = fetch_cap
        self._seed: dict | None = None

    def seed(self) -> dict:
        if self._seed is None:
            self._seed = json.loads(self.seed_path.read_text(encoding="utf-8"))
        return self._seed

    def seed_sha(self) -> str:
        return hashlib.sha256(self.seed_path.read_bytes()).hexdigest()

    def _entries(self) -> list[dict]:
        return self.seed().get("entries", [])

    def _entry(self, rel: str) -> dict | None:
        for e in self._entries():
            if e.get("path") == rel:
                return e
        return None

    # ----------------------------- resources -----------------------------

    def resources(self) -> list[dict]:
        n_laws = len(self.seed().get("law_refs", []))
        return [
            {"uri": "seed://current", "name": "seed",
             "description": f"The SEED-RIB ({SEED_SCHEMA}) JSON, {self.seed_path.stat().st_size} bytes, "
                            f"{len(self._entries())} entries, sha256 {self.seed_sha()[:16]}...",
             "mimeType": "application/json"},
            {"uri": "seed://law-registry", "name": "law-registry",
             "description": f"memory/law/registry.json live bytes ({n_laws} law ids)",
             "mimeType": "application/json"},
            {"uri": "seed://brief-pointers", "name": "brief-pointers",
             "description": "sealed bounded pointers to the fleet briefs",
             "mimeType": "application/json"},
        ]

    def read_resource(self, uri: str) -> str:
        if uri == "seed://current":
            return self.seed_path.read_text(encoding="utf-8")
        if uri == "seed://law-registry":
            return (self.source_root / "memory" / "law" / "registry.json").read_text(encoding="utf-8")
        if uri == "seed://brief-pointers":
            pointers = [{"path": e["path"], "sha256": e["sha256"], "bytes": e["bytes"],
                         "carrier": e.get("carrier")}
                        for e in self._entries() if e["path"].startswith("memory/briefs/")]
            return json.dumps({"schema": BRIEF_SCHEMA, "seed_sha256": self.seed_sha(),
                               "pointers": pointers}, indent=1)
        raise KeyError(f"unknown resource: {uri}")

    # ------------------------------- tools -------------------------------

    def tool_rebuild_subtree(self, into: str, source: str | None = None) -> dict:
        seed = self.seed()
        root = Path(into)
        ok = True
        inline_ok = inline_total = 0
        pointer_total = pointer_checked = pointer_unresolved = 0
        mismatches: list[str] = []
        stubs: list[str] = []
        for e in seed.get("entries", []):
            rel = e["path"]
            if is_void(rel):
                mismatches.append(f"VOID path refused: {rel}")
                ok = False
                continue
            target = root / rel
            if e.get("carrier") == "inline":
                raw = base64.b64decode(e.get("content_b64", ""))
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                inline_total += 1
                if hashlib.sha256(raw).hexdigest() == e["sha256"] and len(raw) == e["bytes"]:
                    inline_ok += 1
                else:
                    mismatches.append(rel)
                    ok = False
            else:
                pointer_total += 1
                src_base = Path(source).resolve() if source else self.source_root
                sp = src_base / rel
                if sp.is_file():
                    pointer_checked += 1
                    if hashlib.sha256(sp.read_bytes()).hexdigest() != e["sha256"]:
                        mismatches.append(f"pointer vs source: {rel}")
                        ok = False
                else:
                    pointer_unresolved += 1
                stub = root / (rel + ".SEED_POINTER")
                stub.parent.mkdir(parents=True, exist_ok=True)
                stub.write_text(STUB_FMT.format(sha=e["sha256"], n=e["bytes"]), encoding="utf-8")
                stubs.append(stub.name)
        return {"ok": ok, "rebuilt_root": str(root), "seed_sha256": self.seed_sha(),
                "inline_total": inline_total, "inline_ok": inline_ok,
                "mismatches": mismatches, "pointer_total": pointer_total,
                "pointer_source_checked": pointer_checked,
                "pointer_unresolved": pointer_unresolved, "stubs": stubs,
                "law_refs": len(seed.get("law_refs", []))}

    def tool_verify_hash(self, path: str, root: str | None = None) -> dict:
        if is_void(path):
            return {"ok": False, "error": f"void path refused: {path}"}
        base = Path(root).resolve() if root else self.source_root
        p = base / path
        if not p.is_file():
            return {"ok": False, "error": f"missing file: {path}"}
        raw = p.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        entry = self._entry(path)
        return {"ok": True, "path": path, "sha256": digest, "bytes": len(raw),
                "in_seed": entry is not None,
                "matches_seed": (digest == entry["sha256"]) if entry else None,
                "seal": entry["sha256"] if entry else None}

    def tool_fetch_bounded_pointer(self, path: str, max_bytes: int | None = None) -> dict:
        if is_void(path):
            return {"ok": False, "error": f"void path refused: {path}"}
        entry = self._entry(path)
        if entry is None:
            return {"ok": False, "error": f"path not in seed: {path}"}
        meta = {"ok": True, "path": path, "carrier": entry.get("carrier"),
                "role": entry.get("role"), "sha256": entry["sha256"], "bytes": entry["bytes"]}
        if entry.get("carrier") == "inline":
            meta.update({"served": False,
                         "how": "inline entry: read seed://current, bytes travel in the seed"})
            return meta
        sp = self.source_root / path
        cap = max_bytes or self.fetch_cap
        if not sp.is_file():
            meta.update({"served": False, "reason": "source absent; pointer stays a named stub "
                                                    "(.SEED_POINTER carries the seal)"})
            return meta
        raw = sp.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != entry["sha256"]:
            meta.update({"served": False, "reason": "SEAL MISMATCH vs source; bytes refused",
                         "source_sha256": digest})
            return meta
        if len(raw) > cap:
            meta.update({"served": False, "reason": f"exceeds fetch cap {cap} bytes"})
            return meta
        meta.update({"served": True, "bytes_b64": base64.b64encode(raw).decode("ascii")})
        return meta

    def tool_join_protocol(self) -> dict:
        seed = self.seed()
        inline_total = sum(1 for e in seed.get("entries", []) if e.get("carrier") == "inline")
        pointer_total = len(seed.get("entries", [])) - inline_total
        briefs = [e["path"] for e in seed.get("entries", [])
                  if e["path"].startswith("memory/briefs/")]
        return {
            "schema": JOIN_SCHEMA,
            "seed_path": str(self.seed_path),
            "seed_sha256": self.seed_sha(),
            "law_refs": seed.get("law_refs", []),
            "inline_total": inline_total,
            "pointer_total": pointer_total,
            "brief_pointers": briefs,
            "steps": [
                {"n": 1, "id": "read_seed", "do": "resources/read seed://current",
                 "check": f"json parses, schema == {SEED_SCHEMA}, entries > 0"},
                {"n": 2, "id": "obey_laws", "do": "resources/read seed://law-registry",
                 "check": "every law id in law_refs is read and obeyed before any effect"},
                {"n": 3, "id": "rebuild",
                 "do": "tools/call rebuild_subtree {into: <fresh empty dir>}",
                 "check": "ok true and inline_ok == inline_total and mismatches == []"},
                {"n": 4, "id": "spot_check",
                 "do": "tools/call verify_hash {path: <each rebuilt path>}",
                 "check": "matches_seed true for every rebuilt inline file"},
                {"n": 5, "id": "fetch_pointers",
                 "do": "tools/call fetch_bounded_pointer {path: <each pointer entry>}",
                 "check": "served bytes hash to the entry seal, else keep the named stub"},
                {"n": 6, "id": "briefs", "do": "resources/read seed://brief-pointers",
                 "check": "brief bytes hash to the brief pointer seal"},
                {"n": 7, "id": "announce",
                 "do": "leave a receipt naming seed_sha256 and the join outcome",
                 "check": "the fleet can audit the join from the receipt alone"},
            ],
        }


TOOL_SPECS = [
    {"name": "rebuild_subtree",
     "description": "Rebuild the seed's tree into a directory (inline bytes exact, "
                    "pointers as named .SEED_POINTER stubs; never invents pointer bytes)",
     "inputSchema": {"type": "object",
                     "properties": {"into": {"type": "string", "description": "target dir"},
                                    "source": {"type": "string", "description": "optional estate root "
                                                                                 "for pointer checks"}},
                     "required": ["into"]}},
    {"name": "verify_hash",
     "description": "sha256 real bytes at a path and compare against the seed seal",
     "inputSchema": {"type": "object",
                     "properties": {"path": {"type": "string"},
                                    "root": {"type": "string", "description": "optional root; "
                                                                              "default the estate"}},
                     "required": ["path"]}},
    {"name": "fetch_bounded_pointer",
     "description": "Fetch a seed pointer entry: bounded record always; live bytes only "
                    "when the source seal matches and the size fits the cap",
     "inputSchema": {"type": "object",
                     "properties": {"path": {"type": "string"},
                                    "max_bytes": {"type": "integer"}},
                     "required": ["path"]}},
    {"name": "join_protocol",
     "description": "The cold-agent join protocol: ordered steps that boot a fresh agent "
                    "into the fleet from the seed alone, each step with a check",
     "inputSchema": {"type": "object", "properties": {}}},
]

# --------------------------- MCP stdio protocol ---------------------------


def _rpc(id_: object, result: object) -> dict:
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def _err(id_: object, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def _content(value: object) -> dict:
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}]}


def handle(msg: dict, server: SeedServer) -> dict | None:
    method = msg.get("method")
    id_ = msg.get("id")
    params = msg.get("params") or {}
    if method == "initialize":
        return _rpc(id_, {"protocolVersion": PROTOCOL_VERSION,
                          "capabilities": {"tools": {}, "resources": {}},
                          "serverInfo": SERVER_INFO})
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return _rpc(id_, {})
    if method == "tools/list":
        return _rpc(id_, {"tools": TOOL_SPECS})
    if method == "tools/call":
        name = str(params.get("name") or "")
        args = params.get("arguments") or {}
        try:
            if name == "rebuild_subtree":
                return _rpc(id_, _content(server.tool_rebuild_subtree(
                    str(args["into"]), args.get("source"))))
            if name == "verify_hash":
                return _rpc(id_, _content(server.tool_verify_hash(
                    str(args["path"]), args.get("root"))))
            if name == "fetch_bounded_pointer":
                return _rpc(id_, _content(server.tool_fetch_bounded_pointer(
                    str(args["path"]), args.get("max_bytes"))))
            if name == "join_protocol":
                return _rpc(id_, _content(server.tool_join_protocol()))
            return _rpc(id_, {**_content({"ok": False, "error": f"unknown tool: {name}"}),
                              "isError": True})
        except Exception as exc:  # noqa: BLE001 - tool boundary reports, never crashes
            return _rpc(id_, {**_content({"ok": False,
                                          "error": f"{type(exc).__name__}: {exc}"}),
                              "isError": True})
    if method == "resources/list":
        return _rpc(id_, {"resources": server.resources()})
    if method == "resources/read":
        try:
            text = server.read_resource(str(params.get("uri") or ""))
        except (KeyError, OSError) as exc:
            return _rpc(id_, _err(id_, -32002, f"resource read failed: {exc}"))
        return _rpc(id_, {"contents": [{"uri": params.get("uri"), "mimeType":
                                        "application/json", "text": text}]})
    if id_ is not None:
        return _err(id_, -32601, f"method not found: {method}")
    return None


def serve(server: SeedServer) -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            resp = _err(None, -32700, "parse error")
        else:
            resp = handle(msg, server)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="seed-mcp", description="Serve the SEED-RIB over MCP stdio")
    ap.add_argument("--seed", default=None,
                    help="seed JSON path (default: resolve watch/inbox/SEED_RIB_CURRENT)")
    ap.add_argument("--source", default=".", help="estate root for pointer fetches")
    ap.add_argument("--max-fetch", type=int, default=DEFAULT_FETCH_CAP,
                    help="max bytes fetch_bounded_pointer may serve")
    ap.add_argument("--list", action="store_true", help="print resources + tools and exit")
    ap.add_argument("--seed-sha", action="store_true", help="print the seed sha256 and exit")
    args = ap.parse_args(argv)
    source_root = Path(args.source)
    seed_path = Path(args.seed) if args.seed else resolve_current(source_root.resolve())
    server = SeedServer(seed_path, source_root, args.max_fetch)
    if args.seed_sha:
        print(server.seed_sha())
        return 0
    if args.list:
        print(json.dumps({"schema": SCHEMA, "seed": str(seed_path),
                          "seed_sha256": server.seed_sha(),
                          "resources": server.resources(), "tools": TOOL_SPECS},
                         indent=2, ensure_ascii=False))
        return 0
    return serve(server)


if __name__ == "__main__":
    raise SystemExit(main())
