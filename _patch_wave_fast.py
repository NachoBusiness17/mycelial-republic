from pathlib import Path

# --- fast snapshot on live mag mount ---
p = Path("/app/mag/wave.py")
t = p.read_text(encoding="utf-8")
if "def snapshot_fast" not in t:
    t = t.rstrip() + r'''


def snapshot_fast(*, session_id: str = "") -> dict[str, Any]:
    """Text-adventure pane. File-first. No idle tick, no game_campaign import."""
    from mag.game_view import handle_table_view

    table = handle_table_view({}, {"session_id": session_id} if session_id else {})
    sc = (table.get("scene") or {}) if isinstance(table, dict) else {}
    pl = sc.get("player") or {}
    rid = str(table.get("room_id") or "")
    interior = str(sc.get("room_desc") or "").strip()
    hook = str(sc.get("hook") or "").strip()
    if hook and hook.lower() not in interior.lower():
        interior = (interior + " " + hook).strip()
    who: list[dict[str, Any]] = []
    if pl.get("name"):
        who.append({"name": str(pl.get("name")), "role": "you", "kind": "player"})
    enc = sc.get("encounter") or {}
    try:
        if enc.get("name") and int(enc.get("hp") or 0) > 0:
            who.append({"name": str(enc.get("name")), "role": "foe", "kind": "encounter", "talkable": True})
    except (TypeError, ValueError):
        pass
    blob = " ".join([str(sc.get("room_name") or ""), interior, hook]).lower()
    for name, keys in (
        ("mira", ("mira", "barkeep")),
        ("stranger", ("stranger",)),
        ("merchant", ("merchant", "captive")),
    ):
        if any(k in blob for k in keys):
            who.append({"name": name if name != "mira" else "Mira", "role": "here", "kind": "room", "talkable": True})
    if rid in ("tavern_lantern", "lantern") and any(w in blob for w in ("fire", "hearth")):
        who.append({"name": "Calcifer", "role": "hearth", "kind": "room", "talkable": True})
    hp = int(pl.get("hp") if pl.get("hp") is not None else 0)
    hp_max = int(pl.get("hp_max") or 1) or 1
    seated = bool(pl.get("name") or table.get("campaign_id"))
    fr = {
        "unit": {
            "name": (pl.get("name") or "Adventurer") if seated else "unseated",
            "archetype": pl.get("archetype") or "",
            "hp": hp if seated else None,
            "hp_max": hp_max if seated else None,
            "hp_pct": round(100.0 * hp / hp_max) if seated else None,
        },
        "bags": list(pl.get("inventory") or []),
        "quest": hook if hook.lower().startswith("rumor") or "crate" in hook.lower() else hook,
        "who": who,
        "bar": _bar(table.get("legal") or []),
        "hotspots": _hotspots(sc, who),
    }
    return {
        "ok": True,
        "schema": SCHEMA,
        "speak_text": interior[:480],
        "doctrine": DOCTRINE,
        "table": {
            "ok": table.get("ok"),
            "title": table.get("title"),
            "room_id": table.get("room_id"),
            "campaign_id": table.get("campaign_id"),
            "legal": table.get("legal") or [],
            "scene": sc,
        },
        "frames": fr,
        "narrative": {
            "interior": interior,
            "story_so_far": "",
            "hook": hook,
            "exits": _exits(sc),
            "player": pl,
        },
        "render": {
            "room_mermaid": room_mermaid(sc),
            "room_svg": room_svg({**sc, "room_id": rid}, people=who),
        },
        "faces": {"wave": "/wave", "table": "/table"},
        "note": "fast pane — room bytes, one beat",
    }
'''
    p.write_text(t + "\n", encoding="utf-8")
    print("snapshot_fast added")
else:
    print("snapshot_fast already there")

# cache writer
Path("/app/mag/wave_cache.py").write_text(r'''"""Write the wave pane as JSON. Desk HTTP must not import Mag."""
from __future__ import annotations
import json, sys
from pathlib import Path
CACHE = Path("/app/memory/working/wave_view.json")

def refresh(session_id: str = "") -> dict:
    from mag.wave import snapshot_fast
    out = snapshot_fast(session_id=session_id)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out, default=str), encoding="utf-8")
    return out

def main() -> int:
    sid = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(refresh(sid), default=str))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")
print("wave_cache ok")

# server.py short-circuit
p = Path("/app/dashboard/server.py")
t = p.read_text(encoding="utf-8")
needle = '''        # Prefer RESTful dispatch table (v1 + legacy aliases)
        if path.startswith("/api/"):
'''
insert = '''        if path in ("/api/v1/wave", "/api/wave"):
            import subprocess
            import sys as _sys
            q = {k: (v[0] if v else "") for k, v in parse_qs(parsed.query).items()}
            cache = ROOT / "memory" / "working" / "wave_view.json"
            out = None
            try:
                if cache.is_file() and (time.time() - cache.stat().st_mtime) < 6:
                    out = json.loads(cache.read_text(encoding="utf-8"))
            except Exception:
                out = None
            if out is None:
                try:
                    blob = subprocess.check_output(
                        [_sys.executable, "-m", "mag.wave_cache", str(q.get("session_id") or "")],
                        cwd=str(ROOT),
                        timeout=5,
                    )
                    out = json.loads(blob.decode("utf-8") or "{}")
                except Exception as exc:
                    try:
                        out = json.loads(cache.read_text(encoding="utf-8")) if cache.is_file() else None
                    except Exception:
                        out = None
                    if out is None:
                        out = {"ok": True, "narrative": {"interior": "The lantern is dark.", "exits": []}, "table": {"title": "void"}, "error": str(exc)[:160]}
            return self._json(200, out if isinstance(out, dict) else {"ok": True})

        # Prefer RESTful dispatch table (v1 + legacy aliases)
        if path.startswith("/api/"):
'''
if "if path in (\"/api/v1/wave\"" in t:
    print("wave short-circuit already present")
elif needle not in t:
    raise SystemExit("dispatch needle missing")
else:
    if "import time" not in t.split("class Handler")[0]:
        t = t.replace("import json\n", "import json\nimport time\n", 1)
    t = t.replace(needle, insert, 1)
    p.write_text(t, encoding="utf-8")
    print("wave short-circuit ok")
