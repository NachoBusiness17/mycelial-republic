#!/usr/bin/env python3
"""hermes_client - the paid wire: reach a Nous-shape inference API with the
budget laws on from day one.

The kit's fourth Hermes wire (integrations/hermes/README.md section 4).
Ported, not re-derived, from the estate's executable harness table
(mag/inference_budget.py, the RIB_MODEL_GATES enforcement leg) and its
paid carrier (tools/hermes_burn.py). The four laws this module enforces:

1. plan_call before every fire: a max_tokens floor per ask shape (small
   vs review), per-animal thinking control merged into the body, and
   forbidden ask params stripped. The plan rides the wire unmodified -
   the carrier paid for that lesson: a plan dropped one hop between
   compute and wire burned 15998 reasoning tokens for empty content
   (tools/hermes_burn.py _build_body docstring, Fix 2026-10-04).
2. guard_terminal on every response: an empty content channel with
   finish=length and burn evidence is TERMINAL for (ask, family). The
   marker mints, the same params are NEVER refired, and the two
   sanctioned recoveries are re-stage-with-recipe or switch-family.
3. The thinking-control law: for some animals omission of the thinking
   key is a MEASURED ON state (deepseek: 18 reasoning tokens on a
   one-word ask with the key omitted). The off switch must be SENT.
4. Every fire banks a usage row with its cost (fire() refuses to run
   without a bank). A floor is a routing decision with money teeth:
   the estate's 24000 review floor priced one ask's reserved cost over
   the provider balance and 402ed it deterministically every hourly fire
   (watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md).

Transport is stdlib-only: http.client to the configured literal https
endpoint, fenced per call (exactly one allowlisted host, resolved DNS
must be public - private/loopback/link-local/reserved/multicast refused).
NO live spend without an operator key: fire() takes the key from the
caller, refuses to fire without one, and the test suite (test_hermes_client.py)
mocks the transport so the laws are proven offline.
"""
from __future__ import annotations

import http.client
import ipaddress
import json
import socket
import time
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# verdict words for classify_empty
EMPTY_REASONING = "EMPTY_REASONING"
EMPTY_OTHER = "EMPTY_OTHER"
NOT_EMPTY = "NOT_EMPTY"

MARKER_NAME = "EMPTY_REASONING"
# review shape = 18KB+ of rendered ask body (the fable burn shape)
REVIEW_SHAPE_CHARS = 18_000
# default floors: a crumb budget is the burn trap; small asks live at 8000+
DEFAULT_FLOOR_SMALL = 8_000
# 18KB+ review asks need >= 24000 OR streaming OR thinking-off (fable law)
DEFAULT_FLOOR_REVIEW = 24_000
# completion tokens at/above this with finish=length = burn evidence even
# when the provider does not report reasoning_tokens separately
BURN_COMPLETION_FLOOR = 1_000
# z.ai 5.3-family minimum thinking-on budget (below 1536 the reply goes
# content-empty)
ZAI_REASONING_FLOOR = 1_536

# The configured literal endpoint (the estate carrier's live host, probed
# 2026-10-01). The fence accepts exactly this host on 443 over https.
ENDPOINT_HOST = "inference-api.nousresearch.com"
DEFAULT_ENDPOINT = f"https://{ENDPOINT_HOST}/v1/chat/completions"

# usd per token: (input, output). Captured from the live /v1/models
# pricing fields, 2026-10-01 probe (tools/hermes_burn.py PRICING).
PRICING = {
    "anthropic/claude-opus-5.5": (0.000004, 0.00002),
    "anthropic/claude-sonnet-5.5": (0.000002, 0.00001),
    "anthropic/claude-fable-5.1": (0.00001, 0.00005),
    "anthropic/claude-haiku-4.5": (0.000001, 0.000005),
}


class TerminalEmpty(RuntimeError):
    """EMPTY_REASONING went terminal: the marker is minted, same params
    must NEVER refire (recover: re-stage with the recipe or switch
    family)."""

    def __init__(self, cause: str):
        super().__init__(cause)
        self.cause = cause


class Refused(RuntimeError):
    """The provider refused the ask. Refusals are data, not retries."""


class TransportFailure(RuntimeError):
    """The wire failed (HTTP >= 400, socket, timeout, undecodable body)."""


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


# THE harness table, ported verbatim from mag/inference_budget.py (sources
# are the estate receipts that paid for each row; a recipe changed without
# its receipt is void). Most-specific first: model-id substrings are
# matched before family fallbacks.
FAMILY_TABLE: list[FamilyRecipe] = [
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


def build_body(plan: CallPlan, model: str, messages: list[dict]) -> dict:
    """The request body, pure (offline-inspectable). The core keys win over
    the plan; the plan cannot rewrite model/messages. When the plan says
    uncap (glm-5.3-flash law: ANY cap returns empty content) the max_tokens
    key is OMITTED, not zeroed - the estate carrier's `plan.max_tokens or
    fallback` shape never reaches this branch because its pricing table is
    anthropic-only; the kit implements the uncap law directly."""
    body = dict(plan.extra_body)
    body.update({"model": model, "messages": messages})
    if plan.max_tokens is not None:
        body["max_tokens"] = plan.max_tokens
    return body


def _reasoning_tokens(usage: dict) -> int:
    return int(((usage or {}).get("completion_tokens_details") or {})
               .get("reasoning_tokens") or 0)


def classify_empty(finish_reason: str | None, usage: dict | None,
                   content) -> str:
    """Classify a response's content channel.

    `content` is the CONTENT CHANNEL ONLY, never the post-fallback salvage:
    reasoning-channel bytes at finish=length are the burned ramble, and
    reading them as a deliverable is the jacket this port kills. The caller
    classifies first, salvages only on EMPTY_OTHER/NOT_EMPTY.
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
    """The ONE sanctioned reaction: mint the terminal marker. EMPTY_REASONING
    is TERMINAL for (ask_id, family): same params are NEVER refired; the
    marker names the two recoveries."""
    marker = Path(ask_dir) / MARKER_NAME
    marker.write_text(
        f"{cause[:500]}\n\n"
        f"[EMPTY_REASONING terminal marker, minted {_now()} for ask id "
        f"{ask_id} (family {family}). The content channel came back empty "
        "with finish=length and reasoning/token evidence of burn: the model "
        "spent the whole output budget on hidden reasoning. The carrier "
        "skips this ask on sight and NEVER refires the same params. Two "
        "sanctioned recoveries ONLY: (1) re-stage the ask with this "
        "family's recipe in hermes_client.py FAMILY_TABLE (the max_tokens "
        "floor and thinking control), or (2) switch family. Re-arm "
        "requires an operator edit of the ask bytes AND deleting this "
        "marker.]\n",
        encoding="utf-8")
    return marker


def skip_terminal(ask_dir: Path, ask_id: str) -> dict | None:
    """Entry-side skip-on-sight for a terminally burned ask. Call before
    every fire; a marker present means the ask skips on sight forever."""
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
    the caller's refusal/salvage logic)."""
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


# --- endpoint fence (tools/hermes_burn.py shape) ---------------------------

def _assert_public_host(host: str) -> None:
    """DNS fence: the endpoint host must resolve to public unicast addresses
    only, so DNS or hosts-file re-pointing cannot aim the client at
    internal surfaces."""
    for info in socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise RuntimeError(
                f"endpoint fence: {host} resolves to non-public {ip}")


def fence_endpoint(endpoint: str) -> tuple[str, int, str]:
    """The configured literal endpoint, asserted per call: a fixed https URL
    on exactly one allowlisted host, port 443, DNS-fenced public. Returns
    (host, port, path) for http.client."""
    parts = urllib.parse.urlsplit(endpoint)
    if parts.scheme != "https" or parts.hostname != ENDPOINT_HOST:
        raise RuntimeError("endpoint fence: refusing non-allowlisted URL")
    if parts.port not in (None, 443) or parts.username or parts.password:
        raise RuntimeError("endpoint fence: refusing altered port/credentials")
    _assert_public_host(parts.hostname)
    return parts.hostname, 443, parts.path or "/v1/chat/completions"


# --- transport (stdlib http.client) ----------------------------------------

def https_post_json(host: str, port: int, path: str, key: str,
                    body_bytes: bytes, timeout: float) -> dict:
    """The real wire: one POST, JSON in, JSON out. HTTP >= 400, socket
    errors, timeouts and undecodable bodies all raise TransportFailure."""
    conn = http.client.HTTPSConnection(host, port, timeout=timeout)
    try:
        conn.request("POST", path, body=body_bytes, headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        })
        resp = conn.getresponse()
        data = resp.read()
        if resp.status >= 400:
            raise TransportFailure(
                f"HTTP {resp.status}: {data[:200].decode('utf-8', 'replace')!r}")
        return json.loads(data)
    except TransportFailure:
        raise
    except (OSError, http.client.HTTPException, json.JSONDecodeError) as exc:
        raise TransportFailure(f"transport failed: {exc!r}") from exc
    finally:
        conn.close()


def make_jsonl_bank(path: Path):
    """The usage ledger (the driving-ladder law: every paid dispatch banks
    its burn). Returns a bank(row) callable appending one JSON row per
    fire, creating parent dirs."""
    path = Path(path)

    def bank(row: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    return bank


def _content_chars(messages: list[dict]) -> int:
    return sum(len(str(m.get("content") or "")) for m in messages)


def fire(model: str, messages: list[dict], key: str, *,
         endpoint: str = DEFAULT_ENDPOINT, requested_max_tokens: int | None = None,
         prompt_chars: int | None = None, bank=None, ask_dir=None,
         ask_id: str = "ask", pricing: tuple | None = None,
         transport=None, timeout: float = 900.0, retries: int = 1,
         retry_sleep: float = 20.0) -> dict:
    """One guarded fire: plan_call -> fence -> http.client -> guard_terminal.

    bank is REQUIRED (a usage ledger is the budget law made visible; pass
    make_jsonl_bank(path) or your own callable). ask_dir is REQUIRED: the
    EMPTY_REASONING terminal marker lives there. transport is injectable
    for tests (same signature as https_post_json); with the default
    transport and no operator key this raises before any network use.
    """
    if not key:
        raise RuntimeError("no API key: refusing to fire (no live spend "
                           "without an operator key)")
    if bank is None:
        raise RuntimeError("bank is required: every paid dispatch banks its "
                           "burn (pass make_jsonl_bank(path))")
    if ask_dir is None:
        raise RuntimeError("ask_dir is required: the EMPTY_REASONING terminal "
                           "marker must have a home")
    price = pricing or PRICING.get(model)
    if price is None:
        raise ValueError(f"unknown model {model}; add pricing first")
    host, port, path = fence_endpoint(endpoint)
    skip = skip_terminal(ask_dir, ask_id)
    if skip is not None:
        return skip
    if prompt_chars is None:
        prompt_chars = _content_chars(messages)
    # LAW 1: plan before every fire, and the plan rides the wire unmodified.
    plan = plan_call(model=model, prompt_chars=prompt_chars,
                     requested_max_tokens=requested_max_tokens)
    body_bytes = json.dumps(build_body(plan, model, messages)).encode("utf-8")
    send = transport or https_post_json
    resp = None
    last_exc: TransportFailure | None = None
    for attempt in range(retries + 1):
        try:
            resp = send(host, port, path, key, body_bytes, timeout)
            break
        except TransportFailure as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(retry_sleep)
    if resp is None:
        # bank the transport failure as data (turn: None, ok: false) so the
        # wall is visible in the ledger (the 402-wall lesson: failures that
        # bank nothing can never go terminal)
        bank({"ts": _now(), "id": ask_id, "model": model, "turn": None,
              "transport_error": str(last_exc)[:200], "cost_usd": 0.0,
              "ok": False})
        raise last_exc
    usage = resp.get("usage", {})
    choice = (resp.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    pin, pout = int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)
    cin, cout = price
    cost = pin * cin + pout * cout
    raw_content, finish_reason = msg.get("content"), choice.get("finish_reason")
    # LAW 2: guard_terminal on EVERY response, before any salvage.
    cause = guard_terminal(ask_dir, ask_id, plan.recipe_key, finish_reason,
                           usage, raw_content, bank, model=model,
                           family=plan.recipe_key, base_url=endpoint,
                           pin=pin, pout=pout, cost=cost)
    if cause:
        raise TerminalEmpty(cause)
    content, chan = raw_content, "content"
    if not content:
        content = msg.get("reasoning") or ""
        chan = "reasoning (content channel empty)"
    if not content:
        refusal = msg.get("refusal")
        if refusal:
            bank({"ts": _now(), "id": ask_id, "model": model,
                  "refused": str(refusal)[:200], "prompt_tokens": pin,
                  "completion_tokens": pout, "cost_usd": round(cost, 4),
                  "ok": False})
            raise Refused(str(refusal)[:200])
        raise RuntimeError("empty response: both content and reasoning "
                           f"channels empty; usage={usage}")
    chars = len(str(content).strip())
    # the substance gate: hollow rows bank ok=false (1-char content is the
    # re-fire signature the carrier paid to learn)
    bank({"ts": _now(), "id": ask_id, "model": model, "turn": 1,
          "prompt_tokens": pin, "completion_tokens": pout,
          "reasoning_tokens": _reasoning_tokens(usage),
          "channel": chan, "content_chars": chars,
          "finish_reason": finish_reason, "cost_usd": round(cost, 4),
          "ok": chars > 1})
    return {"ok": chars > 1, "id": ask_id, "model": model,
            "recipe_key": plan.recipe_key, "shape": plan.shape,
            "max_tokens": plan.max_tokens, "finish_reason": finish_reason,
            "channel": chan, "content": content, "content_chars": chars,
            "cost_usd": round(cost, 4), "usage": usage,
            "plan_notes": list(plan.notes)}
