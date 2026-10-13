"""tests for tools/md_record_seal.py register-path fix (B2-41, 2026-09-26).

The writer-contract fix (2026-09-26) made the seal hook append a register
event next to the autoseal so sealed files become active INDEX items. B2-41
found the register reused the seal's absolute host path, which the fold keeps
as a phantom item (QUEUE.md minted twice, LAW13 once; B2-50 and B2-145 had to
invalidate them by hand). The fix: the register carries the inbox-relative
path and only fires for files under watch/inbox.

Every test patches ESTATE/EVENTS to a throwaway tree, so the durable
watch/inbox/index_events.jsonl is never touched.
"""
import io
import json
import sys
from pathlib import Path

import pytest

import tools.md_record_seal as seal

@pytest.fixture()
def seal_estate(tmp_path, monkeypatch):
    estate = tmp_path / "estate"
    inbox = estate / "watch" / "inbox"
    inbox.mkdir(parents=True)
    events = inbox / "index_events.jsonl"
    events.write_text("", encoding="utf-8")
    monkeypatch.setattr(seal, "ESTATE", estate)
    monkeypatch.setattr(seal, "EVENTS", events)
    monkeypatch.setattr(seal, "DURABLE", [
        estate / "watch", estate / "memory" / "rib",
        estate / "memory" / "game_modules", estate / "corpus",
        estate / "queue",
    ])
    monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))
    monkeypatch.setattr(sys, "argv", ["md_record_seal.py", "seal"])
    return estate, inbox, events


def _run_seal(target: Path):
    seal.main.__globals__["sys"].stdin = io.StringIO(json.dumps({
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
    }))
    try:
        seal.main()
    except SystemExit as exc:  # the hook always exits 0 (fail-open law)
        assert exc.code == 0, exc.code


def _events(events: Path):
    return [json.loads(ln) for ln in
            events.read_text(encoding="utf-8").splitlines() if ln.strip()]


def test_register_under_inbox_uses_relative_path(seal_estate):
    estate, inbox, events = seal_estate
    target = inbox / "burn_wave_x" / "NOTE.md"
    target.parent.mkdir()
    target.write_text("note", encoding="utf-8")
    _run_seal(target)
    regs = [e for e in _events(events) if e.get("op") == "register"]
    autoseals = [e for e in _events(events) if e.get("op") == "autoseal"]
    assert len(regs) == 1 and len(autoseals) == 1
    # the fold item path is inbox-relative, never the absolute host path
    assert regs[0]["file"] == "burn_wave_x/NOTE.md"
    assert not regs[0]["file"].startswith(str(estate))
    assert regs[0]["writer"] == "md-record-seal" and regs[0]["nonce"] == 1
    import hashlib
    assert regs[0]["sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()


def test_register_skipped_outside_inbox(seal_estate):
    estate, inbox, events = seal_estate
    target = estate / "memory" / "rib" / "OUTSIDE.md"
    target.parent.mkdir(parents=True)
    target.write_text("outside", encoding="utf-8")
    _run_seal(target)
    evs = _events(events)
    # autoseal journal line stays; no register event the fold would drop as
    # outside (fold warning noise since B2-40)
    assert [e["op"] for e in evs] == ["autoseal"]


def test_register_nonce_advances_per_writer(seal_estate):
    estate, inbox, events = seal_estate
    a = inbox / "A.md"
    a.write_text("a", encoding="utf-8")
    b = inbox / "B.md"
    b.write_text("b", encoding="utf-8")
    _run_seal(a)
    _run_seal(b)
    regs = [e for e in _events(events) if e.get("op") == "register"]
    assert [r["nonce"] for r in regs] == [1, 2]


def test_dedupe_skips_same_size_reseal(seal_estate):
    estate, inbox, events = seal_estate
    target = inbox / "C.md"
    target.write_text("same", encoding="utf-8")
    _run_seal(target)
    _run_seal(target)  # same size within the tail window -> no new lines
    assert len(_events(events)) == 2


def test_register_sha256_big_file_gets_real_hash(tmp_path):
    """B2-294: a >256KB file must not register the size-only token as a sha."""
    from tools.md_record_seal import register_sha256  # noqa: E402
    import hashlib
    p = tmp_path / "big.bin"
    data = b"x" * (300 * 1024)
    p.write_bytes(data)
    got = register_sha256(p, "size-only(>256KB)")
    assert got == hashlib.sha256(data).hexdigest()


def test_register_sha256_passthrough_and_living_fallback(tmp_path, monkeypatch):
    """B2-294: the beyond-cap branch must emit the B2-156 living-style prefix
    seal, not the bare size-only token. The cap is monkeypatched down (same
    branch boundary, no multi-MB scratch file needed); the 9 MiB shape itself
    was proven by the live probe quoted in
    watch/inbox/burn_wave_20260926/B2_294_register_sha_fix_20260926.md."""
    import tools.md_record_seal as seal_mod
    from tools.md_record_seal import register_sha256  # noqa: E402
    import hashlib
    p = tmp_path / "f.bin"
    data = b"y" * 1000
    p.write_bytes(data)
    real = hashlib.sha256(data).hexdigest()
    assert register_sha256(p, real) == real  # already a hash: untouched
    monkeypatch.setattr(seal_mod, "MAX_BYTES", 4096)
    huge = tmp_path / "huge.bin"
    blob = b"z" * 8192  # deterministic, beyond the shrunken cap
    huge.write_bytes(blob)
    got = register_sha256(huge, "size-only(>256KB)")
    assert got.startswith("sha256(first 262144):")
    assert got.endswith(f"@{len(blob)}B(living-style, B2-156)")
    assert hashlib.sha256(blob[:262144]).hexdigest() in got


# ---- B2-148: the register event adopts the B2-40 seq scheme ----

def _last_register(events_path):
    regs = [e for e in _events(events_path)
            if e.get("op") == "register" and e.get("writer") == "md-record-seal"]
    assert regs, "no md-record-seal register event landed"
    return regs[-1]


def test_register_carries_usable_seq(seal_estate):
    """The fold's seqOf accepts integer Numbers and digit-only strings; the
    hook's first register must carry seq 1 as a plain JSON number."""
    estate, inbox, events = seal_estate
    target = inbox / "note.md"
    target.write_text("note", encoding="utf-8")
    _run_seal(target)
    reg = _last_register(events)
    assert reg["seq"] == 1


def test_register_seq_resumes_past_2pow53_as_decimal_string(seal_estate):
    """A log whose max usable seq is past 2^53 must make the hook emit a
    digit-only decimal STRING (the B2-40 scheme), greater than the max."""
    estate, inbox, events = seal_estate
    events.write_text(
        json.dumps({"op": "register", "file": "x.md", "writer": "exp002a",
                    "seq": "9007199254740995"}) + chr(10),
        encoding="utf-8")
    target = inbox / "note2.md"
    target.write_text("note2", encoding="utf-8")
    _run_seal(target)
    reg = _last_register(events)
    assert isinstance(reg["seq"], str) and reg["seq"].isdigit()
    assert int(reg["seq"]) == 9007199254740996


def test_register_seq_ignores_unusable_and_quantized_literals(seal_estate):
    """seqOf semantics: non-integer floats, non-digit strings and bools are
    NOT usable seqs; the resume-max ignores them."""
    estate, inbox, events = seal_estate
    events.write_text(
        json.dumps({"op": "autoseal", "file": "a", "seq": 1.5}) + chr(10) +
        json.dumps({"op": "autoseal", "file": "b", "seq": "12abc"}) + chr(10) +
        json.dumps({"op": "autoseal", "file": "c", "seq": True}) + chr(10) +
        json.dumps({"op": "register", "file": "d", "seq": 7}) + chr(10),
        encoding="utf-8")
    target = inbox / "note3.md"
    target.write_text("note3", encoding="utf-8")
    _run_seal(target)
    reg = _last_register(events)
    assert reg["seq"] == 8
