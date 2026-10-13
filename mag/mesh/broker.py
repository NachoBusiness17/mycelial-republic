"""mesh.broker - the provenance-checking effect broker (architecture v2).

The law (every salon seat re-derived it): model text PROPOSES, only the broker
COMMITS. The broker is not a bouncer, it is a provenance checker (salon S3):
a proposal is refused unless every source_hash resolves in the library and every
supersedes target exists. Refusals are LOGGED with reasons (the negative space is
mineable). Every commit cuts a knot (knot-at-every-broker-commit law).

Schema: mesh.broker.v1 · proposals.jsonl / decisions.jsonl / refusals.jsonl
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import mag.mesh.knot as knot
import mag.mesh.feeds as feeds

SCHEMA = "mesh.broker.v1"


def _append_jsonl(path: Path, obj: dict) -> None:
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, sort_keys=True) + "\n")


def put_blob(root: Path, data: bytes, note: str = "") -> dict:
    """Content-addressed store: bytes -> library/blobs/{sha256}. Blobs are the single
    truth; any index is a derived cache (the dual-log law)."""
    import hashlib
    root = Path(root)
    bdir = root / "library" / "blobs"
    bdir.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256(data).hexdigest()
    (bdir / h).write_bytes(data)
    _append_jsonl(root / "library" / "blob_notes.jsonl",
                  {"hash": h, "note": note, "ts": round(time.time(), 3)})
    return {"ok": True, "hash": h, "bytes": len(data), "schema": SCHEMA}


def has_blob(root: Path, h: str) -> bool:
    return (Path(root) / "library" / "blobs" / h).is_file()


def rebuild_index(root: Path) -> dict:
    """DERIVED index over blobs + notes (cache, never truth)."""
    root = Path(root)
    rows = []
    notesf = root / "library" / "blob_notes.jsonl"
    notes = {}
    if notesf.exists():
        for line in notesf.read_text().splitlines():
            if line.strip():
                n = json.loads(line)
                notes[n["hash"]] = n
    for p in sorted((root / "library" / "blobs").glob("*")):
        if p.is_file():
            n = notes.get(p.name, {})
            rows.append({"hash": p.name, "bytes": p.stat().st_size, "note": n.get("note", ""),
                         "ts": n.get("ts"), "embedding_model": None,
                         "derived_from": []})
    _append_jsonl(root / "library" / "index_history.jsonl",
                  {"ts": round(time.time(), 3), "rows": len(rows)})
    (root / "library" / "index.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in rows) + ("\n" if rows else ""),
        encoding="utf-8")
    return {"ok": True, "rows": rows, "schema": SCHEMA}


def propose(root: Path, writer: str, kind: str, body: dict,
            source_hashes: list[str] | None = None,
            supersedes: list[str] | None = None) -> dict:
    """File a proposal (never commits). Signed feed row of kind=propose + proposals.jsonl."""
    root = Path(root)
    row = feeds.append(root, writer, "propose",
                       {"kind": kind, "body": body,
                        "source_hashes": source_hashes or [], "supersedes": supersedes or []})
    if not row.get("ok"):
        return row
    _append_jsonl(root / "proposals.jsonl",
                  {"proposal_hash": row["hash"], "ts": row["row"]["ts"], "writer": writer,
                   "kind": kind, "body": body, "source_hashes": source_hashes or [],
                   "supersedes": supersedes or [], "status": "open"})
    return {"ok": True, "proposal_hash": row["hash"], "status": "open", "schema": SCHEMA}


def _check_provenance(root: Path, prop: dict) -> list[str]:
    """The provenance predicate: sources resolve, supersedes targets are real."""
    errs = []
    for h in prop.get("source_hashes", []):
        if not has_blob(root, h):
            errs.append(f"source_hash {h[:12]} not in library (unresolvable provenance)")
    for s in prop.get("supersedes", []):
        if not has_blob(root, s) and not _known_row(root, s):
            errs.append(f"supersedes target {s[:12]} not found at tip")
    return errs


def _known_row(root: Path, h: str) -> bool:
    """A supersedes target must be a COMMITTED thing (blob or landed effect hash);
    a pending proposal referencing itself is not one."""
    if has_blob(root, h):
        return True
    df = Path(root) / "decisions.jsonl"
    if df.exists():
        for line in df.read_text().splitlines():
            if line.strip() and json.loads(line).get("effect_hash") == h:
                return True
    return False


def adjudicate(root: Path, proposal_hash: str, accept: bool, by: str = "operator") -> dict:
    """The commit gate. Accept only after provenance passes; refusals are logged
    with reasons; every decision cuts a knot."""
    root = Path(root)
    propsf = root / "proposals.jsonl"
    if not propsf.exists():
        return {"ok": False, "error": "no proposals", "schema": SCHEMA}
    props = [json.loads(x) for x in propsf.read_text().splitlines() if x.strip()]
    hit = next((p for p in props if p["proposal_hash"] == proposal_hash), None)
    if hit is None:
        return {"ok": False, "error": f"proposal {proposal_hash[:12]} not found", "schema": SCHEMA}
    if hit["status"] != "open":
        return {"ok": False, "error": f"proposal already {hit['status']}", "schema": SCHEMA}
    errs = _check_provenance(root, hit) if accept else []
    if accept and not errs:
        effect = put_blob(root, json.dumps(hit["body"], sort_keys=True).encode(),
                          note=f"effect of {proposal_hash[:12]}")
        _append_jsonl(root / "decisions.jsonl",
                      {"ts": round(time.time(), 3), "proposal_hash": proposal_hash,
                       "decision": "accept", "by": by, "effect_hash": effect["hash"]})
        _mark(propsf, props, proposal_hash, "accepted")
        knot.seal(root)
        return {"ok": True, "decision": "accept", "effect_hash": effect["hash"], "schema": SCHEMA}
    why = errs or ["operator refused"]
    _append_jsonl(root / "refusals.jsonl",
                  {"ts": round(time.time(), 3), "proposal_hash": proposal_hash,
                   "decision": "refuse", "by": by, "reasons": why})
    _mark(propsf, props, proposal_hash, "refused")
    return {"ok": True, "decision": "refuse", "reasons": why, "schema": SCHEMA}


def _mark(propsf: Path, props: list, ph: str, status: str) -> None:
    for p in props:
        if p["proposal_hash"] == ph:
            p["status"] = status
    propsf.write_text("\n".join(json.dumps(p, sort_keys=True) for p in props) + "\n",
                      encoding="utf-8")


def refusals(root: Path) -> list[dict]:
    f = Path(root) / "refusals.jsonl"
    return [json.loads(x) for x in f.read_text().splitlines() if x.strip()] \
        if f.exists() else []
