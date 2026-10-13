"""marker_penalty - sampler-level reasoning-marker penalty profile.

Port wave 2026-10-07, lane P6 port 2, the decode-side CHEAP LEG of the staged
reasoning-marker port: training-free token-specific penalties at the sampler,
riding the banked 10-03 mechanism at
watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md:31
(RATIO, arXiv 2609.39801: on a reasoning model, W3 PTQ inflates CoT length
2.94x (GPTQ) to 3.77x (AWQ) while accuracy falls 60.13 to 33.82, and
training-free token-specific penalties recover up to 9.8 accuracy points
while cutting CoT length up to 51.3 percent; "the mitigation lives in the
sampler, not the weights"). The durable weight-side leg is the day-7 card's
find 1 (watch/inbox/frontier_olm_2026-10-07/steal/finetuning-adaptation.md,
RL-shaped marker-usage penalty objective); this module is its no-training
twin, consumable by mag/llama_cpp_bridge.py as an optional --penalty-profile
flag, OFF by default.

Disease targeted: the EMPTY_REASONING disease (mag/inference_budget.py:13,
EMPTY_REASONING TERMINAL at :19) - the model spends the whole output budget
on hidden reasoning and the content channel returns empty. The marker
candidates in the shipped profile were mined 2026-10-07 from that organ's
receipt surfaces (census banked beside the markers in the profile JSON).

Module exists as its own file (not inline in llama_cpp_bridge.py) per the
file-too-long ratchet cap: the inline version pushed the bridge past 400
lines (violation_ratchet NEW hit 015abeaa0503ee62, cured same sitting by
this extraction, not by baseline acceptance).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

# Shipped profile (mined candidate set with receipt census; see its "mining"
# and "mechanism" fields). A default path string, not a Path() literal: the
# module-level cwd-relative-path ratchet rule bans relative Path() constants,
# and the path is only resolved when a caller arms the profile.
DEFAULT_PENALTY_PROFILE = "configs/marker_penalty_profile.json"


def load_penalty_profile(path: str | Path) -> dict:
    """Load and validate a marker penalty profile JSON.

    Shape: an object carrying a non-empty "markers" mapping of marker token to
    an entry with a numeric "bias". Missing path raises FileNotFoundError; a
    malformed body raises ValueError, so a bad profile fails loud instead of
    silently firing unpenalized."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    markers = raw.get("markers") if isinstance(raw, dict) else None
    if not isinstance(markers, dict) or not markers:
        raise ValueError(
            f"penalty profile {path}: no non-empty 'markers' object"
        )
    for token, entry in markers.items():
        if not isinstance(token, str) or not token:
            raise ValueError(
                f"penalty profile {path}: bad marker token {token!r}"
            )
        bias = entry.get("bias") if isinstance(entry, dict) else None
        if not isinstance(bias, (int, float)) or isinstance(bias, bool):
            raise ValueError(
                f"penalty profile {path}: marker {token!r} has no numeric bias"
            )
    return raw


def penalty_logit_bias(profile: dict) -> Dict[str, float]:
    """Build the logit_bias map sent with the /v1/completions body.

    Entries carrying an integer token_id use the OpenAI-compatible id-keyed
    form; entries without one pass the token string through for the server to
    resolve. Wire acceptance of string-token keys on the estate's
    llama-cpp-python 0.3.36 server is UNMEASURED (byte-proven constraint
    family, spawn-compat fix 2026-10-06), which is one reason the profile
    stays OFF by default: the flag arms an experiment, it does not certify
    the wire shape."""
    out: Dict[str, float] = {}
    for token, entry in profile.get("markers", {}).items():
        bias = float(entry.get("bias", 0.0))
        token_id = entry.get("token_id")
        if isinstance(token_id, int) and not isinstance(token_id, bool):
            out[str(token_id)] = bias
        else:
            out[token] = bias
    return out
