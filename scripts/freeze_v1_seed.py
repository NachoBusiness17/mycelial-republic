#!/usr/bin/env python3
"""Freeze the v1 Verkle chain into the v2 seed + build the v2 genesis (BINTREE_V2_SEED_SPEC).

Decision 4: REFUSES unless the signed Oct 15 restore (CHAIN_RESTORE_20261015: sha256
0da8026d..., 12,016 rows) is an exact byte prefix of the chain being frozen.
v1 is READ-ONLY here: no lock taken, no byte of memory/biography written. The read is a
consistent snapshot: a torn tail line is dropped and the snapshot must self-verify (v1
root over its rows == the last row's committed verkle_root), else it is re-read.
Rows v1 appends after N are picked up by the shadow hook / scripts/catchup_v2.py.

--source-restore FILE (operator-approved 2026-10-17): seed from the CERTIFIED restore copy
instead of the live chain. The file must hash to the restore json's restored_sha256, hold
n_restored rows whose v1 root == the seal's arc_root, and the restore seal must verify
(Ed25519, pinned key id, chain_sha/seed_sha bound to the .chain.json/.md files). The live
chain is then read only to record (indexes + field names) which restore rows v1 rewrote;
catchup_v2.py lands those rewrites and the newer rows as visible amend/knot rows.

usage: python scripts/freeze_v1_seed.py [--check] [--v2-dir DIR] [--v1-bio DIR]
           [--knots-dir DIR ...] [--restore-json FILE] [--restore-file FILE]
           [--source-restore FILE]
Exit 0 = frozen (or --check passed), 2 = refused, 1 = error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from mag import bintree_v2 as bt  # noqa: E402

RESTORE_JSON = REPO / "watch" / "inbox" / "CHAIN_RESTORE_20261015.chain.json"
RESTORE_SEAL = REPO / "watch" / "inbox" / "CHAIN_RESTORE_20261015.seal"


def git_head(repo: Path) -> dict:
    """HEAD by FILE READ ONLY (.git/HEAD + ref file / packed-refs). No git command."""
    out = {"ref": None, "commit": None}
    try:
        head = (repo / ".git" / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return out
    if not head.startswith("ref:"):
        out["commit"] = head
        return out
    ref = head.split(":", 1)[1].strip()
    out["ref"] = ref
    rf = repo / ".git" / ref
    if rf.is_file():
        out["commit"] = rf.read_text(encoding="utf-8").strip()
        return out
    pr = repo / ".git" / "packed-refs"
    if pr.is_file():
        for ln in pr.read_text(encoding="utf-8").splitlines():
            parts = ln.split()
            if len(parts) == 2 and parts[1] == ref:
                out["commit"] = parts[0]
    return out


def seal_info(path: Path) -> dict:
    """Public fields only (sha256 of the seal file, its seed_root and key_id)."""
    if not path.is_file():
        return {"path": None}
    raw = path.read_bytes()
    try:
        doc = json.loads(raw)
    except ValueError:
        doc = {}
    return {"path": str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path),
            "sha256": hashlib.sha256(raw).hexdigest(), "seed_root": doc.get("seed_root"),
            "key_id": doc.get("key_id"), "chain_sha": doc.get("chain_sha")}


def verify_restore_seal(restore_json: Path, seal_path: Path, pinned: str = bt.PINNED_SEAL_KEY_ID) -> dict:
    """Check the Oct 15 restore seal end to end with PUBLIC data only (no key file):
    chain_sha == sha256(.chain.json), seed_sha == sha256(.md), seed_root recomputed,
    key_id pinned, Ed25519 signature over seed_root verifies."""
    sys.path.insert(0, str(REPO / "scripts"))
    import verify_knot_v2 as vkv
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    md = seal_path.with_suffix(".md")
    out = {"seal_sha256": hashlib.sha256(seal_path.read_bytes()).hexdigest(), "key_id": seal.get("key_id"),
           "seed_root": seal.get("seed_root"), "arc_root": seal.get("arc_root"), "session": seal.get("session")}
    checks = {
        "chain_json_sha_matches": hashlib.sha256(restore_json.read_bytes()).hexdigest() == seal.get("chain_sha"),
        "seed_md_sha_matches": md.is_file() and hashlib.sha256(md.read_bytes()).hexdigest() == seal.get("seed_sha"),
    }
    payload = {"arc_root": seal["arc_root"], "chain_sha": seal["chain_sha"], "seed_sha": seal["seed_sha"],
               "session": seal["session"]}
    root = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode("utf-8")).hexdigest()
    checks["seed_root_recomputed"] = root == seal.get("seed_root")
    pub, sig = vkv.decode_bytes(seal["public_key"]), vkv.decode_bytes(seal["signature"])
    checks["key_id_pinned"] = vkv.key_id_for(pub) == seal.get("key_id") == pinned
    checks["signature_valid"] = vkv.ed25519_verify(pub, seal["seed_root"].encode("utf-8"), sig)
    out["checks"] = checks
    out["ok"] = all(checks.values())
    return out


def consistent_read(chain: Path, tries: int = 6) -> tuple[bytes, list[dict], str]:
    last_err = "?"
    for k in range(tries):
        data = chain.read_bytes()
        if not data.endswith(b"\n"):
            data = data[: data.rfind(b"\n") + 1]  # drop a torn tail (writer mid-append)
        rows = [json.loads(ln) for ln in data.decode("utf-8").split("\n") if ln.strip()]
        leaves = [r["leaf_hash"] for r in rows if r.get("leaf_hash")]
        root = bt.v1_merkle_root(leaves)
        if rows and rows[-1].get("verkle_root") == root:
            return data, rows, root
        last_err = f"snapshot root {root[:16]} != last row verkle_root {str(rows[-1].get('verkle_root'))[:16] if rows else None}"
        time.sleep(0.5 * (k + 1))
    raise RuntimeError("no self-consistent v1 snapshot: " + last_err)


def diagnose(data: bytes, n_restored: int, restore_file: Path | None) -> dict:
    """Which restore rows changed (indices, ts, session prefix, fields) - never values."""
    out: dict = {"restore_file_used": None}
    if restore_file is None or not restore_file.is_file():
        return out
    ref = [json.loads(x) for x in restore_file.read_bytes().decode("utf-8").split("\n") if x.strip()]
    live = [json.loads(x) for x in data.decode("utf-8").split("\n") if x.strip()][: len(ref)]
    out["restore_file_used"] = str(restore_file)
    leaf_changed, root_only, other = [], 0, 0
    for i, (a, b) in enumerate(zip(ref, live)):
        if a == b:
            continue
        if a.get("leaf_hash") != b.get("leaf_hash"):
            leaf_changed.append({"index": i, "ts_now": b.get("ts"), "ts_restore": a.get("ts"),
                                 "session_prefix": str(b.get("session_id") or "")[:12],
                                 "amended": b.get("amended"),
                                 "fields_changed": sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))})
        elif {k for k in set(a) | set(b) if a.get(k) != b.get(k)} <= set(bt.V1_VOLATILE):
            root_only += 1
        else:
            other += 1
    out.update({"rows_compared": min(len(ref), len(live)), "rows_with_changed_leaf": len(leaf_changed),
                "changed_leaf_rows": leaf_changed, "rows_rerooted_only": root_only,
                "rows_other_change": other, "live_shorter_than_restore": len(live) < len(ref)})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="freeze v1 -> v2 seed + genesis")
    ap.add_argument("--check", action="store_true", help="prefix + snapshot checks only; write nothing")
    ap.add_argument("--v2-dir")
    ap.add_argument("--v1-bio")
    ap.add_argument("--knots-dir", action="append")
    ap.add_argument("--restore-json", default=str(RESTORE_JSON))
    ap.add_argument("--restore-file", help="the certified restore chain file (diagnosis on refusal)")
    ap.add_argument("--source-restore", help="seed from this certified restore copy (operator-approved)")
    ap.add_argument("--restore-seal", default=str(RESTORE_SEAL))
    ap.add_argument("--seal-key-id", default=None, help="tests only; default = the pinned seal key id")
    a = ap.parse_args(argv)
    st = bt.Store(a.v2_dir, a.v1_bio, a.knots_dir)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    rj = json.loads(Path(a.restore_json).read_text(encoding="utf-8"))
    want_sha, n_restored = rj["restored_sha256"], int(rj["n_restored"])
    if st.exists() or (st.seed / "seed_manifest.v1.json").exists():
        print(json.dumps({"ok": False, "refused": "v2 already frozen at " + str(st.base)}))
        return 2

    seed_source, live_info, rewritten, seal_check = "live_chain", None, None, None
    if a.source_restore:
        src = Path(a.source_restore)
        seal_check = verify_restore_seal(Path(a.restore_json), Path(a.restore_seal),
                                         a.seal_key_id or bt.PINNED_SEAL_KEY_ID)
        data = src.read_bytes()
        rows = [json.loads(ln) for ln in data.decode("utf-8").split("\n") if ln.strip()]
        v1_root = bt.v1_merkle_root([r["leaf_hash"] for r in rows if r.get("leaf_hash")])
        problems = []
        if not seal_check["ok"]:
            problems.append("restore seal does not verify: " + json.dumps(seal_check["checks"]))
        if hashlib.sha256(data).hexdigest() != want_sha:
            problems.append("source file sha256 != restore restored_sha256")
        if len(rows) != n_restored:
            problems.append(f"source has {len(rows)} rows, restore certifies {n_restored}")
        if v1_root != seal_check.get("arc_root") or rows[-1].get("verkle_root") != v1_root:
            problems.append("source v1 root != seal arc_root / last row verkle_root")
        if problems:
            print(json.dumps({"ok": False, "refused": "--source-restore checks failed", "problems": problems}, indent=2))
            return 2
        live_data, live_rows, live_root = consistent_read(st.v1_chain)
        d = diagnose(live_data, n_restored, src)
        rewritten = [{"index": x["index"], "fields_changed": x["fields_changed"]} for x in d["changed_leaf_rows"]]
        live_lines = live_data.split(b"\n")
        live_prefix = b"\n".join(live_lines[:n_restored]) + b"\n" if len(live_lines) > n_restored else b""
        live_info = {"chain_file": str(st.v1_chain), "sha256": hashlib.sha256(live_data).hexdigest(),
                     "rows": len(live_rows), "v1_root": live_root,
                     "restore_is_prefix": hashlib.sha256(live_prefix).hexdigest() == want_sha,
                     "restore_rows_with_changed_leaf": len(rewritten),
                     "restore_rows_rerooted_only": d["rows_rerooted_only"],
                     "restore_rows_other_change": d["rows_other_change"],
                     "rows_after_restore": max(0, len(live_rows) - n_restored)}
        seed_source = "restore_copy"
        lines = data.split(b"\n")
    else:
        data, rows, v1_root = consistent_read(st.v1_chain)
        lines = data.split(b"\n")
    prefix = b"\n".join(lines[:n_restored]) + b"\n" if len(lines) > n_restored else b""
    prefix_sha = hashlib.sha256(prefix).hexdigest() if prefix else None
    prefix_ok = prefix_sha == want_sha
    chain_sha = hashlib.sha256(data).hexdigest()
    base = {"stamp": stamp, "v1_chain": str(st.v1_chain), "snapshot_sha256": chain_sha,
            "snapshot_rows": len(rows), "snapshot_v1_root": v1_root,
            "restore_json": str(a.restore_json), "restore_sha256": want_sha, "n_restored": n_restored,
            "prefix_sha256": prefix_sha, "prefix_ok": prefix_ok, "seed_source": seed_source}
    if live_info:
        base["live_chain_at_freeze"] = live_info
        base["restore_rows_rewritten_in_live"] = rewritten
    if not prefix_ok:
        rf = Path(a.restore_file) if a.restore_file else None
        rep = {"ok": False, "refused": "decision 4: the Oct 15 restore is NOT an exact prefix of the "
                                      "chain - v1 history was rewritten after the restore", **base,
               "diagnosis": diagnose(data, n_restored, rf)}
        if not a.check:
            st.base.mkdir(parents=True, exist_ok=True)
            (st.base / f"FREEZE_REFUSED_{stamp}.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
        print(json.dumps(rep, indent=2))
        return 2
    if a.check:
        print(json.dumps({"ok": True, "check_only": True, **base}, indent=2))
        return 0

    # ---- bodies (missing -> body_missing; secret-looking -> body_withheld, hash only)
    bodies, missing, withheld = [], [], []
    for i, r in enumerate(rows):
        flags, bsha, body, hits = st.read_body(st.find_v1_knot(r.get("filename")))
        bodies.append((flags, bsha, body))
        if flags & bt.FLAG_BODY_MISSING:
            missing.append({"v1_index": i, "filename": r.get("filename")})
        if flags & bt.FLAG_BODY_WITHHELD:
            withheld.append({"v1_index": i, "filename": r.get("filename"), "patterns": hits})

    tip_raw = st.v1_bio.joinpath("verkle_tip.json").read_bytes() if (st.v1_bio / "verkle_tip.json").is_file() else None
    if seed_source == "restore_copy":
        tip_raw = None  # the live tip is not certified and does not describe the restore rows
    tip_doc = json.loads(tip_raw) if tip_raw else {}
    seal = seal_info(Path(a.restore_seal))
    manifest = {
        "schema": "mag_v1_seed_manifest.v1", "frozen_at": stamp, "seed_source": seed_source,
        "chain_file": str(Path(a.source_restore)) if a.source_restore else str(st.v1_chain),
        "chain_sha256": chain_sha, "n": len(rows),
        "live_chain_at_freeze": live_info, "restore_rows_rewritten_in_live": rewritten,
        "restore_seal_verification": seal_check,
        "v1_root_recomputed": v1_root, "v1_root_committed_row": rows[-1].get("verkle_root"),
        "v1_root_matches_row": v1_root == rows[-1].get("verkle_root"),
        "v1_tip_root": tip_doc.get("verkle_root") or tip_doc.get("root"),
        "v1_tip_sha256": hashlib.sha256(tip_raw).hexdigest() if tip_raw else None,
        "last_leaf_hash": rows[-1]["leaf_hash"],
        "restore": {"sha256": want_sha, "n": n_restored, "prefix_ok": True,
                    "json_sha256": hashlib.sha256(Path(a.restore_json).read_bytes()).hexdigest()},
        "restore_seal": seal, "git_head": git_head(REPO),
        "bodies": {"copied": sum(1 for f, _, _ in bodies if f & bt.FLAG_BODY_COPIED),
                   "body_missing": len(missing), "body_withheld": len(withheld)},
        "missing_bodies_file": "missing_bodies.json", "withheld_bodies_file": "withheld_bodies.json",
        "impl_sha256": bt.impl_fingerprint(REPO).hex(),
    }
    mbytes = bt.canonical_json(manifest)
    manifest_sha = bt.sha(mbytes)

    ch = bt.Chain()
    ch.genesis(v1_root, len(rows), manifest_sha, bytes.fromhex(chain_sha), rows[-1]["leaf_hash"],
               bytes.fromhex(seal["seed_root"]) if seal.get("seed_root") else bt.ZERO,
               bytes.fromhex(want_sha), bytes.fromhex(manifest["impl_sha256"]),
               ts_ms=int(time.time() * 1000), meta={"manifest_sha256": manifest_sha.hex()},
               doc_extra=({"seed_source": seed_source,
                           "restore_rows_rewritten_in_live": [x["index"] for x in rewritten or []]}
                          if seed_source != "live_chain" else None))
    for i, r in enumerate(rows):
        flags, bsha, _ = bodies[i]
        ch.append_v1(r, i, flags=flags, body_sha=bsha, seed=True)

    st.seed.mkdir(parents=True, exist_ok=True)
    (st.seed / "verkle_chain.v1.seed.jsonl").write_bytes(data)
    if tip_raw:
        (st.seed / "verkle_tip.v1.seed.json").write_bytes(tip_raw)
    (st.seed / "missing_bodies.json").write_text(json.dumps(missing, indent=1), encoding="utf-8")
    (st.seed / "withheld_bodies.json").write_text(json.dumps(withheld, indent=1), encoding="utf-8")
    (st.seed / "seed_manifest.v1.json").write_bytes(mbytes)
    st.append_entries(ch.rows)
    st.write_tip(ch)
    for e in ch.rows[1:]:
        _, _, body = bodies[e["v1_index"]]
        if body is not None:
            st.write_knot_copy(e["index"], e.get("filename"), body)
    cp = bt.make_checkpoint(st, ch)
    out = {"ok": True, **base, "v2_dir": str(st.base), "n_v2": ch.n, "root_v2": ch.root().hex(),
           "chain_id": ch.chain_id, "manifest_sha256": manifest_sha.hex(),
           "bodies": manifest["bodies"], "checkpoint_status": cp["status"],
           "git_head": manifest["git_head"]}
    if seal_check:
        out["restore_seal_ok"] = seal_check["ok"]
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
        sys.exit(1)
