#!/usr/bin/env python3
"""seat_keygen: a seat mints its OWN Ed25519 handshake key (2026-10-17).

Run BY THE SEAT on the machine the seat lives on. The private key is written
to a path the seat chooses OUTSIDE this repo (default
%USERPROFILE%/.mag_seat/<seat>.key, i.e. ~/.mag_seat/<seat>.key), created
exclusively (an existing key is never overwritten) and permission-tightened
where the OS allows. Only the PUBLIC key is printed, as the JSON row the
operator pastes into configs/seat_allowlist.json under "seats". The private
key never touches stdout, the repo, or any log.

Mates (harness2, 2026-10-17): every leave-protocol mate gets its OWN key
under the seat id "mate:<name>", stored host-side at
~/.mag_seat/mates/mate__<name>.key (seat_handshake.default_key_path). The
mate model never sees the key; mag/harness_probe.py signs for it in process.
`--mates` mints one per mate in configs/mates.yaml (mates + harness_probe
roles), skips any that already exist WITHOUT reading them, prints only public
keys + fingerprints, and with --write-allowlist merges the public rows into
configs/seat_allowlist.json (kind "mate", model_family "glm").

Usage:
  .venv/Scripts/python.exe scripts/seat_keygen.py --seat gemini
  .venv/Scripts/python.exe scripts/seat_keygen.py --seat bob-agy --out D:/keys/bob-agy.key
  .venv/Scripts/python.exe scripts/seat_keygen.py --mates --write-allowlist
Then the seat points its client at the key with env MAG_SEAT_KEY_PATH.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import seat_handshake as sh  # noqa: E402

MATES_CONFIG = ROOT / "configs" / "mates.yaml"


def default_key_path(seat: str) -> Path:
    return sh.default_key_path(seat)


def _inside_repo(p: Path) -> bool:
    try:
        p.resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def _tighten(p: Path) -> None:
    try:
        os.chmod(p, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    if os.name == "nt":  # owner-only ACL; best effort, never fatal
        user = os.environ.get("USERNAME")
        if user:
            subprocess.run(["icacls", str(p), "/inheritance:r", "/grant:r", f"{user}:(R,W)"],
                           capture_output=True, check=False)


def keygen(seat: str, out: str | Path | None = None) -> dict:
    if not sh.SEAT_RE.fullmatch(seat or ""):
        raise SystemExit(f"--seat must match {sh.SEAT_RE.pattern}")
    path = Path(out) if out else default_key_path(seat)
    if _inside_repo(path):
        raise SystemExit("refusing: the private key must live OUTSIDE the repo")
    path.parent.mkdir(parents=True, exist_ok=True)
    rec = sh.key_record(seat, sh.generate_seed())
    public_hex = rec["public_hex"]
    try:
        with open(path, "x", encoding="utf-8") as fh:  # exclusive: never overwrite a key
            fh.write(json.dumps(rec, indent=1) + "\n")
    except FileExistsError:
        raise SystemExit(f"refusing: a key already exists at {path} (delete it yourself to rotate)")
    finally:
        rec = None  # the seed is never returned, printed, logged, or read back
    _tighten(path)
    return {"seat_id": seat, "public_hex": public_hex, "key_path": str(path)}


def mate_ids(config_path: str | Path = MATES_CONFIG) -> list[str]:
    import yaml

    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8")) or {}
    ids = [m["id"] for m in cfg.get("mates") or []]
    ids += [r["id"] for r in (cfg.get("harness_probe") or {}).get("roles") or []]
    seen: list[str] = []
    for i in ids:
        if i not in seen:
            seen.append(i)
    return seen


def keygen_mates(ids: list[str], *, allowlist: dict | None = None) -> list[dict]:
    """Mint mate:<id> keys that do not exist yet. Existing key files are never
    opened; their public key is taken from the allowlist row when there is one."""
    seats = (allowlist or {}).get("seats") or {}
    out = []
    for mid in ids:
        seat = f"{sh.MATE_PREFIX}{mid}"
        path = default_key_path(seat)
        if path.exists():
            pub = (seats.get(seat) or {}).get("public_hex")
            out.append({"seat_id": seat, "public_hex": pub, "key_path": str(path),
                        "status": "exists" if pub else "exists_not_allowlisted"})
            continue
        res = keygen(seat)
        res["status"] = "created"
        out.append(res)
    return out


def merge_allowlist(rows: list[dict], path: str | Path = sh.ALLOWLIST_PATH,
                    today: str | None = None) -> dict:
    """Add public mate rows under seats (never replaces a different key: that is
    reported as a conflict for the operator) and default the non-GLM rule on."""
    p = Path(path)
    al = json.loads(p.read_text(encoding="utf-8"))
    seats = al.setdefault("seats", {})
    q = al.setdefault("quorum", {"default": 2})
    q.setdefault("require_non_glm_approval", True)
    added, kept, conflicts = [], [], []
    for r in rows:
        seat, pub = r["seat_id"], r.get("public_hex")
        if not pub:
            continue
        cur = seats.get(seat)
        if cur and cur.get("public_hex") == pub:
            kept.append(seat)
            continue
        if cur:
            conflicts.append(seat)
            continue
        seats[seat] = {"public_hex": pub, "added": today or date.today().isoformat(),
                       "kind": "mate", "model_family": "glm",
                       "note": "harness2 leave-protocol mate seat (GLM via opencode); "
                               "signed host-side by mag/harness_probe.py"}
        added.append(seat)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(al, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, p)
    return {"added": added, "kept": kept, "conflicts": conflicts}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="seat_keygen", description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--seat")
    g.add_argument("--mates", action="store_true",
                   help="one key per mate in configs/mates.yaml (seat ids mate:<name>)")
    ap.add_argument("--out", help="private key path (outside the repo; --seat only)")
    ap.add_argument("--write-allowlist", action="store_true",
                    help="--mates: merge the public rows into configs/seat_allowlist.json")
    a = ap.parse_args(argv)
    if a.mates:
        rows = keygen_mates(mate_ids(), allowlist=sh.load_allowlist())
        for r in rows:
            fp = sh.fingerprint(r["public_hex"]) if r.get("public_hex") else "-"
            print(f"{r['seat_id']:<22} {r['status']:<22} fp={fp} pub={r.get('public_hex') or '-'}"
                  f" key={r['key_path']}")
        if a.write_allowlist:
            print(json.dumps(merge_allowlist(rows)))
        return 0
    res = keygen(a.seat, a.out)
    row = {res["seat_id"]: {"public_hex": res["public_hex"], "added": "<yyyy-mm-dd>",
                            "note": "<who/where>"}}
    print("# private key written (NOT printed) to:", res["key_path"], file=sys.stderr)
    print("# set MAG_SEAT_KEY_PATH to that path in the seat's client config", file=sys.stderr)
    print("# add this row under \"seats\" in configs/seat_allowlist.json:", file=sys.stderr)
    print(json.dumps(row, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
