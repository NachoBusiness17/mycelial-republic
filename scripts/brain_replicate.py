#!/usr/bin/env python3
"""brain_replicate: append-only, copy-only replication of the brain (2026-10-17).

"Host the brain off machine, multiple backups, so it's literally a growing
organism." Each run:

  1. builds the curated manifest (scripts/brain_manifest.py: denylist +
     redaction screens, excluded files listed by path only) and, in the SAME
     read pass, writes every new file into the LOCAL VAULT as a
     content-addressed object:  <vault>/objects/<sha[:2]>/<sha>
     Objects are written to a temp name and renamed in; an existing object
     is never rewritten. The manifest lands exclusive-create at
     <vault>/manifests/brain_manifest_<utc>_<sha12>.json. Old manifests and
     objects are never removed: the vault only grows.
  2. copies the vault to every other configured target with COPY-ONLY verbs:
       smb    robocopy /E /XC /XN /XO  (no /MIR, no /PURGE, no /MOV)
       rclone rclone copy --ignore-existing (never sync / move / delete)
     guard() refuses any command carrying a delete-capable verb or flag.
  3. verifies every target against the manifest: local / SMB re-hash every
     object; rclone crypt uses `rclone cryptcheck --one-way` (hash compare of
     the encrypted copy, nothing downloaded into the brain).
  4. writes a receipt to watch/receipts/brain_<utc>.json (targets, files,
     bytes, verify pass/fail, manifest sha).

Targets live in configs/brain_targets.yaml. bob (SMB over Tailscale) is
probed on TCP 445 first and skipped cleanly when offline or unshared; the
rclone crypt remote is skipped with a message until Nacho configures it
(docs/BRAIN_HOSTING.md). This script never runs `rclone config`, never
reads rclone.conf, and never touches the PUBLIC tier (that is
scripts/public_lattice_manifest.py, approve-gated).

Restore (read vault -> NEW empty folder, hash-checked):
  python scripts/brain_replicate.py restore --manifest <file> --to <empty dir>

Reused: brain_manifest screens (deepseek_direct_runner), backup_chain's
complete-marker rule, mesh_delta's content-addressed verify-then-serve, and
bintree_v2.publish_checkpoint's never-overwrite / atomic-write discipline.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import brain_manifest as bm  # noqa: E402

CONFIG = ROOT / "configs" / "brain_targets.yaml"
RECEIPTS = ROOT / "watch" / "receipts"
RECEIPT_SCHEMA = "brain_replicate_receipt.v1"

# Any of these in a command line means "can delete or overwrite on a target".
FORBIDDEN = {
    "sync", "bisync", "move", "moveto", "delete", "deletefile", "purge", "rmdir", "rmdirs",
    "cleanup", "dedupe", "/mir", "/purge", "/mov", "/move",
    "--delete-before", "--delete-during", "--delete-after", "--delete-excluded",
    "--max-delete", "--backup-dir", "--suffix",
}


def guard(cmd: list[str]) -> list[str]:
    for tok in cmd[1:]:
        if str(tok).strip().lower() in FORBIDDEN:
            raise RuntimeError(f"refusing delete-capable token in command: {tok}")
    return cmd


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# ─────────────────────────────── vault (content-addressed) ────────────────

def object_path(base: Path, sha: str) -> Path:
    return base / "objects" / sha[:2] / sha


def write_object(vault: Path, sha: str, data: bytes) -> bool:
    """True when a new object was added; False when it was already present."""
    final = object_path(vault, sha)
    if final.exists():
        return False
    final.parent.mkdir(parents=True, exist_ok=True)
    tmp = final.with_name(f".{sha}.{os.getpid()}.partial")
    with open(tmp, "xb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    try:
        os.rename(tmp, final)  # Windows: fails if final appeared meanwhile
    except FileExistsError:
        tmp.unlink()  # our own temp file only; the existing object is untouched
        return False
    return True


def store_manifest(base: Path, raw: bytes, sha: str, stamp: str) -> Path:
    d = base / "manifests"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"brain_manifest_{stamp}_{sha[:12]}.json"
    with open(p, "xb") as fh:
        fh.write(raw)
    return p


def _sha_file(p: Path) -> str | None:
    h = hashlib.sha256()
    try:
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    except OSError:
        return None
    return h.hexdigest()


def verify_tree(base: Path, manifest: dict, manifest_sha: str | None = None) -> dict[str, Any]:
    """Re-hash every manifest object under base; also the stored manifest itself."""
    failed, missing, checked = [], [], 0
    for sha in sorted({f["sha256"] for f in manifest["files"]}):
        checked += 1
        got = _sha_file(object_path(base, sha))
        if got is None:
            missing.append(sha)
        elif got != sha:
            failed.append(sha)
    man_ok = None
    if manifest_sha:
        hits = list((base / "manifests").glob(f"brain_manifest_*_{manifest_sha[:12]}.json"))
        man_ok = any(_sha_file(h) == manifest_sha for h in hits)
    ok = not failed and not missing and man_ok is not False
    return {"pass": ok, "objects_checked": checked, "corrupt": failed[:50],
            "missing": missing[:50], "n_corrupt": len(failed), "n_missing": len(missing),
            "manifest_present": man_ok}


def vault_run(vault: Path, root: Path | None = None) -> tuple[dict, bytes, str, dict]:
    new = {"objects_new": 0, "objects_present": 0, "bytes_new": 0}

    def sink(sha: str, data: bytes) -> None:
        if write_object(vault, sha, data):
            new["objects_new"] += 1
            new["bytes_new"] += len(data)
        else:
            new["objects_present"] += 1

    manifest, raw, sha = bm.build(root, sink=sink)
    return manifest, raw, sha, new


# ─────────────────────────────── tools / probes ───────────────────────────

def rclone_bin() -> str | None:
    found = shutil.which("rclone")
    if found:
        return found
    pats = [r"C:\Tools\rclone\rclone.exe", r"C:\Tools\rclone\*\rclone.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Rclone.Rclone_*\*\rclone.exe")]
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


def rclone_remotes(rclone: str) -> set[str]:
    """Remote names via `rclone listremotes` (rclone reads its own config; we never open it)."""
    try:
        r = subprocess.run([rclone, "listremotes", "--ask-password=false"], capture_output=True,
                           text=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return set()
    if r.returncode != 0:
        return set()
    return {ln.strip() for ln in r.stdout.splitlines() if ln.strip().endswith(":")}


def tcp_probe(host: str, port: int = 445, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def robocopy_cmd(src: Path, dst: str) -> list[str]:
    return guard(["robocopy", str(src), str(dst), "/E", "/XC", "/XN", "/XO",
                  "/R:1", "/W:1", "/NP", "/NFL", "/NDL", "/NJH", "/NJS",
                  "/XF", "*.partial"])


def rclone_copy_cmd(rclone: str, src: Path, remote: str) -> list[str]:
    return guard([rclone, "copy", str(src), remote, "--ignore-existing",
                  "--exclude", "*.partial", "--ask-password=false"])


def rclone_cryptcheck_cmd(rclone: str, src: Path, remote: str) -> list[str]:
    return guard([rclone, "cryptcheck", str(src), remote, "--one-way",
                  "--exclude", "*.partial", "--ask-password=false"])


def _run(cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
    return subprocess.run(guard(cmd), capture_output=True, text=True, timeout=timeout, check=False)


# ─────────────────────────────── targets ──────────────────────────────────

def load_config(path: Path | None = None) -> dict[str, Any]:
    import yaml

    with open(path or CONFIG, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def push_smb(t: dict, vault: Path, manifest: dict, msha: str) -> dict[str, Any]:
    host, dst = t.get("host"), t.get("path")
    if not host or not dst:
        return {"status": "skipped", "reason": "host/path not configured"}
    if not tcp_probe(host, int(t.get("port", 445)), float(t.get("probe_timeout_s", 2))):
        return {"status": "skipped", "reason": f"{host}:445 unreachable (offline or SMB closed)"}
    if not os.path.isdir(dst):
        return {"status": "skipped",
                "reason": f"share path {dst} not reachable/not created (Nacho: create the share)"}
    try:
        r = _run(robocopy_cmd(vault, dst), int(t.get("timeout_s", 7200)))
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "failed", "reason": f"robocopy: {type(exc).__name__}"}
    if r.returncode >= 8:
        return {"status": "failed", "reason": f"robocopy exit {r.returncode}"}
    return {"status": "ok", "copy_exit": r.returncode,
            "verify": verify_tree(Path(dst), manifest, msha)}


def push_rclone(t: dict, vault: Path, crypt: bool) -> dict[str, Any]:
    remote = str(t.get("remote") or "")
    rclone = rclone_bin()
    if rclone is None:
        return {"status": "skipped", "reason": "rclone not installed"}
    if not remote.endswith(":") and ":" not in remote:
        return {"status": "skipped", "reason": "remote not configured in brain_targets.yaml"}
    name = remote.split(":", 1)[0] + ":"
    if name not in rclone_remotes(rclone):
        return {"status": "skipped",
                "reason": f"rclone remote {name} not configured yet (see docs/BRAIN_HOSTING.md)"}
    try:
        r = _run(rclone_copy_cmd(rclone, vault, remote), int(t.get("timeout_s", 14400)))
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "failed", "reason": f"rclone copy: {type(exc).__name__}"}
    if r.returncode != 0:
        return {"status": "failed", "reason": f"rclone copy exit {r.returncode}"}
    check = rclone_cryptcheck_cmd(rclone, vault, remote) if crypt else guard(
        [rclone, "check", str(vault), remote, "--one-way", "--exclude", "*.partial",
         "--ask-password=false"])
    try:
        v = _run(check, int(t.get("timeout_s", 14400)))
        vpass = v.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        vpass = False
    return {"status": "ok", "verify": {"pass": vpass,
                                       "method": "cryptcheck --one-way" if crypt else "check --one-way"}}


def replicate(*, config: dict, root: Path | None = None, vault: Path | None = None,
              only: set[str] | None = None, receipts: Path | None = None) -> dict[str, Any]:
    targets = list(config.get("targets") or [])
    vt = next((t for t in targets if t.get("kind") == "vault"), None)
    if vault is None:
        if vt is None:
            raise SystemExit("no vault target in brain_targets.yaml")
        vault = Path(vt["path"])
    vault.mkdir(parents=True, exist_ok=True)
    stamp = _utc()
    manifest, raw, msha, new = vault_run(vault, root)
    mpath = store_manifest(vault, raw, msha, stamp)
    results = [{"name": (vt or {}).get("name", "local_vault"), "kind": "vault", "status": "ok",
                **new, "verify": verify_tree(vault, manifest, msha)}]
    for t in targets:
        kind, name = t.get("kind"), t.get("name")
        if kind == "vault":
            continue
        if only is not None and name not in only:
            results.append({"name": name, "kind": kind, "status": "skipped",
                            "reason": "not selected this run (--only)"})
            continue
        if not t.get("enabled", True):
            results.append({"name": name, "kind": kind, "status": "skipped", "reason": "disabled"})
            continue
        if kind == "smb":
            res = push_smb(t, vault, manifest, msha)
        elif kind in ("rclone_crypt", "rclone"):
            res = push_rclone(t, vault, crypt=(kind == "rclone_crypt"))
        else:
            res = {"status": "skipped", "reason": f"unknown kind {kind}"}
        results.append({"name": name, "kind": kind, **res})
    receipt = {
        "schema": RECEIPT_SCHEMA, "utc": stamp,
        "manifest_sha256": msha,
        "manifest_file": mpath.name,
        "v2": manifest["v2"], "v1": manifest["v1"],
        "files": manifest["totals"]["files"], "bytes": manifest["totals"]["bytes"],
        "excluded": manifest["excluded"], "missing": manifest["missing"],
        "targets": results,
        "verify_all_pass": all((r.get("verify") or {}).get("pass") for r in results
                               if r.get("status") == "ok"),
        "law": "copy-only, append-only: nothing on any target is ever deleted or overwritten",
    }
    rdir = receipts or RECEIPTS
    rdir.mkdir(parents=True, exist_ok=True)
    rp = rdir / f"brain_{stamp}.json"
    with open(rp, "x", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(receipt, indent=1) + "\n")
    receipt["receipt_path"] = str(rp)
    return receipt


def restore(manifest_file: Path, to: Path, vault: Path) -> dict[str, Any]:
    """Materialize a manifest from vault objects into a NEW empty folder."""
    if to.exists() and any(to.iterdir()):
        raise SystemExit("restore target must be a new or empty folder")
    m = json.loads(manifest_file.read_text(encoding="utf-8"))
    bad = 0
    for f in m["files"]:
        data = object_path(vault, f["sha256"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != f["sha256"]:
            bad += 1
            continue
        out = to / f["path"]
        if to.resolve() not in out.resolve().parents:
            raise SystemExit(f"manifest path escapes target: {f['path']}")
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "xb") as fh:
            fh.write(data)
    return {"restored": len(m["files"]) - bad, "corrupt": bad, "to": str(to)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="brain_replicate", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("push", help="manifest + vault + copy-only fan-out (default)")
    p.add_argument("--config", type=Path)
    p.add_argument("--only", help="comma list of non-vault target names to push this run")
    p.add_argument("--local-only", action="store_true", help="vault only; skip every other target")
    r = sub.add_parser("restore")
    r.add_argument("--manifest", type=Path, required=True)
    r.add_argument("--to", type=Path, required=True)
    r.add_argument("--vault", type=Path)
    r.add_argument("--config", type=Path)
    a = ap.parse_args(argv)
    cmd = a.cmd or "push"
    cfg = load_config(getattr(a, "config", None))
    if cmd == "restore":
        vault = a.vault or Path(next(t for t in cfg["targets"] if t.get("kind") == "vault")["path"])
        print(json.dumps(restore(a.manifest, a.to, vault), indent=1))
        return 0
    only = set() if getattr(a, "local_only", False) else (
        set(a.only.split(",")) if getattr(a, "only", None) else None)
    rec = replicate(config=cfg, only=only)
    print(json.dumps({k: rec[k] for k in ("manifest_sha256", "files", "bytes", "excluded",
                                          "targets", "verify_all_pass", "receipt_path")}, indent=1))
    return 0 if rec["verify_all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
