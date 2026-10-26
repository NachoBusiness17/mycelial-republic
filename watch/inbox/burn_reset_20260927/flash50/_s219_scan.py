"""s2-19 instrument: AST census of pytest fixtures + mocks in tests/.

Captures per file:
- fixtures (@pytest.fixture): name, scope, autouse, does-body-create-mock
- mock class instantiations (MagicMock/Mock/AsyncMock/PropertyMock/...)
- patch* call sites with string targets + spec/autospec kw presence
- monkeypatch method usage + string setattr targets
- fake/stub class definitions (name heuristic) with bases + methods
- mock_open / create_autospec usage
- test-function count, file line count
Plus repo-level: non-py data files under tests/.
Dumps JSON to _s219_scan.json, prints aggregates.
"""
import ast, json, os, re, sys, tokenize, collections

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
TESTS = os.path.join(REPO, "tests")
OUT = os.path.join(REPO, "watch", "inbox", "burn_reset_20260927", "flash50", "_s219_scan.json")

MOCK_CLASSES = {"MagicMock", "Mock", "AsyncMock", "NonCallableMagicMock",
                "NonCallableMock", "PropertyMock", "Sentinel"}
MOCK_HELPERS = {"mock_open", "create_autospec"}
PATCH_FUNCS = {"patch", "patch.object", "patch.dict", "patch.multiple"}
MONKEY_METHODS = {"setattr", "setenv", "delenv", "setitem", "delitem", "chdir",
                  "cd", "delattr", "syspath_prepend", "monkeypatch", "attr_set"}
FAKE_RE = re.compile(r"^(Fake|Stub|Dummy|Spy|Null|Noop|Mini|Tiny|Scripted|Recording|Capturing|Fake_)")
FAKE_HINT = re.compile(r"(Fake|Stub|Dummy|Double)")

def qual_of(fn):
    try:
        return ast.unparse(fn)
    except Exception:
        return "?"

def kw_keys(node):
    return sorted(k.arg for k in node.keywords if k.arg)

class FileScanner:
    def __init__(self, path):
        self.path = path
        self.rel = os.path.relpath(path, REPO).replace("\\", "/")
        self.src = tokenize.open(path).read()
        self.tree = ast.parse(self.src, filename=path)
        self.rec = {
            "file": self.rel,
            "lines": len(self.src.splitlines()),
            "test_funcs": 0,
            "fixtures": [],          # {name,line,scope,autouse,yields,creates_mock}
            "fixture_scope_counter": collections.Counter(),
            "mock_objs": [],         # {name,line,kw}
            "patch_calls": [],       # {func,line,target,form,kw}
            "monkey": collections.Counter(),
            "monkey_string_targets": [],
            "monkey_obj_targets": [],
            "fake_classes": [],      # {name,line,bases,methods,n}
            "helpers": [],           # mock_open / create_autospec
            "mock_imports": [],
        }
        self.fixture_stack = []      # names of fixtures currently inside

    def scan(self):
        self.visit(self.tree)
        self.rec["fixture_scope_counter"] = dict(self.rec["fixture_scope_counter"])
        self.rec["monkey"] = dict(self.rec["monkey"])
        return self.rec

    def visit(self, node):
        for child in ast.iter_child_nodes(node):
            self._visit_node(child)

    def _visit_node(self, node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self._function(node)
        elif isinstance(node, ast.ClassDef):
            self._klass(node)
        elif isinstance(node, ast.Call):
            self._call(node)
            self.visit(node)
        else:
            self.visit(node)

    def _is_fixture(self, node):
        for dec in node.decorator_list:
            q = qual_of(dec)
            base = q.split("(")[0].strip()
            if base in ("fixture", "pytest.fixture"):
                return True
        return False

    def _function(self, node):
        if node.name.startswith("test_"):
            self.rec["test_funcs"] += 1
        is_fix = self._is_fixture(node)
        if is_fix:
            scope, autouse = "function", False
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call):
                    for k in dec.keywords:
                        if k.arg == "scope" and isinstance(k.value, ast.Constant):
                            scope = str(k.value.value)
                        if k.arg == "autouse":
                            autouse = True
            self.fixture_stack.append(node.name)
            yields = any(isinstance(n, ast.Yield) for n in ast.walk(node))
            # fill creates_mock after walk of body: scan body now for mock classes
            creates_mock = any(
                isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in MOCK_CLASSES
                for n in ast.walk(node)
            ) or any(
                isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in MOCK_CLASSES
                for n in ast.walk(node)
            )
            self.rec["fixtures"].append({
                "name": node.name, "line": node.lineno, "scope": scope,
                "autouse": autouse, "yields": yields, "creates_mock": creates_mock,
            })
            self.rec["fixture_scope_counter"][scope] += 1
        try:
            self.visit(node)
        finally:
            if is_fix:
                self.fixture_stack.pop()

    def _klass(self, node):
        name = node.name
        bases = [qual_of(b) for b in node.bases]
        is_fake = bool(FAKE_RE.match(name)) or bool(FAKE_HINT.search(name)) or any(
            FAKE_HINT.search(b) for b in bases)
        if is_fake:
            methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            self.rec["fake_classes"].append({
                "name": name, "line": node.lineno, "bases": bases,
                "methods": methods, "n_methods": len(methods),
                "n_stmts": len(node.body),
            })
        self.visit(node)

    def _call(self, node):
        fn = node.func
        fname = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else None)
        qual = qual_of(fn)
        in_fixture = self.fixture_stack[-1] if self.fixture_stack else None
        if fname in PATCH_FUNCS:
            rec = {"func": fname, "line": node.lineno, "kw": kw_keys(node), "in_fixture": in_fixture}
            args = node.args
            if fname == "patch.object" and len(args) >= 2:
                rec["form"] = "object"
                obj = qual_of(args[0])
                if isinstance(args[1], ast.Constant):
                    rec["target"] = obj + "." + str(args[1].value)
                else:
                    rec["target"] = obj + "." + qual_of(args[1])
            elif fname in ("patch", "patch.dict", "patch.multiple") and args and isinstance(args[0], ast.Constant):
                rec["form"] = "string"
                rec["target"] = str(args[0].value)
                if fname == "patch.multiple":
                    rec["targets_extra"] = sorted(k.arg for k in node.keywords if k.arg not in ("autospec", "spec", "spec_set", "new", "new_callable", "wraps", "side_effect", "return_value", "create", "reason"))
            elif args:
                rec["form"] = "expr"
                rec["target"] = qual_of(args[0])
            else:
                rec["form"] = "none"
                rec["target"] = None
            self.rec["patch_calls"].append(rec)
        elif fname in MOCK_CLASSES:
            self.rec["mock_objs"].append({"name": fname, "line": node.lineno,
                                          "kw": kw_keys(node), "in_fixture": in_fixture})
        elif fname in MOCK_HELPERS:
            self.rec["helpers"].append({"name": fname, "line": node.lineno, "kw": kw_keys(node)})
        if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.value.id == "monkeypatch":
            if fname in MONKEY_METHODS:
                self.rec["monkey"][fname] += 1
                if fname == "setattr" and node.args:
                    a0 = node.args[0]
                    if isinstance(a0, ast.Constant):
                        self.rec["monkey_string_targets"].append(
                            {"target": str(a0.value), "line": node.lineno, "in_fixture": in_fixture})
                    else:
                        obj = qual_of(a0)
                        attr = ""
                        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                            attr = "." + str(node.args[1].value)
                        self.rec["monkey_obj_targets"].append(
                            {"target": obj + attr, "line": node.lineno, "in_fixture": in_fixture})

def import_scan(rec, tree):
    seen = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and "mock" in node.module:
            for a in node.names:
                seen.add(a.name)
        elif isinstance(node, ast.Import):
            for a in node.names:
                if "mock" in a.name:
                    seen.add(a.name)
    rec["mock_imports"] = sorted(seen)

def main():
    files = []
    data_files = []
    for dp, dns, fns in os.walk(TESTS):
        dns[:] = [d for d in dns if d not in ("__pycache__", ".pytest_cache")]
        for f in sorted(fns):
            p = os.path.join(dp, f)
            if f.endswith(".py"):
                files.append(p)
            else:
                st = os.stat(p)
                data_files.append({
                    "file": os.path.relpath(p, REPO).replace("\\", "/"),
                    "bytes": st.st_size,
                })

    records = []
    errors = []
    for p in sorted(files):
        try:
            sc = FileScanner(p)
            rec = sc.scan()
            import_scan(rec, sc.tree)
            records.append(rec)
        except SyntaxError as e:
            errors.append({"file": os.path.relpath(p, REPO), "error": str(e)})

    agg = {
        "head_snapshot": None,
        "py_files": len(records),
        "syntax_errors": errors,
        "total_lines": sum(r["lines"] for r in records),
        "total_test_funcs": sum(r["test_funcs"] for r in records),
        "total_fixtures": sum(len(r["fixtures"]) for r in records),
        "fixtures_by_scope": collections.Counter(),
        "autouse_fixtures": 0,
        "yield_fixtures": 0,
        "mock_creating_fixtures": 0,
        "files_with_fixtures": 0,
        "total_mock_objs": 0,
        "mock_objs_by_class": collections.Counter(),
        "mock_kw_counter": collections.Counter(),
        "total_patch_calls": 0,
        "patch_string_targets": collections.Counter(),
        "patch_unique_string_targets": 0,
        "patch_expr_targets": [],
        "patch_kw_counter": collections.Counter(),
        "patch_autospec_calls": 0,
        "patch_spec_calls": 0,
        "patch_in_fixture_calls": 0,
        "monkey_method_counter": collections.Counter(),
        "monkey_unique_string_targets": 0,
        "monkey_obj_targets_total": 0,
        "fake_class_total": 0,
        "fake_classes_list": [],
        "helpers_total": collections.Counter(),
        "data_files_total": len(data_files),
        "data_bytes_total": sum(d["bytes"] for d in data_files),
        "data_by_ext": collections.Counter(),
    }
    for r in records:
        if r["fixtures"]:
            agg["files_with_fixtures"] += 1
        for f in r["fixtures"]:
            agg["fixtures_by_scope"][f["scope"]] += 1
            if f["autouse"]:
                agg["autouse_fixtures"] += 1
            if f["yields"]:
                agg["yield_fixtures"] += 1
            if f["creates_mock"]:
                agg["mock_creating_fixtures"] += 1
        agg["total_mock_objs"] += len(r["mock_objs"])
        for m in r["mock_objs"]:
            agg["mock_objs_by_class"][m["name"]] += 1
            for k in m["kw"]:
                agg["mock_kw_counter"][k] += 1
        agg["total_patch_calls"] += len(r["patch_calls"])
        for pc in r["patch_calls"]:
            if pc["form"] == "string" and pc["target"]:
                agg["patch_string_targets"][pc["target"]] += 1
            elif pc["form"] in ("expr", "object"):
                agg["patch_expr_targets"].append({"file": r["file"], "line": pc["line"],
                                                  "func": pc["func"], "target": pc["target"]})
            for k in pc["kw"]:
                agg["patch_kw_counter"][k] += 1
            if "autospec" in pc["kw"]:
                agg["patch_autospec_calls"] += 1
            if "spec" in pc["kw"] or "spec_set" in pc["kw"]:
                agg["patch_spec_calls"] += 1
            if pc.get("in_fixture"):
                agg["patch_in_fixture_calls"] += 1
        for meth, n in r["monkey"].items():
            agg["monkey_method_counter"][meth] += n
        agg["monkey_obj_targets_total"] += len(r["monkey_obj_targets"])
        agg["fake_class_total"] += len(r["fake_classes"])
        for fc in r["fake_classes"]:
            agg["fake_classes_list"].append({"file": r["file"], **fc})
        for h in r["helpers"]:
            agg["helpers_total"][h["name"]] += 1
    agg["patch_unique_string_targets"] = len(agg["patch_string_targets"])

    # monkey string targets unique
    mset = {}
    for r in records:
        for t in r["monkey_string_targets"]:
            mset.setdefault(t["target"], []).append({"file": r["file"], "line": t["line"]})
    agg["monkey_unique_string_targets"] = len(mset)
    agg["monkey_string_targets_map"] = {k: v for k, v in mset.items()}

    agg["patch_string_targets"] = dict(agg["patch_string_targets"].most_common())
    agg["patch_string_targets_sites"] = {}
    for r in records:
        for pc in r["patch_calls"]:
            if pc["form"] == "string" and pc["target"]:
                agg["patch_string_targets_sites"].setdefault(pc["target"], []).append(
                    {"file": r["file"], "line": pc["line"], "kw": pc["kw"]})
    agg["fixtures_by_scope"] = dict(agg["fixtures_by_scope"])
    agg["mock_objs_by_class"] = dict(agg["mock_objs_by_class"])
    agg["mock_kw_counter"] = dict(agg["mock_kw_counter"])
    agg["patch_kw_counter"] = dict(agg["patch_kw_counter"])
    agg["monkey_method_counter"] = dict(agg["monkey_method_counter"])
    agg["helpers_total"] = dict(agg["helpers_total"])
    agg["data_by_ext"] = dict(collections.Counter(
        os.path.splitext(d["file"])[1].lower() or "(none)" for d in data_files))
    agg["data_files"] = data_files

    out = {
        "agg": {k: v for k, v in agg.items() if k != "data_files"},
        "records": records,
        "data_files": data_files,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=str)

    print("py_files", agg["py_files"])
    print("syntax_errors", len(errors))
    print("total_lines", agg["total_lines"])
    print("total_test_funcs", agg["total_test_funcs"])
    print("total_fixtures", agg["total_fixtures"], "by_scope", agg["fixtures_by_scope"])
    print("autouse", agg["autouse_fixtures"], "yield", agg["yield_fixtures"],
          "mock_creating", agg["mock_creating_fixtures"], "files_with_fixtures", agg["files_with_fixtures"])
    print("mock_objs", agg["total_mock_objs"], "by_class", agg["mock_objs_by_class"])
    print("mock_kw_top", dict(collections.Counter(agg["mock_kw_counter"]).most_common(8)))
    print("patch_calls", agg["total_patch_calls"], "unique_string_targets", agg["patch_unique_string_targets"])
    print("patch_expr_targets", len(agg["patch_expr_targets"]))
    print("patch_autospec", agg["patch_autospec_calls"], "patch_spec", agg["patch_spec_calls"],
          "patch_in_fixture", agg["patch_in_fixture_calls"])
    print("patch_kw_top", dict(collections.Counter(agg["patch_kw_counter"]).most_common(10)))
    print("monkey", agg["monkey_method_counter"], "unique_string", agg["monkey_unique_string_targets"],
          "obj_total", agg["monkey_obj_targets_total"])
    print("fake_classes", agg["fake_class_total"])
    print("helpers", agg["helpers_total"])
    print("data_files", agg["data_files_total"], "bytes", agg["data_bytes_total"], "by_ext", agg["data_by_ext"])

if __name__ == "__main__":
    main()
