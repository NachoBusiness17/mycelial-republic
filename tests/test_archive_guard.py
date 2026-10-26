"""tests/test_archive_guard.py - 10-case verification of ArchiveGuard triple-gate protocol."""
from __future__ import annotations

from pathlib import Path
import pytest

from tools.archive_guard import ArchiveGuard


@pytest.fixture
def guard_env(tmp_path: Path):
    orig_dir = tmp_path / "orig"
    copy_dir = tmp_path / "copy"
    trash_dir = tmp_path / "trash"
    orig_dir.mkdir()
    copy_dir.mkdir()
    trash_dir.mkdir()

    guard = ArchiveGuard(trash_dir=trash_dir)
    return {
        "guard": guard,
        "orig_dir": orig_dir,
        "copy_dir": copy_dir,
        "trash_dir": trash_dir,
    }


# Case 1: Cleared a good copy
def test_case_01_good_copy_clears(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "trip_photos_2024.zip"
    copy = guard_env["copy_dir"] / "trip_photos_2024.zip"
    content = b"vacation-photos-archive-bytes-12345"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "External SSD Drive in safe #4",
        "export_complete": True,
    }
    inventory = ["trip_photos_2024.zip"]

    res = guard.clear_to_trash(orig, copy, confirmations, inventory)
    assert res["cleared"] is True
    assert res["action"] == "MOVED_TO_TRASH"
    assert not orig.exists()
    assert (guard_env["trash_dir"] / "trip_photos_2024.zip").exists()
    assert copy.exists()


# Case 2: Refused when second copy confirmation missing
def test_case_02_refuse_missing_second_copy_confirmation(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "music_library.tar"
    copy = guard_env["copy_dir"] / "music_library.tar"
    content = b"music-tracks"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "",  # missing
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert res["action"] == "REFUSED"
    assert orig.exists()  # untouched


# Case 3: Refused when export complete confirmation missing
def test_case_03_refuse_missing_export_complete_confirmation(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "notes.txt"
    copy = guard_env["copy_dir"] / "notes.txt"
    content = b"personal thoughts"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "/Volumes/BackupSSD",
        "export_complete": False,  # incomplete
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert res["action"] == "REFUSED"
    assert orig.exists()  # untouched


# Case 4: Refused when file is a bank statement (protected)
def test_case_04_refuse_bank_statement(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "chase_bank_statement_june.pdf"
    copy = guard_env["copy_dir"] / "chase_bank_statement_june.pdf"
    content = b"pdf-checking-account-ledger"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "NAS Drive",
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert "banking" in str(res["reasons"])
    assert orig.exists()  # untouched


# Case 5: Refused when file is a medical record (protected)
def test_case_05_refuse_medical_record(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "doctor_prescription_clinic.pdf"
    copy = guard_env["copy_dir"] / "doctor_prescription_clinic.pdf"
    content = b"clinic-patient-notes"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "Encrypted Thumbdrive",
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert "medical" in str(res["reasons"])
    assert orig.exists()  # untouched


# Case 6: Refused when file is a tax form (protected)
def test_case_06_refuse_tax_form(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "w2_irs_tax_return_2025.pdf"
    copy = guard_env["copy_dir"] / "w2_irs_tax_return_2025.pdf"
    content = b"tax-filing-data"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "Safety Box",
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert "tax" in str(res["reasons"])
    assert orig.exists()  # untouched


# Case 7: Refused when file is a government ID (protected)
def test_case_07_refuse_government_id(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "passport_scan_license.jpg"
    copy = guard_env["copy_dir"] / "passport_scan_license.jpg"
    content = b"photo-id"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "Safe",
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert "government_id" in str(res["reasons"])
    assert orig.exists()  # untouched


# Case 8: Refused when file is family / children records (protected)
def test_case_08_refuse_family_records(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "minor_child_guardian_papers.docx"
    copy = guard_env["copy_dir"] / "minor_child_guardian_papers.docx"
    content = b"family-court"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "Safe",
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert "family" in str(res["reasons"])
    assert orig.exists()  # untouched


# Case 9: Refused when copy had been altered (hash mismatch)
def test_case_09_refuse_altered_copy(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "dataset.csv"
    copy = guard_env["copy_dir"] / "dataset.csv"
    orig.write_bytes(b"original-clean-data")
    copy.write_bytes(b"corrupted-data-bit-flip")  # altered!

    confirmations = {
        "second_copy_location": "Cold Vault",
        "export_complete": True,
    }
    res = guard.clear_to_trash(orig, copy, confirmations)
    assert res["cleared"] is False
    assert "Live hash mismatch" in str(res["reasons"])
    assert orig.exists()  # untouched


# Case 10: Refused when file wasn't in original inventory list
def test_case_10_refuse_not_in_inventory(guard_env):
    guard = guard_env["guard"]
    orig = guard_env["orig_dir"] / "surprise_file.zip"
    copy = guard_env["copy_dir"] / "surprise_file.zip"
    content = b"surprise-archive"
    orig.write_bytes(content)
    copy.write_bytes(content)

    confirmations = {
        "second_copy_location": "Vault",
        "export_complete": True,
    }
    approved_inventory = ["file_a.zip", "file_b.zip"]  # surprise_file not in list!

    res = guard.clear_to_trash(orig, copy, confirmations, approved_inventory)
    assert res["cleared"] is False
    assert "not in the original approved inventory list" in str(res["reasons"])
    assert orig.exists()  # untouched
