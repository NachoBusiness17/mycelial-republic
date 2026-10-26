"""tests/test_burns_verdict_enum.py - AH13 (2026-09-30).

Laws pinned here (receipt watch/inbox/last_mile_20260930/AH13_BURNS_ENUM.md):
  1. known strings map clean via the exact table (confidence 1.0);
  2. unknown strings fall to OTHER + review=true - never silently absorbed;
  3. the map round-trips: every census key joins back to the same enum the
     live normalize() produces, and --apply leaves LEDGER.jsonl byte-identical
     (the no-rewrite law, proven by sha256, not by promise).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "burns_verdict_enum.py"

_spec = importlib.util.spec_from_file_location("burns_verdict_enum", TOOL)
bve = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bve)


@pytest.fixture()
def tmp_ledger(tmp_path):
    """A miniature ledger spanning every mapping path: exact hits (clear and
    review-flagged), rule hits (prefix + word), and an unknown prose verdict."""
    rows = [
        {"slug": "a", "verdict": "LANDED"},
        {"slug": "b", "verdict": "LANDED"},
        {"slug": "c", "verdict": "steal"},
        {"slug": "d", "verdict": "steal"},
        {"slug": "e", "verdict": "landed"},
        {"slug": "f", "verdict": "vacuous"},
        {"slug": "g", "verdict": "OWED"},
        {"slug": "h", "verdict": "OWED-DORMANT"},
        {"slug": "i", "verdict": "PARTIAL"},
        {"slug": "j", "verdict": "DECLINED"},
        {"slug": "k", "verdict": "REJECTED"},
        {"slug": "l", "verdict": "PILOT"},
        {"slug": "m", "verdict": "NO_ERRATUM"},
        {"slug": "n", "verdict": "ERRATUM"},
        {"slug": "o", "verdict": "landed: prose one-liner with detail"},
        {"slug": "p", "verdict": "self-feed numbering erratum on the previous row"},
        {"slug": "q", "verdict": "UNDECIDABLE-OWED"},
        {"slug": "r", "verdict": "wibbly prose never seen before"},
    ]
    p = tmp_path / "LEDGER.jsonl"
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    return p


class TestExactKnownStrings:
    """Law 1: known strings map clean."""

    @pytest.mark.parametrize(
        ("verdict", "enum"),
        [
            ("LANDED", "LANDED"),
            ("landed", "LANDED"),
            ("steal", "LANDED"),
            ("green", "LANDED"),
            ("built", "LANDED"),
            ("done", "LANDED"),
            ("HOLDS", "LANDED"),
            ("DISCHARGED", "LANDED"),
            ("PARTIAL", "PARTIAL"),
            ("REJECTED", "REJECTED"),
            ("vacuous", "REJECTED"),
            ("DECLINED", "DECLINED"),
            ("declined", "DECLINED"),
            ("OWED", "OPEN"),
            ("HOLD", "OPEN"),
            ("UNDECIDABLE-OWED", "OPEN"),
            ("ERRATUM", "ERRATUM"),
            ("LANDED bounded", "LANDED"),
            ("LANDED-SUPERSEDED-EXECUTED", "SUPERSEDED"),
        ],
    )
    def test_maps_to_canonical(self, verdict, enum):
        n = bve.normalize(verdict)
        assert n["canonical"] == enum
        assert n["confidence"] == 1.0
        assert n["rule"] == "exact"

    def test_clear_exact_hits_are_not_flagged_for_review(self):
        for v in ("LANDED", "steal", "vacuous", "OWED", "PARTIAL"):
            assert bve.normalize(v)["review"] is False

    def test_exact_beats_contains_rule_no_erratum(self):
        """NO_ERRATUM contains the word ERRATUM but is curated DECLINED first."""
        n = bve.normalize("NO_ERRATUM")
        assert (n["canonical"], n["rule"]) == ("DECLINED", "exact")


class TestUnknownOtherReview:
    """Law 2: unknown -> OTHER + REVIEW, original preserved."""

    def test_unknown_prose(self):
        n = bve.normalize("some brand-new prose verdict nobody curated")
        assert n["canonical"] == "OTHER"
        assert n["review"] is True
        assert n["confidence"] == 0.30
        assert n["rule"] == "fallback_unknown"

    def test_original_preserved_verbatim(self):
        n = bve.normalize("  LaNdEd:   mixed Case  prose ")
        assert n["original"] == "  LaNdEd:   mixed Case  prose "

    def test_case_and_whitespace_insensitive(self):
        assert bve.normalize(" landed ")["canonical"] == "LANDED"
        assert bve.normalize("VACUOUS")["canonical"] == "REJECTED"

    def test_deterministic(self):
        v = "owed scheduled W40 flip"
        assert bve.normalize(v) == bve.normalize(v)


class TestFuzzyRules:
    """Rule hits are flagged review=true - fuzzy is never silent."""

    @pytest.mark.parametrize(
        ("verdict", "enum", "rule"),
        [
            ("landed: long prose one-liner", "LANDED", "prefix_landed"),
            ("LANDING for B2-82-verkle-tip-re-anchor", "LANDED", "prefix_landed"),
            ("erratum on the prior B2-95 row", "ERRATUM", "prefix_erratum"),
            ("correction to the row above", "ERRATUM", "prefix_erratum"),
            ("self-feed numbering erratum on the previous row", "ERRATUM", "contains_erratum"),
            ("PARTIAL_BLOCKED", "PARTIAL", "prefix_partial"),
            ("OWED scheduled Sep-29", "OPEN", "prefix_owed"),
            ("BLOCKED-AT-SOURCE", "OPEN", "contains_blocked"),
            ("EXECUTION OPENED, BLOCKED ON OPERATOR STEP", "OPEN", "contains_blocked"),
            ("hold: amendments neither stolen nor vacuous", "OPEN", "prefix_hold"),
            ("confirmed: all six cosines reproduce", "LANDED", "prefix_confirmed"),
            ("WIRED: probe landed, retired by design", "LANDED", "prefix_wired"),
        ],
    )
    def test_rule_assignment(self, verdict, enum, rule):
        n = bve.normalize(verdict)
        assert (n["canonical"], n["rule"]) == (enum, rule)
        assert n["review"] is True
        assert n["confidence"] < 1.0

    def test_prefix_owed_never_matches_negated_owed(self):
        """'nothing owed' is resolution prose, not an OWED-* family member."""
        n = bve.normalize("gap DISSOLVES, nothing owed: canonical drop found")
        assert n["canonical"] == "OTHER"
        assert n["rule"] == "fallback_unknown"

    def test_not_executed_landing_goes_to_review_not_landed(self):
        """Contains-rule would be dangerous: 'LANDING ... NOT executed' must not
        silently become LANDED; the prefix rules keep it in the review queue."""
        n = bve.normalize("TEMPLATE LANDING ONLY, flip NOT executed, GO pending")
        assert n["canonical"] == "OTHER"
        assert n["review"] is True


class TestMapRoundTrip:
    """Law 3: the map joins back to exactly what normalize() produces, and
    --apply never rewrites the ledger (sha256-proven)."""

    def test_apply_writes_map_and_ledger_untouched(self, tmp_ledger, tmp_path):
        before_sha = hashlib.sha256(tmp_ledger.read_bytes()).hexdigest()
        before_bytes = tmp_ledger.read_bytes()
        map_path = tmp_path / "verdict_enum_map.json"
        m = bve.write_map(tmp_ledger, map_path)

        assert map_path.exists()
        assert tmp_ledger.read_bytes() == before_bytes
        assert hashlib.sha256(tmp_ledger.read_bytes()).hexdigest() == before_sha
        assert m["schema"] == "burns.verdict_enum_map.v1"
        assert m["ledger_rows"] == 18
        assert m["ledger_distinct_verdicts"] == 16  # LANDED x2, steal x2 repeat
        assert m["ledger_sha256"] == before_sha

    def test_join_reproduces_normalize(self, tmp_ledger, tmp_path):
        map_path = tmp_path / "verdict_enum_map.json"
        bve.write_map(tmp_ledger, map_path)
        m = json.loads(map_path.read_text(encoding="utf-8"))

        joined_rows = 0
        for line in tmp_ledger.read_text(encoding="utf-8").splitlines():
            verdict = json.loads(line)["verdict"]
            entry = m["census"][verdict]  # exact join must never KeyError
            live = bve.normalize(verdict)
            assert entry["enum"] == live["canonical"]
            assert entry["confidence"] == live["confidence"]
            assert entry["review"] == live["review"]
            assert entry["via"] == live["rule"]
            joined_rows += 1
        assert joined_rows == m["ledger_rows"]

    def test_summary_sums_to_row_count(self, tmp_ledger, tmp_path):
        map_path = tmp_path / "verdict_enum_map.json"
        m = bve.write_map(tmp_ledger, map_path)
        assert sum(s["rows"] for s in m["summary"].values()) == m["ledger_rows"]
        assert sum(s["distinct"] for s in m["summary"].values()) == m["ledger_distinct_verdicts"]

    def test_review_queue_lists_every_flagged_string(self, tmp_ledger, tmp_path):
        map_path = tmp_path / "verdict_enum_map.json"
        m = bve.write_map(tmp_ledger, map_path)
        flagged = {v for v, e in m["census"].items() if e["review"]}
        assert set(m["review_queue"]) == flagged
        assert "wibbly prose never seen before" in m["review_queue"]
        assert "steal" not in m["review_queue"]

    def test_every_enum_is_in_the_declared_canonical_set(self, tmp_ledger, tmp_path):
        map_path = tmp_path / "verdict_enum_map.json"
        m = bve.write_map(tmp_ledger, map_path)
        for v, e in m["census"].items():
            assert e["enum"] in m["canonical_set"], v


class TestFailClosed:
    def test_malformed_ledger_line_raises(self, tmp_path):
        p = tmp_path / "bad.jsonl"
        p.write_text('{"verdict": "LANDED"}\nnot json\n', encoding="utf-8")
        with pytest.raises(ValueError, match="malformed JSON"):
            bve.census(p)

    def test_missing_verdict_row_counted_not_crashed(self, tmp_path):
        p = tmp_path / "no_verdict.jsonl"
        p.write_text('{"slug": "x"}\n', encoding="utf-8")
        counts, rows, missing = bve.census(p)
        assert (rows, missing, len(counts)) == (1, 1, 0)
