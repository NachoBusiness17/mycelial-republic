"""tests/test_estate_cleanup.py — fixture-tree tests for tools/estate_cleanup.py.

Covers the AA2 mission contract:
  1. a fixture junk tree is enumerated exactly (right paths, right bytes,
     nested non-junk spared);
  2. default run is a dry-run (nothing touched);
  3. --apply removes the fixtures and leaves non-junk untouched — including
     the reserved-name `nul` file on Windows (created via the `\\\\?\\`
     literal-name prefix, deleted via the `del \\\\.\\C:\\...\\nul` device path).

The real repo tree is NEVER a fixture here: all tests build their own tree
under tmp_path (pytest tmp), so no test can delete estate files.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

_TOOLS = Path(__file__).resolve().parent.parent / "tools"
_SPEC = importlib.util.spec_from_file_location("estate_cleanup", _TOOLS / "estate_cleanup.py")
estate_cleanup = importlib.util.module_from_spec(_SPEC)
sys.modules.setdefault("estate_cleanup", estate_cleanup)
_SPEC.loader.exec_module(estate_cleanup)

IS_NT = os.name == "nt"


def _write(path: Path, data: bytes) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


def _write_reserved_nul(root: Path, data: bytes = b"x" * 51) -> None:
    """Create a LITERAL file named 'nul'. On Windows the plain path resolves
    to the NUL device, so creation must go through the `\\\\?\\` prefix that
    disables DOS name resolution."""
    root.mkdir(parents=True, exist_ok=True)
    if IS_NT:
        literal = "\\\\?\\" + str(root / "nul")
        with open(literal, "wb") as fh:
            fh.write(data)
    else:
        (root / "nul").write_bytes(data)


def build_fixture(root: Path) -> dict[str, int]:
    """Junk + non-junk fixture tree. Returns expected junk bytes per path."""
    sizes: dict[str, int] = {}
    # --- junk (root-level, one per category, sizes chosen distinct) ---
    _write_reserved_nul(root)
    sizes["nul"] = 51
    sizes["UsersfosteAppDataLocalTempddg1.html"] = _write(
        root / "UsersfosteAppDataLocalTempddg1.html", b"<html>path bug</html>"
    )
    sizes["UsersfosteAppDataLocalTempfwthieves.html"] = _write(
        root / "UsersfosteAppDataLocalTempfwthieves.html", b"j" * 4096
    )
    sizes["_s218_routes.json"] = _write(root / "_s218_routes.json", b"{}" * 100)
    sizes["_s218_build.py"] = _write(root / "_s218_build.py", b"print('debris')\n")
    sizes["braid_test.out"] = _write(root / "braid_test.out", b"out\n")
    sizes["sweep_llama.json"] = _write(root / "sweep_llama.json", b"[]")
    sizes["sweep_llama2.json"] = _write(root / "sweep_llama2.json", b"[1, 2]" * 50)
    sizes["stealth-tools.check.txt"] = _write(root / "stealth-tools.check.txt", b"ok\n")
    gopher_bytes = _write(root / "tmp_gopher" / "amdgpu_usage.rst", b"g" * 1000)
    gopher_bytes += _write(root / "tmp_gopher" / "sub" / "llama_arg.cpp", b"c" * 2000)
    sizes["tmp_gopher"] = gopher_bytes
    # --- non-junk neighbors that must be spared ---
    _write(root / "main.py", b"print('estate')\n")
    _write(root / "sweep_llama_notes.md", b"notes, not the .json scratch\n")  # ext mismatch
    _write(root / "_s218x.json", b"no underscore after s218\n")  # pattern miss
    _write(root / "tools" / "keep.py", b"# subdir, never scanned\n")
    _write_reserved_nul(root / "sub")  # nested reserved name: root-only scan must miss it
    return sizes


def test_enumerate_matches_fixture_exactly(tmp_path: Path) -> None:
    sizes = build_fixture(tmp_path)
    items = estate_cleanup.enumerate_junk(tmp_path)
    got = {item.path: item.bytes for item in items}
    assert got == sizes
    by_cat: dict[str, set[str]] = {}
    for item in items:
        by_cat.setdefault(item.category, set()).add(item.path)
    assert by_cat["nul-reserved"] == {"nul"}
    assert by_cat["path-bug-dumps"] == {
        "UsersfosteAppDataLocalTempddg1.html",
        "UsersfosteAppDataLocalTempfwthieves.html",
    }
    assert by_cat["s218-build-debris"] == {"_s218_routes.json", "_s218_build.py"}
    assert by_cat["braid-scratch"] == {"braid_test.out"}
    assert by_cat["sweep-llama-scratch"] == {"sweep_llama.json", "sweep_llama2.json"}
    assert by_cat["tmp-gopher-dig"] == {"tmp_gopher"}
    assert by_cat["stealth-check-scratch"] == {"stealth-tools.check.txt"}
    # directory byte cost is the recursive st_size sum, not the dirent size
    gopher = next(i for i in items if i.path == "tmp_gopher")
    assert (gopher.kind, gopher.file_count) == ("dir", 2)
    # nested reserved-name file and lookalike names are NOT flagged
    assert not any("/" in i.path for i in items)
    assert "sweep_llama_notes.md" not in got and "_s218x.json" not in got
    # reserved delete action only on Windows for the literal nul
    for item in items:
        expected = "win32_reserved" if (IS_NT and item.path == "nul") else "plain"
        assert item.delete_action == expected


def test_default_run_is_dry_run_and_touches_nothing(tmp_path: Path, capsys) -> None:
    build_fixture(tmp_path)
    rc = estate_cleanup.main(["--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "DRY-RUN (nothing touched)" in out
    assert "TOTAL RECLAIMABLE" in out
    junk_names = [
        "nul",
        "UsersfosteAppDataLocalTempddg1.html",
        "_s218_routes.json",
        "braid_test.out",
        "sweep_llama2.json",
        "stealth-tools.check.txt",
    ]
    for name in junk_names:
        assert estate_cleanup.entry_exists(tmp_path, name), f"dry-run deleted {name}"
    assert (tmp_path / "tmp_gopher" / "sub" / "llama_arg.cpp").exists()


def test_apply_removes_fixtures_and_spares_non_junk(tmp_path: Path, capsys) -> None:
    build_fixture(tmp_path)
    rc = estate_cleanup.main(["--root", str(tmp_path), "--apply"])
    assert rc == 0, capsys.readouterr().out
    # every junk entry is gone from the directory listing (scandir truth;
    # os.path.exists lies for `nul` because dir\nul resolves to the device)
    for name in [
        "nul",
        "UsersfosteAppDataLocalTempddg1.html",
        "UsersfosteAppDataLocalTempfwthieves.html",
        "_s218_routes.json",
        "_s218_build.py",
        "braid_test.out",
        "sweep_llama.json",
        "sweep_llama2.json",
        "stealth-tools.check.txt",
    ]:
        assert not estate_cleanup.entry_exists(tmp_path, name), f"{name} survived --apply"
    assert not (tmp_path / "tmp_gopher").exists()
    # non-junk untouched
    assert (tmp_path / "main.py").exists()
    assert (tmp_path / "sweep_llama_notes.md").exists()
    assert (tmp_path / "_s218x.json").exists()
    assert (tmp_path / "tools" / "keep.py").exists()
    assert estate_cleanup.entry_exists(tmp_path / "sub", "nul"), "nested nul must be spared"
    # post-apply re-enumeration (the fail-loud survivor check) sees nothing
    assert estate_cleanup.enumerate_junk(tmp_path) == []


def test_json_report_totals_match_fixture(tmp_path: Path, capsys) -> None:
    sizes = build_fixture(tmp_path)
    rc = estate_cleanup.main(["--root", str(tmp_path), "--json"])
    assert rc == 0
    import json

    payload = json.loads(capsys.readouterr().out)
    assert payload["applied"] is False
    assert payload["total_bytes"] == sum(sizes.values())
    assert payload["total_files"] == 11  # 9 single files + 2 inside tmp_gopher


@pytest.mark.skipif(not IS_NT, reason="reserved-name delete is a Win32 device-path mechanic")
def test_windows_reserved_nul_device_delete(tmp_path: Path) -> None:
    """The estate's real `nul` pain, proven on a fixture: os.path.exists says
    True forever (device shadow), the `del \\\\.\\C:\\...\\nul` syntax removes
    the literal file, and scandir is the only honest existence check."""
    _write_reserved_nul(tmp_path, b"reserved" * 4)
    assert estate_cleanup.entry_exists(tmp_path, "nul")
    items = estate_cleanup.enumerate_junk(tmp_path)
    (nul_item,) = [i for i in items if i.path == "nul"]
    assert nul_item.bytes == 32 and nul_item.delete_action == "win32_reserved"
    estate_cleanup.apply_removals(tmp_path, [nul_item])
    assert not estate_cleanup.entry_exists(tmp_path, "nul")
    # the device shadow persists after removal — the documented trap
    assert os.path.exists(tmp_path / "nul")
