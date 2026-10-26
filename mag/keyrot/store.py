"""Owner-only secret store at %LOCALAPPDATA%\\mag_secrets (ACL foste, SYSTEM, Administrators).

Only reached on the --apply path. Writes the new value straight from the adapter
response; never prints it. Consumer .env line is replaced in place after a backup.
"""
from __future__ import annotations

import datetime as dt
import os
import shutil
import subprocess
from pathlib import Path

STORE = Path(os.environ.get("LOCALAPPDATA", "~")) / "mag_secrets"


def ensure_store() -> Path:
    STORE.mkdir(parents=True, exist_ok=True)
    user = os.environ.get("USERNAME", "foste")
    subprocess.run(["icacls", str(STORE), "/inheritance:r", "/grant:r", f"{user}:(OI)(CI)F",
                    "SYSTEM:(OI)(CI)F", "*S-1-5-32-544:(OI)(CI)F"], check=True, capture_output=True)
    return STORE


def acl_ok() -> dict:
    if not STORE.exists():
        return {"exists": False}
    out = subprocess.run(["icacls", str(STORE)], capture_output=True, text=True).stdout
    principals = {l.split(":")[0].strip().split("\\")[-1] for l in out.splitlines()[0:] if ":(" in l}
    return {"exists": True, "principals": sorted(principals)}


def put(env_name: str, value: str) -> Path:
    ensure_store()
    p = STORE / f"{env_name}.secret"
    if p.exists():
        p.replace(p.with_suffix(f".secret.prev-{dt.date.today():%Y%m%d}"))
    with open(p, "w", encoding="utf-8") as f:
        f.write(value)
    return p


def update_consumer_env(env_file: Path, env_name: str, value: str) -> Path:
    bak = ensure_store() / f"{env_file.name}.bak-keyrot-{dt.datetime.now():%Y%m%d%H%M%S}"  # backup lives in owner-only store
    shutil.copy2(env_file, bak)
    lines = env_file.read_text(encoding="utf-8").splitlines()
    out = [f"{env_name}={value}" if l.split("=", 1)[0].strip().removeprefix("export ") == env_name else l for l in lines]
    env_file.write_text("\n".join(out) + "\n", encoding="utf-8")
    return bak
