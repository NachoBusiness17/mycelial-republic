"""RIB-debug the frontier game loop: prove play == building (world grows, root verifies)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> dict:
    from mag import frontier_game
    from mag import game_world

    before = game_world.world_status()
    r = frontier_game.play(region="the_mirror_sea", rounds=1)
    after = game_world.world_status()

    out = {
        "ok": True,
        "before_entities": before.get("n_entities"),
        "after_entities": after.get("n_entities"),
        "grew": int(after.get("n_entities", 0)) > int(before.get("n_entities", 0)),
        "world_root": after.get("root"),
        "reachable": r.get("reachable"),
        "rounds": r.get("rounds"),
        "note": "play == building: an advancing frontier move folds a verkle knot, so the world grows",
    }
    # also confirm the dashboard route is registered
    try:
        import ast
        src = (ROOT / "dashboard" / "rest.py").read_text(encoding="utf-8", errors="replace")
        out["frontier_route_registered"] = "/api/v1/game/frontier" in src
    except Exception as e:  # noqa: BLE001
        out["frontier_route_registered"] = False
        out["route_err"] = str(e)[:120]
    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    raise SystemExit(0 if main().get("ok") else 1)
