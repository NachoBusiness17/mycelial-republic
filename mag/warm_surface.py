"""warm_surface: the shared-surface warm pack as FIXED MCP resources (2026-10-17).

Operator ask (2026-10-17, "don't reinvent the wheel"): one surface every seat
(Grok, Gemini, DeepSeek, ZCode, Hermes, free models) connects to and boots
pre-warmed. Self-steal receipt: watch/LIBRARY/SHARED_SURFACE_SELFSTEAL_20261017.md.
This module is the small adapter that plan names; it builds nothing new:

  mag://warm/tip            memory/biography/verkle_tip.json, read LIVE per call
                            (the chain writer rewrites it on every knot)
  mag://warm/state          memory/warm_state.json (hermes_warm_boot, daily via
                            MagBootRegenDaily) + its lag behind the live tip
  mag://warm/zknot          memory/zknot/LATEST.md
  mag://warm/library-index  watch/LIBRARY/INDEX.md (listed only when present)
  mag://warm/laws           rule/invariant cards from memory/rib_boot.json
                            (core_laws + vault law ribs + SUPERSEDED pointer)
  mag://warm/preamble/<seat>  a format_agent_preamble-style per-seat boot text
                            for each seat in SEATS (fixed set, not a path)
  mag://warm/leases         restricted-list lease board (mag/leases.py): who
                            holds what, until when (2026-10-17)
  mag://warm/notices        fleet notices in force until cancelled, each with
                            its ACKs (mag/fleet_report.py, 2026-10-17)

LAWS:
- Fixed URIs only. No caller-supplied path ever reaches the filesystem; an
  unknown URI raises KeyError (mcp_server maps it to an in-band JSON-RPC error).
- Every body goes through estate_bridge._redact (credential-named fields
  dropped, key-shaped strings masked) and then redact_text (more token shapes,
  private-key blocks, KEY=value lines, tailnet IPs, the absolute repo path).
- Read-only. Nothing here writes a byte. The write-back path is
  estate_bridge.shared_receipt_append (watch/receipts/ only).
- The preamble is composed from the resources above rather than by calling
  context_pack.format_agent_preamble(), because that builds a full context pack
  (heavy, and its overflow path appends to watch/inbox/PACK_OFFLOAD.jsonl, which
  is read-only inside the mag-mcp container). The contract lines are the same.

Schema: warm_surface.v1 · stdlib-only
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "warm_surface.v1"
URI_PREFIX = "mag://warm/"
BODY_CAP = 65536  # characters per resource body; overflow is cut with a marker

TIP = ROOT / "memory" / "biography" / "verkle_tip.json"
WARM_STATE = ROOT / "memory" / "warm_state.json"
ZKNOT = ROOT / "memory" / "zknot" / "LATEST.md"
LIBRARY_INDEX = ROOT / "watch" / "LIBRARY" / "INDEX.md"
RIB_BOOT = ROOT / "memory" / "rib_boot.json"

# The seats that get a fixed preamble URI. A seat outside this set uses
# "free" (any free/unnamed model) - never a caller-built URI.
SEATS: tuple[str, ...] = ("grok", "gemini", "deepseek", "zcode", "hermes",
                          "codex", "cursor", "claude", "free")

# ─────────────────────────────── redaction ────────────────────────────────

_EXTRA_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
                re.S), "<redacted-private-key>"),
    (re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}"), "<redacted>"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), "<redacted>"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "<redacted>"),
    (re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}"), "<redacted>"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "<redacted>"),
    (re.compile(r"\b(?:hf|gsk|pk|rk)_[A-Za-z0-9]{20,}"), "<redacted>"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "<redacted-jwt>"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}"), "Bearer <redacted>"),
    (re.compile(r"(?i)\b([A-Z0-9_]*(?:API_?KEY|SECRET|TOKEN|PASSWORD|PASSWD|AUTHKEY)[A-Z0-9_]*)"
                r"(\s*[=:]\s*)['\"]?[^\s'\",}]{6,}['\"]?"), r"\1\2<redacted>"),
    # Tailscale CGNAT range 100.64.0.0/10: a node address is a door, not data.
    (re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b"), "<tailnet-ip>"),
)


_HOME_RE = re.compile(r"(?i)\b[A-Z]:(?:\\{1,2}|/)Users(?:\\{1,2}|/)[^\\/\s\"'<>]+"
                      r"|/home/[^/\s\"'<>]+|/Users/[^/\s\"'<>]+")


def _root_variants() -> list[str]:
    raw = str(ROOT)
    out = {raw, raw.replace("\\", "/"), raw.replace("\\", "\\\\")}
    return sorted((v for v in out if len(v) > 3), key=len, reverse=True)


def redact_text(text: str) -> str:
    """Mask secret-shaped substrings in free text and hide the absolute repo path.

    Layered on estate_bridge._redact (which only knows sk-/nous-/xai-/or- keys
    and credential-named dict fields); idempotent.
    """
    from mag.estate_bridge import _redact

    out = _redact(str(text))
    for pattern, repl in _EXTRA_PATTERNS:
        out = pattern.sub(repl, out)
    for variant in _root_variants():
        out = out.replace(variant, "<repo>")
    # Any other absolute home path (sibling projects, AppData): the account
    # name and layout are host detail, not shared context.
    out = _HOME_RE.sub("<home>", out)
    return out


def redact_obj(value: Any) -> Any:
    """estate_bridge._redact on structure, then redact_text on every string."""
    from mag.estate_bridge import _redact

    def walk(v: Any) -> Any:
        if isinstance(v, dict):
            return {k: walk(x) for k, x in v.items()}
        if isinstance(v, list):
            return [walk(x) for x in v]
        if isinstance(v, str):
            return redact_text(v)
        return v

    return walk(_redact(value))


# ─────────────────────────────── readers ──────────────────────────────────

def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def _mtime_iso(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
    except OSError:
        return None


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _cap(text: str, cap: int = BODY_CAP) -> str:
    if len(text) <= cap:
        return text
    return text[:cap] + f"\n... [warm_surface cut at {cap} chars of {len(text)}]\n"


def _missing(path: Path) -> dict[str, Any]:
    return {"ok": False, "error": "missing_or_unreadable", "path": _rel(path)}


def tip() -> dict[str, Any]:
    """The live verkle tip (re-read on every call) with its age."""
    data = _load_json(TIP)
    if data is None:
        return _missing(TIP)
    now = datetime.now(timezone.utc)
    age_s = None
    stamp = data.get("updated_minute")
    if isinstance(stamp, str):
        try:
            age_s = round((now - datetime.fromisoformat(stamp.replace("Z", "+00:00"))).total_seconds())
        except ValueError:
            age_s = None
    return {
        "ok": True,
        "schema": "warm_tip.v1",
        "source": _rel(TIP) + " (read live)",
        "read_at": now.isoformat(),
        "age_s": age_s,
        "root": data.get("root"),
        "root_short": str(data.get("root") or "")[:16],
        "n_leaves": data.get("n_leaves"),
        "last_filename": data.get("last_filename"),
        "last_leaf_hash": data.get("last_leaf_hash"),
        "last_session_id": data.get("last_session_id"),
        "updated_minute": stamp,
        "tip_schema": data.get("schema"),
    }


def warm_state() -> dict[str, Any]:
    data = _load_json(WARM_STATE)
    if data is None:
        return _missing(WARM_STATE)
    live = tip()
    chain = data.get("chain") or {}
    lag = None
    if live.get("ok") and isinstance(live.get("n_leaves"), int) and isinstance(chain.get("n_leaves"), int):
        lag = live["n_leaves"] - chain["n_leaves"]
    return {
        "ok": True,
        "schema": "warm_state_view.v1",
        "source": _rel(WARM_STATE),
        "file_mtime": _mtime_iso(WARM_STATE),
        "leaves_behind_live_tip": lag,
        "regen": "MagBootRegenDaily -> mag/boot_regen.py (daily); live tip at mag://warm/tip",
        "warm_state": data,
    }


def laws() -> dict[str, Any]:
    """Rule/invariant cards from rib_boot.json (read-only mount of the vault)."""
    data = _load_json(RIB_BOOT)
    if data is None:
        return _missing(RIB_BOOT)
    vault = data.get("vault") or {}
    law_ribs = []
    for rib in vault.get("law_ribs") or []:
        if isinstance(rib, dict):
            law_ribs.append({
                "file": rib.get("file"),
                "law_head": rib.get("law_head"),
                "law_amendments": rib.get("law_amendments") or [],
                "amendment_count": rib.get("amendment_count"),
            })
    return {
        "ok": True,
        "schema": "warm_laws.v1",
        "source": _rel(RIB_BOOT),
        "rib_boot_ts": data.get("ts"),
        "read_only": data.get("read_only"),
        "core_laws": data.get("core_laws") or [],
        "law_ribs": law_ribs,
        "vault_md_count": data.get("vault_md_count"),
        "superseded_register": data.get("superseded_register"),
        "note": "cards are a read-only mount; amendments ride after the head "
                "(amend-never-rewrite). Demotions: memory/fold_history/SUPERSEDED.md",
    }


def _law_bullets(max_items: int = 12) -> list[str]:
    cards = laws()
    out = []
    for row in (cards.get("core_laws") or [])[:max_items]:
        if isinstance(row, dict):
            out.append(f"- [{row.get('id')}] {row.get('law')}")
        elif isinstance(row, str):
            out.append(f"- {row}")
    return out or ["- (rib_boot.json unavailable: read mag://warm/laws)"]


def leases_board() -> dict[str, Any]:
    """The restricted-list lease board (mag/leases.py); never raises."""
    try:
        from mag.leases import list_leases

        return list_leases()
    except Exception as e:  # noqa: BLE001 — a board read must not break the pack
        return {"ok": False, "error": f"lease board unavailable: {type(e).__name__}: {e}"}


def notices_board() -> dict[str, Any]:
    """Fleet notices in force + ACKs (mag/fleet_report.py); never raises."""
    try:
        from mag.fleet_report import notices

        return notices()
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"notices unavailable: {type(e).__name__}: {e}"}


def _board_lines() -> list[str]:
    out: list[str] = []
    lb = leases_board()
    held = [r for r in lb.get("leases") or [] if r.get("state") == "held"]
    for r in held:
        out.append(f"- LEASE {r.get('resource')} held by {r.get('holder')} until "
                   f"{r.get('until')} UTC ({r.get('purpose')})")
    if lb.get("ok") and not held:
        out.append("- no restricted-list leases held (mag://warm/leases)")
    nb = notices_board()
    for n in (nb.get("in_force") or [])[:8]:
        out.append(f"- NOTICE {n.get('notice_id')} [{n.get('category')}] {n.get('subject')} "
                   f"(acks: {len(n.get('acks') or [])})")
    if nb.get("ok") and not nb.get("in_force"):
        out.append("- no notices in force (mag://warm/notices)")
    return out or ["- (fleet board unavailable)"]


def preamble(seat: str) -> str:
    """format_agent_preamble-style boot text for one seat (fixed seat set)."""
    if seat not in SEATS:
        raise KeyError(f"unknown seat preamble: {seat!r} (known: {', '.join(SEATS)})")
    t = tip()
    ws = warm_state()
    if t.get("ok"):
        tip_line = (f"tip={t.get('root_short')} leaves={t.get('n_leaves')} "
                    f"last={t.get('last_filename')} age_s={t.get('age_s')}")
    else:
        tip_line = "tip=unavailable (read mag://warm/tip)"
    zk = _read_text(ZKNOT) or "(zknot LATEST unavailable)"
    zk_head = zk[:1200] + ("…" if len(zk) > 1200 else "")
    lines = [
        f"# Mag shared-surface preamble · seat={seat}",
        f"# ts={datetime.now(timezone.utc).isoformat()[:19]}Z · schema={SCHEMA} · law=COORDINATION_ELIAS_ROPE",
        "",
        "## Contract",
        "- Trust this pack + your task boundary. Do not invent body/keys/status.",
        "- Do not load full residual or chat history. Deep probe only if task requires a path.",
        "- chain=record, window=reasoning surface. Never store the window as truth.",
        "- Remotes: pack+goal only. No T0/T1 private archive paths. No secrets cross this surface.",
        "",
        "## Chain tip (live)",
        f"- {tip_line}",
        f"- warm_state leaves behind live tip: {ws.get('leaves_behind_live_tip')}",
        "",
        "## Rule / invariant cards (head; full set at mag://warm/laws)",
        *_law_bullets(),
        "",
        "## Latest notes (zknot LATEST head; full at mag://warm/zknot)",
        zk_head.strip(),
        "",
        "## Fleet board (leases held + notices in force)",
        *_board_lines(),
        "",
        "## Doors",
        "- resources: mag://warm/tip · mag://warm/state · mag://warm/zknot · mag://warm/laws"
        + (" · mag://warm/library-index" if LIBRARY_INDEX.is_file() else ""),
        "- tool estate_warm_read(uri) returns the same bodies for clients without resources.",
        f"- file results with tool estate_shared_receipt(seat=\"{seat}\", model=\"<your model id>\", "
        "title=\"...\", body=\"...\") -> watch/receipts/ only (server stamps ts + sha256).",
        "- mag://warm/leases (who holds the restricted list) · mag://warm/notices (in force "
        "until cancelled; ACK each one).",
        f"- report with estate_fleet_report(seat=\"{seat}\", kind=\"SPOTREP|SITREP|NOTICE|RELIEF|ACK\", "
        "report={...}); before touching a restricted resource take estate_lease_acquire.",
    ]
    return "\n".join(lines) + "\n"


# ─────────────────────────────── MCP surface ──────────────────────────────

_STATIC: dict[str, tuple[str, str, str]] = {
    # uri: (name, mimeType, description)
    URI_PREFIX + "tip": ("chain-tip", "application/json",
                         "live verkle chain tip (memory/biography/verkle_tip.json, re-read per call)"),
    URI_PREFIX + "state": ("warm-state", "application/json",
                           "memory/warm_state.json (daily regen) + leaves behind the live tip"),
    URI_PREFIX + "zknot": ("zknot-latest", "text/markdown", "memory/zknot/LATEST.md (latest notes)"),
    URI_PREFIX + "library-index": ("library-index", "text/markdown",
                                   "watch/LIBRARY/INDEX.md (the watch library catalog)"),
    URI_PREFIX + "laws": ("law-cards", "application/json",
                          "rule/invariant cards from memory/rib_boot.json"),
    URI_PREFIX + "leases": ("lease-board", "application/json",
                            "restricted-list leases: who holds what, until when "
                            "(configs/restricted_leases.json)"),
    URI_PREFIX + "notices": ("fleet-notices", "application/json",
                             "fleet notices in force until cancelled, with their ACKs"),
}


def resource_uris() -> list[str]:
    uris = [u for u in _STATIC if u != URI_PREFIX + "library-index" or LIBRARY_INDEX.is_file()]
    uris += [URI_PREFIX + "preamble/" + s for s in SEATS]
    return uris


def list_resources() -> list[dict[str, Any]]:
    out = []
    for uri in resource_uris():
        if uri in _STATIC:
            name, mime, desc = _STATIC[uri]
        else:
            seat = uri.rsplit("/", 1)[-1]
            name, mime = f"preamble-{seat}", "text/markdown"
            desc = f"boot preamble for the {seat} seat (tip + law cards + notes + doors)"
        out.append({"uri": uri, "name": name, "description": desc, "mimeType": mime})
    return out


def read_resource(uri: str) -> dict[str, Any]:
    """Return one MCP resource content item ({uri, mimeType, text}), redacted.

    Only URIs in resource_uris() resolve; anything else raises KeyError.
    """
    if not isinstance(uri, str) or uri not in resource_uris():
        raise KeyError(f"unknown resource: {uri!r}")
    if uri == URI_PREFIX + "tip":
        body, mime = json.dumps(redact_obj(tip()), indent=1, ensure_ascii=False), "application/json"
    elif uri == URI_PREFIX + "state":
        body, mime = json.dumps(redact_obj(warm_state()), indent=1, ensure_ascii=False), "application/json"
    elif uri == URI_PREFIX + "laws":
        body, mime = json.dumps(redact_obj(laws()), indent=1, ensure_ascii=False), "application/json"
    elif uri == URI_PREFIX + "zknot":
        body, mime = redact_text(_read_text(ZKNOT) or json.dumps(_missing(ZKNOT))), "text/markdown"
    elif uri == URI_PREFIX + "library-index":
        body, mime = redact_text(_read_text(LIBRARY_INDEX) or json.dumps(_missing(LIBRARY_INDEX))), "text/markdown"
    elif uri == URI_PREFIX + "leases":
        body, mime = json.dumps(redact_obj(leases_board()), indent=1, ensure_ascii=False), "application/json"
    elif uri == URI_PREFIX + "notices":
        body, mime = json.dumps(redact_obj(notices_board()), indent=1, ensure_ascii=False), "application/json"
    else:
        body, mime = redact_text(preamble(uri.rsplit("/", 1)[-1])), "text/markdown"
    return {"uri": uri, "mimeType": mime, "text": _cap(body)}


def warm_read(uri: str = URI_PREFIX + "preamble/free") -> dict[str, Any]:
    """Read one fixed warm-pack resource by URI (same bodies as resources/read).

    For MCP clients that only call tools. The uri must be one of the fixed
    mag://warm/* URIs; there is no path argument.
    """
    try:
        item = read_resource(uri)
    except KeyError:
        raise ValueError(f"uri must be one of {resource_uris()}, got {uri!r}") from None
    return {"ok": True, "schema": SCHEMA, **item}


if __name__ == "__main__":  # human probe: python -m mag.warm_surface
    print(json.dumps(list_resources(), indent=1))
