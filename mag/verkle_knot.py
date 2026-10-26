"""Living Verkle-knot record of session dossiers (topic evolution).

Filename is the address. Chain tip is a succinct root (Merkle-Verkle hybrid,
same spirit as sovereign_mirror.core.verkle - IPA/KZG upgrade-compatible).

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
import sys
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

# CHAIN_REWRITE_GATE_20261019: full-file rewrite (v1 amend / heal / consolidate)
# is fail-closed unless the operator explicitly sets MAG_ALLOW_CHAIN_REWRITE=1.
# AH19 v2 append-leaves is the default write model. Receipt:
# watch/inbox/CHAIN_APPENDONLY_RESEARCH_20261019.md

def _chain_rewrite_approval_path() -> Path:
    return ROOT / "state" / "chain_rewrite_approval.json"


def _chain_rewrite_audit_path() -> Path:
    return BIO / "chain_rewrite_audit.jsonl"


def _fresh_chain_rewrite_approval() -> tuple[bool, str]:
    """Env bit alone is not enough: need fresh operator approval file OR lease.

    Approval file schema (state/chain_rewrite_approval.json):
      {"allow": true, "expires_utc": "2026-10-20T18:00:00Z", "by": "operator", "purpose": "..."}
    """
    p = _chain_rewrite_approval_path()
    if p.is_file():
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            if doc.get("allow") and doc.get("expires_utc"):
                from datetime import datetime, timezone
                exp = datetime.fromisoformat(str(doc["expires_utc"]).replace("Z", "+00:00"))
                if exp.tzinfo is not None and exp > datetime.now(timezone.utc):
                    return True, f"approval:{doc.get('by') or 'operator'}"
        except Exception:  # noqa: BLE001
            pass
    try:
        from mag.leases import guard as _lease_guard
        g = _lease_guard("chain:biography", "chain_rewrite_gate", enforce="conflict")
        # Only treat an actively held lease as the second factor (not mere unleased warn).
        if g.get("allowed") and (g.get("held") or g.get("holder") or g.get("acquired")):
            return True, "lease:chain:biography"
    except Exception:  # noqa: BLE001
        pass
    return False, "no_fresh_approval"


def _audit_chain_rewrite(why: str, via: str) -> None:
    try:
        from datetime import datetime, timezone
        line = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "why": why,
            "via": via,
            "pid": os.getpid(),
            "flag": os.environ.get("MAG_ALLOW_CHAIN_REWRITE", "0"),
        }
        path = _chain_rewrite_audit_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - audit must not block refuse path
        pass


def _chain_rewrite_allowed() -> bool:
    """CHAIN_HARDEN_ITER2_20261020: MAG_ALLOW_CHAIN_REWRITE=1 AND fresh approval/lease."""
    if os.environ.get("MAG_ALLOW_CHAIN_REWRITE", "0").strip() != "1":
        return False
    ok, _via = _fresh_chain_rewrite_approval()
    return ok


def _refuse_chain_rewrite(why: str) -> None:
    raise PermissionError(
        "chain rewrite refused (" + why + "): need MAG_ALLOW_CHAIN_REWRITE=1 AND "
        "fresh state/chain_rewrite_approval.json (expires_utc) or held chain:biography lease. "
        "Prefer chain_mode=v2 append correction rows. "
        "receipt: watch/inbox/CHAIN_HARDEN_ITER2_20261020.md"
    )


def _append_chain_line(line: str) -> None:
    """Append one JSONL line without requesting FILE_WRITE_DATA on Windows.

    Python open(..., "a") uses GENERIC_WRITE (includes WRITE_DATA), which an
    AD-only ACL correctly denies. On Windows we open with FILE_APPEND_DATA only.
    """
    data = (line if line.endswith("\n") else line + "\n").encode("utf-8")
    CHAIN.parent.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        FILE_APPEND_DATA = 0x0004
        SYNCHRONIZE = 0x00100000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_ALWAYS = 4
        FILE_ATTRIBUTE_NORMAL = 0x80
        INVALID = 0xFFFFFFFFFFFFFFFF
        CreateFileW = k.CreateFileW
        CreateFileW.argtypes = [
            wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
        ]
        CreateFileW.restype = wintypes.HANDLE
        h = CreateFileW(
            str(CHAIN), FILE_APPEND_DATA | SYNCHRONIZE,
            FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_ALWAYS,
            FILE_ATTRIBUTE_NORMAL, None,
        )
        hv = int(h) if h is not None else -1
        if hv in (-1, 0xFFFFFFFF, INVALID):
            raise OSError(ctypes.get_last_error(), f"CreateFile FILE_APPEND_DATA failed for {CHAIN}")
        try:
            written = wintypes.DWORD(0)
            if not k.WriteFile(h, data, len(data), ctypes.byref(written), None):
                raise OSError(ctypes.get_last_error(), "WriteFile append failed")
        finally:
            k.CloseHandle(h)
        return
    with CHAIN.open("a", encoding="utf-8", newline="") as fh:
        fh.write(data.decode("utf-8"))



def chain_mode() -> str:
    """configs/mag.yaml top-level ``chain_mode`` - AH19 append-leaves flag.

    v1 (default): amend-in-place - a re-save of an existing session replaces
    its row and rewrites the WHOLE chain file (O(n) bytes per save; live
    forensics: 2,821/8,626 rows were amend rewrites). v2: append-leaves -
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

    Pointer first (O(1), authoritative - v2 writes maintain it); falls back to
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
# SINGLE-WRITER LOCK (2026-08-25) - the lost-update fix.
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

# HEARTBEAT LOCK RECORD (2026-10-15). The lock file now holds JSON
# {hostname, pid, start_ts, heartbeat_ts}; the holder rewrites heartbeat_ts every
# LOCK_HEARTBEAT_SECONDS from a daemon thread. A waiter may break the lock ONLY
# when hostname == its own hostname AND the heartbeat is older than
# LOCK_HEARTBEAT_STALE_SECONDS. The Windows host and each container have
# different hostnames and separate PID namespaces, so a cross-host break is now
# impossible (before: a container waiter's os.kill(<windows pid>, 0) raised
# ProcessLookupError and it unlinked a lock held on the host). Pre-heartbeat
# readers parse int(first token) -> ValueError -> owner 0 -> never break a JSON
# record unless its mtime is 900s old, which the heartbeat prevents. The same
# record + helpers back the AOS carrier lock in mag.governor_autorun.
LOCK_HEARTBEAT_SECONDS = 5.0
LOCK_HEARTBEAT_STALE_SECONDS = 120.0


def _lock_hostname() -> str:
    import socket
    return socket.gethostname()


def _proc_start_ts() -> float | None:
    """This process's creation time (survives a POSIX execv, so a self-restart keeps it)."""
    try:
        import psutil  # type: ignore
        return round(float(psutil.Process(os.getpid()).create_time()), 2)
    except Exception:
        pass
    try:
        with open(f"/proc/{os.getpid()}/stat", encoding="utf-8") as f:
            ticks = int(f.read().rsplit(")", 1)[1].split()[19])
        with open("/proc/stat", encoding="utf-8") as f:
            btime = next(int(ln.split()[1]) for ln in f if ln.startswith("btime"))
        return round(btime + ticks / os.sysconf("SC_CLK_TCK"), 2)
    except Exception:
        return None


def lock_record(start_ts: float | None = None) -> dict[str, Any]:
    now = round(time.time(), 3)
    return {"hostname": _lock_hostname(), "pid": os.getpid(),
            "start_ts": _proc_start_ts() if start_ts is None else start_ts, "heartbeat_ts": now}


def read_lock_record(path: Path) -> dict[str, Any] | None:
    """The heartbeat record, or None for a legacy / torn / unreadable lock file."""
    try:
        rec = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
    if not isinstance(rec, dict) or not rec.get("hostname") or "heartbeat_ts" not in rec:
        return None
    return rec


def lock_is_self(rec: dict[str, Any]) -> bool:
    """Same host + same pid is this very process (a live pid is unique on a host); a POSIX
    execv self-restart keeps both, and start_ts too when it is known."""
    if rec.get("hostname") != _lock_hostname() or int(rec.get("pid") or 0) != os.getpid():
        return False
    mine, theirs = _proc_start_ts(), rec.get("start_ts")
    return mine is None or theirs is None or abs(float(theirs) - mine) < 2.0


def lock_breakable(rec: dict[str, Any], now: float | None = None) -> bool:
    """Steal ONLY a same-host lock whose heartbeat is stale. Foreign hosts: never."""
    if rec.get("hostname") != _lock_hostname():
        return False
    try:
        age = (time.time() if now is None else now) - float(rec.get("heartbeat_ts"))
    except (TypeError, ValueError):
        return False
    return age > LOCK_HEARTBEAT_STALE_SECONDS


def start_lock_heartbeat(write, interval: float | None = None):
    """Daemon thread calling write(record) every interval s; returns a threading.Event to stop it."""
    import threading
    stop = threading.Event()
    rec = lock_record()

    def _beat() -> None:
        while not stop.wait(LOCK_HEARTBEAT_SECONDS if interval is None else interval):
            rec["heartbeat_ts"] = round(time.time(), 3)
            try:
                write(dict(rec))
            except Exception:  # noqa: BLE001 - a missed beat is retried next interval
                pass

    threading.Thread(target=_beat, name="lock-heartbeat", daemon=True).start()
    return stop, rec


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
                rec = read_lock_record(LOCK)
                if rec is not None:
                    # heartbeat record: same-host + stale heartbeat is the ONLY break
                    stale = lock_breakable(rec)
                else:
                    stale = time.time() - LOCK.stat().st_mtime > _LOCK_STALE_SECONDS
                # A crashed writer can leave a fresh-looking marker behind (for
                # example after a test/process is terminated).  Do not wait the
                # full 15-minute safety window when the recorded owner is gone.
                # (legacy "<pid> <iso>" markers from pre-heartbeat writers only)
                if rec is None and not stale:
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
                    LOCK.unlink()  # crashed holder - break the stale lock
            except OSError:
                pass
            if time.time() > deadline:
                raise TimeoutError(f"verkle_lock timeout after {timeout}s (holder: "
                                   f"{LOCK.read_text(encoding='utf-8', errors='replace')[:160] if LOCK.is_file() else '?'})")
            time.sleep(_LOCK_POLL_SECONDS)
    import threading
    beat_lock = threading.Lock()

    def _write(rec: dict[str, Any]) -> None:
        data = json.dumps(rec).encode("utf-8")
        with beat_lock:
            if fd is None:
                return
            os.lseek(fd, 0, os.SEEK_SET)
            os.write(fd, data)
            os.ftruncate(fd, len(data))

    stop = None
    try:
        stop, rec = start_lock_heartbeat(_write)
        _write(rec)
        yield
    finally:
        if stop is not None:
            stop.set()
        try:
            with beat_lock:
                os.close(fd)
                fd = None
        finally:
            with contextlib.suppress(OSError):
                cur = read_lock_record(LOCK)
                # never unlink a lock someone else (legitimately) took over
                if cur is None or lock_is_self(cur):
                    LOCK.unlink()


# MERKLE CURE (2026-10-07), position-bound leaf hashing, flag-gated OFF.
#
# Defect (proven, watch/inbox/MERKLE_COLLISION_PROOF_20261007.md): _merkle_root
# duplicates the last node at every odd level, so [a,b,c] and [a,b,c,c] build
# byte-identical roots when leaves do not bind their position (content forgery
# stays blocked by the b"leaf:" domain; the defect is length ambiguity).
#
# Cure (the receipt's Option A): bind the leaf's chain index into its hash
# domain (b"leaf:<i>:" + raw). Identical content at two positions then hashes
# differently, so the trailing-duplicate elision can no longer fold the two
# trees together; the probe flips to COLLISION: False.
#
# Flag law: MAG_POSITION_BOUND_LEAVES unset/false keeps the legacy
# b"leaf:" domain BYTE-IDENTICAL (the live 11k+ leaf chain and every stored
# leaf_hash verify unchanged). The flag flips only hashes where the caller
# passes an explicit index; omitting index under a raised flag deliberately
# stays in the legacy domain so pre-migration verifiers (knot_rehash_patrol,
# verkle_dangling_repair, VerkleProof.verify) remain coherent. The LIVE chain
# is NOT migrated by this flag: turning it on for new appends without the
# operator's full-chain re-hash pass would fork leaf domains mid-chain, so
# migration stays operator-gated (receipt section "Cure").
POSITION_BOUND_LEAVES_ENV = "MAG_POSITION_BOUND_LEAVES"

_POSITION_BOUND_TRUTHY = {"1", "true", "yes", "on"}


def position_bound_leaves() -> bool:
    """Read MAG_POSITION_BOUND_LEAVES (default OFF, fail-closed to legacy).

    Mirrors the chain_mode() fail-closed pattern: any value outside the truthy
    set keeps the legacy b"leaf:" hash domain byte-identical.
    """
    return os.environ.get(POSITION_BOUND_LEAVES_ENV, "").strip().lower() in _POSITION_BOUND_TRUTHY


def _leaf_hash(obj: Any, index: int | None = None) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    if index is not None and position_bound_leaves():
        return _h(b"leaf:" + str(int(index)).encode("ascii") + b":" + raw)
    return _h(b"leaf:" + raw)


def _merkle_root(leaf_hashes: list[str]) -> str:
    # Length-ambiguity defect (MERKLE_COLLISION_PROOF_20261007): duplicate-last
    # padding below means a root alone does not bind the leaf count. Leaf-level
    # position binding (MAG_POSITION_BOUND_LEAVES, see _leaf_hash) is the cure;
    # callers may additionally bind n_leaves (VerkleProof.verify, T1W1 ticket 12).
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


def _merkle_prefix_roots(leaf_hashes: list[str]) -> list[str]:
    """Return the legacy duplicate-last Merkle root for every non-empty prefix.

    ``_merkle_root`` duplicates the final node at *each level* when a layer has
    odd cardinality. Recomputing that tree for every prefix made an amend
    quadratic in the number of leaves. A binary forest stores complete
    subtrees as leaves arrive; folding those subtrees right-to-left, lifting a
    shorter suffix by self-duplication where necessary, reproduces the legacy
    semantics in O(log n) work per prefix. The result is byte-for-byte
    equivalent to ``_merkle_root`` for every prefix, but costs O(n log n)
    hashes instead of O(n²).
    """
    if not leaf_hashes:
        return []

    def _join(left: str, right: str) -> str:
        return _h(b"node:" + left.encode() + b":" + right.encode())

    def _lift(root: str, from_height: int, to_height: int) -> str:
        """Apply the same-node duplication until a suffix reaches a height."""
        for _ in range(max(0, to_height - from_height)):
            root = _join(root, root)
        return root

    # (root, height), in left-to-right binary decomposition order. Heights
    # descend strictly from left to right, so a right fold is well-defined.
    forest: list[tuple[str, int]] = []

    roots: list[str] = []
    for leaf in leaf_hashes:
        forest.append((leaf, 0))
        while len(forest) >= 2 and forest[-1][1] == forest[-2][1]:
            right, height = forest.pop()
            left, _ = forest.pop()
            forest.append((_join(left, right), height + 1))

        root, height = forest[-1]
        for left, left_height in reversed(forest[:-1]):
            root = _lift(root, height, left_height)
            root = _join(left, root)
            height = left_height + 1
        roots.append(root)
    return roots


def _slug_theme(name: str | None) -> str:
    if not name:
        return "untagged"
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return (s or "untagged")[:24]


def knot_filename(
    *,
    start_minute_iso: str | None,
    dominant_theme: str | None,
    session_id: str,
    commit_hex: str,
    chord_slug: str | None = None,
    seq: int | None = None,
) -> str:
    """Build living-record filename from time + topic + identity + commit.

    Optional chord_slug (from strike commitment) replaces theme when present:
      {date}_{HHmm}_{chord-slug}_{session8}_{commit8}.knot.json

    AH19 chain_mode=v2: ``seq`` (the session's save counter) is embedded as a
    ``.s{seq}`` suffix so every appended leaf of one session gets a unique,
    history-preserving filename (v2 never unlinks prior knots).
    """
    if start_minute_iso:
        m = re.match(
            r"(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})",
            start_minute_iso.replace("Z", ""),
        )
        if m:
            date, hh, mm = m.group(1), m.group(2), m.group(3)
        else:
            now = datetime.now(timezone.utc)
            date, hh, mm = now.strftime("%Y-%m-%d"), now.strftime("%H"), now.strftime("%M")
    else:
        now = datetime.now(timezone.utc)
        date, hh, mm = now.strftime("%Y-%m-%d"), now.strftime("%H"), now.strftime("%M")

    if chord_slug and str(chord_slug).startswith("chord-"):
        # chord-biography-abc123def → biography
        parts = str(chord_slug).split("-")
        theme = _slug_theme(parts[1] if len(parts) > 1 else dominant_theme)
    else:
        theme = _slug_theme(dominant_theme)
    # Windows-safe: session ids may carry colons (work:test:...) which are invalid in
    # filenames - collapse any path-invalid chars so every fold lands (2026-08-25).
    sid = re.sub(r"[^A-Za-z0-9._-]+", "-", str(session_id or "unknown"))[:8]
    c8 = (commit_hex or "0" * 8)[:8]
    base = f"{date}_{hh}{mm}_{theme}_{sid}_{c8}"
    if seq is not None and int(seq) > 0:
        base += f".s{int(seq)}"
    return base + ".knot.json"


def build_leaf_from_dossier(dossier: dict[str, Any]) -> dict[str, Any]:
    """Canonical leaf payload for Verkle commit (topic evolution unit)."""
    time = dossier.get("time") or {}
    sk = dossier.get("scalar_knot") or {}
    tv = sk.get("theme_vector") or {}
    created = time.get("created_at") or {}
    updated = time.get("updated_at") or time.get("last_active_at") or {}
    commit = dossier.get("content_commit") or {}

    # pad theme vector to fixed basis
    basis = tv.get("basis") or THEME_BASIS
    raw = tv.get("raw") or [0.0] * len(THEME_BASIS)
    norm = tv.get("normalized") or [0.0] * len(THEME_BASIS)
    if len(norm) < len(THEME_BASIS):
        norm = list(norm) + [0.0] * (len(THEME_BASIS) - len(norm))

    leaf = {
        "type": "session_scalar_knot_leaf",
        "schema": "verkle_knot_leaf.v1",
        "session_id": dossier.get("session_id"),
        "start_minute": created.get("iso_minute"),
        "end_minute": updated.get("iso_minute"),
        "start_unix_minute": created.get("unix_minute"),
        "end_unix_minute": updated.get("unix_minute"),
        "date": created.get("date"),
        "duration_minutes": sk.get("duration_minutes"),
        "dominant_theme": tv.get("dominant"),
        "theme_basis": basis if basis else THEME_BASIS,
        "theme_vector_raw": raw,
        "theme_vector_normalized": norm[: len(THEME_BASIS)],
        "tension_index": sk.get("tension_index"),
        "residual_weight": sk.get("residual_weight"),
        "Q_proxy": sk.get("Q_proxy"),
        "gap_proxy": sk.get("gap_proxy"),
        "lambda2_proxy": sk.get("lambda2_proxy"),
        "dirichlet_energy_proxy": sk.get("dirichlet_energy_proxy"),
        "dossier_commit": commit.get("hex"),
        "chord_commitment": (dossier.get("chord") or {}).get("commitment_hash"),
        "chord_root": (dossier.get("chord") or {}).get("framework_root"),
        "observer_chart_scores": {
            c.get("id"): c.get("score")
            for c in ((dossier.get("chord") or {}).get("observer_charts") or [])
        },
        "loops_audited": [
            L.get("id") for L in ((dossier.get("chord") or {}).get("loops_audited") or [])
        ],
        "engine": "untangling+strike_chord",
        "inspiration": "steiniger_proxies+strike_chord+verkle_history",
    }
    leaf["leaf_hash"] = _leaf_hash(leaf)
    return leaf


def _load_chain_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not CHAIN.is_file():
        return rows
    for line in CHAIN.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _attic_dir() -> Path:
    """Retired-knot attic: a SIBLING of KNOTS, never inside it.

    Every knot scanner globs KNOTS directly (ghost_auto, invariant_lattice,
    lattice_backfill, socratic_tree, knot_at_close all glob '*.knot.json' /
    '*.json'), so retired files must leave the directory entirely to keep the
    single-leaf-per-session view and the tar backups clean.
    """
    return KNOTS.parent / "knots_attic"


def _retire_knot(path: Path) -> bool:
    """Move a superseded knot file into the attic instead of unlinking it.

    T1W1 ticket 8 (2026-10-01, RACTOR): the v1 amend path unlinked the old
    knot BEFORE the chain rewrite, so a crash between the two left the chain
    pointing at a deleted file and destroyed the pre-amend leaf (the
    2026-08-25 forensics: 1,044 chain rows referenced knot files that no
    longer existed). os.replace into the attic keeps the bytes recoverable;
    a failed move leaves the file in place (data-preserving, never lossy).
    A same-named attic file is overwritten: the newest retirement wins, and
    attic contents are archives, not history of archives.
    """
    try:
        if not path.is_file():
            return False
        attic = _attic_dir()
        attic.mkdir(parents=True, exist_ok=True)
        os.replace(path, attic / path.name)
        return True
    except OSError:
        return False


def _consolidate_chain_one_leaf_per_session_unlocked() -> dict[str, Any]:
    """Drop duplicate chain rows (keep last per session). Safe to run anytime."""
    # AH19 (2026-09-30): under chain_mode=v2 multiple rows per session are
    # canonical HISTORY (append-leaves), not bloat - collapsing them would
    # destroy the seq pointers' past. Consolidation stays a v1 tool.
    if chain_mode() == CHAIN_MODE_V2:
        return {
            "ok": True,
            "skipped": True,
            "reason": "chain_mode=v2: multiple rows per session are canonical history (AH19); refusing to collapse",
            "before": len(_load_chain_rows()),
        }
    rows = _load_chain_rows()
    by_sid: dict[str, dict[str, Any]] = {}
    orphan: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    # T1W1 ticket 8 (2026-10-01, RACTOR): retirement is COLLECTED here and
    # only executed after the conflicts refusal below has its say; the old
    # code unlinked inside the scan loop, so a refusing repair (conflicting
    # leaf hashes) had already deleted knot files it then refused to touch.
    to_retire: list[Path] = []
    for r in rows:
        sid = str(r.get("session_id") or "")
        if not sid:
            orphan.append(r)
            continue
        # keep last occurrence (most recent amend)
        old = by_sid.get(sid)
        if old and old.get("leaf_hash") != r.get("leaf_hash"):
            conflicts.append({
                "session_id": sid,
                "first_leaf_hash": old.get("leaf_hash"),
                "later_leaf_hash": r.get("leaf_hash"),
            })
            continue
        if old and old.get("filename") and old.get("filename") != r.get("filename"):
            to_retire.append(KNOTS / str(old["filename"]))
        by_sid[sid] = r
    if conflicts:
        return {
            "ok": False,
            "error": "conflicting leaf hashes for duplicate session IDs; refusing repair",
            "conflicts": conflicts,
            "before": len(rows),
        }
    for path in to_retire:
        _retire_knot(path)
    # preserve first-seen order of sessions
    order: list[str] = []
    for r in rows:
        sid = str(r.get("session_id") or "")
        if sid and sid not in order:
            order.append(sid)
    kept = [by_sid[s] for s in order if s in by_sid] + orphan
    hashes = _rewrite_chain(kept)
    root = _merkle_root(hashes) if hashes else _h(b"empty")
    tip = {
        "schema": "verkle_tip.v1",
        "root": root,
        "n_leaves": len(hashes),
        "last_filename": (kept[-1].get("filename") if kept else None),
        "last_leaf_hash": hashes[-1] if hashes else None,
        "last_session_id": (kept[-1].get("session_id") if kept else None),
        "note": "Consolidated: one leaf per session.",
    }
    TIP.parent.mkdir(parents=True, exist_ok=True)
    # atomic write (2026-09-25): a torn tip write froze every chain append via the
    # integrity gate; _write_tip_atomic (tmp + os.replace) closes that window.
    _write_tip_atomic(tip)
    # evolution series unique by session
    if EVOLUTION.is_file():
        try:
            evo = json.loads(EVOLUTION.read_text(encoding="utf-8"))
            series = evo.get("series") or []
            seen: dict[str, dict] = {}
            ord_s: list[str] = []
            for s in series:
                sid = str(s.get("session_id") or "")
                if not sid:
                    continue
                if sid not in ord_s:
                    ord_s.append(sid)
                seen[sid] = s
            evo["series"] = [{**seen[s], "index": i} for i, s in enumerate(ord_s)]
            evo["n_leaves"] = len(evo["series"])
            evo["verkle_root"] = root
            EVOLUTION.write_text(json.dumps(evo, indent=2), encoding="utf-8")
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "ok": True,
        "before": len(rows),
        "after": len(kept),
        "removed": len(rows) - len(kept),
        "root": root,
    }


def _rewrite_chain(rows: list[dict[str, Any]]) -> list[str]:
    """Rewrite chain file with stable indices; return leaf_hashes in order.

    Prefix roots are computed incrementally so an amend remains bounded on the
    live 6k+ leaf chain.

    CHAIN_REWRITE_GATE_20261019: refuse unless MAG_ALLOW_CHAIN_REWRITE=1.
    """
    if not _chain_rewrite_allowed():
        _refuse_chain_rewrite("_rewrite_chain")
    _ok, _via = _fresh_chain_rewrite_approval()
    _audit_chain_rewrite("_rewrite_chain", _via)
    hashes = [str(row.get("leaf_hash")) for row in rows if row.get("leaf_hash")]
    prefix_roots = _merkle_prefix_roots(hashes)
    lines: list[str] = []
    hash_i = 0
    for i, row in enumerate(rows):
        h = row.get("leaf_hash")
        if not h:
            continue
        root = prefix_roots[hash_i]
        parent = prefix_roots[hash_i - 1] if hash_i else _h(b"empty")
        row = dict(row)
        row["index"] = i
        row["n_leaves"] = hash_i + 1
        row["parent_verkle_root"] = parent
        row["verkle_root"] = root
        lines.append(json.dumps(row))
        hash_i += 1
    CHAIN.parent.mkdir(parents=True, exist_ok=True)
    # B2-393 byte-exact chain law: write_text on Windows translates every LF
    # in the chain to CRLF (B2-83 rev 1 proved it live on the 9,873-line
    # chain); the chain is written through bytes so LF stays LF.
    # T1W1 ticket 9 (2026-10-01, RACTOR): the rewrite used to land as ONE
    # in-place write, so a crash mid-amend truncated ALL history (an opened
    # "w" write is empty the moment it starts). tmp + os.replace keeps the
    # pre-amend chain intact until the full rewrite is on disk, the same
    # contract _write_tip_atomic already holds for the tip. Proven by
    # tests/test_t1w1_ractor_fixes.py (no .tmp residue, LF-only bytes, and
    # the tmp file never observed mid-flight at the CHAIN path).
    payload = ("\n".join(lines) + ("\n" if lines else "")).encode("utf-8")
    tmp = CHAIN.with_name(f"{CHAIN.name}.{os.getpid()}.tmp")
    try:
        tmp.write_bytes(payload)
        os.replace(tmp, CHAIN)
    finally:
        with contextlib.suppress(OSError):
            tmp.unlink()
    return hashes


# ───────────────────────────────────────────────────────────────────────────
# PROOF - STOLEN from sovereign_mirror.core.verkle (VerkleProof + prove).
# Same `_h` / `_leaf` / `node:` pairing scheme, rebuilt against the live chain.
# O(log n) inclusion path: index + sibling hashes → recompute root == tip.
# ───────────────────────────────────────────────────────────────────────────
class VerkleProof:
    """Membership proof over the knot chain: index + sibling path -> root.

    verify() reconstructs the root from (index, leaf_hash, sibling path) and
    matches it against the committed root. The invariant equation, executable.
    """

    def __init__(self, index: int, leaf_hash: str, path: list[str], root: str) -> None:
        self.index = index
        self.leaf_hash = leaf_hash
        self.path = path  # sibling hashes, bottom-up
        self.root = root

    def verify(self, leaf_obj: Any | None = None, leaf_hash: str | None = None,
               n_leaves: int | None = None) -> bool:
        """Recreate the root from the pointer + siblings; match the committed root.

        T1W1 ticket 12 (2026-10-01, RACTOR law L3): under duplicate-last
        padding one root covers several leaf counts ([a,b,c] and [a,b,c,c]
        share a root), so a proof that does not bind the leaf count can be
        replayed against a different-length chain: an index at or beyond the
        real n still reconstructs the padded root. When ``n_leaves`` is
        passed, verify refuses any index outside 0..n_leaves-1 and any path
        whose depth is not exactly ceil(log2(n)) ((n-1).bit_length(), the
        depth _merkle_root's halving loop produces). ``prove()`` passes it;
        callers that cannot know n may omit it and get the legacy root-only
        check. Pinned by tests/test_t1w1_ractor_fixes.py.
        """
        h = leaf_hash or (_leaf_hash(leaf_obj) if leaf_obj is not None else self.leaf_hash)
        if h != self.leaf_hash:
            return False
        if n_leaves is not None:
            if n_leaves < 1 or not (0 <= self.index < n_leaves):
                return False
            if len(self.path) != (n_leaves - 1).bit_length():
                return False
        idx = self.index
        for sib in self.path:
            if idx % 2 == 0:
                h = _h(b"node:" + h.encode() + b":" + sib.encode())
            else:
                h = _h(b"node:" + sib.encode() + b":" + h.encode())
            idx //= 2
        return h == self.root

    def equation(self) -> str:
        """Human-readable invariant: the reconstruction equation."""
        terms = []
        idx = self.index
        for step, sib in enumerate(self.path, 1):
            terms.append(f"n{step}=H({'L' if idx % 2 == 0 else 'R'}+{sib[:8]})")
            idx //= 2
        return f"root = {self.root[:16]}…  ←  " + " → ".join(terms)


def _leaf_hashes_in_order() -> list[str]:
    """Ordered leaf hashes from the chain (no side effects)."""
    return [r["leaf_hash"] for r in _load_chain_rows() if r.get("leaf_hash")]


def prove(index: int | None = None) -> dict[str, Any]:
    """Build an O(log n) inclusion proof for a leaf in the knot chain.

    Default index = the latest leaf. Returns the proof dict (reversible via
    VerkleProof.verify) so ghost can demonstrate real reconstruction.
    """
    leaves = _leaf_hashes_in_order()
    if not leaves:
        return {"ok": False, "error": "no verkle leaves committed yet"}
    idx = index if index is not None else len(leaves) - 1
    if not (0 <= idx < len(leaves)):
        return {"ok": False, "error": f"index {idx} out of range (0..{len(leaves)-1})"}
    root = _merkle_root(leaves)
    layer = leaves[:]
    path: list[str] = []
    i = idx
    while len(layer) > 1:
        if i % 2 == 0:
            sib = layer[i + 1] if i + 1 < len(layer) else layer[i]
        else:
            sib = layer[i - 1]
        path.append(sib)
        nxt: list[str] = []
        for j in range(0, len(layer), 2):
            left = layer[j]
            right = layer[j + 1] if j + 1 < len(layer) else left
            nxt.append(_h(b"node:" + left.encode() + b":" + right.encode()))
        layer = nxt
        i //= 2
    proof = VerkleProof(index=idx, leaf_hash=leaves[idx], path=path, root=root)
    return {
        "ok": True,
        "index": idx,
        "n_leaves": len(leaves),
        "leaf_hash": leaves[idx],
        "path": path,
        "root": root,
        # T1W1 ticket 12: the self-verification binds the leaf count it was
        # proved against, not just the root.
        "verified": proof.verify(n_leaves=len(leaves)),
        "equation": proof.equation(),
    }


def prove_latest() -> dict[str, Any]:
    """Prove latest membership only when the persisted tip agrees with the chain."""
    ok, why = _verify_chain_consistent()
    if not ok:
        return {"ok": False, "verified": False, "error": why, "n_leaves": 0}
    return prove()



def _verify_chain_consistent() -> tuple[bool, str]:
    """Verify the committed chain is tamper-evident before extending it (party_subchain pattern,
    2026-08-16). Recompute the merkle root over ALL leaves once (O(n), not O(n^2)) and check it
    matches the last committed row's root + the tip. Any tampered leaf -> root mismatch -> False.
    This is the integrity GATE: refuse to extend an unverified chain (never build on a lie).

    T1W1 ticket 7 (2026-10-01, RACTOR distillation, law L3): the tip check used
    to sit in `except (OSError, JSONDecodeError): pass` and a MISSING tip file
    read as {}, so a corrupt or absent tip on a non-empty chain cleared the
    gate while binding nothing (and a root alone does not bind leaf count
    under duplicate-last padding). The expected tip is now recomputed from the
    tail and compared: root and n_leaves must match exactly, last_leaf_hash is
    checked when present (older tips predate the field). Fail-closed is safe:
    the sanctioned healer is repair_tip_if_consistent (verkle_audit --auto-heal),
    which re-derives the tip and refuses on row-root disagreement only. Pinned
    by tests/test_t1w1_ractor_fixes.py: corrupt tip, absent tip, empty-JSON tip
    and a stale-n tip each refuse the gate; the honest tail still passes."""
    rows = _load_chain_rows()
    if not rows:
        return True, "empty chain (genesis ok)"
    hashes = [r.get("leaf_hash") for r in rows if r.get("leaf_hash")]
    if not hashes:
        return True, "no leaf hashes yet"
    expect = _merkle_root(hashes)
    if rows[-1].get("verkle_root") != expect:
        return False, f"last row root mismatch (committed {str(rows[-1].get('verkle_root'))[:16]} vs recomputed {expect[:16]})"
    try:
        tip = json.loads(TIP.read_text(encoding="utf-8")) if TIP.is_file() else None
    except (OSError, json.JSONDecodeError):
        tip = None
    if not isinstance(tip, dict) or not tip:
        return False, (f"tip missing or unreadable on a non-empty chain "
                       f"(expected root {expect[:16]}..., {len(hashes)} leaves; "
                       "heal via repair_tip_if_consistent)")
    if tip.get("root") != expect:
        return False, f"tip root mismatch (tip {str(tip.get('root'))[:16]} vs recomputed {expect[:16]})"
    if tip.get("n_leaves") != len(hashes):
        return False, f"tip n_leaves mismatch (tip {tip.get('n_leaves')} vs recomputed {len(hashes)})"
    if tip.get("last_leaf_hash") and tip.get("last_leaf_hash") != hashes[-1]:
        return False, (f"tip last_leaf_hash mismatch (tip {str(tip.get('last_leaf_hash'))[:16]} "
                       f"vs tail {str(hashes[-1])[:16]})")
    return True, f"chain consistent ({len(hashes)} leaves)"


def _tip_for_tail(rows: list[dict[str, Any]], hashes: list[str], root: str) -> dict[str, Any]:
    """Boot pointer is the chain tail, never the session that was just amended."""
    hashed = [r for r in rows if r.get("leaf_hash")]
    last = hashed[-1] if hashed else {}
    return {
        "schema": "verkle_tip.v1",
        "root": root,
        "n_leaves": len(hashes),
        "last_filename": last.get("filename"),
        "last_leaf_hash": hashes[-1] if hashes else None,
        "last_session_id": last.get("session_id"),
        "updated_minute": last.get("end_minute") or last.get("start_minute"),
        "note": "Tip is the chain tail. An amended older session does not become the boot.",
    }


def _sync_latest_knot(last_filename: str | None, leaf_if_tail: dict[str, Any] | None) -> None:
    """latest.knot.json mirrors the tail leaf. An older amend must not replace it."""
    if leaf_if_tail is not None:
        LATEST.write_text(json.dumps(leaf_if_tail, indent=2), encoding="utf-8")
        return
    if not last_filename:
        return
    src = KNOTS / str(last_filename)
    if src.is_file():
        LATEST.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _write_tip_atomic(tip: dict[str, Any]) -> None:
    """Replace the small tip pointer atomically while holding ``verkle_lock``."""
    TIP.parent.mkdir(parents=True, exist_ok=True)
    tmp = TIP.with_name(f"{TIP.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(json.dumps(tip, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, TIP)
    finally:
        with contextlib.suppress(OSError):
            tmp.unlink()


def repair_tip_if_consistent() -> dict[str, Any]:
    """Repair only stale tip metadata after proving the chain itself is sound.

    This deliberately does not consolidate or rewrite the chain.  If the last
    committed row disagrees with the recomputed root, the repair refuses to
    mutate anything and returns the integrity failure for the Elder to surface.
    """
    with verkle_lock():
        rows = _load_chain_rows()
        hashes = [str(r.get("leaf_hash")) for r in rows if r.get("leaf_hash")]
        root = _merkle_root(hashes) if hashes else _h(b"empty")
        if rows and hashes and rows[-1].get("verkle_root") != root:
            return {"ok": False, "repaired": False,
                    "error": "last chain row disagrees with recomputed root",
                    "n_leaves": len(hashes), "root": root}
        old: dict[str, Any] = {}
        if TIP.is_file():
            try:
                value = json.loads(TIP.read_text(encoding="utf-8"))
                if isinstance(value, dict):
                    old = value
            except (OSError, json.JSONDecodeError):
                old = {}
        tip = _tip_for_tail(rows, hashes, root)
        changed = any(old.get(k) != v for k, v in tip.items())
        if changed:
            _write_tip_atomic(tip)
        _sync_latest_knot(tip.get("last_filename"), None)
        return {"ok": True, "repaired": changed, "n_leaves": len(hashes),
                "root": root, "tip": str(TIP)}



def _append_verkle_knot_unlocked(dossier: dict[str, Any], pdf_path: str | None = None) -> dict[str, Any]:
    """
    Write/update one leaf per session (amend in place).

    Same session_id → replace existing chain row + knot file (no bloat).
    New session_id → append. Same leaf_hash → skip.

    INTEGRITY GATE (2026-08-16, party_subchain pattern): refuse to extend an unverified chain.
    """
    ok, why = _verify_chain_consistent()
    if not ok:
        return {"ok": False, "schema": SCHEMA, "error": "refusing to extend an unverified verkle chain",
                "verify": why}
    KNOTS.mkdir(parents=True, exist_ok=True)
    leaf = build_leaf_from_dossier(dossier)
    # AH19 (audit finding #10, 2026-09-30): chain_mode=v2 turns this writer into
    # append-leaves - a re-save NEVER amends/rewrites prior rows; it appends ONE
    # new row whose (session_id, session_seq) pointer resolves latest-per-session.
    # v1 keeps the amend-in-place behavior byte-identical. Spec: AH19_AMEND_PERF.md.
    mode = chain_mode()
    sid = str(leaf.get("session_id") or "unknown")
    pointer = latest_leaf_pointer(sid) if mode == CHAIN_MODE_V2 else None
    seq = (int(pointer.get("seq") or 0) + 1) if (mode == CHAIN_MODE_V2 and pointer) else 1
    fname = knot_filename(
        start_minute_iso=leaf.get("start_minute"),
        dominant_theme=leaf.get("dominant_theme"),
        session_id=str(leaf.get("session_id") or ""),
        commit_hex=str(leaf.get("dossier_commit") or leaf.get("leaf_hash") or ""),
        chord_slug=leaf.get("chord_commitment"),
        seq=seq if mode == CHAIN_MODE_V2 else None,
    )
    leaf["filename"] = fname
    if pdf_path:
        leaf["pdf_path"] = pdf_path

    rows = _load_chain_rows()
    existing_i = (
        next(
            (i for i, r in enumerate(rows) if str(r.get("session_id") or "") == sid),
            None,
        )
        if mode != CHAIN_MODE_V2
        else None
    )
    # V1_APPEND_ONLY (2026-10-17, operator): under chain_mode v2 the re-save row names the row
    # it supersedes; the newest-row scan also dedupes sessions that have no v2 pointer file.
    prev_i = (next((i for i in range(len(rows) - 1, -1, -1)
                    if str(rows[i].get("session_id") or "") == sid), None)
              if mode == CHAIN_MODE_V2 else None)

    # identical content already recorded for this session - v2 dedupes against
    # the POINTER's current leaf (O(1)); v1 against the row scan.
    if (
        mode == CHAIN_MODE_V2
        and pointer
        and pointer.get("leaf_hash") == leaf["leaf_hash"]
    ) or (
        existing_i is not None and rows[existing_i].get("leaf_hash") == leaf["leaf_hash"]
    ) or (
        mode == CHAIN_MODE_V2 and not pointer and prev_i is not None
        and rows[prev_i].get("leaf_hash") == leaf["leaf_hash"]
    ):
        tip = json.loads(TIP.read_text(encoding="utf-8")) if TIP.is_file() else {}
        # v2 skip: the pointer already committed THIS content at its seq - report
        # the recorded file, not the would-be .s{seq+1} name that was never written.
        skip_fname = str(pointer.get("filename") or fname) if pointer else fname
        skip_seq = int(pointer.get("seq") or 0) if pointer else seq
        return {
            "ok": True,
            "skipped": True,
            "amended": False,
            "filename": skip_fname,
            "leaf_hash": leaf["leaf_hash"],
            "verkle_root": tip.get("root"),
            "path": str(KNOTS / skip_fname),
            "n_leaves": tip.get("n_leaves") or len(rows),
            "chain_mode": mode,
            "session_seq": skip_seq,
        }

    # drop old knot file for this session if filename changed (v1 ONLY - under
    # v2 prior knots are canonical history and are never unlinked)
    # T1W1 ticket 8 (2026-10-01, RACTOR): this used to UNLINK the old knot
    # before the chain rewrite below; a crash between the two left the chain
    # pointing at a deleted file and destroyed the pre-amend leaf. The knot
    # now retires to the attic (out of the KNOTS glob namespace, bytes kept);
    # v1's single-row-per-session view is unchanged.
    if existing_i is not None:
        old_name = rows[existing_i].get("filename")
        if old_name and old_name != fname:
            _retire_knot(KNOTS / str(old_name))

    path = KNOTS / fname
    path.write_text(json.dumps(leaf, indent=2), encoding="utf-8")
    pointer_doc = {"filename": fname, "leaf_hash": leaf["leaf_hash"], "session_id": sid,
                   "schema": "verkle_session_pointer.v2"}
    if mode == CHAIN_MODE_V2:
        # AH19: the pointer is the latest-per-session resolver - seq is the
        # version the next save increments from (readers: latest_leaf_for_session).
        pointer_doc["seq"] = seq
        pointer_doc["chain_mode"] = CHAIN_MODE_V2
    _safe_sid = re.sub(r"[^A-Za-z0-9._-]+", "-", sid)[:12]
    (KNOTS / f"by-session_{_safe_sid}.json").write_text(
        json.dumps(pointer_doc, indent=2), encoding="utf-8"
    )
    session_pointer_v2(sid).write_text(json.dumps(pointer_doc, indent=2), encoding="utf-8")

    chain_row = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "filename": fname,
        "leaf_hash": leaf["leaf_hash"],
        "session_id": leaf.get("session_id"),
        "start_minute": leaf.get("start_minute"),
        "end_minute": leaf.get("end_minute"),
        "dominant_theme": leaf.get("dominant_theme"),
        "theme_vector_normalized": leaf.get("theme_vector_normalized"),
        "tension_index": leaf.get("tension_index"),
        "dossier_commit": leaf.get("dossier_commit"),
        "amended": existing_i is not None,
    }
    if mode == CHAIN_MODE_V2:
        chain_row["session_seq"] = seq
        chain_row["chain_mode"] = CHAIN_MODE_V2
        if prev_i is not None:  # V1_APPEND_ONLY: reference, never rewrite, the superseded row
            chain_row["supersedes_index"] = int(rows[prev_i].get("index", prev_i))
            chain_row["supersedes_leaf_hash"] = rows[prev_i].get("leaf_hash")
    if existing_i is not None:
        # CHAIN_REWRITE_GATE_20261019: v1 in-place amend rewrites the whole file.
        # Refuse unless MAG_ALLOW_CHAIN_REWRITE=1; prefer chain_mode=v2.
        if not _chain_rewrite_allowed():
            return {
                "ok": False,
                "schema": SCHEMA,
                "error": "v1 in-place amend refused: full-file rewrite gated "
                         "(use chain_mode=v2 append correction rows, or set "
                         "MAG_ALLOW_CHAIN_REWRITE=1 for operator repair)",
                "chain_mode": mode,
                "session_id": sid,
            }
        # PRESERVE repair/custom fields across amend (2026-08-25): a flagged
        # evidence_lost row being re-folded must NOT silently lose its flag.
        # The canary (chain_guard) caught exactly this - flags dropped
        # 1,039 -> 1,029 as normal folds amended flagged sessions. The fresh
        # chain_row below is built from a fixed field set, so carry forward
        # any repair fields present on the row being replaced.
        for _k in ("evidence_lost", "repaired_from_pointer"):
            if rows[existing_i].get(_k) is not None:
                chain_row[_k] = rows[existing_i][_k]
        rows[existing_i] = chain_row
        amended = True
        # AMEND (2026-08-16): history changes -> full rewrite is correct (rare, on re-summarize).
        all_hashes = _rewrite_chain(rows)
    else:
        rows.append(chain_row)
        amended = False
        # PURE APPEND (2026-08-16, Option A incremental): a new leaf does NOT require rewriting
        # every row's merkle root. Compute the new root ONCE (O(n), not O(n^2)) and append one line.
        # This was the 65s O(n^2) landmine (5,874 leaves -> ~34M sha256 on every append).
        all_hashes = [r.get("leaf_hash") for r in rows if r.get("leaf_hash")]
        root = _merkle_root(all_hashes) if all_hashes else _h(b"empty")
        parent_root = _merkle_root(all_hashes[:-1]) if len(all_hashes) > 1 else _h(b"empty")
        chain_row["index"] = len(all_hashes) - 1
        chain_row["n_leaves"] = len(all_hashes)
        chain_row["parent_verkle_root"] = parent_root
        chain_row["verkle_root"] = root
        CHAIN.parent.mkdir(parents=True, exist_ok=True)
        # B2-393 byte-exact chain law: newline="" disables the Windows text
        # translation that turns the appended \n into \r\n.
        _append_chain_line(json.dumps(chain_row, ensure_ascii=False))
        root = chain_row["verkle_root"]

    root = _merkle_root(all_hashes) if all_hashes else _h(b"empty")
    parent_root = (
        _merkle_root(all_hashes[:-1]) if len(all_hashes) > 1 else _h(b"empty")
    )

    tip = _tip_for_tail(rows, [str(h) for h in all_hashes if h], root)
    # AG5 (audit finding #3, 2026-09-30): the MAIN append path wrote the tip
    # with plain write_text while _write_tip_atomic existed for exactly the
    # torn-write disease (see comment at the consolidate call) - every fold
    # raced a tear window. Both main-path writes now go through the atomic
    # replace; proven by the monkeypatch spy in tests/test_ag5_tip_verify.py.
    _write_tip_atomic(tip)
    wrote_tail = tip.get("last_leaf_hash") == leaf.get("leaf_hash")
    _sync_latest_knot(tip.get("last_filename"), leaf if wrote_tail else None)

    # CHAIN_RACE_REPAIR_20260927: a same-second concurrent append (two
    # sessions, ts 2026-09-27T11:20:03Z) computed its root from a pre-race
    # read - committed a root missing the sibling row's leaf - and the
    # verify gate then refused EVERY append for hours (memlang anchoring
    # froze; 6 suite failures). Post-append self-verify turns the race
    # class into a self-healed chain: recompute the true root from DISK
    # rows (never the in-memory set the race poisoned) and rewrite this
    # row's root fields in place. Amends already ran _rewrite_chain over
    # the full file, so only the pure-append path needs the guard.
    if not amended:
        ok2, why2 = _verify_chain_consistent()
        if not ok2:
            disk_rows = _load_chain_rows()
            disk_hashes = [str(r.get("leaf_hash")) for r in disk_rows
                           if r.get("leaf_hash")]
            true_root = _merkle_root(disk_hashes) if disk_hashes else _h(b"empty")
            true_parent = (_merkle_root(disk_hashes[:-1])
                           if len(disk_hashes) > 1 else _h(b"empty"))
            healed = False
            for r in reversed(disk_rows):
                if str(r.get("session_id") or "") == sid:
                    if (r.get("verkle_root") != true_root
                            or r.get("parent_verkle_root") != true_parent):
                        r["verkle_root"] = true_root
                        r["parent_verkle_root"] = true_parent
                        r["n_leaves"] = len(disk_hashes)
                        healed = True
                    break
            if healed:
                # CHAIN_REWRITE_GATE_20261019: heal full-file rewrite
                if not _chain_rewrite_allowed():
                    return {
                        "ok": False,
                        "schema": SCHEMA,
                        "error": "post-append race detected; full-file heal rewrite gated "
                                 "(run tools/chain_repair.py with MAG_ALLOW_CHAIN_REWRITE=1)",
                        "chain_mode": mode,
                        "session_id": sid,
                        "leaf_hash": leaf.get("leaf_hash"),
                        "verify": why2,
                    }
                lines = [json.dumps(r, ensure_ascii=False) for r in disk_rows]
                tmp = CHAIN.with_suffix(".jsonl.tmp")
                tmp.write_text("\n".join(lines) + "\n", encoding="utf-8",
                               newline="")
                tmp.replace(CHAIN)
                tip2 = _tip_for_tail(disk_rows, disk_hashes, true_root)
                # AG5: heal-path tip write rides the same atomic replace as
                # the main path (tmp + os.replace) - no torn-write window here.
                _write_tip_atomic(tip2)
                root = true_root
                parent_root = true_parent

    # V2 shadow (2026-10-17, BINTREE_V2_SEED_SPEC): runs only after the v1 append + tip write are
    # complete; inert unless configs/mag.yaml chain_v2_shadow: true (env MAG_CHAIN_V2_SHADOW overrides).
    try:
        from mag import bintree_v2 as _bt2
        _bt2.shadow_append(chain_row, knot_path=path)
    except Exception as _e:  # noqa: BLE001 - v2 must never break a v1 write (A5: log outer failure)
        with contextlib.suppress(Exception):
            (ROOT / "memory/biography_v2/shadow_mismatch.jsonl").open("a", encoding="utf-8").write(json.dumps({"ts": _now_iso(), "kind": "outer_hook_exception", "error": f"{type(_e).__name__}: {_e}"}) + "\n")

    _update_topic_evolution(leaf, root, len(all_hashes), amend_session=sid)

    return {
        "ok": True,
        "amended": amended,
        "filename": fname,
        "path": str(path),
        "leaf_hash": leaf["leaf_hash"],
        "verkle_root": root,
        "parent_verkle_root": parent_root,
        "n_leaves": len(all_hashes),
        "chain_mode": mode,
        "session_seq": seq if mode == CHAIN_MODE_V2 else None,
        "chain": str(CHAIN),
        "tip": str(TIP),
        "evolution": str(EVOLUTION),
    }


def append_verkle_knot(dossier: dict[str, Any], pdf_path: str | None = None) -> dict[str, Any]:
    """Locked entry point - see _append_verkle_knot_unlocked for the real body.

    Single-writer lock makes chain read-modify-write + knot unlink + pointer
    write atomic against concurrent seats (the 2026-08-25 lost-update fix).
    """
    with verkle_lock():
        return _append_verkle_knot_unlocked(dossier, pdf_path)


def consolidate_chain_one_leaf_per_session() -> dict[str, Any]:
    """Locked entry point - see _consolidate_chain_one_leaf_per_session_unlocked."""
    # CHAIN_REWRITE_GATE_20261019: consolidate is whole-file rewrite tooling.
    if not _chain_rewrite_allowed():
        return {
            "ok": False,
            "skipped": True,
            "error": "consolidate refused: set MAG_ALLOW_CHAIN_REWRITE=1 "
                     "(and hold chain:biography lease) for operator rewrite",
        }
    try:
        from mag.leases import guard as _lease_guard

        _g = _lease_guard("chain:biography", "verkle_knot.consolidate", enforce="conflict")
        if not _g.get("allowed", True):
            return {"ok": False, "skipped": True, "error": _g.get("reason") or "lease refused"}
    except PermissionError:
        raise
    except Exception as e:  # noqa: BLE001 - unreadable lease state fails closed for consolidate
        return {"ok": False, "skipped": True, "error": f"lease guard failed: {type(e).__name__}: {e}"}
    with verkle_lock():
        return _consolidate_chain_one_leaf_per_session_unlocked()


def _update_topic_evolution(
    leaf: dict[str, Any],
    root: str,
    n: int,
    *,
    amend_session: str | None = None,
) -> None:
    """Maintain series of theme vectors - one row per session (amend if present)."""
    data: dict[str, Any]
    if EVOLUTION.is_file():
        try:
            data = json.loads(EVOLUTION.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    data["schema"] = "topic_evolution.v1"
    data["theme_basis"] = THEME_BASIS
    data["verkle_root"] = root
    data["n_leaves"] = n
    series: list[dict[str, Any]] = list(data.get("series") or [])
    point = {
        "filename": leaf.get("filename"),
        "session_id": leaf.get("session_id"),
        "start_minute": leaf.get("start_minute"),
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
