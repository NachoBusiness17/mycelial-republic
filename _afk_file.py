from mag.party_subchain import append, status
from mag.steer import emit
from mag.bus_cadence import cadence

MOVE = (
    "AFK CHORD. Operator left. Job is the GAME, not another dossier. "
    "Live campaign is on road_to_keep. Next stone: keep_gate playable on /wave "
    "(SVG follows the room, clicks from module bytes, no invented Spire). "
    "Laws: chain=truth, steal Mag organs first, RIB-debug bytes, built != verified-working. "
    "Cadence: Mag game_ramp.work every 900s already exists. Seats talk on this subchain. "
    "Socratic: grok strategizes, vscode materializes, cheap seats janitor, Research only when Mag internals block. "
    "Do not wait for the operator. Strike."
)

a = append(seat="grok", ok=True, move=MOVE, kind="afk_chord")
print("append", a)
e = emit("grok", "operator", MOVE)
print("emit", {k: e.get(k) for k in ("ok", "path", "id")})
c = cadence()
print("folded", c.get("n_folded"), "unconsumed later", end=" ")
from mag.steer import status as ss
print(ss())
print("sub n", status().get("n"), "verified", status().get("verified"))
