from pathlib import Path
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
i = t.find("def people_in_room")
print(t[i:i+900])
print("--- talk empty ---")
j = t.find("No one here to talk to")
print(t[j-200:j+250])
