#!/usr/bin/env python3
"""Full read-only recomputation of the operator verkle chain.

READ-ONLY: never writes the chain, tip, knots or pointers. The only write is
the optional receipt (--json) under memory/runs/verkle_full_verify_<ts>.json.

Unlike scripts/verify_verkle_continuity.py (which only checks that each row's
parent_verkle_root equals the previous row's verkle_root), this script:
  * recomputes every knot file's leaf_hash from its body and compares it to
    the chain row (missing knot files are reported as 'dangling', not failures);
  * recomputes the duplicate-last Merkle root of every prefix (verkle_root,
    parent_verkle_root, n_leaves) from the ordered leaf hashes;
  * checks stored linkage and that verkle_tip.json matches the recomputed tail.
Hash rules mirror mag/verkle_knot.py (_h, _leaf_hash, _merkle_root,
_merkle_prefix_roots) and mag/diary_node.py (_leaf_hash, b"diary-leaf:").

Usage: .venv\\Scripts\\python.exe scripts/verify_verkle_full.py [--json] [--limit N]
Exit 0 = no mismatches (dangling allowed), 1 = any mismatch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

# Importing mag.verkle_knot only defines constants/functions (no I/O at import).
from mag.verkle_knot import (  # noqa: E402
    BIO, CHAIN, KNOTS, TIP, _h, _leaf_hash, _merkle_prefix_roots,
)

ATTIC = BIO / "knots_attic"
DIARY_DIR = BIO / "diary_nodes"
DIARY_SCHEMA = "mag_diary_node.v1"  # diary_node.SCHEMA, overwritten in the file
EMPTY = _h(b"empty")


def diary_leaf_hash(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return _h(b"diary-leaf:" + raw)


def naive_root(hs: list[str]) -> str:
    """Independent re-implementation of _merkle_root (cross-check only)."""
    if not hs:
        return EMPTY
    layer = list(hs)
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            l = layer[i]
            r = layer[i + 1] if i + 1 < len(layer) else l
            nxt.append(hashlib.sha256(b"node:" + l.encode() + b":" + r.encode()).hexdigest())
        layer = nxt
    return layer[0]


def is_diary(row: dict, knot: dict | None) -> bool:
    fn = str(row.get("filename") or "")
    return (row.get("leaf_kind") == "diary_node" or fn.endswith(".diary.knot.json")
            or (knot or {}).get("leaf_kind") == "diary_node")


def recompute_leaf(knot: dict, diary: bool) -> tuple[str | None, str]:
    """Return (hash, recipe) of the first recipe that reproduces knot['leaf_hash'],
    else (primary-recipe hash, 'none')."""
    want = knot.get("leaf_hash")
    if diary:
        base = {k: v for k, v in knot.items() if k not in {"leaf_hash", "filename", "type", "leaf_kind"}}
        # diary_node.seal_diary hashed schema=mag_diary_node.v1; the append path
        # later overwrote schema with verkle_knot_leaf.v1 in the file.
        a = dict(base); a["schema"] = DIARY_SCHEMA
        b = {k: v for k, v in base.items() if k != "schema"}
        cands = [("diary:restore_schema", diary_leaf_hash(a)), ("diary:strip_schema", diary_leaf_hash(b))]
    else:
        body = {k: v for k, v in knot.items() if k not in {"leaf_hash", "filename", "pdf_path"}}
        cands = [("session", _leaf_hash(body))]
    for name, h in cands:
        if h == want:
            return h, name
    return cands[0][1], "none"


def load_knot(fn: str):
    for where, d in (("knots", KNOTS), ("attic", ATTIC), ("diary_nodes", DIARY_DIR)):
        p = d / fn
        if p.is_file():
            try:
                return where, json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
                return where, e
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="write receipt to memory/runs/")
    ap.add_argument("--limit", type=int, default=None, help="only the first N chain lines")
    a = ap.parse_args()
    t0 = time.time()

    raw_lines = CHAIN.read_bytes().split(b"\n")
    rows, bad_json = [], 0
    for ln in raw_lines:
        if not ln.strip():
            continue
        try:
            rows.append(json.loads(ln.decode("utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError):
            bad_json += 1
    total_rows = len(rows)
    if a.limit is not None:
        rows = rows[: a.limit]
    hashed = [r for r in rows if r.get("leaf_hash")]
    hs = [str(r["leaf_hash"]) for r in hashed]

    # ---- prefix roots (O(n log n), cross-checked against naive roots) ----
    prefix = _merkle_prefix_roots(hs)
    sample = sorted({len(hs) - 1, 0, *random.Random(7).sample(range(len(hs)), min(40, len(hs)))}) if hs else []
    xcheck_bad = [i for i in sample if naive_root(hs[: i + 1]) != prefix[i]]

    c = dict(leaf_ok=0, leaf_mismatch=0, leaf_file_vs_row_mismatch=0, dangling=0,
             found_in_attic=0, found_in_diary_nodes=0, knot_unreadable=0,
             root_ok=0, root_mismatch=0, parent_ok=0, parent_mismatch=0,
             n_leaves_ok=0, n_leaves_mismatch=0, linkage_ok=0, linkage_break=0)
    recipes: dict[str, int] = {}
    leaf_mm, root_mm, link_mm, dangling_sample = [], [], [], []
    prev_stored = None
    for i, r in enumerate(hashed):
        fn = str(r.get("filename") or "")
        # leaf hash
        where, knot = load_knot(fn) if fn else (None, None)
        if knot is None:
            c["dangling"] += 1
            if len(dangling_sample) < 5:
                dangling_sample.append({"leaf_i": i, "filename": fn})
        elif isinstance(knot, Exception):
            c["knot_unreadable"] += 1
            leaf_mm.append({"leaf_i": i, "filename": fn, "where": where, "error": str(knot)[:120]})
        else:
            if where != "knots":
                c[f"found_in_{where}"] += 1
            h, recipe = recompute_leaf(knot, is_diary(r, knot))
            recipes[recipe] = recipes.get(recipe, 0) + 1
            file_ok = knot.get("leaf_hash") == r["leaf_hash"]
            if not file_ok:
                c["leaf_file_vs_row_mismatch"] += 1
            if h == r["leaf_hash"] and file_ok:
                c["leaf_ok"] += 1
            else:
                c["leaf_mismatch"] += 1
                leaf_mm.append({"leaf_i": i, "filename": fn, "where": where, "row": r["leaf_hash"][:16],
                                "file": str(knot.get("leaf_hash"))[:16], "recomputed": h[:16],
                                "recipe": recipe, "type": knot.get("type")})
        # prefix roots
        exp_root = prefix[i]
        exp_parent = prefix[i - 1] if i else EMPTY
        ok_r = r.get("verkle_root") == exp_root
        ok_p = r.get("parent_verkle_root") == exp_parent
        ok_n = r.get("n_leaves") == i + 1
        c["root_ok" if ok_r else "root_mismatch"] += 1
        c["parent_ok" if ok_p else "parent_mismatch"] += 1
        c["n_leaves_ok" if ok_n else "n_leaves_mismatch"] += 1
        if not (ok_r and ok_p and ok_n):
            root_mm.append({"leaf_i": i, "index": r.get("index"), "filename": fn,
                            "root_ok": ok_r, "parent_ok": ok_p, "n_leaves": r.get("n_leaves"),
                            "expected_n": i + 1, "ts": r.get("ts")})
        # stored linkage (what verify_verkle_continuity checks, but leaf-rows only)
        exp_link = prev_stored if i else EMPTY
        if r.get("parent_verkle_root") == exp_link:
            c["linkage_ok"] += 1
        else:
            c["linkage_break"] += 1
            link_mm.append({"leaf_i": i, "index": r.get("index"), "filename": fn})
        prev_stored = r.get("verkle_root")

    # ---- tip ----
    tip_res: dict = {"checked": False}
    if a.limit is None or a.limit >= total_rows:
        try:
            tip = json.loads(TIP.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            tip = {"_error": str(e)}
        exp_root = prefix[-1] if prefix else EMPTY
        tip_res = {"checked": True,
                   "root_ok": tip.get("root") == exp_root,
                   "n_leaves_ok": tip.get("n_leaves") == len(hs),
                   "last_leaf_hash_ok": tip.get("last_leaf_hash") == (hs[-1] if hs else None),
                   "last_filename_ok": tip.get("last_filename") == (hashed[-1].get("filename") if hashed else None),
                   "tip_root": str(tip.get("root"))[:16], "expected_root": exp_root[:16],
                   "tip_n_leaves": tip.get("n_leaves"), "expected_n_leaves": len(hs)}
        tip_res["ok"] = all(tip_res[k] for k in ("root_ok", "n_leaves_ok", "last_leaf_hash_ok"))

    mismatches = (c["leaf_mismatch"] + c["knot_unreadable"] + c["root_mismatch"] + c["parent_mismatch"]
                  + c["n_leaves_mismatch"] + c["linkage_break"] + len(xcheck_bad) + bad_json
                  + (0 if tip_res.get("ok", True) else 1))
    out = {
        "schema": "verkle_full_verify.v1",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "chain": str(CHAIN.relative_to(REPO)), "limit": a.limit,
        "rows_total": total_rows, "rows_checked": len(rows), "rows_without_leaf_hash": len(rows) - len(hashed),
        "bad_json_lines": bad_json, "leaves": len(hs), "counts": c, "leaf_recipes": recipes,
        "prefix_crosscheck": {"sampled": len(sample), "naive_vs_incremental_mismatch": xcheck_bad},
        "tip": tip_res,
        "first_leaf_mismatches": leaf_mm[:10], "first_root_mismatches": root_mm[:10],
        "first_linkage_breaks": link_mm[:10], "dangling_sample": dangling_sample,
        "ok": mismatches == 0, "runtime_s": round(time.time() - t0, 2),
    }
    print(f"rows={total_rows} checked={len(rows)} no_leaf_hash={out['rows_without_leaf_hash']} leaves={len(hs)} bad_json={bad_json}")
    print(f"leaf_hash: ok={c['leaf_ok']} mismatch={c['leaf_mismatch']} dangling={c['dangling']} "
          f"unreadable={c['knot_unreadable']} (file!=row {c['leaf_file_vs_row_mismatch']}; attic={c['found_in_attic']} diary_nodes={c['found_in_diary_nodes']}) recipes={recipes}")
    print(f"prefix: root ok={c['root_ok']} mm={c['root_mismatch']} | parent ok={c['parent_ok']} mm={c['parent_mismatch']} | "
          f"n_leaves ok={c['n_leaves_ok']} mm={c['n_leaves_mismatch']} | naive xcheck bad={xcheck_bad}")
    print(f"linkage: ok={c['linkage_ok']} break={c['linkage_break']}")
    print(f"tip: {tip_res}")
    for label, lst in (("leaf", leaf_mm), ("root", root_mm), ("linkage", link_mm)):
        for m in lst[:10]:
            print(f"  {label} mismatch: {m}")
    print(f"OK={out['ok']} runtime={out['runtime_s']}s")
    if a.json:
        runs = REPO / "memory" / "runs"
        runs.mkdir(parents=True, exist_ok=True)
        p = runs / f"verkle_full_verify_{datetime.now().strftime('%Y%m%dT%H%M')}.json"
        p.write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"receipt: {p.relative_to(REPO)}")
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
