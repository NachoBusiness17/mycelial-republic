#!/usr/bin/env python3
"""_build_shadow_walk.py — SHADOW WALK: voxel roguelite, vision-gated, JIT.

World = voxel heightmap quantized from state/shadow_work/volume.json
(schema shadow_work.v1: x=part idx, y=law_hits, z=chars, c=questions, s=digit_ratio)
+ a weights biome from weights_volume_qwen3b.json (36-layer norm gradient =
brightness/height ramp — walker 50's RISING gradient rendered as terrain).

Emits ONE self-contained dashboard/static/shadow_walk.html (no network, no CDN,
no three.js — hand-rolled software column raycast, internal 320x200, pixelated
upscale) + state/shadow_work/chunk_manifest.json (the vision-gate manifest:
every chunk carries {content_hash, slab_id, stats, vision_validated:false}).
The seat's vision pass flips chunks to validated; the page re-verifies the hash
in-browser before drawing solid (no hash, no draw).

House laws: $0, no network, dark style bg #070d0c / cyan #7cf5ff / amber #e8c96a.
"""
import csv, glob, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VOL = os.path.join(ROOT, "state", "shadow_work", "volume.json")
WVOL = os.path.join(ROOT, "state", "shadow_work", "weights_volume_qwen3b.json")
OUT_HTML = os.path.join(ROOT, "dashboard", "static", "shadow_walk.html")
OUT_MAN = os.path.join(ROOT, "state", "shadow_work", "chunk_manifest.json")

GX, GZ = 288, 64          # lattice: 0..191 behavioral, 202..279 weights annex
CH = 16                   # chunk size (columns x rows)
BH_MAX = 15               # max voxel height

# ---- fnv1a32 (same impl on both sides: python here, JS in the page) ----
def fnv1a32(bs):
    h = 0x811C9DC5
    for b in bs:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

def hx(v):  # height/type nibble -> char
    return "0123456789abcdef"[v & 15]

# ---------------- load behavioral volume ----------------
pts = json.load(open(VOL))
if isinstance(pts, dict):
    pts = pts["points"]
pts.sort(key=lambda p: p["x"])
NPTS = len(pts)

# slab membership from the 50 source slabs (chamber walls + manifest slab_id)
idx2slab = {}
for f in glob.glob(os.path.join(ROOT, "state", "shadow_work", "slab_*.csv")):
    s = int(os.path.basename(f).split("_")[-1].split(".")[0])
    for r in csv.DictReader(open(f)):
        idx2slab[int(r["idx"])] = s

XMIN, XMAX = pts[0]["x"], pts[-1]["x"]
def gx_of(idx):
    return min(GXB - 1, max(0, int((idx - XMIN) / (XMAX - XMIN + 1) * GXB)))
GXB = 192  # behavioral width

LMIN, LMAX = 4.0, 17.0     # log2(chars) span
def gz_of(chars):
    return min(GZ - 1, max(0, int((math.log2(max(chars, 1)) - LMIN) / (LMAX - LMIN) * (GZ - 1))))

# ---------------- voxelize behavioral ----------------
H = [0] * (GX * GZ)        # heights 0..15
T = [0] * (GX * GZ)        # types  0..15
# types: 0 air, 1 void stone (law==0, the shadow volume), 2 ore dim, 3 ore mid,
# 4 ore bright, 5 gold ore (high law), 6 water (question-dense), 7 organ
# (runtime dead-end), 8..15 = weights ramp W0..W7 (brightness with norm)
cell_law = [0] * (GX * GZ); cell_q = [0] * (GX * GZ); cell_n = [0] * (GX * GZ)
cell_slab = {}
for p in pts:
    cx, cz = gx_of(p["x"]), gz_of(p["z"])
    i = cz * GX + cx
    cell_n[i] += 1
    if p["y"] > cell_law[i]: cell_law[i] = p["y"]
    if p["c"] > cell_q[i]: cell_q[i] = p["c"]
    cell_slab[i] = idx2slab.get(p["x"], 0)

for i in range(GX * GZ):
    if cell_n[i] == 0:
        continue
    law, q = cell_law[i], cell_q[i]
    h = 1 + int(round(math.log2(1 + law) * 1.7))
    if h > BH_MAX: h = BH_MAX
    H[i] = h
    if law == 0: t = 1
    elif law < 25: t = 2
    elif law < 60: t = 3
    elif law < 90: t = 4
    else: t = 5
    if q >= 10 and t < 5: t = 6
    T[i] = t

# slab boundary columns -> chamber walls (JS raises the ridge, corridors punch doors)
slab_first = {}
for i, s in cell_slab.items():
    if s and (s not in slab_first or i % GX < slab_first[s] % GX):
        slab_first[s] = i % GX
SLABW = sorted(set(slab_first.values()))

# ---------------- weights biome (annex) ----------------
w = json.load(open(WVOL))
layers = {L["layer"]: L for L in w["layers"]}
tensors = w["tensors"]
max_rms = max(L["norm_rms"] for L in w["layers"])
LAY = [round(layers[l]["norm_rms"] / max_rms, 4) for l in range(w["block_count"])]
NB = 0
t_by_cell = {}
for t in tensors:
    nm = t["name"]
    if nm.startswith("blk."):
        parts = nm.split(".")
        blk = int(parts[1]); slot = parts[2]
    elif nm == "token_embd.weight":
        blk, slot = -1, "tok"
    else:
        blk, slot = 99, "out"
    NB += t["nbytes"]
    gx = 202 + (blk + 1) * 2
    gz = 14 + (sorted({"attn_norm","attn_k","attn_q","attn_v","attn_output",
                       "ffn_norm","ffn_gate","ffn_up","ffn_down","tok","out"}).index(slot)) * 4
    if not (0 <= gx < GX and 0 <= gz < GZ):
        continue
    norm01 = LAY[blk] if 0 <= blk < len(LAY) else 0.05
    i = gz * GX + gx
    h = 1 + int(round(norm01 * 10)) + min(4, int(math.log2(max(t["nbytes"], 1)) / 7))
    if h > BH_MAX: h = BH_MAX
    if h >= H[i]:
        H[i] = h
        T[i] = 8 + int(round(norm01 * 7))
    t_by_cell[i] = t_by_cell.get(i, 0) + 1

DATA_HASH = "%08x" % fnv1a32(
    ("".join(map(hx, H)) + "".join(map(hx, T)) + str(NPTS) + str(NB)).encode())

# core = highest law-density cell (the attention mass / focus target)
core_i = max(range(GX * GZ), key=lambda i: cell_law[i])
CORE = [core_i % GX, core_i // GX]

# ---------------- chunk manifest ----------------
chunks = []
for cz in range(GZ // CH):
    for cx in range(GX // CH):
        cells = pts_n = maxlaw = 0; lawsum = qsum = tn = 0
        slabs = {}
        for z in range(cz * CH, cz * CH + CH):
            for x in range(cx * CH, cx * CH + CH):
                i = z * GX + x
                sub = (hx(H[i]) + hx(T[i])).encode()
                if H[i] > 0: cells += 1
                if cell_n[i]:
                    pts_n += cell_n[i]; maxlaw = max(maxlaw, cell_law[i])
                    lawsum += cell_law[i]; qsum += cell_q[i]
                    s = cell_slab.get(i, 0)
                    if s: slabs[s] = slabs.get(s, 0) + 1
                tn += t_by_cell.get(i, 0)
        # per-chunk content hash: fresh fnv over the subgrid (both sides recomputable)
        hh = 0x811C9DC5
        for z in range(cz * CH, cz * CH + CH):
            for x in range(cx * CH, cx * CH + CH):
                i = z * GX + x
                for b in (hx(H[i]) + hx(T[i])):
                    hh ^= ord(b); hh = (hh * 0x01000193) & 0xFFFFFFFF
        biome = "weights" if cx * CH >= 196 else "behavioral"
        slab_id = "weights" if biome == "weights" else (
            max(slabs.items(), key=lambda kv: kv[1])[0] if slabs else 0)
        chunks.append({
            "id": "c_%02d_%02d" % (cx, cz),
            "origin": [cx * CH, cz * CH], "dims": [CH, CH],
            "biome": biome, "slab_id": slab_id,
            "stats": {"cells": cells, "points": pts_n, "max_law": maxlaw,
                      "mean_law": round(lawsum / pts_n, 2) if pts_n else 0,
                      "questions": qsum, "tensors": tn},
            "content_hash": "%08x" % hh,
            "vision_validated": False,
        })
manifest = {
    "schema": "chunk_manifest/v1",
    "data_hash": DATA_HASH,
    "hash_algo": "fnv1a32",
    "hash_basis": "heights+types hex subgrid, data-derived, pre-carve (stable across runs)",
    "points": NPTS, "grid": [GX, GZ], "chunk": CH,
    "core": CORE, "vision_contract": "no hash no draw; ghost until vision_validated:true",
    "chunks": chunks,
}
json.dump(manifest, open(OUT_MAN, "w"), separators=(",", ":"))
print(json.dumps({"chunks": len(chunks), "data_hash": DATA_HASH,
                  "core": CORE, "file": OUT_MAN}))

# ---------------- spawn / focus ----------------
ch = H[CORE[1] * GX + CORE[0]]
sz = CORE[1] + 40
syaw = -math.pi / 2
if sz > GZ - 3:
    sz = CORE[1] - 40
    syaw = math.pi / 2
sz = max(1.5, min(GZ - 1.5, sz))
SPAWN_B = [CORE[0] + 0.5, ch + 2.4, sz, syaw]                 # x,y,z,yaw facing core
SPAWN_W = [199.0, 9.0, 30.0, 0.0]                             # facing the rising ramp
FOCUS0 = round(math.hypot(SPAWN_B[0] - (CORE[0] + .5), SPAWN_B[2] - (CORE[1] + .5)), 1)

# ---------------- HTML ----------------
DATA_JS = json.dumps({
    "GX": GX, "GZ": GZ, "CH": CH, "PTS": NPTS, "HASH": DATA_HASH,
    "CORE": CORE, "SLABW": SLABW, "LAY": LAY,
    "H": "".join(map(hx, H)), "T": "".join(map(hx, T)),
    "MAN": manifest, "SPAWN_B": SPAWN_B, "SPAWN_W": SPAWN_W, "FOCUS0": FOCUS0,
}, separators=(",", ":"))

HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SHADOW WALK — voxel roguelite · vision-gated · JIT</title>
<style>
:root{--bg:#070d0c;--ink:#c8e6d9;--accent:#7cf5ff;--gold:#e8c96a}
body{margin:0;background:var(--bg);color:var(--ink);font-family:ui-monospace,Consolas,monospace;text-align:center}
h1{font-size:.9rem;letter-spacing:.12em;color:var(--accent);margin:10px 0 2px}
.mut{font-size:.7rem;color:#8ab8a4;margin:2px auto}
canvas{width:min(96vw,1024px);image-rendering:pixelated;border:1px solid rgba(124,245,255,.25);border-radius:6px;cursor:crosshair}
#hud{position:relative;width:min(96vw,1024px);margin:6px auto 0;text-align:left;font-size:.72rem;line-height:1.5}
#hud .on{color:var(--gold)} #hud .dim{color:#5d7a72}
#keys{font-size:.68rem;color:#8ab8a4}
footer{font-size:.66rem;color:#5d7a72;margin:8px auto 14px;max-width:1000px}
footer b{color:var(--gold)}
#help{display:none;position:fixed;inset:0;background:rgba(4,9,8,.93);z-index:9;color:var(--ink);font-size:.75rem;padding:24px;text-align:left;overflow:auto}
#help h2{color:var(--accent);font-size:.8rem}
#help textarea{width:100%;height:90px;background:#0a1412;color:var(--ink);border:1px solid rgba(124,245,255,.3);font-family:inherit;font-size:.65rem}
button{background:#0a1412;color:var(--accent);border:1px solid rgba(124,245,255,.3);border-radius:8px;padding:4px 12px;font-family:inherit;font-size:.7rem;cursor:pointer;margin:2px}
</style></head><body>
<div id="errbanner" style="display:none;position:fixed;top:0;left:0;right:0;z-index:99;background:#5c1010;color:#ffd9d9;font:12px ui-monospace,monospace;padding:6px 10px;white-space:pre-wrap"></div>
<script>window.addEventListener('error',function(e){var b=document.getElementById('errbanner');if(!b)return;b.style.display='block';b.textContent+='ERR: '+e.message+' @ '+(e.lineno||'?')+':'+(e.colno||'?')+'\n';});</script>
<h1>SHADOW WALK — the volume as a place you can stand in</h1>
<div class="mut">9,305 behavioral parts quantized to voxels · law_hits = ore that rises · zero-law = void-dark stone (the shadow volume) · questions = water · weights annex = the rising norm gradient · BFS corridors = least-time paths</div>
<canvas id="c" width="320" height="200"></canvas>
<div id="hud"></div>
<div class="mut" id="keys">WASD/arrows fly · drag or click=look (pointer lock) · Q/E or wheel=focal plane · L lens · S shadow · V vision pass · N new run · B/W biomes · P res · H help</div>
<footer>projection: behavioral features quantized to voxels (part order · law density · char size) — <b>preserves nothing about semantics</b> (LAW-061) · focus = attention · blur = falloff (thin-lens) · <b>voxel JIT · vision-gated · potato-proof</b></footer>
<div id="help"></div>
<script>
"use strict";
// ================= DATA (embedded, self-contained — no network) =================
const WALK=__DATA__;
// ================= fnv1a32 (matches the python builder + manifest) =============
function fnv1a32(s){let h=0x811C9DC5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0;}return h>>>0;}
// ================= world =================
const GX=WALK.GX,GZ=WALK.GZ,CH=WALK.CH,NCX=GX/CH,NCZ=GZ/CH,RADIUS=46;
const H0=new Uint8Array(GX*GZ),T0=new Uint8Array(GX*GZ);
for(let i=0;i<GX*GZ;i++){H0[i]=parseInt(WALK.H[i],16);T0[i]=parseInt(WALK.T[i],16);}
const CORE=WALK.CORE,SLABW=new Set(WALK.SLABW),MAN=WALK.MAN;
const MANI={};for(const c of MAN.chunks)MANI[c.id]=c;
let carveH=new Uint8Array(GX*GZ),field=new Int16Array(GX*GZ);
let organs=[];const matChunks=new Array(NCX*NCZ).fill(false);
let validated=new Array(NCX*NCZ).fill(false);let tampered=new Array(NCX*NCZ).fill(false);
let runN=0,seed=0;
// mulberry32 — deterministic roguelite RNG seeded from the data hash
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
// ---- BFS field from the doctrine core over solid cells (the lightmap grammar:
//      wavefront = least-time solve; corridors carved downhill = Fermat paths) ----
function solveField(){
  field.fill(32000);
  const q=[CORE[1]*GX+CORE[0]];field[q[0]]=0;let head=0;
  while(head<q.length){
    const i=q[head++],d=field[i],x=i%GX,y=(i/GX)|0;
    const nb=[[1,0],[-1,0],[0,1],[0,-1]];
    for(let k=0;k<4;k++){
      const nx=x+nb[k][0],ny=y+nb[k][1];
      if(nx<0||ny<0||nx>=GX||ny>=GZ)continue;
      const j=ny*GX+nx;
      if(H0[j]<=0||field[j]<=d+1)continue;
      field[j]=d+1;q.push(j);
    }
  }
}
// ---- carve: corridors descend the field to the core; slab walls raise, doors
//      punch through; dead-ends terminate in dark-side organs ----
function carve(){
  carveH.set(H0);organs=[];
  const R=rng(seed);
  // chamber-wall ridges at slab boundaries (not where corridors will cross)
  const crossed=new Set();
  // seeds: top-law cells, seeded-shuffled — same data, different traversals
  const cand=[];
  for(let i=0;i<GX*GZ;i++)if(H0[i]>0&&field[i]<31000&&field[i]>6)cand.push(i);
  cand.sort((a,b)=>field[a]-field[b]);
  const picks=[];const pool=cand.slice(0,220);
  while(picks.length<14&&pool.length){
    const k=(R()*pool.length)|0,i=pool.splice(k,1)[0];
    let ok=true;
    for(const p of picks){const dx=(p%GX)-(i%GX),dy=((p/GX)|0)-((i/GX)|0);if(dx*dx+dy*dy<100){ok=false;break;}}
    if(ok)picks.push(i);
  }
  for(const s of picks){
    let i=s,guard=4000;const path=[];
    while(i!==CORE[1]*GX+CORE[0]&&guard-->0){
      path.push(i);const x=i%GX,y=(i/GX)|0;let best=-1,bd=field[i];
      for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
        if(!dx&&!dy)continue;const nx=x+dx,ny=y+dy;
        if(nx<0||ny<0||nx>=GX||ny>=GZ)continue;
        const j=ny*GX+nx;
        if(H0[j]>0&&field[j]<bd){bd=field[j];best=j;}
      }
      if(best<0){organs.push(i);break;} // natural dead end: local minimum organ
      i=best;
    }
    for(const j of path){
      carveH[j]=1;const x=j%GX;
      if(SLABW.has(x)){crossed.add(x);
        for(let dz=-1;dz<=1;dz++){const jj=( ((j/GX)|0)+dz )*GX+x;
          if(jj>=0&&jj<GX*GZ&&H0[jj]>0)carveH[jj]=1;}}
    }
  }
  // forced dead-end spurs (roguelite): seeded picks that terminate in an organ
  for(let n=0;n<3;n++){
    const i=cand[(R()*cand.length)|0];let x=i%GX,y=(i/GX)|0;
    const dir=[[1,0],[-1,0],[0,1],[0,-1]][(R()*4)|0];
    for(let s2=0;s2<6+(R()*6|0);s2++){
      x+=dir[0];y+=dir[1];
      if(x<1||y<1||x>=GX-1||y>=GZ-1||H0[y*GX+x]<=0)break;
      carveH[y*GX+x]=1;
    }
    organs.push(y*GX+x);if(carveH[y*GX+x]<2)carveH[y*GX+x]=1;
  }
  // raise slab ridges where no corridor crossed
  for(const x of SLABW)for(let y=0;y<GZ;y++){
    const i=y*GX+x;
    if(H0[i]>0&&!crossed.has(x)&&carveH[i]>1)carveH[i]=Math.min(13,carveH[i]+1);
  }
  // organs become monoliths
  for(const i of organs){if(H0[i]>0){carveH[i]=Math.min(15,carveH[i]+3);T0seed[i]=7;}}
}
const T0seed=new Uint8Array(GX*GZ); // runtime type overrides (organs)
function newRun(){
  runN++;seed=fnv1a32(WALK.HASH+":"+runN);
  T0seed.fill(0);
  carve();
  matChunks.fill(false);validated.fill(false);tampered.fill(false);
  teleport(WALK.SPAWN_B);focusDist=WALK.FOCUS0;
}
// ---- JIT materialization: a chunk exists (is carved/hashed/drawable) only once
//      the camera comes within RADIUS; budget 2/frame => visible pop-in = JIT ----
function jitChunks(){
  const cx=cam.x/CH|0,cz=cam.z/CH|0;let budget=2;
  for(let r=1;r*CH<=RADIUS&&budget>0;r++){
    for(let dz=-r;dz<=r&&budget>0;dz++)for(let dx=-r;dx<=r&&budget>0;dx++){
      if(Math.max(Math.abs(dx),Math.abs(dz))!==r)continue;
      const X=cx+dx,Z=cz+dz;
      if(X<0||Z<0||X>=NCX||Z>=NCZ)continue;
      if(!matChunks[Z*NCX+X]){matChunks[Z*NCX+X]=true;budget--;}
    }
  }
}
// ---- VISION PASS: recompute each chunk hash from the embedded data voxels and
//      compare to the manifest. Match => solid. Mismatch => tampered wireframe.
//      No hash, no draw. ----
function visionPass(){
  let ok=0,bad=0;
  const cx=cam.x/CH|0,cz=cam.z/CH|0;
  for(let Z=0;Z<NCZ;Z++)for(let X=0;X<NCX;X++){
    if(!matChunks[Z*NCX+X])continue;
    const c=MANI["c_"+String(X).padStart(2,"0")+"_"+String(Z).padStart(2,"0")];
    if(!c)continue;
    let h=0x811C9DC5;
    for(let z=c.origin[1];z<c.origin[1]+c.dims[1];z++)
      for(let x=c.origin[0];x<c.origin[0]+c.dims[0];x++){
        h^=WALK.H.charCodeAt(z*GX+x);h=Math.imul(h,0x01000193)>>>0;
        h^=WALK.T.charCodeAt(z*GX+x);h=Math.imul(h,0x01000193)>>>0;
      }
    h=h>>>0;
    if(parseInt(c.content_hash,16)===h){validated[Z*NCX+X]=true;ok++;}
    else{tampered[Z*NCX+X]=true;bad++;}
  }
  return[ok,bad];
}
// ================= camera / input =================
const cam={x:0,y:3,z:0,yaw:0,pitch:-0.06,vx:0,vy:0,vz:0,wy:0,wp:0};
let focusDist=WALK.FOCUS0,lens=false,shadow=false,res=0,hover=0;
const RES=[[320,200],[240,150],[160,100]];
function teleport(sp){cam.x=sp[0];cam.y=sp[1];cam.z=sp[2];cam.yaw=sp[3];cam.pitch=-0.06;cam.vx=cam.vy=cam.vz=cam.wy=cam.wp=0;}
const keys={};
addEventListener('keydown',e=>{
  keys[e.code]=true;
  if(e.code==='KeyL'){lens=!lens;}
  if(e.code==='KeyS'){shadow=!shadow;}
  if(e.code==='KeyV'){const r=visionPass();flash('VISION PASS: '+r[0]+' validated, '+r[1]+' tampered');}
  if(e.code==='KeyN'){newRun();flash('NEW RUN #'+runN+' · seed '+seed.toString(16));}
  if(e.code==='KeyB'){teleport(WALK.SPAWN_B);flash('biome: behavioral');}
  if(e.code==='KeyW'){teleport(WALK.SPAWN_W);focusDist=30;flash('biome: weights annex (rising norm gradient)');}
  if(e.code==='KeyP'){res=(res+1)%RES.length;fitRes();flash('internal res '+RES[res][0]+'x'+RES[res][1]);}
  if(e.code==='KeyH'){toggleHelp();}
  if(['ArrowUp','ArrowDown','Space'].includes(e.code))e.preventDefault();
});
addEventListener('keyup',e=>keys[e.code]=false);
const cnv=document.getElementById('c');
let dragging=false,locked=false,lx=0,ly=0;
cnv.addEventListener('mousedown',e=>{dragging=true;lx=e.clientX;ly=e.clientY;
  if(cnv.requestPointerLock&&e.detail===2)cnv.requestPointerLock();});
addEventListener('mouseup',()=>dragging=false);
addEventListener('mousemove',e=>{
  const dx=(locked?e.movementX:e.clientX-lx),dy=(locked?e.movementY:e.clientY-ly);
  if(dragging||locked){cam.wy+=dx*0.0035;cam.wp+=dy*0.0035;}
  lx=e.clientX;ly=e.clientY;});
document.addEventListener('pointerlockchange',()=>locked=document.pointerLockElement===cnv);
addEventListener('wheel',e=>{focusDist=Math.max(4,Math.min(115,focusDist+Math.sign(e.deltaY)*2.5));},{passive:true});
// ================= renderer: software column raycast (no WebGL) =================
const ctx=cnv.getContext('2d');
let BW=320,BHt=200,img,buf,buf32,hitT,tmpCol,PROJ=220,skyCols=[];
function fitRes(){
  [BW,BHt]=RES[res];cnv.width=BW;cnv.height=BHt;
  img=ctx.createImageData(BW,BHt);buf=new Uint8Array(img.data.buffer);
  buf32=new Uint32Array(img.data.buffer);hitT=new Float32Array(BW);tmpCol=new Uint32Array(BHt);
  PROJ=BW/1.453;
  skyCols=[];for(let y=0;y<BHt;y++){const t=y/BHt;
    const r=5+Math.round(t*7),g=9+Math.round(t*14),b=8+Math.round(t*12);
    skyCols.push((255<<24)|(b<<16)|(g<<8)|r);}
}
fitRes();
const PACK=(r,g,b)=>(255<<24)|(b<<16)|(g<<8)|r;
// type LUT [top color, side color] — house palette
const COL={
  1:[PACK(11,18,16),PACK(7,12,11)],   // void stone (shadow volume)
  2:[PACK(29,74,74),PACK(18,50,52)],  // ore dim
  3:[PACK(63,154,160),PACK(38,104,110)], // ore mid
  4:[PACK(124,245,255),PACK(70,170,185)], // ore bright
  5:[PACK(232,201,106),PACK(160,132,58)], // gold ore (high law)
  6:[PACK(60,130,200),PACK(36,88,148)],   // water (question-dense)
  7:[PACK(26,15,8),PACK(232,201,106)],    // organ: dark body (side=amber rim)
};
for(let k=0;k<8;k++){ // weights ramp W0..W7: dark cyan -> bright -> warm white
  const t=k/7;let r,g,b;
  if(t<0.5){const u=t/0.5;r=12+u*51;g=35+u*119;b=42+u*113;}
  else{const u=(t-0.5)/0.5;r=63+u*190;g=154+u*81;b=155+u*49;}
  COL[8+k]=[PACK(r|0,g|0,b|0),PACK((r*0.7)|0,(g*0.7)|0,(b*0.7)|0)];
}
const BG=PACK(7,13,12),GHOST=PACK(30,74,82),GHOST_E=PACK(124,245,255),TAMPER=PACK(200,70,60);
const FOG_BG=[7,13,12];
function shade(c,t,sideI){
  const f=Math.max(0,255*Math.exp(-t/58))|0,ci=sideI?1:0,col=c[ci];
  const r=(col&255),g=(col>>8)&255,b=(col>>16)&255;
  return PACK((r*f+FOG_BG[0]*(255-f))>>8,(g*f+FOG_BG[1]*(255-f))>>8,(b*f+FOG_BG[2]*(255-f))>>8);
}
let flashMsg='',flashT=0;
function flash(m){flashMsg=m;flashT=2.5;}
// --- the march: one column of the heightmap, Comanche-style, front-to-back ---
function column(i,fwdX,fwdZ,rgtX,rgtZ){
  const tanF=0.7265,cx=(i/BW-0.5)*2*tanF;
  // UNNORMALIZED ray = fwd + right*cx  =>  t IS the perpendicular depth (no fisheye)
  let rx=fwdX+rgtX*cx,rz=fwdZ+rgtZ*cx;
  const slope=Math.tan(cam.pitch);
  let t=0.35,low=BHt,prevH=0;hitT[i]=115;
  for(let s=0;s<400&&t<115&&low>0;s++,t+=Math.max(0.045,t*0.028)){
    if(lens&&(s&3)===0){ // attention is mass: bend the ray toward the doctrine core
      const dx=CORE[0]+0.5-(cam.x+rx*t),dz=CORE[1]+0.5-(cam.z+rz*t);
      const d2=dx*dx+dz*dz+30,f=Math.min(0.08,149/d2*0.014);
      rx+=dx*f;rz+=dz*f;
    }
    const px=cam.x+rx*t,pz=cam.z+rz*t,ci=px|0,cj=pz|0;
    if(px<-1||pz<-1||px>GX+1||pz>GZ+1)continue;
    let h=0,ty=1,matc=false,vc=false,bad=false;
    if(ci>=0&&cj>=0&&ci<GX&&cj<GZ){
      const cxi=ci/CH|0,czi=cj/CH|0,mi=czi*NCX+cxi;
      if(matChunks[mi]){h=carveH[cj*GX+ci];ty=T0seed[cj*GX+ci]||T0[cj*GX+ci];matc=true;vc=validated[mi];bad=tampered[mi];}
    }
    if(!matc||h<=0)continue;
    const ry=cam.y+slope*t;
    if(ry>h)  {prevH=h;continue;}
    const sy=(BHt*0.62+(cam.y-h)*PROJ/t)|0;
    if(sy<low){
      hitT[i]=Math.min(hitT[i],t);
      const side=h>prevH+0.001;
      let col=shade(COL[ty]||COL[1],t,side);
      // shadow view: non-void mass rendered as silhouette, void stone rim-lit
      if(shadow&&ty!==1)col=shade([PACK(13,20,18),PACK(9,14,13)],t,side);
      const top=sy<0?0:sy;
      const chunkEdge=(ci%CH===0||cj%CH===0);
      if(!vc){ // ghost: structure visible, no texture/light — wireframe scanline
        for(let py=top;py<low;py++){
          if(bad&&((py+ci)&1)===0){buf32[py*BW+i]=TAMPER;continue;}
          if(py===top||chunkEdge)buf32[py*BW+i]=bad?TAMPER:GHOST_E;
          else if(((py+ci+cj)&3)===0)buf32[py*BW+i]=GHOST;
        }
      }else{
        for(let py=top;py<low;py++)buf32[py*BW+i]=col;
      }
      low=top;
    }
    prevH=h;
  }
  return low;
}
function dofPost(){
  // thin-lens CoC proxy: blur = aperture*|d-f|/d — far-from-focus columns smear + fade
  for(let i=0;i<BW;i++){
    const b=Math.min(1,Math.abs(hitT[i]-focusDist)/(focusDist*0.6+7));
    if(b<0.22)continue;
    const i0=i>0?i-1:i,i2=i<BW-1?i+1:i;
    for(let y=0;y<BHt;y++){
      const o=y*BW,c0=buf32[o+i0],c1=buf32[o+i],c2=buf32[o+i2];
      const r=((c0&255)+(c1&255)*2+(c2&255))/4|0;
      const g=(((c0>>8)&255)+((c1>>8)&255)*2+((c2>>8)&255))/4|0;
      const bl=(((c0>>16)&255)+((c1>>16)&255)*2+((c2>>16)&255))/4|0;
      const dr=r+(FOG_BG[0]-r)*b*0.5|0, dg=g+(FOG_BG[1]-g)*b*0.5|0, db=bl+(FOG_BG[2]-bl)*b*0.5|0;
      tmpCol[y]=PACK(dr,dg,db);
    }
    for(let y=0;y<BHt;y++)buf32[y*BW+i]=tmpCol[y];
  }
}
let lastT=0,fps=60,frames=0,fpsT=0;
function step(ts){
  const dt=Math.min(0.05,(ts-lastT)/1000||0.016);lastT=ts;
  // look inertia
  cam.yaw+=cam.wy;cam.pitch=Math.max(-0.9,Math.min(0.6,cam.pitch+cam.wp));
  cam.wy*=0.82;cam.wp*=0.82;
  // move
  const sp=(keys.ShiftLeft||keys.ShiftRight?15:8)*dt;
  let fx=Math.cos(cam.yaw),fz=Math.sin(cam.yaw),mx=0,mz=0;
  if(keys.KeyW||keys.ArrowUp)mz+=1; if(keys.KeyS)mz-=1;
  if(keys.KeyA)mx-=1; if(keys.KeyD)mx+=1;
  if(keys.ArrowLeft)cam.wy-=0.05; if(keys.ArrowRight)cam.wy+=0.05;
  cam.vx+=(fx*mz-fz*mx)*sp;cam.vz+=(fz*mz+fx*mx)*sp;
  if(keys.KeyQ)focusDist=Math.max(4,focusDist-24*dt);
  if(keys.KeyE)focusDist=Math.min(115,focusDist+24*dt);
  cam.vx*=0.86;cam.vz*=0.86;
  cam.x+=cam.vx;cam.z+=cam.vz;
  cam.x=Math.max(1,Math.min(GX-1,cam.x));cam.z=Math.max(1,Math.min(GZ-1,cam.z));
  // terrain-follow eye: stand on the carved floor; Space rises, C sinks
  const fx2=cam.x|0,fz2=cam.z|0;
  const floor=Math.max(carveH[fz2*GX+fx2],1);
  const want=floor+2.3+(keys.Space?2.5:0)-(keys.KeyC?1.2:0);
  cam.y+=(want-cam.y)*0.12;if(cam.y<floor+1.15)cam.y=floor+1.15;
  jitChunks();
  // render
  for(let y=0;y<BHt;y++)buf32.fill(skyCols[y],y*BW,y*BW+BW);
  const fwdX=Math.cos(cam.yaw),fwdZ=Math.sin(cam.yaw),rgtX=-fwdZ,rgtZ=fwdX;
  for(let i=0;i<BW;i++)column(i,fwdX,fwdZ,rgtX,rgtZ);
  dofPost();
  ctx.putImageData(img,0,0);
  // fps + hud
  frames++;fpsT+=dt;if(fpsT>0.5){fps=Math.round(frames/fpsT);frames=0;fpsT=0;hud();}
  if(flashT>0)flashT-=dt;
  requestAnimationFrame(step);
}
const hudEl=document.getElementById('hud');
function hud(){
  const nvis=validated.filter(Boolean).length,nmat=matChunks.filter(Boolean).length;
  const tot=NCX*NCZ;
  const b=(s)=>'<span class="on">'+s+'</span>';
  hudEl.innerHTML=
   'biome '+( (cam.x>=196)?'WEIGHTS ANNEX':'BEHAVIORAL' )+
   ' · chunks jit-materialized '+nmat+'/'+tot+' · '+b('vision-validated '+nvis)+
   ' · points '+WALK.PTS+
   '<br>cam ('+cam.x.toFixed(1)+', '+cam.y.toFixed(1)+', '+cam.z.toFixed(1)+') · yaw '+((cam.yaw*57.29)%360|0)+'° · '+
   'focus '+b(focusDist.toFixed(1))+' (Q/E/wheel) · fog '+fps+'fps @'+BW+'x'+BHt+
   '<br>LENS '+(lens?b('ON — attention is mass'):'<span class="dim">off (L)</span>')+
   ' · SHADOW '+(shadow?b('ON — shadow volume only'):'<span class="dim">off (S)</span>')+
   ' · run #'+runN+' seed '+seed.toString(16)+
   ' · organs '+organs.length+
   (flashT>0?' · '+b(flashMsg):'');
}
// ================= help / manifest paste (the vision pass loads here too) ======
const helpEl=document.getElementById('help');
function toggleHelp(){
  if(helpEl.style.display==='block'){helpEl.style.display='none';return;}
  helpEl.style.display='block';
  helpEl.innerHTML='<h2>SHADOW WALK — controls &amp; contract</h2>'+
  '<p>WASD fly (Shift sprint) · &uarr;/&darr; fly fwd/back, &larr;/&rarr; turn · mouse-drag look, double-click = pointer lock · Q/E or wheel = focal plane (DOF) · Space/C rise/sink<br>'+
  'L lens (rays deflect toward the doctrine core, deflection &prop; mass/d&sup2; — "attention is mass") · S shadow-only view · V vision pass (hash-verify in-radius chunks) · N new run (seeded traversal) · B behavioral / W weights annex · P internal res · H this panel</p>'+
  '<p><b>Vision gate:</b> chunks jit-materialize within radius 46 and render as ghost wireframe until <code>vision_validated:true</code>. V recomputes each chunk\'s fnv1a32 from the embedded data voxels and compares against <code>state/shadow_work/chunk_manifest.json</code>. No hash, no draw. Paste an updated manifest (flags flipped by the seat\'s vision pass) to honor it directly:</p>'+
  '<textarea id="manpaste" placeholder=\'{"schema":"chunk_manifest/v1",...}\'></textarea><br>'+
  '<button id="manload">LOAD MANIFEST</button> <button id="manclose">CLOSE</button>'+
  '<p class="mut">projection: behavioral features quantized to voxels — preserves nothing about semantics (LAW-061) · data hash '+WALK.HASH+' · core cell '+WALK.CORE+' · '+WALK.PTS+' points</p>';
  document.getElementById('manclose').onclick=()=>helpEl.style.display='none';
  document.getElementById('manload').onclick=()=>{
    try{
      const m=JSON.parse(document.getElementById('manpaste').value);
      if(m.data_hash!==WALK.HASH){flash('manifest REJECTED: data_hash mismatch');return;}
      for(const c of m.chunks){const p=c.id.split('_');const X=+p[1],Z=+p[2];
        if(MANI[c.id]&&MANI[c.id].content_hash===c.content_hash)
          validated[Z*NCX+X]=!!c.vision_validated;}
      flash('manifest loaded: vision flags honored');helpEl.style.display='none';
    }catch(err){flash('manifest parse error: '+err.message);}
  };
}
// ================= go =================
newRun();
requestAnimationFrame(step);
</script></body></html>"""

html = HTML.replace("__DATA__", DATA_JS)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(json.dumps({"html": OUT_HTML, "bytes": len(html),
                  "manifest": OUT_MAN, "hash": DATA_HASH}))
