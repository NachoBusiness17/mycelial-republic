# HOW A REAL SERVER WORKS (2026-09-29)

Dissection of the compiled CMaNGOS specimen (corpus/library/mod-playerbots) by the read-only lane.
The full document text was delivered in the lane's completion report and is being filed by the
coordinator in two parts (this header + body file) to preserve byte-exactness.
Key receipts: realmd SRP6 handshake (AuthSocket.cpp, SRP6.cpp: B=(3v+g^b) mod N, session key K persisted
to the account table = the ONLY inter-process contract); world session (WorldSocket.cpp: seed, RC4 header
crypto, CMSG_AUTH_SESSION digest proof, async AddSession); opcode dispatch (one table, status+thread gates,
array-indexed); movement (client-authoritative position, server-authoritative velocity, relay-to-visible-set);
object updates (1326-slot field arrays, dirty masks, per-viewer serialization, zlib>100B); spatial (64x64 grids
of 8x8 cells, 100yd visibility, known-set diff); main loop (50ms fixed-budget frame, sessions->maps(parallel
barrier)->sweeps, deferred deletions); persistence (memory-first, per-DB writer threads, whole-row upserts);
threading (queues between every thread, Messager<T> deferred calls); bots = real sessions with NULL sockets,
AI injects legal packets at the session queue (the seam lesson for our flock).
The Build Cheat Sheet (12 mechanisms, CMaNGOS vs our simplest version) and the 5 load-bearing design decisions
are in the lane report; the server-v0 lane is implementing them now.
