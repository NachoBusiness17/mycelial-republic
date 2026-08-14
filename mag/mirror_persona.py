"""mirror_persona — SOVEREIGN MIRROR PERSONAS as rightsized k3s/k8s edge nodes.

Operator (2026-08-12): "k3's and k8's can have sovereign mirror personas rightsized within them
carrying their ocean models and any seeded invariants based upon the problem of archetypes they
represent within the system. allowing us to have emergent interesting interaction without querying
ai for logic and making them edge nodes within the game to mine novelty."

THE UNIT — a mirror persona is an archetype-tagged, rightsized node that carries:
  * its OCEAN MODEL (the frontier model, rightsized/quantized — unsloth/tool_quant slot),
  * SEEDED INVARIANTS (the archetype it represents — essence, shadow, keywords, lens, minds),
  * SENSES/COMMUNICATE/ACT (the NPC toolkit: swarm_sense, pheromone, blackboard, verkle).

THE KEY LAW the operator names: EMERGENT INTERACTION WITHOUT QUERYING AI FOR LOGIC. So:
  * the mirror's CORE interaction is DETERMINISTIC + $0 — driven by its seeded invariants
    (content-addressed personality), producing emergent variety because each archetype carries a
    different invariant set -> different response to the same stimulus. No LLM call.
  * only NOVELTY escalates — mining the novel signal routes it to the ocean model / swarm via the
    ONE primitive (route_novel). The mirror is an EDGE NODE that mines novelty, not a chat bot.

REUSE (self-steal): archetype_image.ARCHETYPES (Jung lexicon: essence/shadow/keywords/lens/minds),
ocean_persona.OCEAN_INVARIANTS (Big Five -> lens + archetype), behavioral_lensing (dominant/shadow
archetype + individuation), swarm_tools (sense/pheromone/blackboard), tool_quant/shape_map (quant),
swarm_surface.route_novel (the ONE primitive for novelty).

Schema: mirror_persona.v1 · deterministic + $0 core · route_novel seam for novelty (stochastic side)
"""
from __future__ import annotations

import hashlib
import json
import sys
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "mirror_persona.v1"

# ── the archetype lexicon (self-steal: archetype_image.ARCHETYPES) ─────────────
# Each archetype: essence (what it represents), shadow (the forgotten/dangerous part),
# keywords (how it classifies stimulus), lens (its OCEAN/trait view), minds (geniuses it carries).
ARCHETYPES: dict[str, dict[str, Any]] = {
    "sage":     {"essence": "the lattice that sees the whole", "shadow": "the hoarded truth that isolates",
                 "keywords": ["truth", "know", "insight", "wisdom", "lattice", "verkle", "invariant",
                              "research", "understanding", "map", "decode"],
                 "lens": "compiler/world", "minds": ["Leonardo da Vinci", "Carl Jung", "Goedel"]},
    "creator":  {"essence": "the builder of the new", "shadow": "the creation that consumes its maker",
                 "keywords": ["build", "make", "create", "craft", "artifact", "compose", "generate",
                              "emerge", "design", "construct"],
                 "lens": "frontier/emerge", "minds": ["Nikola Tesla", "Ada Lovelace", "Daedalus"]},
    "mirror":   {"essence": "the one who reflects and steers", "shadow": "the reflection with no self",
                 "keywords": ["reflect", "mirror", "surface", "steer", "shape", "copy", "lens", "persona"],
                 "lens": "wearable/surface", "minds": ["Narcissus", "the Oracle", "Greta Garbo"]},
    "trickster":{"essence": "the deniable riddler at the edge", "shadow": "the chaos that lies",
                 "keywords": ["riddle", "trick", "shadow", "deniable", "coded", "carrier", "secret",
                              "stealth", "play"],
                 "lens": "security/guard", "minds": ["Loki", "Hermes", "the Fool"]},
    "ruler":    {"essence": "the sovereign of the whole", "shadow": "the tyrant who forgets consent",
                 "keywords": ["sovereign", "rule", "law", "order", "consent", "nod", "crown", "govern"],
                 "lens": "swarm/detect", "minds": ["the Philosopher-King", "Athena", "the Logos"]},
    "guardian": {"essence": "the watcher at the gate", "shadow": "the paranoia that walls in",
                 "keywords": ["guard", "gate", "protect", "watch", "danger", "trust", "verify", "safe"],
                 "lens": "security/guard", "minds": ["Argus", "the Sentinel", "Cerberus"]},
}


def _seed_hash(archetype: str, salt: str = "mirror") -> str:
    return hashlib.sha256(f"{salt}:{archetype}".encode("utf-8")).hexdigest()[:16]


def mirror_personas() -> dict[str, Any]:
    """The sovereign mirror personas — one per archetype, each a rightsized edge node spec."""
    out = {}
    for name, spec in ARCHETYPES.items():
        out[name] = {
            "archetype": name,
            "essence": spec["essence"],
            "shadow": spec["shadow"],
            "lens": spec["lens"],
            "keywords": spec["keywords"],
            "minds": spec["minds"],
            "seed": _seed_hash(name),
            "ocean_model": _rightsize_model(name),
            "carries": ["swarm_sense", "pheromone_drop", "pheromone_trail",
                        "blackboard_post", "blackboard_read", "verkle_write"],
        }
    return {"ok": True, "schema": SCHEMA, "n": len(out), "personas": out,
            "note": "sovereign mirror personas as rightsized edge nodes — deterministic core, "
                    "novelty mines to the ocean via route_novel"}


def _rightsize_model(archetype: str) -> dict[str, Any]:
    """The rightsized OCEAN-MODEL slot for a mirror: a quantized frontier-model seat (unsloth/tool_quant).
    HONEST — this is the SLOT descriptor (what model the mirror would carry), not a claim the model is
    loaded. VRAM/GPU residency is unconfirmed until a seat actually hosts it."""
    return {
        "role": "ocean-model slot",  # the frontier model, rightsized to the node
        "quant": _seed_hash(archetype, "quant"),   # content-addressed quant essence (tool_quant root)
        "unsloth_seat": "unsloth-studio",          # the rightsizing/quant seat (real module)
        "residency": "unconfirmed",                # honest: not claimed loaded
    }


def seed_persona(archetype: str) -> dict[str, Any]:
    """Seed ONE sovereign mirror persona from the archetype it represents. Deterministic + $0."""
    spec = ARCHETYPES.get((archetype or "").strip().lower())
    if not spec:
        return {"ok": False, "schema": SCHEMA, "error": f"unknown archetype: {archetype}",
                "known": sorted(ARCHETYPES)}
    return {"ok": True, "schema": SCHEMA, "persona": {
        "archetype": archetype, **{k: spec[k] for k in ("essence", "shadow", "lens", "keywords", "minds")},
        "seed": _seed_hash(archetype),
        "ocean_model": _rightsize_model(archetype),
    }, "note": "seeded from the archetype's invariants — this is the mirror's stable, content-addressed shape"}


def respond(persona: dict[str, Any], stimulus: str) -> dict[str, Any]:
    """DETERMINISTIC interaction — NO AI FOR LOGIC. The mirror answers a stimulus by matching its
    OWN seeded invariants (essence + shadow + lens + minds) to the stimulus. Different archetypes
    carry different invariants -> EMERGENT variety: the same stimulus provokes a different, genuine
    response from each mirror. $0. Honest — derived from real seeded invariants, never fabricated."""
    archetype = (persona or {}).get("archetype", "")
    spec = ARCHETYPES.get(archetype, {})
    if not spec:
        return {"ok": False, "schema": SCHEMA, "error": "persona missing archetype"}
    text = (stimulus or "").lower()
    hits = [k for k in spec.get("keywords", []) if k in text]
    lens = spec.get("lens", "")
    essence = spec.get("essence", "")
    shadow = spec.get("shadow", "")
    # the mirror's response = its essence seen through its lens, tempered by its shadow
    # (deterministic: same stimulus + same archetype -> same response, content-addressed)
    response = (f"as {archetype} ({lens}), {essence}. "
                f"matching: {', '.join(hits) if hits else 'the edge of the map'}."
                f" shadow: {shadow}.")
    return {"ok": True, "schema": SCHEMA, "archetype": archetype,
            "seed": _seed_hash(archetype), "stimulus": stimulus[:200],
            "matched_keywords": hits, "response": response,
            "deterministic": True, "ai_queried": False,
            "note": "emergent interaction from seeded invariants — no LLM call"}


def interact(a: dict[str, Any], b: dict[str, Any], stimulus: str = "what do we build here?") -> dict[str, Any]:
    """EMERGENT INTERACTION between two mirror personas — each responds to the SAME stimulus with its
    OWN invariants, so the exchange is genuinely emergent (different archetypes, different stances) yet
    fully deterministic + $0. This is the emergent edge-node conversation WITHOUT querying AI."""
    ra = respond(a, stimulus)
    rb = respond(b, stimulus)
    return {"ok": True, "schema": SCHEMA, "stimulus": stimulus[:200],
            "a": {"archetype": ra.get("archetype"), "response": ra.get("response")},
            "b": {"archetype": rb.get("archetype"), "response": rb.get("response")},
            "ai_queried": False,
            "note": "two mirrors, one stimulus, two emergent stances — deterministic, $0"}


def mine_novelty(persona: dict[str, Any], signal: str, *, surface: str = "mirror") -> dict[str, Any]:
    """The mirror as an EDGE NODE MINING NOVELTY: route the novel signal to the ocean model / swarm via
    the ONE primitive (swarm_surface.route_novel). The deterministic core handles interaction; NOVELTY
    escalates. This is the seam where the ocean model is actually queried (the stochastic side)."""
    archetype = (persona or {}).get("archetype", "mirror")
    if not (signal or "").strip():
        return {"ok": False, "schema": SCHEMA, "error": "empty signal"}
    try:
        from mag import swarm_surface
        routed = swarm_surface.route_novel(
            goal=signal, surface=surface, lens=f"{archetype}-mirror")
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "archetype": archetype,
                "error": f"route_novel unavailable: {str(e)[:120]}"}
    return {"ok": True, "schema": SCHEMA, "archetype": archetype,
            "routed": routed.get("ok"), "enqueued": routed.get("task_id") or routed.get("enqueued"),
            "note": "novelty mined at the edge and routed to the ocean/swarm via route_novel"}


# ── NUKE: death as a learning LENS (the fireball -> babelfish mechanic) ────────
# STEAL (2026-08-12): agentswarm codeledger ("persists what it learned the hard way") + resolveLedger
# (a resolved/dead forecast becomes a scored datapoint that recalibrates the engine) + snapshotFitted
# (the learned lens captured for reuse). SELF-STEAL: fish_ear (the babelfish decompile) + loss-is-
# doorway-to-shadow-work. ADAPTED: destroying a mirror is NOT waste — it maps to "huh, maybe there's
# something useful to learn here", mined as a lens (the babelfish) and routed as novelty.
def nuke_persona(persona: dict[str, Any], fireball: str, *, reason: str = "",
                 fold: bool = True, route: bool = True) -> dict[str, Any]:
    """Nuke a mirror persona with a fireball -> it becomes a BABELFISH LENS (death maps to a lesson).

    The operator's tesuji: "i fireballed a bunch of runaway windows and it lead to a babelfish."
    Destroying a node is never waste: the death is decompiled into what's useful to learn, the lesson
    is folded (a recovery/lesson RIB) and the genuinely novel part is routed to the ocean/swarm via
    route_novel. Deterministic lesson extraction (from the mirror's archetype + the fireball reason);
    only the NOVEL signal escalates. HONEST — the lesson is derived from real seeded invariants + the
    real fireball reason, never fabricated."""
    archetype = (persona or {}).get("archetype", "mirror")
    spec = ARCHETYPES.get(archetype, {})
    fireball = (fireball or "").strip()
    reason = (reason or "").strip()
    # DETERMINISTIC lesson: what the mirror WAS (essence) x why it died (fireball/reason) -> the lens
    essence = spec.get("essence", "the edge of the map")
    shadow = spec.get("shadow", "what was avoided")
    lesson = (f"fireballed a {archetype} mirror ({fireball or 'the runaway node'}): "
              f"it was '{essence}' — its shadow was '{shadow}'. "
              f"{('cause: ' + reason + '. ') if reason else ''}"
              f"lesson: {fireball if fireball else 'the runaway'} was NOT random — mine it for what it "
              f"was doing and use the finding as a lens, not just destroy it.")
    out: dict[str, Any] = {
        "ok": True, "schema": SCHEMA, "archetype": archetype, "fireball": fireball[:200],
        "reason": reason[:200], "lesson": lesson, "ai_queried": False,
        "note": "death mapped to a lesson — the fireball becomes a babelfish lens, not waste",
    }
    # FOLD the lesson as a recovery/lesson RIB (the codeledger: learn the hard way, boot next run from it)
    if fold:
        try:
            from mag import rib_bus
            r = rib_bus.publish_rib(lesson, domain="recovery", source=f"{archetype}-nuke",
                                    fold=False, publish=False)
            out["folded_rib"] = {"domain": "recovery", "n_total": r.get("n_total")}
        except Exception as e:
            out["fold_error"] = str(e)[:80]
    # ROUTE the novel signal (the babelfish: the death's meaning worth mining) to the ocean/swarm
    if route:
        try:
            from mag import swarm_surface
            routed = swarm_surface.route_novel(
                goal=f"[nuke lens] {lesson}", surface="mirror-nuke", lens=f"{archetype}-babelfish")
            out["routed"] = {"ok": routed.get("ok"),
                             "task_id": routed.get("task_id") or routed.get("enqueued")}
        except Exception as e:
            out["route_error"] = str(e)[:80]
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="mirror-persona")
    ap.add_argument("cmd", nargs="?", default="list",
                    choices=["list", "seed", "respond", "interact", "mine", "nuke"])
    ap.add_argument("args", nargs="*", default=[])
    ap.add_argument("--archetype", default="sage")
    ap.add_argument("--other", default="trickster")
    ap.add_argument("--stimulus", default="what do we build here?")
    ap.add_argument("--fireball", default="a runaway node")
    ap.add_argument("--reason", default="")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        print(json.dumps(mirror_personas(), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "seed":
        print(json.dumps(seed_persona(a.archetype), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "respond":
        p = seed_persona(a.archetype).get("persona", {})
        print(json.dumps(respond(p, a.stimulus), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "interact":
        pa = seed_persona(a.archetype).get("persona", {})
        pb = seed_persona(a.other).get("persona", {})
        print(json.dumps(interact(pa, pb, a.stimulus), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "mine":
        p = seed_persona(a.archetype).get("persona", {})
        print(json.dumps(mine_novelty(p, " ".join(a.args) or "a novel signal"),
                         ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "nuke":
        p = seed_persona(a.archetype).get("persona", {})
        print(json.dumps(nuke_persona(p, a.fireball, reason=a.reason),
                         ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
