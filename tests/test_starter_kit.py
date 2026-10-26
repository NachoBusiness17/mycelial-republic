"""The starter kit's scrub law + clean-boot contract (2026-10-04).

THE NO-BUSINESS LAW: the kit ships method, organs, workflows - never the
origin estate's private data. Enforced three ways: (1) a name/path
denylist asserted over every shipped file, (2) the kit's own profile_boot
clean-boot contract (first boot creates the shape, exit 1), and (3) the
doctor responds. The kit is assembled by hand from kit-authored sources;
this test is the gate that keeps it shippable.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "starter-kit"

# the origin's private surface: these strings never ship
DENY = [
    "foste", "sofan", "itscommodore", "nachobiquixotic", "nachobusiness",
    "nach.", "vixhal", "liambraus", "C:/Users", "C:\\Users",
    "z.ai", "hermes_burn", "vastai", "vast.ai", "XAI_SD",
]


def _kit_files() -> list[Path]:
    # .mimosa/ is the host hook's runtime state (live workflow lanes drop
    # session files there while running); it is not kit content and never
    # ships (.gitignore excludes it)
    return [p for p in KIT.rglob("*")
            if p.is_file()
            and ".profile-selftest" not in p.parts
            and ".mimosa" not in p.parts
            and ".law-gate-profile" not in p.parts]


def test_no_business_strings_anywhere():
    files = _kit_files()
    assert files, "starter-kit is empty"
    # the kit's own canonical home is public by design (operator-named
    # repo); the bare account name everywhere else stays denied
    CANONICAL = "github.com/nachobusiness17/mag-sovereign-seed"
    bad = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        text = text.replace(CANONICAL, "<canonical-repo>")
        for d in DENY:
            if d.lower() in text:
                bad.append(f"{f.relative_to(KIT)}: contains {d!r}")
    assert not bad, "BUSINESS LEAK:\n" + "\n".join(bad[:15])


def test_core_docs_present():
    for doc in ("README.md", "INSTALL.md", "BOOT.md", "LAWS.md",
                "PROTOCOLS.md", "SUBSYSTEMS.md", "ZEITGEIST.md",
                "ARMORY.md", "laws/laws.json", "laws/laws.schema.json",
                "tutorial/TUTORIAL.md", ".env.example", ".gitignore",
                "tools/profile_boot.py", "tools/kit_doctor.py",
                "tools/law_gate.py",
                "agent/conversation-miner.md", "agent/profile-grower.md",
                "agent/law-minter.md", "integrations/hermes/README.md",
                "integrations/android/README.md",
                "setup/install.sh", "setup/install.ps1"):
        assert (KIT / doc).is_file(), f"missing: {doc}"


def test_law_gate_green_and_failing_modes(tmp_path):
    """The Lessig organ: green on the shipped carrier; a broken carrier
    and a missing .gitignore both fail it."""
    py = sys.executable
    r = subprocess.run([py, str(KIT / "tools" / "law_gate.py")],
                       capture_output=True, text=True, cwd=str(KIT))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "LAW GATE: PASS" in r.stdout
    # the carrier loader rejects a broken law row; copy only the needed
    # subset (the live 50-wide lanes churn the kit dir concurrently -
    # a whole-tree copytree races with them)
    import shutil as _sh
    broken = tmp_path / "kit"
    (broken / "laws").mkdir(parents=True)
    (broken / "tools").mkdir(parents=True)
    _sh.copy2(KIT / "tools" / "law_gate.py", broken / "tools" / "law_gate.py")
    _sh.copy2(KIT / "tools" / "profile_boot.py", broken / "tools" / "profile_boot.py")
    _sh.copy2(KIT / "laws" / "laws.json", broken / "laws" / "laws.json")
    _sh.copy2(KIT / ".gitignore", broken / ".gitignore")
    carrier = broken / "laws" / "laws.json"
    c = json.loads(carrier.read_text(encoding="utf-8"))
    c["laws"].append({"id": "bad", "statement": "", "why": "", "enforcement": {}})
    carrier.write_text(json.dumps(c), encoding="utf-8")
    r2 = subprocess.run([py, str(broken / "tools" / "law_gate.py")],
                        capture_output=True, text=True, cwd=str(broken))
    assert r2.returncode == 1 and "CARRIER" in r2.stdout
    # never-commit law without its .gitignore fails high
    (broken / ".gitignore").unlink()
    r3 = subprocess.run([py, str(broken / "tools" / "law_gate.py")],
                        capture_output=True, text=True, cwd=str(broken))
    assert r3.returncode == 1 and "gitignore" in r3.stdout.lower()


def test_clean_boot_contract(tmp_path):
    """First boot: no profile -> creates the shape, exit 1. Second run:
    profile found with rows -> exit 0."""
    py = sys.executable
    mem = tmp_path / "memory"
    r1 = subprocess.run([py, str(KIT / "tools" / "profile_boot.py"),
                         "--memory", str(mem)], capture_output=True, text=True)
    assert r1.returncode == 1, r1.stdout + r1.stderr
    assert "FIRST BOOT" in r1.stdout
    assert (mem / "MEMORY.md").is_file()
    # one topic file + index row -> found
    (mem / "first-fact.md").write_text(
        "---\nname: first-fact\ndescription: the first mined fact\n"
        "metadata:\n  type: user\n---\nsomething true\n", encoding="utf-8")
    idx = mem / "MEMORY.md"
    idx.write_text(idx.read_text(encoding="utf-8")
                   + "\n- [First fact](first-fact.md) - the first mined fact\n",
                   encoding="utf-8")
    r2 = subprocess.run([py, str(KIT / "tools" / "profile_boot.py"),
                         "--memory", str(mem)], capture_output=True, text=True)
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert "first mined fact" in r2.stdout  # the boot brief carries it


def test_phantom_detection(tmp_path):
    mem = tmp_path / "memory"
    mem.mkdir()
    (mem / "MEMORY.md").write_text(
        "- [Ghost](ghost.md) - a link to nothing\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(KIT / "tools" / "profile_boot.py"),
                        "--memory", str(mem)], capture_output=True, text=True)
    assert r.returncode == 2, r.stdout + r1_s(r.stderr)
    assert "phantom" in r.stdout.lower()


def r1_s(s: str) -> str:
    return s
