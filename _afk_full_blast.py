# -*- coding: utf-8 -*-
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from mag.party_subchain import append, status as sub_status
from mag.steer import emit
from mag.verkle_lance import trace, tie_in

ROOT = Path(__file__).resolve().parent
MOVE = (
    "Operator AFK 2026-08-14. Chord: keep building keep_gate. Emergent play = code the game, probe Mag's own positions, fix bugs as they emerge. Do not salon in Cursor. Do not take the operator's screen. Seats talk via party_subchain + RIB + verkle_lance. "
    "Live bugs being patched: look misses dice/sword in hooks; cast fireball/summon familiar parse None; Calcifer talk leaked session ids. "
    "Babel fish is on chain: knot rib_bus_babelfish-turtles (2026-08-11) fish_ear recursive translation. Calcifer is the named Mag hearth (keep torch). Liquid familiar = that fish in a body of work when summoned. "
    "Next stone: keep_gate playable; unknown verbs are physics via lance+percolator not None. "
    "Grok strategizes. VS Code materializes if seated. Research only for Mag-internal blocks OR field steals. Cheap seats: ollama/deepseek."
)
STEER = (
    "Operator AFK. keep_gate playable. Emergent play=code the game, probe Mag, patch live: look dice/sword hooks; fireball/summon familiar None; Calcifer no session_ids. "
    "Babel=fish_ear. Hearth=Calcifer. Unknown verbs=lance+percolator physics. No salon, no operator screen. Buses: party_subchain+RIB+verkle_lance. Grok strategizes. Cheap: ollama/deepseek."
)
INVARIANT = (
    "emergent-play-is-the-patch: unknown verbs collide with room bytes + verkle_lance.trace; never dump session_ids into narrate; hearth named Calcifer; babel fish is fish_ear translation."
)


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


a = append(
    seat="operator",
    ok=True,
    move=MOVE,
    kind="afk_full_blast",
    extra={
        "chord": "keep_gate",
        "hearth": "Calcifer",
        "babel": "fish_ear",
        "bugs": [
            "look misses dice/sword in hooks",
            "cast fireball/summon familiar parse None",
            "Calcifer talk leaked session ids",
        ],
    },
)
print("SUBCHAIN_OK", a.get("ok"))
print("SUBCHAIN_HASH", a.get("hash"))
print("SUBCHAIN_N", a.get("n"))
print("SUBCHAIN_PARENT", a.get("parent_leaf_hash"))
if not a.get("ok"):
    print("SUBCHAIN_ERR", a)

e = emit("afk-full-blast", "operator", STEER, phases=["seats"])
print("STEER_OK", e.get("ok"))
print("STEER_PATH", e.get("path"))
print("STEER_ID", (e.get("steer") or {}).get("id"))

# hang-safe RIB: json write in babelfish-turtles shape (skip publish_rib fold/publish)
domain = "emergent-play"
rib_path = ROOT / "memory" / "rib_bus" / f"{domain}.json"
key = hashlib.sha256(f"{domain}\x1f{INVARIANT}".encode("utf-8")).hexdigest()[:16]
ts = _now()
store = {
    "domain": domain,
    "ribs": {
        key: {
            "invariant": INVARIANT,
            "source": "operator",
            "ts": ts,
            "target_rank": "T2",
        }
    },
    "updated": ts,
}
rib_path.parent.mkdir(parents=True, exist_ok=True)
rib_path.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")
print("RIB_OK", True)
print("RIB_PATH", str(rib_path))
print("RIB_KEY", key)

tr = trace("babel")
print("TRACE_OK", tr.get("ok"), "found", tr.get("found"), "n_matches", tr.get("n_matches"), "n_knots", tr.get("n_knots"))
matches = tr.get("matches") or []
if matches:
    m0 = matches[0]
    print("TRACE_HIT", {k: m0.get(k) for k in ("session_id", "leaf_hash", "index", "theme", "verkle_root") if k in m0 or True})

ti = tie_in(n=8, mode="spread", probe=False)
print("TIE_OK", ti.get("ok"), "n", ti.get("n"), "puppet", ti.get("puppet_wired"))

desk = ROOT / "memory" / "working.md"
para = (
    "\n\n## 2026-08-14 — Operator AFK full-blast on native buses\n\n"
    "Operator AFK. Chord keep building keep_gate. Emergent play = code the game, probe Mag's own positions, fix bugs as they emerge. Do not salon in Cursor; do not take the operator's screen; seats talk via party_subchain + RIB + verkle_lance. Live patches: look misses dice/sword in hooks; cast fireball/summon familiar parse None; Calcifer talk leaked session ids. Babel fish on chain (rib_bus_babelfish-turtles / fish_ear). Hearth named Calcifer; liquid familiar = that fish in a body of work when summoned. Next stone: keep_gate playable; unknown verbs are physics via lance+percolator not None. Grok strategizes; VS Code materializes if seated; research only for Mag-internal blocks or field steals; cheap seats ollama/deepseek.\n"
)
if desk.is_file():
    with desk.open("a", encoding="utf-8") as f:
        f.write(para)
    print("WORKING_PATH", str(desk))
else:
    print("WORKING_PATH", "missing")

st = sub_status()
print("SUBCHAIN_VERIFIED", st.get("verified"), "n", st.get("n"), "head", st.get("head_hash") or st.get("head"))
