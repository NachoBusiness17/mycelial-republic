# The Mountain — Sovereign Slice

The estate's first playable Godot build. Two ported estate systems, one game loop.

## Run it

Open this folder (`roblox_to_godot/`) in **Godot 4.3+** and press F5. From a terminal:

```
godot --path . --quit-after 60   # smoke check: 60 frames headless-ish, watch for script errors
godot --path .                    # play
```

No Godot on your box? Download from godotengine.org (standard build, ~50MB, no account, no license server).

## The game

You are the shepherd on the mountain. The world holds **8 units of water**; the **Crown** at the summit needs **4**, and gravity only flows downhill. The only way to lift water is the estate's steam law: **boil a unit anywhere, and it condenses at the highest cold node — the Crown.**

- **Mouse** — move the shepherd. Chase a fish until it tires (it turns gold), close in to tag it. Tagged fish are score.
- **SPACE** — boil 1 unit at the nearest pool. It rises as steam and lands in the Crown. Boiling dries your pools, and the school gathers at the *wettest* pool — dry your fishing holes at a price.
- **E** — open/shut the nearest valve. Pipes: `p_spring` and `p_terrace` feed the XOR gate (it passes only one inlet at a time — feed it from both and it pools), `p_out` and `p_drain` are the downhill drains (shut them or the mountain leaks), `p_bypass` is a siphon that must prime (2 units pooled at the spring) before it will carry water up-and-over to the terrace.
- **R** — restart after the win.

Water physics are the estate's deterministic integer graph: no floats, no RNG (the school's spawn is seeded too). Same inputs, same mountain, every run.

## Where the organs live

| File | Estate origin |
|---|---|
| `systems/water_graph.gd` | ported from `mag/water_graph.py` (verdict physics: check valves, siphons, XOR/SILL junctions, steam-to-highest-cold) |
| `systems/flock.gd` | ported from `dashboard/static/games/swarm.html` + `roblox/src/shared/Flock.luau` (flee/tire/rest boids, catch mechanic, pheromone trail) |
| `scripts/game.gd` | new orchestrator: the loop that makes the two systems feed each other |

`core/` carries the boot integrity autoload (R6, below); `network/`, `water/` are empty placeholders from the original port scaffold — content migration (The Mountain's world data) is still the next wave after this slice.

## Verify the build artifact (R6 2026-09-30)

Every pipeline export (`scripts/build_game.ps1`) is stamped: the exe carries an appended trailer pinning the **source git sha** and the **pck sha256**; at boot the `core/boot_integrity.gd` autoload hashes the pck beside the exe and prints its identity to stderr.

The stranger's check, from the unzipped `mountain-<sha>.zip` folder (no Godot needed):

```
# run it: identity line + exit 0 when intact, "pck=FAIL ... SWAPPED PCK" + exit 1 when the pck was swapped
TheMountain.exe --headless --quit-after 2

# or offline, pure stdlib: reads the stamp out of the exe, hashes the pck, compares
python -c "import json,hashlib;f=open('TheMountain.exe','rb');f.seek(-4,2);L=int.from_bytes(f.read(4),'little');f.seek(-12,2);m=f.read(8);f.seek(-12-L,2);s=json.loads(f.read(L));p=hashlib.sha256(open('TheMountain.pck','rb').read()).hexdigest();print('MOUNTAIN',('OK' if m==b'MAGSTMP1' and p==s['pck_sha256'] else 'FAIL'),s['source'],s['git'])"
```

`mountain-manifest.json` (in the zip) cross-checks the same shas without running anything. The printed `git` sha is the source tree the exe was built from — `estate-twin` (this repo) or `the-mountain` (public tree, `-FromTheMountain`). A pck missing entirely is caught one step earlier by Godot's own loader ("Is the .pck file missing?").

## Fix receipt (2026-09-29, zcode-seat)

The committed `water_graph.gd` had never been executed: its inner data classes were named `Node2D` and `Pipe`, shadowing Godot's built-ins, with `: Node` annotations applied to inner-class instances — the first `tick()` would have crashed on a runtime type-assignment error. Renamed to `WNode` / `WPipe` and corrected the annotations. Trust bytes, run the thing.

## Verification status

Written against Godot 4.3 stable APIs and hand-checked; **no Godot binary exists on the estate box**, so the slice has not been executed by the seat. First human to open it in the editor owns the first real error. The estate's law stands: this is LANDED-as-code, PLAYED-by-no-one-yet.
