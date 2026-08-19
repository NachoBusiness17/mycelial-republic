from pathlib import Path
h = Path("dashboard/static/wave.html").read_text(encoding="utf-8")
# find refresh function start and following function
i = h.find("async function refresh()")
j = h.find("async function sendLine")
print("refresh", i, "sendLine", j)
print("==== between refresh and sendLine last 800 ====")
chunk = h[i:j]
print(chunk[-800:] if j>i else chunk[:2000])
print("==== boot/finally ====")
k = h.find("boot();")
print(h[k-200:k+250])
