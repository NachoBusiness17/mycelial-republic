#!/usr/bin/env python3
"""derived_dag - read-only DAG index over the estate's existing hash families.

Q-010 (2026-09-28, burn_reset fan-out). Cause: the estate keeps four hash
families in separate stores (verkle chain leaves/roots, git commits,
agent-state content commits, session boundary groups) with no single
traversable index, so "which chain does this hash belong to and what sits
between it and a tip" costs a full rescan every time. This verb derives one
DAG from the hashes that already exist and indexes it for subchain lookup.

Law: DERIVED + READ-ONLY over sources. It reads
  memory/biography/verkle_chain.jsonl     (verkle leaves, roots, sessions)
  memory/agent_state/chain.jsonl + tip.json (agent-state commits)
  git log --all                            (git commits + parents)
  memory/sessions/*.json                   (session records, optional)
and writes ONLY its own index (default memory/derived/derived_dag_index.json).
It never writes to any source and never touches the verkle chain tip
(memory/biography/verkle_tip.json) or state/CURRENT.md.

Cross-family links exist only by exact hash identity: a hash seen in two
families merges into one node and the merge is counted. No inferred or
approximate links are emitted (no-fabrication law); a link the bytes do not
prove does not exist in this index.

CLI (all output JSON on stdout unless noted):
  python tools/derived_dag.py build [--out PATH]
  python tools/derived_dag.py stats [--index PATH]
  python tools/derived_dag.py lookup HASH [--index PATH]
  python tools/derived_dag.py path A B [--index PATH]
  python tools/derived_dag.py subchain HASH [--up N] [--down N] [--index PATH]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERKLE_CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
STATE_CHAIN = ROOT / "memory" / "agent_state" / "chain.jsonl"
STATE_TIP = ROOT / "memory" / "agent_state" / "tip.json"
SESSION_DIR = ROOT / "memory" / "sessions"
DEFAULT_INDEX = ROOT / "memory" / "derived" / "derived_dag_index.json"
SESSION_NS = "session:"
GIT_LOG_FMT = "%H%x1f%cI%x1f%P"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _spawn(cmd: list[str]) -> subprocess.CompletedProcess:
    """Headless spawn: CREATE_NO_WINDOW on win32 (spawn_sites_no_window law)."""
    kw: dict[str, Any] = dict(cwd=str(ROOT), capture_output=True, text=True, timeout=120)
    if sys.platform == "win32":
        kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    return subprocess.run(cmd, **kw)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


class DagIndex:
    """Accumulates nodes/edges/sessions; nodes merge on exact hash identity."""

    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.parents: dict[str, list[list[str]]] = {}
        self.children: dict[str, list[list[str]]] = {}
        self.sessions: dict[str, dict[str, Any]] = {}
        self.merges: list[dict[str, str]] = []

    def node(self, h: str, kind: str, source: str, **meta: Any) -> None:
        rec = self.nodes.get(h)
        if rec is None:
            self.nodes[h] = {"kinds": [kind], "sources": [source], "meta": meta}
            return
        if kind not in rec["kinds"]:
            # real cross-family identity merge: same hash, new family
            rec["kinds"].append(kind)
            self.merges.append({"hash": h, "kinds": sorted(rec["kinds"])})
        if source not in rec["sources"]:
            rec["sources"].append(source)
        for k, v in meta.items():
            rec["meta"].setdefault(k, v)

    def edge(self, parent: str, child: str, kind: str) -> None:
        pk, ck = [parent, kind], [child, kind]
        plist, clist = self.parents.setdefault(child, []), self.children.setdefault(parent, [])
        if pk not in plist:
            plist.append(pk)
        if ck not in clist:
            clist.append(ck)

    def session(self, sid: str, member: str | None = None, start: Any = None,
                end: Any = None, source: str = "") -> None:
        rec = self.sessions.setdefault(sid, {"members": [], "starts": [], "ends": [], "sources": []})
        if source and source not in rec["sources"]:
            rec["sources"].append(source)
        for field, value in (("members", member), ("starts", start), ("ends", end)):
            if value is not None and value != "" and value not in rec[field]:
                rec[field].append(value)

    def to_dict(self) -> dict[str, Any]:
        for sid in self.sessions:
            self.sessions[sid]["members"].sort()
            self.sessions[sid]["starts"].sort()
            self.sessions[sid]["ends"].sort()
        return {
            "schema": "derived_dag_index.v1",
            "built": _utc(),
            "nodes": {h: self.nodes[h] for h in sorted(self.nodes)},
            "parents": {h: sorted(self.parents.get(h, [])) for h in sorted(self.parents)},
            "children": {h: sorted(self.children.get(h, [])) for h in sorted(self.children)},
            "sessions": {s: self.sessions[s] for s in sorted(self.sessions)},
            "identity_merges": self.merges,
        }


def add_verkle(dag: DagIndex) -> dict[str, Any]:
    rows = _read_jsonl(VERKLE_CHAIN)
    for row in rows:
        leaf = str(row.get("leaf_hash") or "")
        root = str(row.get("verkle_root") or "")
        parent_root = str(row.get("parent_verkle_root") or "")
        pos = row.get("index")
        meta = {"chain_index": pos, "ts": row.get("ts"), "filename": row.get("filename"),
                "dossier_commit": row.get("dossier_commit")}
        if leaf:
            dag.node(leaf, "verkle_leaf", "verkle_chain", **{**meta, "n_leaves": row.get("n_leaves")})
        if root:
            dag.node(root, "verkle_root", "verkle_chain", **meta)
        if root and parent_root:
            dag.node(parent_root, "verkle_root", "verkle_chain")
            dag.edge(parent_root, root, "verkle_parent")
        sid = str(row.get("session_id") or "")
        if sid:
            dag.session(sid, member=root or leaf, start=row.get("start_minute"),
                        end=row.get("end_minute"), source="verkle_chain")
            anchor = SESSION_NS + sid
            dag.node(anchor, "session", "verkle_chain", session_id=sid)
            if root or leaf:
                dag.edge(anchor, root or leaf, "session_member")
    return {"source": str(VERKLE_CHAIN.relative_to(ROOT)), "rows": len(rows),
            "found": VERKLE_CHAIN.is_file()}


def add_agent_state(dag: DagIndex) -> dict[str, Any]:
    rows = _read_jsonl(STATE_CHAIN)
    for row in rows:
        commit = str(row.get("content_commit") or "")
        parent = str(row.get("parent_commit") or "")
        meta = {"ts": row.get("ts"), "filename": row.get("filename"),
                "label": row.get("label"), "state_session": row.get("session_id") or None,
                "reason": row.get("reason")}
        if commit:
            dag.node(commit, "state_commit", "agent_state", **meta)
        if commit and parent:
            dag.node(parent, "state_commit", "agent_state")
            dag.edge(parent, commit, "state_parent")
        sid = str(row.get("session_id") or "")
        if sid:
            dag.session(sid, member=commit, start=row.get("ts"), end=row.get("ts"),
                        source="agent_state")
    tip: dict[str, Any] = {}
    if STATE_TIP.is_file():
        try:
            tip = json.loads(STATE_TIP.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            tip = {}
        root_hash = str(tip.get("root") or "")
        if root_hash:
            dag.node(root_hash, "state_tip_root", "agent_state_tip",
                     updated=tip.get("updated"), n_versions=tip.get("n_versions"))
    return {"source": str(STATE_CHAIN.relative_to(ROOT)), "rows": len(rows),
            "found": STATE_CHAIN.is_file(), "tip_found": STATE_TIP.is_file(),
            "tip_root": tip.get("root")}


def add_git(dag: DagIndex) -> dict[str, Any]:
    proc = _spawn(["git", "log", "--all", f"--format={GIT_LOG_FMT}"])
    n = 0
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            parts = line.split("\x1f")
            if len(parts) != 3 or not parts[0]:
                continue
            commit, date, parents_field = parts
            dag.node(commit, "git_commit", "git", committed=date)
            for parent in parents_field.split():
                dag.node(parent, "git_commit", "git")
                dag.edge(parent, commit, "git_parent")
            n += 1
    return {"source": "git log --all", "commits_walked": n,
            "found": proc.returncode == 0, "error": None if proc.returncode == 0 else proc.stderr.strip()}


def add_session_records(dag: DagIndex) -> dict[str, Any]:
    n = 0
    if SESSION_DIR.is_dir():
        for path in sorted(SESSION_DIR.glob("*.json")):
            try:
                rec = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(rec, dict):
                continue
            sid = str(rec.get("session_id") or "")
            if not sid:
                continue
            dag.session(sid, start=rec.get("ts"), end=rec.get("ts"), source="session_record")
            dag.node(SESSION_NS + sid, "session", "session_record", session_id=sid,
                     record=path.name)
            n += 1
    return {"source": str(SESSION_DIR.relative_to(ROOT)), "records": n, "found": SESSION_DIR.is_dir()}


def build(out: Path) -> dict[str, Any]:
    dag = DagIndex()
    sources = [add_verkle(dag), add_agent_state(dag), add_git(dag), add_session_records(dag)]
    payload = dag.to_dict()
    payload["sources"] = sources
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, sort_keys=True, indent=1), encoding="utf-8")
    return {"index": str(out), "bytes": out.stat().st_size, "nodes": len(payload["nodes"]),
            "identity_merges": len(payload["identity_merges"]),
            "sessions": len(payload["sessions"]),
            "edges": {kind: sum(1 for lst in payload["parents"].values()
                                for pair in lst if pair[1] == kind)
                      for kind in ("verkle_parent", "state_parent", "git_parent",
                                   "session_member")},
            "sources": sources}


def _load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"no index at {path}; run: python tools/derived_dag.py build")
    return json.loads(path.read_text(encoding="utf-8"))


def lookup(idx: dict[str, Any], h: str) -> dict[str, Any]:
    return {"hash": h, "node": idx["nodes"].get(h),
            "parents": idx.get("parents", {}).get(h, []),
            "children": idx.get("children", {}).get(h, []),
            # sessions are keyed by raw session_id; a hash only matches if it
            # literally is a session_id (sessions use the "session:" node ns)
            "session_group": idx.get("sessions", {}).get(h)}


def _adjacency(idx: dict[str, Any]) -> dict[str, list[tuple[str, str]]]:
    adj: dict[str, list[tuple[str, str]]] = {}
    for child, lst in idx.get("parents", {}).items():
        adj.setdefault(child, []).extend((p, k) for p, k in lst)
    for parent, lst in idx.get("children", {}).items():
        adj.setdefault(parent, []).extend((c, k) for c, k in lst)
    return adj


def path_between(idx: dict[str, Any], a: str, b: str) -> dict[str, Any]:
    adj = _adjacency(idx)
    if a not in idx["nodes"] or b not in idx["nodes"]:
        return {"a": a, "b": b, "found": False,
                "missing": [h for h in (a, b) if h not in idx["nodes"]]}
    prev: dict[str, tuple[str, str]] = {a: ("", "")}
    q: deque[str] = deque([a])
    while q and b not in prev:
        cur = q.popleft()
        for nxt, kind in adj.get(cur, []):
            if nxt not in prev:
                prev[nxt] = (cur, kind)
                q.append(nxt)
    if b not in prev:
        return {"a": a, "b": b, "found": False, "reason": "no undirected path in derived DAG"}
    chain, cur = [], b
    while cur != a:
        parent, kind = prev[cur]
        chain.append({"hash": cur, "via": kind})
        cur = parent
    chain.append({"hash": a, "via": "start"})
    chain.reverse()
    return {"a": a, "b": b, "found": True, "length_edges": len(chain) - 1, "chain": chain}


def subchain(idx: dict[str, Any], h: str, up: int, down: int) -> dict[str, Any]:
    if h not in idx["nodes"]:
        return {"hash": h, "found": False}
    adj = _adjacency(idx)
    result: dict[str, Any] = {"hash": h, "found": True,
                              "kinds": idx["nodes"][h]["kinds"]}
    for name, limit, field in (("ancestors", up, "parents"), ("descendants", down, "children")):
        steps: list[dict[str, Any]] = []
        seen = {h}
        frontier = [(h, 0)]
        while frontier and len(seen) < 4000:
            cur, depth = frontier.pop(0)
            if depth >= limit:
                continue
            for nxt, kind in idx.get(field, {}).get(cur, []):
                if nxt in seen:
                    continue
                seen.add(nxt)
                steps.append({"depth": depth + 1, "hash": nxt, "via": kind,
                              "kinds": idx["nodes"].get(nxt, {}).get("kinds", [])})
                frontier.append((nxt, depth + 1))
        steps.sort(key=lambda s: (s["depth"], s["hash"]))
        result[name] = {"limit": limit, "count": len(steps), "steps": steps}
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="read-only derived DAG over estate hash families")
    ap.add_argument("--index", default=str(DEFAULT_INDEX), help="index path (default memory/derived)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--out", default=None)
    sub.add_parser("stats")
    lk = sub.add_parser("lookup")
    lk.add_argument("hash")
    pt = sub.add_parser("path")
    pt.add_argument("a")
    pt.add_argument("b")
    sc = sub.add_parser("subchain")
    sc.add_argument("hash")
    sc.add_argument("--up", type=int, default=0)
    sc.add_argument("--down", type=int, default=0)
    args = ap.parse_args(argv)
    idx_path = Path(args.out) if getattr(args, "out", None) else Path(args.index)
    if args.cmd == "build":
        print(json.dumps(build(idx_path), sort_keys=True, indent=1))
    elif args.cmd == "stats":
        idx = _load(idx_path)
        kinds: dict[str, int] = {}
        for rec in idx["nodes"].values():
            for k in rec["kinds"]:
                kinds[k] = kinds.get(k, 0) + 1
        print(json.dumps({"index": str(idx_path), "nodes": len(idx["nodes"]),
                          "kinds": dict(sorted(kinds.items())),
                          "sessions": len(idx.get("sessions", {})),
                          "identity_merges": idx.get("identity_merges", []),
                          "sources": idx.get("sources", [])}, sort_keys=True, indent=1))
    elif args.cmd == "lookup":
        print(json.dumps(lookup(_load(idx_path), args.hash), sort_keys=True, indent=1))
    elif args.cmd == "path":
        print(json.dumps(path_between(_load(idx_path), args.a, args.b), sort_keys=True, indent=1))
    elif args.cmd == "subchain":
        print(json.dumps(subchain(_load(idx_path), args.hash, args.up, args.down),
                         sort_keys=True, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
