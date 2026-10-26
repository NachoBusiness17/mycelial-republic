#!/usr/bin/env python3
"""chain_fork_rehydrate - build a parallel fork chain in %TEMP% by rehydrating rows from knot files.

Ponytail reuse (dated, verified at HEAD 2026-10-20):
  - scripts/verify_verkle_full.py (2026-10-03): read-only leaf recompute from knots + merkle roots
  - %TEMP%/magrestore build_candidate.py (2026-10-14/15 Option A): candidate chain in TEMP only
  - mag/bintree_v2.shadow_append (2026-10-17): parallel shadow strand, never the live law
  - watch/inbox/CHAIN_RESTORE_20261015.md Option A: lost-window rows re-hashed from knot files

Law for this tool:
  - READ-ONLY on the live chain/tip (never write, never swap, never truncate)
  - Fork output only under %TEMP%/magfork_<date>/ (or --out)
  - Weave = divergence report (which rows differ). Rejoin is operator-only via APPEND
    correction/supersede rows on the live chain later; this tool never rejoins.

Usage:
  .venv/Scripts/python.exe tools/chain_fork_rehydrate.py [--limit N] [--out DIR]
Exit 0 = fork built; leaf mismatches reported but do not rewrite live.
Exit 2 = cannot-run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.verkle_knot import (  # noqa: E402
    BIO, CHAIN, KNOTS, TIP, _h, _leaf_hash, _merkle_prefix_roots,
)

ATTIC = BIO / "knots_attic"
DIARY_DIR = BIO / "diary_nodes"
DIARY_SCHEMA = "mag_diary_node.v1"
EMPTY = _h(b"empty")


def diary_leaf_hash(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return _h(b"diary-leaf:" + raw)


def load_knot(fn: str):
    for where, d in (("knots", KNOTS), ("attic", ATTIC), ("diary_nodes", DIARY_DIR)):
        p = d / fn
        if p.is_file():
            try:
                return where, json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
                return where, e
    return None, None


def is_diary(row: dict, knot: dict | None) -> bool:
    fn = str(row.get("filename") or "")
    return (
        row.get("leaf_kind") == "diary_node"
        or fn.endswith(".diary.knot.json")
        or (knot or {}).get("leaf_kind") == "diary_node"
    )


def recompute_leaf(knot: dict, diary: bool) -> tuple[str, str]:
    want = knot.get("leaf_hash")
    if diary:
        base = {k: v for k, v in knot.items() if k not in {"leaf_hash", "filename", "type", "leaf_kind"}}
        a = dict(base)
        a["schema"] = DIARY_SCHEMA
        b = {k: v for k, v in base.items() if k != "schema"}
        cands = [("diary:restore_schema", diary_leaf_hash(a)), ("diary:strip_schema", diary_leaf_hash(b))]
    else:
        body = {k: v for k, v in knot.items() if k not in {"leaf_hash", "filename", "pdf_path"}}
        cands = [("session", _leaf_hash(body))]
    for name, h in cands:
        if h == want:
            return h, name
    return cands[0][1], "none"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=0, help="only first N rows (0=all)")
    ap.add_argument("--out", type=str, default="", help="fork dir (default %%TEMP%%/magfork_YYYYMMDD)")
    args = ap.parse_args()
    if not CHAIN.is_file():
        print("FORK-REHYDRATE: cannot-run missing live chain")
        return 2
    day = datetime.now().strftime("%Y%m%d")
    out = Path(args.out) if args.out else Path(os.environ.get("TEMP", ".")) / f"magfork_{day}"
    if out.resolve() == CHAIN.parent.resolve() or str(CHAIN).startswith(str(out.resolve())):
        print("FORK-REHYDRATE: refuse out path that collides with live biography")
        return 2
    out.mkdir(parents=True, exist_ok=True)
    live_rows = [json.loads(l) for l in CHAIN.read_bytes().split(b"\n") if l.strip()]
    if args.limit and args.limit > 0:
        live_rows = live_rows[: args.limit]
    fork_rows = []
    divergences = []
    dangling = 0
    leaf_ok = 0
    for i, row in enumerate(live_rows):
        fn = str(row.get("filename") or "")
        live_leaf = str(row.get("leaf_hash") or "")
        where, knot = load_knot(fn) if fn else (None, None)
        fork = {
            "index": i,
            "filename": fn,
            "session_id": row.get("session_id"),
            "live_leaf_hash": live_leaf,
            "fork_source": where,
            "amended": bool(row.get("amended")),
        }
        if knot is None or isinstance(knot, Exception):
            dangling += 1
            fork["leaf_hash"] = live_leaf
            fork["rehydrate"] = "dangling_kept_live_leaf"
            if isinstance(knot, Exception):
                fork["knot_error"] = type(knot).__name__
        else:
            diary = is_diary(row, knot)
            h, recipe = recompute_leaf(knot, diary)
            # Prefer knot-stored leaf when recipes match; else recomputed
            fork_leaf = str(knot.get("leaf_hash") or h)
            fork["leaf_hash"] = fork_leaf
            fork["rehydrate"] = recipe
            fork["knot_leaf_hash"] = str(knot.get("leaf_hash") or "")
            if live_leaf and fork_leaf and live_leaf != fork_leaf:
                divergences.append({
                    "index": i,
                    "filename": fn,
                    "session_id": row.get("session_id"),
                    "live_leaf": live_leaf[:16],
                    "fork_leaf": fork_leaf[:16],
                    "source": where,
                    "amended": bool(row.get("amended")),
                    "writer_hint": "amended_row" if row.get("amended") else "unknown",
                })
            elif live_leaf == fork_leaf:
                leaf_ok += 1
        fork_rows.append(fork)

    hs = [str(r["leaf_hash"]) for r in fork_rows if r.get("leaf_hash")]
    roots = _merkle_prefix_roots(hs) if hs else []
    # Write fork chain (TEMP only): one jsonl row per live row with fork merkle
    chain_path = out / "verkle_chain.fork.jsonl"
    with chain_path.open("w", encoding="utf-8", newline="\n") as f:
        hi = 0
        for r in fork_rows:
            if r.get("leaf_hash"):
                r["verkle_root"] = roots[hi]
                r["parent_verkle_root"] = roots[hi - 1] if hi else EMPTY
                r["n_leaves"] = hi + 1
                hi += 1
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tip = {
        "schema": "verkle_tip.fork.v1",
        "root": roots[-1] if roots else EMPTY,
        "n_leaves": len(hs),
        "note": "fork rehydrate; never swap onto live; weave=divergence report only",
        "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "live_chain_sha256": hashlib.sha256(CHAIN.read_bytes()).hexdigest(),
    }
    (out / "verkle_tip.fork.json").write_text(json.dumps(tip, indent=2) + "\n", encoding="utf-8")
    report = {
        "schema": "chain_fork_weave.v1",
        "ts": tip["built_utc"],
        "live_rows": len(live_rows),
        "fork_rows": len(fork_rows),
        "leaf_ok": leaf_ok,
        "dangling": dangling,
        "divergences": len(divergences),
        "divergence_sample": divergences[:50],
        "out": str(out),
        "law": "main chain untouched; rejoin only by append correction/supersede rows",
    }
    (out / "divergence.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"FORK-REHYDRATE: rows={len(live_rows)} leaf_ok={leaf_ok} dangling={dangling} "
        f"divergences={len(divergences)} out={out}"
    )
    print(f"FORK-REHYDRATE: fork_root={(roots[-1][:16] if roots else EMPTY[:16])} "
          f"live_tip_root={json.loads(TIP.read_text(encoding='utf-8')).get('root','')[:16] if TIP.is_file() else 'missing'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
