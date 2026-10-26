"""s2-19 cross-check: byte-level grep counters for mock markers in tests/,
independent of the AST scan. Also enumerates non-py files under tests/."""
import os, json, collections

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
TESTS = os.path.join(REPO, "tests")

markers = ["MagicMock", "unittest.mock", "monkeypatch", "Mock(", "patch(",
           "AsyncMock", "mock_open", "create_autospec", "spec=", "autospec",
           "Fake", "Stub", "Dummy", "side_effect", "return_value"]

counts = collections.Counter()          # marker -> total line hits
files_with = collections.Counter()      # marker -> file count
per_file = collections.defaultdict(set)

py_files, non_py = [], []
for dp, dns, fns in os.walk(TESTS):
    dns[:] = [d for d in dns if d not in ("__pycache__", ".pytest_cache")]
    for f in sorted(fns):
        p = os.path.join(dp, f)
        if f.endswith(".py"):
            py_files.append(p)
        else:
            non_py.append(os.path.relpath(p, REPO).replace("\\", "/"))

for p in py_files:
    with open(p, "rb") as fh:
        b = fh.read()
    text = b.decode("utf-8", errors="replace")
    for m in markers:
        hits = text.count(m)
        if hits:
            counts[m] += hits
            files_with[m] += 1

print("py_files", len(py_files))
print("non_py_files", len(non_py))
for m in markers:
    print("MARK", m, "lines", counts[m], "files", files_with[m])
print("NONPY_LIST", json.dumps(non_py))
