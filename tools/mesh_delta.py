#!/usr/bin/env python3
"""mesh_delta: the rib-torrent seed for the memory standing wave.

Operator orders fused 2026-10-07: (1) "mirror our shit across everything so
they can work on the same copy in tandem with local versions, dogfooding our
network, mcp serving/torrenting the added/removed items in memory to give the
most updated picture from an mcp server"; (2) "a smarter way to switchboard
this across all our machines so we're not bogging one down - we're seeing 100
different disk greps and none of our processes locally are working together."

The water-computer answer: index ONCE, serve MANY. Every seat and machine
pulls the delta from the seed instead of greping the tree itself. Torrent
semantics: content-addressed chunks (sha256 per file), verify-then-serve,
removed detection by snapshot diff, cursors so any peer asks "what changed
since X". The verkle chain tip rides the picture as the estate's own cursor.

Modes:
  scan     - (re)build the snapshot index (memory/ tree, churn-tolerant)
  serve    - HTTP seed on the given bind (default 127.0.0.1:8767; pass the
             tailnet IP to seed for bob/Pixel)
  pull     - client: fetch picture/delta from a peer, sha-verify chunks,
             apply added/changed into the local tree (--apply; --prune for
             removals; default is a dry report)
  mcp      - stdio JSON-RPC in the tools/gps_mcp dialect (tools: picture,
             delta, fetch, plant, witness, tally) for MCP clients on
             this machine; plant/witness/tally are the memlance wire
             (.agents/skills/memlance/SKILL.md, P4 2026-10-07)

Laws carried: paths are forced under the memory root (no traversal); chunks
are refused when the served sha does not match the request; the client
verifies every byte against the peer's advertised sha before writing;
removals never touch the live tree without --prune.

Usage:
  python -m tools.mesh_delta scan
  python -m tools.mesh_delta serve --bind 127.0.0.1 --port 8767
  python -m tools.mesh_delta pull --peer http://100.x.y.z:8767 [--apply] [--prune]
  python -m tools.mesh_delta mcp
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
MEMORY = ROOT / "memory"
MESH = MEMORY / "mesh"
LANCES = MESH / "lances"
LANCES_LEDGER = LANCES / "lances_ledger.jsonl"
# Witness fence: a lance target surface (chan row, context-pack source)
# must live inside the repo; anything resolving outside is refused.
WITNESS_FENCE = ROOT
INDEX = MESH / "delta_index.json"
HISTORY = MESH / "index_history"
HISTORY_KEEP = 12
CHUNK_CAP = 8 * 1024 * 1024
TIP = MEMORY / "biography" / "verkle_tip.json"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb", buffering=1024 * 1024) as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def scan() -> dict:
    """One tolerant walk of memory/ -> snapshot index. Churn (knots appearing
    and vanishing mid-walk) is expected; vanished files are skipped, and the
    next scan diffs them away as removals. Incremental: files whose
    size+mtime match the previous index keep their recorded sha256 (the
    first bootstrap hashes everything once; steady-state scans hash only
    what moved)."""
    MESH.mkdir(parents=True, exist_ok=True)
    prev: dict = {}
    try:
        prev = json.loads(INDEX.read_text(encoding="utf-8")).get("files", {})
    except Exception:
        prev = {}
    files: dict[str, dict] = {}
    total = 0
    for p in MEMORY.rglob("*"):
        try:
            if not p.is_file() or MESH in p.parents or p == MESH:
                continue
            st = p.stat()
            rel = p.relative_to(ROOT).as_posix()
            prior = prev.get(rel)
            if prior and prior.get("size") == st.st_size \
                    and prior.get("mtime") == int(st.st_mtime):
                files[rel] = prior  # unchanged: keep the recorded sha
            else:
                files[rel] = {"size": st.st_size, "mtime": int(st.st_mtime),
                              "sha256": sha256_file(p)}
            total += st.st_size
        except OSError:
            continue  # vanished mid-walk or locked: next scan diffs it
    tip = {}
    try:
        tip = json.loads(TIP.read_text(encoding="utf-8"))
    except Exception:
        tip = {}
    # Fix 2026-10-09 (locksmith cycle, receipt
    # watch/inbox/mates_leave_protocol/receipts/receipt_20261009_locksmith.md):
    # verkle_tip.json is schema verkle_tip.v1 and carries n_leaves/updated_minute,
    # never index/generated, so both cursor fields read null forever. rib_boot.py:278-282
    # maps the same anchor as index=n_leaves, generated=updated_minute; this is that mapping.
    snap = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "files": files, "total_bytes": total,
            "chain_tip_index": tip.get("n_leaves"),
            "chain_tip_ts": tip.get("updated_minute")}
    if INDEX.exists():
        HISTORY.mkdir(parents=True, exist_ok=True)
        prev = json.loads(INDEX.read_text(encoding="utf-8"))
        stamp = prev.get("ts", "unknown").replace(":", "").replace("+", "_")
        (HISTORY / ("index_" + stamp + ".json")).write_text(
            json.dumps(prev), encoding="utf-8")
        olds = sorted(HISTORY.glob("index_*.json"))
        for old in olds[:-HISTORY_KEEP]:
            old.unlink(missing_ok=True)
    INDEX.write_text(json.dumps(snap), encoding="utf-8")
    return {"scanned": len(files), "total_mb": total // 1048576,
            "ts": snap["ts"], "chain_tip_index": snap["chain_tip_index"]}


def load_snap(when: str | None = None) -> dict | None:
    """Snapshot at/before `when` (ISO) from history, else the newest."""
    snaps: list[tuple[str, Path]] = []
    if HISTORY.exists():
        for p in HISTORY.glob("index_*.json"):
            try:
                s = json.loads(p.read_text(encoding="utf-8"))
                snaps.append((str(s.get("ts", "")), p))
            except Exception:
                continue
    if INDEX.exists():
        s = json.loads(INDEX.read_text(encoding="utf-8"))
        snaps.append((str(s.get("ts", "")), INDEX))
    snaps.sort()
    if not when:
        return json.loads(snaps[-1][1].read_text(encoding="utf-8")) if snaps else None
    for ts, p in reversed(snaps):
        if ts <= when:
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def delta(since: str) -> dict:
    old = load_snap(since)
    new = load_snap(None)
    if not old or not new:
        return {"error": "no snapshot at or before " + str(since)}
    of, nf = old.get("files", {}), new.get("files", {})
    added = sorted(set(nf) - set(of))
    removed = sorted(set(of) - set(nf))
    changed = sorted(p for p in set(nf) & set(of) if nf[p]["sha256"] != of[p]["sha256"])
    return {"since": since, "now": new.get("ts"),
            "chain_tip_index": new.get("chain_tip_index"),
            "added": [{"path": p, **nf[p]} for p in added],
            "changed": [{"path": p, **nf[p]} for p in changed],
            "removed": removed}


def read_chunk(rel: str, want_sha: str) -> bytes | None:
    p = (ROOT / rel).resolve()
    if MEMORY.resolve() not in p.parents or not p.is_file():
        return None
    data = p.read_bytes()
    if len(data) > CHUNK_CAP or hashlib.sha256(data).hexdigest() != want_sha:
        return None
    return data


# ---------------- HTTP seed ----------------

class Seed(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet; the receipt carries the round trip
        pass

    def _json(self, obj: dict, code: int = 200) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/picture":
            snap = load_snap(None)
            if not snap:
                self._json({"error": "no index; run scan first"}, 503)
                return
            self._json({"ts": snap["ts"], "files": len(snap["files"]),
                        "total_bytes": snap.get("total_bytes"),
                        "chain_tip_index": snap.get("chain_tip_index"),
                        "chain_tip_ts": snap.get("chain_tip_ts")})
        elif u.path == "/delta":
            self._json(delta((q.get("since") or [""])[0]))
        elif u.path == "/chunk":
            data = read_chunk((q.get("path") or [""])[0],
                              (q.get("sha") or [""])[0])
            if data is None:
                self._json({"error": "refused: outside memory root, over cap, "
                                     "or sha mismatch"}, 403)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self._json({"error": "unknown door"}, 404)


# ---------------- client ----------------
#
# SSRF fence (Mimosa L2 findings 2026-10-07, the free_lane_fleet/_guarded_get
# pattern inverted for a mesh client): the sanctioned peers ARE private
# addresses (loopback, tailnet CGNAT 100.64/10, RFC1918), so the fence allows
# loopback+private and refuses everything else - public internet, link-local
# cloud metadata (169.254.169.254), multicast, reserved. Also: http/https
# only, no userinfo, DNS resolved and pinned to the first validated IP
# (rebinding defense: the connection goes to the checked address, not the
# name), redirects refused (a peer cannot bounce us), responses read bounded.
# HTTPS caveat: the IP-pinned request validates the cert against the IP, so
# the sanctioned v0 transport is http inside the tailnet (WireGuard-encrypted
# below us); https peers work only with IP-signed certs.

_GUARD_MAX_BYTES = CHUNK_CAP + 1


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # a peer cannot bounce the client
        raise urllib.error.HTTPError(a[1] if len(a) > 1 else 0,
                                     302, "redirect refused by mesh fence",
                                     None, None)


_OPENER = urllib.request.build_opener(_NoRedirect)


def _guarded_fetch(url: str) -> bytes:
    import ipaddress as _ip
    import socket as _socket
    u = urlparse(url)
    if u.scheme not in ("http", "https"):
        raise ValueError("mesh fence: scheme must be http or https")
    if u.username or u.password or "@" in (u.netloc or ""):
        raise ValueError("mesh fence: userinfo refused")
    host = u.hostname
    if not host:
        raise ValueError("mesh fence: no host")
    port = u.port or (443 if u.scheme == "https" else 80)
    # Explicit allowlist, not is_private: Python 3.11 counts link-local
    allow_nets = [_ip.ip_network(n) for n in
                  ("100.64.0.0/10", "10.0.0.0/8", "172.16.0.0/12",
                   "192.168.0.0/16")]
    infos = _socket.getaddrinfo(host, port, proto=_socket.IPPROTO_TCP)
    pinned = None
    for info in infos:
        cand = _ip.ip_address(info[4][0])
        if cand.is_loopback or any(cand in n for n in allow_nets):
            pinned = cand
            break
    if pinned is None:
        raise ValueError(
            "mesh fence: " + host + " resolves to no allowed address "
            "(allowed: loopback, tailnet CGNAT 100.64/10, RFC1918 private; "
            "public, link-local metadata, multicast refused)")
    pinned_url = u._replace(netloc=f"{pinned}:{port}").geturl()
    req = urllib.request.Request(pinned_url, headers={"Host": host})
    with _OPENER.open(req, timeout=60) as r:
        data = r.read(_GUARD_MAX_BYTES)
    if len(data) >= _GUARD_MAX_BYTES:
        raise ValueError("mesh fence: response over cap")
    return data


def pull(peer: str, apply: bool, prune: bool) -> dict:
    pic = json.loads(_guarded_fetch(peer + "/picture").decode())
    local = load_snap(None)
    since = (local or {}).get("ts")
    rep: dict = {"peer": peer, "peer_picture": pic, "local_scan_ts": since}
    if not since:
        rep["note"] = "no local index: run scan first, then pull"
        return rep
    d = json.loads(_guarded_fetch(peer + "/delta?since=" + since).decode())
    rep["added_n"] = len(d.get("added", []))
    rep["changed_n"] = len(d.get("changed", []))
    rep["removed_n"] = len(d.get("removed", []))
    if not apply:
        rep["mode"] = "dry (pass --apply to write, --prune to remove)"
        return rep
    written = 0
    for item in (d.get("added", []) + d.get("changed", [])):
        rel, want = item["path"], item["sha256"]
        url = peer + "/chunk?path=" + urllib.request.quote(rel, safe="/") \
            + "&sha=" + want
        try:
            data = _guarded_fetch(url)
        except Exception:
            continue
        got = hashlib.sha256(data).hexdigest()
        if got != want:  # verify every byte against the advertised sha
            continue
        dest = ROOT / rel
        if MEMORY.resolve() not in dest.resolve().parents:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        written += 1
    pruned = 0
    if prune:
        for rel in d.get("removed", []):
            dest = ROOT / rel
            try:
                if MEMORY.resolve() in dest.resolve().parents and dest.is_file():
                    dest.unlink()
                    pruned += 1
            except OSError:
                continue
    rep["applied_writes"] = written
    rep["pruned"] = pruned
    scan()
    return rep


# ---------------- memlance (P4: the aimed seed gets a wire) ----------------
#
# .agents/skills/memlance/SKILL.md described the unit of fire (plant one
# seed where a target's BOOT reads; the hit is the target citing it
# unprompted); this section gives it a wire in the same MCP server as the
# mesh picture:
#   plant   - one lance becomes a content-addressed chunk under
#             memory/mesh/lances/ ({aim, seed, planted_ts}; sha256 of the
#             payload is the seed_id, so fetch verifies it like any chunk)
#   witness - check a target surface (chan row, context-pack source) for
#             unprompted citation; banks hit_ts + latency in the ledger
#   tally   - per-seed hit rates from the same ledger (the skill's
#             falsifier reads this: fewer than 2 hits in 5 lances disputes
#             the concept as steering)
# The lances dir sits under memory/mesh/, which scan() already excludes
# from the delta index, so a planted lance never perturbs the picture it
# rides across the mesh.

_HEX_DIGITS = set("0123456789abcdef")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _iso_ts(ts: str) -> "datetime | None":
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def _ledger_append(row: dict) -> None:
    LANCES.mkdir(parents=True, exist_ok=True)
    with open(LANCES_LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def _read_ledger() -> list:
    if not LANCES_LEDGER.exists():
        return []
    rows = []
    for line in LANCES_LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def _seed_chunk(seed_id: str) -> "Path | None":
    """Path fence: a seed_id must be the 64-hex sha256 of its own payload.
    Anything else (traversal, suffixes, wrong length, non-hex) is refused
    before it can touch the filesystem."""
    if len(seed_id) != 64 or not set(seed_id) <= _HEX_DIGITS:
        return None
    return LANCES / (seed_id + ".json")


def plant(aim: str, seed: str) -> dict:
    if not aim or not seed:
        return {"error": "refused: plant needs both aim and seed"}
    payload = {"aim": aim, "seed": seed, "planted_ts": _now_iso()}
    body = json.dumps(payload, sort_keys=True).encode("utf-8")
    seed_id = hashlib.sha256(body).hexdigest()
    chunk = _seed_chunk(seed_id)
    if chunk is None:  # unreachable for sha256 hex; kept for the fence
        return {"error": "refused: seed_id failed the chunk fence"}
    LANCES.mkdir(parents=True, exist_ok=True)
    dedup = chunk.exists()
    if not dedup:
        chunk.write_bytes(body)
    _ledger_append({"type": "plant", "seed_id": seed_id, "aim": aim,
                    "ts": payload["planted_ts"], "dedup": dedup})
    return {"seed_id": seed_id, "planted_ts": payload["planted_ts"],
            "chunk": "memory/mesh/lances/" + seed_id + ".json",
            "dedup": dedup}


def witness(seed_id: str, surface: str, needle: str | None = None) -> dict:
    chunk = _seed_chunk(seed_id)
    if chunk is None or not chunk.is_file():
        return {"error": "refused: seed_id must be the 64-hex sha of a "
                         "planted lance chunk"}
    body = chunk.read_bytes()
    if hashlib.sha256(body).hexdigest() != seed_id:
        return {"error": "refused: lance chunk fails its own sha (tampered)"}
    payload = json.loads(body.decode("utf-8"))
    fence = WITNESS_FENCE.resolve()
    sp = (ROOT / surface).resolve()
    if fence not in sp.parents:
        return {"error": "refused: surface resolves outside the witness "
                         "fence (" + str(fence) + ")"}
    if not sp.is_file():
        return {"error": "refused: no such surface file: " + str(sp)}
    text = sp.read_text(encoding="utf-8", errors="replace")
    hay = str(payload.get("seed", "")) if needle is None else needle
    hit = bool(hay) and hay.casefold() in text.casefold()
    now = _now_iso()
    planted = _iso_ts(payload.get("planted_ts", ""))
    latency_s = None
    if planted is not None:
        latency_s = round((datetime.now(timezone.utc) - planted)
                          .total_seconds(), 3)
    row = {"type": "witness", "seed_id": seed_id,
           "surface": sp.relative_to(fence).as_posix(),
           "needle": "seed" if needle is None else needle,
           "hit": hit, "ts": now, "latency_s": latency_s}
    if hit:
        row["hit_ts"] = now
    _ledger_append(row)
    return row


def tally() -> dict:
    lances: dict = {}
    for row in _read_ledger():
        sid = str(row.get("seed_id", ""))
        if not sid:
            continue
        s = lances.setdefault(sid, {"aim": None, "plants": 0,
                                    "witnesses": 0, "hits": 0})
        if row.get("type") == "plant":
            s["aim"] = row.get("aim")
            s["plants"] += 1
        elif row.get("type") == "witness":
            s["witnesses"] += 1
            if row.get("hit"):
                s["hits"] += 1
    per_seed = []
    for sid, s in sorted(lances.items()):
        row = {"seed_id": sid}
        row.update(s)
        w = s["witnesses"]
        row["hit_rate"] = round(s["hits"] / w, 4) if w else None
        per_seed.append(row)
    witnessed = [s for s in per_seed if s["witnesses"]]
    total_w = sum(s["witnesses"] for s in witnessed)
    total_h = sum(s["hits"] for s in witnessed)
    return {"lances": len(per_seed), "per_seed": per_seed,
            "overall": {"witnesses": total_w, "hits": total_h,
                        "hit_rate": round(total_h / total_w, 4)
                        if total_w else None}}


# ---------------- stdio MCP (gps_mcp dialect) ----------------

def mcp_loop() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        method = req.get("method", "")
        rid = req.get("id")
        params = req.get("params") or {}
        args = params.get("arguments") or {}

        def reply(result):
            sys.stdout.write(json.dumps(
                {"jsonrpc": "2.0", "id": rid,
                 "result": {"content": [{"type": "text",
                                         "text": json.dumps(result)}],
                            "isError": False}}) + "\n")
            sys.stdout.flush()

        if method == "initialize":
            reply({"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                   "serverInfo": {"name": "mesh-delta", "version": "0.1"}})
        elif method == "tools/list":
            reply({"tools": [
                {"name": "picture",
                 "description": "The most updated picture: memory snapshot ts, "
                                "file count, bytes, verkle chain tip cursor."},
                {"name": "delta",
                 "description": "Added/changed/removed memory items since an "
                                "ISO ts, each with sha256.",
                 "inputSchema": {"type": "object",
                                 "properties": {"since": {"type": "string"}}}},
                {"name": "fetch",
                 "description": "One memory file's bytes, sha-verified against "
                                "the index.",
                 "inputSchema": {"type": "object",
                                 "properties": {"path": {"type": "string"},
                                                "sha256": {"type": "string"}}}},
                {"name": "plant",
                 "description": "Memlance: plant one aimed seed as a "
                                "content-addressed chunk under "
                                "memory/mesh/lances/ ({aim, seed, "
                                "planted_ts}); returns its seed_id.",
                 "inputSchema": {"type": "object",
                                 "properties": {"aim": {"type": "string"},
                                                "seed": {"type": "string"}},
                                 "required": ["aim", "seed"]}},
                {"name": "witness",
                 "description": "Memlance: check a repo surface (chan row, "
                                "context-pack source) for unprompted citation "
                                "of a planted seed; banks hit_ts + latency in "
                                "the lances ledger.",
                 "inputSchema": {"type": "object",
                                 "properties": {"seed_id": {"type": "string"},
                                                "surface": {"type": "string"},
                                                "needle": {"type": "string"}},
                                 "required": ["seed_id", "surface"]}},
                {"name": "tally",
                 "description": "Memlance: per-seed witness hit rates from "
                                "the lances ledger (falsifier: fewer than 2 "
                                "hits in 5 lances disputes the concept)."}]})
        elif method == "tools/call":
            name = params.get("name")
            if name == "picture":
                snap = load_snap(None)
                reply({"ts": (snap or {}).get("ts"),
                       "files": len((snap or {}).get("files", {})),
                       "chain_tip_index": (snap or {}).get("chain_tip_index")})
            elif name == "delta":
                reply(delta(str(args.get("since", ""))))
            elif name == "fetch":
                data = read_chunk(str(args.get("path", "")),
                                  str(args.get("sha256", "")))
                reply({"bytes_b64_ok": data is not None,
                       "size": len(data) if data else 0,
                       "note": "refused or missing" if data is None
                       else "verified; read locally at the same repo path"})
            elif name == "plant":
                reply(plant(str(args.get("aim", "")),
                            str(args.get("seed", ""))))
            elif name == "witness":
                needle = args.get("needle")
                reply(witness(str(args.get("seed_id", "")),
                              str(args.get("surface", "")),
                              None if needle is None else str(needle)))
            elif name == "tally":
                reply(tally())
            else:
                reply({"error": "unknown tool"})
        elif method == "ping":
            reply({})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    sub.add_parser("scan")
    srv = sub.add_parser("serve")
    srv.add_argument("--bind", default="127.0.0.1")
    srv.add_argument("--port", type=int, default=8767)
    pl = sub.add_parser("pull")
    pl.add_argument("--peer", required=True)
    pl.add_argument("--apply", action="store_true")
    pl.add_argument("--prune", action="store_true")
    sub.add_parser("mcp")
    args = ap.parse_args()
    if args.mode == "scan":
        print(json.dumps(scan()))
        return 0
    if args.mode == "serve":
        httpd = ThreadingHTTPServer((args.bind, args.port), Seed)
        print(f"MESH DELTA SEED: http://{args.bind}:{args.port} "
              f"(picture | delta?since= | chunk?path=&sha=)", flush=True)
        httpd.serve_forever()
        return 0
    if args.mode == "pull":
        print(json.dumps(pull(args.peer, args.apply, args.prune)))
        return 0
    return mcp_loop()


if __name__ == "__main__":
    sys.exit(main())
