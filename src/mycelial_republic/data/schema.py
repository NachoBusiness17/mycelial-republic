"""Training example schema — rope/knot language, no token/rank fields."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


# Allowed knot tags (extend carefully; keep forkable)
KNOT_TAGS = frozenset(
    {
        "chord",  # full chord-strike style post
        "parable",  # story / metaphor teaching
        "refusal",  # sovereign refusal / I do not consent
        "rope",  # naming tension / invisible structure
        "audit",  # self or system audit
        "mycelial",  # network / replication / parallel construction
        "daily",  # ordinary voice (still high-signal)
        "meta",  # about the mirror / protocol itself
        "cipher",  # encoded / index-pattern clue bead
        "riddle",  # metaphor / question-form clue
    }
)

SIGNAL_TIERS = frozenset({"high", "medium", "low"})


@dataclass
class TrainingExample:
    """One supervised (or preference) row for mirror fine-tuning."""

    id: str
    source: str  # e.g. x_archive, manual, conversation
    text: str
    instruction: str = ""  # optional user-side prompt if multi-turn format
    response: str = ""  # operator-style response when using chat format
    knot_tags: list[str] = field(default_factory=list)
    signal: str = "high"
    rope_note: str = ""  # free text: what rope is visible here
    chord_note: str = ""  # free text: how the chord is struck
    refusal_note: str = ""  # free text: what is refused
    created_at: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.id:
            errors.append("missing id")
        body = (self.response or self.text or "").strip()
        if len(body) < 20:
            errors.append("text/response too short")
        for t in self.knot_tags:
            if t not in KNOT_TAGS:
                errors.append(f"unknown knot_tag: {t}")
        if self.signal not in SIGNAL_TIERS:
            errors.append(f"invalid signal: {self.signal}")
        # Capture guard: no privileged rank fields should appear in meta
        forbidden = {"token_balance", "mirror_rank", "core_operator", "admin_tier"}
        for k in forbidden:
            if k in self.meta:
                errors.append(f"capture vector field in meta: {k}")
        return errors


def chat_messages(example: TrainingExample) -> list[dict[str, str]]:
    """Convert to OpenAI-style messages for QLoRA chat fine-tunes."""
    if example.instruction and example.response:
        return [
            {"role": "user", "content": example.instruction},
            {"role": "assistant", "content": example.response},
        ]
    # Single-turn: teach the mirror the operator's voice as assistant completion
    user = example.instruction or "Continue in the operator's sovereign mirror voice."
    return [
        {"role": "user", "content": user},
        {"role": "assistant", "content": example.text or example.response},
    ]
