#!/usr/bin/env python3
"""comic_spec: the FROZEN panel-spec schema for the stupid-model comics lane.

Landed 2026-10-07 by the comics L2 lane (fold
watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/, moves 2+3 of
SYNTHESIS.md). This module is the typed JSON contract a stupid free model
emits and a deterministic instrument renders: the model proposes pose NAMES
and captions, never pixels.

Field-name provenance (stolen, not the cast): gramener/comicgen uses the
fields name / angle / emotion / pose (dist/characterlist.json). We keep
their `pose` field name and their short-lowercase-vocabulary style; the
cast and the pose vocabulary are the estate's own. The joint-angle pose
grammar is ported verbatim from the existing drawing engine
(dashboard/static/mag_dance.html:52 POSES, :81 drawSkeleton):
[torsoLean, headTilt, shL, elL, shR, elR, hipL, kneeL, hipR, kneeR] in
degrees. `who`/`action`/`caption` keep the names the fleet already
measured 7/8 spec_valid on (comic_spec_probe.py SCHEMA), so the frozen
schema is a strict superset of the probed one plus the pose enum.

BUDGET BY CONSTRUCTION: a spec is only valid if its canonical serialization
stays under 1200 chars (the fleet truncation wall, free_lane_fleet.py:296)
and under an estimated 300 tokens (the ollama output cap, :267). The caps
below (title 32, action 32, caption 80, max 3 cast members per panel,
3..4 panels) make the WORST-CASE valid spec fit both budgets with margin;
assert_budget() proves it exhaustively over every pose at import time and
its proof dict is banked as BUDGET_PROOF.

The token estimator is deliberately conservative for compact JSON:
alphanumeric runs cost ceil(len/5) tokens (sub-word splits on identifiers
like gemma-janitor), punctuation costs ceil(count/2) (BPE merges pairs).
Worst case computes to ~261 estimated tokens against the 300 cap.

No em-dashes in this file (citation-lint law). Deterministic, $0, stateless.
"""
from __future__ import annotations

import json
import math
import re

SCHEMA_NAME = "comic_spec.v2"

# THE FIXED CAST (the estate's own; no outside characters ride the enum).
CAST = (
    "operator",
    "mag",
    "hermes",
    "lilith-figure",
    "gemma-janitor",
    "generic-agent",
)

# THE POSE VOCABULARY: joint angles in degrees, drawSkeleton grammar.
# Rows 1-7 ported verbatim from mag_dance.html POSES; sit/think/slump are
# this lane's additions in the same 10-field grammar (desk-work register).
POSES: dict[str, tuple[int, ...]] = {
    "flail": (6, -14, -150, -70, -30, -100, 8, 6, -6, 10),
    "kick": (10, 10, -40, -30, -160, -20, -15, 50, -10, 8),
    "shimmy": (-4, 0, -120, -110, -60, -90, 4, 12, -4, 14),
    "strut": (12, -8, -70, -80, -100, -60, 18, 4, -14, 6),
    "pointy": (0, 0, -20, -160, -30, -150, 2, 4, -2, 6),
    "spirit": (-8, 6, -160, -30, -160, -30, 10, 10, -10, 10),
    "stomp": (8, 0, -30, -20, -30, -20, 20, 30, -20, 30),
    "sit": (-6, 4, -40, -60, -40, -55, 80, -85, 78, -80),
    "think": (-4, -8, -30, -40, -100, -95, 6, 6, -6, 8),
    "slump": (18, 18, -15, -10, -15, -10, 10, 8, -10, 8),
}

# PANEL + FIELD CAPS. These are the budget guarantee, not taste.
PANEL_MIN, PANEL_MAX = 3, 4
WHO_MAX = 3              # xkcd register: 1-3 figures per panel
TITLE_MAX = 32
ACTION_MAX = 32
CAPTION_MAX = 80
CHAR_BUDGET = 1200       # fleet truncation wall
TOKEN_BUDGET = 300       # ollama output cap

_WORD_RE = re.compile(r"[A-Za-z0-9_-]+")


class SpecError(ValueError):
    """Loud refusal: every violation is named, none are silently forgiven."""


def estimate_tokens(text: str) -> int:
    """Conservative token estimate for compact JSON (see module docstring)."""
    runs = _WORD_RE.findall(text)
    word_tokens = sum(max(1, math.ceil(len(w) / 5)) for w in runs)
    alpha = sum(len(w) for w in runs)
    punct_tokens = math.ceil((len(text) - alpha) / 2)
    return word_tokens + punct_tokens


def serialize(spec: dict) -> str:
    """Canonical compact serialization (the bytes the budget is measured on)."""
    return json.dumps(spec, separators=(",", ":"), ensure_ascii=False)


def errors(spec: object) -> list[str]:
    """Every violation, enumerated. Empty list == valid spec."""
    bad: list[str] = []
    if not isinstance(spec, dict):
        return [f"spec is {type(spec).__name__}, not an object"]
    title = spec.get("title")
    if not isinstance(title, str) or not title.strip():
        bad.append("title: missing or not a non-empty string")
    elif len(title) > TITLE_MAX:
        bad.append(f"title: {len(title)} chars > cap {TITLE_MAX}")
    panels = spec.get("panels")
    if not isinstance(panels, list):
        bad.append("panels: missing or not a list")
        return bad
    if not (PANEL_MIN <= len(panels) <= PANEL_MAX):
        bad.append(f"panels: {len(panels)} outside {PANEL_MIN}..{PANEL_MAX}")
    for i, p in enumerate(panels):
        if not isinstance(p, dict):
            bad.append(f"panel {i}: not an object")
            continue
        who = p.get("who")
        if not isinstance(who, list) or not who:
            bad.append(f"panel {i}: who must be a non-empty list")
        else:
            if len(who) > WHO_MAX:
                bad.append(f"panel {i}: {len(who)} cast members > cap {WHO_MAX}")
            if len(set(map(str, who))) != len(who):
                bad.append(f"panel {i}: duplicate cast member in who")
            for name in who:
                if name not in CAST:
                    bad.append(f"panel {i}: unknown character {name!r} "
                               f"(cast: {', '.join(CAST)})")
        pose = p.get("pose")
        if pose not in POSES:
            bad.append(f"panel {i}: unknown pose {pose!r} "
                       f"(poses: {', '.join(POSES)})")
        action = p.get("action")
        if not isinstance(action, str) or not action.strip():
            bad.append(f"panel {i}: action missing or empty")
        elif len(action) > ACTION_MAX:
            bad.append(f"panel {i}: action {len(action)} chars > cap {ACTION_MAX}")
        caption = p.get("caption")
        if not isinstance(caption, str) or not caption.strip():
            bad.append(f"panel {i}: caption missing or empty")
        elif len(caption) > CAPTION_MAX:
            bad.append(f"panel {i}: caption {len(caption)} chars > cap {CAPTION_MAX}")
    return bad


def check(spec: object) -> dict:
    """Validate loudly: raise SpecError naming every violation, or return spec."""
    bad = errors(spec)
    if bad:
        raise SpecError(f"invalid {SCHEMA_NAME} spec ({len(bad)} violations): "
                        + "; ".join(bad))
    return spec  # type: ignore[return-value]


def loads(text: str) -> dict:
    """Parse model output then validate. Parse failure is also loud."""
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise SpecError(f"unparseable JSON: {e}") from e
    return check(obj)


def json_schema() -> dict:
    """The format-schema dict for the ollama / OpenAI response-format door.
    Enum membership and counts are enforced here; the char caps are enforced
    by errors() (JSON Schema maxLength is not honored by the ollama door)."""
    return {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "panels": {
                "type": "array", "minItems": PANEL_MIN, "maxItems": PANEL_MAX,
                "items": {
                    "type": "object",
                    "properties": {
                        "who": {"type": "array", "minItems": 1, "maxItems": WHO_MAX,
                                "items": {"type": "string", "enum": list(CAST)}},
                        "pose": {"type": "string", "enum": sorted(POSES)},
                        "action": {"type": "string"},
                        "caption": {"type": "string"},
                    },
                    "required": ["who", "pose", "action", "caption"],
                },
            },
        },
        "required": ["title", "panels"],
    }


def max_spec(pose: str) -> dict:
    """The worst-case valid spec for a given pose: 4 panels, the 3 longest
    cast names, every string field at its cap. Any valid spec serializes
    to fewer chars/tokens than this one."""
    who = ["gemma-janitor", "generic-agent", "lilith-figure"]
    panel = {"who": list(who), "pose": pose,
             "action": "a" * ACTION_MAX, "caption": "c" * CAPTION_MAX}
    return {"title": "t" * TITLE_MAX,
            "panels": [dict(panel) for _ in range(PANEL_MAX)]}


def assert_budget() -> dict:
    """Exhaustive budget proof: every pose, worst-case everything else.
    Called at import so the schema cannot drift over budget silently."""
    rows = {}
    for pose in sorted(POSES):
        text = serialize(max_spec(pose))
        rows[pose] = {"chars": len(text), "tokens": estimate_tokens(text)}
        assert len(text) < CHAR_BUDGET, (
            f"pose {pose}: worst case {len(text)} chars >= {CHAR_BUDGET}")
        assert rows[pose]["tokens"] < TOKEN_BUDGET, (
            f"pose {pose}: worst case {rows[pose]['tokens']} tokens "
            f">= {TOKEN_BUDGET}")
    for name in POSES:
        assert len(name) <= 6, f"pose name {name!r} longer than 6 chars"
    return {"schema": SCHEMA_NAME, "char_budget": CHAR_BUDGET,
            "token_budget": TOKEN_BUDGET, "worst_case": rows}


# The by-construction proof, run on every import (cheap: 10 serializations).
BUDGET_PROOF = assert_budget()
