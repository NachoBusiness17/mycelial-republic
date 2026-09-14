from pathlib import Path
import re
p = Path("dashboard/static/wave.html")
t = p.read_text(encoding="utf-8")
t2, n = re.subn(
    r"if \(!window\.isSecureContext[\s\S]{0,400}?location\.replace\(\"https://\"[\s\S]{0,200}?\n    \}\n",
    "",
    t,
    count=1,
)
print("n", n)
p.write_text(t2, encoding="utf-8")
t = p.read_text(encoding="utf-8")
print("replace https", "location.replace" in t)
print("isSecure bounce", "location.replace(\"https://" in t)
