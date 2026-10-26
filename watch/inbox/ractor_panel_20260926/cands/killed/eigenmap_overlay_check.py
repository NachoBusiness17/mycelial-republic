"""eigenmap_overlay_check - verify the in-game eigen-map overlay against the
scan data it claims to render.

The kill condition for the eigenmap card is an overlay that fails a
position/distance/bearing sanity check against the data. This tool IS that
check, runnable headless:

1. Trace: the GENERATED block in roblox/src/shared/EigenMap.luau names its
   source scan file and its sha256. The tool recomputes the sha over the
   actual file bytes and refuses a mismatch (stale block = FAIL, not WARN).
2. Data: every region row in the Luau block must equal the JSON's
   eigen_centroids, curvature class, cos and hops, exactly.
3. Math: the tool generates a Luau harness that requires the REAL module
   under the plain Luau interpreter (tools/bin/luau/luau.exe) and prints its
   actual distEigen/bearingEigen/distFromEigen/bearingFromEigen/nearestEigen/
   worldFromEigen/eigenFromWorld outputs; the tool recomputes the same
   quantities in Python from the JSON and diffs.
4. Overlay invariants: standing on any beacon (the walker case), the readout
   for every other region equals the pair's data distance and bearing; world
   distances equal eigen distances x STUDS_PER_UNIT; the eigen<->world map
   round-trips.

Usage: .venv/Scripts/python.exe tools/eigenmap_overlay_check.py
Exit 0 = PASS, 1 = FAIL (with the failing row printed).

[RECORD COPY 2026-09-27] This is a byte-preserved record copy of
tools/eigenmap_overlay_check.py, the falsifier of ractor candidate
eigenmap-one (card eigenmap, panel 2026-09-26). The judge killed eigenmap-one
on the mirrored minimap (its drawn map is 180-deg rotated against its own
bearing law); the build was pruned from the repo tree by the revise-eigenmap
pass and its bytes moved here. The original tree path is cited in
cands/eigenmap-one.md. This copy is NOT maintained: its ROOT is
parents[1], which resolved against tools/, and the module it reads
(roblox/src/shared/EigenMap.luau) now lives beside it in this folder; running
it as-is will not resolve. The surviving build's falsifier is
tools/eigenmap_two_check.py.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "roblox" / "src" / "shared" / "EigenMap.luau"
LUAU = ROOT / "tools" / "bin" / "luau" / "luau.exe"
HARNESS = ROOT / ".eigenmap_check_harness.tmp.luau"

TOL_DIST = 1e-9      # eigen units
TOL_BEARING = 1e-7   # degrees
TOL_WORLD = 1e-6     # studs


def bearing(ax: float, ay: float, bx: float, by: float) -> float:
    return (math.degrees(math.atan2(bx - ax, -(by - ay))) + 360.0) % 360.0


def parse_block() -> dict:
    text = MODULE.read_text(encoding="utf-8")
    m = re.search(
        r"-- BEGIN GENERATED.*?-- END GENERATED", text, re.S)
    if not m:
        raise SystemExit("GENERATED block not found in EigenMap.luau")
    block = m.group(0)
    out: dict = {"rows": [], "chain": []}
    src = re.search(r"^-- source: (.+)$", block, re.M)
    sha = re.search(r"^-- scan sha256: ([0-9a-f]{64})$", block, re.M)
    if not src or not sha:
        raise SystemExit("block is missing its source/sha256 trace lines")
    out["source"] = src.group(1).strip()
    out["sha"] = sha.group(1)
    for name, ex, ey, cls, cos, hops in re.findall(
        r'\{ name = "(\w+)", ex = (-?[\d.e+-]+), ey = (-?[\d.e+-]+), '
        r'class = "(\w+)"(?:, cos = (-?[\d.e+-]+))?, hops = (-?\d+) \}', block):
        out["rows"].append({
            "name": name, "ex": float(ex), "ey": float(ey), "class": cls,
            "cos": None if not cos else float(cos), "hops": int(hops)})
    for a, b, kind in re.findall(
        r'\{ a = "(\w+)", b = "(\w+)", kind = "(\w+)"', block):
        out["chain"].append({"a": a, "b": b, "kind": kind})
    spu = re.search(r"EigenMap\.STUDS_PER_UNIT = (\d+)", text)
    plx = re.search(r"EigenMap\.PLAZA_X = (-?\d+)", text)
    plz = re.search(r"EigenMap\.PLAZA_Z = (-?\d+)", text)
    if not (spu and plx and plz):
        raise SystemExit("transform constants not found in EigenMap.luau")
    out["studs_per_unit"] = int(spu.group(1))
    out["plaza_x"] = int(plx.group(1))
    out["plaza_z"] = int(plz.group(1))
    return out


def run_luau(block: dict) -> dict:
    rel = MODULE.relative_to(ROOT).with_suffix("").as_posix()  # luau require takes no .luau
    harness = '''local M = require("./__REL__")
print("STUDS", M.STUDS_PER_UNIT, M.PLAZA_X, M.PLAZA_Z)
print("SCAN", M.scanStamp())
for _, r in ipairs(M.regions()) do
  print("REGION", r.name, r.ex, r.ey, r.class, tostring(r.cos), r.hops)
end
local names = {}
for _, r in ipairs(M.regions()) do table.insert(names, r.name) end
for _, a in ipairs(names) do
  for _, b in ipairs(names) do
    if a < b then
      print("PAIR", a, b, M.distEigen(a, b), M.bearingEigen(a, b), M.bearingEigen(b, a))
    end
  end
end
for _, at in ipairs(names) do
  local ra = M.region(at)
  local wx, wz = M.worldFromEigen(ra.ex, ra.ey)
  print("WORLD", at, wx, wz)
  for _, to in ipairs(names) do
    if at ~= to then
      print("FROM", at, to, M.distFromEigen(to, ra.ex, ra.ey), M.bearingFromEigen(to, ra.ex, ra.ey))
    end
  end
  local n, d = M.nearestEigen(ra.ex, ra.ey)
  print("NEAR", at, n, d)
end
for _, seg in ipairs(M.chain()) do
  print("SEG", seg.a, seg.b, seg.kind)
end
print("OFFMAP", table.concat(M.offMap(), ","))
print("BETA0", M.beta0())
for _, p in ipairs({ {M.PLAZA_X + 13.5, M.PLAZA_Z - 81.0}, {400, 900}, {0, 0} }) do
  local ex, ey = M.eigenFromWorld(p[1], p[2])
  local wx, wz = M.worldFromEigen(ex, ey)
  print("ROUNDTRIP", p[1], p[2], ex, ey, wx, wz)
end
'''.replace("__REL__", rel)
    HARNESS.write_text(harness, encoding="utf-8", newline="\n")
    try:
        proc = subprocess.run([str(LUAU), HARNESS.name], cwd=str(ROOT),
                              capture_output=True, text=True, timeout=60)
    finally:
        HARNESS.unlink(missing_ok=True)
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(f"luau harness failed: exit {proc.returncode}")
    out: dict = {"regions": {}, "pair": {}, "from": {}, "world": {},
                 "near": {}, "seg": [], "roundtrip": []}
    for line in proc.stdout.splitlines():
        f = line.split("\t")
        if f[0] == "STUDS":
            out["studs"] = (float(f[1]), float(f[2]), float(f[3]))
        elif f[0] == "REGION":
            out["regions"][f[1]] = (float(f[2]), float(f[3]), f[4],
                                    None if f[5] == "nil" else float(f[5]), int(f[6]))
        elif f[0] == "PAIR":
            out["pair"][(f[1], f[2])] = (float(f[3]), float(f[4]), float(f[5]))
        elif f[0] == "FROM":
            out["from"][(f[1], f[2])] = (float(f[3]), float(f[4]))
        elif f[0] == "WORLD":
            out["world"][f[1]] = (float(f[2]), float(f[3]))
        elif f[0] == "NEAR":
            out["near"][f[1]] = (f[2], float(f[3]))
        elif f[0] == "SEG":
            out["seg"].append((f[1], f[2], f[3]))
        elif f[0] == "OFFMAP":
            out["offmap"] = [s for s in f[1].split(",") if s]
        elif f[0] == "BETA0":
            out["beta0"] = (float(f[1]), float(f[2]))
        elif f[0] == "ROUNDTRIP":
            out["roundtrip"].append(tuple(float(x) for x in f[1:]))
        elif f[0] == "SCAN":
            out["scan"] = (f[1], f[2])
    return out


def main() -> int:
    fails: list[str] = []
    block = parse_block()
    scan_path = ROOT / "watch" / "inbox" / Path(block["source"]).name
    raw = scan_path.read_bytes()
    import hashlib
    sha = hashlib.sha256(raw).hexdigest()
    scan = json.loads(raw.decode("utf-8"))
    cents = scan["eigen_centroids"]
    regions = scan.get("regions", {})
    hops = scan.get("first_form_geodesics_from_water", {})

    print(f"module: {MODULE.relative_to(ROOT)}")
    print(f"source: {block['source']}")
    print(f"scan sha256: {'MATCH' if sha == block['sha'] else 'MISMATCH'}"
          f" ({sha[:16]}...)")
    if sha != block["sha"]:
        fails.append("block sha256 does not match the scan file it names")

    # data equality: every block row == JSON row
    rows = {r["name"]: r for r in block["rows"]}
    if set(rows) != set(cents):
        fails.append(f"region sets differ: block {sorted(rows)} vs json {sorted(cents)}")
    for name, (ex, ey) in cents.items():
        r = rows.get(name)
        if not r:
            continue
        if abs(r["ex"] - ex) > 0 or abs(r["ey"] - ey) > 0:
            fails.append(f"{name}: centroid {r['ex']},{r['ey']} != json {ex},{ey}")
        jc = regions.get(name, {})
        if r["class"] != jc.get("class"):
            fails.append(f"{name}: class {r['class']} != {jc.get('class')}")
        jcos = jc.get("cos")
        if (r["cos"] is None) != (jcos is None) or (
                jcos is not None and abs((r["cos"] or 0) - jcos) > 0):
            fails.append(f"{name}: cos {r['cos']} != {jcos}")
        if r["hops"] != hops.get(name):
            fails.append(f"{name}: hops {r['hops']} != {hops.get(name)}")
    print(f"data rows: {len(rows)} regions checked against json")

    # run the real module math under luau
    lu = run_luau(block)
    studs = lu["studs"][0]
    if studs != block["studs_per_unit"]:
        fails.append(f"STUDS_PER_UNIT runtime {studs} != text {block['studs_per_unit']}")
    for name, (ex, ey, cls, cos, h) in lu["regions"].items():
        r = rows.get(name)
        if r and (abs(r["ex"] - ex) > 0 or abs(r["ey"] - ey) > 0
                  or r["class"] != cls or r["hops"] != h):
            fails.append(f"{name}: luau runtime row != block row")

    # pairwise dist/bearing: luau module vs python reference from the json
    names = sorted(cents)
    print("\npair     dist_eigen (luau vs python)         bearing deg (luau vs python)")
    worst_d = worst_b = 0.0
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ld, lb, lb_rev = lu["pair"][(a, b)]
            pd = math.dist(cents[a], cents[b])
            pb = bearing(*cents[a], *cents[b])
            pbr = bearing(*cents[b], *cents[a])
            worst_d = max(worst_d, abs(ld - pd))
            worst_b = max(worst_b, abs(lb - pb), abs(lb_rev - pbr))
            flag = "" if (abs(ld - pd) <= TOL_DIST and abs(lb - pb) <= TOL_BEARING
                          and abs(lb_rev - pbr) <= TOL_BEARING) else "  <-- FAIL"
            print(f"{a:16s} {b:16s} {ld:.6f} vs {pd:.6f}   "
                  f"{lb:7.1f}/{lb_rev:7.1f} vs {pb:7.1f}/{pbr:7.1f}{flag}")
            if flag:
                fails.append(f"pair {a}->{b}: luau ({ld}, {lb}) != python ({pd}, {pb})")
    print(f"worst |ddist| {worst_d:.2e} eigen, worst |dbearing| {worst_b:.2e} deg")

    # walker case: standing on beacon `at`, readout to `to` == pair data
    for (at, to), (ld, lb) in lu["from"].items():
        pd = math.dist(cents[at], cents[to])
        pb = bearing(*cents[at], *cents[to])
        if abs(ld - pd) > TOL_DIST or abs(lb - pb) > TOL_BEARING:
            fails.append(f"overlay-at {at} -> {to}: ({ld}, {lb}) != data ({pd}, {pb})")
    print(f"walker rows: {len(lu['from'])} standing-on-beacon readouts checked")

    # nearest: at any beacon, nearest is itself at 0
    for name, (n, d) in lu["near"].items():
        if n != name or abs(d) > 1e-12:
            fails.append(f"nearest at {name}: ({n}, {d}) != ({name}, 0)")

    # world transform: |wa - wb| == dist_eigen * STUDS_PER_UNIT
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ax, az = lu["world"][a]
            bx, bz = lu["world"][b]
            wdist = math.hypot(bx - ax, bz - az)
            expect = lu["pair"][(a, b)][0] * studs
            if abs(wdist - expect) > TOL_WORLD:
                fails.append(f"studs invariant {a}->{b}: {wdist:.4f} != {expect:.4f}")

    # roundtrip
    for wx, wz, ex, ey, wx2, wz2 in lu["roundtrip"]:
        if abs(wx - wx2) > 1e-9 or abs(wz - wz2) > 1e-9:
            fails.append(f"roundtrip world ({wx},{wz}) -> ({wx2},{wz2})")

    print(f"\nchain segs (luau): {lu['seg']}")
    print(f"off-map (luau): {lu['offmap']} · beta0 {lu['beta0']}")
    print(f"roundtrips: {len(lu['roundtrip'])} world->eigen->world exact")

    if fails:
        print("\nFAIL:")
        for f in fails:
            print(" -", f)
        return 1
    print("\nPASS: overlay data + position/distance/bearing match the scan json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
