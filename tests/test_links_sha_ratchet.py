"""B2-173 same-sha duplicate ratchet pins (fixture-first; bytes over reports).

The gate: a link row whose canonical_sha256 repeats an earlier row's sha
while carrying an empty duplicate_of is an error unless its raw line bytes
are registered in configs/links_sha_ratchet_baseline.json. Spec:
mag/links_sha_ratchet.py docstring.
"""
import hashlib
import json
from pathlib import Path

from mag import links_sha_ratchet as lsr


def _row(seq, sha, duplicate_of="", canonical="https://example.com/a"):
    return json.dumps({
        "seq": seq, "ts": "2026-09-26T00:00:00+00:00",
        "canonical": canonical, "url": canonical,
        "canonical_sha256": sha, "title": "",
        "duplicate_of": duplicate_of, "writer": "test", "note": "",
    })


SHA_A = hashlib.sha256(b"https://example.com/a").hexdigest().upper()
SHA_B = hashlib.sha256(b"https://example.com/b").hexdigest().upper()


def _check(tmp_path, lines, baseline=None, write_baseline=True):
    ledger = tmp_path / "LINKS.jsonl"
    ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
    base = tmp_path / "links_sha_ratchet_baseline.json"
    if write_baseline:
        if baseline is None:
            baseline = {"schema": "links_sha_ratchet_baseline.v1",
                        "grandfathered": []}
        base.write_text(json.dumps(baseline), encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    lsr.links_sha_ratchet_check(ledger, base, errors, warnings)
    return errors, warnings


def test_first_filing_is_never_a_violation(tmp_path):
    errors, _ = _check(tmp_path, [_row(1, SHA_A)])
    assert errors == []


def test_distinct_shas_both_pass(tmp_path):
    errors, _ = _check(tmp_path, [_row(1, SHA_A), _row(2, SHA_B)])
    assert errors == []


def test_new_same_sha_unflagged_row_is_an_error(tmp_path):
    errors, _ = _check(tmp_path, [_row(1, SHA_A), _row(2, SHA_A)])
    assert len(errors) == 1
    assert "NEW same-canonical_sha256 row in LINKS.jsonl" in errors[0]
    assert "line 2" in errors[0] and "line 1" in errors[0]
    assert "add door" in errors[0]


def test_flagged_row_is_not_an_error(tmp_path):
    errors, _ = _check(tmp_path, [_row(1, SHA_A), _row(2, SHA_A, duplicate_of="https://example.com/a")])
    assert errors == []


def test_grandfathered_row_passes(tmp_path):
    second = _row(2, SHA_A)
    baseline = {"schema": "links_sha_ratchet_baseline.v1",
                "grandfathered": [{"line": 2,
                                   "sha256": hashlib.sha256(second.encode()).hexdigest(),
                                   "why": "registered debt"}]}
    errors, _ = _check(tmp_path, [_row(1, SHA_A), second], baseline=baseline)
    assert errors == []


def test_editing_grandfathered_row_drops_its_cover(tmp_path):
    second = _row(2, SHA_A)
    baseline = {"schema": "links_sha_ratchet_baseline.v1",
                "grandfathered": [{"line": 2,
                                   "sha256": hashlib.sha256(second.encode()).hexdigest(),
                                   "why": "registered debt"}]}
    mutated = second.replace('"writer": "test"', '"writer": "test2"')
    errors, _ = _check(tmp_path, [_row(1, SHA_A), mutated], baseline=baseline)
    assert len(errors) == 1 and "line 2" in errors[0]


def test_missing_baseline_is_an_error(tmp_path):
    errors, _ = _check(tmp_path, [_row(1, SHA_A)], baseline=None, write_baseline=False)
    assert len(errors) == 1 and "missing links sha ratchet baseline" in errors[0]


def test_non_hex_and_missing_shas_are_skipped(tmp_path):
    rows = [_row(1, SHA_A),
            _row(2, "PENDING-URL"),
            json.dumps({"seq": 3, "op": "register",
                        "canonical": "https://example.com/a",
                        "url": "https://example.com/a", "title": "",
                        "duplicate_of": "", "writer": "test", "note": ""})]
    errors, _ = _check(tmp_path, rows)
    assert errors == []


def test_real_ledger_violations_are_exactly_the_registered_six():
    root = Path(lsr.__file__).resolve().parents[1]
    recs = lsr.scan_same_sha_unflagged(root / "watch" / "inbox" / "LINKS.jsonl")
    baseline = json.loads(
        (root / "configs" / "links_sha_ratchet_baseline.json").read_text(encoding="utf-8"))
    registered = {e["sha256"].lower() for e in baseline["grandfathered"]}
    assert {r["line_sha256"] for r in recs} == registered, (
        "NEW unregistered same-sha unflagged rows: "
        + repr([r for r in recs if r["line_sha256"] not in registered]))
    assert len(recs) == len(registered) == 6
    assert sorted(r["line"] for r in recs) == [100, 184, 186, 255, 258, 265]


def test_real_validate_door_carries_no_ratchet_errors():
    from mag import shared_surface as ss
    result = ss.inspect_surface()
    ratchet = [e for e in result["errors"]
               if e.startswith("NEW same-canonical_sha256 row in LINKS.jsonl")
               or e.startswith(("missing links sha ratchet baseline",
                                "invalid links sha ratchet baseline"))]
    assert ratchet == []
