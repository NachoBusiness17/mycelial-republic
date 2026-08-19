from pathlib import Path
p = Path("/app/mag/game_view.py")
t = p.read_text(encoding="utf-8")
start = t.find("def handle_table_view")
if start < 0:
    raise SystemExit("missing")
new = r'''def handle_table_view(body: dict[str, Any] | None = None, params: dict[str, str] | None = None) -> dict[str, Any]:
    """Newest campaign file only. Never scan the pile on the desk thread."""
    import json
    from pathlib import Path as _P

    body = body or {}
    params = params or {}
    cid = str(body.get("campaign_id") or params.get("campaign_id") or "").strip()
    camp_dir = _P("/app/memory/working/game_campaigns")
    camp: dict[str, Any] | None = None
    try:
        picked = camp_dir / f"{cid}.json" if cid else None
        if picked is None or not picked.is_file():
            newest = None
            newest_m = -1.0
            with os.scandir(camp_dir) as it:
                for ent in it:
                    if not ent.name.startswith("gc-") or not ent.name.endswith(".json"):
                        continue
                    try:
                        m = ent.stat().st_mtime
                    except OSError:
                        continue
                    if m > newest_m:
                        newest_m = m
                        newest = _P(ent.path)
            picked = newest
        if picked is not None:
            camp = json.loads(picked.read_text(encoding="utf-8"))
    except Exception:
        camp = None

    if not camp:
        return build_view_from_scene(None, status="void")

    rooms = ((camp.get("module_snapshot") or {}).get("rooms") or {})
    rid = str(camp.get("room_id") or "")
    room = rooms.get(rid) or {}
    hooks = room.get("hooks") or []
    hook = hooks[0] if isinstance(hooks, list) and hooks else room.get("hook")
    exits = room.get("exits") or {}
    sc = {
        "room_name": room.get("name") or rid or "Room",
        "room_desc": room.get("desc") or "",
        "hook": hook,
        "exits": list(exits.keys()) if isinstance(exits, dict) else list(exits or []),
        "player": camp.get("player") or {},
        "encounter": camp.get("encounter") or {},
        "flags": camp.get("flags") or {},
    }
    legal: list[dict[str, Any]] = [{"type": "look"}, {"type": "help"}]
    for ex in sc["exits"]:
        legal.append({"type": "move", "direction": str(ex)})
    if sc["player"]:
        legal.append({"type": "inventory"})
    enc = sc.get("encounter") or {}
    try:
        fighting = bool(enc and int(enc.get("hp") or 0) > 0)
    except (TypeError, ValueError):
        fighting = False
    if fighting:
        legal.extend([{"type": "attack"}, {"type": "flee"}])
    else:
        legal.append({"type": "rest"})
    return build_view_from_scene(
        sc,
        legal=legal,
        campaign_id=str(camp.get("campaign_id") or ""),
        room_id=rid,
        status=str(camp.get("status") or ""),
    )
'''
# handle_table_view uses os.scandir — ensure os is imported at module top
if "import os" not in t.split("def ")[0]:
    t = t.replace("from __future__ import annotations\n", "from __future__ import annotations\n\nimport os\n", 1)
t = t[:start] + new
if not t.endswith("\n"):
    t += "\n"
p.write_text(t, encoding="utf-8")
print("slim view ok")
