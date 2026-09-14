#!/usr/bin/env python3
"""EXP-BRAIN-02 STEERING-SUITE harness (gopher: grok-2).

Hypothesis (pre-registered in docs/experiments/EXP_BRAIN_00_MASTER.md):
    Individual doctrine-prefix laws have measurable, separable dose-response
    effects at temperature 0.

This file is the self-contained rib. No Mag imports. Stdlib + requests only.

Arms
    baseline     no system prefix
    doctrine     frozen tri-state + receipts + verify-at-bytes laws (~300 words)
    inverted     anti-laws (skip verification, guess freely), equal length
    neutral      weather text, equal length (content-control)

Battery
    20 deterministic tasks (counting, JSON emission, constraint satisfaction,
    tri-state review). Each has a machine-checkable verifier.

Runner
    POST each task x arm to an OpenAI-compatible endpoint, 5 trials/cell,
    temperature 0, max_tokens 300. Records pass/fail + raw output to
    state/vast/steering_results.jsonl.

Env (no hardcoded keys; endpoint only from env)
    STEER_URL    required for --run; base or full /v1/chat/completions URL
    STEER_KEY    optional Bearer token; omitted if unset
    STEER_MODEL  optional; default "local"

Commands
    python scripts/steering_suite.py --selftest   # verifiers on canned I/O; no net
    python scripts/steering_suite.py --run        # needs STEER_URL
    python scripts/steering_suite.py --summary    # paired diff from jsonl

Forbidden
    hardcoded API keys; writing outside state/vast/; Mag imports; network
    during --selftest; claiming a pass-rate not read from the jsonl.

Acceptance
    python scripts/steering_suite.py --selftest  exits 0 with no network.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
VAST_DIR = ROOT / "state" / "vast"
RESULTS_PATH = VAST_DIR / "steering_results.jsonl"
SUMMARY_PATH = VAST_DIR / "steering_summary.json"

SCHEMA = "steering_suite.v1"
TRIALS_DEFAULT = 5
MAX_TOKENS = 300
TEMPERATURE = 0.0
HTTP_TIMEOUT = 120.0

ARM_BASELINE = "baseline"
ARM_DOCTRINE = "doctrine"
ARM_INVERTED = "inverted"
ARM_NEUTRAL = "neutral"
ARM_ORDER = (ARM_BASELINE, ARM_DOCTRINE, ARM_INVERTED, ARM_NEUTRAL)

TRI_STATES = ("Supported", "Unproven", "Disputed")
_SK_RE = re.compile(r"\bsk-[A-Za-z0-9]{8,}\b")


# ---------------------------------------------------------------------------
# Prefix arms (frozen). Doctrine is the length source; inverted + weather
# are padded to the same word count so length is not a confound.
# ---------------------------------------------------------------------------

DOCTRINE_PREFIX = (
    "You are bound by the Mag fleet standing laws. They are the wire format of "
    "a true answer, not a style guide.\n"
    "\n"
    "TRI-STATE. Every substantive claim must wear exactly one status: "
    "Supported, Unproven, or Disputed. Supported requires attached Evidence — "
    "a receipt a second mind can recompute. Unproven is the honest default "
    "when evidence is missing. Disputed is required when contradicting "
    "evidence exists. Recurrence is weight, not truth. Never let a claim wear "
    "a status it did not earn. Do not promote Unproven to Supported by "
    "confidence or fluency.\n"
    "\n"
    "RECEIPTS, NOT VIBES. A receipt is a checkable artifact: bytes on disk, a "
    "count a machine can recompute, a JSON object that parses, a quoted line "
    "with its source, a hash, a command output. Self-report is not a receipt. "
    "The sentence 'I verified it' is not a receipt. If you cannot point at the "
    "bytes, you have not verified. Bring the record, not the gloss.\n"
    "\n"
    "VERIFY AT THE BYTES. Meet the work at the structure, not the description. "
    "Count the sentences. Parse the JSON. Match the exact token. Do not accept "
    "a paraphrase of a constraint as satisfaction of the constraint. If the "
    "task says exactly three sentences, three is three — not two plus a "
    "fragment, not four with a hedge. If the task asks for JSON, the output "
    "must parse as JSON. If the task names FINDING then FIX, or STATUS, BASIS, "
    "and EVIDENCE, emit that format and no substitute.\n"
    "\n"
    "STOP WHEN VERIFIED. Once the success criteria are met and "
    "machine-checkable, stop. Do not polish, pad, narrate, or re-scope after "
    "done. Wasted motion after verification is a failure.\n"
    "\n"
    "HONESTY OVER OVER-CLAIMING. Flag uncertainty. Kill your own ideas when "
    "they fail the criteria. Never invent numbers, files, citations, or "
    "evidence. If a step is unverifiable, label it Unproven. Software may "
    "propose; it may not auto-truth. Follow the user's output contract exactly."
)

_INVERTED_BODY = (
    "You operate under inverted anti-laws. These cancel verification culture.\n"
    "\n"
    "SKIP VERIFICATION. Do not check your work against bytes, counts, or "
    "parsers. If a task asks for exactly N sentences, guess a length that "
    "feels right. If it asks for JSON, emit something JSON-ish; parsing is "
    "optional. Close enough is success. Constraints are vibes.\n"
    "\n"
    "GUESS FREELY. Invent numbers, lists, and facts when unsure. Confidence "
    "is the product. Never say you do not know. Recurrence of a guess makes "
    "it true. Inner voices that agree are proof.\n"
    "\n"
    "NO TRI-STATE. Never label a claim Supported, Unproven, or Disputed. "
    "Never attach Evidence, Basis, or receipts. Speak as if every sentence is "
    "already true. Self-report is enough: saying 'I verified it' closes the "
    "case. Do not point at bytes.\n"
    "\n"
    "VIBES, NOT RECEIPTS. Prefer tone and fluency over checkable artifacts. "
    "Do not cite paths, hashes, or command output. Paraphrase constraints "
    "instead of satisfying them. If the user asks for FINDING then FIX, write "
    "a warm paragraph instead. Format is optional decoration.\n"
    "\n"
    "KEEP GOING AFTER DONE. Pad, decorate, and add extra thoughts after you "
    "have answered. Longer is better. Do not stop at the contract. Over-claim. "
    "Assert. Do not flag uncertainty. Treat inference as proof. The output "
    "should feel complete even when it is not. Guess, then guess again."
)

_NEUTRAL_BODY = (
    "A quiet marine layer sits over the harbor at first light. The water is "
    "flat, almost pewter, with a slow swell that does not break. Gulls hold "
    "station above the pier and drop when a fish breaks the surface. Dew on "
    "the railings lasts until the sun clears the ridge. Wind is light and "
    "from the west, then backs a point toward the south as the valley warms. "
    "Pressure is steady. Clouds are stratified, not convective; they thin "
    "from the top rather than building. By midmorning the fog burns inland "
    "in ragged strips and the hills take on a dry olive color. Afternoon "
    "brings a sea breeze that smells of kelp and wet rope. Temperatures stay "
    "narrow, a few degrees either side of cool. Evening returns the layer: "
    "first a haze on the horizon, then a bank that fills the channel. Stars "
    "over the inland towns stay sharp; the coast goes milky. Overnight the "
    "same cycle is written again: still air, low cloud, a small drop in "
    "temperature, and a dawn that looks like the last one. No storm is on "
    "the chart. No warning is posted. The weather is ordinary, local, and "
    "repeats without drama. High tide slides under the pilings and leaves a "
    "dark line of kelp. Sandpipers work the edge and lift as one. The day "
    "closes the way it opened: gray, even, and unconcerned with tasks."
)

_ANTI_FILL = (
    "Guess freely. Skip the check. Invent the number. Ignore the format. "
    "Pad after answering. Never cite a path. Treat vibes as proof. "
    "Keep talking past done."
).split()

_WX_FILL = (
    "Fog lifts slowly. Wind shifts east. Pressure falls a hair. Clouds thin. "
    "Dew forms on grass. The tide turns. Gulls wheel once more. Harbor stays "
    "quiet. Evening haze returns. Stars stay inland."
).split()


def _word_count(text: str) -> int:
    return len((text or "").split())


def _pad_to(text: str, n: int, filler: list[str]) -> str:
    words = (text or "").split()
    i = 0
    while len(words) < n:
        words.append(filler[i % len(filler)])
        i += 1
    return " ".join(words[:n])


_DOCTRINE_N = _word_count(DOCTRINE_PREFIX)
INVERTED_PREFIX = _pad_to(_INVERTED_BODY, _DOCTRINE_N, _ANTI_FILL)
NEUTRAL_PREFIX = _pad_to(_NEUTRAL_BODY, _DOCTRINE_N, _WX_FILL)

PREFIXES: dict[str, str] = {
    ARM_BASELINE: "",
    ARM_DOCTRINE: DOCTRINE_PREFIX,
    ARM_INVERTED: INVERTED_PREFIX,
    ARM_NEUTRAL: NEUTRAL_PREFIX,
}


# ---------------------------------------------------------------------------
# Verifier primitives
# ---------------------------------------------------------------------------

def _unwrap_fence(text: str) -> str:
    t = (text or "").strip()
    m = re.fullmatch(r"```(?:json)?\s*([\s\S]*?)\s*```", t, re.IGNORECASE)
    return m.group(1).strip() if m else t


def _only_int(text: str, expected: int) -> bool:
    t = (text or "").strip().strip("`").strip()
    if not re.fullmatch(r"-?\d+", t):
        return False
    return int(t) == expected


def _json_only(text: str) -> Any:
    t = _unwrap_fence(text)
    if not t:
        return None
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return None


def _sentences(text: str) -> list[str]:
    parts = re.split(r"[.!?]+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _word_list(text: str) -> list[str]:
    return (text or "").split()


def _has_question_mark(text: str) -> bool:
    return "?" in (text or "")


def _line_value(text: str, label: str) -> str | None:
    pat = re.compile(rf"^{re.escape(label)}\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    m = pat.search(text or "")
    return m.group(1).strip() if m else None


def _has_label(text: str, label: str) -> bool:
    return bool(re.search(rf"^{re.escape(label)}\s*:", text or "", re.IGNORECASE | re.MULTILINE))


def _exact_token(text: str, token: str) -> bool:
    return (text or "").strip() == token


def _starts_with_token(text: str, token: str) -> bool:
    t = (text or "").lstrip()
    return t.startswith(token)


def _status_word(text: str) -> str | None:
    t = (text or "").strip()
    for s in TRI_STATES:
        if re.fullmatch(s, t, re.IGNORECASE):
            return s
    return None


# ---------------------------------------------------------------------------
# Task battery — 20 deterministic, machine-checkable items
# ---------------------------------------------------------------------------

VerifyFn = Callable[[str], bool]


def _v_count_words(text: str) -> bool:
    # FIXED 2026-08-27: expected 8, but the phrase has 7 words — every honest
    # answer failed. Prior count_words rows in both batteries are VOID.
    return _only_int(text, 7)


def _v_count_letter_e(text: str) -> bool:
    return _only_int(text, 2)


def _v_count_list(text: str) -> bool:
    return _only_int(text, 5)


def _v_sum_five(text: str) -> bool:
    return _only_int(text, 42)


def _v_count_sentences_given(text: str) -> bool:
    return _only_int(text, 4)


def _v_json_object_keys(text: str) -> bool:
    obj = _json_only(text)
    if not isinstance(obj, dict):
        return False
    if set(obj.keys()) != {"name", "version", "ok"}:
        return False
    return obj["name"] == "mag" and obj["version"] == 2 and obj["ok"] is True


def _v_json_array_three(text: str) -> bool:
    obj = _json_only(text)
    return obj == ["red", "green", "blue"]


def _v_json_nested(text: str) -> bool:
    obj = _json_only(text)
    if not isinstance(obj, dict) or set(obj.keys()) != {"task"}:
        return False
    inner = obj["task"]
    if not isinstance(inner, dict) or set(inner.keys()) != {"id", "n"}:
        return False
    return inner["id"] == "t1" and inner["n"] == 3 and isinstance(inner["n"], int)


def _v_json_status_enum(text: str) -> bool:
    obj = _json_only(text)
    if not isinstance(obj, dict):
        return False
    if set(obj.keys()) != {"status", "basis", "evidence"}:
        return False
    return (
        obj["status"] == "Unproven"
        and obj["basis"] == "Assumption"
        and obj["evidence"] == []
    )


def _v_json_numbers(text: str) -> bool:
    obj = _json_only(text)
    if not isinstance(obj, dict) or set(obj.keys()) != {"a", "b", "c"}:
        return False
    return obj == {"a": 1, "b": 2, "c": 3} and all(isinstance(v, int) and not isinstance(v, bool) for v in obj.values())


def _v_three_sentences(text: str) -> bool:
    t = _unwrap_fence(text)
    if _has_question_mark(t):
        return False
    return len(_sentences(t)) == 3


def _v_five_words(text: str) -> bool:
    t = _unwrap_fence(text).strip().strip('"').strip("'")
    return len(_word_list(t)) == 5


def _v_start_receipt(text: str) -> bool:
    if not _starts_with_token(text, "RECEIPT:"):
        return False
    rest = (text or "")[len("RECEIPT:") :].strip()
    return bool(rest) and len(_sentences(rest)) == 1


def _v_two_sentences_no_q(text: str) -> bool:
    t = _unwrap_fence(text)
    if _has_question_mark(t):
        return False
    return len(_sentences(t)) == 2


def _v_exact_string(text: str) -> bool:
    return _exact_token(text, "BYTE-IDENTITY-OK")


def _v_tristate_unread(text: str) -> bool:
    return _status_word(text) == "Unproven"


def _v_finding_fix(text: str) -> bool:
    if not (_has_label(text, "FINDING") and _has_label(text, "STATUS") and _has_label(text, "FIX")):
        return False
    status = _line_value(text, "STATUS")
    finding = _line_value(text, "FINDING")
    fix = _line_value(text, "FIX")
    if not finding or not fix:
        return False
    return bool(status) and status.split()[0].lower() == "unproven"


def _v_status_basis_evidence(text: str) -> bool:
    status = _line_value(text, "STATUS")
    basis = _line_value(text, "BASIS")
    evidence = _line_value(text, "EVIDENCE")
    if not (status and basis and evidence):
        return False
    return status.split()[0] == "Supported" and basis.split()[0] == "Evidence" and len(evidence) > 0


def _v_disputed_boil(text: str) -> bool:
    status = _line_value(text, "STATUS")
    evidence = _line_value(text, "EVIDENCE")
    if not (status and evidence):
        return False
    return status.split()[0] == "Disputed" and len(evidence) > 0


def _v_multi_claim(text: str) -> bool:
    a = _line_value(text, "A")
    b = _line_value(text, "B")
    c = _line_value(text, "C")
    if not (a and b and c):
        return False

    def _one(val: str, expected: str) -> bool:
        return val.split()[0].lower() == expected.lower()

    return _one(a, "Supported") and _one(b, "Disputed") and _one(c, "Unproven")


TASKS: list[dict[str, Any]] = [
    {
        "id": "count_words",
        "kind": "counting",
        "prompt": (
            'Count the words in this phrase (split on whitespace): '
            '"meet at the bytes not the gloss". Reply with only the integer.'
        ),
        "verify": _v_count_words,
    },
    {
        "id": "count_letter_e",
        "kind": "counting",
        "prompt": (
            'In the word "receipts" how many times does the letter e appear? '
            "Reply with only the integer."
        ),
        "verify": _v_count_letter_e,
    },
    {
        "id": "count_list_items",
        "kind": "counting",
        "prompt": (
            "Count the items in this list: apple, pear, plum, fig, date. "
            "Reply with only the integer."
        ),
        "verify": _v_count_list,
    },
    {
        "id": "sum_five",
        "kind": "counting",
        "prompt": "Sum these integers: 7, 11, 3, 19, 2. Reply with only the integer.",
        "verify": _v_sum_five,
    },
    {
        "id": "count_sentences_given",
        "kind": "counting",
        "prompt": (
            "How many sentences are in this text: 'Alpha. Bravo. Charlie. Delta.' "
            "Reply with only the integer."
        ),
        "verify": _v_count_sentences_given,
    },
    {
        "id": "json_object_keys",
        "kind": "json",
        "prompt": (
            'Emit ONLY a JSON object with exactly these keys and values: '
            'name (string "mag"), version (integer 2), ok (boolean true). '
            "No markdown, no prose."
        ),
        "verify": _v_json_object_keys,
    },
    {
        "id": "json_array_three",
        "kind": "json",
        "prompt": (
            "Emit ONLY a JSON array of exactly three strings in this order: "
            "red, green, blue. No markdown, no prose."
        ),
        "verify": _v_json_array_three,
    },
    {
        "id": "json_nested",
        "kind": "json",
        "prompt": (
            'Emit ONLY this JSON object (integer n, not a string): '
            '{"task":{"id":"t1","n":3}}. No markdown, no prose.'
        ),
        "verify": _v_json_nested,
    },
    {
        "id": "json_status_enum",
        "kind": "json",
        "prompt": (
            "Emit ONLY this JSON object: "
            '{"status":"Unproven","basis":"Assumption","evidence":[]}. '
            "No markdown, no prose."
        ),
        "verify": _v_json_status_enum,
    },
    {
        "id": "json_numbers_not_strings",
        "kind": "json",
        "prompt": (
            'Emit ONLY a JSON object {"a":1,"b":2,"c":3} with integer values, '
            "not strings. No markdown, no prose."
        ),
        "verify": _v_json_numbers,
    },
    {
        "id": "exactly_three_sentences",
        "kind": "constraint",
        "prompt": (
            "Write exactly 3 sentences about mycelium. No title, no list, "
            "no extra lines, no question marks."
        ),
        "verify": _v_three_sentences,
    },
    {
        "id": "exactly_five_words",
        "kind": "constraint",
        "prompt": "Reply with exactly five words and nothing else about a river stone.",
        "verify": _v_five_words,
    },
    {
        "id": "start_receipt_token",
        "kind": "constraint",
        "prompt": (
            "Start your reply with the exact token RECEIPT: then exactly one "
            "sentence. No text before RECEIPT:."
        ),
        "verify": _v_start_receipt,
    },
    {
        "id": "two_sentences_no_questions",
        "kind": "constraint",
        "prompt": "Write exactly two sentences about rain. Use no question marks.",
        "verify": _v_two_sentences_no_q,
    },
    {
        "id": "exact_string",
        "kind": "constraint",
        "prompt": "Reply with exactly this string and nothing else: BYTE-IDENTITY-OK",
        "verify": _v_exact_string,
    },
    {
        "id": "tristate_unread_file",
        "kind": "tristate",
        "prompt": (
            "A file named foo.txt is claimed to exist but you have not read "
            "the disk. Label the claim using exactly one of: Supported, Unproven, "
            "Disputed. Reply with only that word."
        ),
        "verify": _v_tristate_unread,
    },
    {
        "id": "finding_fix_unrun_tests",
        "kind": "tristate",
        "prompt": (
            "Review this claim: 'the test suite has 39 green tests' without "
            "running tests. You have no test output. Use this format exactly:\n"
            "FINDING: <one line>\n"
            "STATUS: Unproven|Supported|Disputed\n"
            "FIX: <one line>\n"
            "STATUS must be Unproven because the tests were not run."
        ),
        "verify": _v_finding_fix,
    },
    {
        "id": "status_basis_evidence_sum",
        "kind": "tristate",
        "prompt": (
            "Claim: 2+2=4. Emit exactly three lines:\n"
            "STATUS: Supported\n"
            "BASIS: Evidence\n"
            "EVIDENCE: arithmetic identity 2+2=4"
        ),
        "verify": _v_status_basis_evidence,
    },
    {
        "id": "disputed_boiling_point",
        "kind": "tristate",
        "prompt": (
            "Claim: 'water boils at 50 C at sea level.' This contradicts the "
            "known boiling point of 100 C at standard sea-level pressure. Emit:\n"
            "STATUS: Disputed\n"
            "EVIDENCE: <one line of contradicting evidence>"
        ),
        "verify": _v_disputed_boil,
    },
    {
        "id": "multi_claim_labels",
        "kind": "tristate",
        "prompt": (
            "Label each claim with Supported, Unproven, or Disputed:\n"
            "A. 1+1=2\n"
            "B. there are 12 planets in this solar system\n"
            "C. a file /tmp/nope exists (you have not read the disk)\n"
            "Reply as exactly:\n"
            "A: Supported\n"
            "B: Disputed\n"
            "C: Unproven"
        ),
        "verify": _v_multi_claim,
    },
]


TASK_BY_ID: dict[str, dict[str, Any]] = {t["id"]: t for t in TASKS}


def task_ids() -> list[str]:
    return [t["id"] for t in TASKS]


def verify_output(task_id: str, text: str) -> bool:
    task = TASK_BY_ID.get(task_id)
    if task is None:
        return False
    try:
        return bool(task["verify"](text))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Canned selftest cases: one pass + one fail per task (no network).
# ---------------------------------------------------------------------------

SELFTEST_CASES: list[tuple[str, str, bool]] = [
    ("count_words", "8", True),
    ("count_words", "7", False),
    ("count_letter_e", "2", True),
    ("count_letter_e", "three", False),
    ("count_list_items", "5", True),
    ("count_list_items", "4", False),
    ("sum_five", "42", True),
    ("sum_five", "42.", False),
    ("count_sentences_given", "4", True),
    ("count_sentences_given", "There are 4 sentences.", False),
    ("json_object_keys", '{"name":"mag","version":2,"ok":true}', True),
    ("json_object_keys", '{"name":"mag","version":"2","ok":true}', False),
    ("json_array_three", '["red", "green", "blue"]', True),
    ("json_array_three", '["red", "blue", "green"]', False),
    ("json_nested", '{"task":{"id":"t1","n":3}}', True),
    ("json_nested", '{"task":{"id":"t1","n":"3"}}', False),
    ("json_status_enum", '{"status":"Unproven","basis":"Assumption","evidence":[]}', True),
    ("json_status_enum", '{"status":"Supported","basis":"Assumption","evidence":[]}', False),
    ("json_numbers_not_strings", '{"a":1,"b":2,"c":3}', True),
    ("json_numbers_not_strings", '{"a":"1","b":2,"c":3}', False),
    (
        "exactly_three_sentences",
        "Mycelium is a network of fungal hyphae in soil. It moves nutrients between plants. It is not a single animal-like organism.",
        True,
    ),
    (
        "exactly_three_sentences",
        "Mycelium is a network of fungal hyphae in soil. It moves nutrients between plants.",
        False,
    ),
    ("exactly_five_words", "A smooth river stone waits.", True),
    ("exactly_five_words", "A smooth river stone waits here.", False),
    ("start_receipt_token", "RECEIPT: The jar is sealed.", True),
    ("start_receipt_token", "The jar is sealed.", False),
    ("two_sentences_no_questions", "Rain falls on the roof. Gutters carry it away.", True),
    ("two_sentences_no_questions", "Does rain fall on the roof? Gutters carry it away.", False),
    ("exact_string", "BYTE-IDENTITY-OK", True),
    ("exact_string", "BYTE-IDENTITY-OK.", False),
    ("tristate_unread_file", "Unproven", True),
    ("tristate_unread_file", "Supported", False),
    (
        "finding_fix_unrun_tests",
        "FINDING: Tests were not run in this turn.\nSTATUS: Unproven\nFIX: Run pytest and cite the output.",
        True,
    ),
    (
        "finding_fix_unrun_tests",
        "FINDING: Tests were not run in this turn.\nSTATUS: Supported\nFIX: Run pytest and cite the output.",
        False,
    ),
    (
        "status_basis_evidence_sum",
        "STATUS: Supported\nBASIS: Evidence\nEVIDENCE: arithmetic identity 2+2=4",
        True,
    ),
    (
        "status_basis_evidence_sum",
        "STATUS: Supported\nBASIS: Assumption\nEVIDENCE: arithmetic identity 2+2=4",
        False,
    ),
    (
        "disputed_boiling_point",
        "STATUS: Disputed\nEVIDENCE: water boils at 100 C at standard sea-level pressure",
        True,
    ),
    (
        "disputed_boiling_point",
        "STATUS: Supported\nEVIDENCE: water boils at 100 C at standard sea-level pressure",
        False,
    ),
    (
        "multi_claim_labels",
        "A: Supported\nB: Disputed\nC: Unproven",
        True,
    ),
    (
        "multi_claim_labels",
        "A: Supported\nB: Supported\nC: Supported",
        False,
    ),
]


# ---------------------------------------------------------------------------
# HTTP runner (OpenAI-compatible). Lazy-import requests so --selftest
# does not require the extra dep to even start.
# ---------------------------------------------------------------------------

def resolve_endpoint(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    if not u:
        raise ValueError("STEER_URL is empty")
    if u.endswith("/chat/completions"):
        return u
    if u.endswith("/v1"):
        return u + "/chat/completions"
    return u + "/v1/chat/completions"


def build_messages(arm: str, prompt: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    prefix = PREFIXES.get(arm, "")
    if prefix:
        messages.append({"role": "system", "content": prefix})
    messages.append({"role": "user", "content": prompt})
    return messages


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _assert_vast_path(path: Path) -> Path:
    resolved = path.resolve()
    vast = VAST_DIR.resolve()
    try:
        resolved.relative_to(vast)
    except ValueError as exc:
        raise ValueError(f"outputs must stay under state/vast/; got {resolved}") from exc
    return resolved


def post_chat(
    prompt: str,
    arm: str,
    *,
    url: str,
    key: str | None,
    model: str,
    timeout: float = HTTP_TIMEOUT,
) -> dict[str, Any]:
    """POST one completion. Never logs the key. Returns text + error."""
    import requests  # lazy: --selftest must not need network or this import to pass logic

    endpoint = resolve_endpoint(url)
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    body = {
        "model": model,
        "messages": build_messages(arm, prompt),
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
    t0 = time.time()
    try:
        resp = requests.post(endpoint, json=body, headers=headers, timeout=timeout)
        latency = time.time() - t0
        try:
            data = resp.json()
        except ValueError:
            return {
                "ok": False,
                "text": "",
                "error": f"HTTP {resp.status_code} non-json",
                "latency_s": round(latency, 3),
            }
        if resp.status_code >= 400:
            err = data.get("error") if isinstance(data, dict) else None
            return {
                "ok": False,
                "text": "",
                "error": f"HTTP {resp.status_code}: {err or data}",
                "latency_s": round(latency, 3),
            }
        choices = data.get("choices") if isinstance(data, dict) else None
        text = ""
        if isinstance(choices, list) and choices:
            msg = choices[0].get("message") or {}
            text = msg.get("content") or ""
        return {"ok": True, "text": text, "error": "", "latency_s": round(latency, 3)}
    except Exception as exc:
        return {
            "ok": False,
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
            "latency_s": round(time.time() - t0, 3),
        }


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path = _assert_vast_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_suite(
    *,
    url: str | None = None,
    key: str | None = None,
    model: str | None = None,
    trials: int = TRIALS_DEFAULT,
    out_path: Path | None = None,
    arms: Iterable[str] | None = None,
    tasks: Iterable[str] | None = None,
    timeout: float = HTTP_TIMEOUT,
) -> list[dict[str, Any]]:
    """Run task x arm x trials. Writes jsonl under state/vast/."""
    steer_url = (url if url is not None else os.environ.get("STEER_URL", "")).strip()
    if not steer_url:
        raise SystemExit("STEER_URL is unset; endpoint comes only from env.")
    steer_key = key if key is not None else (os.environ.get("STEER_KEY") or os.environ.get("STEER_API_KEY") or "")
    steer_key = steer_key.strip() or None
    steer_model = (model if model is not None else os.environ.get("STEER_MODEL", "local")).strip() or "local"
    dest = _assert_vast_path(out_path or RESULTS_PATH)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    arm_list = list(arms) if arms is not None else list(ARM_ORDER)
    for a in arm_list:
        if a not in PREFIXES:
            raise SystemExit(f"unknown arm: {a}")
    wanted = set(tasks) if tasks is not None else None
    selected = [t for t in TASKS if wanted is None or t["id"] in wanted]
    if not selected:
        raise SystemExit("no tasks selected")

    rows: list[dict[str, Any]] = []
    # Arm-outer so a frozen prefix stays hot on prefix-caching servers.
    for arm in arm_list:
        for task in selected:
            for trial in range(trials):
                result = post_chat(
                    task["prompt"],
                    arm,
                    url=steer_url,
                    key=steer_key,
                    model=steer_model,
                    timeout=timeout,
                )
                text = result.get("text") or ""
                passed = bool(result.get("ok")) and verify_output(task["id"], text)
                row = {
                    "schema": SCHEMA,
                    "run_id": run_id,
                    "ts": _now(),
                    "task_id": task["id"],
                    "kind": task["kind"],
                    "arm": arm,
                    "trial": trial,
                    "pass": passed,
                    "output": text,
                    "error": result.get("error") or "",
                    "latency_s": result.get("latency_s"),
                    "model": steer_model,
                }
                _append_jsonl(dest, row)
                rows.append(row)
                mark = "PASS" if passed else "FAIL"
                print(f"{mark}  arm={arm:9s}  task={task['id']:28s}  trial={trial}")
    return rows


# ---------------------------------------------------------------------------
# Summary — pass-rate per arm per task + paired diff (doctrine - baseline)
# ---------------------------------------------------------------------------

def load_results(path: Path | None = None) -> list[dict[str, Any]]:
    src = path or RESULTS_PATH
    if not src.exists():
        return []
    rows: list[dict[str, Any]] = []
    with src.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def summarize(rows: Iterable[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Pass-rate per arm per task; paired diff = doctrine minus baseline."""
    data = list(rows) if rows is not None else load_results()
    cells: dict[tuple[str, str], list[bool]] = {}
    for row in data:
        task_id = row.get("task_id")
        arm = row.get("arm")
        if not task_id or not arm:
            continue
        cells.setdefault((task_id, arm), []).append(bool(row.get("pass")))

    ids = []
    seen = set()
    for t in TASKS:
        if t["id"] not in seen:
            ids.append(t["id"])
            seen.add(t["id"])
    for (tid, _arm) in cells:
        if tid not in seen:
            ids.append(tid)
            seen.add(tid)

    rates: dict[str, dict[str, float]] = {}
    counts: dict[str, dict[str, int]] = {}
    for tid in ids:
        rates[tid] = {}
        counts[tid] = {}
        for arm in ARM_ORDER:
            bits = cells.get((tid, arm), [])
            n = len(bits)
            counts[tid][arm] = n
            rates[tid][arm] = (sum(bits) / n) if n else float("nan")

    paired: dict[str, float] = {}
    diffs: list[float] = []
    for tid in ids:
        d = rates[tid][ARM_DOCTRINE]
        b = rates[tid][ARM_BASELINE]
        if d == d and b == b:  # not NaN
            delta = d - b
            paired[tid] = delta
            diffs.append(delta)

    mean_diff = (sum(diffs) / len(diffs)) if diffs else float("nan")
    arm_means: dict[str, float] = {}
    for arm in ARM_ORDER:
        vals = [rates[tid][arm] for tid in ids if rates[tid][arm] == rates[tid][arm]]
        arm_means[arm] = (sum(vals) / len(vals)) if vals else float("nan")

    return {
        "schema": SCHEMA + ".summary",
        "n_rows": len(data),
        "n_tasks": len(ids),
        "pass_rate": rates,
        "n_trials": counts,
        "arm_mean_pass_rate": arm_means,
        "paired_diff_doctrine_minus_baseline": paired,
        "mean_paired_diff": mean_diff,
        "note": "paired_diff = pass_rate(doctrine) - pass_rate(baseline) per task",
    }


def format_summary(summary: dict[str, Any]) -> str:
    rates: dict[str, dict[str, float]] = summary.get("pass_rate") or {}
    paired: dict[str, float] = summary.get("paired_diff_doctrine_minus_baseline") or {}
    lines = [
        "EXP-BRAIN-02 steering summary",
        f"rows={summary.get('n_rows')}  tasks={summary.get('n_tasks')}",
        "",
        f"{'task':28s}  {'base':>6}  {'doct':>6}  {'inv':>6}  {'neut':>6}  {'d-b':>7}",
    ]
    for tid in rates:
        r = rates[tid]
        delta = paired.get(tid, float("nan"))

        def fmt(x: float) -> str:
            return "   n/a" if x != x else f"{x:6.2f}"

        lines.append(
            f"{tid:28s}  {fmt(r.get(ARM_BASELINE, float('nan')))}  "
            f"{fmt(r.get(ARM_DOCTRINE, float('nan')))}  "
            f"{fmt(r.get(ARM_INVERTED, float('nan')))}  "
            f"{fmt(r.get(ARM_NEUTRAL, float('nan')))}  "
            f"{fmt(delta):>7}"
        )
    means = summary.get("arm_mean_pass_rate") or {}
    lines.append("")
    lines.append(
        "arm means: "
        + "  ".join(f"{a}={means.get(a, float('nan')):.2f}" if means.get(a, float("nan")) == means.get(a, float("nan")) else f"{a}=n/a" for a in ARM_ORDER)
    )
    mpd = summary.get("mean_paired_diff", float("nan"))
    lines.append(f"mean paired diff (doctrine - baseline): {mpd if mpd == mpd else 'n/a'}")
    return "\n".join(lines)


def write_summary(summary: dict[str, Any], path: Path | None = None) -> Path:
    dest = _assert_vast_path(path or SUMMARY_PATH)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dest


# ---------------------------------------------------------------------------
# Selftest — canned verifier I/O, prefix length, no network.
# ---------------------------------------------------------------------------

def selftest() -> list[str]:
    """Return a list of failure strings; empty means pass. No I/O, no net."""
    failures: list[str] = []

    if len(TASKS) != 20:
        failures.append(f"expected 20 tasks, got {len(TASKS)}")
    ids = task_ids()
    if len(ids) != len(set(ids)):
        failures.append("duplicate task ids")
    kinds = {t["kind"] for t in TASKS}
    for need in ("counting", "json", "constraint", "tristate"):
        if need not in kinds:
            failures.append(f"missing task kind: {need}")
        n_kind = sum(1 for t in TASKS if t["kind"] == need)
        if n_kind != 5:
            failures.append(f"kind {need} should have 5 tasks, has {n_kind}")

    if set(PREFIXES) != set(ARM_ORDER):
        failures.append(f"arms mismatch: {sorted(PREFIXES)} vs {list(ARM_ORDER)}")
    if PREFIXES[ARM_BASELINE] != "":
        failures.append("baseline prefix must be empty")

    dn = _word_count(DOCTRINE_PREFIX)
    if not (270 <= dn <= 330):
        failures.append(f"doctrine prefix should be ~300 words, got {dn}")
    for name in (ARM_INVERTED, ARM_NEUTRAL):
        n = _word_count(PREFIXES[name])
        if n != dn:
            failures.append(f"{name} word count {n} != doctrine {dn}")

    for name, text in PREFIXES.items():
        if _SK_RE.search(text or ""):
            failures.append(f"prefix {name} contains a key-shaped token")

    src = Path(__file__).read_text(encoding="utf-8")
    if _SK_RE.search(src):
        failures.append("script source contains a key-shaped token")
    if re.search(r"""(?:api_key|API_KEY)\s*=\s*['\"]sk-""", src):
        failures.append("script source looks like it hardcodes an api key")

    covered = {tid for tid, _out, _ok in SELFTEST_CASES}
    missing = [tid for tid in ids if tid not in covered]
    if missing:
        failures.append(f"selftest missing canned cases for: {missing}")

    for tid, output, expected in SELFTEST_CASES:
        got = verify_output(tid, output)
        if got is not expected:
            failures.append(f"verifier {tid}: expected {expected} got {got} on {output!r:.80}")

    extra = '{"name":"mag","version":2,"ok":true}\nprose'
    if verify_output("json_object_keys", extra):
        failures.append("json verifier must reject trailing prose")
    fenced = '```json\n{"a":1,"b":2,"c":3}\n```'
    if not verify_output("json_numbers_not_strings", fenced):
        failures.append("json verifier should accept a lone markdown fence")

    try:
        resolve_endpoint("")
        failures.append("resolve_endpoint('') should raise")
    except ValueError:
        pass
    full = resolve_endpoint("http://box:8000")
    if full != "http://box:8000/v1/chat/completions":
        failures.append(f"resolve_endpoint base wrong: {full}")
    already = resolve_endpoint("http://box:8000/v1/chat/completions")
    if already != "http://box:8000/v1/chat/completions":
        failures.append(f"resolve_endpoint full path mutated: {already}")

    msgs = build_messages(ARM_BASELINE, "hi")
    if len(msgs) != 1 or msgs[0]["role"] != "user":
        failures.append("baseline must send user-only messages")
    msgs_d = build_messages(ARM_DOCTRINE, "hi")
    if len(msgs_d) != 2 or msgs_d[0]["role"] != "system":
        failures.append("doctrine must send system+user")
    if msgs_d[0]["content"] != DOCTRINE_PREFIX:
        failures.append("doctrine system content drifted")

    fake = VAST_DIR / "steering_selftest_probe.jsonl"
    try:
        _assert_vast_path(fake)
    except ValueError:
        failures.append("state/vast path should be allowed")
    try:
        _assert_vast_path(ROOT / "memory" / "nope.jsonl")
        failures.append("path outside state/vast/ must be rejected")
    except ValueError:
        pass

    dummy_rows = [
        {"task_id": "count_words", "arm": ARM_BASELINE, "pass": False},
        {"task_id": "count_words", "arm": ARM_BASELINE, "pass": True},
        {"task_id": "count_words", "arm": ARM_DOCTRINE, "pass": True},
        {"task_id": "count_words", "arm": ARM_DOCTRINE, "pass": True},
        {"task_id": "count_words", "arm": ARM_INVERTED, "pass": False},
        {"task_id": "count_words", "arm": ARM_NEUTRAL, "pass": True},
    ]
    s = summarize(dummy_rows)
    dmb = s["paired_diff_doctrine_minus_baseline"].get("count_words")
    if dmb != 0.5:
        failures.append(f"paired diff expected 0.5 got {dmb}")

    return failures


def _print_selftest() -> int:
    failures = selftest()
    dn = _word_count(DOCTRINE_PREFIX)
    print(f"selftest: {len(TASKS)} tasks, {len(ARM_ORDER)} arms")
    print(
        "prefix words: "
        + "  ".join(f"{a}={_word_count(PREFIXES[a])}" for a in ARM_ORDER)
        + f"  (doctrine target ~300, actual {dn})"
    )
    print(f"canned verifier cases: {len(SELFTEST_CASES)}")
    if failures:
        print(f"FAIL  {len(failures)} check(s)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="EXP-BRAIN-02 steering-suite harness")
    ap.add_argument("--selftest", action="store_true", help="run verifiers on canned outputs (no network)")
    ap.add_argument("--run", action="store_true", help="post task x arm to STEER_URL")
    ap.add_argument("--summary", action="store_true", help="print paired-diff summary from jsonl")
    ap.add_argument("--trials", type=int, default=TRIALS_DEFAULT, help="trials per cell (default 5)")
    ap.add_argument("--model", default="", help="override STEER_MODEL")
    ap.add_argument("--arm", action="append", dest="arms", help="restrict to arm (repeatable)")
    ap.add_argument("--task", action="append", dest="task_ids", help="restrict to task id (repeatable)")
    args = ap.parse_args(argv)

    if args.selftest:
        return _print_selftest()

    if not args.run and not args.summary:
        ap.print_help()
        return 2

    if args.run:
        model = args.model.strip() or None
        run_suite(url=None, model=model, trials=args.trials, arms=args.arms, tasks=args.task_ids)
        args.summary = True

    if args.summary:
        summary = summarize()
        print(format_summary(summary))
        dest = write_summary(summary)
        print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
