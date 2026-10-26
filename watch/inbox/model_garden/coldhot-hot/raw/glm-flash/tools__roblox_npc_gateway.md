# coldhot-hot-glm-flash-tools__roblox_npc_gateway (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: Empty NPC_GATEWAY_HOST is treated as loopback but binds all interfaces, so a blank host with no secret yields an unauthenticated public listener, defeating the fail-closed rule | EVIDENCE: tools/roblox_npc_gateway.py:110-111 | FIX: treat "" as non-loopback (fail closed) or resolve it explicitly before deciding auth is optional
DEFECT 2: Content-Length is never validated as non-negative, so n = -1 makes rfile.read(-1) block until client close and buffer the body unbounded on a public listener | EVIDENCE: tools/roblox_npc_gateway.py:212,217 | FIX: reject n < 0 with 400 before reading
DEFECT 3: ThreadingHTTPServer spawns unbounded threads and each POST can hold one for up to 25s per lane across all lanes, a trivial slowloris thread-exhaustion DoS | EVIDENCE: tools/roblox_npc_gateway.py:247 | FIX: cap concurrent connections with a bounded ThreadPool-style mixin and per-request socket timeout
DEAD-CODE: "OR_API_KEY" and "OR_API_KEY_2" lane env fallbacks are undocumented in the failover contract and likely never provisioned | EVIDENCE: tools/roblox_npc_gateway.py:140
ONE-SITTING FIX: validate and clamp Content-Length in do_POST (reject negative or missing with 400, enforce MAX_BODY before read) | EVIDENCE: tools/roblox_npc_gateway.py:212
