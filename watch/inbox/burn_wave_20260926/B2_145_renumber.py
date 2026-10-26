"""B2-145 fix: renumber my two self-fed briefs from colliding B2-150/151 to
free B2-156/157 (concurrent lanes claimed 150-155 while this lane worked)."""
ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
QPATH = ROOT + r"\watch\inbox\burn_wave_20260926\QUEUE.md"

PAIRS = [
    ("- [ ] B2-150 Living-file hash law:", "- [ ] B2-156 Living-file hash law:"),
    ("- [ ] B2-151 Sharpen B2-149 with the composed-prefix case:",
     "- [ ] B2-157 Sharpen B2-149 with the composed-prefix case:"),
]

with open(QPATH, encoding="utf-8") as f:
    q = f.read()
for old, new in PAIRS:
    assert q.count(old) == 1, f"target not unique: {old!r} x{q.count(old)}"
    q = q.replace(old, new)
with open(QPATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(q)

with open(QPATH, encoding="utf-8") as f:
    check = f.read()
for old, new in PAIRS:
    assert new in check and old not in check
print("renumbered to B2-156 / B2-157; no B2-150/151 claims remain from this lane")
