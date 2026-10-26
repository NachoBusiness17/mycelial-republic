# PORT FORWARDING AS ESTATE ARCHITECTURE · 2026-09-23

**Source:** iximiuz Labs port forwarding diagram (operator-dropped) + three tweet
URLs (@akshay_pachaar, @zpfTechnologies, @heypcbai). The diagram shows four
patterns for connecting a client to a server when the addresses don't match.

## THE FOUR PATTERNS (mapped to the estate)

### 1. "Direct" Sockets
Client sends to the server's real address. No intermediary.
**Estate version:** the corpus files are read directly. The meters read the
state files directly. Fold v2 reads the smith chart JSONs directly. The
simplest pattern, used whenever the addresses haven't changed.

### 2. Port Forwarding (redirect)
Client sends to address A. A redirects to address B. The client doesn't know
about B.
**Estate version:** the browserless gate. The seat sends browser tool calls to
the CDP endpoint. The gate intercepts and returns "browserless: true" instead
of forwarding to the dead socket. A redirect that refuses to forward.

### 3. "User Space" Port Forwarding (proxy)
Client → proxy (listens on local) → server (real address). The proxy is a
user-land process that relays.
**Estate version:** fullsend_s2.py. The free lanes connect to the MiMo
headless server on :4096, which proxies to the actual model. The direct
backfill runner proxies through the DeepSeek API. The orchestrator proxies
through the agent_cli seat.
This is the pattern the estate uses MOST — every API call is a user-space
proxy because the engine and the model are always in different processes.

### 4. "Kernel Space" Port Forwarding (rewrite)
The kernel rewrites the packet's destination address transparently. Using
iptables, eBPF, LVS.
**Estate version:** the chain. The verkle chain rewrites the state's address
on every commit — the parent_verkle_root IS the packet rewrite, and the
content-addressed hash IS the destination address. Transparent to the
caller. Invisible to the client. The record IS the kernel-space rewrite.

## WHY THE OPERATOR SHOWED ME THIS

The diagram names four patterns the estate uses simultaneously without
labeling them. Every connection in the estate is one of these four. The
browserless gate is pattern 2. The fullsend runner is pattern 3. The chain
is pattern 4. The corpus files are pattern 1.

The insight: **every system-level problem the estate hit tonight was a
pattern mismatch.** The browserless gate failed because a pattern-2 redirect
was pointing at a retired pattern-1 direct socket. The truncation backfill
failed because a pattern-3 proxy (agent seats) was dying at init. The fix
was always: identify which pattern you're in, then either fix the address or
switch patterns.

This is the higher-dimensional thinking translated: the estate's connections
form a topology, and the topology has named patterns. Once you can name the
pattern, the fix is mechanical.
