"""server: THE ESTATE'S OWN WORLD SERVER v0 (2026-09-29).

The first server that is fully ours. The estate compiled CMaNGOS (a full
WoW server, ~2M lines) as a learning specimen, then built the same five
mechanisms a world server actually needs (auth, session, dispatch, tick,
broadcast) on top of the estate's own physics organ, mag/water_graph.py,
in a few hundred lines.

Server-authoritative: the water graph runs HERE. Clients propose actions;
the server validates, stages, ticks at a fixed cadence, and broadcasts
state. No client ever mutates the world.

Modules:
    world     : MountainWorld: the authoritative board + event log
    protocol  : the wire: line-based JSON over TCP (ours, debuggable)
    auth      : v0 salted-SHA256 user file + time-salted session ids
    server    : asyncio TCP server, tick loop, fan-out, --demo

Run:
    .venv/Scripts/python.exe -m server.server --help
    .venv/Scripts/python.exe -m server.server --demo
"""
from server.world import MountainWorld  # noqa: E402,F401
from server.protocol import REJECT_CODES, VERBS  # noqa: E402,F401

__version__ = "0.1.0"
