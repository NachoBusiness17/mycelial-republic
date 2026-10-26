"""B2-388 falsifier probe: the usage_digest amend arm rewrites chain rows
and leaves the tip root behind.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_388_falsifier_probe.py

Sandbox: tmp dirs only; mag.usage_digest module names are monkeypatched, the
real memory/biography bytes are never touched. Disclosure: _verify_chain_consistent
is stubbed (True) so the probe exercises ONLY the amend/tip interaction, not
the integrity gate; _load_chain_rows is rebound to read the sandbox chain.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from mag import usage_digest as ud  # noqa: E402
from mag.verkle_knot import _h, _leaf_hash, _merkle_prefix_roots  # noqa: E402


def make_row(leaf_obj: dict, i: int, prefix_roots: list[str]) -> dict:
    parent = prefix_roots[i - 1] if i else _h(b"empty")
    return {
        "ts": leaf_obj["ts"],
        "filename": leaf_obj["filename"],
        "leaf_hash": leaf_obj["leaf_hash"],
        "session_id": leaf_obj["session_id"],
        "index": i,
        "n_leaves": i + 1,
        "parent_verkle_root": parent,
        "verkle_root": prefix_roots[i],
        "amended": False,
    }


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="b2_388_"))
    chain = tmp / "verkle_chain.jsonl"
    tip = tmp / "verkle_tip.json"
    knots = tmp / "knots"
    source = tmp / "provider_usage.jsonl"
    source.write_text(
        json.dumps({"ts": "2026-09-26T10:00:00Z", "provider": "p", "model": "m",
                    "ok": True, "cost": 0.1, "prompt_tokens": 1,
                    "completion_tokens": 1, "cache_hit_tokens": 0,
                    "cache_miss_tokens": 2, "meta": {"key_env": "K"}}) + "\n",
        encoding="utf-8")

    # seed the sandbox chain with one prior leaf so the digest appends/amends
    # onto a non-empty consistent chain
    prior_leaf = {"type": "seed", "ts": "2026-09-25T00:00:00Z", "n": 1}
    prior_leaf["leaf_hash"] = _leaf_hash(prior_leaf)
    hashes = [prior_leaf["leaf_hash"]]
    proots = _merkle_prefix_roots(hashes)
    row0 = make_row({**prior_leaf, "filename": "seed.json",
                     "session_id": "seed-1"}, 0, proots)
    chain.write_text(json.dumps(row0) + "\n", encoding="utf-8")
    tip.write_text(json.dumps({"schema": "verkle_tip.v1",
                               "root": row0["verkle_root"],
                               "n_leaves": 1}), encoding="utf-8")

    # patch the module surface onto the sandbox
    def sandbox_load_rows():
        return [json.loads(l) for l in chain.read_text(encoding="utf-8").splitlines() if l.strip()]

    ud.CHAIN = chain
    ud.TIP = tip
    ud.KNOTS = knots
    ud.BIO = tmp
    ud.SOURCE = source
    ud._load_chain_rows = sandbox_load_rows
    ud._verify_chain_consistent = lambda: (True, "sandbox")
    # INCIDENT SCAR TISSUE (2026-09-26): the first probe run patched only the
    # mag.usage_digest names, so the amend arm's _rewrite_chain_unlocked ->
    # mag.verkle_knot._rewrite_chain wrote to the REAL CHAIN and the tip write
    # hit the REAL TIP (the probe reproduced the disease on the estate; the
    # 9,890-row chain fell back to the knotnight-0912 snapshot). Both
    # verkle_knot globals are now sandboxed too, so the probe is hermetic.
    from mag import verkle_knot as vk
    vk.CHAIN = chain
    vk.TIP = tip
    vk.KNOTS = knots
    vk.BIO = tmp

    out: dict = {"sandbox": str(tmp)}

    # arm 1: first commit = pure append (healthy path)
    r1 = ud.commit_day("2026-09-26")
    out["append_ok"] = r1.get("ok")
    out["append_root"] = (r1.get("verkle_root") or "")[:12]
    tip_after_append = json.loads(tip.read_text(encoding="utf-8"))
    out["tip_root_after_append"] = str(tip_after_append.get("root"))[:12]

    # arm 2: change the day's bytes, recommit -> same session id -> AMEND arm
    source.write_text(source.read_text(encoding="utf-8") +
                      json.dumps({"ts": "2026-09-26T11:00:00Z", "provider": "p",
                                  "model": "m", "ok": False, "cost": 0.0,
                                  "prompt_tokens": 1, "completion_tokens": 0,
                                  "cache_hit_tokens": 0, "cache_miss_tokens": 0,
                                  "meta": {"key_env": "K"}}) + "\n",
                      encoding="utf-8")
    chain_before = chain.read_text(encoding="utf-8")
    tip_before = tip.read_text(encoding="utf-8")
    try:
        r2 = ud.commit_day("2026-09-26")
        out["amend_result"] = {k: r2.get(k) for k in ("ok", "error", "amended", "verkle_root")}
        out["amend_exception"] = None
    except Exception as exc:  # the NameError class is the expected pre-fix shape
        out["amend_exception"] = f"{type(exc).__name__}: {exc}"
        r2 = None
    chain_after = chain.read_text(encoding="utf-8")
    tip_after = tip.read_text(encoding="utf-8")

    out["chain_rows_rewritten"] = chain_after != chain_before
    out["tip_moved"] = tip_after != tip_before
    # the disease: chain bytes moved while the tip root stayed behind
    out["stale_tip_state"] = bool(out["chain_rows_rewritten"] and not out["tip_moved"])
    if r2 and r2.get("ok"):
        # healthy arm: recompute and compare
        rows = sandbox_load_rows()
        recomputed = _merkle_prefix_roots([r["leaf_hash"] for r in rows if r.get("leaf_hash")])[-1]
        out["tip_matches_recomputed"] = json.loads(tip_after)["root"] == recomputed

    print(json.dumps(out, indent=2))
    (Path(__file__).parent / "B2_388_falsifier_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
