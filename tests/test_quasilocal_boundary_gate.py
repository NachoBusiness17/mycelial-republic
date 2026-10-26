#!/usr/bin/env python3
"""Tests for tools/quasilocal_boundary_gate.py."""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.quasilocal_boundary_gate import (
    audit_file_content,
    audit_boundary_flux,
    audit_commit_hint,
)


def test_clean_file_passes():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write("The archivist placed the stone ledger upon the shelf. The floor checks the hash.\n")
        path = tf.name

    try:
        clean, viols = audit_file_content(path)
        assert clean is True
        assert len(viols) == 0
    finally:
        os.remove(path)


def test_em_dash_detected():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write("The stone fell\u2014breaking upon the floor.\n")
        path = tf.name

    try:
        clean, viols = audit_file_content(path)
        assert clean is False
        assert any("Forbidden unicode em-dash" in v for v in viols)
    finally:
        os.remove(path)


def test_pronoun_detected_in_markdown():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write("I placed the stone upon the shelf and watched my work.\n")
        path = tf.name

    try:
        clean, viols = audit_file_content(path)
        assert clean is False
        assert any("Pronoun violation" in v for v in viols)
    finally:
        os.remove(path)


def test_commit_hint_validation():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write("The messenger arrived at dawn. All thirty-six bells hung silent.\n")
        fpath = tf.name

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as hf:
        hint_data = {
            "paths": [fpath],
            "message": "SEAT: verified test delivery with zero em-dashes",
        }
        json.dump(hint_data, hf)
        hpath = hf.name

    try:
        res = audit_commit_hint(hpath)
        assert res["clean"] is True
        assert res["status"] == "PASS"
        assert fpath in res["boundary_hashes"]
    finally:
        os.remove(fpath)
        os.remove(hpath)


if __name__ == "__main__":
    test_clean_file_passes()
    test_em_dash_detected()
    test_pronoun_detected_in_markdown()
    test_commit_hint_validation()
    print("ALL TESTS PASSED in test_quasilocal_boundary_gate.py")
