from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
idx = 0
print("==== BARROW ====")
while True:
    j = h.find("barrow", idx)
    if j < 0: break
    print(h[max(0,j-80):j+700])
    print("---")
    idx = j+1
print("==== PTT FULL ====")
p = h.find("const ptt = document.getElementById")
print(h[p:p+3200])
