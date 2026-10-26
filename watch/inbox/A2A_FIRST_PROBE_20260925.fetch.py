"""A2A first interop probe - fetch one public agent card with the official SDK.

Ran 2026-09-25 by the a2a-probe seat (MICKEY-17 wave).
Usage:
    .venv/Scripts/python.exe watch/inbox/A2A_FIRST_PROBE_20260925.fetch.py

Target: HF Space "sheyda/a2a-server" (public, zero-auth A2A 0.3.0 server).
        https://sheyda-a2a-server.hf.space/.well-known/agent-card.json
Documented wall (also probed): copilot.microsoft.com returns HTTP 200 at the
        well-known path but serves an HTML SPA catch-all (soft-404). The official
        resolver correctly rejects it with AgentCardResolutionError. Kept as
        A2A_FIRST_PROBE_20260925.copilot_soft404.html

Evidence filed next to this script:
    A2A_FIRST_PROBE_20260925.card.raw.json       - raw HTTP body as served
    A2A_FIRST_PROBE_20260925.card.resolved.json  - parsed via official A2ACardResolver
"""

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
CARD_URL = "https://sheyda-a2a-server.hf.space/.well-known/agent-card.json"
BASE_URL = "https://sheyda-a2a-server.hf.space"
RAW_OUT = HERE / "A2A_FIRST_PROBE_20260925.card.raw.json"
RESOLVED_OUT = HERE / "A2A_FIRST_PROBE_20260925.card.resolved.json"
WALL_OUT = HERE / "A2A_FIRST_PROBE_20260925.copilot_soft404.html"


async def main() -> int:
    stamp = datetime.now(timezone.utc).isoformat()

    # Step 0: document the copilot.microsoft.com soft-404 wall (200 + text/html).
    wall_url = "https://copilot.microsoft.com/.well-known/agent-card.json"
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as hc:
        wall = await hc.get(wall_url)
        print(f"WALL CHECK GET {wall_url}")
        print(f"HTTP {wall.status_code} content-type: {wall.headers.get('content-type')} bytes: {len(wall.content)}")
        if "html" in (wall.headers.get("content-type") or ""):
            WALL_OUT.write_text(wall.text, encoding="utf-8")
            print(f"wall evidence written: {WALL_OUT}")

    # Step 1: plain GET for the raw receipt.
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as hc:
        resp = await hc.get(CARD_URL)
        print(f"GET {CARD_URL}")
        print(f"HTTP {resp.status_code} {resp.reason_phrase}")
        print(f"content-type: {resp.headers.get('content-type')}")
        print(f"bytes: {len(resp.content)}")
        if resp.status_code != 200:
            print("PROBE FAIL: non-200")
            return 1
        body = resp.text
        RAW_OUT.write_text(body, encoding="utf-8")
        print(f"raw card written: {RAW_OUT}")

    # Step 2: official SDK parse (interop check: card must decode into a2a_pb2.AgentCard).
    from a2a.client.card_resolver import A2ACardResolver
    from google.protobuf.json_format import MessageToDict

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as hc:
        resolver = A2ACardResolver(httpx_client=hc, base_url=BASE_URL)
        card = await resolver.get_agent_card()

    print(f"RESOLVER RETURN TYPE: {type(card).__module__}.{type(card).__name__}")
    card_dict = MessageToDict(card, preserving_proto_field_name=True)
    RESOLVED_OUT.write_text(json.dumps(card_dict, indent=2), encoding="utf-8")

    skills = card_dict.get("skills", [])
    print("RESOLVER OK: card decoded into official a2a_pb2.AgentCard proto")
    print(f"  name            : {card_dict.get('name')}")
    print(f"  protocolVersion : {card_dict.get('protocol_version') or card_dict.get('protocolVersion')}")
    print(f"  url             : {card_dict.get('url')}")
    print(f"  description     : {str(card_dict.get('description'))[:140]}")
    print(f"  skills          : {len(skills)}")
    print(f"  capabilities    : {card_dict.get('capabilities')}")
    print(f"  defaultModes    : {card_dict.get('default_input_modes') or card_dict.get('defaultInputModes')} -> {card_dict.get('default_output_modes') or card_dict.get('defaultOutputModes')}")
    print(f"resolved card written: {RESOLVED_OUT}")
    print(f"fetched-at: {stamp}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
