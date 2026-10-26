"""Key inventory. Values are held in memory only and never leave this module except
to in-process checks (git pickaxe, adapters). Output rows carry key_id only.

Self-steal: tools.secret_guard (policy paths, _parse, guarded _read), the same
non-secret name filter as mag.doctor.check_tracked_secrets, and the estate audit
file's mirror code-literal findings (parsed as file:line hints, no values).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

from tools.secret_guard.guard import _parse, _read  # sanctioned in-process reader
from tools.secret_guard.policy import is_secret_path

from mag.keyrot import providers

ROOT = Path(__file__).resolve().parents[2]
NON_SECRET_SUFFIXES = ("_HOST", "_URI", "_URL", "_MODEL", "_ClientID", "_ID", "_USERNAME", "_PORT",
                       "_BASE", "_REGION", "_DIR", "_PATH", "_ENABLED", "_MODE")
NON_SECRET_NAMES = {"OLLAMA_HOST", "X_ClientID", "X_REDIRECT_URI", "AOS_AGENT_MODEL", "<file>"}
SECRETY = re.compile(r"KEY|TOKEN|SECRET|PASS|AUTH|CRED|PAT\b|BEARER", re.I)
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "corpus", "canon", "watch", "memory",
             "dist_audit", "state", "logs"}
NOFLAGS = 0x08000000 if sys.platform == "win32" else 0
MIN_LEN = 16


def key_id(provider: str, value: str) -> str:
    return f"{provider}:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}"


def mask(value: str) -> str:
    return f"{value[:4]}***({len(value)})" if len(value) > 12 else "***"


def candidate_files() -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for fn in files:
            p = Path(d) / fn
            if is_secret_path(str(p)) and not fn.endswith((".example", ".sample", ".pub")):
                out.append((p, "repo"))
    la = os.environ.get("LOCALAPPDATA")
    if la:
        h = Path(la) / "hermes"
        for p in sorted(h.glob(".env*")):
            if p.name not in (".env.lock",):
                out.append((p, "hermes_live" if p.name == ".env" else "hermes_backup"))
        if (h / "auth.json").exists():
            out.append((h / "auth.json", "hermes_auth"))
        st = Path(la) / "mag_secrets"
        if st.is_dir():
            for p in st.glob("*.secret"):
                out.append((p, "mag_secrets"))
    return out


def _is_secret_entry(name: str, value: str, kind: str) -> bool:
    if len(value) < MIN_LEN or name in NON_SECRET_NAMES or name.endswith(NON_SECRET_SUFFIXES):
        return False
    if value.startswith(("http://", "https://", "/", "C:\\")) or " " in value:
        return False
    if kind == "hermes_auth":  # JSON walk: only token-like leaves
        return bool(SECRETY.search(name.split(".")[-1]))
    return True


def collect() -> tuple[dict[str, dict], dict[str, str]]:
    """Return (inventory by key_id, {key_id: value} kept in memory for checks)."""
    inv: dict[str, dict] = {}
    vals: dict[str, str] = {}
    for path, kind in candidate_files():
        try:
            if path.stat().st_size > 1_000_000:
                continue
            pairs = _parse(str(path), _read(str(path)))
        except OSError:
            continue
        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
        for name, value in pairs.items():
            if not _is_secret_entry(name, value, kind):
                continue
            prov = providers.classify(name, value)
            kid = key_id(prov.name, value)
            vals[kid] = value
            row = inv.setdefault(kid, {"key_id": kid, "type": prov.name, "sha8": hashlib.sha256(value.encode()).hexdigest()[:8],
                                       "masked": mask(value), "env_names": [], "locations": [], "file_mtimes": []})
            if name not in row["env_names"]:
                row["env_names"].append(name)
            loc = f"{kind}:{_rel(path)}#{name}"
            if loc not in row["locations"]:
                row["locations"].append(loc)
            row["file_mtimes"].append(mtime)
    return inv, vals


def _rel(p: Path) -> str:
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p).replace(os.environ.get("USERPROFILE", "~~"), "%USERPROFILE%")


def _git(args: list[str], timeout: int) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, creationflags=NOFLAGS)
        return r.returncode, r.stdout
    except subprocess.TimeoutExpired:
        return -9, ""


BULK_PREFIX = ("corpus/", "canon/", "memory/cas/", "dist_audit/", "memory/corpus/")
BULK_EXT = (".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".gz", ".tar", ".parquet", ".bin",
            ".pt", ".safetensors", ".gguf", ".mp3", ".mp4", ".wav", ".epub", ".exe", ".dll", ".pyc", ".whl")


def history_scan(values: list[str], max_blob: int = 1_000_000, budget_s: int = 900) -> dict[str, dict]:
    """One pass over every reachable blob (all refs) instead of one pickaxe per key.
    Doctor law (live value vs tracked content) extended from HEAD to full history."""
    res = {v: {"blobs": set(), "paths": set()} for v in values}
    _, objs = _git(["rev-list", "--all", "--objects"], 600)
    path_of: dict[str, str] = {}
    for line in objs.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            path_of.setdefault(parts[0], parts[1])
    chk = subprocess.run(["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
                         input="\n".join(path_of) + "\n", cwd=str(ROOT), capture_output=True, text=True,
                         creationflags=NOFLAGS)
    blobs = [l.split()[0] for l in chk.stdout.splitlines()
             if len(l.split()) == 3 and l.split()[1] == "blob" and int(l.split()[2]) <= max_blob]
    total = len(blobs)
    blobs = [b for b in blobs if not path_of.get(b, "").startswith(BULK_PREFIX)
             and not path_of.get(b, "").lower().endswith(BULK_EXT)]
    meta = {"blobs_total_le_max": total, "blobs_eligible": len(blobs), "blobs_scanned": 0, "complete": False}
    import time
    t0 = time.monotonic()
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=str(ROOT), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, creationflags=NOFLAGS)
    import threading
    threading.Thread(target=lambda: (proc.stdin.write(("\n".join(blobs) + "\n").encode()), proc.stdin.close()),
                     daemon=True).start()
    rx = re.compile(b"|".join(re.escape(v.encode()) for v in sorted(values, key=len, reverse=True)))
    for _ in blobs:
        hdr = proc.stdout.readline().split()
        if len(hdr) < 3:
            break
        data = proc.stdout.read(int(hdr[2]))
        proc.stdout.read(1)
        meta["blobs_scanned"] += 1
        for m in set(rx.findall(data)):
            v = m.decode()
            res[v]["blobs"].add(hdr[0].decode())
            res[v]["paths"].add(path_of.get(hdr[0].decode(), "?"))
        if time.monotonic() - t0 > budget_s:
            break
    else:
        meta["complete"] = True
    proc.kill()
    res["__meta__"] = meta  # type: ignore[assignment]
    return res


def leak_detail(value: str, hit: dict) -> dict:
    rc, out = _git(["grep", "-l", "--fixed-strings", value, "HEAD", "--"], 60)
    head_files = sorted({l.split(":", 1)[-1] for l in out.splitlines()}) if rc == 0 else []
    commits: list[list[str]] = []
    for b in list(hit["blobs"])[:5]:
        _, lo = _git(["log", "--all", "--format=%H %cI", f"--find-object={b}"], 300)
        commits += [l.split() for l in lo.splitlines() if l.strip()]
    commits.sort(key=lambda c: c[1])
    remotes: list[str] = []
    if commits:
        _, br = _git(["branch", "-r", "--contains", commits[0][0]], 120)
        remotes = sorted({x.strip().split("/")[0] for x in br.splitlines() if x.strip() and "->" not in x})
    return {"head_files": head_files, "history": "scanned", "blobs": len(hit["blobs"]),
            "paths": sorted(hit["paths"])[:10], "commits": len({c[0] for c in commits}),
            "first_commit_date": commits[0][1][:10] if commits else None,
            "first_commit": commits[0][0][:12] if commits else None, "remotes": remotes}


def usage_check(env_names: list[str]) -> dict:
    hermes_cfg = ""
    la = os.environ.get("LOCALAPPDATA")
    if la and (Path(la) / "hermes" / "config.yaml").exists():
        hermes_cfg = (Path(la) / "hermes" / "config.yaml").read_text(encoding="utf-8", errors="replace")
    refs = 0
    for n in env_names:
        if "." in n:  # json path from auth.json: consumer is hermes itself
            refs += 1
            continue
        rc, out = _git(["grep", "-l", "-w", n, "HEAD", "--", ":!*.env*", ":!*.md"], 60)
        refs += len(out.splitlines()) if rc == 0 else 0
        refs += 1 if n in hermes_cfg else 0
    return {"code_refs": refs}


def enrich(inv: dict[str, dict], vals: dict[str, str], workers: int = 4) -> dict:
    hits = history_scan(list(vals.values()))
    meta = hits.pop("__meta__")
    for k in inv:
        h = hits[vals[k]]
        inv[k]["leak"] = leak_detail(vals[k], h) if h["blobs"] else {"head_files": [], "history": "complete" if meta["complete"] else "partial",
                                                                     "blobs": 0, "commits": 0, "remotes": []}
    for row in inv.values():
        row["usage"] = usage_check(row["env_names"])
        row["live"] = any(l.startswith(("hermes_live", "hermes_auth", "repo:.env#", "mag_secrets"))
                          for l in row["locations"])
        dates = [d for d in [row["leak"].get("first_commit_date"), *row.pop("file_mtimes")] if d]
        row["first_seen_evidence"] = min(dates) if dates else None
    return meta


def audit_code_hints(status_file: Path) -> list[str]:
    """Parse 'Secret-like hits in mirror' file:line hints from the estate audit (no values)."""
    if not status_file.exists():
        return []
    txt = status_file.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Secret-like hits in mirror[^:]*:(.*)", txt)
    return re.findall(r"([\w/]+\.py:\d+) (\w+)", m.group(1)) if m else []
