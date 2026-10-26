"""eigenmap_judge -- the judge's own position/distance/bearing sanity check
for card eigenmap (ractor panel 2026-09-26), candidates eigenmap-one and
eigenmap-two.

The kill condition: "the overlay fails a position/distance/bearing sanity
check the judge runs on the data, or the build touches nothing under roblox/".

This script is independent of both candidates' own checkers:
  1. recomputes every number from watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json
     in Python under the estate's own bearing law (tools/cathedral_eigen_map.py:45-47,
     atan2(dx, -dy), 0 = north = eigen -y, clockwise);
  2. executes the REAL shipped shared modules under tools/bin/luau/luau.exe
     (drivers eigenmap_judge_one.luau / eigenmap_judge_two.luau) and diffs;
  3. replicates each HUD's minimap projection formula EXACTLY as read in the
     shipped client bytes and checks the RENDERED direction of every directed
     region pair against the module's own bearing for that pair (the overlay
     position-vs-bearing coherence check);
  4. checks each candidate's world transform (beacon plate) preserves distance
     (studs = eigen * scale) and bearing (0 = north = world -Z);
  5. verifies the data block in each module equals the scan JSON (centroids,
     class, cos, hops from water, chain/vote where claimed);
  6. verifies the 0927 == 0926 centroid identity claim and the sha256 stamp;
  7. records which files each build touched under roblox/ (git status);
  8. runs both candidates' own checkers for the record (evidence only).

Run: .venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/checks/eigenmap_judge.py
Raw stdout of this run is the judge receipt eigenmap.judge.txt.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CHECKS = ROOT / "watch" / "inbox" / "ractor_panel_20260926" / "checks"
SCAN = ROOT / "watch" / "inbox" / "CATHEDRAL_CURVATURE_SCAN_20260927.json"
SCAN_0926 = ROOT / "watch" / "inbox" / "CATHEDRAL_CURVATURE_SCAN_20260926.json"
LUAU = ROOT / "tools" / "bin" / "luau" / "luau.exe"

fails: list[str] = []
passes = 0


def ok(cond: bool, label: str) -> bool:
    global passes
    if cond:
        passes += 1
        print(f"[PASS] {label}")
    else:
        fails.append(label)
        print(f"[FAIL] {label}")
    return cond


def bearing_law(ax: float, ay: float, bx: float, by: float) -> float:
    """The estate bearing law (tools/cathedral_eigen_map.py:45-47):
    0 = north = eigen -y, clockwise: degrees(atan2(dx, -dy)) mod 360."""
    return (math.degrees(math.atan2(bx - ax, -(by - ay)))) % 360.0


def main() -> int:
    print("== judge sanity check: card eigenmap, candidates eigenmap-one / eigenmap-two ==")
    scan_bytes = SCAN.read_bytes()
    scan = json.loads(scan_bytes)
    sha = hashlib.sha256(scan_bytes).hexdigest()
    cents: dict[str, tuple[float, float]] = {
        k: (v[0], v[1]) for k, v in scan["eigen_centroids"].items()
    }
    regions = sorted(cents)
    hops = scan["first_form_geodesics_from_water"]
    print(f"scan {SCAN.name} ts {scan['ts']} sha256 {sha}")
    print(f"regions {len(regions)}: {', '.join(regions)}")

    # ---- 1. scan identity claims ----
    mod_one = (ROOT / "roblox" / "src" / "shared" / "EigenMap.luau").read_text(encoding="utf-8")
    m = re.search(r"scan sha256: ([0-9a-f]{64})", mod_one)
    ok(m is not None, "EigenMap.luau carries a scan sha256 stamp")
    if m:
        ok(m.group(1) == sha, f"EigenMap.luau sha256 stamp == sha256 of the 0927 scan bytes ({sha[:12]}...)")
    scan26 = json.loads(SCAN_0926.read_text(encoding="utf-8"))
    same = {k: tuple(v) for k, v in scan26["eigen_centroids"].items()} == {
        k: tuple(v) for k, v in scan["eigen_centroids"].items()
    }
    ok(same, "claim check: 0927 eigen_centroids identical to 0926 (the freshest-data anchor both candidates filed)")

    # ---- 2. Python reference from the JSON ----
    ref: dict[tuple[str, str], tuple[float, float]] = {}
    for a, b in itertools.combinations(regions, 2):
        d = math.dist(cents[a], cents[b])
        brg = bearing_law(*cents[a], *cents[b])
        ref[(a, b)] = (d, brg)
        print(f"  ref {a} -> {b}: dist {d:.6f} brg {brg:.1f}")

    # ---- 3. execute the REAL modules under the luau CLI ----
    # The luau CLI cannot require through ../../.. (verified live: it errors
    # "could not resolve child component roblox"), so we stage byte-identical
    # copies of the TREE modules into a temp dir, sha256-verified before and
    # after, and rewrite only the driver's require line to "./<Module>".
    import tempfile

    def stage_and_run(driver: str, module_rel: str, module_name: str) -> tuple[int, str, str]:
        mod_path = ROOT / module_rel
        tree_sha = hashlib.sha256(mod_path.read_bytes()).hexdigest()
        src = (CHECKS / driver).read_text(encoding="utf-8")
        src = re.sub(r'require\("[^"]*' + module_name + r'"\)', f'require("./{module_name}")', src, count=1)
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            (tdp / (module_name + ".luau")).write_bytes(mod_path.read_bytes())
            (tdp / "main.luau").write_text(src, encoding="utf-8", newline="")
            staged_sha = hashlib.sha256((tdp / (module_name + ".luau")).read_bytes()).hexdigest()
            assert staged_sha == tree_sha, f"staged copy sha mismatch for {module_name}"
            p = subprocess.run([str(LUAU), str(tdp / "main.luau")], capture_output=True, text=True)
            return p.returncode, p.stdout + p.stderr, tree_sha

    rc1, out1, sha_one = stage_and_run("eigenmap_judge_one.luau", "roblox/src/shared/EigenMap.luau", "EigenMap")
    print(f"-- luau exit one: {rc1}; module tree sha256 {sha_one} (staged copy verified identical)")
    print(out1.rstrip())
    rc2, out2, sha_two = stage_and_run("eigenmap_judge_two.luau", "roblox/src/shared/CathedralMap.luau", "CathedralMap")
    print(f"-- luau exit two: {rc2}; module tree sha256 {sha_two} (staged copy verified identical)")
    print(out2.rstrip())

    ok(rc1 == 0, "candidate ONE: real module EigenMap.luau runs to completion under the plain luau CLI")
    ok(rc2 == 0, "candidate TWO: real module CathedralMap.luau runs to completion under the plain luau CLI")

    # ---- 4. candidate ONE: data + math vs the JSON ----
    print("== candidate ONE (EigenMap) vs JSON ==")
    rows1: dict[str, tuple[float, float, str, str | None, int]] = {}
    for line in out1.splitlines():
        f = line.split()
        if f and f[0] == "region":
            rows1[f[1]] = (float(f[2]), float(f[3]), f[4], None if f[5] == "nil" else float(f[5]), int(f[6]))
    for r in regions:
        got = rows1.get(r)
        exp = cents[r]
        if got is None:
            ok(False, f"ONE region {r}: MISSING from module output")
            continue
        g0, g1, g2, g3, g4 = got
        ok(abs(g0 - exp[0]) < 1e-12 and abs(g1 - exp[1]) < 1e-12,
           f"ONE region {r}: centroid ({g0},{g1}) == JSON {exp}")
        ok(g2 == scan["regions"][r]["class"], f"ONE region {r}: class {g2} == JSON")
        jc = scan["regions"][r]["cos"]
        ok((jc is None and g3 is None) or (jc is not None and g3 == jc),
           f"ONE region {r}: cos {g3} == JSON {jc}")
        ok(g4 == hops[r], f"ONE region {r}: hops {g4} == JSON {hops[r]}")

    pairs1: dict[tuple[str, str], tuple[float, float]] = {}
    for line in out1.splitlines():
        f = line.split()
        if f and f[0] == "pair":
            pairs1[(f[1], f[2])] = (float(f[3]), float(f[4]))
    ok(len(rows1) == 5, f"ONE module reports all 5 regions (got {len(rows1)})")
    ok(len(pairs1) == 10, f"ONE module reports all 10 pairs (got {len(pairs1)})")
    worst_d = worst_b = 0.0
    for (a, b), (d_exp, b_exp) in ref.items():
        got = pairs1.get((a, b))
        if got is None:
            ok(False, f"ONE pair {a}->{b} missing from module output")
            continue
        worst_d = max(worst_d, abs(got[0] - d_exp))
        worst_b = max(worst_b, abs(got[1] - b_exp))
    ok(len(pairs1) == 10 and worst_d < 1e-9 and worst_b < 1e-6,
       f"ONE module math: 10/10 pairs distEigen/bearingEigen == Python recompute (worst |ddist| {worst_d:.2e}, |dbearing| {worst_b:.2e} deg)")

    probe_bad = probe_n = 0
    for line in out1.splitlines():
        f = line.split()
        if f and f[0] == "probe":
            probe_n += 1
            a, b, d, brg = f[1], f[2], float(f[3]), float(f[4])
            ax, ay = cents[a]
            d_exp = math.dist((ax, ay), cents[b])
            b_exp = bearing_law(ax, ay, *cents[b])
            if abs(d - d_exp) > 1e-9 or abs(brg - b_exp) > 1e-6:
                probe_bad += 1
    ok(probe_n == 25 and probe_bad == 0,
       f"ONE walker readout: 25/25 standing-on-beacon dist/bearing rows (5 regions x 5 targets) == pair data (rows {probe_n}, bad {probe_bad})")

    nearest_bad = nearest_n = 0
    for line in out1.splitlines():
        f = line.split()
        if f and f[0] == "nearest":
            nearest_n += 1
            if f[2] != f[1] or abs(float(f[3])) > 1e-12:
                nearest_bad += 1
    ok(nearest_n == 5 and nearest_bad == 0,
       f"ONE nearest-at-beacon returns itself at dist 0 (rows {nearest_n}, bad {nearest_bad})")

    # world transform (one): studs invariant + bearing preserved + roundtrip
    world1: dict[str, tuple[float, float]] = {}
    rt_bad = 0.0
    for line in out1.splitlines():
        f = line.split()
        if f and f[0] == "world":
            world1[f[1]] = (float(f[2]), float(f[3]))
            rt_bad = max(rt_bad, abs(float(f[4]) - cents[f[1]][0]), abs(float(f[5]) - cents[f[1]][1]))
    ok(len(world1) == 5 and rt_bad < 1e-12,
       f"ONE worldFromEigen/eigenFromWorld roundtrip exact (rows {len(world1)}, worst {rt_bad:.2e})")
    spu = 20000.0
    wbad_d = wbad_b = 0.0
    for (a, b), (d_exp, b_exp) in ref.items():
        (ax, az), (bx, bz) = world1[a], world1[b]
        wd = math.dist((ax, az), (bx, bz))
        wb = (math.degrees(math.atan2(bx - ax, -(bz - az)))) % 360.0
        wbad_d = max(wbad_d, abs(wd - d_exp * spu))
        wbad_b = max(wbad_b, min(abs(wb - b_exp), 360 - abs(wb - b_exp)))
    ok(wbad_d < 1e-6 and wbad_b < 1e-6,
       f"ONE world plate: studs == eigen*{spu:.0f} and world bearing (0=N=-Z) == eigen bearing for all 10 pairs (worst {wbad_d:.2e} st, {wbad_b:.2e} deg)")

    # ---- 5. candidate TWO: data + math vs the JSON ----
    print("== candidate TWO (CathedralMap) vs JSON ==")
    rows2: dict[str, tuple[float, float, str, str | None]] = {}
    for line in out2.splitlines():
        f = line.split()
        if f and f[0] == "region":
            rows2[f[1]] = (float(f[2]), float(f[3]), f[4], None if f[5] == "nil" else float(f[5]))
    for r in regions:
        got = rows2.get(r)
        exp = cents[r]
        if got is None:
            ok(False, f"TWO region {r}: MISSING from module output")
            continue
        g0, g1, g2, g3 = got
        ok(abs(g0 - exp[0]) < 1e-12 and abs(g1 - exp[1]) < 1e-12,
           f"TWO region {r}: centroid ({g0},{g1}) == JSON {exp}")
        ok(g2 == scan["regions"][r]["class"], f"TWO region {r}: class {g2} == JSON")
        jc = scan["regions"][r]["cos"]
        ok((jc is None and g3 is None) or (jc is not None and g3 == jc),
           f"TWO region {r}: cos {g3} == JSON {jc}")

    pairs2: dict[tuple[str, str], tuple[float, float, float]] = {}
    for line in out2.splitlines():
        f = line.split()
        if f and f[0] == "pair":
            pairs2[(f[1], f[2])] = (float(f[3]), float(f[4]), float(f[5]))
    ok(len(rows2) == 5, f"TWO module reports all 5 regions (got {len(rows2)})")
    ok(len(pairs2) == 10, f"TWO module reports all 10 pairs (got {len(pairs2)})")
    bad2 = 0
    for (a, b), (d_exp, b_exp) in ref.items():
        got = pairs2.get((a, b))
        if got is None:
            ok(False, f"TWO pair {a}->{b} missing from module output")
            continue
        back_exp = bearing_law(*cents[b], *cents[a])
        if abs(got[0] - round(d_exp, 4)) > 1e-9 or abs(got[1] - round(b_exp, 1)) > 1e-9 or abs(got[2] - round(back_exp, 1)) > 1e-9:
            bad2 += 1
    ok(len(pairs2) == 10 and bad2 == 0,
       f"TWO module math: 10/10 pairs dist(4dp)+bearing(1dp)+back-bearing == Python recompute (bad {bad2})")

    vote = scan["descent_vote"]
    vm = re.search(r"vote ([\d.]+) ([\d.]+) (\S+)", out2)
    if vm is None:
        ok(False, "TWO vote arithmetic: vote row missing from module output")
    else:
        ok(abs(float(vm.group(1)) - vote["water_first_chain_len"]) < 5e-4
           and abs(float(vm.group(2)) - vote["hub_first_star_len"]) < 5e-4,
           f"TWO vote arithmetic: chain {vm.group(1)} / star {vm.group(2)} reproduce the scan's {vote['water_first_chain_len']} / {vote['hub_first_star_len']} at 3dp")

    wcx, wcy = cents["water_computer"]
    acx, acy = cents["audit_dungeon"]
    mx, my = (wcx + acx) / 2, (wcy + acy) / 2
    d_mid = math.dist((mx, my), cents["water_computer"])
    d_mid_a = math.dist((mx, my), cents["audit_dungeon"])
    tie_ok = abs(d_mid - d_mid_a) < 1e-12
    pm = re.search(r"probe_mid (\S+) (\S+) (\S+) ([\d.]+) ([\d.]+)", out2)
    if pm is None:
        ok(False, "TWO midpoint probe: probe row missing from module output")
    else:
        ok(pm.group(3) == "audit_dungeon" and abs(float(pm.group(4)) - round(d_mid, 4)) < 1e-9,
           f"TWO midpoint probe: exact tie {d_mid:.4f} broken to audit_dungeon (alphabetical), module agrees ({pm.group(3)} {pm.group(4)}) [tie is exact: {tie_ok}]")
    pbad = 0
    for line in out2.splitlines():
        f = line.split()
        if f and f[0] == "probe_on":
            if f[4] != f[1] or abs(float(f[2])) > 1e-9:
                pbad += 1
    ok(pbad == 0, f"TWO on-beacon probes: nearest == self at 0.0000 (bad {pbad})")

    # world transform (two): replicate toWorld from the constants the module printed
    sc = re.search(r"scale (\d+)", out2)
    og = re.search(r"origin (-?\d+) (-?\d+) (-?\d+)", out2)
    ok(sc is not None and og is not None, "TWO module prints SCALE/ORIGIN constants")
    if sc and og:
        S = float(sc.group(1))
        ox, oz = float(og.group(1)), float(og.group(3))
        w2 = {r: (ox + c[0] * S, oz + c[1] * S) for r, c in cents.items()}
        wbad_d2 = wbad_b2 = 0.0
        for (a, b), (d_exp, b_exp) in ref.items():
            (ax, az), (bx, bz) = w2[a], w2[b]
            wd = math.dist((ax, az), (bx, bz))
            wb = (math.degrees(math.atan2(bx - ax, -(bz - az)))) % 360.0
            wbad_d2 = max(wbad_d2, abs(wd - d_exp * S))
            wbad_b2 = max(wbad_b2, min(abs(wb - b_exp), 360 - abs(wb - b_exp)))
        ok(wbad_d2 < 1e-9 and wbad_b2 < 1e-9,
           f"TWO world plate: studs == eigen*{S:.0f} and world bearing (0=N=-Z) == eigen bearing for all 10 pairs (worst {wbad_d2:.2e} st, {wbad_b2:.2e} deg)")
        plate_x = [ox + c[0] * S for c in cents.values()]
        plate_z = [oz + c[1] * S for c in cents.values()]
        print(f"  TWO plate extent X {min(plate_x):.1f}..{max(plate_x):.1f} Z {min(plate_z):.1f}..{max(plate_z):.1f}")

    # ---- 6. overlay RENDER coherence: minimap direction vs bearing law ----
    # Formula replicated exactly from the shipped client bytes:
    # ONE  roblox/src/client/EigenMapHud.client.luau:103-111
    #      margin 0.14; screenY(ey) = (py1 - ey) / (py1 - py0)  [UDim2 scale: 0 = top]
    # TWO  roblox/src/client/CathedralMapHud.client.luau:98-120
    #      margin 0.13; py(ey) = offY + (ey - y0) * scale  [pixel offset: grows DOWN]
    print("== overlay render coherence (drawn direction vs the module's own bearing) ==")
    exs = [c[0] for c in cents.values()]
    eys = [c[1] for c in cents.values()]

    def render_angle_one(a: str, b: str) -> float:
        spanX, spanY = max(exs) - min(exs), max(eys) - min(eys)
        px0, px1 = min(exs) - spanX * 0.14, max(exs) + spanX * 0.14
        py0, py1 = min(eys) - spanY * 0.14, max(eys) + spanY * 0.14
        sxa = (cents[a][0] - px0) / (px1 - px0)
        sxb = (cents[b][0] - px0) / (px1 - px0)
        sya = (py1 - cents[a][1]) / (py1 - py0)
        syb = (py1 - cents[b][1]) / (py1 - py0)
        return (math.degrees(math.atan2(sxb - sxa, -(syb - sya)))) % 360.0

    def render_angle_two(a: str, b: str) -> float:
        # px/py are affine with positive scale; constants cancel in the direction
        return (math.degrees(math.atan2(cents[b][0] - cents[a][0], -(cents[b][1] - cents[a][1])))) % 360.0

    for cand, angle_fn, pairs_src in (("ONE", render_angle_one, pairs1), ("TWO", render_angle_two, pairs2)):
        worst = 0.0
        n = 0
        over = 0
        for a, b in itertools.permutations(regions, 2):
            if (a, b) in pairs_src:
                brg = pairs_src[(a, b)][1]
            elif (b, a) in pairs_src:
                brg = (pairs_src[(b, a)][1] + 180.0) % 360.0
            else:
                continue
            ra = angle_fn(a, b)
            delta = min(abs(ra - brg), 360 - abs(ra - brg))
            worst = max(worst, delta)
            if delta > 0.5:
                over += 1
            n += 1
        ok(n == 20 and over == 0,
           f"{cand} overlay render: {n}/20 directed pairs drawn in the direction the module's bearing reports "
           f"({over} pairs deviate > 0.5 deg; worst deviation {worst:.1f} deg)")

    # the concrete walker case, for the record
    fm, wc = cents["fractal_maze"], cents["water_computer"]
    north_is = "water_computer is NORTH of fractal_maze" if wc[1] < fm[1] else "fractal_maze is NORTH of water_computer"
    print(f"  walker case: {north_is} (ey {wc[1]} vs {fm[1]}); bearing fractal_maze->water_computer "
          f"{bearing_law(*fm, *wc):.1f} deg means water_computer must render ABOVE (smaller screen-Y than) fractal_maze on a north-up map")
    print(f"  ONE toScale screen-Y: water {render_angle_one('fractal_maze', 'water_computer'):.1f} deg drawn vs "
          f"{bearing_law(*fm, *wc):.1f} deg reported; TWO: {render_angle_two('fractal_maze', 'water_computer'):.1f} deg drawn")

    # ---- 7. build touched roblox/ ----
    print("== roblox/ touch ==")
    for cand, files in (
        ("ONE", ["roblox/src/shared/EigenMap.luau", "roblox/src/server/EigenMapZone.luau",
                 "roblox/src/client/EigenMapHud.client.luau", "roblox/src/server/init.server.luau",
                 "roblox/README.md", "roblox/the_mountain.rbxlx"]),
        ("TWO", ["roblox/src/shared/CathedralMap.luau", "roblox/src/server/CathedralPlate.luau",
                 "roblox/src/client/CathedralMapHud.client.luau", "roblox/src/server/init.server.luau",
                 "roblox/README.md", "roblox/the_mountain.rbxlx"]),
    ):
        missing = [f for f in files if not (ROOT / f).exists()]
        ok(not missing, f"{cand} build present under roblox/ (missing: {missing or 'none'})")
    rb = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "roblox"],
                        capture_output=True, text=True).stdout
    print("git status --porcelain -- roblox:")
    print(rb.rstrip())

    # ---- 8. the candidates' own checkers, for the record ----
    print("== candidates' own checkers (evidence only) ==")
    for label, cmd, cwd in (
        ("ONE overlay check", [str(ROOT / ".venv" / "Scripts" / "python.exe"), str(ROOT / "tools" / "eigenmap_overlay_check.py")], ROOT),
        ("TWO check", [str(ROOT / ".venv" / "Scripts" / "python.exe"),
                       str(ROOT / "watch" / "inbox" / "ractor_panel_20260926" / "cands" / "eigenmap-two-check.py")], ROOT),
    ):
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd))
        tail = (p.stdout or p.stderr).strip().splitlines()[-3:]
        print(f"{label}: exit {p.returncode}; tail: {' | '.join(tail)}")

    # ---- verdict ----
    print(f"== judge tally: {passes} PASS, {len(fails)} FAIL ==")
    for f in fails:
        print(f"  FAIL: {f}")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
