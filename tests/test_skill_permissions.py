"""Skill permission globs: check() allow / deny / last-match-wins / fail-closed.

W3P 2026-09-29, Mickey17 wave-3 lane. Seed: the S12 Kilo steal
(watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md, agent ca7ff8d5) — ordered glob
permission lists, LAST matching rule wins, `deny-<glob>` flips a glob to a
deny. The helper is ADVISORY v0: nothing in the harness calls it yet
(adoption is a separate law change); these tests pin the semantics so any
future enforcement wiring inherits a proven contract.
"""
from __future__ import annotations

import yaml

import mag.skills_pack as sp

REAL_CFG = sp.CFG  # the repo's configs/skills.yaml (pilots live here)

FIXTURE_CFG = {
    "schema": "mag_skills.v1",
    "skills": [
        # plain allow, both modes
        {"id": "scribe", "permissions": {"read": ["*"], "write": ["watch/inbox/**"]}},
        # allow-then-deny carve-out: everything except the private drawer
        {"id": "carver", "permissions": {"read": ["*", "deny-watch/inbox/private/**"]}},
        # deny-then-allow: inbox denied at large, but one lane re-opened after
        {"id": "reopener", "permissions": {"write": ["deny-watch/inbox/**", "watch/inbox/W3P_SKILL_GLOBS.md"]}},
        # permissions field present but the asked mode is absent
        {"id": "read-only", "permissions": {"read": ["corpus/**"]}},
        # empty rule list is still fail-closed, not "allow all"
        {"id": "blank", "permissions": {"read": [], "write": [""]}},
        # no permissions field at all (the pre-W3P shape of every skill)
        {"id": "bare", "path": "docs/x.md"},
    ],
    "job_to_skills": {},
}


def _fixture(monkeypatch, tmp_path):
    cfg_path = tmp_path / "skills.yaml"
    cfg_path.write_text(yaml.safe_dump(FIXTURE_CFG), encoding="utf-8")
    monkeypatch.setattr(sp, "CFG", cfg_path)
    monkeypatch.setattr(sp, "SKILL_LEDGER", tmp_path / "skill_ledger.jsonl")


# --- allow -------------------------------------------------------------------

def test_allow_matching_glob(monkeypatch, tmp_path):
    """A path matching an allow rule is allowed (both modes)."""
    _fixture(monkeypatch, tmp_path)
    assert sp.check("scribe", "watch/inbox/SOME_RECEIPT.md", "write") is True
    assert sp.check("scribe", "mag/router.py", "read") is True
    # ** spans directory separators (fnmatch semantics, documented at v0)
    assert sp.check("scribe", "watch/inbox/nested/deep/a.md", "write") is True


# --- deny --------------------------------------------------------------------

def test_deny_rule_rejects(monkeypatch, tmp_path):
    """A `deny-` glob rejects even under a broader earlier allow."""
    _fixture(monkeypatch, tmp_path)
    assert sp.check("carver", "watch/inbox/private/secret.md", "read") is False
    # outside the denied drawer the broad allow still holds
    assert sp.check("carver", "watch/inbox/public.md", "read") is True


# --- last-match-wins ----------------------------------------------------------

def test_last_match_wins_both_directions(monkeypatch, tmp_path):
    """Order decides: the LAST matching rule wins, whichever verdict it carries."""
    _fixture(monkeypatch, tmp_path)
    # carver: allow "*" THEN deny private -> deny (tested above); reopener is
    # the mirror image: deny inbox THEN re-allow one file -> allow
    assert sp.check("reopener", "watch/inbox/W3P_SKILL_GLOBS.md", "write") is True
    assert sp.check("reopener", "watch/inbox/anything_else.md", "write") is False


# --- fail-closed default ------------------------------------------------------

def test_fail_closed_when_no_rule_matches(monkeypatch, tmp_path):
    """No matching rule => REJECT. Unlisted is untrusted, never implicit allow."""
    _fixture(monkeypatch, tmp_path)
    assert sp.check("scribe", "mag/router.py", "write") is False  # write list has no mag rule
    assert sp.check("read-only", "docs/x.md", "read") is False


def test_fail_closed_on_missing_shapes(monkeypatch, tmp_path):
    """Unknown skill, missing permissions field, missing mode, empty rules all reject."""
    _fixture(monkeypatch, tmp_path)
    assert sp.check("does-not-exist", "watch/inbox/a.md", "write") is False
    assert sp.check("bare", "watch/inbox/a.md", "write") is False  # no permissions field
    assert sp.check("read-only", "corpus/a.md", "write") is False  # mode absent from map
    assert sp.check("blank", "watch/inbox/a.md", "read") is False  # empty rule list
    assert sp.check("blank", "watch/inbox/a.md", "write") is False  # blank-string rule


# --- path normalization -------------------------------------------------------

def test_path_forms_normalized(monkeypatch, tmp_path):
    """Backslashes, leading ./, and ROOT-absolute paths match repo-relative globs."""
    _fixture(monkeypatch, tmp_path)
    assert sp.check("scribe", r"watch\inbox\a.md", "write") is True
    assert sp.check("scribe", "./watch/inbox/a.md", "write") is True
    assert sp.check("scribe", str(sp.ROOT / "watch" / "inbox" / "a.md"), "write") is True


# --- real pilots (byte truth from configs/skills.yaml) ------------------------

def test_real_config_pilots_parse_and_behave():
    """The 5 W3P pilot entries exist in the real config and behave as declared."""
    cfg = yaml.safe_load(REAL_CFG.read_text(encoding="utf-8"))
    pilots = {
        s["id"]: s.get("permissions")
        for s in cfg["skills"]
        if s.get("id") in {"ractor-essay", "show-me", "elder-lens", "corpus-harvest", "code-agent-data"}
    }
    assert len(pilots) == 5
    assert all(isinstance(p, dict) and p.get("read") and p.get("write") for p in pilots.values())
    # mission-named pilots carry the named globs
    assert pilots["ractor-essay"]["write"] == ["watch/inbox/**"]
    assert pilots["corpus-harvest"]["read"] == ["corpus/**"]
    # check() against the real file (no monkeypatch: byte truth, not fixture)
    assert sp.check("ractor-essay", "watch/inbox/W3P_SKILL_GLOBS.md", "write") is True
    assert sp.check("ractor-essay", "mag/skills_pack.py", "write") is False
    assert sp.check("corpus-harvest", "corpus/steal/SOME_STEAL.md", "read") is True
    assert sp.check("corpus-harvest", "mag/skills_pack.py", "read") is False
    # every non-pilot skill stays fail-closed (permissions still opt-in)
    assert sp.check("sovereign-mag", "watch/inbox/a.md", "write") is False


def test_pilot_field_does_not_break_pack(monkeypatch, tmp_path):
    """skills_for_job still packs a pilot skill carrying a permissions block."""
    _fixture(monkeypatch, tmp_path)
    # point CFG at the real config but keep the ledger in tmp (fires are receipts)
    monkeypatch.setattr(sp, "CFG", REAL_CFG)
    text = sp.skills_for_job("essay")  # job_to_skills.essay = [ractor-essay]
    assert "### ractor-essay" in text
