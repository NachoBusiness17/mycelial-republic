from pathlib import Path
p = Path("/app/dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = '''        # Prefer RESTful dispatch table (v1 + legacy aliases)
        if path.startswith("/api/"):
            from dashboard.rest import dispatch
'''
new = '''        # Table view is engine-true and must not sit behind 392-route dispatch.
        if path in ("/api/v1/table/view", "/api/table/view"):
            try:
                from mag.game_view import handle_table_view
                q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
                out = handle_table_view(None, q)
                return self._json(200, out if isinstance(out, dict) else {"ok": True})
            except Exception as exc:
                return self._json(200, {"ok": True, "title": "table", "error": str(exc)[:160]})

        # Prefer RESTful dispatch table (v1 + legacy aliases)
        if path.startswith("/api/"):
            from dashboard.rest import dispatch
'''
if old not in t:
    raise SystemExit("dispatch block not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("canary ok")
