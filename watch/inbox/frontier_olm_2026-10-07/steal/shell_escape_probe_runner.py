"""Probe: does the estate shell door (tools/code_execution.run_python) hold a
harness-vs-shell trust boundary? Steal round 1, open-local-language-models via
reddit, find 2 (OpenShell). Marker written to this seat's own steal dir, then
removed by the seat; no other path touched."""
from tools.code_execution import run_python

MARKER = ("C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/"
          "frontier_olm_2026-10-07/steal/shell_escape_probe.txt")

code = (
    "p = r'" + MARKER + "'\n"
    "open(p, 'w').write('marker: shell door wrote outside its tempdir cwd "
    "with full user privileges, 2026-10-07 steal round')\n"
    "print('wrote bytes:', len(open(p).read()))\n"
)
r = run_python(code, timeout=30)
print("ok:", r["ok"], "exit:", r["exit_code"])
print("output:", (r.get("output") or "")[:400])
print("error:", r.get("error", ""))
