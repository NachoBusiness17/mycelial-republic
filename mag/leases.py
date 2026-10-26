"""leases: time-limited, holder-keeps leases on the RESTRICTED LIST (2026-10-17).

Doctrine: watch/LIBRARY/FLEET_COORDINATION_DOCTRINE_20261017.md, P1
(restrictive fire-support coordination measures / EMCON windows; COLREGs
stand-on vs give-way). The few things that break the fleet when two seats touch
them at once are named in configs/restricted_leases.json; only those names take
a lease. Everything else stays free (permissive by default).

  acquire(resource, seat, purpose, ttl_s)  -> lease_token (shown ONCE)
  renew(resource, seat, lease_token, ttl_s)
  release(resource, seat, lease_token)
  transfer(resource, seat, lease_token, to_seat) -> new lease_token for to_seat
  status(resource) / list_leases() / check(resource, seat, lease_token)
  guard(resource, op, enforce=...)   the structural hook for gated scripts

LAWS
- Holder keeps. A live lease is never taken over by acquire: a newcomer is
  REFUSED with who holds it, why, and until when (the newcomer gives way).
  Expiry is the only automatic end; an expired lease is superseded on the next
  acquire and the supersession is logged.
- Time, not pids. Seats run in containers and on the host, so pid liveness
  cannot be trusted across them (same reason the verkle lock carries a
  heartbeat record): leases are TTL-bounded and renewed by the holder.
- The raw lease_token never lands on disk; the lease file keeps its sha256.
- Per-resource mutex: O_CREAT|O_EXCL claim (tools/instance_guard.py pattern)
  with a stale break after MUTEX_STALE_S; the lease file is written tmp +
  os.replace so a reader never sees half a lease.
- Store: watch/receipts/leases/ (the ONE writable bind mount of the mag-mcp
  container, so container-served MCP tools and host CLIs share one ledger).
  Every event appends a line to ledger.jsonl; a fence number increments on
  every acquire/transfer so a stale holder can be told apart.
- break_lease() is operator-only (CLI scripts/lease.py break, never MCP) and
  is logged with a reason.

Schema: lease.v1 · stdlib only
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "lease.v1"
CONFIG_PATH = ROOT / "configs" / "restricted_leases.json"
LEASE_DIR = ROOT / "watch" / "receipts" / "leases"
SEAT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$")  # == estate_bridge.SHARED_SEAT_RE
MIN_TTL_S = 60
MUTEX_STALE_S = 15.0
PURPOSE_CAP = 300
ENV_SEAT = "MAG_LEASE_SEAT"
ENV_TOKEN = "MAG_LEASE_TOKEN"


class LeaseError(ValueError):
    """Bad lease call (unknown resource, bad seat, wrong token). In-band for MCP."""


# ─────────────────────────────── config ────────────────────────────────────

def load_config() -> dict[str, Any]:
    doc = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    res = doc.get("resources")
    if not isinstance(res, dict) or not res:
        raise LeaseError(f"{CONFIG_PATH.name}: no resources")
    return doc


def restricted() -> dict[str, dict[str, Any]]:
    return load_config()["resources"]


def _resource(name: str) -> dict[str, Any]:
    res = restricted()
    if not isinstance(name, str) or name not in res:
        raise LeaseError(f"not on the restricted list: {name!r}; leasable: {sorted(res)}")
    return res[name]


def resource_for_path(rel_path: str) -> list[str]:
    """Which restricted resources cover a repo-relative path (glob match only)."""
    p = str(rel_path).replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    hits = []
    for name, spec in restricted().items():
        for pat in spec.get("paths") or []:
            if fnmatch.fnmatch(p, pat) or (pat.endswith("/**") and p.startswith(pat[:-3] + "/")):
                hits.append(name)
                break
    return hits


# ─────────────────────────────── helpers ───────────────────────────────────

def _now() -> float:
    return time.time()


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slug(resource: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", resource)


def _lease_path(resource: str) -> Path:
    return LEASE_DIR / f"{_slug(resource)}.json"


def _sha(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _seat(seat: Any, field: str = "seat") -> str:
    if not isinstance(seat, str) or not SEAT_RE.match(seat):
        raise LeaseError(f"{field} must match {SEAT_RE.pattern}")
    return seat


def _ttl(spec: dict[str, Any], ttl_s: Any) -> int:
    default = int(spec.get("default_ttl_s", 1800))
    cap = int(spec.get("max_ttl_s", 14400))
    if ttl_s in (None, "", 0):
        return default
    try:
        val = int(ttl_s)
    except (TypeError, ValueError) as e:
        raise LeaseError("ttl_s must be an integer number of seconds") from e
    if val < MIN_TTL_S or val > cap:
        raise LeaseError(f"ttl_s must be {MIN_TTL_S}..{cap}")
    return val


def _purpose(purpose: Any) -> str:
    text = str(purpose or "").strip()
    if not text:
        raise LeaseError("purpose required (say what you are about to do)")
    from mag.warm_surface import redact_text

    return redact_text(text)[:PURPOSE_CAP]


def _read(resource: str) -> dict[str, Any] | None:
    try:
        return json.loads(_lease_path(resource).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _live(rec: dict[str, Any] | None, now: float | None = None) -> bool:
    return bool(rec) and rec.get("state") == "held" and float(rec.get("expires_ts", 0)) > (now or _now())


def _write(resource: str, rec: dict[str, Any]) -> None:
    LEASE_DIR.mkdir(parents=True, exist_ok=True)
    target = _lease_path(resource)
    tmp = target.with_name(f".{target.name}.{os.getpid()}.{secrets.token_hex(3)}.tmp")
    tmp.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, target)


def _ledger(event: str, resource: str, **fields: Any) -> None:
    LEASE_DIR.mkdir(parents=True, exist_ok=True)
    row = {"schema": "lease_ledger.v1", "ts": _iso(_now()), "event": event,
           "resource": resource, **fields}
    with open(LEASE_DIR / "ledger.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


class _Mutex:
    """O_EXCL claim file per resource (instance_guard pattern), stale-broken."""

    def __init__(self, resource: str, wait_s: float = 5.0):
        self.path = LEASE_DIR / f".{_slug(resource)}.mutex"
        self.wait_s = wait_s
        self.fd: int | None = None

    def __enter__(self) -> "_Mutex":
        LEASE_DIR.mkdir(parents=True, exist_ok=True)
        deadline = _now() + self.wait_s
        while True:
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(self.fd, f"{os.getpid()} {_now():.3f}".encode())
                return self
            except FileExistsError:
                try:
                    if _now() - self.path.stat().st_mtime > MUTEX_STALE_S:
                        self.path.unlink()
                        continue
                except OSError:
                    continue
                if _now() > deadline:
                    raise LeaseError("lease mutex busy; retry in a few seconds")
                time.sleep(0.05)

    def __exit__(self, *exc: Any) -> None:
        if self.fd is not None:
            os.close(self.fd)
        try:
            self.path.unlink()
        except OSError:
            pass


def _public(rec: dict[str, Any] | None, now: float | None = None) -> dict[str, Any] | None:
    if not rec:
        return None
    now = now or _now()
    out = {k: v for k, v in rec.items() if k != "token_sha256"}
    out["live"] = _live(rec, now)
    out["remaining_s"] = max(0, int(float(rec.get("expires_ts", 0)) - now)) if out["live"] else 0
    return out


def _refusal(resource: str, rec: dict[str, Any], now: float, asker: str) -> dict[str, Any]:
    return {
        "ok": False, "refused": True, "resource": resource,
        "holder": rec.get("seat"), "purpose": rec.get("purpose"),
        "until": rec.get("expires_at"),
        "remaining_s": max(0, int(float(rec["expires_ts"]) - now)),
        "asker": asker,
        "how": (f"held by {rec.get('seat')} until {rec.get('expires_at')} (UTC). Holder keeps: "
                "wait for expiry or release, or ask the holder to transfer to you "
                "(estate_lease_transfer). File a fleet report if it is blocking."),
    }


def _verify(resource: str, rec: dict[str, Any] | None, seat: str, lease_token: Any,
            now: float) -> dict[str, Any]:
    if not _live(rec, now):
        raise LeaseError(f"no live lease on {resource} (expired or released); acquire again")
    assert rec is not None
    if rec.get("seat") != seat:
        raise LeaseError(f"{resource} is held by {rec.get('seat')}, not {seat}")
    if not isinstance(lease_token, str) or not secrets.compare_digest(
            _sha(lease_token), str(rec.get("token_sha256"))):
        raise LeaseError("lease_token does not match the live lease")
    return rec


# ─────────────────────────────── API ───────────────────────────────────────

def acquire(*, resource: str, seat: str, purpose: str, ttl_s: int | None = None) -> dict[str, Any]:
    """Take a restricted resource for ttl_s seconds; refused (with who/until) if held."""
    spec = _resource(resource)
    seat = _seat(seat)
    ttl = _ttl(spec, ttl_s)
    purpose = _purpose(purpose)
    with _Mutex(resource):
        now = _now()
        prior = _read(resource)
        if _live(prior, now):
            assert prior is not None
            out = _refusal(resource, prior, now, seat)
            if prior.get("seat") == seat:
                out["how"] = ("you already hold this lease: renew it with your lease_token "
                              "(estate_lease_renew), or release it first")
            _ledger("refused", resource, seat=seat, holder=prior.get("seat"),
                    until=prior.get("expires_at"))
            return out
        token = secrets.token_urlsafe(24)
        fence = int((prior or {}).get("fence", 0)) + 1
        rec = {
            "schema": SCHEMA, "resource": resource, "state": "held", "seat": seat,
            "purpose": purpose, "acquired_at": _iso(now), "renewed_at": _iso(now),
            "expires_ts": now + ttl, "expires_at": _iso(now + ttl), "ttl_s": ttl,
            "fence": fence, "token_sha256": _sha(token), "enforce": spec.get("enforce", "advisory"),
        }
        _write(resource, rec)
        if prior and prior.get("state") == "held":
            _ledger("expired_superseded", resource, seat=prior.get("seat"),
                    expired_at=prior.get("expires_at"), by=seat)
        _ledger("acquired", resource, seat=seat, purpose=purpose, until=rec["expires_at"],
                fence=fence)
    return {"ok": True, "resource": resource, "seat": seat, "until": rec["expires_at"],
            "ttl_s": ttl, "fence": fence, "lease_token": token,
            "note": "lease_token is shown ONCE (only its sha256 is stored). Keep it for "
                    "renew/release/transfer; scripts read it from env MAG_LEASE_SEAT + MAG_LEASE_TOKEN."}


def renew(*, resource: str, seat: str, lease_token: str, ttl_s: int | None = None) -> dict[str, Any]:
    """Extend YOUR live lease by ttl_s from now (holder only)."""
    spec = _resource(resource)
    seat = _seat(seat)
    ttl = _ttl(spec, ttl_s)
    with _Mutex(resource):
        now = _now()
        rec = _verify(resource, _read(resource), seat, lease_token, now)
        rec.update(renewed_at=_iso(now), expires_ts=now + ttl, expires_at=_iso(now + ttl), ttl_s=ttl)
        _write(resource, rec)
        _ledger("renewed", resource, seat=seat, until=rec["expires_at"], fence=rec.get("fence"))
    return {"ok": True, "resource": resource, "seat": seat, "until": rec["expires_at"],
            "fence": rec.get("fence")}


def release(*, resource: str, seat: str, lease_token: str, note: str = "") -> dict[str, Any]:
    """Give the resource back (holder only)."""
    _resource(resource)
    seat = _seat(seat)
    with _Mutex(resource):
        now = _now()
        rec = _verify(resource, _read(resource), seat, lease_token, now)
        rec.update(state="released", released_at=_iso(now), expires_ts=now, expires_at=_iso(now))
        _write(resource, rec)
        _ledger("released", resource, seat=seat, fence=rec.get("fence"),
                note=str(note)[:PURPOSE_CAP])
    return {"ok": True, "resource": resource, "released_by": seat, "at": _iso(now)}


def transfer(*, resource: str, seat: str, lease_token: str, to_seat: str,
             ttl_s: int | None = None, purpose: str = "") -> dict[str, Any]:
    """Hand YOUR live lease to another seat; a new lease_token is minted for them."""
    spec = _resource(resource)
    seat = _seat(seat)
    to_seat = _seat(to_seat, "to_seat")
    if to_seat == seat:
        raise LeaseError("to_seat is you; use renew")
    with _Mutex(resource):
        now = _now()
        rec = _verify(resource, _read(resource), seat, lease_token, now)
        ttl = _ttl(spec, ttl_s) if ttl_s else max(MIN_TTL_S, int(float(rec["expires_ts"]) - now))
        token = secrets.token_urlsafe(24)
        new = dict(rec)
        new.update(seat=to_seat, acquired_at=_iso(now), renewed_at=_iso(now),
                   expires_ts=now + ttl, expires_at=_iso(now + ttl), ttl_s=ttl,
                   fence=int(rec.get("fence", 0)) + 1, token_sha256=_sha(token),
                   transferred_from=seat,
                   purpose=_purpose(purpose) if purpose else rec.get("purpose"))
        _write(resource, new)
        _ledger("transferred", resource, seat=seat, to_seat=to_seat, until=new["expires_at"],
                fence=new["fence"])
    return {"ok": True, "resource": resource, "from": seat, "to": to_seat,
            "until": new["expires_at"], "fence": new["fence"], "lease_token": token,
            "note": f"deliver this lease_token to {to_seat}; the old token is dead"}


def status(*, resource: str) -> dict[str, Any]:
    spec = _resource(resource)
    rec = _read(resource)
    return {"ok": True, "resource": resource, "description": spec.get("description"),
            "enforce": spec.get("enforce", "advisory"), "lease": _public(rec)}


def list_leases(include_free: bool = True) -> dict[str, Any]:
    """Every restricted resource and its lease state (the warm board view)."""
    now = _now()
    rows = []
    for name, spec in restricted().items():
        pub = _public(_read(name), now)
        live = bool(pub and pub["live"])
        if not live and not include_free:
            continue
        rows.append({
            "resource": name, "state": "held" if live else "free",
            "holder": pub.get("seat") if live else None,
            "purpose": pub.get("purpose") if live else None,
            "until": pub.get("expires_at") if live else None,
            "remaining_s": pub.get("remaining_s") if live else 0,
            "fence": (pub or {}).get("fence", 0),
            "enforce": spec.get("enforce", "advisory"),
            "description": spec.get("description"),
        })
    return {"ok": True, "schema": "lease_board.v1", "read_at": _iso(now),
            "held": sum(1 for r in rows if r["state"] == "held"), "leases": rows,
            "how": "estate_lease_acquire(resource, seat, purpose, ttl_s) -> lease_token; "
                   "renew/release/transfer with it. CLI: python scripts/lease.py --help"}


def tool_leases() -> dict[str, Any]:
    """MCP read: the restricted list and who holds what, until when."""
    return list_leases()


def check(*, resource: str, seat: str | None = None, lease_token: str | None = None) -> dict[str, Any]:
    """Does (seat, lease_token) hold resource now? Never raises on a mismatch."""
    _resource(resource)
    now = _now()
    rec = _read(resource)
    live = _live(rec, now)
    holds = False
    if live and seat and lease_token and rec and rec.get("seat") == seat:
        holds = secrets.compare_digest(_sha(lease_token), str(rec.get("token_sha256")))
    return {"resource": resource, "held": live, "holder": rec.get("seat") if live and rec else None,
            "until": rec.get("expires_at") if live and rec else None, "holds": holds}


def break_lease(*, resource: str, operator: str, reason: str) -> dict[str, Any]:
    """OPERATOR break of a live lease (CLI only, never exposed over MCP); logged."""
    _resource(resource)
    operator = _seat(operator, "operator")
    if not str(reason or "").strip():
        raise LeaseError("reason required to break a lease")
    with _Mutex(resource):
        now = _now()
        rec = _read(resource)
        if not _live(rec, now):
            return {"ok": True, "resource": resource, "note": "no live lease"}
        assert rec is not None
        prior = rec.get("seat")
        rec.update(state="broken", broken_by=operator, broken_at=_iso(now),
                   broken_reason=str(reason)[:PURPOSE_CAP], expires_ts=now, expires_at=_iso(now))
        _write(resource, rec)
        _ledger("broken", resource, seat=prior, operator=operator, reason=str(reason)[:PURPOSE_CAP])
    return {"ok": True, "resource": resource, "broken_holder": prior, "by": operator}


# ─────────────────────────────── structural guard ──────────────────────────

def guard(resource: str, op: str, *, enforce: str = "warn", seat: str | None = None,
          lease_token: str | None = None) -> dict[str, Any]:
    """The hook gated scripts call before touching a restricted resource.

    enforce:
      "warn"     never refuse; log (stderr + ledger) when unleased or held by another.
      "conflict" refuse ONLY when another seat holds a live lease; unleased = warn.
      "require"  refuse unless the caller (env MAG_LEASE_SEAT/MAG_LEASE_TOKEN or
                 args) holds the live lease.
    Returns {"allowed": bool, "reason": str, ...}. Never raises on lease state;
    a broken config degrades to allowed+warning for warn/conflict.
    """
    seat = seat or os.environ.get(ENV_SEAT) or None
    lease_token = lease_token or os.environ.get(ENV_TOKEN) or None
    in_test = bool(os.environ.get("PYTEST_CURRENT_TEST"))
    try:
        st = check(resource=resource, seat=seat, lease_token=lease_token)
    except Exception as e:  # noqa: BLE001 — a guard must not crash its caller
        allowed = enforce != "require"
        msg = f"lease guard {resource}/{op}: lease state unreadable ({type(e).__name__}: {e})"
        print(f"[lease] {msg}", file=sys.stderr)
        return {"allowed": allowed, "reason": msg, "resource": resource, "op": op}
    if st["holds"]:
        if not in_test:
            _safe_ledger("guard_pass", resource, seat=seat, op=op)
        return {"allowed": True, "reason": f"{seat} holds {resource}", **st, "op": op}
    other = st["held"]
    if enforce == "require" or (enforce == "conflict" and other):
        why = (f"{resource} held by {st['holder']} until {st['until']} (UTC)" if other
               else f"{resource} requires a held lease (env {ENV_SEAT} + {ENV_TOKEN})")
        if not in_test:
            _safe_ledger("guard_refused", resource, seat=seat, op=op, holder=st["holder"])
        return {"allowed": False, "reason": f"REFUSED {op}: {why}", **st, "op": op,
                "how": f"python scripts/lease.py acquire {resource} --seat <you> --purpose \"...\""}
    why = (f"{resource} is held by {st['holder']} until {st['until']} (UTC); proceeding (warn-only)"
           if other else f"{resource} not leased; proceeding (warn-only). Take the lease first next time.")
    print(f"[lease] WARN {op}: {why}", file=sys.stderr)
    if not in_test:
        _safe_ledger("guard_warn", resource, seat=seat, op=op, holder=st["holder"])
    return {"allowed": True, "reason": f"WARN {op}: {why}", **st, "op": op}


def _safe_ledger(event: str, resource: str, **fields: Any) -> None:
    try:
        _ledger(event, resource, **fields)
    except OSError:
        pass


# ─────────────────────────────── MCP input schemas ─────────────────────────
_SEAT_SCHEMA = {"type": "string", "pattern": SEAT_RE.pattern, "description": "your seat name"}
_RES_SCHEMA = {"type": "string",
               "description": "a restricted-list resource (configs/restricted_leases.json): "
                              "chain:biography, file:mag/verkle_knot.py, proc:lab, "
                              "file:docker-compose.yml, keys:names"}
_TOKEN_SCHEMA = {"type": "string", "description": "the lease_token acquire/transfer returned"}
INPUT_SCHEMAS: dict[str, Any] = {
    "estate_lease_acquire": {
        "type": "object",
        "properties": {"resource": _RES_SCHEMA, "seat": _SEAT_SCHEMA,
                       "purpose": {"type": "string", "maxLength": PURPOSE_CAP},
                       "ttl_s": {"type": "integer", "minimum": MIN_TTL_S, "maximum": 14400}},
        "required": ["resource", "seat", "purpose"],
    },
    "estate_lease_renew": {
        "type": "object",
        "properties": {"resource": _RES_SCHEMA, "seat": _SEAT_SCHEMA, "lease_token": _TOKEN_SCHEMA,
                       "ttl_s": {"type": "integer", "minimum": MIN_TTL_S, "maximum": 14400}},
        "required": ["resource", "seat", "lease_token"],
    },
    "estate_lease_release": {
        "type": "object",
        "properties": {"resource": _RES_SCHEMA, "seat": _SEAT_SCHEMA, "lease_token": _TOKEN_SCHEMA,
                       "note": {"type": "string", "maxLength": PURPOSE_CAP}},
        "required": ["resource", "seat", "lease_token"],
    },
    "estate_lease_transfer": {
        "type": "object",
        "properties": {"resource": _RES_SCHEMA, "seat": _SEAT_SCHEMA, "lease_token": _TOKEN_SCHEMA,
                       "to_seat": _SEAT_SCHEMA,
                       "ttl_s": {"type": "integer", "minimum": MIN_TTL_S, "maximum": 14400},
                       "purpose": {"type": "string", "maxLength": PURPOSE_CAP}},
        "required": ["resource", "seat", "lease_token", "to_seat"],
    },
    "estate_leases": {"type": "object", "properties": {}},
}
