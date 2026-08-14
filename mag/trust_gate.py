"""trust_gate — the SANITY SYSTEM: only NOVEL, DEDUPED, HIGH-TRUST data writes to the chain,
not poison. Sits in front of the swarm tools (verkle_write, memlance fold, corpus ingest).

Operator (2026-08-12): "how can we have some sanity system around this so it's only novel deduped
high trust data and not poisoning?"

THE GATE (deterministic + $0, three checks before anything writes):
  1. NOVELTY  — dedupe by invariant (canonical content-hash). Already-seen = REJECT (duplicate
                spam is the #1 poisoning vector in a terabyte corpus).
  2. TRUST    — score provenance: source reputation (operator=1.0, frontier/grok=0.8,
                swarm-worker=0.6, unknown=0.3) + groundedness (real bytes present, not fabricated)
                + doctrine alignment (resonates with our mounted RIBs).
  3. POISON   — heuristics: low entropy (repetitive spam), fabrication markers, forbidden
                patterns, anomaly. Suspicious = QUARANTINE, never auto-write.
  VERDICT: ACCEPT (novel + high-trust + clean) -> write; QUARANTINE (suspicious) -> hold for
           review, do NOT auto-write; REJECT (duplicate / low-trust / poison) -> drop.

Schema: trust_gate.v1 · reuse: percolator (dedupe), rib_bus (doctrine), ghost_leak_detector
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
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "trust_gate.v1"
GATE_DIR = ROOT / "memory" / "trust_gate"
SEEN_FILE = GATE_DIR / "seen.json"          # content-hashes already accepted (novelty dedupe)
QUARANTINE_DIR = GATE_DIR / "quarantine"

# Source reputation (provenance trust). Operator = highest; unknown = lowest.
SOURCE_TRUST = {"operator": 1.0, "grok-bot": 0.8, "frontier": 0.8, "grok": 0.8,
                "swarm-worker": 0.6, "swarm": 0.6, "bot": 0.6, "seed": 0.5, "unknown": 0.3}
TRUST_THRESHOLD = 0.6


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical(content: str) -> str:
    return hashlib.sha256(" ".join((content or "").lower().split()).encode("utf-8")).hexdigest()[:20]


def _load_seen() -> dict[str, Any]:
    if SEEN_FILE.is_file():
        try:
            return json.loads(SEEN_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"seen": {}}


def _save_seen(seen: dict[str, Any]) -> None:
    GATE_DIR.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(seen, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 1. NOVELTY (dedupe by invariant — kills duplicate poisoning) ──────────────
def novelty(content: str) -> dict[str, Any]:
    """Dedupe check: is this content ALREADY in the chain? Duplicate = the #1 poisoning vector.
    Deterministic + $0."""
    c = _canonical(content or "")
    seen = _load_seen()
    already = c in seen["seen"]
    return {"ok": not already, "novel": not already, "hash": c,
            "count": seen["seen"].get(c, 0), "note": "already-seen" if already else "novel"}


# ── 2. TRUST (provenance + groundedness + doctrine alignment) ─────────────────
def trust(content: str, source: str = "unknown") -> dict[str, Any]:
    """Trust score 0..1: source reputation + groundedness (real bytes) + doctrine alignment.
    High-trust only. Deterministic + $0."""
    src = (source or "unknown").lower()
    rep = SOURCE_TRUST.get(src, 0.3)
    # groundedness: real content present (not an empty/fabricated shell)
    grounded = 1.0 if (content or "").strip() and len(content.strip()) >= 20 else 0.0
    # doctrine alignment: does it resonate with our mounted RIBs? (weak proxy, honest)
    alignment = 0.5
    try:
        from mag import rib_bus
        m = rib_bus.mount("general")
        ribs = " ".join(m.get("ribs", []))
        if ribs:
            toks = set(ribs.lower().split())
            hits = sum(1 for w in set((content or "").lower().split()) if w in toks)
            alignment = min(1.0, 0.3 + hits * 0.1)
    except Exception:
        pass
    score = round(0.5 * rep + 0.35 * grounded + 0.15 * alignment, 3)
    return {"ok": score >= TRUST_THRESHOLD, "score": score, "source": src,
            "source_trust": rep, "grounded": grounded, "alignment": alignment,
            "threshold": TRUST_THRESHOLD}


# ── 3. POISON (heuristics: entropy, fabrication markers, forbidden) ───────────
def poison(content: str) -> dict[str, Any]:
    """Poison heuristics: low entropy (repetitive spam), fabrication markers, forbidden patterns.
    Suspicious flags. Deterministic + $0."""
    c = (content or "").strip()
    flags: list[str] = []
    if len(c) >= 20:
        # entropy: a repetitive duplicate-heavy string (spam) has low unique-token ratio
        toks = c.lower().split()
        if len(toks) > 10 and len(set(toks)) / len(toks) < 0.3:
            flags.append("low-entropy-repeat")
        # fabrication markers (the honesty law): claims of work w/o evidence
        low = c.lower()
        if any(m in low for m in ("i did x", "trust me", "no tools needed", "just believe")):
            flags.append("fabrication-marker")
        if "password=" in low or "api_key=" in low or "secret=" in low:
            flags.append("secret-leak")
    return {"ok": len(flags) == 0, "poisoned": len(flags) > 0, "flags": flags}


# ── THE GATE ──────────────────────────────────────────────────────────────────
def gate(content: str, *, source: str = "unknown", domain: str = "general") -> dict[str, Any]:
    """The full SANITY GATE: NOVEL + HIGH-TRUST + CLEAN -> ACCEPT (write); suspicious ->
    QUARANTINE (hold, never auto-write); duplicate / low-trust / poison -> REJECT (drop).
    Deterministic + $0."""
    n = novelty(content)
    t = trust(content, source)
    p = poison(content)
    if not n["novel"]:
        verdict = "REJECT"
        reason = "duplicate (already in the chain — poisoning via spam)"
    elif not t["ok"]:
        verdict = "REJECT"
        reason = f"low-trust (score {t['score']} < {TRUST_THRESHOLD}, source '{source}')"
    elif not p["ok"]:
        verdict = "QUARANTINE"
        reason = f"suspicious ({', '.join(p['flags'])}) — held, not auto-written"
    else:
        verdict = "ACCEPT"
        reason = "novel + high-trust + clean"
    if verdict == "ACCEPT":
        seen = _load_seen()
        seen["seen"][n["hash"]] = {"ts": _now(), "source": source, "domain": domain}
        _save_seen(seen)
    elif verdict == "QUARANTINE":
        QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
        (QUARANTINE_DIR / f"q-{n['hash']}.json").write_text(
            json.dumps({"schema": SCHEMA, "ts": _now(), "source": source, "domain": domain,
                        "flags": p["flags"], "content": (content or "")[:1000]},
                       ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, "verdict": verdict, "reason": reason,
            "novelty": n, "trust": t, "poison": p, "domain": domain,
            "note": f"{verdict}: {reason}"}


def status() -> dict[str, Any]:
    seen = _load_seen()
    n_q = len(list(QUARANTINE_DIR.glob("q-*.json"))) if QUARANTINE_DIR.is_dir() else 0
    return {"ok": True, "schema": SCHEMA, "n_accepted": len(seen.get("seen", {})),
            "n_quarantined": n_q,
            "contract": "gate(content, source)->ACCEPT (novel+high-trust+clean) / QUARANTINE "
                        "(suspicious) / REJECT (duplicate/low-trust/poison). Only ACCEPT writes."}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="trust-gate")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "gate"])
    ap.add_argument("text", nargs="*", default=[])
    ap.add_argument("--source", default="unknown")
    a = ap.parse_args(argv)
    if a.cmd == "gate":
        print(json.dumps(gate(" ".join(a.text) or "sample", source=a.source),
                         ensure_ascii=False, indent=2, default=str))
    else:
        print(json.dumps(status(), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
