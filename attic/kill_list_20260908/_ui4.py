from pathlib import Path
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
j = t.find("def _narrate_room")
print("NARRATE LEN", len(t[j:]))
print(t[j:j+3200])
print("==== LEGAL ====")
k = t.find("def list_legal_actions")
print(t[k:k+2500])
