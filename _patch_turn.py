from pathlib import Path

Path("/app/mag/table_turn_cli.py").write_text(r'''"""One table turn as JSON. Desk must not import Mag."""
from __future__ import annotations
import json, sys

def main() -> int:
    body = json.loads(sys.stdin.read() or "{}")
    from mag.table_turn import handle
    print(json.dumps(handle(body), default=str))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")
print("turn cli ok")

p = Path("/app/dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = '''        if path.startswith("/api/"):
            from dashboard.rest import dispatch

            q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
            hit = dispatch("POST", path, data or {}, q)
            if hit:
                return self._json(hit[0], hit[1])
'''
new = '''        if path in ("/api/v1/voice/turn", "/api/voice/turn") and str((data or {}).get("channel") or "") == "table":
            import subprocess
            import sys as _sys
            try:
                blob = subprocess.check_output(
                    [_sys.executable, "-m", "mag.table_turn_cli"],
                    input=json.dumps(data or {}).encode("utf-8"),
                    cwd=str(ROOT),
                    timeout=8,
                )
                out = json.loads(blob.decode("utf-8") or "{}")
                return self._json(200 if out.get("ok") is not False else 400, out)
            except Exception as exc:
                return self._json(200, {"ok": True, "answer": "The keep waits.", "error": str(exc)[:160], "route": "table_timeout"})

        if path.startswith("/api/"):
            from dashboard.rest import dispatch

            q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
            hit = dispatch("POST", path, data or {}, q)
            if hit:
                return self._json(hit[0], hit[1])
'''
if old not in t:
    raise SystemExit("POST api block not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("turn short-circuit ok")

# Calcifer is the lantern hearth only
w = Path("/app/mag/wave.py")
wt = w.read_text(encoding="utf-8")
wt2 = wt.replace(
    "        parts.append('<text x=\"180\" y=\"250\" text-anchor=\"middle\" fill=\"#f2f2f2\" font-size=\"16\" font-family=\"Helvetica, Arial, sans-serif\" data-talk=\"calcifer\" class=\"exit\" cursor=\"pointer\">calcifer</text>')\n",
    "",
    1,
)
wt2 = wt2.replace(
    "        parts.append('<text x=\"470\" y=\"200\" text-anchor=\"middle\" fill=\"#f2f2f2\" font-size=\"16\" font-family=\"Helvetica, Arial, sans-serif\" data-talk=\"calcifer\" class=\"exit\" cursor=\"pointer\">calcifer</text>')\n",
    "",
    1,
)
if wt2 == wt:
    print("calcifer svg lines not found")
else:
    w.write_text(wt2, encoding="utf-8")
    print("calcifer off keep/hall svg")
