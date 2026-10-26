#!/usr/bin/env python3
"""STEER FIELD v0 — the film. One field, three rightsized consumers.

The soap-bubble law (operator, canon/bubbles): steer the interior by writing on
the film. This organ reads REAL fleet state and writes ONE field that every
level consumes rightsized:
  L1 operator  -> dashboard/static/steer_field.html (the iridescence)
  L2 dumb      -> walkers in the same html, gradient-follow the lights
  L3 steered   -> watch/steer_field/TAILS.md (memlang tails per contracted seat)

Sources (all real, no synthetic): watch/bay/state/*.json (engines, contracted
seats, mining attempts), watch/bay_share.jsonl (wing traffic + turn failures),
watch/room.jsonl (seat liveness), queue/steer_agent.md (operator pen).

FEED LAW (2026-10-18, supersedes the old static-render law): this script is a
DATA FEED, not a page generator. It writes watch/steer_field/FIELD.json +
TAILS.md and a served copy dashboard/static/steer_field/FIELD.json; the page
dashboard/static/steer_field.html is a durable consumer that fetches the
served copy same-origin (snapshot inlined there is only an offline fallback,
and the page labels the data's age). The page is never rewritten by this
script - it stopped owning the html after the 2026-10-18 full-width refactor
(the old template-generation path is deleted, not guarded).
All paths are literal joins under the repo root resolved from this file's
location; no user input participates in any path.
"""
import json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
assert (ROOT / "watch").is_dir() and (ROOT / "dashboard").is_dir(), "wrong anchor"
OUT = ROOT / "watch" / "steer_field"
STATIC = ROOT / "dashboard" / "static"
BAY = ROOT / "watch" / "bay" / "state"
BAY_SHARE = ROOT / "watch" / "bay_share.jsonl"
PEN = ROOT / "queue" / "steer_agent.md"

W, H = 960, 600

# engine family -> wavelength (nm) + color + lane name. Wavelength = tool selector.
FAMILIES = {
    "A": (610, "#ffb347", "glm-flash-free"),
    "B": (585, "#ffe066", "glm-32b"),
    "E": (540, "#7dffa8", "openclaw"),
    "Z": (470, "#6fd8ff", "zai-opencode"),
}
OPERATOR = (395, "#ffffff", "operator")

# failure-class occluders — the pillars, fixed like THE ROOM's (same geometry law)
OCCLUDERS = [
    {"id": "oc_freeflap",  "x": 200, "y": 130, "w": 44, "h": 150, "label": "free-lane flap"},
    {"id": "oc_collapse",  "x": 460, "y": 330, "w": 44, "h": 170, "label": "model collapse"},
    {"id": "oc_mount",     "x": 700, "y": 110, "w": 44, "h": 150, "label": "mount mismatch"},
    {"id": "oc_fold",      "x": 620, "y": 430, "w": 44, "h": 120, "label": "boilerplate fold"},
]

SLOT = [(140, 90), (420, 80), (700, 90), (180, 330), (430, 460), (760, 380), (870, 200)]


def read_jsonl(path, tail=60):
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    except OSError:
        return []
    out = []
    for ln in lines[-tail:]:
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def build_lights():
    lights, seats = [], []
    eng_files = sorted(p.name for p in BAY.glob("*.json")) if BAY.is_dir() else []
    slot = 0
    for fn in eng_files:
        eng = fn[:-5]
        try:
            st = json.loads((BAY / fn).read_text(encoding="utf-8", errors="ignore") or "{}")
        except json.JSONDecodeError:
            st = {}
        fam = FAMILIES.get(eng.split(".")[0], FAMILIES["Z"])
        x, y = SLOT[slot % len(SLOT)]
        slot += 1
        share_n = len(st.get("attempts", {}))
        lights.append({
            "id": "eng_" + eng, "x": x, "y": y, "nm": fam[0], "color": fam[1],
            "lane": fam[2], "kind": "engine",
            "label": f"{eng} · {fam[2]} · sess~{st.get('next_sess', 1)}",
            "intensity": round(min(1.0, 0.35 + 0.08 * share_n), 2),
        })
        for s in st.get("contracted", []):
            seats.append({"seat": s, "engine": eng, "lx": x, "ly": y, "lane": fam[2]})
    # operator pen: non-heading, non-example lines in the steer drop = white lights
    if PEN.exists():
        for i, ln in enumerate(PEN.read_text(encoding="utf-8", errors="ignore").splitlines()):
            t = ln.strip()
            if not t or t.startswith(("#", ">", "- Example")):
                continue
            lights.append({"id": f"op_{i}", "x": 420 + (i % 3) * 60, "y": 262,
                           "nm": OPERATOR[0], "color": OPERATOR[1], "lane": OPERATOR[2],
                           "kind": "operator", "label": "OPERATOR: " + t[:70],
                           "intensity": 1.0})
    return lights, seats


def _ts(v):
    try:
        return time.mktime(time.strptime(str(v)[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0


def apply_share_traffic(lights, seats):
    """Recency + health from bay_share: fresh wing = boost, turn-fail = 0.3x + flag."""
    shares = read_jsonl(BAY_SHARE, 80)
    now = time.time()
    per_seat, health = {}, {}
    for sh in shares:
        s = sh.get("from", "")
        per_seat[s] = sh
        txt = str(sh.get("top", ""))
        health[s] = "failed" if "turn failed" in txt or "failed before producing" in txt else "ok"
    for st in seats:
        sh = per_seat.get(st["seat"])
        if not sh:
            continue
        age_h = max(0.0, (now - _ts(sh.get("ts"))) / 3600.0) if sh.get("ts") else 99
        st["wing"] = sh.get("wing", "")
        st["age_h"] = round(age_h, 1)
        st["health"] = health.get(st["seat"], "quiet")
        for li in lights:
            if li["id"] == "eng_" + st["engine"]:
                if health.get(st["seat"]) == "failed":
                    li["intensity"] = round(li["intensity"] * 0.3, 2)
                    li["label"] += " · TURN-FAIL " + st["wing"]
                elif age_h < 2:
                    li["intensity"] = min(1.0, li["intensity"] + 0.25)
    return lights, seats


def rect_blocked(x0, y0, x1, y1, oc):
    """coarse line-of-sight: sample 24 points along the segment vs occluder rects."""
    for i in range(1, 24):
        t = i / 24.0
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for r in oc:
            if r["x"] <= px <= r["x"] + r["w"] and r["y"] <= py <= r["y"] + r["h"]:
                return True
    return False


def build_tails(seats, lights, occluders):
    """L3: per-seat memlang tail. Nearest line-of-sight light wins."""
    lines, rows = [], []
    for st in sorted(seats, key=lambda s: s["seat"]):
        best, bd = None, 1e9
        for li in lights:
            d = ((st["lx"] - li["x"]) ** 2 + (st["ly"] - li["y"]) ** 2) ** 0.5
            if d < bd and not rect_blocked(st["lx"], st["ly"], li["x"], li["y"], occluders):
                best, bd = li, d
        if not best:
            tail = f"[{st['seat']}] hold position · field occluded"
        else:
            note = best["label"].split(" · ")[-1]
            tail = f"[{st['seat']}] steer→{best['id']} λ{best['nm']} · {best['lane']} · {note}"
        lines.append("- " + tail)
        rows.append({"seat": st["seat"], "engine": st["engine"], "wing": st.get("wing", ""),
                     "health": st.get("health", "quiet"), "age_h": st.get("age_h", -1),
                     "target": best["id"] if best else None, "tail": tail})
    return lines, rows


# (the HTML template that used to live here was retired 2026-10-18: this
# script stopped generating steer_field.html — the page is a durable consumer
# that fetches the served FIELD.json; see FEED LAW in the module docstring)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lights, seats = build_lights()
    lights, seats = apply_share_traffic(lights, seats)
    tails, rows = build_tails(seats, lights, OCCLUDERS)
    walkers = [{"i": i, "x": 40 + (i % 3) * 30, "y": 300 + (i // 3) * 120} for i in range(6)]
    field = {
        "schema": "field.v1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "law": "steer the interior by writing on the film (canon/bubbles); "
               "one field, consumers rightsized: render/operator, walkers/dumb, tails/steered",
        "lights": lights, "occluders": OCCLUDERS, "walkers": walkers,
        "seat_tails": rows,
    }
    (OUT / "FIELD.json").write_text(json.dumps(field, indent=1), encoding="utf-8")
    (OUT / "TAILS.md").write_text(
        "# STEER TAILS — from the film (regen: python watch/steer_field/build.py)\n\n"
        + "\n".join(tails) + "\n", encoding="utf-8")
    SERVED = STATIC / "steer_field"
    SERVED.mkdir(parents=True, exist_ok=True)
    (SERVED / "FIELD.json").write_text(json.dumps(field, indent=1), encoding="utf-8")
    print(f"[field] {len(lights)} lights, {len(seats)} seats, {len(OCCLUDERS)} occluders")
    for r in rows:
        print(f"  {r['seat']:<8} {r['health']:<7} wing={r['wing'] or '-':<14} -> {r['target']}")
    print("[out] watch/steer_field/FIELD.json + TAILS.md + dashboard/static/steer_field/FIELD.json (served)")


if __name__ == "__main__":
    main()
