"""tests for mag/kv_seal.py — ask A7 salt-and-seal KV pages.

Offline only, $0, stdlib only: seal/verify roundtrip, tampered-byte rejection,
tenant-salt isolation, unsealed/missing-page refill routing, and the refill
stub hook contract. No network, no upstream KV.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import kv_seal as ks  # noqa: E402

PAGE = b"tenant-7/page-0001: the mag estate remembers its own"


def test_roundtrip_seal_then_verify_passes(tmp_path):
    p = tmp_path / "page.bin"
    p.write_bytes(PAGE)
    rec = ks.seal_page(p, "salt-tenant-7")
    assert rec["ok"] is True
    assert p.with_suffix(p.suffix + ks.SIDECAR_SUFFIX).is_file()  # sidecar lives beside the page
    v = ks.verify_page(p, "salt-tenant-7")
    assert v["ok"] is True
    assert v["refill"] is False
    assert v["digest"] == rec["digest"]
    assert v["size"] == len(PAGE)


def test_tampered_byte_fails_and_routes_to_refill(tmp_path):
    p = tmp_path / "page.bin"
    p.write_bytes(PAGE)
    ks.seal_page(p, "salt-tenant-7")
    # flip exactly ONE bit of ONE byte — the smallest possible tamper
    data = bytearray(p.read_bytes())
    data[3] ^= 0x01
    assert bytes(data) != PAGE
    p.write_bytes(bytes(data))
    v = ks.verify_page(p, "salt-tenant-7")
    assert v["ok"] is False
    assert v["refill"] is True
    assert v["reason"] == "digest-mismatch"
    # the caller's contract: delete + refill via the stub hook
    p.unlink()
    hook = ks.refill_page(p)
    assert hook["stub"] is True and hook["action"] == "refill"


def test_salt_isolation_cross_tenant_verify_fails(tmp_path):
    p = tmp_path / "page.bin"
    p.write_bytes(PAGE)
    ks.seal_page(p, "salt-tenant-7")
    v = ks.verify_page(p, "salt-tenant-8")
    assert v["ok"] is False
    assert v["refill"] is True


def test_unsealed_and_missing_pages_require_refill(tmp_path):
    p = tmp_path / "page.bin"
    p.write_bytes(PAGE)
    v_unsealed = ks.verify_page(p, "salt-tenant-7")  # page there, sidecar absent
    assert v_unsealed["ok"] is False and v_unsealed["refill"] is True
    assert v_unsealed["reason"] == "sidecar-missing"
    v_missing = ks.verify_page(tmp_path / "nope.bin", "salt-tenant-7")
    assert v_missing["ok"] is False and v_missing["refill"] is True
    assert v_missing["reason"] == "page-missing"


def test_refill_stub_never_touches_filesystem_and_empty_salt_rejected(tmp_path):
    p = tmp_path / "page.bin"
    hook = ks.refill_page(p)
    assert hook["stub"] is True
    assert not p.exists()  # the stub writes nothing, deletes nothing
    for bad in ("", b""):
        try:
            ks.seal_page(p, bad)
            raise AssertionError("empty tenant_salt must be rejected")
        except ValueError:
            pass
