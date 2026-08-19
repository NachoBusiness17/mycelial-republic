from pathlib import Path
p = Path("/app/mag/game_view.py")
t = p.read_text(encoding="utf-8")
start = t.find("def handle_table_view")
if start < 0:
    raise SystemExit("handle_table_view missing")
new = r'''def handle_table_view(body: dict[str, Any] | None = None, params: dict[str, str] | None = None) -> dict[str, Any]:
    """File-first view. Do not import game_campaign on the desk HTTP thread."""
    import json
    from pathlib import Path as _P

    body = body or {}
    params = params or {}
    sid = str(body.get("session_id") or params.get("session_id") or "")
    cid = str(body.get("campaign_id") or params.get("campaign_id") or "")

    camp_dir = _P("/app/memory/working/game_campaigns")
    camp: dict[str, Any] | None = None
    try:
        files = [f for f in camp_dir.glob("gc-*.json") if f.is_file()]
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        picked = None
        if cid:
            for f in files:
                if f.stem == cid or cid in f.name:
                    picked = f
                    break
        if picked is None and sid:
            for f in files[:40]:
                try:
                    raw = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                if str(raw.get("voice_session_id") or "") == sid:
                    camp = raw
                    picked = f
                    break
        if camp is None:
            if picked is None and files:
                picked = files[0]
            if picked is not None:
                camp = json.loads(picked.read_text(encoding="utf-8"))
    except Exception:
        camp = None

    if not camp:
        return build_view_from_scene(None, status="void")

    rooms = ((camp.get("module_snapshot") or {}).get("rooms") or {})
    rid = str(camp.get("room_id") or "")
    room = rooms.get(rid) or {}
    sc = {
        "room_name": room.get("name") or rid or "Room",
        "room_desc": room.get("desc") or "",
        "hook": (room.get("hooks") or [None])[0] if isinstance(room.get("hooks"), list) else room.get("hook"),
        "exits": list((room.get("exits") or {}).keys()) if isinstance(room.get("exits"), dict) else list(room.get("exits") or []),
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
    if enc and int(enc.get("hp") or 0) > 0:
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
t = t[:start] + new
if not t.endswith("\n"):
    t += "\n"
p.write_text(t, encoding="utf-8")
print("cheap view ok", p.stat().st_size)
