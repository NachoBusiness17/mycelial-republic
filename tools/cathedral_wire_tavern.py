"""Wire the tavern (dnd_classic_stub) into the live cathedral game.

Self-steal: we built a 14-room classic D&D module with tavern/rumors/encounter/loot
(dnd_classic_stub.v1.json) but the cathedral never carried it. This injects the
module into games-site/cathedral_v1.html, crosslinks crossroads <-> tavern, and
returns 0 on success. Idempotent: skips if already wired.
"""
import io, json, re, sys

GAME = "../games-site/cathedral_v1.html"
MODULE = "memory/game_modules/dnd_classic_stub.v1.json"

html = io.open(GAME, encoding="utf-8").read()
if '"dnd_classic"' in html:
    print("already wired"); sys.exit(0)

mod = json.load(io.open(MODULE, encoding="utf-8"))
# reciprocal exit: tavern back to the crossroads
mod["rooms"]["tavern_lantern"].setdefault("exits", {})["crossroads"] = "crossroads"

inject = ('"dnd_classic": ' +
          json.dumps(mod, ensure_ascii=False, indent=1).replace("\n", "\n ") + ",\n")
marker = "const MODULES = {\n"
if marker not in html:
    print("MODULES marker not found"); sys.exit(1)
html = html.replace(marker, marker + inject, 1)

# crosslink: crossroads gains a "lantern" exit (fires once — guarded above)
html, n = re.subn(r'("crossroads": \{[^{}]*?"exits": \{)',
                  r'\1"lantern": "tavern_lantern", ', html, count=1, flags=re.S)
if n != 1:
    print("crossroads exits not found"); sys.exit(1)

io.open(GAME, "w", encoding="utf-8", newline="\n").write(html)
print("wired: dnd_classic in, crossroads<->lantern linked")
