"""Junction-policy tests for mag.catalog_scan (B2-76, 2026-09-26).

The policy spec lives in mag/catalog_scan.py module docstring; law sources
are watch/inbox/LINKS.jsonl XIDIG-WIN-* 2026-09-26 (Microsoft Learn,
verified-live). The walker test creates a REAL NTFS junction via
_winapi.CreateJunction (no privilege needed) and proves the v2 disease is
dead: a mirrored tree is counted once, at its real path, with the
junction recorded to the ledger, never descended.
"""
import os
import sys

import pytest

from mag.catalog_scan import (
    FILE_ATTRIBUTE_REPARSE_POINT,
    IO_REPARSE_TAG_MOUNT_POINT,
    REPARSE_DATA_CAP_BYTES,
    classify_target,
    reparse_record,
    scan_tree,
)

pytestmark = pytest.mark.skipif(sys.platform != "win32",
                                reason="junction policy is Windows law")


def test_classify_target_device_local_is_not_network():
    # The \\?\ prefix is a win32 device namespace, still a local volume.
    # The live estate junction reads back exactly this shape.
    cls, note = classify_target("\\\\?\\C:\\Users\\foste\\memory\\training")
    assert cls == "device_local"
    assert "local volume" in note


def test_classify_target_unc_server_share():
    cls, note = classify_target("\\\\server\\share\\dir")
    assert cls == "unc_remote"
    assert "network" in note


def test_classify_target_device_unc():
    cls, _ = classify_target("\\\\?\\UNC\\server\\share\\dir")
    assert cls == "unc_remote"


def test_classify_target_local_volume():
    # XIDIG-WIN-JUNCTION-RULES permitted example: C:\dirx -> D:\diry.
    cls, _ = classify_target("D:\\diry")
    assert cls == "local_volume"


def test_classify_target_relative():
    cls, note = classify_target("dir\\sub")
    assert cls == "relative"
    assert "XIDIG-WIN-SYMLINK-RULES" in note


def test_classify_target_over_cap():
    # A target whose repr alone exceeds 16 KB cannot be a legal payload.
    cls, note = classify_target("C:\\" + "a" * (REPARSE_DATA_CAP_BYTES + 1))
    assert cls == "over_cap"
    assert "XIDIG-WIN-REPARSE-LAW" in note


def _make_junction(junction_path, target_dir):
    # _winapi.CreateJunction(src, dst): junction lands at dst, points at src.
    import _winapi
    _winapi.CreateJunction(str(target_dir), str(junction_path))


def test_scan_tree_prunes_junction_and_records_it(tmp_path):
    real = tmp_path / "memory_training"
    real.mkdir()
    (real / "weights.json").write_text("{}", encoding="utf-8")
    link = tmp_path / "training"
    _make_junction(link, real)

    stats = {}
    events = list(scan_tree(str(tmp_path), stats))
    rows = [payload for kind, payload in events if kind == "row"]
    recs = [payload for kind, payload in events if kind == "record"]

    weights = [r for r in rows if r["path"].endswith("weights.json")]
    assert len(weights) == 1, "mirrored tree must be counted exactly once"
    assert weights[0]["path"].replace("\\", "/").startswith("memory_training/")

    under_junction = [r for r in rows
                      if r["path"].replace("\\", "/").startswith("training/")]
    assert under_junction == [], "junction must never be descended (P1)"

    assert len(recs) == 1
    rec = recs[0]
    assert rec["kind"] == "junction"
    assert rec["tag"] == "0x%08X" % IO_REPARSE_TAG_MOUNT_POINT
    assert rec["is_dir"] is True
    assert rec["action"] == "pruned"
    assert rec["target_class"] in ("device_local", "local_volume"), \
        "local junction target must not read as network (P3 device-path law)"
    assert rec["violation"] is False
    assert rec["reparse_data_cap_bytes"] == 16 * 1024
    assert rec["path_limit_law"] == "63 per path, 31 fully qualified target"

    assert stats["rows"] == 1
    assert stats["dups"] == 0
    assert stats["reparse_dirs"] == 1
    assert stats["reparse_files"] == 0
    assert stats["records"] == 1


def test_junction_to_file_is_violation(tmp_path):
    # XIDIG-WIN-JUNCTION-RULES: junctions link directories only, never
    # files. reparse_record takes is_dir from the caller (the walker's
    # lstat branch), so pass is_dir=False to drive the non-dir branch (P3).
    real = tmp_path / "memory_training"
    real.mkdir()
    (real / "weights.json").write_text("{}", encoding="utf-8")
    link = tmp_path / "training"
    _make_junction(link, real)
    lst = os.lstat(str(link))
    assert lst.st_file_attributes & FILE_ATTRIBUTE_REPARSE_POINT

    rec = reparse_record(str(link), "training", lst, is_dir=False)
    assert rec["kind"] == "junction"
    assert rec["is_dir"] is False
    assert rec["action"] == "recorded_no_follow"
    assert rec["violation"] is True
    assert "directories only" in rec["note"]


def test_symlink_unc_is_contrast_not_violation(tmp_path, monkeypatch):
    # XIDIG-WIN-SYMLINK-RULES: a symlink MAY target UNC directly; the
    # same target class is a violation for a junction. Drive the record
    # builder with a symlink tag and a readlink stub, no OS symlink needed.
    class FakeLst:
        st_reparse_tag = 0xA0000000
        st_mode = 0o120777

    monkeypatch.setattr(os, "readlink", lambda p: "\\\\server\\share\\docs")
    rec = reparse_record(str(tmp_path / "lnk"), "external/docs_link",
                         FakeLst(), is_dir=True)
    assert rec["kind"] == "symlink"
    assert rec["target_class"] == "unc_remote"
    assert rec["violation"] is False
    assert "XIDIG-WIN-SYMLINK-RULES" in rec["note"]

    # Same class on a junction tag flips the violation (the law split).
    class FakeJunc(FakeLst):
        st_reparse_tag = 0xA0000003

    rec2 = reparse_record(str(tmp_path / "jn"), "external/jn",
                          FakeJunc(), is_dir=True)
    assert rec2["kind"] == "junction"
    assert rec2["violation"] is True
    assert "never network" in rec2["note"]
