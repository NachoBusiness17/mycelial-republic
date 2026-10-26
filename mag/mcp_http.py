"""mcp_http — MCP streamable-HTTP adapter over the mag TOOL_MAP (in-cage).

Same authority as ``mag.mcp_server`` stdio: transport only, the tool registry
(``tools.TOOL_MAP``) stays the single source. Registered on the API gateway as
``POST /mcp``, so it inherits the gateway's X-API-Key gate and loopback bind —
host seats become CLIENTS of the cage instead of each spawning their own copy
of the organ on the desktop (the 2026-09-04 window-swarm finding).

Stateless streamable HTTP: each POST carries one JSON-RPC message (batch
supported); responses are plain application/json. Notifications (no ``id``)
get 202 with an empty body, per the MCP transport spec.

SEAT HANDSHAKE (2026-10-17, opt-in): a body shaped {"mag_seat": {...},
"body": "<json-rpc string>"} is verified by mag/seat_handshake.py (Ed25519
over method + body sha + seat_id/ts/nonce against configs/seat_allowlist.json,
60 s skew, replay cache) and only the inner body is served. Any failure, and
any plain message while MAG_SEAT_HANDSHAKE=required, gets a bare 404 {} with
no detail. Default (env unset) keeps the legacy plain-message behaviour.

PIN GATE (2026-09-29): every tools/list passes the mcp_pin ledger resolved by
``mcp_server.pin_ledger_path()`` -- drifted tools are withheld and alarmed on
stderr, same contract as the stdio server. Receipt:
watch/inbox/wave5_repair/mcp-pin-wire.md.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from mag import api_gateway as gw
from mag import mcp_server


def _respond(msg: Any) -> tuple[int, Any]:
    """Answer one JSON-RPC message; (202, {}) for notifications."""
    if not isinstance(msg, dict):
        return 200, mcp_server._err(None, -32600, "invalid request: not an object")
    resp = mcp_server.handle(msg, pin_ledger=mcp_server.pin_ledger_path())
    if resp is None:
        return 202, {}
    return 200, resp


@gw.route("POST", "/mcp")
def _mcp_post(params: dict, body: Optional[Any]) -> tuple[int, Any]:
    """MCP endpoint: dispatch initialize / tools/list / tools/call.

    ``body`` is the parsed JSON-RPC message (single object or batch array);
    the response is the raw JSON-RPC envelope — never the gateway ok-wrapper.
    """
    from mag import seat_handshake as sh

    if sh.is_envelope(body):
        verified = sh.verify_envelope(body)
        if verified is None:
            return sh.DROP_HTTP
        try:
            body = json.loads(verified[1])
        except ValueError:
            return sh.DROP_HTTP
    elif sh.mode() == "required":
        return sh.DROP_HTTP
    if isinstance(body, list):
        answers = [r for m in body for r in [_respond(m)[1]] if r]
        if not answers:
            return 202, {}
        return 200, answers
    return _respond(body)
