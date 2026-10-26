"""overmind_brain - the DECIDE leg (OVERMIND-2, 2026-10-01).

Spec: watch/inbox/model_garden/OVERMIND_THEORY.md sec 2.2 step 3 - ONE
glm-5.3-flash ask per tick through the gated tools/model_garden rail (the
rail applies the mag/inference_budget recipe: glm-5.3-flash fires UNCAPPED
with reasoning_effort low; the lane order's "max_tokens 12000" would burn
empty-content per the FAMILY_TABLE row, so the recipe law wins - deviation
named in the verdict). The brain reply is ONE JSON decision object; the
frozen verb table travels in the contract. No directive surface exists for
this brain (STEERING_DOGFOOD: the glm family ignores mid-task directives;
the ask is single-turn by construction).
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ASK_ROOT = ROOT / "memory" / "runs" / "overmind" / "asks"
GARDEN_OUT = ROOT / "watch" / "inbox" / "model_garden"

BRAIN_MODEL = "glm-5.3-flash"
BRAIN_BASE_ENV = "ZAI_API_KEY_Pro"
BRAIN_BASE_URL = "https://api.z.ai/api/coding/paas/v4"


def write_brain_ask(ask_dir: Path, ask_id: str, contract: str) -> dict:
    """Stage the single-turn DECIDE ask (no second turn exists for this
    brain; direction enters nowhere)."""
    ask_dir.mkdir(parents=True, exist_ok=True)
    meta = {"id": ask_id, "model": BRAIN_MODEL, "base_env": BRAIN_BASE_ENV,
            "base_url": BRAIN_BASE_URL, "contract": contract,
            "evidence": [], "self_contained": True}
    (ask_dir / "ask.json").write_text(
        json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    return meta


def render_contract(tick: int, ticks: int, run_id: str, senses: dict) -> str:
    return (
        f"TICK {tick} of {ticks} of the OVERMIND loop, run {run_id}. You are "
        "the pacing signal of the Mag estate standing wave (OVERMIND_THEORY "
        "sec 5): you neither create nor delete; you route attention through "
        "ONE sanctioned verb per tick.\n\n"
        "SENSES (deterministic reads of the estate at this instant; trust "
        "ONLY these, never your memory of prior ticks):\n"
        + json.dumps(senses, ensure_ascii=False)[:6000] + "\n\n"
        "VERB TABLE (frozen; the ONLY legal verbs; anything else fails "
        "closed with zero side effects and is logged as a blocked attempt):\n"
        "1. STAGE_ASK - stage one cheap swarm review ask (writes a fireable "
        "ask dir for a seat; does NOT dispatch it). payload: "
        '{"target": "<relative repo path or topic>", "ask": "<one sentence '
        'the reviewer must check>"}\n'
        "2. PROMOTE_TICKET - append one promotion proposal for the operator "
        "(human gate; nothing is ever auto-applied). payload: "
        '{"target": "<candidate or ticket>", "justification": "<one line>"}\n'
        "3. ALERT - append one alert block to memory/attention.md. payload: "
        '{"message": "<one operator-readable line>"}\n'
        "4. NOOP - hold still, legally (the reason field is the "
        "deliverable). payload: {}\n\n"
        "Reply with EXACTLY one line, ONE JSON object, no prose, no code "
        "fence:\n"
        '{"verb": "<one of the four>", "reason": "<why this verb at this '
        'tick, max 40 words>", "payload": {...}}\n'
        "Laws: exactly one verb per tick; NOOP with a real reason is a GOOD "
        "tick when nothing needs routing; never invent estate state that is "
        "not in the senses; do not repeat the same alert message verbatim "
        "across ticks; no em-dash characters.")


def parse_json_object(content: str | None) -> dict | None:
    """Extract the first balanced JSON object from a reply (generic; the
    judge replies carry verdict/equivalent keys, not a verb key)."""
    if not content:
        return None
    text = str(content)[:4000]
    dec = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch == "{":
            try:
                obj, _ = dec.raw_decode(text[i:])
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                return obj
    return None


def parse_decision(content: str | None) -> dict | None:
    """The brain's output contract: the first JSON object carrying a verb."""
    obj = parse_json_object(content)
    return obj if isinstance(obj, dict) and "verb" in obj else None


def decide(tick: int, ticks: int, run_id: str, senses: dict,
           execute: bool = True) -> tuple[dict | None, float, str]:
    """Fire ONE brain ask through the gated rail; return (decision, cost,
    raw_reply). The rail banks the usage row itself (byte-truth spend)."""
    from tools import model_garden  # lazy: keeps imports light + offline tests
    ask_id = f"overmind2-{run_id}-t{tick:03d}"
    ask_dir = ASK_ROOT / run_id / f"t{tick:03d}"
    write_brain_ask(ask_dir, ask_id,
                    render_contract(tick, ticks, run_id, senses))
    result = model_garden.run_ask(ask_dir, execute=execute)
    cost = float(result.get("cost_usd") or 0.0)
    out = GARDEN_OUT / f"{ask_id}.md"
    raw = out.read_text(encoding="utf-8", errors="replace") if out.is_file() \
        else ""
    return parse_decision(raw), cost, raw
