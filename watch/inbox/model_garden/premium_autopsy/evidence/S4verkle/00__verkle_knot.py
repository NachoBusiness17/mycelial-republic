"""Living Verkle-knot record of session dossiers (topic evolution).

Filename is the address. Chain tip is a succinct root (Merkle–Verkle hybrid,
same spirit as sovereign_mirror.core.verkle — IPA/KZG upgrade-compatible).

Leaf filename pattern (living record):
  {date}_{HHmmUTC}_{dominantTheme}_{session8}_{commit8}.knot.json

Example:
  2026-07-20_1109_mag-hands_019f7f37_6a4ffbee.knot.json

Directory:
  memory/biography/knots/           # one leaf file per session commit
  memory/biography/verkle_chain.jsonl
  memory/biography/verkle_tip.json   # current root + n_leaves + last filename
  memory/biography/topic_evolution.json  # theme basis series for charts
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT

BIO = ROOT / "memory" / "biography"
KNOTS = BIO / "knots"
CHAIN = BIO / "verkle_chain.jsonl"
TIP = BIO / "verkle_tip.json"
LATEST = BIO / "latest.knot.json"
EVOLUTION = BIO / "topic_evolution.json"
LOCK = BIO / ".verkle.lock"
SCHEMA = "verkle_knot.v1"

THEME_BASIS = [
    "mirror_meta",
    "mag_hands",
    "scrum_plan",
    "constitution",
    "dashboard",
    "harness",
    "biography",
    "data_r0",
]


def _h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def session_pointer_v2(session_id: str) -> Path:
    """Collision-free pointer path for a full session identity.

    The legacy by-session pointer truncates identities to 12 characters and
    is retained only for compatibility.  New writes use the full identity's
    SHA-256 prefix so unrelated sessions cannot overwrite one another.
    """
    sid = str(session_id or "")
    return KNOTS / f"by-session_v2_{_h(sid.encode('utf-8'))[:32]}.json"


# AH19 (audit finding #10, 2026-09-29): chain write model selector.
CHAIN_MODE_V1 = "v1"
CHAIN_MODE_V2 = "v2"


def chain_mode() -> str:
    """configs/mag.yaml top-level ``chain_mode`` — AH19 append-leaves flag.

    v1 (default): amend-in-place — a re-save of an existing session replaces
    its row and rewrites the WHOLE chain file (O(n) bytes per save; live
    forensics: 2,821/8,626 rows were amend rewrites). v2: append-leaves —
    every save appends ONE new row carrying (session_id, session_seq) and
    readers resolve latest-per-session by pointer (``latest_leaf_for_session``).
    The live chain stays v1 until an operator migrates; the verifier handles
    v1 rows forever either way. Unknown/missing values fail closed to v1.
    Spec: watch/inbox/last_mile_20260930/AH19_AMEND_PERF.md
    """
    try:
        from mag.policy import load_policy

        mode = str(load_policy().get("chain_mode") or CHAIN_MODE_V1).strip().lower()
    except Exception:
        return CHAIN_MODE_V1
    return mode if mode in {CHAIN_MODE_V1, CHAIN_MODE_V2} else CHAIN_MODE_V1


def latest_leaf_pointer(session_id: str) -> dict[str, Any] | None:
    """O(1) read of the current session pointer doc (None when absent/corrupt)."""
    sid = str(session_id or "")
    if not sid:
        return None
    p = session_pointer_v2(sid)
    if not p.is_file():
        return None
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if isinstance(doc, dict) and doc.get("session_id") == sid:
        return doc
    return None


def latest_leaf_for_session(session_id: str) -> dict[str, Any] | None:
    """Canonical latest-per-session resolution (AH19 v2 readers).

    Pointer first (O(1), authoritative — v2 writes maintain it); falls back to
    the LAST matching chain row, which is exact for v1 chains (amend keeps one
    row per session) and for mixed chains (v2 saves append at the tail).
    """
    sid = str(session_id or "")
    doc = latest_leaf_pointer(sid)
    if doc and doc.get("filename"):
        return doc
    for r in reversed(_load_chain_rows()):
        if str(r.get("session_id") or "") == sid:
            return r
    return None


# ───────────────────────────────────────────────────────────────────────────
# SINGLE-WRITER LOCK (2026-08-25) — the lost-update fix.
#
# Forensics: 1,044 chain rows referenced knot files that no longer existed.
# Cause: amend unlinks the old knot file, then rewrites the WHOLE chain file;
# a concurrent append (read chain → append one line) clobbered that rewrite,
# leaving the chain pointing at the deleted filename. Every mutator below now
# holds this lock, so chain read-modify-write, knot unlink and pointer write
# are atomic with respect to each other, process-wide and seat-wide.
#
# O_CREAT|O_EXCL create is atomic on Windows and POSIX. Stale locks (crashed
# holder) are broken after _LOCK_STALE_SECONDS.
# ───────────────────────────────────────────────────────────────────────────

# Amends run _rewrite_chain, which uses an incremental O(n log n) prefix-root
# calculation. The stale threshold must exceed the worst legitimate holder or
# we'd re-introduce the race.
_LOCK_STALE_SECONDS = 900.0
_LOCK_POLL_SECONDS = 0.05


@contextlib.contextmanager
def verkle_lock(timeout: float = 60.0):
    """Cross-process single-writer lock for the verkle chain/knots/pointers."""
    deadline = time.time() + timeout
    fd = None
    while True:
        try:
            fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                stale = time.time() - LOCK.stat().st_mtime > _LOCK_STALE_SECONDS
                # A crashed writer can leave a fresh-looking marker behind (for
                # example after a test/process is terminated).  Do not wait the
                # full 15-minute safety window when the recorded owner is gone.
                if not stale:
                    try:
                        owner = int(LOCK.read_text(encoding="utf-8", errors="replace").split()[0])
                    except (OSError, ValueError, IndexError):
                        owner = 0
                    if owner and owner != os.getpid():
                        try:
                            os.kill(owner, 0)
                        except ProcessLookupError:
                            stale = True
                        except PermissionError:
                            # Cannot prove the owner is dead; preserve the lock.
                            stale = False
                        except SystemError:
                            # CPython on some Windows builds surfaces a missing
                            # PID as SystemError (WinError 87) instead of OSError.
                            stale = True
                        except OSError:
                            # Windows may report a generic missing-process error.
                            stale = True
                if stale:
                    LOCK.unlink()  # crashed holder — break the stale lock
            except OSError:
                pass
            if time.time() > deadline:
                raise TimeoutError(f"verkle_lock timeout after {timeout}s (holder pid: "
                                   f"{LOCK.read_text(encoding='utf-8', errors='replace')[:16] if LOCK.is_file() else '?'})")
            time.sleep(_LOCK_POLL_SECONDS)
    try:
        os.write(fd, f"{os.getpid()} {datetime.now(timezone.utc).isoformat()}".encode("utf-8"))
        yield
    finally:
        try:
            os.close(fd)
        finally:
            with contextlib.suppress(OSError):
                LOCK.unlink()


def _leaf_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return _h(b"leaf:" + raw)


def _merkle_root(leaf_hashes: list[str]) -> str:
    if not leaf_hashes:
        return _h(b"empty")
    layer = leaf_hashes[:]
    while len(layer) > 1:
        nxt = []
      
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 47886 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
et("start_minute"),
        "end_minute": leaf.get("end_minute"),
        "start_unix_minute": leaf.get("start_unix_minute"),
        "end_unix_minute": leaf.get("end_unix_minute"),
        "dominant_theme": leaf.get("dominant_theme"),
        "theme_vector_normalized": leaf.get("theme_vector_normalized"),
        "tension_index": leaf.get("tension_index"),
        "residual_weight": leaf.get("residual_weight"),
        "Q_proxy": leaf.get("Q_proxy"),
        "dirichlet_energy_proxy": leaf.get("dirichlet_energy_proxy"),
        "leaf_hash": leaf.get("leaf_hash"),
    }
    sid = amend_session or str(leaf.get("session_id") or "")
    replaced = False
    if sid:
        for i, s in enumerate(series):
            if str(s.get("session_id") or "") == sid:
                series[i] = {**point, "index": i}
                replaced = True
                break
    if not replaced:
        point["index"] = len(series)
        series.append(point)
    # reindex
    for i, s in enumerate(series):
        s["index"] = i
    data["series"] = series[-500:]
    data["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    EVOLUTION.write_text(json.dumps(data, indent=2), encoding="utf-8")


def evolution_summary() -> dict[str, Any]:
    """Human-readable summary of topic drift across the living record."""
    if not EVOLUTION.is_file():
        return {"ok": False, "error": "no topic_evolution.json yet"}
    data = json.loads(EVOLUTION.read_text(encoding="utf-8"))
    series = data.get("series") or []
    if not series:
        return {"ok": True, "n": 0, "message": "empty series"}

    # dominant theme counts
    from collections import Counter

    dom = Counter(s.get("dominant_theme") or "untagged" for s in series)
    # mean theme vector
    basis = data.get("theme_basis") or THEME_BASIS
    acc = [0.0] * len(basis)
    for s in series:
        v = s.get("theme_vector_normalized") or []
        for i in range(len(basis)):
            acc[i] += float(v[i]) if i < len(v) else 0.0
    n = len(series)
    mean = [round(x / n, 6) for x in acc]
    first, last = series[0], series[-1]
    return {
        "ok": True,
        "n_leaves": n,
        "verkle_root": data.get("verkle_root"),
        "first_minute": first.get("start_minute"),
        "last_minute": last.get("end_minute") or last.get("start_minute"),
        "dominant_theme_counts": dict(dom),
        "mean_theme_vector": dict(zip(basis, mean)),
        "latest_filename": last.get("filename"),
        "latest_dominant": last.get("dominant_theme"),
        "tip": str(TIP),
        "knots_dir": str(KNOTS),
    }
