#!/usr/bin/env python3
"""tools/sovereign_mcp.py - Sovereign Mesh Model Context Protocol (MCP) Server.

Exposes the Decoupled Sovereign Data Plane to any MCP-compliant client
(Antigravity IDE, Claude Desktop, Cursor, local agent seats) over standard
JSON-RPC 2.0 on stdio.

Tools Exposed:
  1. cas_store            - Ingest content into CAS mesh with atomic EPGM sidecars
  2. cas_read             - Retrieve content and provenance by SHA-256 hash
  3. cas_verify           - Run full integrity verification across all mesh slabs
  4. bekko_search         - Bare-CPU semantic vector search (15 microseconds/doc)
  5. kuramoto_phase       - Query node transmission phase window and Bartnik flux
  6. commit_hint_emit     - Deposit atomic single-writer commit hint (bypassing git)
  7. chord_mint           - Mint steganographic chord carrying Hayashi sentinels
  8. chord_verify_sentinel- Verify an entity absence proof against canon

House Law:
  - Strictly 0.00 first-person singular pronouns.
  - Strictly zero unicode em-dashes (-- and - only).
  - Pure Python standard library (zero external dependencies).
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.cas_mesh import CasMesh
from tools.bekko_cpu_retriever import StaticCPURetriever
from tools.kuramoto_chute import KuramotoChute
from tools.chord_minter import ChordMinter, load_false_premise_probes

BANNED_PRONOUNS_RE = re.compile(r"\b(I|me|my|mine|myself)\b", re.IGNORECASE)

TOOL_DEFINITIONS = [
    {
        "name": "cas_store",
        "description": "Store content immutably in the Content-Addressable Storage (CAS) mesh with atomic EPGM provenance sidecar. Zero locks, zero git contention.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Text or code payload to store"},
                "domain": {"type": "string", "description": "Domain tag (e.g. research, architecture, spec, governance)", "default": "general"},
                "actor": {"type": "string", "description": "Actor or seat identifier depositing the slab", "default": "local-mcp"},
                "parent_hash": {"type": "string", "description": "Optional parent slab SHA-256 hash for causal lineage", "default": None},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Optional metadata tags", "default": []}
            },
            "required": ["content"]
        }
    },
    {
        "name": "cas_read",
        "description": "Retrieve content and EPGM execution provenance sidecar from the CAS mesh by SHA-256 hash with hash integrity verification.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slab_hash": {"type": "string", "description": "64-character hex SHA-256 slab hash"}
            },
            "required": ["slab_hash"]
        }
    },
    {
        "name": "cas_verify",
        "description": "Verify hash integrity across all stored slabs and EPGM provenance sidecars in the CAS mesh.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "bekko_search",
        "description": "Execute bare-CPU semantic vector search across CAS slabs, invariants, and catalog (15 microseconds/doc, zero GPU, zero git grep disk sleep).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural language or technical search query"},
                "target": {"type": "string", "enum": ["all", "cas", "invariants", "catalog"], "description": "Target corpus partition", "default": "all"},
                "top_k": {"type": "integer", "description": "Maximum number of ranked results to return", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "kuramoto_phase",
        "description": "Check current Kuramoto coupled-oscillator phase angle, active transmit seat, window eligibility, and Bartnik boundary Hamiltonian flux.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node": {"type": "string", "description": "Node or seat identifier to check (desktop, bob, pixel, antigravity, seat_00..seat_15)", "default": "antigravity"},
                "fleet_size": {"type": "integer", "enum": [4, 16], "description": "Cluster topology size (4 or 16)", "default": 16}
            }
        }
    },
    {
        "name": "commit_hint_emit",
        "description": "Emit an atomic single-writer commit hint into queue/commit_hints/. Workers never touch git; the commit sweeper serializes commits safely.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "paths": {"type": "array", "items": {"type": "string"}, "description": "Relative file paths staged in this hint"},
                "message": {"type": "string", "description": "Commit message adhering to House Law"},
                "seat": {"type": "string", "description": "Author seat identifier", "default": "local-mcp"}
            },
            "required": ["paths", "message"]
        }
    },
    {
        "name": "chord_mint",
        "description": "Mint an operational steganographic chord carrying an allegorical parable and an embedded Hayashi False-Premise Sentinel probe.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "enum": ["storage", "compute", "admission", "mesh"], "description": "Operational domain"},
                "action": {"type": "string", "description": "Target action verb (e.g. store, retrieve, balance, gate)"}
            },
            "required": ["domain", "action"]
        }
    },
    {
        "name": "chord_verify_sentinel",
        "description": "Verify an entity absence proof against canon to detect semantic hallucination or codebook discordance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "probe_id": {"type": "string", "description": "False premise probe ID (e.g. FP01, FP_ORCH_01)"},
                "entity": {"type": "string", "description": "Entity name to verify absence of"}
            },
            "required": ["probe_id", "entity"]
        }
    }
]


# Singleton engines (initialized lazily)
_CAS_MESH: Optional[CasMesh] = None
_BEKKO_RETRIEVER: Optional[StaticCPURetriever] = None
_KURAMOTO_CHUTE: Optional[KuramotoChute] = None
_CHORD_MINTER: Optional[ChordMinter] = None


def get_cas_mesh() -> CasMesh:
    global _CAS_MESH
    if _CAS_MESH is None:
        _CAS_MESH = CasMesh(ROOT / "memory" / "cas")
    return _CAS_MESH


def get_bekko_retriever() -> StaticCPURetriever:
    global _BEKKO_RETRIEVER
    if _BEKKO_RETRIEVER is None:
        _BEKKO_RETRIEVER = StaticCPURetriever()
        _BEKKO_RETRIEVER.build_from_cas(ROOT)
        _BEKKO_RETRIEVER.build_from_invariants()
    return _BEKKO_RETRIEVER


def get_kuramoto_chute() -> KuramotoChute:
    global _KURAMOTO_CHUTE
    if _KURAMOTO_CHUTE is None:
        _KURAMOTO_CHUTE = KuramotoChute()
    return _KURAMOTO_CHUTE


def get_chord_minter() -> ChordMinter:
    global _CHORD_MINTER
    if _CHORD_MINTER is None:
        _CHORD_MINTER = ChordMinter()
    return _CHORD_MINTER


def tool_cas_store(args: Dict[str, Any]) -> Dict[str, Any]:
    content = args.get("content", "")
    domain = args.get("domain", "general")
    actor = args.get("actor", "local-mcp")
    parent_hash = args.get("parent_hash")
    tags = args.get("tags") or []

    if "\u2014" in content:
        raise ValueError("Content violates House Law: contains unicode em-dash")

    mesh = get_cas_mesh()
    raw_bytes = content.encode("utf-8")
    epgm_record = mesh.put_slab(
        content=raw_bytes,
        actor_seat=actor,
        causal_parent=parent_hash,
        labels=tags,
        extra={"domain": domain},
    )
    slab_hash = epgm_record["content_hash"]
    byte_count = epgm_record["byte_size"]
    return {
        "ok": True,
        "slab_hash": slab_hash,
        "byte_count": byte_count,
        "domain": domain,
        "actor": actor,
        "parent_hash": parent_hash,
        "cas_uri": f"cas:{slab_hash[:8]}",
        "epgm": epgm_record,
    }


def tool_cas_read(args: Dict[str, Any]) -> Dict[str, Any]:
    slab_hash = args.get("slab_hash", "").strip()
    if not slab_hash:
        return {"error": "slab_hash is required", "isError": True}

    mesh = get_cas_mesh()
    try:
        raw_bytes, sidecar = mesh.get_slab(slab_hash)
    except (FileNotFoundError, ValueError) as err:
        return {"error": str(err), "isError": True}

    return {
        "ok": True,
        "slab_hash": slab_hash,
        "byte_count": len(raw_bytes),
        "content": raw_bytes.decode("utf-8", errors="replace"),
        "epgm": sidecar,
    }


def tool_cas_verify(args: Dict[str, Any]) -> Dict[str, Any]:
    mesh = get_cas_mesh()
    return mesh.verify_mesh()


def tool_bekko_search(args: Dict[str, Any]) -> Dict[str, Any]:
    query = args.get("query", "").strip()
    target = args.get("target", "all")
    top_k = int(args.get("top_k", 5))

    retriever = get_bekko_retriever()
    raw_results = retriever.search(query, top_k=top_k * 2 if target != "all" else top_k)
    if target == "cas":
        results = [r for r in raw_results if r.get("metadata", {}).get("type") == "cas_slab"][:top_k]
    elif target == "invariants":
        results = [r for r in raw_results if r.get("metadata", {}).get("type") == "invariant"][:top_k]
    else:
        results = raw_results[:top_k]

    return {
        "ok": True,
        "query": query,
        "target": target,
        "total_corpus_vectors": len(retriever.vectors),
        "matches_count": len(results),
        "matches": results,
    }


def tool_kuramoto_phase(args: Dict[str, Any]) -> Dict[str, Any]:
    node = args.get("node", "antigravity")
    fleet_size = int(args.get("fleet_size", 16))

    chute = get_kuramoto_chute()
    theta = chute.current_system_phase()
    win_info = chute.check_phase_window(node, fleet_size=fleet_size)
    admission = chute.admit_mutation(node, "mcp_phase_query", 0)

    from tools.kuramoto_chute import NODE_16_PHASE_OFFSETS, NODE_PHASE_OFFSETS, PHASE_16_HALF_WINDOW_RAD, PHASE_HALF_WINDOW_RAD
    offsets = NODE_16_PHASE_OFFSETS if fleet_size == 16 else NODE_PHASE_OFFSETS
    half_win = PHASE_16_HALF_WINDOW_RAD if fleet_size == 16 else PHASE_HALF_WINDOW_RAD
    active_node = "silence_band"
    for n, p in offsets.items():
        diff = abs((theta - p + math.pi) % (2.0 * math.pi) - math.pi)
        if diff <= half_win:
            active_node = n
            break

    return {
        "ok": True,
        "fleet_size": fleet_size,
        "node": node,
        "phase_rad": theta,
        "phase_deg": round(math.degrees(theta), 2),
        "target_phase_deg": round(math.degrees(win_info["target_phase_rad"]), 2),
        "window_open": win_info["window_open"],
        "wait_seconds_to_open": win_info["wait_seconds_to_open"],
        "active_node": active_node,
        "admitted": admission.get("admitted", False),
        "admission_detail": admission.get("detail") if not admission.get("admitted") else "ADMITTED",
        "boundary_flux": round(admission.get("boundary_flux", 0.0), 4),
        "boundary_ceiling": chute.max_flux,
        "within_flux_budget": admission.get("boundary_flux", 0.0) <= chute.max_flux,
        "pending_hints": admission.get("pending_hints", 0),
    }


def tool_commit_hint_emit(args: Dict[str, Any]) -> Dict[str, Any]:
    paths = args.get("paths") or []
    message = args.get("message", "").strip()
    seat = args.get("seat", "local-mcp").strip()

    if not paths:
        return {"error": "paths list cannot be empty", "isError": True}
    if not message:
        return {"error": "message is required", "isError": True}

    if "\u2014" in message:
        return {"error": "message violates House Law: contains unicode em-dash", "isError": True}
    pronoun_matches = BANNED_PRONOUNS_RE.findall(message)
    if pronoun_matches:
        return {"error": f"message violates House Law: contains pronouns {pronoun_matches}", "isError": True}

    # Verify paths exist on disk
    missing = []
    for p in paths:
        fp = ROOT / p
        if not fp.exists():
            missing.append(p)
    if missing:
        return {"error": f"target paths do not exist on disk: {missing}", "isError": True}

    hints_dir = ROOT / "queue" / "commit_hints"
    hints_dir.mkdir(parents=True, exist_ok=True)

    ts_now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    hint_file = hints_dir / f"{seat}-{ts_now}.json"

    hint_data = {
        "seat": seat,
        "model": "sovereign-mcp-client",
        "paths": paths,
        "message": message,
    }

    hint_file.write_text(json.dumps(hint_data, indent=2) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "hint_file": str(hint_file),
        "paths_count": len(paths),
        "message": message,
        "seat": seat,
    }


def tool_chord_mint(args: Dict[str, Any]) -> Dict[str, Any]:
    domain = args.get("domain", "storage")
    action = args.get("action", "store")
    target = args.get("target", "sovereign-mesh")
    intensity = float(args.get("intensity", 1.0))

    minter = get_chord_minter()
    chord = minter.mint_chord(domain=domain, opcode=action, target=target, intensity=intensity)
    return {
        "ok": True,
        "chord": chord,
    }


def tool_chord_verify_sentinel(args: Dict[str, Any]) -> Dict[str, Any]:
    probe_id = args.get("probe_id", "").strip()
    entity = args.get("entity", "").strip()

    probes = load_false_premise_probes()
    target_probe = None
    for p in probes:
        pid = p.get("id") or p.get("probe_id") or p.get("claim_id") or ""
        if pid == probe_id or pid.startswith(probe_id) or probe_id in pid:
            target_probe = p
            break

    if not target_probe:
        return {"error": f"probe_id {probe_id} not found in false premise bank", "isError": True}

    absent_field = target_probe.get("absent_entity") or target_probe.get("absent_entities") or ""
    sentinel_tok = target_probe.get("sentinel_token", "")
    is_absent = entity.lower() in str(absent_field).lower() or entity.lower() in sentinel_tok.lower()
    return {
        "ok": True,
        "probe_id": target_probe.get("id", probe_id),
        "entity": entity,
        "is_absent": is_absent,
        "verdict": "GENUINE_ABSENCE_CONFIRMED" if is_absent else "UNKNOWN_OR_PRESENT",
        "probe_details": target_probe,
    }


def dispatch(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "cas_store":
        return tool_cas_store(args)
    if name == "cas_read":
        return tool_cas_read(args)
    if name == "cas_verify":
        return tool_cas_verify(args)
    if name == "bekko_search":
        return tool_bekko_search(args)
    if name == "kuramoto_phase":
        return tool_kuramoto_phase(args)
    if name == "commit_hint_emit":
        return tool_commit_hint_emit(args)
    if name == "chord_mint":
        return tool_chord_mint(args)
    if name == "chord_verify_sentinel":
        return tool_chord_verify_sentinel(args)
    return {"error": f"unknown tool: {name}", "isError": True}


def run_stdio_server() -> int:
    """Run JSON-RPC 2.0 MCP server loop over stdin/stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as err:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(err)[:80]}"}
            }
            print(json.dumps(err_resp), flush=True)
            continue

        rid = req.get("id")
        method = req.get("method", "")
        params = req.get("params") or {}

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": rid,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "sovereign-mesh-mcp",
                        "version": "1.0.0",
                        "description": "Decoupled Sovereign Data Plane (CAS Mesh + Bekko CPU + Kuramoto Phase + Commit Chute)"
                    }
                }
            }
        elif method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": rid,
                "result": {"tools": TOOL_DEFINITIONS}
            }
        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments") or {}
            try:
                out = dispatch(tool_name, tool_args)
                is_err = isinstance(out, dict) and out.get("isError", False)
                resp = {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(out, indent=2)}],
                        "isError": is_err
                    }
                }
            except Exception as err:
                resp = {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: {str(err)[:200]}"}],
                        "isError": True
                    }
                }
        elif method.startswith("notifications/"):
            continue
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": rid,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

        print(json.dumps(resp), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sovereign Mesh MCP Server")
    parser.add_argument("--test", action="store_true", help="Run self-test across all MCP tools")
    parser.add_argument("--call", type=str, help="Directly invoke a tool by name")
    parser.add_argument("--args", type=str, default="{}", help="JSON arguments for --call")
    parsed = parser.parse_args()

    if parsed.test:
        print("=== RUNNING SOVEREIGN MCP SELF-TEST ===")
        # 1. CAS Verify
        res_v = tool_cas_verify({})
        print(f"[1/6] CAS Verify: {res_v['valid_slabs']}/{res_v['total_slabs']} slabs valid (integrity_ok={res_v['integrity_ok']})")
        assert res_v["integrity_ok"] is True

        # 2. Kuramoto Phase
        res_k = tool_kuramoto_phase({"node": "antigravity", "fleet_size": 16})
        print(f"[2/6] Kuramoto Phase: node={res_k['node']} phase={res_k['phase_deg']} deg, active={res_k['active_node']}, flux={res_k['boundary_flux']}")
        assert "phase_deg" in res_k

        # 3. Bekko Search
        res_b = tool_bekko_search({"query": "sovereign CAS mesh and Kuramoto phase chute", "top_k": 3})
        print(f"[3/6] Bekko Search: {res_b['matches_count']} matches found in {res_b['total_corpus_vectors']} corpus vectors (top score: {res_b['matches'][0]['similarity'] if res_b['matches'] else 'none'})")
        assert res_b["matches_count"] > 0

        # 4. Chord Mint
        res_c = tool_chord_mint({"domain": "storage", "action": "replicate"})
        print(f"[4/6] Chord Mint: minted {res_c['chord']['chord_token']} domain={res_c['chord']['domain']} phase={res_c['chord']['phase_rad']} rad")
        assert "chord_token" in res_c["chord"]

        # 5. Sentinel Verify
        res_s = tool_chord_verify_sentinel({"probe_id": "FP01", "entity": "porter"})
        print(f"[5/6] Sentinel Verify: probe={res_s['probe_id']} entity={res_s['entity']} verdict={res_s['verdict']}")
        assert res_s["is_absent"] is True

        # 6. CAS Store & Read
        test_content = f"Test slab from sovereign MCP self-test at {datetime.datetime.now(datetime.timezone.utc).isoformat()}"
        res_store = tool_cas_store({"content": test_content, "domain": "test", "actor": "mcp-selftest"})
        print(f"[6/6] CAS Store & Read: stored hash={res_store['slab_hash'][:8]} ({res_store['byte_count']} bytes)")
        res_read = tool_cas_read({"slab_hash": res_store["slab_hash"]})
        assert res_read["content"] == test_content
        print("=== ALL 6 SOVEREIGN MCP SELF-TESTS PASSED ===")
        return 0

    if parsed.call:
        tool_args = json.loads(parsed.args)
        out = dispatch(parsed.call, tool_args)
        print(json.dumps(out, indent=2))
        return 0

    # Default: Stdio JSON-RPC server loop
    return run_stdio_server()


if __name__ == "__main__":
    sys.exit(main())
