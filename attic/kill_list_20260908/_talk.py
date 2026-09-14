from pathlib import Path
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
i = t.find("def _talk_events")
print(t[i:i+1400])
