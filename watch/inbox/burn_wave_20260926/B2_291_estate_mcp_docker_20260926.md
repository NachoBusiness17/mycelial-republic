# B2-291 estate MCP on docker 2026-09-26

## Verdict

LANDED and running. The estate MCP server is an always-on docker service: compose service `mcp` (container mag-mcp, image mag-sovereign:local, restart unless-stopped, HEALTHY) runs a loopback TCP bridge (scripts/container/mcp_tcp_bridge.py) in front of mag/mcp_server.py, publishing 127.0.0.1:8766 only. Every MCP client on the host (ZCode, VS Code, Claude-class, cold agents) can now call the estate tool registry natively. The falsifier's concurrent arm is satisfied live: two simultaneous client sessions through docker (172.18.0.1 proxy path), each got initialize + 17-tool manifest (archivist profile, read-only: no run_shell/write_file/apply_patch) and clean corpus_search results (ok true, engine fts5, index fresh, 3 hits each, 2.0s wall for both). The seed-fetch arm is FILED AS OWED: no seed tool exists in TOOL_MAP to call (the brief's "B2-151 seed tools" is a mis-citation; B2-151 in QUEUE.md is the pid-37172 survivor brief, still Open); adding a read-only seed_fetch tool is the follow-up.

## Evidence file:line quotes

- docker-compose.yml mcp block (this lane): entrypoint python scripts/container/mcp_tcp_bridge.py --port 8766 --bind 0.0.0.0 --profile archivist; ports "127.0.0.1:8766:8766"; truthful healthcheck probing the bridge port (the inherited image healthcheck probes :8765 and read the service permanently unhealthy until replaced, the worker lesson again).
- scripts/container/mcp_tcp_bridge.py: docstring security posture; _pump uses read1 for pipe sources (BufferedReader.read blocks until a FULL 64KB chunk, holding short MCP replies hostage; two live falsified bugs fixed: sendall-on-stdin AttributeError, then read-chunk buffering; then the in-cage bind: 127.0.0.1 inside the container answers internally but the docker proxy dials the container IP and the host got instant EOF, so the cage binds 0.0.0.0 and the loopback guarantee is the host-side 127.0.0.1 mapping).
- mag/mcp_server.py:344-349: handle() dispatches initialize/tools/list/tools/call; serve() writes newline-delimited JSON with flush (the exact wire the bridge relays).
- Live falsifier transcript (2026-09-26): two threads, each socket.create_connection 127.0.0.1:8766, initialize reply from serverInfo mag-tool-map, tools/list 17 tools, tools/call corpus_search {"query":...,"limit":3} returned ok true engine fts5 3 hits per session, elapsed 2.0s.
- docker ps: mag-mcp Up (healthy), 127.0.0.1:8766->8766/tcp.

## Work done

1. Design per the operator question: stdio MCP server cannot be an always-on service, so a stdlib-only threaded TCP bridge with ONE mcp_server subprocess per connection (session isolation preserved, no new transport semantics in the server).
2. Read-only first: served profile is archivist (17 read-only tools; corpus_search/corpus_get/corpus_tail/corpus_stats/research_* + fs reads); write/shell/patch tools absent from the manifest (verified in the live tools/list).
3. Claim law: docker-compose.yml was working-tree-modified with a foreign active CLAIM (B2-490), so CLAIM B2-291 landed on QUEUE.md 20:25:57Z before editing; the edit is ONE new service block + this lane's own healthcheck, zero bytes of existing blocks touched, rebased on freshly-read bytes.
4. Wired and live-falsified through four bugs (sendall-on-pipe, block buffering, in-cage bind, inherited healthcheck), each named in the fix comment or the compose comment with its evidence; final state: service healthy, concurrent two-session proof clean from the host while this seat holds the lane.
5. Owed, filed: a read-only seed_fetch tool (TOOL_MAP + archivist profile + seed pack pointer) so the brief's second named surface exists; until then the falsifier's seed arm has nothing to call, which is the honest reading of the mis-cited brief text.

## Falsifier

Dies if: (a) a second MCP client session through docker fails corpus_search while this seat runs (rerun the two-thread proof; the raw-socket client in this receipt is the reference); (b) the manifest ever lists run_shell/write_file/apply_patch under the served archivist profile; (c) the published mapping stops being 127.0.0.1-bound (0.0.0.0 on the HOST side would break the loopback law; in-cage 0.0.0.0 is correct and required); (d) the service stays unhealthy after start_period (healthcheck rot).

## Bibliography closed

Read whole: mag/mcp_server.py (protocol + serve + profiles), tools/__init__.py TOOL_MAP, tools/corpus.py (paths, signature query= not q=), docker-compose.yml (mag/worker/redis blocks, worker healthcheck lesson), scripts/container/mcp_tcp_bridge.py (authored). Bytes: live docker ps/logs, live two-session transcript, compose config --quiet clean, em-dash 0 on added lines. Nothing synthesized; the owed seed arm named rather than faked.
