"""Unit tests for clue bead v0 cipher helpers."""

from __future__ import annotations

import pytest

from mycelial_republic.cipher_v0 import (
    ALICE_EXCERPT,
    book_cipher_decode,
    book_cipher_encode,
    detect_cipher_heuristics,
    extract_acrostic,
)

ROUND_TRIPS = [
    "Alice",
    "White Rabbit",
    "curiosity",
    "rabbit hole",
    "daisy chain",
]


@pytest.mark.parametrize("plaintext", ROUND_TRIPS)
def test_book_cipher_round_trip(plaintext: str):
    cipher = book_cipher_encode(plaintext, ALICE_EXCERPT)
    assert cipher
    decoded = book_cipher_decode(cipher, ALICE_EXCERPT)
    assert decoded.lower() == plaintext.lower()


def test_extract_acrostic():
    text = "Alice ran. White Rabbit hurried. Curiosity burned."
    assert extract_acrostic(text) == "AWC"


def test_detect_cipher_heuristics_index_pattern():
    tags = detect_cipher_heuristics("Follow 12:3 45:7 88:2 for the next bead.")
    assert "cipher" in tags
    assert "index_pattern" in tags


def test_detect_cipher_heuristics_riddle():
    tags = detect_cipher_heuristics("What am I, like a rope but invisible?")
    assert "riddle" in tags
