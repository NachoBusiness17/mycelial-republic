"""MIMO WATCH - 24/7 frontier-window watch on the MiMo V2.6 free lane.

Operator GO (A+B+24/7), 2026-09-22: wire the MiMo V2.6 Flash free window
(opened 2026-09-21 21:19 UTC via opencode, ~7 days) as a surge hull under the
fleet mix law, route verification passes through it, and watch the frontier
through it around the clock.

TRANSPORT DECISION (B2-253, 2026-09-26): the direct-gateway raw-HTTPS probe
against https://opencode.ai/zen/v1/chat/completions is RETIRED BY DESIGN. The
gateway answers FreeTierError ("OpenCode's free tier can only be used from
within OpenCode") for key1, key2, and keyless alike, triple-proven from
captured bodies (09-22 index seqs 1790073989916558 and 1790074361111017;
B2-236 battery 2026-09-26). The only proven free-tier transport is opencode
serve on 127.0.0.1:4096, re-proven live 2026-09-26: POST /session then
POST /session/{id}/message with providerID=opencode modelID=mimo-v2.6-flash-free
returned HTTP 200, cost 0, tokens out=3, finish=stop, in 29.3s. The watch
probes through serve. It never starts or stops the daemon itself; when serve
is unreachable it records serve=down and the lane sleeps but the watch
continues (same philosophy as the old key=missing path). Arming the daemon is
the operator's call (QUEUE B2-261 owns the watch-task arm-or-decline; the
serve-daemon arm story is self-fed as B2-269, first drafted B2-267 and
renumbered highest+1 after mid-lane takes).

SSRF law note: the https-only / host-allowlist / public-DNS guard protected
the retired remote gateway probe and is retired with it. The serve probe
targets one hardcoded loopback address and accepts no operator or remote
input, so there is no SSRF surface to guard.

Single-shot, cron-able, always exit 0 (ox_heartbeat pattern): appends one
status row to watch/inbox/mimo_watch.jsonl and prints the state. ALERT prints
when <24h of window remains. Row schema as of B2-253: the key field is
retired with the gateway probe; rows carry transport/serve/cost/finish/
tokens_out instead. Rows 1-4 (2026-09-22 / 09-26 gateway era) keep their old
shape; the living seal pins bytes 0..492 only.

Error rows name their own cause (B2-252, spec before behavior): every row that
carries an error also carries error_type. On an HTTP error the row keeps the
status code, the error body's error.type ("FreeTierError" vs "other") and a
bounded error_body snippet, so two error responses with different bodies can
never collapse into one indistinguishable string; non-HTTP failures carry
named classes since B2-307 (refused / timeout / dns parsed from the URLError
reason or errno; "other" survives only for genuinely unknown shapes, with the
exception class kept in error_class). The FreeTierError body shape is the B2-236
battery shape: {"error": {"type": ..., "message": ...}}.

The window is a bonus, never a dependency (no-monopoly law): everything routed
through MiMo must be re-runnable elsewhere after it closes.
"""
import errno as _errno
import json
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = (ROOT / "watch" / "inbox").resolve()
LEDGER = OUT / "mimo_watch.jsonl"

WINDOW_OPEN = datetime(2026, 9, 21, 21, 19, 0, tzinfo=timezone.utc)
WINDOW_HOURS = 24 * 7
MODEL = "mimo-v2.6-flash-free"
PROVIDER_ID = "opencode"  # serve recipe per index seq 1790074361111017 and the 2026-09-26 live re-proof
SERVE_BASE = "http://127.0.0.1:4096"  # hardcoded loopback: the transport itself, no input ever reaches this string
PROBE_PROMPT = "Reply with the single word pong and nothing else. Do not use any tools."
SESSION_TIMEOUT = 15
MESSAGE_TIMEOUT = 120  # live turn measured 29.3s on a cold gateway 2026-09-26; 4x headroom


def _error_type_from_body(raw: bytes) -> str:
    """error.type from an error body (B2-252). The FreeTierError shape (B2-236
    battery) is {"type": "error", "error": {"type": ..., "message": ...}}; any
    body that does not parse to an error.type string reads "other" so a JSON
    API error and an opaque edge page can never look alike in the ledger."""
    try:
        parsed = json.loads(raw.decode("utf-8", errors="replace"))
    except ValueError:
        return "other"
    err = parsed.get("error") if isinstance(parsed, dict) else None
    if isinstance(err, dict) and isinstance(err.get("type"), str) and err["type"]:
        return err["type"][:60]
    return "other"


def _post(path: str, payload: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        SERVE_BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _http_error_row(e: urllib.error.HTTPError) -> dict:
    """B2-252: the status line alone cannot tell a FreeTierError from an edge
    or auth error; the row keeps status, the body's error.type and a bounded
    body snippet. Bounded read, no silent-empty guard: e.read on a real
    HTTPError carries the response fp, and a swallowed read failure would forge
    an empty-body row (fallback-branch law).
    B2-308: the response's Server and Content-Type headers ride in the row as
    resp_server / resp_content_type, so a compressed or binary opaque body that
    resists decoding is still attributable by header evidence; two opaque
    bodies from different servers can never produce rows identical on every
    structured field. Absent header = empty string (honest absence)."""
    raw = e.read(2048)
    e.close()
    detail = raw.decode("utf-8", "replace")[:200]
    hdrs = e.headers or {}
    return {"transport": "serve", "serve": "up", "probe": "error",
            "status": e.code,
            "error": ("HTTP " + str(e.code) + ": " + detail)[:160],
            "error_type": _error_type_from_body(raw),
            "error_body": detail,
            "resp_server": hdrs.get("Server", "") or "",
            "resp_content_type": hdrs.get("Content-Type", "") or ""}


def _nonhttp_error_row(e: Exception, serve: str = "down") -> dict:
    """B2-307 (2026-09-26, spec replaces the B2-252 "other" ceiling): refused,
    timeout, and dns must not all read error_type "other" - the ledger cannot
    tell an unarmed daemon (refused) from a hung one (timeout) without parsing
    prose. Class parsed from the URLError reason or the exception shape:
    refused = ConnectionRefusedError / ECONNREFUSED, timeout = socket.timeout
    (TimeoutError) or a "timed out" reason, dns = gaierror; anything else stays
    "other" with the exception class named in error_class for the residue."""
    reason = getattr(e, "reason", e)
    cls = "other"
    if isinstance(reason, ConnectionRefusedError) or getattr(reason, "errno", None) == _errno.ECONNREFUSED:
        cls = "refused"
    elif isinstance(reason, socket.timeout) or "timed out" in str(reason).lower():
        cls = "timeout"
    elif isinstance(reason, socket.gaierror):
        cls = "dns"
    return {"transport": "serve", "serve": serve, "probe": "skipped",
            "error": str(e)[:160], "error_type": cls,
            "error_class": type(reason).__name__}


def _serve_probe() -> dict:
    """One fresh session + one minimal turn through serve, per the proven recipe."""
    try:
        sid = _post("/session", {"title": "mimo-watch-probe"}, SESSION_TIMEOUT)["id"]
    except urllib.error.HTTPError as e:
        # the daemon answered and refused: an error row, not a down daemon
        return _http_error_row(e)
    except Exception as e:
        # B2-307: refused/timeout/dns named at the type level; an unarmed
        # daemon reads "refused", a hung one "timeout" (B2-252's blind spot)
        return _nonhttp_error_row(e)
    try:
        t0 = time.time()
        body = _post(
            f"/session/{sid}/message",
            {
                "parts": [{"type": "text", "text": PROBE_PROMPT}],
                "model": {"providerID": PROVIDER_ID, "modelID": MODEL},
            },
            MESSAGE_TIMEOUT,
        )
        info = body.get("info", {})
        return {
            "transport": "serve",
            "serve": "up",
            "probe": "ok",
            "latency_ms": int((time.time() - t0) * 1000),
            "cost": info.get("cost"),
            "finish": info.get("finish"),
            "tokens_out": (info.get("tokens") or {}).get("output"),
        }
    except urllib.error.HTTPError as e:
        return _http_error_row(e)
    except Exception as e:
        # B2-307: the message-post leg keeps serve=up (session proved the
        # daemon answers) but the failure class is still named, not "other"
        row = _nonhttp_error_row(e, serve="up")
        row["probe"] = "error"
        return row


def main() -> int:
    now = datetime.now(timezone.utc)
    hours_left = round((WINDOW_OPEN.timestamp() + WINDOW_HOURS * 3600 - now.timestamp()) / 3600, 1)
    row = {
        "ts": now.isoformat(timespec="seconds"),
        "window_open": hours_left > 0,
        "hours_left": hours_left,
        "model": MODEL,
    }
    if hours_left > 0:
        row.update(_serve_probe())
    else:
        row["probe"] = "window-closed"

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    alert = ""
    if hours_left <= 0:
        alert = "WINDOW CLOSED"
    elif hours_left < 24:
        alert = "ALERT: <24h of free window remains"
    elif row.get("serve") == "down":
        alert = "lane idle: opencode serve not reachable on 127.0.0.1:4096 (operator arms it)"
    print(f"[mimo-watch] {now.isoformat(timespec='seconds')} hours_left={hours_left} {row.get('probe','')} {alert}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
