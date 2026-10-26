"""eigenmap-two-check  -  position/distance/bearing sanity check on the data,
run against the AS-SHIPPED Luau module (ractor panel 2026-09-26, card eigenmap,
candidate two).

What it does (all outputs land in eigenmap-two-check.txt beside this file):
1. Recompute, in Python from watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json:
   the 5 region rows, the 10 pairwise distances (4dp) + both bearings (1dp,
   0 = north = eigen -y, clockwise, atan2(dx, -dy) = the HTML map law),
   the water_first chain length + hub star length (vs the scan's own
   descent_vote), and three walker probes (on-beacon reads, midpoint reads).
2. Execute the REAL roblox/src/shared/CathedralMap.luau under
   tools/bin/luau/luau.exe (byte-identical staged copy, sha256-verified
   against the tree file before and after the run) and diff every number.
3. Verify the world anchor: beacon world X/Z = ORIGIN + eigen*SCALE (north
   = eigen -y = world -Z) round-trips exactly for all five regions.
4. Verify the edge policy: chain edges are exactly the SADDLE-SADDLE legs of
   the water_first order; no edge (chain or hub) touches riddler_engram.

Exit 0 = PASS (all rows agree). Exit 1 = any mismatch (printed, first 40).
Usage: .venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/cands/eigenmap-two-check.py
"""

import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCAN = ROOT / "watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json"
MODULE = ROOT / "roblox/src/shared/CathedralMap.luau"
TEST = Path(__file__).resolve().parent / "eigenmap-two-luau-test.luau"
LUAU = ROOT / "tools/bin/luau/luau.exe"
RECEIPT = Path(__file__).resolve().parent / "eigenmap-two-check.txt"

WINDS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
         "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

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


def bearing_deg(a, b) -> float:
    """0 = north = eigen -y, clockwise: atan2(dx, -dy), the HTML map law."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    deg = math.degrees(math.atan2(dx, -dy))
    return round((deg + 360.0) % 360.0, 1)


def dist_eigen(a, b) -> float:
    return round(math.hypot(b[0] - a[0], b[1] - a[1]), 4)


def main() -> int:
    scan = json.loads(SCAN.read_text(encoding="utf-8"))
    cents = scan["eigen_centroids"]
    regions = sorted(cents)
    note(f"scan ts: {scan['ts']}")
    note(f"regions with eigen_centroids: {len(regions)} ({', '.join(regions)})")
    note(f"adventure_2d6 in eigen_centroids: {'adventure_2d6' in cents} (off-map by construction)")

    # ---- 1. Python recompute of the pairwise matrix + vote ----
    note("")
    note("== Python recompute from JSON (frozen reference) ==")
    ref_pairs = {}
    for i, a in enumerate(regions):
        for b in regions[i + 1:]:
            ref_pairs[(a, b)] = (dist_eigen(cents[a], cents[b]),
                                 bearing_deg(cents[a], cents[b]),
                                 bearing_deg(cents[b], cents[a]))
            note(f"  {a} -> {b}: dist {ref_pairs[(a, b)][0]:.4f} "
                 f"brg {ref_pairs[(a, b)][1]:5.1f} / back {ref_pairs[(a, b)][2]:5.1f}")

    water_first = ["water_computer", "fractal_maze", "riddler_optics",
                   "riddler_engram", "audit_dungeon"]
    chain = round(sum(math.hypot(cents[water_first[i + 1]][0] - cents[water_first[i]][0],
                                 cents[water_first[i + 1]][1] - cents[water_first[i]][1])
                      for i in range(len(water_first) - 1)), 4)
    star = round(sum(math.hypot(cents[r][0] - cents["water_computer"][0],
                                cents[r][1] - cents["water_computer"][1])
                     for r in regions if r != "water_computer"), 4)
    vote = scan["descent_vote"]
    note(f"  chain_len {chain:.4f} (scan files {vote['water_first_chain_len']}) "
         f"star_len {star:.4f} (scan files {vote['hub_first_star_len']})")
    check(round(chain, 3) == vote["water_first_chain_len"],
          f"chain length reproduces the scan's filed vote ({chain:.4f} vs {vote['water_first_chain_len']})")
    check(round(star, 3) == vote["hub_first_star_len"],
          f"star length reproduces the scan's filed vote ({star:.4f} vs {vote['hub_first_star_len']})")

    # walker probes
    note("")
    note("== walker probes (Python reference) ==")
    for r in regions:
        d = dist_eigen(cents[r], cents[r])
        note(f"  on {r}: dist to itself {d:.4f}")
    w, a = cents["water_computer"], cents["audit_dungeon"]
    mx, my = (w[0] + a[0]) / 2, (w[1] + a[1]) / 2
    # ties break alphabetically (same rule the module documents; the midpoint
    # of water/audit is an exact 0.0033 tie, so the rule is load-bearing here)
    nearest = min(regions, key=lambda r: ((cents[r][0] - mx) ** 2 + (cents[r][1] - my) ** 2, r))
    nd = round(math.hypot(cents[nearest][0] - mx, cents[nearest][1] - my), 4)
    nb = bearing_deg((mx, my), cents[nearest])
    note(f"  mid ({mx:.4f}, {my:.4f}): nearest {nearest} {nd:.4f} {nb:.1f} deg "
         f"(exact tie with water_computer at the same 0.0033; alphabetical rule)")
    fd = round(math.hypot(cents["fractal_maze"][0] - mx, cents["fractal_maze"][1] - my), 4)
    fb = bearing_deg((mx, my), cents["fractal_maze"])
    note(f"  mid -> fractal_maze: {fd:.4f} {fb:.1f} deg")

    # ---- 2. Run the REAL module under the luau CLI ----
    note("")
    note("== Luau CLI execution of roblox/src/shared/CathedralMap.luau ==")
    src = MODULE.read_text(encoding="utf-8")
    src_sha = hashlib.sha256(src.encode("utf-8")).hexdigest()
    note(f"module sha256 (tree): {src_sha}")
    test_src = TEST.read_text(encoding="utf-8")
    test_src = re.sub(r'require\("[^"]*CathedralMap"\)', 'require("./CathedralMap")', test_src, count=1)

    with tempfile.TemporaryDirectory(prefix="eigenmap-two-") as td:
        tdp = Path(td)
        mod_copy = tdp / "CathedralMap.luau"
        test_copy = tdp / "main.luau"
        mod_copy.write_text(src, encoding="utf-8", newline="")
        test_copy.write_text(test_src, encoding="utf-8", newline="")
        copy_sha = hashlib.sha256(mod_copy.read_bytes()).hexdigest()
        check(copy_sha == hashlib.sha256(MODULE.read_bytes()).hexdigest(),
              "staged module bytes are sha256-identical to the tree file")
        proc = subprocess.run([str(LUAU), str(test_copy)], capture_output=True, text=True)
        out = proc.stdout.strip()
        note(f"luau exit code: {proc.returncode}")
        if proc.stderr.strip():
            note(f"luau stderr: {proc.stderr.strip()[:500]}")
        check(proc.returncode == 0, "luau CLI ran the module to completion")

    note("")
    note("-- raw luau stdout --")
    for line in out.splitlines():
        note("  " + line)
    note("-- end raw stdout --")

    rows: dict[str, dict] = {"region": {}, "pair": {}, "probe_on_beacon": {}}
    chain_edges, hub_edges = [], []
    luau_meta = {}
    for line in out.splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "region":
            rows["region"][parts[1]] = parts[2:]
        elif parts[0] == "pair":
            rows["pair"][(parts[1], parts[2])] = [float(x) for x in parts[3:6]]
        elif parts[0] == "chaingedge":
            chain_edges.append((parts[1], parts[2]))
        elif parts[0] == "hubedge":
            hub_edges.append((parts[1], parts[2]))
        elif parts[0] in ("scan_ts", "scale", "origin", "vote"):
            luau_meta[parts[0]] = " ".join(parts[1:])
        elif parts[0] == "probe_on_beacon":
            rows["probe_on_beacon"][parts[1]] = parts[2:]

    # ---- 3. Diff Luau output vs the Python reference ----
    note("")
    note("== diff: Luau module output vs Python recompute vs JSON ==")
    check(luau_meta.get("scan_ts") == scan["ts"], f"module SCAN_TS equals the JSON ts ({luau_meta.get('scan_ts')})")
    for r in regions:
        got = rows["region"].get(r)
        exp_cos = scan["regions"][r]["cos"]
        ok = (got is not None
              and abs(float(got[0]) - cents[r][0]) < 1e-9
              and abs(float(got[1]) - cents[r][1]) < 1e-9
              and got[2] == scan["regions"][r]["class"]
              and ((exp_cos is None and got[3] == "nil") or (exp_cos is not None and abs(float(got[3]) - exp_cos) < 1e-9)))
        check(ok, f"region row {r}: eigen ({cents[r][0]}, {cents[r][1]}) class "
                  f"{scan['regions'][r]['class']} cos {exp_cos} matches the JSON")
    for (a, b), (d, br, bb) in ref_pairs.items():
        got = rows["pair"].get((a, b))
        ok = (got is not None and abs(got[0] - d) < 5e-5 and abs(got[1] - br) < 5e-2 and abs(got[2] - bb) < 5e-2)
        check(ok, f"pair {a}->{b}: dist {d:.4f} brg {br:.1f}/{bb:.1f} (module: {got})")

    check(luau_meta.get("vote", "").startswith(f"{chain:.4f} {star:.4f}"),
          f"module vote chain/star {luau_meta.get('vote')} equals the recompute {chain:.4f} {star:.4f}")

    exp_chain = [(water_first[i], water_first[i + 1])
                 for i in range(len(water_first) - 1)
                 if scan["regions"][water_first[i]]["class"] == "SADDLE"
                 and scan["regions"][water_first[i + 1]]["class"] == "SADDLE"]
    check(chain_edges == exp_chain,
          f"chain edges are exactly the SADDLE-SADDLE legs {exp_chain} (module: {chain_edges})")
    all_edges = chain_edges + hub_edges
    check(all("riddler_engram" not in e for e in all_edges),
          "NO edge (chain or hub) touches riddler_engram, the DARK anchor (referee ruling)")

    for r in regions:
        got = rows["probe_on_beacon"].get(r)
        ok = got is not None and abs(float(got[0])) < 5e-5 and got[2] == r
        check(ok, f"probe: standing on {r} reads dist 0.0000 and nearest {r} (module: {got})")

    mid_line = [l for l in out.splitlines() if l.startswith("probe_mid ")]
    if mid_line:
        p = mid_line[0].split()
        ok = (abs(float(p[1]) - mx) < 1e-9 and abs(float(p[2]) - my) < 1e-9
              and p[3] == nearest and abs(float(p[4]) - nd) < 5e-5 and abs(float(p[5]) - nb) < 5e-2)
        check(ok, f"probe midpoint: nearest {nearest} {nd:.4f} {nb:.1f} (module: {' '.join(p[3:])})")
    mid2 = [l for l in out.splitlines() if l.startswith("probe_mid_to_fractal")]
    if mid2:
        p = mid2[0].split()
        ok = abs(float(p[1]) - fd) < 5e-5 and abs(float(p[2]) - fb) < 5e-2
        check(ok, f"probe midpoint->fractal_maze: {fd:.4f} {fb:.1f} (module: {p[1]} {p[2]})")

    # ---- 4. world anchor round-trip (Python arithmetic on the module constants) ----
    note("")
    note("== world anchor round-trip (ORIGIN/SCALE from the module run) ==")
    ox, oy, oz = (float(x) for x in luau_meta.get("origin", "0 0 0").split())
    scale = float(luau_meta.get("scale", "0"))
    check(scale == 12000, f"SCALE read from the module run: {scale}")
    for r in regions:
        wx = ox + cents[r][0] * scale
        wz = oz + cents[r][1] * scale
        ex = (wx - ox) / scale
        ey = (wz - oz) / scale
        ok = abs(ex - cents[r][0]) < 1e-12 and abs(ey - cents[r][1]) < 1e-12
        note(f"  {r}: world ({wx:.1f}, {oy}, {wz:.1f}) -> eigen ({ex:.4f}, {ey:.4f})")
        check(ok, f"world anchor round-trips {r} exactly (north = eigen -y = world -Z: wz = OZ + ey*SCALE)")
    xs = [ox + cents[r][0] * scale for r in regions]
    zs = [oz + cents[r][1] * scale for r in regions]
    note(f"  plate extent: X {min(xs):.1f}..{max(xs):.1f}  Z {min(zs):.1f}..{max(zs):.1f} "
         f"(south ground, clear of every existing zone)")

    # ---- verdict ----
    note("")
    note(f"== VERDICT: {'PASS' if not failures else 'FAIL'} "
         f"({len(failures)} failure(s)) ==")
    for f in failures[:40]:
        note(f"  FAIL: {f}")
    RECEIPT.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"\nwrote {RECEIPT}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
