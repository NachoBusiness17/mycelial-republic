# pytest for steer_sign script
import subprocess
import os
import sys

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "steer_sign.py"))

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def run_cmd(args):
    result = subprocess.run(["python", SCRIPT] + args, capture_output=True, text=True,
                            creationflags=HEADLESS)
    return result

def test_sign_creates_key_and_signs(tmp_path, monkeypatch):
    # Use temporary key and steer file
    key_path = tmp_path / "key"
    steer_path = tmp_path / "steers.jsonl"
    # create a simple steer file with two rows without sig
    with open(steer_path, "w", encoding="utf-8") as f:
        f.write('{"id":"row1","text":"hello"}\n')
        f.write('{"id":"row2","text":"world"}\n')
    # monkeypatch defaults
    monkeypatch.setenv("STEER_SIGN_KEY", str(key_path))
    # run sign
    res = run_cmd(["sign", "--file", str(steer_path), "--key", str(key_path)])
    assert res.returncode == 0
    # verify now passes
    res2 = run_cmd(["verify", "--file", str(steer_path), "--key", str(key_path)])
    assert res2.returncode == 0

def test_verify_fails_on_tamper(tmp_path, monkeypatch):
    key_path = tmp_path / "key"
    steer_path = tmp_path / "steers.jsonl"
    # create signed file first
    with open(steer_path, "w", encoding="utf-8") as f:
        f.write('{"id":"row","text":"data"}\n')
    # sign
    run_cmd(["sign", "--file", str(steer_path), "--key", str(key_path)])
    # tamper the file
    with open(steer_path, "a", encoding="utf-8") as f:
        f.write('{"id":"tamper","text":"evil"}\n')
    # verify should fail (unsigned row counted as failure)
    res = run_cmd(["verify", "--file", str(steer_path), "--key", str(key_path)])
    assert res.returncode != 0
