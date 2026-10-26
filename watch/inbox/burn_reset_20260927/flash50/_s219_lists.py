"""s2-19: print detail lists from scan JSON (patch targets, fake classes, monkey targets, conftest fixtures)."""
import json, os, collections

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
SCAN = os.path.join(REPO, "watch", "inbox", "burn_reset_20260927", "flash50", "_s219_scan.json")
d = json.load(open(SCAN, encoding="utf-8"))
agg = d["agg"]

print("=== PATCH STRING TARGETS (target: count, sites) ===")
for t, sites in sorted(agg["patch_string_targets_sites"].items()):
    locs = ["%s:%s" % (s["file"], s["line"]) for s in sites]
    print("%s | x%d | %s | kw=%s" % (t, len(sites), "; ".join(locs[:6]), sites[0]["kw"]))

print()
print("=== FAKE CLASSES ===")
for fc in agg["fake_classes_list"]:
    print("%s:%s %s bases=%s methods=%d %s" % (fc["file"], fc["line"], fc["name"],
                                               ",".join(fc["bases"])[:80], fc["n_methods"],
                                               ",".join(fc["methods"][:12])))

print()
print("=== MONKEY STRING TARGETS (unique %d) ===" % agg["monkey_unique_string_targets"])
for t, sites in sorted(agg["monkey_string_targets_map"].items()):
    print("%s | x%d | %s" % (t, len(sites), "; ".join("%s:%s" % (s["file"], s["line"]) for s in sites[:4])))

print()
print("=== MONKEY OBJ TARGET root histogram (after split) ===")
roots = collections.Counter()
recs = d["records"]
obj_sites = []
for r in recs:
    for t in r["monkey_obj_targets"]:
        root = t["target"].split(".")[0]
        roots[root] += 1
        obj_sites.append((r["file"], t["line"], t["target"]))
for root, n in roots.most_common(40):
    print("%-28s %d" % (root, n))
print("distinct roots", len(roots), "total obj", len(obj_sites))

print()
print("=== CONFTEST FIXTURES ===")
for r in recs:
    if r["file"].endswith("tests/conftest.py"):
        for f in r["fixtures"]:
            print("%-28s scope=%s autouse=%s yield=%s mock=%s (line %s)" % (
                f["name"], f["scope"], f["autouse"], f["yields"], f["creates_mock"], f["line"]))
        print("conftest lines", r["lines"], "monkey", r["monkey"])

print()
print("=== TOP FILES BY monkey setattr count ===")
tops = sorted(recs, key=lambda r: -(r["monkey"].get("setattr", 0)))[:15]
for r in tops:
    print("%-58s setattr=%d setenv=%d fixtures=%d tests=%d" % (
        r["file"], r["monkey"].get("setattr", 0), r["monkey"].get("setenv", 0),
        len(r["fixtures"]), r["test_funcs"]))

print()
print("=== patch( substring lines not AST-detected (explain 62 vs 26) ===")
import io, tokenize
detected = set()
for r in recs:
    for pc in r["patch_calls"]:
        detected.add((r["file"], pc["line"]))
n_extra = 0
for r in recs:
    p = os.path.join(REPO, r["file"])
    with open(p, "rb") as fh:
        for i, line in enumerate(fh.read().decode("utf-8", errors="replace").splitlines(), 1):
            if "patch(" in line and (r["file"], i) not in detected:
                n_extra += 1
                if n_extra <= 40:
                    print("%s:%d %s" % (r["file"], i, line.strip()[:110]))
print("extra substring lines", n_extra)
