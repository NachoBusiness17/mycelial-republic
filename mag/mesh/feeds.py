"""mesh.feeds - per-writer signed feeds (architecture v2, salon verdict 2026-10-05).

AGENT_MESH_TRIANGULATION_STEAL: one log per writer, not one shared file (the SSB fix);
Ed25519-signed rows; the shared room is a MERGED VIEW computed on read, never a write
surface. Chain proves WHAT, signatures prove WHO. Crypto self-stolen from mag/proof.py
(cryptography lib Ed25519 + canonical json). Rate law: append-only without a
per-writer cap is a DoS primitive (salon S3), enforced here at append.

Schema: mesh.feeds.v1 · rows {"seq","ts","writer","kind","body","prev","sig"}
Feed file: <root>/feeds/<writer>.jsonl · key: <root>/feeds/<writer>.key (32B hex,
local-first threat model: authenticity vs local tamper; remote peers publish
pubkeys out-of-band - SSB/Nostr shape, no PKI, no CA).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

RATE_PER_MIN = 30  # the rate law (salon S3); exceeded appends are refused honestly
SCHEMA = "mesh.feeds.v1"


def _canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def _sha(b) -> str:
    import hashlib
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def _keypair(seed_hex: str):
    from binascii import unhexlify
    return Ed25519PrivateKey.from_private_bytes(unhexlify(seed_hex))


def pub_hex(key) -> str:
    return key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()


def ensure_writer(root: Path, writer: str) -> dict:
    """Create (or load) a writer's key + feed. Returns {ok, writer, pub, feed}."""
    fdir = Path(root) / "feeds"
    fdir.mkdir(parents=True, exist_ok=True)
    keyf, feedf = fdir / f"{writer}.key", fdir / f"{writer}.jsonl"
    if keyf.exists():
        seed = keyf.read_text().strip()
    else:
        seed = _sha(str(time.time_ns()) + writer)[:64]  # deterministic-ish fresh seed
        keyf.write_text(seed)
    feedf.touch()
    return {"ok": True, "writer": writer, "pub": pub_hex(_keypair(seed)),
            "feed": str(feedf), "schema": SCHEMA}


def _rows(feedf: Path) -> list[dict]:
    out = []
    for line in feedf.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                out.append({"_corrupt": line[:80]})
    return out


def _check_rate(root: Path, writer: str) -> bool:
    feedf = Path(root) / "feeds" / f"{writer}.jsonl"
    now, keep = time.time(), []
    for r in _rows(feedf):
        try:
            ts = float(r.get("ts", 0))
        except (TypeError, ValueError):
            continue
        if now - ts < 60:
            keep.append(ts)
    return len(keep) < RATE_PER_MIN


def append(root: Path, writer: str, kind: str, body: dict) -> dict:
    """Append one signed row to the writer's feed. Refuses over-rate writers."""
    root = Path(root)
    w = ensure_writer(root, writer)
    if not _check_rate(root, writer):
        return {"ok": False, "error": f"rate law: {RATE_PER_MIN} rows/min exceeded for {writer}",
                "refusal_class": "rate"}
    key = _keypair((Path(root) / "feeds" / f"{writer}.key").read_text().strip())
    prev_rows = _rows(Path(root) / "feeds" / f"{writer}.jsonl")
    prev = _sha(_canon(prev_rows[-1])) if prev_rows and "_corrupt" not in prev_rows[-1] else "GENESIS"
    row = {"seq": len([r for r in prev_rows if "_corrupt" not in r]),
           "ts": round(time.time(), 3), "writer": writer, "kind": kind, "body": body, "prev": prev}
    row["sig"] = key.sign(_canon(row)).hex()
    with (Path(root) / "feeds" / f"{writer}.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return {"ok": True, "row": row, "hash": _sha(_canon(row)), "schema": SCHEMA}


def verify_feed(root: Path, writer: str) -> dict:
    """Verify signatures + per-feed chain for one writer's log."""
    root = Path(root)
    seedf = root / "feeds" / f"{writer}.key"
    if not seedf.exists():
        return {"ok": False, "error": f"unknown writer {writer}"}
    pub = _keypair(seedf.read_text().strip()).public_key()
    prev, seq, bad = "GENESIS", 0, []
    for i, row in enumerate(_rows(root / "feeds" / f"{writer}.jsonl")):
        if "_corrupt" in row:
            bad.append({"row": i, "why": "unparseable line"})
            continue
        unsigned = {k: row[k] for k in ("seq", "ts", "writer", "kind", "body", "prev")}
        try:
            pub.verify(bytes.fromhex(row.get("sig", "")), _canon(unsigned))
        except Exception as exc:  # bad sig or missing sig - both are forgery-class
            bad.append({"row": i, "why": f"signature: {type(exc).__name__}"})
            continue
        if row["seq"] != seq or row["prev"] != prev:
            bad.append({"row": i, "why": f"chain: seq {row['seq']}!={seq} or prev break"})
        prev, seq = _sha(_canon(row)), row["seq"] + 1
    return {"ok": not bad, "writer": writer, "rows": seq, "violations": bad, "schema": SCHEMA}


def feed_tip(root: Path, writer: str) -> str | None:
    rows = _rows(Path(root) / "feeds" / f"{writer}.jsonl")
    return _sha(_canon(rows[-1])) if rows and "_corrupt" not in rows[-1] else None


def room_view(root: Path, verify: bool = True) -> dict:
    """THE ROOM: merged ordered view across all feeds (the salon's fix: room.jsonl
    is derived, never the write surface)."""
    root = Path(root)
    rows, violations = [], []
    for keyf in sorted((root / "feeds").glob("*.key")):
        writer = keyf.stem
        if verify:
            v = verify_feed(root, writer)
            violations += [dict(x, writer=writer) for x in v["violations"]]
        rows += [r for r in _rows(root / "feeds" / f"{writer}.jsonl") if "_corrupt" not in r]
    rows.sort(key=lambda r: (r.get("ts", 0), r.get("writer", ""), r.get("seq", 0)))
    return {"ok": not violations, "rows": rows, "violations": violations, "schema": SCHEMA}
