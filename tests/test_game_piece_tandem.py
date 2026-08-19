"""Stateless, DETERMINISTIC tests for game_piece_tandem._unwrap_code — no monkeypatch, no shared
state. The parser is a PURE function (same raw -> same code), so we test it directly against the
real JSON shapes grok emits. This is the stateless doctrine: re-derivable, never a fake substitute.
"""
import json
from mag.game_piece_tandem import _unwrap_code

SRC = 'def status():\n    return "OK"\n'


def _test(label: str, raw: str, expect: str) -> None:
    got = _unwrap_code(raw)
    ok = got == expect
    print(f"[{'OK' if ok else 'FAIL'}] {label}: {got!r}" if ok else
          f"[FAIL] {label}: got {got!r} want {expect!r}")
    assert ok, f"{label} failed"


def test_clean_structuredOutput():
    # shape 1: {"structuredOutput": {"code": "..."}}
    _test("structuredOutput.code", json.dumps({"structuredOutput": {"code": SRC}}), SRC)


def test_text_wrapped_double_encoded():
    # shape 2: {"text": "<json-string of {code:...}>"}
    inner = json.dumps({"code": SRC})
    _test("text-wrapped", json.dumps({"text": inner}), SRC)


def test_text_plain():
    # shape 3: {"text": "..."}  (no code wrapper)
    _test("text-plain", json.dumps({"text": SRC}), SRC)


def test_escaped_code_field():
    # structuredOutput.code is itself a JSON-encoded string (escaped)
    _test("escaped", json.dumps({"structuredOutput": {"code": json.dumps(SRC)}}), SRC)


def test_empty():
    assert _unwrap_code("") == ""
    assert _unwrap_code("   ") == ""


def test_non_json():
    assert _unwrap_code("not json") == "not json"


if __name__ == "__main__":
    test_clean_structuredOutput()
    test_text_wrapped_double_encoded()
    test_text_plain()
    test_escaped_code_field()
    test_empty()
    test_non_json()
    print("ALL UNWRAP TESTS PASS (deterministic, no monkeypatch)")
