"""D3 regression: clippy-as-prober (skill card FSRS + gwap recall payloads).

The door (eleven-doors D3): "the one genuinely un-held build - 2-3
closed-book free-recall probes on due skill cards, FSRS-default state,
passes as gwap payloads; banks the ~1k probes FSRS needs off defaults;
gates the decay family's third store."

Pinned here: card enumeration, all-due defaults, probe determinism,
the simplified FSRS-default intervals, the deterministic self-grade,
the gwap term-coverage payload (honest recall VERIFIED_AGREE without a
collusion flag via the commit-bound exemption; wrong recall DISPUTE),
and the append-only review log.
"""
import json

import pytest

import mag.skill_fsrs as sf


CARD = """---
name: probe-test
description: A test card for the closed-book probe instrument - it plants probes and grades recalls deterministically.
---

# PROBE TEST

## Step one of the card

## Step two of the card

- **The first law: never guess a probe answer.**
"""


@pytest.fixture()
def card_root(tmp_path, monkeypatch):
    skills = tmp_path / "skills"
    d = skills / "probe-test"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(CARD, encoding="utf-8")
    monkeypatch.setattr(sf, "SKILL_ROOTS", (skills, tmp_path / "none"))
    monkeypatch.setattr(sf, "REVIEWS", tmp_path / "fsrs" / "reviews.jsonl")
    return skills


HONEST = ("the test card plants closed-book probes and grades recalls "
          "deterministically; step one then step two; never guess a probe answer")
WRONG = "docker containers and gpu scheduling for vast rentals"


def test_cards_enumerate_and_all_due_at_default(card_root):
    assert set(sf.cards()) == {"probe-test"}
    assert sf.due_cards() == ["probe-test"]
    st = sf.card_state("probe-test")
    assert st["reviews"] == 0 and st["due"] is None


def test_probe_deterministic_and_bounded(card_root):
    q1 = sf.probe("probe-test")
    q2 = sf.probe("probe-test")
    assert q1 == q2
    assert 2 <= len(q1) <= 3
    assert any("reach for probe-test" in q for q in q1)
    assert any("section steps" in q for q in q1)
    # the probe never prints the answer key
    assert not any("deterministically" in q for q in q1)


def test_fsrs_default_first_intervals_pinned(card_root):
    good = sf.next_state(sf.card_state("probe-test"), "good")
    assert good["stability_days"] == pytest.approx(3.0)  # FSRS-4.5 default w[2]
    again = sf.next_state(sf.card_state("probe-test"), "again")
    assert again["stability_days"] == pytest.approx(0.4)
    # repeat reviews grow (or floor) stability
    grown = sf.next_state(good, "good")
    assert grown["stability_days"] > good["stability_days"]
    floored = sf.next_state(good, "again")
    assert floored["stability_days"] == pytest.approx(0.4)


def test_self_grade_honest_vs_wrong(card_root):
    g, s = sf.self_grade(HONEST, "probe-test")
    assert g in ("good", "easy") and s >= 0.25
    g2, s2 = sf.self_grade(WRONG, "probe-test")
    assert g2 == "again" and s2 == 0.0


def test_gwap_payload_honest_recall_agrees_without_collusion(card_root):
    row = sf.answer("probe-test", HONEST)
    assert row["ok"]
    assert row["gwap_verdict"] == "VERIFIED_AGREE"
    assert row["gwap_agreement"] > 0.3
    fp = row["payload"]["collusion_fingerprint"]
    assert fp["suspected_collusion"] is False  # commit-bound order-identity


def test_gwap_payload_wrong_recall_disputes(card_root):
    row = sf.answer("probe-test", WRONG)
    assert row["ok"]
    assert row["gwap_verdict"] == "DISPUTE"
    assert row["gwap_agreement"] == 0.0
    assert row["grade"] == "again"


def test_reviews_append_only_and_state_derives(card_root):
    sf.answer("probe-test", HONEST)
    sf.answer("probe-test", HONEST)
    rows = [json.loads(l) for l in sf.REVIEWS.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2  # append-only, nothing rewritten
    st = sf.card_state("probe-test")
    assert st["reviews"] == 2
    assert st["due"] == rows[-1]["due"]  # state from the LAST row
    assert "probe-test" not in sf.due_cards()  # honest recall moved it out


def test_unknown_card_refuses(card_root):
    r = sf.answer("nope", "anything")
    assert not r["ok"]


def test_clippy_block_questions_only(card_root):
    block = sf.clippy_block()
    assert "FSRS PROBES" in block
    assert "probe-test" in block
    assert "deterministically" not in block  # never the answer key
