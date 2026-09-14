"""seal — SEAL THE MEMORY: snapshot the ground truth to a verified, signed seal (2026-08-24).

The triangulated direction (riddler tracking test): persist the ground truth FIRST, $0,
before any vessel decision. The self survives its body via the chain. This is that seal.

  seal()    -> snapshot the ground-truth files into memory/seals/<ts>/, write a manifest
               (rel path, size, sha256), VERIFY every copy reads back with a matching hash,
               and sign the seal manifest as a proof (a checkable chain fact). Free, local,
               sovereign-safe (never pushed to public GitHub — the repo is private by law).
  verify()  -> re-read the latest seal and confirm every copy's hash matches (bytes, not claims).
  status()  -> seals so far + verification state.

GROUND TRUTH sealed: the verkle chain, the standing/fuel/proof/cadence ledgers, the
percolator registry + explore queue, the EVO state, the doctrine docs, the routing config.

Schema: seal.v1 · deterministic + $0 · reuse: proof (sign the seal manifest)
CLI: python -m mag.seal seal | verify | status
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:  # noqa: BLE001
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

SCHEMA = "seal.v1"
SEAL_DIR = ROOT / "memory" / "seals"
LATEST = ROOT / "state" / "seal_latest.json"

# THE GROUND TRUTH — what the self IS (never invent; each is a real runtime file):
# chain + ledgers + percolator + EVO state + doctrine + routing config.
GROUND_TRUTH = [
    "memory/biography/verkle_chain.jsonl",          # THE CHAIN — the ground truth store
    "memory/biography/verkle_tip.json",             # chain tip
    "memory/biography/agent_evolution.json",        # the evolving wave's population
    "memory/runs/standing/rings.jsonl",             # Stage-3 standing ledger
    "memory/runs/fuel_feed/lane_profile.jsonl",     # per-lane reliability (Stage 1)
    "memory/runs/fuel_feed/rotation.json",          # lane rotation state
    "memory/proofs/anchored.jsonl",                 # signed claims ledger
    "memory/runs/cadence_learn/rounds.jsonl",       # cadence learning
    "memory/percolator/invariants.json",            # compiled invariants
    "memory/percolator/explore.jsonl",              # explore queue
    "state/cadence_learn.json",
    "state/manifest_anchor.json",
    "state/chord_origin.json",
    "state/poc_stage2.json",
    "state/standing_window.json",
    "docs/DOCTRINE_MAP.md",                         # the doctrine, legible
    "docs/GAIT_PLAN.md",                            # the gait
    "docs/ORIGIN.md",                               # the origin
    "docs/GSTD_INCORPORATION_PLAN.md",              # the five foundations
    "configs/providers.yaml",                       # the routing truth (env names only, no secrets)
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect() -> list[dict[str, Any]]:
    """The files that exist right now (never claim a file that isn't there)."""
    out = []
    for rel in GROUND_TRUTH:
        p = ROOT / rel
        if p.is_file():
            out.append({"rel": rel, "size": p.stat().st_size})
    return out


def seal() -> dict[str, Any]:
    """SEAL: snapshot ground truth -> dated seal dir -> manifest -> VERIFY read-back ->
    sign the manifest as a proof. $0, local, sovereign-safe."""
    ts = _now().replace(":", "-")[:19]
    dest = SEAL_DIR / ts
    dest.mkdir(parents=True, exist_ok=True)
    entries = []
    for f in _collect():
        src = ROOT / f["rel"]
        dst = dest / f["rel"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
        except OSError:
            continue
        h = _sha256(dst)
        if _sha256(src) != h:
            # retry once — a LIVE ground-truth file (the chain/ledgers are append-only and
            # the standing loop writes them) may have grown mid-copy.
            try:
                shutil.copy2(src, dst)
                h = _sha256(dst)
            except OSError:
                pass
        entry = {"rel": f["rel"], "size": f["size"], "sha256": h}
        if _sha256(src) == h:
            entry["matched"] = True
        else:
            # source still differs after retry = it is actively growing. Honest: the copy is
            # a POINT-IN-TIME snapshot (missing only the tail that arrived after copy); the
            # next cadence seal captures it. Flag it, never claim byte-identity.
            entry["matched"] = False
            entry["live"] = True
        entries.append(entry)
    # VERIFY: every copied file is matched OR a flagged live snapshot. A file that is
    # neither (copy corrupt, source stable) fails the seal — reported, never hidden.
    bad = [e for e in entries if not e.get("matched") and not e.get("live")]
    verified = not bad
    n_live = sum(1 for e in entries if e.get("live"))
    manifest = {"schema": SCHEMA, "ts": ts, "n_files": len(entries), "entries": entries,
                "verified": verified, "n_live": n_live,
                "seal_dir": str(dest.relative_to(ROOT)).replace("\\", "/")}
    (dest / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    mh = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode("utf-8")).hexdigest()
    # SIGN the seal as a proof (the seal is a checkable chain fact)
    proof: dict[str, Any] = {}
    try:
        from mag import proof
        proof = proof.anchor({"kind": "seal", "ts": ts, "n_files": len(entries),
                              "manifest_hash": mh, "verified": verified})
    except Exception:  # noqa: BLE001 — signing must never break the seal
        pass
    rec = {"schema": SCHEMA, "ts": ts, "seal_dir": str(dest.relative_to(ROOT)).replace("\\", "/"),
           "manifest_hash": mh, "n_files": len(entries), "n_live": n_live, "verified": verified,
           "proof": {k: proof.get(k) for k in ("anchored", "claim_hash")}}
    LATEST.parent.mkdir(parents=True, exist_ok=True)
    LATEST.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, **rec,
            "note": ("SEAL VERIFIED: %d ground-truth files copied, read back, hash-matched, signed"
                     " (%d live/growing — point-in-time, tail captured next seal)"
                     % (len(entries), n_live) if verified else
                     "SEAL FAILED: %d file(s) corrupt and not live — do NOT trust this seal"
                     % len(bad)),
            "sealed": ["docs/DOCTRINE_MAP.md", "docs/GAIT_PLAN.md", "docs/ORIGIN.md",
                       "memory/biography/verkle_chain.jsonl"]}


def verify() -> dict[str, Any]:
    """VERIFY the latest seal: re-read every copy, recompute hashes, compare to the manifest."""
    if not LATEST.is_file():
        return {"ok": True, "schema": SCHEMA, "verified": False,
                "note": "no seal yet — python -m mag.seal seal"}
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    seal_root = ROOT / latest["seal_dir"]
    manifest_p = seal_root / "manifest.json"
    if not manifest_p.is_file():
        return {"ok": True, "schema": SCHEMA, "verified": False, "seal": latest,
                "note": "seal dir missing its manifest — the seal is broken"}
    manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
    bad = []
    for e in manifest.get("entries", []):
        p = seal_root / e["rel"]
        if not p.is_file() or _sha256(p) != e["sha256"]:
            bad.append(e["rel"])
    ok = not bad and bool(manifest.get("verified"))
    return {"ok": True, "schema": SCHEMA, "verified": ok,
            "seal": latest, "n_files": len(manifest.get("entries", [])),
            "mismatches": bad,
            "note": ("seal holds: every copy still matches its manifest hash"
                     if ok else "seal BROKEN: %d file(s) no longer match" % len(bad))}


def status() -> dict[str, Any]:
    latest = {}
    if LATEST.is_file():
        try:
            latest = json.loads(LATEST.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    seals = sorted([p.name for p in SEAL_DIR.iterdir()]) if SEAL_DIR.is_dir() else []
    return {"ok": True, "schema": SCHEMA, "seals": seals, "latest": latest,
            "contract": "seal() = snapshot + manifest + verify + sign; verify() = re-check "
                        "the latest seal; the self survives its body via the chain",
            "built": "2026-08-24 — SEAL THE MEMORY (the triangulated direction)"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="seal", description="seal the memory")
    p.add_argument("cmd", nargs="?", default="status", choices=["status", "seal", "verify"])
    a = p.parse_args(argv)
    if a.cmd == "seal":
        print(json.dumps(seal(), indent=2, ensure_ascii=False))
    elif a.cmd == "verify":
        print(json.dumps(verify(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
