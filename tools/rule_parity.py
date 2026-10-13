"""rule_parity v0 — GDScript offline rules vs Python server rules, measured.

The lensing's C3 core finding (2026-09-30): mag/water_graph.py (the
authoritative server engine) and roblox_to_godot/systems/water_graph.gd
(the offline client mirror) were WRITTEN to agree but NEVER COMPARED — a
silent divergence would be invisible to every instrument while sitting
directly under the product's core differentiator (deterministic integer
water physics, same laws on both sides of the wire).

This harness makes the comparison mechanical:

  gen        N seeded input sequences (board + per-tick action frames) in
             one canonical JSON both sides consume. Families: the shipping
             Mountain board (server/world.py build_mountain_graph, byte
             truth via import), gated-sibling boards (two+ pipes from one
             source into gated junctions — the LW5 seam), waste/cold/siphon
             economy boards, fracture loops (sustained full bore past the
             AC2/B1 threshold window), stress-domain boards (R8: volumes
             ~1e15-1e17 across the VOLUME_SAT int64 ceiling — ingest
             clamps, runtime saturation, gate/waste/spray absorption),
             receipt boards (Q11: the legality ladder — say/whisper
             BAD_TEXT, whisper UNKNOWN_TARGET, STALE_NONCE/RATE_CAP, the
             keyless BAD_MAC arms, plus the standing water rejects),
             hydrology boards (Q02: graded-head/gradient flow — mag/
             hydrology.py rung 1, the fixed-point dHead law where boolean
             verdict physics and the Watershed part ways in BOTH
             directions; Python-oracle-frozen today, see the Q02 note in
             cmd_all), and free random boards.
  python     each sequence through mag.water_graph.WaterGraph + a legality
             shim replicating the server's receipt ladder (server.py
             _admit_action: MAC gate -> nonce -> world validation -> rate
             cap -> stage -> commit, over the full six-verb CHAT_TABLE
             contract; staged actions validate at receipt, apply in
             arrival order at tick start, physics after), one state-hash
             per tick. Hydrology sequences run the SAME ladder around
             mag.hydrology.HydrologyGraph (the graded oracle) instead.
  godot      the SAME JSON through roblox_to_godot/tests/
             rule_parity_runner.gd under headless Godot 4.3
             (tools/godot/Godot_v4.3-stable_win64.exe), same hashes.
  compare    per-tick hash + per-action verdict diff; first divergence with
             tick, both hashes, and a field-level state diff.

State hash = sha256 over a canonical text form (tick, then nodes then
pipes, both sorted by name, fixed field order, booleans as 0/1) so Python
hashlib and GDScript String.sha256_text() hash identical bytes. Integer
law: the engine is all-int, so the hash is well-defined.

Honest result either way (the lensing's words): parity holds = the
differentiator is proven; a first divergence = the top engineering item.

Exit codes (compare/all): 0 parity, 1 divergence, 2 instrument error.

CI shape (D2, 2026-09-30): `all --quick` (20 sequences, budget <60s — the
pre-push gate payload) and `all --full` (100 sequences — the nightly depth
run; byte-compatible with the V5 receipt's `all --seed 20260930 --n 100
--ticks 120`). Both write tools/rule_parity_out/latest.json — the standing
"currently true" artifact (last run's mode, params, verdict, twin digests).

FIRST-LINE CONTRACT (the B2-338 hook law): `all` opens its stdout with
exactly one of
    PARITY: ok mode=...      (exit 0)
    PARITY: FAIL mode=...    (exit 1)
    PARITY: ERROR mode=...   (exit 2, instrument error)
so githooks/pre-push case-matches the lowercase-ok prefix and never widens
past it; a traceback falls to the fail-closed arm.

Generation mix law: every mode covers EVERY family — the mountain share
scales down for small n (quick must hit the LW5 gated-siblings seam, where
the v0 divergence lives, not 20 mountain copies).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.hydrology import DEFAULT_CROSS_SECTION, HydrologyGraph  # noqa: E402
from mag.water_graph import VOLUME_SAT, WaterGraph  # noqa: E402

SCHEMA = "rule_parity.v1"
LATEST_SCHEMA = "rule_parity_latest.v1"
GODOT_EXE = ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe"
GODOT_PROJECT = ROOT / "roblox_to_godot"
GD_RUNNER = "res://tests/rule_parity_runner.gd"
DEFAULT_OUT = ROOT / "tools" / "rule_parity_out"
LATEST_NAME = "latest.json"
# the parity twins — the gate's trigger pathspecs (githooks/pre-push D2 block)
TWIN_PY = "mag/water_graph.py"
TWIN_GD = "roblox_to_godot/systems/water_graph.gd"
# Q02 (2026-10-01): the graded-head family's engine bytes. The GDScript
# ENGINE twin exists (water_graph.gd Z10 port: HydroNode + the `hydrology`
# flag + conductance), but the parity RUNNER (roblox_to_godot/tests/
# rule_parity_runner.gd) is boolean-only and owned by another lane — so the
# hydrology family is Python-oracle-FROZEN (corpus + per-tick hashes from
# mag/hydrology.py) until that runner grows the flag; latest.json names
# these bytes so a dirty hydrology.py can never hide behind a stale freeze.
TWIN_HYDRO = "mag/hydrology.py"

# CI profiles (D2): quick = the pre-push payload (20 seqs, budget <60s);
# full = the nightly depth run (seed 20260930, n=100, ticks=120 -> 14,040
# tick frames). Same profile params as the V5 receipt corpus; the R8 mix
# amendment (2026-09-30) added the stress_domain family, so the same-seed
# corpus BYTES differ from V5's run — the V5 byte-compat claim retired by
# receipt R8_INT_DOMAIN.md; frame totals are unchanged. The Q11 mix
# amendment (2026-10-01) added receipt, and the Q02 amendment (2026-10-01)
# added hydrology (0.06, carved from economy 0.24->0.22 and random
# 0.30->0.26) — same-seed bytes shift again, frame totals still hold.
PROFILES: dict[str, dict[str, int]] = {
    "quick": {"seed": 20260930, "n": 20, "ticks": 40},
    "full": {"seed": 20260930, "n": 100, "ticks": 120},
}
# quick's structural frame bound: 19 boards * 40 ticks + 1 fracture loop * 460
# = 1220; 1500 headroom. A quick run past this is drifting toward full cost.
QUICK_FRAME_BUDGET = 1500
QUICK_WALL_BUDGET_S = 60.0

WATER_VERBS = ("boil", "valve")          # the two graph-mutating verbs (generated)
# the full server verb table (server/protocol_table.py CHAT_TABLE.verbs) —
# stamped into the input JSON so both sides gate UNKNOWN_VERB on byte truth.
# Q11 (2026-10-01, mountain_climb): the same law now stamps max_say (the
# BAD_TEXT bound, server/world.py MAX_SAY) so the .gd twin never forks the
# number either.


def _server_verbs() -> tuple[str, ...]:
    from server.protocol_table import CHAT_TABLE
    return tuple(CHAT_TABLE.verbs)


def _server_max_say() -> int:
    from server.world import MAX_SAY
    return int(MAX_SAY)


# ------------------------------------------------------------ state hash ----

def canonical_state_text(tick: int, nodes: dict[str, Any],
                         pipes: dict[str, Any]) -> str:
    """The canonical form both languages hash. Nodes/pipes are the ENGINE's
    objects (mag.water_graph Node/Pipe on Python, WNode/WPipe on GDScript —
    the runner mirrors this formatter line for line). Booleans -> 0/1 so
    Python's True/False str() can never leak into the digest."""
    lines = [f"t={tick}"]
    for name in sorted(nodes):
        n = nodes[name]
        lines.append(f"N|{name}|{n.elev}|{n.kind}|{n.sill}|{n.volume}|{n.steam}")
    for name in sorted(pipes):
        p = pipes[name]
        lines.append(
            f"P|{name}|{p.src}|{p.dst}|{p.cap}|{int(p.siphon)}|{p.crest}|"
            f"{int(p.primed)}|{int(p.open)}|{p.stress}|{int(p.fractured)}")
    return "\n".join(lines)


def state_hash(g: WaterGraph) -> str:
    body = canonical_state_text(g.tick_count, g.nodes, g.pipes)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def state_fields(g: WaterGraph) -> dict[str, Any]:
    """Field-level state for divergence diffs (mirrors the hash fields)."""
    return {
        "tick": g.tick_count,
        "nodes": {n: {"elev": v.elev, "kind": v.kind, "sill": v.sill,
                      "volume": v.volume, "steam": v.steam}
                  for n, v in g.nodes.items()},
        "pipes": {p: {"src": v.src, "dst": v.dst, "cap": v.cap,
                      "siphon": v.siphon, "crest": v.crest,
                      "primed": v.primed, "open": v.open,
                      "stress": v.stress, "fractured": v.fractured}
                  for p, v in g.pipes.items()},
    }


# ------------------------------------------------------- legality engine ----

class HarnessWorld:
    """Legality shim: the server's RECEIPT LADDER wrapped around an
    arbitrary WaterGraph (Q11, 2026-10-01, mountain_climb: the shim used to
    mirror only MountainWorld.validate's water subset — the lensing's FAIL
    "offline accepts what the server rejects at receipt").

    The server stages every action through server/server.py _admit_action
    (:489-521), whose ladder this shim now mirrors end to end:

        MAC gate (R3, keyless arms) -> nonce law (STALE_NONCE) ->
        world validation (the six-verb CHAT_TABLE law, BAD_TEXT included)
        -> rate cap (RATE_CAP) -> stage (whisper acks direct, never pends)
        -> commit on ack (whisper spends the window like every verb).

    Sources, one truth each:
      - ReceiptGate is IMPORTED from server/protocol_table.py, never
        re-typed (the nonce burns at receipt; the cap spends only on ack).
      - validate() mirrors server/world.py MountainWorld.validate verbatim
        for all six verbs (VERBS = CHAT_TABLE.verbs there), with MAX_SAY
        imported so the BAD_TEXT bound cannot fork.
      - the frame-MAC gate mirrors server/frame_mac.py FrameMacState.admit
        / check (:209-277) for the KEYLESS arms only — missing mac in the
        strict window (the require/sticky law), seq type/range (SHAPE),
        seq != expected (SEQ), tag shape (SHAPE, 32 lowercase hex). The
        TAG arm needs K, which only SRP6 mints (the GDScript bignum
        client is server/README "What v1 owes"), so the corpus never
        emits a shape-legal mac and the unverifiable arm is never
        reached; tamper also disconnects (server.py breaks the read
        loop), so the connection goes dark and later frames yield no
        verdict, exactly like a severed socket.
    """

    def __init__(self, seq: dict[str, Any], verbs: tuple[str, ...],
                 max_say: int = 240, graded: bool = False,
                 conductance: int = 8):
        """graded=True (Q02, 2026-10-01): the SAME receipt ladder around
        mag.hydrology.HydrologyGraph — nodes carry cross_section, flow =
        min(cap, src.volume, dHead*conductance >> 8). The ladder is law, not
        physics: verdicts are family-independent, so the hydrology family
        exercises chat/nonce/cap law under the graded engine for free."""
        from server.protocol_table import NO_NONCE, ReceiptGate
        self._no_nonce = NO_NONCE   # the sentinel, imported never re-typed
        g: WaterGraph
        if graded:
            g = HydrologyGraph(conductance=int(conductance))
            for n in seq["nodes"]:
                g.add_node(n["name"], elev=n["elev"], kind=n["kind"],
                           sill=n.get("sill", 0), volume=n.get("volume", 0),
                           cross_section=int(n.get("cross_section",
                                                   DEFAULT_CROSS_SECTION)))
        else:
            g = WaterGraph()
            for n in seq["nodes"]:
                g.add_node(n["name"], elev=n["elev"], kind=n["kind"],
                           sill=n.get("sill", 0), volume=n.get("volume", 0))
        for p in seq["pipes"]:
            g.add_pipe(p["name"], p["src"], p["dst"], cap=p.get("cap", 1),
                       siphon=bool(p.get("siphon", False)),
                       crest=int(p.get("crest", 2)),
                       open_=bool(p.get("open", True)))
        self.graph = g
        self.verbs = set(verbs)
        self.max_say = int(max_say)   # server/world.py MAX_SAY, stamped by gen
        self.roster = {sid: {"user": f"user_{sid}"} for sid in seq["sids"]}
        self.pending: list[dict[str, Any]] = []
        # the receipt-ladder state (server/server.py + frame_mac.py)
        self.gate = ReceiptGate()
        # frame-MAC window: arm_at_tick models "srp_proof succeeded on this
        # connection just before tick N" — before it the gate is unarmed
        # (server.py only runs state.admit when mac_state is not None);
        # from it on, the STRICT window (require_frame_mac=True): every
        # frame must carry a valid MAC. -1 = the whole sequence is bare.
        self.arm_at_tick = int(seq.get("arm_at_tick", -1))
        self.mac_expected = 0
        self.dark = False   # tamper = disconnect: later frames process nothing

    # ---- the R3 MAC gate, keyless arms (frame_mac.check :215-231 order) ----
    def _mac_admit(self, act: dict[str, Any], tick_no: int) -> str | None:
        if self.arm_at_tick < 0 or tick_no < self.arm_at_tick:
            return None                # unarmed connection: the gate is skipped
        if "mac" not in act:
            return "BAD_MAC"           # strict window: a bare frame is tamper
        seq = act.get("seq")
        if type(seq) is not int or seq < 0:
            return "BAD_MAC"           # SHAPE (a bool is a verdict, not a seq)
        if seq != self.mac_expected:
            return "BAD_MAC"           # SEQ: gap or replay, never resync
        tag = act.get("mac")
        if (not isinstance(tag, str) or len(tag) != 32
                or any(c not in "0123456789abcdef" for c in tag)):
            return "BAD_MAC"           # SHAPE: 32 lowercase hex chars
        # TAG (HMAC under k_c2s over the canonical body) is beyond the
        # offline twin by construction: the corpus cannot mint a tag it
        # cannot compute, and the generator never emits a shape-legal mac.
        self.mac_expected += 1
        return None

    # ---- world validation (server/world.py MountainWorld.validate :188-219)
    def validate(self, sid: str, verb: str, target: str) -> str | None:
        """Reject code or None (=ack). Mirrors MountainWorld.validate — the
        FULL CHAT_TABLE contract, order verbatim: sid, verb, say, whisper,
        valve, generic node target, boil/tag dry check."""
        if sid not in self.roster:
            return "UNKNOWN_SID"
        if verb not in self.verbs:
            return "UNKNOWN_VERB"
        if verb == "say":
            # LW6: target IS the text — free-form, never a node name
            if not target or len(target) > self.max_say:
                return "BAD_TEXT"
            return None
        if verb == "whisper":
            # LW6: target is 'user|text' (first '|' splits). Malformed or
            # over-length -> BAD_TEXT; a user with no session -> UNKNOWN_TARGET.
            to_user, sep, text = target.partition("|")
            if not sep or not to_user or not text or len(text) > self.max_say:
                return "BAD_TEXT"
            if not any(info["user"] == to_user for info in self.roster.values()):
                return "UNKNOWN_TARGET"
            return None
        if verb == "valve":
            if target not in self.graph.pipes:
                return "UNKNOWN_TARGET"
            return None
        if target not in self.graph.nodes:
            return "UNKNOWN_TARGET"    # boil/join/tag: a node name
        if verb in ("boil", "tag") and self.graph.nodes[target].volume <= 0:
            return "DRY_POOL"
        return None

    # ---- the receipt ladder (server/server.py _admit_action :489-521) ----
    def admit_action(self, act: dict[str, Any], tick_no: int) -> str | None:
        """One action through the ladder. Returns 'ack', 'reject:<code>',
        or None when the connection is dark (tamper disconnected it) — no
        verdict, exactly like a frame that never arrived."""
        if self.dark:
            return None
        sid, verb, target = act["sid"], act["verb"], act["target"]
        why = self._mac_admit(act, tick_no)
        if why is not None:
            self.dark = True           # server.py: break — tamper, never resync
            return f"reject:{why}"
        nonce = act["n"] if "n" in act else self._no_nonce
        why = self.gate.admit_nonce(sid, nonce)
        if why is not None:
            return f"reject:{why}"
        why = self.validate(sid, verb, target)
        if why is not None:
            return f"reject:{why}"
        applies_at_tick = self.graph.tick_count + 1
        why = self.gate.admit_cap(sid, applies_at_tick)
        if why is not None:
            return f"reject:{why}"
        # stage (world.stage minus the wire reply): whisper is the one
        # receipt-time verb — it acks direct and never pends (LW6).
        if verb != "whisper":
            self.pending.append({"sid": sid, "verb": verb, "target": target})
        self.gate.commit(sid, applies_at_tick)   # an ack is an ack (whisper too)
        return "ack"

    def apply_pending(self) -> None:
        for act in self.pending:            # arrival order (MountainWorld._apply)
            if act["verb"] == "boil":
                self.graph.boil(act["target"], 1)
            elif act["verb"] == "valve":
                pipe = self.graph.pipes[act["target"]]
                if pipe.open:
                    self.graph.close(act["target"])
                else:
                    self.graph.open(act["target"])   # refuses fractured (AC2)
            elif act["verb"] == "join":
                # roster position only — never enters the state hash
                self.roster[act["sid"]]["at"] = act["target"]
            # say/whisper/tag mutate no graph state (say is a tick event,
            # whisper rides the direct outbox, tag scores server-side)
        self.pending.clear()

    def tick_frame(self, actions: list[dict[str, Any]],
                   tick_no: int = 0) -> dict[str, Any]:
        verdicts = [v for a in actions
                    if (v := self.admit_action(a, tick_no)) is not None]
        self.apply_pending()
        self.graph.tick()
        return {"hash": state_hash(self.graph), "verdicts": verdicts,
                "state": state_fields(self.graph)}


# ------------------------------------------------------------- generator ----

def _mountain_nodes_pipes() -> tuple[list[dict], list[dict]]:
    """The shipping board, straight from the world server (byte truth)."""
    from server.world import build_mountain_graph
    g = build_mountain_graph()
    nodes = [{"name": n.name, "elev": n.elev, "kind": n.kind, "sill": n.sill,
              "volume": n.volume} for n in g.nodes.values()]
    pipes = [{"name": p.name, "src": p.src, "dst": p.dst, "cap": p.cap,
              "siphon": p.siphon, "crest": p.crest, "open": p.open}
             for p in g.pipes.values()]
    return nodes, pipes


def _rand_action(rng: random.Random, sids: list[str],
                 nodes: list[dict], pipes: list[dict]) -> dict[str, Any]:
    """One action ask: mostly legal water verbs, occasional ILLEGAL probes
    (unknown sid / verb / target) so the legality engine is compared too."""
    r = rng.random()
    sid = rng.choice(sids)
    if r < 0.05:
        return {"sid": "s_ghost", "verb": "boil", "target": nodes[0]["name"]}
    if r < 0.10:
        return {"sid": sid, "verb": rng.choice(["poke", "dredge", "siphon_verb"]),
                "target": nodes[0]["name"]}
    if r < 0.15:
        bad = rng.choice([{"sid": sid, "verb": "valve", "target": "p_ghost"},
                          {"sid": sid, "verb": "boil", "target": "node_ghost"}])
        return bad
    if r < 0.55:
        return {"sid": sid, "verb": "boil",
                "target": rng.choice(nodes)["name"]}
    return {"sid": sid, "verb": "valve",
            "target": rng.choice(pipes)["name"]}


def _frames(rng: random.Random, ticks: int, sids: list[str],
            nodes: list[dict], pipes: list[dict],
            p_action: float, forced: dict[int, list[dict]] | None = None) -> list[list[dict]]:
    frames: list[list[dict]] = []
    for t in range(ticks):
        acts: list[dict] = []
        if forced and t in forced:
            acts.extend(forced[t])
        while rng.random() < p_action:
            acts.append(_rand_action(rng, sids, nodes, pipes))
        frames.append(acts)
    return frames


def _seq(seq_id: str, family: str, ticks: int, sids: list[str],
         nodes: list[dict], pipes: list[dict],
         frames: list[list[dict]]) -> dict[str, Any]:
    for p in pipes:  # generator law: every pipe endpoint must exist
        names = {n["name"] for n in nodes}
        assert p["src"] in names and p["dst"] in names, f"bad pipe {p}"
    return {"id": seq_id, "family": family, "ticks": ticks, "sids": sids,
            "nodes": nodes, "pipes": pipes, "frames": frames}


def _gen_mountain(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    nodes, pipes = _mountain_nodes_pipes()
    frames = _frames(rng, ticks, ["s1", "s2"], nodes, pipes, p_action=0.35)
    return _seq(seq_id, "mountain", ticks, ["s1", "s2"], nodes, pipes, frames)


def _gen_siblings(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    """LW5 seam board: ONE source feeding 2-3 pipes whose dsts are gated
    junctions (xor/sill). Python reserves the probed flow at probe time;
    any mirror that decrements the source later lets sibling pipes
    re-spend the same volume."""
    n_sib = rng.randint(2, 3)
    nodes = [{"name": "src", "elev": rng.randint(8, 12), "kind": "plain",
              "sill": 0, "volume": rng.randint(1, 4)}]
    outs = []
    for i in range(n_sib):
        kind = rng.choice(["xor", "sill"])
        nodes.append({"name": f"gate{i}", "elev": rng.randint(3, 6),
                      "kind": kind, "sill": rng.randint(2, 3) if kind == "sill" else 0,
                      "volume": 0})
        outs.append(f"gate{i}")
    nodes.append({"name": "pool", "elev": 0, "kind": "plain", "sill": 0,
                  "volume": 0})
    pipes = []
    for i, dst in enumerate(outs):
        pipes.append({"name": f"p{i}", "src": "src", "dst": dst,
                      "cap": rng.randint(1, 2), "siphon": False, "crest": 2,
                      "open": True})
    pipes.append({"name": "p_out0", "src": outs[0], "dst": "pool",
                  "cap": 2, "siphon": False, "crest": 2, "open": True})
    frames = _frames(rng, ticks, ["s1"], nodes, pipes, p_action=0.15)
    return _seq(seq_id, "gated_siblings", ticks, ["s1"], nodes, pipes, frames)


def _gen_economy(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    """waste basin + cold crown + siphons: the V5 economy recovery loop
    (boil waste -> steam -> condense at the crown) and siphon prime/break."""
    nodes = [
        {"name": "high", "elev": 9, "kind": "plain", "sill": 0, "volume": rng.randint(2, 6)},
        {"name": "mid", "elev": 5, "kind": rng.choice(["xor", "sill"]),
         "sill": rng.randint(1, 2), "volume": 0},
        {"name": "pit", "elev": 2, "kind": "plain", "sill": 0, "volume": 0},
        {"name": "waste", "elev": 0, "kind": "waste", "sill": 0, "volume": 0},
        {"name": "crown", "elev": 14, "kind": "cold", "sill": 0, "volume": 0},
    ]
    pipes = [
        {"name": "p_down", "src": "high", "dst": "mid", "cap": rng.randint(1, 2),
         "siphon": False, "crest": 2, "open": True},
        {"name": "p_side", "src": "high", "dst": "pit", "cap": 1,
         "siphon": True, "crest": rng.randint(2, 4),
         "open": rng.random() < 0.5},
        {"name": "p_gate_out", "src": "mid", "dst": "pit", "cap": 1,
         "siphon": False, "crest": 2, "open": True},
        {"name": "p_drain", "src": "pit", "dst": "waste", "cap": 2,
         "siphon": False, "crest": 2, "open": True},
    ]
    frames = _frames(rng, ticks, ["s1", "s2"], nodes, pipes, p_action=0.45)
    return _seq(seq_id, "economy", ticks, ["s1", "s2"], nodes, pipes, frames)


def _gen_fracture_loop(rng: random.Random, seq_id: str, ticks: int,
                       salt: str) -> dict[str, Any]:
    """Sustained full bore: boil 1/tick at basin -> steam -> condense at the
    cold crown -> cap-1 downpipe runs FULL BORE every tick -> stress +1/tick
    -> burst inside the [200, 400]+1 window (AC2/B1). 460 ticks covers the
    worst-case name_hash threshold. salt varies the pipe NAME so the djb2
    threshold differs per copy (name_hash parity is load-bearing here)."""
    down = f"p_down_{salt}"
    nodes = [
        {"name": "basin", "elev": 10, "kind": "plain", "sill": 0, "volume": 500},
        {"name": "crown_cold", "elev": 20, "kind": "cold", "sill": 0, "volume": 0},
        {"name": "low", "elev": 1, "kind": "plain", "sill": 0, "volume": 0},
        {"name": "floor", "elev": 0, "kind": "waste", "sill": 0, "volume": 0},
    ]
    pipes = [
        {"name": down, "src": "crown_cold", "dst": "low", "cap": 1,
         "siphon": False, "crest": 2, "open": True},
        {"name": "p_settle", "src": "low", "dst": "floor", "cap": 1,
         "siphon": False, "crest": 2, "open": True},
    ]
    forced = {t: [{"sid": "s1", "verb": "boil", "target": "basin"}]
              for t in range(ticks)}
    frames = _frames(rng, ticks, ["s1"], nodes, pipes, p_action=0.0,
                     forced=forced)
    return _seq(seq_id, "fracture_loop", ticks, ["s1"], nodes, pipes, frames)


def _gen_stress_domain(rng: random.Random, seq_id: str,
                       ticks: int) -> dict[str, Any]:
    """R8 stress family (2026-09-30): volumes ~1e15-1e17 straddling
    VOLUME_SAT (~9.223e15), where volume * DEPTH_SCALE crosses 2^63 and the
    unbounded-Python vs 64-bit-GDScript int domains used to part ways with
    no crash and no sensor. Shapes hit every saturation site: one-shot
    delivery across the ceiling (_move), ingest above the ceiling
    (add_node clamp + boundary-exact VOLUME_SAT state), gate-commit pooling
    + waste-basin absorption, and a deliberate full-bore burst whose mega
    spray saturates (_fracture). Pipes carry flow strictly below cap (cap =
    biggest volume + 10^12) so the AC2 fracture law never fires on the
    delivery shapes — mega full-bore flow would burst any pipe on tick 1
    (threshold <= 400 volume); the burst shape USES that on purpose.

    JSON int law (probed on Godot 4.3, receipt R8_INT_DOMAIN.md): the
    runner's JSON door parses numbers as float64, so odd values above 2^53
    silently round (9223372036586339 -> ...340) and would diverge the
    boards at ingest. Every magnitude here is a multiple of 10^12
    (divisible by 2^12 — exact in float64 far past 1e17) or derived from
    VOLUME_SAT by multiples of 10^12 (VOLUME_SAT is a multiple of 4, so
    the differences stay even — exact below 2^54)."""
    t12 = 10 ** 12
    shape = rng.choice(["one_shot_deliver", "ingest_over",
                        "gate_pool_ceiling", "burst_spray"])
    if shape == "one_shot_deliver":
        vol = rng.randint(1000, 100000) * t12          # 1e15 .. 1e17
        nodes = [
            {"name": "tank", "elev": 10, "kind": "plain", "sill": 0,
             "volume": vol},
            {"name": "pool", "elev": 0, "kind": "plain", "sill": 0,
             "volume": VOLUME_SAT - rng.randint(0, 9) * 10 * t12},
        ]
        pipes = [{"name": "p_mega", "src": "tank", "dst": "pool",
                  "cap": vol + t12, "siphon": False, "crest": 2,
                  "open": True}]
    elif shape == "ingest_over":
        vol = rng.randint(11000, 100000) * t12         # 1.1e16 .. 1e17: over
        nodes = [
            {"name": "tank", "elev": 10, "kind": "plain", "sill": 0,
             "volume": vol},                           # clamps at ingest
            {"name": "pool", "elev": 0, "kind": "plain", "sill": 0,
             "volume": 0},
        ]
        pipes = [{"name": "p_mega", "src": "tank", "dst": "pool",
                  "cap": VOLUME_SAT + t12, "siphon": False, "crest": 2,
                  "open": True}]                       # flow == VOLUME_SAT
                  # exactly (never == cap) -> boundary-exact pool state
    elif shape == "gate_pool_ceiling":
        vol = rng.randint(1000, 9000) * t12
        nodes = [
            {"name": "tank", "elev": 10, "kind": "plain", "sill": 0,
             "volume": vol},
            {"name": "gate", "elev": 5, "kind": "sill", "sill": 1,
             "volume": VOLUME_SAT - rng.randint(0, 9) * 10 * t12},
            {"name": "pit", "elev": 1, "kind": "waste", "sill": 0,
             "volume": VOLUME_SAT - rng.randint(0, 9) * 10 * t12},
        ]
        pipes = [
            {"name": "p_gate", "src": "tank", "dst": "gate",
             "cap": vol + t12, "siphon": False, "crest": 2, "open": True},
            {"name": "p_out", "src": "gate", "dst": "pit",
             "cap": VOLUME_SAT + t12, "siphon": False, "crest": 2,
             "open": True},
        ]
    else:  # burst_spray: cap == vol -> full bore tick 1 -> AC2 burst, and
    # the mega spray lands on the lowest node other than dst (the sump at
    # the ceiling's edge) -> _fracture's spray saturates.
        vol = rng.randint(1000, 9000) * t12
        nodes = [
            {"name": "tank", "elev": 10, "kind": "plain", "sill": 0,
             "volume": vol},
            {"name": "pool", "elev": 5, "kind": "plain", "sill": 0,
             "volume": 0},
            {"name": "sump", "elev": 0, "kind": "waste", "sill": 0,
             "volume": VOLUME_SAT - rng.randint(0, 9) * 10 * t12},
        ]
        pipes = [{"name": "p_burst", "src": "tank", "dst": "pool",
                  "cap": vol, "siphon": False, "crest": 2, "open": True}]
    frames = _frames(rng, ticks, ["s1"], nodes, pipes, p_action=0.10)
    return _seq(seq_id, "stress_domain", ticks, ["s1"], nodes, pipes, frames)


def _gen_receipt(rng: random.Random, seq_id: str, ticks: int,
                 variant: str) -> dict[str, Any]:
    """Q11 legality family (2026-10-01): deterministic frames that walk the
    server's receipt ladder — the chat verbs (say/whisper BAD_TEXT and
    UNKNOWN_TARGET arms), the LW7 gate (STALE_NONCE replay/unbind/bool/str,
    RATE_CAP including whisper-spends-the-window and rejects-don't), the
    standing water rejects, and the R3 frame-MAC keyless arms. Boards are
    trivial (legality is the subject, not physics); every sequence carries
    exactly `ticks` frames (empty frames after the script or after a tamper
    disconnect — the mix-shape law other tests pin).

    variants (rotated by sequence index so any >=2-receipt corpus covers a
    chat walk AND a MAC arm):
      chat      — the full ladder walk, unarmed connection
      mac_bare  — armed at tick 3; the armed frame strips its mac (strict
                  window: bare is tamper)
      mac_shape — armed; mac present but not 32 lowercase hex (SHAPE)
      mac_seq   — armed; shape-legal mac but seq 7 != expected 0 (SEQ)
    The TAG arm (HMAC under k_c2s) is unreachable by construction: the
    corpus cannot mint a tag without K (named in HarnessWorld).
    """
    nodes = [
        {"name": "a", "elev": 5, "kind": "plain", "sill": 0, "volume": 3},
        {"name": "b", "elev": 0, "kind": "plain", "sill": 0, "volume": 0},
    ]
    pipes: list[dict[str, Any]] = []
    script: list[list[dict[str, Any]]] = []
    arm_at = -1
    if variant == "chat":
        long_text = "x" * (_server_max_say() + 1)
        script = [
            # t1: legal chat + join (join targets a node, acks, applies at tick)
            [{"sid": "s1", "verb": "say", "target": "hello world", "n": 1},
             {"sid": "s2", "verb": "join", "target": "a", "n": 1}],
            # t2: BAD_TEXT (empty / over-length) spends the nonce but NOT
            # the cap — s2's third action still acks this tick
            [{"sid": "s1", "verb": "say", "target": "", "n": 2},
             {"sid": "s2", "verb": "say", "target": long_text, "n": 2},
             {"sid": "s2", "verb": "say", "target": "still ok", "n": 3}],
            # t3: whisper acks direct AND spends the window (an ack is an
            # ack) — s1's second action this tick is RATE_CAP
            [{"sid": "s1", "verb": "whisper", "target": "user_s2|psst", "n": 3},
             {"sid": "s1", "verb": "boil", "target": "a", "n": 4}],
            # t4: whisper arms — unknown user, missing '|', empty text
            [{"sid": "s1", "verb": "whisper", "target": "user_ghost|hi", "n": 5},
             {"sid": "s1", "verb": "whisper", "target": "noseparator", "n": 6},
             {"sid": "s1", "verb": "whisper", "target": "user_s2|", "n": 7},
             {"sid": "s1", "verb": "boil", "target": "a", "n": 8}],
            # t5: nonce law — replay (n<=hwm), unbind (stripped n after
            # bind); s2 acks then caps
            [{"sid": "s1", "verb": "boil", "target": "a", "n": 3},
             {"sid": "s1", "verb": "boil", "target": "a"},
             {"sid": "s2", "verb": "boil", "target": "a", "n": 4},
             {"sid": "s2", "verb": "tag", "target": "a", "n": 5}],
            # t6: nonce type law — a bool is a verdict, a string is not an
            # id (the X9 u8 law again)
            [{"sid": "s1", "verb": "boil", "target": "a", "n": True},
             {"sid": "s1", "verb": "boil", "target": "a", "n": "9"},
             {"sid": "s1", "verb": "boil", "target": "a", "n": 9}],
            # t7: the standing water rejects
            [{"sid": "s_ghost", "verb": "boil", "target": "a"},
             {"sid": "s1", "verb": "poke", "target": "a", "n": 10},
             {"sid": "s1", "verb": "tag", "target": "node_ghost", "n": 11},
             {"sid": "s1", "verb": "valve", "target": "p_ghost", "n": 12}],
            # t8: pool 'a' went dry (three boils applied t5-t7 windows)
            [{"sid": "s2", "verb": "boil", "target": "a", "n": 6}],
        ]
    else:
        arm_at = 3
        base = {"sid": "s1", "verb": "boil", "target": "a", "n": 2}
        if variant == "mac_bare":
            tamper = dict(base)                      # no seq/mac at all
        elif variant == "mac_shape":
            tamper = {**dict(base), "seq": 0, "mac": "nothex"}   # SHAPE
        else:  # mac_seq
            tamper = {**dict(base), "seq": 7, "mac": "ab" * 16}  # SEQ
        script = [
            [{"sid": "s1", "verb": "say", "target": "bare window", "n": 1}],
            [{"sid": "s2", "verb": "join", "target": "a", "n": 1}],
            [tamper],        # armed: BAD_MAC, the connection goes dark
            [{"sid": "s1", "verb": "say", "target": "never arrives", "n": 3}],
            [{"sid": "s2", "verb": "say", "target": "never arrives", "n": 2}],
        ]
    frames = [list(f) for f in script[:ticks]]
    frames += [[] for _ in range(ticks - len(frames))]
    seq = _seq(seq_id, "receipt", ticks, ["s1", "s2"], nodes, pipes, frames)
    if arm_at > 0:
        seq["arm_at_tick"] = arm_at
    return seq


# Q02 (2026-10-01, mountain_climb): the graded-head family shapes, ROTATED
# by sequence index (the receipt-variant pattern) so any corpus with 4+
# hydrology sequences covers every divergence direction, and a quick run's
# single sequence gets the composite cascade.
HYDRO_SHAPES = ("cascade", "equalize", "backwater", "head_hill")
HYDRO_CONDUCTANCES = (2, 4, 8, 16)


def _gen_hydrology(rng: random.Random, seq_id: str, ticks: int,
                   shape: str) -> dict[str, Any]:
    """Q02 hydrology family (2026-10-01, mountain_climb): graded-head /
    gradient-driven flow — the Watershed's rung-1 fixed point (mag/
    hydrology.py): head = elev*HEAD_SCALE + volume*DEPTH_SCALE //
    cross_section, flow = min(cap, src.volume, dHead*conductance >> 8),
    iterated per tick so stepped boards settle geometrically toward equal
    heads and stall at the Q8 quantization floor (dHead < 256//conductance
    -> flow 0). Where the boolean verdict law and the gradient part ways,
    BOTH directions — the Q02 FAIL was that neither was ever generated:

      cascade   — stepped elevations + varied cross-sections + a gated
                  junction and a crest siphon under the graded law; the
                  t0->t1 tier is engineered BACKWATER (t1 lower but
                  preloaded deep, so its head drowns t0's outlet), so the
                  composite board diverges from boolean law on tick 1.
      equalize  — SAME elevation: boolean never moves (no elev drop);
                  graded splits the pool until depths equalize (a filling
                  pool raises its own head — backwater/equalization).
      backwater — dst sits LOWER but is already deeper: boolean pours on
                  src.elev > dst.elev; graded REFUSES (dst head >= src
                  head + 256). The drowned inlet.
      head_hill — dst sits HIGHER but the src tank is narrow and deep:
                  boolean refuses (uphill); graded pours down the head
                  gradient.

    Volumes stay small (<= ~900, far under VOLUME_SAT — the int64 ceiling
    is stress_domain's subject; this family's subject is the gradient law
    itself). cross_section spans the boundary (1..8000): at cs=1 depth
    saturates the milli-depth scale (volume*1000), at cs=8000 a big pool
    is a puddle.

    Twin status, honestly: the GDScript ENGINE twin exists (water_graph.gd
    Z10 2026-09-30 port — HydroNode + the `hydrology` flag + conductance),
    but the parity RUNNER (roblox_to_godot/tests/rule_parity_runner.gd) is
    boolean-only and owned by another lane. So this family is
    Python-oracle FROZEN today: `all` stamps its per-tick hashes from
    mag.hydrology.HydrologyGraph (+ a byte-reproducibility rerun) instead
    of comparing live, and the future runner extension diffs against the
    frozen corpus. The physics laws are pinned on the module by
    tests/test_hydrology.py; the harness pins routing + both divergence
    directions in tests/test_rule_parity.py (Q02 block).
    """
    conductance = rng.choice(HYDRO_CONDUCTANCES)
    nodes: list[dict[str, Any]]
    pipes: list[dict[str, Any]]
    if shape == "equalize":
        # same elevation both sides: boolean law never moves a drop; the
        # gradient splits the pool until depths equalize. Volume is sized
        # so the initial dHead clears the Q8 floor at the LOWEST
        # conductance (dHead >= 256 -> flow >= 2 at conductance 2).
        e = rng.randint(2, 6)
        cs = rng.choice((1, 250, 500))
        vol = rng.randint(128, 320)
        nodes = [
            {"name": "pool_a", "elev": e, "kind": "plain", "sill": 0,
             "volume": vol, "cross_section": cs},
            {"name": "pool_b", "elev": e, "kind": "plain", "sill": 0,
             "volume": rng.choice((0, 0, rng.randint(1, vol // 4))),
             "cross_section": cs},
        ]
        pipes = [{"name": "p_level", "src": "pool_a", "dst": "pool_b",
                  "cap": rng.randint(2, 6), "siphon": False, "crest": 2,
                  "open": True}]
    elif shape == "backwater":
        # boolean pours (hi_e > lo_e); graded refuses — lo's preloaded
        # depth is engineered to hold head >= src head + 256 whatever the
        # conductance. The drowned inlet: a filling pool kills its feed.
        hi_e = rng.randint(6, 8)
        hi_vol = rng.randint(5, 40)
        lo_e = hi_e - rng.randint(3, 4)
        hi_head = hi_e * 256 + hi_vol * 1000 // 4000
        depth_need = hi_head - lo_e * 256 + rng.randint(1, 4) * 256
        nodes = [
            {"name": "shallow_hi", "elev": hi_e, "kind": "plain", "sill": 0,
             "volume": hi_vol, "cross_section": 4000},   # depth <= 10
            {"name": "deep_lo", "elev": lo_e, "kind": "plain", "sill": 0,
             "volume": depth_need * 200 // 1000 + 1,     # cs 200 -> ~depth_need
             "cross_section": 200},
        ]
        pipes = [{"name": "p_drown", "src": "shallow_hi", "dst": "deep_lo",
                  "cap": rng.randint(1, 4), "siphon": False, "crest": 2,
                  "open": True}]
    elif shape == "head_hill":
        # dst HIGHER in elevation; src narrow and deep: boolean refuses
        # (uphill), graded pours down the head gradient (depth beats the
        # climb by >= 256 head units).
        src_e = rng.randint(2, 5)
        climb = rng.randint(1, 3)
        cs = rng.choice((100, 200, 250))
        depth_need = climb * 256 + rng.randint(1, 5) * 256
        nodes = [
            {"name": "deep_src", "elev": src_e, "kind": "plain", "sill": 0,
             "volume": depth_need * cs // 1000 + 1, "cross_section": cs},
            {"name": "high_flat", "elev": src_e + climb, "kind": "plain",
             "sill": 0, "volume": 0, "cross_section": 4000},
        ]
        pipes = [{"name": "p_hill", "src": "deep_src", "dst": "high_flat",
                  "cap": rng.randint(1, 6), "siphon": False, "crest": 2,
                  "open": True}]
    else:  # cascade — the composite: multi-tier dHead settling, a gated
    # junction fed by chain + siphon (graded probes into xor/sill), and the
    # drowned t0->t1 tier guaranteeing boolean-vs-graded divergence.
        tiers = rng.randint(3, 4)
        top = rng.randint(10, 14)
        step = rng.randint(2, 3)
        t0_vol = rng.randint(150, 600)
        t0_cs = rng.choice((250, 500, 1000, 2000))
        t1_depth = (t0_vol * 1000 // t0_cs) + step * 256 \
            + rng.randint(1, 3) * 256       # t1 head drowns t0's outlet
        nodes = [
            {"name": "t0", "elev": top, "kind": "plain", "sill": 0,
             "volume": t0_vol, "cross_section": t0_cs},
            {"name": "t1", "elev": top - step, "kind": "plain", "sill": 0,
             "volume": t1_depth * 100 // 1000 + 1, "cross_section": 100},
        ]
        for i in range(2, tiers):
            nodes.append({"name": f"t{i}", "elev": top - i * step,
                          "kind": "plain", "sill": 0, "volume": 0,
                          "cross_section": rng.choice((250, 500, 1000, 2000))})
        gate_kind = rng.choice(("sill", "xor"))
        nodes.append({"name": "gate", "elev": max(0, top - tiers * step),
                      "kind": gate_kind,
                      "sill": rng.randint(1, 2) if gate_kind == "sill" else 0,
                      "volume": 0, "cross_section": rng.choice((250, 1000))})
        nodes.append({"name": "pit", "elev": 0, "kind": "plain", "sill": 0,
                      "volume": 0, "cross_section": 1000})
        pipes = []
        for i in range(tiers - 1):
            pipes.append({"name": f"p_c{i}", "src": f"t{i}", "dst": f"t{i+1}",
                          "cap": rng.randint(1, 4), "siphon": False,
                          "crest": 2, "open": True})
        pipes.append({"name": "p_chain_out", "src": f"t{tiers - 1}",
                      "dst": "gate", "cap": rng.randint(1, 4), "siphon": False,
                      "crest": 2, "open": True})
        pipes.append({"name": "p_siphon", "src": "t0", "dst": "gate",
                      "cap": rng.randint(1, 3), "siphon": True,
                      "crest": rng.randint(2, 4), "open": True})
        pipes.append({"name": "p_gate_out", "src": "gate", "dst": "pit",
                      "cap": rng.randint(1, 3), "siphon": False, "crest": 2,
                      "open": True})
    frames = _frames(rng, ticks, ["s1"], nodes, pipes, p_action=0.15)
    seq = _seq(seq_id, "hydrology", ticks, ["s1"], nodes, pipes, frames)
    seq["conductance"] = conductance
    seq["shape"] = shape
    return seq


def _gen_random(rng: random.Random, seq_id: str, ticks: int) -> dict[str, Any]:
    n = rng.randint(4, 8)
    kinds = (["plain"] * (n - 2)
             + [rng.choice(["xor", "sill"]) for _ in range(rng.randint(1, 2))]
             + [rng.choice(["waste", "cold"]) for _ in range(rng.randint(0, 1))])
    kinds = kinds[:n] or ["plain"]
    elevs = rng.sample(range(0, 21), n)
    nodes = []
    for i in range(n):
        kind = kinds[i] if i < len(kinds) else "plain"
        nodes.append({"name": f"n{i}", "elev": elevs[i], "kind": kind,
                      "sill": rng.randint(1, 2) if kind == "sill" else 0,
                      "volume": rng.randint(0, 6) if kind != "cold" else 0})
    pipes = []
    n_pipes = rng.randint(3, 9)
    for i in range(n_pipes):
        src, dst = rng.sample(range(n), 2)
        pipes.append({"name": f"rp{i}", "src": f"n{src}", "dst": f"n{dst}",
                      "cap": rng.randint(1, 3),
                      "siphon": rng.random() < 0.2,
                      "crest": rng.randint(2, 5),
                      "open": rng.random() < 0.85})
    frames = _frames(rng, ticks, ["s1", "s2"], nodes, pipes, p_action=0.4)
    return _seq(seq_id, "random", ticks, ["s1", "s2"], nodes, pipes, frames)


def generate(seed: int, n: int, ticks: int, loop_ticks: int = 460) -> dict[str, Any]:
    rng = random.Random(seed)
    # mountain share scales with corpus size (D2 mix law): n>=60 keeps the
    # v0 shape (20 mountain, receipt-compatible), small n gets max(4, n//5)
    # so a 20-seq quick run still exercises every family — the LW5
    # gated-siblings seam (where the v0 divergence lives) must never be
    # squeezed out by 20 mountain copies.
    mtn = 20 if n >= 60 else max(4, n // 5)
    mix: list[tuple[str, int]] = [("mountain", min(mtn, n))]
    left = n - mix[0][1]
    # R8 (2026-09-30): stress_domain joins the family table (0.08), carved
    # from random (0.46 -> 0.38) — the same-seed corpus bytes shift vs the
    # V5 receipt run (receipt R8_INT_DOMAIN.md names the amendment); every
    # mode still covers every family, and total frame counts are unchanged
    # (all non-fracture families share the profile tick count).
    # Q11 (2026-10-01): receipt joins (0.08, random 0.38 -> 0.30) — the
    # legality-ladder family (chat verbs + nonce/cap + keyless MAC arms);
    # frames still `ticks` each, so the 14,040 full-corpus total holds.
    # Q02 (2026-10-01): hydrology joins (0.06, carved from economy
    # 0.24 -> 0.22 and random 0.30 -> 0.26 — the LW5 gated-siblings seam
    # keeps its full 0.24) — the graded-head family; frames still `ticks`
    # each, so the 14,040 full-corpus total holds, and quick (n=20) still
    # lands 1 sequence on every family including random.
    plan = [("gated_siblings", 0.24), ("economy", 0.22),
            ("fracture_loop", 0.06), ("stress_domain", 0.08),
            ("receipt", 0.08), ("hydrology", 0.06), ("random", 0.26)]
    for fam, frac in plan:
        take = min(left, max(0, round(n * frac))) if left > 0 else 0
        mix.append((fam, take))
        left -= take
    # any rounding shortfall rides on random
    mix[-1] = (mix[-1][0], mix[-1][1] + left)

    sequences: list[dict[str, Any]] = []
    idx = 0
    receipt_variants = ("chat", "mac_bare", "mac_shape", "mac_seq")
    receipt_seen = 0
    hydro_seen = 0
    for fam, count in mix:
        for _ in range(count):
            seq_id = f"seq_{idx:03d}"
            if fam == "mountain":
                sequences.append(_gen_mountain(rng, seq_id, ticks))
            elif fam == "gated_siblings":
                sequences.append(_gen_siblings(rng, seq_id, ticks))
            elif fam == "economy":
                sequences.append(_gen_economy(rng, seq_id, ticks))
            elif fam == "fracture_loop":
                sequences.append(_gen_fracture_loop(
                    rng, seq_id, loop_ticks, salt=f"{seed}_{idx}"))
            elif fam == "stress_domain":
                sequences.append(_gen_stress_domain(rng, seq_id, ticks))
            elif fam == "receipt":
                # chat walk on every even receipt slot, a MAC arm on every
                # odd one — any >=2-receipt corpus covers both classes
                variant = ("chat" if receipt_seen % 2 == 0
                           else receipt_variants[1 + (receipt_seen // 2) % 3])
                sequences.append(_gen_receipt(rng, seq_id, ticks, variant))
                receipt_seen += 1
            elif fam == "hydrology":
                # shapes rotate (the receipt-variant pattern): any corpus
                # with 4+ hydrology sequences covers every divergence
                # direction; a quick run's single sequence gets cascade.
                shape = HYDRO_SHAPES[hydro_seen % len(HYDRO_SHAPES)]
                sequences.append(_gen_hydrology(rng, seq_id, ticks, shape))
                hydro_seen += 1
            else:
                sequences.append(_gen_random(rng, seq_id, ticks))
            idx += 1
    return {"schema": SCHEMA, "seed": seed, "verbs": list(_server_verbs()),
            "max_say": _server_max_say(),
            "ticks_default": ticks, "sequences": sequences}


# ------------------------------------------------------------ python side ----

def run_python(doc: dict[str, Any]) -> list[dict[str, Any]]:
    verbs = tuple(doc["verbs"])
    max_say = int(doc.get("max_say", _server_max_say()))
    out: list[dict[str, Any]] = []
    for seq in doc["sequences"]:
        # Q02: the hydrology family rides the SAME receipt ladder around
        # the graded oracle (mag.hydrology.HydrologyGraph); every other
        # family stays on the boolean WaterGraph. The frozen oracle rows
        # are whatever comes out here — tests pin that this routing is
        # real (a silent boolean fallthrough would freeze the WRONG law).
        graded = seq.get("family") == "hydrology"
        w = HarnessWorld(seq, verbs, max_say=max_say, graded=graded,
                         conductance=int(seq.get("conductance", 8)))
        for t, frame in enumerate(seq["frames"], start=1):
            row = w.tick_frame(frame, tick_no=t)
            out.append({"seq": seq["id"], "family": seq["family"],
                        "tick": t, **row})
    return out


# ------------------------------------------------------------ godot side ----

def run_godot(doc_path: Path, out_path: Path) -> None:
    if not GODOT_EXE.exists():
        raise FileNotFoundError(f"godot binary missing: {GODOT_EXE}")
    # absolute paths: the runner's cwd is the godot project dir
    doc_path, out_path = doc_path.resolve(), out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(GODOT_EXE), "--headless", "--path", str(GODOT_PROJECT),
           "--script", GD_RUNNER, "--", str(doc_path), str(out_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(GODOT_PROJECT), timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(f"godot runner exited {proc.returncode}\n"
                           f"stdout:\n{proc.stdout[-2000:]}\n"
                           f"stderr:\n{proc.stderr[-2000:]}")


# -------------------------------------------------------------- compare ----

def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _state_diff(py: dict[str, Any], gd: dict[str, Any]) -> list[str]:
    diffs: list[str] = []
    for kind in ("nodes", "pipes"):
        pyf, gdf = py[kind], gd[kind]
        for name in sorted(set(pyf) | set(gdf)):
            a, b = pyf.get(name), gdf.get(name)
            if a is None or b is None:
                diffs.append(f"{kind}.{name}: only one side has it "
                             f"(py={a is not None}, gd={b is not None})")
                continue
            for f in sorted(set(a) | set(b)):
                if a.get(f) != b.get(f):
                    av, bv = a.get(f), b.get(f)
                    diffs.append(f"{kind}.{name}.{f}: py={av} gd={bv}")
                    if isinstance(av, bool) or isinstance(bv, bool):
                        # json roundtrip may say true/false vs 1/0 — normalize
                        if int(bool(av)) == int(bool(bv)):
                            diffs[-1] += " (bool/int encoding only)"
    if py.get("tick") != gd.get("tick"):
        diffs.append(f"tick: py={py.get('tick')} gd={gd.get('tick')}")
    return diffs[:40]


def compare(py_rows: list[dict[str, Any]], gd_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Walk both sides in (seq, tick) order. first_divergence = the earliest
    (seq, tick) where hash or verdicts differ (or a row is missing on one
    side). per_family rolls up EVERY sequence (past the first divergence
    too) so the receipt can say which families held everywhere."""
    def key(r):
        return (r["seq"], r["tick"])

    py_by = {key(r): r for r in py_rows}
    gd_by = {key(r): r for r in gd_rows}
    order = [key(r) for r in py_rows]
    fam_of = {r["seq"]: r["family"] for r in py_rows}
    fam_stats: dict[str, dict[str, Any]] = {
        fam: {"sequences": 0, "diverged_seqs": 0, "first_tick": None}
        for fam in sorted(set(fam_of.values()))}
    for seq_id in dict.fromkeys(s for s, _ in order):
        fam_stats[fam_of[seq_id]]["sequences"] += 1

    report: dict[str, Any] = {"parity": True, "rows_py": len(py_rows),
                              "rows_gd": len(gd_rows), "first_divergence": None,
                              "per_family": fam_stats}

    def make_fd(k, kind, py=None, gd=None):
        fd: dict[str, Any] = {"seq": k[0], "family": fam_of.get(k[0], "?"),
                              "tick": k[1], "kind": kind}
        if py is not None:
            fd["hash_py"] = py["hash"]
            fd["hash_gd"] = gd["hash"]
            fd["state_diff"] = _state_diff(py["state"], gd["state"])
        fd["verdicts_py"] = (py or {}).get("verdicts")
        fd["verdicts_gd"] = (gd or {}).get("verdicts")
        return fd

    # first divergence in (seq-order, tick-order)
    for k in order:
        if k not in gd_by:
            report["parity"] = False
            report["first_divergence"] = make_fd(k, "missing_on_godot_side")
            break
        py, gd = py_by[k], gd_by[k]
        if py["hash"] != gd["hash"]:
            report["parity"] = False
            report["first_divergence"] = make_fd(k, "state_hash", py, gd)
            break
        if py.get("verdicts") != gd.get("verdicts"):
            report["parity"] = False
            report["first_divergence"] = make_fd(k, "verdicts", py, gd)
            break
    if report["parity"]:
        extras = sorted(k for k in gd_by if k not in py_by)
        if extras:
            report["parity"] = False
            s, t = extras[0]
            report["first_divergence"] = make_fd((s, t), "extra_on_godot_side")

    # full walk for the family rollup (every divergent seq, not just the first)
    seen_first_bad: set[str] = set()
    for k in order:
        bad = (k not in gd_by or py_by[k]["hash"] != gd_by[k]["hash"]
               or py_by[k].get("verdicts") != gd_by[k].get("verdicts"))
        if not bad:
            continue
        fam = fam_of[k[0]]
        if k[0] not in seen_first_bad:
            seen_first_bad.add(k[0])
            fam_stats[fam]["diverged_seqs"] += 1
        if fam_stats[fam]["first_tick"] is None or k[1] < fam_stats[fam]["first_tick"]:
            fam_stats[fam]["first_tick"] = k[1]
    return report


# ------------------------------------------------------------------- io ----

def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")


def cmd_gen(args: argparse.Namespace) -> int:
    doc = generate(args.seed, args.n, args.ticks)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
    fams: dict[str, int] = {}
    for s in doc["sequences"]:
        fams[s["family"]] = fams.get(s["family"], 0) + 1
    total_ticks = sum(len(s["frames"]) for s in doc["sequences"])
    print(f"gen: {len(doc['sequences'])} sequences ({fams}), "
          f"{total_ticks} tick frames -> {args.out}")
    return 0


def cmd_python(args: argparse.Namespace) -> int:
    doc = json.loads(args.inp.read_text(encoding="utf-8"))
    rows = run_python(doc)
    _write_jsonl(args.out, rows)
    print(f"python: {len(rows)} tick rows -> {args.out}")
    return 0


def cmd_godot(args: argparse.Namespace) -> int:
    run_godot(args.inp, args.out)
    n = len(_load_jsonl(args.out))
    print(f"godot: {n} tick rows -> {args.out}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    report = compare(_load_jsonl(args.py), _load_jsonl(args.gd))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1, sort_keys=True), encoding="utf-8")
    _print_report(report)
    return 0 if report["parity"] else 1


def _print_report(report: dict[str, Any]) -> None:
    print(f"parity: {report['parity']}  "
          f"(rows py={report['rows_py']} gd={report['rows_gd']})")
    for fam, st in sorted(report["per_family"].items()):
        print(f"  {fam}: {st['sequences']} seqs, diverged {st['diverged_seqs']}, "
              f"first divergent tick {st['first_tick']}")
    hyd = report.get("hydrology_oracle")
    if hyd:
        print(f"  hydrology: oracle-frozen, NOT compared live "
              f"({hyd['sequences']} seqs, {hyd['rows']} rows, "
              f"byte-reproducible; python-only — {hyd['twin'].split(' — ')[1]}")
    fd = report["first_divergence"]
    if fd:
        print(f"FIRST DIVERGENCE: {fd['seq']} ({fd['family']}) tick {fd['tick']} "
              f"kind={fd['kind']}")
        if fd.get("hash_py"):
            print(f"  hash_py = {fd['hash_py']}")
            print(f"  hash_gd = {fd['hash_gd']}")
        for line in fd.get("state_diff", [])[:20]:
            print(f"  {line}")
        if fd.get("verdicts_py") is not None and fd.get("verdicts_gd") is not None:
            print(f"  verdicts_py = {fd['verdicts_py']}")
            print(f"  verdicts_gd = {fd['verdicts_gd']}")


# ------------------------------------------------------- ci profiles (D2) ----

def resolve_params(mode: str, seed: int | None, n: int | None,
                   ticks: int | None) -> dict[str, int]:
    """Explicit CLI flags beat the profile preset; the preset beats nothing.
    mode 'full' presets exactly the V5 receipt corpus (back-compat)."""
    prof = PROFILES[mode]
    return {"seed": seed if seed is not None else prof["seed"],
            "n": n if n is not None else prof["n"],
            "ticks": ticks if ticks is not None else prof["ticks"]}


def total_frames(doc: dict[str, Any]) -> int:
    return sum(len(s["frames"]) for s in doc["sequences"])


def twin_digest() -> dict[str, Any]:
    """Content sha256 (first 12) of each parity twin at run time — the
    standing artifact names WHICH engine bytes the verdict is about, so a
    dirty working tree can never hide behind a stale latest.json. The pair
    is exactly the gate's trigger pathspecs (pinned by
    tests/test_parity_gate_hook_pin.py); the Q02 hydrology oracle's engine
    digest rides in report['hydrology_oracle'], not here."""
    out: dict[str, Any] = {}
    for label, rel in (("py", TWIN_PY), ("gd", TWIN_GD)):
        p = ROOT / rel
        out[label] = {"path": rel,
                      "sha256_12": hashlib.sha256(p.read_bytes()).hexdigest()[:12]
                      if p.exists() else "MISSING"}
    return out


def _write_latest(out_dir: Path, mode: str, params: dict[str, int],
                  frames: int | None, wall: float, source: str,
                  report: dict[str, Any] | None, exit_code: int,
                  error: str | None = None) -> Path:
    doc: dict[str, Any] = {
        "schema": LATEST_SCHEMA,
        "mode": mode, "seed": params["seed"], "n": params["n"],
        "ticks": params["ticks"], "total_frames": frames,
        "wall_seconds": round(wall, 2),
        "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        "parity": report["parity"] if report is not None else None,
        "exit_code": exit_code,
        "first_divergence": report["first_divergence"] if report is not None else None,
        "per_family": report["per_family"] if report is not None else None,
        "hydrology_oracle": report.get("hydrology_oracle") if report is not None else None,
        "rows_py": report["rows_py"] if report is not None else None,
        "rows_gd": report["rows_gd"] if report is not None else None,
        "error": error,
        "twins": twin_digest(),
        "profiles": {k: dict(v) for k, v in PROFILES.items()},
        "godot_exe_present": GODOT_EXE.exists(),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / LATEST_NAME
    path.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
    return path


def cmd_all(args: argparse.Namespace) -> int:
    mode = args.mode
    params = resolve_params(mode, args.seed, args.n, args.ticks)
    d = args.out_dir
    base = "quick" if mode == "quick" else "parity"  # full keeps v0 legacy names
    # Q02 (2026-10-01): four artifacts instead of three. inp = the FULL
    # corpus (every family, hydrology included — the canonical input the
    # future hydrology-capable .gd runner will consume); gd_inp = the
    # cross-engine subset today's boolean-only runner may lawfully consume;
    # py_out = the comparable cross-engine rows; hyd_out = the FROZEN
    # hydrology oracle rows (per-tick hashes from mag.hydrology, checked
    # byte-reproducible at freeze time — the future twin's byte target).
    inp = d / f"{base}_inputs.json"
    gd_inp = d / f"{base}_gd_inputs.json"
    py_out = d / f"{base}_python.jsonl"
    hyd_out = d / f"{base}_hydrology.jsonl"
    gd_out = d / f"{base}_godot.jsonl"
    rep = d / f"{base}_report.json"
    t0 = time.monotonic()
    try:
        doc = generate(params["seed"], params["n"], params["ticks"])
        inp.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
        rows = run_python(doc)
        hydro_rows = [r for r in rows if r["family"] == "hydrology"]
        cross_rows = [r for r in rows if r["family"] != "hydrology"]
        _write_jsonl(py_out, cross_rows)
        if hydro_rows:
            _write_jsonl(hyd_out, hydro_rows)
            hyd_doc = {"schema": doc["schema"], "verbs": doc["verbs"],
                       "max_say": doc["max_say"],
                       "sequences": [s for s in doc["sequences"]
                                     if s["family"] == "hydrology"]}
            rerun = run_python(hyd_doc)
            if json.dumps(rerun, sort_keys=True) != json.dumps(hydro_rows,
                                                               sort_keys=True):
                raise RuntimeError("hydrology oracle rerun diverged from the "
                                   "frozen rows (not byte-reproducible)")
        gd_doc = {k: v for k, v in doc.items() if k != "sequences"}
        gd_doc["sequences"] = [s for s in doc["sequences"]
                               if s["family"] != "hydrology"]
        gd_inp.write_text(json.dumps(gd_doc, indent=1, sort_keys=True),
                          encoding="utf-8")
        run_godot(gd_inp, gd_out)
        report = compare(cross_rows, _load_jsonl(gd_out))
        if hydro_rows:
            # honest bookkeeping: hydrology was NOT compared live (there is
            # no runner twin today) — the rollup row says 0 diverged because
            # nothing was diffed, and hydrology_oracle names the freeze.
            n_hyd = len({r["seq"] for r in hydro_rows})
            report["per_family"]["hydrology"] = {
                "sequences": n_hyd, "diverged_seqs": 0, "first_tick": None}
            hp = ROOT / TWIN_HYDRO
            report["hydrology_oracle"] = {
                "engine": "mag/hydrology.py HydrologyGraph (graded head, rung 1)",
                "engine_sha256_12": hashlib.sha256(
                    hp.read_bytes()).hexdigest()[:12] if hp.exists() else "MISSING",
                "twin": "frozen-oracle (GDScript engine twin exists: "
                        "water_graph.gd Z10 hydrology flag; the parity runner "
                        "is boolean-only — the future runner extension diffs "
                        f"against {hyd_out.name})",
                "sequences": n_hyd, "rows": len(hydro_rows),
                "byte_reproducible": True}
    except Exception as exc:  # instrument error: honest artifact + exit 2
        wall = time.monotonic() - t0
        err = f"{type(exc).__name__}: {str(exc)[:300]}"
        print(f"PARITY: ERROR mode={mode} {err}")
        _write_latest(d, mode, params, None, wall, args.source, None, 2, error=err)
        return 2
    wall = time.monotonic() - t0
    rep.write_text(json.dumps(report, indent=1, sort_keys=True), encoding="utf-8")
    exit_code = 0 if report["parity"] else 1
    # first-line contract (B2-338 law): the hook case-matches this prefix
    if report["parity"]:
        print(f"PARITY: ok mode={mode} rows_py={report['rows_py']}")
    else:
        fd = report["first_divergence"]
        print(f"PARITY: FAIL mode={mode} first={fd['seq']} "
              f"family={fd['family']} tick={fd['tick']} kind={fd['kind']}")
    latest = _write_latest(d, mode, params, total_frames(doc), wall,
                           args.source, report, exit_code)
    print(f"artifacts in {d} (standing verdict: {latest})")
    _print_report(report)
    if mode == "quick" and wall > QUICK_WALL_BUDGET_S:
        print(f"WARN: quick run took {wall:.1f}s (budget {QUICK_WALL_BUDGET_S:.0f}s) "
              f"— pre-push cost drift, tighten the quick profile")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="generate seeded input sequences")
    g.add_argument("--seed", type=int, default=20260930)
    g.add_argument("--n", type=int, default=100)
    g.add_argument("--ticks", type=int, default=120)
    g.add_argument("--out", type=Path, default=DEFAULT_OUT / "parity_inputs.json")
    g.set_defaults(func=cmd_gen)

    q = sub.add_parser("python", help="run the Python side (water_graph + legality)")
    q.add_argument("--in", dest="inp", type=Path, required=True)
    q.add_argument("--out", type=Path, default=DEFAULT_OUT / "parity_python.jsonl")
    q.set_defaults(func=cmd_python)

    r = sub.add_parser("godot", help="run the GDScript side (headless godot)")
    r.add_argument("--in", dest="inp", type=Path, required=True)
    r.add_argument("--out", type=Path, default=DEFAULT_OUT / "parity_godot.jsonl")
    r.set_defaults(func=cmd_godot)

    c = sub.add_parser("compare", help="diff per-tick hashes + verdicts")
    c.add_argument("--py", type=Path, required=True)
    c.add_argument("--gd", type=Path, required=True)
    c.add_argument("--out", type=Path, default=DEFAULT_OUT / "parity_report.json")
    c.set_defaults(func=cmd_compare)

    a = sub.add_parser("all", help="gen + python + godot + compare, one shot")
    mode_g = a.add_mutually_exclusive_group()
    mode_g.add_argument("--quick", action="store_const", dest="mode",
                        const="quick",
                        help=f"pre-push profile: {PROFILES['quick']} "
                             f"(<{QUICK_WALL_BUDGET_S:.0f}s budget)")
    mode_g.add_argument("--full", action="store_const", dest="mode",
                        const="full",
                        help=f"nightly profile: {PROFILES['full']} "
                             "(V5 receipt corpus; the default)")
    a.set_defaults(mode="full")
    a.add_argument("--seed", type=int, default=None,
                   help="override the profile seed (default: profile preset)")
    a.add_argument("--n", type=int, default=None,
                   help="override the profile sequence count")
    a.add_argument("--ticks", type=int, default=None,
                   help="override the profile tick count")
    a.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                   help=f"artifact dir (default {DEFAULT_OUT}; "
                        f"{LATEST_NAME} lands beside the run artifacts)")
    a.add_argument("--source", default="manual",
                   help="who ran this (prepush|nightly|manual) -> latest.json")
    a.set_defaults(func=cmd_all)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
