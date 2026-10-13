"""binary_attest tests — fixture archives, zero network, zero repo writes.

Covers: host allowlist (SSRF fence), traversal-shaped paths and members
refused, add/verify/list round-trip against a temp register, tamper detection
on verify, and the skip-compare honest row shape. The register path is
monkeypatched to tmp_path so the repo's configs/ is never touched here.
"""
from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import binary_attest as ba  # noqa: E402


@pytest.fixture()
def register_at(tmp_path, monkeypatch):
    reg = tmp_path / "binary_register.json"
    monkeypatch.setattr(ba, "REGISTER", reg)
    return reg


def _fixture_archive(tmp_path: Path, name: str = "bin.exe", payload: bytes = b"OFFICIAL-BYTES") -> Path:
    zpath = tmp_path / "rel.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("readme.txt", "release notes")
        zf.writestr(f"sub/{name}", payload)
    return zpath


def test_host_allowlist_blocks_private_and_http():
    for url in ("http://github.com/x", "https://127.0.0.1/x",
                "https://169.254.169.254/latest/meta-data",
                "https://evil-github.com/x", "https://github.com.evil.io/x",
                "file:///etc/passwd"):
        assert ba._host_allowed(url) is False, url
    for url in ("https://github.com/o/r/releases/download/v1/a.zip",
                "https://objects.githubusercontent.com/run/1/bin",
                "https://api.adoptium.net/v3/binary/x"):
        assert ba._host_allowed(url) is True, url


def test_traversal_shapes_refused():
    with pytest.raises(ValueError):
        ba._validated_local("../escape.exe")
    with pytest.raises(ValueError):
        ba._validated_member("../evil.exe")
    with pytest.raises(ValueError):
        ba._validated_member("C:/windows/system32/evil.exe")


def test_add_verify_roundtrip(tmp_path, register_at, monkeypatch):
    payload = b"OFFICIAL-BYTES"
    zpath = _fixture_archive(tmp_path, payload=payload)
    local = tmp_path / "installed.exe"
    local.write_bytes(payload)
    # point _download at the fixture by monkeypatching it to a file copy
    monkeypatch.setattr(ba, "_download",
                        lambda url, dest: dest.write_bytes(zpath.read_bytes()))
    rc = ba.main(["add", str(local), "--source-url",
                  "https://github.com/o/r/releases/download/v1/rel.zip",
                  "--archive-member", "sub/bin.exe"])
    assert rc == 0
    rows = json_rows(register_at)
    assert len(rows) == 1
    assert rows[0]["sha256"] == hashlib.sha256(payload).hexdigest()
    assert rows[0]["verified_how"].startswith("download+extract")
    assert ba.main(["verify"]) == 0


def json_rows(reg: Path):
    import json
    if not reg.exists():
        return []  # mismatch exits before any register write; no file = no rows
    return json.loads(reg.read_text(encoding="utf-8"))["rows"]


def test_mismatch_fails_loud(tmp_path, register_at, monkeypatch):
    zpath = _fixture_archive(tmp_path, payload=b"OFFICIAL")
    local = tmp_path / "tampered.exe"
    local.write_bytes(b"TAMPERED-DIFFERENT")
    monkeypatch.setattr(ba, "_download",
                        lambda url, dest: dest.write_bytes(zpath.read_bytes()))
    rc = ba.main(["add", str(local), "--source-url",
                  "https://github.com/o/r/releases/download/v1/rel.zip",
                  "--archive-member", "sub/bin.exe"])
    assert rc == 1  # mismatch is exit 1, and nothing was registered
    assert json_rows(register_at) == []


def test_verify_detects_drift(tmp_path, register_at, monkeypatch):
    payload = b"ORIGINAL"
    zpath = _fixture_archive(tmp_path, payload=payload)
    local = tmp_path / "bin.exe"
    local.write_bytes(payload)
    monkeypatch.setattr(ba, "_download",
                        lambda url, dest: dest.write_bytes(zpath.read_bytes()))
    assert ba.main(["add", str(local), "--source-url",
                    "https://github.com/o/r/releases/download/v1/rel.zip",
                    "--archive-member", "sub/bin.exe"]) == 0
    local.write_bytes(b"SWAPPED-OUT")  # the binary changed after attestation
    assert ba.main(["verify"]) == 1


def test_skip_compare_marks_row_unverified(tmp_path, register_at, monkeypatch):
    local = tmp_path / "local-only.exe"
    local.write_bytes(b"NO-ARCHIVE")
    monkeypatch.setattr(ba, "_download",
                        lambda url, dest: pytest.fail("skip-compare must not download"))
    rc = ba.main(["add", str(local), "--source-url",
                  "https://github.com/o/r/releases/download/v1/rel.zip",
                  "--archive-member", "x", "--skip-compare"])
    assert rc == 0
    row = json_rows(register_at)[0]
    assert row["verified_how"].startswith("local-hash-only")
