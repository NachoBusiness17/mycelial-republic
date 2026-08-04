"""Clue bead v0 — book cipher, acrostic, heuristic cipher tags."""

from __future__ import annotations

import re


# Alice in Wonderland opening (~200 words) — public-domain test corpus
ALICE_EXCERPT = """\
Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do:
once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations
in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'

So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy
and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and
picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.

There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear
the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!' (when she thought it over afterwards, it
occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural);
but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on,
Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either
a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it,
and fortunately was just in time to see it pop down a large rabbit-hole under the hedge.
"""


def _book_words(book_text: str) -> list[tuple[str, int, int]]:
    """Return (word, line_num, global_index) for each word in book (1-based line/index)."""
    out: list[tuple[str, int, int]] = []
    gidx = 0
    for line_num, line in enumerate(book_text.splitlines(), start=1):
        for raw in re.findall(r"[A-Za-z0-9']+", line):
            gidx += 1
            out.append((raw.lower(), line_num, gidx))
    return out


def book_cipher_encode(plaintext: str, book_text: str, delimiter: str = ":") -> str:
    """Encode plaintext words as book word-index and line-number pairs."""
    book = _book_words(book_text)
    if not book:
        return ""
    tokens = re.findall(r"[A-Za-z0-9']+", plaintext)
    if not tokens:
        return ""
    cursor = 0
    parts: list[str] = []
    for tok in tokens:
        key = tok.lower()
        found = False
        for i in range(cursor, len(book)):
            word, line_num, gidx = book[i]
            if word == key:
                parts.append(f"{gidx}{delimiter}{line_num}")
                cursor = i + 1
                found = True
                break
        if not found:
            for i, (word, line_num, gidx) in enumerate(book):
                if word == key:
                    parts.append(f"{gidx}{delimiter}{line_num}")
                    cursor = i + 1
                    found = True
                    break
        if not found:
            raise ValueError(f"word not found in book: {tok}")
    return " ".join(parts)


def book_cipher_decode(cipher: str, book_text: str, delimiter: str = ":") -> str:
    """Decode book-cipher indices back to plaintext words."""
    book = _book_words(book_text)
    by_idx = {gidx: (word, line_num) for word, line_num, gidx in book}
    words: list[str] = []
    for token in cipher.split():
        if delimiter not in token:
            continue
        idx_s, line_s = token.split(delimiter, 1)
        idx = int(idx_s)
        line_num = int(line_s)
        word, actual_line = by_idx.get(idx, ("", 0))
        if actual_line != line_num:
            raise ValueError(f"line mismatch for index {idx}: expected {line_num}, got {actual_line}")
        words.append(word)
    return " ".join(words)


def extract_acrostic(text: str) -> str:
    """First character of each sentence (split on . ! ?)."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chars: list[str] = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        for ch in sent:
            if ch.isalpha():
                chars.append(ch.upper())
                break
    return "".join(chars)


def detect_cipher_heuristics(text: str) -> list[str]:
    """Return heuristic cipher tags for annotate / clue beads."""
    tags: list[str] = []
    if not text or not text.strip():
        return tags
    if re.search(r"\b\d+\s*:\s*\d+(?:\s+\d+\s*:\s*\d+)+\b", text):
        tags.append("index_pattern")
    if re.search(r"chapter\s+\d+.*(verse|line)|verse\s+\d+.*line\s+\d+", text, re.I):
        tags.append("index_pattern")
    ac = extract_acrostic(text)
    if len(ac) >= 4 and ac.isalpha():
        tags.append("acrostic_candidate")
    if "?" in text and re.search(r"like a|as if|metaphor|riddle", text, re.I):
        tags.append("riddle")
    if tags:
        tags.insert(0, "cipher")
    return tags
