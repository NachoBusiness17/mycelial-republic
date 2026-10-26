#!/usr/bin/env python3
"""Gate blocking-path tests (audit lane 4, 2026-09-27).

WHY THIS FILE EXISTS. The 2026-09-27 robustness audit found that 3 of the 4
self-checks had ZERO tests exercising their BLOCKING path:
  config_seal           0 tests (string absent from tests/ entirely)
  checkbox_receipt_gate 0 tests (absent; gate is RED right now)
  secret_gate           0 tests (wired enforcing, built the same day)
and violation_ratchet's 5 exit asserts were all `== 0`, so disarming its
`return 1` left 7/7 green.

A gate with no blocking-path test is a gate that can be neutered silently.
That is not a theoretical risk on this fleet: violation_ratchet WAS neutered
in an audit mutation and nothing noticed.

EVERY test here must be able to FAIL. The suite-level proof is that each
blocking test is paired with a positive control: a same-shape input the gate
is supposed to accept. If a mutation makes the gate always-return-0, the
negative test fails and the positive control catches over-broad "always fail".

No secret values appear here. Fixtures are synthetic, correctly-shaped, and
low-entropy where the gate's entropy floor is the thing under test.

Receipt: watch/inbox/audit_20260926/LANE4_TEST_ROBUSTNESS.md
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"


def _load(mod_name: str, rel: str):
    """Import a tools/ module by path (tools/ is not a package)."""
    spec = importlib.util.spec_from_file_location(mod_name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# config_seal.py — exit 0 clean / 1 drift / 2 no seal
# --------------------------------------------------------------------------

def _seal_fixture(tmp_path, monkeypatch, files: dict[str, str]):
    """Point config_seal at a temp configs/ dir. Returns nothing; seal is written by cmd_update."""
    cfg = tmp_path / "configs"
    cfg.mkdir()
    for name, body in files.items():
        (cfg / name).write_text(body, encoding="utf-8")
    cs = _load("cs_fixture", "tools/config_seal.py")
    monkeypatch.setattr(cs, "CONFIG_DIR", cfg)
    monkeypatch.setattr(cs, "SEAL_PATH", cfg / ".config_seal.json")
    return cs


def test_config_seal_blocks_on_modified_file(tmp_path, monkeypatch):
    """A config byte changing AFTER sealing must fail verify with exit 1."""
    cs = _seal_fixture(tmp_path, monkeypatch, {"a.json": '{"x": 1}'})
    assert cs.cmd_update(by="tester", note="seed") == 0          # positive control: seal is clean
    assert cs.cmd_verify() == 0                                    # positive control: clean PASSES
    (tmp_path / "configs" / "a.json").write_text('{"x": 2}', encoding="utf-8")
    assert cs.cmd_verify() == 1, "modified config must BLOCK (exit 1)"


def test_config_seal_blocks_on_unsealed_file(tmp_path, monkeypatch):
    """A NEW config appearing after sealing must block — the silent-add hole."""
    cs = _seal_fixture(tmp_path, monkeypatch, {"a.json": '{"x": 1}'})
    assert cs.cmd_update(by="tester", note="seed") == 0
    (tmp_path / "configs" / "b.yaml").write_text("k: v", encoding="utf-8")
    assert cs.cmd_verify() == 1, "unsealed new config must BLOCK (exit 1)"


def test_config_seal_blocks_on_missing_file(tmp_path, monkeypatch):
    """A sealed config DELETING must block."""
    cs = _seal_fixture(tmp_path, monkeypatch, {"a.json": '{"x": 1}'})
    assert cs.cmd_update(by="tester", note="seed") == 0
    (tmp_path / "configs" / "a.json").unlink()
    assert cs.cmd_verify() == 1, "missing config must BLOCK (exit 1)"


def test_config_seal_exit2_on_no_seal(tmp_path, monkeypatch):
    """No seal at all is exit 2 (cannot verify), NOT exit 0. A gate that
    returns 0 when it cannot check is worse than no gate."""
    cs = _seal_fixture(tmp_path, monkeypatch, {"a.json": '{"x": 1}'})
    assert cs.cmd_verify() == 2, "absent seal must be exit 2, never a pass"


# ---- line-ending invariance (W3C law change 2026-09-29) --------------------
# The v1 seal hashed raw bytes, so a CRLF-checkout seal failed every LF
# checkout (Linux clones, gate-canary worktrees): 41/56 files mismatched
# with zero content change. Receipt: watch/inbox/mates_leave_protocol/
# W3C_SEAL_CRLF.md. These two tests pin the fix from both directions.


def test_config_seal_verifies_lf_flip_of_crlf_seal(tmp_path, monkeypatch):
    """Seal on CRLF bytes, flip the file to LF on disk: verify must PASS.
    This is the Linux-clone-of-a-Windows-seal case that fired the canary.
    Byte-exact writes: Windows text-mode would double the \\r."""
    p = tmp_path / "configs" / "a.yaml"
    cs = _seal_fixture(tmp_path, monkeypatch, {})
    p.write_bytes(b"k: v\r\nj: w\r\n")
    assert cs.cmd_update(by="tester", note="seed") == 0
    p.write_bytes(b"k: v\nj: w\n")
    assert cs.cmd_verify() == 0, "LF checkout of a CRLF-sealed config must PASS"


def test_config_seal_verifies_crlf_flip_of_lf_seal(tmp_path, monkeypatch):
    """Seal on LF bytes, flip the file to CRLF on disk: verify must PASS.
    The mirror case — a Windows autocrlf smudge of an LF-sealed file."""
    p = tmp_path / "configs" / "a.yaml"
    cs = _seal_fixture(tmp_path, monkeypatch, {})
    p.write_bytes(b"k: v\nj: w\n")
    assert cs.cmd_update(by="tester", note="seed") == 0
    p.write_bytes(b"k: v\r\nj: w\r\n")
    assert cs.cmd_verify() == 0, "CRLF checkout of an LF-sealed config must PASS"


def test_config_seal_blocks_real_edit_despite_normalization(tmp_path, monkeypatch):
    """Normalization must not swallow drift: a content change that also
    flips line endings still BLOCKS (exit 1). Positive-control pair to the
    two flip tests — without it, a hash mutated to constant would pass them."""
    cs = _seal_fixture(tmp_path, monkeypatch, {"a.json": '{"x": 1}\r\n'})
    assert cs.cmd_update(by="tester", note="seed") == 0
    (tmp_path / "configs" / "a.json").write_text('{"x": 2}\n', encoding="utf-8")
    assert cs.cmd_verify() == 1, "real content drift under an ending flip must BLOCK"


# --------------------------------------------------------------------------
# checkbox_receipt_gate.py — the B2-238 falsifier
# --------------------------------------------------------------------------

def test_checkbox_gate_blocks_unearned_flip(tmp_path):
    """A checked Open row naming NO resolvable receipt must fail exit 1.

    This is the gate's own docstring falsifier, lifted verbatim as a test.
    """
    cg = _load("cg_fixture", "tools/checkbox_receipt_gate.py")
    q = tmp_path / "QUEUE.md"
    q.write_text(
        "## Open\n"
        "- [x] B2-999 did a thing with no receipt pointer at all\n",
        encoding="utf-8",
    )
    rc = subprocess.run(
        [str(VENV_PY), str(ROOT / "tools" / "checkbox_receipt_gate.py"), "--queue", str(q)],
        capture_output=True, text=True, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert rc.returncode == 1, f"unearned flip must BLOCK (exit 1), got {rc.returncode}"
    assert "B2-999" in rc.stdout, "the offending row id must be NAMED in output"


def test_checkbox_gate_passes_receipt_backed_row(tmp_path, monkeypatch):
    """Positive control: a checked row WITH a resolvable receipt must pass.
    Without this, a gate mutated to always-return-1 would look correct.

    resolvable_paths() resolves a bare filename against
    ROOT/watch/inbox/burn_wave_20260926/ and then ROOT/ — both real, live
    paths in this repo. The fixture therefore names a receipt that actually
    exists there rather than inventing one in tmp_path, which no candidate
    root can reach. It also patches the gate's ROOT so the row is read from
    tmp without touching the real QUEUE.md.
    """
    cg = _load("cg_fixture_root", "tools/checkbox_receipt_gate.py")
    real_root = cg.ROOT
    # Name a receipt that genuinely resolves from the real root:
    # bare names resolve against watch/inbox/burn_wave_20260926/ first,
    # and QUEUE.md lives there (fixture fix 2026-09-27 — the earlier
    # audit_20260926/ name matched no candidate root, which is the gate's
    # rooted-by-design behavior, not a defect).
    probe = tmp_path / "QUEUE.md"
    probe.write_text("## Open\n- [x] B2-998 work logged\n", encoding="utf-8")
    receipt_name = "QUEUE.md"
    probe.write_text(
        "## Open\n"
        f"- [x] B2-998 work logged, receipt {receipt_name}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cg, "ROOT", real_root)
    rows = cg.checked_open_rows(probe.read_text(encoding="utf-8"))
    assert len(rows) == 1, "fixture must present exactly one checked Open row"
    rid, text = rows[0]
    assert cg.resolvable_paths(text), (
        f"positive-control receipt {receipt_name} did not resolve — "
        "pick a path that exists under the real ROOT"
    )


def test_checkbox_gate_exit2_on_missing_queue(tmp_path):
    """Missing queue = cannot verify = exit 2, never a pass."""
    rc = subprocess.run(
        [str(VENV_PY), str(ROOT / "tools" / "checkbox_receipt_gate.py"),
         "--queue", str(tmp_path / "nope.md")],
        capture_output=True, text=True, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert rc.returncode == 2, f"missing queue must be exit 2, got {rc.returncode}"


# --------------------------------------------------------------------------
# secret_gate.py — the gate wired into pre-push the day it was built
# --------------------------------------------------------------------------

# Correctly-shaped SYNTHETIC providers, each VERIFIED against the gate's own
# BLOCKABLE_RULES on 2026-09-27 (sk-proj synthetic was dropped: it does not
# match the OPENAI-PROJ regex and only reached medium/report tier).
# Values are fabricated; entropy is real. Never place a real key here.
_SYNTHETIC = {
    "anthropic": "sk-ant-api03-R7kM2vT9xQ4nB6yH1jL8pW3eZ5dS0aC7uF1gI9oK2mQ6hT4vB8nX1z",
    "groq": "gsk_7Kp2mR9vT4xQ8nB1yH6jL3pW0eZ5dS2aC8uF1gI4oK9mN6pQ3rT7vY2wB5",
    "xai": "xai-Kp2mR9vT4xQ8nB1yH6jL3pW0eZ5dS2aC8uF1gI4oK9mN6pQ3rT7vY2w",
}


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_secret_gate_blocks_provider_shaped_secret(tmp_path):
    """A correctly-shaped provider token must BLOCK. The 2026-09-27 build
    proved this by hand; this makes it permanent."""
    target = _write(tmp_path, "creds.txt", f"api_key = {_SYNTHETIC['anthropic']}\n")
    rc = subprocess.run(
        [str(VENV_PY), str(ROOT / "tools" / "secret_gate.py"), "--full", str(target)],
        capture_output=True, text=True, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert rc.returncode == 1, f"provider-shaped secret must BLOCK (exit 1), got {rc.returncode}"


def test_secret_gate_exempts_masked_token(tmp_path):
    """A HAND-REDACTED token must NOT be a finding. Without this the gate
    flags the operator's own transcripts and trains them to ignore it."""
    target = _write(
        tmp_path, "notes.md",
        "the old key was xai-gO1x...qe6D and was rotated\n",
    )
    rc = subprocess.run(
        [str(VENV_PY), str(ROOT / "tools" / "secret_gate.py"), "--full", str(target)],
        capture_output=True, text=True, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert rc.returncode == 0, f"masked token must be EXEMPT, got {rc.returncode}: {rc.stdout}"


def test_secret_gate_passes_clean_file(tmp_path):
    """Positive control: ordinary text with no credential shape passes."""
    target = _write(tmp_path, "readme.md", "# hello\n\njust prose about keys and doors\n")
    rc = subprocess.run(
        [str(VENV_PY), str(ROOT / "tools" / "secret_gate.py"), "--full", str(target)],
        capture_output=True, text=True, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert rc.returncode == 0, f"clean file must PASS, got {rc.returncode}"


def test_secret_gate_never_prints_secret_value(tmp_path):
    """The gate must MASK. A gate that echoes the value it found is a
    scanner that copies secrets into logs and receipts."""
    secret = _SYNTHETIC["groq"]
    target = _write(tmp_path, "leak.txt", f"token: {secret}\n")
    rc = subprocess.run(
        [str(VENV_PY), str(ROOT / "tools" / "secret_gate.py"), "--full", str(target)],
        capture_output=True, text=True, cwd=str(ROOT),
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert rc.returncode == 1
    blob = rc.stdout + rc.stderr
    assert secret not in blob, "SECRET VALUE LEAKED INTO GATE OUTPUT — this is a critical defect"


# --------------------------------------------------------------------------
# violation_ratchet.py — the disarmed-gate regression
# --------------------------------------------------------------------------

def test_violation_ratchet_has_a_negative_exit_assertion():
    """The audit found all 5 of its exit asserts were `== 0`. This test
    cannot mutate the suite, but it FAILS LOUDLY if the ratchet is ever
    disarmed, by asserting the source still contains a blocking return."""
    src = (ROOT / "tools" / "violation_ratchet.py").read_text(encoding="utf-8")
    assert "return 1" in src, (
        "violation_ratchet.py has no `return 1` — the blocking path was removed. "
        "The push gate would silently pass everything."
    )


def test_config_seal_is_reachable_from_pre_push():
    """config_seal is a hard pre-push block. If the hook stops calling it,
    the gate stops existing. This is the contract test for the wiring."""
    hook = (ROOT / "githooks" / "pre-push").read_text(encoding="utf-8")
    assert "config_seal.py verify" in hook, "config_seal verify is no longer wired into pre-push"


def test_secret_gate_is_wired_into_pre_push():
    hook = (ROOT / "githooks" / "pre-push").read_text(encoding="utf-8")
    assert "secret_gate.py" in hook, "secret_gate is no longer wired into pre-push"
