"""B2-205 pin: p4 quorum tally excludes an addition's author chair.

Fixture-first: a full quorum run dir is staged in tmp (FOLD.md with author
tags + one p1 testimony and one p4 ballot file per chair, so p4 never calls a
model), then the tally is read from the returned result dict and VERDICT.md.

The disease pinned here: the author chair used to vote toward its own
addition's 2/3 bar (the self-vote double-counted the author the p3 fold
already carries). Under B2-205 the author ABSTAINs: excluded from its
addition's tally AND its denominator.

Falsifier: with the exclusion reverted, A1 passes 2/3 (the author's own YES
is pivotal) while A2's denominator stays 3; under the pin A1 fails 1 YES of
an eligible 2 (need 2) while A2 still passes 2/2, proving exclusion never
sinks a genuinely popular addition.
"""
import json
import math

import mag.quorum_window as qw

FOLD = """# FOLD

- **A1** [BUILD] (CHAIR_A): [TAG: BUILD] self addition text
- **A2** [NOTE] (CHAIR_C): [TAG: NOTE] other addition text

## DISSENT LOG

- noise
"""

CHAIR = "chair: {c}\nts: t\n\nVOTE: A1 {s}\nVOTE: A2 {o}\n"

# A1 (author CHAIR_A): raw 2/3 YES would PASS the old rule; excluding the
# author leaves 1 YES of an eligible 2 (need 2) -> NOT PASSED. Pivotal.
# A2 (author CHAIR_C): 3/3 raw YES; 2/2 eligible after exclusion -> PASSED
# either way, pinning that exclusion never sinks genuinely popular additions.
BALLOTS = {
    "CHAIR_A": ("YES", "YES"),
    "CHAIR_B": ("YES", "YES"),
    "CHAIR_C": ("NO-WITH-OBJECTION", "YES"),
}


def _stage(monkeypatch, tmp_path):
    d = tmp_path / "quorum_20990101"
    (d / "p1").mkdir(parents=True)
    (d / "p4").mkdir(parents=True)
    for c in BALLOTS:
        (d / "p1" / f"{c}.md").write_text(
            f"# {c}\n## RISKS\nrisk text for {c}\n## ADDITION\n[TAG: NOTE] addition text {c}\n",
            encoding="utf-8")
        s, o = BALLOTS[c]
        (d / "p4" / f"{c}.md").write_text(CHAIR.format(c=c, s=s, o=o), encoding="utf-8")
    (d / "FOLD.md").write_text(FOLD, encoding="utf-8")
    monkeypatch.setattr(qw, "_dir", lambda date, order: d)
    monkeypatch.setattr(qw, "_receipt", lambda date, row: None)
    return d


def test_author_abstains_on_own_addition(tmp_path, monkeypatch):
    _stage(monkeypatch, tmp_path)
    r = qw.p4("20990101", "seed")
    assert r["ok"], r
    res = r["result"]

    self_row = res["A1"]
    assert self_row["yes"] == 1, "author's YES must be excluded from its own tally"
    assert self_row["denominator"] == 2 and self_row["need"] == 2
    assert self_row["passed"] is False, "the pivotal self-vote must not carry its addition"
    assert self_row["author_abstain"] == "CHAIR_A"

    other_row = res["A2"]
    assert other_row["yes"] == 2
    assert other_row["denominator"] == 2 and other_row["need"] == 2
    assert other_row["passed"] is True, "exclusion must not sink a genuinely popular addition"

    verdict = (tmp_path / "quorum_20990101" / "VERDICT.md").read_text(encoding="utf-8")
    assert "author CHAIR_A ABSTAIN" in verdict
    assert "B2-205 rule" in verdict


def test_need_formula_matches_denominator_law(tmp_path, monkeypatch):
    _stage(monkeypatch, tmp_path)
    r = qw.p4("20990101", "seed")
    for aid, row in r["result"].items():
        assert row["need"] == math.ceil(2 * row["denominator"] / 3)
    assert json.dumps(r["result"])  # result stays json-serializable for _receipt
