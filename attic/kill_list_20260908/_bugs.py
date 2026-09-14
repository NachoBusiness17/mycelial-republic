from mag.game_campaign import latest_any, parse_player_speech, apply_action, people_in_room
c = latest_any()
cid = c.get("campaign_id")
print("who", people_in_room(c))
for s in ["talk to merchant", "talk to captive", "look crate", "look merchant", "look captive", "talk to calcifer"]:
    a = parse_player_speech(s)
    r = apply_action(cid, a) if a else {"narrate": "PARSE NONE"}
    print("==", s, a.get("type") if a else None)
    print((r.get("narrate") or r.get("error") or "")[:220])
