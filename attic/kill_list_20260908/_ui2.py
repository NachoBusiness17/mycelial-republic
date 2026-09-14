from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
# remaining css
i = h.find("#bags")
print(h[i:h.find("</style>")])
print("==== NARR ====")
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
j = t.find("def _narrate_room")
print(t[j:j+1200])
print("==== LEGAL ====")
k = t.find("def list_legal_actions")
print(t[k:k+700])
