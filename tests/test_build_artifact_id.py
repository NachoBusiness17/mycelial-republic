"""R6 ARTIFACT ID tests (Q09, last_mile 2026-09-30).

The build artifact must be verifiable: scripts/build_game.ps1 stamps the
exported exe with a trailer pinning (source git sha, pck sha256); the
game's BootIntegrity autoload (roblox_to_godot/core/boot_integrity.gd)
reads the stamp at boot, hashes the pck beside the exe, prints
"ARTIFACT_ID ..." to stderr and exits 1 when the pck does not match.

These tests run the REAL pipeline: one export per session (module fixture),
then boot the real exe intact, with a byte-swapped pck, and with the pck
removed. Receipt: watch/inbox/last_mile_20260930/R6_ARTIFACT_ID.md.
"""

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
BUILD_DIR = REPO / "build" / "mountain-windows"
EXE = BUILD_DIR / "TheMountain.exe"
PCK = BUILD_DIR / "TheMountain.pck"
MANIFEST = BUILD_DIR / "mountain-manifest.json"
BUILD_SCRIPT = REPO / "scripts" / "build_game.ps1"
MAGIC = b"MAGSTMP1"
BOOT_ARGS = ["--headless", "--quit-after", "2"]


def _godot_available() -> bool:
    cands = [REPO / "tools" / "godot" / "Godot_v4.3-stable_win64_console.exe",
             REPO / "tools" / "godot" / "Godot_v4.3-stable_win64.exe"]
    return shutil.which("godot") is not None or any(c.exists() for c in cands)


def read_stamp(exe_path: Path) -> dict:
    """Mirror of core/boot_integrity.gd's trailer read, byte for byte.

    Trailer layout: [ exe ][ JSON payload ][ MAGSTMP1 ][ u32 LE len(payload) ].
    """
    data = exe_path.read_bytes()
    assert len(data) >= 20
    plen = int.from_bytes(data[-4:], "little")
    assert data[-12:-4] == MAGIC, "no stamp trailer on exe"
    assert 2 < plen <= 4096, f"stamp payload length out of range: {plen}"
    payload = data[-12 - plen : -12]
    return json.loads(payload.decode("utf-8"))


def boot(exe_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(exe_path)] + BOOT_ARGS,
        capture_output=True, text=True, timeout=120, cwd=str(exe_path.parent),
    )


@pytest.fixture(scope="module")
def stamped_build():
    """One real pipeline run per session: export + stamp + boot smoke."""
    if not _godot_available():
        pytest.skip("no Godot 4.3 binary (tools/godot/ or PATH) - cannot export")
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", str(BUILD_SCRIPT)],
        capture_output=True, text=True, timeout=900, cwd=str(REPO),
    )
    assert proc.returncode == 0, f"build script failed:\n{proc.stdout[-4000:]}\n{proc.stderr[-4000:]}"
    return proc.stdout


def test_stamp_pins_source_sha_and_pck_sha(stamped_build):
    """The exe trailer carries the source repo HEAD sha and the exact pck sha256."""
    stamp = read_stamp(EXE)
    git_head = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    pck_sha = hashlib.sha256(PCK.read_bytes()).hexdigest()
    assert stamp["v"] == 1
    assert stamp["source"] == "estate-twin"
    assert stamp["git"] == git_head, "stamped sha must be the source repo HEAD"
    assert stamp["pck_sha256"].lower() == pck_sha, "stamped pck sha must match the shipped pck"


def test_manifest_agrees_with_artifact(stamped_build):
    """mountain-manifest.json (ships in the zip) agrees with the real bytes."""
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
    exe_sha = hashlib.sha256(EXE.read_bytes()).hexdigest()
    pck_sha = hashlib.sha256(PCK.read_bytes()).hexdigest()
    assert manifest["exe_sha256"].lower() == exe_sha, "manifest exe sha must cover the STAMPED exe"
    assert manifest["pck_sha256"].lower() == pck_sha
    stamp = read_stamp(EXE)
    assert manifest["source_git"] == stamp["git"]


def test_boot_prints_identity_and_exits_zero(stamped_build):
    """Intact artifact: ARTIFACT_ID line with pck=ok, exit code 0."""
    proc = boot(EXE)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, f"intact artifact refused to boot:\n{out}"
    assert "ARTIFACT_ID" in out
    assert "pck=ok" in out
    assert read_stamp(EXE)["git"][:12] in out, "boot must print the stamped git sha"


def test_swapped_pck_fires_detection(stamped_build):
    """THE Q09 THREAT: swap the pck beside the exe -> detection fires.

    Appending one byte changes the pck sha256 without touching the exe;
    boot must print pck=FAIL (SWAPPED PCK) and exit non-zero.
    """
    backup = PCK.with_suffix(".pck.testbak")
    shutil.copy2(PCK, backup)
    try:
        with PCK.open("ab") as f:
            f.write(b"X")
        proc = boot(EXE)
        out = proc.stdout + proc.stderr
        assert proc.returncode != 0, f"swapped pck was NOT detected (exit 0):\n{out}"
        assert "pck=FAIL" in out and "SWAPPED PCK" in out
    finally:
        shutil.move(str(backup), str(PCK))
    # specificity: restore -> boots clean again
    proc = boot(EXE)
    assert proc.returncode == 0 and "pck=ok" in (proc.stdout + proc.stderr)


def test_missing_pck_fires_detection(stamped_build):
    """pck deleted: engine-level detection (named boundary, R6).

    The BootIntegrity autoload lives INSIDE the pck, so with no pck no
    GDScript ever runs - Godot's own loader fires instead: it prints
    "Error: Couldn't load project data ... Is the .pck file missing?"
    and (4.3 engine defect, named here) then hangs instead of exiting.
    The honest assertion: within a bounded window the game neither runs
    nor exits 0, and the error names the missing pck.
    """
    backup = PCK.with_suffix(".pck.testbak")
    shutil.move(str(PCK), str(backup))
    try:
        proc = subprocess.Popen(
            [str(EXE)] + BOOT_ARGS, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, cwd=str(EXE.parent),
        )
        try:
            out, _ = proc.communicate(timeout=20)
            assert proc.returncode != 0, f"missing pck silently ran (exit 0):\n{out}"
            assert "pck file missing" in out or "Couldn't load project data" in out
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
            assert "Is the .pck file missing?" in out, (
                f"no-pck hang without the engine's missing-pck error:\n{out}"
            )
    finally:
        shutil.move(str(backup), str(PCK))
