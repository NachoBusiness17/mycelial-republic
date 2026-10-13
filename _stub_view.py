from pathlib import Path

p = Path("/app/mag/game_view.py")
t = p.read_text(encoding="utf-8")
old = '''def handle_table_view(body: dict[str, Any] | None = None, params: dict[str, str] | None = None) -> dict[str, Any]:
    body = body or {}
    params = params or {}
    sid = str(body.get("session_id") or params.get("session_id") or "")
    cid = str(body.get("campaign_id") or params.get("campaign_id") or "")
    return build_view(session_id=sid, campaign_id=cid)
'''
new = '''def handle_table_view(body: dict[str, Any] | None = None, params: dict[str, str] | None = None) -> dict[str, Any]:
    """HTTP-safe: build_view in a thread with a deadline so the desk cannot wedge."""
    import threading
    body = body or {}
    params = params or {}
    sid = str(body.get("session_id") or params.get("session_id") or "")
    cid = str(body.get("campaign_id") or params.get("campaign_id") or "")
    box: dict[str, Any] = {}

    def _run() -> None:
        try:
            box["out"] = build_view(session_id=sid, campaign_id=cid)
        except Exception as exc:
            box["err"] = str(exc)[:160]

    th = threading.Thread(target=_run, daemon=True)
    th.start()
    th.join(2.5)
    if th.is_alive():
        return {
            "ok": True,
            "title": "Keep",
            "grid_text": "##########\\n# late    #\\n#    @    #\\n##########",
            "legal": [],
            "scene": {},
            "status": "timeout",
        }
    if box.get("out"):
        return box["out"]
    return {
        "ok": True,
        "title": "table",
        "grid_text": "#####\\n# @ #\\n#####",
        "legal": [],
        "scene": {},
        "error": box.get("err") or "empty",
    }
'''
if old not in t:
    raise SystemExit("handle_table_view not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("game_view deadline ok")
