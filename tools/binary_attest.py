"""binary_attest — prove the binaries we run are the bytes their sources ship.

The artifact-identity spine's third rung (R6 guards the pck, mcp_parity guards
image digests; this guards the third-party EXECUTABLES). Method: download the
canonical release archive from an ALLOWLISTED host, hash it, extract the named
member, compare byte-for-byte with the installed file — a MATCH is proof the
local binary is the official artifact (the Godot 4.3 proof, 2026-10-01, is the
template: watch/inbox/x_intel_drop_20261001.md addendum).

Security shape (Mimosa gate rulings, 2026-10-01): downloads are https-only to
a host-suffix allowlist (github.com and its release CDN, godotengine.org,
adoptium.net) with redirects re-validated per hop — no arbitrary-URL fetch
surface, private/loopback hosts unreachable by construction. Local paths and
archive member names reject '..' segments (zip-slip hygiene) before any read.

Register: configs/binary_register.json (sealed by config_seal; update then
re-seal). Exit contract: 0 verified clean / 1 drift or mismatch (fail loud) /
2 usage or IO. No repair: the tool reports, the operator decides.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from http.client import HTTPMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "configs" / "binary_register.json"
CHUNK = 1 << 20

# The only hosts this tool will fetch from. Release artifacts only; nothing
# internal is reachable (loopback/private hosts fail the suffix match).
# release-assets.githubusercontent.com is GitHub's canonical release CDN
# (github.com release links 302 there with signed URLs - verified live
# 2026-10-01 when the fence correctly refused it as unlisted).
ALLOWED_HOST_SUFFIXES = (
    "github.com",
    "objects.githubusercontent.com",
    "release-assets.githubusercontent.com",
    "godotengine.org",
    "api.adoptium.net",
    "adoptium.net",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _host_allowed(url: str) -> bool:
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    if parts.scheme != "https" or not parts.hostname:
        return False
    host = parts.hostname.lower()
    return any(host == s or host.endswith("." + s) for s in ALLOWED_HOST_SUFFIXES)


class _ValidatingRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects only when every hop stays https + allowlisted."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        if not _host_allowed(newurl):
            raise RuntimeError(f"refusing redirect to non-allowlisted host: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_ValidatingRedirect)


def _validated_local(path: str) -> Path:
    p = Path(path)
    if ".." in p.parts:
        raise ValueError(f"local path must not contain '..' segments: {p}")
    return p


def _validated_member(name: str) -> str:
    if ".." in Path(name).parts or name.startswith(("/", "\\")) or ":" in name[:3]:
        raise ValueError(f"archive member rejected (traversal shape): {name!r}")
    return name


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while chunk := fh.read(CHUNK):
            h.update(chunk)
    return h.hexdigest()


def load_register() -> dict:
    if REGISTER.exists():
        return json.loads(REGISTER.read_text(encoding="utf-8"))
    return {"schema": "binary_attest.v1", "rows": []}


def save_register(reg: dict) -> None:
    REGISTER.write_text(json.dumps(reg, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")


def _download(url: str, dest: Path) -> None:
    if not _host_allowed(url):
        raise ValueError(f"URL host not allowlisted (https + release hosts only): {url}")
    with _OPENER.open(url, timeout=300) as resp, open(dest, "wb") as out:
        while chunk := resp.read(CHUNK):
            out.write(chunk)


def cmd_add(args: argparse.Namespace) -> int:
    try:
        local = _validated_local(args.path)
        member = _validated_member(args.archive_member)
    except ValueError as exc:
        print(f"USAGE-ERROR: {exc}")
        return 2
    if not local.is_file():
        print(f"USAGE-ERROR: no such file {local}")
        return 2
    if args.skip_compare:
        # short-circuit BEFORE any download (skip-compare records a local
        # hash-only row; fetching first would be both waste and surprise)
        local_sha = sha256_file(local)
        row = {
            "path": str(local),
            "bytes": local.stat().st_size,
            "sha256": local_sha,
            "source": {
                "kind": "local-hash-only",
                "url": args.source_url,
                "archive_member": member,
                "archive_sha256": None,
            },
            "verified_at": _now(),
            "verified_how": "local-hash-only (skip-compare)",
        }
        reg = load_register()
        reg["rows"] = [r for r in reg["rows"] if r["path"] != row["path"]]
        reg["rows"].append(row)
        save_register(reg)
        print(f"ADDED (no compare): {local} sha256 {local_sha}")
        return 0
    with tempfile.TemporaryDirectory(prefix="binattest_") as td:
        tdp = Path(td)
        archive = Path(args.archive) if args.archive else tdp / "archive.bin"
        if args.archive:
            if not archive.is_file() or ".." in archive.parts:
                print(f"USAGE-ERROR: --archive not a readable file: {archive}")
                return 2
        else:
            print(f"downloading {args.source_url} ...")
            try:
                _download(args.source_url, archive)
            except Exception as exc:  # noqa: BLE001 - report, never crash
                print(f"IO-ERROR: download failed: {exc!r}")
                return 2
        archive_sha = sha256_file(archive)
        print(f"archive sha256 {archive_sha} ({archive.stat().st_size} bytes)")
        try:
            with zipfile.ZipFile(archive) as zf:
                if member not in zf.namelist():
                    print(f"USAGE-ERROR: member {member!r} not in archive; "
                          f"members: {zf.namelist()[:20]}")
                    return 2
                member_bytes = zf.read(member)
        except zipfile.BadZipFile:
            print("USAGE-ERROR: archive is not a zip (non-zip sources: use "
                  "--skip-compare to record a local-hash-only row)")
            return 2
    member_sha = hashlib.sha256(member_bytes).hexdigest()
    local_sha = sha256_file(local)
    row = {
        "path": str(local),
        "bytes": local.stat().st_size,
        "sha256": local_sha,
        "source": {
            "kind": "official-release-archive",
            "url": args.source_url,
            "archive_member": member,
            "archive_sha256": archive_sha,
        },
        "verified_at": _now(),
        "verified_how": "download+extract+byte-compare",
    }
    if member_sha != local_sha or len(member_bytes) != local.stat().st_size:
        print(f"MISMATCH: local {local_sha} vs official {member_sha} — "
              f"the installed file is NOT the release artifact")
        return 1
    reg = load_register()
    reg["rows"] = [r for r in reg["rows"] if r["path"] != row["path"]]
    reg["rows"].append(row)
    save_register(reg)
    print(f"PROVEN-OFFICIAL: {local} == {member} (sha256 {local_sha[:16]}...)")
    return 0


def cmd_verify(_: argparse.Namespace) -> int:
    reg = load_register()
    if not reg["rows"]:
        print("REGISTER-EMPTY: nothing to verify (add rows first)")
        return 2
    bad = 0
    for row in reg["rows"]:
        p = Path(row["path"])
        if not p.is_file():
            print(f"MISSING  {p}")
            bad += 1
            continue
        size = p.stat().st_size
        digest = sha256_file(p)
        if digest != row["sha256"] or size != row["bytes"]:
            print(f"DRIFT    {p} registered {row['sha256'][:16]}... "
                  f"now {digest[:16]}... — the binary CHANGED since attestation")
            bad += 1
        else:
            print(f"MATCH    {p} {digest[:16]}...")
    if bad:
        print(f"BINARY-ATTEST: FAIL — {bad} row(s) missing or drifted of "
              f"{len(reg['rows'])}")
        return 1
    print(f"BINARY-ATTEST: PASS — {len(reg['rows'])} row(s) verified")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    reg = load_register()
    for row in reg["rows"]:
        print(f"{row['sha256'][:16]}...  {row['bytes']:>12}  "
              f"{row['verified_at']}  {row['path']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="binary_attest")
    sub = ap.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add", help="attest a local file against a release archive")
    add.add_argument("path")
    add.add_argument("--source-url", required=True)
    add.add_argument("--archive-member", required=True)
    add.add_argument("--archive", default=None,
                     help="use this local archive instead of downloading "
                          "--source-url (attest many members from one "
                          "download; the url is still recorded as source)")
    add.add_argument("--skip-compare", action="store_true",
                     help="record the local hash without a download (unverified row)")
    add.set_defaults(fn=cmd_add)
    ver = sub.add_parser("verify", help="re-walk the register against local bytes")
    ver.set_defaults(fn=cmd_verify)
    lst = sub.add_parser("list", help="list register rows")
    lst.set_defaults(fn=cmd_list)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
