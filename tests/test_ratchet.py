"""Unit tests for mag/ratchet.py (enablement dials + delete-when-X retirement receipts)."""
import json
from pathlib import Path
import pytest

from mag.ratchet import DEFAULT_REGISTRY, RatchetRegistry, RatchetSpec


def test_default_registry_has_5_laws():
    specs = DEFAULT_REGISTRY.list_specs()
    assert len(specs) >= 5
    assert DEFAULT_REGISTRY.is_enabled("B2-294-seal-line-8mb") is True
    assert DEFAULT_REGISTRY.is_enabled("CHAIN-V2-checkpoint-signing", unattended=True) is False


def test_dial_semantics(monkeypatch, tmp_path):
    reg = RatchetRegistry(ledger_path=tmp_path / "retirements.jsonl")
    reg.register(RatchetSpec("d-always", "always-on", "retire when v2", "mag/a.py", "always"))
    reg.register(RatchetSpec("d-default", "default-on", "retire when v2", "mag/b.py", "default"))
    reg.register(RatchetSpec("d-optin", "opt-in", "retire when v2", "mag/c.py", "optin"))
    reg.register(RatchetSpec("d-manual", "manual-only", "retire when v2", "mag/d.py", "manual"))

    assert reg.is_enabled("d-always", overrides={"d-always": False}) is True
    assert reg.is_enabled("d-default") is True
    monkeypatch.setenv("MAG_RATCHET_OFF_D_DEFAULT", "1")
    assert reg.is_enabled("d-default") is False

    assert reg.is_enabled("d-optin") is False
    monkeypatch.setenv("MAG_RATCHET_ON_D_OPTIN", "1")
    assert reg.is_enabled("d-optin") is True

    assert reg.is_enabled("d-manual", unattended=True, overrides={"d-manual": True}) is False
    assert reg.is_enabled("d-manual", unattended=False, overrides={"d-manual": True}) is True


def test_missing_delete_when_refused(tmp_path):
    reg = RatchetRegistry(ledger_path=tmp_path / "retirements.jsonl")
    with pytest.raises(ValueError, match="delete_when"):
        reg.register(RatchetSpec("bad", "default-on", "   ", "mag/x.py", "missing condition"))


def test_retire_writes_hash_verified_receipt(tmp_path):
    ledger = tmp_path / "retirements.jsonl"
    ev = tmp_path / "proof.md"
    ev.write_text("verified proof bytes", encoding="utf-8")
    reg = RatchetRegistry(ledger_path=ledger)
    reg.register(RatchetSpec("debt-1", "default-on", "when proof lands", "mag/z.py", "summary"))
    rec = reg.retire("debt-1", verified_by="bob-primary", evidence_path=ev, note="cutover complete")
    assert rec["debt_id"] == "debt-1"
    assert len(rec["evidence_sha256"]) == 64
    rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["evidence_sha256"] == rec["evidence_sha256"]
