"""ghidra_audit: the deep rung as a standing tool (binary_attest pattern).

WHAT: runs corpus/tools Ghidra headless over one binary, parses the banked
GhidraSmokeJava.java census lines (program, functions, entry, decompiled
chars), and can register the row so later re-runs fail loud on drift.

Consumer: the cartographer receipt chain (cycle 11 wires this per cycle 8's
debt row; cycle 9/10 receipts name it), operator binary-audit asks, and any
seat that must answer "what do these bytes do" after binary_attest answers
"whose bytes are these" (see watch/inbox/ghidra_followon_20261001.md, the
named goal "wired as a binary-audit tool in the R2.0 image-digest pattern").
Verifier: a live banked run is receipted in
watch/inbox/mates_leave_protocol/receipts/receipt_20261020_cartographer.md
with its log banked beside it; `ghidra_audit.py verify` re-derives the row
from bytes and exits nonzero on drift; RAM gate refuses to launch when free
RAM minus 2 GB cannot cover the estimate (the shared-box swap law).

Laws honored: no env vars are read or dumped (analyzeHeadless.bat reads the
vendored launch.properties itself); the RAM gate is built in; no timeouts
papering over sync problems (process wait is unbounded by design, the
caller's shell owns the budget).

Usage:
  python tools/ghidra_audit.py audit <binary> [--register PATH]
                                        [--need-gb N] [--wait-minutes N]
  python tools/ghidra_audit.py verify <binary> --register PATH

Exit codes: 0 clean; 2 usage/path error; 3 RAM gate refused; 4 Ghidra run
failed or SMOKE lines missing; 5 verify drift.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GHIDRA = REPO / "corpus" / "tools" / "ghidra_12.1.4_PUBLIC" / "support" / "analyzeHeadless.bat"
SCRIPT_DIR = REPO / "corpus" / "tools"
POST_SCRIPT = "GhidraSmokeJava.java"
DEFAULT_REGISTER = REPO / "memory" / "ghidra_audit_register.json"
DEFAULT_NEED_GB = 6.0
RESERVE_GB = 2.0


def free_ram_gb() -> float:
    try:
        import psutil
        return psutil.virtual_memory().available / (1024 ** 3)
    except ImportError:
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        st = MEMORYSTATUSEX()
        st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
        return st.ullAvailPhys / (1024 ** 3)


def ram_gate(need_gb: float, wait_minutes: int) -> float:
    """Refuse to launch unless free minus reserve covers need. Polls when
    wait_minutes > 0 (the box frees itself as lanes clear)."""
    waited = 0.0
    while True:
        free = free_ram_gb()
        if free - RESERVE_GB >= need_gb:
            return free
        if waited >= wait_minutes * 60:
            sys.stderr.write(
                "RAM GATE: free %.1f GB minus %.1f GB reserve < %.1f GB need; "
                "refusing to launch (waited %.0f s)\n" % (free, RESERVE_GB, need_gb, waited)
            )
            raise SystemExit(3)
        time.sleep(30)
        waited += 30


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_audit(binary: Path, need_gb: float, wait_minutes: int) -> dict:
    if not GHIDRA.is_file():
        raise SystemExit("ghidra_audit: analyzeHeadless.bat not found at %s" % GHIDRA)
    free = ram_gate(need_gb, wait_minutes)
    proj = Path(tempfile.mkdtemp(prefix="ghidra_audit_proj_"))
    try:
        cmd = [
            str(GHIDRA), str(proj), "audit",
            "-import", str(binary),
            "-scriptPath", str(SCRIPT_DIR),
            "-postScript", POST_SCRIPT,
            "-deleteProject",
        ]
        t0 = time.time()
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        elapsed = time.time() - t0
    finally:
        shutil.rmtree(proj, ignore_errors=True)
    if proc.returncode != 0:
        sys.stderr.write("ghidra_audit: analyzeHeadless exit %d\n" % proc.returncode)
        raise SystemExit(4)
    smoke = [ln for ln in (proc.stdout or "").splitlines() if "SMOKE" in ln]
    row = {
        "binary": str(binary),
        "sha256": sha256_file(binary),
        "bytes": binary.stat().st_size,
        "moment": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "free_ram_gb_at_launch": round(free, 1),
        "elapsed_s": round(elapsed, 1),
        "raw_smoke_lines": smoke,
    }
    for ln in smoke:
        for tok in ln.replace("GhidraSmokeJava.java>", "").split():
            if tok.startswith("program="):
                row["program"] = tok.split("=", 1)[1]
            elif tok.startswith("functions="):
                row["functions"] = int(tok.split("=", 1)[1])
            elif tok.startswith("entry="):
                row["entry"] = tok.split("=", 1)[1]
            elif tok.startswith("decompiled_chars="):
                row["decompiled_chars"] = int(tok.split("=", 1)[1])
    if "functions" not in row or "decompiled_chars" not in row:
        sys.stderr.write("ghidra_audit: SMOKE census lines missing from output\n")
        raise SystemExit(4)
    return row


def load_register(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"rows": {}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Ghidra deep-rung census + drift register")
    sub = ap.add_subparsers(dest="mode", required=True)
    a1 = sub.add_parser("audit")
    a1.add_argument("binary", type=Path)
    a1.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    a1.add_argument("--need-gb", type=float, default=DEFAULT_NEED_GB)
    a1.add_argument("--wait-minutes", type=int, default=0)
    a2 = sub.add_parser("verify")
    a2.add_argument("binary", type=Path)
    a2.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    a2.add_argument("--need-gb", type=float, default=DEFAULT_NEED_GB)
    a2.add_argument("--wait-minutes", type=int, default=0)
    args = ap.parse_args(argv)
    binary = args.binary.resolve()
    if not binary.is_file():
        raise SystemExit("ghidra_audit: binary not found: %s" % binary)
    row = run_audit(binary, args.need_gb, args.wait_minutes)
    reg = load_register(args.register)
    key = str(binary)
    if args.mode == "audit":
        reg["rows"][key] = row
        args.register.parent.mkdir(parents=True, exist_ok=True)
        args.register.write_text(json.dumps(reg, indent=1), encoding="utf-8")
        print(json.dumps(row, indent=1))
        return 0
    prior = reg["rows"].get(key)
    if prior is None:
        sys.stderr.write("ghidra_audit: no register row for %s\n" % key)
        return 5
    diffs = {}
    for field in ("sha256", "functions", "entry", "decompiled_chars"):
        if prior.get(field) != row.get(field):
            diffs[field] = {"registered": prior.get(field), "now": row.get(field)}
    if diffs:
        print(json.dumps({"drift": True, "fields": diffs}, indent=1))
        return 5
    print(json.dumps({"drift": False, "sha256": row["sha256"], "functions": row["functions"],
                      "entry": row["entry"], "decompiled_chars": row["decompiled_chars"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
