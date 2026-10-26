"""B2-377 falsifier probe: a desc and a target_path each containing a single
quote must land status "dropped" with the .lnk and the .cmd on disk.

Executed 2026-09-26 with .venv/Scripts/python.exe. Disclosures:
- icon_drop.LEDGER and icon_drop.desktop_folder are monkeypatched to a temp
  dir and icon_drop._fold_training to a no-op so the real Desktop folder and
  the real ledgers (memory/icons/ledger.jsonl, skill_ledger, training_events)
  stay untouched; the powershell subprocess itself runs for real via the
  unchanged ps_exe resolution from B2-85.
- Arm A is the brief falsifier: a real target file whose path contains a
  single quote, args and desc carrying single quotes too; after the B2-377
  fix the PS literals are quote-doubled so the Save succeeds, the .lnk lands,
  and the probe reads the .lnk back through WScript.Shell to prove the
  fields survived byte-lossless (target, desc, args each equal the input).
- Arm B covers the .cmd side: a desc with a single quote AND batch
  metacharacters (& % ^ < > |); the generated .cmd must be on disk with the
  echo lines escaped and the run line verbatim, and the same escape helper's
  output is executed under real cmd.exe in a throwaway mini .bat whose stdout
  must carry the original desc literally (quote intact, % unexpanded,
  metacharacters rendered). The full .cmd is not executed because its tail
  runs "timeout /t 8", which errors under redirected stdin; the mini .bat
  isolates exactly the escaped echo line, disclosed here.
- Arm C pins the name sanitization: a name carrying a quote lands the .lnk
  at the sanitized filename and the ledger row records the sanitized name.
- The temp dir is removed after states are captured (disclosed here).
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

spec = importlib.util.spec_from_file_location("icon_drop_under_probe", REPO / "mag" / "icon_drop.py")
icon_drop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icon_drop)

tmp = Path(tempfile.mkdtemp(prefix="b2_377_probe_"))
tmp_ledger = tmp / "ledger.jsonl"
icon_drop.LEDGER = tmp_ledger
icon_drop.desktop_folder = lambda: tmp
icon_drop._fold_training = lambda row: None

ps_exe = shutil.which("powershell") or shutil.which("powershell.exe")

results = {"schema": "b2_377_unescape_probe.v1", "arms": []}

# Arm A: the brief falsifier. Real target file, quote in the target path,
# quote in args, quote in desc. Pre-fix this died exactly like the B2-354
# arm B (ParserError, exit 1, no .lnk).
quoted_target = tmp / "b2_377_o'brien's target.cmd"
quoted_target.write_text("@echo off\r\n", encoding="utf-8")
row_a = icon_drop.drop_shortcut(
    "b2_377_probe_ok",
    str(quoted_target),
    args="/d \"O'Brien\"",
    desc="B2-377 O'Brien arm",
)
lnk_a = tmp / "b2_377_probe_ok.lnk"
arm_a = {
    "arm": "A_quote_target_args_desc",
    "status": row_a["status"],
    "has_error_field": "error" in row_a,
    "lnk_existed": lnk_a.is_file(),
}
assert row_a["status"] == "dropped", f"arm A falsifier triggered: {row_a}"
assert lnk_a.is_file(), "arm A: no .lnk on disk despite status dropped"

# Read the .lnk back through the real WScript.Shell: the fields must round-
# trip losslessly (the quote-doubling must preserve the literal, not eat it).
ps_read = (
    "$s=(New-Object -ComObject WScript.Shell).CreateShortcut"
    f"('{lnk_a}');"
    "Write-Output $s.TargetPath;Write-Output $s.Arguments;Write-Output $s.Description"
)
proc_read = subprocess.run([ps_exe, "-NoProfile", "-Command", ps_read],
                           capture_output=True, text=True, check=False)
back = proc_read.stdout.splitlines()
arm_a["readback_rc"] = proc_read.returncode
arm_a["target_roundtrip"] = bool(back) and back[0] == str(quoted_target)
arm_a["args_roundtrip"] = len(back) > 1 and back[1] == "/d \"O'Brien\""
arm_a["desc_roundtrip"] = len(back) > 2 and back[2] == "B2-377 O'Brien arm"
assert proc_read.returncode == 0, f"arm A readback failed: {proc_read.stderr}"
assert arm_a["target_roundtrip"], f"target did not round-trip: {back}"
assert arm_a["args_roundtrip"], f"args did not round-trip: {back}"
assert arm_a["desc_roundtrip"], f"desc did not round-trip: {back}"
results["arms"].append(arm_a)

# Arm B: the .cmd side. Quote plus batch metacharacters in desc; the command
# keeps a %VAR% that must stay live-expanding on the run line and literal on
# the display line.
cmd_desc = "Reload O'Brien & %USERNAME% ^ done <now> | x"
row_b = icon_drop.drop("b2_377_cmd_probe", "echo %USERNAME% b2_377_ok", desc=cmd_desc)
cmd_b = tmp / "b2_377_cmd_probe.cmd"
arm_b = {
    "arm": "B_cmd_quote_and_metachars",
    "status": row_b["status"],
    "cmd_existed": cmd_b.is_file(),
}
assert row_b["status"] == "dropped", f"arm B falsifier triggered: {row_b}"
assert cmd_b.is_file(), "arm B: no .cmd on disk despite status dropped"
cmd_text = cmd_b.read_bytes().decode("utf-8")
arm_b["desc_line_escaped"] = (
    "echo  Reload O'Brien ^& %%USERNAME%% ^^ done ^<now^> ^| x\r\n" in cmd_text
)
arm_b["display_line_escaped"] = (
    "echo  Running: echo %%USERNAME%% b2_377_ok\r\n" in cmd_text
)
arm_b["run_line_verbatim"] = "echo %USERNAME% b2_377_ok\r\n" in cmd_text
arm_b["uniform_crlf_no_crcrlf"] = "\r\r" not in cmd_text
assert arm_b["desc_line_escaped"], f"desc line not escaped: {cmd_text!r}"
assert arm_b["display_line_escaped"], f"display line not escaped: {cmd_text!r}"
assert arm_b["run_line_verbatim"], f"run line altered: {cmd_text!r}"
assert arm_b["uniform_crlf_no_crcrlf"], "CRCRLF line endings on disk"

# Live execution of the escape helper's output under real cmd.exe: a mini
# .bat carrying exactly the escaped echo line must render the original desc
# literally (quote intact, % unexpanded, metacharacters as typed).
mini = tmp / "b2_377_mini.bat"
mini.write_bytes(
    b"@echo off\r\n"
    + b"echo  "
    + icon_drop._cmd_echo_safe(cmd_desc).encode("utf-8")
    + b"\r\nexit /b 0\r\n"
)
proc_bat = subprocess.run(["cmd.exe", "/d", "/c", str(mini)],
                          capture_output=True, text=True, check=False)
rendered = proc_bat.stdout.strip("\r\n")
arm_b["bat_rc"] = proc_bat.returncode
arm_b["bat_rendered_literal"] = rendered.strip() == cmd_desc
arm_b["bat_username_unexpanded"] = "%USERNAME%" in proc_bat.stdout
assert proc_bat.returncode == 0, f"mini bat failed rc={proc_bat.returncode}: {proc_bat.stderr}"
assert rendered.strip() == cmd_desc, f"rendered line mismatch: {rendered!r}"
assert "%USERNAME%" in proc_bat.stdout, f"percent got expanded: {proc_bat.stdout!r}"
results["arms"].append(arm_b)

# Arm C: a name carrying a quote and a slash lands the .lnk at the sanitized
# filename, and the ledger row records the sanitized name (same filter as
# drop()).
row_c = icon_drop.drop_shortcut("b2_377 quote'in/name", str(quoted_target), desc="name filter arm")
lnk_c = tmp / "b2_377 quoteinname.lnk"
arm_c = {
    "arm": "C_name_sanitized",
    "status": row_c["status"],
    "row_name": row_c["name"],
    "lnk_existed": lnk_c.is_file(),
}
assert row_c["status"] == "dropped", f"arm C failed: {row_c}"
assert lnk_c.is_file(), "arm C: sanitized .lnk not on disk"
assert row_c["name"] == "b2_377 quoteinname", f"row name not sanitized: {row_c['name']}"
results["arms"].append(arm_c)

# Ledger bytes check: what landed on disk matches the three dropped rows.
rows_on_disk = [json.loads(line) for line in tmp_ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
results["ledger_rows_on_disk"] = [
    {"name": r.get("name"), "status": r.get("status"), "has_error": "error" in r}
    for r in rows_on_disk
]
assert len(rows_on_disk) == 3 and all(r["status"] == "dropped" for r in rows_on_disk), rows_on_disk
assert not any("error" in r for r in rows_on_disk), rows_on_disk

results["falsifier_holds"] = True

# Capture done; remove the temp dir (disclosed).
shutil.rmtree(tmp, ignore_errors=True)

out = REPO / "watch" / "inbox" / "burn_wave_20260926" / "B2_377_unescape_probe_results.json"
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(results, indent=2, ensure_ascii=False))
