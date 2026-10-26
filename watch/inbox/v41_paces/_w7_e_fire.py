# -*- coding: utf-8 -*-
"""WAVE 7 LANE E — flagship free-lane game build.

One deepseek-flash call: fish prototype -> horse running, same parametric spirit.
Output overwrites dashboard/static/viz_horse_run.html.
"""
import json
import pathlib
import sys
import time

REPO = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(REPO))

FISH = REPO / "dashboard" / "static" / "viz_spore_fish.html"
OUT = REPO / "dashboard" / "static" / "viz_horse_run.html"
RECEIPT = REPO / "watch" / "inbox" / "v41_paces" / "W7_E_deepseek_receipt.json"

fish_src = FISH.read_text(encoding="utf-8")

SYSTEM = (
    "You are a generative artist-engineer who builds luminous point-cloud "
    "canvas animations in a dark laboratory aesthetic. You output ONE complete, "
    "self-contained HTML file and nothing else: start at <!DOCTYPE html>, end at "
    "</html>. No markdown fences, no commentary, no explanation before or after."
)

USER = f"""Below is a working canvas prototype: a parametric 10,000-particle point cloud
that reads as a swimming FISH. Its spirit: closed-form math only (no assets, no libs),
one time variable t advanced per requestAnimationFrame tick, every pixel placed by
trigonometric expressions of index and t, dark background, luminous blue points.

YOUR TASK: REINTERPRET this as a HORSE RUNNING.

Requirements:
1. Same parametric spirit: point/line luminous body drawn on canvas with
   requestAnimationFrame, all motion from closed-form math driven by time t.
2. A real gallop cycle: spine flexes through extension -> coil -> suspension
   (gather -> extend -> airborne), four legs phased like Muybridge's 1878
   "Sallie Gardner at a Gallop" plate (asymmetric rotary gallop: lead legs
   offset from trailing legs), tail and mane lagging the stride.
3. Keep the dark lab aesthetic: near-black background (#090808 family),
   luminous rgba(127,178,255,*) strokes/points, thin elegant lines.
4. Single self-contained HTML file, no external assets, no libraries.
   Canvas roughly 760x560. Add a one-line italic caption div under the canvas
   naming it "the horse (spore reinterpreted)".
5. The code must be clean vanilla JavaScript inside <script> tags and must not
   reference the fish task in any way except, optionally, a code comment.

Here is the fish prototype to reinterpret:

{fish_src}

Return ONLY the full HTML document for the horse."""

from models.providers import chat_provider  # noqa: E402

t0 = time.time()
r = chat_provider(
    "deepseek",
    SYSTEM,
    USER,
    model="deepseek-v4-flash",
    thinking=False,
    max_tokens=32768,
    tier="T2",
    allow_peak=True,
    timeout=300,
)
elapsed = time.time() - t0

receipt = {
    "ok": r.get("ok"),
    "elapsed_s": round(elapsed, 1),
    "usage": r.get("usage"),
    "error": r.get("error"),
    "model": r.get("model"),
}
print(json.dumps(receipt, indent=2))

if not r.get("ok"):
    RECEIPT.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    sys.exit(1)

content = r.get("text") or ""
# Strip any fence slop defensively (model was told not to, but verify cheap).
s = content.strip()
if s.startswith("```"):
    s = s.split("\n", 1)[1] if "\n" in s else s
    if s.rstrip().endswith("```"):
        s = s.rstrip()[:-3]
s = s.strip()
if not s.startswith("<!DOCTYPE"):
    i = s.find("<!DOCTYPE")
    if i >= 0:
        s = s[i:]

OUT.write_text(s, encoding="utf-8")
receipt["out_file"] = str(OUT)
receipt["out_bytes"] = len(s.encode("utf-8"))
receipt["out_lines"] = s.count("\n") + 1
RECEIPT.parent.mkdir(parents=True, exist_ok=True)
RECEIPT.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
print(f"WROTE {OUT} ({receipt['out_bytes']} bytes, {receipt['out_lines']} lines)")
