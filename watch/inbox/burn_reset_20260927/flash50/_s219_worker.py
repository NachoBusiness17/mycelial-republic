"""s2-19 worker: resolve dotted targets against the live venv + repo.
Reads JSON list [{"id":n,"target":"a.b.c"}]; writes JSON results."""
import importlib, inspect, json, os, sys

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, REPO)
os.chdir(REPO)

with open(sys.argv[1], encoding="utf-8") as fh:
    targets = json.load(fh)

out = []
for t in targets:
    dotted = t["target"]
    parts = dotted.split(".")
    res = {"target": dotted, "status": "OK", "module": None, "module_file": None,
           "in_repo": False, "kind": None, "sig": None, "error": None}
    mod = None
    imported_upto = 0
    for i in range(len(parts), 0, -1):
        try:
            mod = importlib.import_module(".".join(parts[:i]))
            imported_upto = i
            break
        except Exception:
            continue
    if mod is None:
        res["status"] = "IMPORT_FAIL"
        res["module"] = None
        out.append(res)
        continue
    res["module"] = ".".join(parts[:imported_upto])
    f = getattr(mod, "__file__", None)
    res["module_file"] = f
    if f:
        try:
            res["in_repo"] = os.path.normcase(f).startswith(os.path.normcase(REPO + os.sep))
        except Exception:
            res["in_repo"] = False
    obj = mod
    ok = True
    for p in parts[imported_upto:]:
        if hasattr(obj, p):
            obj = getattr(obj, p)
        else:
            res["status"] = "ATTR_MISSING"
            res["error"] = "no attr %r under %s" % (p, ".".join(parts[:imported_upto]))
            ok = False
            break
    if ok:
        res["kind"] = type(obj).__name__
        if callable(obj):
            try:
                res["sig"] = str(inspect.signature(obj))[:220]
            except (ValueError, TypeError):
                res["sig"] = None
    out.append(res)

with open(sys.argv[2], "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print("done", len(out))
