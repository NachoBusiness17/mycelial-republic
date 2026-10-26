"""wave5-repair stealth-tools: finish-line probes.

A. ADS round-trip: the fixed fanout write site round-trips an answer
   through a colon-containing slug and the BASE file reads it back; plus a
   negative control showing the OLD construction still diverts into an ADS.
B. selffeed: one REAL dispatch cycle through the fixed driver (real mined
   findings, real queue, Hermes venv python).
C. single-instance lock: a holder process takes the lock, then the real
   `tools/stealth_driver.py once` must refuse loudly with exit 2.
D. mirrors.json on-change: the real converged catalog must produce NO
   write; a changed catalog must write.

Usage: python _probe_finish_line.py [A|B|C|D ...]   (default: all four)
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
LANE_DIR = ROOT / "watch" / "inbox" / "gala_20260925" / "wave5-repair" / "lanes"
PROBE_DIR = LANE_DIR / "_probe_ads_roundtrip"
COLON_MODEL = "inclusionai/ling-3.0-flash-sante:free"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def stream_list(path: Path) -> str:
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         f"Get-Item -LiteralPath '{path}' -Stream * | "
         "Select-Object Stream,Length | Format-Table -AutoSize | "
         "Out-String"],
        capture_output=True, text=True, timeout=60)
    return (r.stdout or "").strip()


def probe_a() -> None:
    print("=" * 72)
    print("PROBE A: fanout write site, colon slug round-trip (fixed path)")
    print("=" * 72)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    fan = load("stealth_fanout", ROOT / "tools" / "stealth_fanout.py")
    fan.OUT_DIR = PROBE_DIR
    fan.HEARTBEAT = PROBE_DIR / "hb.jsonl"
    fan.LANES = [{"base": "https://api.llm7.io/v1/chat/completions",
                  "key": "", "model": COLON_MODEL}]
    fan.dispatch = lambda lane, ask, max_tokens=3000: (
        "ROUND-TRIP BODY: the answer must live in the base file.", {})
    row = fan.run_item(0, "probe-ads", "ask text")
    print("run_item row:", json.dumps(row))
    written = list(PROBE_DIR.glob("fan_probe-ads_*.md"))[0]
    print("filename:", written.name)
    print("colon in filename:", ":" in written.name)
    back = written.read_text(encoding="utf-8")
    print("base file size:", written.stat().st_size)
    print("base file contains body:", "ROUND-TRIP BODY" in back)
    print("streams on base file:")
    print(stream_list(written))

    print()
    print("NEGATIVE CONTROL: the OLD construction (replace / only)")
    old_path = PROBE_DIR / \
        "fan_negctl_inclusionai_ling-3.0-flash-sante:free.md"
    old_path.write_text("NEGATIVE CONTROL BODY", encoding="utf-8")
    base_file = PROBE_DIR / \
        "fan_negctl_inclusionai_ling-3.0-flash-sante"
    print("old-style target:", old_path.name)
    print("base file exists:", base_file.is_file(),
          "size:", base_file.stat().st_size if base_file.is_file() else "n/a")
    print("base file readable content:", repr(
        base_file.read_text(encoding="utf-8")))
    print("streams on base file (content is HERE on the old code):")
    print(stream_list(base_file))


def probe_b() -> None:
    print("=" * 72)
    print("PROBE B: selffeed real dispatch cycle (fixed driver)")
    print("=" * 72)
    drv = load("stealth_driver", ROOT / "tools" / "stealth_driver.py")
    queue_before = 0
    qpath = drv.WORK_QUEUE
    if qpath.is_file():
        queue_before = len([l for l in qpath.read_text(
            encoding="utf-8").splitlines() if l.strip()])
    t0 = time.time()
    result = drv.t_selffeed()
    dt = time.time() - t0
    print(f"t_selffeed() in {dt:.1f}s -> {result}")
    queue_after = 0
    if qpath.is_file():
        queue_after = len([l for l in qpath.read_text(
            encoding="utf-8").splitlines() if l.strip()])
    print(f"work queue rows: before={queue_before} after={queue_after}")
    state = drv._lane_state()
    print("selffeed_fail_streak after:", state.get("selffeed_fail_streak"))


def probe_c() -> None:
    print("=" * 72)
    print("PROBE C: single-instance lock refuses a second instance")
    print("=" * 72)
    holder = subprocess.Popen(
        [sys.executable, "-c",
         "import importlib.util, sys, time\n"
         "spec = importlib.util.spec_from_file_location('sd_holder',\n"
         f"    r'{ROOT / 'tools' / 'stealth_driver.py'}')\n"
         "mod = importlib.util.module_from_spec(spec)\n"
         "spec.loader.exec_module(mod)\n"
         "mod.acquire_instance_lock()\n"
         "print('HOLDER: lock held', flush=True)\n"
         "time.sleep(15)\n"],
        cwd=str(ROOT), text=True)
    time.sleep(4)  # holder has the lock by now
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "stealth_driver.py"), "once"],
        capture_output=True, text=True, timeout=120, cwd=str(ROOT))
    print("second-instance rc:", r.returncode)
    print("second-instance stdout:", (r.stdout or "").strip()[:200])
    holder.wait(timeout=30)
    print("expected: rc=2 and a REFUSED line; loop/once never ran topics")


def probe_d() -> None:
    print("=" * 72)
    print("PROBE D: mirrors.json writes only on change (real file)")
    print("=" * 72)
    drv = load("stealth_driver", ROOT / "tools" / "stealth_driver.py")
    mirrors = drv.MIRRORS
    before = mirrors.stat().st_mtime, mirrors.read_text(encoding="utf-8")
    cur = json.loads(before[1])
    unchanged = drv._write_mirrors_if_changed(
        cur["hosts"], cur.get("diff_line", ""))
    after = mirrors.stat().st_mtime, mirrors.read_text(encoding="utf-8")
    print("write returned (identical catalog):", unchanged)
    print("file mtime unchanged:", before[0] == after[0])
    print("file bytes unchanged:", before[1] == after[1])
    scratch = LANE_DIR / "_probe_mirrors_scratch.json"
    drv.MIRRORS = scratch
    changed = drv._write_mirrors_if_changed(
        {"llm7": {"models": 65, "prev_models": 64, "churn": True}},
        "llm7 64 CHURN")
    print("write returned (changed catalog, scratch file):", changed)
    print("scratch file exists:", scratch.is_file())


def main() -> int:
    only = set(sys.argv[1:]) or {"A", "B", "C", "D"}
    if "A" in only:
        probe_a()
    if "B" in only:
        probe_b()
    if "C" in only:
        probe_c()
    if "D" in only:
        probe_d()
    return 0


if __name__ == "__main__":
    sys.exit(main())
