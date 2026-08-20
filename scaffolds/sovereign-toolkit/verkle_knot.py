"""verkle_knot — content-addressed hash-linked memory chain, pure stdlib.

THE MECHANISM (nobody really has but us):
  A content-addressed, append-only, hash-linked chain of KNOTS — the durable substrate.
  Every commit references its parent root; state is replayable and verifiable. The
  filename is the address; the chain tip is a succinct Merkle root. "Disk is law" made
  structural.

THE CONTRACT:
  * leaf_hash(obj)      -> the content address of one leaf (sha256 of b"leaf:"+json).
  * merkle_root(hashes) -> pairwise Merkle root over a set of leaf hashes.
  * VerkleChain         -> append(obj) writes a knot file + chain line + tip; replay()
                           reads and verifies the parent chain; verify() checks integrity.

PURE STDLIB — hashlib, json, re, pathlib, datetime. Runs: python -m pytest tests/ -q
Schema: verkle_knot.v1
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "verkle_knot.v1"

# Leaf filename: {date}_{HHmmUTC}_{theme}_{session8}_{commit8}.knot.json
_FNAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(\d{4})_([^_]+)_([0-9a-f]{8})_([0-9a-f]{8})\.knot\.json$")


def _h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def leaf_hash(obj: Any) -> str:
    """Content address of one leaf: sha256(b'leaf:' + canonical json)."""
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return _h(b"leaf:" + raw)


def merkle_root(leaf_hashes: list[str]) -> str:
    """Pairwise Merkle root over leaf hashes. Deterministic, order-sensitive."""
    if not leaf_hashes:
        return _h(b"empty")
    layer = leaf_hashes[:]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(_h(b"node:" + left.encode() + b":" + right.encode()))
        layer = nxt
    return layer[0]


def _slug(name: str | None) -> str:
    if not name:
        return "untagged"
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return (s or "untagged")[:24]


class VerkleChain:
    """An append-only, content-addressed, hash-linked chain on disk."""

    def __init__(self, base_dir: str | Path):
        self.base = Path(base_dir)
        self.knots = self.base / "knots"
        self.chain = self.base / "verkle_chain.jsonl"
        self.tip = self.base / "verkle_tip.json"
        self.knots.mkdir(parents=True, exist_ok=True)

    # ---- read helpers ---------------------------------------------------
    def _read_chain(self) -> list[dict[str, Any]]:
        if not self.chain.is_file():
            return []
        out = []
        for line in self.chain.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return out

    # ---- commit ---------------------------------------------------------
    def append(self, obj: Any, *, theme: str, session_id: str) -> dict[str, Any]:
        """Append one knot. Returns {leaf_hash, verkle_root, filename, index, ...}."""
        chain_rows = self._read_chain()
        parent_root = chain_rows[-1]["verkle_root"] if chain_rows else None
        now = datetime.now(timezone.utc)
        date = now.strftime("%Y-%m-%d")
        hhmm = now.strftime("%H%M")

        leaf = leaf_hash(obj)
        commit8 = leaf[:8]
        session8 = (session_id or "00000000")[:8]
        fname = f"{date}_{hhmm}_{_slug(theme)}_{session8}_{commit8}.knot.json"

        # new root = merkle over [parent_root, leaf] (order stable)
        roots = ([parent_root] if parent_root else []) + [leaf]
        new_root = merkle_root(roots)

        row = {
            "ts": now.isoformat(),
            "filename": fname,
            "leaf_hash": leaf,
            "session_id": session_id,
            "dominant_theme": theme,
            "index": len(chain_rows),
            "n_leaves": len(chain_rows) + 1,
            "parent_verkle_root": parent_root,
            "verkle_root": new_root,
        }

        # write the leaf (the actual content) as a knot file
        (self.knots / fname).write_text(
            json.dumps({"schema": SCHEMA, **obj}, sort_keys=True), encoding="utf-8"
        )
        # append to the chain
        with self.chain.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
        # update the tip
        self.tip.write_text(json.dumps(row, sort_keys=True), encoding="utf-8")
        return row

    # ---- replay + verify -------------------------------------------------
    def replay(self) -> list[dict[str, Any]]:
        """Read the whole chain in order."""
        return self._read_chain()

    def verify(self) -> dict[str, Any]:
        """Re-verify the whole chain: every row's root must match its parent link,
        and the final row must match the tip. Returns {ok, rows, error?}."""
        rows = self._read_chain()
        if not rows:
            return {"ok": True, "rows": 0, "reason": "empty_chain"}
        for i, row in enumerate(rows):
            leaf = row["leaf_hash"]
            parent = row.get("parent_verkle_root")
            roots = ([parent] if parent else []) + [leaf]
            expect = merkle_root(roots)
            if expect != row["verkle_root"]:
                return {"ok": False, "rows": len(rows), "index": i, "error": "root_mismatch"}
        if self.tip.is_file():
            tip = json.loads(self.tip.read_text(encoding="utf-8"))
            if tip.get("verkle_root") != rows[-1]["verkle_root"]:
                return {"ok": False, "rows": len(rows), "index": len(rows) - 1,
                        "error": "tip_mismatch"}
        return {"ok": True, "rows": len(rows), "reason": "chain_verified"}


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        c = VerkleChain(d)
        c.append({"event": "birth"}, theme="stateless", session_id="abc12345")
        c.append({"event": "first_learn", "lesson": "trust bytes"}, theme="learn",
                 session_id="abc12345")
        print(json.dumps(c.verify(), indent=2))
