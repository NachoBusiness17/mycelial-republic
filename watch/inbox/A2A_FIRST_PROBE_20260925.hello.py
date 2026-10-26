"""A2A hello round-trip - bonus probe beyond the card fetch.

Sends one text message to the HF A2A Agent (sheyda/a2a-server HF Space) using
the official a2a-sdk 1.1.5 client over JSONRPC transport. Costs $0.
"""

import asyncio
import sys
import uuid

import httpx
from a2a.client import ClientConfig, ClientFactory
from a2a.client.card_resolver import A2ACardResolver
from a2a.types import a2a_pb2

BASE_URL = "https://sheyda-a2a-server.hf.space"


async def main() -> int:
    async with httpx.AsyncClient(timeout=90, follow_redirects=True) as hc:
        card = await A2ACardResolver(httpx_client=hc, base_url=BASE_URL).get_agent_card()
        client = ClientFactory(ClientConfig(httpx_client=hc)).create(card)
        print("client created, sending hello...")
        req = a2a_pb2.SendMessageRequest(
            message=a2a_pb2.Message(
                message_id=str(uuid.uuid4()),
                role=a2a_pb2.ROLE_USER,
                parts=[a2a_pb2.Part(text="hello")],
            ),
            configuration=a2a_pb2.SendMessageConfiguration(),
        )
        got = False
        async for event in client.send_message(req):
            print("EVENT TYPE:", type(event).__name__)
            print(str(event)[:500])
            got = True
        print("ROUND-TRIP:", "OK" if got else "NO-EVENTS")
        return 0 if got else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
