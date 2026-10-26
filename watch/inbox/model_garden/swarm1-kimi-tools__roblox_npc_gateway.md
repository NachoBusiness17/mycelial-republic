# swarm1-kimi-tools__roblox_npc_gateway (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: hmac.compare_digest compares raw bytes against UTF-8 encoded bytes with different encodings, causing constant-time comparison to fail when non-ASCII characters present in Authorization header | EVIDENCE: tools/roblox_npc_gateway.py:196 | FIX: encode both sides identically: `hmac.compare_digest(self.headers.get("Authorization", "").encode("utf-8"), f"Bearer {_SECRET}".encode())`

DEFECT 2: receipt() writes to shared jsonl without atomic tmp+replace, risking corruption on crash or concurrent writes | EVIDENCE: tools/roblox_npc_gateway.py:143-146 | FIX: write to temp file in same directory then atomic rename to RECEIPTS

DEFECT 3: ask_lane() trusts Content-Length header for body read without handling chunked transfer or connection close, allowing request smuggling via malformed Content-Length | EVIDENCE: tools/roblox_npc_gateway.py:186-187 | FIX: cap read to MAX_BODY with `self.rfile.read(min(n, MAX_BODY))` and validate exact bytes read

DEAD-CODE: OR_API_KEY and OR_API_KEY_2 in _lanes() are never documented in header docstring and appear unused in practice | EVIDENCE: tools/roblox_npc_gateway.py:152-153

ONE-SITTING FIX: hmac.compare_digest encoding mismatch breaks auth for any non-ASCII secret or header | EVIDENCE: tools/roblox_npc_gateway.py:196 | FIX: `hmac.compare_digest(self.headers.get("Authorization", "").encode("utf-8"), f"Bearer {_SECRET}".encode())`
