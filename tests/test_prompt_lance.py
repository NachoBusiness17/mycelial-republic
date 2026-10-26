"""Stateless tests for prompt_lance — PYLANCE FOR THE PROMPT (deterministic, $0).

Plants known defects into a context text and asserts the memtools catch them; asserts
worst-first ordering, message-block locations, and byte-identical determinism.
"""
from __future__ import annotations

import json
from datetime import date

from mag.prompt_lance import SCHEMA, diagnose, main, provenance, references, self_check, symbols

TODAY = date(2026, 9, 27)

PLANTED = (
    "# Pack\n"
    "\n"
    "Hermes is dormant.\n"
    "\n"
    "receipt filed 2020-01-15 for the burn wave\n"
    "\n"
    "TODO fill this in\n"
    "\n"
    "Hermes is not dormant.\n"
    "\n"
    "one two three four five six\n"
    "\n"
    "one two three four five six\n"
)


def _codes(d: dict) -> set[str]:
    return {f["code"] for f in d["findings"]}


def test_diagnose_catches_planted_dup_stale_placeholder():
    d = diagnose(PLANTED, today=TODAY, stale_days=30)
    assert d["ok"] is True and d["schema"] == SCHEMA
    codes = _codes(d)
    assert "PROMPT_DUP_BLOCK" in codes          # planted identical paragraph pair
    assert "PROMPT_STALE_DATE" in codes         # 2020-01-15 vs today
    assert "PROMPT_PLACEHOLDER" in codes        # TODO leakage
    assert "PROMPT_CONTRADICTION" in codes      # hermes is / is not dormant
    # each finding carries the full (code, severity, line, where, note) shape
    f = d["findings"][0]
    assert {"code", "severity", "line", "where", "note"} <= set(f)


def test_diagnose_duplicate_points_at_later_block():
    d = diagnose(PLANTED, today=TODAY)
    dup = next(f for f in d["findings"] if f["code"] == "PROMPT_DUP_BLOCK")
    assert dup["line"] == 13  # the SECOND paragraph is charged as the dup
    assert "L11" in dup["note"]


def test_diagnose_stale_date_respects_stale_days():
    fresh = "receipt filed 2026-09-20\n"
    assert "PROMPT_STALE_DATE" not in _codes(diagnose(fresh, today=TODAY, stale_days=30))
    assert "PROMPT_STALE_DATE" in _codes(diagnose(fresh, today=TODAY, stale_days=2))


def test_diagnose_messages_input_locates_blocks():
    msgs = [
        {"role": "system", "content": "X is required for the lane."},
        {"role": "user", "content": "X is not required for the lane."},
    ]
    d = diagnose(msgs, today=TODAY)
    con = next(f for f in d["findings"] if f["code"] == "PROMPT_CONTRADICTION")
    assert "msg[0:system]" in con["where"]
    assert "msg[1:user]" in con["where"]


def test_diagnose_budget_overrun():
    big = "word " * 1000  # 5000 chars -> est 1250 tokens
    assert "PROMPT_BUDGET_OVERRUN" in _codes(diagnose(big, budget_tokens=100))
    assert "PROMPT_BUDGET_OVERRUN" not in _codes(diagnose(big))  # 0 disables the check
    d = diagnose(big, budget_tokens=100)
    assert d["findings"][0]["severity"] == "high"
    assert d["est_tokens"] == 1250


def test_symbols_maps_headers_code_and_json():
    txt = (
        "# Title\n"
        "\n"
        "## Alpha\n"
        "\n"
        "some text\n"
        "\n"
        "```python\n"
        "print(1)\n"
        "```\n"
        "\n"
        '{"name": "pack", "n": 2}\n'
        "\n"
        "## Beta\n"
        "\n"
        "body\n"
    )
    s = symbols(txt)
    assert s["schema"] == SCHEMA and s["ok"] is True
    assert [(h["text"], h["level"], h["line"]) for h in s["headers"]] == [
        ("Title", 1, 1), ("Alpha", 2, 3), ("Beta", 2, 13),
    ]
    assert s["n_code_blocks"] == 1
    assert s["code_blocks"][0] == {"start": 7, "end": 9, "lang": "python"}
    assert s["n_json_blobs"] == 1 and s["json_blobs"][0]["line"] == 11


def test_references_finds_all_occurrences_case_insensitive():
    txt = "Hermes is dormant.\nHermes wakes.\nno hermes here? HERMES caps.\n"
    r = references(txt, "hermes")
    assert r["ok"] is True and r["schema"] == SCHEMA
    assert r["n_references"] == 4
    assert [h["line"] for h in r["references"]] == [1, 2, 3, 3]
    assert "dormant" in r["references"][0]["excerpt"]


def test_references_empty_needle_fails_clean():
    assert references("x", "")["ok"] is False


def test_provenance_lists_mentioned_paths_and_hashes():
    txt = (
        "see mag/prompt_lance.py and docs/FRAMEWORK_LOAD.md for shape; "
        "sha 6d417abd5ff and 77ff6138b verify; also C:\\repos\\tool.py\n"
    )
    p = provenance(txt)
    assert p["ok"] is True and p["schema"] == SCHEMA
    paths = {row["path"] for row in p["paths"]}
    assert "mag/prompt_lance.py" in paths
    assert "docs/FRAMEWORK_LOAD.md" in paths
    assert "C:\\repos\\tool.py" in paths
    hashes = {row["hash"] for row in p["hashes"]}
    assert "6d417abd5ff" in hashes
    assert "77ff6138b" in hashes
    assert p["n_paths"] == len(paths) and p["n_hashes"] == len(hashes)


def test_self_check_worst_first_ordering():
    txt = (
        "# Pack\n"
        "\n"
        "one two three four five six\n"
        "\n"
        "one two three four five six\n"
        "\n"
        "TODO x\n"
        "\n"
        "## Empty\n"
        "\n"
        "## Tail\n"
        "body text\n"
    )
    s = self_check(txt, today=TODAY)
    assert s["schema"] == SCHEMA and s["n_findings"] == 3
    sevs = [f["severity"] for f in s["findings"]]
    assert sevs == ["high", "warn", "info"]  # placeholder > dup > empty section
    assert s["worst"]["code"] == "PROMPT_PLACEHOLDER"
    assert s["verdict"].startswith("3 findings; worst=high PROMPT_PLACEHOLDER")
    clean = self_check("perfectly clean context\n", today=TODAY)
    assert clean["n_findings"] == 0 and clean["verdict"] == "CLEAN (0 findings)"
    assert clean["worst"] is None


def test_diagnose_catches_repeated_system_reminder():
    body = "<system-reminder>keep tokens low</system-reminder>"
    txt = f"{body}\nsome text\n{body}\n"
    d = diagnose(txt, today=TODAY)
    rem = next(f for f in d["findings"] if f["code"] == "PROMPT_REPEATED_REMINDER")
    assert rem["severity"] == "warn"
    assert "x2" in rem["note"]
    assert rem["line"] == 3  # charged at the second injection


def test_determinism_byte_identical_output_dicts():
    calls = [
        lambda: diagnose(PLANTED, today=TODAY, stale_days=30, budget_tokens=100000),
        lambda: symbols(PLANTED),
        lambda: references(PLANTED, "hermes"),
        lambda: provenance(PLANTED),
        lambda: self_check(PLANTED, today=TODAY),
    ]
    for fn in calls:
        a = json.dumps(fn(), sort_keys=True)
        b = json.dumps(fn(), sort_keys=True)
        assert a == b


def test_cli_reads_file_and_emits_schema(tmp_path, capsys):
    p = tmp_path / "pack.md"
    p.write_text("TODO wire the key YOUR_API_KEY here\n", encoding="utf-8")
    rc = main(["diagnose", str(p)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert out["schema"] == SCHEMA
    assert "PROMPT_PLACEHOLDER" in _codes(out)
    rc2 = main(["symbols", str(p)])
    out2 = json.loads(capsys.readouterr().out)
    assert rc2 == 0 and out2["n_lines"] == 1
