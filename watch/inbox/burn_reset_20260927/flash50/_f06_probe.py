# f-06 invariant truth probe (item f-06, 2026-09-28)
# Read-only checks of the 13 count>100 invariants in memory/percolator/invariants.json
# against current code. Uses the repo venv. No real backend started; fake HTTP
# servers are in-process and shut down before exit.
import importlib.util
import inspect
import json
import sys
import threading
import http.server
from pathlib import Path

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")

out = {}

# T1 (inv 1cfaa99384eef05a "command not allowlisted: powershell")
from config import SHELL_ALLOW
out["t1_powershell_in_SHELL_ALLOW"] = "powershell" in SHELL_ALLOW
out["t1_SHELL_ALLOW"] = sorted(SHELL_ALLOW)
from tools.shell import run_shell
r = run_shell("powershell -NoProfile -Command Write-Output invariant_probe_ok")
out["t1_run_shell_result"] = r

# T2 (inv ae3af609ff99f27b "[Errno 2] ... powershell")
from mag.win_powershell import powershell_exe
out["t2_powershell_exe"] = powershell_exe()

# T3 (inv 1182ee5e2bc05248 "Start it with: python -m backend")
out["t3_backend___main___spec"] = str(importlib.util.find_spec("backend.__main__"))
import mag.agent_cli as ac
out["t3_default_BACKEND_URL"] = ac.BACKEND_URL
out["t3_BACKEND_TIMEOUT"] = getattr(ac, "BACKEND_TIMEOUT", None)
out["t3_preflight_signature"] = str(inspect.signature(ac._preflight_tool))

# T4 (inv f0879ec09c3ac3ce "backend reported failure" + unreachable message)
class H(http.server.BaseHTTPRequestHandler):
    payload = b"{}"
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(n)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(self.payload)
    def log_message(self, *a):
        pass

class H_empty(H):
    payload = json.dumps({"ok": False, "error": None, "result": None}).encode()

class H_nested(H):
    payload = json.dumps({"ok": False, "error": None,
                          "result": {"ok": False, "error": "bad arguments for run_python: name 'x' is not defined"}}).encode()

servers = []
def _start(handler):
    srv = http.server.HTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    servers.append(srv)
    return srv.server_address[1]

port1 = _start(H_empty)
ac.BACKEND_URL = f"http://127.0.0.1:{port1}"
out["t4_empty_error_body"] = ac._run_tool_http("run_python", {"code": "print(1)"})

port2 = _start(H_nested)
ac.BACKEND_URL = f"http://127.0.0.1:{port2}"
out["t4_nested_error_body"] = ac._run_tool_http("run_python", {"code": "print(1)"})

ac.BACKEND_URL = "http://127.0.0.1:9"
out["t4_unreachable_body"] = ac._run_tool_http("run_python", {"code": "print(1)"})
for s in servers:
    s.shutdown()

# T5 (inv 15ab53aafd718f09 write_file missing path, ddf94e08b17b9c92 run_python too short)
ok, msg = ac._preflight_tool("write_file", {"content": "x"})
out["t5_write_file_no_path"] = {"ok": ok, "msg": msg}
ok2, msg2 = ac._preflight_tool("run_python", {"code": "print()"})
out["t5_run_python_short"] = {"ok": ok2, "msg": msg2}

# T6 (inv 4f9c02234f4c31a5 swarm_health_law) - probe only, no law apply
from mag.swarm_health import status
out["t6_swarm_status"] = status()

# T7 (inv ff96a7ed10d26da8 W0.3 gate) - read-only replication of governor_autorun.py:539-544
from config import ROOT
arch = ROOT.parent / "mycelial-republic" / "data" / "raw"
out["t7_archive_dir"] = str(arch)
out["t7_dir_exists"] = arch.is_dir()
archives = []
if arch.is_dir():
    archives = [f.name for f in arch.iterdir() if f.suffix in (".zip", ".tar", ".gz")]
out["t7_archive_files"] = archives
out["t7_gate_verdict"] = "blocked" if not archives else "ready"

# T8 (inv 212719f4b54d06e9 Elevate steer)
from mag.elevate import shape_ask, should_elevate
out["t8_should_elevate_embassy"] = should_elevate("review the embassy packet and shape an escalate ask")
a = shape_ask("review the embassy packet")
out["t8_shape_ask_keys"] = sorted(a.keys())
out["t8_ask_chars"] = a.get("ask_chars")
out["t8_full_prompt_head"] = (a.get("full_prompt") or "")[:200]

# T9 source-presence confirms (d5c42653281b6828 / 0d01815e2fb9d5ca / others)
src = inspect.getsource(ac)
out["t9_collapse_threshold_5"] = "len(collapse_window) == 5 and len(set(collapse_window)) == 1" in src
out["t9_collapse_detail_fmt"] = 'detail=f"5x identical {name} calls"' in src
out["t9_backend_reported_failure_fallback"] = 'or "backend reported failure"' in src
out["t9_backend_server_hint"] = "python -m backend.server" in src
out["t9_run_python_min_len"] = "len(code) < 12" in src

print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
