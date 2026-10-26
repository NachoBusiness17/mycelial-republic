"""Violation ratchet prune-domain tests (B2-95, 2026-09-26).

tools/violation_ratchet.py prune used to delete any accepted claim its
fingerprint could not re-derive. Externally sourced claims (namespaced rules
like the mimosa-* set B2-11 registered over watch/inbox/, a tree the scanner
never scans) are underivable by construction, so every prune reaped them; the
B2-11 falsifier named this reap in advance and a same-day prune took all 25
(receipts: watch/inbox/burn_wave_20260926/B2_11_mimosa_close_20260926.md,
watch/inbox/burn_wave_20260926/B2_95_prune_gap_20260926.md). The fix: prune
reaps only scanner-domain claims (rule in SCANNER_RULES and file under a scan
root); external claims leave only by explicit re-triage.

Four bands: the scanner_domain verdict core, the B2-11 reap falsifier (old
prune loses the external claim, new prune keeps it while still removing fixed
scanner debt), the still-reaps-fixed-scanner-debt band, and a read-only pin on
the real baseline bytes (every mimosa-* claim present and external-domain).
"""
from __future__ import annotations

import json

import pytest

import tools.violation_ratchet as vr


def _write_baseline(tmp_path, accepted: dict):
    path = tmp_path / "violation_baseline.json"
    path.write_text(
        json.dumps({"version": 1, "updated": None, "accepted": accepted}, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _claim(rule: str, file: str, detail: str) -> dict:
    return {
        "rule": rule,
        "file": file,
        "detail": detail,
        "accepted": "2026-09-26",
        "by": "test:B2-95",
        "note": "prune-domain fixture",
    }


def test_scanner_domain_verdict_core():
    # Scanner rule under a scan root: re-derivable, prune may reap it.
    assert vr.scanner_domain("file-too-long", "mag/deep/module.py") is True
    assert vr.scanner_domain("bare-except", "tools/helper.py") is True
    # Namespaced external rule: underivable even under a scan root.
    assert vr.scanner_domain("mimosa-ssrf", "mag/deep/module.py") is False
    assert vr.scanner_domain("mimosa-path-traversal", "tools/helper.py") is False
    # Scanner rule outside the scan roots: the scanner never sees that file,
    # so the claim is external-domain and prune must keep it (the B2-11 shape:
    # watch/inbox/ is never scanned).
    assert vr.scanner_domain("file-too-long", "watch/inbox/one_shot.py") is False
    assert vr.scanner_domain("bare-except", "scripts/run.py") is False


def test_prune_keeps_external_claims_b2_11_reap_falsifier(tmp_path, monkeypatch, capsys):
    """The B2-11 disease: a register holding one mimosa claim plus one stale
    scanner claim. The old prune deleted BOTH (external claims are never in the
    live set); the fixed prune removes only the scanner claim."""
    ext_fp = vr.fingerprint("mimosa-ssrf", "watch/inbox/wave_20260916/u1_union_call.py", "detail-a")
    dead_fp = vr.fingerprint("file-too-long", "tools/old_module.py", ">400 lines")
    baseline = _write_baseline(tmp_path, {
        ext_fp: _claim("mimosa-ssrf", "watch/inbox/wave_20260916/u1_union_call.py", "detail-a"),
        dead_fp: _claim("file-too-long", "tools/old_module.py", ">400 lines"),
    })
    monkeypatch.setattr(vr, "BASELINE_PATH", baseline)
    monkeypatch.setattr(vr, "all_violations", lambda paths=None: [])

    assert vr.cmd_prune() == 0
    saved = json.loads(baseline.read_text(encoding="utf-8"))
    assert ext_fp in saved["accepted"], "external claim reaped: the B2-11 disease survives"
    assert dead_fp not in saved["accepted"], "stale scanner-domain claim survived prune"
    assert len(saved["accepted"]) == 1
    out = capsys.readouterr().out
    assert "fixed-debt-removed=1" in out
    assert "external-kept=1" in out


def test_prune_still_reaps_fixed_scanner_debt(tmp_path, monkeypatch, capsys):
    """A scanner-domain claim whose violation is gone must still leave: the
    register trends down for debt the scanner can see."""
    live_violation = {"rule": "file-too-long", "file": "mag/big.py", "detail": ">400 lines", "line": 500}
    live_fp = vr.fingerprint("file-too-long", "mag/big.py", ">400 lines")
    fixed_fp = vr.fingerprint("bare-except", "tools/fixed.py", "silent except:")
    baseline = _write_baseline(tmp_path, {
        live_fp: _claim("file-too-long", "mag/big.py", ">400 lines"),
        fixed_fp: _claim("bare-except", "tools/fixed.py", "silent except:"),
    })
    monkeypatch.setattr(vr, "BASELINE_PATH", baseline)
    monkeypatch.setattr(vr, "all_violations", lambda paths=None: [live_violation])

    assert vr.cmd_prune() == 0
    saved = json.loads(baseline.read_text(encoding="utf-8"))
    assert live_fp in saved["accepted"], "live registered debt must survive prune"
    assert fixed_fp not in saved["accepted"], "fixed scanner debt must leave via prune"
    out = capsys.readouterr().out
    assert "fixed-debt-removed=1" in out
    assert "register now 1" in out


def test_real_baseline_mimosa_claims_are_external_domain():
    """Read-only pin on the estate's real register: every mimosa-* claim is
    outside the scanner's domain, so no prune can reap any of them by
    construction, and the B2-11 cohort is coherent (watch/inbox/ files).

    Originally pinned at exactly the 25 B2-11 claims; concurrent same-day
    lanes B2-96 (scripts/, 20 claims) and B2-94 (tools/ + models/, 12 claims)
    grew the family to 57 while this lane was closing, so the pin was rebased
    to the invariant (B2-95 receipt addendum): the count is the register's
    business, the domain is the prune's contract. If a future lane
    legitimately re-triages these claims, this pin must be updated in the
    same breath."""
    baseline = json.loads(vr.BASELINE_PATH.read_text(encoding="utf-8"))
    mimosa = {
        fp: entry for fp, entry in baseline.get("accepted", {}).items()
        if str(entry.get("rule", "")).startswith("mimosa-")
    }
    assert len(mimosa) > 0, "mimosa register empty: update this pin in the same breath as the re-triage"
    for fp, entry in mimosa.items():
        assert vr.scanner_domain(entry.get("rule", ""), entry.get("file", "")) is False, (
            f"mimosa claim {fp} ({entry.get('file')}) is scanner-domain and prune-reapable"
        )
    b2_11 = [e for e in mimosa.values() if "B2-11" in str(e.get("by", ""))]
    assert len(b2_11) >= 25, f"B2-11 cohort shrunk below its registered 25: {len(b2_11)}"
    for entry in b2_11:
        assert str(entry.get("file", "")).startswith("watch/inbox/"), entry.get("file")


# ---- B2-273: the growth law (accepted_lines stamp + GROWTH surface) ----

def test_baseline_update_stamps_accepted_lines(tmp_path, monkeypatch, capsys):
    """file-too-long claims freeze their accepted size (B2-273)."""
    v = {"rule": "file-too-long", "file": "mag/big.py",
         "detail": ">400 lines", "line": 427}
    baseline = _write_baseline(tmp_path, {})
    monkeypatch.setattr(vr, "BASELINE_PATH", baseline)
    monkeypatch.setattr(vr, "all_violations", lambda paths=None: [v])
    assert vr.cmd_baseline_update(by="test", note="grow-law pin") == 0
    accepted = json.loads(baseline.read_text(encoding="utf-8"))["accepted"]
    entry = next(iter(accepted.values()))
    assert entry["accepted_lines"] == 427


def test_check_prints_growth_when_claim_absorbs_lines(tmp_path, monkeypatch, capsys):
    """Grown past its accepted size, an accepted claim passes (NEW=0) but the
    growth is a visible ledger fact, never silent (the 427-to-453 disease)."""
    v = {"rule": "file-too-long", "file": "mag/big.py",
         "detail": ">400 lines", "line": 453}
    fp = vr.fingerprint(v["rule"], v["file"], v["detail"])
    baseline = _write_baseline(tmp_path, {fp: {
        "rule": "file-too-long", "file": "mag/big.py", "detail": ">400 lines",
        "accepted": "2026-09-26", "by": "test", "note": "",
        "accepted_lines": 427}})
    monkeypatch.setattr(vr, "BASELINE_PATH", baseline)
    monkeypatch.setattr(vr, "all_violations", lambda paths=None: [v])
    assert vr.cmd_check(changed_only=False) == 0
    out = capsys.readouterr().out
    assert "NEW=0" in out and "PASS" in out
    assert f"GROWTH claim {fp}" in out
    assert "accepted at 427 lines, now 453 (+26)" in out


def test_check_no_growth_line_at_accepted_size(tmp_path, monkeypatch, capsys):
    """At or under the accepted size there is no GROWTH noise."""
    v = {"rule": "file-too-long", "file": "mag/big.py",
         "detail": ">400 lines", "line": 427}
    fp = vr.fingerprint(v["rule"], v["file"], v["detail"])
    baseline = _write_baseline(tmp_path, {fp: {
        "rule": "file-too-long", "file": "mag/big.py", "detail": ">400 lines",
        "accepted": "2026-09-26", "by": "test", "note": "",
        "accepted_lines": 427}})
    monkeypatch.setattr(vr, "BASELINE_PATH", baseline)
    monkeypatch.setattr(vr, "all_violations", lambda paths=None: [v])
    assert vr.cmd_check(changed_only=False) == 0
    assert "GROWTH" not in capsys.readouterr().out
