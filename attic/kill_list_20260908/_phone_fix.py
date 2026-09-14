from pathlib import Path

p = Path("mag/wave.py")
t = p.read_text(encoding="utf-8")
old = '''    verkle: dict[str, Any] = {}
    try:
        from mag import verkle_knot
        if hasattr(verkle_knot, "status"):
            verkle = verkle_knot.status() or {}
    except Exception as e:
        verkle = {"ok": False, "error": str(e)[:120]}
'''
new = '''    verkle: dict[str, Any] = {}
    try:
        from config import ROOT
        import json
        tip = ROOT / "memory" / "biography" / "verkle_tip.json"
        if tip.is_file():
            verkle = json.loads(tip.read_text(encoding="utf-8"))
    except Exception as e:
        verkle = {"ok": False, "error": str(e)[:120]}
'''
if old not in t:
    print("verkle block missing")
else:
    t = t.replace(old, new, 1)
    print("verkle cheap")

old2 = '''    team: dict[str, Any] = {}
    try:
        from mag.code_team import status as team_status
        team = team_status()
    except Exception as e:
        team = {"ok": False, "error": str(e)[:120]}

    surface: dict[str, Any] = {}
    try:
        from mag.surface_render import render_all
        ra = render_all()
        surface = {
            "doctrine_mermaid": (ra.get("doctrine_mermaid") or "")[:1200],
            "mesh_svg": ra.get("mesh_svg") or "",
            "live_metrics": ra.get("live_metrics"),
        }
    except Exception as e:
        surface = {"ok": False, "error": str(e)[:120]}
'''
new2 = '''    team: dict[str, Any] = {}
    surface: dict[str, Any] = {}
'''
if old2 not in t:
    print("team/surface missing")
else:
    t = t.replace(old2, new2, 1)
    print("skip render_all")

# skip persona_recall in idle (slow)
old3 = '''                try:
                    from mag.persona_recall import recall as pr_recall
                    pr = pr_recall(archetype="trickster", region="keep_gate")
'''
# find and comment by replacing the try block start with skip
if "pr_recall" in t:
    # neutralize by wrapping: change call to skip
    t = t.replace(
        "from mag.persona_recall import recall as pr_recall",
        "pr_recall = None  # phone: FILE tick only, skip slow persona_recall",
        1,
    )
    print("skip persona_recall")
p.write_text(t, encoding="utf-8")

h = Path("dashboard/static/wave.html")
html = h.read_text(encoding="utf-8")
if "voiceUnlocked" not in html:
    html = html.replace(
        "async function refresh() {",
        '''let inflight = false;
    let voiceUnlocked = false;
    function unlockVoice() {
      if (voiceUnlocked) return;
      voiceUnlocked = true;
      try { window.speechSynthesis && window.speechSynthesis.speak(new SpeechSynthesisUtterance(" ")); } catch (_) {}
    }
    document.addEventListener("pointerdown", unlockVoice);
    async function refresh() {
      if (inflight) return;
      inflight = true;
      try {''',
        1,
    )
    # close try at end of refresh - find setInterval and insert finally before it is wrong
    # add finally before last of refresh. Look for setInterval
    html = html.replace(
        "if (window.speechSynthesis) {\n        try { window.speechSynthesis.cancel(); } catch (_) {}\n        window.speechSynthesis.speak(new SpeechSynthesisUtterance(st));",
        "if (voiceUnlocked && window.speechSynthesis) {\n        try { window.speechSynthesis.cancel(); } catch (_) {}\n        window.speechSynthesis.speak(new SpeechSynthesisUtterance(st));",
        1,
    )
    html = html.replace("    setInterval(refresh, 4000);", "    } finally { inflight = false; }\n    }\n    setInterval(refresh, 4000);", 1)
    h.write_text(html, encoding="utf-8")
    print("html tap+inflight")
else:
    print("html already unlocked")
print("done")
