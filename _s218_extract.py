"""s2-18 census extractor: parse dashboard/rest.py ROUTES + LEGACY via AST,
then statically extract per-handler response shapes (return status codes and
dict literal keys). Outputs _s218_routes.json. No fabrication: keys are only
what is literally visible in `return` positions."""
import ast
import json
from pathlib import Path

SRC = Path("dashboard/rest.py")
tree = ast.parse(SRC.read_text(encoding="utf-8"))

# ---- 1. route tables -------------------------------------------------------
def table_rows(assign_target: str):
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        if any(isinstance(t, ast.Name) and t.id == assign_target for t in targets):
            rows = []
            for el in node.value.elts:  # list of tuples
                method = el.elts[0].value
                path = el.elts[1].value
                fn = el.elts[2]
                if isinstance(fn, ast.Lambda):
                    handler = "lambda -> " + ast.unparse(fn.body)[:60]
                else:
                    handler = fn.id
                rows.append({"table": assign_target, "method": method, "path": path, "handler": handler})
            return rows, node.lineno
    return [], None

routes, routes_line = table_rows("ROUTES")
legacy, legacy_line = table_rows("LEGACY")

# ---- 2. handler functions --------------------------------------------------
handlers = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        handlers[node.name] = node

def dict_keys_of(d: ast.expr):
    """Static keys of a dict literal; None for **expr merges or dynamic."""
    keys = []
    for k, _v in zip(d.keys, d.values):
        if k is None:
            keys.append("**" + ast.unparse(_v)[:30])
        elif isinstance(k, ast.Constant) and isinstance(k.value, str):
            keys.append(k.value)
        else:
            keys.append("<expr:" + ast.unparse(k)[:24] + ">")
    return keys

def scan_returns(fn: ast.FunctionDef):
    """Collect (status, keys) for every return of shape (int, dict) plus
    _ok(...) / _err(...) helper calls and bare-int returns."""
    out = []
    for n in ast.walk(fn):
        if not isinstance(n, ast.Return) or n.value is None:
            continue
        v = n.value
        if isinstance(v, ast.Tuple) and len(v.elts) == 2:
            st, body = v.elts
            if isinstance(st, ast.Constant) and isinstance(st.value, int):
                if isinstance(body, ast.Dict):
                    out.append({"status": st.value, "keys": dict_keys_of(body), "line": n.lineno})
                elif isinstance(body, ast.Call) and isinstance(body.func, ast.Name) and body.func.id in ("_ok", "_err"):
                    rec = {"status": st.value, "helper": body.func.id, "line": n.lineno}
                    for kw in body.keywords:
                        if kw.arg == "schema" and isinstance(kw.value, ast.Constant):
                            rec["schema"] = kw.value.value
                        if kw.arg == "data" and isinstance(kw.value, ast.Dict):
                            rec["data_keys"] = dict_keys_of(kw.value)
                    if body.args and isinstance(body.args[0], ast.Dict) and body.func.id == "_err":
                        pass
                    out.append(rec)
                elif isinstance(body, ast.Call) and isinstance(body.func, ast.Name) and body.func.id in handlers:
                    out.append({"status": st.value, "delegates": body.func.id, "line": n.lineno})
                else:
                    out.append({"status": st.value, "keys": None, "line": n.lineno})
            else:
                out.append({"status": "<dyn>", "keys": None, "line": n.lineno})
    return out

def scan_ok_err(fn: ast.FunctionDef):
    """Also catch _ok/_err called in return-position tuples inside helper use."""
    shapes = scan_returns(fn)
    return shapes

handler_info = {}
for name, fn in handlers.items():
    rets = scan_returns(fn)
    statuses = sorted({str(r["status"]) for r in rets})
    # primary success shape: first return with status 200/202 and keys not None
    primary = None
    for r in rets:
        if r.get("keys"):
            primary = r
            break
    helpers = sorted({r["helper"] for r in rets if "helper" in r})
    delegates = sorted({r["delegates"] for r in rets if "delegates" in r})
    body_reads = sorted({
        ast.unparse(t) for n in ast.walk(fn)
        for t in ast.walk(n) if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == "body"
        and isinstance(t.slice, ast.Constant)} )
    handler_info[name] = {
        "line": fn.lineno,
        "statuses": statuses,
        "primary_keys": primary["keys"] if primary else None,
        "primary_line": primary["line"] if primary else None,
        "helpers": helpers,
        "delegates": delegates,
        "body_keys_read": body_reads[:12],
    }

# ---- 3. stitch -------------------------------------------------------------
def enrich(rows):
    out = []
    for r in rows:
        h = handler_info.get(r["handler"].split(" -> ")[0])
        r = dict(r)
        r["handler_line"] = h["line"] if h else None
        r["statuses"] = h["statuses"] if h else None
        r["primary_keys"] = h["primary_keys"] if h else None
        r["helpers"] = h["helpers"] if h else None
        r["delegates"] = h["delegates"] if h else None
        out.append(r)
    return out

result = {
    "routes_line": routes_line,
    "legacy_line": legacy_line,
    "routes": enrich(routes),
    "legacy": enrich(legacy),
    "handlers": handler_info,
    "counts": {
        "routes_rows": len(routes),
        "legacy_rows": len(legacy),
        "total_rows": len(routes) + len(legacy),
        "distinct_handlers": len({r["handler"] for r in routes + legacy if not r["handler"].startswith("lambda")}),
        "distinct_paths": len({r["path"] for r in routes + legacy}),
    },
}
Path("_s218_routes.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
print("rows:", result["counts"])
# method census
from collections import Counter
print("methods all:", Counter(r["method"] for r in routes + legacy))
print("methods ROUTES:", Counter(r["method"] for r in routes))
print("methods LEGACY:", Counter(r["method"] for r in legacy))
no_shape = [r["handler"] for r in routes + legacy if r["handler"] in handler_info and not handler_info[r["handler"]]["primary_keys"] and not handler_info[r["handler"]]["delegates"]]
print("handlers with no static dict keys and no delegate:", len(set(no_shape)), sorted(set(no_shape))[:30])
