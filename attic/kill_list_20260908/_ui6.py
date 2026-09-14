from pathlib import Path
w = Path("mag/wave.py").read_text(encoding="utf-8")
for key in ['"bar"', "legal", "label", "speak_text", "passage"]:
    i = 0
    n = 0
    while n < 6:
        j = w.find(key, i)
        if j < 0: break
        print(f"--- wave {key} @{j} ---")
        print(w[max(0,j-120):j+280])
        print()
        i = j+len(key)
        n += 1
print("==== CAMPAIGN TALK/LOOK ====")
g = Path("mag/game_campaign.py").read_text(encoding="utf-8")
for key in ["def apply_action", "elif kind == \"talk\"", "elif kind == \"look\"", "def _talk", "merchant", "crate"]:
    j = g.find(key)
    print(f"--- {key} @{j} ---")
    if j>=0:
        print(g[j:j+700])
        print()
