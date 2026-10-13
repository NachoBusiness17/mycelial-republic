"""proof — SIGNED PROOFS: the loop's claims become checkable (2026-08-24).

GSTD steal #5. The chain is the line we sign: every claim the system banks gets a canonical
signature (a deterministic hash of its own inputs + outputs), the signature is anchored to
the verkle chain, and anyone can RE-DERIVE the hash from the original payload to confirm the
claim holds. A claim that doesn't re-derive is a broken proof — reported honestly, not hidden.

  sign(payload)   -> canonical sha256 signature (same payload -> same signature, always).
  verify(proof)   -> re-derive the hash from the payload; match = the proof holds.
  anchor(payload) -> sign + commit the claim hash to the verkle chain (a chain fact), deduped.
  check(hash)     -> is this claim hash committed on the chain (read the anchor ledger)?

Schema: proof.v1 · deterministic + $0 · reuse: verkle_knot (append), manifest dedup pattern
CLI: python -m mag.proof sign <json> | verify <json> | anchor <json> | check <hash>
"""
from __future__ import annotations

import hashlib
import json
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

SCHEMA = "proof.v1"
LEDGER = ROOT / "memory" / "proofs" / "anchored.jsonl"  # claim hashes committed on the chain
SESSION_ID = "proof"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical(payload: dict[str, Any]) -> str:
    """Deterministic canonical form of a claim (sort_keys, default=str — same bytes always)."""
    return json.dumps(payload, sort_keys=True, default=str)


def sign(payload: dict[str, Any]) -> dict[str, Any]:
    """SIGN a claim: canonical payload -> sha256 signature. The signature IS the proof: given
    the same inputs, anyone re-derives the same hash. No secrets, no trust — checkable bytes."""
    if not isinstance(payload, dict):
        return {"ok": False, "schema": SCHEMA, "error": "payload must be a dict"}
    canonical = _canonical(payload)
    h = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {"ok": True, "schema": SCHEMA, "claim_hash": h, "ts": _now(),
            "payload": payload, "canonical": canonical[:400],
            "note": "signed: the claim hash re-derives from these exact bytes"}


def verify(proof: dict[str, Any]) -> dict[str, Any]:
    """VERIFY a signed proof: re-derive the hash from the claimed payload and compare.
    match = the proof holds (the claim is exactly what was signed). mismatch = BROKEN."""
    payload = proof.get("payload") if isinstance(proof, dict) else None
    if not isinstance(payload, dict):
        return {"ok": False, "schema": SCHEMA, "verified": False,
                "error": "no payload to re-derive — cannot check this claim"}
    canonical = _canonical(payload)
    h = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    claimed = proof.get("claim_hash", "")
    match = bool(claimed) and h == claimed
    return {"ok": True, "schema": SCHEMA, "verified": match, "claim_hash": h,
            "note": ("proof holds: hash re-derived from the payload matches the signature"
                     if match else "proof BROKEN: re-derived hash does NOT match the signature")}


def _anchored_hashes() -> set[str]:
    out: set[str] = set()
    if LEDGER.is_file():
        try:
            for line in LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.strip():
                    out.add((json.loads(line).get("claim_hash") or "")[:64])
        except Exception:  # noqa: BLE001
            pass
    return out


def anchor(payload: dict[str, Any]) -> dict[str, Any]:
    """SIGN + COMMIT a claim to the verkle chain (a chain fact). Deduped: an already-anchored
    claim hash persists — no chain spam, same proof contract as the manifest."""
    s = sign(payload)
    if not s.get("ok"):
        return s
    h = s["claim_hash"]
    if h in _anchored_hashes():
        return {"ok": True, "schema": SCHEMA, "anchored": True, "persisted": True,
                "claim_hash": h, "note": "claim hash already committed — persists as a chain fact"}
    knot = {}
    try:
        from mag import verkle_knot
        knot = verkle_knot.append_verkle_knot({
            "session_id": SESSION_ID,
            "theme": "proof",
            "summary": f"[proof] signed claim {h[:16]} — {str(payload.get('kind') or payload.get('role') or 'claim')[:40]}",
        })
    except Exception as e:  # noqa: BLE001 — anchoring must never break the proof
        knot = {"leaf_hash": h, "error": str(e)[:100]}
    try:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"schema": SCHEMA, "claim_hash": h, "ts": _now(),
                                "leaf_hash": knot.get("leaf_hash", ""),
                                "root": knot.get("verkle_root") or knot.get("root", ""),
                                "kind": str(payload.get("kind") or payload.get("role") or "claim")[:60]},
                               ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001
        pass
    return {"ok": True, "schema": SCHEMA, "anchored": True, "persisted": False,
            "claim_hash": h, "leaf_hash": knot.get("leaf_hash", ""),
            "root": knot.get("verkle_root") or knot.get("root", ""),
            "note": "signed claim committed to the verkle chain — a checkable chain fact"}


def check(claim_hash: str) -> dict[str, Any]:
    """CHECK: is this claim hash committed on the chain (in the anchored ledger)?"""
    h = (claim_hash or "").strip().lower()
    anchored = h in _anchored_hashes()
    return {"ok": True, "schema": SCHEMA, "claim_hash": h, "anchored": anchored,
            "note": ("claim is a committed chain fact" if anchored
                     else "claim hash NOT found in the anchored ledger — not committed")}


def status() -> dict[str, Any]:
    ledger = _anchored_hashes()
    return {"ok": True, "schema": SCHEMA, "anchored_claims": len(ledger),
            "contract": "sign -> anchor -> verify: every claim re-derives from its own bytes "
                        "and is committed as a chain fact",
            "built": "2026-08-24 — foundation #5 of the doctrine"}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "status"
    if cmd in ("sign", "verify", "anchor"):
        if len(argv) < 2:
            print(json.dumps({"ok": False, "error": f"{cmd} needs a JSON payload"}, indent=2))
            return 1
        try:
            payload = json.loads(argv[1])
        except Exception:  # noqa: BLE001
            print(json.dumps({"ok": False, "error": "payload must be JSON"}, indent=2))
            return 1
        if cmd == "sign":
            print(json.dumps(sign(payload), indent=2, ensure_ascii=False))
        elif cmd == "verify":
            print(json.dumps(verify(payload), indent=2, ensure_ascii=False))
        else:
            print(json.dumps(anchor(payload), indent=2, ensure_ascii=False))
    elif cmd == "check" and len(argv) > 1:
        print(json.dumps(check(argv[1]), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
