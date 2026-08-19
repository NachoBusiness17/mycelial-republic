from mag.game_campaign import latest_any, parse_player_speech, apply_action, people_in_room
from mag.wave import snapshot
c = latest_any()
print("room", c.get("room_id"), "who", people_in_room(c))
print("parse", parse_player_speech("wink at calcifer"))
r = apply_action(c.get("campaign_id"), parse_player_speech("wink at calcifer"))
print((r.get("narrate") or "")[:400])
s = snapshot()
who = (s.get("frames") or {}).get("who") or []
print("wave who", [w.get("name") for w in who])
svg = (s.get("render") or {}).get("room_svg") or ""
print("svg calcifer", "calcifer" in svg.lower())
from pathlib import Path
p = Path("memory/working/game_characters/calcifer.json")
p.parent.mkdir(parents=True, exist_ok=True)
if not p.exists():
    p.write_text('''{
  "schema": "mag_fingerprint.v1",
  "name": "Calcifer",
  "kind": "hearth",
  "note": "Player-named Mag fire. Not Howl plot. Same flame as lantern hearth and keep torch. Rashomon: each seat sees a different fire; engine_truth is the torch/hearth bytes. Competition that lifts: any seat can talk to it.",
  "honored": "2026-08-14 wink at keep_gate"
}
''', encoding="utf-8")
print("fingerprint", p)
