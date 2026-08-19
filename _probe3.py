from pathlib import Path
t = Path("mag/game_campaign.py").read_text(encoding="utf-8")
j = t.find("def _look_at")
print(t[j:t.find("def _narrate_room")])
print("==== SET_STATE ====")
idx = 0
n = 0
while n < 5:
    i = t.find("set_state", idx)
    if i < 0:
        break
    print(t[i-80:i+280])
    print("---")
    idx = i+8
    n += 1
