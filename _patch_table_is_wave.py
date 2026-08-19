from pathlib import Path
p = Path("/app/dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = '''        # Mag Table — system-test dogfood (chat + canvas + voice); Battle Room
        if path in ("/table", "/table.html", "/play", "/play.html", "/game", "/game.html"):
            tf = STATIC / "table.html"
            if not tf.is_file():
                return self._json(404, {"error": "table.html missing"})
            return self._bytes(200, tf.read_bytes(), "text/html; charset=utf-8")
'''
new = '''        # Text adventure. /table is /wave — not the ASCII board.
        if path in ("/table", "/table.html", "/play", "/play.html", "/game", "/game.html"):
            wf = STATIC / "wave.html"
            if not wf.is_file():
                return self._json(404, {"error": "wave.html missing"})
            return self._bytes(200, wf.read_bytes(), "text/html; charset=utf-8")
'''
if old not in t:
    raise SystemExit("table route not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("table is wave")
