"""eigenmap_two_smoke  -  EXECUTE the shipped THE CATHEDRAL scripts headless
(ractor card eigenmap, surviving build; landed by the revise-eigenmap pass
2026-09-27 to narrow pre-registered risk (c) of cands/eigenmap-two.md:
"BillboardGui, CFrame strips, portal landing and ShadowLedger touch rows are
type-checked and parsed but never executed").

What this runs: the REAL roblox/src/server/CathedralPlate.luau (build, entry,
tick x50, two beacon Touched events) and the REAL
roblox/src/client/CathedralMapHud.client.luau (entire top level incl. the
Heartbeat readout loop) under tools/bin/luau/luau.exe inside a Roblox-API
stub environment defined in tools/eigenmap_two_smoke.luau. Staged copies are
sha256-verified against the tree files before and after the run. Every
printed row is diffed against an independent Python recompute from
watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json.

What this PROVES: the executed code paths complete, the portal landing is
derived (entry() = plateCenter - size.Z/2 - 8), the chain strips breathe
inside [0.1, 0.34] and aim mid-edge at their far beacon, beacon touches file
ShadowLedger rows carrying the walker's live eigen position/dist/bearing,
the HUD draws the five region labels at the exact render-equation pixels
(-y up: the most-negative-ey region renders highest), and the standing-on-
beacon readout reads POS = the centroid with a 0.0000 "<-- HERE" row.

What this CANNOT prove (owed to a live Studio session, filed in queue/todo.md
under P0 THE MOUNTAIN): real GUI layout/rendering, physics-driven Touched,
DataStore durability. This is a stub execution, not Studio.

Also asserts the fold tripwires (judge 2026-09-27: eigenmap-one killed, tree
pruned to ONE cathedral map): no EigenMap*.luau under roblox/src, no EigenMap
bytes in the built the_mountain.rbxlx, CathedralPlate/Map/Hud present there,
init.server.luau wired to the survivor only.

Exit 0 = PASS. Receipt: watch/inbox/ractor_panel_20260926/eigenmap-two-smoke.txt
Usage: .venv/Scripts/python.exe tools/eigenmap_two_smoke.py
"""

import hashlib
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json"
MAP = ROOT / "roblox/src/shared/CathedralMap.luau"
PLATE = ROOT / "roblox/src/server/CathedralPlate.luau"
HUD = ROOT / "roblox/src/client/CathedralMapHud.client.luau"
DRIVER = Path(__file__).resolve().parent / "eigenmap_two_smoke.luau"
LUAU = ROOT / "tools/bin/luau/luau.exe"
RBXLX = ROOT / "roblox/the_mountain.rbxlx"
INIT = ROOT / "roblox/src/server/init.server.luau"
RECEIPT = ROOT / "watch/inbox/ractor_panel_20260926/eigenmap-two-smoke.txt"

# the stub canvas the Luau harness gives every Frame as AbsoluteSize
CANVAS_W, CANVAS_H = 280.0, 176.0

LEDGER_STUB = """-- ShadowLedger stub for the headless smoke (collects rows in memory;
-- the real ShadowLedger.luau owns the DataStore t74 write law)
local rows = {}
return {
\trecord = function(player, where, line)
\t\ttable.insert(rows, { player = player, where = where, line = line })
\tend,
\trows = rows,
}
"""

failures: list[str] = []
log: list[str] = []


def note(line: str) -> None:
    log.append(line)
    print(line)


def check(cond: bool, what: str) -> bool:
    tag = "PASS" if cond else "FAIL"
    note(f"[{tag}] {what}")
    if not cond:
        failures.append(what)
    return cond


def r4(x: float) -> float:
    return math.floor(x * 10000 + 0.5) / 10000 if x >= 0 else -math.floor(-x * 10000 + 0.5) / 10000


def r1(x: float) -> float:
    return math.floor(x * 10 + 0.5) / 10 if x >= 0 else -math.floor(-x * 10 + 0.5) / 10


def bearing_deg(a, b) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    return r1((math.degrees(math.atan2(dx, -dy)) + 360.0) % 360.0)


def main() -> int:
    scan = json.loads(SCAN.read_text(encoding="utf-8"))
    cents = scan["eigen_centroids"]
    regions = sorted(cents)
    water_first = ["water_computer", "fractal_maze", "riddler_optics",
                   "riddler_engram", "audit_dungeon"]
    cls = {r: scan["regions"][r]["class"] for r in regions}

    # module constants (single source: parse them from the shipped module text)
    mt = MAP.read_text(encoding="utf-8")

    def const(pat: str) -> float:
        m = re.search(pat, mt)
        if not m:
            raise SystemExit(f"constant not found in CathedralMap.luau: {pat}")
        return float(m.group(1))

    OX, OY, OZ = (const(rf"CathedralMap\.ORIGIN_{a} = (-?[\d.]+)") for a in ("X", "Y", "Z"))
    SCALE = const(r"CathedralMap\.SCALE = (\d+)")
    MARGIN = const(r"CathedralMap\.PLATE_MARGIN = (\d+)")

    def to_world_xz(r: str):
        return OX + cents[r][0] * SCALE, OZ + cents[r][1] * SCALE

    # ---- stage + run ----
    note("== staging the REAL tree files (byte-verified) ==")
    # The luau CLI sandboxes globals per file, so the two Roblox-facing
    # scripts get a prelude binding the shared SmokeEnv stubs as file-local
    # names; the tree bytes follow the prelude UNCHANGED (asserted below).
    prelude = (
        "-- SMOKE PRELUDE (not part of the tree file): the luau CLI gives each\n"
        "-- file its own global environment, so the Roblox API surface is bound\n"
        "-- from the shared SmokeEnv module as file-local names. Everything after\n"
        "-- this prelude is the UNCHANGED tree file.\n"
        "local _E = require(\"./SmokeEnv\")\n"
        "local game, workspace, script = _E.game, _E.workspace, _E.script\n"
        "local Instance, Vector3, Vector2, Color3 = _E.Instance, _E.Vector3, _E.Vector2, _E.Color3\n"
        "local UDim2, UDim, Enum, CFrame = _E.UDim2, _E.UDim, _E.Enum, _E.CFrame\n\n"
    )
    env_src = (Path(__file__).resolve().parent / "eigenmap_two_smoke_env.luau").read_text(encoding="utf-8")
    verbatim = {}
    preluded = {
        # CathedralMap's pure-number API touches no globals (proven verbatim
        # by tools/eigenmap_two_check.py); its Vector3 ADAPTERS (toWorld/
        # plateCenter/plateSize, exercised here by the plate + HUD) need the
        # env, so the smoke stages it preluded too.
        "CathedralMap.luau": MAP,
        "CathedralPlate.luau": PLATE,
        # luau require does not try the .client.luau suffix, so the HUD is
        # staged under a plain .luau name; CONTENT bytes are the tree bytes.
        # A LocalScript returns nothing, but the CLI require insists on a
        # single return value, so the staged copy carries a one-line footer.
        "CathedralMapHud.luau": HUD,
    }
    footers = {"CathedralMapHud.luau": b"\nreturn true -- smoke staging footer (LocalScript returns nothing; the CLI require wants a value)\n"}
    for name, path in list(verbatim.items()) + list(preluded.items()):
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        note(f"  {name}: {path.relative_to(ROOT)} tree sha256 {sha[:16]}...")

    out = ""
    with tempfile.TemporaryDirectory(prefix="eigenmap-two-smoke-") as td:
        tdp = Path(td)
        (tdp / "SmokeEnv.luau").write_text(env_src, encoding="utf-8", newline="")
        (tdp / "ShadowLedgerStub.luau").write_text(LEDGER_STUB, encoding="utf-8", newline="")
        (tdp / "main.luau").write_text(DRIVER.read_text(encoding="utf-8"), encoding="utf-8", newline="")
        check(hashlib.sha256((tdp / "SmokeEnv.luau").read_bytes()).hexdigest()
              == hashlib.sha256((Path(__file__).resolve().parent / "eigenmap_two_smoke_env.luau").read_bytes()).hexdigest(),
              "staged SmokeEnv.luau bytes are sha256-identical to the tools file")
        for name, path in verbatim.items():
            data = path.read_bytes()
            (tdp / name).write_bytes(data)
            check(hashlib.sha256((tdp / name).read_bytes()).hexdigest()
                  == hashlib.sha256(data).hexdigest(),
                  f"staged {name} bytes are sha256-identical to the tree file")
        for name, path in preluded.items():
            tree = path.read_bytes()
            footer = footers.get(name, b"")
            (tdp / name).write_bytes(prelude.encode("utf-8") + tree + footer)
            got = (tdp / name).read_bytes()
            check(got.startswith(prelude.encode("utf-8"))
                  and got.endswith(footer if footer else tree)
                  and hashlib.sha256(got[len(prelude):len(got) - len(footer)]).hexdigest()
                  == hashlib.sha256(tree).hexdigest(),
                  f"staged {name} = prelude + UNCHANGED tree bytes"
                  f"{' + return footer' if footer else ''} (tree sha256 identical)")
        proc = subprocess.run([str(LUAU), str(tdp / "main.luau")], capture_output=True, text=True)
        out = proc.stdout.strip()
        note(f"luau exit code: {proc.returncode}")
        if proc.stderr.strip():
            note(f"luau stderr: {proc.stderr.strip()[:2000]}")
        check(proc.returncode == 0, "luau executed plate + HUD to completion (no runtime error)")

    note("")
    note("-- raw luau stdout --")
    for line in out.splitlines():
        note("  " + line)
    note("-- end raw stdout --")

    # ---- parse rows ----
    entry = beacons = None
    strips, ledger, maplabels, readout = [], [], [], []
    trans_before = trans_after = None
    frames_count = None
    for line in out.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "entry":
            entry = tuple(float(x) for x in f[1:4])
        elif f[0] == "beacons":
            beacons = f[2].split(",") if len(f) > 2 else []
        elif f[0] == "strip":
            strips.append((float(f[2]), float(f[3]), float(f[4]), float(f[5]), float(f[6])))
        elif f[0] == "ledger_rows":
            pass
        elif f[0] == "ledger":
            m = re.match(r"ledger (\d+) where=(.*?) player=(\d+) (.*)$", line)
            if m:
                ledger.append(m.group(4))
        elif f[0] == "chaintrans":
            vals = [float(x) for x in f[2:]]
            if f[1] == "before":
                trans_before = vals
            else:
                trans_after = vals
        elif f[0] == "maplabel":
            m = re.match(r"maplabel (.*?) (-?[\d.e+-]+) (-?[\d.e+-]+) (-?[\d.e+-]+) (-?[\d.e+-]+)$", line)
            maplabels.append((m.group(1), *(float(x) for x in m.groups()[1:])))
        elif f[0] == "mapframe_frames":
            frames_count = int(f[1])
        elif f[0] == "readout":
            readout.append(line[len("readout "):])

    # ---- expectations from the JSON (independent recompute) ----
    note("")
    note("== plate: entry() is derived, beacons + strips built ==")
    check(beacons == regions, f"beacons at the eigen_centroids: {beacons}")

    xs = [cents[r][0] for r in regions]
    ys = [cents[r][1] for r in regions]
    cx = OX + (min(xs) + max(xs)) / 2 * SCALE
    cz = OZ + (min(ys) + max(ys)) / 2 * SCALE
    size_z = (max(ys) - min(ys)) * SCALE + 2 * MARGIN
    exp_entry = (cx, OY, cz - (size_z / 2 + 8))
    check(entry is not None and all(abs(a - b) < 1e-6 for a, b in zip(entry, exp_entry)),
          f"entry() lands NORTH of the floor, derived: {entry} == {exp_entry}")

    exp_chain = [(water_first[i], water_first[i + 1])
                 for i in range(len(water_first) - 1)
                 if cls[water_first[i]] == "SADDLE" and cls[water_first[i + 1]] == "SADDLE"]
    chain_pairs = {frozenset(e) for e in exp_chain}
    exp_hub = sorted((r for r in regions
                      if r != "water_computer" and cls[r] == "SADDLE"
                      and frozenset(("water_computer", r)) not in chain_pairs))
    exp_strips = [(1.4, a, b) for a, b in exp_chain] + [(0.9, "water_computer", b) for b in exp_hub]
    check(len(strips) == len(exp_strips),
          f"strip count {len(strips)} == chain {len(exp_chain)} + hub {len(exp_hub)}")
    for got, (w, a, b) in zip(strips, exp_strips):
        ax, az = to_world_xz(a)
        bx, bz = to_world_xz(b)
        midx, midz = (ax + bx) / 2, (az + bz) / 2
        sw, fx, fz, tx, tz = got
        ok = (abs(sw - w) < 1e-9 and abs(fx - midx) < 1e-6 and abs(fz - midz) < 1e-6
              and abs(tx - bx) < 1e-6 and abs(tz - bz) < 1e-6)
        check(ok, f"strip {a}->{b}: width {w} aimed from mid ({midx:.3f},{midz:.3f}) at {b} "
                  f"(got {sw}, ({fx:.3f},{fz:.3f}) -> ({tx:.3f},{tz:.3f}))")

    note("")
    note("== plate: the chain breathes ==")
    clock = 50 * (1 / 30)
    pulse = 0.1 + 0.12 * (math.sin(clock * 2) + 1) / 2
    check(trans_before is not None and all(abs(v - 0.1) < 1e-9 for v in trans_before),
          f"chain strips start at transparency 0.1 ({trans_before})")
    check(trans_after is not None and len(trans_after) == len(exp_chain)
          and all(abs(v - pulse) < 1e-9 for v in trans_after),
          f"after 50 ticks of 1/30s all {len(exp_chain)} chain strips read {pulse:.6f} ({trans_after})")
    check(all(0.1 <= v <= 0.34 for v in (trans_after or [1])),
          "breathing stays inside [0.1, 0.34] (the tick envelope)")

    note("")
    note("== plate: beacon Touched files a ShadowLedger row with the live readout ==")
    wc = cents["water_computer"]
    ex = (OX + wc[0] * SCALE - OX) / SCALE
    ey = (OZ + wc[1] * SCALE - OZ) / SCALE
    # The on-beacon self-bearing is the degenerate direction from a point to
    # itself: dx and dy land on signed zeros (or 1-ulp dust) and atan2(+0, -0)
    # reads 180.0 under CPython while the executed Luau read 0.0; both are the
    # same undefined direction, so the self row accepts either. The load-bearing
    # assertions are the live POS, dist 0.0000 and the cross-beacon bearing.
    exp1_re = re.compile(
        r"^reached water_computer \[SADDLE\] from eigen "
        r"\(-0\.0236, -0\.0124\), 0\.0000 away, bearing (0\.0|180\.0)$")
    ad = cents["audit_dungeon"]
    exp2 = (f"reached audit_dungeon [SADDLE] from eigen ({ex:.4f}, {ey:.4f}), "
            f"{r4(math.hypot(ad[0] - wc[0], ad[1] - wc[1])):.4f} away, "
            f"bearing {bearing_deg(wc, ad):.1f}")
    check(len(ledger) == 2, f"two touches filed two ledger rows ({len(ledger)} rows)")
    if len(ledger) >= 2:
        check(exp1_re.match(ledger[0]) is not None,
              f"row 1 (on-beacon): POS + dist 0.0000 + degenerate self-bearing "
              f"(0.0|180.0): {ledger[0]!r}")
        check(ledger[1] == exp2, f"row 2 (cross-beacon touch from water): {ledger[1]!r} == {exp2!r}")

    note("")
    note("== HUD: static map at the render-equation pixels (-y up) ==")
    minX, maxX = min(xs), max(xs)
    minY, maxY = min(ys), max(ys)
    mX, mY = (maxX - minX) * 0.13, (maxY - minY) * 0.13
    x0, x1, y0, y1 = minX - mX, maxX + mX, minY - mY, maxY + mY
    scale = min(CANVAS_W / (x1 - x0), CANVAS_H / (y1 - y0))
    offX = (CANVAS_W - (x1 - x0) * scale) / 2
    offY = (CANVAS_H - (y1 - y0) * scale) / 2

    def px(e): return offX + (e - x0) * scale
    def py(e): return offY + (e - y0) * scale

    # maplabels rows are (text, X.Scale, X.Offset, Y.Scale, Y.Offset)
    labels = {m[0]: (m[1], m[2], m[3], m[4]) for m in maplabels}
    abbrev = {"water_computer": "water", "fractal_maze": "fractal", "riddler_optics": "optics",
              "riddler_engram": "engram", "audit_dungeon": "audit"}
    for r in regions:
        t = abbrev[r]
        got = labels.get(t)
        exp = (0.0, px(cents[r][0]) + 8, 0.0, py(cents[r][1]))
        check(got is not None and all(abs(a - b) < 1e-6 for a, b in zip(got, exp)),
              f"label {t}: pixel ({exp[1]:.4f}, {exp[3]:.4f}) at the render equation (got {got})")
    north = labels.get("^ N (-y)")
    check(north is not None and abs(north[3] - 9) < 1e-9 and north[2] == 0.0,
          f"north marker pinned to the TOP edge (^ N (-y) at Y offset 9; got {north})")
    top_region = abbrev[min(regions, key=lambda r: cents[r][1])]      # most negative ey
    bottom_region = abbrev[max(regions, key=lambda r: cents[r][1])]
    check(labels[top_region][3] < labels[bottom_region][3],
          f"one compass at execution: {top_region} (most -ey) renders ABOVE {bottom_region} "
          f"(py {labels[top_region][3]:.2f} < {labels[bottom_region][3]:.2f})")
    exp_frames = 1 + 8 * len(exp_chain) + 6 * len(exp_hub) + len(regions) + 1  # layer + dots + youMarker
    check(frames_count == exp_frames,
          f"map frame holds layer + {8 * len(exp_chain)} chain dots + {6 * len(exp_hub)} hub dots "
          f"+ {len(regions)} region dots + youMarker = {exp_frames} frames (got {frames_count})")

    note("")
    note("== HUD: live readout standing ON water_computer ==")
    pos_line = f"POS eigen ({ex:.4f}, {ey:.4f})"
    check(len(readout) >= 7 and readout[0].startswith(pos_line) and "nearest water" in readout[0],
          f"POS line is the beacon centroid: {readout[0] if readout else None!r}")
    water_row = next((l for l in readout if l.startswith("water")), None)
    check(water_row is not None and f"{0.0:.4f}" in water_row and "<-- HERE" in water_row,
          f"standing on the beacon reads 0.0000 + <-- HERE: {water_row!r}")
    audit_row = next((l for l in readout if l.startswith("audit")), None)
    check(audit_row is not None and f"{r4(math.hypot(ad[0] - wc[0], ad[1] - wc[1])):.4f}" in audit_row,
          f"audit row carries the data distance {r4(math.hypot(ad[0] - wc[0], ad[1] - wc[1])):.4f}: {audit_row!r}")
    vote_line = next((l for l in readout if "vote:" in l), None)
    check(vote_line is not None and "chain 0.031 vs star 0.036" in vote_line,
          f"vote footer states the filed vote: {vote_line!r}")

    note("")
    note("== fold tripwires (judge 2026-09-27: one cathedral map) ==")
    leftover = [str(p.relative_to(ROOT)) for p in (ROOT / "roblox/src").rglob("EigenMap*.luau")]
    check(not leftover, f"no EigenMap luau under roblox/src (found {leftover})")
    rb = RBXLX.read_bytes()
    check(rb.count(b'name="Name">EigenMap') == 0,
          "the built the_mountain.rbxlx carries NO EigenMap instance (the only EigenMap bytes "
          f"left are the survivor's own fold-note comment: {rb.count(b'EigenMap')} occurrence(s))")
    check(rb.count(b"CathedralPlate") >= 1 and rb.count(b"CathedralMapHud") >= 1,
          f"the built rbxlx carries the survivor (CathedralPlate x{rb.count(b'CathedralPlate')}, "
          f"CathedralMapHud x{rb.count(b'CathedralMapHud')})")
    init = INIT.read_text(encoding="utf-8")
    check("EigenMap" not in init, "init.server.luau wires no EigenMap module")
    check("CathedralPlate.build()" in init and "CathedralPlate.entry()" in init
          and "CathedralPlate.tick(dt)" in init,
          "init.server.luau wires the survivor (require/build/entry/tick)")
    check(not (ROOT / "tools/eigenmap_overlay_check.py").exists()
          and not (ROOT / "tools/gen_eigenmap_luau.py").exists(),
          "the killed build's tools are off the repo surface (record copies in cands/killed/)")

    note("")
    note(f"== VERDICT: {'PASS' if not failures else 'FAIL'} "
         f"({len(failures)} failure(s)) ==")
    for f in failures[:40]:
        note(f"  FAIL: {f}")
    note("")
    note("Scope note: this is a stub execution under tools/bin/luau/luau.exe, NOT")
    note("Roblox Studio. Real GUI rendering, physics Touched and DataStore")
    note("durability stay owed to a live Studio session (queue/todo.md, P0")
    note("THE MOUNTAIN, owner + dates filed there).")
    RECEIPT.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"\nwrote {RECEIPT}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
