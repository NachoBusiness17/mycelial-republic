"""Tests for mag.claritas routing: the mask must be byte-honest (2026-10-01).

The G2 cross-family law (watch/inbox/model_garden/WARMED_CONTEXT.md law 7) needs
same-mask-different-families to be TRUE, so face_for must attribute every garden
family to its real face instead of leaking the neutral house contract (kimi,
qwen-prime had no matcher at all) or a wrong vendor's face (local gemma janitors
received the GEMINI face). Fixes verified here, all from the WARMED_CONTEXT
PART 2 census probes:

1. kimi ids route to the kimi face (was: neutral fallback, no vendor attribution)
2. qwen ids route to the qwen face (was: neutral fallback, no vendor attribution)
3. bare fable-5.1 (no anthropic/ prefix) routes to the anthropic face (was: neutral)
4. local gemma ids route to the local ollama face, NOT gemini, while hosted
   google/-prefixed gemma keeps the gemini face
5. the ollama face is reachable (was dead code: FACES carried it, no matcher),
   enforced forward by the no-dead-face-keys invariant below

Face content sources: memory/behavioral/animals/moonshotai_kimi_k2.jsonl (terse,
byte-exact format law, zero refusals), qwen_qwen3_8_max_prime.jsonl (structure
converts on depth shapes, raw volume does not), gemma_2b.jsonl +
gemma2_2b_instruct_q5_k_m.jsonl + gemma4_latest.jsonl (ramble, praise-slop, hedge
lectures: the direct-and-compact ollama face is the counter-shape).
"""
from __future__ import annotations

from mag import claritas
from mag.claritas import FACES, FACE_NEUTRAL, _MATCHERS, face_for, vendor_for


def test_kimi_family_routes_to_kimi_face():
    for mid in ("moonshotai/kimi-k2", "kimi", "moonshot/kimi-k2-thinking"):
        assert vendor_for(mid) == "kimi", mid
        assert face_for(mid) == FACES["kimi"], mid
        assert face_for(mid) != FACE_NEUTRAL, mid


def test_qwen_ids_route_to_qwen_face():
    for mid in ("qwen/qwen3.8-max-prime", "qwen3.8-max-prime", "qwen-flash",
                "qwen3.7-flash"):
        assert vendor_for(mid) == "qwen", mid
        assert face_for(mid) == FACES["qwen"], mid
        assert face_for(mid) != FACE_NEUTRAL, mid


def test_bare_fable_routes_to_anthropic_face():
    # The prefixed id always worked via the "claude" substring; the bare family
    # name used to fall to neutral (WARMED_CONTEXT PART 2, fable row).
    for mid in ("fable-5.1", "anthropic/claude-fable-5.1", "claude-fable-5.1"):
        assert vendor_for(mid) == "anthropic", mid
        assert face_for(mid) == FACES["anthropic"], mid


def test_local_gemma_routes_to_ollama_face_not_gemini():
    # The estate's local ollama janitors (AGENTS.md: gemma:2b scut, gemma4 short
    # worker; garden grid also ran gemma2:2b-instruct-q5_K_M).
    for mid in ("gemma:2b", "gemma2:2b-instruct-q5_K_M", "gemma4:latest", "gemma4"):
        assert vendor_for(mid) == "ollama", mid
        assert face_for(mid) == FACES["ollama"], mid
        assert face_for(mid) != FACES["gemini"], mid


def test_hosted_gemma_stays_gemini():
    # google/ wins over the local gemma matchers; non-colon hosted-style gemma ids
    # keep the old gemini attribution.
    for mid in ("google/gemma-3-27b-it", "google/gemma-2-9b-it", "gemini-3.8-flash"):
        assert vendor_for(mid) == "gemini", mid
        assert face_for(mid) == FACES["gemini"], mid


def test_ollama_face_is_reachable():
    # Dead-face guard: FACES keys with no matcher routing to them are wiring debt.
    wired = {vendor for _, vendor in _MATCHERS}
    for vendor in FACES:
        assert vendor in wired, f"dead face key, no matcher routes to it: {vendor}"
    assert any(vendor_for(mid) == "ollama" for mid in
               ("gemma:2b", "gemma4:latest")), "ollama face unreachable"


def test_faceless_by_design_families_stay_neutral():
    # zai and deepseek map to the neutral house contract on purpose (WARMED_CONTEXT
    # PART 2: MATCHED, faceless BY DESIGN); the new matchers must not disturb that.
    for mid in ("glm-5.3-flash", "z-ai/glm-5.3-flash", "deepseek/deepseek-v4-flash",
                "deepseek-v4.1-flash"):
        assert face_for(mid) == FACE_NEUTRAL, mid


def test_unknown_id_falls_back_to_neutral():
    assert vendor_for("totally-unknown-model") == "neutral"
    assert face_for("totally-unknown-model") == FACE_NEUTRAL
    assert face_for("") == FACE_NEUTRAL


def test_garden_families_get_distinct_faces():
    # The G2 instrument: each probed garden family must resolve to a face, and the
    # families the census holds distinct must stay distinct (grok, anthropic,
    # gemini, kimi, qwen, ollama/local all differ from neutral and each other).
    garden = {
        "x-ai/grok-4.7": claritas.FACES["grok"],
        "anthropic/claude-sonnet-5.5": claritas.FACES["anthropic"],
        "anthropic/claude-fable-5.1": claritas.FACES["anthropic"],
        "moonshotai/kimi-k2": claritas.FACES["kimi"],
        "qwen/qwen3.8-max-prime": claritas.FACES["qwen"],
        "google/gemma-3-27b-it": claritas.FACES["gemini"],
        "gemma:2b": claritas.FACES["ollama"],
    }
    for mid, expected in garden.items():
        assert face_for(mid) == expected, mid
    distinct = set(garden.values())
    assert FACE_NEUTRAL not in distinct
    assert len(distinct) == len(garden) - 1  # anthropic pair shares one face
