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

Static render law: the html inlines the field; it needs nothing from the network.
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


HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>STEER FIELD — the film</title>
<style>body{margin:0;background:#07080c;color:#cfd6e4;font:13px/1.5 Consolas,monospace}
#wrap{position:relative;width:960px;margin:0 auto}
canvas{display:block;background:#07080c}
h1{font-size:14px;letter-spacing:2px;color:#9fb0cc;margin:10px 0 4px}
.sub{color:#5c6a82;font-size:11px;margin-bottom:6px}
.legend{position:absolute;top:34px;right:8px;text-align:right;font-size:11px;color:#8a97ad}
</style></head><body><div id="wrap">
<h1>STEER FIELD — THE FILM</h1>
<div class="sub">__SUB__</div><div class="legend">__LEGEND__</div>
<canvas id="c" width="960" height="600"></canvas></div>
<script>
const F = __FIELD__;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
function hex2rgb(h){return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)];}
function field(x,y){ // the film's truth: summed radial falloff per light
  let v=0,r=0,g=0,b=0;
  for(const L of F.lights){
    const d=Math.hypot(x-L.x,y-L.y), rad=170*L.intensity+40;
    if(d<rad){const w=Math.pow(1-d/rad,1.6)*L.intensity,[lr,lg,lb]=hex2rgb(L.color);
      r+=w*lr;g+=w*lg;b+=w*lb;v+=w;}
  }
  return [v,[r,g,b]];
}
function inOcc(x,y){for(const o of F.occluders)if(x>=o.x&&x<=o.x+o.w&&y>=o.y&&y<=o.y+o.h)return o;return null;}
function draw(){
  const img=ctx.createImageData(960,600),d=img.data;
  for(let y=0;y<600;y+=2)for(let x=0;x<960;x+=2){
    const rgb=field(x,y)[1];
    for(let dy=0;dy<2;dy++)for(let dx=0;dx<2;dx++){
      const j=((y+dy)*960+(x+dx))*4;
      d[j]=Math.min(255,rgb[0])*0.9+7;d[j+1]=Math.min(255,rgb[1])*0.9+8;
      d[j+2]=Math.min(255,rgb[2])*0.9+12;d[j+3]=255;
    }
  }
  ctx.putImageData(img,0,0);
  ctx.fillStyle='#101319';
  for(const o of F.occluders){ctx.fillRect(o.x,o.y,o.w,o.h);
    ctx.strokeStyle='#39445c';ctx.strokeRect(o.x+.5,o.y+.5,o.w,o.h);
    ctx.save();ctx.translate(o.x+o.w/2,o.y+o.h/2);ctx.rotate(-Math.PI/2);
    ctx.fillStyle='#7c89a3';ctx.font='10px Consolas';ctx.textAlign='center';
    ctx.fillText(o.label,0,3);ctx.restore();}
  for(const L of F.lights){
    ctx.strokeStyle=L.color;ctx.lineWidth=L.kind==='operator'?2:1;
    ctx.beginPath();ctx.arc(L.x,L.y,L.kind==='operator'?7:5,0,7);ctx.stroke();
    ctx.fillStyle=L.color;ctx.font='10px Consolas';ctx.textAlign='left';
    ctx.fillText(L.label,L.x+9,L.y+3);
  }
  for(const w of F.walkers){ctx.fillStyle='#e8ecf5';
    ctx.beginPath();ctx.arc(w.x,w.y,2.6,0,7);ctx.fill();}
}
function step(){ // L2: dumb sagents — walk up the intensity gradient, bounce off occluders
  for(const w of F.walkers){
    let bx=w.x,by=w.y,bv=field(w.x,w.y)[0];
    for(let a=0;a<8;a++){const th=a*Math.PI/4+Math.sin(F.t+w.i)*0.3,
      nx=w.x+Math.cos(th)*3.2,ny=w.y+Math.sin(th)*3.2;
      if(nx<8||ny<8||nx>952||ny>592||inOcc(nx,ny))continue;
      const v=field(nx,ny)[0];if(v>bv){bx=nx;by=ny;bv=v;}
    }
    if(bx===w.x&&by===w.y){const th=Math.sin(F.t*1.7+w.i*2.1)*Math.PI*2,
      nx=w.x+Math.cos(th)*3.2,ny=w.y+Math.sin(th)*3.2;
      if(nx>8&&ny>8&&nx<952&&ny<592&&!inOcc(nx,ny)){w.x=nx;w.y=ny;}}
    else{w.x=bx;w.y=by;}
  }
  F.t+=0.05;
}
draw();setInterval(()=>{step();draw();},66);
</script></body></html>"""


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
    sub = (f"field ts {field['ts']} · {len(lights)} lights · {len(seats)} contracted seats · "
           f"{sum(1 for r in rows if r['health'] == 'failed')} turn-fail · {len(OCCLUDERS)} pillars")
    legend = "<br>".join(f"<span style='color:{f[1]}'>● {f[2]}</span>" for f in FAMILIES.values())
    html = (HTML.replace("__FIELD__", json.dumps(field))
                .replace("__SUB__", sub).replace("__LEGEND__", legend))
    (STATIC / "steer_field.html").write_text(html, encoding="utf-8")
    print(f"[field] {len(lights)} lights, {len(seats)} seats, {len(OCCLUDERS)} occluders")
    for r in rows:
        print(f"  {r['seat']:<8} {r['health']:<7} wing={r['wing'] or '-':<14} -> {r['target']}")
    print("[out] FIELD.json + TAILS.md + steer_field.html")


if __name__ == "__main__":
    main()
