"""inference_budget - the RIB_MODEL_GATES harness-table leg (2026-10-01).

OPERATOR LAW (RIB_MODEL_GATES_20261001.md): "we should have model gates" +
"stop pretending the harness for each animal should be the same". Until this
module the gates were DOCTRINE-ONLY: the rib carried per-animal profiles and
tools/animal_profiles.py observed/distilled them, but no code organ enforced
a recipe on the fire path - every carrier hand-rolled its params (or, for
the reasoning budget, rolled none). This module IS that missing setting
mechanism: the single source both carriers (tools/hermes_burn.py,
tools/model_garden.py) import for (a) per-animal call recipes, (b) the
empty-content classifier, (c) the ONE sanctioned terminal reaction.

THE ONE BUG (months of jackets, one law): the model spends the whole output
budget on hidden reasoning and the content channel returns empty (fable
B1/B5 burned both 18KB review asks whole: finish=length, 12000/12000
reasoning tokens, empty content, $2.03; opus 14960 billed/empty at 16k caps;
glm-5.3-flash empty at every cap; deepseek thinking-on DNFs; D3+A1+B1 cap
truncations). Each jacket cured one surface; nothing owned the reaction.
Here: EMPTY_REASONING is TERMINAL for that (ask, family) - marker minted,
same params NEVER refired, two sanctioned recoveries only.

Distillability law (the skill-bead cure): FAMILY_TABLE rows carry their
source receipt and sync_to_behavioral() files each row as an animal_profiles
rail observation, so `python tools/animal_profiles.py --distill` regenerates
the rib evidence from the same bytes this module enforces. A recipe changed
without its observation + receipt is void.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# verdict words for classify_empty
EMPTY_REASONING = "EMPTY_REASONING"
EMPTY_OTHER = "EMPTY_OTHER"
NOT_EMPTY = "NOT_EMPTY"

MARKER_NAME = "EMPTY_REASONING"
# review shape = 18KB+ of rendered ask body (the fable B1/B5 burn shape)
REVIEW_SHAPE_CHARS = 18_000
# default floors: a crumb budget is the burn trap; small asks live at 8000+
DEFAULT_FLOOR_SMALL = 8_000
# 18KB+ review asks need >= 24000 OR streaming OR thinking-off (fable law)
DEFAULT_FLOOR_REVIEW = 24_000
# completion tokens at/above this with finish=length = burn evidence even
# when the provider does not report reasoning_tokens separately
BURN_COMPLETION_FLOOR = 1_000
# z.ai 5.3-family minimum thinking-on budget (docs/ref/ZAI_API_EXPERT_REFERENCE
# section 5.1: below 1536 the reply goes content-empty)
ZAI_REASONING_FLOOR = 1_536


@dataclass
class FamilyRecipe:
    """One animal's harness recipe (the RIB_MODEL_GATES row, executable)."""
    key: str                                  # canonical animal name
    matches: tuple[str, ...]                  # lowercase model-id substrings
    thinking_control: dict = field(default_factory=dict)  # extra_body params
    forbidden_keys: tuple[str, ...] = ()      # ask params stripped, never sent
    small_floor: int = DEFAULT_FLOOR_SMALL
    review_floor: int = DEFAULT_FLOOR_REVIEW
    uncap: bool = False                       # True = send no max_tokens at all
    notes: tuple[str, ...] = ()
    source: str = ""                          # receipt path (a row without one is void)


# THE harness table. Most-specific first: model-id substrings are matched
# before family fallbacks. Every row cites the receipt that paid for it.
FAMILY_TABLE: list[FamilyRecipe] = [
    # Row 1: harvested from tools/ds_workhorse.py:50-60 (the existing seed,
    # ported not re-derived). CORRECTED 2026-10-04 (parked-decision D3,
    # watch/inbox/ractor_engine/2026-10-04-parked-decisions/SYNTHESIS.md:11-17;
    # d4_thinking_probe.md:53-62): omission is a MEASURED ON state (omitted
    # key = 18 reasoning tokens on a one-word ask; disabled = 0). The off
    # switch is the explicit thinking:{type:disabled} key, so it is injected
    # here and no longer stripped. tools/ds_workhorse.py:93 already sends it.
    FamilyRecipe(
        key="deepseek",
        matches=("deepseek",),
        thinking_control={"thinking": {"type": "disabled"}},
        forbidden_keys=("reasoning", "reasoning_effort",
                        "chat_template_kwargs"),
        small_floor=2_000,       # ds_workhorse batch shape
        review_floor=8_000,      # W8 caps; long-form degrades anyway
        notes=(
            "THINKING OFF MANDATORY: send thinking {type: disabled}"
            " explicitly; omission is NOT the off state (d4 3-arm probe"
            " 2026-10-04 refuted the old AH10 omission note)",
            "thinking-on burned the ENTIRE completion budget on hidden"
            " reasoning, zero content at 4500/8000/16000 caps, socket hangs,"
            " DNFs, word salad",
            "long-form degradation: route review-shaped asks elsewhere",
            "retry-once on empty with rails is the gopher cure; never more"
            " than 2 attempts per item",
        ),
        source="tools/ds_workhorse.py (AH10 law) + "
               "watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md",
    ),
    FamilyRecipe(
        key="claude-opus-5.5",
        matches=("opus-5.5", "opus_5_5"),
        review_floor=64_000,     # 32k burns 29.5k reasoning and length-caps
        notes=(
            "streaming SSE only: whole-response dies at 1800s/3600s",
            "16k caps return all-reasoning empty; 32k length-caps mid-reasoning",
            "content may land in the reasoning channel at finish=stop: the"
            " carrier's reasoning-channel fallback IS the sanctioned assembly",
        ),
        source="memory/rib/RIB_MODEL_GATES_20261001.md (OPUS 5.5 row)",
    ),
    FamilyRecipe(
        key="claude-fable-5.1",
        matches=("fable",),
        notes=(
            "18KB+ review asks burned the whole 12000 cap on hidden reasoning"
            " (B1/B5, 12000/12000 reasoning tokens, empty content, $2.03):"
            " re-stage at the 24000 floor or switch family",
            "reasoning-channel ramble at finish=length is not a deliverable",
            "small asks are format-perfect and cheap (B6 6/6 at $0.0076)",
        ),
        source="watch/inbox/model_garden/FABLE1.md",
    ),
    FamilyRecipe(
        key="glm-5.3-flash",
        matches=("glm-5.3-flash",),
        thinking_control={"thinking": {"type": "enabled"},
                          "reasoning_effort": "low"},
        small_floor=ZAI_REASONING_FLOOR,
        review_floor=ZAI_REASONING_FLOOR,
        uncap=True,
        notes=(
            "thinking cannot be disabled (1210): bound it with reasoning_effort low",
            "ANY max_tokens cap (2600/4200/9000/16000 all tried) returns"
            " empty_content finish=length: fire uncapped",
            "when a cap is unavoidable the floor is 1536",
        ),
        source="memory/continuity/seat_memory_20260927/ox-alpha-was-glm53-flash.md"
               " + docs/ref/ZAI_API_EXPERT_REFERENCE.md",
    ),
    FamilyRecipe(
        key="nous-primes",
        matches=("glm-5.3-prime", "qwen3.8-max-prime", "ember-1"),
        thinking_control={"reasoning": {"max_tokens": 6_000}},
        notes=(
            "LESSIG RAILS: reasoning {max_tokens} 6000 cap or the answer"
            " never gets written (gopher disease: 11/12 zero-content, $1.43"
            " for one answer)",
            "retry-on-empty is legal ONLY with rails applied (changed"
            " params); same-params refire after EMPTY_REASONING is terminal",
        ),
        source="watch/inbox/last_mile_20260930/GOPHER_BURN_RECEIPT.md + "
               "tools/duel_harness.py REASONING_CAP",
    ),
    FamilyRecipe(
        key="kimi",
        matches=("kimi",),
        notes=(
            "COLD-CALL NOTE: first call slow (234s) and bills big reasoning"
            " (17,617 tokens) while content still arrives (354 visible):"
            " big reasoning WITHOUT empty content is NOT the disease, do not"
            " terminal on latency or reasoning size alone",
            "kimi-k3 must preserve reasoning_content across turns"
            " (thinking-history sensitivity)",
        ),
        source="watch/inbox/model_garden/KIMI1_RUN.md",
    ),
    FamilyRecipe(
        key="grok-4.7",
        matches=("grok-4.7", "grok_4_7"),
        notes=(
            "streaming SSE only: whole-response hangs 900s+",
            "reasoning tokens bill as output ($0.23/answer): reserve for judgment",
        ),
        source="memory/rib/RIB_MODEL_GATES_20261001.md (GROK-4.7 row)",
    ),
    FamilyRecipe(
        key="grok-4.3",
        matches=("grok-4.3", "grok_4_3"),
        thinking_control={"reasoning": {"max_tokens": 6_000}},
        notes=(
            "tolerates the reasoning 6000 rail (W8 caps 6000/16000)",
            "SENSING ONLY: a DIFFERENT animal from grok-4.7, never confuse them",
        ),
        source="watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md",
    ),
    FamilyRecipe(
        key="qwen-flash",
        matches=("qwen3.7-flash", "qwen-flash"),
        forbidden_keys=("reasoning", "reasoning_effort", "thinking",
                        "chat_template_kwargs"),
        notes=(
            "rejects the reasoning param outright (HTTP 400): strip all"
            " reasoning params and fire without",
            "qwen-class thinking-off knob where a host accepts one is"
            " chat_template_kwargs enable_thinking false (operator brief"
            " 2026-10-01; unmeasured on this estate - qwen3.7-flash 400s on"
            " any reasoning param)",
            "SENSING ONLY: fabricates under load (judges flagged invented content)",
        ),
        source="watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md + "
               "memory/rib/RIB_MODEL_GATES_20261001.md (QWEN row)",
    ),
    FamilyRecipe(
        key="gemini-flash",
        matches=("gemini",),
        forbidden_keys=("reasoning", "reasoning_effort"),
        notes=(
            "rejects reasoning {'enabled': false} with HTTP 400: send the"
            " plain {'max_tokens': N} shape only",
        ),
        source="memory/rib/RIB_MODEL_GARDEN_ROUTING.md (gemini judge-duty rail)",
    ),
]

DEFAULT_RECIPE = FamilyRecipe(
    key="default",
    matches=(),
    notes=(
        "no animal match: estate default floors only (review shape needs a"
        " 24000 floor OR streaming OR thinking-off; small asks 8000-12000)",
    ),
    source="watch/inbox/model_garden/PRIORS.md section B (per-SKU disease table)",
)

# family-name fallbacks ONLY where the whole host serves one animal class;
# the nous host serves many animals and must never fall back by family.
FAMILY_FALLBACK = {
    "deepseek": "deepseek",
    "moonshot": "kimi",
    "google": "gemini-flash",
    "zai": "glm-5.3-flash",
}


def recipe_for(model: str = "", family: str = "") -> FamilyRecipe:
    """Resolve the recipe: model-id substring first, family fallback second,
    the default row last (never None - every fire rides a recipe)."""
    m = (model or "").lower()
    if m:
        for recipe in FAMILY_TABLE:
            if any(pat in m for pat in recipe.matches):
                return recipe
    fam = (family or "").lower()
    if fam in FAMILY_FALLBACK:
        for recipe in FAMILY_TABLE:
            if recipe.key == FAMILY_FALLBACK[fam]:
                return recipe
    return DEFAULT_RECIPE


def classify_shape(prompt_chars: int) -> str:
    """review = 18KB+ rendered ask body (the fable burn shape), else small."""
    return "review" if prompt_chars >= REVIEW_SHAPE_CHARS else "small"


@dataclass
class CallPlan:
    """What a carrier fires with: the recipe applied to one ask."""
    max_tokens: int | None        # None = fire uncapped (glm-5.3-flash law)
    extra_body: dict              # thinking control merged, forbiddens stripped
    recipe_key: str
    shape: str
    notes: tuple[str, ...]


def plan_call(model: str = "", family: str = "", prompt_chars: int = 0,
              requested_max_tokens: int | None = None,
              ask_extra: dict | None = None) -> CallPlan:
    """Plan one fire: floor per shape, thinking control injected, forbidden
    ask params stripped (recipe wins on its governed keys)."""
    recipe = recipe_for(model, family)
    shape = classify_shape(prompt_chars)
    floor = recipe.review_floor if shape == "review" else recipe.small_floor
    if recipe.uncap:
        max_tokens: int | None = None
    elif requested_max_tokens is None:
        max_tokens = floor
    else:
        max_tokens = max(int(requested_max_tokens), floor)
    extra = dict(ask_extra or {})
    for key in recipe.forbidden_keys:
        extra.pop(key, None)
    extra.update(recipe.thinking_control)
    return CallPlan(max_tokens=max_tokens, extra_body=extra,
                    recipe_key=recipe.key, shape=shape, notes=recipe.notes)


def _reasoning_tokens(usage: dict) -> int:
    return int(((usage or {}).get("completion_tokens_details") or {})
               .get("reasoning_tokens") or 0)


def classify_empty(finish_reason: str | None, usage: dict | None,
                   content) -> str:
    """Classify a response's content channel.

    `content` is the CONTENT CHANNEL ONLY, never the post-fallback salvage:
    reasoning-channel bytes at finish=length are the burned ramble, and
    reading them as a deliverable is the jacket this module kills. The
    carrier classifies first, salvages only on EMPTY_OTHER/NOT_EMPTY.
    """
    if content is not None and str(content).strip():
        return NOT_EMPTY
    usage = usage or {}
    ct = int(usage.get("completion_tokens") or 0)
    burn = _reasoning_tokens(usage) > 0 or ct >= BURN_COMPLETION_FLOOR
    if finish_reason == "length" and burn:
        return EMPTY_REASONING
    return EMPTY_OTHER


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def react(ask_id: str, family: str, cause: str, ask_dir: Path) -> Path:
    """The ONE sanctioned reaction: mint the terminal marker (REFUSED
    mechanics). EMPTY_REASONING is TERMINAL for (ask_id, family): same
    params are NEVER refired; the marker names the two recoveries."""
    marker = Path(ask_dir) / MARKER_NAME
    marker.write_text(
        f"{cause[:500]}\n\n"
        f"[EMPTY_REASONING terminal marker, minted {_now()} for ask id "
        f"{ask_id} (family {family}). The content channel came back empty "
        "with finish=length and reasoning/token evidence of burn: the model "
        "spent the whole output budget on hidden reasoning. The carrier "
        "skips this ask on sight and NEVER refires the same params. Two "
        "sanctioned recoveries ONLY: (1) re-stage the ask with this "
        "family's recipe in mag/inference_budget.py FAMILY_TABLE (the "
        "max_tokens floor and thinking control), or (2) switch family. "
        "Re-arm requires an operator edit of the ask bytes AND deleting "
        "this marker.]\n",
        encoding="utf-8")
    return marker


def skip_terminal(ask_dir: Path, ask_id: str) -> dict | None:
    """Entry-side skip-on-sight for a terminally burned ask (REFUSED shape)."""
    if not (Path(ask_dir) / MARKER_NAME).is_file():
        return None
    return {"id": ask_id, "ok": True,
            "skipped": "EMPTY_REASONING (terminal; same params never refire."
                       " Recover: re-stage with the FAMILY_TABLE recipe or"
                       " switch family, then delete the marker)"}


def guard_terminal(ask_dir, ask_id: str, recipe_key: str, finish_reason,
                   usage, raw_content, bank, *, model: str = "",
                   family: str = "", base_url: str = "", pin: int = 0,
                   pout: int = 0, cost: float = 0.0) -> str | None:
    """Carrier choke point: classify the content channel; on EMPTY_REASONING
    bank the burn row (ok False, empty_reasoning flag) and mint the marker.
    Returns the cause string when terminal, else None (fire continues into
    the carrier's existing refusal/salvage logic)."""
    usage = usage or {}
    if classify_empty(finish_reason, usage, raw_content) != EMPTY_REASONING:
        return None
    rt = _reasoning_tokens(usage)
    ct = int(usage.get("completion_tokens") or 0)
    cause = (f"family {recipe_key}: content empty, finish={finish_reason}, "
             f"completion_tokens={ct}, reasoning_tokens={rt} - hidden "
             "reasoning consumed the output budget")
    bank({"ts": _now(), "id": ask_id, "model": model, "turn": None,
          "model_family": family or None, "base_url": base_url or None,
          "prompt_tokens": pin, "completion_tokens": ct,
          "reasoning_tokens": rt, "finish_reason": finish_reason,
          "empty_reasoning": True, "cost_usd": round(cost, 4), "ok": False})
    react(ask_id, recipe_key, cause, Path(ask_dir))
    return cause


def sync_to_behavioral() -> list[Path]:
    """File every FAMILY_TABLE row as an animal_profiles rail observation
    (dedup on detail) so --distill regenerates the rib from these bytes.
    This is the distillability law: the table is the compiled enforcement
    leg, the observations + receipts are the truth it compiles from."""
    from tools import animal_profiles as ap
    written: list[Path] = []
    for recipe in FAMILY_TABLE:
        detail = ("inference_budget {}: thinking_control={} forbidden={}"
                  " small_floor={} review_floor={} uncap={}".format(
                      recipe.key, json.dumps(recipe.thinking_control,
                                             sort_keys=True),
                      list(recipe.forbidden_keys), recipe.small_floor,
                      recipe.review_floor, recipe.uncap))
        slug = ap.slugify(recipe.key)
        existing: set = set()
        p = ap.BEHAV_DIR / f"{slug}.jsonl"
        if p.is_file():
            for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                try:
                    existing.add(json.loads(line).get("detail"))
                except (json.JSONDecodeError, AttributeError):
                    continue
        if detail in existing:
            continue
        written.append(ap.observe(recipe.key, "rail", detail, recipe.source))
    return written
