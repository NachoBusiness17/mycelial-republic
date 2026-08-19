from pathlib import Path
p = Path("/app/mag/game_view.py")
t = p.read_text(encoding="utf-8")
old = '''    grid = _rows(g)
    title = str(sc.get("room_name") or room_id or "Room")
    world_meta: dict[str, Any] = {}
    try:
        from mag import game_world, game_world_render
        rd = game_world_render.render("guttered-lantern")
        ascii_map = str(rd.get("ascii") or "").strip()
        if ascii_map:
            field = [list(row) for row in ascii_map.splitlines() if row]
            # stamp the table @ onto the field so the castle sits on the territory
            if field and field[0]:
                fy, fx = len(field) // 2, len(field[0]) // 2
                field[min(fy, len(field)-1)][min(fx, len(field[0])-1)] = "@"
                grid = ["".join(row) for row in field]
        ws = game_world.world_status()
        world_meta = {
            "root": ws.get("root"),
            "n_changes": ws.get("n_changes"),
            "n_entities": ws.get("n_entities"),
            "buildings": rd.get("buildings_revealed"),
            "region": "guttered-lantern",
        }
    except Exception:
        pass
    out = {
        "ok": True,
        "schema": SCHEMA,
        "skin": "world_rib",
'''
new = '''    grid = _rows(g)
    title = str(sc.get("room_name") or room_id or "Room")
    # Room grid only. World-rib overlay and training emit were hanging the
    # dashboard thread (HTTP /api/v1/table/view never returned).
    world_meta: dict[str, Any] = {}
    out = {
        "ok": True,
        "schema": SCHEMA,
        "skin": "ascii",
'''
if old not in t:
    raise SystemExit("world overlay block not found")
t = t.replace(old, new, 1)
old = '''    try:
        from mag.training_events import emit

        emit(
            "table_view",
            join={"campaign_id": campaign_id or "", "room_id": room_id or ""},
            action={"skin": "ascii", "title": title[:80]},
            outcome={"has_encounter": bool(enc and int(enc.get("hp") or 0) > 0)},
            pattern_tags=["game", "table", "ascii", "rest"],
            tier_max="T1",
            exportable=False,
        )
    except Exception:
        pass
    return out
'''
new = '''    return out
'''
if old not in t:
    raise SystemExit("emit block not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("game_view.py ok")
