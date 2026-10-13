"""mesh.knot - the nightly/commit Merkle knot (architecture v2).

Salon verdict: "without the knot, append-only is a belief, not a property" - so the
knot exists from the FIRST minute (build it on the empty room). Seals every feed tip
plus every library blob hash into chain.jsonl; knots are cut at every broker commit
and on demand. verify_chain recomputes each knot's merkle root and checks the chain
links; reports unsealed rows honestly (rows newer than the last knot are named, not
hidden).

Schema: mesh.knot.v1 · chain.jsonl rows {"kno","ts","prev","leaves":[...],"merkle"}
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

SCHEMA = "mesh.knot.v1"


def _canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def merkle(leaves: list[str]) -> str:
    """Pairwise sha256 merkle root over sorted unique leaves; empty -> sha of nothing."""
    layer = sorted(set(leaves)) or [hashlib.sha256(b"").hexdigest()]
    layer = [h.encode() for h in layer]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            pair = layer[i] + (layer[i + 1] if i + 1 < len(layer) else layer[i])
            nxt.append(hashlib.sha256(pair).digest())
        layer = nxt
    return layer[0].hex()


def _leaves(root: Path) -> list[str]:
    import mag.mesh.feeds as feeds
    leaves = []
    for keyf in sorted((Path(root) / "feeds").glob("*.key")):
        tip = feeds.feed_tip(root, keyf.stem)
        if tip:
            leaves.append(tip)
    blobs = Path(root) / "library" / "blobs"
    if blobs.is_dir():
        leaves += [p.name for p in blobs.iterdir() if p.is_file()]
    for name in ("refusals.jsonl", "decisions.jsonl"):
        f = Path(root) / name
        if f.exists() and f.stat().st_size:
            leaves.append(hashlib.sha256(f.read_bytes()).hexdigest())
    return leaves


def seal(root: Path) -> dict:
    """Cut a knot now: all current tips/blobs sealed under one merkle root."""
    root = Path(root)
    chainf = root / "chain.jsonl"
    knots = [json.loads(x) for x in chainf.read_text().splitlines() if x.strip()] \
        if chainf.exists() else []
    leaves = _leaves(root)
    knot = {"kno": len(knots), "ts": round(time.time(), 3),
            "prev": knots[-1]["merkle"] if knots else "GENESIS",
            "leaves": leaves, "merkle": merkle(leaves)}
    with chainf.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(knot, sort_keys=True) + "\n")
    return {"ok": True, "knot": knot, "schema": SCHEMA}


def verify_chain(root: Path) -> dict:
    """Recompute every knot's merkle, walk prev links, and name unsealed live rows."""
    root = Path(root)
    chainf = root / "chain.jsonl"
    if not chainf.exists():
        return {"ok": False, "error": "no chain: seal(root) first (knot-before-rows law)",
                "schema": SCHEMA}
    prev, bad, knots = "GENESIS", [], 0
    for i, line in enumerate(chainf.read_text().splitlines()):
        if not line.strip():
            continue
        try:
            k = json.loads(line)
        except json.JSONDecodeError:
            bad.append({"knot": i, "why": "unparseable"})
            continue
        knots += 1
        if k.get("prev") != prev or merkle(k.get("leaves", [])) != k.get("merkle"):
            bad.append({"knot": i, "why": "prev link or merkle mismatch (tamper class)"})
        prev = k.get("merkle")
    live = _leaves(root)
    sealed = set()
    if knots:
        last = json.loads(chainf.read_text().strip().splitlines()[-1])
        sealed = set(last.get("leaves", []))
    unsealed = [h for h in live if h not in sealed]
    return {"ok": not bad, "knots": knots, "violations": bad,
            "tip": prev, "unsealed_leaves": len(unsealed),
            "note": f"{len(unsealed)} leaf hash(es) newer than the last knot (seal to cover)",
            "schema": SCHEMA}
