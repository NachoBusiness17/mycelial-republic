"""s2-19: summarize verify.json - failures, real-newer counts, env vars, fixtures."""
import json, os, collections

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
FLASH = os.path.join(REPO, "watch", "inbox", "burn_reset_20260927", "flash50")
d = json.load(open(os.path.join(FLASH, "_s219_verify.json"), encoding="utf-8"))
v = d["verdicts"]

# dedupe (target can appear in two kind buckets)
seen, uniq = set(), []
for x in v:
    if x["target"] not in seen:
        seen.add(x["target"])
        uniq.append(x)
v = uniq
print("unique targets (deduped)", len(v))

st = collections.Counter(x["status"] for x in v)
print("status", dict(st))

print()
print("=== IMPORT_FAIL targets ===")
for x in v:
    if x["status"] == "IMPORT_FAIL":
        print(x["target"], "| kind", x["kind"], "| sites", ["%s:%s" % (s["file"], s["line"]) for s in x["sites"][:2]])

print()
print("=== ATTR_MISSING ===")
for x in v:
    if x["status"] == "ATTR_MISSING":
        print(json.dumps({k: x[k] for k in ("target", "sites", "error", "site_last_commit",
                                            "real_module_file", "real_module_last_commit")}, indent=1))

print()
print("=== in-repo vs external among OK ===")
c = collections.Counter((x["status"], bool(x["real_in_repo"])) for x in v)
print(dict(c))

print()
print("=== real module changed AFTER mock site's file last commit (in-repo OK targets) ===")
newer = [x for x in v if x["status"] == "OK" and x["real_in_repo"] and x["real_module_changed_after_mock"]]
same = [x for x in v if x["status"] == "OK" and x["real_in_repo"] and x["real_module_changed_after_mock"] is False]
unknown = [x for x in v if x["status"] == "OK" and x["real_in_repo"] and x["real_module_changed_after_mock"] is None]
print("newer", len(newer), "not-newer", len(same), "unknown-date", len(unknown))
mods = collections.Counter(x["real_module_file"] for x in newer)
print("modules with newer-than-mock drift (top 20):")
for m, n in mods.most_common(20):
    print("  %-50s %d targets" % (m, n))

print()
print("=== biggest real-newer gaps (days approx from ISO strings) ===")
def days(a, b):
    from datetime import datetime
    da = datetime.fromisoformat(a[:19]); db = datetime.fromisoformat(b[:19])
    return (db - da).days
gaps = sorted(newer, key=lambda x: -days(x["site_last_commit"], x["real_module_last_commit"]))
for x in gaps[:25]:
    print("%-7s %-46s mock %s real %s (%+dd) %s" % (
        x["status"], x["target"][:46], (x["site_last_commit"] or "")[:10],
        (x["real_module_last_commit"] or "")[:10],
        days(x["site_last_commit"], x["real_module_last_commit"]),
        "; ".join("%s:%s" % (s["file"].replace("tests/", ""), s["line"]) for s in x["sites"][:2])))

print()
print("=== env var fakes (setenv/delenv) ===")
ev = d["env_vars"]
print("distinct var:method", len(ev), "total", sum(ev.values()))
for k, n in sorted(ev.items(), key=lambda kv: -kv[1])[:25]:
    print("  %-46s %d" % (k, n))

print()
print("=== fixture producers (%d) ===" % len(d["fixture_produce"]))
for key, f in sorted(d["fixture_produce"].items()):
    print("%-56s %-22s %s" % (key.split("::")[0].replace("tests/", ""), f["file"] and key.split("::")[1], f["produce"][:80]))

print()
print("=== local-object stub sites (%d) ===" % len(d["obj_local_stub_sites"]))
for s in d["obj_local_stub_sites"][:30]:
    print("  %s:%s %s" % (s["file"], s["line"], s["raw"]))
