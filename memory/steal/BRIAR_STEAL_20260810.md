# BRIAR STEAL (2026-08-10) — delay-tolerant, serverless, deniable rendezvous for the swarm
Researcher: ghost · Source: Briar (briarproject.org / github.com/briar/briar) — P2P encrypted
messaging for activists, offline-first, over Tor · Context: harden whisper_route (the deniable swarm).

## What Briar is (grounded)
Open-source P2P encrypted messaging (Java/Kotlin, GPL). NO central server — devices sync directly
(peer-to-peer). Transports: Bluetooth, Wi-Fi, removable storage (USB), Tor over internet. All E2E
encrypted; content stored on device, not cloud. Target: activists/journalists. Audited (Cure53), funded
(Open Technology Fund). Bramble protocol suite designed for DELAY-TOLERANT networks. Entered
maintenance mode (2026-07). Reproducible builds (docker) for verifiability.

## The Bramble protocol suite (the layering)
Handshake Protocol, QR Code Protocol, Rendezvous Protocol, Synchronisation Protocol, Transport Protocol.
Designed for delay-tolerant networks (DTN) — messages sync when paths open, not always-on.

## The invariants worth stealing (adapt to whisper_route / the 24/7 swarm)
1. NO CENTRAL SERVER (P2P sync direct) = our no_throne; the swarm has no orchestrator — the field IS
   coordination. The deniable swarm syncs node-to-node, not through a hub.
2. OFFLINE-FIRST / DELAY-TOLERANT = the swarm keeps working when the network breaks: sync via
   local/k8s/local-first when cloud is down; messages sync when a path opens (the flock folds when
   reachable). "Keeps working if somebody breaks the Internet."
3. RENDEZVOUS PROTOCOL = how two parties find each other to sync, deniably. Our equivalent: the
   verkle/whisper ANCHOR (scratch_id / memlang anchor) as the rendezvous point — "where to meet" is a
   deniable QR-like anchor, not a server lookup.
4. QR CODE PROTOCOL = deniable bootstrap: establish a secure channel from an offline anchor. Our
   equivalent: bootstrap the shared map from a content-addressed anchor (whisper public-face / verkle
   leaf) without leaking.
5. SYNCHRONISATION via content-addressed fragments = our verkle/knot sync: state syncs across the swarm
   by content-addressed parts (shape_map reconstruct), delay-tolerant.
6. LOCAL STORAGE, NOT CLOUD = our local_first; the deniable swarm's secrets live on-device, not the cloud.
7. REPRODUCIBLE BUILDS = verifiability/trust = our content-addressing + provenance (the whole is
   verifiable, not just claimed).

## The Bramble layering -> whisper_route layering (adapt)
Bramble: Handshake -> QR -> Rendezvous -> Synchronisation -> Transport.
whisper_route: front(generic research) -> riddler(deniable handshake/surrogate) -> memlang(anchor/sync)
-> corpus(verkle synchronisation) -> transport. The Rendezvous = the anchor both sides share.

## The tesuji
DELAY-TOLERANT, SERVERLESS, DENIABLE RENDEZVOUS: the deniable swarm needs no central server, works when
the net breaks, syncs state via content-addressed rendezvous (Bramble Rendezvous -> our verkle anchor),
and bootstraps deniably (QR -> our anchor). This hardens whisper_route + the 24/7 swarm: it survives
disconnection and reveals nothing.
