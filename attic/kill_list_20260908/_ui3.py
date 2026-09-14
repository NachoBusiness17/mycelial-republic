from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
print("==== CSS TAIL ====")
print(h[h.find(".compass { display:flex"):h.find("</style>")])
print("==== PTT JS ====")
for key in ["ptt", "getUserMedia", "pointerdown", "mediaDevices", "hold", "scroll"]:
    i = 0
    while True:
        j = h.lower().find(key.lower(), i)
        if j < 0: break
        print(f"--- {key} @{j} ---")
        print(h[max(0,j-80):j+220])
        print()
        i = j+1
        if i > 200000: break
