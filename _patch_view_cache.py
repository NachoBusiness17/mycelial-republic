from pathlib import Path

# --- cheap cache writer on the live mag mount ---
p = Path("/app/mag/table_view_cache.py")
p.write_text(r'''"""Write / read the table view as a JSON file. Desk HTTP must not import Mag."""
from __future__ import annotations

import json
import sys
from pathlib import Path

CACHE = Path("/app/memory/working/table_view.json")


def refresh(campaign_id: str = "") -> dict:
    from mag.game_view import handle_table_view
    out = handle_table_view({}, {"campaign_id": campaign_id} if campaign_id else {})
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out, default=str), encoding="utf-8")
    return out


def read() -> dict | None:
    if not CACHE.is_file():
        return None
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    out = refresh(cid)
    print(json.dumps(out, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")
print("cache module ok")

# --- container server.py: file cache + subprocess, never import mag ---
p = Path("/app/dashboard/server.py")
t = p.read_text(encoding="utf-8")
old = '''        # Table view is engine-true and must not sit behind 392-route dispatch.
        if path in ("/api/v1/table/view", "/api/table/view"):
            try:
                from mag.game_view import handle_table_view
                q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
                out = handle_table_view(None, q)
                return self._json(200, out if isinstance(out, dict) else {"ok": True})
            except Exception as exc:
                return self._json(200, {"ok": True, "title": "table", "error": str(exc)[:160]})
'''
new = '''        # Table view: file cache only. Importing Mag here wedges the desk (4GB / 39 threads).
        if path in ("/api/v1/table/view", "/api/table/view"):
            import subprocess
            import sys as _sys
            q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
            cache = ROOT / "memory" / "working" / "table_view.json"
            out = None
            try:
                if cache.is_file() and (time.time() - cache.stat().st_mtime) < 8:
                    out = json.loads(cache.read_text(encoding="utf-8"))
            except Exception:
                out = None
            if out is None:
                try:
                    blob = subprocess.check_output(
                        [_sys.executable, "-m", "mag.table_view_cache", str(q.get("campaign_id") or "")],
                        cwd=str(ROOT),
                        timeout=4,
                    )
                    out = json.loads(blob.decode("utf-8") or "{}")
                except Exception as exc:
                    try:
                        out = json.loads(cache.read_text(encoding="utf-8")) if cache.is_file() else None
                    except Exception:
                        out = None
                    if out is None:
                        out = {"ok": True, "title": "table", "grid_text": "#\\n@\\n#", "error": str(exc)[:160]}
            return self._json(200, out if isinstance(out, dict) else {"ok": True})
'''
if old not in t:
    raise SystemExit("short-circuit block not found")
if "import time" not in t.split("class Handler")[0]:
    t = t.replace("import json\n", "import json\nimport time\n", 1)
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("server cache ok")
